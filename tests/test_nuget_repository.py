"""Offline ordinary repository occurrence/CLI/output semantics on every host."""

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.cli import main
from libyears.model import MetricSummary, NuGetPublication, RegistryResult
from libyears.nuget_discovery import NuGetRecognition
from libyears.nuget_registry import NuGetRegistryAdapter
from libyears.nuget_sources import NuGetRepositoryRequestError
from libyears.nuget_supervisor import PackageResult
from libyears.output import format_human, format_json, report_to_dict
from libyears.scan import NuGetRequest, scan_mixed_repository
from tests.nuget_fixtures import fixture_nuget_reads
from tests.test_nuget_scan import nuget_inputs, USED, LATEST
from tests.test_nuget_sources import repository_inputs


def success(authority):
    return PackageResult(origin_state='public_content_verified', content_hash_state='public_agreement',
        used_publication=NuGetPublication(authority.normalized_version, USED, True),
        latest_publication=NuGetPublication('3.0.0', LATEST, True))


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.guards = []
        for target in ('subprocess.Popen', 'subprocess.run', 'os.system',
                       'socket.socket', 'urllib.request.urlopen'):
            guard = patch(target, side_effect=AssertionError(target))
            self.guards.append(guard.start())
            self.addCleanup(guard.stop)

    def tearDown(self):
        for guard in self.guards:
            guard.assert_not_called()

    def lookup(self, authorities):
        return tuple((authority, success(authority)) for authority in authorities)

    def scan(self, projects, *, accepted=True, lookup=None, status='complete', **kwargs):
        witnesses = tuple((name, 'witness.json') for name in projects) if accepted else ()
        with repository_inputs(self.root, projects, status=status):
            return scan_mixed_repository(self.root, nuget_repository=True,
                nuget_witnesses=witnesses, nuget_lookup=lookup or self.lookup, **kwargs)

    def test_same_package_different_versions_and_same_basenames_are_two_occurrences(self):
        projects = {'a/Witness.csproj': nuget_inputs(selected='1.0.0'),
                    'b/Witness.csproj': nuget_inputs(selected='2.0.0')}
        def lookup(authorities):
            return tuple((a, replace(success(a), used_publication=NuGetPublication(
                a.normalized_version, USED if a.normalized_version == '1.0.0' else LATEST, True)))
                for a in authorities)
        batch = Mock(side_effect=lookup)
        report = self.scan(projects, lookup=batch)
        self.assertEqual(len(batch.call_args.args[0]), 2)
        batch.assert_called_once()
        self.assertEqual(report.summary, MetricSummary(2, 2, 1.0, 1.0, 0.5, 0.5, 1.0))
        data = report_to_dict(report, 'SECRET_ROOT')
        self.assertEqual(data['schema_version'], 3)
        self.assertNotIn('nuget', data['version_evidence'])
        self.assertEqual([row['source_id'] for row in data['dependencies']], sorted(projects))
        self.assertEqual([row['used_version'] for row in data['dependencies']], ['1.0.0', '2.0.0'])
        self.assertEqual([row['name'] for row in data['dependencies']], ['alpha', 'alpha'])
        self.assertEqual([row['source_id'] for row in data['nuget_sources']], sorted(projects))
        self.assertTrue(all(row['summary']['dependencies_discovered'] == 1 for row in data['nuget_sources']))
        human = format_human(report, 'SECRET_ROOT', verbose=True)
        self.assertNotIn('SECRET_ROOT', human)
        for name in projects:
            self.assertIn('NuGet source: ' + json.dumps(name), human)
        self.assertIn('no cross-project deduplication', human)
        self.assertNotIn('selection is required', human)

    def test_identical_capabilities_with_differing_results_stay_independent_in_one_batch(self):
        projects = {'a/Witness.csproj': nuget_inputs(), 'b/Witness.csproj': nuget_inputs()}
        supervisor = Mock()
        supervisor.lookup.side_effect = [success(Mock(normalized_version='1.0.0')),
                                         PackageResult(reason='registry_error')]
        report = self.scan(projects, nuget_adapter=NuGetRegistryAdapter(supervisor),
                           lookup=NuGetRegistryAdapter(supervisor).lookup_all)
        self.assertEqual(supervisor.lookup.call_count, 2)
        self.assertEqual(supervisor.lookup.call_args_list[0], supervisor.lookup.call_args_list[1])
        supervisor.close.assert_called_once()
        data = report_to_dict(report, '')
        self.assertEqual(data['summary']['coverage'], 0.5)
        self.assertEqual(data['dependencies'][0]['source_id'], 'a/Witness.csproj')
        self.assertEqual(data['unmeasurable'][0]['source_id'], 'b/Witness.csproj')
        self.assertEqual([s['summary']['dependencies_measured'] for s in data['nuget_sources']], [1, 0])
        self.assertEqual(data['unmeasurable'][0]['nuget_evidence']['origin_state'], 'asserted_public')
        both = self.scan(projects)
        self.assertEqual((len(both.measurements), both.summary.dependencies_discovered), (2, 2))

    def test_known_unavailable_and_unknown_keep_successful_project_and_ecosystem(self):
        (self.root / 'requirements.txt').write_text('alpha==1.0\n')
        for unknown in (False, True):
            failed = {'Witness.csproj': b'broken'} if unknown else nuget_inputs()
            if not unknown:
                del failed['packages.lock.json']
            report = self.scan({'a/Witness.csproj': nuget_inputs(), 'b/Witness.csproj': failed},
                pypi_lookup=lambda n, v: RegistryResult(n, v, USED, '3.0.0', LATEST))
            self.assertEqual(report.summary.dependencies_discovered, None if unknown else 3)
            self.assertEqual(report.summary.dependencies_measured, 2)
            self.assertIsNone(report.summary.coverage)
            self.assertEqual(report.summary.total_libyears, 2.0)
            self.assertEqual(report.by_ecosystem['pypi'].coverage, 1.0)
            self.assertEqual(report.by_ecosystem['nuget'].dependencies_measured, 1)
            self.assertEqual(report.by_ecosystem['nuget'].total_libyears, 1.0)
            self.assertIsNone(report.by_nuget_source['b/Witness.csproj'].total_libyears)
            error, = report_to_dict(report, '')['source_errors']
            self.assertEqual(error['source_id'], 'b/Witness.csproj')
            self.assertNotIn('source_id', report_to_dict(report, '')['dependencies'][0])

    def test_all_three_root_ecosystems_survive_failed_nuget_sources(self):
        (self.root / 'requirements.txt').write_text('alpha==1.0\n')
        (self.root / 'package.json').write_text('{"dependencies":{"alpha":"1.0.0"}}')
        (self.root / 'package-lock.json').write_text(json.dumps({
            'lockfileVersion': 3, 'packages': {'': {}, 'node_modules/alpha': {'version': '1.0.0'}}}))
        (self.root / 'Gemfile.lock').write_text(
            'GEM\n  remote: https://rubygems.org/\n  specs:\n    alpha (1.0.0)\n\n'
            'PLATFORMS\n  ruby\n\nDEPENDENCIES\n  alpha\n\nBUNDLED WITH\n   2.5.0\n')
        def lookup(name, version):
            return RegistryResult(name, version, USED, '3.0.0', LATEST)
        report = self.scan({'broken/A.csproj': {'A.csproj': b'broken'}},
            pypi_lookup=lookup, npm_lookup=lookup, rubygems_lookup=lookup)
        self.assertEqual([row.dependency.ecosystem for row in report.measurements], ['pypi', 'npm', 'rubygems'])
        self.assertEqual((report.summary.dependencies_discovered,
                          report.summary.dependencies_measured, report.summary.total_libyears), (None, 3, 3.0))
        for ecosystem in ('pypi', 'npm', 'rubygems'):
            self.assertEqual(report.by_ecosystem[ecosystem].coverage, 1.0)
        self.assertEqual(set(report_to_dict(report, '')['version_evidence']), {'pypi', 'npm', 'rubygems'})

    def test_shared_parent_lock_failures_keep_two_source_identities(self):
        projects = {'A.csproj': {'A.csproj': nuget_inputs()['Witness.csproj']},
                    'B.csproj': {'B.csproj': nuget_inputs()['Witness.csproj']}}
        report = self.scan(projects, accepted=False)
        self.assertEqual([error.source for error in report.source_errors], ['packages.lock.json'] * 2)
        self.assertEqual([error.source_id for error in report.source_errors], ['A.csproj', 'B.csproj'])
        self.assertEqual(report.summary.dependencies_discovered, 2)
        self.assertIsNone(report.summary.coverage)
        self.assertIsNone(report.summary.dependencies_measured)

    def test_constructor_refusal_is_unknown_and_preserves_project_and_root_sibling(self):
        (self.root / 'requirements.txt').write_text('alpha==1.0\n')
        for refused in ('bad\\name.csproj', 'bad\\parent/Witness.csproj'):
            projects = {'a/Witness.csproj': nuget_inputs(), refused: {}}
            with repository_inputs(self.root, projects) as reads:
                report = scan_mixed_repository(self.root, nuget_repository=True,
                    nuget_witnesses=(('a/Witness.csproj', 'witness.json'),),
                    nuget_lookup=self.lookup,
                    pypi_lookup=lambda n, v: RegistryResult(n, v, USED, '3.0.0', LATEST))
            self.assertEqual((report.summary.dependencies_discovered,
                              report.summary.dependencies_measured, report.summary.coverage), (None, 2, None))
            self.assertEqual(report.summary.total_libyears, 2.0)
            self.assertEqual(report.by_ecosystem['nuget'].dependencies_measured, 1)
            self.assertEqual(report.by_ecosystem['pypi'].coverage, 1.0)
            self.assertTrue(all(project == 'a/Witness.csproj' for project, _ in reads))
            data = report_to_dict(report, '')
            self.assertEqual(data['source_errors'], [{'ecosystem': 'nuget',
                'source': refused.rsplit('/', 1)[-1], 'reason': 'invalid_nuget_project',
                'source_id': refused}])
            self.assertEqual(data['nuget_sources'][1]['summary'],
                             {key: None for key in data['nuget_sources'][1]['summary']})
            human = format_human(report, 'SECRET_ROOT')
            self.assertIn(json.dumps(refused), human)
            self.assertNotIn('SECRET_ROOT', human)

    def test_empty_all_failed_partial_full_and_whole_unavailable_are_distinct(self):
        for names, failures in (((), 0), (('alpha', 'beta'), 2),
                                (('alpha', 'beta'), 1), (('alpha', 'beta'), 0)):
            def lookup(authorities):
                return tuple((a, PackageResult(reason='registry_error') if i < failures else success(a))
                             for i, a in enumerate(authorities))
            report = self.scan({'a/Witness.csproj': nuget_inputs(names)}, lookup=lookup)
            summary = report.by_nuget_source['a/Witness.csproj']
            self.assertEqual(summary.dependencies_discovered, len(names))
            self.assertEqual(summary.dependencies_measured, len(names) - failures)
            self.assertEqual(summary.coverage, (len(names) - failures) / len(names) if names else None)
        report = self.scan({'a/Witness.csproj': nuget_inputs()}, accepted=False)
        self.assertEqual(report.by_ecosystem['nuget'], MetricSummary(1, None, None, None, None, None, None))
        self.assertEqual(report.unmeasurable, ())
        self.assertEqual(report.summary.total_libyears, 0.0)

    def test_local_h3_failure_does_not_remove_other_occurrence(self):
        private = nuget_inputs(witness_change=lambda w: w['packages'][0].update(origins=['SECRET_ORIGIN']))
        batch = Mock(side_effect=self.lookup)
        report = self.scan({'a/Witness.csproj': private, 'b/Witness.csproj': nuget_inputs()}, lookup=batch)
        self.assertEqual(len(batch.call_args.args[0]), 1)
        self.assertEqual(report.summary.coverage, 0.5)
        self.assertEqual(report.unmeasurable[0].reason, 'unsupported_dependency_source')
        self.assertNotIn('SECRET_ORIGIN', format_json(report, '') + format_human(report, ''))

    def test_discovery_refusal_and_unmatched_mapping_are_safe_unknown_sources(self):
        for status in ('incomplete', 'unavailable'):
            batch = Mock()
            report = self.scan({}, status=status, lookup=batch)
            batch.assert_not_called()
            data = report_to_dict(report, '')
            self.assertEqual(data['nuget_sources'][0]['source_id'], None)
            self.assertEqual(data['source_errors'][0]['source_id'], None)
            self.assertEqual(data['source_errors'][0]['reason'], 'nuget_discovery_' + status)
            self.assertIsNone(data['summary']['dependencies_discovered'])
        with repository_inputs(self.root, {}):
            report = scan_mixed_repository(self.root, nuget_repository=True,
                                           nuget_witnesses=(('Missing.csproj', 'w.json'),))
        self.assertEqual(report.source_errors[0].reason, 'nuget_witness_project_missing')
        self.assertEqual(report.by_nuget_source['Missing.csproj'].dependencies_discovered, None)

    def test_project_reference_and_private_assets_preserve_population_boundary(self):
        projects = {'Test/Witness.csproj': nuget_inputs(project_change=lambda b: b.replace(
            b'</ItemGroup>', b'<ProjectReference Include="../SECRET.csproj" />'
            b'</ItemGroup>').replace(b'Version="1.0"', b'Version="1.0" PrivateAssets="all"'))}
        report = self.scan(projects)
        self.assertEqual((len(report.measurements), report.summary.dependencies_discovered), (1, 1))
        self.assertNotIn('SECRET', format_json(report, '') + format_human(report, ''))

    def test_controls_in_automatic_names_are_framed_in_human_and_json(self):
        name = 'a/line\n\x1b\u202e.csproj'
        with repository_inputs(self.root, {name: {'line\n\x1b\u202e.csproj': b'broken'}}):
            report = scan_mixed_repository(self.root, nuget_repository=True)
        human = format_human(report, 'SECRET_ROOT', verbose=True)
        self.assertIn(json.dumps(name, ensure_ascii=True), human)
        self.assertNotIn(name, human)
        self.assertNotIn('SECRET_ROOT', human)
        self.assertNotIn('\x1b', human)
        self.assertEqual(report_to_dict(report, '')['source_errors'][0]['source_id'], name)

    def test_explicit_shape_matches_exact_preimplementation_snapshot(self):
        def lookup(authorities):
            return tuple((a, replace(success(a), latest_publication=NuGetPublication('2.0.0', LATEST, True)))
                         for a in authorities)
        with fixture_nuget_reads(self.root, nuget_inputs()):
            report = scan_mixed_repository(self.root, nuget_request=NuGetRequest('Witness.csproj', 'witness.json'),
                                           nuget_lookup=lookup)
        baseline = (Path(__file__).parent / 'fixtures/nuget/explicit-report-v3.json').read_text()
        current = json.loads(format_json(report, ''))
        evidence = current['dependencies'][0]['nuget_evidence']
        self.assertEqual(evidence.pop('measurement_basis'), 'bound_snapshot_namespace')
        self.assertEqual(evidence.pop('namespace_basis'), 'accepted_producer_origin')
        self.assertEqual(evidence.pop('assurance')['public_content'], 'public_agreement')
        self.assertEqual(evidence.pop('population_basis'), 'declaration_derived')
        self.assertEqual(current['version_evidence']['nuget'].pop('population_basis'), 'declaration_derived')
        self.assertEqual(current, json.loads(baseline))
        self.assertNotIn('source_id', baseline)
        self.assertNotIn('nuget_sources', baseline)

    def call(self, options, **kwargs):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main([str(self.root), *options], **kwargs)
        return code, out.getvalue(), err.getvalue()

    def test_ordinary_cli_human_json_verbose_explicit_mapping_and_no_selection(self):
        projects = {'a/Witness.csproj': nuget_inputs(), 'b/Witness.csproj': nuget_inputs()}
        for options in ((), ('--json',), ('--json', '--verbose')):
            with repository_inputs(self.root, projects):
                code, output, errors = self.call(options)
            self.assertEqual((code, errors), (0, ''))
            if '--json' in options:
                self.assertEqual(len(json.loads(output)['nuget_sources']), 2)
            else:
                self.assertIn('NuGet source "a/Witness.csproj"', output)
                self.assertNotIn('selection is required', output)
        with repository_inputs(self.root, projects), patch('libyears.scan.NuGetRegistryAdapter') as adapter:
            adapter.return_value.lookup_all.side_effect = self.lookup
            code, output, errors = self.call(['--json', '--nuget-witness', 'b/Witness.csproj=witness.json'])
        self.assertEqual((code, errors), (0, ''))
        self.assertEqual(json.loads(output)['dependencies'][0]['source_id'], 'b/Witness.csproj')
        self.assertEqual(json.loads(output)['summary']['coverage'], None)
        adapter.return_value.lookup_all.assert_called_once()

    def test_bad_mappings_are_private_usage_errors_before_ca_snapshot_or_scan(self):
        invalid = [['--nuget-witness', value] for value in (
            'SECRET', 'A.csproj=SECRET=w.json', '../SECRET.csproj=w.json',
            'A.csproj=../SECRET.json', 'A.csproj=packages.lock.json', '=SECRET.json')]
        invalid += [['--nuget-witness', 'A.csproj=w.json', '--nuget-witness', 'A.csproj=SECRET.json'],
                    ['--nuget-witness', 'A.csproj=SECRET.json', '--nuget-project', 'A.csproj'],
                    ['--nuget-wit', 'A.csproj=SECRET.json']]
        for options in invalid:
            scan = Mock()
            with patch('libyears.cli.parse_snapshot') as snapshot, patch('libyears.cli.ssl.create_default_context') as ca:
                code, output, errors = self.call([*options, '--resolved', 'SECRET', '--ca-bundle', 'SECRET'], scan=scan)
            self.assertEqual((code, output), (1, ''))
            self.assertNotIn('SECRET', errors)
            scan.assert_not_called(); snapshot.assert_not_called(); ca.assert_not_called()
        with patch('libyears.scan._python_source_result') as read:
            with self.assertRaises(NuGetRepositoryRequestError):
                scan_mixed_repository(self.root, nuget_repository=True, nuget_request=NuGetRequest('A.csproj'))
            read.assert_not_called()

    def test_direct_file_bypasses_discovery_and_mapping_rejected(self):
        path = self.root / 'requirements.txt'
        path.write_text('')
        with patch('libyears.nuget_sources.discover_nuget_candidates') as discover, \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(main([str(path), '--json']), 0)
            self.assertEqual(main([str(path), '--nuget-witness', 'A.csproj=w.json']), 1)
        discover.assert_not_called()

    def test_ordinary_systemic_and_render_errors_do_not_echo_private_paths(self):
        for target in ('scan', 'render'):
            options = {}
            if target == 'scan':
                options['scan'] = Mock(side_effect=RuntimeError('SECRET_PATH'))
                context = patch('libyears.cli.format_human')
            else:
                context = patch('libyears.cli.format_human', side_effect=RuntimeError('SECRET_PATH'))
            with repository_inputs(self.root, {}), context:
                code, output, errors = self.call([], **options)
            self.assertEqual((code, output), (2, ''))
            self.assertNotIn('SECRET_PATH', errors)
