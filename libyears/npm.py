"""Static discovery of root npm production dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import quote

from .model import (
    DependencyCandidate,
    RegistryFailure,
    RegistryResult,
    SourceError,
    SourceEvidence,
    SourceResult,
    UnmeasurableDependency,
)
from .registry import TransportFailure, VerifiedJSONTransport
from .yarn import YarnEntry, YarnFailure, parse_lockfile


INVALID_MANIFEST = "invalid_manifest"
INVALID_LOCKFILE = "invalid_lockfile"
UNSUPPORTED_LOCKFILE_VERSION = "unsupported_lockfile_version"
UNSUPPORTED_DEPENDENCY_SOURCE = "unsupported_dependency_source"
LOCK_VERSION_MISSING = "lock_version_missing"
DECLARATION_LOCK_CONFLICT = "declaration_lock_conflict"
AMBIGUOUS_LOCK_EVIDENCE = "ambiguous_lock_evidence"
CONFLICTING_RESOLUTION_SOURCES = "conflicting_resolution_sources"
PACKAGE_NOT_FOUND = "package_not_found"
VERSION_NOT_FOUND = "version_not_found"
RELEASE_DATE_MISSING = "release_date_missing"
NO_STABLE_RELEASE = "no_stable_release"
REGISTRY_ERROR = "registry_error"
INVALID_REGISTRY_RESPONSE = "invalid_registry_response"

_GITHUB_SHORTHAND = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*(?:\.git)?(?:#[^\s]+)?$"
)
_EXACT_VERSION = re.compile(
    r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
_SEMVER_VERSION = re.compile(
    r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
    r"(?:-((?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*))*))?"
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


NpmRegistryResult = RegistryResult
NpmRegistryFailure = RegistryFailure


def _npm_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(timezone.utc)


def _is_stable_version(version: str) -> bool:
    """Accept canonical stable SemVer strings and reject prereleases."""
    match = _SEMVER_VERSION.fullmatch(version)
    return match is not None and match.group(1) is None


class NpmAdapter:
    """Fetch public npm package metadata and select by publication time."""

    def __init__(
        self,
        *,
        timeout: float = 10.0,
        user_agent: str = "libyears/0.1",
        ca_bundle: str | None = None,
    ) -> None:
        self.transport = VerifiedJSONTransport(
            timeout=timeout, user_agent=user_agent, ca_bundle=ca_bundle
        )
        self.timeout = self.transport.timeout
        self.user_agent = self.transport.user_agent
        self.ssl_context = self.transport.ssl_context
        self.tls_trust = self.transport.tls_trust

    def lookup(
        self, name: str, used_version: str
    ) -> NpmRegistryResult | NpmRegistryFailure:
        """Look up an exact used version and timestamp-ordered latest release."""
        url_name = quote(name, safe="@")
        response_body = self.transport.get(f"https://registry.npmjs.org/{url_name}")
        if isinstance(response_body, TransportFailure):
            if response_body.status == 404:
                return NpmRegistryFailure(
                    name, used_version, PACKAGE_NOT_FOUND, "HTTP 404"
                )
            return NpmRegistryFailure(
                name, used_version, REGISTRY_ERROR, response_body.diagnostic
            )

        try:
            payload = json.loads(response_body.decode("utf-8"))
        except (AttributeError, TypeError, UnicodeError, json.JSONDecodeError):
            return NpmRegistryFailure(
                name,
                used_version,
                INVALID_REGISTRY_RESPONSE,
                "malformed registry response (invalid JSON)",
            )

        if (
            not isinstance(payload, dict)
            or not isinstance(payload.get("versions"), dict)
            or not isinstance(payload.get("time"), dict)
            or not isinstance(payload.get("dist-tags", {}), dict)
        ):
            return NpmRegistryFailure(
                name,
                used_version,
                INVALID_REGISTRY_RESPONSE,
                "malformed registry response (unexpected structure)",
            )

        versions = payload["versions"]
        release_times = payload["time"]
        if used_version not in versions:
            return NpmRegistryFailure(name, used_version, VERSION_NOT_FOUND)
        if not isinstance(versions[used_version], dict):
            return NpmRegistryFailure(
                name,
                used_version,
                INVALID_REGISTRY_RESPONSE,
                "malformed registry response (invalid version entry)",
            )
        used_release_time = _npm_timestamp(release_times.get(used_version))
        if used_release_time is None:
            return NpmRegistryFailure(name, used_version, RELEASE_DATE_MISSING)

        candidates = [
            (timestamp, version)
            for version in versions
            if isinstance(version, str)
            and _is_stable_version(version)
            and isinstance(versions[version], dict)
            and (timestamp := _npm_timestamp(release_times.get(version))) is not None
        ]
        if not candidates:
            return NpmRegistryFailure(name, used_version, NO_STABLE_RELEASE)

        latest_timestamp = max(timestamp for timestamp, _ in candidates)
        tied_versions = sorted(
            version for timestamp, version in candidates if timestamp == latest_timestamp
        )
        latest_tag = payload.get("dist-tags", {}).get("latest")
        latest_version = latest_tag if latest_tag in tied_versions else tied_versions[0]
        return NpmRegistryResult(
            name, used_version, used_release_time, latest_version, latest_timestamp
        )

    resolve = lookup


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


def match_yarn_entries(
    declarations: tuple[NpmDeclaration, ...], entries: tuple[YarnEntry, ...]
) -> tuple[tuple[DependencyCandidate, ...], tuple[UnmeasurableDependency, ...]]:
    """Match decoded selector text without resolving ranges or reading files.

    Count matching entries rather than selectors, keeping repeated entries
    ambiguous even when they contain the same version.
    """
    candidates = []
    unmeasurable = []
    for declaration in declarations:
        reason = declaration.reason
        version = None
        if reason is None:
            target = declaration.name + "@" + declaration.declared
            matches = [entry for entry in entries if target in entry.selectors]
            if not matches:
                reason = LOCK_VERSION_MISSING
            elif len(matches) > 1:
                reason = AMBIGUOUS_LOCK_EVIDENCE
            else:
                version = matches[0].version
                if version is None or not _is_exact_version(version):
                    reason = AMBIGUOUS_LOCK_EVIDENCE
                elif _is_exact_version(declaration.declared) and declaration.declared != version:
                    reason = DECLARATION_LOCK_CONFLICT

        if reason is not None:
            unmeasurable.append(
                UnmeasurableDependency(
                    "npm", declaration.name, declaration.declared, reason
                )
            )
        else:
            candidates.append(
                DependencyCandidate(
                    "npm",
                    declaration.name,
                    declaration.name,
                    declaration.declared,
                    version,
                    "yarn_lock",
                )
            )
    return tuple(candidates), tuple(unmeasurable)


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


def _with_reason(
    discovery: ManifestDiscovery, reason: str
) -> ManifestDiscovery:
    """Assign a lockfile reason without replacing earlier source reasons."""
    return ManifestDiscovery(
        tuple(
            declaration
            if declaration.reason is not None
            else NpmDeclaration(declaration.name, declaration.declared, reason)
            for declaration in discovery.dependencies
        ),
        discovery.reason,
    )


def _valid_lock_entry(package: Any) -> bool:
    if not isinstance(package, dict) or "link" in package:
        return False
    version = package.get("version")
    return (
        isinstance(version, str)
        and bool(version)
        and _EXACT_VERSION.fullmatch(version) is not None
    )


def resolve_lockfile(
    root: str | Path,
    discovery: ManifestDiscovery,
    *,
    lockfile_present: bool | None = None,
) -> ManifestDiscovery:
    """Resolve direct evidence from a supported root package-lock file.

    The selector supplies its presence check; legacy callers still check here.
    """
    if discovery.reason is not None or not discovery.dependencies:
        return discovery

    lockfile_path = Path(root) / "package-lock.json"
    if lockfile_present is None:
        lockfile_present = lockfile_path.exists()
    if not lockfile_present:
        return resolve_v2_lockfile(discovery, {})

    try:
        lockfile = json.loads(lockfile_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return _with_reason(discovery, INVALID_LOCKFILE)

    if not isinstance(lockfile, dict):
        return _with_reason(discovery, INVALID_LOCKFILE)

    version = lockfile.get("lockfileVersion")
    if type(version) is not int or version not in (2, 3):
        return _with_reason(discovery, UNSUPPORTED_LOCKFILE_VERSION)

    packages = lockfile.get("packages")
    if not isinstance(packages, dict):
        return _with_reason(discovery, INVALID_LOCKFILE)

    invalid_names = set()
    for declaration in discovery.dependencies:
        package_path = f"node_modules/{declaration.name}"
        if (
            declaration.reason is None
            and package_path in packages
            and not _valid_lock_entry(packages[package_path])
        ):
            invalid_names.add(declaration.name)

    resolver = resolve_v2_lockfile if version == 2 else resolve_v3_lockfile
    resolved = resolver(discovery, packages)
    if not invalid_names:
        return resolved

    dependencies = tuple(
        NpmDeclaration(
            declaration.name,
            declaration.declared,
            INVALID_LOCKFILE,
        )
        if declaration.name in invalid_names
        else declaration
        for declaration in resolved.dependencies
    )
    return ManifestDiscovery(dependencies)


def _resolve_yarn_evidence(path: Path, discovery: ManifestDiscovery) -> SourceResult:
    """Adapt Yarn evidence without promoting dependency failures to the source."""
    evidence = SourceEvidence("package.json", "yarn.lock", "yarn_lock_v1", include_format=True)
    entries = parse_lockfile(path)
    if isinstance(entries, YarnFailure):
        diagnostic = "malformed Yarn Classic v1 structure"
        if entries.reason == "unsupported_lockfile_format":
            evidence = SourceEvidence("package.json", "yarn.lock", include_format=True)
            diagnostic = entries.diagnostic
        return SourceResult(
            "npm", (), (),
            (SourceError("npm", "yarn.lock", entries.reason),), evidence,
            dependencies_discovered=len(discovery.dependencies),
            measurement_available=False,
            diagnostics=(("yarn.lock", diagnostic),),
        )

    candidates, unmeasurable = match_yarn_entries(discovery.dependencies, entries)
    return SourceResult(
        "npm", candidates, unmeasurable, (), evidence,
        dependencies_discovered=len(discovery.dependencies),
        measurement_available=True,
    )


def resolve_npm_evidence(root: str | Path, discovery: ManifestDiscovery) -> SourceResult:
    """Select root npm resolution evidence without resolving declarations."""
    evidence = SourceEvidence("package.json", "package-lock.json")
    if discovery.reason is not None:
        return SourceResult(
            "npm", (), (),
            (SourceError("npm", "package.json", discovery.reason),), evidence,
            dependencies_discovered=None, measurement_available=False,
        )

    root = Path(root)
    package_lock_present = (root / "package-lock.json").exists()
    yarn_lock_present = (root / "yarn.lock").exists()
    if package_lock_present and yarn_lock_present:
        return SourceResult(
            "npm", (), (),
            (SourceError(
                "npm", "package-lock.json + yarn.lock", CONFLICTING_RESOLUTION_SOURCES
            ),),
            SourceEvidence("package.json", None, include_format=True),
            dependencies_discovered=len(discovery.dependencies),
            measurement_available=False,
        )
    if yarn_lock_present:
        return _resolve_yarn_evidence(root / "yarn.lock", discovery)

    resolved = resolve_lockfile(root, discovery, lockfile_present=package_lock_present)
    candidates = []
    unmeasurable = []
    for declaration in resolved.dependencies:
        if declaration.reason is not None:
            unmeasurable.append(UnmeasurableDependency(
                "npm", declaration.name, declaration.declared, declaration.reason
            ))
        elif declaration.used_version is not None:
            candidates.append(DependencyCandidate(
                "npm", declaration.name, declaration.name, declaration.declared,
                declaration.used_version, "package_lock",
            ))
        else:
            raise ValueError(f"npm source produced no evidence or reason for {declaration.name}")
    return SourceResult(
        "npm", tuple(candidates), tuple(unmeasurable), (), evidence,
        dependencies_discovered=len(discovery.dependencies), measurement_available=True,
        source_present=(root / "package.json").is_file(),
    )


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
    "AMBIGUOUS_LOCK_EVIDENCE",
    "CONFLICTING_RESOLUTION_SOURCES",
    "INVALID_MANIFEST",
    "INVALID_LOCKFILE",
    "INVALID_REGISTRY_RESPONSE",
    "DECLARATION_LOCK_CONFLICT",
    "LOCK_VERSION_MISSING",
    "NO_STABLE_RELEASE",
    "ManifestDiscovery",
    "NpmAdapter",
    "NpmDeclaration",
    "NpmRegistryFailure",
    "NpmRegistryResult",
    "PACKAGE_NOT_FOUND",
    "REGISTRY_ERROR",
    "RELEASE_DATE_MISSING",
    "UNSUPPORTED_DEPENDENCY_SOURCE",
    "UNSUPPORTED_LOCKFILE_VERSION",
    "VERSION_NOT_FOUND",
    "discover_manifest",
    "resolve_lockfile",
    "resolve_npm_evidence",
    "match_yarn_entries",
    "resolve_v2_lockfile",
    "resolve_v3_lockfile",
]
