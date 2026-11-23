"""Explicit whitelist projection and tables; raw document facts never serialize."""

from collections import Counter
import json

from .sbom_document import document_assertions, safe_display
from .sbom_identity import identify

SCOPE = 'sbom_asserted_unique_component_versions'
LIMITATIONS = (
    'sbom_supplier_assertions', 'sbom_completeness_unknown',
    'current_checkout_association_not_established', 'resolved_direct_population_not_established',
    'runtime_deployment_not_established', 'central_correspondence_assumed',
    'coordinate_disclosure_for_admitted_lookups', 'acquisition_content_not_established',
    'publication_history_not_established', 'variant_availability_not_established',
)
SUMMARY_KEYS = ('dependencies_discovered', 'dependencies_measured', 'coverage',
                'total_libyears', 'mean_libyears', 'median_libyears', 'max_libyears')


def _identity(identity):
    if identity is None:
        return None
    return {name: getattr(identity, name) for name in ('group_id', 'artifact_id', 'version', 'type', 'classifier')}


def _timestamp(value):
    from datetime import timezone
    return value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def _age(age):
    if age is None:
        return None
    result = {key: getattr(age, key) for key in (
        'comparison_version', 'libyears', 'timestamp_order_anomaly', 'comparator_basis',
        'time_basis', 'ordering_basis', 'eligibility_policy',
    )}
    for key in ('measured_version_pom_last_modified', 'comparison_version_pom_last_modified', 'catalogue_retrieved_at'):
        result[key] = _timestamp(getattr(age, key))
    result['limitations'] = list(age.limitations)
    return result


def _counts(reasons):
    return [{'reason': str(reason), 'count': count} for reason, count in sorted(Counter(
        reason for reason in reasons if reason is not None).items())]


def sbom_to_dict(report):
    """A complete SBOM section, independent of any legacy report or summary."""
    if report is None:
        return None
    intake = report.intake
    discovery, selection = intake.discovery, intake.selection
    result = {
        'format_version': 1, 'scope': SCOPE, 'legacy_fields_exclude_sbom': True,
        'state': 'unavailable' if report.document is None else 'available',
        'reason': intake.reason,
        'discovery': {key: getattr(discovery, key) for key in (
            'mode', 'state', 'candidate_count', 'search_complete', 'reason')},
        'selection': {key: getattr(selection, key) for key in ('mode', 'state', 'source_id')},
        'document': None, 'population': None,
        'summary': {key: getattr(report.summary, key) for key in SUMMARY_KEYS},
        'components': [],
        'graph': {'state': 'unknown', 'reason': None, 'subject_id': None,
                  'vertices': [], 'edges': [], 'cycles_present': None},
        'reason_counts': {'source': _counts([intake.reason]), 'components': [], 'graph': []},
        'limitations': list(sorted(LIMITATIONS)),
    }
    if report.document is None:
        return result
    document = report.document
    serial, created, producer, compositions = document_assertions(document)
    subject_name = safe_display(document.subject['name'])
    subject_identity, unused = identify(document.subject)
    result['document'] = {
        'source_id': selection.source_id, 'sha256': document.snapshot.sha256,
        'format': 'CycloneDX', 'spec_version': '1.5',
        'document_version': document.root.get('version', 1),
        'serial_number': serial, 'created': created, 'producer': producer,
        'subject': {'id': 'subject', 'name': subject_name,
                    'name_status': 'available' if subject_name is not None else 'redacted',
                    'identity': _identity(subject_identity)},
        'compositions': compositions,
    }
    redacted = subject_name is None or producer['state'] == 'redacted'
    for member in report.members:
        identity = member.identity
        if identity is not None:
            label, status = identity.group_id + ':' + identity.artifact_id, 'available'
        else:
            label = safe_display(member.records[0][1].get('name'))
            status = 'available' if label is not None else 'redacted'
            label = label if label is not None else f'component #{member.index}'
        redacted |= status == 'redacted'
        result['components'].append({
            'id': member.id, 'identity': _identity(identity), 'label': label, 'label_status': status,
            'version': member.version, 'version_basis': 'sbom_asserted_component_version',
            'record_count': len(member.records),
            'reference_ids': [f'component-ref-{index}' for index, record in member.records if 'bom-ref' in record],
            'relationship': member.relationship, 'direct_path': member.direct_path,
            'transitive_path': member.transitive_path, 'age': _age(member.age),
            'reason': str(member.reason) if member.reason is not None else None,
        })
    graph = report.graph
    result['graph'] = {
        'state': graph.state, 'reason': graph.reason, 'subject_id': graph.subject_id,
        'vertices': [{key: getattr(vertex, key) for key in ('id', 'kind', 'member_id', 'dependencies_known')}
                     for vertex in graph.vertices],
        'edges': [{'from': source, 'to': target} for source, target in graph.edges],
        'cycles_present': graph.cycles_present,
    }
    relationships = Counter(member.relationship for member in report.members)
    result['population'] = {
        'basis': SCOPE, 'inventory_records': len(document.records),
        'subject_aliases_excluded': document.subject_aliases, 'services_excluded': len(document.services),
        'members': len(report.members), 'supported_exact': sum(m.identity is not None for m in report.members),
        'completeness': 'unknown',
        'relationships': {key: relationships[key] for key in ('direct', 'transitive', 'unknown')},
    }
    result['reason_counts']['components'] = _counts(member.reason for member in report.members)
    result['reason_counts']['graph'] = _counts([graph.reason])
    if any(member.reason is not None for member in report.members) or graph.state == 'unavailable':
        result['state'] = 'partial'
    extra = []
    if graph.reason is not None:
        extra.append(graph.reason)
    if compositions['state'] == 'unsupported':
        extra.append('sbom_composition_unsupported')
    if redacted:
        extra.append('sbom_assertion_redacted')
    result['limitations'] = sorted(set(LIMITATIONS) | set(extra))
    return result


def format_sbom_json(report):
    return json.dumps(sbom_to_dict(report), indent=2, ensure_ascii=True, allow_nan=False)


def _cell(value):
    if value is None:
        return 'unavailable'
    # Quotes, backslashes and controls are escaped before measuring table widths.
    return json.dumps(str(value), ensure_ascii=True)[1:-1]


def _table(headers, rows):
    cells = [[_cell(value) for value in row] for row in [headers, *rows]]
    widths = [max(len(row[index]) for row in cells) for index in range(len(headers))]
    return '\n'.join('  '.join(value.ljust(widths[index]) for index, value in enumerate(row)).rstrip()
                     for row in cells)


def _label(row):
    identity = row['identity']
    if identity is None:
        return row['label']
    label = row['label']
    if identity['type'] != 'jar':
        label += ':' + identity['type']
    if identity['classifier'] is not None:
        label += ':' + identity['classifier']
    return label


def _remedy(reason):
    if reason == 'sbom_selection_required':
        return 'Select one file explicitly.'
    if reason.startswith('sbom_identity_'):
        return 'Correct the component identity.'
    if reason.startswith('sbom_version_'):
        return 'Obtain an exact supported component version.'
    if reason in ('sbom_comparator_refused', 'sbom_policy_unknown', 'sbom_variant_unsupported'):
        return 'Supply supported component and comparator evidence.'
    if reason.startswith('sbom_'):
        return 'Supply a supported complete document through safe local input.'
    return 'Retry metadata availability; dates must have supported evidence.'


def format_sbom(report, *, verbose=False):
    section = sbom_to_dict(report)
    if section is None:
        return ''
    lines = ['SBOM dependency age', 'Source: ' + _cell(section['selection']['source_id'])]
    if section['document'] is None:
        lines.append('Unavailable: ' + section['reason'])
        lines.append(_remedy(section['reason']))
    else:
        document, summary = section['document'], section['summary']
        lines.extend(['Format: CycloneDX 1.5', 'Subject: ' + _cell(document['subject']['name']),
                      'Basis: ' + SCOPE,
                      'SBOM population age coverage: ' + _cell(summary['dependencies_measured']) + '/' +
                      _cell(summary['dependencies_discovered']) + ' (' + _cell(summary['coverage']) + ')',
                      'Measured subset libyears: total=' + _cell(summary['total_libyears']) +
                      ' mean=' + _cell(summary['mean_libyears']) + ' median=' + _cell(summary['median_libyears']) +
                      ' max=' + _cell(summary['max_libyears'])])
        measured = [row for row in section['components'] if row['age'] is not None]
        refused = [row for row in section['components'] if row['reason'] is not None]
        lines.append(_table(['DEPENDENCY', 'VERSION', 'RELATION', 'LATEST', 'LIBYEARS', 'SOURCE'], [
            [_label(row), row['version'], row['relationship'], row['age']['comparison_version'],
             row['age']['libyears'], 'SBOM'] for row in measured]))
        if refused:
            lines.extend(['Unmeasurable', _table(['DEPENDENCY', 'VERSION', 'REASON'], [
                [_label(row), row['version'], row['reason']] for row in refused])])
        if section['graph']['reason'] is not None:
            lines.append('Graph: ' + section['graph']['reason'])
    lines.append('Time basis: conventional Maven POM Last-Modified; publication history and variant availability are not established.')
    lines.append('Maven Central correspondence is assumed; admitted coordinates may be disclosed. Current checkout association is not established.')
    for item in section['reason_counts']['components']:
        lines.append(item['reason'] + ': ' + _remedy(item['reason']))
    lines.append('Limitations: ' + ', '.join(section['limitations']))
    if verbose:
        lines.append(json.dumps(section, indent=2, ensure_ascii=True, allow_nan=False))
    return '\n'.join(lines)
