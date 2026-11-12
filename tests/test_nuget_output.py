"""Schema-v3 NuGet evidence snapshots; no public CLI activation (T011)."""

import base64
from dataclasses import asdict, replace
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from libyears.model import NuGetPublication, RegistryResult
from libyears.nuget_supervisor import PackageResult
from libyears.output import format_human, format_json, report_to_dict
from libyears.scan import NuGetRequest, scan_mixed_repository
from tests.nuget_fixtures import fixture_nuget_reads
from tests.test_nuget_scan import HASH, nuget_inputs, nuget_unavailable_cases


USED = datetime(2020, 1, 1, tzinfo=timezone.utc)
LATEST = USED + timedelta(days=365.25)
SOURCE = {
    'declaration_source': 'Witness.csproj', 'snapshot_source': 'packages.lock.json',
    'provenance_source': 'witness.json', 'scope': 'explicit_direct_packagereference',
    'format': 'packages_lock_v1', 'framework': 'net10.0',
    'trust_basis': 'supplied_producer_assertion',
    'publication_basis': 'nuget_org_first_receipt_created',
    'population_basis': 'declaration_derived',
}
BASE_ROW = {
    'project': 'Witness.csproj', 'framework': 'net10.0', 'requested': '1.0',
    'origin_state': 'unavailable', 'content_hash_state': 'unavailable',
    'publication_basis': 'nuget_org_first_receipt_created',
    'population_basis': 'declaration_derived',
}
SELECTION = {
    'lock_requested': '[1.0.0, )', 'selected_version': '1.0.0',
    'normalized_version': '1.0.0', 'selection_source': 'packages.lock.json',
}
USED_PUBLICATION = {'version': '1.0.0', 'created': '2020-01-01T00:00:00Z', 'listed': True}
LATEST_PUBLICATION = {'version': '2.0.0', 'created': '2020-12-31T06:00:00Z', 'listed': True}


def admitted_evidence(evidence, local='local_agreement'):
    result = dict(evidence, measurement_basis='bound_snapshot_namespace',
                  namespace_basis='accepted_producer_origin')
    final = evidence['content_hash_state']
    public = (final if final == 'public_agreement' or
              (local == 'local_agreement' and final in ('mismatch', 'unavailable'))
              else 'not_checked')
    limits = ['accepted_snapshot_not_evaluated_runtime', 'acquisition_testimony_not_authenticated',
              'reproducibility_not_established', 'deployment_not_established']
    if public != 'public_agreement':
        limits.append('content_correspondence_not_established')
    result['assurance'] = dict(producer_event='asserted', local_content=local,
                               public_content=public, limitations=limits)
    return result


class NuGetJSONTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for target in ('subprocess.Popen', 'subprocess.run', 'os.system',
                       'socket.socket', 'urllib.request.urlopen'):
            guard = patch(target, side_effect=AssertionError(target))
            guard.start()
            self.addCleanup(guard.stop)

    def success(self, authority):
        strong = authority.local_content_state == 'local_agreement'
        return PackageResult(origin_state='public_content_verified' if strong else 'asserted_public',
            content_hash_state='public_agreement' if strong else authority.local_content_state,
            used_publication=NuGetPublication(authority.normalized_version, USED, True),
            latest_publication=NuGetPublication('2.0.0', LATEST, True))

    def scan(self, files=None, *, package_result=None, request=None):
        if files is None:
            files = nuget_inputs()
        def lookup(authorities):
            return tuple((authority, self.success(authority) if package_result is None
                          else package_result) for authority in authorities)
        with fixture_nuget_reads(self.root, files):
            return scan_mixed_repository(self.root,
                nuget_request=request or NuGetRequest('Witness.csproj', 'witness.json'),
                nuget_lookup=lookup,
                pypi_lookup=lambda name, version: RegistryResult(name, version, USED, '2.0.0', LATEST))

    def data(self, report):
        encoded = format_json(report, '.')
        self.assertEqual(json.loads(encoded), report_to_dict(report, '.'))
        # Diagnostics and TLS explanation are human-only, including verbose mode.
        verbose_report = replace(report, diagnostics=(('secret', 'SECRET-DIAGNOSTIC'),),
                                 tls_trust='SECRET-CA-PATH')
        self.assertEqual(encoded, format_json(verbose_report, '.'))
        for secret in (HASH, 'project_sha256', 'lock_sha256', '"producer"', 'sdk_version',
                       'api.nuget.org', 'SECRET', 'baseline', 'content_hash"'):
            self.assertNotIn(secret, encoded)
        return json.loads(encoded)

    def test_full_schema_v3_snapshot(self):
        data = self.data(self.scan())
        summary = {'dependencies_discovered': 1, 'dependencies_measured': 1,
                   'coverage': 1.0, 'total_libyears': 1.0, 'mean_libyears': 1.0,
                   'median_libyears': 1.0, 'max_libyears': 1.0}
        evidence = dict(BASE_ROW, **SELECTION, origin_state='public_content_verified',
                        content_hash_state='public_agreement', used_publication=USED_PUBLICATION,
                        latest_publication=LATEST_PUBLICATION)
        evidence = admitted_evidence(evidence)
        self.assertEqual(data, {
            'schema_version': 3, 'metric': 'libyears', 'dependency_scope': 'direct',
            'ecosystems': ['nuget'], 'version_evidence': {'nuget': SOURCE},
            'summary': dict(summary, by_ecosystem={'nuget': summary}),
            'dependencies': [{'ecosystem': 'nuget', 'name': 'alpha', 'used_version': '1.0.0',
                'used_release_time': USED_PUBLICATION['created'], 'latest_stable_version': '2.0.0',
                'latest_stable_release_time': LATEST_PUBLICATION['created'], 'libyears': 1.0,
                'timestamp_anomaly': False, 'version_source': 'packages_lock',
                'nuget_evidence': evidence}],
            'unmeasurable': [], 'source_errors': [],
        })

    def test_source_rejection_snapshot_required_nulls_and_no_fabricated_rows(self):
        for names in ((), ('alpha',)):
            for reason, files, count in nuget_unavailable_cases(names):
                with self.subTest(reason=reason, count=count, names=names):
                    report = self.scan(files)
                    data = self.data(report)
                    source = report.source_results[-1]
                    rejected_input = source.source_errors[0].source
                    project_rejected = rejected_input == 'Witness.csproj'
                    expected = dict(SOURCE,
                        population_basis='unknown' if count is None else 'declaration_derived',
                        framework=None if project_rejected else 'net10.0',
                        format=None if project_rejected or rejected_input == 'packages.lock.json'
                            else 'packages_lock_v1')
                    self.assertEqual(data['version_evidence'], {'nuget': expected})
                    self.assertEqual(data['dependencies'], [])
                    self.assertEqual(data['unmeasurable'], [])
                    self.assertEqual(data['source_errors'], [{key: value for key, value in asdict(source.source_errors[0]).items() if key != 'source_id'}])
                    self.assertEqual(data['source_errors'][0]['reason'], reason)
                    self.assertEqual(data['summary']['by_ecosystem'], {'nuget': {
                        'dependencies_discovered': count, 'dependencies_measured': None,
                        'coverage': None, 'total_libyears': None, 'mean_libyears': None,
                        'median_libyears': None, 'max_libyears': None,
                    }})
                    self.assertEqual(data['summary']['total_libyears'], 0.0)

    def test_missing_witness_option_has_explicit_null_provenance_source(self):
        data = self.data(self.scan(request=NuGetRequest('Witness.csproj')))
        self.assertEqual(data['version_evidence'], {'nuget': dict(SOURCE, provenance_source=None)})
        self.assertEqual(data['source_errors'], [{'ecosystem': 'nuget', 'source': 'Witness.csproj',
                                                'reason': 'nuget_provenance_missing'}])

    def test_local_association_stage_snapshots_omit_unestablished_facts(self):
        cases = (
            ('lock_dependency_missing', lambda value: value['dependencies']['net10.0'].clear(),
             BASE_ROW),
            ('declaration_lock_requirement_mismatch',
             lambda value: value['dependencies']['net10.0']['alpha'].update(requested='[2.0.0, )'),
             dict(BASE_ROW, lock_requested='[2.0.0, )')),
            ('declaration_lock_requirement_mismatch',
             lambda value: value['dependencies']['net10.0']['alpha'].update(requested='SECRET-XML'),
             BASE_ROW),
            ('lock_version_missing', lambda value: value['dependencies']['net10.0']['alpha'].pop('resolved'),
             dict(BASE_ROW, lock_requested='[1.0.0, )')),
            ('unsupported_lock_evidence',
             lambda value: value['dependencies']['net10.0']['alpha'].update(resolved='1'),
             dict(BASE_ROW, lock_requested='[1.0.0, )', selected_version='1',
                  selection_source='packages.lock.json')),
            ('unsupported_lock_evidence',
             lambda value: value['dependencies']['net10.0']['alpha'].update(resolved='SECRET-selected'),
             dict(BASE_ROW, lock_requested='[1.0.0, )')),
        )
        for reason, change, evidence in cases:
            with self.subTest(reason=reason, evidence=evidence):
                data = self.data(self.scan(nuget_inputs(lock_change=change)))
                self.assertEqual(data['unmeasurable'], [{'ecosystem': 'nuget', 'name': 'alpha',
                    'declared': 'alpha (1.0)', 'reason': reason, 'nuget_evidence': evidence}])
                self.assertEqual(data['dependencies'], [])
                self.assertEqual(data['source_errors'], [])
                self.assertEqual(data['summary']['coverage'], 0.0)

    def test_origin_failure_and_local_hash_assurance_snapshots(self):
        private = nuget_inputs(witness_change=lambda value:
            value['packages'][0].update(origins=['https://user:SECRET@private.invalid/feed']))
        data = self.data(self.scan(private))
        self.assertEqual(data['unmeasurable'][0]['reason'], 'unsupported_dependency_source')
        self.assertNotIn('measurement_basis', data['unmeasurable'][0]['nuget_evidence'])
        for content, state in (('SECRET', 'unavailable'),
                               (base64.b64encode(b'x'*64).decode(), 'mismatch')):
            files = nuget_inputs(lock_change=lambda value:
                value['dependencies']['net10.0']['alpha'].update(contentHash=content))
            data = self.data(self.scan(files))
            self.assertEqual(data['unmeasurable'], [])
            evidence = data['dependencies'][0]['nuget_evidence']
            self.assertEqual(evidence['content_hash_state'], state)
            self.assertEqual(evidence['assurance']['local_content'], state)
            self.assertEqual(evidence['assurance']['public_content'], 'not_checked')
            self.assertEqual(data['dependencies'][0]['libyears'], 1.0)

    def test_registry_stages_preserve_only_established_publications(self):
        stages = (
            PackageResult(reason='registry_error'),
            PackageResult(reason='content_hash_unavailable', content_hash_state='unavailable'),
            PackageResult(reason='content_hash_mismatch', content_hash_state='mismatch'),
            PackageResult(reason='release_date_missing', origin_state='public_content_verified',
                          content_hash_state='public_agreement'),
            PackageResult(reason='no_stable_release', origin_state='public_content_verified',
                          content_hash_state='public_agreement',
                          used_publication=NuGetPublication('1.0.0', USED, False)),
        )
        for result in stages:
            with self.subTest(result=result):
                data = self.data(self.scan(package_result=result))
                expected = dict(BASE_ROW, **SELECTION, origin_state=result.origin_state,
                                content_hash_state=result.content_hash_state)
                if result.used_publication is not None:
                    expected['used_publication'] = dict(USED_PUBLICATION, listed=False)
                expected = admitted_evidence(expected)
                self.assertEqual(data['unmeasurable'][0]['nuget_evidence'], expected)
                self.assertEqual(data['unmeasurable'][0]['reason'], result.reason)

    def test_original_selected_spelling_and_utc_publication_serialization(self):
        offset = timezone(timedelta(hours=2))
        result = PackageResult(origin_state='public_content_verified', content_hash_state='public_agreement',
            used_publication=NuGetPublication('1.0.0', USED.astimezone(offset), False),
            latest_publication=NuGetPublication('2.0.0', LATEST.astimezone(offset), True))
        data = self.data(self.scan(nuget_inputs(selected='01.0.0.0+build'), package_result=result))
        row = data['dependencies'][0]
        self.assertEqual(row['used_version'], '1.0.0')
        self.assertEqual(row['nuget_evidence']['selected_version'], '01.0.0.0+build')
        self.assertEqual(row['nuget_evidence']['used_publication'], dict(USED_PUBLICATION, listed=False))
        self.assertEqual(row['nuget_evidence']['latest_publication'], LATEST_PUBLICATION)

    def test_partial_empty_and_zero_coverage_numeric_snapshots(self):
        for names, failure in (((), False), (('alpha',), True), (('alpha',), False)):
            with self.subTest(names=names, failure=failure):
                report = self.scan(nuget_inputs(names), package_result=(
                    PackageResult(reason='registry_error') if failure else None))
                data = self.data(report)
                self.assertEqual(data['summary']['by_ecosystem']['nuget'], asdict(report.by_ecosystem['nuget']))
                self.assertEqual(data['summary']['coverage'], 0.0 if failure else 1.0 if names else None)
        files = nuget_inputs(('alpha', 'beta'), lock_change=lambda value:
            value['dependencies']['net10.0']['beta'].pop('resolved'))
        data = self.data(self.scan(files))
        self.assertEqual((data['summary']['dependencies_discovered'],
                          data['summary']['dependencies_measured'], data['summary']['coverage']), (2, 1, 0.5))
        self.assertEqual(data['summary']['total_libyears'], 1.0)
        self.assertEqual([row['name'] for row in data['dependencies']], ['alpha'])
        self.assertEqual([row['name'] for row in data['unmeasurable']], ['beta'])

    def test_ordinary_sibling_json_has_no_nuget_additions(self):
        (self.root / 'requirements.txt').write_text('alpha==1.0\n')
        def lookup(name, version):
            return RegistryResult(name, version, USED, '2.0.0', LATEST)
        before = scan_mixed_repository(self.root, pypi_lookup=lookup)
        for name in ('Witness.csproj', 'packages.lock.json', 'witness.json'):
            (self.root / name).write_text('SECRET-unselected')
        after = scan_mixed_repository(self.root, pypi_lookup=lookup)
        self.assertEqual(format_json(before, '.'), format_json(after, '.'))
        self.assertNotIn('nuget', format_json(after, '.'))
        data = self.data(self.scan())
        sibling = data['dependencies'][0]
        self.assertEqual(sibling['ecosystem'], 'pypi')
        self.assertNotIn('nuget_evidence', sibling)
        self.assertEqual(data['version_evidence']['pypi'],
                         {'declaration_source': 'requirements.txt', 'snapshot_source': None})

    def assert_human_row(self, human, row, *, verbose=True):
        evidence = row['nuget_evidence']
        if not verbose:
            self.assertIn(row['name'], human)
            if 'reason' in row:
                self.assertIn(row['reason'] + ':', human)
            else:
                self.assertIn(f"{row['libyears']:.2f}", human)
            self.assertNotIn('    Origin state:', human)
            return
        for value in (row['name'], evidence['project'], evidence['framework'], evidence['requested'],
                      evidence['origin_state'], evidence['content_hash_state']):
            self.assertIn(value, human)
        for field, label in (('lock_requested', 'Lock requested'),
                             ('selected_version', 'Selected version'),
                             ('normalized_version', 'Normalized selected version')):
            if field in evidence:
                self.assertIn(f"{label}: {evidence[field]}", human)
            else:
                self.assertNotIn(label + ':', human)
        for field, label in (('used_publication', 'Used'), ('latest_publication', 'Latest')):
            if field in evidence:
                publication = evidence[field]
                listed = str(publication['listed']).lower()
                self.assertIn(f"{label} publication: version {publication['version']}; "
                              f"created {publication['created']}; listed {listed}.", human)
            else:
                self.assertNotIn(label + ' publication:', human)
        if 'reason' in row:
            self.assertIn(row['reason'] + ':', human)
        else:
            self.assertIn(f"{row['libyears']:.2f}", human)
            self.assertIn('timestamp_anomaly: ' + str(row['timestamp_anomaly']).lower(), human)

    def test_human_success_corresponds_to_json_and_explains_evidence_limits(self):
        report = self.scan(nuget_inputs(selected='01.0+build'))
        data = self.data(report)
        for verbose in (False, True):
            human = format_human(report, '.', verbose=verbose)
            self.assert_human_row(human, data['dependencies'][0], verbose=verbose)
            if not verbose:
                self.assertIn('explicitly accepted public namespace', human)
                continue
            for text in ('Witness.csproj', 'packages.lock.json', 'witness.json', 'net10.0',
                         'explicit direct PackageReferences', 'test, tool, analyzer and PrivateAssets',
                         'version-1 producer testimony', 'version-2 retained snapshot/namespace testimony',
                         'native NuGet package provenance plus contemporaneous producer attestation',
                         'same event, exact project/lock bytes, framework and required input-influence assertions',
                         'Retrospective replay does not substitute for producer attestation of the original event',
                         'evaluated MSBuild completeness', 'installed/deployed/runtime scope',
                         'restore success', 'compatibility or cryptographic provenance',
                         'first receipt by nuget.org from catalog created', 'not original upstream release',
                         'greatest currently listed stable version', 'no framework, request or compatibility filter',
                         'hashes compare supplied content assertions, not producing history',
                         'changed listing or records may change future measurements',
                         '1 / 1 measured; 100.0% coverage', 'Total:    1.00 libyears'):
                self.assertIn(text, human)

    def test_human_source_failures_correspond_to_json_and_hide_root_and_diagnostics(self):
        for reason, files, count in nuget_unavailable_cases():
            report = self.scan(files)
            data = self.data(report)
            for verbose in (False, True):
                with self.subTest(reason=reason, verbose=verbose):
                    human = format_human(replace(report,
                        diagnostics=(('SECRET-NAME', 'SECRET-EXCEPTION'),),
                        tls_trust='/private/SECRET-CA'), '/private/SECRET-ROOT', verbose=verbose)
                    self.assertNotIn('SECRET', human)
                    self.assertNotIn(HASH, human)
                    self.assertIn('Libyears: selected repository', human)
                    self.assertIn(reason + ':', human)
                    self.assertIn(data['source_errors'][0]['source'], human)
                    self.assertIn('nuget: null coverage;', human)
                    self.assertIn('total null, mean null, median null, max null libyears', human)
                    if count is None:
                        self.assertIn('NuGet population unavailable', human)
                    else:
                        self.assertIn('NuGet measurement unavailable; known explicit population: 1', human)

    def test_human_distinguishes_unavailable_zero_empty_partial_and_full(self):
        cases = (
            (nuget_inputs(()), None, 'validated empty population: 0 / 0 measured; null coverage; total 0.00'),
            (nuget_inputs(), PackageResult(reason='registry_error'),
             'wholly unmeasurable: 0 / 1 measured; 0.0% coverage'),
            (nuget_inputs(), None, 'accepted population: 1 / 1 measured; 100.0% coverage'),
            (nuget_inputs(('alpha', 'beta'), lock_change=lambda value:
                value['dependencies']['net10.0']['beta'].pop('resolved')), None,
             'accepted population: 1 / 2 measured; 50.0% coverage'),
        )
        for files, result, expected in cases:
            with self.subTest(expected=expected):
                report = self.scan(files, package_result=result)
                human = format_human(report, '.')
                self.assertIn(expected, human)
                data = self.data(report)
                for row in data['dependencies'] + data['unmeasurable']:
                    # Multiple rows can establish different optional facts.
                    if len(data['dependencies']) + len(data['unmeasurable']) == 1:
                        self.assert_human_row(human, row, verbose=False)
        files = nuget_inputs(())
        del files['witness.json']
        human = format_human(self.scan(files), '.')
        self.assertIn('measurement unavailable; known explicit population: 0', human)
        self.assertNotIn('validated empty population', human)

    def test_human_staged_failures_preserve_omissions_and_private_canaries(self):
        from libyears.nuget_supervisor import REASONS
        stages = [PackageResult(reason=reason) for reason in sorted(REASONS)]
        stages.append(PackageResult(reason='no_stable_release', origin_state='public_content_verified',
            content_hash_state='public_agreement', used_publication=NuGetPublication('1.0.0', USED, False)))
        reports = [self.scan(package_result=result) for result in stages]
        reports.extend((
            self.scan(nuget_inputs(lock_change=lambda value:
                value['dependencies']['net10.0'].clear())),
            self.scan(nuget_inputs(lock_change=lambda value:
                value['dependencies']['net10.0']['alpha'].pop('resolved'))),
            self.scan(nuget_inputs(lock_change=lambda value:
                value['dependencies']['net10.0']['alpha'].update(resolved='1'))),
            self.scan(nuget_inputs(lock_change=lambda value:
                value['dependencies']['net10.0']['alpha'].update(contentHash='SECRET-HASH'))),
            self.scan(nuget_inputs(lock_change=lambda value:
                value['dependencies']['net10.0']['alpha'].update(
                    contentHash=base64.b64encode(b'x' * 64).decode()))),
            self.scan(nuget_inputs(lock_change=lambda value:
                value['dependencies']['net10.0']['alpha'].update(requested='[2.0.0, )'))),
            self.scan(nuget_inputs(lock_change=lambda value:
                value['dependencies']['net10.0']['alpha'].update(requested='SECRET-REQUEST'))),
            self.scan(nuget_inputs(witness_change=lambda value:
                value['packages'][0].update(origins=['https://user:SECRET@private.invalid/feed']))),
        ))
        for report in reports:
            data = self.data(report)
            row, = data['unmeasurable'] or data['dependencies']
            for verbose in (False, True):
                with self.subTest(reason=row.get('reason', 'measured'), verbose=verbose):
                    human = format_human(replace(report, diagnostics=(('SECRET', 'SECRET-response'),)),
                                         '/private/SECRET-path', verbose=verbose)
                    self.assert_human_row(human, row, verbose=verbose)
                    for private in ('SECRET', 'private.invalid', 'project_sha256', HASH, 'sdk_version'):
                        self.assertNotIn(private, human)

    def test_human_anomaly_and_same_name_sibling_correspondence(self):
        result = PackageResult(origin_state='public_content_verified', content_hash_state='public_agreement',
            used_publication=NuGetPublication('1.0.0', USED, True),
            latest_publication=NuGetPublication('2.0.0', USED - timedelta(days=1), True))
        (self.root / 'requirements.txt').write_text('alpha==1.0\n')
        report = self.scan(package_result=result)
        human = format_human(report, '.', verbose=True)
        data = self.data(report)
        nuget = next(row for row in data['dependencies'] if row['ecosystem'] == 'nuget')
        self.assert_human_row(human, nuget)
        self.assertIn('negative date delta clamped to zero', human)
        self.assertEqual(nuget['libyears'], 0.0)
        self.assertIn('pypi', human)
        self.assertIn('nuget', human)
        self.assertIn('Repository: 100.0% coverage; 2 / 2 measured; total 1.00', human)
        self.assertIn('nuget: 100.0% coverage; 1 / 1 measured; total 0.00', human)
        self.assertIn('pypi: 100.0% coverage; 1 / 1 measured; total 1.00', human)

    def test_ordinary_human_output_stays_identical_and_keeps_verbose_diagnostics(self):
        (self.root / 'requirements.txt').write_text('alpha==1.0\n')
        lookup = lambda name, version: RegistryResult(name, version, USED, '2.0.0', LATEST)
        before = scan_mixed_repository(self.root, pypi_lookup=lookup)
        (self.root / 'Witness.csproj').write_text('unselected')
        after = scan_mixed_repository(self.root, pypi_lookup=lookup)
        for verbose in (False, True):
            self.assertEqual(format_human(before, '/ordinary/path', verbose=verbose),
                             format_human(after, '/ordinary/path', verbose=verbose))
        human = format_human(replace(after, diagnostics=(('alpha', 'safe diagnostic'),),
                                    tls_trust='explicit trust'), '/ordinary/path', verbose=True)
        self.assertIn('Libyears: /ordinary/path', human)
        self.assertIn('safe diagnostic', human)
        self.assertIn('explicit trust', human)
        self.assertNotIn('NuGet', human)

    def test_mixed_yarn_failure_cannot_reintroduce_private_diagnostic_context(self):
        (self.root / 'package.json').write_text('{"dependencies":{"alpha":"^1.0.0"}}')
        (self.root / 'yarn.lock').write_text('unsupported SECRET-YARN')
        report = self.scan()
        self.assertTrue(any(error.source == 'yarn.lock' for error in report.source_errors))
        report = replace(report, diagnostics=(('yarn.lock', 'SECRET-DIAGNOSTIC'),))
        for verbose in (False, True):
            human = format_human(report, '/private/SECRET-ROOT', verbose=verbose)
            self.assertNotIn('SECRET', human)
            self.assertIn('yarn.lock', human)
            self.assertIn('npm dependencies could not be measured from this evidence source', human)
        ordinary = scan_mixed_repository(self.root)
        ordinary = replace(ordinary, diagnostics=(('yarn.lock', 'safe established Yarn context'),))
        for verbose in (False, True):
            human = format_human(ordinary, '.', verbose=verbose)
            self.assertIn('safe established Yarn context', human)


def setUpModule():
    # This module tests sibling semantics with certified Maven absence.
    from tests.maven_fixtures import declare_maven_absent
    declare_maven_absent()


if __name__ == '__main__':
    unittest.main()
