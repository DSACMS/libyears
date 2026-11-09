"""Occurrence-specific comparator, real adapter/codecs, no live network."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from libyears import nuget_registry as registry
from libyears.nuget_comparator import parse_repository_policy
from libyears.nuget_provenance import PUBLIC_ORIGIN
from libyears.nuget_supervisor import (authority_message, decode_authority, decode_result,
                                      failed_package, result_message)
from libyears.output import format_human, report_to_dict
from libyears.registry import TransportFailure
from libyears.scan import scan_mixed_repository
from tests.test_nuget_acceptance import metadata
from tests.test_nuget_comparator import config, source, mapping, local
from tests.test_nuget_population_source import files_for
from tests.test_nuget_scan import nuget_inputs
from tests.test_nuget_sources import repository_inputs


class ComparatorSourceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.calls, self.urls = [], []
        for name in ('socket.socket', 'subprocess.Popen', 'urllib.request.urlopen'):
            guard = patch(name, side_effect=AssertionError('no network/process in offline test'))
            spy = guard.start(); self.addCleanup(spy.assert_not_called); self.addCleanup(guard.stop)

    def scan(self, files=None, *, configs=(), witnesses=(), projects=None, policies=None, documents=None):
        files = files_for() if files is None else files
        projects = {'a/Witness.csproj': files} if projects is None else projects
        policies = {} if policies is None else policies
        def policy(reader, project):
            relative = (reader.root.relative_to(self.root)/'Witness.csproj').as_posix()
            inputs = policies.get(relative, configs)
            return parse_repository_policy(tuple(local(c) for c in inputs), project)
        documents = metadata(('example','alpha','beta')) if documents is None else documents
        class Transport:
            def get(inner, url):
                self.urls.append(url)
                item = documents[url]
                if isinstance(item, TransportFailure):
                    return item
                return json.dumps(item).encode()
        def lookup(authorities):
            client = registry.NuGetMetadataClient(transport=Transport(), clock=lambda:100)
            results = []
            for authority in authorities:
                self.calls.append(authority)
                authority = decode_authority(authority_message(authority))
                client.begin_package(authority.package_key)
                try:
                    result = registry.lookup_authorized_package(authority, client)
                except registry.NuGetRegistryFailure as failure:
                    result = failed_package(authority, failure.reason)
                results.append((authority, decode_result(result_message(result))))
            return results
        with repository_inputs(self.root, projects), \
                patch('libyears.nuget_sources.RepositoryNuGetReader.comparator_policy', policy):
            return scan_mixed_repository(self.root, nuget_repository=True,
                nuget_witnesses=witnesses, nuget_lookup=lookup)

    def test_no_config_b1_and_a_use_same_truthful_age_floor(self):
        for unsupported in (True,False):
            report = self.scan(files_for(unsupported=unsupported))
            self.assertEqual((report.summary.dependencies_discovered,report.summary.dependencies_measured,
                              report.summary.coverage),(1,1,1.0))
            row, = report.measurements
            evidence = row.dependency.nuget_evidence
            self.assertEqual(evidence.comparator_basis,'conventional_public_policy')
            self.assertEqual(evidence.population_basis,
                'qualified_repository_snapshot' if unsupported else 'declaration_derived')
            self.assertEqual(evidence.measurement_basis,'public_comparator_version_age')
            self.assertEqual((evidence.origin_state,evidence.content_hash_state),('unavailable','unavailable'))
            self.assertEqual(row.libyears,0.0)
            if not unsupported:
                self.assertIn('supplier_baseline_not_established',report.source_results[-1].evidence.population_limitations)
            data=report_to_dict(report,'')
            self.assertEqual(data['schema_version'],3)
            ev=data['dependencies'][0]['nuget_evidence']
            self.assertIn('namespace_correspondence_assumed_by_policy',ev['comparator_limitations'])
            self.assertEqual(ev['assurance']['producer_event'],'unavailable')
            self.assertNotIn('accepted_snapshot_not_evaluated_runtime',ev['assurance']['limitations'])
            self.assertIn('assumes namespace correspondence',format_human(report,''))
            self.assertTrue(self.urls)

    def test_mapping_public_and_private_and_exact_over_prefix_zero_http(self):
        entries=source()+source('private','https://private.invalid')
        for maps,expected in [(mapping('public','Example'),'repository_mapping'),
                              (mapping('private','Example'),'nuget_comparator_private'),
                              (mapping('private','Example')+mapping('public','Example*'),'nuget_comparator_private'),
                              (mapping('private','Example')+mapping('public','Example'),'nuget_comparator_ambiguous')]:
            self.calls.clear();self.urls.clear()
            report=self.scan(configs=(config(entries,maps,closed=True),))
            if expected=='repository_mapping':
                self.assertEqual(report.measurements[0].dependency.nuget_evidence.comparator_basis,expected)
            else:
                self.assertEqual(report.unmeasurable[0].reason,expected)
                self.assertEqual((self.calls,self.urls),([],[]))

    def test_alternate_local_unsupported_and_source_property_never_reach_http(self):
        cases=[(files_for(),config(source()+source('private','https://private.invalid')),'nuget_comparator_ambiguous'),
               (files_for(),config(source('local','/local/feed')),'nuget_comparator_ambiguous'),
               (files_for(),'<configuration><unknown /></configuration>','nuget_comparator_unknown')]
        files=files_for(); files['Witness.csproj']=files['Witness.csproj'].replace(b'</Project>',
            b'<PropertyGroup><RestoreSources>https://private.invalid</RestoreSources></PropertyGroup></Project>')
        cases.append((files,config(source()),'nuget_comparator_unknown'))
        for files,text,reason in cases:
            report=self.scan(files,configs=(text,))
            self.assertEqual(report.unmeasurable[0].reason,reason)
        self.assertEqual((self.calls,self.urls),([],[]))

    def test_explicit_namespace_resolves_eligibility_but_not_conflict_or_unknown_policy(self):
        files=files_for(public=True)
        alternate=config(source('other','https://other.invalid'))
        report=self.scan(files,configs=(alternate,),witnesses=(('a/Witness.csproj','witness.json'),))
        row=report.measurements[0].dependency.nuget_evidence
        self.assertEqual((row.comparator_basis,row.namespace_basis),('explicit_testimony','accepted_snapshot_namespace'))
        self.assertIn('accepted_retained_external_direct_snapshot',report.source_results[-1].evidence.population_limitations)
        self.calls.clear();self.urls.clear()
        for text in (config(source('other','/private'),mapping('other','Example'),closed=True),
                     '<configuration><unknown /></configuration>'):
            report=self.scan(files,configs=(text,),witnesses=(('a/Witness.csproj','witness.json'),))
            self.assertEqual(report.summary.dependencies_measured,0)
        self.assertEqual((self.calls,self.urls),([],[]))

    def test_exact_private_unknown_conflicting_testimony_cannot_use_public_namesake(self):
        for namespace in ('private','unknown',PUBLIC_ORIGIN+',private'):
            files=files_for(public=True)
            witness=json.loads(files['witness.json']);witness['packages'][0]['namespace']=namespace
            files['witness.json']=json.dumps(witness).encode()
            report=self.scan(files,witnesses=(('a/Witness.csproj','witness.json'),))
            self.assertEqual(report.unmeasurable[0].reason,'unsupported_dependency_source')
        self.assertEqual((self.calls,self.urls),([],[]))

    def test_valid_whole_witness_missing_row_may_cascade_invalid_whole_may_not(self):
        report=self.scan(files_for(),witnesses=(('a/Witness.csproj','witness.json'),))
        self.assertEqual(report.measurements[0].dependency.nuget_evidence.comparator_basis,'conventional_public_policy')
        self.calls.clear();self.urls.clear()
        files=files_for();w=json.loads(files['witness.json']);w['project_sha256']='0'*64
        files['witness.json']=json.dumps(w).encode()
        report=self.scan(files,witnesses=(('a/Witness.csproj','witness.json'),))
        self.assertTrue(report.source_errors);self.assertIsNone(report.summary.coverage)
        self.assertEqual((self.calls,self.urls),([],[]))

    def test_a_stronger_v1_accepted_meaning_preserved_and_missing_record_cascades(self):
        for missing in (False,True):
            files=nuget_inputs()
            if missing:
                witness=json.loads(files['witness.json']);witness['packages']=[]
                files['witness.json']=json.dumps(witness).encode()
            report=self.scan(files,witnesses=(('a/Witness.csproj','witness.json'),))
            evidence=report.measurements[0].dependency.nuget_evidence
            self.assertEqual(evidence.population_basis,'declaration_derived')
            self.assertEqual(evidence.comparator_basis,'conventional_public_policy' if missing else 'explicit_testimony')
            if not missing:
                self.assertEqual(evidence.namespace_basis,'accepted_producer_origin')
                self.assertEqual(evidence.origin_state,'public_content_verified')

    def test_a_whole_pair_coherence_and_attribution_refusal_keeps_known_n(self):
        files=files_for(unsupported=False)
        for field,value in [('requested','[9.0.0, )'),('resolved','unsafe'),('type','Transitive')]:
            changed=deepcopy(files);lock=json.loads(changed['packages.lock.json'])
            lock['dependencies']['net10.0']['Example'][field]=value
            changed['packages.lock.json']=json.dumps(lock).encode()
            report=self.scan(changed)
            self.assertEqual(report.summary.dependencies_discovered,1)
            self.assertIsNone(report.summary.coverage)
            self.assertTrue(report.source_errors)
        self.assertEqual((self.calls,self.urls),([],[]))

    def test_same_identity_different_project_policy_mixed_partial_coverage(self):
        projects={'a/Witness.csproj':files_for(), 'b/Witness.csproj':files_for()}
        private=config(source('private','/local'),mapping('private','Example'),closed=True)
        report=self.scan(projects=projects,policies={'b/Witness.csproj':(private,)})
        self.assertEqual((report.summary.dependencies_discovered,report.summary.dependencies_measured,
                          report.summary.coverage),(2,1,0.5))
        self.assertEqual(report.measurements[0].dependency.nuget_evidence.source_id,'a/Witness.csproj')
        self.assertEqual(report.unmeasurable[0].nuget_evidence.source_id,'b/Witness.csproj')
        self.assertEqual(len(self.calls),1)

    def test_absent_package_version_and_transport_remain_registry_reality(self):
        for kind,reason in [('package','package_not_found'),('version','version_not_found'),
                            ('rate','registry_error'),('transport','registry_error')]:
            docs=metadata(('example',))
            url=registry.REGISTRATION_BASE+'example/index.json'
            if kind=='package':docs[url]=TransportFailure(404, 'not found')
            if kind=='version':
                page=docs[url]['items'][0];page['items']=page['items'][:1];page['count']=1;page['upper']='1.0.0';page['@id']=url+'#page/1.0.0/1.0.0'
            if kind=='rate':docs[url]=TransportFailure(429, 'rate limited')
            if kind=='transport':docs[url]=TransportFailure(None, 'network')
            report=self.scan(documents=docs)
            self.assertEqual(report.unmeasurable[0].reason,reason)
            self.assertEqual(report.unmeasurable[0].nuget_evidence.comparator_basis,'conventional_public_policy')

    def test_policy_codecs_reject_fabricated_producer_content_assurance(self):
        self.scan()
        authority=self.calls[0]
        value=authority_message(authority)
        self.assertEqual(decode_authority(value),authority)
        value['local_content_state']='mismatch'
        with self.assertRaises(ValueError):decode_authority(value)
        result=result_message(failed_package(authority))
        result['origin_state']='asserted_public'
        with self.assertRaises(ValueError):decode_result(result)

    def test_b2_public_testimony_with_unextractable_request_remains_independent(self):
        from tests.test_nuget_population_source import rebind
        files = files_for(public=True)
        files['Witness.csproj'] = files['Witness.csproj'].replace(b'Version="1.0"', b'Version="$(Chosen)"')
        report = self.scan(rebind(files), witnesses=(('a/Witness.csproj','witness.json'),))
        evidence = report.measurements[0].dependency.nuget_evidence
        self.assertEqual(evidence.population_basis, 'resolved_snapshot')
        self.assertEqual(evidence.comparator_basis, 'explicit_testimony')

    def test_a_shared_lock_never_gets_automatic_current_pair_attribution(self):
        first = files_for(unsupported=False)
        second = dict(first)
        second['Other.csproj'] = second.pop('Witness.csproj')
        report = self.scan(projects={'a/Witness.csproj': first, 'a/Other.csproj': second})
        self.assertEqual(report.summary.dependencies_discovered, 2)
        self.assertIsNone(report.summary.coverage)
        self.assertEqual([e.reason for e in report.source_errors], ['nuget_provenance_missing']*2)
        self.assertEqual((self.calls, self.urls), ([], []))

    def test_explicit_public_exclusion_cannot_be_downgraded_by_alternate_eligibility(self):
        files = files_for(public=True)
        entries = source()+source('other', '/local/feed')
        for text in (config(entries, disabled='<add key="public" value="true" />'),
                     config(source('other', '/local/feed'), closed=True)):
            report = self.scan(files, configs=(text,), witnesses=(('a/Witness.csproj','witness.json'),))
            self.assertEqual(report.unmeasurable[0].reason, 'nuget_comparator_private')
            self.assertEqual((self.calls, self.urls), ([], []))
