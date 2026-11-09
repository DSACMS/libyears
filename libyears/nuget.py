"""Internal selected NuGet source; no scan activation or registry access."""

from dataclasses import dataclass, replace
from pathlib import Path
import re

from .model import (DependencyCandidate, NuGetEvidence, SourceError,
                    SourceEvidence, SourceResult, UnmeasurableDependency)
from .nuget_input import NuGetInputFailure, ScopedNuGetReader, decode_json
from .nuget_population import repository_snapshot_population, snapshot_population
from .nuget_lock import parse_lock
from .nuget_project import parse_project
from .nuget_provenance import (LocalAuthority, LocalAuthorityFailure,
                               authorize_measurement, parse_provenance,
                               parse_population_provenance)
from .nuget_version import MAX_VERSION_LENGTH, parse_selected_identity


@dataclass(frozen=True, slots=True)
class NuGetSourceEvidence(SourceEvidence):
    provenance_source: str | None = None
    framework: str | None = None
    trust_basis: str = 'supplied_producer_assertion'
    population_basis: str = 'unknown'
    population_limitations: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AuthorizedCandidate:
    """An adapter must consume the capability, never infer it from the candidate."""

    candidate: DependencyCandidate
    authority: LocalAuthority


@dataclass(frozen=True, slots=True)
class NuGetSource:
    result: SourceResult
    authorized_candidates: tuple[AuthorizedCandidate, ...] = ()


def _safe_lock_request(value: str) -> str | None:
    # A mismatch can contain arbitrary text. Retain only bounded numeric range
    # notation, including noncanonical spelling; never echo paths or free text.
    if (len(value) <= MAX_VERSION_LENGTH and value
            and re.fullmatch(r'[0-9.\[\](), *+\-]+', value)):
        return value
    return None


def _source_reason(stage: str, category: str) -> str:
    if category == 'context_mismatch':
        return 'nuget_context_mismatch'
    if stage == 'project':
        return {'missing': 'nuget_project_missing',
                'unsupported': 'unsupported_nuget_project',
                'limit': 'unsupported_nuget_project',
                'duplicate': 'duplicate_nuget_declaration'}.get(category, 'invalid_nuget_project')
    if stage == 'lock':
        return {'missing': 'lockfile_missing',
                'unsupported': 'unsupported_lockfile_format',
                'limit': 'unsupported_lockfile_format'}.get(category, 'invalid_lockfile')
    return {'missing': 'nuget_provenance_missing',
            'context_mismatch': 'nuget_context_mismatch',
            'unsupported': 'unsupported_nuget_project'}.get(category, 'invalid_nuget_provenance')


def read_nuget_source(root: Path, project_name: str,
                      provenance_name: str | None = None, *,
                      reader: ScopedNuGetReader | None = None,
                      repository_snapshot: bool = False,
                      unambiguous_snapshot: bool = True) -> NuGetSource:
    """Read bounded local inputs and stage safe population evidence before lookup.

    Filenames are immediate names validated by the caller. The scoped reader
    independently enforces containment. Whole
    source rejection returns no dependency rows or adapter capabilities.
    """
    evidence = NuGetSourceEvidence(
        declaration_source=project_name, snapshot_source='packages.lock.json',
        include_format=True, scope='explicit_direct_packagereference',
        publication_basis='nuget_org_first_receipt_created',
        provenance_source=provenance_name)
    count = None
    stage = 'project'
    source_name = project_name

    def rejected(reason: str) -> NuGetSource:
        result = SourceResult('nuget', (), (),
                              (SourceError('nuget', source_name, reason),),
                              replace(evidence, population_basis=('unknown' if count is None
                                      else evidence.population_basis)), count, False)
        return NuGetSource(result)

    try:
        with (reader or ScopedNuGetReader(root, project_name, provenance_name)) as reader:
            project_source = reader.read(project_name)
            fallback = False
            try:
                project = parse_project(project_source)
            except NuGetInputFailure as failure:
                if (failure.category != 'unsupported'
                        or (provenance_name is None and not repository_snapshot)):
                    raise
                fallback = True
            if fallback:
                context = None
                lock_source = None
                qualified = None
                if repository_snapshot:
                    stage = 'lock'
                    source_name = 'packages.lock.json'
                    lock_source = reader.read(source_name)
                    lock = parse_lock(lock_source)
                    stage = 'project'
                    source_name = project_name
                    # Check known contradictions even if the directory has more
                    # than one project and automatic attribution is unavailable.
                    qualified = repository_snapshot_population(project_source, lock)
                if qualified is not None and unambiguous_snapshot:
                    project = qualified
                    count = len(project.declarations)
                    evidence = replace(evidence, framework=project.framework,
                        format='packages_lock_v1', population_basis='qualified_repository_snapshot',
                        trust_basis='repository_snapshot_policy',
                        population_limitations=(
                            'policy_selected_current_repository_snapshot',
                            'historical_producing_association_not_established',
                            'current_evaluated_declaration_completeness_not_established',
                            'acquisition_content_deployment_reproducibility_not_established'))
                    if provenance_name is not None:
                        stage = 'witness'
                        source_name = provenance_name
                        witness_source = reader.read(provenance_name)
                        context = parse_population_provenance(
                            witness_source, project_name=project_name,
                            project_source=project_source, lock_source=lock_source,
                            framework=lock.framework)
                        evidence = replace(evidence,
                            trust_basis='supplied_snapshot_population_assertion',
                            population_limitations=evidence.population_limitations + (
                                'accepted_retained_external_direct_snapshot',))
                else:
                    if provenance_name is None:
                        source_name = project_name
                        return rejected('unsupported_nuget_project')
                    stage = 'witness'
                    source_name = provenance_name
                    witness_source = reader.read(provenance_name)
                    value = decode_json(witness_source.data.decode('utf-8', errors='strict'))
                    if (not isinstance(value, dict) or type(value.get('version')) is not int
                            or value['version'] != 3):
                        # Older contracts cannot be reinterpreted as snapshot population.
                        source_name = project_name
                        return rejected('unsupported_nuget_project')
                    if lock_source is None:
                        stage = 'lock'
                        source_name = 'packages.lock.json'
                        lock_source = reader.read(source_name)
                        lock = parse_lock(lock_source)
                    stage = 'witness'
                    source_name = provenance_name
                    context = parse_population_provenance(
                        witness_source, project_name=project_name,
                        project_source=project_source, lock_source=lock_source,
                        framework=lock.framework)
                    stage = 'project'
                    source_name = project_name
                    project = snapshot_population(project_source, lock)
                    count = len(project.declarations)
                    evidence = replace(evidence, framework=project.framework,
                        format='packages_lock_v1', population_basis='resolved_snapshot',
                        trust_basis='supplied_snapshot_population_assertion',
                        population_limitations=(
                            'accepted_retained_external_direct_snapshot',
                            'current_evaluated_declaration_completeness_not_established',
                            'acquisition_content_deployment_reproducibility_not_established'))
            else:
                count = len(project.declarations)
                evidence = replace(evidence, framework=project.framework,
                                   population_basis='declaration_derived')

                stage = 'lock'
                source_name = 'packages.lock.json'
                lock_source = reader.read(source_name)
                lock = parse_lock(lock_source)
                evidence = replace(evidence, format='packages_lock_v1')
                declared_keys = {item.package_key for item in project.declarations}
                if (lock.framework != project.framework
                        or any(item.kind == 'Direct' and item.package_key not in declared_keys
                               for item in lock.entries)):
                    return rejected('nuget_context_mismatch')

                stage = 'witness'
                # An absent option identifies the project requiring testimony; no
                # conventional witness name is invented or inspected.
                source_name = provenance_name or project_name
                if provenance_name is None:
                    return rejected('nuget_provenance_missing')
                witness_source = reader.read(provenance_name)
                context = parse_provenance(
                    witness_source, project_name=project_name,
                    project_source=project_source, lock_source=lock_source, project=project)
                if context.contract_version == 2:
                    evidence = replace(evidence, trust_basis='supplied_snapshot_assertion')
    except NuGetInputFailure as failure:
        if stage == 'witness' and failure.witness_version == 2:
            evidence = replace(evidence, trust_basis='supplied_snapshot_assertion')
        if stage == 'witness' and failure.category == 'unsupported':
            count = None
        return rejected(_source_reason(stage, failure.category))

    direct = {item.package_key: item for item in lock.entries if item.kind == 'Direct'}
    authorized = []
    failures = []
    for declaration in sorted(project.declarations, key=lambda item: item.package_key):
        row_evidence = NuGetEvidence(project_name, project.framework,
                                     declaration.declared_version,
                                     population_basis=evidence.population_basis)
        entry = direct.get(declaration.package_key)
        reason = None
        if entry is None:
            reason = 'lock_dependency_missing'
        else:
            row_evidence = replace(row_evidence, lock_requested=_safe_lock_request(entry.requested))
            expected = '[' + declaration.requested_minimum.normalized_version + ', )'
            if entry.requested != expected:
                reason = 'declaration_lock_requirement_mismatch'
            elif entry.resolved is None:
                reason = 'lock_version_missing'
            else:
                selected = parse_selected_identity(entry.resolved)
                if selected is None:
                    reason = 'unsupported_lock_evidence'
                    if (len(entry.resolved) <= MAX_VERSION_LENGTH
                            and re.fullmatch(r'[0-9]+(?:\.[0-9]+)*', entry.resolved)):
                        row_evidence = replace(row_evidence, selected_version=entry.resolved,
                                               selection_source='packages.lock.json')
                else:
                    row_evidence = replace(
                        row_evidence, selected_version=selected.original_version,
                        normalized_version=selected.normalized_version,
                        selection_source='packages.lock.json')
                    authority = (LocalAuthorityFailure('unsupported_dependency_source')
                                 if context is None else authorize_measurement(
                                     context, declaration.package_key, selected, entry.content_hash))
                    if isinstance(authority, LocalAuthorityFailure):
                        reason = authority.reason
                        row_evidence = replace(row_evidence, origin_state=authority.origin_state,
                                               content_hash_state=authority.content_hash_state)
                    else:
                        row_evidence = replace(
                            row_evidence, measurement_basis='bound_snapshot_namespace',
                            namespace_basis=authority.namespace_basis,
                            local_content_state=authority.local_content_state,
                            origin_state=('asserted_public' if context.contract_version == 1
                                          else 'unavailable'),
                            content_hash_state=authority.local_content_state)
        request_label = ('snapshot minimum ' if evidence.population_basis in (
            'resolved_snapshot', 'qualified_repository_snapshot') else '')
        declared = declaration.package_name + ' (' + request_label + declaration.declared_version + ')'
        if reason is not None:
            failures.append(UnmeasurableDependency('nuget', declaration.package_name,
                                                   declared, reason, nuget_evidence=row_evidence))
        else:
            candidate = DependencyCandidate(
                'nuget', declaration.package_name, declaration.package_key, declared,
                selected.original_version, 'packages_lock', nuget_evidence=row_evidence)
            authorized.append(AuthorizedCandidate(candidate, authority))
    result = SourceResult('nuget', tuple(item.candidate for item in authorized),
                          tuple(failures), (), evidence, count, True)
    return NuGetSource(result, tuple(authorized))
