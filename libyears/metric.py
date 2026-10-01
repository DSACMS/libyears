"""Pure arithmetic for the CHAOSS Libyears metric."""

from __future__ import annotations

from datetime import datetime
from statistics import mean, median
from typing import Iterable

from .model import Dependency, DependencyMeasurement, MetricReport, MetricSummary

DAYS_PER_LIBYEAR = 365.25


def libyears_between(used_release_time: datetime, latest_stable_release_time: datetime) -> tuple[float, bool]:
    """Return ``(libyears, anomaly)`` for two UTC-aware timestamps."""
    probe = Dependency("_", "_", "_", used_release_time, "_", latest_stable_release_time)
    age_days = (probe.latest_stable_release_time - probe.used_release_time).total_seconds() / 86400
    anomaly = age_days < 0
    return max(age_days, 0) / DAYS_PER_LIBYEAR, anomaly


def measure_dependency(dependency: Dependency) -> DependencyMeasurement:
    """Calculate one dependency's Libyears value."""
    value, anomaly = libyears_between(dependency.used_release_time, dependency.latest_stable_release_time)
    return DependencyMeasurement(dependency, value, anomaly)


def calculate_summary(
    measurements: Iterable[DependencyMeasurement], *, dependencies_discovered: int | None = None
) -> MetricSummary:
    """Calculate aggregates from measured dependencies only."""
    values = [measurement.libyears for measurement in measurements]
    measured = len(values)
    discovered = measured if dependencies_discovered is None else dependencies_discovered
    if discovered < 0 or discovered < measured:
        raise ValueError("discovered dependency count is invalid")
    coverage = None if discovered == 0 else measured / discovered
    if not values:
        return MetricSummary(discovered, 0, coverage, 0.0, None, None, None)
    return MetricSummary(
        discovered, measured, coverage, sum(values), mean(values), median(values), max(values)
    )


def build_report(
    measurements: Iterable[DependencyMeasurement], *, dependencies_discovered: int | None = None
) -> MetricReport:
    """Build a report while preserving the measured dependency records."""
    records = tuple(measurements)
    return MetricReport(calculate_summary(records, dependencies_discovered=dependencies_discovered), records)
