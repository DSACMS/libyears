import json
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

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
        with patch("libyears.pypi.request.urlopen", return_value=Response(payload)) as urlopen:
            result = adapter.lookup("example-package", version)
        urlopen.assert_called_once()
        args, kwargs = urlopen.call_args
        self.assertEqual(kwargs["timeout"], 3.5)
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
        self.assertEqual(result.latest_stable_version, "1.1")
        self.assertEqual(result.used_release_time, datetime(2023, 1, 1, tzinfo=timezone.utc))

    def test_newer_prerelease_is_excluded(self):
        result = self.lookup({"releases": {
            "1.0": [file("2023-01-01T00:00:00Z")],
            "2.0rc1": [file("2025-01-01T00:00:00Z")],
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
        with patch("libyears.pypi.request.urlopen", return_value=response):
            result = adapter.lookup("example", "1.0")
        self.assertEqual(result.reason, INVALID_REGISTRY_RESPONSE)

    def test_invalid_utf8_is_invalid_registry_response(self):
        adapter = PyPIAdapter()
        response = Response({})
        response.read = lambda: b"\xff"
        with patch("libyears.pypi.request.urlopen", return_value=response):
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
        with patch("libyears.pypi.request.urlopen", side_effect=error):
            result = adapter.lookup("example", "1.0")
        self.assertEqual(result.reason, REGISTRY_ERROR)

    def test_http_404_is_package_not_found(self):
        adapter = PyPIAdapter()
        error = OSError("not found")
        error.code = 404
        with patch("libyears.pypi.request.urlopen", side_effect=error):
            result = adapter.lookup("example", "1.0")
        self.assertEqual(result.reason, PACKAGE_NOT_FOUND)

    def test_latest_stable_can_equal_used_version(self):
        result = self.lookup({"releases": {"1.0": [file("2023-01-01T00:00:00Z")]}})
        self.assertEqual(result.latest_stable_version, "1.0")
        self.assertEqual(result.latest_stable_release_time, result.used_release_time)


if __name__ == "__main__":
    unittest.main()
