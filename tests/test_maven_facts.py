"""T005 repository-only declared facts/population; no registry or target input."""

import unittest
from unittest.mock import patch

from libyears.maven_input import MavenInputSnapshot, parse_pom
from libyears.maven_model import MavenDiscovery, MavenFieldBasis, MavenReason
from libyears.maven_project import build_project_graph, declared_sources
from libyears.maven_properties import PropertyFailure, ScalarProperty, expand_scalar
from libyears.maven_results import summarize_sources
from libyears.maven_model import MavenFieldOrigin
from test_maven_project import pom, dependency, dependencies, management, parent, modules


def properties(**values):
    return '<properties>' + ''.join(f'<{key}>{value}</{key}>' for key, value in values.items()) + '</properties>'


def profile(body):
    return '<profiles><profile><id>conditional</id>' + body + '</profile></profiles>'


def facts(documents):
    snapshots = {name: MavenInputSnapshot(name, data, ('fixture',), parse_pom(data))
                 for name, data in documents.items()}
    graph = build_project_graph(MavenDiscovery(True, tuple(documents)), snapshots.__getitem__)
    return declared_sources(graph)


class MavenFactTests(unittest.TestCase):
    def source(self, documents, source='pom.xml'):
        return next(item for item in facts(documents) if item.context.source_id == source)

    def single(self, body, **identity):
        return self.source({'pom.xml': pom(body, **identity)})

    def row(self, body, **identity):
        return self.single(body, **identity).declared.rows[0]

    def test_inherited_explicit_version_beats_child_management_and_keeps_scope(self):
        documents = {
            'pom.xml': pom(dependencies(dependency(extra='<version>1</version><scope>test</scope>'))),
            'child/pom.xml': pom(parent() + management(dependency(extra='<version>2</version>')),
                                 artifact='child'),
        }
        row = self.source(documents, 'child/pom.xml').declared.rows[0]
        self.assertEqual((row.declared.version, row.scope, row.optional), ('1', 'test', False))
        self.assertEqual(row.declared.origins[0].basis, MavenFieldBasis.INHERITED_DEPENDENCY)

    def test_raw_inherited_expression_uses_consumer_properties(self):
        documents = {
            'pom.xml': pom(properties(v='1', indirect='${v}') + dependencies(dependency(extra='<version>${indirect}</version>'))),
            'child/pom.xml': pom(parent() + properties(v='2'), artifact='child'),
        }
        sources = facts(documents)
        root = next(s for s in sources if s.context.source_id == 'pom.xml').declared.rows[0]
        child = next(s for s in sources if s.context.source_id == 'child/pom.xml').declared.rows[0]
        self.assertEqual((root.declared.version, child.declared.version), ('1', '2'))
        self.assertEqual(child.declared.request, '${indirect}')
        self.assertIn(('child/pom.xml', 'v', MavenFieldBasis.PROPERTY),
                      {(o.source_id, o.field_name, o.basis) for o in child.declared.origins})

    def test_reserved_builtins_cannot_be_shadowed(self):
        body = properties(**{'project.version': '99'}) + dependencies(dependency(extra='<version>${project.version}</version>'))
        self.assertEqual(self.row(body, version='2').declared.version, '2')
        documents = {'pom.xml': pom(version='3'),
                     'child/pom.xml': pom(parent(version='3') + properties(**{'project.parent.version': '99'})
                                          + dependencies(dependency(extra='<version>${project.parent.version}</version>')),
                                          artifact='child', version='4')}
        self.assertEqual(self.source(documents, 'child/pom.xml').declared.rows[0].declared.version, '3')

    def test_unsupported_namespaces_directory_cycles_missing_and_duplicates_refuse_fact(self):
        for name in ('project.directory', 'project.name', 'pom.version', 'env.VERSION',
                     'system.version', 'settings.version', 'user.version', 'session.version',
                     'basedir', 'baseUri'):
            body = properties(**{name: '1'}) + dependencies(dependency(extra=f'<version>${{{name}}}</version>'))
            row = self.row(body)
            self.assertIsNone(row.declared.version, name)
            self.assertEqual(row.declared.reason, MavenReason.UNSUPPORTED_VERSION)
        self.assertIsNone(self.row(dependencies(dependency(extra='<version>${missing}</version>'))).declared.version)
        for props in (properties(a='${b}', b='${a}'), '<properties><a>1</a><a>2</a></properties>'):
            self.assertIsNone(self.row(props + dependencies(dependency(extra='<version>${a}</version>'))).declared.version)

    def test_parent_project_directory_is_never_inherited_as_a_scalar(self):
        docs = {'pom.xml': pom(properties(**{'project.directory': '1'})),
                'c/pom.xml': pom(parent() + dependencies(dependency(extra='<version>${project.directory}</version>')),
                                 artifact='c')}
        self.assertIsNone(self.source(docs, 'c/pom.xml').declared.rows[0].declared.version)

    def test_scope_default_is_delayed_and_optional_is_never_managed(self):
        row = self.row(management(dependency(extra='<scope>test</scope><optional>true</optional><version>1</version>'))
                       + dependencies(dependency()))
        self.assertEqual((row.declared.version, row.scope, row.optional), ('1', 'test', False))
        row = self.row(dependencies(dependency(extra='<version>1</version>')))
        self.assertEqual((row.scope, row.optional), ('compile', False))

    def test_unresolved_import_blocks_inherited_field_not_consumer_written_field(self):
        base = (management(dependency(extra='<version>1</version>'),
                           dependency('bom', '<type>pom</type><scope>import</scope><version>1</version>')))
        docs = {'pom.xml': pom(base), 'c/pom.xml': pom(parent() + management(dependency(extra='<scope>test</scope>'))
                + dependencies(dependency()), artifact='c')}
        row = self.source(docs, 'c/pom.xml').declared.rows[0]
        self.assertIsNone(row.declared.version)
        self.assertEqual((row.scope, row.optional), ('test', False))
        docs['c/pom.xml'] = pom(parent() + management(dependency(extra='<version>2</version>'))
                                + dependencies(dependency()), artifact='c')
        row = self.source(docs, 'c/pom.xml').declared.rows[0]
        self.assertEqual(row.declared.version, '2')
        self.assertIsNone(row.scope)
        self.assertFalse(row.optional)

    def test_inherited_management_allowed_without_imports_and_optional_inherited_directly(self):
        docs = {'pom.xml': pom(management(dependency(extra='<version>1</version>'))
                               + dependencies(dependency(extra='<optional>true</optional>'))),
                'c/pom.xml': pom(parent(), artifact='c')}
        row = self.source(docs, 'c/pom.xml').declared.rows[0]
        self.assertEqual((row.declared.version, row.scope, row.optional), ('1', 'compile', True))

    def test_all_missing_bom_versions_keep_known_population_and_zero_measurements(self):
        body = management(dependency('bom', '<type>pom</type><scope>import</scope><version>1</version>'))
        source = self.single(body + dependencies(dependency('a'), dependency('b')))
        self.assertEqual(source.declared.population_count, 2)
        self.assertTrue(source.declared.accepted)
        self.assertTrue(all(row.declared.version is None for row in source.declared.rows))
        self.assertTrue(all(row.optional is False for row in source.declared.rows))
        self.assertFalse(source.observed.accepted)
        summary = summarize_sources((source,)).declared.summary
        self.assertEqual((summary.dependencies_discovered, summary.dependencies_measured,
                          summary.coverage, summary.total_libyears), (2, 0, 0, 0.0))

    def test_exact_singleton_and_used_prerelease_are_facts_but_selectors_ranges_snapshots_are_not(self):
        for request, expected in (('[1.2]', '1.2'), ('1-alpha1', '1-alpha1'), ('1-vendor', '1-vendor'),
                                  ('[1,2)', None), ('[1,2]', None), ('LATEST', None),
                                  ('RELEASE', None), ('1-SNAPSHOT', None), ('1-20261112.120000-1', None)):
            row = self.row(dependencies(dependency(extra=f'<version>{request}</version>')))
            self.assertEqual(row.declared.request, request)
            self.assertEqual(row.declared.version, expected)
            self.assertIsNone(row.declared.age)

    def test_all_scopes_optional_tooling_and_ordinary_pom_are_counted(self):
        entries = [dependency('a'+str(i), f'<version>1</version><scope>{scope}</scope><optional>true</optional>')
                   for i, scope in enumerate(('compile', 'runtime', 'test', 'provided', 'system'))]
        entries.append(dependency('tooling', '<type>pom</type><version>1</version>'))
        source = self.single(dependencies(*entries))
        self.assertEqual(source.declared.population_count, 6)
        self.assertTrue(all(row.declared.version == '1' for row in source.declared.rows))
        self.assertEqual(source.declared.rows[-1].artifact_key.extension, 'pom')

    def test_repeated_modules_have_independent_occurrences(self):
        docs = {'pom.xml': pom(modules('a', 'b') + dependencies(dependency(extra='<version>1</version>'))),
                'a/pom.xml': pom(parent(), artifact='a'), 'b/pom.xml': pom(parent(), artifact='b')}
        sources = facts(docs)
        self.assertEqual([s.declared.population_count for s in sources], [1, 1, 1])
        self.assertEqual(len({s.declared.rows[0].key for s in sources}), 3)

    def test_internal_exclusion_needs_exact_gav_and_association(self):
        for version, expected in (('1', 0), ('2', 1)):
            docs = {'pom.xml': pom(modules('child') + dependencies(dependency('child', f'<version>{version}</version>', group='g'))),
                    'child/pom.xml': pom(artifact='child')}
            self.assertEqual(self.source(docs).declared.population_count, expected)
        docs['pom.xml'] = pom(dependencies(dependency('child', '<version>1</version>', group='g')))
        self.assertEqual(self.source(docs).declared.population_count, 1)

    def test_internal_snapshot_identity_does_not_become_external_release_age(self):
        docs = {'pom.xml': pom(modules('child') + dependencies(dependency('child', '<version>1-SNAPSHOT</version>', group='g'))),
                'child/pom.xml': pom(artifact='child', version='1-SNAPSHOT')}
        self.assertEqual(self.source(docs).declared.population_count, 0)

    def test_missing_parent_keeps_safe_local_rows_but_denominator_unknown(self):
        source = self.single(parent(path='') + dependencies(dependency(extra='<version>1</version>')))
        self.assertIsNone(source.declared.population_count)
        self.assertEqual(source.declared.rows[0].declared.version, '1')

    def test_unknown_version_that_could_name_internal_project_is_not_counted_external(self):
        docs = {'pom.xml': pom(modules('child') + dependencies(
            dependency('child', '<version>${missing}</version>', group='g'),
            dependency('safe', '<version>1</version>'))),
            'child/pom.xml': pom(artifact='child')}
        source = self.source(docs)
        self.assertIsNone(source.declared.population_count)
        self.assertEqual([r.key.model_key.artifact_id for r in source.declared.rows], ['safe'])

    def test_external_profile_version_change_keeps_n_and_withholds_only_affected_fact(self):
        body = dependencies(dependency(extra='<version>1</version>'), dependency('safe', '<version>1</version>'))
        source = self.single(body + profile(dependencies(dependency(extra='<version>2</version>'))))
        self.assertEqual(source.declared.population_count, 2)
        self.assertEqual([r.declared.version for r in source.declared.rows], [None, '1'])

    def test_profile_property_and_ancestor_effects_are_not_ignored(self):
        docs = {'pom.xml': pom(properties(v='1') + dependencies(dependency(extra='<version>${v}</version>'))
                               + profile(properties(v='2'))),
                'c/pom.xml': pom(parent(), artifact='c')}
        self.assertIsNone(self.source(docs, 'c/pom.xml').declared.rows[0].declared.version)
        docs['c/pom.xml'] = pom(parent() + properties(v='3'), artifact='c')
        self.assertEqual(self.source(docs, 'c/pom.xml').declared.rows[0].declared.version, '3')

    def test_profile_crossing_internal_version_makes_population_unknown(self):
        body = modules('child') + dependencies(dependency('child', '<version>2</version>', group='g'))
        body += profile(dependencies(dependency('child', '<version>1</version>', group='g')))
        source = self.source({'pom.xml': pom(body), 'child/pom.xml': pom(artifact='child')})
        self.assertIsNone(source.declared.population_count)
        self.assertEqual(source.declared.rows, ())

    def test_profile_membership_unknown_preserves_independent_base_fact(self):
        source = self.single(dependencies(dependency('base', '<version>1</version>'))
                             + profile(dependencies(dependency('extra', '<version>1</version>'))))
        self.assertIsNone(source.declared.population_count)
        self.assertEqual(source.declared.rows[0].declared.version, '1')
        source = self.single(dependencies(dependency(extra='<version>1</version>'))
                             + profile('<build><plugins/></build>'))
        self.assertEqual(source.declared.population_count, 1)
        self.assertEqual(source.declared.rows[0].declared.version, '1')

    def test_profile_module_association_and_unknown_identity_withhold_population(self):
        docs = {'pom.xml': pom(profile(modules('child')) + dependencies(
            dependency('child', '<version>1</version>', group='g'), dependency('safe', '<version>1</version>'))),
            'child/pom.xml': pom(artifact='child')}
        source = self.source(docs)
        self.assertIsNone(source.declared.population_count)
        self.assertEqual([r.key.model_key.artifact_id for r in source.declared.rows], ['safe'])
        source = self.single(dependencies(dependency(group='${group}')))
        self.assertIsNone(source.declared.population_count)

    def test_management_profile_changes_do_not_override_explicit_dependency_version(self):
        body = management(dependency(extra='<version>1</version>'))
        body += profile(management(dependency(extra='<version>2</version>')))
        self.assertIsNone(self.row(body + dependencies(dependency())).declared.version)
        self.assertEqual(self.row(body + dependencies(dependency(extra='<version>3</version>'))).declared.version, '3')

    def test_no_file_host_or_bom_lookup_during_fact_resolution(self):
        body = management(dependency('bom', '<type>pom</type><scope>import</scope><version>1</version>'))
        body += dependencies(dependency(extra='<version>1</version><scope>system</scope><systemPath>/never</systemPath>'))
        with patch('builtins.open', side_effect=AssertionError('file lookup')), \
                patch('os.getenv', side_effect=AssertionError('host lookup')):
            self.assertEqual(self.row(body).declared.version, '1')

    def test_malformed_management_changes_facts_not_known_direct_population(self):
        source = self.single('<dependencyManagement/><dependencyManagement/>'
                             + dependencies(dependency(extra='<version>1</version>')))
        self.assertEqual(source.declared.population_count, 1)
        self.assertEqual(source.declared.rows[0].declared.version, '1')
        self.assertIsNone(source.declared.rows[0].scope)

    def test_unknown_root_shape_prevents_complete_population_but_keeps_safe_row(self):
        source = self.single('<unknownModelPopulation/>'
                             + dependencies(dependency(extra='<version>1</version>')))
        self.assertIsNone(source.declared.population_count)
        self.assertEqual(source.declared.rows[0].declared.version, '1')

    def test_absent_profile_id_uses_pinned_default_without_activation(self):
        body = '<profiles><profile>' + dependencies(dependency(extra='<version>2</version>')) + '</profile></profiles>'
        source = self.single(dependencies(dependency(extra='<version>1</version>')) + body)
        self.assertEqual(source.declared.population_count, 1)
        self.assertIsNone(source.declared.rows[0].declared.version)

    def test_unrelated_custom_management_does_not_poison_supported_local_fields(self):
        body = management(dependency(extra='<version>1</version>'),
                          dependency('unrelated', '<type>custom</type><version>9</version>'))
        row = self.row(body + dependencies(dependency()))
        self.assertEqual((row.declared.version, row.scope, row.optional), ('1', 'compile', False))

    def test_duplicate_management_is_key_local_and_optional_stays_unmanaged(self):
        body = management(dependency('a', '<version>1</version>'),
                          dependency('bad', '<version>2</version>'), dependency('bad', '<version>3</version>'))
        source = self.single(body + dependencies(dependency('a'), dependency('bad')))
        self.assertEqual(source.declared.population_count, 2)
        self.assertEqual(source.declared.rows[0].declared.version, '1')
        self.assertEqual(source.declared.rows[0].scope, 'compile')
        self.assertIsNone(source.declared.rows[1].declared.version)
        self.assertIsNone(source.declared.rows[1].scope)
        self.assertFalse(source.declared.rows[1].optional)

    def test_child_property_replacement_survives_unknown_ancestor_properties(self):
        docs = {'pom.xml': pom(properties(a='1', b='2')),
                'child/pom.xml': pom(parent() + properties(v='2') + dependencies(
                    dependency('safe', '<version>${v}</version>'),
                    dependency('unknown', '<version>${a}</version>')), artifact='child')}
        with patch('libyears.maven_properties.MAX_PROPERTIES', 1):
            source = self.source(docs, 'child/pom.xml')
        self.assertEqual(source.declared.population_count, 2)
        self.assertEqual([r.declared.version for r in source.declared.rows], ['2', None])
        docs['child/pom.xml'] = pom(parent() + properties(v='${a}')
                                    + dependencies(dependency(extra='<version>${v}</version>')), artifact='child')
        with patch('libyears.maven_properties.MAX_PROPERTIES', 1):
            self.assertIsNone(self.source(docs, 'child/pom.xml').declared.rows[0].declared.version)

    def test_candidate_project_profile_identity_uncertainty_prevents_internal_exclusion(self):
        docs = {'pom.xml': pom(modules('child') + dependencies(
            dependency('child', '<version>1</version>', group='g'),
            dependency('safe', '<version>1</version>'))),
            'child/pom.xml': pom(profile('<version>2</version>'), artifact='child')}
        source = self.source(docs)
        self.assertIsNone(source.declared.population_count)
        self.assertEqual([r.key.model_key.artifact_id for r in source.declared.rows], ['safe'])

    def test_conditional_incoming_association_affects_module_not_only_aggregator(self):
        docs = {'pom.xml': pom(profile(modules('b'))),
                'b/pom.xml': pom(dependencies(dependency('project', '<version>1</version>', group='g'),
                                             dependency('safe', '<version>1</version>')), artifact='b')}
        source = self.source(docs, 'b/pom.xml')
        self.assertIsNone(source.declared.population_count)
        self.assertEqual([r.key.model_key.artifact_id for r in source.declared.rows], ['safe'])
        docs['b/pom.xml'] = pom(dependencies(dependency('project', '<version>2</version>', group='g')),
                                artifact='b')
        self.assertEqual(self.source(docs, 'b/pom.xml').declared.population_count, 1)

    def test_certified_empty_population_survives_module_association_uncertainty(self):
        for body in (modules('missing'), profile(modules('future')),
                     modules(*[f'm{i}' for i in range(101)])):
            source = self.single(body)
            self.assertTrue(source.declared.accepted)
            self.assertEqual(source.declared.population_count, 0)
            self.assertEqual(source.declared.rows, ())
        source = self.single(parent(path='') + modules('missing'))
        self.assertFalse(source.declared.accepted)
        self.assertIsNone(source.declared.population_count)


class MavenExpansionBudgetTests(unittest.TestCase):
    def prop(self, value):
        return ScalarProperty(value, MavenFieldOrigin('pom.xml', 'v', MavenFieldBasis.PROPERTY))

    def test_depth_substitution_and_expanded_size_boundaries(self):
        values = {'v'+str(i): self.prop('${v'+str(i+1)+'}') for i in range(15)}
        values['v15'] = self.prop('1')
        self.assertEqual(expand_scalar('${v0}', values, {})[0], '1')
        values['v15'] = self.prop('${v16}'); values['v16'] = self.prop('1')
        with self.assertRaises(PropertyFailure):
            expand_scalar('${v0}', values, {})
        self.assertEqual(len(expand_scalar('${v}'*1024, {'v':self.prop('1')}, {})[0]), 1024)
        with self.assertRaises(PropertyFailure):
            expand_scalar('${v}'*1025, {'v':self.prop('1')}, {})
        self.assertEqual(len(expand_scalar('${v}', {'v':self.prop('a'*65536)}, {})[0]), 65536)
        with self.assertRaises(PropertyFailure):
            expand_scalar('${v}', {'v':self.prop('a'*65537)}, {})

    def test_property_budget_does_not_destroy_literal_sibling(self):
        body = '<properties>' + ''.join(f'<p{i}>1</p{i}>' for i in range(4097)) + '</properties>'
        body += dependencies(dependency('property', '<version>${p0}</version>'),
                             dependency('literal', '<version>1</version>'))
        source = facts({'pom.xml':pom(body)})[0]
        self.assertEqual(source.declared.population_count, 2)
        self.assertEqual([r.declared.version for r in source.declared.rows], [None, '1'])


if __name__ == '__main__':
    unittest.main()
