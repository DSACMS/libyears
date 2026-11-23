"""Bounded filename discovery and descriptor-bound local SBOM snapshots."""

import hashlib
import os
import stat

from .maven_input import (
    MavenInputFailure, directory_identity, file_identity, filesystem_available,
    relative_parts, reparse_point,
)
from .sbom_model import (
    SbomDiscovery, SbomFailure, SbomIntake, SbomRequest, SbomSelection, SbomSnapshot,
)

MAX_BYTES = 8 * 1024 * 1024
MAX_DEPTH = 3
MAX_DIRECTORIES = 128
MAX_ENTRIES = 10_000
MAX_CANDIDATES = 16
EXCLUDED_DIRECTORIES = frozenset({
    'node_modules', 'vendor', 'packages', 'venv', '__pycache__', 'bin', 'obj',
})


def _parts(name):
    try:
        return relative_parts(name)
    except MavenInputFailure:
        raise SbomFailure('sbom_input_unsafe') from None


def _matches(name):
    return name in ('bom.json', 'sbom.json') or name.endswith(('.cdx.json', '.cyclonedx.json'))


class SbomInputReader:
    """Single-use root anchor; never reads manifests, settings or other inputs."""

    def __init__(self, root):
        self.root = os.fspath(root)
        self.directory = None
        self._root_chain = []
        self._directory_ids = {}
        self._used = False
        self._candidates = {}

    @staticmethod
    def _flags():
        return os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_NONBLOCK

    def __enter__(self):
        if self._used:
            raise RuntimeError('SBOM reader is single-use')
        self._used = True
        if not filesystem_available():
            raise SbomFailure('sbom_input_unavailable')
        try:
            if self.root == '.':
                absolute = os.getcwd()
            elif self.root.startswith('/'):
                absolute = self.root
            else:
                _parts(self.root)
                absolute = os.getcwd() + '/' + self.root
            parts = _parts(absolute[1:]) if absolute != '/' else ()
            anchor = os.open('/', self._flags())
            try:
                info = os.fstat(anchor)
                if not stat.S_ISDIR(info.st_mode) or reparse_point(info):
                    raise SbomFailure('sbom_input_unsafe')
            except BaseException:
                os.close(anchor)
                raise
            self._root_chain.append((None, None, anchor, directory_identity(info)))
            parent = anchor
            for name in parts:
                child, identity = self._open_directory(parent, name)
                self._root_chain.append((parent, name, child, identity))
                parent = child
            self.directory = parent
            self._check_bindings([])
        except BaseException as error:
            self.__exit__()
            if isinstance(error, (OSError, ValueError, NotImplementedError)) and not isinstance(error, SbomFailure):
                raise SbomFailure('sbom_input_unavailable') from None
            raise
        return self

    def __exit__(self, *unused):
        for parent, name, descriptor, identity in reversed(self._root_chain):
            os.close(descriptor)
        self._root_chain.clear()
        self.directory = None

    def _open_directory(self, parent, name, expected=None):
        info = os.stat(name, dir_fd=parent, follow_symlinks=False)
        if not stat.S_ISDIR(info.st_mode) or reparse_point(info):
            raise SbomFailure('sbom_input_unsafe')
        if expected is not None and directory_identity(info) != expected:
            raise SbomFailure('sbom_input_changed')
        descriptor = os.open(name, self._flags(), dir_fd=parent)
        try:
            opened = os.fstat(descriptor)
            if reparse_point(opened) or directory_identity(opened) != directory_identity(info):
                raise SbomFailure('sbom_input_changed')
        except BaseException:
            os.close(descriptor)
            raise
        return descriptor, directory_identity(opened)

    def _check_bindings(self, bindings):
        for parent, name, descriptor, identity in self._root_chain + bindings:
            opened = os.fstat(descriptor)
            if reparse_point(opened) or directory_identity(opened) != identity:
                raise SbomFailure('sbom_input_changed')
            if parent is not None:
                current = os.stat(name, dir_fd=parent, follow_symlinks=False)
                if reparse_point(current) or directory_identity(current) != identity:
                    raise SbomFailure('sbom_input_changed')

    def discover(self):
        count = entries = directories = 0
        candidates = {}
        unsafe = False

        def visit(descriptor, relative, depth, bindings):
            nonlocal count, entries, directories, unsafe
            directories += 1
            if directories > MAX_DIRECTORIES:
                raise SbomFailure('sbom_budget_exceeded')
            self._check_bindings(bindings)
            before = os.fstat(descriptor)
            state = (directory_identity(before), before.st_mtime_ns, before.st_ctime_ns)
            names = []
            with os.scandir(descriptor) as iterator:
                for entry in iterator:
                    if entries >= MAX_ENTRIES:
                        raise SbomFailure('sbom_budget_exceeded')
                    entries += 1
                    if not entry.name.startswith('.') and _matches(entry.name):
                        count += 1
                        if count > MAX_CANDIDATES:
                            raise SbomFailure('sbom_budget_exceeded')
                    names.append(entry.name)
            for name in sorted(names):
                if name.startswith('.'):
                    continue
                source_id = relative + '/' + name if relative else name
                matching = _matches(name)
                _parts(source_id)
                self._check_bindings(bindings)
                info = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
                if matching:
                    if not stat.S_ISREG(info.st_mode) or reparse_point(info):
                        unsafe = True
                    else:
                        candidates[source_id] = file_identity(info)
                elif (name not in EXCLUDED_DIRECTORIES and stat.S_ISDIR(info.st_mode)
                      and not reparse_point(info) and depth < MAX_DEPTH):
                    if directories >= MAX_DIRECTORIES:
                        raise SbomFailure('sbom_budget_exceeded')
                    child, identity = self._open_directory(descriptor, name)
                    self._directory_ids[source_id] = identity
                    try:
                        visit(child, source_id, depth + 1,
                              bindings + [(descriptor, name, child, identity)])
                    finally:
                        os.close(child)
            self._check_bindings(bindings)
            after = os.fstat(descriptor)
            if state != (directory_identity(after), after.st_mtime_ns, after.st_ctime_ns):
                raise SbomFailure('sbom_input_changed')

        try:
            visit(self.directory, '', 0, [])
        except (SbomFailure, OSError, ValueError, NotImplementedError):
            return SbomDiscovery('automatic', 'incomplete', count, False,
                                 'sbom_discovery_unavailable'), ()
        self._candidates = candidates
        if unsafe:
            return SbomDiscovery('automatic', 'incomplete', count, False,
                                 'sbom_discovery_unavailable'), ()
        return SbomDiscovery('automatic', 'complete', count, True), tuple(sorted(candidates))

    def snapshot(self, source_id):
        parts = _parts(source_id)
        descriptors = []
        bindings = []
        file_descriptor = None
        try:
            self._check_bindings([])
            parent = self.directory
            for index, name in enumerate(parts[:-1]):
                prefix = '/'.join(parts[:index + 1])
                child, identity = self._open_directory(parent, name, self._directory_ids.get(prefix))
                descriptors.append(child)
                bindings.append((parent, name, child, identity))
                parent = child
            info = os.stat(parts[-1], dir_fd=parent, follow_symlinks=False)
            if not stat.S_ISREG(info.st_mode) or reparse_point(info):
                raise SbomFailure('sbom_input_unsafe')
            identity = file_identity(info)
            if source_id in self._candidates and identity != self._candidates[source_id]:
                raise SbomFailure('sbom_input_changed')
            if info.st_size > MAX_BYTES:
                raise SbomFailure('sbom_budget_exceeded')
            self._check_bindings(bindings)
            file_descriptor = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
            opened = os.fstat(file_descriptor)
            if reparse_point(opened) or file_identity(opened) != identity:
                raise SbomFailure('sbom_input_changed')
            chunks = []
            remaining = info.st_size
            while remaining:
                chunk = os.read(file_descriptor, min(remaining, 64 * 1024))
                if not chunk or len(chunk) > remaining:
                    raise SbomFailure('sbom_input_changed')
                chunks.append(chunk)
                remaining -= len(chunk)
            if os.read(file_descriptor, 1):
                raise SbomFailure('sbom_input_changed')
            self._check_bindings(bindings)
            current = os.stat(parts[-1], dir_fd=parent, follow_symlinks=False)
            if (reparse_point(current) or file_identity(current) != identity
                    or file_identity(os.fstat(file_descriptor)) != identity):
                raise SbomFailure('sbom_input_changed')
            data = b''.join(chunks)
            return SbomSnapshot(source_id, data, hashlib.sha256(data).hexdigest())
        except SbomFailure:
            raise
        except (OSError, ValueError, NotImplementedError):
            raise SbomFailure('sbom_input_unavailable') from None
        finally:
            if file_descriptor is not None:
                os.close(file_descriptor)
            for descriptor in reversed(descriptors):
                os.close(descriptor)


def intake_sbom(root, request=SbomRequest(), *, reader_factory=SbomInputReader):
    """Library selection seam; disabled and complete absence return no section."""
    if request.disabled:
        return None
    explicit = request.source_id is not None
    mode = 'explicit' if explicit else 'automatic'
    discovery = SbomDiscovery(mode, 'bypassed' if explicit else 'incomplete',
                              None if explicit else 0, None if explicit else False,
                              None if explicit else 'sbom_discovery_unavailable')
    selection = SbomSelection(mode, 'selected' if explicit else 'unavailable', request.source_id)
    try:
        with reader_factory(root) as reader:
            if not explicit:
                discovery, candidates = reader.discover()
                if not discovery.search_complete:
                    return SbomIntake(discovery, selection, reason='sbom_discovery_unavailable')
                if not candidates:
                    return None
                if len(candidates) > 1:
                    return SbomIntake(discovery, SbomSelection(mode, 'required'),
                                      reason='sbom_selection_required')
                selection = SbomSelection(mode, 'selected', candidates[0])
            snapshot = reader.snapshot(selection.source_id)
            return SbomIntake(discovery, selection, snapshot)
    except SbomFailure as failure:
        reason = failure.reason if explicit or selection.source_id else 'sbom_discovery_unavailable'
        return SbomIntake(discovery, selection, reason=reason)
