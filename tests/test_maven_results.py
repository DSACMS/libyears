"""Pure T001 summary counterexamples, independent of discovery or metadata I/O."""

from datetime import datetime, timezone
import unittest

from libyears.maven_model import (
    MavenAge, MavenArtifactKey, MavenAvailability, MavenCollection, MavenContext,
    MavenModelKey, MavenOccurrence, MavenOccurrenceKey, MavenPopulationState,
    MavenReason, MavenSource, MavenVersionBasis, MavenVersionFact, MavenView,
)
from libyears.maven_results import summarize_collection, summarize_sources


STAMP = datetime(2020, 1, 1, tzinfo=timezone.utc)


def row(source_id, name, value=None, *, view=MavenView.DECLARED,
        reason=MavenReason.UNSUPPORTED_VERSION):
    basis = (MavenVersionBasis.DECLARED if view == MavenView.DECLARED
             else MavenVersionBasis.OBSERVED)
    if value is None:
        fact = MavenVersionFact(basis, reason=reason)
    else:
        # Values are supplied established inputs; T001 never calculates an age.
        age = MavenAge('2', STAMP, STAMP, value)
        fact = MavenVersionFact(basis, version='1', age=age)
    return MavenOccurrence(
        MavenOccurrenceKey(source_id, 'base_model', MavenModelKey('g', name)),
        MavenArtifactKey('g', name, 'jar'), **{view.value: fact},
    )


def source(source_id, values=(), *, known=True):
    rows = tuple(row(source_id, str(index), value) for index, value in enumerate(values))
    collection = MavenCollection(
        MavenView.DECLARED, len(rows) if known else None, rows, True,
    )
    return MavenSource(MavenContext(source_id), collection)


def unavailable(source_id, count=None):
    return MavenSource(
        MavenContext(source_id),
        MavenCollection(MavenView.DECLARED, count, (), False, MavenReason.UNSUPPORTED_MODEL),
    )


class MavenResultsTests(unittest.TestCase):
    def assert_summary(self, result, expected):
        summary = result.summary
        self.assertEqual((
            summary.dependencies_discovered, summary.dependencies_measured,
            summary.coverage, summary.total_libyears, summary.mean_libyears,
            summary.median_libyears, summary.max_libyears,
        ), expected)

    def test_known_population_with_measurable_rows(self):
        result = summarize_sources((source('pom.xml', (1.0, 3.0)),)).declared
        self.assert_summary(result, (2, 2, 1.0, 4.0, 2.0, 2.0, 3.0))
        self.assertEqual(result.availability, MavenAvailability.AVAILABLE)
        self.assertEqual(result.population_state, MavenPopulationState.KNOWN)

    def test_partial_row_failures_keep_known_denominator(self):
        result = summarize_sources((source('pom.xml', (2.0, None)),)).declared
        self.assert_summary(result, (2, 1, 0.5, 2.0, 2.0, 2.0, 2.0))
        self.assertEqual(result.availability, MavenAvailability.PARTIAL)
        self.assertIn(MavenReason.UNSUPPORTED_VERSION, result.reasons)

    def test_all_missing_bom_versions_are_known_rows_not_unknown_collection(self):
        current = source('pom.xml', (None, None))
        self.assertTrue(current.declared.accepted)
        self.assertEqual(len(current.declared.rows), 2)
        for record in current.declared.rows:
            self.assertIsNone(record.declared.request)
            self.assertIsNone(record.declared.version)
        result = summarize_collection(current.declared)
        self.assert_summary(result, (2, 0, 0.0, 0.0, None, None, None))
        self.assertEqual(result.availability, MavenAvailability.PARTIAL)

    def test_all_policy_refused_exact_versions_keep_known_rows(self):
        records = []
        for name in ('a', 'b'):
            fact = MavenVersionFact(MavenVersionBasis.DECLARED, version='1',
                                    reason=MavenReason.COMPARATOR_REFUSED)
            records.append(MavenOccurrence(
                MavenOccurrenceKey('pom.xml', 'base_model', MavenModelKey('g', name)),
                declared=fact,
            ))
        collection = MavenCollection(MavenView.DECLARED, 2, tuple(records), True)
        self.assert_summary(summarize_collection(collection), (2, 0, 0.0, 0.0, None, None, None))
        self.assertEqual(summarize_collection(collection).reasons, (MavenReason.COMPARATOR_REFUSED,))

    def test_all_row_failure_reasons_preserve_denominator_with_successful_sibling(self):
        for reason in (MavenReason.UNSUPPORTED_VERSION, MavenReason.COMPARATOR_REFUSED,
                       MavenReason.POLICY_UNKNOWN, MavenReason.TIME_BASIS_UNAVAILABLE,
                       MavenReason.METADATA_WORKER_UNAVAILABLE):
            rows = tuple(row('a/pom.xml', name, reason=reason) for name in ('a', 'b'))
            failed = MavenSource(MavenContext('a/pom.xml'),
                                 MavenCollection(MavenView.DECLARED, 2, rows, True))
            with self.subTest(reason=reason):
                result = summarize_sources((failed, source('b/pom.xml', (3.0,)))).declared
                self.assert_summary(result, (3, 1, 1 / 3, 3.0, 3.0, 3.0, 3.0))

    def test_all_sources_admitted_with_some_row_failures(self):
        result = summarize_sources((source('a/pom.xml', (1.0, None)),
                                    source('b/pom.xml', (3.0,)))).declared
        self.assert_summary(result, (3, 2, 2 / 3, 4.0, 2.0, 2.0, 3.0))

    def test_known_whole_unavailable_sibling_makes_coverage_null(self):
        result = summarize_sources((source('a/pom.xml', (3.0, None)),
                                    unavailable('b/pom.xml', 4))).declared
        self.assert_summary(result, (6, 1, None, 3.0, 3.0, 3.0, 3.0))
        self.assertEqual(result.availability, MavenAvailability.PARTIAL)

    def test_unknown_whole_unavailable_sibling_preserves_measured_subset(self):
        result = summarize_sources((source('a/pom.xml', (2.0,)),
                                    unavailable('b/pom.xml'))).declared
        self.assert_summary(result, (None, 1, None, 2.0, 2.0, 2.0, 2.0))
        self.assertEqual(result.population_state, MavenPopulationState.UNKNOWN)

    def test_every_collection_unavailable_retains_only_independently_known_n(self):
        for second_count, expected_count in ((3, 5), (None, None)):
            with self.subTest(second_count=second_count):
                result = summarize_sources((unavailable('a/pom.xml', 2),
                                            unavailable('b/pom.xml', second_count))).declared
                self.assert_summary(result, (expected_count, None, None, None, None, None, None))
                self.assertEqual(result.availability, MavenAvailability.UNAVAILABLE)

    def test_certified_empty_source_adds_zero_to_admitted_sibling(self):
        result = summarize_sources((source('a/pom.xml'),
                                    source('b/pom.xml', (2.0, None)))).declared
        self.assert_summary(result, (2, 1, 0.5, 2.0, 2.0, 2.0, 2.0))

    def test_every_source_certified_empty(self):
        result = summarize_sources((source('a/pom.xml'), source('b/pom.xml'))).declared
        self.assert_summary(result, (0, 0, None, 0.0, None, None, None))
        self.assertEqual(result.availability, MavenAvailability.AVAILABLE)

    def test_zero_measured_with_unavailable_sibling_keeps_coverage_null(self):
        result = summarize_sources((source('a/pom.xml', (None,)),
                                    unavailable('b/pom.xml', 2))).declared
        self.assert_summary(result, (3, 0, None, 0.0, None, None, None))

    def test_empty_admitted_source_with_unavailable_sibling_is_partial_zero(self):
        result = summarize_sources((source('a/pom.xml'), unavailable('b/pom.xml', 2))).declared
        self.assert_summary(result, (2, 0, None, 0.0, None, None, None))

    def test_unknown_population_with_safe_rows_remains_partial_not_unavailable(self):
        for values, expected in (((2.0, None), (None, 1, None, 2.0, 2.0, 2.0, 2.0)),
                                 ((None,), (None, 0, None, 0.0, None, None, None))):
            with self.subTest(values=values):
                result = summarize_sources((source('pom.xml', values, known=False),)).declared
                self.assert_summary(result, expected)
                self.assertEqual(result.availability, MavenAvailability.PARTIAL)

    def test_unknown_population_without_safe_rows_is_unavailable(self):
        result = summarize_sources((unavailable('pom.xml'),)).declared
        self.assert_summary(result, (None, None, None, None, None, None, None))

    def test_known_zero_population_without_collection_authority_is_not_certified_empty(self):
        result = summarize_sources((unavailable('pom.xml', 0),)).declared
        self.assert_summary(result, (0, None, None, None, None, None, None))

    def test_unknown_discovery_forces_null_population_but_preserves_safe_values(self):
        result = summarize_sources((source('pom.xml', (2.0,)),), discovery_complete=False).declared
        self.assert_summary(result, (None, 1, None, 2.0, 2.0, 2.0, 2.0))
        self.assertIn(MavenReason.DISCOVERY_UNAVAILABLE, result.reasons)
        self.assertEqual(result.availability, MavenAvailability.PARTIAL)

    def test_no_source_collection_never_fabricates_numeric_summary(self):
        for complete in (True, False):
            with self.subTest(complete=complete):
                result = summarize_sources((), discovery_complete=complete).declared
                self.assert_summary(result, (None, None, None, None, None, None, None))

    def test_initial_observed_does_not_copy_any_declared_value_or_denominator(self):
        summaries = summarize_sources((source('pom.xml', (2.0, 3.0)),))
        self.assertEqual(summaries.declared.summary.total_libyears, 5.0)
        self.assert_summary(summaries.observed, (None, None, None, None, None, None, None))
        self.assertIn(MavenReason.OBSERVED_READER_UNAVAILABLE, summaries.observed.reasons)
        self.assertFalse(hasattr(summaries, 'summary'))
        self.assertFalse(hasattr(summaries, 'total_libyears'))

    def test_paired_and_observed_only_model_cases_keep_independent_population(self):
        declared_row = row('pom.xml', 'shared', 4.0)
        observed_row = row('pom.xml', 'shared', 1.0, view=MavenView.OBSERVED)
        paired = MavenOccurrence(declared_row.key, declared_row.artifact_key,
                                 declared=declared_row.declared, observed=observed_row.observed)
        observed_only = row('pom.xml', 'observed-only', 3.0, view=MavenView.OBSERVED)
        declared = MavenCollection(MavenView.DECLARED, 1, (paired,), True)
        observed = MavenCollection(MavenView.OBSERVED, 2, (paired, observed_only), True)
        summaries = summarize_sources((MavenSource(MavenContext('pom.xml'), declared, observed),))
        self.assert_summary(summaries.declared, (1, 1, 1.0, 4.0, 4.0, 4.0, 4.0))
        self.assert_summary(summaries.observed, (2, 2, 1.0, 4.0, 2.0, 2.0, 3.0))

    def test_each_views_unavailability_is_independent(self):
        observed_row = row('pom.xml', 'observed-only', 3.0, view=MavenView.OBSERVED)
        declared = MavenCollection(MavenView.DECLARED, None, (), False, MavenReason.UNSUPPORTED_MODEL)
        observed = MavenCollection(MavenView.OBSERVED, 1, (observed_row,), True)
        result = summarize_sources((MavenSource(MavenContext('pom.xml'), declared, observed),))
        self.assert_summary(result.declared, (None, None, None, None, None, None, None))
        self.assert_summary(result.observed, (1, 1, 1.0, 3.0, 3.0, 3.0, 3.0))

    def test_observed_partial_composition_uses_its_own_rows_and_population(self):
        observed_rows = (row('a/pom.xml', 'ok', 2.0, view=MavenView.OBSERVED),
                         row('a/pom.xml', 'failed', view=MavenView.OBSERVED))
        declared = source('a/pom.xml', (99.0,)).declared
        observed = MavenCollection(MavenView.OBSERVED, 2, observed_rows, True)
        first = MavenSource(MavenContext('a/pom.xml'), declared, observed)
        for unavailable_count, expected_count in ((3, 5), (None, None)):
            second = MavenSource(
                MavenContext('b/pom.xml'), source('b/pom.xml').declared,
                MavenCollection(MavenView.OBSERVED, unavailable_count, (), False,
                                MavenReason.UNSUPPORTED_MODEL),
            )
            with self.subTest(unavailable_count=unavailable_count):
                result = summarize_sources((first, second))
                self.assert_summary(result.declared, (1, 1, 1.0, 99.0, 99.0, 99.0, 99.0))
                self.assert_summary(result.observed,
                                    (expected_count, 1, None, 2.0, 2.0, 2.0, 2.0))
                self.assertEqual(result.observed.availability, MavenAvailability.PARTIAL)

    def test_statistics_use_union_not_average_of_source_statistics(self):
        result = summarize_sources((source('a/pom.xml', (1.0, 2.0, 100.0)),
                                    source('b/pom.xml', (200.0,)))).declared
        self.assert_summary(result, (4, 4, 1.0, 303.0, 75.75, 51.0, 200.0))

    def test_repeated_module_requirements_are_not_deduplicated(self):
        result = summarize_sources((source('a/pom.xml', (2.0,)),
                                    source('b/pom.xml', (2.0,)))).declared
        self.assert_summary(result, (2, 2, 1.0, 4.0, 2.0, 2.0, 2.0))

    def test_duplicate_source_inputs_refuse_instead_of_double_counting(self):
        current = source('pom.xml', (2.0,))
        with self.assertRaises(ValueError):
            summarize_sources((current, current))

    def test_finite_rows_cannot_produce_nonfinite_total(self):
        with self.assertRaises(ValueError):
            summarize_sources((source('pom.xml', (1e308, 1e308)),))
