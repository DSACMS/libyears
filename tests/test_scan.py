import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from libyears.pypi import PyPIResult, RegistryFailure
from libyears.scan import scan_repository


UTC = timezone.utc


def timestamp(day: int) -> datetime:
    return datetime(2024, 1, day, tzinfo=UTC)


class FakeAdapter:
    def __init__(self, results):
        self.results = results
        self.calls = []

    def lookup(self, name, version):
        self.calls.append((name, version))
        return self.results[name]


class ScanTests(unittest.TestCase):
    def scan(self, content, adapter):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "requirements.txt").write_text(content, encoding="utf-8")
            return scan_repository(root, adapter=adapter)

    def test_mixed_dependencies_preserve_unmeasurable_and_calculate_summary(self):
        adapter = FakeAdapter({
            "old-package": PyPIResult(
                "old-package", "1.0", timestamp(1), "2.0", timestamp(3)
            ),
            "failed-package": RegistryFailure("failed-package", "1.0", "package_not_found"),
        })
        report = self.scan(
            "old-package==1.0\n"
            "failed-package==1.0\n"
            "flexible-package>=2.0\n",
            adapter,
        )
        self.assertEqual(adapter.calls, [("old-package", "1.0"), ("failed-package", "1.0")])
        self.assertEqual(report.summary.dependencies_discovered, 3)
        self.assertEqual(report.summary.dependencies_measured, 1)
        self.assertAlmostEqual(report.summary.coverage, 1 / 3)
        self.assertAlmostEqual(report.summary.total_libyears, 2 / 365.25)
        self.assertAlmostEqual(report.summary.mean_libyears, 2 / 365.25)
        self.assertAlmostEqual(report.summary.median_libyears, 2 / 365.25)
        self.assertAlmostEqual(report.summary.max_libyears, 2 / 365.25)
        self.assertEqual(
            {item.reason for item in report.unmeasurable},
            {"package_not_found", "non_exact_version"},
        )

    def test_registry_failure_does_not_abort_other_packages(self):
        adapter = FakeAdapter({
            "broken": RegistryFailure("broken", "1.0", "registry_error"),
            "good": PyPIResult("good", "1.0", timestamp(1), "1.1", timestamp(2)),
        })
        report = self.scan("broken==1.0\ngood==1.0\n", adapter)
        self.assertEqual(len(report.measurements), 1)
        self.assertEqual(report.measurements[0].dependency.name, "good")
        self.assertEqual(report.unmeasurable[0].reason, "registry_error")

    def test_zero_dependencies_have_null_coverage_and_empty_measurement_statistics(self):
        adapter = FakeAdapter({})
        report = self.scan("# no dependencies\n\n", adapter)
        self.assertEqual(report.summary.dependencies_discovered, 0)
        self.assertEqual(report.summary.dependencies_measured, 0)
        self.assertIsNone(report.summary.coverage)
        self.assertEqual(report.summary.total_libyears, 0.0)
        self.assertIsNone(report.summary.mean_libyears)
        self.assertIsNone(report.summary.median_libyears)
        self.assertIsNone(report.summary.max_libyears)
        self.assertEqual(report.measurements, ())
        self.assertEqual(report.unmeasurable, ())

    def test_missing_requirements_file_is_an_empty_scan(self):
        with tempfile.TemporaryDirectory() as directory:
            report = scan_repository(directory, lookup=lambda name, version: None)
        self.assertEqual(report.summary.dependencies_discovered, 0)

    def test_original_name_is_retained_for_measured_dependency(self):
        adapter = FakeAdapter({
            "my-package": PyPIResult("my-package", "1.0", timestamp(1), "1.1", timestamp(2))
        })
        report = self.scan("My_Package==1.0\n", adapter)
        self.assertEqual(report.measurements[0].dependency.name, "My_Package")


if __name__ == "__main__":
    unittest.main()
