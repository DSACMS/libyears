"""Injected supervised metadata only; admission precedes even cache reuse."""

from dataclasses import dataclass, field, replace
from datetime import datetime
from statistics import mean, median

from .maven import MavenCapability
from .maven_model import MavenAge, MavenReason
from .maven_registry import MavenPomDate, MavenTarget, RegistryFailure, pom_path
from .metric import libyears_between
from .model import MetricSummary


_METADATA_REASONS = frozenset({
    MavenReason.CATALOGUE_UNAVAILABLE, MavenReason.UNKNOWN_LATEST_ELIGIBILITY,
    MavenReason.AMBIGUOUS_LATEST_VERSION, MavenReason.NO_STABLE_RELEASE,
    MavenReason.TIME_BASIS_UNAVAILABLE, MavenReason.METADATA_WORKER_UNAVAILABLE,
    MavenReason.METADATA_BUDGET_EXCEEDED,
})


@dataclass(frozen=True, slots=True)
class SbomAge(MavenAge):
    """Reuse established time/value validation, with a distinct SBOM comparator."""

    comparator_basis: str = field(init=False, default='sbom_maven_central_convention')


def summarize_members(members):
    if members is None:
        return MetricSummary(None, None, None, None, None, None, None)
    values = [member.age.libyears for member in members if member.age is not None]
    population, measured = len(members), len(values)
    return MetricSummary(population, measured, measured / population if population else None,
                         sum(values, 0.0), mean(values) if values else None,
                         median(values) if values else None, max(values) if values else None)


def _aware(value):
    return isinstance(value, datetime) and value.utcoffset() is not None


def _target_reason(target, capability):
    if (not isinstance(target, MavenTarget)
            or (target.group_id, target.artifact_id) != (capability.group_id, capability.artifact_id)):
        return MavenReason.CATALOGUE_UNAVAILABLE
    if target.reason is not None:
        return target.reason if target.reason in _METADATA_REASONS else MavenReason.CATALOGUE_UNAVAILABLE
    try:
        pom_path(capability.group_id, capability.artifact_id, target.version)
    except RegistryFailure:
        return MavenReason.CATALOGUE_UNAVAILABLE
    if not _aware(target.retrieved_at):
        return MavenReason.CATALOGUE_UNAVAILABLE
    return None


def _date_reason(date, capability, version):
    if (not isinstance(date, MavenPomDate) or (date.group_id, date.artifact_id, date.version)
            != (capability.group_id, capability.artifact_id, version)):
        return MavenReason.TIME_BASIS_UNAVAILABLE
    if date.reason is not None:
        return date.reason if date.reason in _METADATA_REASONS else MavenReason.TIME_BASIS_UNAVAILABLE
    if not _aware(date.last_modified) or not _aware(date.retrieved_at):
        return MavenReason.TIME_BASIS_UNAVAILABLE
    return None


def measure_members(members, *, supervisor_factory):
    """No default factory: this offline slice cannot create production transport."""
    admitted = sorted((member for member in members if member.reason is None), key=lambda m: (
        m.identity.group_id, m.identity.artifact_id, m.identity.version,
        m.identity.type, m.identity.classifier or '', m.index))
    if not admitted:
        return members
    if supervisor_factory is None:
        raise TypeError('SBOM metadata factory is required')
    work = [(member, MavenCapability(member.identity.group_id, member.identity.artifact_id,
                                    member.identity.version)) for member in admitted]
    targets = {}
    dates = {}
    outcomes = {}
    with supervisor_factory(tuple(capability for member, capability in work)) as supervisor:
        for member, capability in work:
            ga = (capability.group_id, capability.artifact_id)
            if ga not in targets:
                targets[ga] = supervisor.select_target(capability)
            target = targets[ga]
            reason = _target_reason(target, capability)
            age = None
            if reason is None:
                for version in dict.fromkeys((target.version, capability.version)):
                    key = (*ga, version)
                    if key not in dates:
                        dates[key] = supervisor.pom_date(capability, version)
                    reason = _date_reason(dates[key], capability, version)
                    if reason is not None:
                        break
                if reason is None:
                    comparison = dates[(*ga, target.version)]
                    measured = dates[(*ga, capability.version)]
                    value, anomaly = libyears_between(measured.last_modified, comparison.last_modified)
                    age = SbomAge(target.version, measured.last_modified, comparison.last_modified,
                                  value, anomaly, catalogue_retrieved_at=target.retrieved_at)
            outcomes[member.index] = (age, reason)
    return tuple(replace(member, age=outcomes[member.index][0], reason=outcomes[member.index][1])
                 if member.index in outcomes else member for member in members)
