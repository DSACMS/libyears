import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from libyears.model import RegistryFailure, RegistryResult
from libyears.output import format_human, format_json
from libyears.scan import scan_mixed_repository
from libyears.snapshot import parse_snapshot_text


class MixedScanTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def write_python(self, contents="alpha==1.0\n"):
        (self.root / "requirements.txt").write_text(contents, encoding="utf-8")

    def write_npm(self, manifest=None, lock=None):
        if manifest is not None:
            (self.root / "package.json").write_text(manifest, encoding="utf-8")
        if lock is not None:
            (self.root / "package-lock.json").write_text(lock, encoding="utf-8")

    def successful_lookup(self, name, version):
        used = datetime(2023, 1, 1, tzinfo=timezone.utc)
        latest = datetime(2024, 1, 1, tzinfo=timezone.utc)
        return RegistryResult(name, version, used, "2.0.0", latest)

    def lookup_for_libyears(self, name, version, value):
        used = datetime(2020, 1, 1, tzinfo=timezone.utc)
        latest = used + timedelta(days=365.25 * value)
        return RegistryResult(name, version, used, "2.0.0", latest)

    def write_one_npm_dependency(self):
        self.write_npm(
            json.dumps({"dependencies": {"alpha": "^1.0.0"}}),
            json.dumps(
                {
                    "lockfileVersion": 3,
                    "packages": {
                        "": {"name": "fixture"},
                        "node_modules/alpha": {"version": "1.2.3"},
                    },
                }
            ),
        )

    def test_python_only_and_npm_only_sources_measure_independently(self):
        self.write_python()
        python_only = scan_mixed_repository(
            self.root,
            pypi_lookup=self.successful_lookup,
            npm_lookup=lambda *_: self.fail("npm lookup should not run"),
        )
        self.assertEqual(
            [(item.dependency.ecosystem, item.dependency.version_source)
             for item in python_only.measurements],
            [("pypi", "requirements_exact")],
        )
        self.assertEqual(python_only.source_results[1].dependencies_discovered, 0)

        (self.root / "requirements.txt").unlink()
        self.write_one_npm_dependency()
        npm_only = scan_mixed_repository(
            self.root,
            pypi_lookup=lambda *_: self.fail("PyPI lookup should not run"),
            npm_lookup=self.successful_lookup,
        )
        self.assertEqual(
            [(item.dependency.ecosystem, item.dependency.used_version,
              item.dependency.version_source)
             for item in npm_only.measurements],
            [("npm", "1.2.3", "package_lock")],
        )

    def test_mixed_sources_keep_both_ecosystem_measurements(self):
        self.write_python()
        self.write_one_npm_dependency()
        report = scan_mixed_repository(
            self.root,
            pypi_lookup=self.successful_lookup,
            npm_lookup=self.successful_lookup,
        )
        self.assertEqual(
            [item.dependency.ecosystem for item in report.measurements],
            ["pypi", "npm"],
        )

    def test_python_resolved_snapshot_evidence_is_preserved(self):
        self.write_python("alpha>=1.0\n")
        used_versions = []

        def lookup(name, version):
            used_versions.append(version)
            return self.successful_lookup(name, version)

        report = scan_mixed_repository(
            self.root,
            pypi_lookup=lookup,
            npm_lookup=lambda *_: self.fail("npm source is empty"),
            snapshot=parse_snapshot_text("alpha==2.5\n"),
        )
        self.assertEqual(used_versions, ["2.5"])
        self.assertEqual(
            report.measurements[0].dependency.version_source,
            "resolved_snapshot",
        )
        self.assertEqual(
            [result.ecosystem for result in report.source_results],
            ["pypi", "npm"],
        )

    def test_registry_failure_in_either_ecosystem_preserves_other_measurement(self):
        self.write_python()
        self.write_one_npm_dependency()

        for failing_ecosystem in ("pypi", "npm"):
            with self.subTest(failing_ecosystem=failing_ecosystem):
                def pypi_lookup(name, version):
                    if failing_ecosystem == "pypi":
                        return RegistryFailure(name, version, "registry_error")
                    return self.successful_lookup(name, version)

                def npm_lookup(name, version):
                    if failing_ecosystem == "npm":
                        return RegistryFailure(name, version, "registry_error")
                    return self.successful_lookup(name, version)

                report = scan_mixed_repository(
                    self.root,
                    pypi_lookup=pypi_lookup,
                    npm_lookup=npm_lookup,
                )
                self.assertEqual(len(report.measurements), 1)
                expected = "npm" if failing_ecosystem == "pypi" else "pypi"
                self.assertEqual(report.measurements[0].dependency.ecosystem, expected)
                self.assertEqual(len(report.unmeasurable), 1)
                self.assertEqual(report.unmeasurable[0].ecosystem, failing_ecosystem)

    def test_invalid_npm_manifest_is_source_error_without_synthetic_rows(self):
        self.write_python()
        self.write_npm('{"dependencies": {"ghost": "^1.0.0"')
        report = scan_mixed_repository(
            self.root,
            pypi_lookup=self.successful_lookup,
            npm_lookup=lambda *_: self.fail("invalid manifest has no npm candidates"),
        )
        self.assertEqual(len(report.measurements), 1)
        self.assertEqual(report.measurements[0].dependency.ecosystem, "pypi")
        self.assertEqual(report.unmeasurable, ())
        self.assertEqual(
            [(error.ecosystem, error.source, error.reason)
             for error in report.source_errors],
            [("npm", "package.json", "invalid_manifest")],
        )
        self.assertIsNone(report.source_results[1].dependencies_discovered)
        data = json.loads(format_json(report, str(self.root)))
        self.assertEqual(data["schema_version"], 3)
        self.assertEqual(data["source_errors"][0]["reason"], "invalid_manifest")
        self.assertEqual([item["ecosystem"] for item in data["dependencies"]], ["pypi"])
        human = format_human(report, str(self.root))
        self.assertIn("npm manifest discovery failed", human)
        self.assertIn("alpha", human)

    def test_invalid_lockfile_remains_dependency_level_and_pypi_survives(self):
        self.write_python()
        self.write_npm(
            json.dumps({"dependencies": {"alpha": "^1.0.0"}}),
            json.dumps({"lockfileVersion": 3, "packages": None}),
        )
        report = scan_mixed_repository(
            self.root,
            pypi_lookup=self.successful_lookup,
            npm_lookup=lambda *_: self.fail("invalid lockfile has no candidates"),
        )
        self.assertEqual(len(report.measurements), 1)
        self.assertEqual(report.measurements[0].dependency.ecosystem, "pypi")
        self.assertEqual(len(report.unmeasurable), 1)
        self.assertEqual(report.unmeasurable[0].ecosystem, "npm")
        self.assertEqual(report.unmeasurable[0].reason, "invalid_lockfile")
        self.assertEqual(report.source_errors, ())

    def test_repository_and_ecosystem_aggregates_use_each_source_denominator(self):
        self.write_python("py-one==1.0\npy-two==1.0\n")
        npm_dependencies = {name: "^1.0.0" for name in ("npm-one", "npm-two", "npm-three")}
        lock_packages = {"": {"name": "fixture"}}
        lock_packages.update({
            f"node_modules/{name}": {"version": "1.0.0"}
            for name in npm_dependencies
        })
        self.write_npm(
            json.dumps({"dependencies": npm_dependencies}),
            json.dumps({"lockfileVersion": 3, "packages": lock_packages}),
        )

        def pypi_lookup(name, version):
            if name == "py-two":
                return RegistryFailure(name, version, "registry_error")
            return self.lookup_for_libyears(name, version, 1.0)

        def npm_lookup(name, version):
            if name == "npm-three":
                return RegistryFailure(name, version, "registry_error")
            value = 2.0 if name == "npm-one" else 4.0
            return self.lookup_for_libyears(name, version, value)

        report = scan_mixed_repository(
            self.root, pypi_lookup=pypi_lookup, npm_lookup=npm_lookup
        )
        summary = report.summary
        self.assertEqual(summary.dependencies_discovered, 5)
        self.assertEqual(summary.dependencies_measured, 3)
        self.assertEqual(summary.coverage, 0.6)
        self.assertEqual(summary.total_libyears, 7.0)
        self.assertAlmostEqual(summary.mean_libyears, 7 / 3)
        self.assertEqual(summary.median_libyears, 2.0)
        self.assertEqual(summary.max_libyears, 4.0)
        self.assertEqual(list(report.by_ecosystem), ["npm", "pypi"])
        pypi = report.by_ecosystem["pypi"]
        self.assertEqual(
            (pypi.dependencies_discovered, pypi.dependencies_measured, pypi.coverage),
            (2, 1, 0.5),
        )
        self.assertEqual(pypi.total_libyears, 1.0)
        npm = report.by_ecosystem["npm"]
        self.assertEqual(
            (npm.dependencies_discovered, npm.dependencies_measured), (3, 2)
        )
        self.assertAlmostEqual(npm.coverage, 2 / 3)
        self.assertEqual(
            (npm.total_libyears, npm.mean_libyears, npm.median_libyears, npm.max_libyears),
            (6.0, 3.0, 3.0, 4.0),
        )

    def test_failed_discovery_nulls_ecosystem_and_repository_denominators(self):
        self.write_python()
        self.write_npm('{"dependencies": {"ghost": "^1.0.0"')
        report = scan_mixed_repository(
            self.root,
            pypi_lookup=lambda name, version: self.lookup_for_libyears(
                name, version, 1.0
            ),
            npm_lookup=lambda *_: self.fail("invalid manifest has no npm candidate"),
        )
        self.assertIsNone(report.summary.dependencies_discovered)
        self.assertEqual(report.summary.dependencies_measured, 1)
        self.assertIsNone(report.summary.coverage)
        self.assertEqual(report.summary.total_libyears, 1.0)
        self.assertEqual(report.summary.mean_libyears, 1.0)
        npm = report.by_ecosystem["npm"]
        self.assertEqual(
            (
                npm.dependencies_discovered,
                npm.dependencies_measured,
                npm.coverage,
                npm.total_libyears,
                npm.mean_libyears,
                npm.median_libyears,
                npm.max_libyears,
            ),
            (None, None, None, None, None, None, None),
        )
        self.assertEqual(report.by_ecosystem["pypi"].dependencies_measured, 1)

    def test_empty_and_zero_measurement_source_summaries(self):
        self.write_python("")
        self.write_npm(json.dumps({"dependencies": {"alpha": "^1.0.0"}}))
        report = scan_mixed_repository(
            self.root,
            pypi_lookup=lambda *_: self.fail("no Python candidates"),
            npm_lookup=lambda *_: self.fail("missing lockfile gives no npm candidates"),
        )
        pypi = report.by_ecosystem["pypi"]
        self.assertEqual((pypi.dependencies_discovered, pypi.dependencies_measured), (0, 0))
        self.assertIsNone(pypi.coverage)
        self.assertEqual(pypi.total_libyears, 0.0)
        self.assertIsNone(pypi.mean_libyears)

        npm = report.by_ecosystem["npm"]
        self.assertEqual((npm.dependencies_discovered, npm.dependencies_measured), (1, 0))
        self.assertEqual(npm.coverage, 0.0)
        self.assertEqual(npm.total_libyears, 0.0)
        self.assertIsNone(npm.mean_libyears)
        self.assertEqual((report.summary.dependencies_discovered, report.summary.dependencies_measured), (1, 0))

    def test_missing_sources_are_not_added_to_ecosystem_summaries(self):
        self.write_python()
        report = scan_mixed_repository(
            self.root,
            pypi_lookup=self.successful_lookup,
            npm_lookup=lambda *_: self.fail("npm manifest is absent"),
        )
        self.assertEqual(list(report.by_ecosystem), ["pypi"])


if __name__ == "__main__":
    unittest.main()
