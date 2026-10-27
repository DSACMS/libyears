"""Immutable domain objects used by the Libyears metric."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Sequence


def _utc(timestamp: datetime) -> datetime:
    """Return an aware UTC timestamp, rejecting ambiguous naive timestamps."""
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("timestamps must be timezone-aware")
    return timestamp.astimezone(timezone.utc)


@dataclass(frozen=True, slots=True)
class Dependency:
    """A dependency with both release timestamps resolved by an adapter."""

    ecosystem: str
    name: str
    used_version: str
    used_release_time: datetime
    latest_stable_version: str
    latest_stable_release_time: datetime
    version_source: str = "requirements_exact"

    def __post_init__(self) -> None:
        if not self.ecosystem or not self.name or not self.used_version:
            raise ValueError("ecosystem, name, and used_version are required")
        if not self.latest_stable_version:
            raise ValueError("latest_stable_version is required")
        object.__setattr__(self, "used_release_time", _utc(self.used_release_time))
        object.__setattr__(self, "latest_stable_release_time", _utc(self.latest_stable_release_time))


@dataclass(frozen=True, slots=True)
class RegistryResult:
    """Common release timestamps returned by a registry adapter."""

    name: str
    used_version: str
    used_release_time: datetime
    latest_stable_version: str
    latest_stable_release_time: datetime


@dataclass(frozen=True, slots=True)
class RegistryFailure:
    """Common machine-readable registry failure with a safe diagnostic."""

    name: str
    used_version: str
    reason: str
    diagnostic: str | None = None


@dataclass(frozen=True, slots=True)
class DependencyCandidate:
    """A source candidate with exact evidence ready for registry lookup."""

    ecosystem: str
    name: str
    registry_name: str
    declared: str
    used_version: str
    version_source: str


@dataclass(frozen=True, slots=True)
class UnmeasurableDependency:
    """A discovered dependency that cannot proceed to registry lookup."""

    ecosystem: str
    name: str
    declared: str
    reason: str


@dataclass(frozen=True, slots=True)
class SourceError:
    """A source-level failure with no fabricated dependency row."""

    ecosystem: str
    source: str
    reason: str


@dataclass(frozen=True, slots=True)
class SourceEvidence:
    """Human-readable declaration and exact-version evidence source names."""

    declaration_source: str
    snapshot_source: str | None
    format: str | None = None
    # Existing evidence omits format; rejected Yarn evidence explicitly uses null.
    include_format: bool = False


@dataclass(frozen=True, slots=True)
class SourceResult:
    """Common output of one concrete ecosystem dependency source."""

    ecosystem: str
    candidates: tuple[DependencyCandidate, ...]
    unmeasurable: tuple[UnmeasurableDependency, ...]
    source_errors: tuple[SourceError, ...]
    evidence: SourceEvidence
    dependencies_discovered: int | None
    measurement_available: bool
    source_present: bool = True
    diagnostics: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class DependencyMeasurement:
    """A dependency and its calculated Libyears value."""
    dependency: Dependency
    libyears: float
    timestamp_anomaly: bool = False


@dataclass(frozen=True, slots=True)
class MetricSummary:
    """Aggregate values for a repository scan."""
    dependencies_discovered: int | None
    dependencies_measured: int | None
    coverage: float | None
    total_libyears: float | None
    mean_libyears: float | None
    median_libyears: float | None
    max_libyears: float | None


@dataclass(frozen=True, slots=True)
class MetricReport:
    """The arithmetic portion of a complete metric report."""
    summary: MetricSummary
    measurements: Sequence[DependencyMeasurement]
