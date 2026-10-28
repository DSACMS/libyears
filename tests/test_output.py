import json
import unittest
from dataclasses import replace
from datetime import datetime, timezone

from libyears.model import (Dependency, DependencyMeasurement, MetricSummary,
                            SourceEvidence, SourceError, SourceResult)
from libyears.requirements import UnmeasurableRequirement
from libyears.output import format_human, format_json, report_to_dict
from libyears.scan import MixedScanReport, ScanReport


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
        self.assertEqual(data["schema_version"], 3)
        self.assertNotIn("repository", data)
        self.assertEqual(
            data["version_evidence"],
            {"pypi": {"declaration_source": "requirements.txt", "snapshot_source": None}},
        )
        self.assertEqual(data["summary"]["coverage"], 2 / 3)
        self.assertEqual(data["dependencies"][0]["used_release_time"], "2023-01-01T00:00:00Z")
        self.assertIsInstance(data["dependencies"][0]["libyears"], float)
        self.assertEqual(data["dependencies"][0]["version_source"], "requirements_exact")
        self.assertEqual(data["unmeasurable"][0]["reason"], "non_exact_version")
        self.assertEqual(data["summary"]["by_ecosystem"]["pypi"]["coverage"], 2 / 3)
        self.assertEqual(data["source_errors"], [])

    def test_json_with_snapshot_reports_v2_evidence_and_source(self):
        report = ScanReport(
            MetricSummary(1, 1, 1.0, 1.0, 1.0, 1.0, 1.0),
            (
                DependencyMeasurement(
                    Dependency(
                        "pypi", "requests", "2.31.0",
                        datetime(2023, 1, 1, tzinfo=timezone.utc),
                        "2.32.0", datetime(2024, 1, 1, tzinfo=timezone.utc),
                        "resolved_snapshot",
                    ),
                    1.0,
                ),
            ),
            (),
            "resolved.txt",
        )
        data = json.loads(format_json(report, "."))
        self.assertEqual(data["schema_version"], 3)
        self.assertEqual(
            data["version_evidence"]["pypi"]["snapshot_source"],
            {"format": "pip_freeze_exact", "path": "resolved.txt"},
        )
        self.assertEqual(data["dependencies"][0]["version_source"], "resolved_snapshot")

    def test_schema_v3_supports_npm_and_mixed_source_evidence(self):
        summary = MetricSummary(1, 0, 0.0, 0.0, None, None, None)
        npm = SourceResult(
            "npm", (), (), (), SourceEvidence("package.json", "package-lock.json"),
            dependencies_discovered=0, measurement_available=True,
        )
        pypi = SourceResult(
            "pypi", (), (), (), SourceEvidence("requirements.txt", None),
            dependencies_discovered=0, measurement_available=True,
        )
        for sources, expected in (((npm,), ["npm"]), ((pypi,), ["pypi"]), ((npm, pypi), ["npm", "pypi"])):
            report = MixedScanReport((), (), (), sources, summary,
                                     {source.ecosystem: summary for source in sources})
            data = json.loads(format_json(report, "."))
            self.assertEqual(data["schema_version"], 3)
            self.assertEqual(data["ecosystems"], expected)
            self.assertEqual(set(data["version_evidence"]), set(expected))
            self.assertEqual(set(data["summary"]["by_ecosystem"]), set(expected))

    def test_yarn_format_is_additive_and_existing_evidence_is_unchanged(self):
        summary = MetricSummary(1, 1, 1.0, 0.0, 0.0, 0.0, 0.0)
        original = report_with_data().measurements[0].dependency
        for ecosystem, snapshot, version_source, evidence_format, include_format in (
            ("npm", "yarn.lock", "yarn_lock", "yarn_lock_v1", True),
            ("npm", "package-lock.json", "package_lock", None, False),
            ("pypi", None, "requirements_exact", None, False),
        ):
            with self.subTest(ecosystem=ecosystem, snapshot=snapshot):
                declaration = "package.json" if ecosystem == "npm" else "requirements.txt"
                source = SourceResult(
                    ecosystem, (), (), (),
                    SourceEvidence(declaration, snapshot, evidence_format, include_format),
                    dependencies_discovered=1, measurement_available=True,
                )
                dependency = replace(original, ecosystem=ecosystem, version_source=version_source)
                report = MixedScanReport(
                    (DependencyMeasurement(dependency, 0.0),), (), (), (source,),
                    summary, {ecosystem: summary},
                )
                data = report_to_dict(report, ".")
                expected = {"declaration_source": declaration, "snapshot_source": snapshot}
                if include_format:
                    expected["format"] = evidence_format
                self.assertEqual(data["version_evidence"], {ecosystem: expected})
                self.assertNotIn("rubygems_evidence", data["dependencies"][0])
                self.assertNotIn("scope", data["version_evidence"][ecosystem])
                self.assertNotIn("publication_basis", data["version_evidence"][ecosystem])
                self.assertEqual(data["schema_version"], 3)
                self.assertEqual(data["dependencies"][0]["version_source"], version_source)
                if version_source == "yarn_lock":
                    self.assertIn("yarn.lock", format_human(report, "."))
                    python_source = replace(source, ecosystem="pypi", evidence=SourceEvidence("requirements.txt", None))
                    mixed = replace(report, source_results=(source, python_source))
                    self.assertIn("yarn.lock", format_human(mixed, "."))

    def test_schema_v3_keeps_source_failure_distinct_from_dependency_rows(self):
        summary = MetricSummary(None, 0, None, 0.0, None, None, None)
        source = SourceResult(
            "npm", (), (), (SourceError("npm", "package.json", "invalid_manifest"),),
            SourceEvidence("package.json", "package-lock.json"),
            dependencies_discovered=None, measurement_available=False,
        )
        report = MixedScanReport((), (), source.source_errors, (source,), summary, {"npm": summary})
        data = json.loads(format_json(report, "."))
        self.assertEqual(data["source_errors"], [{"ecosystem": "npm", "source": "package.json", "reason": "invalid_manifest"}])
        self.assertEqual(data["unmeasurable"], [])

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
        self.assertIn("exact version not available", output)
        self.assertNotIn("non_exact_version", output)
        self.assertNotIn("SOURCE", output)

    def test_human_output_reports_evidence_and_mixed_sources(self):
        report = report_with_data()
        mixed_measurements = (
            report.measurements[0],
            DependencyMeasurement(
                Dependency(
                    "pypi", "newer", "2.0", datetime(2023, 1, 1, tzinfo=timezone.utc),
                    "2.1", datetime(2023, 1, 2, tzinfo=timezone.utc),
                    "resolved_snapshot",
                ),
                0.002,
            ),
        )
        mixed = ScanReport(report.summary, mixed_measurements, report.unmeasurable, "resolved.txt")
        output = format_human(mixed, ".")
        self.assertIn("Version evidence: requirements.txt; resolved snapshot: resolved.txt", output)
        self.assertIn("SOURCE", output)
        self.assertIn("requirements.txt", output)
        self.assertIn("snapshot", output)

    def test_human_output_uses_friendly_snapshot_failure_reasons(self):
        output = format_human(
            ScanReport(
                MetricSummary(4, 0, 0.0, 0.0, None, None, None),
                (),
                tuple(
                    UnmeasurableRequirement("pkg", "pkg", reason)
                    for reason in (
                        "snapshot_version_missing",
                        "snapshot_version_conflict",
                        "snapshot_version_incompatible",
                        "declared_snapshot_conflict",
                    )
                ),
                "resolved.txt",
            ),
            ".",
        )
        for text in (
            "exact version missing from supplied snapshot",
            "conflicting versions in supplied snapshot",
            "snapshot version does not satisfy declaration",
            "snapshot version conflicts with exact repository pin",
        ):
            self.assertIn(text, output)

    def test_human_output_distinguishes_no_supported_dependencies(self):
        report = ScanReport(MetricSummary(0, 0, None, 0.0, None, None, None), (), ())
        output = format_human(report, ".")
        self.assertIn("No supported dependency manifests or dependencies were found.", output)
        self.assertIn("Currently supported ecosystems: pypi", output)
        self.assertIn("No libyears measurement was calculated.", output)
        self.assertNotIn("DEPENDENCY", output)
        self.assertNotIn("Coverage:", output)
        self.assertNotIn("Total:", output)
        self.assertNotIn("failure", output.lower())

    def test_human_output_explains_zero_measurement_from_non_exact_versions(self):
        output = format_human(report_with_unmeasurable("non_exact_version"), ".")
        self.assertIn("No libyears measurement could be calculated", output)
        self.assertIn("All discovered dependencies lack exact versions.", output)
        self.assertIn("reproducible measurement", output)
        self.assertIn("exact version not available", output)
        self.assertNotIn("non_exact_version", output)
        self.assertIn("Measured: 0 / 1 dependencies", output)
        self.assertIn("Coverage: 0.0%", output)
        self.assertNotIn("DEPENDENCY", output)
        self.assertNotIn("Total:", output)

    def test_human_output_distinguishes_partial_measurement(self):
        output = format_human(report_with_data(), ".")
        self.assertIn("Partial measurement: 2 / 3 dependencies measured (66.7%).", output)
        self.assertIn("Total:", output)
        self.assertIn("exact version not available", output)
        self.assertNotIn("non_exact_version", output)

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
        human = format_human(report, ".")
        self.assertNotIn("null", human)
        self.assertNotIn("Coverage:", human)
        self.assertNotIn("Total:", human)


if __name__ == "__main__":
    unittest.main()
