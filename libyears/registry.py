"""Verified JSON-over-HTTPS transport shared by registry adapters."""

from __future__ import annotations

from dataclasses import dataclass
import math
import os
import ssl
import stat
import sys
import sysconfig
from pathlib import Path
from typing import Any
from urllib import error as urlerror, request


@dataclass(frozen=True, slots=True)
class TransportFailure:
    """Transport details that an adapter maps to registry-specific reasons."""

    status: Any
    diagnostic: str


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
    ) -> None:
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be finite and positive")
        self.timeout = timeout
        self.user_agent = user_agent
        self.ssl_context, self.tls_trust = select_tls_context(ca_bundle)

    def get(self, url: str) -> bytes | TransportFailure:
        http_request = request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            kwargs = {"timeout": self.timeout}
            if self.ssl_context is not None:
                kwargs["context"] = self.ssl_context
            with request.urlopen(http_request, **kwargs) as response:
                return response.read()
        except Exception as error:
            return TransportFailure(getattr(error, "code", None), diagnostic(error))


__all__ = [
    "TransportFailure",
    "VerifiedJSONTransport",
    "diagnostic",
    "select_tls_context",
]
