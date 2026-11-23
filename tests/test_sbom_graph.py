import unittest
from unittest.mock import patch

from libyears.sbom_document import accept_document
from libyears.sbom_graph import attach_graph
from libyears.sbom_identity import canonical_members
from tests.test_sbom_document import snapshot, synthetic_document
from tests.test_sbom_identity import maven_component


class GraphTests(unittest.TestCase):
    def graph(self, records, dependencies=None, *, services=None, absent=False):
        value = synthetic_document(components=records, services=services or [])
        if not absent:
            value['dependencies'] = dependencies
        document = accept_document(snapshot(value))
        with patch('socket.socket', side_effect=AssertionError('socket')):
            return attach_graph(document, canonical_members(document))

    def test_missing_empty_and_partial_graph(self):
        records = [maven_component(**{'bom-ref': 'a'}), maven_component('b', **{'bom-ref': 'b'})]
        graph, rows = self.graph(records, absent=True)
        self.assertEqual(graph.reason, 'sbom_graph_unknown')
        self.assertIsNone(rows[0].direct_path)
        graph, rows = self.graph(records, [])
        self.assertEqual(graph.state, 'available')
        self.assertFalse(rows[0].direct_path)
        graph, rows = self.graph(records, [{'ref': 'root', 'dependsOn': ['a']}, {'ref': 'a'}, {'ref': 'b', 'dependsOn': []}])
        known = {vertex.id: vertex.dependencies_known for vertex in graph.vertices}
        self.assertEqual(known, {'subject': True, 'component-ref-0': False, 'component-ref-1': True})
        self.assertEqual([row.relationship for row in rows], ['direct', 'unknown'])

    def test_service_paths_direct_and_longer_and_cycles(self):
        records = [maven_component(**{'bom-ref': 'a'}), maven_component('b', **{'bom-ref': 'b'}),
                   maven_component('c', **{'bom-ref': 'c'})]
        nodes = [{'ref': 'root', 'dependsOn': ['a', 'svc']}, {'ref': 'svc', 'dependsOn': ['a', 'b']},
                 {'ref': 'b', 'dependsOn': ['b']}, {'ref': 'c', 'dependsOn': ['c']}]
        graph, rows = self.graph(records, nodes, services=[{'bom-ref': 'svc'}])
        self.assertTrue(graph.cycles_present)
        self.assertEqual((rows[0].direct_path, rows[0].transitive_path), (True, True))
        self.assertEqual(rows[1].relationship, 'transitive')
        self.assertEqual(rows[2].relationship, 'unknown')
        self.assertEqual(len(graph.vertices), 5)

    def test_unreachable_cycle_and_back_edge(self):
        records = [maven_component(**{'bom-ref': 'a'}), maven_component('b', **{'bom-ref': 'b'})]
        for nodes in ([{'ref': 'a', 'dependsOn': ['b']}, {'ref': 'b', 'dependsOn': ['a']}],
                      [{'ref': 'root', 'dependsOn': ['a']}, {'ref': 'a', 'dependsOn': ['root']}]):
            self.assertTrue(self.graph(records, nodes)[0].cycles_present)

    def test_graph_refusal_preserves_population_and_no_partial_edges(self):
        records = [maven_component(**{'bom-ref': 'pkg:maven/opaque/ref@1'})]
        for nodes in (None, {}, [1], [{'ref': 'unknown'}], [{'ref': 'root', 'extra': []}],
                      [{'ref': 'root', 'dependsOn': ['unknown']}], [{'ref': 'root'}, {'ref': 'root'}],
                      [{'ref': 'root', 'dependsOn': ['root', 'root']}], [{'ref': 'root', 'dependsOn': [None]}],
                      [{'ref': 'root', 'dependsOn': 'a'}], [{'ref': 'urn:cdx:external'}]):
            graph, rows = self.graph(records, nodes)
            self.assertEqual(graph.reason, 'sbom_graph_invalid')
            self.assertEqual(graph.edges, ())
            self.assertEqual(len(rows), 1)
            self.assertIsNone(rows[0].direct_path)
        self.assertEqual(self.graph(records, [{'ref': 'root', 'dependsOn': ['pkg:maven/opaque/ref@1']}])[1][0].relationship, 'direct')

    def test_alias_collapse_cannot_manufacture_paths(self):
        records = [maven_component(**{'bom-ref': 'a1'}), maven_component(**{'bom-ref': 'a2'}),
                   maven_component('b', **{'bom-ref': 'b'}), maven_component('c')]
        nodes = [{'ref': 'root', 'dependsOn': ['a1']}, {'ref': 'a2', 'dependsOn': ['b']}]
        graph, rows = self.graph(records, nodes)
        self.assertEqual(len(rows), 3)
        self.assertEqual([row.relationship for row in rows], ['direct', 'unknown', 'unknown'])
        self.assertEqual(sum(row.relationship == 'unknown' for row in rows), 2)
        self.assertEqual([vertex.member_id for vertex in graph.vertices if vertex.kind == 'component'][:2], ['component-0', 'component-0'])

    def test_iterative_long_graph(self):
        records = [maven_component(str(i), **{'bom-ref': str(i)}) for i in range(1200)]
        nodes = [{'ref': 'root', 'dependsOn': ['0']}] + [
            {'ref': str(i), 'dependsOn': [str(i + 1)] if i < 1199 else []} for i in range(1200)]
        graph, rows = self.graph(records, nodes)
        self.assertFalse(graph.cycles_present)
        self.assertEqual(sum(row.relationship == 'transitive' for row in rows), 1199)
