"""Pure, restriction-only reduction before SBOM metadata capabilities exist."""

from dataclasses import replace

from .maven_model import MavenReason
from .maven_policy import central_url
from .sbom_identity import qualifiers


def _restricted(record):
    return (bool(record.get('properties')) or bool(record.get('evidence'))
            or bool(record.get('pedigree'))
            or ('modified' in record and record['modified'] is not False))


def admit_members(document, members, known_vetoes=()):
    global_restriction = (bool(document.root.get('properties'))
                          or bool(document.root['metadata'].get('properties'))
                          or bool(document.root.get('formulation'))
                          or _restricted(document.subject))
    vetoes = {}
    for group, artifact, reason in known_vetoes:
        key = (group, artifact)
        if key not in vetoes or reason == MavenReason.COMPARATOR_REFUSED:
            vetoes[key] = reason
    result = []
    for member in members:
        reason = member.reason
        if reason is None:
            identity = member.identity
            veto = vetoes.get((identity.group_id, identity.artifact_id))
            if veto is not None:
                reason = ('sbom_comparator_refused' if veto == MavenReason.COMPARATOR_REFUSED
                          else 'sbom_policy_unknown')
            # A positive alias namespace refusal dominates weaker unknown evidence.
            for index, record in member.records:
                values, unused = qualifiers(record['purl'])
                if 'repository_url' in values and not central_url(values['repository_url']):
                    reason = 'sbom_comparator_refused'
            if reason is None and (global_restriction or any(_restricted(r) for i, r in member.records)):
                reason = 'sbom_policy_unknown'
        result.append(replace(member, reason=reason))
    return tuple(result)
