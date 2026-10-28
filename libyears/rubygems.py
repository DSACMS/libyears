"""Static Ruby lock evidence and public-source authorization; no HTTP."""

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


def authorize_public_selection(
    lock: ParsedGemfileLock,
    direct: LockDependency,
    used_version: str,
    selected_artifacts: tuple[SelectedRubyArtifact, ...],
) -> DependencyCandidate | UnmeasurableDependency:
    """Construct a candidate only after checking every exact-name association.

    The matcher supplies validated selected identity. Authority is checked here
    even if a public occurrence coexists with a private or pinned namesake.
    Remote values never leave this boundary as diagnostics or request inputs.
    """
    if not _has_public_authority(lock, direct):
        return UnmeasurableDependency(
            'rubygems', direct.name, direct.declared, 'unsupported_dependency_source',
        )
    if not any(spec.name == direct.name for source in lock.sources for spec in source.specs):
        return UnmeasurableDependency(
            'rubygems', direct.name, direct.declared, 'lock_version_missing',
        )
    return DependencyCandidate(
        'rubygems', direct.name, direct.name, direct.declared, used_version,
        'gemfile_lock', RubyGemsEvidence(selected_artifacts),
    )
