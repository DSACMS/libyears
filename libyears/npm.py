"""Static discovery of root npm production dependencies."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any


INVALID_MANIFEST = "invalid_manifest"
UNSUPPORTED_DEPENDENCY_SOURCE = "unsupported_dependency_source"
LOCK_VERSION_MISSING = "lock_version_missing"
DECLARATION_LOCK_CONFLICT = "declaration_lock_conflict"

_GITHUB_SHORTHAND = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*(?:\.git)?(?:#[^\s]+)?$"
)
_EXACT_VERSION = re.compile(
    r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


@dataclass(frozen=True, slots=True)
class NpmDeclaration:
    """A direct production declaration from the root package manifest."""

    name: str
    declared: str
    reason: str | None = None
    used_version: str | None = None


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


def _unsupported_source(declared: str) -> bool:
    """Return whether a declaration clearly names a non-registry source."""
    value = declared.strip()
    lowered = value.lower()
    return (
        lowered.startswith(
            (
                "git+",
                "git://",
                "ssh://",
                "git@",
                "github:",
                "file:",
                "link:",
                "workspace:",
                "npm:",
                "http://",
                "https://",
            )
        )
        or _GITHUB_SHORTHAND.fullmatch(value) is not None
    )


def _is_exact_version(declared: str) -> bool:
    """Recognize a concrete version literal without evaluating ranges."""
    return _EXACT_VERSION.fullmatch(declared) is not None


def resolve_v2_lockfile(
    discovery: ManifestDiscovery, packages: Any
) -> ManifestDiscovery:
    """Add v2 exact versions using only root ``node_modules`` package paths.

    ``packages`` is the v2 lockfile's path-keyed package map. Lockfile format
    and structural validation are handled by the source boundary task.
    """
    if discovery.reason is not None:
        return discovery

    resolved: list[NpmDeclaration] = []
    for declaration in discovery.dependencies:
        if declaration.reason is not None:
            resolved.append(declaration)
            continue

        package_path = f"node_modules/{declaration.name}"
        package = packages.get(package_path) if isinstance(packages, dict) else None
        version = package.get("version") if isinstance(package, dict) else None
        if not isinstance(version, str) or not version:
            resolved.append(
                NpmDeclaration(
                    declaration.name,
                    declaration.declared,
                    LOCK_VERSION_MISSING,
                )
            )
        elif _is_exact_version(declaration.declared) and declaration.declared != version:
            resolved.append(
                NpmDeclaration(
                    declaration.name,
                    declaration.declared,
                    DECLARATION_LOCK_CONFLICT,
                )
            )
        else:
            resolved.append(
                NpmDeclaration(
                    declaration.name,
                    declaration.declared,
                    used_version=version,
                )
            )

    return ManifestDiscovery(tuple(resolved))


def resolve_v3_lockfile(
    discovery: ManifestDiscovery, packages: Any
) -> ManifestDiscovery:
    """Add v3 exact versions from its path-keyed package map."""
    return resolve_v2_lockfile(discovery, packages)


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
        NpmDeclaration(
            name,
            declared,
            UNSUPPORTED_DEPENDENCY_SOURCE if _unsupported_source(declared) else None,
        )
        for name, declared in dependencies.items()
        if name not in optional_dependencies
    )
    return ManifestDiscovery(declarations)


__all__ = [
    "INVALID_MANIFEST",
    "DECLARATION_LOCK_CONFLICT",
    "LOCK_VERSION_MISSING",
    "ManifestDiscovery",
    "NpmDeclaration",
    "UNSUPPORTED_DEPENDENCY_SOURCE",
    "discover_manifest",
    "resolve_v2_lockfile",
    "resolve_v3_lockfile",
]
