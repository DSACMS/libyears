"""Exact NuGet activation, safe usage/errors and composed reports (T013)."""

from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.cli import main
from libyears.model import NuGetPublication
from libyears.nuget_supervisor import NuGetWorkerFailure, PackageResult
from libyears.scan import NuGetRequest, scan_mixed_repository
from tests.nuget_fixtures import fixture_nuget_reads
from tests.test_nuget_scan import nuget_inputs


class NuGetCLITests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for target in ('subprocess.Popen', 'subprocess.run', 'os.system',
                       'socket.socket', 'urllib.request.urlopen'):
            guard = patch(target, side_effect=AssertionError(target))
            guard.start()
            self.addCleanup(guard.stop)

    def call(self, options, *, scan=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(options, scan=scan)
        return status, stdout.getvalue(), stderr.getvalue()

    def lookup_all(self, authorities):
        used = datetime(2020, 1, 1, tzinfo=timezone.utc)
        return tuple((authority, PackageResult(origin_state='public_content_verified',
            content_hash_state='public_agreement',
            used_publication=NuGetPublication(authority.normalized_version, used, True),
            latest_publication=NuGetPublication('2.0.0', used + timedelta(days=365.25), True)))
            for authority in authorities)

    def composed_scan(self, path, **kwargs):
        return scan_mixed_repository(path, nuget_lookup=self.lookup_all, **kwargs)

    def options(self, *extra):
        return [str(self.root), '--nuget-project', 'Witness.csproj',
                '--nuget-provenance', 'witness.json', *extra]

    def test_help_explains_bound_provenance_and_contemporaneous_attestation(self):
        status, stdout, stderr = self.call(['--help'])
        self.assertEqual((status, stderr), (0, ''))
        help_text = ' '.join(stdout.split())
        for text in ('native NuGet package provenance', 'contemporaneous producer attestation',
                     'exact project/lock bytes, framework and input influences',
                     'retrospective replay cannot substitute for original-event attestation'):
            self.assertIn(text, help_text)

    def test_explicit_selection_composes_scan_and_both_reports_with_exit_zero(self):
        for extra in ((), ('--verbose',), ('--json',), ('--json', '--verbose')):
            with self.subTest(extra=extra), fixture_nuget_reads(self.root, nuget_inputs()):
                status, stdout, stderr = self.call(self.options(*extra), scan=self.composed_scan)
                self.assertEqual((status, stderr), (0, ''))
                if '--json' in extra:
                    data = json.loads(stdout)
                    self.assertEqual(data['schema_version'], 3)
                    self.assertEqual(data['ecosystems'], ['nuget'])
                    self.assertEqual(data['dependencies'][0]['version_source'], 'packages_lock')
                else:
                    self.assertIn('Witness.csproj; framework: net10.0', stdout)
                    self.assertIn('supplied producer/supplier assertions', stdout)
        with fixture_nuget_reads(self.root, nuget_inputs()):
            ordinary = self.call(self.options('--json'), scan=self.composed_scan)[1]
            verbose = self.call(self.options('--json', '--verbose'), scan=self.composed_scan)[1]
        self.assertEqual(ordinary, verbose)

    def test_usage_failures_are_safe_and_precede_all_content_reads(self):
        invalid = [
            ['--nuget-provenance', 'SECRET.json'],
            ['--nuget-project', 'A.csproj', '--nuget-project', 'SECRET.csproj'],
            ['--nuget-project', 'A.csproj', '--nuget-provenance', 'A.json',
             '--nuget-provenance', 'SECRET.json'],
            ['--nuget-project'], ['--nuget-provenance'],
            ['--nuget-project='], ['--nuget-project', 'A.csproj', '--nuget-provenance='],
            ['--nuget-project', 'A.csproj', '--nuget-provenance', 'packages.lock.json'],
        ]
        invalid += [[option, 'SECRET-value'] for option in (
            '--n', '--nuget', '--nuget-proj', '--nuget-prov', '--nuget-projects',
            '-nuget-project', '-nuget-provenance', '---nuget-project', '---nuget-provenance')]
        invalid += [[option + '=SECRET-value'] for option in (
            '-nuget-project', '-nuget-provenance', '---nuget-project', '---nuget-provenance')]
        values = ('../SECRET.csproj', '/SECRET.csproj', r'C:\SECRET.csproj',
                  'C:SECRET.csproj', r'nested\SECRET.csproj', 'SECRET/*.csproj',
                  '*.csproj', '?.csproj', '[SECRET].csproj', '{SECRET}.csproj',
                  'A.csproj;SECRET.csproj', 'A.csproj,SECRET.csproj', 'SECRET.txt',
                  'SECRET\n.csproj', 'SECRET\x00.csproj', 'https://user:SECRET@host/A.csproj')
        invalid += [['--nuget-project', value] for value in values]
        invalid += [['--nuget-project', 'A.csproj', '--nuget-provenance', value]
                    for value in ('../SECRET.json', '/SECRET.json', '*.json', 'A.json;SECRET.json',
                                  'SECRET.txt', 'SECRET\n.json', 'https://user:SECRET@host/A.json')]
        scan = Mock(side_effect=AssertionError('usage must precede scan'))
        with patch('libyears.cli.parse_snapshot') as snapshot, \
                patch('libyears.cli.ssl.create_default_context') as ca:
            for options in invalid:
                with self.subTest(options=options):
                    status, stdout, stderr = self.call([str(self.root), *options,
                        '--resolved', 'SECRET-snapshot', '--ca-bundle', 'SECRET-ca'], scan=scan)
                    self.assertEqual((status, stdout), (1, ''))
                    self.assertIn('invalid NuGet command line arguments', stderr)
                    self.assertNotIn('SECRET', stderr)
            snapshot.assert_not_called()
            ca.assert_not_called()
        scan.assert_not_called()

    def test_direct_file_and_missing_root_are_safe_usage_errors(self):
        target = self.root / 'SECRET-requirements.txt'
        target.write_text('not read')
        scan = Mock()
        for path in (str(target), str(self.root / 'SECRET-missing')):
            status, stdout, stderr = self.call([path, '--nuget-project', 'Witness.csproj'], scan=scan)
            self.assertEqual((status, stdout), (1, ''))
            self.assertNotIn('SECRET', stderr)
        scan.assert_not_called()

    def test_root_inspection_failure_is_safe_before_any_content_read(self):
        scan = Mock()
        for error in (OSError('SECRET-root'), ValueError('SECRET-root')):
            with self.subTest(error=type(error).__name__), \
                    patch('libyears.cli.Path.is_dir', side_effect=error), \
                    patch('libyears.cli.parse_snapshot') as snapshot, \
                    patch('libyears.cli.ssl.create_default_context') as ca:
                status, stdout, stderr = self.call(self.options(
                    '--resolved', 'SECRET-snapshot', '--ca-bundle', 'SECRET-ca'), scan=scan)
                self.assertEqual((status, stdout), (1, ''))
                self.assertNotIn('SECRET', stderr)
                self.assertNotIn('Traceback', stderr)
                snapshot.assert_not_called()
                ca.assert_not_called()
        scan.assert_not_called()

    def test_capitalized_malformed_options_do_not_echo_secret_values(self):
        for option in ('--NuGet-project=SECRET-canary', '--NUGET-PROVENANCE=SECRET-canary'):
            with self.subTest(option=option):
                status, stdout, stderr = self.call([str(self.root), option])
                self.assertEqual((status, stdout), (1, ''))
                self.assertNotIn('SECRET', stderr)
                self.assertIn('invalid NuGet command line arguments', stderr)

    def test_case_variant_abbreviated_and_malformed_options_are_safe_before_content_reads(self):
        scan = Mock(side_effect=AssertionError('malformed options must not activate scan'))
        names = ('NuGet-project', 'NUGET-PROJECT', 'NuGeT-ProJect',
                 'NuGet-provenance', 'NUGET-PROVENANCE', 'nUgEt-pRoVeNaNcE',
                 'N', 'NuG', 'NUGET-PROJ', 'NuGet-PrOv')
        with patch('libyears.cli.parse_snapshot') as snapshot, \
                patch('libyears.cli.ssl.create_default_context') as ca:
            for name in names:
                for prefix in ('-', '--', '---'):
                    for joined in (False, True):
                        option = prefix + name
                        values = [option + '=SECRET-value'] if joined else [option, 'SECRET-value']
                        with self.subTest(option=option, joined=joined):
                            status, stdout, stderr = self.call([str(self.root), *values,
                                '--resolved', 'SECRET-snapshot', '--ca-bundle', 'SECRET-ca'], scan=scan)
                            self.assertEqual((status, stdout), (1, ''))
                            self.assertNotIn('SECRET', stderr)
                            self.assertNotIn('Traceback', stderr)
                            self.assertIn('invalid NuGet command line arguments', stderr)
            snapshot.assert_not_called()
            ca.assert_not_called()
        scan.assert_not_called()

    def test_unrelated_ordinary_argparse_errors_keep_their_existing_context(self):
        scan = Mock()
        status, stdout, stderr = self.call([str(self.root), '--UNKNOWN=PUBLIC-value'], scan=scan)
        self.assertEqual((status, stdout), (1, ''))
        self.assertIn('unrecognized arguments: --UNKNOWN=PUBLIC-value', stderr)
        self.assertNotIn('invalid NuGet command line arguments', stderr)
        scan.assert_not_called()

    def test_missing_project_and_source_failures_empty_partial_are_completed_reports(self):
        cases = []
        missing = nuget_inputs()
        del missing['Witness.csproj']
        cases.append((missing, 'nuget_project_missing'))
        missing_lock = nuget_inputs()
        del missing_lock['packages.lock.json']
        cases.append((missing_lock, 'lockfile_missing'))
        cases.append((nuget_inputs(()), None))
        cases.append((nuget_inputs(('alpha', 'beta'), lock_change=lambda value:
            value['dependencies']['net10.0']['beta'].pop('resolved')), None))
        for files, reason in cases:
            for extra in ((), ('--json',)):
                with self.subTest(reason=reason, extra=extra), fixture_nuget_reads(self.root, files):
                    status, stdout, stderr = self.call(self.options(*extra), scan=self.composed_scan)
                    self.assertEqual((status, stderr), (0, ''))
                    if reason is not None:
                        self.assertIn(reason, stdout)
                    if '--json' in extra:
                        data = json.loads(stdout)
                        self.assertEqual(data['ecosystems'], ['nuget'])

    def test_omitted_witness_never_accepts_found_file(self):
        with fixture_nuget_reads(self.root, nuget_inputs()) as reads:
            status, stdout, stderr = self.call([str(self.root), '--nuget-project', 'Witness.csproj',
                                               '--json'], scan=self.composed_scan)
        self.assertEqual((status, stderr), (0, ''))
        self.assertEqual(json.loads(stdout)['source_errors'][0]['reason'], 'nuget_provenance_missing')
        self.assertNotIn('witness.json', [call.args[1] for call in reads.call_args_list])

    def test_ordinary_scan_omits_colocated_nuget_and_preserves_other_abbreviations(self):
        for name in ('Witness.csproj', 'Other.csproj', 'packages.lock.json', 'witness.json',
                     'project.assets.json', 'packages.config'):
            (self.root / name).write_text('SECRET-unselected')
        with patch('libyears.scan.read_nuget_source') as source:
            status, stdout, stderr = self.call([str(self.root), '--js'], scan=self.composed_scan)
        self.assertEqual((status, stderr), (0, ''))
        self.assertNotIn('nuget', stdout)
        self.assertNotIn('SECRET', stdout)
        source.assert_not_called()

    def test_one_selected_project_and_python_ruby_options_keep_their_scopes(self):
        (self.root / 'Other.csproj').write_text('SECRET-unselected-project')
        snapshot_file = self.root / 'resolved.txt'
        snapshot_file.write_text('alpha==1.5\n')
        seen = []
        def scan(path, **kwargs):
            seen.append(kwargs)
            return self.composed_scan(path, **kwargs)
        with fixture_nuget_reads(self.root, nuget_inputs()) as reads:
            status, stdout, stderr = self.call(self.options('--resolved', str(snapshot_file), '--json'), scan=scan)
        self.assertEqual((status, stderr), (0, ''))
        self.assertEqual(seen[0]['nuget_request'], NuGetRequest('Witness.csproj', 'witness.json'))
        self.assertEqual(seen[0]['snapshot'].entries[0].version, '1.5')
        self.assertNotIn('Other.csproj', [call.args[1] for call in reads.call_args_list])
        (self.root / 'Gemfile').write_text('source "https://rubygems.org"\n')
        (self.root / 'Gemfile.lock').write_text('GEM\n  remote: https://rubygems.org\n  specs:\n'
                                             '\nPLATFORMS\n  ruby\n\nDEPENDENCIES\n')
        with fixture_nuget_reads(self.root, nuget_inputs()):
            status, stdout, stderr = self.call(self.options('--ruby-group', 'default', '--json'), scan=scan)
        self.assertEqual((status, stderr), (0, ''))
        self.assertEqual(seen[-1]['ruby_groups'], ('default',))
        self.assertEqual(json.loads(stdout)['version_evidence']['rubygems']['scope'], 'selected_declared_groups')

    def test_safe_input_systemic_and_rendering_failures_and_success_path_privacy(self):
        for error, expected in ((OSError('SECRET-input'), 1),
                                (RuntimeError('SECRET-exception'), 2), (NuGetWorkerFailure(), 2)):
            for extra in ((), ('--json', '--verbose')):
                status, stdout, stderr = self.call(self.options(*extra), scan=Mock(side_effect=error))
                self.assertEqual((status, stdout), (expected, ''))
                self.assertNotIn('SECRET', stderr)
                self.assertNotIn('Traceback', stderr)
        for target in ('libyears.cli.parse_snapshot', 'libyears.cli.ssl.create_default_context'):
            with patch(target, side_effect=OSError('SECRET-argument')):
                options = self.options('--resolved', 'SECRET-snapshot') if 'snapshot' in target else self.options('--ca-bundle', 'SECRET-ca')
                status, stdout, stderr = self.call(options)
                self.assertEqual((status, stdout), (1, ''))
                self.assertNotIn('SECRET', stderr)
        for extra, formatter in (((), 'format_human'), (('--json',), 'format_json')):
            with fixture_nuget_reads(self.root, nuget_inputs()), \
                    patch('libyears.cli.' + formatter, side_effect=RuntimeError('SECRET-render')):
                status, stdout, stderr = self.call(self.options(*extra), scan=self.composed_scan)
            self.assertEqual((status, stdout), (2, ''))
            self.assertNotIn('SECRET', stderr)
        private_root = self.root / 'SECRET-root'
        private_root.mkdir()
        with fixture_nuget_reads(private_root, nuget_inputs()):
            for extra in ((), ('--verbose',), ('--json',), ('--json', '--verbose')):
                status, stdout, stderr = self.call([str(private_root), '--nuget-project', 'Witness.csproj',
                    '--nuget-provenance', 'witness.json', *extra], scan=self.composed_scan)
                self.assertEqual((status, stderr), (0, ''))
                self.assertNotIn('SECRET', stdout)


if __name__ == '__main__':
    unittest.main()
