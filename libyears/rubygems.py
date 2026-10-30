"""Static Ruby lock evidence and public-source authorization; no HTTP."""

import os
import re
import stat
from dataclasses import dataclass, replace
from pathlib import Path

from .gemfile import GemfileParseFailure, parse_gemfile, supported_name, supported_requirement
from .gemfile_lock import LockDependency, LockParseFailure, ParsedGemfileLock, parse_lockfile
from .model import (
    DependencyCandidate, GemfileEvidence, RubyGemsEvidence, SelectedRubyArtifact,
    SourceError, SourceEvidence, SourceResult, UnmeasurableDependency,
)


PUBLIC_SOURCE = 'https://rubygems.org'

_MAX_GEMFILE_BYTES = 1024 * 1024
_MAX_SCOPED_LOCK_BYTES = 16 * 1024 * 1024
# Keep the capability identity stable when tests interpose at the final open.
_DIRECTORY_OPEN = os.open


@dataclass(frozen=True)
class _ScopedReadFailure:
    reason: str
    safe_category: str


class _ScopedRubyReader:
    """Read the two scoped inputs within one resolved containment boundary."""

    def __init__(self, root: Path):
        try:
            self.root = root.resolve(strict=True)
        except (OSError, RuntimeError):
            self.root = None

    def read(self, name: str) -> str | _ScopedReadFailure:
        if name not in ('Gemfile', 'Gemfile.lock'):
            raise ValueError('Only scoped Ruby root input names are supported.')
        invalid = 'invalid_gemfile' if name == 'Gemfile' else 'invalid_lockfile'
        missing = 'gemfile_missing' if name == 'Gemfile' else 'lockfile_missing'
        if self.root is None:
            return _ScopedReadFailure(invalid, 'Cannot establish scoped root.')
        required_flags = ('O_DIRECTORY', 'O_NOFOLLOW', 'O_NONBLOCK')
        if (any(not getattr(os, flag, 0) for flag in required_flags)
                or _DIRECTORY_OPEN not in getattr(os, 'supports_dir_fd', ())):
            return _ScopedReadFailure(invalid, 'Safe scoped access is unavailable.')

        path = self.root / name
        try:
            path.lstat()
        except FileNotFoundError:
            return _ScopedReadFailure(missing, 'Scoped input is missing.')
        except OSError:
            return _ScopedReadFailure(invalid, 'Cannot inspect scoped input.')

        try:
            resolved = path.resolve(strict=True)
            try:
                relative = resolved.relative_to(self.root)
            except ValueError:
                unsafe = 'unsafe_gemfile' if name == 'Gemfile' else invalid
                return _ScopedReadFailure(unsafe, 'Scoped target is outside root.')
            if not stat.S_ISREG(resolved.stat().st_mode):
                return _ScopedReadFailure(invalid, 'Scoped input is not regular.')
        except (OSError, RuntimeError):
            return _ScopedReadFailure(invalid, 'Cannot validate scoped target.')

        limit = _MAX_GEMFILE_BYTES if name == 'Gemfile' else _MAX_SCOPED_LOCK_BYTES
        descriptors = []
        try:
            directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
            directory = os.open(self.root, directory_flags)
            descriptors.append(directory)
            for component in relative.parts[:-1]:
                directory = os.open(component, directory_flags, dir_fd=directory)
                descriptors.append(directory)
            descriptor = os.open(
                relative.parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                dir_fd=directory,
            )
            descriptors.append(descriptor)
            # Replacement FIFOs must be rejected before even the first read.
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                return _ScopedReadFailure(invalid, 'Scoped input is not regular.')
            chunks = []
            remaining = limit + 1
            while remaining:
                chunk = os.read(descriptor, min(remaining, 64 * 1024))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            content = b''.join(chunks)
        except (OSError, NotImplementedError):
            return _ScopedReadFailure(invalid, 'Cannot safely read scoped input.')
        finally:
            for descriptor in reversed(descriptors):
                os.close(descriptor)

        excess = 'unsupported_gemfile_syntax' if name == 'Gemfile' else invalid
        if len(content) > limit:
            return _ScopedReadFailure(excess, 'Scoped input byte limit exceeded.')
        try:
            text = content.decode('utf-8', errors='strict')
        except UnicodeError:
            return _ScopedReadFailure(invalid, 'Scoped input is not UTF-8.')
        # Only LF/CRLF are physical line endings; leave other framing to parsers.
        text = text.replace('\r\n', '\n')
        # The Gemfile parser enforces its line cap in physical-line order, so
        # a later oversized line cannot hide an earlier recognition defect.
        return text


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


_VERSION = r'[0-9]+(?:\.[A-Za-z0-9]+)*'
_SELECTION = re.compile(r'(' + _VERSION + r')(?:-([A-Za-z0-9_.-]+))?\Z')


def _failure(direct, reason, artifacts=()):
    evidence = RubyGemsEvidence(artifacts) if artifacts else None
    return UnmeasurableDependency(
        'rubygems', direct.name, direct.declared, reason, evidence,
    )


def _public_authorization_failure(
    lock: ParsedGemfileLock,
    direct: LockDependency,
) -> UnmeasurableDependency | None:
    """Preserve ordinary name, requirement, then source failure precedence."""
    if not supported_name(direct.name):
        return _failure(direct, 'unsupported_dependency_name')
    if not supported_requirement(direct.requirement_text):
        return _failure(direct, 'unsupported_requirement')
    if not _has_public_authority(lock, direct):
        return _failure(direct, 'unsupported_dependency_source')
    return None


def authorize_public_selection(
    lock: ParsedGemfileLock,
    direct: LockDependency,
) -> DependencyCandidate | UnmeasurableDependency:
    """Validate all exact-name source associations before public selection."""
    failure = _public_authorization_failure(lock, direct)
    if failure is not None:
        return failure
    return _authorized_lock_selection(lock, direct)


def _authorized_lock_selection(lock, direct):
    """Select artifacts only after the caller has established public authority."""
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


def schedule_ruby_candidates(
    candidates: tuple[DependencyCandidate, ...],
) -> tuple[DependencyCandidate, ...]:
    """Order authorized candidates before a scan-local adapter starts requests."""
    return tuple(sorted(candidates, key=lambda candidate: (candidate.name, candidate.used_version)))


def _source_evidence(accepted: bool) -> SourceEvidence:
    return SourceEvidence(
        'Gemfile.lock', 'Gemfile.lock', 'gemfile_lock' if accepted else None, True,
        'all_direct_locked', 'earliest_admissible_supported_observable',
    )


def _rejected_source(reason: str, diagnostic: str) -> SourceResult:
    return SourceResult(
        'rubygems', (), (), (SourceError('rubygems', 'Gemfile.lock', reason),),
        _source_evidence(False), None, False,
        diagnostics=(('Gemfile.lock', diagnostic),),
    )


def _local_diagnostic(reason: str) -> str:
    messages = {
        'unsupported_dependency_name': 'Unsupported isolated gem name.',
        'unsupported_requirement': 'Unsupported direct requirement framing.',
        'unsupported_dependency_source':
            'Public source authority is not established; no public namesake substitution.',
        'lock_version_missing': 'No ordinary selected lock spec.',
        'ambiguous_lock_evidence': 'Differing versions or duplicate selected artifacts.',
        'unsupported_lock_evidence': 'Unsupported selected version or artifact identity.',
        'lock_dependency_missing': 'Selected declaration has no direct lock identity.',
        'declaration_lock_requirement_mismatch':
            'Textual requirement evidence differs; equivalence not inferred.',
    }
    return messages[reason]


def ruby_source_result(root: Path | None) -> SourceResult:
    """Read only an exactly named root lock, without inspecting Gemfile."""
    absent = SourceResult(
        'rubygems', (), (), (), _source_evidence(False), 0, True, source_present=False,
    )
    if root is None or not root.is_dir():
        return absent
    lock_path = root / 'Gemfile.lock'
    try:
        lock_path.lstat()
    except FileNotFoundError:
        return absent
    except OSError:
        return _rejected_source('invalid_lockfile', 'Cannot inspect root lock artifact.')

    try:
        if not stat.S_ISREG(lock_path.stat().st_mode):
            return _rejected_source('invalid_lockfile', 'Root lock artifact is not regular.')
        text = lock_path.read_text(encoding='utf-8')
    except (OSError, UnicodeError):
        return _rejected_source('invalid_lockfile', 'Cannot read root lock as UTF-8 text.')

    lock = parse_lockfile(text)
    if isinstance(lock, LockParseFailure):
        context = lock.safe_category
        if lock.section is not None:
            context += '; section ' + lock.section
        if lock.line is not None:
            context += '; line ' + str(lock.line)
        return _rejected_source(lock.reason, context)
    candidates, failures = match_lock_dependencies(lock)
    return SourceResult(
        'rubygems', candidates, failures, (), _source_evidence(True),
        len(lock.dependencies), True,
        diagnostics=tuple((item.name, _local_diagnostic(item.reason)) for item in failures),
    )


def _scoped_source_evidence(requested_groups, accepted=False):
    return SourceEvidence(
        'Gemfile', 'Gemfile.lock', 'gemfile_lock' if accepted else None, True,
        'selected_declared_groups', 'earliest_admissible_supported_observable',
        requested_groups,
    )


def _scoped_source_failure(evidence, source, failure, count=None):
    diagnostic = failure.safe_category
    line = getattr(failure, 'line', None)
    if line is not None:
        diagnostic += '; line ' + str(line)
    return SourceResult(
        'rubygems', (), (), (SourceError('rubygems', source, failure.reason),),
        evidence, count, False, diagnostics=((source, diagnostic),),
    )


def _declaration_failure(declaration, reason):
    requirement = ', '.join(declaration.requirements)
    declared = declaration.name
    if declaration.requirements:
        declared += ' (' + requirement + ')'
    return UnmeasurableDependency(
        'rubygems', declaration.name, declared, reason,
        gemfile_evidence=GemfileEvidence(
            declaration.declared_groups, declaration.requirements,
        ),
    )


def _associate_scoped_declarations(gemfile, selected, lock):
    """Associate only direct identities, keeping membership separate from versions."""
    directs = {direct.name: direct for direct in lock.dependencies}
    candidates = []
    failures = []
    for declaration in selected:
        direct = directs.get(declaration.name)
        row = _declaration_failure(declaration, 'lock_dependency_missing')
        evidence = row.gemfile_evidence
        if direct is not None and supported_requirement(direct.requirement_text):
            evidence = replace(
                evidence, lock_requirement=direct.requirement_text, include_lock_requirement=True,
            )
        if not gemfile.public_source_authorized:
            result = replace(row, reason='unsupported_dependency_source')
        elif direct is None:
            result = row
        else:
            result = _public_authorization_failure(lock, direct)
            if result is None:
                requirement = ', '.join(declaration.requirements) if declaration.requirements else None
                if requirement != direct.requirement_text:
                    result = replace(row, reason='declaration_lock_requirement_mismatch')
                else:
                    result = _authorized_lock_selection(lock, direct)
        # Even inherited failures must use safe Gemfile framing, never raw lock text.
        result = replace(result, declared=row.declared, gemfile_evidence=evidence)
        if isinstance(result, DependencyCandidate):
            candidates.append(result)
        else:
            failures.append(result)
    return tuple(candidates), tuple(failures)


def scoped_ruby_source_result(root: Path, requested_groups: tuple[str, ...]) -> SourceResult:
    """Establish complete declared scope before inspecting the bounded lock."""
    requested = tuple(sorted(set(requested_groups)))
    evidence = _scoped_source_evidence(requested)
    reader = _ScopedRubyReader(root)
    text = reader.read('Gemfile')
    if isinstance(text, _ScopedReadFailure):
        return _scoped_source_failure(evidence, 'Gemfile', text)
    gemfile = parse_gemfile(text)
    if isinstance(gemfile, GemfileParseFailure):
        return _scoped_source_failure(evidence, 'Gemfile', gemfile)
    if not set(requested).issubset(gemfile.established_groups):
        failure = _ScopedReadFailure('unknown_ruby_group', 'Requested group is not established.')
        return _scoped_source_failure(evidence, 'Gemfile', failure)
    selected = tuple(
        declaration for declaration in gemfile.declarations
        if set(requested).intersection(declaration.declared_groups)
    )
    count = len(selected)
    text = reader.read('Gemfile.lock')
    if isinstance(text, _ScopedReadFailure):
        if text.reason == 'lockfile_missing':
            failures = tuple(_declaration_failure(item, 'lockfile_missing') for item in selected)
            return SourceResult('rubygems', (), failures, (), evidence, count, True)
        return _scoped_source_failure(evidence, 'Gemfile.lock', text, count)
    lock = parse_lockfile(text)
    if isinstance(lock, LockParseFailure):
        return _scoped_source_failure(evidence, 'Gemfile.lock', lock, count)
    candidates, failures = _associate_scoped_declarations(gemfile, selected, lock)
    return SourceResult(
        'rubygems', candidates, failures, (), _scoped_source_evidence(requested, True), count, True,
        diagnostics=tuple((item.name, _local_diagnostic(item.reason)) for item in failures),
    )
