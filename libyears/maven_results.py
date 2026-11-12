"""Pure S6 collection summaries; inputs are already established Maven records."""

from math import isfinite
from statistics import mean, median

from .maven_model import (
    MavenAvailability, MavenCollection, MavenPopulationState, MavenReason,
    MavenSource, MavenSummaries, MavenView, MavenViewSummary,
)
from .model import MetricSummary


def summarize_collection(collection: MavenCollection) -> MavenViewSummary:
    return _summarize((collection,), collection.view, discovery_complete=True)


def summarize_sources(
    sources: tuple[MavenSource, ...], *, discovery_complete: bool = True,
) -> MavenSummaries:
    """Compose each view independently, retaining every module occurrence."""
    if type(sources) is not tuple or type(discovery_complete) is not bool:
        raise ValueError('invalid Maven source inventory')
    source_ids = [source.context.source_id for source in sources]
    if len(set(source_ids)) != len(source_ids):
        raise ValueError('duplicate Maven source identity')
    return MavenSummaries(
        _summarize(tuple(source.declared for source in sources), MavenView.DECLARED,
                   discovery_complete=discovery_complete),
        _summarize(tuple(source.observed for source in sources), MavenView.OBSERVED,
                   discovery_complete=discovery_complete),
    )


def _summarize(collections, view, *, discovery_complete):
    reasons = []
    values = []
    accepted = False
    complete_population = bool(collections) and discovery_complete
    complete_collections = True
    partial = not discovery_complete
    discovered = 0
    if not discovery_complete:
        reasons.append(MavenReason.DISCOVERY_UNAVAILABLE)
    for collection in collections:
        if collection.population_count is None:
            complete_population = False
        else:
            discovered += collection.population_count
        if collection.reason is not None:
            reasons.append(collection.reason)
        if not collection.accepted:
            complete_collections = False
            partial = True
            continue
        accepted = True
        if collection.population_count is None:
            partial = True
        for row in collection.rows:
            fact = getattr(row, view.value)
            if fact.age is None:
                partial = True
                reasons.append(fact.reason)
            else:
                values.append(fact.age.libyears)
    if not complete_population:
        reasons.append(MavenReason.POPULATION_UNKNOWN)
    population = discovered if complete_population else None
    state = (MavenPopulationState.KNOWN if complete_population
             else MavenPopulationState.UNKNOWN)
    unique_reasons = tuple(dict.fromkeys(reasons))
    if not accepted:
        return MavenViewSummary(
            view, state, MavenAvailability.UNAVAILABLE,
            MetricSummary(population, None, None, None, None, None, None),
            unique_reasons,
        )
    measured = len(values)
    coverage = None
    if complete_population and complete_collections and discovered > 0:
        coverage = measured / discovered
    total = sum(values, 0.0)
    if not isfinite(total):
        raise ValueError('Maven total must be finite')
    summary = MetricSummary(
        population, measured, coverage, total,
        mean(values) if values else None,
        median(values) if values else None,
        max(values) if values else None,
    )
    availability = MavenAvailability.PARTIAL if partial else MavenAvailability.AVAILABLE
    return MavenViewSummary(view, state, availability, summary, unique_reasons)
