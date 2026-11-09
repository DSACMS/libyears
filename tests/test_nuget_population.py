"""Synthetic explicit snapshot acceptance; never target testimony or history."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from libyears.nuget_input import LocalInput, NuGetInputFailure
from libyears.nuget_lock import parse_lock
from libyears.nuget_population import snapshot_population
from libyears.nuget_provenance import (
    PUBLIC_ORIGIN, LocalAuthority, LocalAuthorityFailure, authorize_measurement,
    parse_population_provenance, parse_provenance,
)
from libyears.nuget_version import parse_selected_identity


def local(data):
    if isinstance(data, dict):
        data = json.dumps(data).encode()
    return LocalInput(data, data.decode())


def snapshot_inputs(*, unsupported=True, packages=None):
    extra = '<Uninterpreted>value</Uninterpreted>' if unsupported else ''
    project = ('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>'
               '<TargetFramework>net10.0</TargetFramework>' + extra +
               '</PropertyGroup><ItemGroup><PackageReference Include="Example" '
               'Version="1.0" /></ItemGroup></Project>').encode()
    lock = local({'version': 1, 'dependencies': {'net10.0': {
        'Example': {'type': 'Direct', 'requested': '[1.0.0, )', 'resolved': '2.0.0'}}}})
    witness = {'version': 3, 'project': 'Witness.csproj', 'framework': 'net10.0',
               'project_sha256': hashlib.sha256(project).hexdigest(),
               'lock_sha256': hashlib.sha256(lock.data).hexdigest(),
               'coherent_snapshot': True, 'explicit_external_direct_complete': True,
               'packages': [] if packages is None else packages}
    return project, lock.data, witness


class SnapshotPrimitiveTests(unittest.TestCase):
    def setUp(self):
        for target in ('socket.socket', 'subprocess.Popen', 'urllib.request.urlopen'):
            guard = patch(target, side_effect=AssertionError(target))
            guard.start()
            self.addCleanup(guard.stop)
        self.project, self.lock, self.witness = snapshot_inputs()

    def population(self, project=None, lock=None):
        return snapshot_population(local(self.project if project is None else project),
                                   parse_lock(local(self.lock if lock is None else lock)))

    def parse_testimony(self, witness=None, project=None, lock=None):
        return parse_population_provenance(local(self.witness if witness is None else witness),
            project_name='Witness.csproj', project_source=local(project or self.project),
            lock_source=local(lock or self.lock), framework='net10.0')

    def test_unknown_declarations_are_not_static_completeness_prerequisite(self):
        project = self.project.replace(b'Version="1.0"', b'Version="$(ChosenVersion)"')
        context = self.population(project)
        self.assertEqual(context.framework, 'net10.0')
        self.assertEqual([(d.package_name, d.declared_version) for d in context.declarations],
                         [('Example', '1.0.0')])
        self.assertEqual(self.parse_testimony().contract_version, 3)

    def test_direct_only_population_and_empty_snapshot(self):
        value = json.loads(self.lock)
        entries = value['dependencies']['net10.0']
        entries['Closure'] = dict(type='Transitive', resolved='1.0.0', contentHash='opaque')
        entries['Sibling'] = dict(type='Project')
        self.assertEqual(len(self.population(lock=value).declarations), 1)
        del entries['Example']
        project = self.project.replace(b'<PackageReference Include="Example" Version="1.0" />', b'')
        self.assertEqual(self.population(project, value).declarations, ())

    def test_every_direct_request_and_selected_version_must_be_supported(self):
        for field, value in [('requested', 'SECRET/path'), ('requested', '[1.0, )'),
                             ('requested', '[1.0.0, 2.0.0)'), ('resolved', None),
                             ('resolved', 'SECRET/path')]:
            lock = json.loads(self.lock)
            entry = lock['dependencies']['net10.0']['Example']
            if value is None:
                del entry[field]
            else:
                entry[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(NuGetInputFailure):
                self.population(lock=lock)
        with patch('libyears.nuget_population.MAX_DIRECT_REFERENCES', 0):
            with self.assertRaises(NuGetInputFailure):
                self.population()

    def test_known_literal_contradictions_refuse_even_with_unknown_syntax(self):
        for before, after in [(b'net10.0', b'net9.0'), (b'net10.0', b'net10.0;net9.0'),
                              (b'Include="Example"', b'Include="Added"'),
                              (b'Version="1.0"', b'Version="3.0"')]:
            with self.subTest(after=after), self.assertRaises(NuGetInputFailure) as caught:
                self.population(self.project.replace(before, after))
            self.assertEqual(caught.exception.category, 'context_mismatch')
        # A literal identity is known even when its version is computed.
        with self.assertRaises(NuGetInputFailure):
            self.population(self.project.replace(b'Include="Example" Version="1.0"',
                                                 b'Include="Added" Version="$(Unknown)"'))

    def test_dtd_malformed_and_mixed_duplicate_input_never_salvages(self):
        duplicate = self.project.replace(b'</ItemGroup>',
            b'<PackageReference Include="EXAMPLE" Version="1.0" /></ItemGroup>')
        for project in [duplicate, b'<!DOCTYPE Project>'+self.project,
                        b'<!DOCTYPE Project [<!ENTITY x "value">]>'+self.project,
                        self.project[:-1], self.project.replace(b'Project Sdk=', b'Other Sdk=')]:
            with self.subTest(project=project[:40]), self.assertRaises(NuGetInputFailure):
                self.population(project)

    def test_conditional_unknown_facts_are_not_evaluated_as_contradictions(self):
        project = self.project.replace(b'<ItemGroup>', b'<ItemGroup Condition="opaque">')
        lock = json.loads(self.lock)
        lock['dependencies']['net10.0'] = {}
        self.assertEqual(self.population(project, lock).declarations, ())

    def test_binding_false_assertions_and_stale_substitution_refuse(self):
        for key, value in [('project', 'Other.csproj'), ('framework', 'net9.0'),
                           ('project_sha256', '0'*64), ('lock_sha256', '0'*64),
                           ('coherent_snapshot', False), ('explicit_external_direct_complete', False)]:
            witness = deepcopy(self.witness); witness[key] = value
            with self.subTest(key=key), self.assertRaises(NuGetInputFailure) as caught:
                self.parse_testimony(witness)
            self.assertEqual(caught.exception.category, 'context_mismatch')
        for args in [dict(project=self.project+b'\n'), dict(lock=self.lock+b'\n')]:
            with self.assertRaises(NuGetInputFailure):
                self.parse_testimony(**args)

    def test_exact_framing_and_whole_record_validation_precede_semantics(self):
        for key, value in [('version', True), ('version', 2), ('packages', {}),
                           ('coherent_snapshot', 1), ('extra', 'SECRET'),
                           ('explicit_external_direct_complete', 'yes')]:
            witness = deepcopy(self.witness); witness[key] = value
            with self.subTest(key=key), self.assertRaises(NuGetInputFailure):
                self.parse_testimony(witness)
        witness = deepcopy(self.witness)
        witness['coherent_snapshot'] = False
        witness['packages'] = [dict(id='Example', version='2.0.0', namespace=[])]
        with self.assertRaises(NuGetInputFailure) as caught:
            self.parse_testimony(witness)
        self.assertEqual(caught.exception.category, 'malformed')
        witness['packages'] = [dict(id='Example', version='2.0.0', namespace=PUBLIC_ORIGIN),
                               dict(id='EXAMPLE', version='2.0', namespace='private')]
        with self.assertRaises(NuGetInputFailure):
            self.parse_testimony(witness)

    def test_population_acceptance_alone_never_authorizes_namespace(self):
        selected = parse_selected_identity('2.0.0')
        for namespace in [None, 'unknown', 'private', PUBLIC_ORIGIN+',private', PUBLIC_ORIGIN+'/']:
            witness = deepcopy(self.witness)
            if namespace is not None:
                witness['packages'] = [dict(id='Example', version='2.0.0', namespace=namespace)]
            authority = authorize_measurement(self.parse_testimony(witness), 'Example', selected, None)
            self.assertIsInstance(authority, LocalAuthorityFailure)
            self.assertEqual(authority.reason, 'unsupported_dependency_source')
        witness['packages'] = [dict(id='Example', version='2.0.0', namespace=PUBLIC_ORIGIN)]
        authority = authorize_measurement(self.parse_testimony(witness), 'Example', selected, None)
        self.assertIsInstance(authority, LocalAuthority)
        self.assertEqual(authority.namespace_basis, 'accepted_snapshot_namespace')
        self.assertIsNone(authority.content_hash)

    def test_a_witness_parser_does_not_accept_v3(self):
        with self.assertRaises(NuGetInputFailure):
            parse_provenance(local(self.witness), project_name='Witness.csproj',
                project_source=local(self.project), lock_source=local(self.lock), project=self.population())
