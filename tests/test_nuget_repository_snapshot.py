"""Qualified current snapshot policy; no supplier history or namespace inference."""

from copy import deepcopy
import json
import unittest
from unittest.mock import patch

from libyears.nuget_input import NuGetInputFailure
from libyears.nuget_lock import parse_lock
from libyears.nuget_population import repository_snapshot_population
from libyears.nuget_project import parse_project
from tests.test_nuget_population import local, snapshot_inputs


class RepositorySnapshotPrimitiveTests(unittest.TestCase):
    def setUp(self):
        self.project, self.lock, _ = snapshot_inputs()

    def qualify(self, project=None, lock=None):
        return repository_snapshot_population(local(self.project if project is None else project),
            parse_lock(local(self.lock if lock is None else lock)))

    def refuse(self, project=None, lock=None, category=None):
        with self.assertRaises(NuGetInputFailure) as caught:
            self.qualify(project, lock)
        if category:
            self.assertEqual(caught.exception.category, category)

    def test_unrelated_syntax_does_not_require_complete_a_semantics(self):
        with self.assertRaises(NuGetInputFailure):
            parse_project(local(self.project))
        with patch('subprocess.run', side_effect=AssertionError('no Git/evaluation')), \
                patch('socket.socket', side_effect=AssertionError('no namespace')):
            population = self.qualify()
        self.assertEqual(population.framework, 'net10.0')
        self.assertEqual([d.package_key for d in population.declarations], ['example'])
        ancillary = self.project.replace(b'</Project>',
            b'<PropertyGroup Condition="opaque"><OutputPath /></PropertyGroup>'
            b'<ItemGroup><None Update="opaque"><Unknown>%(Uninterpreted)</Unknown></None></ItemGroup></Project>')
        self.assertIsNotNone(self.qualify(ancillary))

    def test_both_directions_and_changed_requests_are_terminal(self):
        added = self.project.replace(b'</ItemGroup>',
            b'<PackageReference Include="Added" Version="1.0" /></ItemGroup>')
        removed = self.project.replace(b'<PackageReference Include="Example" Version="1.0" />', b'')
        changed = self.project.replace(b'Version="1.0"', b'Version="3.0"')
        for project in (added, removed, changed):
            with self.subTest(project=project):
                self.refuse(project, category='context_mismatch')
        extra = json.loads(self.lock)
        extra['dependencies']['net10.0']['Extra'] = deepcopy(extra['dependencies']['net10.0']['Example'])
        self.refuse(lock=extra, category='context_mismatch')
        missing = json.loads(self.lock)
        missing['dependencies']['net10.0'].clear()
        self.refuse(lock=missing, category='context_mismatch')

    def test_copied_matching_pair_and_normalized_minimum_are_eligible(self):
        copied = bytes(bytearray(self.project))
        self.assertIsNotNone(self.qualify(copied.replace(b'Version="1.0"', b'Version="1.0.0.0"')))
        self.refuse(copied.replace(b'Include="Example"', b'Include="Other"'))

    def test_framework_conflicts_ambiguity_and_unextractable_facts(self):
        self.refuse(self.project.replace(b'net10.0', b'net9.0'), category='context_mismatch')
        self.refuse(self.project.replace(b'net10.0', b'net10.0;net9.0'), category='context_mismatch')
        for replacement in (b'$(Framework)', b'net10.0<Other/>', b''):
            self.assertIsNone(self.qualify(self.project.replace(b'>net10.0<', b'>'+replacement+b'<')))
        repeated = self.project.replace(b'</PropertyGroup>',
            b'<TargetFramework>net10.0</TargetFramework></PropertyGroup>')
        self.assertIsNone(self.qualify(repeated))
        self.refuse(repeated.replace(b'<TargetFramework>net10.0</TargetFramework></PropertyGroup>',
                                     b'<TargetFramework>net9.0</TargetFramework></PropertyGroup>'))

    def test_unknown_reference_facts_and_named_mutations_do_not_qualify(self):
        for old, new in [(b'Version="1.0"', b'Version="$(Version)"'),
                         (b'Include="Example"', b'Update="Example"'),
                         (b'Include="Example"', b'Remove="Example"'),
                         (b'<ItemGroup>', b'<ItemGroup Condition="true">'),
                         (b'Version="1.0"', b'Version="1.0" Condition="true"'),
                         (b'Version="1.0" />', b'Version="1.0"><Unknown /></PackageReference>'),
                         (b'<PackageReference', b'<packagereference')]:
            with self.subTest(new=new):
                self.assertIsNone(self.qualify(self.project.replace(old, new)))
        for name in ('Import', 'Target', 'Choose', 'PackageVersion', 'GlobalPackageReference',
                     'ManagePackageVersionsCentrally', 'CentralPackageVersionOverrideEnabled',
                     'CentralPackageTransitivePinningEnabled', 'RuntimeIdentifier', 'RuntimeIdentifiers'):
            project = self.project.replace(b'</Project>', ('<'+name+' /></Project>').encode())
            self.assertIsNone(self.qualify(project))
        root_condition = self.project.replace(b'<Project Sdk=', b'<Project Condition="opaque" Sdk=')
        self.assertIsNone(self.qualify(root_condition))
        nested = self.project.replace(b'<ItemGroup>', b'<Other><ItemGroup>').replace(
            b'</ItemGroup>', b'</ItemGroup></Other>')
        self.assertIsNone(self.qualify(nested))

    def test_known_conflict_survives_other_ineligibility(self):
        extra = json.loads(self.lock)
        extra['dependencies']['net10.0']['Extra'] = deepcopy(extra['dependencies']['net10.0']['Example'])
        for project in (self.project.replace(b'net10.0', b'$(Framework)'),
                        self.project.replace(b'</Project>', b'<Import /></Project>')):
            self.refuse(project, extra, 'context_mismatch')
        conflict = self.project.replace(b'Version="1.0" />',
            b'Version="1.0"><Version>3.0</Version></PackageReference>')
        self.refuse(conflict, category='context_mismatch')

    def test_duplicate_unsafe_and_over_budget_input_never_salvages(self):
        duplicate = self.project.replace(b'</ItemGroup>',
            b'<PackageReference Include="EXAMPLE" Version="1.0" /></ItemGroup>')
        self.refuse(duplicate, category='duplicate')
        self.refuse(b'<!DOCTYPE Project>'+self.project)
        self.refuse(self.project[:-1], category='malformed')
        with patch('libyears.nuget_population.MAX_PROJECT_BYTES', 1):
            self.refuse(category='limit')
        for field, value in [('requested', '[1.0, )'), ('requested', 'private/path'),
                             ('resolved', None), ('resolved', 'private/path')]:
            lock = json.loads(self.lock)
            lock['dependencies']['net10.0']['Example'][field] = value
            self.refuse(lock=lock)
        for value in ({'version': 2, 'dependencies': {}}, {'version': 1, 'dependencies': {'net10.0': {}, 'net9.0': {}}}):
            self.refuse(lock=value)
        alias = json.loads(self.lock)
        alias['dependencies']['net10.0']['EXAMPLE'] = alias['dependencies']['net10.0']['Example']
        self.refuse(lock=alias)

    def test_empty_direct_and_closure_never_inflate_population(self):
        lock = json.loads(self.lock)
        entries = lock['dependencies']['net10.0']
        entries['Closure'] = dict(type='Transitive', resolved='1.0.0', contentHash='opaque')
        entries['Project'] = dict(type='Project')
        self.assertEqual(len(self.qualify(lock=lock).declarations), 1)
        del entries['Example']
        project = self.project.replace(b'<PackageReference Include="Example" Version="1.0" />', b'')
        self.assertEqual(self.qualify(project, lock).declarations, ())
