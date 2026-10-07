"""PyPI JSON registry adapter."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import math
import os
import re
import ssl
import stat
import sys
import sysconfig
from pathlib import Path
from typing import Any
from urllib import error as urlerror, request


PACKAGE_NOT_FOUND = "package_not_found"
VERSION_NOT_FOUND = "version_not_found"
RELEASE_DATE_MISSING = "release_date_missing"
NO_STABLE_RELEASE = "no_stable_release"
REGISTRY_ERROR = "registry_error"
INVALID_REGISTRY_RESPONSE = "invalid_registry_response"

_PRERELEASE = re.compile(r"(?:alpha|beta|preview|dev|rc|c\d|a\d|b\d)", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class PyPIResult:
    """Metadata needed to measure one exact-pinned package."""

    name: str
    used_version: str
    used_release_time: datetime
    latest_stable_version: str
    latest_stable_release_time: datetime


@dataclass(frozen=True, slots=True)
class RegistryFailure:
    """A stable, machine-readable registry lookup failure."""

    name: str
    used_version: str
    reason: str
    diagnostic: str | None = None


def _timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(timezone.utc)


def _release_files(release: Any) -> list[tuple[datetime, bool]]:
    if not isinstance(release, list):
        return []
    files: list[tuple[datetime, bool]] = []
    for item in release:
        if not isinstance(item, dict):
            continue
        timestamp = _timestamp(item.get("upload_time_iso_8601"))
        if timestamp is None:
            timestamp = _timestamp(item.get("upload_time"))
        if timestamp is not None:
            files.append((timestamp, bool(item.get("yanked", False))))
    return files


def _canonical_release_time(files: list[tuple[datetime, bool]]) -> datetime | None:
    """Use the first valid upload timestamp as the release's canonical time."""
    return min((timestamp for timestamp, _ in files), default=None)


def _is_prerelease(version: str) -> bool:
    return _PRERELEASE.search(version) is not None


class PyPIAdapter:
    """Fetch package metadata from PyPI's JSON API."""

    def __init__(self, *, timeout: float = 10.0, user_agent: str = "libyears/0.1", ca_bundle: str | None = None) -> None:
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be finite and positive")
        self.timeout = timeout
        self.user_agent = user_agent
        self.ssl_context, self.tls_trust = select_tls_context(ca_bundle)

    def lookup(self, name: str, used_version: str) -> PyPIResult | RegistryFailure:
        """Resolve release timestamps for a normalized package and exact version."""
        url = f"https://pypi.org/pypi/{name}/json"
        http_request = request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            kwargs = {"timeout": self.timeout}
            if self.ssl_context is not None:
                kwargs["context"] = self.ssl_context
            with request.urlopen(http_request, **kwargs) as response:
                response_body = response.read()
        except Exception as error:
            code = getattr(error, "code", None)
            if code == 404:
                return RegistryFailure(name, used_version, PACKAGE_NOT_FOUND, "HTTP 404")
            return RegistryFailure(name, used_version, REGISTRY_ERROR, _diagnostic(error))

        try:
            payload = json.loads(response_body.decode("utf-8"))
        except (AttributeError, TypeError, UnicodeError, json.JSONDecodeError):
            return RegistryFailure(name, used_version, INVALID_REGISTRY_RESPONSE, "malformed registry response (invalid JSON)")

        if not isinstance(payload, dict) or not isinstance(payload.get("releases"), dict):
            return RegistryFailure(name, used_version, INVALID_REGISTRY_RESPONSE, "malformed registry response (unexpected structure)")
        releases = payload["releases"]
        if used_version not in releases:
            return RegistryFailure(name, used_version, VERSION_NOT_FOUND)

        used_files = _release_files(releases[used_version])
        if not used_files:
            return RegistryFailure(name, used_version, RELEASE_DATE_MISSING)
        used_release_time = _canonical_release_time(used_files)

        candidates: list[tuple[datetime, str]] = []
        for version, release in releases.items():
            if not isinstance(version, str) or _is_prerelease(version):
                continue
            files = _release_files(release)
            if not files or all(yanked for _, yanked in files):
                continue
            release_time = _canonical_release_time(files)
            if release_time is not None:
                candidates.append((release_time, version))
        if not candidates:
            return RegistryFailure(name, used_version, NO_STABLE_RELEASE)

        latest_timestamp, latest_version = max(candidates, key=lambda candidate: candidate[0])
        return PyPIResult(name, used_version, used_release_time, latest_version, latest_timestamp)

    resolve = lookup


def _diagnostic(error: Exception) -> str:
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
    """Select verified TLS trust using explicit, Python, then pip-bundled trust."""
    if ca_bundle:
        return ssl.create_default_context(cafile=ca_bundle), f"explicit CA bundle: {ca_bundle}"

    env_file = os.environ.get("SSL_CERT_FILE")
    env_dir = os.environ.get("SSL_CERT_DIR")
    try:
        context = ssl.create_default_context()
    except (OSError, ssl.SSLError):
        # An explicit OpenSSL override is authoritative; do not silently replace it.
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

    # Fail closed: an empty verified context retains normal certificate checks.
    return ssl.create_default_context(), "Python default trust store"


def lookup_package(
    name: str, used_version: str, *, timeout: float = 10.0, user_agent: str = "libyears/0.1"
) -> PyPIResult | RegistryFailure:
    """Convenience wrapper around :class:`PyPIAdapter`."""
    return PyPIAdapter(timeout=timeout, user_agent=user_agent).lookup(name, used_version)


__all__ = [
    "INVALID_REGISTRY_RESPONSE",
    "NO_STABLE_RELEASE",
    "PACKAGE_NOT_FOUND",
    "PyPIAdapter",
    "PyPIResult",
    "RELEASE_DATE_MISSING",
    "REGISTRY_ERROR",
    "RegistryFailure",
    "select_tls_context",
    "VERSION_NOT_FOUND",
    "lookup_package",
]
