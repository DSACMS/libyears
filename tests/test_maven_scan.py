"""T009 source orchestration with local staged facts and injected metadata."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.maven import MavenAdmission, measure_admission, scan_maven
from libyears.maven_input import MavenInputFailure, MavenInputIssue, MavenInputSnapshot, filesystem_available, parse_pom
from libyears.maven_model import MavenDiscovery, MavenReason
from libyears.maven_registry import MavenTarget, MavenPomDate
from libyears.maven_results import summarize_sources
from test_maven_project import pom, dependency, dependencies, parent
from test_maven_policy import repositories, repo, StagedReader

UTC = timezone.utc
OLD = datetime(2020, 1, 1, tzinfo=UTC)
NEW = OLD + timedelta(days=365.25)
RETRIEVED = datetime(2026, 11, 12, tzinfo=UTC)


def row(artifact='a', version='1', extra=''):
    return dependency(artifact, '<version>' + version + '</version>' + extra, group='g')


class Reader(StagedReader):
    def __init__(self, documents, *, complete=True, controls=None):
        super().__init__(controls)
        self.documents = documents
        self.complete = complete

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        pass

    def inventory(self):
        return SimpleNamespace(discovery=MavenDiscovery(self.complete, tuple(self.documents),
            None if self.complete else MavenReason.DISCOVERY_UNAVAILABLE))

    def snapshot_pom(self, path):
        data = self.documents[path]
        return MavenInputSnapshot(path, data, ('safe-staged-fixture',), parse_pom(data))


class Metadata:
    def __init__(self, *, targets=None, dates=None):
        self.targets = targets or {}
        self.dates = dates or {}
        self.calls = []
        self.closed = False

    def __call__(self, capabilities, **kwargs):
        self.capabilities = capabilities
        self.options = kwargs
        return self

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        self.closed = True

    def select_target(self, cap):
        self.calls.append(('target', cap.group_id, cap.artifact_id))
        target = self.targets.get(cap.artifact_id, '2')
        return MavenTarget(cap.group_id, cap.artifact_id,
                           None if isinstance(target, MavenReason) else target, RETRIEVED,
                           target if isinstance(target, MavenReason) else None)

    def pom_date(self, cap, version=None):
        version = version or cap.version
        self.calls.append(('date', cap.group_id, cap.artifact_id, version))
        value = self.dates.get((cap.artifact_id, version), NEW if version == '2' else OLD)
        return MavenPomDate(cap.group_id, cap.artifact_id, version,
                            None if isinstance(value, MavenReason) else value, RETRIEVED,
                            value if isinstance(value, MavenReason) else None)


class MavenScanTests(unittest.TestCase):
    def scan(self, documents, *, metadata=None, complete=True, controls=None):
        self.metadata = metadata or Metadata()
        reader = Reader(documents, complete=complete, controls=controls)
        return scan_maven('fixture', reader_factory=lambda root: reader,
                          supervisor_factory=self.metadata, ca_bundle='explicit-ca.pem')

    def test_exact_dates_use_existing_arithmetic_and_keep_observed_all_null(self):
        result = self.scan({'pom.xml': pom(dependencies(row()))})
        fact = result.sources[0].declared.rows[0].declared
        self.assertEqual(fact.age.libyears, 1.0)
        self.assertEqual(result.summaries.declared.summary.dependencies_discovered, 1)
        self.assertEqual(result.summaries.declared.summary.coverage, 1.0)
        observed = result.summaries.observed.summary
        self.assertEqual((observed.dependencies_discovered, observed.dependencies_measured, observed.coverage,
                          observed.total_libyears, observed.mean_libyears, observed.median_libyears, observed.max_libyears),
                         (None,) * 7)
        self.assertEqual(self.metadata.options, {'ca_bundle': 'explicit-ca.pem'})
        self.assertTrue(self.metadata.closed)

    def test_same_version_needs_one_admitted_date_and_produces_exact_zero(self):
        result = self.scan({'pom.xml': pom(dependencies(row()))}, metadata=Metadata(targets={'a': '1'}))
        self.assertEqual(result.sources[0].declared.rows[0].declared.age.libyears, 0.0)
        self.assertEqual(self.metadata.calls, [('target', 'g', 'a'), ('date', 'g', 'a', '1')])
        result = self.scan({'pom.xml': pom(dependencies(row()))}, metadata=Metadata(
            targets={'a': '1'}, dates={('a', '1'): MavenReason.TIME_BASIS_UNAVAILABLE}))
        self.assertIsNone(result.sources[0].declared.rows[0].declared.age)
        self.assertEqual(result.summaries.declared.summary.coverage, 0.0)

    def test_repeated_modules_weight_rows_but_share_metadata_and_keep_policy_separate(self):
        documents = {'pom.xml': pom(dependencies(row())),
                     'child/pom.xml': pom(parent(), artifact='child'),
                     'denied/pom.xml': pom(dependencies(row()) + repositories(repo(url='https://private.invalid')), artifact='denied')}
        result = self.scan(documents)
        summary = result.summaries.declared.summary
        self.assertEqual((summary.dependencies_discovered, summary.dependencies_measured, summary.coverage,
                          summary.total_libyears), (3, 2, 2 / 3, 2.0))
        self.assertEqual(len(self.metadata.calls), 3)
        denied = next(s for s in result.sources if s.context.source_id == 'denied/pom.xml')
        self.assertEqual(denied.declared.rows[0].declared.reason, MavenReason.COMPARATOR_REFUSED)
        self.assertIsNone(denied.declared.rows[0].declared.age)

    def test_unknown_discovery_and_missing_parent_keep_safe_measured_rows_and_null_coverage(self):
        explicit = dependencies(row(extra='<scope>compile</scope><optional>false</optional>'))
        for body, complete in ((explicit, False), (parent(path='') + explicit, True)):
            result = self.scan({'pom.xml': pom(body)}, complete=complete)
            summary = result.summaries.declared.summary
            self.assertIsNone(summary.dependencies_discovered)
            self.assertIsNone(summary.coverage)
            self.assertEqual((summary.dependencies_measured, summary.total_libyears), (1, 1.0))

    def test_whole_bad_source_does_not_erase_successful_sibling(self):
        result = self.scan({'pom.xml': pom(dependencies(row())), 'broken/pom.xml': b'not XML'})
        summary = result.summaries.declared.summary
        self.assertEqual((summary.dependencies_measured, summary.total_libyears), (1, 1.0))
        self.assertIsNone(summary.dependencies_discovered)
        self.assertIsNone(summary.coverage)
        self.assertFalse(next(s for s in result.sources if s.context.source_id == 'broken/pom.xml').declared.accepted)

    def test_all_policy_or_version_refusals_keep_zero_collection_without_creating_supervisor(self):
        factory = Mock(side_effect=AssertionError('must not create worker'))
        for body in (dependencies(row()) + repositories(repo(url='${central}')),
                     dependencies(dependency('a', group='g'))):
            reader = Reader({'pom.xml': pom(body)})
            result = scan_maven('fixture', reader_factory=lambda root: reader, supervisor_factory=factory)
            summary = result.summaries.declared.summary
            self.assertEqual((summary.dependencies_discovered, summary.dependencies_measured,
                              summary.coverage, summary.total_libyears), (1, 0, 0.0, 0.0))
        factory.assert_not_called()

    def test_target_missing_date_or_catalogue_failure_never_requests_older_or_unnecessary_dates(self):
        documents = {'pom.xml': pom(dependencies(row()))}
        for metadata in (Metadata(targets={'a': MavenReason.UNKNOWN_LATEST_ELIGIBILITY}),
                         Metadata(dates={('a', '2'): MavenReason.TIME_BASIS_UNAVAILABLE})):
            result = self.scan(documents, metadata=metadata)
            self.assertEqual(result.summaries.declared.summary.dependencies_measured, 0)
            self.assertNotIn(('date', 'g', 'a', '1'), metadata.calls)
            self.assertIsNone(result.sources[0].declared.rows[0].declared.age)

    def test_partial_ga_and_worker_failures_preserve_successful_rows_and_deterministic_schedule(self):
        metadata = Metadata(targets={'c': MavenReason.METADATA_WORKER_UNAVAILABLE},
                            dates={('b', '1'): MavenReason.TIME_BASIS_UNAVAILABLE})
        result = self.scan({'pom.xml': pom(dependencies(row('c'), row('b'), row('a')))}, metadata=metadata)
        self.assertEqual(result.summaries.declared.summary.dependencies_measured, 1)
        self.assertEqual([c for c in metadata.calls if c[0] == 'target'],
                         [('target', 'g', 'a'), ('target', 'g', 'b'), ('target', 'g', 'c')])
        self.assertEqual(result.summaries.declared.summary.coverage, 1 / 3)

    def test_negative_pom_date_order_clamps_and_flags_without_changing_versions(self):
        result = self.scan({'pom.xml': pom(dependencies(row()))}, metadata=Metadata(
            dates={('a', '1'): NEW, ('a', '2'): OLD}))
        age = result.sources[0].declared.rows[0].declared.age
        self.assertEqual(age.libyears, 0.0)
        self.assertTrue(age.timestamp_order_anomaly)
        self.assertEqual(age.comparison_version, '2')

    def test_complete_absence_omits_maven_but_empty_pom_and_unknown_discovery_are_distinct(self):
        self.assertIsNone(self.scan({}))
        empty = self.scan({'pom.xml': pom()})
        self.assertEqual(empty.summaries.declared.summary.dependencies_discovered, 0)
        self.assertEqual(empty.summaries.declared.summary.total_libyears, 0.0)
        unknown = self.scan({}, complete=False)
        self.assertIsNone(unknown.summaries.declared.summary.dependencies_discovered)
        self.assertIsNone(unknown.summaries.declared.summary.dependencies_measured)
        self.assertIsNone(unknown.summaries.declared.summary.total_libyears)

    def test_empty_unavailable_and_all_missing_bom_sources_compose_without_fabricated_coverage(self):
        empty_plus = self.scan({'pom.xml': pom(), 'child/pom.xml': pom(dependencies(row()), artifact='child')})
        self.assertEqual(empty_plus.summaries.declared.summary.coverage, 1.0)
        empty = self.scan({'pom.xml': pom(), 'child/pom.xml': pom(artifact='child')})
        self.assertEqual((empty.summaries.declared.summary.dependencies_discovered,
                          empty.summaries.declared.summary.dependencies_measured,
                          empty.summaries.declared.summary.total_libyears), (0, 0, 0.0))
        failed = self.scan({'pom.xml': b'not XML'})
        self.assertIsNone(failed.summaries.declared.summary.dependencies_measured)
        self.assertIsNone(failed.summaries.declared.summary.total_libyears)
        bom = ('<dependencyManagement><dependencies>'
               + dependency('bom', '<version>1</version><type>pom</type><scope>import</scope>', group='g')
               + '</dependencies></dependencyManagement>')
        missing = dependencies(dependency('a', group='g'), dependency('b', group='g'))
        failed = self.scan({'pom.xml': pom(bom + missing)})
        summary = failed.summaries.declared.summary
        self.assertEqual((summary.dependencies_discovered, summary.dependencies_measured,
                          summary.coverage, summary.total_libyears), (2, 0, 0.0, 0.0))
        mixed = self.scan({'pom.xml': pom(bom + missing),
                           'ok/pom.xml': pom(dependencies(row('ok')), artifact='other')})
        self.assertEqual(mixed.summaries.declared.summary.coverage, 1 / 3)
        self.assertEqual([call for call in self.metadata.calls if call[0] == 'target'], [('target', 'g', 'ok')])

    def test_independently_known_whole_unavailable_collection_keeps_n_but_null_coverage(self):
        from libyears.maven import admit_sources
        from libyears.maven_project import build_project_graph
        reader = Reader({'pom.xml': pom(dependencies(row())), 'other/pom.xml': pom(artifact='other')})
        graph = build_project_graph(reader.inventory().discovery, reader.snapshot_pom)
        admission = admit_sources(graph, reader)
        other = next(source for source in admission.sources if source.context.source_id == 'other/pom.xml')
        root = next(source for source in admission.sources if source.context.source_id == 'pom.xml')
        unavailable = replace(other.declared, population_count=2, accepted=False,
                              reason=MavenReason.UNSUPPORTED_MODEL)
        modified = MavenAdmission((root, replace(other, declared=unavailable)), admission.work)
        measured = measure_admission(modified, supervisor_factory=Metadata())
        summary = summarize_sources(measured).declared.summary
        self.assertEqual((summary.dependencies_discovered, summary.dependencies_measured,
                          summary.total_libyears), (3, 1, 1.0))
        self.assertIsNone(summary.coverage)

    def test_missing_root_primitives_returns_unknown_discovery_without_metadata(self):
        factory = Mock(side_effect=AssertionError('no worker'))
        with patch('libyears.maven_input.filesystem_available', return_value=False):
            report = scan_maven('not-inspected', supervisor_factory=factory)
        self.assertFalse(report.discovery.complete)
        self.assertEqual(report.sources, ())
        factory.assert_not_called()

    @unittest.skipUnless(filesystem_available(), 'safe descriptor primitives unavailable')
    def test_native_scan_stages_regular_pom_once_and_does_not_modify_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            source = root / 'pom.xml'
            data = pom(dependencies(row()))
            source.write_bytes(data)
            info = source.stat()
            report = scan_maven(root, supervisor_factory=Metadata())
            self.assertEqual(report.summaries.declared.summary.dependencies_measured, 1)
            self.assertEqual(source.read_bytes(), data)
            self.assertEqual(source.stat().st_mtime_ns, info.st_mtime_ns)
            self.assertIsNone(scan_maven(source, supervisor_factory=Metadata()))


if __name__ == '__main__':
    unittest.main()
