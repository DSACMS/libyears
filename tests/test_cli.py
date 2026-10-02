import json
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from libyears.cli import main
from libyears.model import MetricSummary
from libyears.scan import ScanReport


def empty_report():
    return ScanReport(MetricSummary(0, 0, None, 0.0, None, None, None), (), ())


class CLITests(unittest.TestCase):
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

    def test_json_output_is_parseable(self):
        output = io.StringIO()
        with patch("libyears.cli.scan_repository", return_value=empty_report()), redirect_stdout(output):
            code = main(["--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["schema_version"], 1)

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
