"""Repository scanning orchestration for the Libyears MVP."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .constraints import (
    DECLARED_SNAPSHOT_CONFLICT,
    SNAPSHOT_VERSION_INCOMPATIBLE,
    validate_snapshot_version,
)
from .metric import build_report, measure_dependency
from .model import (
    Dependency,
    DependencyCandidate,
    DependencyMeasurement,
    MetricSummary,
    RegistryFailure,
    RegistryResult,
    SourceError,
    SourceEvidence,
    SourceResult,
    UnmeasurableDependency,
)
from .npm import NpmAdapter, discover_manifest, resolve_lockfile
from .pypi import PyPIAdapter, PyPIResult
from .requirements import (
    ExactRequirement,
    Requirements,
    UnmeasurableRequirement,
    discover_requirements,
    normalize_name,
)
from .snapshot import SNAPSHOT_VERSION_CONFLICT, Snapshot


@dataclass(frozen=True, slots=True)
class ScanReport:
    """Structured output from scanning one repository."""

    summary: MetricSummary
    measurements: tuple[DependencyMeasurement, ...]
    unmeasurable: tuple[UnmeasurableRequirement, ...]
    snapshot_source: str | None = None
    diagnostics: tuple[tuple[str, str], ...] = ()
    tls_trust: str | None = None

    @property
    def dependencies(self) -> tuple[DependencyMeasurement, ...]:
        """Alias suitable for later output serialization."""
        return self.measurements


def _requirements_path(path: str | Path) -> Path | None:
    root = Path(path)
    if root.is_file():
        return root if root.name == "requirements.txt" else None
    if root.is_dir():
        candidate = root / "requirements.txt"
        return candidate if candidate.is_file() else None
    raise FileNotFoundError(root)


def _discover(path: str | Path) -> Requirements:
    requirements_path = _requirements_path(path)
    if requirements_path is None:
        return Requirements((), ())
    return discover_requirements(requirements_path)


def scan_repository(
    path: str | Path,
    *,
    adapter: PyPIAdapter | None = None,
    lookup: Callable[[str, str], PyPIResult | RegistryFailure] | None = None,
    snapshot: Snapshot | None = None,
    ca_bundle: str | None = None,
) -> ScanReport:
    """Scan the supported requirements input at *path*.

    ``lookup`` is an optional registry boundary for deterministic callers and
    tests. When omitted, the supplied or default PyPI adapter is used.
    """
    requirements = _discover(path)
    active_adapter = adapter or (None if lookup is not None else PyPIAdapter(ca_bundle=ca_bundle))
    registry_lookup = lookup or active_adapter.lookup
    measurements: list[DependencyMeasurement] = []
    unmeasurable: list[UnmeasurableRequirement] = []
    diagnostics: list[tuple[str, str]] = []

    snapshot_entries = {} if snapshot is None else {
        entry.normalized_name: entry for entry in snapshot.entries
    }
    snapshot_conflicts = {} if snapshot is None else {
        conflict.normalized_name: conflict for conflict in snapshot.conflicts
    }

    for requirement in requirements.exact:
        version_source = "requirements_exact"
        if snapshot is not None:
            conflict = snapshot_conflicts.get(requirement.normalized_name)
            entry = snapshot_entries.get(requirement.normalized_name)
            if conflict is not None or (
                entry is not None and entry.version != requirement.version
            ):
                unmeasurable.append(
                    UnmeasurableRequirement(
                        name=requirement.name,
                        declared=requirement.declared,
                        reason=DECLARED_SNAPSHOT_CONFLICT,
                        ecosystem=requirement.ecosystem,
                    )
                )
                continue
        result = registry_lookup(requirement.normalized_name, requirement.version)
        if isinstance(result, RegistryFailure):
            if result.diagnostic:
                diagnostics.append((requirement.name, result.diagnostic))
            unmeasurable.append(
                UnmeasurableRequirement(
                    name=requirement.name,
                    declared=requirement.declared,
                    reason=result.reason,
                    ecosystem=requirement.ecosystem,
                )
            )
            continue
        dependency = result_to_dependency(requirement, result, version_source=version_source)
        measurements.append(measure_dependency(dependency))

    for unmeasurable_requirement in requirements.unmeasurable:
        if snapshot is None or unmeasurable_requirement.reason != "non_exact_version":
            unmeasurable.append(unmeasurable_requirement)
            continue

        normalized_name = normalize_name(unmeasurable_requirement.name)
        conflict = snapshot_conflicts.get(normalized_name)
        if conflict is not None:
            unmeasurable.append(
                UnmeasurableRequirement(
                    name=unmeasurable_requirement.name,
                    declared=unmeasurable_requirement.declared,
                    reason=SNAPSHOT_VERSION_CONFLICT,
                    ecosystem=unmeasurable_requirement.ecosystem,
                )
            )
            continue

        entry = snapshot_entries.get(normalized_name)
        if entry is None:
            unmeasurable.append(
                UnmeasurableRequirement(
                    name=unmeasurable_requirement.name,
                    declared=unmeasurable_requirement.declared,
                    reason="snapshot_version_missing",
                    ecosystem=unmeasurable_requirement.ecosystem,
                )
            )
            continue

        compatibility = validate_snapshot_version(
            unmeasurable_requirement.declared, entry.version
        )
        if not compatibility.compatible:
            unmeasurable.append(
                UnmeasurableRequirement(
                    name=unmeasurable_requirement.name,
                    declared=unmeasurable_requirement.declared,
                    reason=compatibility.reason or SNAPSHOT_VERSION_INCOMPATIBLE,
                    ecosystem=unmeasurable_requirement.ecosystem,
                )
            )
            continue

        requirement = ExactRequirement(
            name=unmeasurable_requirement.name,
            normalized_name=normalized_name,
            version=entry.version,
            declared=unmeasurable_requirement.declared,
            ecosystem=unmeasurable_requirement.ecosystem,
        )
        result = registry_lookup(requirement.normalized_name, requirement.version)
        if isinstance(result, RegistryFailure):
            if result.diagnostic:
                diagnostics.append((requirement.name, result.diagnostic))
            unmeasurable.append(
                UnmeasurableRequirement(
                    name=requirement.name,
                    declared=requirement.declared,
                    reason=result.reason,
                    ecosystem=requirement.ecosystem,
                )
            )
            continue
        dependency = result_to_dependency(
            requirement, result, version_source="resolved_snapshot"
        )
        measurements.append(measure_dependency(dependency))

    report = build_report(measurements, dependencies_discovered=requirements.discovered)
    snapshot_source = None
    if snapshot is not None:
        snapshot_source = snapshot.source_path or "<supplied snapshot>"
    return ScanReport(
        report.summary,
        tuple(report.measurements),
        tuple(unmeasurable),
        snapshot_source,
        tuple(diagnostics),
        getattr(active_adapter, "tls_trust", None),
    )


def result_to_dependency(
    requirement: ExactRequirement,
    result: PyPIResult,
    *,
    version_source: str = "requirements_exact",
):
    """Combine a parsed requirement with adapter metadata into a domain object."""
    from .model import Dependency

    return Dependency(
        ecosystem=requirement.ecosystem,
        name=requirement.name,
        used_version=requirement.version,
        used_release_time=result.used_release_time,
        latest_stable_version=result.latest_stable_version,
        latest_stable_release_time=result.latest_stable_release_time,
        version_source=version_source,
    )


scan = scan_repository


@dataclass(frozen=True, slots=True)
class MixedScanReport:
    """Internal mixed-source result before the public schema migration."""

    measurements: tuple[DependencyMeasurement, ...]
    unmeasurable: tuple[UnmeasurableDependency, ...]
    source_errors: tuple[SourceError, ...]
    source_results: tuple[SourceResult, ...]
    diagnostics: tuple[tuple[str, str], ...] = ()
    tls_trust: str | None = None

    @property
    def dependencies(self) -> tuple[DependencyMeasurement, ...]:
        return self.measurements


def _python_source_result(
    path: str | Path, snapshot: Snapshot | None
) -> SourceResult:
    requirements = _discover(path)
    snapshot_entries = {} if snapshot is None else {
        entry.normalized_name: entry for entry in snapshot.entries
    }
    snapshot_conflicts = {} if snapshot is None else {
        conflict.normalized_name: conflict for conflict in snapshot.conflicts
    }
    candidates: list[DependencyCandidate] = []
    unmeasurable: list[UnmeasurableDependency] = []

    for requirement in requirements.exact:
        conflict = snapshot_conflicts.get(requirement.normalized_name)
        entry = snapshot_entries.get(requirement.normalized_name)
        if snapshot is not None and (
            conflict is not None or (entry is not None and entry.version != requirement.version)
        ):
            unmeasurable.append(
                UnmeasurableDependency(
                    requirement.ecosystem,
                    requirement.name,
                    requirement.declared,
                    DECLARED_SNAPSHOT_CONFLICT,
                )
            )
            continue
        candidates.append(
            DependencyCandidate(
                requirement.ecosystem,
                requirement.name,
                requirement.normalized_name,
                requirement.declared,
                requirement.version,
                "requirements_exact",
            )
        )

    for item in requirements.unmeasurable:
        if snapshot is None or item.reason != "non_exact_version":
            unmeasurable.append(
                UnmeasurableDependency(
                    item.ecosystem, item.name, item.declared, item.reason
                )
            )
            continue

        normalized_name = normalize_name(item.name)
        conflict = snapshot_conflicts.get(normalized_name)
        if conflict is not None:
            reason = SNAPSHOT_VERSION_CONFLICT
            entry = None
        else:
            entry = snapshot_entries.get(normalized_name)
            if entry is None:
                reason = "snapshot_version_missing"
            else:
                compatibility = validate_snapshot_version(item.declared, entry.version)
                reason = compatibility.reason or SNAPSHOT_VERSION_INCOMPATIBLE
                if compatibility.compatible:
                    candidates.append(
                        DependencyCandidate(
                            item.ecosystem,
                            item.name,
                            normalized_name,
                            item.declared,
                            entry.version,
                            "resolved_snapshot",
                        )
                    )
                    continue
        unmeasurable.append(
            UnmeasurableDependency(item.ecosystem, item.name, item.declared, reason)
        )

    snapshot_source = None
    if snapshot is not None:
        snapshot_source = snapshot.source_path or "<supplied snapshot>"
    return SourceResult(
        "pypi",
        tuple(candidates),
        tuple(unmeasurable),
        (),
        SourceEvidence("requirements.txt", snapshot_source),
    )


def _npm_source_result(root: Path | None) -> SourceResult:
    evidence = SourceEvidence("package.json", "package-lock.json")
    if root is None:
        return SourceResult("npm", (), (), (), evidence)

    discovery = discover_manifest(root)
    if discovery.reason is not None:
        return SourceResult(
            "npm",
            (),
            (),
            (SourceError("npm", "package.json", discovery.reason),),
            evidence,
        )

    resolved = resolve_lockfile(root, discovery)
    candidates: list[DependencyCandidate] = []
    unmeasurable: list[UnmeasurableDependency] = []
    for declaration in resolved.dependencies:
        if declaration.reason is not None:
            unmeasurable.append(
                UnmeasurableDependency(
                    "npm", declaration.name, declaration.declared, declaration.reason
                )
            )
        elif declaration.used_version is not None:
            candidates.append(
                DependencyCandidate(
                    "npm",
                    declaration.name,
                    declaration.name,
                    declaration.declared,
                    declaration.used_version,
                    "package_lock",
                )
            )
        else:
            # The source resolver must account for every declaration.
            raise ValueError(f"npm source produced no evidence or reason for {declaration.name}")
    return SourceResult(
        "npm", tuple(candidates), tuple(unmeasurable), (), evidence
    )


def scan_mixed_repository(
    path: str | Path,
    *,
    adapter: PyPIAdapter | None = None,
    npm_adapter: NpmAdapter | None = None,
    pypi_lookup: Callable[[str, str], PyPIResult | RegistryFailure] | None = None,
    npm_lookup: Callable[[str, str], RegistryResult | RegistryFailure] | None = None,
    snapshot: Snapshot | None = None,
    ca_bundle: str | None = None,
) -> MixedScanReport:
    """Discover and measure the two explicit supported ecosystems internally."""
    python_result = _python_source_result(path, snapshot)
    root = Path(path)
    npm_root = root if root.is_dir() else None
    npm_result = _npm_source_result(npm_root)

    pypi_adapter = adapter or (
        None if pypi_lookup is not None else PyPIAdapter(ca_bundle=ca_bundle)
    )
    active_npm_adapter = npm_adapter or (
        None if npm_lookup is not None else NpmAdapter(ca_bundle=ca_bundle)
    )
    pypi_registry_lookup = pypi_lookup or pypi_adapter.lookup
    npm_registry_lookup = npm_lookup or active_npm_adapter.lookup

    # This static pair list is deliberately limited to the two approved sources.
    source_pairs = (
        (python_result, pypi_registry_lookup),
        (npm_result, npm_registry_lookup),
    )
    measurements: list[DependencyMeasurement] = []
    unmeasurable = [
        item
        for source in (python_result, npm_result)
        for item in source.unmeasurable
    ]
    source_errors = [
        error
        for source in (python_result, npm_result)
        for error in source.source_errors
    ]
    diagnostics: list[tuple[str, str]] = []

    for source, registry_lookup in source_pairs:
        for candidate in source.candidates:
            result = registry_lookup(candidate.registry_name, candidate.used_version)
            if isinstance(result, RegistryFailure):
                if result.diagnostic:
                    diagnostics.append((candidate.name, result.diagnostic))
                unmeasurable.append(
                    UnmeasurableDependency(
                        candidate.ecosystem,
                        candidate.name,
                        candidate.declared,
                        result.reason,
                    )
                )
                continue
            dependency = Dependency(
                candidate.ecosystem,
                candidate.name,
                candidate.used_version,
                result.used_release_time,
                result.latest_stable_version,
                result.latest_stable_release_time,
                candidate.version_source,
            )
            measurements.append(measure_dependency(dependency))

    return MixedScanReport(
        tuple(measurements),
        tuple(unmeasurable),
        tuple(source_errors),
        (python_result, npm_result),
        tuple(diagnostics),
        getattr(pypi_adapter or active_npm_adapter, "tls_trust", None),
    )

__all__ = [
    "MixedScanReport",
    "ScanReport",
    "result_to_dependency",
    "scan",
    "scan_mixed_repository",
    "scan_repository",
]
