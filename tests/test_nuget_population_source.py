"""Portable A/B source, namespace, occurrence and output behavior."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.nuget import read_nuget_source
from libyears.nuget_provenance import PUBLIC_ORIGIN
from libyears.output import format_human, report_to_dict
from libyears.scan import NuGetRequest, scan_mixed_repository
from tests.nuget_fixtures import fixture_nuget_reads
from tests.test_nuget_population import snapshot_inputs
from tests.test_nuget_sources import repository_inputs
from tests.test_nuget_scan import nuget_inputs


def files_for(*, public=False, unsupported=True):
    packages = [dict(id='Example', version='2.0.0', namespace=PUBLIC_ORIGIN)] if public else []
    project, lock, witness = snapshot_inputs(unsupported=unsupported, packages=packages)
    return {'Witness.csproj': project, 'packages.lock.json': lock,
            'witness.json': json.dumps(witness).encode()}


def rebind(files):
    """Synthetic fixture assertion only; never applied to real target evidence."""
    value = json.loads(files['witness.json'])
    value['project_sha256'] = hashlib.sha256(files['Witness.csproj']).hexdigest()
    value['lock_sha256'] = hashlib.sha256(files['packages.lock.json']).hexdigest()
    files['witness.json'] = json.dumps(value).encode()
    return files


class SnapshotSourceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.lookups = []
        self.urls = []
        self.guards = []
        for target in ('socket.socket', 'subprocess.Popen', 'subprocess.run', 'os.system',
                       'urllib.request.urlopen'):
            guard = patch(target, side_effect=AssertionError(target))
            self.guards.append(guard.start())
            self.addCleanup(guard.stop)

    def tearDown(self):
        for guard in self.guards:
            guard.assert_not_called()

    def source(self, files=None, *, accepted=True):
        files = files_for() if files is None else files
        with fixture_nuget_reads(self.root, files) as reads:
            source = read_nuget_source(self.root, 'Witness.csproj', 'witness.json' if accepted else None)
        return source, [c.args[1] for c in reads.call_args_list]

    def scan(self, files, *, documents=None):
        from libyears import nuget_registry as registry
        from libyears.nuget_supervisor import (authority_message, decode_authority,
                                               result_message, decode_result, failed_package)
        from tests.test_nuget_acceptance import metadata
        documents = metadata(('example',)) if documents is None else documents
        class Transport:
            def get(inner, url):
                self.urls.append(url)
                value = documents[url]
                if isinstance(value, Exception):
                    raise value
                return json.dumps(value).encode()
        def lookup(authorities):
            results = []
            client = registry.NuGetMetadataClient(transport=Transport(), clock=lambda: 100)
            for authority in authorities:
                self.lookups.append(authority)
                authority = decode_authority(authority_message(authority))
                client.begin_package(authority.package_key)
                try:
                    row = registry.lookup_authorized_package(authority, client)
                except registry.NuGetRegistryFailure as failure:
                    row = failed_package(authority, failure.reason)
                results.append((authority, decode_result(result_message(row))))
            return results
        with fixture_nuget_reads(self.root, files):
            return scan_mixed_repository(self.root, nuget_request=NuGetRequest('Witness.csproj', 'witness.json'),
                                         nuget_lookup=lookup)

    def assert_unknown(self, files, *, accepted=True):
        source, _ = self.source(files, accepted=accepted)
        self.assertIsNone(source.result.dependencies_discovered)
        self.assertFalse(source.result.measurement_available)
        self.assertEqual(source.result.evidence.population_basis, 'unknown')
        self.assertEqual(source.authorized_candidates, ())
        self.assertEqual(source.result.unmeasurable, ())
        self.assertTrue(source.result.source_errors)
        return source

    def test_b_requires_explicit_acceptance_and_never_reads_discovered_witness(self):
        source, reads = self.source(accepted=False)
        self.assertIsNone(source.result.dependencies_discovered)
        self.assertEqual(reads, ['Witness.csproj'])
        accepted, _ = self.source()
        self.assertEqual(accepted.result.dependencies_discovered, 1)
        self.assertEqual(accepted.result.evidence.population_basis, 'resolved_snapshot')

    def test_old_v1_v2_contracts_never_become_population_acceptance(self):
        for version in (1, 2):
            files = files_for()
            files['witness.json'] = json.dumps(dict(version=version)).encode()
            source = self.assert_unknown(files)
            self.assertEqual(source.result.source_errors[0].reason, 'unsupported_nuget_project')

    def test_a_precedence_refuses_v3_with_known_population(self):
        files = files_for(unsupported=False, public=True)
        source, _ = self.source(files)
        self.assertEqual(source.result.dependencies_discovered, 1)
        self.assertEqual(source.result.evidence.population_basis, 'declaration_derived')
        self.assertEqual(source.result.source_errors[0].reason, 'invalid_nuget_provenance')
        self.assertFalse(source.result.measurement_available)
        files['packages.lock.json'] = b'broken'
        source, reads = self.source(files)
        self.assertEqual(source.result.dependencies_discovered, 1)
        self.assertNotIn('witness.json', reads)

    def test_unsupported_baseline_on_a_cannot_invoke_b(self):
        files = nuget_inputs()
        witness = json.loads(files['witness.json'])
        witness['baseline']['unsupported_membership_version_influences'] = True
        files['witness.json'] = json.dumps(witness).encode()
        source = self.assert_unknown(files)
        self.assertEqual(source.result.source_errors[0].reason, 'unsupported_nuget_project')

    def test_ineligible_project_failures_never_read_acceptance(self):
        for project in (b'<broken', b'\xff', b'<Project />'):
            files = files_for()
            files['Witness.csproj'] = project
            source, reads = self.source(files)
            self.assertIsNone(source.result.dependencies_discovered)
            if project != b'<Project />':
                self.assertEqual(reads, ['Witness.csproj'])
        files = files_for()
        with patch('libyears.nuget_project.MAX_PROJECT_BYTES', 0):
            _, reads = self.source(files)
        self.assertEqual(reads, ['Witness.csproj'])

    def test_stale_mismatched_and_false_snapshot_acceptance_remains_unknown(self):
        for key, value in [('project', 'Other.csproj'), ('framework', 'net9.0'),
                           ('project_sha256', '0'*64), ('lock_sha256', '0'*64),
                           ('coherent_snapshot', False), ('explicit_external_direct_complete', False),
                           ('packages', {}), ('extra', 'PRIVATE_CANARY')]:
            files = files_for(public=True)
            witness = json.loads(files['witness.json'])
            witness[key] = value
            files['witness.json'] = json.dumps(witness).encode()
            with self.subTest(key=key):
                self.assert_unknown(files)
        for name in ('Witness.csproj', 'packages.lock.json'):
            files = files_for(public=True)
            files[name] += b'\n'
            self.assert_unknown(files)

    def test_known_contradictions_and_mixed_duplicates_never_escape(self):
        for old, new in [(b'net10.0', b'net9.0'), (b'net10.0', b'net10.0;net9.0'),
                         (b'Version="1.0"', b'Version="3.0"'),
                         (b'Include="Example"', b'Include="Added"'),
                         (b'</ItemGroup>', b'<PackageReference Include="EXAMPLE" Version="1.0" /></ItemGroup>')]:
            files = files_for(public=True)
            files['Witness.csproj'] = files['Witness.csproj'].replace(old, new)
            self.assert_unknown(rebind(files))
        files = files_for(public=True)
        files['Witness.csproj'] = b'<!DOCTYPE Project>'+files['Witness.csproj']
        self.assert_unknown(rebind(files))

    def test_repeated_identical_literal_framework_facts_accept_one_snapshot_context(self):
        for property_name in ('TargetFramework', 'TargetFrameworks'):
            files = files_for(unsupported=False)
            extra = ('<' + property_name + '>net10.0</' + property_name + '>').encode()
            files['Witness.csproj'] = files['Witness.csproj'].replace(
                b'</PropertyGroup>', extra+b'</PropertyGroup>')
            report = self.scan(rebind(files))
            self.assertEqual(report.summary.dependencies_discovered, 1)
            self.assertEqual(report.summary.dependencies_measured, 0)
            self.assertEqual(report.source_results[-1].evidence.population_basis, 'resolved_snapshot')
            self.assertEqual(report.unmeasurable[0].reason, 'unsupported_dependency_source')
            self.assertEqual(self.lookups, [])
            self.assertEqual(self.urls, [])

    def test_any_distinct_literal_framework_fact_still_refuses_the_whole_snapshot(self):
        for value in ('net9.0', 'net10.0;net9.0'):
            files = files_for(unsupported=False, public=True)
            extra = ('<TargetFrameworks>' + value + '</TargetFrameworks>').encode()
            files['Witness.csproj'] = files['Witness.csproj'].replace(
                b'</PropertyGroup>', extra+b'</PropertyGroup>')
            self.assert_unknown(rebind(files))

    def test_whole_direct_request_selected_and_context_failures_keep_n_unknown(self):
        for change in ('missing_selected', 'unsafe_selected', 'bad_request', 'extra_context', 'alias'):
            files = files_for(public=True)
            lock = json.loads(files['packages.lock.json'])
            entry = lock['dependencies']['net10.0']['Example']
            if change == 'missing_selected': del entry['resolved']
            if change == 'unsafe_selected': entry['resolved'] = 'PRIVATE_CANARY'
            if change == 'bad_request': entry['requested'] = 'PRIVATE_CANARY'
            if change == 'extra_context': lock['dependencies']['net10.0/win-x64'] = {}
            if change == 'alias': lock['dependencies']['net10.0']['EXAMPLE'] = deepcopy(entry)
            files['packages.lock.json'] = json.dumps(lock).encode()
            with self.subTest(change=change):
                self.assert_unknown(rebind(files))

    def test_absent_private_unknown_namespaces_establish_population_without_lookup(self):
        for namespace in (None, 'private', 'unknown', PUBLIC_ORIGIN+',private', PUBLIC_ORIGIN+'/'):
            files = files_for(public=True)
            witness = json.loads(files['witness.json'])
            if namespace is None:
                witness['packages'] = []
            else:
                witness['packages'][0]['namespace'] = namespace
            files['witness.json'] = json.dumps(witness).encode()
            report = self.scan(files)
            self.assertEqual((report.summary.dependencies_discovered, report.summary.dependencies_measured,
                              report.summary.coverage), (1, 0, 0.0))
            self.assertEqual(report.unmeasurable[0].reason, 'unsupported_dependency_source')
            self.assertEqual(report.unmeasurable[0].nuget_evidence.population_basis, 'resolved_snapshot')
            self.assertEqual(self.lookups, [])
            self.assertEqual(self.urls, [])

    def test_positive_snapshot_namespace_age_has_no_acquisition_or_content_claim(self):
        report = self.scan(files_for(public=True))
        data = report_to_dict(report, 'PRIVATE_CANARY')
        self.assertEqual(data['schema_version'], 3)
        row, = data['dependencies']
        self.assertEqual((row['used_version'], row['libyears']), ('2.0.0', 0.0))
        evidence = row['nuget_evidence']
        self.assertEqual(evidence['population_basis'], 'resolved_snapshot')
        self.assertEqual(evidence['namespace_basis'], 'accepted_snapshot_namespace')
        self.assertEqual(evidence['origin_state'], 'unavailable')
        self.assertEqual(evidence['assurance']['producer_event'], 'unavailable')
        source = data['version_evidence']['nuget']
        self.assertIn('population_limitations', source)
        human = format_human(report, 'PRIVATE_CANARY')
        verbose = format_human(report, 'PRIVATE_CANARY', verbose=True)
        self.assertIn('accepted resolved snapshot', human)
        self.assertIn('current_evaluated_declaration_completeness_not_established', verbose)
        for secret in ('PRIVATE_CANARY', PUBLIC_ORIGIN, 'project_sha256', 'lock_sha256'):
            self.assertNotIn(secret, json.dumps(data)+human+verbose)

    def test_snapshot_nonzero_age_uses_unchanged_metric(self):
        files = files_for(public=True)
        lock = json.loads(files['packages.lock.json'])
        lock['dependencies']['net10.0']['Example']['resolved'] = '1.0.0'
        files['packages.lock.json'] = json.dumps(lock).encode()
        witness = json.loads(files['witness.json'])
        witness['packages'][0]['version'] = '1.0.0'
        files['witness.json'] = json.dumps(witness).encode()
        report = self.scan(rebind(files))
        self.assertEqual(report.summary.total_libyears, 1.0)
        self.assertEqual(report.summary.coverage, 1.0)

    def test_later_metadata_failure_retains_snapshot_basis_and_selected_evidence(self):
        from tests.test_nuget_acceptance import metadata
        documents = metadata(('example',))
        index = next(k for k in documents if k.endswith('/example/index.json'))
        documents[index] = ValueError('PRIVATE_CANARY')
        report = self.scan(files_for(public=True), documents=documents)
        row, = report.unmeasurable
        self.assertEqual(row.nuget_evidence.population_basis, 'resolved_snapshot')
        self.assertEqual(row.nuget_evidence.selected_version, '2.0.0')
        self.assertEqual(report.summary.dependencies_discovered, 1)

    def test_accepted_empty_snapshot_is_known_zero_not_unknown(self):
        files = files_for()
        files['Witness.csproj'] = files['Witness.csproj'].replace(
            b'<PackageReference Include="Example" Version="1.0" />', b'')
        lock = json.loads(files['packages.lock.json'])
        lock['dependencies']['net10.0'] = {}
        files['packages.lock.json'] = json.dumps(lock).encode()
        report = self.scan(rebind(files))
        self.assertEqual(report.summary.dependencies_discovered, 0)
        self.assertEqual(report.summary.dependencies_measured, 0)
        self.assertIsNone(report.summary.coverage)
        self.assertEqual(report.source_results[-1].evidence.population_basis, 'resolved_snapshot')
        self.assertEqual(self.lookups, [])

    def test_b_selection_is_snapshot_request_with_unknown_computed_declaration(self):
        files = files_for()
        files['Witness.csproj'] = files['Witness.csproj'].replace(b'Version="1.0"', b'Version="$(Unknown)"')
        report = self.scan(rebind(files))
        row, = report.unmeasurable
        self.assertIn('snapshot minimum', row.declared)
        self.assertEqual(row.nuget_evidence.selected_version, '2.0.0')
        self.assertEqual(row.nuget_evidence.population_basis, 'resolved_snapshot')

    def test_mixed_a_b_occurrences_survive_unknown_sibling_without_deduplication(self):
        projects = {'a/Witness.csproj': files_for(), 'b/Witness.csproj': files_for(),
                    'c/Witness.csproj': nuget_inputs(), 'd/Bad.csproj': {'Bad.csproj': b'broken'}}
        witnesses = [(p, 'witness.json') for p in projects if p != 'd/Bad.csproj']
        # No public authority for B; A's ordinary v1 has one capability.
        from tests.test_nuget_repository import success
        lookup = Mock(side_effect=lambda authorities: tuple((a, success(a)) for a in authorities))
        with repository_inputs(self.root, projects):
            report = scan_mixed_repository(self.root, nuget_repository=True,
                nuget_witnesses=witnesses, nuget_lookup=lookup)
        self.assertIsNone(report.summary.dependencies_discovered)
        self.assertEqual(report.summary.dependencies_measured, 1)
        self.assertIsNone(report.summary.coverage)
        data = report_to_dict(report, '')
        self.assertEqual([s['version_evidence']['population_basis'] for s in data['nuget_sources']],
                         ['resolved_snapshot', 'resolved_snapshot', 'declaration_derived', 'unknown'])
        self.assertEqual([r['source_id'] for r in data['unmeasurable'] if r['name']=='Example'],
                         ['a/Witness.csproj', 'b/Witness.csproj'])
        self.assertIn('accepted resolved snapshot', format_human(report, ''))
