"""Production capability refusal, separate from injected semantic fixtures."""

from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from libyears.cli import main
from libyears.model import RegistryResult
from libyears.rubygems import _ScopedRubyReader, scoped_ruby_source_result


class ScopedCapabilityTests(unittest.TestCase):
    def test_unavailable_access_reaches_cli_without_content_reads_or_ruby_lookup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'Gemfile').write_text('source "https://rubygems.org"\ngem "rack"\n')
            (root / 'Gemfile.lock').write_text('must not be consumed')
            (root / 'requirements.txt').write_text('sibling==1\n')
            date = datetime(2020, 1, 1, tzinfo=timezone.utc)
            python_result = RegistryResult('sibling', '1', date, '1', date)
            for siblings in (False, True):
                # Discover real siblings independently of refused Ruby access.
                if not siblings:
                    (root / 'requirements.txt').unlink()
                else:
                    (root / 'requirements.txt').write_text('sibling==1\n')
                with self.subTest(siblings=siblings), \
                        patch.object(os, 'supports_dir_fd', set()), \
                        patch.object(os, 'open', side_effect=AssertionError('unsafe fallback')), \
                        patch.object(os, 'read', side_effect=AssertionError('content read')), \
                        patch('libyears.scan.RubyGemsAdapter.lookup') as ruby, \
                        patch('libyears.scan.PyPIAdapter.lookup', return_value=python_result), \
                        patch('urllib.request.OpenerDirector.open', side_effect=AssertionError('network')):
                    reports = []
                    for flags in (['--json'], ['--verbose']):
                        output, errors = io.StringIO(), io.StringIO()
                        with redirect_stdout(output), redirect_stderr(errors):
                            code = main([str(root), '--ruby-group', 'default', *flags])
                        self.assertEqual((code, errors.getvalue()), (0, ''))
                        reports.append(output.getvalue())
                    ruby.assert_not_called()
                data = json.loads(reports[0])
                self.assertEqual(data['source_errors'], [{
                    'ecosystem': 'rubygems', 'source': 'Gemfile', 'reason': 'invalid_gemfile',
                }, {'ecosystem': 'nuget', 'source': 'repository',
                    'reason': 'nuget_discovery_unavailable', 'source_id': None}])
                self.assertEqual(data['unmeasurable'], [])
                self.assertEqual([row['name'] for row in data['dependencies']],
                                 ['sibling'] if siblings else [])
                self.assertIsNone(data['summary']['dependencies_discovered'])
                self.assertIsNone(data['summary']['coverage'])
                self.assertEqual(data['summary']['dependencies_measured'], 1 if siblings else None)
                ruby_summary = data['summary']['by_ecosystem']['rubygems']
                self.assertTrue(all(value is None for value in ruby_summary.values()))
                self.assertIsNone(data['version_evidence']['rubygems']['format'])
                self.assertIn('Gemfile unavailable: unreadable, nonregular or malformed declaration evidence', reports[1])
                self.assertIn('nuget_discovery_unavailable', reports[1])
                self.assertNotIn('must not be consumed', ''.join(reports))

    def test_lock_capability_refusal_retains_independently_established_scope(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real_read = _ScopedRubyReader.read
            reads = []

            def read(reader, name):
                reads.append(name)
                if name == 'Gemfile':
                    # Inject only recognized declarations; the lock uses the
                    # actual production capability boundary on every host.
                    return 'source "https://rubygems.org"\ngem "rack"\n'
                return real_read(reader, name)

            with patch.object(_ScopedRubyReader, 'read', read), \
                    patch.object(os, 'supports_dir_fd', set()), \
                    patch.object(os, 'open') as opened, patch.object(os, 'read') as consumed:
                source = scoped_ruby_source_result(root, ('default',))
            self.assertEqual(reads, ['Gemfile', 'Gemfile.lock'])
            self.assertEqual(source.dependencies_discovered, 1)
            self.assertFalse(source.measurement_available)
            self.assertEqual((source.candidates, source.unmeasurable), ((), ()))
            self.assertEqual([(error.source, error.reason) for error in source.source_errors],
                             [('Gemfile.lock', 'invalid_lockfile')])
            self.assertIsNone(source.evidence.format)
            opened.assert_not_called()
            consumed.assert_not_called()


def setUpModule():
    # Independent sibling semantics certify absence; Maven safety is separate.
    from tests.maven_fixtures import declare_maven_absent
    declare_maven_absent()
