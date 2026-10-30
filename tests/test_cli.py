import json
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from libyears.cli import main
from libyears.model import MetricSummary, RegistryResult
from libyears.pypi import PyPIResult
from libyears.scan import RubyGroupRequestError, ScanReport


def empty_report():
    return ScanReport(MetricSummary(0, 0, None, 0.0, None, None, None), (), ())


class CLITests(unittest.TestCase):
    def test_resolved_dogfooding_snapshot_matches_only_direct_dependencies(self):
        requirements = """requests
pygal
pandas
pytest
pylint
metrics-dash-backend-tools
urllib3>=2.6.3
"""
        snapshot = """astroid==4.3.3
certifi==2026.7.22
charset-normalizer==3.5.2
dill==0.4.1
idna==3.20
importlib_metadata==9.0.1
iniconfig==2.3.0
isort==9.0.2
mccabe==0.7.0
metrics-dash-backend-tools==0.1.5
mypy_extensions==1.1.0
numpy==2.4.6
packaging==26.3
pandas==2.3.3
platformdirs==4.12.2
pluggy==1.6.0
pygal==3.1.3
Pygments==2.21.0
pylint==4.1.1
pytest==9.1.1
python-dateutil==2.9.0.post0
pytz==2026.4
requests==2.34.2
six==1.17.0
tomlkit==0.15.1
tzdata==2026.4
urllib3==2.8.0
zipp==4.1.0
"""
        expected = {
            "requests": "2.34.2",
            "pygal": "3.1.3",
            "pandas": "2.3.3",
            "pytest": "9.1.1",
            "pylint": "4.1.1",
            "metrics-dash-backend-tools": "0.1.5",
            "urllib3": "2.8.0",
        }
        release_time = datetime(2024, 1, 1, tzinfo=timezone.utc)

        def lookup(name, version):
            return PyPIResult(name, version, release_time, version, release_time)

        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "requirements.txt").write_text(requirements, encoding="utf-8")
            snapshot_path = root / "resolved.txt"
            snapshot_path.write_text(snapshot, encoding="utf-8")
            with patch("libyears.scan.PyPIAdapter.lookup", side_effect=lookup) as registry, redirect_stdout(output):
                code = main([str(root), "--resolved", str(snapshot_path), "--json"])

        self.assertEqual(code, 0)
        report = json.loads(output.getvalue())
        self.assertEqual(report["unmeasurable"], [])
        self.assertEqual(report["summary"]["dependencies_discovered"], 7)
        self.assertEqual(report["summary"]["dependencies_measured"], 7)
        self.assertEqual(report["summary"]["coverage"], 1.0)
        self.assertEqual(
            {item["name"]: item["used_version"] for item in report["dependencies"]},
            expected,
        )
        self.assertCountEqual(
            [call.args for call in registry.call_args_list], list(expected.items())
        )

    def test_default_path(self):
        output = io.StringIO()
        with patch("libyears.cli.scan_mixed_repository", return_value=empty_report()) as scan, redirect_stdout(output):
            code = main([])
        self.assertEqual(code, 0)
        scan.assert_called_once_with(".")

    def test_ca_bundle_is_threaded_to_scan(self):
        with patch("libyears.cli.ssl.create_default_context"), patch("libyears.cli.scan_mixed_repository", return_value=empty_report()) as scan:
            self.assertEqual(main([".", "--ca-bundle", "/tmp/ca.pem"]), 0)
        scan.assert_called_once_with(".", ca_bundle="/tmp/ca.pem")

    def test_missing_ca_bundle_is_filesystem_error(self):
        errors = io.StringIO()
        with patch("libyears.cli.scan_mixed_repository") as scan, redirect_stderr(errors):
            code = main([".", "--ca-bundle", "/definitely/missing/libyears-ca.pem"])
        self.assertEqual(code, 1)
        scan.assert_not_called()

    def test_explicit_path(self):
        with patch("libyears.cli.scan_mixed_repository", return_value=empty_report()) as scan:
            code = main(["/tmp/repository"])
        self.assertEqual(code, 0)
        scan.assert_called_once_with("/tmp/repository")

    def test_resolved_snapshot_is_parsed_and_passed_to_scan(self):
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / "resolved.txt"
            snapshot_path.write_text("requests==2.31.0\n", encoding="utf-8")
            with patch("libyears.cli.scan_mixed_repository", return_value=empty_report()) as scan, redirect_stdout(output):
                code = main([".", "--resolved", str(snapshot_path)])
        self.assertEqual(code, 0)
        scan.assert_called_once()
        self.assertEqual(scan.call_args.args, (".",))
        snapshot = scan.call_args.kwargs["snapshot"]
        self.assertEqual(snapshot.entries[0].version, "2.31.0")
        self.assertEqual(snapshot.source_path, str(snapshot_path))

    def test_missing_resolved_snapshot_is_filesystem_error(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / "missing.txt")
            errors = io.StringIO()
            with patch("libyears.cli.scan_mixed_repository") as scan, redirect_stderr(errors):
                code = main([".", "--resolved", missing])
        self.assertEqual(code, 1)
        scan.assert_not_called()

    def test_resolved_snapshot_scan_failure_is_systemic_error(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / "resolved.txt"
            snapshot_path.write_text("requests==2.31.0\n", encoding="utf-8")
            with redirect_stderr(io.StringIO()):
                code = main(
                    [".", "--resolved", str(snapshot_path)],
                    scan=lambda path, snapshot: (_ for _ in ()).throw(RuntimeError("boom")),
                )
        self.assertEqual(code, 2)

    def test_resolved_snapshot_measurement_gap_is_success(self):
        report = ScanReport(MetricSummary(1, 0, 0.0, 0.0, None, None, None), (), ())
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / "resolved.txt"
            snapshot_path.write_text("other==1.0\n", encoding="utf-8")
            with patch("libyears.cli.scan_mixed_repository", return_value=report):
                code = main([".", "--resolved", str(snapshot_path)])
        self.assertEqual(code, 0)

    def test_json_output_is_parseable(self):
        output = io.StringIO()
        with patch("libyears.cli.scan_mixed_repository", return_value=empty_report()), redirect_stdout(output):
            code = main(["--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["schema_version"], 3)

    def test_verbose_registry_diagnostics_do_not_change_json(self):
        from libyears.requirements import UnmeasurableRequirement
        report = ScanReport(
            MetricSummary(1, 0, 0.0, 0.0, None, None, None), (),
            (UnmeasurableRequirement("requests", "requests==1.0", "registry_error"),),
            diagnostics=(("requests", "TLS certificate verification failure"),),
            tls_trust="pip-bundled CA fallback",
        )
        human = io.StringIO()
        with patch("libyears.cli.scan_mixed_repository", return_value=report), redirect_stdout(human):
            main(["--verbose"])
        self.assertIn("TLS certificate verification failure", human.getvalue())
        self.assertIn("TLS trust: pip-bundled CA fallback", human.getvalue())
        plain = io.StringIO()
        with patch("libyears.cli.scan_mixed_repository", return_value=report), redirect_stdout(plain):
            main([])
        self.assertNotIn("TLS certificate", plain.getvalue())
        machine = io.StringIO()
        with patch("libyears.cli.scan_mixed_repository", return_value=report), redirect_stdout(machine):
            main(["--verbose", "--json"])
        payload = json.loads(machine.getvalue())
        self.assertEqual(payload["unmeasurable"][0]["reason"], "registry_error")
        self.assertNotIn("diagnostic", machine.getvalue())
        self.assertNotIn("tls_trust", machine.getvalue())

    def test_human_output_preserves_zero_coverage_success(self):
        output = io.StringIO()
        report = ScanReport(
            MetricSummary(1, 0, 0.0, 0.0, None, None, None), (), ()
        )
        with patch("libyears.cli.scan_mixed_repository", return_value=report), redirect_stdout(output):
            code = main([])
        self.assertEqual(code, 0)
        self.assertIn("No libyears measurement could be calculated", output.getvalue())
        self.assertIn("Measured: 0 / 1 dependencies", output.getvalue())
        self.assertNotIn("DEPENDENCY", output.getvalue())
        self.assertNotIn("Total:", output.getvalue())

    def test_scan_failure_returns_systemic_error(self):
        errors = io.StringIO()
        with redirect_stderr(errors):
            code = main([], scan=lambda path: (_ for _ in ()).throw(RuntimeError("boom")))
        self.assertEqual(code, 2)
        self.assertIn("systemic", errors.getvalue())

    def test_domain_value_error_returns_systemic_error(self):
        with redirect_stderr(io.StringIO()):
            code = main([], scan=lambda path: (_ for _ in ()).throw(ValueError("invalid domain data")))
        self.assertEqual(code, 2)

    def test_filesystem_failure_returns_one(self):
        with redirect_stderr(io.StringIO()):
            code = main([], scan=lambda path: (_ for _ in ()).throw(FileNotFoundError("missing")))
        self.assertEqual(code, 1)

    def test_usage_error_returns_one(self):
        with redirect_stderr(io.StringIO()):
            code = main(["one", "two"])
        self.assertEqual(code, 1)


class RubyPublicCLITests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for target in ('urllib.request.urlopen', 'urllib.request.OpenerDirector.open',
                       'subprocess.Popen', 'os.system'):
            guard = patch(target, side_effect=AssertionError('live HTTP or execution'))
            guard.start()
            self.addCleanup(guard.stop)

    def run_cli(self, *args):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = main([str(self.root), *args])
        return code, output.getvalue(), errors.getvalue()

    def test_lock_only_cli_json_verbosity_resolved_isolation_and_unchanged_target(self):
        fixture = Path(__file__).parent / 'fixtures' / 'rubygems' / 'direct_scope.lock'
        lock = self.root / 'Gemfile.lock'
        before = fixture.read_bytes()
        lock.write_bytes(before)
        snapshot = self.root / 'resolved.txt'
        snapshot.write_text('sample==99.0\nbundler==2.0\ntzinfo-data==1.0\n')
        date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        def lookup(name, version):
            return PyPIResult(name, version, date, version, date)
        with patch('libyears.scan.RubyGemsAdapter.lookup', side_effect=lookup) as registry:
            plain = self.run_cli('--json')
            verbose = self.run_cli('--json', '--verbose')
            resolved = self.run_cli('--json', '--resolved', str(snapshot))
            human = self.run_cli()
        self.assertEqual(plain, verbose)
        self.assertEqual(plain, resolved)
        self.assertEqual(plain[0], 0)
        data = json.loads(plain[1])
        self.assertEqual(data['ecosystems'], ['rubygems'])
        self.assertEqual(data['summary']['dependencies_discovered'], 3)
        self.assertEqual(data['summary']['dependencies_measured'], 1)
        self.assertEqual(data['dependencies'][0]['used_version'], '1.0')
        self.assertEqual([item['reason'] for item in data['unmeasurable']],
                         ['lock_version_missing', 'lock_version_missing'])
        self.assertEqual([call.args for call in registry.call_args_list], [('sample', '1.0')] * 4)
        self.assertIn('Measured: 1 / 3', human[1])
        self.assertIn('groups are not interpreted', human[1])
        self.assertEqual(lock.read_bytes(), before)

    def test_completed_no_source_empty_and_broken_source_reports_exit_zero(self):
        (self.root / 'Gemfile').write_text('not executed')
        cases = (None, 'empty_scope.lock', 'direct_scope.lock')
        with patch('libyears.scan.RubyGemsAdapter.lookup', side_effect=AssertionError('no candidates')):
            for fixture_name in cases:
                with self.subTest(fixture=fixture_name):
                    if fixture_name:
                        fixture = Path(__file__).parent / 'fixtures' / 'rubygems' / fixture_name
                        (self.root / 'Gemfile.lock').write_bytes(fixture.read_bytes())
                    if fixture_name == 'direct_scope.lock':
                        (self.root / 'Gemfile.lock').write_text('GEM\n  specs:\n\tbroken\n')
                    code, output, errors = self.run_cli('--json')
                    self.assertEqual((code, errors), (0, ''))
                    data = json.loads(output)
                    if fixture_name == 'direct_scope.lock':
                        self.assertEqual(data['source_errors'][0]['reason'], 'invalid_lockfile')
                        self.assertIsNone(data['summary']['dependencies_measured'])
                    else:
                        self.assertEqual(data['summary']['dependencies_measured'], 0)
                        self.assertEqual(data['ecosystems'], ['rubygems'] if fixture_name else [])
                        self.assertEqual(data['summary']['total_libyears'], 0.0)

    def test_population_budget_failures_never_become_cli_metrics_or_modify_target(self):
        from http.client import IncompleteRead
        from unittest.mock import Mock
        from libyears.rubygems_registry import MAX_RESPONSE_BYTES, RubyGemsAdapter
        from tests.test_registry import BoundedResponse
        from tests.test_rubygems_registry import FakeClock, artifact
        lock = self.root / 'Gemfile.lock'
        lock.write_text('GEM\n  remote: https://rubygems.org\n  specs:\n'
                        '    sample (1.0)\n\nPLATFORMS\n  ruby\nDEPENDENCIES\n  sample\n')
        (self.root / 'Gemfile').write_text('raise "must not execute"\n')
        before = {path.name: path.read_bytes() for path in self.root.iterdir()}
        body = json.dumps([artifact()]).encode()
        cases = (
            BoundedResponse(body, {'Content-Length': str(MAX_RESPONSE_BYTES + 1)}),
            BoundedResponse(body, {'Content-Length': str(len(body) + 1)}),
            BoundedResponse(b'', read_error=IncompleteRead(body, 1)),
        )
        for response in cases:
            with self.subTest(headers=response.headers, error=response.read_error):
                opener = Mock()
                opener.open.side_effect = [BoundedResponse(b'{"name":"sample"}'), response]
                clock = FakeClock()
                with patch('libyears.registry.request.build_opener', return_value=opener):
                    adapter = RubyGemsAdapter(monotonic=clock.monotonic, sleep=clock.sleep)
                with patch('libyears.scan.RubyGemsAdapter', return_value=adapter):
                    code, output, errors = self.run_cli('--json')
                self.assertEqual((code, errors), (0, ''))
                data = json.loads(output)
                self.assertEqual(data['dependencies'], [])
                self.assertEqual(data['source_errors'], [])
                failure = data['unmeasurable'][0]
                self.assertEqual((failure['name'], failure['declared'], failure['reason']),
                                 ('sample', 'sample', 'invalid_registry_response'))
                self.assertEqual(failure['rubygems_evidence'], {'selected_artifacts': [
                    {'version': '1.0', 'platform': 'ruby', 'source': 'https://rubygems.org'}]})
                self.assertEqual(data['summary']['dependencies_discovered'], 1)
                self.assertEqual(data['summary']['dependencies_measured'], 0)
                self.assertEqual(data['summary']['coverage'], 0.0)
                self.assertEqual(data['summary']['total_libyears'], 0.0)
                self.assertEqual(opener.open.call_count, 2)
                self.assertEqual({path.name: path.read_bytes() for path in self.root.iterdir()}, before)

    def test_ruby_cli_ca_bundle_reaches_verified_adapter(self):
        (self.root / 'Gemfile.lock').write_text(
            'GEM\n  remote: https://rubygems.org\n  specs:\n'
            '\nPLATFORMS\n  ruby\nDEPENDENCIES\n')
        with patch('libyears.cli.ssl.create_default_context') as context, \
             patch('libyears.scan.RubyGemsAdapter') as adapter:
            adapter.return_value.tls_trust = 'explicit CA bundle'
            code, human, errors = self.run_cli('--ca-bundle', 'approved.pem', '--verbose')
        self.assertEqual((code, errors), (0, ''))
        adapter.assert_called_once_with(ca_bundle='approved.pem')
        context.assert_any_call(cafile='approved.pem')
        self.assertIn('TLS trust: explicit CA bundle', human)


class ScopedRubyCLITests(unittest.TestCase):
    source = 'source "https://rubygems.org"\n'
    lock = ('GEM\n  remote: https://rubygems.org\n  specs:\n'
            '    rack (1)\n    rake (1)\n    debug (1)\n'
            'PLATFORMS\n  ruby\nDEPENDENCIES\n  rack\n  rake\n  debug\n')

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        for target in ('urllib.request.urlopen', 'urllib.request.OpenerDirector.open',
                       'subprocess.Popen', 'os.system'):
            guard = patch(target, side_effect=AssertionError('live HTTP or execution'))
            guard.start()
            self.addCleanup(guard.stop)

    def invoke(self, *args, scan=None, path=None):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = main([str(path or self.root), *args], scan=scan)
        return code, output.getvalue(), errors.getvalue()

    def lookup(self, name, version):
        used = datetime(2020, 1, 1, tzinfo=timezone.utc)
        return RegistryResult(name, version, used, '2', used + timedelta(days=365.25 * 2))

    def write_inputs(self):
        (self.root / 'Gemfile').write_text(self.source +
            'gem "rack"\ngroup :test, :development, optional: true do\n'
            'gem "rake", group: :extra\nend\ngem "debug", group: :Test\n')
        (self.root / 'Gemfile.lock').write_text(self.lock)

    def test_explicit_exact_groups_union_duplicates_and_expected_age(self):
        self.write_inputs()
        cases = (
            (('test',), ['rake']), (('Test',), ['debug']),
            (('default',), ['rack']), (('test', 'development', 'test'), ['rake']),
            (('default', 'test', 'Test'), ['rack', 'rake', 'debug']),
        )
        for groups, names in cases:
            with self.subTest(groups=groups), patch(
                    'libyears.scan.RubyGemsAdapter.lookup', side_effect=self.lookup) as lookup:
                options = [value for group in groups for value in ('--ruby-group', group)]
                code, output, errors = self.invoke('--json', *options)
                self.assertEqual((code, errors), (0, ''))
                data = json.loads(output)
                self.assertCountEqual([row['name'] for row in data['dependencies']], names)
                self.assertEqual(data['summary']['dependencies_discovered'], len(names))
                self.assertEqual(data['summary']['coverage'], 1.0)
                self.assertEqual(data['summary']['total_libyears'], len(names) * 2.0)
                self.assertEqual(data['version_evidence']['rubygems']['requested_groups'],
                                 sorted(set(groups)))
                self.assertCountEqual([call.args for call in lookup.call_args_list],
                                      [(name, '1') for name in names])

    def test_cli_validates_and_passes_only_canonical_requested_keyword(self):
        from unittest.mock import Mock
        scan = Mock(return_value=empty_report())
        code, _, errors = self.invoke('--ruby-group', 'test', '--ruby-group', 'Test',
                                      '--ruby-group', 'test', scan=scan)
        self.assertEqual((code, errors), (0, ''))
        scan.assert_called_once_with(str(self.root), ruby_groups=('Test', 'test'))
        scan.reset_mock()
        self.invoke(scan=scan)
        scan.assert_called_once_with(str(self.root))

    def test_malformed_missing_empty_and_comma_values_are_usage_errors_before_scan(self):
        from unittest.mock import Mock
        scan = Mock(return_value=empty_report())
        for options in (('--ruby-group',), ('--ruby-group', '--json'),
                        *(('--ruby-group', value) for value in
                          ('', 'test,default', ':test', ' test', 'test ', 'test-name',
                           '1test', 'é', 'test\n'))):
            with self.subTest(options=options):
                code, output, errors = self.invoke(*options, scan=scan)
                self.assertEqual(code, 1)
                self.assertEqual(output, '')
                self.assertTrue(errors)
                scan.assert_not_called()

    def test_scoped_direct_file_and_invalid_paths_are_usage_errors(self):
        from unittest.mock import Mock
        scan = Mock(return_value=empty_report())
        for name in ('Gemfile', 'Gemfile.lock', 'requirements.txt', 'package.json'):
            path = self.root / name
            path.write_text('not consumed')
            code, output, _ = self.invoke('--ruby-group', 'default', scan=scan, path=path)
            self.assertEqual((code, output), (1, ''))
        code, output, _ = self.invoke('--ruby-group', 'default', scan=scan,
                                     path=self.root / 'missing')
        self.assertEqual((code, output), (1, ''))
        scan.assert_not_called()

    def test_evidence_failures_and_empty_scopes_are_completed_reports(self):
        cases = (
            (None, None, 'default', 'gemfile_missing', None),
            (self.source, None, 'default', None, 0),
            (self.source + 'gem "rack"\n', None, 'default', 'lockfile_missing', 1),
            (self.source, self.lock, 'unknown', 'unknown_ruby_group', None),
            (self.source + 'gem "rack"\n', 'BAD\n', 'default',
             'unsupported_lockfile_format', 1),
        )
        for gemfile, lock, group, reason, count in cases:
            with self.subTest(reason=reason):
                for name, text in (('Gemfile', gemfile), ('Gemfile.lock', lock)):
                    path = self.root / name
                    if path.exists():
                        path.unlink()
                    if text is not None:
                        path.write_text(text)
                code, output, errors = self.invoke('--json', '--ruby-group', group)
                self.assertEqual((code, errors), (0, ''))
                data = json.loads(output)
                self.assertEqual(data['summary']['dependencies_discovered'], count)
                if reason:
                    self.assertEqual((data['source_errors'] + data['unmeasurable'])[0]['reason'], reason)

    def test_request_errors_and_unrelated_systemic_errors_keep_distinct_exits(self):
        from unittest.mock import Mock
        for exception, expected in ((RubyGroupRequestError('invalid request'), 1),
                                    (ValueError('domain failure'), 2),
                                    (RuntimeError('systemic failure'), 2)):
            code, output, errors = self.invoke('--ruby-group', 'default',
                                               scan=Mock(side_effect=exception))
            self.assertEqual((code, output), (expected, ''))
            self.assertIn(str(exception), errors)

    def test_resolved_remains_python_only_and_verbose_json_is_identical(self):
        self.write_inputs()
        (self.root / 'requirements.txt').write_text('rack>=1\n')
        snapshot = self.root / 'resolved.txt'
        snapshot.write_text('rack==3\nrake==99\n')
        before = {path.name: path.read_bytes() for path in self.root.iterdir()}
        with patch('libyears.scan.RubyGemsAdapter.lookup', side_effect=self.lookup) as ruby, \
                patch('libyears.scan.PyPIAdapter.lookup', side_effect=self.lookup) as python:
            options = ('--json', '--ruby-group', 'test', '--resolved', str(snapshot))
            plain = self.invoke(*options)
            verbose = self.invoke(*options, '--verbose')
        self.assertEqual(plain, verbose)
        self.assertEqual(plain[0], 0)
        data = json.loads(plain[1])
        self.assertEqual({(row['ecosystem'], row['name']): row['used_version']
                          for row in data['dependencies']},
                         {('pypi', 'rack'): '3', ('rubygems', 'rake'): '1'})
        self.assertEqual([call.args for call in ruby.call_args_list], [('rake', '1')] * 2)
        self.assertEqual([call.args for call in python.call_args_list], [('rack', '3')] * 2)
        self.assertEqual(before, {path.name: path.read_bytes() for path in self.root.iterdir()})


if __name__ == "__main__":
    unittest.main()
