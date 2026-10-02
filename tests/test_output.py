import json
import unittest
from datetime import datetime, timezone

from libyears.model import Dependency, DependencyMeasurement, MetricSummary
from libyears.requirements import UnmeasurableRequirement
from libyears.output import format_human, format_json, report_to_dict
from libyears.scan import ScanReport


def report_with_data():
    utc = timezone.utc
    first = Dependency("pypi", "older", "1.0", datetime(2023, 1, 1, tzinfo=utc), "2.0", datetime(2024, 1, 1, tzinfo=utc))
    second = Dependency("pypi", "newer", "2.0", datetime(2023, 1, 1, tzinfo=utc), "2.1", datetime(2023, 1, 2, tzinfo=utc))
    return ScanReport(
        MetricSummary(3, 2, 2 / 3, 1.002, 0.501, 0.501, 1.0),
        (DependencyMeasurement(first, 1.0), DependencyMeasurement(second, 0.002)),
        (type("Unmeasurable", (), {"ecosystem": "pypi", "name": "missing", "declared": "missing>=1", "reason": "non_exact_version"})(),),
    )


def report_with_unmeasurable(*reasons):
    return ScanReport(
        MetricSummary(len(reasons), 0, 0.0, 0.0, None, None, None),
        (),
        tuple(
            UnmeasurableRequirement("package", f"package=={index}", reason)
            for index, reason in enumerate(reasons, start=1)
        ),
    )


class OutputTests(unittest.TestCase):
    def test_json_matches_schema_and_uses_utc_timestamps(self):
        report = report_with_data()
        rendered = format_json(report, ".")
        data = json.loads(rendered)
        self.assertEqual(data["schema_version"], 1)
        self.assertNotIn("repository", data)
        self.assertEqual(data["summary"]["coverage"], 2 / 3)
        self.assertEqual(data["dependencies"][0]["used_release_time"], "2023-01-01T00:00:00Z")
        self.assertIsInstance(data["dependencies"][0]["libyears"], float)
        self.assertEqual(data["unmeasurable"][0]["reason"], "non_exact_version")

    def test_json_preserves_fractional_seconds_without_adding_them(self):
        report = report_with_data()
        dependency = report.measurements[0].dependency
        dependency_with_fraction = Dependency(
            dependency.ecosystem,
            dependency.name,
            dependency.used_version,
            dependency.used_release_time.replace(microsecond=123400),
            dependency.latest_stable_version,
            dependency.latest_stable_release_time,
        )
        report = ScanReport(
            report.summary,
            (DependencyMeasurement(dependency_with_fraction, 1.0),),
            report.unmeasurable,
        )
        data = report_to_dict(report, ".")
        self.assertEqual(data["dependencies"][0]["used_release_time"], "2023-01-01T00:00:00.123400Z")
        self.assertEqual(data["dependencies"][0]["latest_stable_release_time"], "2024-01-01T00:00:00Z")

    def test_human_output_sorts_by_libyears_and_includes_summary(self):
        output = format_human(report_with_data(), ".")
        self.assertLess(output.index("older"), output.index("newer"))
        self.assertIn("Measured: 2 / 3 dependencies", output)
        self.assertIn("Coverage: 66.7%", output)
        self.assertIn("non_exact_version", output)

    def test_human_output_distinguishes_no_supported_dependencies(self):
        report = ScanReport(MetricSummary(0, 0, None, 0.0, None, None, None), (), ())
        output = format_human(report, ".")
        self.assertIn("No supported dependency manifests or dependencies were found.", output)
        self.assertIn("Currently supported ecosystems: pypi", output)
        self.assertNotIn("failure", output.lower())

    def test_human_output_explains_zero_measurement_from_non_exact_versions(self):
        output = format_human(report_with_unmeasurable("non_exact_version"), ".")
        self.assertIn("No libyears measurement could be calculated", output)
        self.assertIn("All discovered dependencies lack exact versions.", output)
        self.assertIn("reproducible measurement", output)
        self.assertIn("exact version not available (non_exact_version)", output)

    def test_human_output_distinguishes_partial_measurement(self):
        output = format_human(report_with_data(), ".")
        self.assertIn("Partial measurement: 2 / 3 dependencies measured (66.7%).", output)
        self.assertIn("Total:", output)
        self.assertIn("non_exact_version", output)

    def test_human_output_distinguishes_complete_measurement(self):
        report = report_with_data()
        complete = ScanReport(
            MetricSummary(2, 2, 1.0, 1.002, 0.501, 0.501, 1.0),
            report.measurements,
            (),
        )
        output = format_human(complete, ".")
        self.assertIn("Measurement complete: 2 / 2 dependencies measured.", output)
        self.assertNotIn("Partial measurement", output)

    def test_zero_report_uses_null_values_where_required(self):
        report = ScanReport(MetricSummary(0, 0, None, 0.0, None, None, None), (), ())
        data = report_to_dict(report, ".")
        self.assertIsNone(data["summary"]["coverage"])
        self.assertIsNone(data["summary"]["mean_libyears"])
        self.assertEqual(format_human(report, ".").count("null"), 4)


if __name__ == "__main__":
    unittest.main()
