"""Explicit static scope evidence: field applicability never grants HTTP."""

import base64
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from libyears.maven_input import MavenInputSnapshot, filesystem_available, parse_pom
from libyears.maven_management import (
    BASIS, ManagementProofs, MavenManagementRequestError, decode_management, load_management,
)
from libyears.maven_model import MavenDiscovery
from libyears.maven_project import build_project_graph, declared_sources
from test_maven_project import pom, dependency, dependencies, management


def parent(artifact='parent', version='1'):
    return f'<parent><groupId>p</groupId><artifactId>{artifact}</artifactId><version>{version}</version><relativePath/></parent>'


def imported(artifact, version='1'):
    return dependency(artifact, f'<version>{version}</version><type>pom</type><scope>import</scope>', group='p')


def envelope(local, external, *, keys=None):
    documents = []
    for artifact, raw in external.items():
        documents.append({'gav': ['p', artifact, '1'], 'roles': ['parent', 'bom'],
                          'sha256': hashlib.sha256(raw).hexdigest(),
                          'content_base64': base64.b64encode(raw).decode()})
    key = {'group_id': 'g', 'artifact_id': 'a', 'type': 'jar', 'classifier': None}
    return {'schema_version': 1, 'basis': BASIS, 'documents': documents,
            'consumers': [{'source_id': 'pom.xml', 'context_id': 'base_model',
                           'bindings': {s: hashlib.sha256(raw).hexdigest() for s, raw in local.items()},
                           'keys': keys or [key]}]}


def fixture(body='', parent_body='', *, external=None, ordinary=None):
    ordinary = ordinary if ordinary is not None else dependency('a', '<version>1</version>', group='g')
    local = {'pom.xml': pom(parent() + body + dependencies(ordinary), group='c', artifact='consumer')}
    external = dict(external or {})
    external['parent'] = pom(parent_body, group='p', artifact='parent')
    return local, external


def engine(local, external, *, supplied=None):
    snapshots = {s: MavenInputSnapshot(s, raw, (), parse_pom(raw)) for s, raw in local.items()}
    graph = build_project_graph(MavenDiscovery(True, tuple(local)), snapshots.__getitem__)
    accepted = decode_management(json.dumps(supplied or envelope(local, external)).encode())
    proofs = ManagementProofs(graph, accepted)
    rows = [r for source in declared_sources(graph) for r in source.declared.rows]
    return proofs, rows


class ManagementCompositionTests(unittest.TestCase):
    def scope(self, local, external, **kwargs):
        proofs, rows = engine(local, external, **kwargs)
        return proofs.scope(rows[0])

    def test_whole_entry_shields_omitted_scope_from_losing_and_unread_imports(self):
        local, ext = fixture(management(imported('missing')), management(dependency('a', group='g')))
        self.assertEqual(self.scope(local, ext).scope, 'compile')
        # Child entry wins over the complete parent's same key, without field fill.
        local, ext = fixture(management(dependency('a', group='g') + imported('missing')),
                             management(dependency('a', '<scope>test</scope>', group='g')))
        self.assertEqual(self.scope(local, ext).scope, 'compile')

    def test_ordered_imports_first_whole_key_wins_and_unknown_earlier_blocks(self):
        ext = {'first': pom(management(dependency('a', group='g')), group='p', artifact='first'),
               'later': pom(management(dependency('a', '<scope>test</scope>', group='g')), group='p', artifact='later')}
        local, ext = fixture(management(imported('first') + imported('later')), external=ext)
        self.assertEqual(self.scope(local, ext).scope, 'compile')
        local2 = {'pom.xml': local['pom.xml'].replace(b'<artifactId>first</artifactId>', b'<artifactId>missing</artifactId>')}
        self.assertIsNone(self.scope(local2, ext))
        # Use an explicit reversed declaration; no cached same-GA bypass.
        local3, ext = fixture(management(imported('later') + imported('first')), external=ext)
        self.assertEqual(self.scope(local3, ext).scope, 'test')

    def test_parent_raw_interpolation_and_independent_bom_context(self):
        local, ext = fixture('<properties><s>test</s></properties>',
                             '<properties><s>runtime</s></properties>' + management(dependency('a', '<scope>${s}</scope>', group='g')))
        self.assertEqual(self.scope(local, ext).scope, 'test')
        bom = pom('<properties><s>runtime</s></properties>' + management(dependency('a', '<scope>${s}</scope>', group='g')), group='p', artifact='bom')
        local, ext = fixture('<properties><s>test</s></properties>' + management(imported('bom')), external={'bom': bom})
        self.assertEqual(self.scope(local, ext).scope, 'runtime')

    def test_exact_type_classifier_no_alias_and_unknown_prevents_default(self):
        for fields in ('<type>test-jar</type>', '<classifier>tests</classifier>'):
            local, ext = fixture(management(imported('missing')), management(dependency('a', fields, group='g')))
            self.assertIsNone(self.scope(local, ext))

    def test_complete_empty_management_can_default_but_missing_parent_cannot(self):
        local, ext = fixture()
        self.assertEqual(self.scope(local, ext).scope, 'compile')
        ext['parent'] = pom(parent('missing'), group='p', artifact='parent')
        self.assertIsNone(self.scope(local, ext))

    def test_binding_mismatch_missing_role_and_wrong_parent_refuse(self):
        local, ext = fixture(parent_body=management(dependency('a', group='g')))
        data = envelope(local, ext)
        for mutate in ('binding', 'role', 'gav'):
            supplied = deepcopy(data)
            if mutate == 'binding':
                supplied['consumers'][0]['bindings']['pom.xml'] = '0' * 64
            elif mutate == 'role':
                supplied['documents'][0]['roles'] = ['bom']
            else:
                changed = local['pom.xml'].replace(b'<artifactId>parent</artifactId>', b'<artifactId>unknown</artifactId>')
                local = {'pom.xml': changed}
                supplied['consumers'][0]['bindings']['pom.xml'] = hashlib.sha256(changed).hexdigest()
            self.assertIsNone(self.scope(local, ext, supplied=supplied), mutate)

    def test_duplicate_unsupported_winner_and_profiles_refuse_without_parent_fallback(self):
        for bad in (dependency('a', group='g') * 2,
                    dependency('a', '<scope>${missing}</scope>', group='g'),
                    dependency('a', '<unknown/>', group='g')):
            local, ext = fixture(management(bad), management(dependency('a', '<scope>test</scope>', group='g')))
            self.assertIsNone(self.scope(local, ext))
        for body in ('<properties><s>test</s></properties>', management(dependency('a', group='g')),
                     dependencies(dependency('a', group='g')), '<unknown/>'):
            local, ext = fixture(parent_body=management(dependency('a', group='g')) + '<profiles><profile><id>x</id>' + body + '</profile></profiles>')
            self.assertIsNone(self.scope(local, ext))

    def test_known_unrelated_profile_dependency_does_not_poison_field(self):
        profile = '<profiles><profile><id>x</id>' + dependencies(dependency('other', '<scope>test</scope>', group='g')) + '</profile></profiles>'
        local, ext = fixture(parent_body=management(dependency('a', group='g')) + profile)
        self.assertEqual(self.scope(local, ext).scope, 'compile')

    def test_ordinary_collision_cannot_fill_or_fall_back(self):
        local, ext = fixture(parent_body=dependencies(dependency('a', '<scope>test</scope>', group='g')) + management(dependency('a', group='g')))
        self.assertIsNone(self.scope(local, ext))

    def test_parent_and_import_cycles_and_resource_limits_refuse(self):
        local, ext = fixture(parent_body=parent())
        self.assertIsNone(self.scope(local, ext))
        local, ext = fixture(management(imported('bom')), external={'bom': pom(management(imported('bom')), group='p', artifact='bom')})
        self.assertIsNone(self.scope(local, ext))
        local, ext = fixture(parent_body=management(dependency('a', group='g')))
        with patch('libyears.maven_management.MAX_BUILDS', 1):
            self.assertIsNone(self.scope(local, ext))
        with patch('libyears.maven_management.MAX_TOTAL_BUILDS', 1):
            self.assertIsNone(self.scope(local, ext))

    def test_external_parent_policy_veto_is_separate_from_scope_and_bom_policy(self):
        repository = '<repositories><repository><id>central</id></repository></repositories>'
        local, ext = fixture(parent_body=repository + management(dependency('a', group='g')))
        proof = self.scope(local, ext)
        self.assertEqual(proof.scope, 'compile')
        self.assertFalse(proof.comparison_allowed)
        local, ext = fixture(management(imported('bom')), external={'bom': pom(repository + management(dependency('a', group='g')), group='p', artifact='bom')})
        self.assertTrue(self.scope(local, ext).comparison_allowed)

    def test_proof_boundary_refuses_ineligible_rows_without_poisoning_eligible_sibling(self):
        from libyears.maven_model import MavenOccurrenceKey, MavenReason
        local, ext = fixture(parent_body=management(dependency('a', group='g')))
        proofs, rows = engine(local, ext)
        row = rows[0]
        for refused in (
                replace(row, key=replace(row.key, model_key=replace(row.key.model_key, artifact_id='different')),
                        artifact_key=None),
                replace(row, key=MavenOccurrenceKey('pom.xml', 'other_context', row.key.model_key)),
                replace(row, optional=None), replace(row, scope='test'),
                replace(row, artifact_key=None),
                replace(row, declared=replace(row.declared, reason=MavenReason.UNSUPPORTED_VERSION))):
            self.assertIsNone(proofs.scope(refused))
            self.assertEqual(proofs.scope(row).scope, 'compile')
        supplied = envelope(local, ext)
        supplied['consumers'][0]['keys'][0]['artifact_id'] = 'different'
        proofs, rows = engine(local, ext, supplied=supplied)
        self.assertFalse(proofs.requested(rows[0]))
        self.assertIsNone(proofs.scope(rows[0]))

    def test_changed_version_refuses_and_no_observed_fact_is_created(self):
        local, ext = fixture(parent_body=management(dependency('a', group='g')))
        proofs, rows = engine(local, ext)
        self.assertIsNone(rows[0].observed)
        self.assertIsNone(proofs.scope(replace(rows[0], declared=replace(rows[0].declared, version='99'))))
        self.assertIsNone(rows[0].observed)


class ManagementEnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.local, self.external = fixture()
        self.value = envelope(self.local, self.external)

    def refuse(self, value):
        with self.assertRaisesRegex(MavenManagementRequestError, '^invalid Maven management evidence$'):
            decode_management(json.dumps(value).encode())

    def test_strict_schema_types_digests_base64_and_identity(self):
        for key, bad in (('schema_version', True), ('documents', {}), ('consumers', None), ('basis', 'other')):
            value = deepcopy(self.value); value[key] = bad
            self.refuse(value)
        for key, bad in (('sha256', 'A' * 64), ('content_base64', '%%%'), ('gav', ['p', 'wrong', '1']), ('roles', ['parent', 'parent'])):
            value = deepcopy(self.value); value['documents'][0][key] = bad
            self.refuse(value)
        value = deepcopy(self.value); value['consumers'].append(value['consumers'][0]); self.refuse(value)
        value = deepcopy(self.value); value['documents'].append(value['documents'][0]); self.refuse(value)

    def test_duplicate_json_members_nested_depth_utf8_and_limits(self):
        for raw in (b'{"schema_version":1,"schema_version":1}', b'{"a":{"b":1,"b":2}}',
                    b'[' * 17 + b']' * 17, b'\xff', b'{"a":NaN}', b' ' * (4 * 1024 * 1024 + 1)):
            with self.assertRaises(MavenManagementRequestError):
                decode_management(raw)

    def test_unsafe_or_dtd_document_and_unknown_members_refuse(self):
        for raw in (b'<!DOCTYPE project><project/>', b'<project/>'):
            value = deepcopy(self.value); document = value['documents'][0]
            document['content_base64'] = base64.b64encode(raw).decode(); document['sha256'] = hashlib.sha256(raw).hexdigest()
            self.refuse(value)
        value = deepcopy(self.value); value['origin'] = 'ignored'; self.refuse(value)

    @unittest.skipUnless(filesystem_available(), 'safe filesystem primitives unavailable')
    def test_selected_envelope_regular_symlink_fifo_and_changed_file(self):
        import os
        with tempfile.TemporaryDirectory() as temporary:
            # macOS temporary aliases are resolved only by this test fixture.
            root = Path(temporary).resolve(); selected = root / 'accepted.json'
            selected.write_text(json.dumps(self.value))
            self.assertEqual(len(load_management(selected).documents), 1)
            alias = root / 'alias.json'; alias.symlink_to(selected)
            with self.assertRaises(MavenManagementRequestError):
                load_management(alias)
            fifo = root / 'fifo.json'; os.mkfifo(fifo)
            with self.assertRaises(MavenManagementRequestError):
                load_management(fifo)
            from libyears.maven_input import MavenInputReader, MavenInputFailure, MavenInputIssue
            with patch.object(MavenInputReader, '_check_bindings', side_effect=MavenInputFailure(MavenInputIssue.CHANGED)):
                with self.assertRaises(MavenManagementRequestError):
                    load_management(selected)

    def test_missing_file_and_unavailable_safety_capabilities_refuse(self):
        with self.assertRaises(MavenManagementRequestError):
            load_management('/nonexistent-selected-envelope.json')
        with patch('libyears.maven_input.filesystem_available', return_value=False):
            with self.assertRaises(MavenManagementRequestError):
                load_management('accepted.json')
