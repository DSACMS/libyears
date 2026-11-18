"""Ordinary Declared table; these constructed facts grant no measurement work."""

from copy import deepcopy
from dataclasses import replace
import json
import unittest

from libyears.maven import MavenScanReport
from libyears.maven_model import (
    MavenCollection, MavenContext, MavenDiscovery, MavenModelKey,
    MavenReason, MavenSource, MavenView,
)
from libyears.maven_output import _maven_data_human_lines, maven_human_lines, maven_to_dict
from libyears.maven_results import summarize_sources
from test_maven_model import occurrence, paired_source_fixture


def report_for(rows, *, population_known=True, complete=True, accepted=True):
    grouped = {}
    for row in rows:
        grouped.setdefault(row.key.source_id, []).append(row)
    if not grouped:
        grouped['pom.xml'] = []
    sources = []
    for source_id, values in grouped.items():
        collection = MavenCollection(MavenView.DECLARED,
            len(values) if population_known else None, tuple(values), accepted,
            None if accepted else MavenReason.UNSUPPORTED_MODEL)
        sources.append(MavenSource(MavenContext(source_id), collection))
    sources = tuple(sources)
    return MavenScanReport(MavenDiscovery(complete, tuple(grouped),
        None if complete else MavenReason.DISCOVERY_UNAVAILABLE), sources,
        summarize_sources(sources, discovery_complete=complete))


def measured(source='pom.xml', artifact='example', *, version='1', latest='2', value=1.0,
             kind='jar', classifier=None):
    row = occurrence(source, artifact, value)
    key = replace(row.key, model_key=MavenModelKey('org.example', artifact, kind, classifier))
    fact = replace(row.declared, version=version, age=replace(row.declared.age, comparison_version=latest))
    return replace(row, key=key, declared=fact)


def table(lines):
    start = next(i for i, line in enumerate(lines) if line.startswith('MODULE  '))
    result = []
    for line in lines[start:]:
        if line.startswith(('  Declared unmeasurable:', '  Observed unmeasurable:',
                            'Declared: static', 'Central correspondence')):
            break
        result.append(line)
    return result


class MavenOrdinaryTableTests(unittest.TestCase):
    def test_header_and_fully_rendered_long_cells_determine_alignment(self):
        rows = [measured('z-long-module-name/pom.xml', 'long-library-coordinate',
                         version='1234567890.1234567890', latest='2345678901.2345678901', value=1234.6789),
                measured('a/pom.xml', 'tiny', value=0.0),
                measured('b/pom.xml', 'other', version='9', latest='10', value=0.459338511)]
        lines = table(maven_human_lines(report_for(rows)))
        headers = ['MODULE', 'DEPENDENCY', 'DECLARED', 'LATEST', 'LIBYEARS']
        starts = [lines[0].index(header) for header in headers]
        expected = [
            ['"a/pom.xml"', 'org.example:tiny', '1', '2', '0.000'],
            ['"b/pom.xml"', 'org.example:other', '9', '10', '0.459'],
            ['"z-long-module-name/pom.xml"', 'org.example:long-library-coordinate',
             '1234567890.1234567890', '2345678901.2345678901', '1234.679'],
        ]
        # Source sorting is the existing serializer's order; no table reordering.
        self.assertEqual(len(lines), 4)
        for line, cells in zip(lines[1:], expected):
            for start, cell in zip(starts[:-1], cells[:-1]):
                self.assertEqual(line[start:start + len(cell)], cell)
            self.assertTrue(line.endswith(cells[-1]))
            self.assertEqual(len(line), len(lines[0]))
        short = table(maven_human_lines(report_for([measured(value=0.0)])))
        self.assertEqual(short[0], 'MODULE     DEPENDENCY           DECLARED  LATEST  LIBYEARS')
        self.assertTrue(short[1].endswith('     0.000'))
        self.assertNotIn('USED', short[0])

    def test_repeated_modules_zeros_and_exact_identity_decorations_survive(self):
        rows = [measured('a/pom.xml', 'same', value=0.0),
                measured('b/pom.xml', 'same', value=0.0),
                measured('a/pom.xml', 'same', kind='test-jar'),
                measured('a/pom.xml', 'same', classifier='tests'),
                measured('a/pom.xml', 'same', kind='test-jar', classifier='tests')]
        result = table(maven_human_lines(report_for(rows)))
        self.assertEqual(len(result), 6)
        self.assertEqual(sum(line.rstrip().endswith('0.000') for line in result), 2)
        self.assertEqual(sum('type=test-jar' in line for line in result), 2)
        self.assertEqual(sum('classifier=tests' in line for line in result), 2)
        self.assertNotIn('type=jar', '\n'.join(result))
        self.assertNotIn('(absent)', '\n'.join(result))
        self.assertEqual(len(set(result[1:])), 5)
        self.assertEqual(report_for(rows).summaries.declared.summary.dependencies_measured, 5)

    def test_all_text_cells_escape_controls_quotes_backslashes_and_unicode_before_widths(self):
        row = measured('module"\u2603/pom.xml', 'library\n\t\x1b[31m"\\\u2603',
                       version='1\n\t"\\\u2603', latest='2\r\x1b"\\\u2603',
                       kind='test-jar\n', classifier='tests\t')
        data = maven_to_dict(report_for([row]))
        # Source identities reject C0 controls at construction; retained projections
        # still exercise escaping of every rendered cell, including source cells.
        data['occurrences'][0]['key']['source_id'] = 'module\n\t\x1b/pom.xml'
        lines = table(_maven_data_human_lines(data))
        self.assertEqual(len(lines), 2)
        self.assertTrue(all(ord(c) >= 32 and ord(c) < 127 for c in ''.join(lines)))
        for escaped in ('\\n', '\\t', '\\r', '\\u001b', '\\u2603', '\\"', '\\\\'):
            self.assertIn(escaped, lines[1])
        self.assertEqual(len(lines[0]), len(lines[1]))

    def test_empty_all_unmeasurable_unavailable_and_partial_keep_disclosures_and_counts(self):
        empty = maven_human_lines(report_for([]))
        self.assertFalse(any(line.startswith('MODULE  ') for line in empty))
        unavailable = maven_human_lines(report_for([], accepted=False, population_known=False))
        self.assertIn('Declared: unavailable', '\n'.join(unavailable))
        failed = [occurrence('pom.xml', 'first'), occurrence('pom.xml', 'second')]
        all_failed = maven_human_lines(report_for(failed))
        self.assertFalse(any(line.startswith('MODULE  ') for line in all_failed))
        self.assertIn('Declared unmeasurable: 2', '\n'.join(all_failed))
        self.assertIn('No declared ages measured;', '\n'.join(all_failed))
        partial = maven_human_lines(report_for([*failed, measured(value=0.0)], population_known=False, complete=False))
        self.assertEqual(len(table(partial)), 2)
        self.assertIn('Declared unmeasurable: 2', '\n'.join(partial))
        self.assertIn('Discovery incomplete:', '\n'.join(partial))
        self.assertIn('unknown', next(line for line in partial if line.startswith('Coverage')))
        self.assertEqual(sum(line.startswith('Observed is unavailable:') for line in partial), 1)
        self.assertNotIn('| Observed: unavailable', '\n'.join(partial))
        self.assertIn('not establish first publication', '\n'.join(partial))

    def test_existing_observed_only_and_dual_view_rendering_is_not_relabeled_or_dropped(self):
        source = paired_source_fixture()
        for paired in (True, False):
            selected = source
            if not paired:
                selected = replace(source, declared=MavenCollection(MavenView.DECLARED, None, (), False,
                    MavenReason.UNSUPPORTED_MODEL))
            report = MavenScanReport(MavenDiscovery(True, ('pom.xml',)), (selected,),
                                     summarize_sources((selected,)))
            lines = maven_human_lines(report)
            text = '\n'.join(lines)
            self.assertIn('Observed: 3 / 2.000 libyears', text)
            self.assertIn('Declared: 1 / 1.000 libyears' if paired else 'Declared: unavailable', text)
            self.assertNotIn('Observed is unavailable:', text)
            self.assertFalse(any(line.startswith('MODULE  ') for line in lines))
            self.assertEqual(report.summaries.observed.summary.total_libyears, 2.0)
            self.assertEqual(report.summaries.declared.summary.total_libyears, 1.0 if paired else None)

    def test_unmeasured_observed_version_and_refusal_remain_visible(self):
        source = paired_source_fixture()
        observed = replace(source.observed.rows[0].observed, age=None, reason=MavenReason.COMPARATOR_REFUSED)
        row = replace(source.observed.rows[0], observed=observed)
        source = replace(source, observed=replace(source.observed, rows=(row,)))
        report = MavenScanReport(MavenDiscovery(True, ('pom.xml',)), (source,), summarize_sources((source,)))
        text = '\n'.join(maven_human_lines(report))
        self.assertIn('Observed: 3 / Central comparison refused', text)
        self.assertIn('Observed unmeasurable: 1', text)

    def test_presentation_leaves_json_summaries_and_verbose_evidence_exactly_unchanged(self):
        row = replace(measured(), management_status='accepted')
        report = report_for([row], population_known=False, complete=False)
        before = deepcopy(report)
        json_before = json.dumps(maven_to_dict(report), sort_keys=True)
        verbose_before = maven_human_lines(report, verbose=True)
        normal = maven_human_lines(report)
        self.assertIn('External management: explicitly accepted', '\n'.join(normal))
        self.assertEqual(report, before)
        self.assertEqual(json.dumps(maven_to_dict(report), sort_keys=True), json_before)
        self.assertEqual(maven_human_lines(report, verbose=True), verbose_before)
        self.assertIn('| Declared: 1 / 1.000 libyears | Observed: unavailable', '\n'.join(verbose_before))
        self.assertEqual(maven_human_lines(report), normal)
