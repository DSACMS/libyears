import json
import math
import ssl
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from libyears.npm import (
    INVALID_REGISTRY_RESPONSE,
    PACKAGE_NOT_FOUND,
    RELEASE_DATE_MISSING,
    REGISTRY_ERROR,
    VERSION_NOT_FOUND,
    NpmAdapter,
    NpmRegistryFailure,
    NO_STABLE_RELEASE,
)
from libyears.metric import measure_dependency
from libyears.model import Dependency, RegistryFailure, RegistryResult


class Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def payload(versions, times, latest=None):
    result = {
        "versions": {version: {"name": "example"} for version in versions},
        "time": times,
        "dist-tags": {},
    }
    if latest is not None:
        result["dist-tags"]["latest"] = latest
    return result


class NpmRegistryTests(unittest.TestCase):
    def lookup(self, metadata, used_version="1.0.0", name="example"):
        adapter = NpmAdapter(timeout=4.25, user_agent="registry-test")
        with patch(
            "libyears.registry.request.urlopen", return_value=Response(metadata)
        ) as urlopen:
            result = adapter.lookup(name, used_version)
        args, kwargs = urlopen.call_args
        return result, args[0], kwargs

    def test_uses_public_registry_metadata_and_publication_timestamps(self):
        result, request, kwargs = self.lookup(
            payload(
                ["1.0.0", "2.0.0", "10.0.0"],
                {
                    "1.0.0": "2022-01-01T00:00:00Z",
                    "2.0.0": "2024-01-01T00:00:00Z",
                    "10.0.0": "2023-01-01T00:00:00Z",
                },
            )
        )
        self.assertEqual(request.full_url, "https://registry.npmjs.org/example")
        self.assertEqual(kwargs["timeout"], 4.25)
        self.assertTrue(math.isfinite(kwargs["timeout"]) and kwargs["timeout"] > 0)
        self.assertEqual(request.headers["User-agent"], "registry-test")
        self.assertEqual(result.latest_stable_version, "2.0.0")
        self.assertIs(type(result), RegistryResult)
        self.assertEqual(
            result.used_release_time,
            datetime(2022, 1, 1, tzinfo=timezone.utc),
        )
        self.assertEqual(
            result.latest_stable_release_time,
            datetime(2024, 1, 1, tzinfo=timezone.utc),
        )

    def test_explicit_ca_bundle_uses_selected_verified_context(self):
        context = ssl.create_default_context()
        with patch(
            "libyears.registry.ssl.create_default_context", return_value=context
        ) as create_context:
            adapter = NpmAdapter(ca_bundle="/approved/ca.pem")
        create_context.assert_called_once_with(cafile="/approved/ca.pem")
        with patch(
            "libyears.registry.request.urlopen",
            return_value=Response(
                payload(["1.0.0"], {"1.0.0": "2024-01-01T00:00:00Z"})
            ),
        ) as urlopen:
            adapter.lookup("example", "1.0.0")
        kwargs = urlopen.call_args.kwargs
        self.assertEqual(kwargs["context"], context)
        self.assertEqual(kwargs["context"].verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(kwargs["context"].check_hostname)

    def test_scoped_package_encodes_slash_and_preserves_identity(self):
        result, request, _ = self.lookup(
            payload(["1.0.0"], {"1.0.0": "2024-01-01T00:00:00Z"}),
            name="@scope/package",
        )
        self.assertEqual(
            request.full_url,
            "https://registry.npmjs.org/@scope%2Fpackage",
        )
        self.assertEqual(result.name, "@scope/package")

    def test_dist_tag_breaks_only_a_greatest_timestamp_tie(self):
        tagged, _, _ = self.lookup(
            payload(
                ["1.0.0", "2.0.0", "3.0.0"],
                {
                    "1.0.0": "2022-01-01T00:00:00Z",
                    "2.0.0": "2024-01-01T00:00:00Z",
                    "3.0.0": "2024-01-01T00:00:00Z",
                },
                latest="3.0.0",
            )
        )
        ignored_tag, _, _ = self.lookup(
            payload(
                ["1.0.0", "2.0.0", "3.0.0"],
                {
                    "1.0.0": "2022-01-01T00:00:00Z",
                    "2.0.0": "2024-01-01T00:00:00Z",
                    "3.0.0": "2024-01-01T00:00:00Z",
                },
                latest="1.0.0",
            )
        )
        self.assertEqual(tagged.latest_stable_version, "3.0.0")
        self.assertEqual(ignored_tag.latest_stable_version, "2.0.0")
        self.assertEqual(
            tagged.latest_stable_release_time,
            ignored_tag.latest_stable_release_time,
        )

    def test_deprecated_available_release_remains_eligible(self):
        metadata = payload(
            ["1.0.0", "2.0.0"],
            {
                "1.0.0": "2022-01-01T00:00:00Z",
                "2.0.0": "2024-01-01T00:00:00Z",
            },
        )
        metadata["versions"]["2.0.0"]["deprecated"] = "use a newer release"
        result, _, _ = self.lookup(metadata)
        self.assertEqual(result.latest_stable_version, "2.0.0")

    def test_canonical_stable_and_build_versions_beat_newer_prereleases(self):
        result, _, _ = self.lookup(
            payload(
                ["1.2.3", "2.0.0+build.7", "3.0.0-rc.1"],
                {
                    "1.2.3": "2022-01-01T00:00:00Z",
                    "2.0.0+build.7": "2024-01-01T00:00:00Z",
                    "3.0.0-rc.1": "2026-01-01T00:00:00Z",
                },
            ),
            used_version="1.2.3",
        )
        self.assertEqual(result.latest_stable_version, "2.0.0+build.7")

    def test_prerelease_used_version_remains_measurable(self):
        result, _, _ = self.lookup(
            payload(
                ["1.0.0", "2.0.0-rc.1"],
                {
                    "1.0.0": "2024-01-01T00:00:00Z",
                    "2.0.0-rc.1": "2025-01-01T00:00:00Z",
                },
            ),
            used_version="2.0.0-rc.1",
        )
        self.assertEqual(result.used_version, "2.0.0-rc.1")
        self.assertEqual(result.latest_stable_version, "1.0.0")

    def test_malformed_prefixed_and_unclassifiable_versions_are_excluded(self):
        rejected = [
            "v4.0.0",
            "01.2.3",
            "1.2",
            "1.2.3-01",
            "1.2.3+",
            "not-a-version",
        ]
        metadata = payload(
            rejected,
            {version: f"202{index + 5}-01-01T00:00:00Z" for index, version in enumerate(rejected)},
        )
        metadata["versions"]["1.2.3-01"]["time"] = "bad prerelease"
        result, _, _ = self.lookup(metadata, used_version="v4.0.0")
        self.assertEqual(result.reason, NO_STABLE_RELEASE)

    def test_same_used_and_latest_stable_version_measures_exactly_zero(self):
        result, _, _ = self.lookup(
            payload(["1.2.3"], {"1.2.3": "2024-01-01T00:00:00Z"}),
            used_version="1.2.3",
        )
        dependency = Dependency(
            "npm",
            result.name,
            result.used_version,
            result.used_release_time,
            result.latest_stable_version,
            result.latest_stable_release_time,
        )
        self.assertEqual(measure_dependency(dependency).libyears, 0.0)

    def test_package_version_and_timestamp_misses_use_existing_reasons(self):
        missing_version, _, _ = self.lookup(
            payload(["2.0.0"], {"2.0.0": "2024-01-01T00:00:00Z"})
        )
        missing_time, _, _ = self.lookup(
            payload(["1.0.0"], {}), used_version="1.0.0"
        )
        self.assertEqual(missing_version.reason, VERSION_NOT_FOUND)
        self.assertEqual(missing_time.reason, RELEASE_DATE_MISSING)

    def test_malformed_required_response_data_is_invalid_registry_response(self):
        for malformed in (
            [],
            {"versions": [], "time": {}},
            {"versions": {"1.0.0": {}}, "time": []},
        ):
            with self.subTest(malformed=malformed):
                result, _, _ = self.lookup(malformed)
                self.assertEqual(result.reason, INVALID_REGISTRY_RESPONSE)

    def test_transport_failure_uses_registry_error_and_safe_diagnostic(self):
        adapter = NpmAdapter()
        error = OSError("sensitive network detail")
        with patch("libyears.registry.request.urlopen", side_effect=error):
            result = adapter.lookup("example", "1.0.0")
        self.assertIsInstance(result, NpmRegistryFailure)
        self.assertIsInstance(result, RegistryFailure)
        self.assertEqual(result.reason, REGISTRY_ERROR)
        self.assertEqual(result.diagnostic, "network connection failure")
        self.assertNotIn("sensitive", result.diagnostic)

    def test_http_404_is_package_not_found(self):
        adapter = NpmAdapter()
        error = OSError("not found")
        error.code = 404
        with patch("libyears.registry.request.urlopen", side_effect=error):
            result = adapter.lookup("example", "1.0.0")
        self.assertEqual(result.reason, PACKAGE_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
