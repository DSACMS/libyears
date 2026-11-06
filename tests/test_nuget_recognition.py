"""Portable human recognition composition, separate from real traversal tests."""

from contextlib import ExitStack, redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.cli import main
from libyears.model import RegistryResult
from libyears.nuget_discovery import NuGetRecognition
from libyears.output import format_human, format_json
from libyears.scan import NuGetRequest, scan_mixed_repository


class RecognitionCompositionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.empty = scan_mixed_repository(self.root)

    def call(self, recognition, *options, report=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        scan = Mock(return_value=self.empty if report is None else report)
        with patch('libyears.cli.discover_nuget_candidates', return_value=recognition) as discover, \
                redirect_stdout(stdout), redirect_stderr(stderr):
            code = main([str(self.root), *options], scan=scan)
        self.assertEqual((code, stderr.getvalue()), (0, ''))
        return stdout.getvalue(), scan, discover

    def test_zero_candidates_preserves_exact_human_output(self):
        output, scan, discover = self.call(NuGetRecognition())
        self.assertEqual(output, format_human(self.empty, str(self.root)))
        scan.assert_called_once_with(str(self.root))
        discover.assert_called_once_with(str(self.root))

    def test_one_and_many_never_select_measure_or_query_nuget(self):
        for names in (('Only.csproj',), ('a/One.csproj', 'b/Two.csproj')):
            with self.subTest(names=names), ExitStack() as stack:
                guards = [stack.enter_context(patch(target)) for target in (
                    'libyears.scan.read_nuget_source', 'subprocess.Popen',
                    'subprocess.run', 'socket.socket', 'urllib.request.urlopen',
                )]
                evidence = NuGetRecognition(candidates=names)
                output, scan, _ = self.call(evidence)
                self.assertIn(f'NuGet / C# project candidates: {len(names)} (bounded search).', output)
                self.assertIn('Search covers root through depth 4;', output)
                self.assertIn('hidden/generated/dependency directories are excluded', output)
                self.assertNotIn('Ecosystems: none', output)
                self.assertIn('Ecosystems scanned for measurement: none', output)
                self.assertIn('No NuGet measurement was performed.', output)
                self.assertIn("parent directory as PATH", output)
                self.assertIn('--nuget-project NAME.csproj', output)
                self.assertIn('packages.lock.json', output)
                self.assertIn('--nuget-provenance NAME.json', output)
                self.assertIn('0 / 0 measured; total 0.00', output)
                for name in names:
                    self.assertIn(json.dumps(name), output)
                scan.assert_called_once_with(str(self.root))
                for guard in guards:
                    guard.assert_not_called()

    def test_incomplete_unavailable_and_root_metadata_failure_are_truthful(self):
        for status in ('incomplete', 'unavailable'):
            output, _, _ = self.call(NuGetRecognition(status))
            self.assertIn(f'NuGet project recognition {status}', output)
            self.assertIn('presence and candidate count are undetermined', output)
            self.assertIn('No NuGet measurement was performed.', output)
            self.assertNotIn('Ecosystems: none', output)
            self.assertNotIn('project candidates: 0', output)
        stdout = io.StringIO()
        with patch('libyears.cli.Path.is_dir', side_effect=OSError('private diagnostic')), \
                redirect_stdout(stdout):
            code = main([str(self.root)], scan=Mock(return_value=self.empty))
        self.assertEqual(code, 0)
        self.assertIn('recognition incomplete', stdout.getvalue())
        self.assertNotIn('private diagnostic', stdout.getvalue())

    def test_candidate_names_are_escaped_and_never_interpolated_into_commands(self):
        names = ('a/line\n\x1b[31m$(not-a-command)`literal`\u202e.csproj',)
        output, _, _ = self.call(NuGetRecognition(candidates=names))
        self.assertIn(json.dumps(names[0], ensure_ascii=True), output)
        self.assertNotIn(names[0], output)
        self.assertEqual([line.strip() for line in output.splitlines() if line.strip().startswith('python3')],
                         ['python3 -m libyears PATH --nuget-project NAME.csproj'])

    def test_json_and_verbose_json_are_byte_identical_and_never_discover(self):
        (self.root / 'Present.csproj').write_text('not read')
        expected = format_json(self.empty, str(self.root))
        for extra in (('--json',), ('--json', '--verbose')):
            output, scan, discover = self.call(NuGetRecognition(candidates=('Present.csproj',)), *extra)
            self.assertEqual(output, expected)
            discover.assert_not_called()
            scan.assert_called_once_with(str(self.root))

    def test_direct_file_and_explicit_project_bypass_recognition(self):
        target = self.root / 'requirements.txt'
        target.write_text('')
        stdout = io.StringIO()
        with patch('libyears.cli.discover_nuget_candidates') as discover, redirect_stdout(stdout):
            self.assertEqual(main([str(target)], scan=Mock(return_value=self.empty)), 0)
        discover.assert_not_called()
        output, scan, discover = self.call(NuGetRecognition(candidates=('Other.csproj',)),
                                         '--nuget-project', 'Chosen.csproj')
        discover.assert_not_called()
        scan.assert_called_once_with(str(self.root), nuget_request=NuGetRequest('Chosen.csproj', None))
        self.assertEqual(output, format_human(self.empty, str(self.root)))

    def test_three_measurable_siblings_keep_exact_report_and_numeric_facts(self):
        (self.root / 'requirements.txt').write_text('alpha==1.0\n')
        (self.root / 'package.json').write_text('{"dependencies":{"alpha":"^1.0.0"}}')
        (self.root / 'package-lock.json').write_text(json.dumps({
            'lockfileVersion': 3, 'packages': {'': {}, 'node_modules/alpha': {'version': '1.0.0'}},
        }))
        (self.root / 'Gemfile.lock').write_text(
            'GEM\n  remote: https://rubygems.org/\n  specs:\n    alpha (1.0.0)\n\n'
            'PLATFORMS\n  ruby\n\nDEPENDENCIES\n  alpha\n\nBUNDLED WITH\n   2.5.0\n')
        used = datetime(2020, 1, 1, tzinfo=timezone.utc)
        def lookup(name, version):
            return RegistryResult(name, version, used, '2.0.0', used + timedelta(days=365.25))

        with patch('os.supports_dir_fd', set()), \
                patch('libyears.scan.read_nuget_source') as nuget_source:
            report = scan_mixed_repository(self.root, pypi_lookup=lookup,
                                          npm_lookup=lookup, rubygems_lookup=lookup)
            baseline_json = format_json(report, str(self.root))
            self.assertEqual([row.dependency.ecosystem for row in report.measurements],
                             ['pypi', 'npm', 'rubygems'])
            self.assertEqual((report.summary.dependencies_discovered,
                              report.summary.dependencies_measured, report.summary.total_libyears), (3, 3, 3.0))
            for recognition in (NuGetRecognition(candidates=('one/P.csproj',)),
                                NuGetRecognition('incomplete'), NuGetRecognition('unavailable')):
                output, scan, _ = self.call(recognition, report=report)
                self.assertIn('Ecosystems scanned for measurement: npm, pypi, rubygems', output)
                self.assertIn('3 / 3 measured; total 3.00', output)
                self.assertIn('No NuGet measurement was performed.', output)
                for ecosystem in ('npm', 'pypi', 'rubygems'):
                    self.assertIn(f'{ecosystem}: 100.0% coverage; 1 / 1 measured', output)
                self.assertEqual(format_json(report, str(self.root)), baseline_json)
                scan.assert_called_once_with(str(self.root))
            nuget_source.assert_not_called()

    def test_single_measured_ecosystem_and_verbose_keep_metrics(self):
        (self.root / 'requirements.txt').write_text('alpha==1.0\n')
        used = datetime(2020, 1, 1, tzinfo=timezone.utc)
        report = scan_mixed_repository(self.root, pypi_lookup=lambda n, v: RegistryResult(n, v, used, v, used))
        evidence = NuGetRecognition(candidates=('Only.csproj',))
        for extra in ((), ('--verbose',)):
            output, _, _ = self.call(evidence, *extra, report=report)
            self.assertIn('Ecosystem scanned for measurement: pypi', output)
            self.assertIn('Measured: 1 / 1 dependencies', output)
            self.assertIn('No NuGet measurement was performed.', output)


class RecognitionFilesystemIntegrationTests(unittest.TestCase):
    def test_ordinary_cli_uses_real_discovery_or_explicit_capability_refusal(self):
        # This asserts the real integration on every host. Successful traversal
        # safety itself has separate capability-gated filesystem witnesses.
        from libyears.nuget_discovery import discovery_available
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'Only.csproj').write_text('malformed, never parsed')
            for disabled in (False, True):
                stdout = io.StringIO()
                with patch('os.supports_dir_fd', set() if disabled else os.supports_dir_fd), \
                        patch('libyears.scan.read_nuget_source') as source, redirect_stdout(stdout):
                    available = discovery_available()
                    self.assertEqual(main([str(root)]), 0)
                    source.assert_not_called()
                output = stdout.getvalue()
                self.assertNotIn('Ecosystems: none', output)
                self.assertIn('No NuGet measurement was performed.', output)
                if available:
                    self.assertIn('project candidates: 1', output)
                else:
                    self.assertIn('recognition unavailable', output)
