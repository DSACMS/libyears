"""Pure, restriction-only reduction before SBOM metadata capabilities exist."""

from dataclasses import replace

from .maven_model import MavenReason
from .maven_policy import central_url
from .sbom_identity import qualifiers, safe_atom


def _restricted(record):
    return (bool(record.get('properties')) or bool(record.get('evidence'))
            or bool(record.get('pedigree'))
            or ('modified' in record and record['modified'] is not False))


def _repository_reason(record):
    purl = record.get('purl')
    if not isinstance(purl, str) or '?' not in purl:
        return None
    values, reason = qualifiers(purl)
    if reason is not None:
        # An uninterpretable explicit repository pointer is not absence of one.
        keys = [part.split('=', 1)[0] for part in purl.split('?', 1)[1].split('&')]
        return 'sbom_policy_unknown' if 'repository_url' in keys else None
    if 'repository_url' in values and not central_url(values['repository_url']):
        return 'sbom_comparator_refused'
    return None


def _namespace_ga(record):
    group, artifact, purl = (record.get(key) for key in ('group', 'name', 'purl'))
    if (not safe_atom(group, group=True) or not safe_atom(artifact)
            or not isinstance(purl, str) or not purl.startswith('pkg:maven/')):
        return None
    coordinates = purl[len('pkg:maven/'):].split('?', 1)[0].split('@', 1)[0]
    # Version failure cannot erase a coherent, explicit namespace assignment.
    return (group, artifact) if coordinates == group + '/' + artifact else None


def admit_members(document, members, known_vetoes=()):
    global_reason = _repository_reason(document.subject)
    if global_reason is None and (bool(document.root.get('properties'))
                                 or bool(document.root['metadata'].get('properties'))
                                 or bool(document.root.get('formulation'))
                                 or _restricted(document.subject)):
        global_reason = 'sbom_policy_unknown'
    vetoes = {}

    def retain_veto(key, reason):
        if key not in vetoes or reason == 'sbom_comparator_refused':
            vetoes[key] = reason

    for group, artifact, reason in known_vetoes:
        retain_veto((group, artifact), 'sbom_comparator_refused'
                    if reason == MavenReason.COMPARATOR_REFUSED else 'sbom_policy_unknown')
    for index, record in document.records:
        key = _namespace_ga(record)
        reason = _repository_reason(record)
        if key is not None and reason is not None:
            retain_veto(key, reason)
    result = []
    for member in members:
        reason = member.reason
        if reason is None:
            identity = member.identity
            veto = vetoes.get((identity.group_id, identity.artifact_id))
            if 'sbom_comparator_refused' in (global_reason, veto):
                reason = 'sbom_comparator_refused'
            elif global_reason is not None or veto is not None:
                reason = 'sbom_policy_unknown'
            elif any(_restricted(record) for index, record in member.records):
                reason = 'sbom_policy_unknown'
        result.append(replace(member, reason=reason))
    return tuple(result)
