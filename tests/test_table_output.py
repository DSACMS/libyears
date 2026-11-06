"""Human table alignment across legacy, single and mixed ecosystem reports."""

from dataclasses import replace
from datetime import datetime, timezone
import re
import unittest

from libyears.model import (Dependency, DependencyMeasurement, GemfileEvidence,
                            MetricSummary, NuGetEvidence, SourceEvidence,
                            SourceResult, UnmeasurableDependency)
from libyears.output import format_human, report_to_dict
from libyears.nuget import NuGetSourceEvidence
from libyears.requirements import UnmeasurableRequirement
from libyears.scan import MixedScanReport, ScanReport


DATE = datetime(2020, 1, 1, tzinfo=timezone.utc)
SUMMARY = MetricSummary(3, 2, 2 / 3, 12345.0, 6172.5, 6172.5, 12345.0)


def measurements(ecosystem):
    return (
        DependencyMeasurement(Dependency(
            ecosystem, 'very-long-dependency-name-exceeding-old-width',
            '1.0.0-long-version-label', DATE, '2026.11.123456789', DATE,
        ), 12345.0),
        DependencyMeasurement(Dependency(
            ecosystem, 'x', '1', DATE, '2', DATE,
        ), 0.0),
    )


def source(ecosystem):
    evidence = SourceEvidence('manifest', 'lock')
    if ecosystem == 'nuget':
        evidence = NuGetSourceEvidence('App.csproj', 'packages.lock.json')
    return SourceResult(ecosystem, (), (), (), evidence,
                        dependencies_discovered=3, measurement_available=True)


class HumanTableTests(unittest.TestCase):
    def assert_table_alignment(self, output, *, mixed=False, sources=False):
        lines = output.splitlines()
        header = next(line for line in lines if line.startswith('DEPENDENCY'))
        rows = [line for line in lines if line.startswith(('very-long-', 'x '))]
        self.assertEqual(len(rows), 2)
        headers = list(re.finditer(r'\S+', header))
        expected = ['DEPENDENCY', 'USED', 'LATEST', 'LIBYEARS']
        if mixed:
            expected.insert(1, 'ECOSYSTEM')
        if sources:
            expected.append('SOURCE')
        self.assertEqual([match.group() for match in headers], expected)
        for row in rows:
            cells = list(re.finditer(r'\S+', row))
            self.assertEqual(len(cells), len(headers))
            for heading, cell in zip(headers, cells):
                if heading.group() == 'LIBYEARS':
                    self.assertEqual(cell.end(), heading.end())
                else:
                    self.assertEqual(cell.start(), heading.start())
            self.assertNotIn('\t', row)
            self.assertNotIn('\x1b', row)
            self.assertEqual(row, row.rstrip())
        self.assertIn('12345.00', rows[0])
        self.assertIn('0.00', rows[1])
        self.assertIn('very-long-dependency-name-exceeding-old-width', rows[0])
        self.assertIn('1.0.0-long-version-label', rows[0])

    def test_legacy_python_table_and_optional_source_column(self):
        failure = UnmeasurableRequirement('missing', 'missing>=1', 'non_exact_version')
        report = ScanReport(SUMMARY, measurements('pypi'), (failure,))
        self.assert_table_alignment(format_human(report, '.'))
        second = report.measurements[1]
        report = replace(report, measurements=(report.measurements[0], replace(
            second, dependency=replace(second.dependency, version_source='resolved_snapshot'))))
        output = format_human(report, '.')
        self.assert_table_alignment(output, sources=True)
        self.assertIn('missing>=1', output)
        self.assertIn('exact version not available', output)

    def test_single_ecosystem_tables_preserve_failure_and_evidence_details(self):
        for ecosystem in ('pypi', 'npm', 'rubygems', 'nuget'):
            with self.subTest(ecosystem=ecosystem):
                rows = measurements(ecosystem)
                evidence = {}
                if ecosystem == 'rubygems':
                    evidence['gemfile_evidence'] = GemfileEvidence(('test',), ('>=1',))
                if ecosystem == 'nuget':
                    evidence['nuget_evidence'] = NuGetEvidence('App.csproj', 'net10.0', '1.0')
                rows = (replace(rows[0], dependency=replace(rows[0].dependency, **evidence)), rows[1])
                failure = UnmeasurableDependency(ecosystem, 'missing', 'missing', 'lock_version_missing')
                report = MixedScanReport(rows, (failure,), (), (source(ecosystem),),
                                         SUMMARY, {ecosystem: SUMMARY})
                before = report_to_dict(report, '.')
                output = format_human(report, '.')
                self.assert_table_alignment(output)
                self.assertIn('Unmeasurable:', output)
                self.assertIn('missing', output)
                if ecosystem == 'rubygems':
                    self.assertIn('Gemfile declared groups: test', output)
                if ecosystem == 'nuget':
                    self.assertIn('App.csproj', output)
                self.assertEqual(report_to_dict(report, '.'), before)

    def test_mixed_table_aligns_ecosystem_source_and_numeric_columns(self):
        first, second = measurements('rubygems')
        first = replace(first, dependency=replace(first.dependency, version_source='gemfile_lock'))
        second = replace(second, dependency=replace(second.dependency, ecosystem='nuget',
                         version_source='packages_lock'))
        report = MixedScanReport((first, second), (), (),
                                 (source('rubygems'), source('nuget')), SUMMARY,
                                 {'rubygems': SUMMARY, 'nuget': SUMMARY})
        self.assert_table_alignment(format_human(report, '.'), mixed=True, sources=True)

    def test_unmeasurable_only_reports_have_no_numeric_table_or_fake_versions(self):
        summary = MetricSummary(1, 0, 0.0, 0.0, None, None, None)
        legacy = ScanReport(summary, (), (UnmeasurableRequirement(
            'missing', 'missing>=1', 'non_exact_version'),))
        reports = [legacy]
        for ecosystem in ('pypi', 'npm', 'rubygems', 'nuget'):
            reports.append(MixedScanReport((), (UnmeasurableDependency(
                ecosystem, 'missing', 'missing', 'lock_version_missing'),), (),
                (source(ecosystem),), summary, {ecosystem: summary}))
        for report in reports:
            output = format_human(report, '.')
            self.assertNotIn('DEPENDENCY', output)
            self.assertNotIn('None', output)
            self.assertIn('missing', output)


if __name__ == '__main__':
    unittest.main()
