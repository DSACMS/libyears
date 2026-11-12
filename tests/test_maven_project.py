"""T004 graph/raw-field fixtures; none establishes final external population."""

from dataclasses import FrozenInstanceError, fields
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.maven_input import (
    MavenInputFailure, MavenInputIssue, MavenInputReader, MavenInputSnapshot,
    filesystem_available, parse_pom,
)
from libyears.maven_model import MavenDiscovery, MavenFieldBasis, MavenModelKey, MavenReason
from libyears.maven_project import (
    ModelIssue, RawModel, artifact_for, build_project_graph,
)


def pom(body='', *, group='g', artifact='project', version='1'):
    identity = ''.join(f'<{name}>{value}</{name}>' for name, value in (
        ('groupId', group), ('artifactId', artifact), ('version', version),
    ) if value is not None)
    return ('<project><modelVersion>4.0.0</modelVersion>' + identity + body + '</project>').encode()


def dependency(artifact='library', extra='', *, group='external'):
    return (f'<dependency><groupId>{group}</groupId><artifactId>{artifact}</artifactId>'
            + extra + '</dependency>')


def dependencies(*entries):
    return '<dependencies>' + ''.join(entries) + '</dependencies>'


def management(*entries):
    return '<dependencyManagement>' + dependencies(*entries) + '</dependencyManagement>'


def parent(artifact='project', path=None, *, group='g', version='1'):
    relative = '' if path is None else f'<relativePath>{path}</relativePath>'
    return (f'<parent><groupId>{group}</groupId><artifactId>{artifact}</artifactId>'
            f'<version>{version}</version>{relative}</parent>')


def modules(*paths):
    return '<modules>' + ''.join('<module>' + path + '</module>' for path in paths) + '</modules>'


class MavenProjectTests(unittest.TestCase):
    def graph(self, documents, *, complete=True, reader=None):
        snapshots = {name: MavenInputSnapshot(name, data, ('fixture',), parse_pom(data))
                     for name, data in documents.items()}
        snapshot_reader = reader or Mock(side_effect=snapshots.__getitem__)
        discovery = MavenDiscovery(complete, tuple(sorted(documents)),
                                   None if complete else MavenReason.DISCOVERY_UNAVAILABLE)
        return build_project_graph(discovery, snapshot_reader)

    def model(self, graph, source='pom.xml'):
        return next(model for model in graph.models if model.context.source_id == source)

    def issues(self, model):
        return {problem.issue for problem in model.problems}

    def test_default_parent_and_literal_identity_inherit_from_accepted_chain(self):
        graph = self.graph({
            'pom.xml': pom(dependencies(dependency(extra='<version>1</version>'))),
            'child/pom.xml': pom(parent(), group=None, artifact='child', version=None),
        })
        child = self.model(graph, 'child/pom.xml')
        self.assertEqual(child.identity.gav, ('g', 'child', '1'))
        self.assertEqual(child.context.parent_sources, ('pom.xml',))
        self.assertTrue(child.parent_chain_complete)
        record = child.dependencies[0]
        self.assertEqual(record.consumer_source, 'child/pom.xml')
        self.assertEqual(record.declaration_source, 'pom.xml')
        self.assertEqual(record.field('version').origin.source_id, 'pom.xml')
        self.assertEqual(record.field('version').origin.basis, MavenFieldBasis.INHERITED_DEPENDENCY)

    def test_literal_file_and_directory_parent_paths(self):
        for path in ('../parent/pom.xml', '../parent'):
            with self.subTest(path=path):
                graph = self.graph({'parent/pom.xml': pom(),
                                    'child/pom.xml': pom(parent(path=path), artifact='child')})
                self.assertEqual(self.model(graph, 'child/pom.xml').context.parent_sources,
                                 ('parent/pom.xml',))

    def test_empty_parent_path_is_external_without_path_fallback(self):
        graph = self.graph({'pom.xml': pom(dependencies(dependency())),
                            'child/pom.xml': pom(parent(path=''), artifact='child')})
        child = self.model(graph, 'child/pom.xml')
        self.assertEqual(child.dependencies, ())
        self.assertEqual(child.context.parent_sources, ())
        self.assertFalse(child.parent_chain_complete)
        self.assertIn(ModelIssue.PARENT_EXTERNAL, self.issues(child))

    def test_missing_mismatched_escaping_and_dynamic_parent_keep_safe_local_rows(self):
        for reference, issue in (
            (parent(path='../missing/pom.xml'), ModelIssue.PARENT_MISSING),
            (parent(artifact='different'), ModelIssue.PARENT_MISMATCH),
            (parent(group='G'), ModelIssue.PARENT_MISMATCH),
            (parent(version='1.0'), ModelIssue.PARENT_MISMATCH),
            (parent(path='../../pom.xml'), ModelIssue.PARENT_PATH),
            (parent(path='${parentPath}'), ModelIssue.PARENT_PATH),
            (parent(path='https://example.invalid/pom.xml'), ModelIssue.PARENT_PATH),
        ):
            with self.subTest(reference=reference):
                graph = self.graph({'pom.xml': pom(dependencies(dependency('parent-only'))),
                                    'child/pom.xml': pom(reference + dependencies(dependency('local')),
                                                         artifact='child')})
                child = self.model(graph, 'child/pom.xml')
                self.assertIn(issue, self.issues(child))
                self.assertEqual([r.key.artifact_id for r in child.dependencies], ['local'])
                self.assertFalse(child.parent_chain_complete)

    def test_undiscovered_parent_is_never_read(self):
        data = pom(parent(path='../not-discovered/pom.xml'), artifact='child')
        reader = Mock(return_value=MavenInputSnapshot('child/pom.xml', data, (), parse_pom(data)))
        graph = self.graph({'child/pom.xml': data}, reader=reader)
        self.assertIn(ModelIssue.PARENT_MISSING, self.issues(self.model(graph, 'child/pom.xml')))
        reader.assert_called_once_with('child/pom.xml')

    def test_parent_cycle_and_self_reference_do_not_inherit_cyclic_rows(self):
        graph = self.graph({
            'a/pom.xml': pom(parent('b', '../b/pom.xml') + dependencies(dependency('a-only')), artifact='a'),
            'b/pom.xml': pom(parent('a', '../a/pom.xml') + dependencies(dependency('b-only')), artifact='b'),
        })
        for source in ('a/pom.xml', 'b/pom.xml'):
            model = self.model(graph, source)
            self.assertIn(ModelIssue.PARENT_CYCLE, self.issues(model))
            self.assertEqual(model.context.parent_sources, ())
            self.assertEqual(len(model.dependencies), 1)
            self.assertFalse(model.parent_chain_complete)
        model = self.model(self.graph({'pom.xml': pom(parent(path='pom.xml'))}))
        self.assertIn(ModelIssue.PARENT_CYCLE, self.issues(model))

    def test_parent_chain_16_allowed_17_refused(self):
        documents = {}
        for index in range(17):
            reference = '' if index == 0 else parent('p' + str(index - 1), f'../p{index-1}/pom.xml')
            documents[f'p{index}/pom.xml'] = pom(reference, artifact=f'p{index}')
        graph = self.graph(documents)
        model16 = self.model(graph, 'p15/pom.xml')
        self.assertTrue(model16.parent_chain_complete)
        self.assertEqual(len(model16.context.parent_sources), 15)
        model17 = self.model(graph, 'p16/pom.xml')
        self.assertFalse(model17.parent_chain_complete)
        self.assertIn(ModelIssue.PARENT_DEPTH, self.issues(model17))

    def test_partial_merge_one_consumer_record_and_no_early_scope_optional_defaults(self):
        graph = self.graph({
            'pom.xml': pom(dependencies(dependency(extra='<version>${v}</version><scope>test</scope>'))),
            'child/pom.xml': pom(parent() + dependencies(dependency(extra='<version>2</version>')),
                                 artifact='child'),
        })
        root = self.model(graph).dependencies[0]
        child = self.model(graph, 'child/pom.xml').dependencies[0]
        self.assertEqual(len(self.model(graph, 'child/pom.xml').dependencies), 1)
        self.assertEqual(root.field('version').value, '${v}')
        self.assertEqual(child.field('version').value, '2')
        self.assertEqual(child.field('version').origin.source_id, 'child/pom.xml')
        self.assertEqual(child.field('scope').value, 'test')
        self.assertEqual(child.field('scope').origin.source_id, 'pom.xml')
        self.assertIsNone(child.field('optional'))
        self.assertEqual(root.consumer_source, 'pom.xml')

    def test_management_merges_raw_fields_but_never_supplies_dependency_facts(self):
        graph = self.graph({
            'pom.xml': pom(management(dependency(extra='<version>1</version><optional>true</optional>'))),
            'child/pom.xml': pom(parent() + management(dependency(extra='<scope>test</scope>'))
                                 + dependencies(dependency()), artifact='child'),
        })
        child = self.model(graph, 'child/pom.xml')
        self.assertEqual(child.dependencies[0].fields, ())
        managed = child.management[0]
        self.assertEqual(managed.field('version').value, '1')
        self.assertEqual(managed.field('version').origin.basis, MavenFieldBasis.INHERITED_MANAGEMENT)
        self.assertEqual(managed.field('scope').origin.basis, MavenFieldBasis.CONSUMER_MANAGEMENT)
        self.assertEqual(managed.field('optional').value, 'true')
        self.assertEqual(self.model(graph).dependencies, ())

    def test_explicit_empty_field_does_not_inherit_or_default(self):
        graph = self.graph({'pom.xml': pom(dependencies(dependency(extra='<version>1</version>'))),
                            'child/pom.xml': pom(parent() + dependencies(dependency(extra='<version/>')),
                                                 artifact='child')})
        self.assertEqual(self.model(graph, 'child/pom.xml').dependencies[0].field('version').value, '')

    def test_same_key_duplicates_are_ambiguous_even_when_only_scope_or_version_differs(self):
        for second in ('<version>2</version>', '<scope>test</scope>', ''):
            graph = self.graph({'pom.xml': pom(dependencies(
                dependency(extra='<version>1</version>'), dependency(extra=second)))})
            model = self.model(graph)
            self.assertEqual(model.dependencies, ())
            self.assertIn(ModelIssue.DUPLICATE, self.issues(model))
            self.assertEqual(len(model.ambiguous_dependencies), 1)

    def test_child_ambiguous_key_cannot_fall_back_to_parent(self):
        graph = self.graph({'pom.xml': pom(dependencies(dependency())),
                            'child/pom.xml': pom(parent() + dependencies(dependency(), dependency()),
                                                 artifact='child')})
        self.assertEqual(self.model(graph, 'child/pom.xml').dependencies, ())

    def test_malformed_known_child_field_cannot_inherit_a_convenient_parent_value(self):
        graph = self.graph({'pom.xml': pom(dependencies(dependency(extra='<version>1</version>'))),
                            'child/pom.xml': pom(parent() + dependencies(dependency(
                                extra='<version>2</version><version>3</version>')), artifact='child')})
        child = self.model(graph, 'child/pom.xml')
        self.assertEqual(child.dependencies, ())
        self.assertIn(ModelIssue.STRUCTURE, self.issues(child))

    def test_model_key_aliases_stay_distinct_during_inheritance_and_management(self):
        graph = self.graph({
            'pom.xml': pom(dependencies(dependency(extra='<type>test-jar</type><version>1</version>'))
                           + management(dependency(extra='<type>jar</type><classifier>tests</classifier><version>9</version>'))),
            'child/pom.xml': pom(parent() + dependencies(dependency(extra='<classifier>tests</classifier>')),
                                 artifact='child'),
        })
        child = self.model(graph, 'child/pom.xml')
        self.assertEqual(len(child.dependencies), 2)
        self.assertNotEqual(child.dependencies[0].key, child.dependencies[1].key)
        self.assertEqual(child.dependencies[0].artifact_key, child.dependencies[1].artifact_key)
        self.assertIsNone(child.dependencies[1].field('version'))
        graph = self.graph({'pom.xml': pom(dependencies(dependency(), dependency(extra='<type>jar</type>')))})
        self.assertIn(ModelIssue.DUPLICATE, self.issues(self.model(graph)))

    def test_all_pinned_handlers_and_explicit_classifier_override(self):
        expected = {
            'pom': ('pom', None), 'jar': ('jar', None), 'test-jar': ('jar', 'tests'),
            'maven-plugin': ('jar', None), 'ejb': ('jar', None), 'ejb-client': ('jar', 'client'),
            'war': ('war', None), 'ear': ('ear', None), 'rar': ('rar', None),
            'java-source': ('jar', 'sources'), 'javadoc': ('jar', 'javadoc'),
        }
        facts_path = Path(__file__).parents[1] / 'third_party/maven-3.9.11/artifact-handlers.json'
        facts = json.loads(facts_path.read_text())
        self.assertEqual(set(facts['handlers']), set(expected))
        for kind, (extension, classifier) in expected.items():
            with self.subTest(kind=kind):
                artifact = artifact_for(MavenModelKey('g', 'a', kind))
                self.assertEqual((artifact.extension, artifact.classifier), (extension, classifier))
                self.assertEqual(facts['handlers'][kind],
                                 {'extension': extension, 'default_classifier': classifier})
                explicit = artifact_for(MavenModelKey('g', 'a', kind, 'custom'))
                self.assertEqual(explicit.classifier, 'custom')

    def test_three_test_artifact_aliases_have_distinct_raw_model_keys(self):
        graph = self.graph({'pom.xml': pom(dependencies(
            dependency(extra='<type>test-jar</type>'),
            dependency(extra='<type>test-jar</type><classifier>tests</classifier>'),
            dependency(extra='<classifier>tests</classifier>'),
        ))})
        records = self.model(graph).dependencies
        self.assertEqual(len({record.key for record in records}), 3)
        self.assertEqual(len({record.artifact_key for record in records}), 1)

    def test_custom_handler_keeps_raw_model_key_but_empty_classifier_is_unsupported(self):
        graph = self.graph({'pom.xml': pom(dependencies(
            dependency('custom', '<type>custom</type>'),
            dependency('empty', '<classifier/>'), dependency('safe')),)})
        model = self.model(graph)
        self.assertEqual([r.key.artifact_id for r in model.dependencies], ['custom', 'safe'])
        self.assertIsNone(model.dependencies[0].artifact_key)
        self.assertIn(ModelIssue.ARTIFACT, self.issues(model))
        self.assertIn(ModelIssue.KEY, self.issues(model))
        self.assertIsNone(artifact_for(MavenModelKey('g', 'a', 'JAR')))

    def test_plugin_management_bom_and_nested_dependencies_never_add_direct_rows(self):
        nested = dependencies(dependency('plugin-only'))
        body = ('<build><plugins><plugin>' + nested + '</plugin></plugins></build>'
                + '<reporting>' + nested + '</reporting>'
                + management(dependency('bom', '<type>pom</type><scope>import</scope>'))
                + dependencies(dependency('ordinary-pom', '<type>pom</type>')))
        model = self.model(self.graph({'pom.xml': pom(body)}))
        self.assertEqual([r.key.artifact_id for r in model.dependencies], ['ordinary-pom'])
        self.assertEqual([r.key.artifact_id for r in model.management], ['bom'])
        self.assertEqual(model.dependencies[0].artifact_key.extension, 'pom')

    def test_system_path_and_bom_never_trigger_secondary_reads(self):
        data = pom(dependencies(dependency(extra='<scope>system</scope><systemPath>/private/never</systemPath>'))
                   + management(dependency('bom', '<type>pom</type><scope>import</scope>')))
        reader = Mock(return_value=MavenInputSnapshot('pom.xml', data, (), parse_pom(data)))
        with patch('builtins.open', side_effect=AssertionError('unexpected file read')):
            graph = self.graph({'pom.xml': data}, reader=reader)
        self.assertEqual(self.model(graph).dependencies[0].field('scope').value, 'system')
        reader.assert_called_once_with('pom.xml')

    def test_aggregation_is_not_inheritance_and_colocation_is_not_aggregation(self):
        graph = self.graph({
            'pom.xml': pom(modules('child') + dependencies(dependency())),
            'child/pom.xml': pom(artifact='child'),
            'colocated/pom.xml': pom(artifact='unrelated'),
            'inherits/pom.xml': pom(parent(), artifact='inherits'),
        })
        self.assertEqual(self.model(graph, 'child/pom.xml').dependencies, ())
        self.assertEqual(len(self.model(graph, 'inherits/pom.xml').dependencies), 1)
        self.assertEqual({a.source_ids for a in graph.aggregations}, {
            ('child/pom.xml', 'pom.xml'),
            ('colocated/pom.xml',), ('inherits/pom.xml',),
        })

    def test_nested_aggregation_and_compatible_root_reachability(self):
        graph = self.graph({'pom.xml': pom(modules('a', 'a/b')),
                            'a/pom.xml': pom(modules('b'), artifact='a'),
                            'a/b/pom.xml': pom(artifact='b')})
        self.assertEqual(len(graph.aggregations), 1)
        self.assertTrue(graph.aggregations[0].complete)
        self.assertEqual(graph.aggregations[0].roots, ('pom.xml',))

    def test_incompatible_roots_shared_module_refuse_association(self):
        graph = self.graph({'a/pom.xml': pom(modules('../shared'), artifact='a'),
                            'b/pom.xml': pom(modules('../shared'), artifact='b'),
                            'shared/pom.xml': pom(artifact='shared')})
        association = graph.aggregations[0]
        self.assertFalse(association.complete)
        self.assertIn(ModelIssue.ROOTS, self.issues(association))

    def test_duplicate_project_gav_within_component_but_independent_roots_stay_separate(self):
        graph = self.graph({'pom.xml': pom(modules('a')), 'a/pom.xml': pom()})
        self.assertFalse(graph.aggregations[0].complete)
        self.assertIn(ModelIssue.DUPLICATE_GAV, self.issues(graph.aggregations[0]))
        graph = self.graph({'a/pom.xml': pom(), 'b/pom.xml': pom()})
        self.assertEqual(len(graph.aggregations), 2)
        self.assertTrue(all(a.complete for a in graph.aggregations))

    def test_module_missing_escape_property_self_duplicate_and_cycles_refuse(self):
        for path in ('missing', '../escape', '${module}', '.', 'child/pom.xml', '/child'):
            with self.subTest(path=path):
                graph = self.graph({'pom.xml': pom(modules(path)),
                                    'child/pom.xml': pom(artifact='child')})
                root = next(a for a in graph.aggregations if 'pom.xml' in a.source_ids)
                self.assertFalse(root.complete)
        graph = self.graph({'pom.xml': pom(modules('child', './child')),
                            'child/pom.xml': pom(modules('..'), artifact='child')})
        self.assertFalse(graph.aggregations[0].complete)
        self.assertIn(ModelIssue.MODULE_CYCLE, self.issues(graph.aggregations[0]))

    def test_profile_modules_and_101_modules_leave_association_incomplete(self):
        for body in ('<profiles><profile><modules><module>child</module></modules></profile></profiles>',
                     modules(*[f'm{i}' for i in range(101)])):
            self.assertFalse(self.graph({'pom.xml': pom(body)}).aggregations[0].complete)
        body = '<profiles><profile><build><plugins/></build></profile></profiles>'
        self.assertTrue(self.graph({'pom.xml': pom(body)}).aggregations[0].complete)
        for count in (100, 101):
            graph = self.graph({'pom.xml': pom(modules(*[f'm{i}' for i in range(count)]))})
            self.assertEqual(len(graph.projects[0].modules), min(count, 100))
            self.assertEqual(graph.projects[0].modules_complete, count == 100)

    def test_field_structure_foreign_namespace_and_duplicate_parent_refuse(self):
        bodies = [
            '<dependencies/><dependencies/>',
            '<dependencies xmlns="urn:foreign"/>',
            parent() + parent(),
            dependencies(dependency(extra='<version><nested/></version>')),
        ]
        for body in bodies:
            with self.subTest(body=body):
                self.assertIn(ModelIssue.STRUCTURE, self.issues(self.model(self.graph({'pom.xml': pom(body)}))))
        graph = self.graph({'pom.xml': pom(parent() + parent())})
        self.assertFalse(self.model(graph).parent_chain_complete)

    def test_malformed_profiles_cannot_certify_module_association(self):
        graph = self.graph({
            'pom.xml': pom(modules('child') + '<profiles><unexpected/></profiles>'),
            'child/pom.xml': pom(artifact='child'),
        })
        self.assertFalse(graph.projects[1].modules_complete)
        self.assertIn(ModelIssue.STRUCTURE, self.issues(graph.projects[1]))
        self.assertEqual(graph.aggregations[0].source_ids, ('child/pom.xml', 'pom.xml'))
        self.assertFalse(graph.aggregations[0].complete)

    def test_unknown_management_container_child_keeps_uncertainty_and_safe_records(self):
        body = ('<dependencyManagement><unexpected/>' + dependencies(dependency('managed'))
                + '</dependencyManagement>' + dependencies(dependency('direct')))
        model = self.model(self.graph({'pom.xml': pom(body)}))
        self.assertIn(ModelIssue.STRUCTURE, self.issues(model))
        self.assertEqual([r.key.artifact_id for r in model.management], ['managed'])
        self.assertEqual([r.key.artifact_id for r in model.dependencies], ['direct'])

    def test_unsupported_dependency_entry_keeps_independent_safe_siblings(self):
        bad_entries = (
            '<dependency xmlns="urn:foreign"><groupId>x</groupId><artifactId>bad</artifactId></dependency>',
            '<dependency unknown="true"><groupId>x</groupId><artifactId>bad</artifactId></dependency>',
        )
        for bad in bad_entries:
            for managed in (False, True):
                body = dependencies(dependency('safe'), bad, dependency('other'))
                if managed:
                    body = '<dependencyManagement>' + body + '</dependencyManagement>'
                model = self.model(self.graph({'pom.xml': pom(body)}))
                records = model.management if managed else model.dependencies
                self.assertEqual([r.key.artifact_id for r in records], ['safe', 'other'])
                self.assertIn(ModelIssue.STRUCTURE, self.issues(model))

    def test_refused_dependency_entry_still_consumes_source_budget(self):
        bad = '<dependency xmlns="urn:foreign"/>'
        with patch('libyears.maven_project.MAX_RECORDS', 2):
            model = self.model(self.graph({'pom.xml': pom(dependencies(
                bad, dependency('safe'), dependency('too-late')))}))
        self.assertEqual([r.key.artifact_id for r in model.dependencies], ['safe'])
        self.assertIn(ModelIssue.STRUCTURE, self.issues(model))
        self.assertIn(ModelIssue.LIMIT, self.issues(model))

    def test_snapshot_source_binding_mismatch_is_unavailable(self):
        data = pom(dependencies(dependency()))
        reader = Mock(return_value=MavenInputSnapshot('other/pom.xml', data, (), parse_pom(data)))
        model = self.model(self.graph({'pom.xml': data}, reader=reader))
        self.assertEqual(model.dependencies, ())
        self.assertIn(ModelIssue.INPUT, self.issues(model))

    def test_input_failure_retains_siblings_and_never_salvages_partial_xml(self):
        safe = pom(dependencies(dependency()))
        snapshots = {'b/pom.xml': MavenInputSnapshot('b/pom.xml', safe, (), parse_pom(safe))}
        def read(source):
            if source == 'a/pom.xml':
                raise MavenInputFailure(MavenInputIssue.XML_MALFORMED)
            return snapshots[source]
        graph = self.graph({'a/pom.xml': safe, 'b/pom.xml': safe}, reader=read, complete=False)
        self.assertFalse(graph.discovery.complete)
        self.assertEqual(self.model(graph, 'a/pom.xml').dependencies, ())
        self.assertEqual(len(self.model(graph, 'b/pom.xml').dependencies), 1)

    def test_raw_graph_has_no_final_population_or_version_resolution_and_is_immutable(self):
        graph = self.graph({'pom.xml': pom(dependencies(dependency(extra='<version>${v}</version>')))})
        record = self.model(graph).dependencies[0]
        self.assertEqual(record.field('version').value, '${v}')
        self.assertNotIn('population_count', {f.name for f in fields(RawModel)})
        self.assertFalse(hasattr(record, 'declared'))
        with self.assertRaises(FrozenInstanceError):
            record.consumer_source = 'other/pom.xml'

    def test_10000_source_records_and_expanded_scan_budget(self):
        entries = [dependency('a' + str(i)) for i in range(10_001)]
        graph = self.graph({'pom.xml': pom(dependencies(*entries))})
        self.assertEqual(len(self.model(graph).dependencies), 10_000)
        self.assertIn(ModelIssue.LIMIT, self.issues(self.model(graph)))
        # Bound expanded occurrences, not distinct package names or source rows.
        with patch('libyears.maven_project.MAX_RECORDS', 3):
            graph = self.graph({'pom.xml': pom(dependencies(dependency('a'), dependency('b'))),
                                'z/pom.xml': pom(parent(), artifact='z')})
        self.assertEqual(len(self.model(graph).dependencies), 2)
        self.assertEqual(len(self.model(graph, 'z/pom.xml').dependencies), 1)
        self.assertIn(ModelIssue.LIMIT, self.issues(self.model(graph, 'z/pom.xml')))

    def test_each_discovered_snapshot_read_once_and_input_order_is_irrelevant(self):
        docs = {'pom.xml': pom(), 'child/pom.xml': pom(parent(), artifact='child')}
        snapshots = {name: MavenInputSnapshot(name, data, ('fixture',), parse_pom(data))
                     for name, data in docs.items()}
        reader = Mock(side_effect=snapshots.__getitem__)
        graph = self.graph(docs, reader=reader)
        self.assertEqual(reader.call_count, 2)
        self.assertEqual(graph, self.graph(dict(reversed(list(docs.items())))))


@unittest.skipUnless(filesystem_available(), 'native descriptor primitives unavailable')
class MavenProjectNativeTests(unittest.TestCase):
    def test_real_inventory_reader_supplies_only_discovered_snapshots(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as directory:
            root = Path(directory)
            (root / 'child').mkdir()
            (root / 'pom.xml').write_bytes(pom(modules('child')))
            (root / 'child/pom.xml').write_bytes(pom(parent(), artifact='child'))
            before = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in root.rglob('pom.xml')}
            with MavenInputReader(root) as reader:
                inventory = reader.inventory()
                graph = build_project_graph(inventory.discovery, reader.snapshot_pom)
            self.assertTrue(graph.aggregations[0].complete)
            self.assertTrue(all(model.parent_chain_complete for model in graph.models))
            self.assertEqual(before, {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in root.rglob('pom.xml')})


if __name__ == '__main__':
    unittest.main()
