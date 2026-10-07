import json
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from libyears.cli import main
from libyears.model import MetricSummary
from libyears.pypi import PyPIResult
from libyears.scan import ScanReport


def empty_report():
    return ScanReport(MetricSummary(0, 0, None, 0.0, None, None, None), (), ())


class CLITests(unittest.TestCase):
    def test_resolved_dogfooding_snapshot_matches_only_direct_dependencies(self):
        requirements = """requests
pygal
pandas
pytest
pylint
metrics-dash-backend-tools
urllib3>=2.6.3
"""
        snapshot = """astroid==4.3.3
certifi==2026.7.22
charset-normalizer==3.5.2
dill==0.4.1
idna==3.20
importlib_metadata==9.0.1
iniconfig==2.3.0
isort==9.0.2
mccabe==0.7.0
metrics-dash-backend-tools==0.1.5
mypy_extensions==1.1.0
numpy==2.4.6
packaging==26.3
pandas==2.3.3
platformdirs==4.12.2
pluggy==1.6.0
pygal==3.1.3
Pygments==2.21.0
pylint==4.1.1
pytest==9.1.1
python-dateutil==2.9.0.post0
pytz==2026.4
requests==2.34.2
six==1.17.0
tomlkit==0.15.1
tzdata==2026.4
urllib3==2.8.0
zipp==4.1.0
"""
        expected = {
            "requests": "2.34.2",
            "pygal": "3.1.3",
            "pandas": "2.3.3",
            "pytest": "9.1.1",
            "pylint": "4.1.1",
            "metrics-dash-backend-tools": "0.1.5",
            "urllib3": "2.8.0",
        }
        release_time = datetime(2024, 1, 1, tzinfo=timezone.utc)

        def lookup(name, version):
            return PyPIResult(name, version, release_time, version, release_time)

        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "requirements.txt").write_text(requirements, encoding="utf-8")
            snapshot_path = root / "resolved.txt"
            snapshot_path.write_text(snapshot, encoding="utf-8")
            with patch("libyears.scan.PyPIAdapter.lookup", side_effect=lookup) as registry, redirect_stdout(output):
                code = main([str(root), "--resolved", str(snapshot_path), "--json"])

        self.assertEqual(code, 0)
        report = json.loads(output.getvalue())
        self.assertEqual(report["unmeasurable"], [])
        self.assertEqual(report["summary"]["dependencies_discovered"], 7)
        self.assertEqual(report["summary"]["dependencies_measured"], 7)
        self.assertEqual(report["summary"]["coverage"], 1.0)
        self.assertEqual(
            {item["name"]: item["used_version"] for item in report["dependencies"]},
            expected,
        )
        self.assertCountEqual(
            [call.args for call in registry.call_args_list], list(expected.items())
        )

    def test_default_path(self):
        output = io.StringIO()
        with patch("libyears.cli.scan_repository", return_value=empty_report()) as scan, redirect_stdout(output):
            code = main([])
        self.assertEqual(code, 0)
        scan.assert_called_once_with(".")

    def test_explicit_path(self):
        with patch("libyears.cli.scan_repository", return_value=empty_report()) as scan:
            code = main(["/tmp/repository"])
        self.assertEqual(code, 0)
        scan.assert_called_once_with("/tmp/repository")

    def test_resolved_snapshot_is_parsed_and_passed_to_scan(self):
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / "resolved.txt"
            snapshot_path.write_text("requests==2.31.0\n", encoding="utf-8")
            with patch("libyears.cli.scan_repository", return_value=empty_report()) as scan, redirect_stdout(output):
                code = main([".", "--resolved", str(snapshot_path)])
        self.assertEqual(code, 0)
        scan.assert_called_once()
        self.assertEqual(scan.call_args.args, (".",))
        snapshot = scan.call_args.kwargs["snapshot"]
        self.assertEqual(snapshot.entries[0].version, "2.31.0")
        self.assertEqual(snapshot.source_path, str(snapshot_path))

    def test_missing_resolved_snapshot_is_filesystem_error(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / "missing.txt")
            errors = io.StringIO()
            with patch("libyears.cli.scan_repository") as scan, redirect_stderr(errors):
                code = main([".", "--resolved", missing])
        self.assertEqual(code, 1)
        scan.assert_not_called()

    def test_resolved_snapshot_scan_failure_is_systemic_error(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / "resolved.txt"
            snapshot_path.write_text("requests==2.31.0\n", encoding="utf-8")
            with redirect_stderr(io.StringIO()):
                code = main(
                    [".", "--resolved", str(snapshot_path)],
                    scan=lambda path, snapshot: (_ for _ in ()).throw(RuntimeError("boom")),
                )
        self.assertEqual(code, 2)

    def test_resolved_snapshot_measurement_gap_is_success(self):
        report = ScanReport(MetricSummary(1, 0, 0.0, 0.0, None, None, None), (), ())
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / "resolved.txt"
            snapshot_path.write_text("other==1.0\n", encoding="utf-8")
            with patch("libyears.cli.scan_repository", return_value=report):
                code = main([".", "--resolved", str(snapshot_path)])
        self.assertEqual(code, 0)

    def test_json_output_is_parseable(self):
        output = io.StringIO()
        with patch("libyears.cli.scan_repository", return_value=empty_report()), redirect_stdout(output):
            code = main(["--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["schema_version"], 2)

    def test_human_output_preserves_zero_coverage_success(self):
        output = io.StringIO()
        report = ScanReport(
            MetricSummary(1, 0, 0.0, 0.0, None, None, None), (), ()
        )
        with patch("libyears.cli.scan_repository", return_value=report), redirect_stdout(output):
            code = main([])
        self.assertEqual(code, 0)
        self.assertIn("No libyears measurement could be calculated", output.getvalue())
        self.assertIn("Measured: 0 / 1 dependencies", output.getvalue())
        self.assertNotIn("DEPENDENCY", output.getvalue())
        self.assertNotIn("Total:", output.getvalue())

    def test_scan_failure_returns_systemic_error(self):
        errors = io.StringIO()
        with redirect_stderr(errors):
            code = main([], scan=lambda path: (_ for _ in ()).throw(RuntimeError("boom")))
        self.assertEqual(code, 2)
        self.assertIn("systemic", errors.getvalue())

    def test_domain_value_error_returns_systemic_error(self):
        with redirect_stderr(io.StringIO()):
            code = main([], scan=lambda path: (_ for _ in ()).throw(ValueError("invalid domain data")))
        self.assertEqual(code, 2)

    def test_filesystem_failure_returns_one(self):
        with redirect_stderr(io.StringIO()):
            code = main([], scan=lambda path: (_ for _ in ()).throw(FileNotFoundError("missing")))
        self.assertEqual(code, 1)

    def test_usage_error_returns_one(self):
        with redirect_stderr(io.StringIO()):
            code = main(["one", "two"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
