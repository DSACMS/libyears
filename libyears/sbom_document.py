"""The accepted flat CycloneDX 1.5 projection, never general schema validation."""

from dataclasses import dataclass
import json

from .sbom_json import decode_document
from .sbom_model import SbomFailure, SbomSnapshot

MAX_COMPONENTS = 10_000
MAX_SERVICES = 1_000
MAX_NODES = 11_001
MAX_EDGES = 50_000
ROOT_FIELDS = frozenset({
    '$schema', 'bomFormat', 'specVersion', 'serialNumber', 'version', 'metadata',
    'components', 'services', 'dependencies', 'externalReferences', 'compositions',
    'vulnerabilities', 'annotations', 'signature', 'properties', 'formulation',
})


@dataclass(frozen=True)
class SbomDocument:
    snapshot: SbomSnapshot
    root: dict
    subject: dict
    records: tuple[tuple[int, dict], ...]
    services: tuple[dict, ...]
    subject_aliases: int


def _unsupported():
    raise SbomFailure('sbom_unsupported_format')


def _reference(record, *, required=False):
    ref = record.get('bom-ref')
    if 'bom-ref' not in record and not required:
        return None
    if not isinstance(ref, str) or not 1 <= len(ref.encode('utf-8')) <= 1024:
        _unsupported()
    return ref


def _nested(record):
    if 'components' in record:
        if not isinstance(record['components'], list):
            _unsupported()
        if record['components']:
            raise SbomFailure('sbom_nested_population_unsupported')


def _containers(record):
    # Only these correspondence-bearing containers are interpreted later.
    for key, expected in (('properties', list), ('evidence', dict), ('pedigree', dict)):
        if key in record and not isinstance(record[key], expected):
            _unsupported()


def accept_document(snapshot):
    root = decode_document(snapshot.data)
    if (root.get('bomFormat') != 'CycloneDX' or root.get('specVersion') != '1.5'
            or set(root) - ROOT_FIELDS):
        _unsupported()
    version = root.get('version', 1)
    if type(version) is not int or version < 1:
        _unsupported()
    metadata = root.get('metadata')
    subject = metadata.get('component') if isinstance(metadata, dict) else None
    if (not isinstance(subject, dict) or not isinstance(subject.get('name'), str)
            or not subject['name'] or not isinstance(subject.get('bom-ref'), str)
            or not 1 <= len(subject['bom-ref'].encode('utf-8')) <= 1024):
        raise SbomFailure('sbom_subject_unavailable')
    components = root.get('components')
    services = root.get('services', [])
    if not isinstance(components, list) or not isinstance(services, list):
        _unsupported()
    if len(components) > MAX_COMPONENTS or len(services) > MAX_SERVICES:
        raise SbomFailure('sbom_budget_exceeded')
    if any(not isinstance(record, dict) for record in components + services):
        _unsupported()
    _nested(subject)
    _containers(root)
    _containers(metadata)
    _containers(subject)
    if 'formulation' in root and not isinstance(root['formulation'], list):
        _unsupported()
    refs = {subject['bom-ref']}
    aliases = 0
    records = []
    for index, record in enumerate(components):
        _nested(record)
        _containers(record)
        ref = _reference(record)
        if ref in refs:
            if ref == subject['bom-ref'] and json.dumps(record, sort_keys=True) == json.dumps(subject, sort_keys=True) and aliases == 0:
                aliases += 1
                continue
            raise SbomFailure('sbom_duplicate_reference')
        if ref is not None:
            refs.add(ref)
        records.append((index, record))
    for service in services:
        ref = _reference(service)
        if ref in refs:
            raise SbomFailure('sbom_duplicate_reference')
        if ref is not None:
            refs.add(ref)
    # Graph semantic errors are isolated in sbom_graph. Resource ceilings are
    # whole-source framing limits, including duplicate nodes/edges.
    graph = root.get('dependencies')
    if isinstance(graph, list):
        if len(graph) > MAX_NODES:
            raise SbomFailure('sbom_budget_exceeded')
        edges = sum(len(node['dependsOn']) for node in graph
                    if isinstance(node, dict) and isinstance(node.get('dependsOn'), list))
        if edges > MAX_EDGES:
            raise SbomFailure('sbom_budget_exceeded')
    return SbomDocument(snapshot, root, subject, tuple(records), tuple(services), aliases)


def safe_display(value):
    """Public assertion labels only; canonical Maven identity has its own grammar."""
    import re
    if (not isinstance(value, str) or not 1 <= len(value) <= 128
            or not value.isascii() or not value.isprintable()
            or any(character in value for character in '/\\@`$;&|<>(){}')
            or re.match(r'[A-Za-z][A-Za-z0-9+.-]*:', value)):
        return None
    return value


def document_assertions(document):
    from datetime import datetime, timezone
    import re
    root = document.root
    def assertion(container, key, convert):
        if key not in container:
            return {'value': None, 'status': 'absent'}
        value = convert(container[key])
        return {'value': value, 'status': 'available' if value is not None else 'invalid'}
    def serial(value):
        if isinstance(value, str) and re.fullmatch(r'urn:uuid:[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}', value):
            return value
        return None
    def created(value):
        if (not isinstance(value, str) or not re.fullmatch(
                r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})', value)):
            return None
        try:
            # fromisoformat accepts out-of-range offset minutes by normalization.
            if value[-1] != 'Z' and (int(value[-5:-3]) > 23 or int(value[-2:]) > 59):
                return None
            return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
        except (ValueError, OverflowError):
            return None
    serial_value = assertion(root, 'serialNumber', serial)
    created_value = assertion(root['metadata'], 'timestamp', created)
    producer = {'state': 'absent', 'tools': [], 'tools_omitted': 0}
    tools = root['metadata'].get('tools', [])
    if isinstance(tools, dict):
        tools = tools.get('components')
    if not isinstance(tools, list) or any(not isinstance(tool, dict) for tool in tools):
        producer['state'] = 'redacted'
    else:
        producer['tools_omitted'] = max(0, len(tools) - 32)
        for tool in tools[:32]:
            name = safe_display(tool.get('name'))
            version = safe_display(tool.get('version')) if 'version' in tool else None
            status = 'available' if name is not None and ('version' not in tool or version is not None) else 'redacted'
            producer['tools'].append({'name': name, 'version': version, 'status': status})
        if tools:
            producer['state'] = 'redacted' if producer['tools_omitted'] or any(t['status'] == 'redacted' for t in producer['tools']) else 'available'
    compositions = root.get('compositions', [])
    allowed = {'complete', 'incomplete', 'incomplete_first_party_only',
               'incomplete_third_party_only', 'unknown', 'not_specified'}
    if not isinstance(compositions, list) or any(not isinstance(c, dict) or not isinstance(c.get('aggregate'), str) or c['aggregate'] not in allowed for c in compositions):
        composition = {'state': 'unsupported', 'aggregates': []}
    elif compositions:
        composition = {'state': 'asserted', 'aggregates': sorted({c['aggregate'] for c in compositions})}
    else:
        composition = {'state': 'absent', 'aggregates': []}
    return serial_value, created_value, producer, composition
