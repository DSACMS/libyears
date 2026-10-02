"""Human-readable and JSON output for scan reports."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import json
from typing import Any

from .scan import ScanReport


_REASON_TEXT = {
    "non_exact_version": "exact version not available",
    "unsupported_requirement": "unsupported requirement format",
    "conflicting_versions": "conflicting exact versions",
    "package_not_found": "package not found in PyPI",
    "version_not_found": "used version not found in PyPI",
    "release_date_missing": "release timestamp unavailable",
    "no_stable_release": "no stable release available",
    "registry_error": "registry or transport error",
    "invalid_registry_response": "invalid registry response",
}


def _timestamp(value: datetime) -> str:
    utc = value.astimezone(timezone.utc)
    return utc.isoformat().replace("+00:00", "Z")


def report_to_dict(report: ScanReport, path: str) -> dict[str, Any]:
    """Convert a scan report to the stable JSON data shape."""
    summary = report.summary
    dependencies = []
    for measurement in report.measurements:
        dependency = measurement.dependency
        dependencies.append(
            {
                "ecosystem": dependency.ecosystem,
                "name": dependency.name,
                "used_version": dependency.used_version,
                "used_release_time": _timestamp(dependency.used_release_time),
                "latest_stable_version": dependency.latest_stable_version,
                "latest_stable_release_time": _timestamp(dependency.latest_stable_release_time),
                "libyears": measurement.libyears,
                "timestamp_anomaly": measurement.timestamp_anomaly,
            }
        )
    return {
        "schema_version": 1,
        "metric": "libyears",
        "dependency_scope": "direct",
        "ecosystems": ["pypi"],
        "summary": asdict(summary),
        "dependencies": dependencies,
        "unmeasurable": [
            {
                "ecosystem": item.ecosystem,
                "name": item.name,
                "declared": item.declared,
                "reason": item.reason,
            }
            for item in report.unmeasurable
        ],
    }


def format_json(report: ScanReport, path: str) -> str:
    """Serialize a scan report as indented JSON."""
    return json.dumps(report_to_dict(report, path), indent=2) + "\n"


def format_human(report: ScanReport, path: str) -> str:
    """Format a scan report for terminal readers."""
    summary = report.summary
    lines = [f"Libyears: {path}", ""]
    if summary.dependencies_discovered == 0:
        lines.extend(
            [
                "No supported dependency manifests or dependencies were found.",
                "Currently supported ecosystems: pypi (Python packages from PyPI).",
                "No libyears measurement was calculated.",
            ]
        )
        return "\n".join(lines) + "\n"
    elif summary.dependencies_measured == 0:
        lines.append(
            "No libyears measurement could be calculated "
            f"(0 / {summary.dependencies_discovered} dependencies measured)."
        )
        if report.unmeasurable and all(
            item.reason == "non_exact_version" for item in report.unmeasurable
        ):
            lines.extend(
                [
                    "All discovered dependencies lack exact versions.",
                    "Libyears requires exact dependency versions to produce a reproducible measurement.",
                ]
            )
        else:
            lines.append("All discovered dependencies were unmeasurable; see reasons below.")
        lines.extend(
            [
                "",
                f"Measured: {summary.dependencies_measured} / {summary.dependencies_discovered} dependencies",
                f"Coverage: {_coverage(summary.coverage)}",
            ]
        )
        if report.unmeasurable:
            lines.extend(["", "Unmeasurable:"])
            lines.extend(
                f"  {item.declared}    {_reason_text(item.reason)}"
                for item in report.unmeasurable
            )
        return "\n".join(lines) + "\n"
    elif summary.dependencies_measured < summary.dependencies_discovered:
        lines.append(
            "Partial measurement: "
            f"{summary.dependencies_measured} / {summary.dependencies_discovered} dependencies measured "
            f"({_coverage(summary.coverage)})."
        )
    else:
        lines.append(
            "Measurement complete: "
            f"{summary.dependencies_measured} / {summary.dependencies_discovered} dependencies measured."
        )

    lines.extend(["", "DEPENDENCY       USED       LATEST       LIBYEARS"])
    for measurement in sorted(report.measurements, key=lambda item: item.libyears, reverse=True):
        dependency = measurement.dependency
        lines.append(
            f"{dependency.name:<16} {dependency.used_version:<10} "
            f"{dependency.latest_stable_version:<12} {measurement.libyears:.2f}"
        )
    lines.extend(
        [
            "",
            f"Measured: {summary.dependencies_measured} / {summary.dependencies_discovered} dependencies",
            f"Coverage: {_coverage(summary.coverage)}",
            f"Total:    {_number(summary.total_libyears)} libyears",
            f"Mean:     {_number(summary.mean_libyears)}",
            f"Median:   {_number(summary.median_libyears)}",
            f"Maximum:  {_number(summary.max_libyears)}",
        ]
    )
    if report.unmeasurable:
        lines.extend(["", "Unmeasurable:"])
        lines.extend(
            f"  {item.declared}    {_reason_text(item.reason)}"
            for item in report.unmeasurable
        )
    return "\n".join(lines) + "\n"


def _coverage(value: float | None) -> str:
    return "null" if value is None else f"{value * 100:.1f}%"


def _number(value: float | None) -> str:
    return "null" if value is None else f"{value:.2f}"


def _reason_text(reason: str) -> str:
    return _REASON_TEXT.get(reason, "measurement unavailable")


__all__ = ["format_human", "format_json", "report_to_dict"]
