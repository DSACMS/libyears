"""Maven-only plural JSON and paired human disclosure, separate from legacy rows."""

from dataclasses import asdict
from datetime import timezone
import json
import re

from .maven_model import MavenView, MavenVersionBasis
from .maven_results import summarize_collection

LIMITATIONS = (
    'static_base_model_not_evaluated', 'module_occurrence_weighted',
    'correspondence_assumed', 'acquisition_not_established', 'content_not_established',
    'producer_history_not_established', 'runtime_state_not_established',
    'machine_settings_not_inspected',
)
TIME_BASIS = 'maven_conventional_pom_last_modified'

_REASON_TEXT = {
    'maven_discovery_unavailable': 'bounded Maven discovery unavailable',
    'maven_population_unknown': 'external dependency population unknown',
    'maven_unsupported_model': 'supported local model fact unavailable',
    'maven_unsupported_version': 'exact declared version unavailable (unsupported request or unresolved local property/management)',
    'maven_comparator_refused': 'Central comparison refused by local policy or system assignment',
    'maven_policy_unknown': 'unknown or unsupported relevant source policy',
    'maven_policy_input_unavailable': 'safe local policy evidence unavailable',
    'maven_policy_budget_exceeded': 'local source policy budget exceeded',
    'maven_observed_reader_unavailable': 'no accepted Maven retained-selection reader',
    'maven_catalogue_unavailable': 'current GA catalogue unavailable',
    'maven_time_basis_unavailable': 'versioned POM Last-Modified unavailable',
    'maven_metadata_worker_unavailable': 'safe metadata worker unavailable',
    'maven_metadata_budget_exceeded': 'metadata budget exceeded',
    'unknown_latest_eligibility': 'potentially maximal version eligibility unknown',
    'ambiguous_latest_version': 'distinct equivalent latest versions ambiguous',
    'no_stable_release': 'no known eligible stable target',
}


def _timestamp(value):
    return None if value is None else value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def _view(result):
    declared = result.view == MavenView.DECLARED
    return {
        'population_state': result.population_state.value,
        'availability': result.availability.value,
        'reason': result.reasons[0].value if result.reasons else None,
        'reasons': [reason.value for reason in result.reasons],
        'version_basis': (MavenVersionBasis.DECLARED.value if declared else
                          MavenVersionBasis.OBSERVED.value if result.availability != 'unavailable' else None),
        'comparator_basis': 'conventional_central',
        'time_basis': TIME_BASIS,
        'ordering_basis': 'maven_comparable_version_3_9_11',
        'eligibility_policy': 'maven_conservative_stable_v1',
        'limitations': list(LIMITATIONS),
        'summary': asdict(result.summary),
    }


def _request(value):
    # Unsupported requests remain useful only when their text cannot disclose a
    # URL, credential-bearing location, absolute path or arbitrary markup.
    if (value is None or len(value.encode('utf-8')) > 16 * 1024
            or not re.fullmatch(r'[A-Za-z0-9._+*${}\[\](), -]+', value, re.ASCII)):
        return None
    return value


def _fact(fact):
    if fact is None:
        return None
    age = None
    if fact.age is not None:
        age = asdict(fact.age)
        age['limitations'] = list(age['limitations'])
        for name in ('measured_version_pom_last_modified', 'comparison_version_pom_last_modified',
                     'catalogue_retrieved_at'):
            age[name] = _timestamp(age[name])
    return {
        'request': _request(fact.request), 'version': fact.version,
        'version_basis': fact.version_basis.value,
        'evidence_origins': [asdict(origin) for origin in fact.origins],
        'availability': fact.availability.value,
        'age_availability': fact.age_availability.value,
        'reason': fact.reason.value if fact.reason is not None else None,
        'limitations': list(LIMITATIONS), 'age': age,
    }


def maven_to_dict(report):
    sources = []
    occurrences = []
    for source in sorted(report.sources, key=lambda item: item.context.source_id):
        views = {view.value: _view(summarize_collection(getattr(source, view.value))) for view in MavenView}
        sources.append({
            'source_id': source.context.source_id,
            'context': {'context_id': source.context.context_id,
                        'parent_sources': list(source.context.parent_sources)},
            'basis': 'supported_local_base_model_request',
            'limitations': list(LIMITATIONS), 'views': views,
        })
        declared_rows = {row.key: row for row in source.declared.rows}
        observed_rows = {row.key: row for row in source.observed.rows}
        rows = {**declared_rows, **observed_rows}
        for key in sorted(rows, key=lambda k: (k.model_key.group_id, k.model_key.artifact_id,
                                               k.model_key.type, k.model_key.classifier or '')):
            declared = declared_rows[key].declared if key in declared_rows else None
            observed = observed_rows[key].observed if key in observed_rows else None
            row = rows[key]
            occurrences.append({
                'key': {'source_id': key.source_id, 'context_id': key.context_id, **asdict(key.model_key)},
                'artifact_key': asdict(row.artifact_key) if row.artifact_key is not None else None,
                'scope': row.scope, 'optional': row.optional,
                'declared': _fact(declared), 'observed': _fact(observed),
            })
    return {
        'discovery': {'state': 'complete' if report.discovery.complete else 'unavailable',
                      'reason': report.discovery.reason.value if report.discovery.reason is not None else None},
        'sources': sources, 'occurrences': occurrences,
        'views': {view.value: _view(getattr(report.summaries, view.value)) for view in MavenView},
    }


def _count(value, view):
    if value is not None:
        return str(value)
    return 'unavailable' if view['availability'] == 'unavailable' else 'unknown'


def _number(value):
    return 'unavailable' if value is None else f'{value:.3f}'


def maven_human_lines(report, *, verbose=False):
    data = maven_to_dict(report)
    views = data['views']
    lines = ['Conventional Maven dependency age',
             'Time basis: Maven conventional (versioned public POM Last-Modified)',
             'Declared uses static local base-model requests; repeated consumer modules count separately.',
             '', f"{'Measure':28} {'Declared':>18} {'Observed':>18}"]
    for name, label in (('dependencies_discovered', 'Dependencies discovered'),
                        ('dependencies_measured', 'Dependencies measured'),
                        ('coverage', 'Coverage'), ('total_libyears', 'Total libyears'),
                        ('mean_libyears', 'Mean libyears'), ('median_libyears', 'Median libyears'),
                        ('max_libyears', 'Maximum libyears')):
        values = []
        for view in (views['declared'], views['observed']):
            value = view['summary'][name]
            if name.startswith('dependencies_'):
                rendered = _count(value, view)
            elif name == 'coverage':
                rendered = (f'{value:.1%}' if value is not None else 'n/a (empty)' if
                            view['summary']['dependencies_discovered'] == 0 else _count(None, view))
            else:
                rendered = _number(value)
            values.append(rendered)
        lines.append(f'{label:28} {values[0]:>18} {values[1]:>18}')
    for name in ('declared', 'observed'):
        view = views[name]
        reasons = '; '.join(_REASON_TEXT[reason] for reason in view['reasons'])
        lines.append(f"{name.title()}: {view['availability']}" + (f' ({reasons})' if reasons else ''))
    if 'maven_observed_reader_unavailable' in views['observed']['reasons']:
        lines.append('Observed is unavailable: no accepted Maven retained-selection reader.')
    if not report.discovery.complete:
        lines.append('Discovery incomplete: Maven presence/population cannot be certified complete.')
    if (views['declared']['summary']['dependencies_measured'] == 0
            and views['declared']['summary']['dependencies_discovered'] != 0):
        lines.append('No declared ages measured; zero total describes an empty measured subset.')
    if data['sources']:
        lines.append('Sources: ' + ', '.join(json.dumps(s['source_id'], ensure_ascii=True) for s in data['sources']))
    for occurrence in data['occurrences']:
        key = occurrence['key']
        facts = []
        for name in ('declared', 'observed'):
            fact = occurrence[name]
            if fact is None:
                text = 'unavailable'
            else:
                text = fact['version'] or 'unavailable version'
                text += ' / ' + (_number(fact['age']['libyears']) + ' libyears' if fact['age'] is not None
                                 else _REASON_TEXT.get(fact['reason'], 'unavailable age'))
            facts.append(text)
        identity = json.dumps(key['source_id'], ensure_ascii=True) + ' ' + key['group_id'] + ':' + key['artifact_id']
        classifier = key['classifier'] if key['classifier'] is not None else '(absent)'
        identity += f" type={key['type']} classifier={classifier}"
        lines.append(identity + ' | Declared: ' + facts[0] + ' | Observed: ' + facts[1])
    if verbose:
        lines.extend(['', 'Public repository-reported modification times of versioned POM representations are a conventional release-age surrogate.',
                      'First publication, upstream release and classifier availability/compatibility are not established.',
                      'Acquisition, content correspondence, producer history, evaluated and runtime state are not established.',
                      'Machine settings are not inspected; conventional Central correspondence is assumed.'])
        for row in data['occurrences']:
            key = row['key']
            lines.append('  ' + json.dumps(key, ensure_ascii=True, sort_keys=True))
            lines.append(f"    scope: {row['scope']}; optional: {row['optional']}")
            for name in ('declared', 'observed'):
                fact = row[name]
                if fact is None:
                    continue
                lines.append(f"  {name} version_basis: {fact['version_basis']}")
                for origin in fact['evidence_origins']:
                    lines.append('    origin: ' + json.dumps(origin, ensure_ascii=True, sort_keys=True))
                if fact['age'] is not None:
                    age = fact['age']
                    for field in ('comparison_version', 'measured_version_pom_last_modified',
                                  'comparison_version_pom_last_modified', 'catalogue_retrieved_at',
                                  'comparator_basis', 'eligibility_policy', 'timestamp_order_anomaly'):
                        lines.append(f'    {field}: {age[field]}')
                    lines.append('    limitations: ' + ', '.join(age['limitations']))
    return lines
