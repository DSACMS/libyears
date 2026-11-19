"""Accepted managed versions are static Declared facts, never selected evidence."""

from copy import deepcopy
from dataclasses import replace, FrozenInstanceError
import json
import unittest
from unittest.mock import patch

from libyears.maven_management import apply_management, decode_management
from libyears.maven_model import (
    MavenOccurrenceKey, MavenReason, MavenVersionBasis, MavenVersionFact,
)
from libyears.maven_project import declared_sources
from test_maven_management import engine, envelope, fixture, imported, parent
from test_maven_project import dependency, dependencies, management, pom


def version_fixture(*, ordinary_fields='<scope>test</scope>', managed_fields='<version>2</version>',
                    body='', parent_body='', external=None):
    return fixture(body, parent_body + management(dependency('a', managed_fields, group='g')),
                   ordinary=dependency('a', ordinary_fields, group='g'), external=external)


def applied(local, external, supplied=None):
    from libyears.maven_input import MavenInputSnapshot, parse_pom
    from libyears.maven_model import MavenDiscovery
    from libyears.maven_project import build_project_graph
    snapshots = {s: MavenInputSnapshot(s, raw, (), parse_pom(raw)) for s, raw in local.items()}
    graph = build_project_graph(MavenDiscovery(True, tuple(local)), snapshots.__getitem__)
    sources = declared_sources(graph)
    accepted = decode_management(json.dumps(supplied or envelope(local, external)).encode())
    return sources, apply_management(graph, sources, accepted)


class ManagedVersionProofTests(unittest.TestCase):
    def proof(self, local, external, **kwargs):
        proofs, rows = engine(local, external, **kwargs)
        return proofs.version(rows[0])

    def test_absent_version_uses_exact_managed_fact_and_preserves_ordinary_request(self):
        local, external = version_fixture()
        before, after = applied(local, external)
        old = before[0].declared.rows[0]
        row = after[0].declared.rows[0]
        self.assertEqual((row.key, row.scope, row.optional), (old.key, 'test', False))
        self.assertEqual(row.declared.version, '2')
        self.assertIsNone(row.declared.request)
        self.assertEqual(row.declared.origins, old.declared.origins)
        self.assertEqual(row.version_management_status, 'accepted')
        evidence = row.declared.managed_version
        self.assertEqual(evidence.document_gav, ('p', 'parent', '1'))
        self.assertIsNone(evidence.source_id)
        self.assertEqual(evidence.local_sources, ('pom.xml',))
        self.assertIn(evidence.document_gav, evidence.external_gavs)
        self.assertEqual(row.declared.reason, MavenReason.TIME_BASIS_UNAVAILABLE)
        self.assertIsNone(row.observed)
        self.assertEqual(before[0].declared.population_count, after[0].declared.population_count)
        self.assertEqual(after[0].observed, before[0].observed)

    def test_existing_exact_ordinary_version_never_changes(self):
        for fields in ('<version>1</version><scope>test</scope>',
                       '<version>${v}</version><scope>test</scope>'):
            local, external = version_fixture(ordinary_fields=fields, body='<properties><v>1</v></properties>')
            before, after = applied(local, external)
            self.assertEqual(after[0].declared.rows[0].declared, before[0].declared.rows[0].declared)
            self.assertIsNone(after[0].declared.rows[0].version_management_status)
            self.assertIsNone(self.proof(local, external))

    def test_present_unusable_versions_are_not_absence(self):
        values = ('', ' ', '${missing}', '[1,3)', 'LATEST', 'RELEASE', '1-SNAPSHOT',
                  'https://invalid.example/version', '${env.VERSION}')
        for value in values:
            with self.subTest(value=value):
                local, external = version_fixture(ordinary_fields=f'<version>{value}</version><scope>test</scope>')
                self.assertIsNone(self.proof(local, external))
                before, after = applied(local, external)
                self.assertEqual(after[0].declared.rows[0].declared, before[0].declared.rows[0].declared)
        for malformed in ('<version><nested/></version>', '<version>1</version><version>2</version>'):
            local, external = version_fixture(ordinary_fields=malformed + '<scope>test</scope>')
            before, after = applied(local, external)
            self.assertEqual(before, after)  # No row can be invented from a blocked key.

    def test_managed_exact_rules_and_no_alternate_version_fallback(self):
        for text, expected in (('2', '2'), ('[2]', '2'), ('2-rc1', '2-rc1'),
                               ('[1,3)', None), ('', None), ('LATEST', None),
                               ('2-SNAPSHOT', None), ('${missing}', None)):
            with self.subTest(text=text):
                local, external = version_fixture(managed_fields=f'<version>{text}</version>')
                proof = self.proof(local, external)
                self.assertEqual(proof.version if proof else None, expected)

    def test_whole_winning_key_missing_or_bad_version_shields_parent_and_imports(self):
        for nearer in ('', '<version>${missing}</version>'):
            local, external = version_fixture(body=management(dependency('a', nearer, group='g') + imported('missing')))
            self.assertIsNone(self.proof(local, external))

    def test_ordered_boms_first_winner_and_unknown_earlier_refusal(self):
        first = pom(management(dependency('a', '<version>3</version>', group='g')), group='p', artifact='first')
        second = pom(management(dependency('a', '<version>4</version>', group='g')), group='p', artifact='second')
        for imports, expected in ((imported('first') + imported('second'), '3'),
                                  (imported('second') + imported('first'), '4'),
                                  (imported('missing') + imported('first'), None),
                                  (imported('first') + imported('missing'), '3')):
            local, external = fixture(management(imports), external={'first': first, 'second': second},
                                      ordinary=dependency('a', '<scope>test</scope>', group='g'))
            proof = self.proof(local, external)
            self.assertEqual(proof.version if proof else None, expected)
        first = pom(management(dependency('a', group='g')), group='p', artifact='first')
        local, external = fixture(management(imported('first') + imported('second')),
                                  external={'first': first, 'second': second},
                                  ordinary=dependency('a', '<scope>test</scope>', group='g'))
        self.assertIsNone(self.proof(local, external))

    def test_parent_properties_use_consumer_bom_properties_use_bom(self):
        local, external = version_fixture(body='<properties><v>3</v></properties>',
            parent_body='<properties><v>2</v></properties>', managed_fields='<version>${v}</version>')
        self.assertEqual(self.proof(local, external).version, '3')
        bom = pom('<properties><v>4</v></properties>' + management(dependency('a', '<version>${v}</version>', group='g')),
                  group='p', artifact='bom')
        local, external = fixture('<properties><v>3</v></properties>' + management(imported('bom')),
                                  ordinary=dependency('a', '<scope>test</scope>', group='g'), external={'bom': bom})
        proof = self.proof(local, external)
        self.assertEqual((proof.version, proof.evidence.request), ('4', '${v}'))
        self.assertEqual(proof.evidence.document_gav, ('p', 'bom', '1'))

    def test_wrong_bytes_role_identity_context_and_ungranted_key_refuse(self):
        local, external = version_fixture()
        data = envelope(local, external)
        for kind in ('binding', 'role', 'key'):
            supplied = deepcopy(data)
            if kind == 'binding':
                supplied['consumers'][0]['bindings']['pom.xml'] = '0' * 64
            elif kind == 'role':
                supplied['documents'][0]['roles'] = ['bom']
            else:
                supplied['consumers'][0]['keys'][0]['artifact_id'] = 'other'
            self.assertIsNone(self.proof(local, external, supplied=supplied), kind)
        changed = {'pom.xml': local['pom.xml'].replace(b'<artifactId>parent</artifactId>', b'<artifactId>absent</artifactId>')}
        self.assertIsNone(self.proof(changed, external))
        proofs, rows = engine(local, external)
        row = rows[0]
        for bad in (replace(row, key=MavenOccurrenceKey('pom.xml', 'other', row.key.model_key)),
                    replace(row, optional=None), replace(row, artifact_key=None),
                    replace(row, declared=replace(row.declared, reason=MavenReason.UNSUPPORTED_MODEL))):
            self.assertIsNone(proofs.version(bad))
            self.assertEqual(proofs.version(row).version, '2')

    def test_type_classifier_and_ordinary_collisions_never_join(self):
        for fields in ('<type>test-jar</type>', '<classifier>tests</classifier>'):
            local, external = version_fixture(managed_fields='<version>2</version>' + fields)
            self.assertIsNone(self.proof(local, external))
        local, external = version_fixture(parent_body=dependencies(dependency('a', '<version>3</version>', group='g')))
        self.assertIsNone(self.proof(local, external))

    def test_same_coordinate_consumers_verify_their_own_bindings_and_keep_siblings(self):
        local, external = version_fixture()
        local['pom.xml'] = pom(parent() + '<modules><module>one</module><module>two</module></modules>',
                               group='c', artifact='consumer')
        for name in ('one', 'two'):
            local[name + '/pom.xml'] = pom(
                '<parent><groupId>c</groupId><artifactId>consumer</artifactId><version>1</version></parent>'
                + dependencies(dependency('a', '<scope>test</scope>', group='g')
                               + dependency('safe', '<version>1</version><scope>test</scope>', group='g')),
                group='c', artifact=name)
        data = envelope(local, external)
        template = data['consumers'][0]
        data['consumers'] = []
        for name in ('one', 'two'):
            grant = deepcopy(template)
            grant['source_id'] = name + '/pom.xml'
            grant['bindings'] = {s: h for s, h in grant['bindings'].items()
                                 if s in ('pom.xml', grant['source_id'])}
            if name == 'one':
                grant['bindings'][grant['source_id']] = '0' * 64
            data['consumers'].append(grant)
        before, after = applied(local, external, data)
        old = {r.key: r for s in before for r in s.declared.rows}
        new = {r.key: r for s in after for r in s.declared.rows}
        self.assertEqual(old.keys(), new.keys())
        for key, row in new.items():
            if key.model_key.artifact_id == 'safe':
                self.assertEqual(row, old[key])
            elif key.source_id == 'one/pom.xml':
                self.assertIsNone(row.declared.version)
            else:
                self.assertEqual(row.declared.version, '2')

    def test_blocked_keys_profiles_cycles_and_budgets_keep_safe_sibling(self):
        bad_records = (dependency('a', '<version>2</version>', group='g') * 2,
                       dependency('a', '<version>2</version><unknown/>', group='g'))
        for bad in bad_records:
            local, external = version_fixture(body=management(bad))
            self.assertIsNone(self.proof(local, external))
        for body in ('<properties><v>3</v></properties>', management(dependency('a', '<version>3</version>', group='g')),
                     dependencies(dependency('a', '<version>3</version>', group='g'))):
            local, external = version_fixture(parent_body='<profiles><profile><id>x</id>' + body + '</profile></profiles>')
            self.assertIsNone(self.proof(local, external))
        local, external = version_fixture(parent_body=parent())
        self.assertIsNone(self.proof(local, external))
        local, external = version_fixture()
        for constant in ('MAX_BUILDS', 'MAX_TOTAL_BUILDS'):
            with patch('libyears.maven_management.' + constant, 1):
                self.assertIsNone(self.proof(local, external))
        proofs, rows = engine(local, external)
        row = rows[0]
        bad = replace(row, key=replace(row.key, model_key=replace(row.key.model_key, classifier='tests')))
        self.assertIsNone(proofs.version(bad))
        self.assertEqual(proofs.version(row).version, '2')

    def test_version_and_scope_are_independent_and_share_per_occurrence_budget(self):
        local, external = version_fixture(ordinary_fields='')
        before, after = applied(local, external)
        row = after[0].declared.rows[0]
        self.assertEqual((row.declared.version, row.scope, row.management_status), ('2', 'compile', 'accepted'))
        self.assertIsNone(row.observed)
        local, external = version_fixture(ordinary_fields='<scope>${missing}</scope>')
        before, after = applied(local, external)
        row = after[0].declared.rows[0]
        self.assertEqual(row.declared.version, '2')
        self.assertIsNone(row.scope)
        self.assertEqual(row.declared.reason, MavenReason.UNSUPPORTED_MODEL)
        self.assertEqual(row.management_status, 'refused')
        local, external = version_fixture(ordinary_fields='')
        with patch('libyears.maven_management.MAX_BUILDS', 4):
            unused, after = applied(local, external)
        row = after[0].declared.rows[0]
        self.assertEqual(row.declared.version, '2')
        self.assertIsNone(row.scope)  # Version used four builds; scope cannot reset its budget.

    def test_conflicting_established_scope_refuses_and_parent_policy_preserves_facts(self):
        local, external = version_fixture()
        proofs, rows = engine(local, external)
        self.assertIsNone(proofs.version(replace(rows[0], scope='runtime')))
        local, external = version_fixture(body=management(dependency('a', '<version>2</version><scope>test</scope>', group='g')),
                                           ordinary_fields='')
        proofs, rows = engine(local, external)
        self.assertIsNone(proofs.version(replace(rows[0], scope='runtime')))
        local, external = version_fixture(ordinary_fields='', parent_body='<repositories/>')
        unused, after = applied(local, external)
        row = after[0].declared.rows[0]
        self.assertEqual((row.declared.version, row.scope, row.declared.reason), ('2', 'compile', MavenReason.POLICY_UNKNOWN))
        self.assertIsNotNone(row.declared.managed_version)

    def test_evidence_is_immutable_and_cannot_be_attached_to_observed_or_unknown_version(self):
        local, external = version_fixture()
        evidence = self.proof(local, external).evidence
        with self.assertRaises(FrozenInstanceError):
            evidence.request = 'changed'
        for basis, version in ((MavenVersionBasis.OBSERVED, '2'), (MavenVersionBasis.DECLARED, None)):
            with self.assertRaises(ValueError):
                MavenVersionFact(basis, version=version, managed_version=evidence, reason=MavenReason.UNSUPPORTED_MODEL)
        with self.assertRaises(ValueError):
            replace(evidence, local_sources=[])
        with self.assertRaises(ValueError):
            replace(evidence, document_gav=None)


class ManagedVersionIntegrationTests(unittest.TestCase):
    def scan(self, local, external, *, metadata=None, accepted=True):
        from libyears.maven import scan_maven
        from test_maven_scan import Reader, Metadata
        kwargs = {}
        if accepted:
            kwargs['management'] = decode_management(json.dumps(envelope(local, external)).encode())
        metadata = metadata or Metadata()
        report = scan_maven('fixture', reader_factory=lambda root: Reader(local),
                            supervisor_factory=metadata, **kwargs)
        return report, metadata

    def test_json_and_verbose_identify_origin_after_each_metadata_failure(self):
        from libyears.maven_output import maven_human_lines, maven_to_dict
        from test_maven_scan import Metadata
        for metadata, reason in (
                (Metadata(targets={'a': MavenReason.CATALOGUE_UNAVAILABLE}), MavenReason.CATALOGUE_UNAVAILABLE),
                (Metadata(targets={'a': MavenReason.METADATA_WORKER_UNAVAILABLE}), MavenReason.METADATA_WORKER_UNAVAILABLE),
                (Metadata(dates={('a', '2'): MavenReason.TIME_BASIS_UNAVAILABLE}), MavenReason.TIME_BASIS_UNAVAILABLE)):
            with self.subTest(reason=reason):
                local, external = version_fixture()
                report, unused = self.scan(local, external, metadata=metadata)
                row = maven_to_dict(report)['occurrences'][0]
                self.assertEqual((row['declared']['version'], row['declared']['reason']), ('2', reason.value))
                self.assertIsNone(row['declared']['request'])
                self.assertEqual(row['declared']['version_basis'], MavenVersionBasis.DECLARED.value)
                self.assertEqual(row['version_management_status'], 'accepted')
                self.assertEqual(row['management_status'], 'refused')  # Scope was already known.
                self.assertIsNone(row['scope_basis'])
                evidence = row['declared']['managed_version']
                self.assertEqual(evidence['document_gav'], ['p', 'parent', '1'])
                self.assertEqual(evidence['local_sources'], ['pom.xml'])
                self.assertEqual(evidence['request'], '2')
                self.assertIn('byte_bindings_verified', evidence['applicability'])
                verbose = '\n'.join(maven_human_lines(report, verbose=True))
                self.assertIn('managed_version:', verbose)
                self.assertIn('"document_gav": ["p", "parent", "1"]', verbose)
                ordinary = '\n'.join(maven_human_lines(report))
                self.assertIn('Unmeasurable', ordinary)
                self.assertIn('version: 2', ordinary)
                self.assertIn('static field evidence', ordinary)
                for forbidden in ('content_base64', 'sha256', '_external/', 'evidence.json'):
                    self.assertNotIn(forbidden, verbose)
                    self.assertNotIn(forbidden, json.dumps(row))

    def test_parent_policy_refusal_preserves_version_evidence_without_http(self):
        from libyears.maven_output import maven_to_dict
        local, external = version_fixture(parent_body='<repositories/>')
        report, metadata = self.scan(local, external)
        row = maven_to_dict(report)['occurrences'][0]
        self.assertEqual(row['declared']['reason'], MavenReason.POLICY_UNKNOWN.value)
        self.assertEqual(row['declared']['managed_version']['document_gav'], ['p', 'parent', '1'])
        self.assertEqual(metadata.calls, [])

    def test_paired_observed_occurrence_cannot_hide_declared_managed_status(self):
        from libyears.maven_output import maven_to_dict, maven_human_lines
        from libyears.maven_results import summarize_sources
        local, external = version_fixture()
        report, unused = self.scan(local, external)
        source = report.sources[0]
        declared = source.declared.rows[0]
        observed = replace(declared, declared=None,
                           observed=MavenVersionFact(MavenVersionBasis.OBSERVED, version='9',
                                                     reason=MavenReason.CATALOGUE_UNAVAILABLE),
                           management_status=None, version_management_status=None)
        source = replace(source, observed=replace(source.observed, rows=(observed,), accepted=True, reason=None))
        report = replace(report, sources=(source,), summaries=summarize_sources((source,)))
        row = maven_to_dict(report)['occurrences'][0]
        self.assertEqual((row['declared']['version'], row['observed']['version']), ('2', '9'))
        self.assertEqual(row['version_management_status'], 'accepted')
        self.assertEqual(row['management_status'], 'refused')
        text = '\n'.join(maven_human_lines(report))
        self.assertIn('static field evidence', text)
        self.assertIn('Observed: 9 /', text)

    def test_existing_versions_scopes_safe_measurements_and_view_statistics_survive(self):
        from libyears.maven_output import maven_human_lines, maven_to_dict
        local, external = version_fixture()
        safe = dependency('safe', '<version>1</version><scope>test</scope>', group='g').encode()
        local['pom.xml'] = local['pom.xml'].replace(b'</dependencies>', safe + b'</dependencies>')
        before, unused = self.scan(local, external, accepted=False)
        after, unused = self.scan(local, external)
        old = {r['key']['artifact_id']: r for r in maven_to_dict(before)['occurrences']}
        data = maven_to_dict(after)
        new = {r['key']['artifact_id']: r for r in data['occurrences']}
        self.assertEqual(old.keys(), new.keys())
        self.assertEqual(old['safe'], new['safe'])
        self.assertEqual(new['a']['scope'], old['a']['scope'])
        self.assertEqual(new['a']['declared']['age']['libyears'], 0.0)
        self.assertEqual(data['views']['declared']['summary']['dependencies_measured'], 2)
        self.assertIsNone(data['views']['declared']['summary']['dependencies_discovered'])
        self.assertIsNone(data['views']['declared']['summary']['coverage'])
        self.assertEqual(data['views']['observed'], maven_to_dict(before)['views']['observed'])
        self.assertTrue(all(r['observed'] is None for r in data['occurrences']))
        self.assertIn('MODULE', '\n'.join(maven_human_lines(after)))
        self.assertNotIn('managed_version', old['safe']['declared'])
        self.assertNotIn('version_management_status', old['safe'])

    def test_real_cli_displays_managed_origin_and_keeps_found_failures(self):
        import contextlib
        import io
        from pathlib import Path
        import tempfile
        from libyears.cli import main
        from libyears.maven_input import filesystem_available
        from test_maven_scan import Metadata
        if not filesystem_available():
            self.skipTest('safe filesystem primitives unavailable')
        local, external = version_fixture()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / 'pom.xml').write_bytes(local['pom.xml'])
            evidence = root / 'accepted.json'
            evidence.write_text(json.dumps(envelope(local, external)))
            for option in ('--json', '--verbose', ''):
                output, error = io.StringIO(), io.StringIO()
                args = [str(root), '--maven-management', str(evidence)] + ([option] if option else [])
                with patch('libyears.maven_supervisor.MavenSupervisor', Metadata(targets={'a': MavenReason.CATALOGUE_UNAVAILABLE})), \
                        contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
                    self.assertEqual(main(args), 0)
                self.assertEqual(error.getvalue(), '')
                if option == '--json':
                    row = json.loads(output.getvalue())['maven']['occurrences'][0]
                    self.assertEqual(row['declared']['managed_version']['request'], '2')
                    self.assertEqual(row['declared']['version'], '2')
                elif option == '--verbose':
                    self.assertIn('managed_version:', output.getvalue())
                else:
                    self.assertIn('Unmeasurable', output.getvalue())
                    self.assertIn('version: 2', output.getvalue())
