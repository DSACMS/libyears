"""Verified JSON-over-HTTPS transport shared by registry adapters."""

from __future__ import annotations

from dataclasses import dataclass
from http.client import IncompleteRead
import math
import os
import ssl
import stat
import sys
import sysconfig
from pathlib import Path
from typing import Any
from urllib import error as urlerror, request
from urllib.parse import urlsplit


@dataclass(frozen=True, slots=True)
class TransportFailure:
    """Transport details that an adapter maps to registry-specific reasons."""

    status: Any
    diagnostic: str
    bounded_failure: str | None = None
    retry_after: str | None = None


def _retry_after(error: Exception) -> str | None:
    if not isinstance(error, urlerror.HTTPError) or error.code != 429 or error.headers is None:
        return None
    value = error.headers.get("Retry-After")
    # Retain only a short printable header value, never arbitrary header objects
    # or control text. Interpreting seconds/HTTP dates belongs to the adapter.
    if not isinstance(value, str) or not value or len(value) > 128:
        return None
    if any(character < " " or character > "~" for character in value):
        return None
    return value


class _RejectRedirects(request.HTTPRedirectHandler):
    """Restricted requests never follow a metadata-supplied destination."""

    def http_error_302(self, req, fp, code, msg, headers):
        raise urlerror.HTTPError(req.full_url, code, "redirect rejected", headers, fp)

    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302
    http_error_308 = http_error_302


def _read_bounded_response(response: Any, limit: int) -> bytes | TransportFailure:
    declared_length = response.headers.get("Content-Length")
    if isinstance(declared_length, str) and declared_length.isascii() and declared_length.isdecimal():
        declared_length = int(declared_length)
    else:
        declared_length = None
    if declared_length is not None and declared_length > limit:
        return TransportFailure(None, "response exceeds byte limit", "response_too_large")
    try:
        body = response.read(limit + 1)
    except IncompleteRead:
        return TransportFailure(None, "incomplete response", "incomplete_response")
    if len(body) > limit:
        return TransportFailure(None, "response exceeds byte limit", "response_too_large")
    if declared_length is not None and len(body) < declared_length:
        return TransportFailure(None, "incomplete response", "incomplete_response")
    return body


def diagnostic(error: Exception) -> str:
    """Return a concise transport diagnostic without exposing error details."""
    if isinstance(error, ssl.SSLCertVerificationError):
        return "TLS certificate verification failure"
    if isinstance(error, urlerror.HTTPError):
        return f"HTTP error (status {error.code})"
    if isinstance(error, TimeoutError):
        return "network timeout"
    if isinstance(error, urlerror.URLError):
        cause = error.reason
        if isinstance(cause, ssl.SSLCertVerificationError):
            return "TLS certificate verification failure"
        if isinstance(cause, TimeoutError):
            return "network timeout"
        if isinstance(cause, OSError) and getattr(cause, "errno", None) in {-2, -3, 8}:
            return "DNS lookup failure"
        return "network connection failure"
    return "network connection failure"


def _pip_ca_candidates() -> tuple[Path, ...]:
    """Return a small ordered set of pip-vendored CA paths for this interpreter."""
    version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    candidates: list[Path] = []
    purelib = sysconfig.get_path("purelib")
    if purelib:
        candidates.append(Path(purelib) / "pip" / "_vendor" / "certifi" / "cacert.pem")
    for prefix in dict.fromkeys((sys.prefix, sys.base_prefix)):
        candidates.append(
            Path(prefix) / "lib" / version / "site-packages" / "pip" / "_vendor" / "certifi" / "cacert.pem"
        )
    return tuple(dict.fromkeys(candidates))


def _regular_readable_file(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.stat().st_mode) and os.access(path, os.R_OK)
    except OSError:
        return False


def select_tls_context(ca_bundle: str | None = None) -> tuple[ssl.SSLContext, str]:
    """Select verified trust using explicit, Python, then pip-bundled trust."""
    if ca_bundle:
        return ssl.create_default_context(cafile=ca_bundle), f"explicit CA bundle: {ca_bundle}"

    env_file = os.environ.get("SSL_CERT_FILE")
    env_dir = os.environ.get("SSL_CERT_DIR")
    try:
        context = ssl.create_default_context()
    except (OSError, ssl.SSLError):
        if env_file or env_dir:
            raise
        context = None

    if context is not None:
        paths = ssl.get_default_verify_paths()
        cafile = paths.cafile
        capath = paths.capath
        usable_path = bool(cafile and _regular_readable_file(Path(cafile)))
        directory_paths = [path for value in (env_dir, capath) if value for path in value.split(os.pathsep)]
        usable_path = usable_path or any(
            Path(path).is_dir() and os.access(path, os.R_OK) for path in directory_paths
        )
        if context.get_ca_certs() or usable_path:
            if env_file:
                return context, "SSL_CERT_FILE"
            if env_dir:
                return context, "SSL_CERT_DIR"
            return context, "Python default trust store"

    for candidate in _pip_ca_candidates():
        if not _regular_readable_file(candidate):
            continue
        try:
            context = ssl.create_default_context(cafile=str(candidate))
        except (OSError, ssl.SSLError):
            continue
        if context.get_ca_certs():
            return context, "pip-bundled CA fallback"

    return ssl.create_default_context(), "Python default trust store"


class VerifiedJSONTransport:
    """Fetch response bytes with the project's verified HTTPS policy."""

    def __init__(
        self,
        *,
        timeout: float = 10.0,
        user_agent: str = "libyears/0.1",
        ca_bundle: str | None = None,
        max_response_bytes: int | None = None,
        allowed_authority: str | None = None,
    ) -> None:
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be finite and positive")
        if max_response_bytes is not None:
            if type(max_response_bytes) is not int or max_response_bytes <= 0:
                raise ValueError("max_response_bytes must be a positive integer")
        if allowed_authority is not None:
            authority_url = urlsplit("https://" + allowed_authority)
            if (not allowed_authority or not allowed_authority.isascii()
                    or authority_url.netloc != allowed_authority
                    or authority_url.hostname is None or authority_url.username is not None
                    or authority_url.path or authority_url.query or authority_url.fragment):
                raise ValueError("allowed_authority must be an HTTPS authority without credentials")
        self.timeout = timeout
        self.user_agent = user_agent
        self.max_response_bytes = max_response_bytes
        self.allowed_authority = allowed_authority
        self.ssl_context, self.tls_trust = select_tls_context(ca_bundle)
        self._restricted_opener = None
        if max_response_bytes is not None or allowed_authority is not None:
            self._restricted_opener = request.build_opener(
                request.HTTPSHandler(context=self.ssl_context), _RejectRedirects()
            )

    def get(self, url: str) -> bytes | TransportFailure:
        try:
            if self._restricted_opener is not None:
                return self._get_restricted(url)
            http_request = request.Request(url, headers={"User-Agent": self.user_agent})
            kwargs = {"timeout": self.timeout}
            if self.ssl_context is not None:
                kwargs["context"] = self.ssl_context
            with request.urlopen(http_request, **kwargs) as response:
                return response.read()
        except Exception as error:
            return TransportFailure(
                getattr(error, "code", None), diagnostic(error), retry_after=_retry_after(error)
            )

    def _get_restricted(self, url: str) -> bytes | TransportFailure:
        destination = urlsplit(url)
        if (destination.scheme != "https" or not destination.netloc
                or destination.username is not None or destination.password is not None
                or (self.allowed_authority is not None
                    and destination.netloc != self.allowed_authority)):
            return TransportFailure(None, "unsupported request authority")
        http_request = request.Request(url, headers={"User-Agent": self.user_agent})
        with self._restricted_opener.open(http_request, timeout=self.timeout) as response:
            if self.max_response_bytes is None:
                return response.read()
            return _read_bounded_response(response, self.max_response_bytes)


__all__ = [
    "TransportFailure",
    "VerifiedJSONTransport",
    "diagnostic",
    "select_tls_context",
]
