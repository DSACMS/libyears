"""Conservative compatibility checks for snapshot-supplied versions."""

from __future__ import annotations

from dataclasses import dataclass
import re


DECLARED_SNAPSHOT_CONFLICT = "declared_snapshot_conflict"
SNAPSHOT_VERSION_INCOMPATIBLE = "snapshot_version_incompatible"

_NAME = r"[A-Za-z0-9][A-Za-z0-9._-]*"
_BARE = re.compile(rf"^(?P<name>{_NAME})$")
_EXACT = re.compile(rf"^(?P<name>{_NAME})\s*==\s*(?P<version>\S+)$")
_MINIMUM = re.compile(rf"^(?P<name>{_NAME})\s*>=\s*(?P<version>\S+)$")
_NUMERIC_DOTTED = re.compile(r"^\d+(?:\.\d+)*$")


@dataclass(frozen=True, slots=True)
class CompatibilityResult:
    """Result of checking one declaration against a snapshot version."""

    compatible: bool
    reason: str | None = None


def _numeric_release(value: str) -> tuple[int, ...] | None:
    if _NUMERIC_DOTTED.fullmatch(value) is None:
        return None
    return tuple(int(component) for component in value.split("."))


def validate_snapshot_version(
    declaration: str, snapshot_version: str
) -> CompatibilityResult:
    """Check whether a snapshot version is safe for a supported declaration.

    This intentionally handles only bare names, exact pins, and numeric-dotted
    minimum versions. All other declaration syntax is rejected conservatively.
    """
    if not snapshot_version:
        return CompatibilityResult(False, SNAPSHOT_VERSION_INCOMPATIBLE)

    if _BARE.fullmatch(declaration.strip()) is not None:
        return CompatibilityResult(True)

    exact = _EXACT.fullmatch(declaration.strip())
    if exact is not None:
        if snapshot_version == exact.group("version"):
            return CompatibilityResult(True)
        return CompatibilityResult(False, DECLARED_SNAPSHOT_CONFLICT)

    minimum = _MINIMUM.fullmatch(declaration.strip())
    if minimum is not None:
        declared_version = _numeric_release(minimum.group("version"))
        supplied_version = _numeric_release(snapshot_version)
        if declared_version is None or supplied_version is None:
            return CompatibilityResult(False, SNAPSHOT_VERSION_INCOMPATIBLE)
        if supplied_version < declared_version:
            return CompatibilityResult(False, SNAPSHOT_VERSION_INCOMPATIBLE)
        return CompatibilityResult(True)

    return CompatibilityResult(False, SNAPSHOT_VERSION_INCOMPATIBLE)


check_snapshot_compatibility = validate_snapshot_version

__all__ = [
    "CompatibilityResult",
    "DECLARED_SNAPSHOT_CONFLICT",
    "SNAPSHOT_VERSION_INCOMPATIBLE",
    "check_snapshot_compatibility",
    "validate_snapshot_version",
]
