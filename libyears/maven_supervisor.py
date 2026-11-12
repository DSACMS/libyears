"""One isolated scan-wide Maven metadata batch, with bounded cancellation."""

from datetime import datetime, timezone
import os
import stat
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

from .maven import MavenCapability
from .maven_model import MavenReason
from .maven_protocol import (
    MAX_ATTEMPTS, MAX_BYTES, available, command, read_message, result, timestamp, write_message,
)
from .maven_registry import (
    MAX_CATALOGUE_BYTES, MAX_POM_BYTES, MavenPomDate, MavenTarget, pom_path,
)

COMMAND_SECONDS = 10.0
GA_SECONDS = 60.0
SCAN_SECONDS = 300.0
CLEANUP_SECONDS = 0.5
READY_SECONDS = 10.0
_DEFERRED = []


class MavenWorkerFailure(RuntimeError):
    def __init__(self):
        super().__init__('Maven metadata worker unavailable')


class MavenSupervisor:
    def __init__(self, capabilities, *, ca_bundle=None, clock=time.monotonic,
                 pause=time.sleep, process_factory=subprocess.Popen):
        self.capabilities = frozenset(capabilities)
        for capability in self.capabilities:
            if type(capability) is not MavenCapability:
                raise ValueError('Maven capability')
            pom_path(capability.group_id, capability.artifact_id, capability.version)
        self.measured = {(c.group_id, c.artifact_id, c.version) for c in self.capabilities}
        self.gas = {(c.group_id, c.artifact_id) for c in self.capabilities}
        self.clock = clock
        self.pause = pause
        self.process_factory = process_factory
        self.ca_bundle = ca_bundle
        self.started = clock()
        self.ga_started = {}
        self.sequence = 0
        self.attempts = 0
        self.body_bytes = 0
        self.targets = {}
        self.cache = {}
        self.process = None
        self.directory = None
        self.cancelled = False
        self.closed = False

    def _start(self):
        if not available() or _DEFERRED:
            raise MavenWorkerFailure()
        self.directory = Path(tempfile.mkdtemp(prefix='libyears-maven-'))
        if self.ca_bundle is not None:
            # Only an explicitly supplied TLS override is copied, never host Maven config.
            info = os.stat(self.ca_bundle, follow_symlinks=False)
            if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 4 * 1024 * 1024:
                raise MavenWorkerFailure()
            identity = (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)
            descriptor = os.open(self.ca_bundle, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            with os.fdopen(descriptor, 'rb') as stream:
                opened = os.fstat(stream.fileno())
                body = stream.read(4 * 1024 * 1024 + 1)
                final = os.fstat(stream.fileno())
            current = os.stat(self.ca_bundle, follow_symlinks=False)
            for item in (opened, final, current):
                if (not stat.S_ISREG(item.st_mode)
                        or (item.st_dev, item.st_ino, item.st_size, item.st_mtime_ns, item.st_ctime_ns) != identity):
                    raise MavenWorkerFailure()
            if len(body) != info.st_size:
                raise MavenWorkerFailure()
            trust = self.directory / 'trust.pem'
            trust.write_bytes(body)
            trust.chmod(0o600)
        entry = Path(__file__).with_name('maven_worker.py').resolve()
        self.process = self.process_factory(
            [str(Path(sys.executable).resolve()), '-I', str(entry)], shell=False,
            cwd=str(self.directory), env={}, close_fds=True,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cutoff = min(self.clock() + READY_SECONDS, self.started + SCAN_SECONDS)
        self._await(self.directory / 'ready.json', cutoff)
        ready = read_message(self.directory / 'ready.json')
        if set(ready) != {'ready'} or type(ready['ready']) is not int or ready['ready'] != 1:
            raise MavenWorkerFailure()

    def _await(self, path, deadline):
        while self.clock() < deadline:
            if path.exists():
                return
            if self.process.poll() is not None:
                raise MavenWorkerFailure()
            self.pause(min(0.01, max(0, deadline - self.clock())))
        raise MavenWorkerFailure()

    def select_target(self, capability):
        if capability not in self.capabilities:
            raise ValueError('Maven capability')
        return self._lookup('select_target', capability.group_id, capability.artifact_id, None)

    def pom_date(self, capability, version=None):
        if capability not in self.capabilities:
            raise ValueError('Maven capability')
        version = capability.version if version is None else version
        ga = (capability.group_id, capability.artifact_id)
        if (ga[0], ga[1], version) not in self.measured and self.targets.get(ga) != version:
            raise ValueError('Maven capability')
        return self._lookup('pom_date', *ga, version)

    @staticmethod
    def _failure(operation, group, artifact, version, reason):
        retrieved = datetime.now(timezone.utc)
        if operation == 'select_target':
            return MavenTarget(group, artifact, None, retrieved, reason)
        return MavenPomDate(group, artifact, version, None, retrieved, reason)

    def _lookup(self, operation, group, artifact, version):
        key = (operation, group, artifact, version)
        if key in self.cache:
            return self.cache[key]
        reason = MavenReason.METADATA_WORKER_UNAVAILABLE
        if self.closed or self.cancelled:
            return self._failure(operation, group, artifact, version, reason)
        now = self.clock()
        ga = (group, artifact)
        self.ga_started.setdefault(ga, now)
        if (now >= self.started + SCAN_SECONDS or now >= self.ga_started[ga] + GA_SECONDS
                or self.attempts >= MAX_ATTEMPTS or self.body_bytes >= MAX_BYTES):
            failed = self._failure(operation, group, artifact, version, MavenReason.METADATA_BUDGET_EXCEEDED)
            self.cache[key] = failed
            return failed
        try:
            if self.process is None:
                self._start()
            deadline = min(self.clock() + COMMAND_SECONDS, self.started + SCAN_SECONDS,
                           self.ga_started[ga] + GA_SECONDS)
            # Reserve cleanup within the command's wall deadline.
            cutoff = deadline - CLEANUP_SECONDS
            if self.clock() >= cutoff:
                raise MavenWorkerFailure()
            self.sequence += 1
            request = command(dict(sequence=self.sequence, operation=operation, group_id=group,
                                   artifact_id=artifact, version=version, deadline=cutoff))
            wall_started = datetime.now(timezone.utc)
            write_message(self.directory / f'command-{self.sequence}.json', request)
            path = self.directory / f'result-{self.sequence}.json'
            self._await(path, cutoff)
            value = result(read_message(path), request)
            if (self.clock() >= cutoff or value['attempts'] != self.attempts + 1
                    or value['body_bytes'] < self.body_bytes
                    or value['body_bytes'] - self.body_bytes > (
                        MAX_CATALOGUE_BYTES + 1 if operation == 'select_target' else MAX_POM_BYTES + 1)
                    or not wall_started <= timestamp(value['retrieved_at']) <= datetime.now(timezone.utc)):
                raise MavenWorkerFailure()
            self.attempts = value['attempts']
            self.body_bytes = value['body_bytes']
            failure = MavenReason(value['reason']) if value['reason'] is not None else None
            retrieved = timestamp(value['retrieved_at'])
            if operation == 'select_target':
                parsed = MavenTarget(group, artifact, value['selected_version'], retrieved, failure)
                if parsed.version is not None:
                    self.targets[ga] = parsed.version
            else:
                modified = timestamp(value['last_modified']) if value['last_modified'] is not None else None
                parsed = MavenPomDate(group, artifact, version, modified, retrieved, failure)
            self.cache[key] = parsed
            return parsed
        except (OSError, ValueError, RecursionError, MavenWorkerFailure):
            self.cancelled = True
            self.close()
            return self._failure(operation, group, artifact, version, reason)
        except BaseException:
            self.cancelled = True
            self.close()
            raise

    def close(self):
        self.closed = True
        process = self.process
        if process is not None and process.poll() is None:
            try:
                process.kill()
            except OSError:
                pass
        if process is not None:
            try:
                process.wait(timeout=CLEANUP_SECONDS)
            except (subprocess.TimeoutExpired, OSError):
                if self not in _DEFERRED:
                    _DEFERRED.append(self)
                return
        if self.directory is not None:
            try:
                shutil.rmtree(self.directory)
            except OSError:
                if self not in _DEFERRED:
                    _DEFERRED.append(self)
                return
            self.directory = None
        if self in _DEFERRED:
            _DEFERRED.remove(self)

    def reap_deferred(self):
        if self.process is not None and self.process.poll() is None:
            return False
        self.close()
        return self not in _DEFERRED

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        self.close()
