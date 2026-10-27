import json
import math
import ssl
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock, patch

from libyears.metric import build_report, measure_dependency
from libyears.model import Dependency, RegistryResult
from libyears.pypi import (
    INVALID_REGISTRY_RESPONSE,
    NO_STABLE_RELEASE,
    PACKAGE_NOT_FOUND,
    RELEASE_DATE_MISSING,
    REGISTRY_ERROR,
    VERSION_NOT_FOUND,
    PyPIAdapter,
    RegistryFailure,
)


class Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps(self.payload).encode()


def file(timestamp, *, yanked=False):
    return {"upload_time_iso_8601": timestamp, "yanked": yanked}


class PyPITests(unittest.TestCase):
    def lookup(self, payload, version="1.0"):
        adapter = PyPIAdapter(timeout=3.5, user_agent="test-agent")
        with patch("libyears.registry.request.urlopen", return_value=Response(payload)) as urlopen:
            result = adapter.lookup("example-package", version)
        urlopen.assert_called_once()
        args, kwargs = urlopen.call_args
        self.assertEqual(kwargs["timeout"], 3.5)
        self.assertTrue(math.isfinite(kwargs["timeout"]) and kwargs["timeout"] > 0)
        self.assertTrue(args[0].full_url.startswith("https://"))
        self.assertEqual(args[0].headers["User-agent"], "test-agent")
        return result

    def test_normal_package_uses_earliest_used_file_and_newest_release_timestamp(self):
        result = self.lookup(
            {"releases": {
                "1.0": [file("2023-01-02T00:00:00Z"), file("2023-01-01T00:00:00Z")],
                "1.1": [file("2024-01-01T00:00:00Z")],
                "1.2": [file("2023-12-01T00:00:00Z")],
            }}
        )
        self.assertIsInstance(result, RegistryResult)
        self.assertIs(type(result), RegistryResult)
        self.assertEqual(result.latest_stable_version, "1.1")
        self.assertEqual(result.used_release_time, datetime(2023, 1, 1, tzinfo=timezone.utc))

    def test_multiple_files_share_canonical_release_time_and_same_version_is_zero(self):
        payload = {"releases": {
            "1.0": [file("2023-01-01T00:00:00Z")],
            "2.0": [
                file("2024-02-01T00:00:00Z"),
                file("2024-02-03T00:00:00Z"),
            ],
        }}
        result = self.lookup(payload, "2.0")

        self.assertEqual(result.latest_stable_version, "2.0")
        self.assertEqual(result.used_release_time, datetime(2024, 2, 1, tzinfo=timezone.utc))
        self.assertEqual(result.latest_stable_release_time, result.used_release_time)

        same_release = Dependency(
            "pypi", "example-package", result.used_version,
            result.used_release_time, result.latest_stable_version,
            result.latest_stable_release_time,
        )
        one_year_old = Dependency(
            "pypi", "older-package", "1.0",
            datetime(2023, 2, 1, tzinfo=timezone.utc), "2.0",
            datetime(2024, 2, 1, tzinfo=timezone.utc),
        )
        older_measurement = measure_dependency(one_year_old)
        report = build_report([measure_dependency(same_release), older_measurement])
        self.assertEqual(report.measurements[0].libyears, 0.0)
        self.assertEqual(report.summary.total_libyears, older_measurement.libyears)
        self.assertEqual(report.summary.mean_libyears, older_measurement.libyears / 2)
        self.assertEqual(report.summary.median_libyears, older_measurement.libyears / 2)

    def test_latest_stable_selection_uses_canonical_time_for_multi_file_releases(self):
        result = self.lookup({"releases": {
            "1.0": [file("2023-01-01T00:00:00Z")],
            "2.0": [file("2024-02-01T00:00:00Z"), file("2024-02-04T00:00:00Z")],
            "3.0rc1": [file("2025-01-01T00:00:00Z")],
        }}, "1.0")
        self.assertEqual(result.latest_stable_version, "2.0")
        self.assertEqual(
            result.latest_stable_release_time,
            datetime(2024, 2, 1, tzinfo=timezone.utc),
        )

    def test_newer_prerelease_is_excluded(self):
        result = self.lookup({"releases": {
            "1.0": [file("2023-01-01T00:00:00Z")],
            "2.0rc1": [file("2025-01-01T00:00:00Z")],
        }})
        self.assertEqual(result.latest_stable_version, "1.0")

    def test_c_release_candidate_is_excluded_from_latest_stable(self):
        result = self.lookup({"releases": {
            "1.0": [file("2023-01-01T00:00:00Z")],
            "1.0c1": [file("2025-01-01T00:00:00Z")],
        }})
        self.assertEqual(result.latest_stable_version, "1.0")

    def test_all_yanked_release_is_excluded(self):
        result = self.lookup({"releases": {
            "1.0": [file("2023-01-01T00:00:00Z")],
            "2.0": [file("2025-01-01T00:00:00Z", yanked=True)],
        }})
        self.assertEqual(result.latest_stable_version, "1.0")

    def test_used_version_not_found(self):
        result = self.lookup({"releases": {"2.0": [file("2023-01-01T00:00:00Z")]}}, "1.0")
        self.assertIsInstance(result, RegistryFailure)
        self.assertEqual(result.reason, VERSION_NOT_FOUND)

    def test_source_result_contract_carries_common_evidence_and_failures(self):
        from libyears.model import (
            DependencyCandidate,
            SourceError,
            SourceEvidence,
            SourceResult,
            UnmeasurableDependency,
        )

        python_result = SourceResult(
            "pypi",
            (
                DependencyCandidate(
                    "pypi", "Requests", "requests", "Requests==2.0", "2.0", "requirements_exact"
                ),
            ),
            (
                UnmeasurableDependency(
                    "pypi", "other", "other>=1", "non_exact_version"
                ),
            ),
            (),
            SourceEvidence("requirements.txt", None),
            dependencies_discovered=2, measurement_available=True,
        )
        failed_npm_result = SourceResult(
            "npm",
            (),
            (),
            (SourceError("npm", "package.json", "invalid_manifest"),),
            SourceEvidence("package.json", "package-lock.json"),
            dependencies_discovered=None, measurement_available=False,
        )
        self.assertEqual(python_result.dependencies_discovered, 2)
        self.assertEqual(python_result.candidates[0].registry_name, "requests")
        self.assertEqual(python_result.evidence.snapshot_source, None)
        self.assertIsNone(failed_npm_result.dependencies_discovered)
        self.assertEqual(failed_npm_result.source_errors[0].reason, "invalid_manifest")

    def test_missing_upload_timestamps(self):
        result = self.lookup({"releases": {"1.0": [{"yanked": False}]}})
        self.assertEqual(result.reason, RELEASE_DATE_MISSING)

    def test_no_stable_release(self):
        result = self.lookup(
            {"releases": {"1.0rc1": [file("2023-01-01T00:00:00Z")]}}, "1.0rc1"
        )
        self.assertEqual(result.reason, NO_STABLE_RELEASE)

    def test_invalid_json(self):
        adapter = PyPIAdapter()
        response = Response({})
        response.read = lambda: b"not json"
        with patch("libyears.registry.request.urlopen", return_value=response):
            result = adapter.lookup("example", "1.0")
        self.assertEqual(result.reason, INVALID_REGISTRY_RESPONSE)

    def test_invalid_utf8_is_invalid_registry_response(self):
        adapter = PyPIAdapter()
        response = Response({})
        response.read = lambda: b"\xff"
        with patch("libyears.registry.request.urlopen", return_value=response):
            result = adapter.lookup("example", "1.0")
        self.assertEqual(result.reason, INVALID_REGISTRY_RESPONSE)

    def test_timeout_must_be_finite_and_positive(self):
        for timeout in (0, -1, float("nan"), float("inf"), float("-inf")):
            with self.subTest(timeout=timeout):
                with self.assertRaises(ValueError):
                    PyPIAdapter(timeout=timeout)

    def test_malformed_response(self):
        result = self.lookup({"releases": []})
        self.assertEqual(result.reason, INVALID_REGISTRY_RESPONSE)

    def test_http_error(self):
        adapter = PyPIAdapter()
        error = OSError("connection failed")
        with patch("libyears.registry.request.urlopen", side_effect=error):
            result = adapter.lookup("example", "1.0")
        self.assertEqual(result.reason, REGISTRY_ERROR)
        self.assertEqual(result.diagnostic, "network connection failure")

    def test_default_request_uses_normal_urlopen_tls_defaults(self):
        adapter = PyPIAdapter()
        with patch("libyears.registry.request.urlopen", return_value=Response({"releases": {"1.0": [file("2023-01-01T00:00:00Z")]}})) as urlopen:
            adapter.lookup("example", "1.0")
        context = urlopen.call_args.kwargs["context"]
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)

    def test_custom_ca_bundle_uses_verified_default_context(self):
        context = object()
        with patch("libyears.registry.ssl.create_default_context", return_value=context) as create_context:
            adapter = PyPIAdapter(ca_bundle="/tmp/org-ca.pem")
        self.assertEqual(adapter.tls_trust, "explicit CA bundle: /tmp/org-ca.pem")
        create_context.assert_called_once_with(cafile="/tmp/org-ca.pem")
        with patch("libyears.registry.request.urlopen", return_value=Response({"releases": {"1.0": [file("2023-01-01T00:00:00Z")]}})) as urlopen:
            adapter.lookup("example", "1.0")
        self.assertIs(urlopen.call_args.kwargs["context"], context)
        with patch("libyears.registry.ssl.create_default_context", return_value=context), \
             patch("libyears.registry._pip_ca_candidates", side_effect=AssertionError("fallback used")), \
             patch("libyears.registry.ssl.get_default_verify_paths", side_effect=AssertionError("default checked")):
            PyPIAdapter(ca_bundle="/tmp/authoritative.pem")

    def test_tls_error_diagnostic_is_concise(self):
        adapter = PyPIAdapter()
        error = ssl.SSLCertVerificationError("sensitive underlying details")
        with patch("libyears.registry.request.urlopen", side_effect=error):
            result = adapter.lookup("example", "1.0")
        self.assertEqual(result.reason, REGISTRY_ERROR)
        self.assertEqual(result.diagnostic, "TLS certificate verification failure")
        self.assertNotIn("sensitive", result.diagnostic)

    def test_python_default_trust_is_kept_when_available(self):
        from libyears.pypi import select_tls_context
        context = Mock()
        context.get_ca_certs.return_value = [{}]
        with patch("libyears.registry.ssl.create_default_context", return_value=context) as create, \
             patch("libyears.registry._pip_ca_candidates", side_effect=AssertionError("fallback used")):
            selected, source = select_tls_context()
        self.assertIs(selected, context)
        self.assertEqual(source, "Python default trust store")
        create.assert_called_once_with()

    def test_ssl_cert_file_is_reported_and_used_through_python_defaults(self):
        from libyears.pypi import select_tls_context
        context = Mock()
        context.get_ca_certs.return_value = [{}]
        with patch.dict("os.environ", {"SSL_CERT_FILE": "/approved/ca.pem"}), \
             patch("libyears.registry.ssl.create_default_context", return_value=context) as create:
            selected, source = select_tls_context()
        self.assertIs(selected, context)
        self.assertEqual(source, "SSL_CERT_FILE")
        create.assert_called_once_with()

    def test_ssl_cert_dir_is_reported_and_used_through_python_defaults(self):
        from libyears.pypi import select_tls_context
        context = Mock()
        context.get_ca_certs.return_value = [{}]
        with patch.dict("os.environ", {"SSL_CERT_DIR": "/approved/ca-dir"}, clear=True), \
             patch("libyears.registry.ssl.create_default_context", return_value=context) as create:
            selected, source = select_tls_context()
        self.assertIs(selected, context)
        self.assertEqual(source, "SSL_CERT_DIR")
        create.assert_called_once_with()

    def test_pip_fallback_only_when_default_has_no_trust_and_uses_verified_cafile(self):
        from libyears.pypi import select_tls_context
        empty = Mock()
        empty.get_ca_certs.return_value = []
        populated = Mock()
        populated.get_ca_certs.return_value = [{}]
        populated.verify_mode = ssl.CERT_REQUIRED
        populated.check_hostname = True
        with tempfile.TemporaryDirectory() as directory:
            ca_path = Path(directory) / "cacert.pem"
            ca_path.write_text("test fixture", encoding="ascii")
            with patch("libyears.registry.ssl.create_default_context", side_effect=[empty, populated]) as create, \
                 patch("libyears.registry.ssl.get_default_verify_paths", return_value=ssl.DefaultVerifyPaths(None, None, "", "", "", "")), \
                 patch("libyears.registry._pip_ca_candidates", return_value=(ca_path,)):
                selected, source = select_tls_context()
        self.assertIs(selected, populated)
        self.assertEqual(source, "pip-bundled CA fallback")
        self.assertEqual(create.call_args_list[-1].kwargs, {"cafile": str(ca_path)})
        self.assertEqual(selected.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(selected.check_hostname)

    def test_missing_pip_fallback_keeps_secure_default_context(self):
        from libyears.pypi import select_tls_context
        empty = Mock()
        empty.get_ca_certs.return_value = []
        empty.verify_mode = ssl.CERT_REQUIRED
        empty.check_hostname = True
        with patch("libyears.registry.ssl.create_default_context", return_value=empty), \
             patch("libyears.registry.ssl.get_default_verify_paths", return_value=ssl.DefaultVerifyPaths(None, None, "", "", "", "")), \
             patch("libyears.registry._pip_ca_candidates", return_value=()):
            selected, source = select_tls_context()
        self.assertIs(selected, empty)
        self.assertEqual(source, "Python default trust store")
        self.assertEqual(selected.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(selected.check_hostname)

    def test_http_404_is_package_not_found(self):
        adapter = PyPIAdapter()
        error = OSError("not found")
        error.code = 404
        with patch("libyears.registry.request.urlopen", side_effect=error):
            result = adapter.lookup("example", "1.0")
        self.assertEqual(result.reason, PACKAGE_NOT_FOUND)

    def test_latest_stable_can_equal_used_version(self):
        result = self.lookup({"releases": {"1.0": [file("2023-01-01T00:00:00Z")]}})
        self.assertEqual(result.latest_stable_version, "1.0")
        self.assertEqual(result.latest_stable_release_time, result.used_release_time)


if __name__ == "__main__":
    unittest.main()
