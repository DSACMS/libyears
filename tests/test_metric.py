import unittest
from datetime import datetime, timedelta, timezone

from libyears.metric import build_report, calculate_summary, libyears_between, measure_dependency
from libyears.model import Dependency


UTC = timezone.utc


def timestamp(days: float) -> datetime:
    return datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=days)


def dependency(used_days: float, latest_days: float) -> Dependency:
    return Dependency(
        ecosystem="pypi",
        name="example",
        used_version="1.0",
        used_release_time=timestamp(used_days),
        latest_stable_version="2.0",
        latest_stable_release_time=timestamp(latest_days),
    )


class MetricTests(unittest.TestCase):
    def test_one_dependency(self) -> None:
        measurement = measure_dependency(dependency(0, 365.25))
        self.assertAlmostEqual(measurement.libyears, 1.0)
        self.assertFalse(measurement.timestamp_anomaly)

    def test_multiple_dependencies(self) -> None:
        report = build_report(
            [measure_dependency(dependency(0, 365.25)), measure_dependency(dependency(0, 730.5))]
        )
        self.assertEqual(report.summary.dependencies_measured, 2)
        self.assertAlmostEqual(report.summary.total_libyears, 3.0)

    def test_zero_age_dependency(self) -> None:
        measurement = measure_dependency(dependency(10, 10))
        self.assertEqual(measurement.libyears, 0.0)
        self.assertFalse(measurement.timestamp_anomaly)

    def test_timestamp_anomaly_is_clamped_and_flagged(self) -> None:
        measurement = measure_dependency(dependency(10, 9))
        self.assertEqual(measurement.libyears, 0.0)
        self.assertTrue(measurement.timestamp_anomaly)

    def test_total(self) -> None:
        summary = calculate_summary(
            [measure_dependency(dependency(0, 365.25)), measure_dependency(dependency(0, 730.5))]
        )
        self.assertAlmostEqual(summary.total_libyears, 3.0)

    def test_mean(self) -> None:
        summary = calculate_summary(
            [measure_dependency(dependency(0, 365.25)), measure_dependency(dependency(0, 730.5))]
        )
        self.assertAlmostEqual(summary.mean_libyears, 1.5)

    def test_median(self) -> None:
        summary = calculate_summary(
            [
                measure_dependency(dependency(0, 365.25)),
                measure_dependency(dependency(0, 730.5)),
                measure_dependency(dependency(0, 1461)),
            ]
        )
        self.assertAlmostEqual(summary.median_libyears, 2.0)

    def test_maximum(self) -> None:
        summary = calculate_summary(
            [measure_dependency(dependency(0, 365.25)), measure_dependency(dependency(0, 730.5))]
        )
        self.assertAlmostEqual(summary.max_libyears, 2.0)

    def test_measurement_coverage(self) -> None:
        summary = calculate_summary(
            [measure_dependency(dependency(0, 365.25))], dependencies_discovered=2
        )
        self.assertEqual(summary.dependencies_discovered, 2)
        self.assertEqual(summary.dependencies_measured, 1)
        self.assertEqual(summary.coverage, 0.5)

    def test_zero_discovered_dependencies(self) -> None:
        summary = calculate_summary([], dependencies_discovered=0)
        self.assertIsNone(summary.coverage)
        self.assertEqual(summary.total_libyears, 0.0)
        self.assertIsNone(summary.mean_libyears)
        self.assertIsNone(summary.median_libyears)
        self.assertIsNone(summary.max_libyears)

    def test_discovered_but_zero_measurable_dependencies(self) -> None:
        summary = calculate_summary([], dependencies_discovered=3)
        self.assertEqual(summary.dependencies_discovered, 3)
        self.assertEqual(summary.dependencies_measured, 0)
        self.assertEqual(summary.coverage, 0.0)
        self.assertEqual(summary.total_libyears, 0.0)
        self.assertIsNone(summary.mean_libyears)
        self.assertIsNone(summary.median_libyears)
        self.assertIsNone(summary.max_libyears)


if __name__ == "__main__":
    unittest.main()
