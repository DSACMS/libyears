"""PyPI JSON registry adapter."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import re
from typing import Any
from urllib import request


PACKAGE_NOT_FOUND = "package_not_found"
VERSION_NOT_FOUND = "version_not_found"
RELEASE_DATE_MISSING = "release_date_missing"
NO_STABLE_RELEASE = "no_stable_release"
REGISTRY_ERROR = "registry_error"
INVALID_REGISTRY_RESPONSE = "invalid_registry_response"

_PRERELEASE = re.compile(r"(?:alpha|beta|preview|dev|rc|a\d|b\d)", re.IGNORECASE)


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


def _is_prerelease(version: str) -> bool:
    return _PRERELEASE.search(version) is not None


class PyPIAdapter:
    """Fetch package metadata from PyPI's JSON API."""

    def __init__(self, *, timeout: float = 10.0, user_agent: str = "libyears/0.1") -> None:
        if timeout <= 0:
            raise ValueError("timeout must be finite and positive")
        self.timeout = timeout
        self.user_agent = user_agent

    def lookup(self, name: str, used_version: str) -> PyPIResult | RegistryFailure:
        """Resolve release timestamps for a normalized package and exact version."""
        url = f"https://pypi.org/pypi/{name}/json"
        http_request = request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            with request.urlopen(http_request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception as error:
            if getattr(error, "code", None) == 404:
                return RegistryFailure(name, used_version, PACKAGE_NOT_FOUND)
            return RegistryFailure(name, used_version, REGISTRY_ERROR)

        if not isinstance(payload, dict) or not isinstance(payload.get("releases"), dict):
            return RegistryFailure(name, used_version, INVALID_REGISTRY_RESPONSE)
        releases = payload["releases"]
        if used_version not in releases:
            return RegistryFailure(name, used_version, VERSION_NOT_FOUND)

        used_files = _release_files(releases[used_version])
        if not used_files:
            return RegistryFailure(name, used_version, RELEASE_DATE_MISSING)
        used_release_time = min(timestamp for timestamp, _ in used_files)

        candidates: list[tuple[datetime, str]] = []
        for version, release in releases.items():
            if not isinstance(version, str) or _is_prerelease(version):
                continue
            files = _release_files(release)
            if not files or all(yanked for _, yanked in files):
                continue
            candidates.append((max(timestamp for timestamp, _ in files), version))
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
    "VERSION_NOT_FOUND",
    "lookup_package",
]
