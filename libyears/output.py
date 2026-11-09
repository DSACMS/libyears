"""Human-readable and JSON output for scan reports."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import json
from typing import Any

from .model import DependencyMeasurement, GemfileEvidence, NuGetEvidence, RubyGemsEvidence
from .nuget_discovery import NuGetRecognition
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
    "ambiguous_lock_evidence": "ambiguous exact version evidence in yarn.lock",
    "unsupported_lockfile_format": "unsupported or unclassifiable Yarn format",
    "conflicting_resolution_sources": "conflicting resolution sources; neither lockfile supplied evidence",
}


def _timestamp(value: datetime) -> str:
    utc = value.astimezone(timezone.utc)
    return utc.isoformat().replace("+00:00", "Z")


def _summary_dict(summary: Any) -> dict[str, Any]:
    return asdict(summary)


def _source_evidence_dict(source) -> dict[str, Any]:
    evidence = source.evidence
    result = {"declaration_source": evidence.declaration_source,
              "snapshot_source": evidence.snapshot_source}
    if evidence.include_format:
        result["format"] = evidence.format
    if evidence.scope is not None:
        result["scope"] = evidence.scope
    if evidence.publication_basis is not None:
        result["publication_basis"] = evidence.publication_basis
    if evidence.requested_groups is not None:
        result["requested_groups"] = sorted(set(evidence.requested_groups))
    if source.ecosystem == "nuget":
        result.update(provenance_source=evidence.provenance_source,
                      framework=evidence.framework, trust_basis=evidence.trust_basis,
                      population_basis=evidence.population_basis)
        if evidence.population_limitations:
            result["population_limitations"] = list(evidence.population_limitations)
    return result


def _report_parts(report: ScanReport | MixedScanReport) -> tuple[Any, dict[str, Any], list[str], list[Any], list[Any], list[Any], dict[str, Any]]:
    if isinstance(report, MixedScanReport):
        sources = [source for source in report.source_results if source.source_present]
        evidence = {source.ecosystem: _source_evidence_dict(source) for source in sources
                    if not (report.nuget_repository and source.ecosystem == "nuget")}
        ecosystems = sorted({source.ecosystem for source in sources}
                            | {error.ecosystem for error in report.source_errors})
        summaries = {key: _summary_dict(value) for key, value in report.by_ecosystem.items()}
        return report.summary, evidence, ecosystems, list(report.measurements), list(report.unmeasurable), list(report.source_errors), summaries

    evidence = {"pypi": {
        "declaration_source": "requirements.txt",
        "snapshot_source": ({"format": SNAPSHOT_FORMAT, "path": report.snapshot_source}
                            if report.snapshot_source is not None else None),
    }}
    ecosystems = ["pypi"] if report.summary.dependencies_discovered != 0 else []
    return report.summary, evidence, ecosystems, list(report.measurements), list(report.unmeasurable), [], {"pypi": _summary_dict(report.summary)}


def _ruby_evidence_dict(evidence: RubyGemsEvidence) -> dict[str, Any]:
    """Serialize only established artifacts, omitting unavailable populations."""
    result = {"selected_artifacts": [
        {"version": item.version, "platform": item.platform, "source": item.source}
        for item in evidence.selected_artifacts
    ]}
    for field, artifacts in (
        ("used_publication_artifacts", evidence.used_publication_artifacts),
        ("latest_publication_artifacts", evidence.latest_publication_artifacts),
    ):
        if artifacts is None:
            continue
        rows = []
        for artifact in artifacts:
            row = {
                "version": artifact.version,
                "platform": artifact.platform,
                "publication_time": _timestamp(artifact.publication_time),
            }
            if artifact.yanked is not None:
                row["yanked"] = artifact.yanked
            rows.append(row)
        result[field] = rows
    return result


def _gemfile_evidence_dict(evidence: GemfileEvidence) -> dict[str, Any]:
    """Keep safe membership evidence distinct from established lock text."""
    result = {
        "declared_groups": sorted(set(evidence.declared_groups)),
        "declaration_requirements": list(evidence.declaration_requirements),
    }
    if evidence.include_lock_requirement:
        result["lock_requirement"] = evidence.lock_requirement
    return result


def _nuget_evidence_dict(evidence: NuGetEvidence) -> dict[str, Any]:
    """Emit safe established facts, never private authority or unpassed stages."""
    result = {
        "project": evidence.project,
        "framework": evidence.framework,
        "requested": evidence.requested,
        "origin_state": evidence.origin_state,
        "content_hash_state": evidence.content_hash_state,
        "publication_basis": evidence.publication_basis,
    }
    for field in ("lock_requested", "selected_version", "normalized_version", "selection_source"):
        value = getattr(evidence, field)
        if value is not None:
            result[field] = value
    if evidence.population_basis is not None:
        result["population_basis"] = evidence.population_basis
    if evidence.comparator_basis is not None:
        result['comparator_basis'] = evidence.comparator_basis
        if evidence.comparator_limitations:
            result['comparator_limitations'] = list(evidence.comparator_limitations)
    if evidence.measurement_basis is not None:
        result['measurement_basis'] = evidence.measurement_basis
        result['namespace_basis'] = evidence.namespace_basis
        result['assurance'] = _nuget_assurance(evidence)
    for field in ("used_publication", "latest_publication"):
        publication = getattr(evidence, field)
        if publication is not None:
            result[field] = {
                "version": publication.version,
                "created": _timestamp(publication.created),
                "listed": publication.listed,
            }
    return result


def _nuget_assurance(evidence: NuGetEvidence) -> dict[str, Any]:
    local = evidence.local_content_state
    if evidence.content_hash_state == 'public_agreement':
        public = 'public_agreement'
    elif local == 'local_agreement' and evidence.content_hash_state in ('mismatch', 'unavailable'):
        public = evidence.content_hash_state
    else:
        public = 'not_checked'
    producer = evidence.namespace_basis == 'accepted_producer_origin'
    limitations = [('policy_selected_snapshot_not_evaluated_runtime'
                    if evidence.measurement_basis == 'public_comparator_version_age'
                    else 'accepted_snapshot_not_evaluated_runtime'),
                   'acquisition_testimony_not_authenticated' if producer else 'acquisition_not_established',
                   'reproducibility_not_established', 'deployment_not_established']
    if public != 'public_agreement':
        limitations.append('content_correspondence_not_established')
    return {'producer_event': 'asserted' if producer else 'unavailable',
            'local_content': local, 'public_content': public, 'limitations': limitations}


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
        if dependency.rubygems_evidence is not None:
            dependencies[-1]["rubygems_evidence"] = _ruby_evidence_dict(dependency.rubygems_evidence)
        if dependency.gemfile_evidence is not None:
            dependencies[-1]["gemfile_evidence"] = _gemfile_evidence_dict(dependency.gemfile_evidence)
        if dependency.nuget_evidence is not None:
            dependencies[-1]["nuget_evidence"] = _nuget_evidence_dict(dependency.nuget_evidence)
            if dependency.nuget_evidence.source_id is not None:
                dependencies[-1]["source_id"] = dependency.nuget_evidence.source_id
    failures = []
    for item in unmeasurable:
        row = {"ecosystem": item.ecosystem, "name": item.name,
               "declared": item.declared, "reason": item.reason}
        if getattr(item, "rubygems_evidence", None) is not None:
            row["rubygems_evidence"] = _ruby_evidence_dict(item.rubygems_evidence)
        if getattr(item, "gemfile_evidence", None) is not None:
            row["gemfile_evidence"] = _gemfile_evidence_dict(item.gemfile_evidence)
        if getattr(item, "nuget_evidence", None) is not None:
            row["nuget_evidence"] = _nuget_evidence_dict(item.nuget_evidence)
            if item.nuget_evidence.source_id is not None:
                row["source_id"] = item.nuget_evidence.source_id
        failures.append(row)
    errors = []
    repository_mode = isinstance(report, MixedScanReport) and report.nuget_repository
    for error in source_errors:
        row = {"ecosystem": error.ecosystem, "source": error.source, "reason": error.reason}
        if repository_mode and error.ecosystem == "nuget":
            row["source_id"] = error.source_id
        errors.append(row)
    result = {
        "schema_version": 3,
        "metric": "libyears",
        "dependency_scope": "direct",
        "ecosystems": ecosystems,
        "version_evidence": version_evidence,
        "summary": {**asdict(summary), "by_ecosystem": by_ecosystem},
        "dependencies": dependencies,
        "unmeasurable": failures,
        "source_errors": errors,
    }
    if repository_mode and "nuget" in ecosystems:
        result["nuget_sources"] = [
            {"source_id": source.source_id,
             "version_evidence": _source_evidence_dict(source),
             "summary": _summary_dict(report.by_nuget_source[source.source_id]),
             "measurement_available": source.measurement_available}
            for source in report.source_results if source.ecosystem == "nuget"]
    return result


def format_json(report: ScanReport, path: str) -> str:
    """Serialize a scan report as indented JSON."""
    return json.dumps(report_to_dict(report, path), indent=2) + "\n"


def _measurement_table(
    measurements: list[DependencyMeasurement], *,
    ecosystem_column: bool = False, source_column: bool = False,
) -> list[str]:
    """Align rendered cells, including headers, using plain-text padding."""
    headers = ["DEPENDENCY"]
    if ecosystem_column:
        headers.append("ECOSYSTEM")
    headers.extend(["USED", "LATEST", "LIBYEARS"])
    numeric_column = headers.index("LIBYEARS")
    if source_column:
        headers.append("SOURCE")

    rows = []
    for measurement in measurements:
        dependency = measurement.dependency
        cells = [dependency.name]
        if ecosystem_column:
            cells.append(dependency.ecosystem)
        cells.extend([dependency.used_version, dependency.latest_stable_version,
                      f"{measurement.libyears:.2f}"])
        if source_column:
            cells.append(_source_text(dependency.version_source))
        rows.append(cells)

    widths = [len(header) for header in headers]
    for cells in rows:
        for index, cell in enumerate(cells):
            widths[index] = max(widths[index], len(cell))
    lines = []
    for cells in [headers, *rows]:
        padded = []
        for index, cell in enumerate(cells):
            if index == numeric_column:
                padded.append(cell.rjust(widths[index]))
            else:
                padded.append(cell.ljust(widths[index]))
        lines.append("  ".join(padded).rstrip())
    return lines


def _nuget_recognition_lines(recognition: NuGetRecognition | None) -> list[str]:
    if recognition is None or (recognition.status == 'complete' and not recognition.candidates):
        return []
    if recognition.status == 'complete':
        lines = [f'NuGet / C# project candidates: {len(recognition.candidates)} (bounded search).',
                 'Search covers root through depth 4; hidden/generated/dependency directories are excluded.']
        lines.extend(f'  {json.dumps(name, ensure_ascii=True)}' for name in recognition.candidates)
    else:
        label = 'incomplete' if recognition.status == 'incomplete' else 'unavailable'
        lines = [f'NuGet project recognition {label}; presence and candidate count are undetermined.']
    lines.extend([
        'No NuGet measurement was performed. Explicit project selection is required.',
        'Use the chosen project\'s parent directory as PATH and its filename as NAME.csproj:',
        '  python3 -m libyears PATH --nuget-project NAME.csproj',
        'Measurement still requires an eligible project, packages.lock.json and an explicitly',
        'accepted --nuget-provenance NAME.json witness. Candidate names alone establish none of these.',
        '',
    ])
    return lines


def format_human(report: ScanReport | MixedScanReport, path: str, *, verbose: bool = False,
                 nuget_recognition: NuGetRecognition | None = None) -> str:
    """Format a scan report for terminal readers."""
    if isinstance(report, MixedScanReport):
        return _format_mixed_human(report, path, verbose=verbose, nuget_recognition=nuget_recognition)
    summary = report.summary
    evidence = "Version evidence: requirements.txt"
    if report.snapshot_source is not None:
        evidence += f"; resolved snapshot: {report.snapshot_source}"
    lines = [f"Libyears: {path}", evidence, ""]
    lines.extend(_nuget_recognition_lines(nuget_recognition))
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
    ordered = sorted(report.measurements, key=lambda item: item.libyears, reverse=True)
    lines.extend(["", *_measurement_table(ordered, source_column=source_column)])
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


def _format_mixed_human(report: MixedScanReport, path: str, *, verbose: bool,
                        nuget_recognition: NuGetRecognition | None = None) -> str:
    ecosystems = sorted({source.ecosystem for source in report.source_results if source.source_present})
    labels = ", ".join(ecosystems) if ecosystems else "none"
    recognition_lines = _nuget_recognition_lines(nuget_recognition)
    summary = report.summary
    yarn_evidence = any(
        source.evidence.snapshot_source == "yarn.lock"
        for source in report.source_results
    )
    scoped_ruby = next((source for source in report.source_results
                        if source.ecosystem == "rubygems"
                        and source.evidence.requested_groups is not None), None)
    ruby_disclosure = []
    if "rubygems" in ecosystems:
        ruby_disclosure = [
            "RubyGems version evidence: Gemfile.lock.",
            "All direct dependencies recorded in Gemfile.lock; groups are not interpreted.",
            "Publication dates are earliest admissible supported observable evidence, not complete historical knowledge.",
            "Missing public records prove neither yanking nor never-existence; record disappearance may change future measurements.",
            "Null counts and coverage mean unavailable.",
        ]
    if scoped_ruby is not None:
        ruby_disclosure = _scoped_ruby_disclosure(scoped_ruby, report.by_ecosystem["rubygems"])
    nuget_source = next((source for source in report.source_results
                         if source.ecosystem == "nuget" and source.source_present), None)
    nuget_disclosure = []
    heading = f"Libyears: {path}"
    if nuget_source is not None:
        # The root and raw diagnostics can contain private paths. NuGet reports
        # identify inputs by the safe selected filenames and stable facts only.
        heading = "Libyears: selected repository"
        if report.nuget_repository:
            nuget_disclosure = _nuget_repository_disclosure(report, verbose=verbose)
        else:
            nuget_disclosure = _nuget_disclosure(nuget_source, report.by_ecosystem["nuget"], verbose=verbose)
    if len(ecosystems) == 1 and not report.source_errors:
        ecosystem = ecosystems[0]
        ecosystem_label = 'Ecosystem scanned for measurement' if recognition_lines else 'Ecosystem'
        lines = [heading, f"{ecosystem_label}: {ecosystem}", ""]
        lines.extend(recognition_lines)
        lines.extend(ruby_disclosure)
        lines.extend(nuget_disclosure)
        if yarn_evidence:
            lines.append("Version evidence: yarn.lock")
        if report.measurements:
            ordered = sorted(report.measurements, key=lambda item: item.libyears, reverse=True)
            table = _measurement_table(ordered)
            lines.append(table[0])
            for measurement, row in zip(ordered, table[1:]):
                dependency = measurement.dependency
                lines.append(row)
                lines.extend(_gemfile_detail_lines(dependency.gemfile_evidence))
                lines.extend(_nuget_detail_lines(dependency.nuget_evidence, verbose=verbose))
                if dependency.nuget_evidence is not None and (verbose or measurement.timestamp_anomaly):
                    lines.append(_nuget_anomaly_line(measurement.timestamp_anomaly))
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
            for item in report.unmeasurable:
                declaration = item.declared
                if yarn_evidence:
                    declaration = f"{item.name} ({item.declared})"
                reason = _dependency_reason_text(item.reason, yarn_evidence, item.ecosystem)
                if item.gemfile_evidence is not None:
                    reason = _scoped_dependency_reason(item.reason)
                lines.append(f"  {declaration}    {reason}")
                lines.extend(_gemfile_detail_lines(item.gemfile_evidence))
                lines.extend(_nuget_detail_lines(item.nuget_evidence, verbose=verbose))
        if verbose and nuget_source is None and report.tls_trust:
            lines.extend(["", f"TLS trust: {report.tls_trust}"])
        if verbose and nuget_source is None and report.diagnostics:
            lines.extend(["", "Registry diagnostics:", *(f"  {name}: {message}" for name, message in report.diagnostics)])
        return "\n".join(lines) + "\n"

    ecosystem_label = 'Ecosystems scanned for measurement' if recognition_lines else 'Ecosystems'
    lines = [heading, f"{ecosystem_label}: {labels}", ""]
    lines.extend(recognition_lines)
    lines.extend(ruby_disclosure)
    lines.extend(nuget_disclosure)
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
        ordered = sorted(report.measurements, key=lambda item: item.libyears, reverse=True)
        table = _measurement_table(ordered, ecosystem_column=True, source_column=True)
        lines.extend(["", table[0]])
        for measurement, row in zip(ordered, table[1:]):
            dependency = measurement.dependency
            lines.append(row)
            lines.extend(_gemfile_detail_lines(dependency.gemfile_evidence))
            lines.extend(_nuget_detail_lines(dependency.nuget_evidence, verbose=verbose))
            if dependency.nuget_evidence is not None and (verbose or measurement.timestamp_anomaly):
                lines.append(_nuget_anomaly_line(measurement.timestamp_anomaly))
    if report.unmeasurable:
        lines.extend(["", "Unmeasurable:"])
        for item in report.unmeasurable:
            reason = _dependency_reason_text(item.reason, yarn_evidence and item.ecosystem == 'npm', item.ecosystem)
            if item.gemfile_evidence is not None:
                reason = _scoped_dependency_reason(item.reason)
            declaration = item.declared if item.ecosystem == 'nuget' else f"{item.name} ({item.declared})"
            lines.append(f"  {item.ecosystem}: {declaration}    {reason}")
            lines.extend(_gemfile_detail_lines(item.gemfile_evidence))
            lines.extend(_nuget_detail_lines(item.nuget_evidence, verbose=verbose))
    if report.source_errors:
        lines.extend(["", "Source errors:"])
        for error in report.source_errors:
            explanation = "npm manifest discovery failed; no npm dependencies were invented" if error.reason == "invalid_manifest" else _reason_text(error.reason)
            if error.ecosystem == "rubygems":
                explanation = _ruby_reason_text(error.reason)
            if error.ecosystem == "nuget":
                explanation = _nuget_reason_text(error.reason)
            if error.source == "yarn.lock":
                context = None if nuget_source is not None else dict(report.diagnostics).get("yarn.lock")
                explanation = context or _reason_text(error.reason)
                explanation += "; npm dependencies could not be measured from this evidence source"
            source_name = error.source
            if report.nuget_repository and error.ecosystem == "nuget":
                source_name = f"{json.dumps(error.source_id, ensure_ascii=True)} {json.dumps(error.source, ensure_ascii=True)}"
            lines.append(f"  {error.ecosystem} {source_name}: {explanation}")
    if verbose and nuget_source is None:
        if report.tls_trust:
            lines.extend(["", f"TLS trust: {report.tls_trust}"])
        if report.diagnostics:
            lines.extend(["Registry diagnostics:", *(f"  {name}: {message}" for name, message in report.diagnostics)])
    return "\n".join(lines) + "\n"


def _nuget_repository_disclosure(report, *, verbose=False) -> list[str]:
    sources = [source for source in report.source_results if source.ecosystem == "nuget"]
    lines = [
        "NuGet repository sources: independent direct-dependency occurrences; no cross-project deduplication.",
        "Search covers root through depth 4; hidden/generated/dependency directories and links/reparse points are excluded.",
        "ProjectReference edges add no external dependency rows; solutions do not define the population.",
        "Witnesses are accepted only through explicit --nuget-witness PROJECT=NAME.json mappings.",
    ]
    # Reuse the established trust/date/scope explanation once, without claiming
    # a representative project or whole-ecosystem availability for one source.
    conventional = any(
        item.nuget_evidence is not None
        and item.nuget_evidence.comparator_basis == 'conventional_public_policy'
        for item in (*report.unmeasurable, *(m.dependency for m in report.measurements)))
    automatic = any(
        item.nuget_evidence is not None
        and item.nuget_evidence.comparator_basis in ('repository_mapping', 'conventional_public_policy')
        for item in (*report.unmeasurable, *(m.dependency for m in report.measurements)))
    lines.extend(_nuget_policy_lines(verbose=verbose, conventional=conventional, automatic=automatic))
    for source in sources:
        summary = report.by_nuget_source[source.source_id]
        evidence = source.evidence
        label = json.dumps(source.source_id, ensure_ascii=True)
        population = 'unknown' if summary.dependencies_discovered is None else str(summary.dependencies_discovered)
        measured = 'null' if summary.dependencies_measured is None else str(summary.dependencies_measured)
        available = 'available' if source.measurement_available else 'unavailable'
        lines.append(f"NuGet source {label}: population {population}; measurement {available}; "
                     f"{measured} / {population} measured; {_coverage(summary.coverage)} coverage; "
                     f"total {_number(summary.total_libyears)}, mean {_number(summary.mean_libyears)}, "
                     f"median {_number(summary.median_libyears)}, max {_number(summary.max_libyears)} libyears.")
        lines.extend(_nuget_population_lines(evidence, verbose=verbose))
        if not verbose:
            continue
        lines.append(f"  Project: {json.dumps(evidence.declaration_source, ensure_ascii=True)}; "
                     f"framework: {evidence.framework or 'unavailable'}; "
                     f"snapshot: {json.dumps(evidence.snapshot_source, ensure_ascii=True)}; "
                     f"witness: {json.dumps(evidence.provenance_source, ensure_ascii=True)}; "
                     f"lock: {'accepted' if evidence.format == 'packages_lock_v1' else 'unavailable'}.")
    return lines


def _nuget_population_lines(evidence, *, verbose=False) -> list[str]:
    lines = []
    if evidence.population_basis == 'qualified_repository_snapshot':
        lines.append("  NuGet population basis: policy-selected current repository snapshot (external Direct records).")
    if evidence.population_basis == 'resolved_snapshot':
        lines.append("  NuGet population basis: accepted resolved snapshot (external Direct records).")
    if verbose:
        lines.append("  Population basis: " + evidence.population_basis + '.')
        if evidence.population_limitations:
            lines.append("  Population limitations: " + ', '.join(evidence.population_limitations) + '.')
    return lines


def _nuget_policy_lines(*, verbose=False, conventional=False, automatic=False) -> list[str]:
    lines = [
        ("NuGet measures qualified project/lock snapshot versions against an authorized public comparator."
         if automatic else "NuGet measures accepted project/lock snapshot versions in an explicitly accepted public namespace."),
        "Stronger assurance is separate; use --verbose or JSON to inspect evidence and limitations.",
    ]
    if conventional:
        lines.insert(1, "Conventional nuget.org comparison assumes namespace correspondence; external configuration is uninspected.")
        lines.insert(2, "A private namesake or fork may have a different history; public lookup discloses the package identity.")
        lines.insert(3, "Comparator policy does not establish acquisition, content correspondence or producer/restore history.")
    if not verbose:
        return lines
    return lines + [
        "Scope: all supported explicit direct PackageReferences, including test, tool, analyzer and PrivateAssets references.",
        "Trust basis: explicit version-1 producer testimony, version-2 retained snapshot/namespace testimony, or version-3 fallback population/namespace testimony.",
        "Version 3 accepts the bound retained external Direct population only when declaration-first population is unsupported; namespace remains separate.",
        "Version 1 retains native NuGet package provenance plus contemporaneous producer attestation, bound to the same event, "
        "exact project/lock bytes, framework and required input-influence assertions.",
        "Retrospective replay does not substitute for producer attestation of the original event.",
        "Version 2 asserts snapshot association and applicable namespace, without acquisition-origin or event evidence.",
        "asserted_public is supplier testimony; public_content_verified and public_agreement require public identity and SHA512 correspondence.",
        "Missing or mismatched optional hashes narrow assurance; unknown/private/conflicting namespace prevents lookup.",
        "This supplied snapshot does not establish evaluated MSBuild completeness, installed/deployed/runtime scope, "
        "restore success, compatibility or cryptographic provenance; hashes compare supplied content assertions, not producing history.",
        "Publication basis: first receipt by nuget.org from catalog created, not original upstream release.",
        "Latest comparator: greatest currently listed stable version; no framework, request or compatibility filter.",
        "Missing public records do not establish never-existence; changed listing or records may change future measurements.",
    ]


def _nuget_disclosure(source, summary, *, verbose=False) -> list[str]:
    evidence = source.evidence
    lines = [
        f"NuGet project: {evidence.declaration_source}; framework: {evidence.framework or 'unavailable'}.",
        f"NuGet declaration source: {evidence.declaration_source}; version snapshot: {evidence.snapshot_source}; "
        f"provenance source: {evidence.provenance_source or 'not supplied'}.",
    ]
    lines.extend(_nuget_policy_lines(verbose=verbose))
    lines.extend(_nuget_population_lines(evidence, verbose=verbose))
    lock_state = 'accepted' if evidence.format == 'packages_lock_v1' else 'unavailable'
    lines.append(f"NuGet packages.lock.json recognition: {lock_state}.")
    if source.dependencies_discovered is None:
        lines.append("NuGet population unavailable; discovered, measured, coverage and numeric aggregates are null.")
    elif not source.measurement_available:
        lines.append(f"NuGet measurement unavailable; known explicit population: {summary.dependencies_discovered}; "
                     "measured, coverage and numeric aggregates are null.")
    elif summary.dependencies_discovered == 0:
        lines.append("NuGet validated empty population: 0 / 0 measured; null coverage; total 0.00 libyears.")
    elif summary.dependencies_measured == 0:
        lines.append(f"NuGet accepted population is wholly unmeasurable: 0 / {summary.dependencies_discovered} "
                     "measured; 0.0% coverage.")
    else:
        lines.append(f"NuGet accepted population: {summary.dependencies_measured} / "
                     f"{summary.dependencies_discovered} measured; {_coverage(summary.coverage)} coverage.")
    return lines


def _nuget_detail_lines(evidence: NuGetEvidence | None, *, verbose=True) -> list[str]:
    if evidence is None:
        return []
    project = evidence.project
    lines = []
    if evidence.source_id is not None:
        lines.append(f"    NuGet source: {json.dumps(evidence.source_id, ensure_ascii=True)}.")
        project = json.dumps(project, ensure_ascii=True)
    if not verbose:
        return lines
    request_label = ('snapshot minimum' if evidence.population_basis in (
        'resolved_snapshot', 'qualified_repository_snapshot') else 'requested')
    lines.append(f"    NuGet project: {project}; framework: {evidence.framework}; {request_label}: {evidence.requested}.")
    if evidence.population_basis is not None:
        lines.append(f"    Population basis: {evidence.population_basis}.")
    if evidence.lock_requested is not None:
        lines.append(f"    Lock requested: {evidence.lock_requested}")
    if evidence.selected_version is not None:
        lines.append(f"    Selected version: {evidence.selected_version}; selection source: {evidence.selection_source}.")
    if evidence.normalized_version is not None:
        lines.append(f"    Normalized selected version: {evidence.normalized_version}")
    lines.append(f"    Origin state: {evidence.origin_state}; content hash state: {evidence.content_hash_state}.")
    if evidence.measurement_basis is not None:
        assurance = _nuget_assurance(evidence)
        lines.append(f"    Measurement basis: {evidence.measurement_basis}; namespace basis: {evidence.namespace_basis}.")
        lines.append(f"    Stronger assurance: producer event {assurance['producer_event']}; "
                     f"local content {assurance['local_content']}; public content {assurance['public_content']}.")
        lines.append("    Limitations: " + ', '.join(assurance['limitations']) + '.')
    for label, publication in (("Used", evidence.used_publication), ("Latest", evidence.latest_publication)):
        if publication is not None:
            listed = 'true' if publication.listed else 'false'
            lines.append(f"    {label} publication: version {publication.version}; created {_timestamp(publication.created)}; listed {listed}.")
    return lines


def _nuget_anomaly_line(anomaly: bool) -> str:
    if anomaly:
        return "    timestamp_anomaly: true; negative date delta clamped to zero."
    return "    timestamp_anomaly: false"


def _nuget_reason_text(reason: str) -> str:
    explanation = {
        'nuget_discovery_incomplete': 'bounded project discovery incomplete; repository population unknown',
        'nuget_discovery_unavailable': 'safe bounded project discovery unavailable; repository population unknown',
        'nuget_witness_project_missing': 'mapped project absent from bounded discovery; population unknown',
        'nuget_project_missing': 'selected project is missing; declaration population unavailable',
        'invalid_nuget_project': 'selected project is unreadable, unsafe or malformed; declaration population unavailable',
        'unsupported_nuget_project': 'unsupported project, context or population influence; declaration population unavailable',
        'duplicate_nuget_declaration': 'duplicate package declaration identity; declaration population unavailable',
        'lockfile_missing': 'packages.lock.json is missing; measurement unavailable',
        'invalid_lockfile': 'packages.lock.json is unreadable, unsafe or malformed; measurement unavailable',
        'unsupported_lockfile_format': 'unsupported packages.lock.json format or context; measurement unavailable',
        'nuget_context_mismatch': 'supplied project, lock and witness do not establish one coherent snapshot',
        'nuget_provenance_missing': 'explicit supplier witness unavailable; measurement authority not established',
        'invalid_nuget_provenance': 'supplied witness is unreadable, unsafe, malformed or unsupported',
        'lock_dependency_missing': 'matching Direct entry missing from packages.lock.json; no transitive fallback',
        'declaration_lock_requirement_mismatch': 'declaration and lock numeric minimum requests disagree; selection not established',
        'lock_version_missing': 'selected version missing from packages.lock.json',
        'unsupported_lock_evidence': 'unsupported selected version syntax in packages.lock.json',
        'unsupported_dependency_source': 'accepted public namespace authority unavailable; no public namesake is substituted',
        'nuget_comparator_ambiguous': 'repository source policy leaves comparator ambiguity; no public lookup',
        'nuget_comparator_private': 'repository policy assigns or restricts to a nonpublic comparator; no public lookup',
        'nuget_comparator_unknown': 'repository comparator policy cannot be safely determined; no public lookup',
        'content_hash_unavailable': 'usable SHA512 content evidence unavailable',
        'content_hash_mismatch': 'content hashes disagree; content correspondence not established',
        'package_not_found': 'authorized public nuget.org package metadata absent',
        'version_not_found': 'authorized selected public version metadata absent',
        'release_date_missing': 'usable catalog created timestamp unavailable for used or actual latest version',
        'no_stable_release': 'complete public enumeration has no listed stable version',
        'invalid_registry_response': 'public metadata is malformed, conflicting, unsupported or incomplete',
        'registry_error': 'public metadata transport, service, rate limit or work budget unavailable',
    }.get(reason, 'measurement unavailable')
    return f"{reason}: {explanation}"


def _scoped_ruby_disclosure(source, summary) -> list[str]:
    groups = ", ".join(source.evidence.requested_groups)
    lines = [
        f"RubyGems selected declared groups: {groups}.",
        "Supplied declaration source: Gemfile; supplied version snapshot: Gemfile.lock.",
        "Declaration membership does not establish installed/deployed/runtime scope or historical coherence.",
        "Publication dates are earliest admissible supported observable evidence, not complete historical knowledge.",
        "Missing public records prove neither yanking nor never-existence; record disappearance may change future measurements.",
    ]
    if source.dependencies_discovered is None:
        lines.append("Requested declaration scope unavailable; lock recognition unavailable.")
    else:
        lock_state = "accepted" if source.evidence.format == "gemfile_lock" else "unavailable"
        lines.append(f"Requested declaration scope recognized; Gemfile.lock recognition: {lock_state}.")
        if not source.measurement_available:
            lines.append(f"Ruby measurement unavailable; known selected population: {summary.dependencies_discovered}.")
        elif summary.dependencies_discovered == 0:
            lines.append("Selected declared scope is empty (0 / 0 measured; null coverage).")
        elif summary.dependencies_measured == 0:
            lines.append(f"Selected declared scope is wholly unmeasurable (0 / {summary.dependencies_discovered} measured; 0.0% coverage).")
    return lines


def _gemfile_detail_lines(evidence: GemfileEvidence | None) -> list[str]:
    if evidence is None:
        return []
    # JSON string framing makes literal requirement whitespace visible to readers.
    requirements = json.dumps(list(evidence.declaration_requirements))
    lines = [f"    Gemfile declared groups: {', '.join(evidence.declared_groups)}; declaration requirements: {requirements}"]
    if evidence.include_lock_requirement:
        lines.append(f"    Gemfile.lock requirement: {json.dumps(evidence.lock_requirement)}")
    else:
        lines.append("    Gemfile.lock requirement: unavailable")
    return lines


def _scoped_dependency_reason(reason: str) -> str:
    if reason == "unsupported_dependency_source":
        return ("public source authority not established; nonpublic Gemfile sources are unsupported; "
                "lock authority is checked independently; no public namesake is substituted")
    return _ruby_reason_text(reason)


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


def _dependency_reason_text(reason: str, yarn_evidence: bool, ecosystem: str = "") -> str:
    if ecosystem == "nuget":
        return _nuget_reason_text(reason)
    if ecosystem == "rubygems":
        return _ruby_reason_text(reason)
    if yarn_evidence and reason == "lock_version_missing":
        return "exact version unavailable in yarn.lock"
    return _reason_text(reason)


def _ruby_reason_text(reason: str) -> str:
    return {
        "package_not_found": "public RubyGems metadata reports package absence",
        "version_not_found": "used version absent from supported observable RubyGems records",
        "lock_version_missing": "exact selected spec unavailable in Gemfile.lock",
        "unsupported_dependency_name": "unsupported RubyGems dependency name",
        "unsupported_dependency_source": "supported public RubyGems authority not established; no public namesake is substituted",
        "unsupported_lock_evidence": "unsupported selected version or artifact identity in Gemfile.lock",
        "ambiguous_lock_evidence": "differing versions or duplicate selected artifacts in Gemfile.lock",
        "gemfile_missing": "Gemfile unavailable: supplied declaration file is missing",
        "invalid_gemfile": "Gemfile unavailable: unreadable, nonregular or malformed declaration evidence",
        "unsafe_gemfile": "Gemfile unavailable: declaration target is outside the supplied root",
        "unsupported_gemfile_syntax": "Gemfile scope unavailable: unsupported static declaration syntax",
        "duplicate_gemfile_declaration": "Gemfile scope unavailable: duplicate gem declarations",
        "unknown_ruby_group": "requested Ruby group is not established; entire requested scope unavailable",
        "lockfile_missing": "Gemfile.lock unavailable: exact version evidence is missing",
        "lock_dependency_missing": "selected declaration is absent from direct Gemfile.lock dependencies",
        "declaration_lock_requirement_mismatch": "textual requirement evidence differs; equivalence not inferred",
        "invalid_lockfile": "unreadable or malformed Gemfile.lock",
        "unsupported_lockfile_format": "unsupported or unclassifiable Gemfile.lock format",
    }.get(reason, _reason_text(reason))


def _reason_text(reason: str) -> str:
    return _REASON_TEXT.get(reason, "measurement unavailable")


def _source_text(source: str) -> str:
    return {
        "requirements_exact": "requirements.txt",
        "resolved_snapshot": "snapshot",
        "yarn_lock": "yarn.lock",
        "gemfile_lock": "Gemfile.lock",
        "packages_lock": "packages.lock.json",
    }.get(source, source)


__all__ = ["format_human", "format_json", "report_to_dict"]
