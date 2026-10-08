"""PyPI JSON registry adapter."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import re
from typing import Any

from .registry import (
    TransportFailure,
    VerifiedJSONTransport,
    diagnostic as _diagnostic,
    select_tls_context,
)
from .model import RegistryFailure, RegistryResult


PACKAGE_NOT_FOUND = "package_not_found"
VERSION_NOT_FOUND = "version_not_found"
RELEASE_DATE_MISSING = "release_date_missing"
NO_STABLE_RELEASE = "no_stable_release"
REGISTRY_ERROR = "registry_error"
INVALID_REGISTRY_RESPONSE = "invalid_registry_response"

_PRERELEASE = re.compile(r"(?:alpha|beta|preview|dev|rc|c\d|a\d|b\d)", re.IGNORECASE)


PyPIResult = RegistryResult


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
        self.transport = VerifiedJSONTransport(
            timeout=timeout, user_agent=user_agent, ca_bundle=ca_bundle
        )
        self.timeout = self.transport.timeout
        self.user_agent = self.transport.user_agent
        self.ssl_context = self.transport.ssl_context
        self.tls_trust = self.transport.tls_trust

    def lookup(self, name: str, used_version: str) -> PyPIResult | RegistryFailure:
        """Resolve release timestamps for a normalized package and exact version."""
        url = f"https://pypi.org/pypi/{name}/json"
        response_body = self.transport.get(url)
        if isinstance(response_body, TransportFailure):
            if response_body.status == 404:
                return RegistryFailure(name, used_version, PACKAGE_NOT_FOUND, "HTTP 404")
            return RegistryFailure(
                name, used_version, REGISTRY_ERROR, response_body.diagnostic
            )

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
