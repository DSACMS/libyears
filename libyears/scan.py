"""Repository scanning orchestration for the Libyears MVP."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .metric import build_report, measure_dependency
from .model import DependencyMeasurement, MetricSummary
from .pypi import PyPIAdapter, PyPIResult, RegistryFailure
from .requirements import (
    ExactRequirement,
    Requirements,
    UnmeasurableRequirement,
    discover_requirements,
)


@dataclass(frozen=True, slots=True)
class ScanReport:
    """Structured output from scanning one repository."""

    summary: MetricSummary
    measurements: tuple[DependencyMeasurement, ...]
    unmeasurable: tuple[UnmeasurableRequirement, ...]

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
) -> ScanReport:
    """Scan the supported requirements input at *path*.

    ``lookup`` is an optional registry boundary for deterministic callers and
    tests. When omitted, the supplied or default PyPI adapter is used.
    """
    requirements = _discover(path)
    registry_lookup = lookup or (adapter or PyPIAdapter()).lookup
    measurements: list[DependencyMeasurement] = []
    unmeasurable = list(requirements.unmeasurable)

    for requirement in requirements.exact:
        result = registry_lookup(requirement.normalized_name, requirement.version)
        if isinstance(result, RegistryFailure):
            unmeasurable.append(
                UnmeasurableRequirement(
                    name=requirement.name,
                    declared=requirement.declared,
                    reason=result.reason,
                    ecosystem=requirement.ecosystem,
                )
            )
            continue
        dependency = result_to_dependency(requirement, result)
        measurements.append(measure_dependency(dependency))

    report = build_report(measurements, dependencies_discovered=requirements.discovered)
    return ScanReport(report.summary, tuple(report.measurements), tuple(unmeasurable))


def result_to_dependency(requirement: ExactRequirement, result: PyPIResult):
    """Combine a parsed requirement with adapter metadata into a domain object."""
    from .model import Dependency

    return Dependency(
        ecosystem=requirement.ecosystem,
        name=requirement.name,
        used_version=requirement.version,
        used_release_time=result.used_release_time,
        latest_stable_version=result.latest_stable_version,
        latest_stable_release_time=result.latest_stable_release_time,
    )


scan = scan_repository

__all__ = ["ScanReport", "result_to_dependency", "scan", "scan_repository"]
