"""T001 records only: these constructed facts are not a retained-evidence reader."""

from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone
import unittest

from libyears.maven_model import (
    MavenAge, MavenArtifactKey, MavenAvailability, MavenCollection, MavenContext,
    MavenDiscovery, MavenFieldBasis, MavenFieldOrigin, MavenModelKey,
    MavenOccurrence, MavenOccurrenceKey, MavenReason, MavenSource, MavenSummaries,
    MavenVersionBasis, MavenVersionFact, MavenView,
)


def established_age(value=1.0):
    stamp = datetime(2020, 1, 1, tzinfo=timezone.utc)
    return MavenAge('2', stamp, stamp + timedelta(days=365.25 * value), value)


def occurrence(source='pom.xml', name='example', value=None, *, observed=False):
    basis = MavenVersionBasis.OBSERVED if observed else MavenVersionBasis.DECLARED
    if value is None:
        fact = MavenVersionFact(basis, reason=MavenReason.UNSUPPORTED_VERSION)
    else:
        fact = MavenVersionFact(basis, version='1', age=established_age(value))
    kwargs = {'observed' if observed else 'declared': fact}
    return MavenOccurrence(
        MavenOccurrenceKey(source, 'base_model', MavenModelKey('org.example', name)),
        MavenArtifactKey('org.example', name, 'jar'), **kwargs,
    )


def paired_source_fixture():
    """Prospective model-only views, never a runtime retained-selection reader."""
    stamp = datetime(2020, 1, 1, tzinfo=timezone.utc)
    freshness = datetime(2026, 11, 12, tzinfo=timezone.utc)
    declared = MavenVersionFact(MavenVersionBasis.DECLARED, version='1', request='1',
        age=MavenAge('4', stamp, stamp + timedelta(days=365.25), 1.0,
                     catalogue_retrieved_at=freshness))
    observed = MavenVersionFact(MavenVersionBasis.OBSERVED, version='3',
        age=MavenAge('4', stamp, stamp + timedelta(days=365.25 * 2), 2.0,
                     catalogue_retrieved_at=freshness))
    key = MavenOccurrenceKey('pom.xml', 'base_model', MavenModelKey('g', 'a'))
    row = MavenOccurrence(key, MavenArtifactKey('g', 'a', 'jar'), declared=declared, observed=observed)
    return MavenSource(MavenContext('pom.xml'),
        MavenCollection(MavenView.DECLARED, 1, (row,), True),
        MavenCollection(MavenView.OBSERVED, 1, (row,), True))


class MavenModelTests(unittest.TestCase):
    def test_module_context_and_case_are_part_of_occurrence_identity(self):
        root = occurrence()
        module = occurrence('module/pom.xml')
        changed_case = MavenOccurrenceKey(
            'pom.xml', 'base_model', MavenModelKey('Org.Example', 'example'),
        )
        self.assertNotEqual(root.key, module.key)
        self.assertNotEqual(root.key, changed_case)
        self.assertEqual(root.key.model_key, MavenModelKey('org.example', 'example', 'jar'))

    def test_model_keys_preserve_handler_aliases_without_mapping_them(self):
        implicit_tests = MavenModelKey('g', 'a', 'test-jar')
        explicit_tests = MavenModelKey('g', 'a', 'test-jar', 'tests')
        jar_tests = MavenModelKey('g', 'a', 'jar', 'tests')
        self.assertEqual(len({implicit_tests, explicit_tests, jar_tests}), 3)
        artifact = MavenArtifactKey('g', 'a', 'jar', 'tests')
        self.assertEqual(artifact.classifier, 'tests')
        with self.assertRaises(ValueError):
            MavenModelKey('g', 'a', classifier='')

    def test_nullable_fact_keeps_origin_and_known_occurrence(self):
        origin = MavenFieldOrigin('parent/pom.xml', 'version', MavenFieldBasis.INHERITED_MANAGEMENT)
        fact = MavenVersionFact(
            MavenVersionBasis.DECLARED, origins=(origin,),
            reason=MavenReason.UNSUPPORTED_VERSION,
        )
        self.assertIsNone(fact.request)
        self.assertIsNone(fact.version)
        self.assertIsNone(fact.age)
        self.assertEqual(fact.origins[0].source_id, 'parent/pom.xml')
        self.assertEqual(fact.availability, MavenAvailability.UNAVAILABLE)

    def test_available_version_can_have_unavailable_age(self):
        fact = MavenVersionFact(
            MavenVersionBasis.DECLARED, request='[1]', version='1',
            reason=MavenReason.COMPARATOR_REFUSED,
        )
        self.assertEqual(fact.request, '[1]')
        self.assertEqual(fact.availability, MavenAvailability.AVAILABLE)
        self.assertEqual(fact.age_availability, MavenAvailability.UNAVAILABLE)

    def test_distinct_views_can_share_one_occurrence_without_replacing_versions(self):
        declared = MavenVersionFact(MavenVersionBasis.DECLARED, request='1', version='1',
                                    reason=MavenReason.TIME_BASIS_UNAVAILABLE)
        observed = MavenVersionFact(MavenVersionBasis.OBSERVED, version='3',
                                    reason=MavenReason.TIME_BASIS_UNAVAILABLE)
        row = MavenOccurrence(occurrence().key, declared=declared, observed=observed)
        self.assertEqual((row.declared.version, row.observed.version), ('1', '3'))
        self.assertNotEqual(row.declared.version_basis, row.observed.version_basis)
        self.assertNotIn('version', {item.name for item in fields(row.key)})

    def test_other_view_is_never_a_collection_fallback(self):
        with self.assertRaises(ValueError):
            MavenCollection(MavenView.OBSERVED, 1, (occurrence(),), True)
        with self.assertRaises(ValueError):
            MavenOccurrence(occurrence().key, observed=occurrence().declared)

    def test_initial_source_defaults_to_unavailable_observed(self):
        declared = MavenCollection(MavenView.DECLARED, 1, (occurrence(),), True)
        source = MavenSource(MavenContext('pom.xml'), declared)
        self.assertFalse(source.observed.accepted)
        self.assertIsNone(source.observed.population_count)
        self.assertEqual(source.observed.rows, ())
        self.assertEqual(source.observed.reason, MavenReason.OBSERVED_READER_UNAVAILABLE)
        self.assertEqual([item.name for item in fields(MavenSummaries)], ['declared', 'observed'])

    def test_records_and_nested_collections_are_immutable(self):
        row = occurrence()
        with self.assertRaises(FrozenInstanceError):
            row.scope = 'test'
        with self.assertRaises(ValueError):
            MavenCollection(MavenView.DECLARED, 1, [row], True)
        with self.assertRaises(ValueError):
            MavenVersionFact(MavenVersionBasis.DECLARED, origins=[],
                             reason=MavenReason.UNSUPPORTED_VERSION)
        with self.assertRaises(ValueError):
            MavenContext('pom.xml', parent_sources=['parent/pom.xml'])

    def test_closed_bases_reasons_and_required_failure_state(self):
        with self.assertRaises(ValueError):
            MavenVersionFact('guessed', reason=MavenReason.UNSUPPORTED_VERSION)
        with self.assertRaises(ValueError):
            MavenVersionFact(MavenVersionBasis.DECLARED, reason='raw parser diagnostic')
        with self.assertRaises(ValueError):
            MavenVersionFact(MavenVersionBasis.DECLARED)
        with self.assertRaises(ValueError):
            MavenVersionFact(MavenVersionBasis.DECLARED, age=established_age())
        with self.assertRaises(ValueError):
            MavenVersionFact(MavenVersionBasis.DECLARED, version='1', age=established_age(),
                             reason=MavenReason.COMPARATOR_REFUSED)

    def test_collection_admission_requires_rows_or_explicit_certified_emptiness(self):
        for count in (None, 2):
            with self.subTest(count=count), self.assertRaises(ValueError):
                MavenCollection(MavenView.DECLARED, count, (), True)
        with self.assertRaises(ValueError):
            MavenCollection(MavenView.DECLARED, None, (occurrence(),), False,
                            MavenReason.UNSUPPORTED_MODEL)
        with self.assertRaises(ValueError):
            MavenCollection(MavenView.DECLARED, 2, (occurrence(),), True)
        with self.assertRaises(ValueError):
            MavenCollection(MavenView.DECLARED, 2, (occurrence(), occurrence()), True)
        with self.assertRaises(ValueError):
            MavenCollection(MavenView.DECLARED, True, (), False, MavenReason.UNSUPPORTED_MODEL)

    def test_source_cannot_take_another_modules_rows(self):
        declared = MavenCollection(MavenView.DECLARED, 1, (occurrence('other/pom.xml'),), True)
        with self.assertRaises(ValueError):
            MavenSource(MavenContext('pom.xml'), declared)

    def test_discovery_records_do_not_treat_incomplete_as_empty(self):
        incomplete = MavenDiscovery(False, (), MavenReason.DISCOVERY_UNAVAILABLE)
        self.assertFalse(incomplete.complete)
        self.assertEqual(incomplete.source_ids, ())
        for complete, reason in ((True, MavenReason.DISCOVERY_UNAVAILABLE), (False, None)):
            with self.subTest(complete=complete), self.assertRaises(ValueError):
                MavenDiscovery(complete, reason=reason)
        for name in ('/pom.xml', '../pom.xml', 'a/../pom.xml', 'a\\pom.xml'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                MavenContext(name)

    def test_age_carries_exact_conventional_evidence_without_calculating(self):
        age = established_age(2.0)
        self.assertEqual(age.libyears, 2.0)
        self.assertEqual(age.time_basis, 'maven_conventional_pom_last_modified')
        self.assertEqual(age.comparator_basis, 'conventional_central')
        self.assertIn('publication_history_not_established', age.limitations)
        self.assertIn('variant_availability_not_established', age.limitations)
        with self.assertRaises(TypeError):
            MavenAge('2', datetime.now(timezone.utc), datetime.now(timezone.utc), 0,
                     time_basis='publication')
        for stamp in (None, datetime(2020, 1, 1)):
            with self.subTest(stamp=stamp), self.assertRaises(ValueError):
                MavenAge('1', stamp, datetime.now(timezone.utc), 0.0)

    def test_age_rejects_nonfinite_or_negative_already_computed_values(self):
        now = datetime(2020, 1, 1, tzinfo=timezone.utc)
        for value in (float('nan'), float('inf'), -1.0, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                MavenAge('2', now, now, value)
        offset = datetime(2020, 1, 1, tzinfo=timezone(timedelta(hours=2)))
        self.assertEqual(MavenAge('2', offset, offset, 0).measured_version_pom_last_modified.hour, 22)
