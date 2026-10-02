"""Parsing for the deliberately narrow pip-freeze exact snapshot format."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .requirements import normalize_name


SNAPSHOT_FORMAT = "pip_freeze_exact"
SNAPSHOT_VERSION_CONFLICT = "snapshot_version_conflict"

_EXACT = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)\s*==\s*(?P<version>[^\s#]+)$"
)


@dataclass(frozen=True, slots=True)
class SnapshotEntry:
    """One accepted exact package entry from a snapshot."""

    name: str
    normalized_name: str
    version: str
    source_line: str
    line_number: int
    format: str = SNAPSHOT_FORMAT


@dataclass(frozen=True, slots=True)
class SnapshotConflict:
    """Conflicting exact versions for one normalized package name."""

    name: str
    normalized_name: str
    versions: tuple[str, ...]
    entries: tuple[SnapshotEntry, ...]
    reason: str = SNAPSHOT_VERSION_CONFLICT


@dataclass(frozen=True, slots=True)
class RejectedSnapshotLine:
    """A non-empty snapshot line that is not exact evidence."""

    source_line: str
    line_number: int


@dataclass(frozen=True, slots=True)
class Snapshot:
    """Parsed exact entries and diagnostics from a snapshot file."""

    entries: tuple[SnapshotEntry, ...]
    conflicts: tuple[SnapshotConflict, ...]
    rejected: tuple[RejectedSnapshotLine, ...]
    format: str = SNAPSHOT_FORMAT
    source_path: str | None = None


def _without_trailing_comment(line: str) -> str:
    for index, character in enumerate(line):
        if character == "#" and (index == 0 or line[index - 1].isspace()):
            return line[:index].rstrip()
    return line.strip()


def parse_snapshot_text(text: str) -> Snapshot:
    """Parse exact ``NAME==VERSION`` entries from snapshot text."""
    grouped: dict[str, list[SnapshotEntry]] = {}
    rejected: list[RejectedSnapshotLine] = []

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = _without_trailing_comment(raw_line)
        if not line or line.startswith("#"):
            continue
        match = _EXACT.fullmatch(line)
        if match is None:
            rejected.append(RejectedSnapshotLine(raw_line, line_number))
            continue
        entry = SnapshotEntry(
            name=match.group("name"),
            normalized_name=normalize_name(match.group("name")),
            version=match.group("version"),
            source_line=raw_line,
            line_number=line_number,
        )
        grouped.setdefault(entry.normalized_name, []).append(entry)

    entries: list[SnapshotEntry] = []
    conflicts: list[SnapshotConflict] = []
    for package_entries in grouped.values():
        versions = tuple(dict.fromkeys(entry.version for entry in package_entries))
        if len(versions) > 1:
            conflicts.append(
                SnapshotConflict(
                    name=package_entries[0].name,
                    normalized_name=package_entries[0].normalized_name,
                    versions=versions,
                    entries=tuple(package_entries),
                )
            )
        else:
            entries.append(package_entries[0])

    return Snapshot(tuple(entries), tuple(conflicts), tuple(rejected))


def parse_snapshot(path: str | Path) -> Snapshot:
    """Parse a ``pip_freeze_exact`` snapshot file."""
    parsed = parse_snapshot_text(Path(path).read_text(encoding="utf-8"))
    return Snapshot(parsed.entries, parsed.conflicts, parsed.rejected, parsed.format, str(path))


parse = parse_snapshot

__all__ = [
    "RejectedSnapshotLine",
    "SNAPSHOT_FORMAT",
    "SNAPSHOT_VERSION_CONFLICT",
    "Snapshot",
    "SnapshotConflict",
    "SnapshotEntry",
    "parse",
    "parse_snapshot",
    "parse_snapshot_text",
]
