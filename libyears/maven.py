"""Local Maven admission boundary. Metadata transport is not enabled here."""

from dataclasses import dataclass, replace

from .maven_model import MavenOccurrenceKey, MavenReason, MavenSource
from .maven_policy import source_policy
from .maven_project import declared_sources
from .maven_version import VersionError, is_snapshot, parse_version


@dataclass(frozen=True, slots=True)
class MavenCapability:
    """One admitted occurrence; sharing GA evidence never transfers this authority."""

    group_id: str
    artifact_id: str
    version: str


@dataclass(frozen=True, slots=True)
class MavenAdmission:
    sources: tuple[MavenSource, ...]
    work: tuple[tuple[MavenOccurrenceKey, MavenCapability], ...]

    @property
    def capabilities(self):
        return tuple(capability for key, capability in self.work)


def admit_sources(graph, reader):
    """Retain population and facts; mint lookup work only after local policy."""
    sources = []
    capabilities = []
    for source in declared_sources(graph):
        decision = source_policy(graph, source.context.source_id, reader)
        rows = []
        for row in source.declared.rows:
            fact = row.declared
            reason = decision.reason
            if row.scope == 'system':
                reason = MavenReason.COMPARATOR_REFUSED
            if (fact.version is not None and reason is None and row.artifact_key is not None
                    and fact.reason == MavenReason.TIME_BASIS_UNAVAILABLE):
                try:
                    parsed = parse_version(fact.version)
                    if is_snapshot(parsed):
                        raise VersionError('snapshot')
                except VersionError:
                    reason = MavenReason.UNSUPPORTED_VERSION
                else:
                    key = row.key.model_key
                    capabilities.append((row.key, MavenCapability(key.group_id, key.artifact_id,
                                                                  fact.version)))
            if reason is not None and fact.version is not None:
                row = replace(row, declared=replace(fact, age=None, reason=reason))
            rows.append(row)
        sources.append(replace(source, declared=replace(source.declared, rows=tuple(rows))))
    return MavenAdmission(tuple(sources), tuple(capabilities))


def admitted_lookups(admission, lookup):
    """Injected verification seam; no transport/default lookup exists in T006."""
    return tuple((key, lookup(capability)) for key, capability in admission.work)
