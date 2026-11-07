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


if __name__ == '__main__':
    unittest.main()
