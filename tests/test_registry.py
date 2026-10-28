import ssl
import unittest
from unittest.mock import patch
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
