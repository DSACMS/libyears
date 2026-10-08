"""Human-readable and JSON output for scan reports."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import json
from typing import Any

from .scan import MixedScanReport, ScanReport
from .snapshot import SNAPSHOT_FORMAT


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
    "snapshot_version_missing": "exact version missing from supplied snapshot",
    "snapshot_version_conflict": "conflicting versions in supplied snapshot",
    "snapshot_version_incompatible": "snapshot version does not satisfy declaration",
    "declared_snapshot_conflict": "snapshot version conflicts with exact repository pin",
    "lock_version_missing": "exact version unavailable in package-lock.json",
    "declaration_lock_conflict": "lock version conflicts with exact manifest declaration",
    "unsupported_dependency_source": "unsupported dependency source",
    "unsupported_lockfile_version": "unsupported package-lock version",
    "invalid_lockfile": "invalid package-lock.json",
    "invalid_manifest": "invalid package.json",
}


def _timestamp(value: datetime) -> str:
    utc = value.astimezone(timezone.utc)
    return utc.isoformat().replace("+00:00", "Z")


def _summary_dict(summary: Any) -> dict[str, Any]:
    return asdict(summary)


def _report_parts(report: ScanReport | MixedScanReport) -> tuple[Any, dict[str, Any], list[str], list[Any], list[Any], list[Any], dict[str, Any]]:
    if isinstance(report, MixedScanReport):
        sources = [source for source in report.source_results if source.source_present]
        evidence = {
            source.ecosystem: {
                "declaration_source": source.evidence.declaration_source,
                "snapshot_source": source.evidence.snapshot_source,
            }
            for source in sources
        }
        ecosystems = sorted(set(evidence) | {error.ecosystem for error in report.source_errors})
        summaries = {key: _summary_dict(value) for key, value in report.by_ecosystem.items()}
        return report.summary, evidence, ecosystems, list(report.measurements), list(report.unmeasurable), list(report.source_errors), summaries

    evidence = {"pypi": {
        "declaration_source": "requirements.txt",
        "snapshot_source": ({"format": SNAPSHOT_FORMAT, "path": report.snapshot_source}
                            if report.snapshot_source is not None else None),
    }}
    ecosystems = ["pypi"] if report.summary.dependencies_discovered != 0 else []
    return report.summary, evidence, ecosystems, list(report.measurements), list(report.unmeasurable), [], {"pypi": _summary_dict(report.summary)}


def report_to_dict(report: ScanReport | MixedScanReport, path: str) -> dict[str, Any]:
    """Convert a scan report to the stable schema-v3 JSON data shape."""
    summary, version_evidence, ecosystems, measurements, unmeasurable, source_errors, by_ecosystem = _report_parts(report)
    dependencies = []
    for measurement in measurements:
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
                "version_source": dependency.version_source,
            }
        )
    return {
        "schema_version": 3,
        "metric": "libyears",
        "dependency_scope": "direct",
        "ecosystems": ecosystems,
        "version_evidence": version_evidence,
        "summary": {**asdict(summary), "by_ecosystem": by_ecosystem},
        "dependencies": dependencies,
        "unmeasurable": [
            {
                "ecosystem": item.ecosystem,
                "name": item.name,
                "declared": item.declared,
                "reason": item.reason,
            }
            for item in unmeasurable
        ],
        "source_errors": [asdict(item) for item in source_errors],
    }


def format_json(report: ScanReport, path: str) -> str:
    """Serialize a scan report as indented JSON."""
    return json.dumps(report_to_dict(report, path), indent=2) + "\n"


def format_human(report: ScanReport | MixedScanReport, path: str, *, verbose: bool = False) -> str:
    """Format a scan report for terminal readers."""
    if isinstance(report, MixedScanReport):
        return _format_mixed_human(report, path, verbose=verbose)
    summary = report.summary
    evidence = "Version evidence: requirements.txt"
    if report.snapshot_source is not None:
        evidence += f"; resolved snapshot: {report.snapshot_source}"
    lines = [f"Libyears: {path}", evidence, ""]
    if summary.dependencies_discovered == 0:
        lines.extend(
            [
                "No supported dependency manifests or dependencies were found.",
                "Currently supported ecosystems: pypi (Python packages from PyPI).",
                "No libyears measurement was calculated.",
            ]
        )
        if verbose:
            lines.extend(_diagnostic_lines(report))
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
        if verbose:
            lines.extend(_diagnostic_lines(report))
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

    mixed_sources = {
        measurement.dependency.version_source for measurement in report.measurements
    }
    source_column = len(mixed_sources) > 1
    header = "DEPENDENCY       USED       LATEST       LIBYEARS"
    if source_column:
        header += "  SOURCE"
    lines.extend(["", header])
    for measurement in sorted(report.measurements, key=lambda item: item.libyears, reverse=True):
        dependency = measurement.dependency
        line = (
            f"{dependency.name:<16} {dependency.used_version:<10} "
            f"{dependency.latest_stable_version:<12} {measurement.libyears:.2f}"
        )
        if source_column:
            line += f"  {_source_text(dependency.version_source)}"
        lines.append(line)
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
    if verbose:
        lines.extend(_diagnostic_lines(report))
    return "\n".join(lines) + "\n"


def _format_mixed_human(report: MixedScanReport, path: str, *, verbose: bool) -> str:
    ecosystems = sorted(source.ecosystem for source in report.source_results if source.source_present)
    labels = ", ".join(ecosystems) if ecosystems else "none"
    summary = report.summary
    if len(ecosystems) == 1 and not report.source_errors:
        ecosystem = ecosystems[0]
        lines = [f"Libyears: {path}", f"Ecosystem: {ecosystem}", ""]
        if report.measurements:
            lines.extend(["DEPENDENCY       USED       LATEST       LIBYEARS"])
            for measurement in sorted(report.measurements, key=lambda item: item.libyears, reverse=True):
                dependency = measurement.dependency
                lines.append(
                    f"{dependency.name:<16} {dependency.used_version:<10} "
                    f"{dependency.latest_stable_version:<12} {measurement.libyears:.2f}"
                )
        lines.extend([
            "", f"Measured: {summary.dependencies_measured} / {summary.dependencies_discovered} dependencies",
            f"Coverage: {_coverage(summary.coverage)}",
            f"Total:    {_number(summary.total_libyears)} libyears",
            f"Mean:     {_number(summary.mean_libyears)}",
            f"Median:   {_number(summary.median_libyears)}",
            f"Maximum:  {_number(summary.max_libyears)}",
        ])
        if report.unmeasurable:
            lines.extend(["", "Unmeasurable:"])
            lines.extend(
                f"  {item.declared}    {_reason_text(item.reason)}"
                for item in report.unmeasurable
            )
        if verbose and report.diagnostics:
            lines.extend(["", "Registry diagnostics:", *(f"  {name}: {message}" for name, message in report.diagnostics)])
        return "\n".join(lines) + "\n"

    lines = [f"Libyears: {path}", f"Ecosystems: {labels}", ""]
    lines.append(
        f"Repository: {_coverage(summary.coverage)} coverage; "
        f"{summary.dependencies_measured} / {summary.dependencies_discovered} measured; "
        f"total {_number(summary.total_libyears)}, mean {_number(summary.mean_libyears)}, "
        f"median {_number(summary.median_libyears)}, max {_number(summary.max_libyears)} libyears"
    )
    for ecosystem in sorted(report.by_ecosystem):
        item = report.by_ecosystem[ecosystem]
        lines.append(
            f"{ecosystem}: {_coverage(item.coverage)} coverage; "
            f"{item.dependencies_measured} / {item.dependencies_discovered} measured; "
            f"total {_number(item.total_libyears)}, mean {_number(item.mean_libyears)}, "
            f"median {_number(item.median_libyears)}, max {_number(item.max_libyears)} libyears"
        )
    if report.measurements:
        lines.extend(["", "DEPENDENCY       ECOSYSTEM  USED       LATEST       LIBYEARS  SOURCE"])
        for measurement in sorted(report.measurements, key=lambda item: item.libyears, reverse=True):
            dependency = measurement.dependency
            lines.append(
                f"{dependency.name:<16} {dependency.ecosystem:<10} "
                f"{dependency.used_version:<10} {dependency.latest_stable_version:<12} "
                f"{measurement.libyears:.2f}  {_source_text(dependency.version_source)}"
            )
    if report.unmeasurable:
        lines.extend(["", "Unmeasurable:"])
        lines.extend(
            f"  {item.ecosystem}: {item.name} ({item.declared})    {_reason_text(item.reason)}"
            for item in report.unmeasurable
        )
    if report.source_errors:
        lines.extend(["", "Source errors:"])
        for error in report.source_errors:
            explanation = "npm manifest discovery failed; no npm dependencies were invented" if error.reason == "invalid_manifest" else _reason_text(error.reason)
            lines.append(f"  {error.ecosystem} {error.source}: {explanation}")
    if verbose:
        if report.tls_trust:
            lines.extend(["", f"TLS trust: {report.tls_trust}"])
        if report.diagnostics:
            lines.extend(["Registry diagnostics:", *(f"  {name}: {message}" for name, message in report.diagnostics)])
    return "\n".join(lines) + "\n"


def _diagnostic_lines(report: ScanReport) -> list[str]:
    if not report.diagnostics and not report.tls_trust:
        return []
    lines = [""]
    if report.tls_trust:
        lines.append(f"TLS trust: {report.tls_trust}")
    if report.diagnostics:
        lines.append("Registry diagnostics:")
        lines.extend(f"  {name}: {message}" for name, message in report.diagnostics)
    return lines


def _coverage(value: float | None) -> str:
    return "null" if value is None else f"{value * 100:.1f}%"


def _number(value: float | None) -> str:
    return "null" if value is None else f"{value:.2f}"


def _reason_text(reason: str) -> str:
    return _REASON_TEXT.get(reason, "measurement unavailable")


def _source_text(source: str) -> str:
    return {
        "requirements_exact": "requirements.txt",
        "resolved_snapshot": "snapshot",
    }.get(source, source)


__all__ = ["format_human", "format_json", "report_to_dict"]
