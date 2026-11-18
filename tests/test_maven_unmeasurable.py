"""Ordinary refusal rows preserve evidence; they never define population scope."""

from copy import deepcopy
from dataclasses import replace
import json
import unittest

from libyears.maven import MavenScanReport
from libyears.maven_model import MavenCollection, MavenDiscovery, MavenReason, MavenView
from libyears.maven_output import _maven_data_human_lines, maven_human_lines, maven_to_dict
from libyears.maven_results import summarize_sources
from test_maven_model import occurrence, paired_source_fixture
from test_maven_table import measured, report_for, table


def unmeasurable(source='pom.xml', artifact='example', *, version=None, request=None,
                 reason=MavenReason.UNSUPPORTED_VERSION, kind='jar', classifier=None):
    row = occurrence(source, artifact)
    key = replace(row.key, model_key=replace(row.key.model_key, type=kind, classifier=classifier))
    fact = replace(row.declared, version=version, request=request, reason=reason)
    return replace(row, key=key, declared=fact)


def refusal_table(lines):
    start = lines.index('Unmeasurable') + 1
    result = []
    for line in lines[start:]:
        if line.startswith(('  Declared unmeasurable:', '  Observed unmeasurable:',
                            'Declared: static', 'Central correspondence')):
            break
        result.append(line)
    return result


class MavenUnmeasurableTests(unittest.TestCase):
    def test_mixed_rows_keep_identity_multiplicity_and_measured_zeros(self):
        rows = [measured('a/pom.xml', 'current', value=0.0),
                unmeasurable('a/pom.xml', 'same'), unmeasurable('b/pom.xml', 'same'),
                unmeasurable('a/pom.xml', 'same', kind='test-jar'),
                unmeasurable('a/pom.xml', 'same', classifier='tests'),
                unmeasurable('a/pom.xml', 'same', kind='test-jar', classifier='tests')]
        lines = maven_human_lines(report_for(rows, population_known=False))
        self.assertEqual(len(table(lines)), 2)
        self.assertTrue(table(lines)[1].endswith('0.000'))
        refusals = refusal_table(lines)
        self.assertEqual(len(refusals), 6)
        self.assertEqual(len(set(refusals[1:])), 5)
        self.assertEqual(sum('type=test-jar' in line for line in refusals), 2)
        self.assertEqual(sum('classifier=tests' in line for line in refusals), 2)
        self.assertNotIn('type=jar', '\n'.join(refusals))
        self.assertIn('Declared unmeasurable: 5', '\n'.join(lines))

    def test_exact_version_request_only_and_unavailable_are_distinguished_with_faithful_reasons(self):
        rows = [unmeasurable(artifact='exact', version='1.2.3', request='[1,2)', reason=MavenReason.UNSUPPORTED_MODEL),
                unmeasurable(artifact='request', request='[1,2)'), unmeasurable(artifact='missing'),
                unmeasurable(artifact='catalogue', version='2.0', reason=MavenReason.CATALOGUE_UNAVAILABLE)]
        lines = refusal_table(maven_human_lines(report_for(rows)))
        by_artifact = {name: next(line for line in lines if 'org.example:' + name in line)
                       for name in ('exact', 'request', 'missing', 'catalogue')}
        self.assertIn('version: 1.2.3', by_artifact['exact'])
        self.assertNotIn('[1,2)', by_artifact['exact'])
        self.assertIn('supported local model fact unavailable', by_artifact['exact'])
        self.assertNotIn('scope', by_artifact['exact'])
        self.assertIn('request: [1,2)', by_artifact['request'])
        self.assertIn('exact declared version unavailable', by_artifact['request'])
        self.assertIn('unavailable', by_artifact['missing'])
        self.assertIn('version: 2.0', by_artifact['catalogue'])
        self.assertIn('current GA catalogue unavailable', by_artifact['catalogue'])

    def test_long_fully_escaped_cells_and_headers_align_without_truncation(self):
        row = unmeasurable('long-module-name/pom.xml', 'long-library-coordinate', request='[1234567890,2345678901)')
        report = report_for([row, unmeasurable('a/pom.xml', 'short')])
        data = maven_to_dict(report)
        long = next(r for r in data['occurrences'] if r['key']['artifact_id']=='long-library-coordinate')
        long['key'].update(source_id='long-module\n\t\x1b\\\u2603/pom.xml', classifier='tests\n"')
        long['declared']['request'] = '[1234567890,2345678901)\t"\\\u2603'
        lines = refusal_table(_maven_data_human_lines(data))
        starts = [lines[0].index(h) for h in ('MODULE', 'DEPENDENCY', 'DECLARED', 'REASON')]
        for line, record in zip(lines[1:], data['occurrences']):
            identity = record['key']['group_id'] + ':' + record['key']['artifact_id']
            if record['key']['classifier'] is not None:
                identity += ' classifier=' + record['key']['classifier']
            value = ('request: ' + record['declared']['request']) if record['declared']['request'] is not None else 'unavailable'
            cells = [json.dumps(record['key']['source_id'], ensure_ascii=True),
                     json.dumps(identity, ensure_ascii=True)[1:-1], json.dumps(value, ensure_ascii=True)[1:-1]]
            for start, cell in zip(starts, cells):
                self.assertEqual(line[start:start+len(cell)], cell)
        text = ''.join(lines)
        self.assertTrue(all(32 <= ord(c) < 127 for c in text))
        for escaped in ('\\n', '\\t', '\\u001b', '\\u2603', '\\"', '\\\\'):
            self.assertIn(escaped, text)
        self.assertIn('1234567890,2345678901', text)

    def test_all_unmeasurable_empty_and_source_uncertainty_do_not_create_a_denominator(self):
        for complete in (True, False):
            report = report_for([unmeasurable(artifact='first'), unmeasurable(artifact='second')],
                                population_known=False, complete=complete)
            lines = maven_human_lines(report)
            self.assertEqual(len(refusal_table(lines)), 3)
            self.assertIn('unknown', next(line for line in lines if line.startswith('Coverage')))
            self.assertIsNone(report.summaries.declared.summary.dependencies_discovered)
            self.assertIsNone(report.summaries.declared.summary.coverage)
        report = report_for([], population_known=False, complete=False, accepted=False)
        lines = maven_human_lines(report)
        self.assertNotIn('Unmeasurable', lines)
        self.assertFalse(any(line.startswith('MODULE  ') for line in lines))
        self.assertIn('Discovery incomplete:', '\n'.join(lines))
        self.assertIn('Declared: unavailable', '\n'.join(lines))
        self.assertNotIn('Unmeasurable', maven_human_lines(report_for([])))

    def test_unavailable_observed_is_section_level_and_actual_observed_stays_independent(self):
        normal = '\n'.join(maven_human_lines(report_for([unmeasurable(artifact='one'), unmeasurable(artifact='two')])))
        self.assertEqual(normal.count('Observed is unavailable:'), 1)
        self.assertNotIn('| Observed: unavailable', normal)
        source = paired_source_fixture()
        row = source.declared.rows[0]
        row = replace(row, declared=replace(row.declared, age=None, reason=MavenReason.CATALOGUE_UNAVAILABLE))
        source = replace(source, declared=replace(source.declared, rows=(row,)),
                         observed=replace(source.observed, rows=(row,)))
        report = MavenScanReport(MavenDiscovery(True, ('pom.xml',)), (source,), summarize_sources((source,)))
        lines = maven_human_lines(report)
        self.assertIn('Observed: 3 / 2.000 libyears', '\n'.join(lines))
        self.assertIn('version: 1', '\n'.join(refusal_table(lines)))
        self.assertEqual(report.summaries.observed.summary.dependencies_measured, 1)
        self.assertEqual(report.summaries.declared.summary.dependencies_measured, 0)
        observed_only = replace(source, declared=MavenCollection(MavenView.DECLARED, None, (), False, MavenReason.UNSUPPORTED_MODEL))
        report = replace(report, sources=(observed_only,), summaries=summarize_sources((observed_only,)))
        self.assertNotIn('Unmeasurable', maven_human_lines(report))
        self.assertIn('Observed: 3 / 2.000 libyears', '\n'.join(maven_human_lines(report)))

    def test_json_raw_statistics_verbose_and_request_sanitization_survive(self):
        report = report_for([measured(), unmeasurable(artifact='missing', request='${missing}'),
                            unmeasurable(artifact='unsafe', request='https://private.invalid/example')],
                           population_known=False, complete=False)
        original = deepcopy(report)
        serialized = json.dumps(maven_to_dict(report), sort_keys=True)
        verbose = maven_human_lines(report, verbose=True)
        normal = '\n'.join(maven_human_lines(report))
        self.assertIn('request: ${missing}', normal)
        self.assertNotIn('private.invalid', normal)
        self.assertEqual(report, original)
        self.assertEqual(json.dumps(maven_to_dict(report), sort_keys=True), serialized)
        self.assertEqual(maven_human_lines(report, verbose=True), verbose)
        self.assertNotIn('Unmeasurable', verbose)
