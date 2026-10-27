import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock, patch

from libyears.model import (
    MetricSummary, RegistryFailure, RegistryResult, SourceError, SourceEvidence, SourceResult,
)
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
        self.assertFalse(report.source_results[1].measurement_available)
        data = json.loads(format_json(report, str(self.root)))
        self.assertEqual(data["schema_version"], 3)
        self.assertEqual(data["source_errors"][0]["reason"], "invalid_manifest")
        self.assertEqual([item["ecosystem"] for item in data["dependencies"]], ["pypi"])
        self.assertIsNone(data["summary"]["dependencies_discovered"])
        self.assertIsNone(data["summary"]["coverage"])
        self.assertIsNone(data["summary"]["by_ecosystem"]["npm"]["coverage"])
        self.assertAlmostEqual(data["summary"]["total_libyears"], 365 / 365.25)
        self.assertAlmostEqual(data["summary"]["by_ecosystem"]["pypi"]["total_libyears"], 365 / 365.25)
        human = format_human(report, str(self.root))
        self.assertIn("npm manifest discovery failed", human)
        self.assertIn("alpha", human)
        self.assertIn("Repository: null coverage", human)
        self.assertIn("npm: null coverage", human)
        self.assertIn("pypi: 100.0% coverage", human)

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
        self.assertTrue(report.source_results[1].measurement_available)
        self.assertEqual(report.by_ecosystem["npm"], MetricSummary(1, 0, 0.0, 0.0, None, None, None))

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
        payload = json.loads(format_json(report, str(self.root)))
        self.assertEqual(payload["schema_version"], 3)
        self.assertEqual(payload["summary"]["dependencies_discovered"], 5)
        self.assertEqual(payload["summary"]["dependencies_measured"], 3)
        self.assertAlmostEqual(payload["summary"]["coverage"], 0.6)
        self.assertEqual(payload["summary"]["total_libyears"], 7.0)
        self.assertEqual(payload["summary"]["by_ecosystem"]["npm"]["dependencies_discovered"], 3)
        self.assertEqual(payload["version_evidence"]["npm"]["snapshot_source"], "package-lock.json")
        human = format_human(report, str(self.root))
        self.assertIn("Ecosystems: npm, pypi", human)
        self.assertIn("Repository: 60.0% coverage", human)
        self.assertIn("npm: 66.7% coverage", human)
        self.assertIn("pypi: 50.0% coverage", human)

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

    def test_rejected_source_retains_known_count_without_dependency_rows(self):
        # Inject source results before the evidence selector is integrated.
        for discovered in (0, 10):
            for errors in ((), (SourceError("npm", "fixture", "invalid_lockfile"),)):
                with self.subTest(discovered=discovered, errors=errors):
                    rejected = SourceResult(
                        "npm", (), (), errors, SourceEvidence("package.json", None),
                        dependencies_discovered=discovered, measurement_available=False,
                    )
                    with patch("libyears.scan._npm_source_result", return_value=rejected):
                        report = scan_mixed_repository(
                            self.root,
                            pypi_lookup=lambda *_: self.fail("no Python candidates"),
                            npm_lookup=lambda *_: self.fail("rejected source has no candidates"),
                        )
                    expected = MetricSummary(discovered, None, None, 0.0, None, None, None)
                    self.assertEqual(report.summary, expected)
                    self.assertEqual(report.by_ecosystem["npm"], expected)
                    self.assertEqual(report.measurements, ())
                    self.assertEqual(report.unmeasurable, ())
                    self.assertEqual(report.source_errors, errors)

    def test_rejected_source_preserves_mixed_counts_and_numeric_aggregates(self):
        self.write_python("one==1.0\ntwo==1.0\nthree==1.0\nfour>=1.0\n")
        rejected = SourceResult(
            "npm", (), (), (SourceError("npm", "fixture", "invalid_lockfile"),),
            SourceEvidence("package.json", None),
            dependencies_discovered=10, measurement_available=False,
        )

        def lookup(name, version):
            return self.lookup_for_libyears(name, version, {"one": 1, "two": 2, "three": 6}[name])

        with patch("libyears.scan._npm_source_result", return_value=rejected):
            report = scan_mixed_repository(
                self.root, pypi_lookup=lookup,
                npm_lookup=lambda *_: self.fail("rejected source has no candidates"),
            )
        self.assertEqual(report.summary, MetricSummary(14, 3, None, 9.0, 3.0, 2.0, 6.0))
        self.assertEqual(report.by_ecosystem["pypi"], MetricSummary(4, 3, 0.75, 9.0, 3.0, 2.0, 6.0))
        self.assertEqual(report.by_ecosystem["npm"], MetricSummary(10, None, None, 0.0, None, None, None))
        self.assertEqual(len(report.measurements), 3)
        self.assertEqual([item.ecosystem for item in report.unmeasurable], ["pypi"])

    def test_available_source_is_not_rejected_based_on_errors(self):
        available = SourceResult(
            "npm", (), (), (SourceError("npm", "fixture", "diagnostic"),),
            SourceEvidence("package.json", None),
            dependencies_discovered=0, measurement_available=True,
        )
        with patch("libyears.scan._npm_source_result", return_value=available):
            report = scan_mixed_repository(
                self.root,
                pypi_lookup=lambda *_: self.fail("no Python candidates"),
                npm_lookup=lambda *_: self.fail("no npm candidates"),
            )
        self.assertEqual(report.summary, MetricSummary(0, 0, None, 0.0, None, None, None))
        self.assertEqual(report.by_ecosystem["npm"], report.summary)

    def test_yarn_candidate_reaches_npm_adapter_with_scoped_identity(self):
        self.write_npm(json.dumps({"dependencies": {"@scope/widget": "^2.0.0"}}))
        (self.root / "yarn.lock").write_text(
            '# yarn lockfile v1\n"@scope/widget@^2.0.0":\n  version "2.0.0"\n'
        )
        adapter = Mock()
        timestamp = datetime(2024, 1, 1, tzinfo=timezone.utc)
        adapter.lookup.return_value = RegistryResult(
            "@scope/widget", "2.0.0", timestamp, "2.0.0", timestamp
        )
        report = scan_mixed_repository(
            self.root, npm_adapter=adapter,
            pypi_lookup=lambda *_: self.fail("no Python candidates"),
        )
        adapter.lookup.assert_called_once_with("@scope/widget", "2.0.0")
        dependency = report.measurements[0].dependency
        self.assertEqual((dependency.ecosystem, dependency.version_source), ("npm", "yarn_lock"))
        self.assertEqual(report.measurements[0].libyears, 0.0)
        self.assertEqual(report.summary.coverage, 1.0)
        data = json.loads(format_json(report, "."))
        self.assertEqual(data["schema_version"], 3)
        self.assertEqual(data["dependencies"][0]["version_source"], "yarn_lock")
        self.assertEqual(data["version_evidence"]["npm"], {
            "declaration_source": "package.json", "snapshot_source": "yarn.lock",
            "format": "yarn_lock_v1",
        })
        self.assertIn("Version evidence: yarn.lock", format_human(report, "."))

    def test_yarn_dependency_failures_preserve_declarations_and_partial_coverage(self):
        declarations = {
            "good": "^1.0.0", "missing": "^3.0.0", "local": "file:../local",
            "conflict": "1.0.0", "ambiguous": "^1.0.0",
        }
        self.write_npm(json.dumps({"dependencies": declarations}))
        (self.root / "yarn.lock").write_text(
            '# yarn lockfile v1\ngood@^1.0.0:\n  version "1.2.0"\n'
            'conflict@1.0.0:\n  version "1.1.0"\n'
            'ambiguous@^1.0.0:\n  version "1.0.0"\n'
            'ambiguous@^1.0.0, ambiguous@~1.0.0:\n  version "1.0.0"\n'
        )
        lookup = Mock(side_effect=self.successful_lookup)
        report = scan_mixed_repository(
            self.root, npm_lookup=lookup, pypi_lookup=self.successful_lookup,
        )
        lookup.assert_called_once_with("good", "1.2.0")
        self.assertEqual((report.summary.dependencies_discovered,
                          report.summary.dependencies_measured, report.summary.coverage), (5, 1, 0.2))
        self.assertEqual({item.name: item.reason for item in report.unmeasurable}, {
            "missing": "lock_version_missing", "local": "unsupported_dependency_source",
            "conflict": "declaration_lock_conflict", "ambiguous": "ambiguous_lock_evidence",
        })
        self.assertEqual(report.source_errors, ())
        human = format_human(report, ".")
        for item in report.unmeasurable:
            self.assertEqual(item.declared, declarations[item.name])
            self.assertIn(item.declared, human)
        for explanation in ("exact version unavailable in yarn.lock", "unsupported dependency source",
                            "lock version conflicts", "ambiguous exact version evidence"):
            self.assertIn(explanation, human)
        self.assertEqual(len(json.loads(format_json(report, "."))["unmeasurable"]), 4)

    def test_yarn_whole_source_failures_preserve_mixed_aggregates(self):
        cases = (
            ('# yarn lockfile v1\ninvalid key\n', "invalid_lockfile", "yarn_lock_v1",
             "malformed Yarn Classic v1 structure"),
            ('# yarn lockfile v2\n', "unsupported_lockfile_format", None,
             "unsupported or contradictory Yarn generation header"),
            ('widget@^1.0.0:\n  version "1.0.0"\n', "unsupported_lockfile_format", None,
             "could not identify Yarn Classic v1"),
            ('# yarn lockfile v1\n', "conflicting_resolution_sources", None,
             "neither lockfile supplied evidence"),
        )
        self.write_npm(json.dumps({"dependencies": {f"npm-{i}": "^1.0.0" for i in range(10)}}))
        for contents, reason, evidence_format, explanation in cases:
            for mixed in (False, True):
                with self.subTest(reason=reason, explanation=explanation, mixed=mixed):
                    (self.root / "yarn.lock").write_text(contents)
                    if reason == "conflicting_resolution_sources":
                        (self.root / "package-lock.json").write_text("invalid JSON is not parsed")
                    if mixed:
                        self.write_python("one==1.0\ntwo==1.0\nthree==1.0\nfour>=1.0\n")
                    else:
                        (self.root / "requirements.txt").unlink(missing_ok=True)
                    report = scan_mixed_repository(
                        self.root,
                        npm_lookup=lambda *_: self.fail("rejected npm source must not reach lookup"),
                        pypi_lookup=lambda name, version: self.lookup_for_libyears(name, version, 1.0),
                    )
                    self.assertEqual(report.by_ecosystem["npm"], MetricSummary(10, None, None, 0.0, None, None, None))
                    expected = MetricSummary(14, 3, None, 3.0, 1.0, 1.0, 1.0) if mixed else report.by_ecosystem["npm"]
                    self.assertEqual(report.summary, expected)
                    self.assertFalse(any(item.ecosystem == "npm" for item in report.unmeasurable))
                    data = json.loads(format_json(report, "."))
                    source = "package-lock.json + yarn.lock" if reason == "conflicting_resolution_sources" else "yarn.lock"
                    self.assertEqual(data["source_errors"], [{"ecosystem": "npm", "source": source, "reason": reason}])
                    self.assertEqual(data["version_evidence"]["npm"], {
                        "declaration_source": "package.json",
                        "snapshot_source": None if reason == "conflicting_resolution_sources" else "yarn.lock",
                        "format": evidence_format,
                    })
                    human = format_human(report, ".")
                    self.assertIn(explanation, human)
                    self.assertIn(source, human)
                    self.assertIn("npm: null coverage", human)
                    self.assertIn("Repository: null coverage", human)
                    self.assertNotIn("unsafe", human)
                    self.assertNotIn(explanation, format_json(report, "."))

    def test_yarn_without_root_manifest_does_not_create_npm_scope(self):
        (self.root / "yarn.lock").write_text("unsupported")
        report = scan_mixed_repository(
            self.root, npm_lookup=lambda *_: self.fail("no npm scope"),
            pypi_lookup=lambda *_: self.fail("no Python scope"),
        )
        self.assertEqual(report.source_errors, ())
        self.assertNotIn("npm", report.by_ecosystem)

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
