"""Document-reference graph first; package collapse only combines final labels."""

from collections import deque
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class SbomVertex:
    id: str
    kind: str
    member_id: str | None
    dependencies_known: bool = False


@dataclass(frozen=True)
class SbomGraph:
    state: str = 'unknown'
    reason: str | None = None
    subject_id: str | None = None
    vertices: tuple[SbomVertex, ...] = ()
    edges: tuple[tuple[str, str], ...] = ()
    cycles_present: bool | None = None


def _cycles(adjacency):
    color = {}
    for start in adjacency:
        if color.get(start, 0):
            continue
        color[start] = 1
        stack = [(start, iter(adjacency[start]))]
        while stack:
            vertex, children = stack[-1]
            child = next(children, None)
            if child is None:
                color[vertex] = 2
                stack.pop()
            elif color.get(child, 0) == 1:
                return True
            elif color.get(child, 0) == 0:
                color[child] = 1
                stack.append((child, iter(adjacency[child])))
    return False


def attach_graph(document, members):
    unknown = SbomGraph('unknown', 'sbom_graph_unknown', 'subject')
    invalid = SbomGraph('unavailable', 'sbom_graph_invalid', 'subject')
    if 'dependencies' not in document.root:
        return unknown, members
    nodes = document.root['dependencies']
    if not isinstance(nodes, list):
        return invalid, members
    by_ref = {document.subject['bom-ref']: SbomVertex('subject', 'subject', None)}
    for member in members:
        for index, record in member.records:
            if 'bom-ref' in record:
                by_ref[record['bom-ref']] = SbomVertex(f'component-ref-{index}', 'component', member.id)
    for index, record in enumerate(document.services):
        if 'bom-ref' in record:
            by_ref[record['bom-ref']] = SbomVertex(f'service-ref-{index}', 'service', None)
    adjacency = {vertex.id: [] for vertex in by_ref.values()}
    seen = set()
    edges = []
    def supported_ref(value):
        return isinstance(value, str) and not value.startswith('urn:cdx:') and value in by_ref
    for node in nodes:
        if (not isinstance(node, dict) or set(node) - {'ref', 'dependsOn'}
                or not supported_ref(node.get('ref')) or node['ref'] in seen):
            return invalid, members
        raw_ref = node['ref']
        seen.add(raw_ref)
        if 'dependsOn' not in node:
            continue
        children = node['dependsOn']
        if not isinstance(children, list):
            return invalid, members
        by_ref[raw_ref] = replace(by_ref[raw_ref], dependencies_known=True)
        child_refs = set()
        for child in children:
            if not supported_ref(child) or child in child_refs:
                return invalid, members
            child_refs.add(child)
            source, target = by_ref[raw_ref].id, by_ref[child].id
            adjacency[source].append(target)
            edges.append((source, target))
    reached = set()
    pending = deque([('subject', 0)])
    while pending:
        vertex, depth = pending.popleft()
        if (vertex, depth) in reached:
            continue
        reached.add((vertex, depth))
        for child in adjacency[vertex]:
            pending.append((child, min(2, depth + 1)))
    attached = []
    for member in members:
        refs = [f'component-ref-{index}' for index, record in member.records if 'bom-ref' in record]
        direct = any((ref, 1) in reached for ref in refs)
        transitive = any((ref, 2) in reached for ref in refs)
        label = 'direct' if direct else 'transitive' if transitive else 'unknown'
        attached.append(replace(member, relationship=label, direct_path=direct, transitive_path=transitive))
    graph = SbomGraph('available', None, 'subject',
                      tuple(sorted(by_ref.values(), key=lambda vertex: vertex.id)),
                      tuple(sorted(edges)), _cycles(adjacency))
    return graph, tuple(attached)
