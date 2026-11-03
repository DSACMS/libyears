"""Offline T010 source/registry/metric integration and S6 availability."""

import base64
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.model import MetricSummary, NuGetPublication, RegistryResult
from libyears.nuget_provenance import LocalAuthority
from libyears.nuget_registry import NuGetRegistryAdapter
from libyears.nuget_supervisor import PackageResult, REASONS
from libyears.scan import NuGetRequest, scan_mixed_repository
from tests.nuget_fixtures import fixture_nuget_reads


FIXTURES = Path(__file__).parent / 'fixtures/nuget'
HASH = base64.b64encode(bytes(range(64))).decode()
USED = datetime(2020, 1, 1, tzinfo=timezone.utc)
LATEST = USED + timedelta(days=365.25)


def nuget_inputs(names=('alpha',), *, selected='1.0.0', project_change=None,
                 lock_change=None, witness_change=None):
    """Bind synthetic exact bytes; mutations precede binding unless explicit."""
    references = ''.join('<PackageReference Include="' + name + '" Version="1.0" />'
                         for name in names)
    project = ('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>'
               '<TargetFramework>net10.0</TargetFramework></PropertyGroup>'
               '<ItemGroup>' + references + '</ItemGroup></Project>').encode()
    if project_change:
        project = project_change(project)
    lock = {'version': 1, 'dependencies': {'net10.0': {
        name: {'type': 'Direct', 'requested': '[1.0.0, )',
               'resolved': selected, 'contentHash': HASH} for name in names}}}
    if lock_change:
        lock_change(lock)
    lock_bytes = json.dumps(lock).encode()
    witness = json.loads((FIXTURES / 'witness-v1.json').read_text())
    witness['project_sha256'] = hashlib.sha256(project).hexdigest()
    witness['lock_sha256'] = hashlib.sha256(lock_bytes).hexdigest()
    template = witness['packages'][0]
    witness['packages'] = [dict(deepcopy(template), id=name, version=selected)
                           for name in names]
    if witness_change:
        witness_change(witness)
    return {'Witness.csproj': project, 'packages.lock.json': lock_bytes,
            'witness.json': json.dumps(witness).encode()}


def nuget_unavailable_cases(names=('alpha',)):
    cases = []
    for missing, reason, count in (
            ('Witness.csproj', 'nuget_project_missing', None),
            ('packages.lock.json', 'lockfile_missing', len(names)),
            ('witness.json', 'nuget_provenance_missing', len(names))):
        files = nuget_inputs(names)
        del files[missing]
        cases.append((reason, files, count))
    for filename, reason, count in (
            ('Witness.csproj', 'invalid_nuget_project', None),
            ('packages.lock.json', 'invalid_lockfile', len(names)),
            ('witness.json', 'invalid_nuget_provenance', len(names))):
        files = nuget_inputs(names)
        files[filename] = b'broken SECRET'
        cases.append((reason, files, count))
    cases.append(('unsupported_nuget_project', nuget_inputs(names,
        project_change=lambda data: data.replace(b'net10.0', b'net10.0;net9.0')), None))
    cases.append(('unsupported_nuget_project', nuget_inputs(names,
        witness_change=lambda value: value['baseline'].update(
            unsupported_membership_version_influences=True)), None))
    cases.append(('unsupported_lockfile_format', nuget_inputs(names,
        lock_change=lambda value: value.update(version=2)), len(names)))
    cases.append(('nuget_context_mismatch', nuget_inputs(names,
        witness_change=lambda value: value.update(project_sha256='0' * 64)), len(names)))
    if names:
        cases.append(('duplicate_nuget_declaration', nuget_inputs(names,
            project_change=lambda data: data.replace(b'</ItemGroup>',
                b'<PackageReference Include="ALPHA" Version="1.0" /></ItemGroup>')), None))
    return cases


class NuGetScanTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        # The injected registry boundary is the only permitted metadata seam.
        for target in ('subprocess.Popen', 'subprocess.run', 'os.system',
                       'socket.socket', 'urllib.request.urlopen'):
            guard = patch(target, side_effect=AssertionError(target))
            guard.start()
            self.addCleanup(guard.stop)

    def successful_package(self, authority):
        self.assertIsInstance(authority, LocalAuthority)
        return PackageResult(
            origin_state='public_content_verified', content_hash_state='public_agreement',
            used_publication=NuGetPublication(authority.normalized_version, USED, True),
            latest_publication=NuGetPublication('2.0.0', LATEST, True))

    def lookup_all(self, authorities):
        return tuple((authority, self.successful_package(authority)) for authority in authorities)

    def sibling_lookup(self, name, version):
        return RegistryResult(name, version, USED, '2.0.0', LATEST)

    def scan(self, files, *, lookup=None, request=None, **kwargs):
        before = {path.name: path.read_bytes() for path in self.root.iterdir() if path.is_file()}
        with fixture_nuget_reads(self.root, files):
            report = scan_mixed_repository(
                self.root, nuget_request=request or NuGetRequest('Witness.csproj', 'witness.json'),
                nuget_lookup=lookup or self.lookup_all,
                pypi_lookup=self.sibling_lookup, npm_lookup=self.sibling_lookup,
                rubygems_lookup=self.sibling_lookup, **kwargs)
        after = {path.name: path.read_bytes() for path in self.root.iterdir() if path.is_file()}
        self.assertEqual(before, after)
        return report

    def test_source_unavailability_matrix_known_and_unknown_including_zero(self):
        for names in ((), ('alpha',)):
            for reason, files, count in nuget_unavailable_cases(names):
                with self.subTest(names=names, reason=reason):
                    lookup = Mock(side_effect=AssertionError('local rejection reached lookup'))
                    report = self.scan(files, lookup=lookup)
                    self.assertEqual(report.by_ecosystem['nuget'],
                                     MetricSummary(count, None, None, None, None, None, None))
                    self.assertEqual(report.summary,
                                     MetricSummary(count, None, None, 0.0, None, None, None))
                    self.assertEqual([error.reason for error in report.source_errors], [reason])
                    self.assertEqual(report.measurements, ())
                    self.assertEqual(report.unmeasurable, ())
                    lookup.assert_not_called()

    def test_missing_witness_option_is_unavailable_even_with_found_file(self):
        lookup = Mock()
        report = self.scan(nuget_inputs(), lookup=lookup,
                           request=NuGetRequest('Witness.csproj'))
        lookup.assert_not_called()
        self.assertEqual(report.by_ecosystem['nuget'],
                         MetricSummary(1, None, None, None, None, None, None))
        self.assertEqual(report.source_errors[0].reason, 'nuget_provenance_missing')

    def test_empty_all_failed_partial_and_full_accepted_population(self):
        for count, failures in ((0, 0), (2, 2), (2, 1), (2, 0)):
            with self.subTest(count=count, failures=failures):
                names = ('alpha', 'beta')[:count]
                def lookup(authorities):
                    return tuple((authority, PackageResult(reason='registry_error')
                                  if index < failures else self.successful_package(authority))
                                 for index, authority in enumerate(authorities))
                report = self.scan(nuget_inputs(names), lookup=lookup)
                measured = count - failures
                expected = MetricSummary(count, measured, measured / count if count else None,
                                         float(measured), 1.0 if measured else None,
                                         1.0 if measured else None, 1.0 if measured else None)
                self.assertEqual(report.by_ecosystem['nuget'], expected)
                self.assertEqual(report.summary, expected)
                self.assertEqual(len(report.unmeasurable), failures)
                self.assertEqual(report.source_errors, ())

    def test_metric_arithmetic_identity_zero_anomaly_and_measured_only_totals(self):
        for selected, latest_version, latest_time, value, anomaly in (
                ('1.0.0', '2.0.0', LATEST, 1.0, False),
                ('01.0+build', '1.0.0', USED, 0.0, False),
                ('1.0.0', '2.0.0', USED - timedelta(days=1), 0.0, True)):
            with self.subTest(selected=selected, latest=latest_time):
                def lookup(authorities):
                    authority, = authorities
                    result = replace(self.successful_package(authority),
                        latest_publication=NuGetPublication(latest_version, latest_time, True))
                    return ((authority, result),)
                report = self.scan(nuget_inputs(selected=selected), lookup=lookup)
                row, = report.measurements
                self.assertEqual((row.libyears, row.timestamp_anomaly), (value, anomaly))
                self.assertEqual(row.dependency.used_version, '1.0.0')
                self.assertEqual(row.dependency.nuget_evidence.selected_version, selected)
                self.assertEqual(row.dependency.version_source, 'packages_lock')
                self.assertEqual(report.summary.total_libyears, value)

    def test_staged_safe_evidence_survives_every_registry_failure(self):
        for reason in sorted(REASONS):
            for verified in (False, True):
                with self.subTest(reason=reason, verified=verified):
                    def lookup(authorities):
                        authority, = authorities
                        result = (replace(self.successful_package(authority), reason=reason,
                                          latest_publication=None) if verified
                                  else PackageResult(reason=reason))
                        return ((authority, result),)
                    report = self.scan(nuget_inputs(), lookup=lookup)
                    row, = report.unmeasurable
                    evidence = row.nuget_evidence
                    self.assertEqual((row.ecosystem, row.name, row.declared, row.reason),
                                     ('nuget', 'alpha', 'alpha (1.0)', reason))
                    self.assertEqual((evidence.requested, evidence.lock_requested,
                                      evidence.selected_version, evidence.normalized_version),
                                     ('1.0', '[1.0.0, )', '1.0.0', '1.0.0'))
                    self.assertEqual(evidence.origin_state,
                                     'public_content_verified' if verified else 'asserted_public')
                    self.assertEqual(evidence.used_publication is not None, verified)
                    self.assertIsNone(evidence.latest_publication)

    def test_local_failure_retains_evidence_and_does_not_reach_adapter(self):
        lookup = Mock()
        files = nuget_inputs(lock_change=lambda value: value['dependencies']['net10.0']['alpha']
                             .update(requested='[2.0.0, )'))
        report = self.scan(files, lookup=lookup)
        lookup.assert_not_called()
        evidence = report.unmeasurable[0].nuget_evidence
        self.assertEqual(evidence.lock_requested, '[2.0.0, )')
        self.assertIsNone(evidence.selected_version)
        self.assertIsNone(evidence.normalized_version)
        self.assertIsNone(evidence.selection_source)

    def test_default_adapter_receives_local_authorities_in_one_supervised_batch(self):
        supervisor = Mock()
        supervisor.lookup.side_effect = self.successful_package
        adapter = NuGetRegistryAdapter(supervisor)
        with fixture_nuget_reads(self.root, nuget_inputs(('zebra', 'Alpha'))):
            report = scan_mixed_repository(self.root,
                nuget_request=NuGetRequest('Witness.csproj', 'witness.json'), nuget_adapter=adapter)
        self.assertEqual([call.args[0].package_key for call in supervisor.lookup.call_args_list],
                         ['alpha', 'zebra'])
        self.assertEqual([row.dependency.name for row in report.measurements], ['Alpha', 'zebra'])
        supervisor.close.assert_called_once_with()
        self.assertTrue(all(row.dependency.nuget_evidence.used_publication is not None
                            for row in report.measurements))

    def test_ordinary_scan_never_reads_or_constructs_nuget_adapter(self):
        for name in ('Witness.csproj', 'packages.lock.json', 'witness.json', 'project.assets.json'):
            (self.root / name).write_text('not inspected')
        with patch('libyears.scan.read_nuget_source') as source, \
                patch('libyears.scan.NuGetRegistryAdapter') as adapter:
            report = scan_mixed_repository(self.root)
        source.assert_not_called()
        adapter.assert_not_called()
        self.assertNotIn('nuget', report.by_ecosystem)
        self.assertEqual([source.ecosystem for source in report.source_results],
                         ['pypi', 'npm', 'rubygems'])

    def test_production_reader_refusal_remains_unknown_without_open_or_lookup(self):
        lookup = Mock(side_effect=AssertionError('capability refusal reached metadata'))
        with patch('libyears.nuget_input.os.O_NOFOLLOW', 0, create=True), \
                patch('os.open', side_effect=AssertionError('unsafe filesystem read')):
            report = scan_mixed_repository(self.root,
                nuget_request=NuGetRequest('Witness.csproj', 'witness.json'), nuget_lookup=lookup)
        lookup.assert_not_called()
        self.assertEqual(report.by_ecosystem['nuget'],
                         MetricSummary(None, None, None, None, None, None, None))
        self.assertEqual(report.source_errors[0].reason, 'invalid_nuget_project')
        self.assertEqual(report.unmeasurable, ())

    def test_internal_direct_file_request_rejects_before_any_source_read(self):
        target = self.root / 'requirements.txt'
        target.write_text('alpha==1.0\n')
        with patch('libyears.scan._python_source_result') as python_source, \
                patch('libyears.scan.read_nuget_source') as nuget_source:
            with self.assertRaisesRegex(ValueError, 'NuGet selection requires a directory'):
                scan_mixed_repository(target, nuget_request=NuGetRequest('Witness.csproj'))
        python_source.assert_not_called()
        nuget_source.assert_not_called()


if __name__ == '__main__':
    unittest.main()
