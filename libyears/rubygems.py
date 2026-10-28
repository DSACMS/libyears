"""Static Ruby lock evidence and public-source authorization; no HTTP."""

import re

from .gemfile_lock import LockDependency, ParsedGemfileLock
from .model import (
    DependencyCandidate, RubyGemsEvidence, SelectedRubyArtifact,
    UnmeasurableDependency,
)


PUBLIC_SOURCE = 'https://rubygems.org'


def _has_public_authority(lock: ParsedGemfileLock, direct: LockDependency) -> bool:
    if direct.source_pinned:
        return False
    for source in lock.sources:
        if not any(spec.name == direct.name for spec in source.specs):
            continue
        remotes = [value for key, value in source.metadata if key == 'remote']
        if source.kind != 'GEM' or remotes not in ([PUBLIC_SOURCE], [PUBLIC_SOURCE + '/']):
            return False
    return True


_NAME = re.compile(r'[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?\Z')
_VERSION = r'[0-9]+(?:\.[A-Za-z0-9]+)*'
_SELECTION = re.compile(r'(' + _VERSION + r')(?:-([A-Za-z0-9_.-]+))?\Z')
_REQUIREMENT_TERM = re.compile(r'(?:!=|>=|<=|~>|=|>|<)?\s*' + _VERSION + r'\Z')


def _supported_requirement(requirement: str | None) -> bool:
    if requirement is None:
        return True
    for term in requirement.split(','):
        if not _REQUIREMENT_TERM.fullmatch(term.strip()):
            return False
    return True


def _failure(direct, reason, artifacts=()):
    evidence = RubyGemsEvidence(artifacts) if artifacts else None
    return UnmeasurableDependency(
        'rubygems', direct.name, direct.declared, reason, evidence,
    )


def authorize_public_selection(
    lock: ParsedGemfileLock,
    direct: LockDependency,
) -> DependencyCandidate | UnmeasurableDependency:
    """Validate local evidence before the sole Ruby candidate construction.

    Every exact-name source association must authorize public identity, even
    when a public occurrence coexists with a private or pinned namesake.
    Requirements delimit evidence; they never select or validate a version.
    """
    if not _NAME.fullmatch(direct.name) or not re.search(r'[A-Za-z]', direct.name):
        return _failure(direct, 'unsupported_dependency_name')
    if not _supported_requirement(direct.requirement_text):
        return _failure(direct, 'unsupported_requirement')
    if not _has_public_authority(lock, direct):
        return _failure(direct, 'unsupported_dependency_source')

    occurrences = [
        spec for source in lock.sources for spec in source.specs
        if spec.name == direct.name
    ]
    if not occurrences:
        return _failure(direct, 'lock_version_missing')

    artifacts = []
    unsupported = False
    for spec in occurrences:
        match = _SELECTION.fullmatch(spec.raw_selection)
        if match is None:
            unsupported = True
            continue
        version, platform = match.groups()
        artifacts.append(SelectedRubyArtifact(version, platform or 'ruby', PUBLIC_SOURCE))
    artifacts = tuple(sorted(artifacts, key=lambda item: (item.version, item.platform)))
    versions = {artifact.version for artifact in artifacts}
    identities = {(artifact.version, artifact.platform) for artifact in artifacts}
    # Collect all supported evidence so row order cannot hide proven ambiguity.
    if len(versions) > 1 or len(identities) < len(artifacts):
        return _failure(direct, 'ambiguous_lock_evidence', artifacts)
    if unsupported:
        return _failure(direct, 'unsupported_lock_evidence', artifacts)
    return DependencyCandidate(
        'rubygems', direct.name, direct.name, direct.declared, artifacts[0].version,
        'gemfile_lock', RubyGemsEvidence(artifacts),
    )


def match_lock_dependencies(lock: ParsedGemfileLock):
    """Match only recorded direct names, preserving known scope on failures."""
    candidates = []
    failures = []
    for direct in lock.dependencies:
        result = authorize_public_selection(lock, direct)
        if isinstance(result, DependencyCandidate):
            candidates.append(result)
        else:
            failures.append(result)
    return tuple(candidates), tuple(failures)
