"""Private NuGet process controller; no target paths or synchronous fallback."""

import base64
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time

from .model import NuGetPublication
from .nuget_provenance import LocalAuthority
from .nuget_version import parse_selected_identity

PROTOCOL_LIMIT = 16 * 1024
PACKAGE_SECONDS = 60.0
SCAN_SECONDS = 300.0
CLEANUP_SECONDS = 0.5
READY_SECONDS = 10.0
POLL_SECONDS = 0.01
# Retain OS handles and paths until a caller can perform a nonblocking reap.
_DEFERRED = []
REASONS = frozenset({'registry_error', 'invalid_registry_response',
                     'package_not_found', 'version_not_found', 'no_stable_release',
                     'content_hash_unavailable', 'content_hash_mismatch',
                     'release_date_missing'})


class NuGetWorkerFailure(RuntimeError):
    """Safe systemic failure, including startup or an unreaped process."""

    def __init__(self):
        super().__init__('NuGet worker unavailable')


@dataclass(frozen=True)
class PackageResult:
    reason: str | None = None
    origin_state: str = 'asserted_public'
    content_hash_state: str = 'local_agreement'
    used_publication: NuGetPublication | None = None
    latest_publication: NuGetPublication | None = None
    namespace_basis: str = 'accepted_producer_origin'


def write_message(path, value):
    body = json.dumps(value, allow_nan=False, separators=(',', ':')).encode('utf-8')
    if len(body) > PROTOCOL_LIMIT:
        raise ValueError('protocol')
    temporary = path.with_suffix('.tmp')
    with temporary.open('xb') as stream:
        stream.write(body)
    os.replace(temporary, path)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('protocol')
        result[key] = value
    return result


def _invalid_constant(unused):
    raise ValueError('protocol')


def read_message(path):
    # Open only completed regular files; never follow a replaced symlink or FIFO.
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > PROTOCOL_LIMIT:
        raise ValueError('protocol')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    descriptor = os.open(path, flags)
    with os.fdopen(descriptor, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        if (not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino)):
            raise ValueError('protocol')
        body = stream.read(PROTOCOL_LIMIT + 1)
    if len(body) > PROTOCOL_LIMIT:
        raise ValueError('protocol')
    value = json.loads(body, object_pairs_hook=_pairs,
                       parse_constant=_invalid_constant)
    if not isinstance(value, dict):
        raise ValueError('protocol')
    return value


def authority_message(authority):
    if not isinstance(authority, LocalAuthority):
        raise ValueError('authority')
    value = {'project_sha256': authority.project_sha256,
             'lock_sha256': authority.lock_sha256,
             'package_key': authority.package_key,
             'normalized_version': authority.normalized_version,
             'content_hash': (base64.b64encode(authority.content_hash).decode('ascii')
                              if authority.content_hash is not None else None),
             'namespace_basis': authority.namespace_basis,
             'local_content_state': authority.local_content_state}
    decode_authority(value)
    return value


def decode_authority(value):
    fields = {'project_sha256', 'lock_sha256', 'package_key',
              'normalized_version', 'content_hash', 'namespace_basis', 'local_content_state'}
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError('authority')
    if any(not isinstance(value[key], str) for key in fields - {'content_hash'}):
        raise ValueError('authority')
    if any(not re.fullmatch('[0-9a-f]{64}', value[key])
           for key in ('project_sha256', 'lock_sha256')):
        raise ValueError('authority')
    if not re.fullmatch('[a-z0-9][a-z0-9._-]{0,99}', value['package_key']):
        raise ValueError('authority')
    identity = parse_selected_identity(value['normalized_version'])
    if identity is None or identity.normalized_version != value['normalized_version']:
        raise ValueError('authority')
    basis = value['namespace_basis']
    state = value['local_content_state']
    if basis not in ('accepted_producer_origin', 'accepted_snapshot_namespace'):
        raise ValueError('authority')
    if state not in ('local_agreement', 'mismatch', 'unavailable'):
        raise ValueError('authority')
    digest = None
    if value['content_hash'] is not None:
        if not isinstance(value['content_hash'], str):
            raise ValueError('authority')
        digest = base64.b64decode(value['content_hash'], validate=True)
        if len(digest) != 64:
            raise ValueError('authority')
    if (state == 'local_agreement') != (digest is not None):
        raise ValueError('authority')
    if basis == 'accepted_snapshot_namespace' and state != 'unavailable':
        raise ValueError('authority')
    return LocalAuthority(value['project_sha256'], value['lock_sha256'],
                          value['package_key'], value['normalized_version'], digest, basis, state)


def failed_package(authority, reason='registry_error'):
    """Failure cannot manufacture producer or content facts for a weaker input."""
    origin = ('asserted_public' if authority.namespace_basis == 'accepted_producer_origin'
              else 'unavailable')
    return PackageResult(reason=reason, origin_state=origin,
                         content_hash_state=authority.local_content_state,
                         namespace_basis=authority.namespace_basis)


def _publication(value):
    if not isinstance(value, dict) or set(value) != {'version', 'created', 'listed'}:
        raise ValueError('protocol')
    text = value['version']
    identity = parse_selected_identity(text) if isinstance(text, str) else None
    if identity is None or identity.normalized_version != text or type(value['listed']) is not bool:
        raise ValueError('protocol')
    created = value['created']
    if not isinstance(created, str) or not re.fullmatch(
            r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z', created):
        raise ValueError('protocol')
    date = datetime.fromisoformat(created.replace('Z', '+00:00'))
    if date.year == 1900:
        raise ValueError('protocol')
    return NuGetPublication(text, date, value['listed'])


def decode_result(value):
    fields = {'reason', 'origin_state', 'content_hash_state',
              'used_publication', 'latest_publication', 'namespace_basis'}
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError('protocol')
    if value['reason'] is not None and (not isinstance(value['reason'], str) or value['reason'] not in REASONS):
        raise ValueError('protocol')
    basis = value['namespace_basis']
    if basis not in ('accepted_producer_origin', 'accepted_snapshot_namespace'):
        raise ValueError('protocol')
    origins = (('unavailable',) if basis == 'accepted_snapshot_namespace'
               else ('asserted_public', 'public_content_verified'))
    if value['origin_state'] not in origins:
        raise ValueError('protocol')
    if value['content_hash_state'] not in ('local_agreement', 'unavailable', 'mismatch', 'public_agreement'):
        raise ValueError('protocol')
    verified = value['origin_state'] == 'public_content_verified'
    if basis == 'accepted_snapshot_namespace' and value['content_hash_state'] != 'unavailable':
        raise ValueError('protocol')
    if verified != (value['content_hash_state'] == 'public_agreement'):
        raise ValueError('protocol')
    publications = {}
    for key in ('used_publication', 'latest_publication'):
        publications[key] = _publication(value[key]) if value[key] is not None else None
    if value['reason'] is None and any(v is None for v in publications.values()):
        raise ValueError('protocol')
    return PackageResult(value['reason'], value['origin_state'], value['content_hash_state'],
                         namespace_basis=basis, **publications)


def result_message(result):
    if not isinstance(result, PackageResult):
        raise ValueError('protocol')
    value = {'reason': result.reason, 'origin_state': result.origin_state,
             'content_hash_state': result.content_hash_state, 'namespace_basis': result.namespace_basis}
    for key in ('used_publication', 'latest_publication'):
        publication = getattr(result, key)
        value[key] = None if publication is None else {
            'version': publication.version,
            'created': publication.created.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'listed': publication.listed}
    decode_result(value)
    return value


class NuGetSupervisor:
    """One sequential scan; cancellation permanently suppresses further work.

    worker_entry is a trusted internal testing seam, never user/target input.
    The clock, pause and process factory permit deterministic controller tests.
    """

    def __init__(self, *, worker_entry=None, clock=time.monotonic,
                 pause=time.sleep, process_factory=subprocess.Popen):
        self.clock = clock
        self.pause = pause
        self.process_factory = process_factory
        self.worker_entry = Path(worker_entry or Path(__file__).with_name('nuget_worker.py')).resolve()
        self.directory = None
        self.process = None
        self.scan_deadline = None
        self.cancelled = False
        self.closed = False
        self.sequence = 0

    def _start(self):
        try:
            self.directory = tempfile.mkdtemp(prefix='libyears-nuget-')
            self.path = Path(self.directory)
            self.process = self.process_factory(
                [str(Path(sys.executable).resolve()), '-I', str(self.worker_entry)], shell=False,
                cwd=str(self.path), stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            deadline = self.clock() + READY_SECONDS
            while True:
                if self.clock() >= deadline:
                    raise NuGetWorkerFailure()
                ready = self.path / 'ready.json'
                if ready.exists():
                    value = read_message(ready)
                    if (set(value) != {'ready'} or type(value['ready']) is not int
                            or value['ready'] != 1 or self.clock() >= deadline):
                        raise NuGetWorkerFailure()
                    return
                if self.process.poll() is not None:
                    raise NuGetWorkerFailure()
                self.pause(min(POLL_SECONDS, deadline - self.clock()))
        except BaseException as failure:
            self.cancelled = True
            self._cleanup(self.clock() + CLEANUP_SECONDS)
            if isinstance(failure, (KeyboardInterrupt, SystemExit)):
                raise
            raise NuGetWorkerFailure() from None

    def lookup(self, authority):
        facts = authority_message(authority)
        if self.closed or self.cancelled:
            return failed_package(authority)
        if self.process is None:
            self._start()
        now = self.clock()
        if self.scan_deadline is None:
            self.scan_deadline = now + SCAN_SECONDS
        deadline = min(now + PACKAGE_SECONDS, self.scan_deadline)
        cutoff = deadline - CLEANUP_SECONDS
        try:
            if now >= cutoff:
                self._cancel(deadline)
                return failed_package(authority)
            self.sequence += 1
            write_message(self.path / 'command.json', {
                'sequence': self.sequence, 'authority': facts,
                'package_deadline': cutoff,
                'scan_deadline': self.scan_deadline - CLEANUP_SECONDS})
            while self.clock() < cutoff:
                result_path = self.path / 'result.json'
                if result_path.exists():
                    value = read_message(result_path)
                    if set(value) != {'sequence', 'result'} or type(value['sequence']) is not int or value['sequence'] != self.sequence:
                        raise ValueError('protocol')
                    result = decode_result(value['result'])
                    if result.namespace_basis != authority.namespace_basis:
                        raise ValueError('protocol')
                    if (result.origin_state == 'public_content_verified'
                            and authority.local_content_state != 'local_agreement'):
                        raise ValueError('protocol')
                    if (authority.local_content_state != 'local_agreement'
                            and result.content_hash_state != authority.local_content_state):
                        raise ValueError('protocol')
                    if (result.used_publication is not None
                            and result.used_publication.version != authority.normalized_version):
                        raise ValueError('protocol')
                    if self.clock() >= cutoff:
                        break
                    result_path.unlink()
                    return result
                if self.process.poll() is not None:
                    raise ValueError('protocol')
                self.pause(min(POLL_SECONDS, max(0, cutoff - self.clock())))
            self._cancel(deadline)
            return failed_package(authority)
        except (OSError, ValueError, RecursionError):
            self._cancel(min(deadline, self.clock() + CLEANUP_SECONDS))
            return failed_package(authority)
        except BaseException:
            self._cancel(min(deadline, self.clock() + CLEANUP_SECONDS))
            raise

    def _cancel(self, deadline):
        self.cancelled = True
        self._cleanup(deadline)

    def _cleanup(self, deadline):
        self.closed = True
        process = self.process
        if process is not None:
            if process.poll() is None:
                try:
                    process.terminate()
                except OSError:
                    pass
                try:
                    process.wait(timeout=max(0, min(0.25, deadline - self.clock())))
                except (subprocess.TimeoutExpired, OSError):
                    pass
            if process.poll() is None:
                try:
                    process.kill()
                except OSError:
                    pass
            try:
                process.wait(timeout=max(0, deadline - self.clock()))
            except (subprocess.TimeoutExpired, OSError):
                # Keep process and directory alive for a later nonblocking reap.
                if self not in _DEFERRED:
                    _DEFERRED.append(self)
                raise NuGetWorkerFailure() from None
        if process is not None:
            for name in ('stdin', 'stdout', 'stderr'):
                stream = getattr(process, name, None)
                if stream is not None:
                    stream.close()
            # Popen has no public close operation for its Windows process handle.
            # Release it after wait has cached returncode; poll remains usable.
            handle = getattr(process, '_handle', None)
            if handle is not None:
                handle.Close()
        if self.directory is not None:
            try:
                shutil.rmtree(self.directory)
            except OSError:
                raise NuGetWorkerFailure() from None
            self.directory = None
        if self in _DEFERRED:
            _DEFERRED.remove(self)

    def reap_deferred(self):
        """Never wait on an unreaped OS process; delete only once exit is observed."""
        self._cleanup(self.clock())

    def close(self):
        if self.directory is None:
            self.closed = True
            return
        deadline = self.clock() + CLEANUP_SECONDS
        if self.scan_deadline is not None:
            deadline = min(deadline, self.scan_deadline)
        self._cleanup(deadline)
