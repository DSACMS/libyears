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


class RepositorySnapshotSourceTests(unittest.TestCase):
    def setUp(self):
        from pathlib import Path
        import tempfile
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.calls = []
        self.urls = []
        for name in ('socket.socket', 'subprocess.Popen', 'subprocess.run', 'os.system',
                     'urllib.request.urlopen'):
            guard = patch(name, side_effect=AssertionError(name))
            spy = guard.start()
            self.addCleanup(spy.assert_not_called)
            self.addCleanup(guard.stop)

    def scan(self, projects=None, *, witnesses=(), lookup=None):
        from libyears.scan import scan_mixed_repository
        from tests.test_nuget_sources import repository_inputs
        from tests.test_nuget_population_source import files_for
        projects = {'a/Witness.csproj': files_for()} if projects is None else projects
        with repository_inputs(self.root, projects) as reads:
            report = scan_mixed_repository(self.root, nuget_repository=True,
                nuget_witnesses=witnesses, nuget_lookup=lookup or self.lookup)
        self.reads = reads
        return report

    def lookup(self, authorities):
        from libyears import nuget_registry as registry
        from libyears.nuget_supervisor import authority_message, decode_authority, result_message, decode_result
        from tests.test_nuget_acceptance import metadata
        documents = metadata(('example',))
        class Transport:
            def get(inner, url):
                self.urls.append(url)
                return json.dumps(documents[url]).encode()
        client = registry.NuGetMetadataClient(transport=Transport(), clock=lambda: 100)
        results = []
        for authority in authorities:
            self.calls.append(authority)
            authority = decode_authority(authority_message(authority))
            client.begin_package(authority.package_key)
            row = registry.lookup_authorized_package(authority, client)
            results.append((authority, decode_result(result_message(row))))
        return tuple(results)

    def test_automatic_b1_namespace_absent_knows_population_and_never_reads_witness(self):
        from libyears.output import format_human, report_to_dict
        report = self.scan()
        self.assertEqual((report.summary.dependencies_discovered, report.summary.dependencies_measured,
                          report.summary.coverage), (1, 0, 0.0))
        self.assertEqual([name for _, name in self.reads], ['Witness.csproj', 'packages.lock.json'])
        self.assertEqual(report.source_errors, ())
        row, = report.unmeasurable
        self.assertEqual(row.reason, 'unsupported_dependency_source')
        self.assertEqual(row.nuget_evidence.selected_version, '2.0.0')
        self.assertEqual(row.nuget_evidence.population_basis, 'qualified_repository_snapshot')
        self.assertIn('snapshot minimum', row.declared)
        data = report_to_dict(report, 'PRIVATE_CANARY')
        self.assertEqual(data['schema_version'], 3)
        evidence = data['nuget_sources'][0]['version_evidence']
        self.assertEqual(evidence['trust_basis'], 'repository_snapshot_policy')
        self.assertIn('historical_producing_association_not_established', evidence['population_limitations'])
        human = format_human(report, 'PRIVATE_CANARY')
        verbose = format_human(report, 'PRIVATE_CANARY', verbose=True)
        self.assertIn('policy-selected current repository snapshot', human)
        self.assertIn('accepted public namespace authority unavailable', human)
        self.assertNotIn('explicit supplier witness unavailable', human)
        for secret in ('PRIVATE_CANARY', 'project_sha256', 'lock_sha256', 'https://api.nuget.org'):
            self.assertNotIn(secret, human+verbose+json.dumps(data))
        self.assertEqual((self.calls, self.urls), ([], []))

    def test_a_precedence_preserves_missing_testimony_and_v3_refusal(self):
        from tests.test_nuget_population_source import files_for
        files = files_for(unsupported=False)
        for witnesses in ((), (('a/Witness.csproj', 'witness.json'),)):
            report = self.scan({'a/Witness.csproj': files}, witnesses=witnesses)
            self.assertEqual(report.source_results[-1].evidence.population_basis, 'declaration_derived')
            self.assertEqual(report.summary.dependencies_discovered, 1)
            self.assertEqual(report.unmeasurable, ())
            self.assertEqual(report.source_errors[0].reason,
                'invalid_nuget_provenance' if witnesses else 'nuget_provenance_missing')
        self.assertEqual(self.calls, [])

    def test_bidirectional_stale_and_mismatched_locks_cannot_be_repaired_by_v3(self):
        from tests.test_nuget_population_source import files_for, rebind
        for mutation in ('added', 'removed', 'request', 'extra', 'missing', 'framework', 'duplicate', 'version_child'):
            files = files_for(public=True)
            project = files['Witness.csproj']
            lock = json.loads(files['packages.lock.json'])
            entries = lock['dependencies']['net10.0']
            if mutation == 'added': project = project.replace(b'</ItemGroup>', b'<PackageReference Include="Added" Version="1.0" /></ItemGroup>')
            if mutation == 'removed': project = project.replace(b'<PackageReference Include="Example" Version="1.0" />', b'')
            if mutation == 'request': project = project.replace(b'Version="1.0"', b'Version="3.0"')
            if mutation == 'extra': entries['Extra'] = deepcopy(entries['Example'])
            if mutation == 'missing': entries.clear()
            if mutation == 'framework': project = project.replace(b'net10.0', b'net9.0')
            if mutation == 'duplicate': project = project.replace(b'</ItemGroup>', b'<PackageReference Include="EXAMPLE" Version="1.0" /></ItemGroup>')
            if mutation == 'version_child': project = project.replace(b'Version="1.0" />', b'Version="1.0"><Version>3.0</Version></PackageReference>')
            files.update({'Witness.csproj': project, 'packages.lock.json': json.dumps(lock).encode()})
            rebind(files)  # Synthetic fixture testimony cannot repair current conflict.
            for witnesses in ((), (('a/Witness.csproj', 'witness.json'),)):
                with self.subTest(mutation=mutation, witnesses=witnesses):
                    report = self.scan({'a/Witness.csproj': files}, witnesses=witnesses)
                    self.assertIsNone(report.summary.dependencies_discovered)
                    self.assertTrue(report.source_errors)
                    self.assertEqual(report.unmeasurable, ())
                    self.assertNotIn(('a/Witness.csproj', 'witness.json'), self.reads)
        self.assertEqual((self.calls, self.urls), ([], []))

    def test_reverse_conflict_is_terminal_even_with_unextractable_context(self):
        from tests.test_nuget_population_source import files_for, rebind
        files = files_for(public=True)
        files['Witness.csproj'] = files['Witness.csproj'].replace(b'net10.0', b'$(Framework)')
        lock = json.loads(files['packages.lock.json'])
        lock['dependencies']['net10.0']['Extra'] = deepcopy(lock['dependencies']['net10.0']['Example'])
        files['packages.lock.json'] = json.dumps(lock).encode()
        report = self.scan({'a/Witness.csproj': rebind(files)}, witnesses=(('a/Witness.csproj','witness.json'),))
        self.assertIsNone(report.summary.dependencies_discovered)
        self.assertEqual(report.source_errors[0].reason, 'nuget_context_mismatch')
        self.assertEqual(self.calls, [])

    def test_b2_remains_available_for_computed_reference_and_repeated_equal_framework(self):
        from tests.test_nuget_population_source import files_for, rebind
        for mutation in ('computed', 'repeated', 'import'):
            files = files_for()
            if mutation == 'computed':
                files['Witness.csproj'] = files['Witness.csproj'].replace(b'Version="1.0"', b'Version="$(Chosen)"')
            if mutation == 'repeated':
                files['Witness.csproj'] = files['Witness.csproj'].replace(b'</PropertyGroup>', b'<TargetFramework>net10.0</TargetFramework></PropertyGroup>')
            if mutation == 'import':
                files['Witness.csproj'] = files['Witness.csproj'].replace(b'</Project>', b'<Import Project="opaque" /></Project>')
            rebind(files)
            report = self.scan({'a/Witness.csproj': files})
            self.assertIsNone(report.summary.dependencies_discovered)
            report = self.scan({'a/Witness.csproj': files}, witnesses=(('a/Witness.csproj','witness.json'),))
            self.assertEqual(report.summary.dependencies_discovered, 1)
            self.assertEqual(report.source_results[-1].evidence.population_basis, 'resolved_snapshot')
        self.assertEqual(self.calls, [])

    def test_shared_immediate_lock_requires_explicit_attribution(self):
        from tests.test_nuget_population_source import files_for, rebind
        first = files_for()
        second = deepcopy(first)
        second['Other.csproj'] = second.pop('Witness.csproj')
        value = json.loads(second['witness.json']); value['project'] = 'Other.csproj'
        second['witness.json'] = json.dumps(value).encode()
        projects = {'a/Witness.csproj': first, 'a/Other.csproj': second}
        report = self.scan(projects)
        self.assertIsNone(report.summary.dependencies_discovered)
        report = self.scan(projects, witnesses=tuple((p,'witness.json') for p in projects))
        self.assertEqual(report.summary.dependencies_discovered, 2)
        self.assertEqual([s.evidence.population_basis for s in report.source_results if s.ecosystem=='nuget'],
                         ['resolved_snapshot', 'resolved_snapshot'])

    def test_b1_plus_valid_v3_retains_supplier_meaning_and_namespace_path(self):
        from tests.test_nuget_population_source import files_for
        from libyears.output import report_to_dict
        report = self.scan({'a/Witness.csproj': files_for(public=True)}, witnesses=(('a/Witness.csproj','witness.json'),))
        self.assertEqual((report.summary.dependencies_discovered, report.summary.dependencies_measured), (1,1))
        row, = report.measurements
        self.assertEqual(row.libyears, 0.0)
        evidence = row.dependency.nuget_evidence
        self.assertEqual(evidence.population_basis, 'qualified_repository_snapshot')
        self.assertEqual(evidence.namespace_basis, 'accepted_snapshot_namespace')
        self.assertEqual(evidence.origin_state, 'unavailable')
        source = report_to_dict(report, '')['nuget_sources'][0]['version_evidence']
        self.assertEqual(source['trust_basis'], 'supplied_snapshot_population_assertion')
        self.assertIn('accepted_retained_external_direct_snapshot', source['population_limitations'])
        self.assertEqual(len(self.calls), 1)
        self.assertTrue(self.urls)

    def test_supplied_invalid_v3_is_not_ignored_and_keeps_b1_n(self):
        from tests.test_nuget_population_source import files_for
        for key, value in [('project_sha256', '0'*64), ('lock_sha256', '0'*64),
                           ('project', 'Other.csproj'), ('framework', 'net9.0'),
                           ('coherent_snapshot', False), ('explicit_external_direct_complete', False),
                           ('packages', {}), ('extra', 'PRIVATE_CANARY'), ('version', 2), ('version', 1)]:
            files = files_for(public=True)
            witness = json.loads(files['witness.json']); witness[key] = value
            files['witness.json'] = json.dumps(witness).encode()
            with self.subTest(key=key, value=value):
                report = self.scan({'a/Witness.csproj': files}, witnesses=(('a/Witness.csproj','witness.json'),))
                self.assertEqual(report.summary.dependencies_discovered, 1)
                self.assertIsNone(report.summary.coverage)
                self.assertFalse(report.source_results[-1].measurement_available)
                self.assertTrue(report.source_errors)
                self.assertEqual(report.source_results[-1].evidence.population_basis, 'qualified_repository_snapshot')
        self.assertEqual((self.calls, self.urls), ([], []))

    def test_private_unknown_conflicting_namespace_never_grants_capability(self):
        from libyears.nuget_provenance import PUBLIC_ORIGIN
        from tests.test_nuget_population_source import files_for
        for namespace in ('private', 'unknown', PUBLIC_ORIGIN+',private', PUBLIC_ORIGIN+'/'):
            files = files_for(public=True)
            witness = json.loads(files['witness.json']); witness['packages'][0]['namespace'] = namespace
            files['witness.json'] = json.dumps(witness).encode()
            report = self.scan({'a/Witness.csproj': files}, witnesses=(('a/Witness.csproj','witness.json'),))
            self.assertEqual(report.unmeasurable[0].reason, 'unsupported_dependency_source')
            self.assertEqual(report.summary.coverage, 0.0)
        self.assertEqual((self.calls, self.urls), ([], []))

    def test_unavailable_a_and_independent_b1_occurrences_preserve_null_coverage(self):
        from tests.test_nuget_population_source import files_for
        projects = {'a/Witness.csproj': files_for(), 'b/Witness.csproj': files_for(),
                    'c/Witness.csproj': files_for(unsupported=False)}
        report = self.scan(projects)
        self.assertEqual((report.summary.dependencies_discovered, report.summary.dependencies_measured), (3,0))
        self.assertIsNone(report.summary.coverage)
        self.assertEqual([r.nuget_evidence.source_id for r in report.unmeasurable],
                         ['a/Witness.csproj','b/Witness.csproj'])
        self.assertEqual(report.source_errors[0].source_id, 'c/Witness.csproj')
        self.assertEqual(report.by_nuget_source['a/Witness.csproj'].coverage, 0.0)

    def test_unsafe_and_unsupported_whole_evidence_never_reaches_witness(self):
        from tests.test_nuget_population_source import files_for
        for kind in ('malformed_project', 'dtd', 'malformed_lock', 'unsupported_lock', 'contexts', 'alias', 'selected', 'requested'):
            files = files_for(public=True)
            if kind == 'malformed_project': files['Witness.csproj'] = b'<broken'
            if kind == 'dtd': files['Witness.csproj'] = b'<!DOCTYPE Project>'+files['Witness.csproj']
            if kind == 'malformed_lock': files['packages.lock.json'] = b'broken'
            if kind in ('unsupported_lock','contexts','alias','selected','requested'):
                lock = json.loads(files['packages.lock.json'])
                entry = lock['dependencies']['net10.0']['Example']
                if kind == 'unsupported_lock': lock['version'] = 2
                if kind == 'contexts': lock['dependencies']['net9.0'] = {}
                if kind == 'alias': lock['dependencies']['net10.0']['EXAMPLE'] = deepcopy(entry)
                if kind == 'selected': entry['resolved'] = 'PRIVATE_CANARY'
                if kind == 'requested': entry['requested'] = 'PRIVATE_CANARY'
                files['packages.lock.json'] = json.dumps(lock).encode()
            with self.subTest(kind=kind):
                report = self.scan({'a/Witness.csproj': files}, witnesses=(('a/Witness.csproj','witness.json'),))
                self.assertIsNone(report.summary.dependencies_discovered)
                self.assertEqual(report.unmeasurable, ())
                self.assertNotIn(('a/Witness.csproj','witness.json'), self.reads)
        self.assertEqual(self.calls, [])


from tests.nuget_fixtures import SAFE_SCOPED_READ
from libyears.nuget_discovery import discovery_available


@unittest.skipUnless(SAFE_SCOPED_READ and discovery_available(), 'safe anchored filesystem unavailable')
class RepositorySnapshotFilesystemTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        from pathlib import Path
        from tests.test_nuget_population_source import files_for
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for name, data in files_for().items():
            if name != 'witness.json':
                (self.root/name).write_bytes(data)

    def assert_current_policy(self):
        from libyears.nuget_sources import read_repository_sources
        with patch('subprocess.Popen', side_effect=AssertionError('no Git/target execution')), \
                patch('socket.socket', side_effect=AssertionError('no lookup')):
            source, = read_repository_sources(self.root)
        self.assertEqual(source.result.dependencies_discovered, 1)
        self.assertEqual(source.result.evidence.population_basis, 'qualified_repository_snapshot')
        self.assertEqual(source.result.unmeasurable, ())
        self.assertEqual(source.authorized_candidates[0].authority.namespace_basis, 'conventional_public_policy')

    def test_non_git_directory_current_pair_needs_no_git(self):
        self.assertFalse((self.root/'.git').exists())
        self.assert_current_policy()

    def test_dirty_current_project_and_untracked_lock_remain_eligible(self):
        import shutil
        import subprocess
        if shutil.which('git') is None:
            self.skipTest('Git needed only to construct this dirty-state witness')
        subprocess.run(['git','init','--quiet',str(self.root)], check=True)
        subprocess.run(['git','-C',str(self.root),'add','Witness.csproj'], check=True)
        project = self.root/'Witness.csproj'
        project.write_bytes(project.read_bytes()+b'\n')
        before = subprocess.check_output(['git','-C',str(self.root),'status','--porcelain'])
        self.assertIn(b'Witness.csproj', before)
        self.assertIn(b'?? packages.lock.json', before)
        self.assert_current_policy()
        self.assertEqual(subprocess.check_output(['git','-C',str(self.root),'status','--porcelain']), before)


def setUpModule():
    # This module tests sibling semantics with certified Maven absence.
    from tests.maven_fixtures import declare_maven_absent
    declare_maven_absent()
