"""Deterministic scoped Ruby scan propagation and availability contracts."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears import scan as scan_module
from libyears.model import (
    MetricSummary, RegistryFailure, RegistryResult, RubyGemsEvidence,
    RubyPublicationArtifact,
)
from libyears.scan import RubyGroupRequestError, scan_mixed_repository
from libyears.snapshot import parse_snapshot_text


SOURCE = 'source "https://rubygems.org"\n'
LOCK = ('GEM\n  remote: https://rubygems.org\n  specs:\n    rack (1)\n'
        'PLATFORMS\n  ruby\nDEPENDENCIES\n  rack\n')
USED = datetime(2020, 1, 1, tzinfo=timezone.utc)
LATEST = USED + timedelta(days=365.25 * 2)


class ScopedScanTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write(self, name, text):
        if text is not None:
            (self.root / name).write_text(text, encoding='utf-8')

    def lookup(self, name, version):
        return RegistryResult(name, version, USED, '2', LATEST)

    def scan(self, **kwargs):
        arguments = dict(pypi_lookup=self.lookup, npm_lookup=self.lookup,
                         rubygems_lookup=self.lookup, ruby_groups=('default',))
        arguments.update(kwargs)
        return scan_mixed_repository(self.root, **arguments)

    def siblings(self):
        self.write('requirements.txt', 'rack==1\n')
        self.write('package.json', json.dumps({'dependencies': {'rack': '1.0.0'}}))
        self.write('package-lock.json', json.dumps({
            'lockfileVersion': 3, 'packages': {'': {}, 'node_modules/rack': {'version': '1.0.0'}},
        }))

    def test_invalid_requests_fail_before_any_source_reads(self):
        invalid = [(), [], '', 'default', 7, ('',), ('a,b',), (' a',),
                   ('a-b',), ('é',), ('1a',), (None,), ('test\n',)]
        for groups in invalid:
            with self.subTest(groups=groups), \
                    patch('libyears.scan._python_source_result') as python, \
                    patch('libyears.scan._npm_source_result') as npm, \
                    patch('libyears.scan.scoped_ruby_source_result') as scoped, \
                    patch('libyears.scan.ruby_source_result') as ordinary:
                with self.assertRaises(RubyGroupRequestError):
                    self.scan(ruby_groups=groups)
                for source in (python, npm, scoped, ordinary):
                    source.assert_not_called()
        self.write('requirements.txt', 'rack==1\n')
        for path in (self.root / 'requirements.txt', self.root / 'missing'):
            with self.subTest(path=path), patch('libyears.scan._python_source_result') as source:
                with self.assertRaises(RubyGroupRequestError):
                    scan_mixed_repository(path, ruby_groups=('default',))
                source.assert_not_called()

    def test_scoped_request_is_canonical_and_chooses_only_scoped_source(self):
        self.write('Gemfile', SOURCE + 'gem "rack", groups: [:test, :Test]\n')
        self.write('Gemfile.lock', LOCK)
        with patch('libyears.scan.scoped_ruby_source_result',
                   wraps=scan_module.scoped_ruby_source_result) as scoped, \
                patch('libyears.scan.ruby_source_result') as ordinary:
            report = self.scan(ruby_groups=['test', 'Test', 'test'])
        scoped.assert_called_once_with(self.root, ('Test', 'test'))
        ordinary.assert_not_called()
        self.assertEqual(report.source_results[2].evidence.requested_groups, ('Test', 'test'))
        self.assertEqual(report.summary.dependencies_discovered, 1)
        self.assertEqual(report.measurements[0].dependency.gemfile_evidence.declared_groups,
                         ('Test', 'test'))

    def test_ordinary_path_never_opens_gemfile_and_retains_source_call(self):
        self.write('Gemfile.lock', LOCK)
        for gemfile in (None, SOURCE + 'gem "rack"\n', 'arbitrary Ruby code\n'):
            with self.subTest(gemfile=gemfile):
                self.write('Gemfile', gemfile)
                with patch('libyears.scan.scoped_ruby_source_result') as scoped, \
                        patch('libyears.scan.ruby_source_result',
                              wraps=scan_module.ruby_source_result) as ordinary, \
                        patch('libyears.rubygems._ScopedRubyReader') as reader:
                    report = self.scan(ruby_groups=None)
                ordinary.assert_called_once_with(self.root)
                scoped.assert_not_called()
                reader.assert_not_called()
                self.assertEqual(report.summary, MetricSummary(1, 1, 1.0, 2.0, 2.0, 2.0, 2.0))
                self.assertIsNone(report.measurements[0].dependency.gemfile_evidence)

    def test_availability_matrix_with_and_without_successful_siblings(self):
        cases = [
            ('missing Gemfile', None, None, None, False, 0, 'gemfile_missing'),
            ('invalid Gemfile', 'end\n', LOCK, None, False, 0, 'invalid_gemfile'),
            ('unsupported Gemfile', 'eval "x"\n', LOCK, None, False, 0,
             'unsupported_gemfile_syntax'),
            ('unknown group', SOURCE + 'gem "rack", group: :test\n', LOCK,
             None, False, 0, 'unknown_ruby_group'),
            ('rejected positive', SOURCE + 'gem "rack"\n', 'BAD\n', 1, False, 0,
             'unsupported_lockfile_format'),
            ('rejected empty', SOURCE, 'BAD\n', 0, False, 0, 'unsupported_lockfile_format'),
            ('missing positive', SOURCE + 'gem "rack"\n', None, 1, True, 1, None),
            ('missing empty', SOURCE, None, 0, True, 0, None),
            ('accepted empty', SOURCE, LOCK, 0, True, 0, None),
            ('local failure', SOURCE + 'gem "other"\n', LOCK, 1, True, 1, None),
        ]
        for label, gemfile, lock, count, available, rows, reason in cases:
            for siblings in (False, True):
                with self.subTest(state=label, siblings=siblings), tempfile.TemporaryDirectory() as directory:
                    self.root = Path(directory)
                    self.write('Gemfile', gemfile)
                    self.write('Gemfile.lock', lock)
                    if siblings:
                        self.siblings()
                    lookup = Mock(side_effect=AssertionError('unauthorized Ruby lookup'))
                    report = self.scan(rubygems_lookup=lookup, ruby_groups=(
                        'missing' if label == 'unknown group' else 'default',))
                    lookup.assert_not_called()
                    self.assertEqual(len(report.unmeasurable), rows)
                    self.assertEqual([error.reason for error in report.source_errors],
                                     [] if reason is None else [reason])
                    ruby = report.by_ecosystem['rubygems']
                    self.assertEqual(ruby, MetricSummary(
                        count, 0 if available else None,
                        0.0 if available and count else None,
                        0.0 if available else None, None, None, None,
                    ))
                    self.assertEqual(report.summary, MetricSummary(
                        None if count is None else count + (2 if siblings else 0),
                        2 if siblings else (0 if available else None),
                        (2 / (count + 2) if siblings else (0.0 if count else None))
                        if available else None,
                        4.0 if siblings else 0.0,
                        2.0 if siblings else None, 2.0 if siblings else None,
                        2.0 if siblings else None,
                    ))
                    self.assertEqual([m.dependency.ecosystem for m in report.measurements],
                                     ['pypi', 'npm'] if siblings else [])

    def test_registry_success_and_failure_preserve_safe_declarations_and_artifacts(self):
        self.write('Gemfile', SOURCE + 'gem "rack", ">= 1", groups: [:default, :test]\n')
        self.write('Gemfile.lock', LOCK.replace('  rack\n', '  rack (>= 1)\n'))
        publication = RubyGemsEvidence((),
            (RubyPublicationArtifact('1', 'ruby', USED),),
            (RubyPublicationArtifact('2', 'x86_64-linux', LATEST),))
        outcomes = [
            RegistryResult('rack', '1', USED, '2', LATEST, publication),
            RegistryFailure('rack', '1', 'release_date_missing', 'safe diagnostic', publication),
        ]
        for outcome in outcomes:
            with self.subTest(outcome=type(outcome).__name__):
                lookup = Mock(return_value=outcome)
                report = self.scan(rubygems_lookup=lookup)
                lookup.assert_called_once_with('rack', '1')
                row = (report.measurements[0].dependency if report.measurements
                       else report.unmeasurable[0])
                self.assertEqual(row.gemfile_evidence.declared_groups, ('default', 'test'))
                self.assertEqual(row.gemfile_evidence.declaration_requirements, ('>= 1',))
                self.assertEqual(row.gemfile_evidence.lock_requirement, '>= 1')
                self.assertTrue(row.gemfile_evidence.include_lock_requirement)
                self.assertEqual(row.rubygems_evidence.selected_artifacts[0].version, '1')
                self.assertEqual(row.rubygems_evidence.used_publication_artifacts,
                                 publication.used_publication_artifacts)
                self.assertEqual(row.rubygems_evidence.latest_publication_artifacts,
                                 publication.latest_publication_artifacts)
                if report.measurements:
                    self.assertEqual(report.measurements[0].libyears, 2.0)
                else:
                    self.assertEqual(row.declared, 'rack (>= 1)')
                    self.assertEqual(report.summary.coverage, 0.0)
                    self.assertEqual(report.summary.total_libyears, 0.0)
                    self.assertEqual(report.diagnostics, (('rack', 'safe diagnostic'),))

    def test_same_version_zero_and_flagged_timestamp_clamping(self):
        self.write('Gemfile', SOURCE + 'gem "rack"\n')
        self.write('Gemfile.lock', LOCK)
        for latest_version, latest_date, anomaly in (
                ('1', USED, False), ('2', USED - timedelta(days=1), True)):
            with self.subTest(latest=latest_version):
                report = self.scan(rubygems_lookup=lambda name, version: RegistryResult(
                    name, version, USED, latest_version, latest_date))
                self.assertEqual(report.measurements[0].libyears, 0.0)
                self.assertEqual(report.measurements[0].timestamp_anomaly, anomaly)

    def test_three_ecosystems_keep_same_name_and_snapshot_python_only(self):
        self.siblings()
        self.write('requirements.txt', 'rack>=1\n')
        self.write('Gemfile', SOURCE + 'gem "rack"\n')
        self.write('Gemfile.lock', LOCK)
        python = Mock(side_effect=self.lookup)
        npm = Mock(side_effect=self.lookup)
        ruby = Mock(side_effect=self.lookup)
        report = self.scan(snapshot=parse_snapshot_text('rack==3\n'),
                           pypi_lookup=python, npm_lookup=npm, rubygems_lookup=ruby)
        python.assert_called_once_with('rack', '3')
        npm.assert_called_once_with('rack', '1.0.0')
        ruby.assert_called_once_with('rack', '1')
        self.assertEqual([(m.dependency.ecosystem, m.dependency.version_source)
                          for m in report.measurements],
                         [('pypi', 'resolved_snapshot'), ('npm', 'package_lock'),
                          ('rubygems', 'gemfile_lock')])
        self.assertEqual(report.summary, MetricSummary(3, 3, 1.0, 6.0, 2.0, 2.0, 2.0))

    def test_scoped_default_adapter_retains_ca_bundle_and_trust(self):
        self.write('Gemfile', SOURCE + 'gem "rack"\n')
        self.write('Gemfile.lock', LOCK)
        with patch('libyears.scan.RubyGemsAdapter') as factory:
            factory.return_value.lookup.side_effect = self.lookup
            factory.return_value.tls_trust = 'custom CA bundle'
            report = self.scan(rubygems_lookup=None, ca_bundle='approved.pem')
        factory.assert_called_once_with(ca_bundle='approved.pem')
        factory.return_value.lookup.assert_called_once_with('rack', '1')
        self.assertEqual(report.tls_trust, 'custom CA bundle')
