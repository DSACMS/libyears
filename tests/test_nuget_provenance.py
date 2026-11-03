"""Synthetic AC-13–17 supplier framing, binding and no-lookup gate witnesses."""

import base64
from copy import deepcopy
from dataclasses import FrozenInstanceError, asdict
import json
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from libyears.model import NuGetEvidence
from libyears.nuget_input import (
    LocalInput, NuGetInputFailure, ScopedNuGetReader, MAX_PACKAGE_RECORDS,
)
from libyears.nuget_project import parse_project
from libyears.nuget_provenance import (
    LocalAuthority, LocalAuthorityFailure, PUBLIC_ORIGIN, authorize_package,
    decode_content_hash, parse_provenance,
)
from libyears.nuget_version import parse_selected_identity


FIXTURES = Path(__file__).parent / 'fixtures/nuget'


def local(data):
    return LocalInput(data, data.decode('utf-8', errors='replace'))


class NuGetProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.project_source = local((FIXTURES / 'Witness.csproj').read_bytes())
        self.lock_source = local((FIXTURES / 'witness-lock-v1.json').read_bytes())
        self.project = parse_project(self.project_source)
        self.witness = json.loads((FIXTURES / 'witness-v1.json').read_text())
        self.hash = self.witness['packages'][0]['content_hash']
        self.selected = parse_selected_identity('2.0.0')

    def parse(self, value=None, **changes):
        value = self.witness if value is None else value
        data = value if isinstance(value, bytes) else json.dumps(value).encode()
        arguments = dict(project_name='Witness.csproj', project_source=self.project_source,
                         lock_source=self.lock_source, project=self.project)
        arguments.update(changes)
        return parse_provenance(local(data), **arguments)

    def rejected(self, value, category='malformed', **changes):
        with self.assertRaises(NuGetInputFailure) as caught:
            self.parse(value, **changes)
        self.assertEqual(caught.exception.category, category)
        self.assertEqual(str(caught.exception), 'NuGet input rejected: ' + category + '.')

    def gate(self, value=None, lock_hash=None):
        context = self.parse(value)
        return authorize_package(context, 'EXAMPLE', self.selected,
                                 self.hash if lock_hash is None else lock_hash)

    def test_exact_fixture_binding_and_immutable_authority(self):
        context = self.parse()
        authority = self.gate()
        self.assertIsInstance(authority, LocalAuthority)
        self.assertEqual(authority.package_key, 'example')
        self.assertEqual(authority.normalized_version, '2.0.0')
        self.assertEqual(authority.content_hash, bytes(range(64)))
        for record in (context, context.packages[0], authority):
            with self.assertRaises(FrozenInstanceError):
                record.package_key = 'changed'
        self.assertNotIn(self.hash, repr(context))
        self.assertNotIn(self.hash, repr(authority))
        self.assertNotIn(authority.project_sha256, repr(authority))

    def test_parser_has_no_discovery_and_reader_rejects_unselected_conventional_name(self):
        # Files found by convention, config and caches cannot enter the parser.
        reader = ScopedNuGetReader(FIXTURES, 'Witness.csproj')
        with patch('builtins.open') as opening, patch('os.open') as os_open:
            self.parse()
            with self.assertRaises(ValueError):
                reader.read('witness-v1.json')
            opening.assert_not_called()
            os_open.assert_not_called()

    def test_context_binds_raw_bytes_not_equivalent_decoded_documents(self):
        for field in ('project_source', 'lock_source'):
            source = getattr(self, field)
            self.rejected(self.witness, 'context_mismatch',
                          **{field: local(source.data + b'\n')})
        for field, replacement in (('project', 'Other.csproj'), ('framework', 'net9.0'),
                                    ('project_sha256', '0' * 64),
                                    ('lock_sha256', '0' * 64), ('coherent_snapshot', False)):
            value = deepcopy(self.witness)
            value[field] = replacement
            self.rejected(value, 'context_mismatch')
        value = deepcopy(self.witness)
        value['baseline']['sdk'] = 'Microsoft.NET.Sdk.Web'
        self.rejected(value, 'context_mismatch')

    def test_incomplete_or_unsupported_influences_invalidate_population(self):
        for key in self.witness['baseline']:
            if key in ('sdk', 'sdk_version'):
                continue
            value = deepcopy(self.witness)
            value['baseline'][key] = key != 'explicit_population_complete'
            self.rejected(value, 'unsupported')

    def test_complete_structure_precedes_context_and_population(self):
        for field, replacement in (('coherent_snapshot', False), ('framework', 'net9.0')):
            value = deepcopy(self.witness)
            value[field] = replacement
            value['packages'].append({'id': 'Later', 'version': '1.0', 'origins': [False]})
            self.rejected(value)
        value = deepcopy(self.witness)
        value['baseline']['explicit_population_complete'] = False
        value['packages'][0]['content_hash'] = False
        self.rejected(value)

    def test_required_fields_and_exact_types(self):
        for key in self.witness:
            value = deepcopy(self.witness)
            del value[key]
            self.rejected(value)
        for version in (True, False, '1', 1.0, None, 2):
            value = deepcopy(self.witness)
            value['version'] = version
            self.rejected(value)
        for key in ('project', 'framework', 'project_sha256', 'lock_sha256'):
            for wrong in (None, True, [], {}, 1, ''):
                value = deepcopy(self.witness)
                value[key] = wrong
                self.rejected(value)
        for container in ('producer', 'baseline', 'packages'):
            for wrong in (None, True, 'secret', 1):
                value = deepcopy(self.witness)
                value[container] = wrong
                self.rejected(value)
        for key in self.witness['baseline']:
            value = deepcopy(self.witness)
            del value['baseline'][key]
            self.rejected(value)
            value = deepcopy(self.witness)
            value['baseline'][key] = 1
            self.rejected(value)
        for key in ('name', 'version'):
            value = deepcopy(self.witness)
            value['producer'][key] = ''
            self.rejected(value)
        for digest in ('A' * 64, '0' * 63, 'z' * 64):
            value = deepcopy(self.witness)
            value['project_sha256'] = digest
            self.rejected(value)

    def test_unknown_and_duplicate_fields_at_every_level(self):
        for location in ((), ('producer',), ('baseline',), ('packages', 0)):
            value = deepcopy(self.witness)
            container = value
            for key in location:
                container = container[key]
            container['secret_unknown'] = True
            self.rejected(value)
        data = json.dumps(self.witness)
        for original, duplicate in (('"version": 1', '"version": 1, "version": 1'),
                                     ('"id": "Example"', '"id": "Example", "id": "Example"'),
                                     ('"name": "synthetic-supplier"',
                                      '"name": "synthetic-supplier", "name": "other"')):
            self.rejected(data.replace(original, duplicate).encode())
        self.rejected(b'\xff')

    def test_duplicate_normalized_id_version_records_and_distinct_versions(self):
        for version in ('02.0', '2.0.0.0', '2.0.0+build'):
            value = deepcopy(self.witness)
            other = deepcopy(value['packages'][0])
            other.update(id='eXamPle', version=version)
            value['packages'].append(other)
            self.rejected(value)
        value = deepcopy(self.witness)
        value['packages'].append({'id': 'Example', 'version': '3.0', 'origins': []})
        self.assertIsInstance(self.gate(value), LocalAuthority)

    def test_unselected_records_require_framing_without_public_authority(self):
        value = deepcopy(self.witness)
        value['packages'].append({'id': 'Private.Helper', 'version': '1.0',
                                  'content_hash': 'not-a-hash',
                                  'origins': ['https://private.invalid/SECRET']})
        self.assertIsInstance(self.gate(value), LocalAuthority)
        for field, wrong in (('id', '../secret'), ('version', '*'),
                             ('content_hash', None), ('origins', 'public')):
            broken = deepcopy(value)
            broken['packages'][-1][field] = wrong
            self.rejected(broken)

    def test_missing_private_alternate_and_conflicting_origins_never_admit_lookup(self):
        alternatives = [[], ['unknown'], ['https://private.invalid/SECRET'],
                        ['https://www.nuget.org/api/v2'], [PUBLIC_ORIGIN + '/'],
                        [PUBLIC_ORIGIN.upper()], [PUBLIC_ORIGIN, PUBLIC_ORIGIN],
                        [PUBLIC_ORIGIN, 'https://private.invalid/SECRET']]
        for origins in alternatives:
            value = deepcopy(self.witness)
            value['packages'][0]['origins'] = origins
            self.assert_rejected_gate(value, 'unsupported_dependency_source', 'unsupported')
        for change in ('missing_record', 'missing_origins', 'wrong_version', 'wrong_id'):
            value = deepcopy(self.witness)
            if change == 'missing_record':
                value['packages'] = []
            elif change == 'missing_origins':
                del value['packages'][0]['origins']
            elif change == 'wrong_version':
                value['packages'][0]['version'] = '3.0'
            else:
                value['packages'][0]['id'] = 'Other'
            self.assert_rejected_gate(value, 'unsupported_dependency_source', 'unsupported')

    def assert_rejected_gate(self, value, reason, origin_state, lock_hash=None):
        adapter = Mock(side_effect=AssertionError('unauthorized lookup'))
        result = self.gate(value, lock_hash)
        if isinstance(result, LocalAuthority):
            adapter(result)
        adapter.assert_not_called()
        self.assertIsInstance(result, LocalAuthorityFailure)
        self.assertEqual(result.reason, reason)
        self.assertEqual(result.origin_state, origin_state)
        self.assertEqual(result.content_hash_state,
                         'mismatch' if reason == 'content_hash_mismatch' else 'unavailable')
        return result

    def test_config_mapping_cache_blanket_and_hash_only_do_not_authorize(self):
        for marker in ('public', 'sources', 'source_mapping', 'cache', 'all_public'):
            value = deepcopy(self.witness)
            value[marker] = True
            self.rejected(value)
        value = deepcopy(self.witness)
        del value['packages'][0]['origins']
        self.assert_rejected_gate(value, 'unsupported_dependency_source', 'unsupported')

    def test_hash_absent_invalid_and_mismatch_exact_reasons_and_precedence(self):
        invalid = ['', 'not-base64', self.hash + '\n', self.hash.replace('+', '-'),
                   base64.b64encode(b'x' * 63).decode(),
                   base64.b64encode(b'x' * 65).decode(), 'é', 'AAAA====']
        # The fixture encoding need not contain '+': supply an explicit URL-safe case.
        invalid[3] = base64.urlsafe_b64encode(b'\xfb' * 64).decode()
        for bad in invalid:
            value = deepcopy(self.witness)
            value['packages'][0]['content_hash'] = bad
            self.assert_rejected_gate(value, 'content_hash_unavailable', 'asserted_public')
            self.assert_rejected_gate(self.witness, 'content_hash_unavailable', 'asserted_public', bad)
        value = deepcopy(self.witness)
        del value['packages'][0]['content_hash']
        self.assert_rejected_gate(value, 'content_hash_unavailable', 'asserted_public')
        result = authorize_package(self.parse(), 'example', self.selected, None)
        self.assertEqual(result.reason, 'content_hash_unavailable')
        other = base64.b64encode(b'x' * 64).decode()
        self.assert_rejected_gate(self.witness, 'content_hash_mismatch', 'asserted_public', other)
        value['packages'][0]['origins'] = []
        self.assert_rejected_gate(value, 'unsupported_dependency_source', 'unsupported', 'bad')
        self.assertIsNone(decode_content_hash(None))
        self.assertEqual(decode_content_hash(self.hash), bytes(range(64)))

    def test_only_safe_states_enter_public_evidence(self):
        value = deepcopy(self.witness)
        value['producer']['name'] = 'SECRET-PRODUCER'
        value['baseline']['sdk_version'] = 'SECRET-SDK'
        context = self.parse(value)
        authority = authorize_package(context, 'example', self.selected, self.hash)
        self.assertIsInstance(authority, LocalAuthority)
        evidence = NuGetEvidence('Witness.csproj', 'net10.0', '1.0.0',
                                 origin_state='asserted_public', content_hash_state='local_agreement')
        public = json.dumps(asdict(evidence))
        for private in (self.hash, PUBLIC_ORIGIN, 'SECRET-PRODUCER', 'SECRET-SDK',
                        context.project_sha256, context.lock_sha256, 'baseline', 'origins'):
            self.assertNotIn(private, public)

    def test_assertion_and_framework_exact_limits(self):
        for location, key, cap in (('producer', 'name', 256), ('producer', 'version', 256),
                                    ('baseline', 'sdk_version', 256)):
            value = deepcopy(self.witness)
            value[location][key] = 'x' * cap
            self.parse(value)
            value[location][key] += 'x'
            self.rejected(value, 'limit')
        for field, cap in (('framework', 128), ('project', 256)):
            value = deepcopy(self.witness)
            value[field] = 'x' * cap
            self.rejected(value, 'context_mismatch')
            value[field] += 'x'
            self.rejected(value, 'limit')
        value = deepcopy(self.witness)
        value['baseline']['sdk'] = 'x' * 256
        self.rejected(value, 'context_mismatch')
        value['baseline']['sdk'] += 'x'
        self.rejected(value, 'limit')

    def test_package_count_and_witness_bytes_caps(self):
        # Reduced caps isolate the owning bound; shared JSON guards have real-cap tests.
        value = deepcopy(self.witness)
        with patch('libyears.nuget_provenance.MAX_PACKAGE_RECORDS', 1):
            self.parse(value)
            value['packages'].append({'id': 'Other', 'version': '1.0'})
            self.rejected(value, 'limit')
        data = json.dumps(self.witness).encode()
        with patch('libyears.nuget_provenance.MAX_PROVENANCE_BYTES', len(data)):
            self.parse(data)
            self.rejected(data + b' ', 'limit')

    def test_real_package_record_count_cap_and_cap_plus_one(self):
        value = deepcopy(self.witness)
        # Minimal records keep the shared 200,000-value budget independent of
        # this count boundary, while still validating every identity completely.
        value['packages'] = [
            {'id': 'Package' + str(index), 'version': '1.0'}
            for index in range(MAX_PACKAGE_RECORDS)
        ]
        self.assertEqual(len(self.parse(value).packages), MAX_PACKAGE_RECORDS)
        value['packages'].append({'id': 'Extra', 'version': '1.0'})
        self.rejected(value, 'limit')


if __name__ == '__main__':
    unittest.main()
