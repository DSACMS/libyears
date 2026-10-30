"""Composed offline witnesses; the fixture README indexes all 28 criteria."""

from contextlib import ExitStack, redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
import io
import json
import os
from pathlib import Path
import ssl
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.cli import main
from libyears.model import RegistryFailure, RegistryResult
from tests.test_registry import BoundedResponse
from tests.test_rubygems_registry import FakeClock, artifact


SOURCE = 'source "https://rubygems.org"\n'
PRIVATE = 'source "https://PRIVATE_AUTHORITY_MARKER.invalid"\n'
USED = datetime(2020, 1, 1, tzinfo=timezone.utc)


def lock(direct='rack', specs=('rack (1)',), remote='https://rubygems.org'):
    return ('GEM\n  remote: ' + remote + '\n  specs:\n'
            + ''.join('    ' + row + '\n' for row in specs)
            + 'PLATFORMS\n  ruby\nDEPENDENCIES\n'
            + ''.join('  ' + row + '\n' for row in direct.splitlines()))


class RubyGroupAcceptanceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        for target in ('urllib.request.urlopen', 'urllib.request.OpenerDirector.open',
                       'subprocess.Popen', 'os.system', 'os.execve',
                       'tarfile.open', 'zipfile.ZipFile'):
            guard = patch(target, side_effect=AssertionError('forbidden IO/execution'))
            guard.start()
            self.addCleanup(guard.stop)

    def write(self, name, text):
        path = self.root / name
        if text is None:
            path.unlink(missing_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')

    def invoke(self, *options):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = main([str(self.root), *options])
        self.assertEqual((code, errors.getvalue()), (0, ''))
        return output.getvalue()

    def siblings(self):
        self.write('requirements.txt', 'rack==1\n')
        self.write('package.json', json.dumps({'dependencies': {'rack': '1.0.0'}}))
        self.write('package-lock.json', json.dumps({
            'lockfileVersion': 3,
            'packages': {'': {}, 'node_modules/rack': {'version': '1.0.0'}},
        }))

    def test_cli_precedence_stages_safe_output_and_successful_siblings(self):
        # Each later defect is deliberately present behind the winning stage.
        cases = (
            ('recognition', 'eval "UNSUPPORTED_PROGRAM_MARKER"\n', 'BAD\n',
             ('default', 'unknown'), 'unsupported_gemfile_syntax', None, False),
            ('unknown', PRIVATE + 'gem "rack"\n', 'BAD\n',
             ('default', 'unknown'), 'unknown_ruby_group', None, False),
            ('absent lock', PRIVATE + 'gem "rack", "= 1"\n', None,
             ('default',), 'lockfile_missing', 1, False),
            ('rejected lock', PRIVATE + 'gem "rack"\n', 'BAD\n',
             ('default',), 'unsupported_lockfile_format', 1, False),
            ('F1', PRIVATE + 'gem "rack", ">= 1"\n', lock('other'),
             ('default',), 'unsupported_dependency_source', 1, True),
            ('missing direct', SOURCE + 'gem "rack", "= 1"\n', lock('other'),
             ('default',), 'lock_dependency_missing', 1, True),
            ('F2', SOURCE + 'gem "rack", ">= 1"\n',
             lock('rack (https://UNSAFE_REQUIREMENT_MARKER.invalid)', ()),
             ('default',), 'unsupported_requirement', 1, True),
            ('local authority', SOURCE + 'gem "rack", ">= 1"\n',
             lock('rack', ('rack (unknown)',), remote='https://LOCK_AUTHORITY_MARKER.invalid'),
             ('default',), 'unsupported_dependency_source', 1, True),
            ('mismatch', SOURCE + 'gem "rack", ">= 1"\n', lock('rack', ()),
             ('default',), 'declaration_lock_requirement_mismatch', 1, True),
            ('selection', SOURCE + 'gem "rack"\n', lock('rack', ()),
             ('default',), 'lock_version_missing', 1, True),
            ('registry', SOURCE + 'gem "rack"\n', lock(),
             ('default',), 'release_date_missing', 1, True),
        )
        for label, gemfile, snapshot, groups, reason, count, accepted in cases:
            for siblings in (False, True):
                with self.subTest(stage=label, siblings=siblings), ExitStack() as stack:
                    self.write('Gemfile', gemfile)
                    self.write('Gemfile.lock', snapshot)
                    for name in ('requirements.txt', 'package.json', 'package-lock.json'):
                        self.write(name, None)
                    if siblings:
                        self.siblings()
                    ruby = stack.enter_context(patch('libyears.scan.RubyGemsAdapter.lookup',
                        return_value=RegistryFailure('rack', '1', 'release_date_missing')))
                    for adapter in ('PyPIAdapter', 'NpmAdapter'):
                        stack.enter_context(patch('libyears.scan.' + adapter + '.lookup',
                            side_effect=lambda name, version: RegistryResult(
                                name, version, USED, '2', USED + timedelta(days=365.25))))
                    options = [value for group in groups for value in ('--ruby-group', group)]
                    rendered = self.invoke(*options, '--json')
                    self.assertEqual(rendered, self.invoke(*options, '--json', '--verbose'))
                    data = json.loads(rendered)
                    human = self.invoke(*options)
                    verbose = self.invoke(*options, '--verbose')
                    self.assertEqual(data['schema_version'], 3)
                    self.assertEqual([row['reason'] for row in
                                     data['source_errors'] + data['unmeasurable']], [reason])
                    self.assertEqual(data['summary']['by_ecosystem']['rubygems']['dependencies_discovered'], count)
                    self.assertEqual(data['version_evidence']['rubygems']['format'],
                                     'gemfile_lock' if accepted else None)
                    self.assertEqual(data['summary']['dependencies_discovered'],
                                     None if count is None else count + (2 if siblings else 0))
                    self.assertEqual([(row['ecosystem'], row['name']) for row in data['dependencies']],
                                     [('pypi', 'rack'), ('npm', 'rack')] if siblings else [])
                    self.assertEqual(data['summary']['total_libyears'], 2.0 if siblings else 0.0)
                    for text in (rendered, human, verbose):
                        for marker in ('PRIVATE_AUTHORITY_MARKER', 'UNSAFE_REQUIREMENT_MARKER',
                                       'LOCK_AUTHORITY_MARKER', 'UNSUPPORTED_PROGRAM_MARKER'):
                            self.assertNotIn(marker, text)
                    if label == 'registry':
                        self.assertEqual([call.args for call in ruby.call_args_list], [('rack', '1')] * 4)
                    else:
                        ruby.assert_not_called()
                    if label in ('F1', 'F2', 'mismatch'):
                        row = data['unmeasurable'][0]
                        self.assertEqual(row['declared'], 'rack (>= 1)')
                        self.assertEqual(row['gemfile_evidence']['declaration_requirements'], ['>= 1'])
                        self.assertNotIn('rubygems_evidence', row)
                        if label in ('F1', 'F2'):
                            self.assertNotIn('lock_requirement', row['gemfile_evidence'])
                        else:
                            self.assertIsNone(row['gemfile_evidence']['lock_requirement'])
                            self.assertIn('textual requirement evidence differs; equivalence not inferred', human)

    def test_real_adapter_population_reaches_scoped_cli_with_platform_dates(self):
        self.write('Gemfile', SOURCE + 'gem "rack", groups: [:test, :extra]\n')
        self.write('Gemfile.lock', lock(specs=('rack (1)', 'rack (1-java)')))
        population = [
            artifact(number='1', created_at='2021-01-01T00:00:00Z'),
            artifact(number='1', platform='java', created_at='2020-01-01T00:00:00Z'),
            artifact(number='1', platform='invalid-date', created_at='not-a-date'),
            artifact(number='2', created_at='2022-01-01T00:00:00Z'),
            artifact(number='2', platform='java', created_at='2023-01-01T00:00:00Z'),
            artifact(number='3.pre', prerelease=True, created_at='2024-01-01T00:00:00Z'),
        ]
        opener = Mock()
        opener.open.side_effect = [BoundedResponse(b'{"name":"Rack"}'),
                                  BoundedResponse(json.dumps(population).encode())]
        clock = FakeClock()
        from libyears.rubygems_registry import RubyGemsAdapter
        with patch('libyears.registry.request.build_opener', return_value=opener):
            adapter = RubyGemsAdapter(monotonic=clock.monotonic, sleep=clock.sleep,
                                      wall_clock=clock.wall_clock)
        with patch('libyears.scan.RubyGemsAdapter', return_value=adapter):
            data = json.loads(self.invoke('--ruby-group', 'test', '--json'))
        row = data['dependencies'][0]
        self.assertEqual((row['used_version'], row['latest_stable_version']), ('1', '2'))
        self.assertEqual(row['libyears'], 731 / 365.25)
        self.assertEqual(row['used_release_time'], '2020-01-01T00:00:00Z')
        self.assertEqual(row['latest_stable_release_time'], '2022-01-01T00:00:00Z')
        self.assertEqual(row['gemfile_evidence']['declared_groups'], ['extra', 'test'])
        evidence = row['rubygems_evidence']
        self.assertEqual([a['platform'] for a in evidence['selected_artifacts']], ['java', 'ruby'])
        self.assertEqual({a['platform'] for a in evidence['used_publication_artifacts']}, {'ruby', 'java'})
        self.assertEqual({a['platform'] for a in evidence['latest_publication_artifacts']}, {'ruby', 'java'})
        self.assertEqual([call.args[0].full_url for call in opener.open.call_args_list], [
            'https://rubygems.org/api/v1/gems/rack.json',
            'https://rubygems.org/api/v1/versions/Rack.json'])
        self.assertTrue(all(call.kwargs == {'timeout': 10.0} for call in opener.open.call_args_list))
        self.assertEqual(adapter.transport.allowed_authority, 'rubygems.org')
        self.assertEqual(adapter.transport.max_response_bytes, 16 * 1024 * 1024)
        self.assertEqual(adapter.ssl_context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(adapter.ssl_context.check_hostname)
        self.assertEqual(len(clock.sleeps), 1)

    def test_root_read_allowlist_integrity_and_no_implicit_production_or_default(self):
        self.write('Gemfile', SOURCE + 'gem "rack"\n'
                   'group :test, optional: false do\ngem "rake"\nend\n'
                   'gem "debug", group: :production\n')
        self.write('Gemfile.lock', lock('rack\nrake\ndebug',
                                       ('rack (1)', 'rake (1)', 'debug (1)')))
        for name in ('.bundle/config', '.gem/credentials', '.env', 'project.gemspec',
                     'nested/Gemfile', 'nested/Gemfile.lock', 'gems.rb', 'payload.gem',
                     'included.Gemfile', 'project.rb'):
            self.write(name, 'DECOY_MUST_NOT_BE_READ')
        before = {str(path.relative_to(self.root)): path.read_bytes()
                  for path in self.root.rglob('*') if path.is_file()}
        real_open = os.open
        opened = []

        def allowed_open(path, flags, *args, **kwargs):
            # Scoped safe reads use a root descriptor and exactly named children.
            target = Path(path)
            self.assertIn(target, (self.root, Path('Gemfile'), Path('Gemfile.lock')))
            opened.append(target)
            return real_open(path, flags, *args, **kwargs)

        with patch('libyears.rubygems.os.open', side_effect=allowed_open), \
                patch('builtins.open', side_effect=AssertionError('unexpected Python open')), \
                patch('io.open', side_effect=AssertionError('unexpected Path/config read')), \
                patch('libyears.scan.RubyGemsAdapter.lookup', side_effect=lambda name, version:
                    RegistryResult(name, version, USED, version, USED)) as lookup:
            for group, expected in (('test', 'rake'), ('production', 'debug'), ('default', 'rack')):
                data = json.loads(self.invoke('--ruby-group', group, '--json'))
                self.assertEqual([row['name'] for row in data['dependencies']], [expected])
                self.assertEqual(data['summary']['dependencies_discovered'], 1)
                self.assertEqual(data['dependencies'][0]['libyears'], 0.0)
            self.assertEqual([call.args for call in lookup.call_args_list],
                             [('rake', '1'), ('debug', '1'), ('rack', '1')])
        self.assertEqual(opened.count(Path('Gemfile')), 3)
        self.assertEqual(opened.count(Path('Gemfile.lock')), 3)
        after = {str(path.relative_to(self.root)): path.read_bytes()
                 for path in self.root.rglob('*') if path.is_file()}
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
