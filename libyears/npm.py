"""Static discovery of root npm production dependencies."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


INVALID_MANIFEST = "invalid_manifest"


@dataclass(frozen=True, slots=True)
class NpmDeclaration:
    """A direct production declaration from the root package manifest."""

    name: str
    declared: str


@dataclass(frozen=True, slots=True)
class ManifestDiscovery:
    """Discovered root npm declarations or a source-level parse failure."""

    dependencies: tuple[NpmDeclaration, ...]
    reason: str | None = None


def _dependency_map(value: Any) -> dict[str, str] | None:
    """Return a valid package dependency map, or ``None`` for invalid data."""
    if not isinstance(value, dict):
        return None
    if any(not isinstance(name, str) or not isinstance(declared, str) for name, declared in value.items()):
        return None
    return value


def discover_manifest(root: str | Path) -> ManifestDiscovery:
    """Discover production dependencies from *root*/``package.json``.

    An absent manifest is an empty discovery. Invalid JSON or malformed root
    dependency maps fail closed as ``invalid_manifest`` and yield no rows.
    """
    manifest_path = Path(root) / "package.json"
    if not manifest_path.exists():
        return ManifestDiscovery(())

    try:
        document = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return ManifestDiscovery((), INVALID_MANIFEST)

    if not isinstance(document, dict):
        return ManifestDiscovery((), INVALID_MANIFEST)

    dependencies_value = document.get("dependencies", {})
    optional_value = document.get("optionalDependencies", {})
    dependencies = _dependency_map(dependencies_value)
    optional_dependencies = _dependency_map(optional_value)
    if dependencies is None or optional_dependencies is None:
        return ManifestDiscovery((), INVALID_MANIFEST)

    declarations = tuple(
        NpmDeclaration(name, declared)
        for name, declared in dependencies.items()
        if name not in optional_dependencies
    )
    return ManifestDiscovery(declarations)


__all__ = [
    "INVALID_MANIFEST",
    "ManifestDiscovery",
    "NpmDeclaration",
    "discover_manifest",
]
