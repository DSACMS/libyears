"""Maven-only evidence records; no parsing, lookup, selection or age calculation."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from math import isfinite

from .model import MetricSummary


class MavenView(StrEnum):
    DECLARED = 'declared'
    OBSERVED = 'observed'


class MavenVersionBasis(StrEnum):
    DECLARED = 'supported_local_base_model_request'
    OBSERVED = 'retained_dependency_system_selection'


class MavenFieldBasis(StrEnum):
    DEPENDENCY = 'dependency'
    INHERITED_DEPENDENCY = 'inherited_dependency'
    PROPERTY = 'property'
    CONSUMER_MANAGEMENT = 'consumer_local_management'
    INHERITED_MANAGEMENT = 'inherited_management'
    DEFAULT = 'supported_default'


class MavenReason(StrEnum):
    DISCOVERY_UNAVAILABLE = 'maven_discovery_unavailable'
    POPULATION_UNKNOWN = 'maven_population_unknown'
    UNSUPPORTED_MODEL = 'maven_unsupported_model'
    UNSUPPORTED_VERSION = 'maven_unsupported_version'
    COMPARATOR_REFUSED = 'maven_comparator_refused'
    POLICY_UNKNOWN = 'maven_policy_unknown'
    POLICY_INPUT_UNAVAILABLE = 'maven_policy_input_unavailable'
    POLICY_BUDGET_EXCEEDED = 'maven_policy_budget_exceeded'
    OBSERVED_READER_UNAVAILABLE = 'maven_observed_reader_unavailable'
    CATALOGUE_UNAVAILABLE = 'maven_catalogue_unavailable'
    UNKNOWN_LATEST_ELIGIBILITY = 'unknown_latest_eligibility'
    AMBIGUOUS_LATEST_VERSION = 'ambiguous_latest_version'
    NO_STABLE_RELEASE = 'no_stable_release'
    TIME_BASIS_UNAVAILABLE = 'maven_time_basis_unavailable'
    METADATA_WORKER_UNAVAILABLE = 'maven_metadata_worker_unavailable'
    METADATA_BUDGET_EXCEEDED = 'maven_metadata_budget_exceeded'
    PLURAL_PROJECTION_UNAVAILABLE = 'maven_plural_projection_unavailable'


class MavenPopulationState(StrEnum):
    KNOWN = 'known'
    UNKNOWN = 'unknown'


class MavenAvailability(StrEnum):
    AVAILABLE = 'available'
    PARTIAL = 'partial'
    UNAVAILABLE = 'unavailable'


def _source_id(value: str) -> None:
    # Representation only; filesystem containment/race checks belong to T002.
    if (not isinstance(value, str) or not value or '\\' in value
            or any(part in ('', '.', '..') for part in value.split('/'))
            or ':' in value or any(ord(char) < 32 for char in value)):
        raise ValueError('invalid Maven source identity')


def _nonempty(value: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError('empty Maven identity')


def _reason(value: MavenReason | None) -> None:
    if value is not None and not isinstance(value, MavenReason):
        raise ValueError('unknown Maven reason')


@dataclass(frozen=True, slots=True)
class MavenDiscovery:
    complete: bool
    source_ids: tuple[str, ...] = ()
    reason: MavenReason | None = None

    def __post_init__(self):
        if type(self.complete) is not bool or type(self.source_ids) is not tuple:
            raise ValueError('invalid Maven discovery state')
        for source_id in self.source_ids:
            _source_id(source_id)
        if len(set(self.source_ids)) != len(self.source_ids):
            raise ValueError('duplicate Maven source identity')
        _reason(self.reason)
        if ((self.complete and self.reason is not None)
                or (not self.complete and self.reason is None)):
            raise ValueError('discovery completion and reason disagree')


@dataclass(frozen=True, slots=True)
class MavenContext:
    source_id: str
    context_id: str = 'base_model'
    parent_sources: tuple[str, ...] = ()

    def __post_init__(self):
        _source_id(self.source_id)
        _nonempty(self.context_id)
        if type(self.parent_sources) is not tuple:
            raise ValueError('parent identities must be immutable')
        for source_id in self.parent_sources:
            _source_id(source_id)


@dataclass(frozen=True, slots=True)
class MavenModelKey:
    group_id: str
    artifact_id: str
    type: str = 'jar'
    classifier: str | None = None

    def __post_init__(self):
        for value in (self.group_id, self.artifact_id, self.type):
            _nonempty(value)
        if self.classifier is not None:
            _nonempty(self.classifier)


@dataclass(frozen=True, slots=True)
class MavenArtifactKey:
    group_id: str
    artifact_id: str
    extension: str
    classifier: str | None = None

    def __post_init__(self):
        for value in (self.group_id, self.artifact_id, self.extension):
            _nonempty(value)
        if self.classifier is not None:
            _nonempty(self.classifier)


@dataclass(frozen=True, slots=True)
class MavenOccurrenceKey:
    source_id: str
    context_id: str
    model_key: MavenModelKey

    def __post_init__(self):
        _source_id(self.source_id)
        _nonempty(self.context_id)
        if not isinstance(self.model_key, MavenModelKey):
            raise ValueError('invalid Maven model key')


@dataclass(frozen=True, slots=True)
class MavenFieldOrigin:
    source_id: str
    field_name: str
    basis: MavenFieldBasis

    def __post_init__(self):
        _source_id(self.source_id)
        _nonempty(self.field_name)
        if not isinstance(self.basis, MavenFieldBasis):
            raise ValueError('unknown Maven field basis')


@dataclass(frozen=True, slots=True)
class MavenAge:
    """Already established evidence/value; constructing this never calculates age."""

    comparison_version: str
    measured_version_pom_last_modified: datetime
    comparison_version_pom_last_modified: datetime
    libyears: float
    timestamp_order_anomaly: bool = False
    comparator_basis: str = field(init=False, default='conventional_central')
    time_basis: str = field(init=False, default='maven_conventional_pom_last_modified')
    ordering_basis: str = field(init=False, default='maven_comparable_version_3_9_11')
    eligibility_policy: str = field(init=False, default='maven_conservative_stable_v1')
    limitations: tuple[str, ...] = field(init=False, default=(
        'publication_history_not_established', 'variant_availability_not_established',
    ))

    def __post_init__(self):
        _nonempty(self.comparison_version)
        if (type(self.libyears) not in (int, float) or not isfinite(self.libyears)
                or self.libyears < 0 or type(self.timestamp_order_anomaly) is not bool):
            raise ValueError('invalid established Maven age')
        for name in ('measured_version_pom_last_modified',
                     'comparison_version_pom_last_modified'):
            timestamp = getattr(self, name)
            if not isinstance(timestamp, datetime) or timestamp.utcoffset() is None:
                raise ValueError('Maven time evidence must be timezone-aware')
            object.__setattr__(self, name, timestamp.astimezone(timezone.utc))


@dataclass(frozen=True, slots=True)
class MavenVersionFact:
    version_basis: MavenVersionBasis
    request: str | None = None
    version: str | None = None
    origins: tuple[MavenFieldOrigin, ...] = ()
    age: MavenAge | None = None
    reason: MavenReason | None = None

    def __post_init__(self):
        if not isinstance(self.version_basis, MavenVersionBasis):
            raise ValueError('unknown Maven version basis')
        for value in (self.request, self.version):
            if value is not None:
                _nonempty(value)
        if type(self.origins) is not tuple:
            raise ValueError('field origins must be immutable')
        if any(not isinstance(origin, MavenFieldOrigin) for origin in self.origins):
            raise ValueError('invalid Maven field origin')
        if self.age is not None and not isinstance(self.age, MavenAge):
            raise ValueError('invalid established Maven age record')
        _reason(self.reason)
        if self.age is None:
            if self.reason is None:
                raise ValueError('unmeasured Maven fact needs a reason')
        elif self.version is None or self.reason is not None:
            raise ValueError('measured Maven fact needs an exact version and no failure')

    @property
    def availability(self) -> MavenAvailability:
        if self.version is None:
            return MavenAvailability.UNAVAILABLE
        return MavenAvailability.AVAILABLE

    @property
    def age_availability(self) -> MavenAvailability:
        if self.age is None:
            return MavenAvailability.UNAVAILABLE
        return MavenAvailability.AVAILABLE


@dataclass(frozen=True, slots=True)
class MavenOccurrence:
    key: MavenOccurrenceKey
    artifact_key: MavenArtifactKey | None = None
    scope: str | None = None
    optional: bool | None = None
    declared: MavenVersionFact | None = None
    observed: MavenVersionFact | None = None

    def __post_init__(self):
        if not isinstance(self.key, MavenOccurrenceKey):
            raise ValueError('invalid Maven occurrence key')
        if self.optional is not None and type(self.optional) is not bool:
            raise ValueError('invalid Maven optional fact')
        if self.scope is not None:
            _nonempty(self.scope)
        if self.declared is None and self.observed is None:
            raise ValueError('known occurrence needs a view record')
        for fact, basis in ((self.declared, MavenVersionBasis.DECLARED),
                            (self.observed, MavenVersionBasis.OBSERVED)):
            if fact is not None and (not isinstance(fact, MavenVersionFact)
                                     or fact.version_basis != basis):
                raise ValueError('Maven view and version basis disagree')
        if self.artifact_key is not None:
            if not isinstance(self.artifact_key, MavenArtifactKey):
                raise ValueError('invalid Maven artifact key')
            model = self.key.model_key
            if (model.group_id, model.artifact_id) != (
                    self.artifact_key.group_id, self.artifact_key.artifact_id):
                raise ValueError('Maven model and artifact identity disagree')
        if self.artifact_key is None and any(
                fact is not None and fact.age is not None
                for fact in (self.declared, self.observed)):
            raise ValueError('measured occurrence needs supported artifact identity')


@dataclass(frozen=True, slots=True)
class MavenCollection:
    """Accepted safe rows or certified emptiness, distinct from row age success."""

    view: MavenView
    population_count: int | None
    rows: tuple[MavenOccurrence, ...]
    accepted: bool
    reason: MavenReason | None = None

    def __post_init__(self):
        if not isinstance(self.view, MavenView) or type(self.accepted) is not bool:
            raise ValueError('invalid Maven collection state')
        if self.population_count is not None and (
                type(self.population_count) is not int or self.population_count < 0):
            raise ValueError('invalid Maven population count')
        if type(self.rows) is not tuple:
            raise ValueError('Maven collection rows must be immutable')
        _reason(self.reason)
        if not self.accepted:
            if self.rows or self.reason is None:
                raise ValueError('unavailable collection has no rows and needs a reason')
            return
        if not self.rows and self.population_count != 0:
            raise ValueError('accepted collection needs safe rows or certified emptiness')
        if self.population_count is not None and self.population_count != len(self.rows):
            raise ValueError('known population must include every occurrence record')
        keys = set()
        for row in self.rows:
            if not isinstance(row, MavenOccurrence):
                raise ValueError('invalid Maven occurrence record')
            if row.key in keys:
                raise ValueError('duplicate Maven occurrence identity')
            keys.add(row.key)
            if getattr(row, self.view.value) is None:
                raise ValueError('collection cannot borrow the other view')

    @property
    def population_state(self) -> MavenPopulationState:
        if self.population_count is None:
            return MavenPopulationState.UNKNOWN
        return MavenPopulationState.KNOWN


def unavailable_observed_collection() -> MavenCollection:
    return MavenCollection(
        MavenView.OBSERVED, None, (), False, MavenReason.OBSERVED_READER_UNAVAILABLE,
    )


@dataclass(frozen=True, slots=True)
class MavenSource:
    context: MavenContext
    declared: MavenCollection
    observed: MavenCollection = field(default_factory=unavailable_observed_collection)

    def __post_init__(self):
        if not isinstance(self.context, MavenContext):
            raise ValueError('invalid Maven source context')
        for collection, view in ((self.declared, MavenView.DECLARED),
                                 (self.observed, MavenView.OBSERVED)):
            if not isinstance(collection, MavenCollection) or collection.view != view:
                raise ValueError('source and collection view disagree')
            for row in collection.rows:
                if (row.key.source_id, row.key.context_id) != (
                        self.context.source_id, self.context.context_id):
                    raise ValueError('occurrence belongs to another source context')


@dataclass(frozen=True, slots=True)
class MavenViewSummary:
    view: MavenView
    population_state: MavenPopulationState
    availability: MavenAvailability
    summary: MetricSummary
    reasons: tuple[MavenReason, ...] = ()

    def __post_init__(self):
        if (not isinstance(self.view, MavenView)
                or not isinstance(self.population_state, MavenPopulationState)
                or not isinstance(self.availability, MavenAvailability)
                or not isinstance(self.summary, MetricSummary)
                or type(self.reasons) is not tuple):
            raise ValueError('invalid Maven summary record')
        for reason in self.reasons:
            if not isinstance(reason, MavenReason):
                raise ValueError('unknown Maven summary reason')


@dataclass(frozen=True, slots=True)
class MavenSummaries:
    """Two independent answers; deliberately no combined Maven total."""

    declared: MavenViewSummary
    observed: MavenViewSummary

    def __post_init__(self):
        for result, view in ((self.declared, MavenView.DECLARED),
                             (self.observed, MavenView.OBSERVED)):
            if not isinstance(result, MavenViewSummary) or result.view != view:
                raise ValueError('summary and Maven view disagree')
