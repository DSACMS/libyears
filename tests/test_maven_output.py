"""T010 ordinary dispatch and additive schema3 / paired presentation contracts."""

from contextlib import redirect_stdout
from dataclasses import replace
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.cli import main
from libyears.maven import scan_maven
from libyears.maven_input import filesystem_available
from libyears.model import MetricSummary, RegistryResult, SourceError, SourceEvidence, SourceResult
from libyears.output import format_human, report_to_dict
from libyears.scan import scan_mixed_repository
from test_maven_project import pom, dependencies, dependency
from test_maven_scan import Reader, Metadata, row


class MavenOutputTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()

    def maven(self, documents=None, *, complete=True):
        reader = Reader({'pom.xml': pom(dependencies(row()))} if documents is None else documents,
                        complete=complete)
        return scan_maven('fixture', reader_factory=lambda root: reader, supervisor_factory=Metadata())

    def report(self, maven=None, **kwargs):
        selected = self.maven() if maven is None else maven
        return scan_mixed_repository(self.root, maven_scan=lambda *args, **opts: selected, **kwargs)

    def test_maven_only_has_separate_views_and_all_null_legacy_projection(self):
        report = self.report()
        data = report_to_dict(report, '/private/absolute-root')
        self.assertEqual(data['schema_version'], 3)
        self.assertEqual(data['ecosystems'], ['maven'])
        self.assertEqual(data['dependencies'], [])
        self.assertEqual(data['unmeasurable'], [])
        self.assertEqual(set(data['maven']), {'discovery', 'sources', 'occurrences', 'views'})
        self.assertEqual(data['version_evidence']['maven']['mode'], 'plural')
        self.assertEqual(set(data['summary']['by_ecosystem']['maven'].values()), {None})
        self.assertTrue(all(value is None for key, value in data['summary'].items() if key != 'by_ecosystem'))
        self.assertEqual(data['source_errors'], [{'ecosystem': 'maven', 'source': 'pom.xml',
            'reason': 'maven_plural_projection_unavailable', 'source_id': 'pom.xml'}])
        declared = data['maven']['views']['declared']
        observed = data['maven']['views']['observed']
        self.assertEqual(declared['summary']['dependencies_measured'], 1)
        self.assertEqual(set(observed['summary'].values()), {None})
        self.assertEqual(observed['reason'], 'maven_observed_reader_unavailable')
        occurrence = data['maven']['occurrences'][0]
        self.assertIsNone(occurrence['observed'])
        self.assertEqual(occurrence['key'], {'source_id': 'pom.xml', 'context_id': 'base_model',
            'group_id': 'g', 'artifact_id': 'a', 'type': 'jar', 'classifier': None})
        age = occurrence['declared']['age']
        self.assertEqual(age['time_basis'], 'maven_conventional_pom_last_modified')
        self.assertEqual(age['catalogue_retrieved_at'], '2026-11-12T00:00:00Z')
        self.assertIn('publication_history_not_established', age['limitations'])
        self.assertNotIn('/private/absolute-root', json.dumps(data))

    def test_paired_human_leads_with_maven_and_safe_conventional_disclosure(self):
        report = self.report()
        normal = format_human(report, '/private/secret/root')
        verbose = format_human(report, '/private/secret/root', verbose=True)
        self.assertIn('Ecosystems: maven', normal)
        self.assertIn('Observed', normal)
        self.assertIn('no accepted Maven retained-selection reader', normal)
        self.assertEqual(normal.count('Time basis: Maven conventional (versioned public POM Last-Modified)'), 1)
        self.assertIn('public repository-reported modification times', verbose.lower())
        self.assertIn('catalogue_retrieved_at: 2026-11-12T00:00:00Z', verbose)
        self.assertNotIn('/private/secret/root', verbose)
        self.assertIn('comparison_version_pom_last_modified', verbose)
        self.assertNotIn('Legacy subset', normal)
        self.assertIn('Legacy subset (incomplete scalar projection', verbose)

    def test_nullable_safe_requests_versions_and_policy_failures_keep_known_rows(self):
        bad_request = 'https://name:credential@private.invalid/absolute/path'
        documents = {'pom.xml': pom(dependencies(dependency('a', '<version>' + bad_request + '</version>', group='g'),
                                                     dependency('b', group='g')))}
        report = self.report(self.maven(documents))
        data = report_to_dict(report, '.')
        self.assertEqual(data['maven']['views']['declared']['summary']['dependencies_discovered'], 2)
        self.assertEqual(data['maven']['views']['declared']['summary']['dependencies_measured'], 0)
        for occurrence in data['maven']['occurrences']:
            fact = occurrence['declared']
            self.assertIsNone(fact['request'])
            self.assertIsNone(fact['version'])
            self.assertIsNone(fact['age'])
            self.assertEqual(fact['reason'], 'maven_unsupported_version')
        rendered = json.dumps(data) + format_human(report, '.', verbose=True)
        self.assertNotIn('credential', rendered)
        self.assertNotIn('private.invalid', rendered)
        self.assertNotIn('/absolute/path', rendered)

    def test_incomplete_discovery_has_explicit_null_source_id_and_unknown_presence(self):
        report = self.report(self.maven({}, complete=False))
        data = report_to_dict(report, '.')
        self.assertEqual(data['maven']['discovery']['state'], 'unavailable')
        self.assertEqual(data['maven']['sources'], [])
        self.assertEqual(data['source_errors'][0]['source_id'], None)
        self.assertEqual(data['source_errors'][0]['source'], 'discovery')
        self.assertEqual(set(data['maven']['views']['declared']['summary'].values()), {None})

    def test_python_npm_ruby_successful_and_empty_sources_keep_their_contracts(self):
        from libyears.model import DependencyCandidate
        used = datetime(2020, 1, 1, tzinfo=timezone.utc)
        latest = datetime(2021, 1, 1, tzinfo=timezone.utc)
        lookup = lambda *args: RegistryResult('sibling', '1', used, '2', latest)
        absent = SourceResult('pypi', (), (), (), SourceEvidence('none', None),
                              dependencies_discovered=0, measurement_available=True, source_present=False)
        for ecosystem, boundary in (('pypi', '_python_source_result'), ('npm', '_npm_source_result'),
                                    ('rubygems', 'ruby_source_result')):
            for empty in (False, True):
                with self.subTest(ecosystem=ecosystem, empty=empty):
                    candidate = DependencyCandidate(ecosystem, 'sibling', 'sibling', '1', '1', 'fixture')
                    source = replace(absent, ecosystem=ecosystem, source_present=True,
                                     candidates=() if empty else (candidate,),
                                     dependencies_discovered=0 if empty else 1)
                    with patch('libyears.scan._python_source_result', return_value=replace(absent, ecosystem='pypi')), \
                         patch('libyears.scan._npm_source_result', return_value=replace(absent, ecosystem='npm')), \
                         patch('libyears.scan.ruby_source_result', return_value=replace(absent, ecosystem='rubygems')), \
                         patch('libyears.scan.' + boundary, return_value=source):
                        baseline = scan_mixed_repository(self.root, pypi_lookup=lookup, npm_lookup=lookup,
                            rubygems_lookup=lookup, maven_scan=lambda *args, **kw: None)
                        report = self.report(pypi_lookup=lookup, npm_lookup=lookup, rubygems_lookup=lookup)
                    self.assert_sibling_preserved(baseline, report, ecosystem, empty)

    def assert_sibling_preserved(self, baseline, report, ecosystem, empty):
        before = report_to_dict(baseline, '.')
        after = report_to_dict(report, '.')
        self.assertEqual(after['dependencies'], before['dependencies'])
        self.assertEqual(after['version_evidence'][ecosystem], before['version_evidence'][ecosystem])
        self.assertEqual(after['summary']['by_ecosystem'][ecosystem], before['summary']['by_ecosystem'][ecosystem])
        self.assertIsNone(after['summary']['dependencies_discovered'])
        self.assertIsNone(after['summary']['coverage'])
        self.assertEqual(after['summary']['dependencies_measured'], 0 if empty else 1)
        self.assertEqual(after['summary']['total_libyears'], before['summary']['total_libyears'])

    def test_nuget_successful_and_empty_sources_preserve_established_evidence(self):
        from libyears.model import NuGetPublication
        from libyears.nuget_supervisor import PackageResult
        from libyears.scan import NuGetRequest
        from tests.nuget_fixtures import fixture_nuget_reads
        from tests.test_nuget_scan import nuget_inputs, USED, LATEST
        def lookup(authorities):
            return tuple((authority, PackageResult(origin_state='public_content_verified',
                content_hash_state='public_agreement',
                used_publication=NuGetPublication(authority.normalized_version, USED, True),
                latest_publication=NuGetPublication('2.0.0', LATEST, True))) for authority in authorities)
        for empty in (False, True):
            files = nuget_inputs(names=() if empty else ('alpha',))
            with fixture_nuget_reads(self.root, files):
                baseline = scan_mixed_repository(self.root, nuget_request=NuGetRequest('Witness.csproj', 'witness.json'),
                    nuget_lookup=lookup, maven_scan=lambda *args, **kw: None)
                report = self.report(nuget_request=NuGetRequest('Witness.csproj', 'witness.json'), nuget_lookup=lookup)
            self.assert_sibling_preserved(baseline, report, 'nuget', empty)

    def test_prospective_paired_model_keeps_differing_versions_and_totals_independent(self):
        from libyears.maven import MavenScanReport
        from libyears.maven_model import MavenDiscovery
        from libyears.maven_results import summarize_sources
        from test_maven_model import paired_source_fixture
        source = paired_source_fixture()
        maven = MavenScanReport(MavenDiscovery(True, ('pom.xml',)), (source,), summarize_sources((source,)))
        report = self.report(maven)
        data = report_to_dict(report, '.')
        occurrence = data['maven']['occurrences'][0]
        self.assertEqual((occurrence['declared']['version'], occurrence['observed']['version']), ('1', '3'))
        self.assertEqual(data['maven']['views']['declared']['summary']['total_libyears'], 1.0)
        self.assertEqual(data['maven']['views']['observed']['summary']['total_libyears'], 2.0)
        self.assertIsNone(data['summary']['total_libyears'])
        human = format_human(report, '.')
        self.assertIn('Declared: 1 / 1.000', human)
        self.assertIn('Observed: 3 / 2.000', human)
        self.assertNotIn('Observed is unavailable:', human)

    def test_all_unavailable_legacy_sources_have_null_numerics_with_maven(self):
        (self.root / 'package.json').write_text('{invalid')
        data = report_to_dict(self.report(), '.')
        self.assertIsNone(data['summary']['dependencies_measured'])
        self.assertIsNone(data['summary']['total_libyears'])
        self.assertEqual(data['summary']['by_ecosystem']['npm']['dependencies_discovered'], None)

    @unittest.skipUnless(filesystem_available(), 'safe descriptor primitives unavailable')
    def test_actual_ordinary_directory_auto_discovery_and_no_maven_absence(self):
        baseline = scan_mixed_repository(self.root)
        self.assertIsNone(baseline.maven)
        self.assertNotIn('maven', report_to_dict(baseline, '.'))
        (self.root / 'pom.xml').write_bytes(pom())
        report = scan_mixed_repository(self.root)
        self.assertIsNotNone(report.maven)
        self.assertEqual(report.maven.summaries.declared.summary.dependencies_discovered, 0)
        self.assertIsNone(scan_mixed_repository(self.root / 'pom.xml').maven)

    def test_no_native_discovery_is_unknown_and_never_silently_certifies_absence(self):
        with patch('libyears.maven_input.filesystem_available', return_value=False):
            report = scan_mixed_repository(self.root)
        self.assertIsNotNone(report.maven)
        self.assertFalse(report.maven.discovery.complete)
        self.assertIsNone(report.summary.dependencies_discovered)
        self.assertEqual(report.source_errors[0].source_id, None)
        output = io.StringIO()
        with patch('libyears.maven_input.filesystem_available', return_value=False), redirect_stdout(output):
            self.assertEqual(main([str(self.root), '--json']), 0)
        self.assertEqual(json.loads(output.getvalue())['maven']['discovery']['state'], 'unavailable')

    def test_cli_ordinary_root_no_new_flags_resolved_stays_python_only_and_exit_zero(self):
        result = self.maven()
        def scan(path, **kwargs):
            return scan_mixed_repository(path, maven_scan=lambda *args, **opts: result, **kwargs)
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main([str(self.root), '--json'], scan=scan), 0)
        data = json.loads(output.getvalue())
        self.assertIn('maven', data)
        self.assertEqual(data['maven']['occurrences'][0]['declared']['version'], '1')
        source = self.root / 'python-snapshot.txt'
        source.write_text('unrelated==9\n')
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main([str(self.root), '--json', '--resolved', str(source)], scan=scan), 0)
        after = json.loads(output.getvalue())
        self.assertEqual(after['maven'], data['maven'])


if __name__ == '__main__':
    unittest.main()
