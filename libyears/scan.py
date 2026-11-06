"""Repository scanning orchestration for the Libyears MVP."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field, replace
from pathlib import Path
import re
from typing import Callable

from .constraints import (
    DECLARED_SNAPSHOT_CONFLICT,
    SNAPSHOT_VERSION_INCOMPATIBLE,
    validate_snapshot_version,
)
from .metric import build_report, calculate_summary, measure_dependency
from .model import (
    Dependency,
    DependencyCandidate,
    DependencyMeasurement,
    MetricSummary,
    RegistryFailure,
    RegistryResult,
    RubyGemsEvidence,
    SourceError,
    SourceEvidence,
    SourceResult,
    UnmeasurableDependency,
)
from .npm import NpmAdapter, discover_manifest, resolve_npm_evidence
from .nuget import NuGetSource, read_nuget_source
from .nuget_provenance import LocalAuthority
from .nuget_registry import NuGetRegistryAdapter
from .nuget_supervisor import PackageResult
from .nuget_sources import (NuGetRepositoryRequestError, read_repository_sources,
                            validate_witnesses)
from .pypi import PyPIAdapter, PyPIResult
from .requirements import (
    ExactRequirement,
    Requirements,
    UnmeasurableRequirement,
    discover_requirements,
    normalize_name,
)
from .rubygems import ruby_source_result, schedule_ruby_candidates, scoped_ruby_source_result
from .rubygems_registry import RubyGemsAdapter
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
    summary: MetricSummary
    by_ecosystem: dict[str, MetricSummary]
    diagnostics: tuple[tuple[str, str], ...] = ()
    tls_trust: str | None = None
    nuget_repository: bool = False
    by_nuget_source: dict[str | None, MetricSummary] = field(default_factory=dict)

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
        dependencies_discovered=requirements.discovered,
        measurement_available=True,
        source_present=_requirements_path(path) is not None,
    )


def _npm_source_result(root: Path | None) -> SourceResult:
    evidence = SourceEvidence("package.json", "package-lock.json")
    if root is None:
        return SourceResult(
            "npm", (), (), (), evidence,
            dependencies_discovered=0, measurement_available=True, source_present=False,
        )

    # Lockfiles alone do not establish npm dependency scope.
    if not (root / "package.json").exists():
        return SourceResult(
            "npm", (), (), (), evidence,
            dependencies_discovered=0, measurement_available=True, source_present=False,
        )
    return resolve_npm_evidence(root, discover_manifest(root))


def _available_summary(
    measurements: list[DependencyMeasurement],
    *,
    discovered: int | None,
    measurement_available: bool,
    coverage_available: bool,
    discovery_failed: bool = False,
    unavailable_numeric: bool = False,
) -> MetricSummary:
    """Combine scan-derived availability with the existing numeric aggregates."""
    numeric = calculate_summary(
        measurements,
        dependencies_discovered=discovered,
        discovery_failed=discovery_failed,
    )
    return MetricSummary(
        dependencies_discovered=numeric.dependencies_discovered,
        dependencies_measured=(
            numeric.dependencies_measured if measurement_available else None
        ),
        coverage=numeric.coverage if coverage_available else None,
        total_libyears=None if unavailable_numeric else numeric.total_libyears,
        mean_libyears=None if unavailable_numeric else numeric.mean_libyears,
        median_libyears=None if unavailable_numeric else numeric.median_libyears,
        max_libyears=None if unavailable_numeric else numeric.max_libyears,
    )


class RubyGroupRequestError(ValueError):
    """An invalid scoped Ruby request, before any dependency source is read."""


@dataclass(frozen=True, slots=True)
class NuGetRequest:
    """Explicit internal activation; filenames have no implicit defaults."""

    project: str
    provenance: str | None = None


def _nuget_registry_results(source: NuGetSource, lookup_all):
    """Consume only local capabilities and join safe worker facts to declarations."""
    candidates = {item.authority: item.candidate for item in source.authorized_candidates}
    results = {}
    for authority, result in lookup_all(tuple(candidates)):
        candidate = candidates[authority]
        evidence = replace(
            candidate.nuget_evidence,
            origin_state=result.origin_state,
            content_hash_state=result.content_hash_state,
            used_publication=result.used_publication,
            latest_publication=result.latest_publication,
        )
        if result.reason is not None:
            combined = RegistryFailure(candidate.name, authority.normalized_version,
                                       result.reason, nuget_evidence=evidence)
        else:
            combined = RegistryResult(
                candidate.name, authority.normalized_version,
                result.used_publication.created, result.latest_publication.version,
                result.latest_publication.created, nuget_evidence=evidence,
            )
        results[(candidate.registry_name, candidate.used_version)] = combined
    return results


def validate_ruby_groups(path: str | Path, groups: tuple[str, ...]) -> tuple[str, ...]:
    """Validate a scoped request and return its canonical group names."""
    if not isinstance(groups, (tuple, list)) or not groups:
        raise RubyGroupRequestError("Ruby groups must be a nonempty sequence of names")
    for group in groups:
        if not isinstance(group, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", group):
            raise RubyGroupRequestError("Invalid Ruby group name")
    if not Path(path).is_dir():
        raise RubyGroupRequestError("Ruby group selection requires a directory")
    return tuple(sorted(set(groups)))


def scan_mixed_repository(
    path: str | Path,
    *,
    adapter: PyPIAdapter | None = None,
    npm_adapter: NpmAdapter | None = None,
    rubygems_adapter: RubyGemsAdapter | None = None,
    pypi_lookup: Callable[[str, str], PyPIResult | RegistryFailure] | None = None,
    npm_lookup: Callable[[str, str], RegistryResult | RegistryFailure] | None = None,
    rubygems_lookup: Callable[[str, str], RegistryResult | RegistryFailure] | None = None,
    snapshot: Snapshot | None = None,
    ca_bundle: str | None = None,
    ruby_groups: tuple[str, ...] | None = None,
    nuget_request: NuGetRequest | None = None,
    nuget_repository: bool = False,
    nuget_witnesses: tuple[tuple[str, str], ...] = (),
    nuget_adapter: NuGetRegistryAdapter | None = None,
    nuget_lookup: Callable[[tuple[LocalAuthority, ...]],
                           tuple[tuple[LocalAuthority, PackageResult], ...]] | None = None,
) -> MixedScanReport:
    """Discover supported sources, with explicit internal NuGet mode requests."""
    validate_witnesses(nuget_witnesses)
    if ((nuget_repository and (nuget_request is not None or not Path(path).is_dir()))
            or (nuget_witnesses and not nuget_repository)):
        raise NuGetRepositoryRequestError('invalid NuGet repository request')
    if ruby_groups is not None:
        ruby_groups = validate_ruby_groups(path, ruby_groups)
    if nuget_request is not None and not Path(path).is_dir():
        raise ValueError('NuGet selection requires a directory')
    python_result = _python_source_result(path, snapshot)
    root = Path(path)
    npm_root = root if root.is_dir() else None
    npm_result = _npm_source_result(npm_root)
    if ruby_groups is None:
        ruby_result = ruby_source_result(npm_root)
    else:
        ruby_result = scoped_ruby_source_result(root, ruby_groups)

    pypi_adapter = adapter or (
        None if pypi_lookup is not None else PyPIAdapter(ca_bundle=ca_bundle)
    )
    active_npm_adapter = npm_adapter or (
        None if npm_lookup is not None else NpmAdapter(ca_bundle=ca_bundle)
    )
    pypi_registry_lookup = pypi_lookup or pypi_adapter.lookup
    npm_registry_lookup = npm_lookup or active_npm_adapter.lookup

    active_ruby_adapter = rubygems_adapter or (
        None if rubygems_lookup is not None else RubyGemsAdapter(ca_bundle=ca_bundle)
    )
    ruby_registry_lookup = rubygems_lookup or active_ruby_adapter.lookup

    # Keep discovery explicit; each source owns its ecosystem policy.
    source_pairs = (
        (python_result, pypi_registry_lookup),
        (npm_result, npm_registry_lookup),
        (ruby_result, ruby_registry_lookup),
    )
    nuget_sources = ()
    if nuget_request is not None:
        nuget_sources = (read_nuget_source(root, nuget_request.project, nuget_request.provenance),)
    elif nuget_repository:
        nuget_sources = read_repository_sources(root, nuget_witnesses)
    authorities = tuple(item.authority for source in nuget_sources
                        for item in source.authorized_candidates)
    package_results = defaultdict(deque)
    if authorities:
        active_nuget_adapter = nuget_adapter or (
            None if nuget_lookup is not None else NuGetRegistryAdapter()
        )
        nuget_registry_lookup = nuget_lookup or active_nuget_adapter.lookup_all
        for authority, result in nuget_registry_lookup(authorities):
            package_results[authority].append(result)
    for source in nuget_sources:
        # Equal capabilities still get separate results and their own staged
        # source evidence. Stable adapter ordering preserves equal-key order.
        def queued_results(requested):
            return tuple((authority, package_results[authority].popleft())
                         for authority in requested)
        results = _nuget_registry_results(source, queued_results)
        source_pairs += ((source.result, lambda name, version, rows=results: rows[(name, version)]),)
    sources = tuple(source for source, _ in source_pairs)
    measurements: list[DependencyMeasurement] = []
    unmeasurable = [
        item
        for source in sources
        for item in source.unmeasurable
    ]
    source_errors = [
        error
        for source in sources
        for error in source.source_errors
    ]
    diagnostics = [
        diagnostic
        for source in sources
        for diagnostic in source.diagnostics
    ]

    for source, registry_lookup in source_pairs:
        candidates = source.candidates
        if source.ecosystem == "rubygems":
            candidates = schedule_ruby_candidates(candidates)
        for candidate in candidates:
            result = registry_lookup(candidate.registry_name, candidate.used_version)
            ruby_evidence = candidate.rubygems_evidence
            nuget_evidence = result.nuget_evidence or candidate.nuget_evidence
            if ruby_evidence is not None and result.rubygems_evidence is not None:
                ruby_evidence = RubyGemsEvidence(
                    ruby_evidence.selected_artifacts,
                    result.rubygems_evidence.used_publication_artifacts,
                    result.rubygems_evidence.latest_publication_artifacts,
                )
            if isinstance(result, RegistryFailure):
                if result.diagnostic:
                    diagnostics.append((candidate.name, result.diagnostic))
                unmeasurable.append(
                    UnmeasurableDependency(
                        candidate.ecosystem,
                        candidate.name,
                        candidate.declared,
                        result.reason,
                        ruby_evidence,
                        candidate.gemfile_evidence,
                        nuget_evidence,
                    )
                )
                continue
            dependency = Dependency(
                candidate.ecosystem,
                candidate.name,
                result.used_version if source.ecosystem == 'nuget' else candidate.used_version,
                result.used_release_time,
                result.latest_stable_version,
                result.latest_stable_release_time,
                candidate.version_source,
                ruby_evidence,
                candidate.gemfile_evidence,
                nuget_evidence,
            )
            measurements.append(measure_dependency(dependency))

    detected_sources = tuple(
        source
        for source in sources
        if source.source_present or source.source_errors
    )
    discovery_unavailable = any(
        source.dependencies_discovered is None for source in detected_sources
    )
    discovered = (
        None
        if discovery_unavailable
        else sum(source.dependencies_discovered for source in detected_sources)
    )
    summary = _available_summary(
        measurements,
        discovered=discovered,
        measurement_available=(
            not detected_sources
            or any(source.measurement_available for source in detected_sources)
        ),
        coverage_available=all(
            source.measurement_available for source in detected_sources
        ),
    )
    by_ecosystem = {}
    for ecosystem in sorted({source.ecosystem for source in detected_sources}):
        members = [source for source in detected_sources if source.ecosystem == ecosystem]
        available = any(source.measurement_available for source in members)
        unknown = any(source.dependencies_discovered is None for source in members)
        by_ecosystem[ecosystem] = _available_summary(
            [item for item in measurements if item.dependency.ecosystem == ecosystem],
            discovered=None if unknown else sum(source.dependencies_discovered for source in members),
            measurement_available=available,
            coverage_available=all(source.measurement_available for source in members),
            discovery_failed=unknown and not available,
            unavailable_numeric=not available and (
                ecosystem == 'nuget' or members[0].evidence.requested_groups is not None),
        )
    by_nuget_source = {}
    if nuget_repository:
        for source in nuget_sources:
            member = source.result
            rows = [item for item in measurements if item.dependency.ecosystem == 'nuget'
                    and item.dependency.nuget_evidence.source_id == member.source_id]
            by_nuget_source[member.source_id] = _available_summary(
                rows, discovered=member.dependencies_discovered,
                measurement_available=member.measurement_available,
                coverage_available=member.measurement_available,
                discovery_failed=member.dependencies_discovered is None,
                unavailable_numeric=not member.measurement_available)

    tls_trust = None
    for source, active_adapter in (
        (python_result, pypi_adapter),
        (npm_result, active_npm_adapter),
        (ruby_result, active_ruby_adapter),
    ):
        if source.source_present and active_adapter is not None:
            tls_trust = getattr(active_adapter, "tls_trust", None)
            break

    return MixedScanReport(
        tuple(measurements),
        tuple(unmeasurable),
        tuple(source_errors),
        sources,
        summary,
        by_ecosystem,
        tuple(diagnostics),
        tls_trust,
        nuget_repository,
        by_nuget_source,
    )

__all__ = [
    "MixedScanReport",
    "ScanReport",
    "RubyGroupRequestError",
    "NuGetRequest",
    "result_to_dependency",
    "scan",
    "scan_mixed_repository",
    "scan_repository",
    "validate_ruby_groups",
]
