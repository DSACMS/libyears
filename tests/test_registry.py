import ssl
import unittest
from http.client import IncompleteRead
from unittest.mock import Mock, patch
from urllib import request
from urllib.error import HTTPError, URLError

from libyears.npm import NpmAdapter
from libyears.pypi import PyPIAdapter
from libyears.registry import TransportFailure, VerifiedJSONTransport


class LegacyResponse:
    """Existing callers need neither headers nor sized reads."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return b"{}"


class LegacyTransport:
    def __init__(self, result):
        self.result = result
        self.urls = []

    def get(self, url):
        self.urls.append(url)
        return self.result


class TransportCompatibilityTests(unittest.TestCase):
    def test_default_path_preserves_urlopen_arguments_and_no_argument_read(self):
        context = ssl.create_default_context()
        with patch("libyears.registry.select_tls_context", return_value=(context, "test trust")):
            transport = VerifiedJSONTransport(timeout=2.5, user_agent="test-agent")
        with patch("libyears.registry.request.urlopen", return_value=LegacyResponse()) as open_url:
            self.assertEqual(transport.get("https://example.org/data"), b"{}")
        args, kwargs = open_url.call_args
        self.assertEqual(args[0].full_url, "https://example.org/data")
        self.assertEqual(args[0].get_header("User-agent"), "test-agent")
        self.assertEqual(kwargs, {"timeout": 2.5, "context": context})
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)

    def test_existing_adapters_accept_get_url_only_doubles(self):
        for adapter_class, url in (
            (PyPIAdapter, "https://pypi.org/pypi/example/json"),
            (NpmAdapter, "https://registry.npmjs.org/example"),
        ):
            for response, reason in (
                (b"not json", "invalid_registry_response"),
                (TransportFailure(404, "HTTP error (status 404)"), "package_not_found"),
                (TransportFailure(None, "network timeout"), "registry_error"),
            ):
                with self.subTest(adapter=adapter_class.__name__, reason=reason):
                    adapter = adapter_class()
                    adapter.transport = LegacyTransport(response)
                    with patch("libyears.registry.request.urlopen", side_effect=AssertionError("live request")):
                        result = adapter.lookup("example", "1.0")
                    self.assertEqual(result.reason, reason)
                    self.assertEqual(adapter.transport.urls, [url])

    def test_default_failures_keep_status_and_safe_diagnostics(self):
        transport = VerifiedJSONTransport()
        for error, status, message in (
            (HTTPError("https://example.org", 404, "private", {}, None), 404, "HTTP error (status 404)"),
            (URLError(TimeoutError("private")), None, "network timeout"),
            (ssl.SSLCertVerificationError("private"), None, "TLS certificate verification failure"),
        ):
            with self.subTest(message=message):
                with patch("libyears.registry.request.urlopen", side_effect=error):
                    self.assertEqual(transport.get("https://example.org"), TransportFailure(status, message))


class BoundedResponse(LegacyResponse):
    def __init__(self, body, headers=None, read_error=None):
        self.body = body
        self.headers = headers or {}
        self.read_error = read_error
        self.read_sizes = []

    def read(self, size):
        self.read_sizes.append(size)
        if self.read_error is not None:
            raise self.read_error
        return self.body[:size]


class BoundedTransportTests(unittest.TestCase):
    def fetch(self, response):
        opener = Mock()
        opener.open.return_value = response
        with patch("libyears.registry.request.build_opener", return_value=opener), patch(
            "libyears.registry.request.urlopen", side_effect=AssertionError("default path used")
        ):
            transport = VerifiedJSONTransport(max_response_bytes=4, allowed_authority="rubygems.org")
            result = transport.get("https://rubygems.org/data")
        opener.open.assert_called_once()
        return result

    def test_exact_limit_and_smaller_bodies_are_complete(self):
        for body, headers in (
            (b"1234", {}), (b"1234", {"Content-Length": "4"}),
            (b"12", {"Content-Length": "2"}), (b"", {"Content-Length": "0"}),
            (b"1234", {"Content-Length": "invalid"}),
        ):
            with self.subTest(body=body, headers=headers):
                response = BoundedResponse(body, headers)
                self.assertEqual(self.fetch(response), body)
                self.assertEqual(response.read_sizes, [5])

    def test_oversize_never_returns_a_prefix(self):
        for headers in ({}, {"Content-Length": "5"}, {"Content-Length": "3"}):
            with self.subTest(headers=headers):
                response = BoundedResponse(b"123456789", headers)
                result = self.fetch(response)
                self.assertEqual(result, TransportFailure(None, "response exceeds byte limit", "response_too_large"))
                expected_reads = [] if headers.get("Content-Length") == "5" else [5]
                self.assertEqual(response.read_sizes, expected_reads)

    def test_truncation_discards_partial_bytes(self):
        for response in (
            BoundedResponse(b"12", {"Content-Length": "4"}),
            BoundedResponse(b"", read_error=IncompleteRead(b"12", 2)),
        ):
            with self.subTest(response=response):
                self.assertEqual(self.fetch(response), TransportFailure(None, "incomplete response", "incomplete_response"))

    def test_restricted_opener_reuses_selected_context_timeout_and_user_agent(self):
        context = ssl.create_default_context()
        with patch("libyears.registry.select_tls_context", return_value=(context, "explicit trust")), patch(
            "libyears.registry.request.build_opener"
        ) as build_opener:
            transport = VerifiedJSONTransport(
                max_response_bytes=4, allowed_authority="rubygems.org",
                timeout=1.5, user_agent="bounded-test", ca_bundle="approved.pem",
            )
        https_handler, redirect_handler = build_opener.call_args.args
        self.assertIsInstance(https_handler, request.HTTPSHandler)
        self.assertIs(https_handler._context, context)
        self.assertIsInstance(redirect_handler, request.HTTPRedirectHandler)
        self.assertTrue(context.check_hostname)
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertEqual(transport.tls_trust, "explicit trust")
        opener = build_opener.return_value
        opener.open.return_value = BoundedResponse(b"1234")
        self.assertEqual(transport.get("https://rubygems.org/data"), b"1234")
        args, kwargs = opener.open.call_args
        self.assertEqual(args[0].get_header("User-agent"), "bounded-test")
        self.assertEqual(kwargs, {"timeout": 1.5})

    def test_rejected_destinations_never_reach_opener(self):
        with patch("libyears.registry.request.build_opener") as build_opener:
            transport = VerifiedJSONTransport(allowed_authority="rubygems.org")
        for url in (
            "http://rubygems.org/data", "https://private.example/data",
            "https://rubygems.org.private.example/data", "https://user:secret@rubygems.org/data",
            "https://rubygems.org:444/data", "file:///data",
        ):
            with self.subTest(url=url):
                result = transport.get(url)
                self.assertEqual(result, TransportFailure(None, "unsupported request authority"))
        build_opener.return_value.open.assert_not_called()

    def test_each_control_can_be_enabled_independently(self):
        for controls, response in (
            ({"max_response_bytes": 4}, BoundedResponse(b"1234")),
            ({"allowed_authority": "rubygems.org"}, LegacyResponse()),
        ):
            with self.subTest(controls=controls):
                with patch("libyears.registry.request.build_opener") as build_opener:
                    transport = VerifiedJSONTransport(**controls)
                build_opener.return_value.open.return_value = response
                self.assertIsInstance(transport.get("https://rubygems.org/data"), bytes)

    def test_all_redirect_statuses_are_rejected_without_a_second_request(self):
        # Use the actual opener dispatch with an offline HTTPS handler so this
        # checks redirect enforcement, rather than just inspecting handler types.
        class RedirectResponse(LegacyResponse):
            code = 302
            msg = "redirect"
            url = "https://rubygems.org/data"

            def __init__(self, code, location):
                self.code = code
                self.headers = {"Location": location}

            def info(self):
                return self.headers

            def close(self):
                pass

        class OfflineHTTPS(request.HTTPSHandler):
            def https_open(self, req):
                self.urls.append(req.full_url)
                return self.response

        for code in (301, 302, 303, 307, 308):
            for location in ("https://private.example/secret", "https://rubygems.org/other", "/relative"):
                with self.subTest(code=code, location=location):
                    transport = VerifiedJSONTransport(max_response_bytes=4)
                    offline = OfflineHTTPS()
                    offline.urls = []
                    offline.response = RedirectResponse(code, location)
                    redirect_handler = next(
                        handler for handler in transport._restricted_opener.handlers
                        if isinstance(handler, request.HTTPRedirectHandler)
                    )
                    transport._restricted_opener = request.build_opener(offline, redirect_handler)
                    with patch("libyears.registry.request.urlopen", side_effect=AssertionError("live request")):
                        result = transport.get("https://rubygems.org/data")
                    self.assertEqual(result, TransportFailure(code, f"HTTP error (status {code})"))
                    self.assertEqual(offline.urls, ["https://rubygems.org/data"])

    def test_ordinary_restricted_errors_keep_existing_classification(self):
        for error, message in (
            (TimeoutError("private"), "network timeout"),
            (ssl.SSLCertVerificationError("private"), "TLS certificate verification failure"),
            (URLError("private"), "network connection failure"),
        ):
            with self.subTest(message=message):
                with patch("libyears.registry.request.build_opener") as build_opener:
                    transport = VerifiedJSONTransport(max_response_bytes=4)
                build_opener.return_value.open.side_effect = error
                self.assertEqual(transport.get("https://rubygems.org/data"), TransportFailure(None, message))

    def test_invalid_controls_fail_at_construction(self):
        for limit in (0, -1, True, 1.5, float("inf")):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                VerifiedJSONTransport(max_response_bytes=limit)
        for authority in ("", "https://rubygems.org", "user@rubygems.org", "rubygems.org/path", "rubygems.org?q=1"):
            with self.subTest(authority=authority), self.assertRaises(ValueError):
                VerifiedJSONTransport(allowed_authority=authority)


class RateLimitMetadataTests(unittest.TestCase):
    def fetch_failure(self, *, restricted, status=429, headers=None):
        error = HTTPError("https://rubygems.org/data", status, "private error text", headers, None)
        if restricted:
            with patch("libyears.registry.request.build_opener") as build_opener:
                transport = VerifiedJSONTransport(max_response_bytes=4, allowed_authority="rubygems.org")
            build_opener.return_value.open.side_effect = error
            result = transport.get("https://rubygems.org/data")
            build_opener.return_value.open.assert_called_once()
            return result
        transport = VerifiedJSONTransport()
        with patch("libyears.registry.request.urlopen", side_effect=error) as open_url:
            result = transport.get("https://rubygems.org/data")
        open_url.assert_called_once()
        return result

    def test_seconds_and_http_date_are_retained_without_retry_or_diagnostic_leak(self):
        for restricted in (False, True):
            for value in ("12", "Wed, 28 Oct 2026 12:00:00 GMT", "0"):
                with self.subTest(restricted=restricted, value=value):
                    result = self.fetch_failure(restricted=restricted, headers={"Retry-After": value})
                    self.assertEqual(result.status, 429)
                    self.assertEqual(result.diagnostic, "HTTP error (status 429)")
                    self.assertEqual(result.retry_after, value)
                    self.assertIsNone(result.bounded_failure)

    def test_missing_or_unsafe_metadata_is_unavailable(self):
        for restricted in (False, True):
            for headers in (
                None, {}, {"Retry-After": ""}, {"Retry-After": "1\r\nPrivate: secret"},
                {"Retry-After": "1\t2"}, {"Retry-After": "é"},
                {"Retry-After": "1" * 129}, {"Retry-After": 12},
            ):
                with self.subTest(restricted=restricted, headers=headers):
                    result = self.fetch_failure(restricted=restricted, headers=headers)
                    self.assertEqual(result, TransportFailure(429, "HTTP error (status 429)"))

    def test_printable_invalid_value_is_left_for_adapter_policy(self):
        result = self.fetch_failure(restricted=True, headers={"Retry-After": "tomorrow"})
        self.assertEqual(result.retry_after, "tomorrow")

    def test_other_http_errors_do_not_acquire_rate_limit_metadata(self):
        for status in (404, 503):
            for restricted in (False, True):
                with self.subTest(status=status, restricted=restricted):
                    result = self.fetch_failure(
                        restricted=restricted, status=status, headers={"Retry-After": "12"}
                    )
                    self.assertEqual(result, TransportFailure(status, f"HTTP error (status {status})"))

    def test_existing_consumers_ignore_added_metadata(self):
        for adapter_class in (PyPIAdapter, NpmAdapter):
            with self.subTest(adapter=adapter_class.__name__):
                adapter = adapter_class()
                adapter.transport = LegacyTransport(
                    TransportFailure(429, "HTTP error (status 429)", retry_after="12")
                )
                result = adapter.lookup("example", "1.0")
                self.assertEqual(result.reason, "registry_error")
                self.assertEqual(result.diagnostic, "HTTP error (status 429)")
                self.assertEqual(len(adapter.transport.urls), 1)

    def test_failure_metadata_defaults_preserve_existing_constructor(self):
        result = TransportFailure(None, "network timeout")
        self.assertIsNone(result.retry_after)
        self.assertIsNone(result.bounded_failure)
