"""Prospective snapshot namespace admission; synthetic evidence, never history."""

import base64
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from libyears.nuget_input import LocalInput, NuGetInputFailure
from libyears.nuget_project import parse_project
from libyears.nuget_provenance import (
    LocalAuthority, LocalAuthorityFailure, PUBLIC_ORIGIN, authorize_measurement,
    authorize_package, parse_provenance,
)
from libyears.nuget_version import parse_selected_identity

FIXTURES = Path(__file__).parent / 'fixtures/nuget'


def snapshot_witness(value):
    """Change assertion contract explicitly; this is only a synthetic fixture."""
    value = deepcopy(value)
    value['version'] = 2
    del value['producer']
    del value['baseline']['sdk_version']
    value['packages'] = [dict(id=p['id'], version=p['version'], namespace=PUBLIC_ORIGIN)
                         for p in value['packages']]
    return value


class CascadeLocalTests(unittest.TestCase):
    def setUp(self):
        def local(name):
            data = (FIXTURES / name).read_bytes()
            return LocalInput(data, data.decode())
        self.project_source = local('Witness.csproj')
        self.lock_source = local('witness-lock-v1.json')
        self.project = parse_project(self.project_source)
        self.v1 = json.loads((FIXTURES / 'witness-v1.json').read_text())
        self.v2 = snapshot_witness(self.v1)
        self.selected = parse_selected_identity('2.0.0')
        self.content = self.v1['packages'][0]['content_hash']

    def parse(self, value, **overrides):
        data = json.dumps(value).encode()
        args = dict(project_name='Witness.csproj', project_source=self.project_source,
                    lock_source=self.lock_source, project=self.project)
        args.update(overrides)
        return parse_provenance(LocalInput(data, data.decode()), **args)

    def gate(self, value, content=None):
        with patch('socket.socket', side_effect=AssertionError('network')), \
                patch('subprocess.Popen', side_effect=AssertionError('execution')):
            return authorize_measurement(self.parse(value), 'EXAMPLE', self.selected, content)

    def reject(self, value, category='malformed', **overrides):
        with self.assertRaises(NuGetInputFailure) as caught:
            self.parse(value, **overrides)
        self.assertEqual(caught.exception.category, category)

    def test_snapshot_namespace_is_sufficient_without_event_or_hash(self):
        authority = self.gate(self.v2)
        self.assertIsInstance(authority, LocalAuthority)
        self.assertEqual(authority.namespace_basis, 'accepted_snapshot_namespace')
        self.assertEqual(authority.local_content_state, 'unavailable')
        self.assertIsNone(authority.content_hash)
        self.assertNotIn(PUBLIC_ORIGIN, repr(authority))
        self.assertEqual(self.parse(self.v2).contract_version, 2)

    def test_v1_keeps_strong_check_and_optional_failure_facts(self):
        for content, state in ((self.content, 'local_agreement'), (None, 'unavailable'),
                ('bad', 'unavailable'), (base64.b64encode(b'x' * 64).decode(), 'mismatch')):
            authority = self.gate(self.v1, content)
            self.assertIsInstance(authority, LocalAuthority)
            self.assertEqual(authority.namespace_basis, 'accepted_producer_origin')
            self.assertEqual(authority.local_content_state, state)
            self.assertEqual(authority.content_hash is not None, state == 'local_agreement')
        strict = authorize_package(self.parse(self.v1), 'example', self.selected, None)
        self.assertEqual(strict.reason, 'content_hash_unavailable')
        value = deepcopy(self.v1)
        del value['packages'][0]['content_hash']
        self.assertEqual(self.gate(value, self.content).local_content_state, 'unavailable')

    def test_namesakes_private_unknown_and_other_versions_never_authorize(self):
        for namespace in ('unknown', 'https://private.invalid/SECRET', PUBLIC_ORIGIN+'/',
                          PUBLIC_ORIGIN.upper(), PUBLIC_ORIGIN+',private'):
            value = deepcopy(self.v2)
            value['packages'][0]['namespace'] = namespace
            self.assertIsInstance(self.gate(value), LocalAuthorityFailure)
        for version in (1, 2):
            value = deepcopy(self.v1 if version == 1 else self.v2)
            value['packages'] = []
            self.assertEqual(self.gate(value).reason, 'unsupported_dependency_source')
            value = deepcopy(self.v1 if version == 1 else self.v2)
            value['packages'][0]['version'] = '3.0'
            self.assertEqual(self.gate(value).reason, 'unsupported_dependency_source')
        value = deepcopy(self.v1)
        value['packages'][0]['origins'] = [PUBLIC_ORIGIN, 'private']
        self.assertEqual(self.gate(value, self.content).reason, 'unsupported_dependency_source')

    def test_snapshot_context_and_population_cannot_fall_back(self):
        for field, wrong in (('project', 'Other.csproj'), ('framework', 'net9.0'),
                             ('project_sha256', '0'*64), ('lock_sha256', '0'*64),
                             ('coherent_snapshot', False)):
            value = deepcopy(self.v2)
            value[field] = wrong
            self.reject(value, 'context_mismatch')
        changed = replace(self.project_source, data=self.project_source.data+b'\n')
        self.reject(self.v2, 'context_mismatch', project_source=changed)
        for key in self.v2['baseline']:
            value = deepcopy(self.v2)
            if key == 'sdk':
                value['baseline'][key] = 'Other.SDK'
                category = 'context_mismatch'
            else:
                value['baseline'][key] = key != 'explicit_population_complete'
                category = 'unsupported'
            self.reject(value, category)

    def test_exact_v2_framing_has_no_implicit_event_or_content_fields(self):
        for key in self.v2:
            value = deepcopy(self.v2)
            del value[key]
            self.reject(value)
        for location, field, extra in (((), 'producer', {'name':'x','version':'1'}),
                (('baseline',), 'sdk_version', '1'), (('packages',0), 'origins', [PUBLIC_ORIGIN]),
                (('packages',0), 'content_hash', self.content)):
            value = deepcopy(self.v2)
            target = value
            for part in location:
                target = target[part]
            target[field] = extra
            self.reject(value)
        for wrong in (None, False, 1, [], {}, ''):
            value = deepcopy(self.v2)
            value['packages'][0]['namespace'] = wrong
            self.reject(value)
        value = deepcopy(self.v2)
        value['packages'].append(dict(value['packages'][0], id='eXamPle', version='02.0'))
        self.reject(value)

    def test_whole_framing_precedes_context_and_bounds_are_preserved(self):
        value = deepcopy(self.v2)
        value['coherent_snapshot'] = False
        value['packages'][0]['namespace'] = []
        self.reject(value)
        value = deepcopy(self.v2)
        value['packages'][0]['namespace'] = 'x'*256
        self.parse(value)
        value['packages'][0]['namespace'] += 'x'
        self.reject(value, 'limit')
        with patch('libyears.nuget_provenance.MAX_PACKAGE_RECORDS', 0):
            self.reject(self.v2, 'limit')


class CascadeMeasurementTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.lookups = []
        self.urls = []
        for name in ('socket.socket', 'subprocess.Popen', 'urllib.request.urlopen'):
            guard = patch(name, side_effect=AssertionError('unexpected network/process'))
            guard.start()
            self.addCleanup(guard.stop)

    def files(self, *, version=2, **changes):
        from tests.test_nuget_scan import nuget_inputs
        files = nuget_inputs(**changes)
        if version == 2:
            files['witness.json'] = json.dumps(snapshot_witness(
                json.loads(files['witness.json']))).encode()
        return files

    def scan(self, files, documents=None):
        from libyears import nuget_registry as registry
        from libyears.nuget_supervisor import (failed_package, authority_message, decode_authority,
                                              result_message, decode_result)
        from libyears.scan import NuGetRequest, scan_mixed_repository
        from tests.nuget_fixtures import fixture_nuget_reads
        from tests.test_nuget_acceptance import metadata
        documents = metadata(('alpha',)) if documents is None else documents
        urls = self.urls
        class Transport:
            def get(self, url):
                urls.append(url)
                value = documents[url]
                from libyears.registry import TransportFailure
                if isinstance(value, TransportFailure):
                    return value
                if isinstance(value, Exception):
                    raise value
                return json.dumps(value).encode()
        def lookup(authorities):
            result = []
            client = registry.NuGetMetadataClient(transport=Transport(), clock=lambda: 100)
            for authority in authorities:
                self.lookups.append(authority)
                authority = decode_authority(authority_message(authority))
                client.begin_package(authority.package_key)
                try:
                    row = registry.lookup_authorized_package(authority, client)
                except registry.NuGetRegistryFailure as failure:
                    row = failed_package(authority, failure.reason)
                result.append((authority, decode_result(result_message(row))))
            return result
        with fixture_nuget_reads(self.root, files):
            return scan_mixed_repository(self.root,
                nuget_request=NuGetRequest('Witness.csproj', 'witness.json'), nuget_lookup=lookup)

    def test_v2_measures_age_without_acquisition_event_or_content_claim(self):
        from libyears.output import report_to_dict, format_human
        report = self.scan(self.files())
        data = report_to_dict(report, '')
        self.assertEqual(data['schema_version'], 3)
        self.assertEqual(data['summary']['coverage'], 1.0)
        row, = data['dependencies']
        self.assertEqual((row['used_version'], row['latest_stable_version'], row['libyears']),
                         ('1.0.0', '2.0.0', 1.0))
        evidence = row['nuget_evidence']
        self.assertEqual(evidence['origin_state'], 'unavailable')
        self.assertEqual(evidence['content_hash_state'], 'unavailable')
        self.assertEqual(evidence['measurement_basis'], 'bound_snapshot_namespace')
        self.assertEqual(evidence['namespace_basis'], 'accepted_snapshot_namespace')
        self.assertEqual(evidence['assurance']['producer_event'], 'unavailable')
        self.assertEqual(evidence['assurance']['local_content'], 'unavailable')
        self.assertEqual(evidence['assurance']['public_content'], 'not_checked')
        self.assertEqual(data['version_evidence']['nuget']['trust_basis'], 'supplied_snapshot_assertion')
        ordinary = format_human(report, '')
        detailed = format_human(report, '', verbose=True)
        self.assertIn('explicitly accepted public namespace', ordinary)
        self.assertNotIn('Origin state:', ordinary)
        self.assertIn('namespace basis: accepted_snapshot_namespace', detailed)
        self.assertIn('acquisition_not_established', detailed)
        for secret in (PUBLIC_ORIGIN, 'project_sha256', 'lock_sha256', 'sdk_version'):
            self.assertNotIn(secret, json.dumps(data))
            self.assertNotIn(secret, detailed)

    def test_v1_strong_and_missing_local_public_hashes_retain_true_assurance(self):
        from libyears.output import report_to_dict
        from tests.test_nuget_acceptance import metadata
        cases = [('strong', 'local_agreement', 'public_agreement'),
                 ('missing_local', 'unavailable', 'not_checked'),
                 ('mismatch_local', 'mismatch', 'not_checked'),
                 ('missing_public', 'local_agreement', 'unavailable'),
                 ('mismatch_public', 'local_agreement', 'mismatch')]
        for kind, local, public in cases:
            with self.subTest(kind=kind):
                changes = {}
                if kind == 'missing_local':
                    changes['lock_change'] = lambda d: d['dependencies']['net10.0']['alpha'].pop('contentHash')
                if kind == 'mismatch_local':
                    changes['lock_change'] = lambda d: d['dependencies']['net10.0']['alpha'].update(
                        contentHash=base64.b64encode(b'x'*64).decode())
                docs = metadata(('alpha',))
                used = next(v for k,v in docs.items() if '/catalog0/' in k and '1.0.0' in k)
                if kind == 'missing_public':
                    del used['packageHash']
                if kind == 'mismatch_public':
                    used['packageHash'] = base64.b64encode(b'x'*64).decode()
                report = self.scan(self.files(version=1, **changes), docs)
                data = report_to_dict(report, '')
                row, = data['dependencies']
                self.assertEqual(row['libyears'], 1.0)
                evidence = row['nuget_evidence']
                self.assertEqual(evidence['assurance']['producer_event'], 'asserted')
                self.assertEqual(evidence['assurance']['local_content'], local)
                self.assertEqual(evidence['assurance']['public_content'], public)
                self.assertEqual(evidence['origin_state'],
                                 'public_content_verified' if kind == 'strong' else 'asserted_public')
                self.assertEqual(data['summary']['coverage'], 1.0)

    def test_unknown_private_missing_and_mismatched_namespace_make_no_public_requests(self):
        for version in (1, 2):
            for change in ('private', 'missing', 'wrong_version'):
                with self.subTest(version=version, change=change):
                    files = self.files(version=version)
                    witness = json.loads(files['witness.json'])
                    if change == 'missing':
                        witness['packages'] = []
                    elif change == 'wrong_version':
                        witness['packages'][0]['version'] = '3.0'
                    elif version == 1:
                        witness['packages'][0]['origins'] = ['https://private.invalid/SECRET']
                    else:
                        witness['packages'][0]['namespace'] = 'https://private.invalid/SECRET'
                    files['witness.json'] = json.dumps(witness).encode()
                    report = self.scan(files)
                    self.assertEqual(report.unmeasurable[0].reason, 'unsupported_dependency_source')
                    if version == 2:
                        self.assertEqual(report.unmeasurable[0].nuget_evidence.origin_state, 'unavailable')
                    self.assertEqual(report.summary.coverage, 0.0)
                    self.assertEqual(self.lookups, [])
                    self.assertEqual(self.urls, [])

    def test_v2_cannot_repair_stale_context_request_or_unsupported_population(self):
        for change, reason, count in (('stale', 'nuget_context_mismatch', 1),
                                     ('framework', 'nuget_context_mismatch', 1),
                                     ('influence', 'unsupported_nuget_project', None),
                                     ('request', 'declaration_lock_requirement_mismatch', 1),
                                     ('project', 'unsupported_nuget_project', None)):
            with self.subTest(change=change):
                files = self.files()
                witness = json.loads(files['witness.json'])
                if change == 'stale':
                    files['Witness.csproj'] += b'\n'
                elif change == 'framework':
                    witness['framework'] = 'net9.0'
                elif change == 'influence':
                    witness['baseline']['unsupported_membership_version_influences'] = True
                elif change == 'request':
                    files = self.files(lock_change=lambda d:
                        d['dependencies']['net10.0']['alpha'].update(requested='[2.0.0, )'))
                    witness = json.loads(files['witness.json'])
                else:
                    files['Witness.csproj'] = b'<Project />'
                files['witness.json'] = json.dumps(witness).encode()
                report = self.scan(files)
                rows = report.source_errors or report.unmeasurable
                self.assertEqual(rows[0].reason, reason)
                if change in ('stale', 'framework', 'influence'):
                    self.assertEqual(report.source_results[-1].evidence.trust_basis,
                                     'supplied_snapshot_assertion')
                self.assertEqual(report.summary.dependencies_discovered, count)
                self.assertEqual(self.lookups, [])
                self.assertEqual(self.urls, [])

    def test_missing_latest_date_is_measurement_blocker_and_retains_assurance(self):
        from libyears.output import report_to_dict
        from tests.test_nuget_acceptance import metadata
        for version in (1, 2):
            docs = metadata(('alpha',))
            latest = next(v for k,v in docs.items() if '/catalog0/' in k and '2.0.0' in k)
            latest['created'] = None
            report = self.scan(self.files(version=version), docs)
            data = report_to_dict(report, '')
            row, = data['unmeasurable']
            self.assertEqual(row['reason'], 'release_date_missing')
            self.assertIn('used_publication', row['nuget_evidence'])
            self.assertNotIn('latest_publication', row['nuget_evidence'])
            self.assertEqual(row['nuget_evidence']['assurance']['public_content'],
                             'public_agreement' if version == 1 else 'not_checked')
            self.assertEqual(data['summary']['coverage'], 0.0)

    def test_throwing_latest_failure_retains_selected_assurance_in_json(self):
        from libyears.output import report_to_dict
        from libyears.registry import TransportFailure
        from tests.test_nuget_acceptance import metadata
        for version, expected in ((1, 'public_agreement'), (2, 'not_checked')):
            docs = metadata(('alpha',))
            url = next(k for k in docs if '/catalog0/' in k and '2.0.0' in k)
            docs[url] = TransportFailure(503, 'SECRET')
            data = report_to_dict(self.scan(self.files(version=version), docs), '')
            row, = data['unmeasurable']
            self.assertEqual(row['reason'], 'registry_error')
            self.assertEqual(row['nuget_evidence']['assurance']['public_content'], expected)
            self.assertIn('used_publication', row['nuget_evidence'])
            self.assertNotIn('latest_publication', row['nuget_evidence'])
            self.assertEqual(data['dependencies'], [])
            self.assertEqual(data['summary']['coverage'], 0.0)
            self.assertNotIn('SECRET', json.dumps(data))

    def test_namespace_only_worker_failure_never_inherits_producer_facts(self):
        from libyears import nuget_registry as registry
        from libyears.output import report_to_dict
        from tests.test_nuget_acceptance import metadata
        docs = metadata(('alpha',))
        docs[registry.REGISTRATION_BASE+'alpha/index.json'] = TimeoutError('SECRET')
        data = report_to_dict(self.scan(self.files(), docs), '')
        evidence = data['unmeasurable'][0]['nuget_evidence']
        self.assertEqual(data['unmeasurable'][0]['reason'], 'registry_error')
        self.assertEqual(evidence['origin_state'], 'unavailable')
        self.assertEqual(evidence['assurance']['producer_event'], 'unavailable')
        self.assertEqual(evidence['assurance']['local_content'], 'unavailable')
        self.assertNotIn('SECRET', json.dumps(data))


def setUpModule():
    # This module tests sibling semantics with certified Maven absence.
    from tests.maven_fixtures import declare_maven_absent
    declare_maven_absent()


if __name__ == '__main__':
    unittest.main()
