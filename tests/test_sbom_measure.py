from dataclasses import astuple, replace
from datetime import timedelta
import unittest
from unittest.mock import Mock, patch

from libyears.maven import MavenCapability
from libyears.maven_model import MavenReason
from libyears.maven_registry import MavenTarget, MavenPomDate
from libyears.sbom_document import accept_document
from libyears.sbom_identity import canonical_members
from libyears.sbom_measure import measure_members, summarize_members
from libyears.sbom_policy import admit_members
from tests.test_sbom_document import snapshot, synthetic_document
from tests.test_sbom_identity import maven_component
from test_maven_scan import Metadata, OLD, NEW, RETRIEVED


class MeasurementTests(unittest.TestCase):
    def measure(self, records, metadata=None):
        document = accept_document(snapshot(synthetic_document(components=records)))
        members = admit_members(document, canonical_members(document))
        metadata = metadata or Metadata()
        with patch('subprocess.Popen', side_effect=AssertionError('process')), patch('socket.socket', side_effect=AssertionError('socket')):
            result = measure_members(members, supervisor_factory=metadata)
        return result, summarize_members(result), metadata

    def test_positive_zero_and_missing_same_version_dates(self):
        records = [maven_component(version='1'), maven_component('equal', version='2')]
        rows, summary, metadata = self.measure(records)
        self.assertEqual([row.age.libyears for row in rows], [1.0, 0.0])
        self.assertEqual(summary.dependencies_discovered, 2)
        self.assertEqual(summary.total_libyears, 1.0)
        self.assertEqual(rows[0].age.time_basis, 'maven_conventional_pom_last_modified')
        self.assertEqual(rows[0].age.ordering_basis, 'maven_comparable_version_3_9_11')
        self.assertEqual(rows[0].age.comparator_basis, 'sbom_maven_central_convention')
        self.assertEqual(len(rows[0].age.limitations), 2)
        self.assertEqual(summary.coverage, 1.0)
        self.assertTrue(all(type(cap) is MavenCapability for cap in metadata.capabilities))
        self.assertTrue(metadata.closed)
        rows, summary, metadata = self.measure([records[1]], Metadata(dates={('equal', '2'): MavenReason.TIME_BASIS_UNAVAILABLE}))
        self.assertIsNone(rows[0].age)
        self.assertEqual(rows[0].reason, MavenReason.TIME_BASIS_UNAVAILABLE)
        self.assertEqual(summary.coverage, 0.0)

    def test_inversion_and_identity_bound_response(self):
        rows, summary, metadata = self.measure([maven_component(version='1')], Metadata(dates={('a', '1'): NEW + timedelta(days=1)}))
        self.assertEqual(rows[0].age.libyears, 0.0)
        self.assertTrue(rows[0].age.timestamp_order_anomaly)
        metadata = Metadata()
        metadata.pom_date = lambda cap, version=None: MavenPomDate('wrong', cap.artifact_id, version, OLD, RETRIEVED)
        rows, summary, unused = self.measure([maven_component(version='1')], metadata)
        self.assertEqual(rows[0].reason, MavenReason.TIME_BASIS_UNAVAILABLE)

    def test_failure_matrix_and_completed_siblings(self):
        for failure in (MavenReason.CATALOGUE_UNAVAILABLE, MavenReason.UNKNOWN_LATEST_ELIGIBILITY,
                        MavenReason.AMBIGUOUS_LATEST_VERSION, MavenReason.NO_STABLE_RELEASE,
                        MavenReason.METADATA_BUDGET_EXCEEDED, MavenReason.METADATA_WORKER_UNAVAILABLE):
            rows, summary, metadata = self.measure([maven_component(version='1'), maven_component('b', version='1')], Metadata(targets={'b': failure}))
            self.assertEqual(rows[0].age.libyears, 1.0)
            self.assertEqual(rows[1].reason, failure)
            self.assertEqual((summary.dependencies_discovered, summary.dependencies_measured, summary.coverage), (2, 1, .5))
        for version in ('1', '2'):
            rows, summary, unused = self.measure([maven_component(version='1')], Metadata(dates={('a', version): MavenReason.TIME_BASIS_UNAVAILABLE}))
            self.assertEqual(rows[0].reason, MavenReason.TIME_BASIS_UNAVAILABLE)

    def test_variant_weight_cache_and_scheduling_after_admission(self):
        records = [maven_component('z', version='1'), maven_component(version='1', suffix='?classifier=sources'),
                   maven_component(version='1'), maven_component('private', suffix='?repository_url=https:%2F%2Fprivate.invalid')]
        rows, summary, metadata = self.measure(records)
        self.assertEqual(summary.dependencies_measured, 3)
        self.assertEqual(summary.total_libyears, 3.0)
        self.assertEqual(metadata.calls, [('target', 'org.example', 'a'), ('date', 'org.example', 'a', '2'),
                                         ('date', 'org.example', 'a', '1'), ('target', 'org.example', 'z'),
                                         ('date', 'org.example', 'z', '2'), ('date', 'org.example', 'z', '1')])
        self.assertEqual([row.index for row in rows], [0, 1, 2, 3])

    def test_empty_refused_unknown_and_no_default(self):
        for records in ([], [{}]):
            rows, summary, metadata = self.measure(records)
            self.assertEqual(summary.dependencies_measured, 0)
            self.assertEqual(summary.total_libyears, 0.0)
            self.assertEqual(summary.coverage, None if not records else 0.0)
            self.assertFalse(hasattr(metadata, 'capabilities'))
        self.assertEqual(astuple(summarize_members(None)), (None,) * 7)
        with self.assertRaises(TypeError):
            measure_members(())
