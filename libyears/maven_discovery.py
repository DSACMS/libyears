"""Bounded filename inventory only; never dependency population or POM semantics."""

from dataclasses import dataclass
import os
import stat

from .maven_input import (
    MavenInputFailure, MavenInputIssue, MavenInputReader, directory_identity,
    file_identity, relative_parts, reparse_point,
)
from .maven_model import MavenDiscovery, MavenReason

MAX_DEPTH = 4
MAX_DIRECTORIES = 256
MAX_ENTRIES = 10_000
MAX_POMS = 100
EXCLUDED_DIRECTORIES = frozenset({
    'bin', 'obj', 'node_modules', 'packages', 'vendor', 'venv', '__pycache__',
    'target', 'build',
})


@dataclass(frozen=True, slots=True)
class MavenCandidate:
    source_id: str
    identity: tuple | None
    issue: MavenInputIssue | None = None


@dataclass(frozen=True, slots=True)
class MavenInventory:
    discovery: MavenDiscovery
    candidates: tuple[MavenCandidate, ...] = ()
    issue: MavenInputIssue | None = None


def discover_maven_candidates(root) -> MavenInventory:
    """Convenience filename inventory; content reads require the scoped reader."""
    try:
        with MavenInputReader(root) as reader:
            return reader.inventory()
    except MavenInputFailure as failure:
        if failure.issue == MavenInputIssue.NOT_DIRECTORY:
            return MavenInventory(MavenDiscovery(True))
        return MavenInventory(
            MavenDiscovery(False, (), MavenReason.DISCOVERY_UNAVAILABLE), issue=failure.issue,
        )


def inventory_reader(reader: MavenInputReader) -> MavenInventory:
    if reader._inventoried:
        raise RuntimeError('Maven inventory already established')
    candidates = []
    accepted = {}
    incomplete = False
    issue = None
    directories = 0
    entries = 0
    pom_count = 0

    def directory_state(descriptor):
        info = os.fstat(descriptor)
        return (*directory_identity(info), info.st_mtime_ns, info.st_ctime_ns)

    def visit(descriptor, relative, depth, bindings):
        nonlocal directories, entries, pom_count, incomplete, issue
        directories += 1
        if directories > MAX_DIRECTORIES:
            raise MavenInputFailure(MavenInputIssue.LIMIT)
        reader._check_bindings(bindings)
        before = directory_state(descriptor)
        names = []
        with os.scandir(descriptor) as iterator:
            for entry in iterator:
                entries += 1
                if entries > MAX_ENTRIES:
                    raise MavenInputFailure(MavenInputIssue.LIMIT)
                names.append(entry.name)
        reader._check_bindings(bindings)
        for name in sorted(names):
            # Exclusions are part of the supported projection, not unread sources.
            if name.startswith('.') or name in EXCLUDED_DIRECTORIES:
                continue
            source_id = relative + '/' + name if relative else name
            if name == 'pom.xml':
                # A refused metadata probe still consumed a candidate slot.
                if pom_count >= MAX_POMS:
                    raise MavenInputFailure(MavenInputIssue.LIMIT)
                pom_count += 1
            try:
                relative_parts(source_id)
                reader._check_bindings(bindings)
                info = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
                if name == 'pom.xml':
                    if not stat.S_ISREG(info.st_mode) or reparse_point(info):
                        candidates.append(MavenCandidate(source_id, None, MavenInputIssue.UNSAFE))
                        incomplete = True
                        issue = MavenInputIssue.UNSAFE
                    else:
                        accepted[source_id] = file_identity(info)
                        candidates.append(MavenCandidate(source_id, file_identity(info)))
                elif stat.S_ISDIR(info.st_mode) and not reparse_point(info) and depth < MAX_DEPTH:
                    if directories >= MAX_DIRECTORIES:
                        raise MavenInputFailure(MavenInputIssue.LIMIT)
                    child, identity = reader.open_child(descriptor, name, source_id)
                    try:
                        visit(child, source_id, depth + 1,
                              bindings + [(descriptor, name, child, identity)])
                    finally:
                        os.close(child)
            except MavenInputFailure as failure:
                if failure.issue == MavenInputIssue.LIMIT:
                    raise
                incomplete = True
                issue = failure.issue
                if name == 'pom.xml':
                    candidates.append(MavenCandidate(source_id, None, failure.issue))
            except (OSError, ValueError, NotImplementedError):
                incomplete = True
                issue = MavenInputIssue.IO
                if name == 'pom.xml':
                    candidates.append(MavenCandidate(source_id, None, MavenInputIssue.IO))
        reader._check_bindings(bindings)
        if before != directory_state(descriptor):
            raise MavenInputFailure(MavenInputIssue.CHANGED)

    try:
        visit(reader.directory, '', 0, [])
    except MavenInputFailure as failure:
        incomplete = True
        issue = failure.issue
    except (OSError, ValueError, NotImplementedError):
        incomplete = True
        issue = MavenInputIssue.IO
    reader._register(accepted)
    source_ids = tuple(sorted(accepted))
    discovery = MavenDiscovery(not incomplete, source_ids,
                               MavenReason.DISCOVERY_UNAVAILABLE if incomplete else None)
    return MavenInventory(discovery, tuple(sorted(candidates, key=lambda item: item.source_id)), issue)
