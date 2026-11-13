"""Cross-ecosystem display boundaries without changing measurement evidence."""

from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from libyears.maven import scan_maven
from libyears.maven_input import filesystem_available
from libyears.nuget_discovery import NuGetRecognition, discover_nuget_candidates, discovery_available
from libyears.output import format_human, format_json
from libyears.scan import scan_mixed_repository
from tests.test_nuget_sources import repository_inputs
from tests.test_nuget_scan import nuget_inputs
from test_maven_scan import Reader, Metadata, row
from test_maven_project import pom, dependencies


class PresentationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.guard = patch('socket.socket', side_effect=AssertionError('unexpected network'))
        self.guard.start()
        self.addCleanup(self.guard.stop)

    def uncertain_maven(self):
        return scan_maven('fixture', reader_factory=lambda root: Reader({}, complete=False))

    def scan(self, *, python=False, maven=None):
        (self.root / 'package.json').write_text('{"dependencies":{"alpha":"*"}}')
        if python:
            (self.root / 'requirements.txt').write_text('beta>=1\n')
        with patch('libyears.nuget_sources.discover_nuget_candidates',
                   return_value=NuGetRecognition('incomplete')):
            return scan_mixed_repository(self.root, nuget_repository=True,
                maven_scan=lambda *args, **kwargs: maven or self.uncertain_maven())

    def test_npm_and_mixed_positive_sources_hide_only_unconfirmed_ecosystems(self):
        for python in (False, True):
            with self.subTest(python=python):
                report = self.scan(python=python)
                before = format_json(report, '.')
                normal = format_human(report, 'private-root')
                verbose = format_human(report, 'private-root', verbose=True)
                self.assertIn('npm', normal)
                self.assertEqual('pypi' in normal, python)
                self.assertNotIn('Maven', normal)
                self.assertNotIn('NuGet', normal)
                self.assertNotIn('maven_plural_projection_unavailable', normal)
                self.assertIn('Repository scalar subset (incomplete)', normal)
                self.assertIn('unknown coverage', normal)
                self.assertNotIn('None', normal)
                self.assertIn('Conventional Maven dependency age', verbose)
                self.assertIn('nuget_discovery_incomplete', verbose)
                self.assertIn('not certified absent', normal)
                self.assertNotIn('private-root', normal + verbose)
                self.assertEqual(format_json(report, '.'), before)
                self.assertIn('"maven"', before)
                self.assertIn('nuget_discovery_incomplete', before)

    def test_complete_npm_and_pypi_measurements_survive_unknown_sibling_discovery(self):
        from datetime import datetime, timezone
        from libyears.model import RegistryResult
        (self.root / 'package.json').write_text('{"dependencies":{"alpha":"1.0.0"}}')
        (self.root / 'package-lock.json').write_text(json.dumps({
            'lockfileVersion': 3, 'packages': {'node_modules/alpha': {'version': '1.0.0'}}}))
        stamp = datetime(2020, 1, 1, tzinfo=timezone.utc)
        def lookup(name, version):
            return RegistryResult(name, version, stamp, version, stamp)
        for python in (False, True):
            if python:
                (self.root / 'requirements.txt').write_text('beta==1.0.0\n')
            with patch('libyears.nuget_sources.discover_nuget_candidates',
                       return_value=NuGetRecognition('incomplete')):
                report = scan_mixed_repository(self.root, nuget_repository=True,
                    npm_lookup=lookup, pypi_lookup=lookup,
                    maven_scan=lambda *a, **k: self.uncertain_maven())
            normal = format_human(report, '.')
            self.assertIn('npm: 100.0% coverage; 1 / 1 measured', normal)
            if python:
                self.assertIn('pypi: 100.0% coverage; 1 / 1 measured', normal)
            self.assertNotIn('Maven', normal)
            self.assertNotIn('NuGet', normal)
            self.assertEqual(report.summary.dependencies_measured, 2 if python else 1)
            self.assertIsNone(report.summary.dependencies_discovered)
            self.assertIn('unknown coverage', normal)

    def test_maven_relevance_flag_changes_display_without_changing_json_or_summary(self):
        report = self.scan()
        positive = replace(report, maven=replace(report.maven, positive_local_evidence=True))
        self.assertEqual(format_json(report, '.'), format_json(positive, '.'))
        normal = format_human(positive, '.')
        self.assertIn('Ecosystems: maven, npm', normal)
        self.assertIn('Declared: unavailable', normal)
        self.assertIn('Observed: unavailable', normal)
        self.assertIn('Time basis: Maven conventional', normal)
        self.assertNotIn('Legacy subset', normal)
        self.assertEqual(positive.summary, report.summary)

    def test_safe_maven_rows_survive_with_independent_views_and_refusal_summary(self):
        reader = Reader({'pom.xml': pom(dependencies(row(), row('b', '${missing}')))}, complete=False)
        maven = scan_maven('fixture', reader_factory=lambda root: reader, supervisor_factory=Metadata())
        report = self.scan(maven=maven)
        normal = format_human(report, '.')
        verbose = format_human(report, '.', verbose=True)
        self.assertIn('Declared: partial', normal)
        self.assertIn('Observed: unavailable', normal)
        self.assertIn('Declared unmeasurable: 1', normal)
        self.assertIn('g:a', normal)
        self.assertNotIn('g:b', normal)
        self.assertIn('g:b', verbose)
        self.assertIn('comparison_version_pom_last_modified', verbose)
        self.assertIsNone(report.summary.coverage)

    def test_relevant_nuget_keeps_failures_but_moves_methodology_to_verbose(self):
        with repository_inputs(self.root, {'a/Witness.csproj': nuget_inputs()}):
            report = scan_mixed_repository(self.root, nuget_repository=True, maven_scan=lambda *a, **k: None)
        normal = format_human(report, '.')
        verbose = format_human(report, '.', verbose=True)
        self.assertIn('nuget', normal)
        self.assertIn('measurement unavailable', normal)
        self.assertIn('nuget_provenance_missing', normal)
        self.assertNotIn('Search covers root through depth 4', normal)
        self.assertNotIn('ProjectReference edges', normal)
        self.assertIn('Search covers root through depth 4', verbose)
        self.assertIn('ProjectReference edges', verbose)

    def test_failed_nuget_inventory_boolean_does_not_supply_population_or_authority(self):
        reports = []
        for positive in (False, True):
            with patch('libyears.nuget_sources.discover_nuget_candidates', return_value=
                       NuGetRecognition('incomplete', positive_local_evidence=positive)):
                reports.append(scan_mixed_repository(self.root, nuget_repository=True, maven_scan=lambda *a, **k: None))
        absent, present = reports
        self.assertEqual(format_json(absent, '.'), format_json(present, '.'))
        self.assertNotIn('NuGet', format_human(absent, '.'))
        self.assertIn('NuGet', format_human(present, '.'))
        self.assertIn('nuget_discovery_incomplete', format_human(present, '.'))
        self.assertIsNone(present.summary.dependencies_discovered)
        self.assertEqual(present.measurements, ())

    def test_explicit_witness_keeps_unavailable_nuget_visible_without_candidate(self):
        with patch('libyears.nuget_sources.discover_nuget_candidates', return_value=NuGetRecognition('unavailable')):
            report = scan_mixed_repository(self.root, nuget_repository=True, nuget_witnesses=(('Missing.csproj', 'w.json'),),
                                           maven_scan=lambda *a, **k: None)
        self.assertIn('NuGet', format_human(report, '.'))

    @unittest.skipUnless(filesystem_available(), 'safe Maven input primitives unavailable')
    def test_refused_maven_candidate_remains_relevant_without_following_link(self):
        (self.root / 'pom.xml').symlink_to('missing')
        report = scan_mixed_repository(self.root, nuget_repository=True)
        self.assertTrue(report.maven.positive_local_evidence)
        self.assertEqual(report.maven.discovery.source_ids, ())
        self.assertIn('Declared: unavailable', format_human(report, '.'))

    @unittest.skipUnless(discovery_available(), 'safe NuGet enumeration unavailable')
    def test_candidate_before_budget_failure_retains_only_relevance(self):
        (self.root / 'A.csproj').write_text('unread')
        (self.root / 'z').mkdir()
        with patch('libyears.nuget_discovery.MAX_DIRECTORIES', 1):
            inventory = discover_nuget_candidates(self.root)
        self.assertEqual(inventory.status, 'incomplete')
        self.assertEqual(inventory.candidates, ())
        self.assertTrue(inventory.positive_local_evidence)
        with patch('libyears.nuget_discovery.MAX_ENTRIES', 0):
            inventory = discover_nuget_candidates(self.root)
        self.assertFalse(inventory.positive_local_evidence)

class RetainedJavaJourneyTests(unittest.TestCase):
    """Replay sanitized public evidence, without network or private trust inputs."""

    def retained(self, directory, summary_name, occurrences_name):
        import csv
        base = Path(__file__).resolve().parents[1] / 'specs/007-maven-dependency-age' / directory
        summary = json.loads((base / summary_name).read_text())
        with (base / occurrences_name).open(newline='') as handle:
            rows = list(csv.DictReader(handle))
        occurrences = []
        for row in rows:
            age = None
            if row.get('libyears'):
                age = {name: row[name] for name in (
                    'comparison_version', 'measured_version_pom_last_modified',
                    'comparison_version_pom_last_modified', 'catalogue_retrieved_at')}
                age.update(libyears=float(row['libyears']), comparator_basis='conventional_central',
                           eligibility_policy='maven_conservative_stable_v1',
                           timestamp_order_anomaly=row['timestamp_order_anomaly'] == 'True', limitations=[])
            occurrences.append({
                'key': {name: row.get(name) or None for name in
                        ('source_id', 'group_id', 'artifact_id', 'type', 'classifier')},
                'scope': row['scope'], 'optional': row.get('optional'),
                'declared': {'version': row['version'] or None, 'age': age,
                             'reason': row['reason'] or None,
                             'version_basis': 'supported_local_base_model_request', 'evidence_origins': []},
                'observed': None})
        return {'views': summary['views'], 'discovery': {'state': 'unavailable'},
                'sources': [{'source_id': name} for name in sorted({row['source_id'] for row in rows})],
                'occurrences': occurrences}

    def test_ab2d_positive_and_dpc_adversarial_remain_truthful_and_compact(self):
        from libyears.maven_output import _maven_data_human_lines
        for directory, summary_name, occurrence_name, measured in (
            ('positive-validation', 'verified-summary.json', 'verified-occurrences.csv', 40),
            ('public-validation', 'summary.json', 'occurrences.csv', 0),
        ):
            with self.subTest(witness=directory):
                data = self.retained(directory, summary_name, occurrence_name)
                original = json.dumps(data, sort_keys=True)
                normal = '\n'.join(_maven_data_human_lines(data))
                verbose = '\n'.join(_maven_data_human_lines(data, verbose=True))
                self.assertIn('Declared: partial', normal)
                self.assertIn('Observed: unavailable', normal)
                self.assertIn('Time basis: Maven conventional', normal)
                self.assertIn('Discovery incomplete', normal)
                self.assertEqual(data['views']['declared']['summary']['dependencies_measured'], measured)
                self.assertIsNone(data['views']['declared']['summary']['coverage'])
                self.assertLess(len(normal), len(verbose) / 2)
                self.assertIn('static local base-model requests', verbose)
                self.assertEqual(json.dumps(data, sort_keys=True), original)
                if measured:
                    self.assertIn('9.268', normal)
                    self.assertEqual(sum(row['declared']['age'] is not None for row in data['occurrences']), 40)
                    self.assertIn('comparison_version_pom_last_modified', verbose)
                else:
                    self.assertIn('No declared ages measured', normal)
                    self.assertIn('zero total describes an empty measured subset', normal)

class MavenViewPresentationTests(unittest.TestCase):
    def source(self, *, declared=True, measured_observed=False, measured_declared=False):
        from libyears.maven_model import MavenCollection, MavenView, MavenReason
        from test_maven_model import paired_source_fixture
        source = paired_source_fixture()
        row = source.declared.rows[0]
        declared_fact = row.declared
        if not declared:
            declared_fact = None
        elif not measured_declared:
            declared_fact = replace(declared_fact, age=None, reason=MavenReason.UNSUPPORTED_VERSION)
        observed_fact = row.observed
        if not measured_observed:
            observed_fact = replace(observed_fact, age=None, reason=MavenReason.TIME_BASIS_UNAVAILABLE)
        row = replace(row, declared=declared_fact, observed=observed_fact)
        return replace(source,
            declared=(replace(source.declared, rows=(row,)) if declared else
                      MavenCollection(MavenView.DECLARED, None, (), False,
                                      MavenReason.POPULATION_UNKNOWN)),
            observed=replace(source.observed, rows=(row,)))

    def render(self, source):
        from libyears.maven import MavenScanReport
        from libyears.maven_model import MavenDiscovery
        from libyears.maven_results import summarize_sources
        from libyears.maven_output import maven_human_lines, maven_to_dict
        report = MavenScanReport(MavenDiscovery(True, ('pom.xml',)), (source,), summarize_sources((source,)))
        before = maven_to_dict(report)
        normal = '\n'.join(maven_human_lines(report))
        self.assertEqual(before, maven_to_dict(report))
        return normal, before

    def test_observed_only_refusal_never_fabricates_declared_membership(self):
        normal, data = self.render(self.source(declared=False))
        self.assertIn('Declared: unavailable', normal)
        self.assertIn('Observed unmeasurable: 1', normal)
        self.assertNotIn('Declared unmeasurable:', normal)
        self.assertIsNone(data['occurrences'][0]['declared'])
        self.assertEqual(data['views']['observed']['summary']['dependencies_discovered'], 1)

    def test_paired_refusals_remain_independent(self):
        normal, _ = self.render(self.source())
        self.assertIn('Declared unmeasurable: 1 — exact declared version unavailable', normal)
        self.assertIn('Observed unmeasurable: 1 — versioned POM Last-Modified unavailable', normal)

    def test_measured_sibling_does_not_erase_other_view_refusal(self):
        for declared_measured in (False, True):
            normal, _ = self.render(self.source(measured_declared=declared_measured,
                                               measured_observed=not declared_measured))
            self.assertIn('g:a', normal)
            self.assertIn(('Observed' if declared_measured else 'Declared') + ' unmeasurable: 1', normal)

    def test_measured_observed_only_row_remains_visible(self):
        normal, _ = self.render(self.source(declared=False, measured_observed=True))
        self.assertIn('Observed: 3 / 2.000', normal)
        self.assertNotIn('Declared unmeasurable:', normal)


if __name__ == "__main__":
    unittest.main()
