"""Bounded filename recognition for human guidance, never measurement evidence."""

from dataclasses import dataclass
import os
from pathlib import Path
import stat


MAX_DEPTH = 4
MAX_DIRECTORIES = 256
MAX_ENTRIES = 10_000
MAX_CANDIDATES = 100
EXCLUDED_DIRECTORIES = frozenset({
    'bin', 'obj', 'node_modules', 'packages', 'vendor', 'venv', '__pycache__',
})
# Keep capability identities stable when tests wrap filesystem operations.
_OPEN = os.open
_STAT = os.stat
_SCANDIR = os.scandir


@dataclass(frozen=True)
class NuGetRecognition:
    status: str = 'complete'
    candidates: tuple[str, ...] = ()
    # Incomplete inventories still discard names and all population authority.
    positive_local_evidence: bool = False


def discovery_available() -> bool:
    """Refuse traversal where the required non-following primitives are absent."""
    return (all(getattr(os, name, 0) for name in
                ('O_DIRECTORY', 'O_NOFOLLOW', 'O_NONBLOCK'))
            and _OPEN in os.supports_dir_fd
            and _STAT in os.supports_dir_fd
            and _STAT in os.supports_follow_symlinks
            and _SCANDIR in os.supports_fd)


class _IncompleteRecognition(Exception):
    pass


def _identity(metadata):
    return metadata.st_dev, metadata.st_ino


def _directory_state(metadata):
    return (*_identity(metadata), metadata.st_mtime_ns, metadata.st_ctime_ns)


def _reparse_point(metadata) -> bool:
    return bool(getattr(metadata, 'st_file_attributes', 0)
                & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0))


def discover_nuget_candidates(root: str | Path) -> NuGetRecognition:
    """Observe regular .csproj names without opening any project contents.

    Incomplete observations discard the entire list, so neither enumeration
    order nor partial access can produce an apparently complete population.
    """
    if not discovery_available():
        return NuGetRecognition('unavailable')
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_NONBLOCK
    candidates = []
    positive_local_evidence = False
    directory_count = 0
    entry_count = 0

    def visit(descriptor, relative, depth):
        nonlocal directory_count, entry_count, positive_local_evidence
        directory_count += 1
        if directory_count > MAX_DIRECTORIES:
            raise _IncompleteRecognition
        before = os.fstat(descriptor)
        entries = []
        with os.scandir(descriptor) as iterator:
            for entry in iterator:
                entry_count += 1
                if entry_count > MAX_ENTRIES:
                    raise _IncompleteRecognition
                metadata = entry.stat(follow_symlinks=False)
                entries.append((entry.name, metadata))
                if (entry.name.endswith('.csproj') and stat.S_ISREG(metadata.st_mode)
                        and not _reparse_point(metadata)):
                    positive_local_evidence = True

        for name, metadata in sorted(entries):
            if _reparse_point(metadata):
                continue
            child_relative = f'{relative}/{name}' if relative else name
            if stat.S_ISREG(metadata.st_mode) and name.endswith('.csproj'):
                candidates.append(child_relative)
                if len(candidates) > MAX_CANDIDATES:
                    raise _IncompleteRecognition
            elif stat.S_ISDIR(metadata.st_mode):
                if name.startswith('.') or name in EXCLUDED_DIRECTORIES:
                    continue
                if depth == MAX_DEPTH:
                    continue
                child = os.open(name, flags, dir_fd=descriptor)
                try:
                    if _identity(metadata) != _identity(os.fstat(child)):
                        raise _IncompleteRecognition
                    visit(child, child_relative, depth + 1)
                    current = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
                    if _identity(current) != _identity(metadata):
                        raise _IncompleteRecognition
                finally:
                    os.close(child)
        if _directory_state(before) != _directory_state(os.fstat(descriptor)):
            raise _IncompleteRecognition

    try:
        descriptor = os.open(root, flags)
        try:
            visit(descriptor, '', 0)
        finally:
            os.close(descriptor)
    except (OSError, ValueError, NotImplementedError, _IncompleteRecognition):
        return NuGetRecognition('incomplete', positive_local_evidence=positive_local_evidence)
    return NuGetRecognition(candidates=tuple(sorted(candidates)))
