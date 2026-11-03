"""Whole schema-1 lock framing, without association, resolution or I/O."""

from dataclasses import dataclass
import re

from .nuget_input import (
    LocalInput, NuGetInputFailure, ValidationFindings, check_count, decode_json,
    MAX_FRAMEWORK_LENGTH, MAX_LOCK_BYTES, MAX_LOCK_ENTRIES,
)
from .nuget_version import MAX_COMPONENT_DIGITS, MAX_VERSION_LENGTH


_PACKAGE_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,99}')
_FRAMEWORK = re.compile(r'[A-Za-z0-9][A-Za-z0-9.-]*')
_DIGITS = re.compile(r'[0-9]+')
_FIELDS = {
    'Direct': frozenset({'type', 'requested', 'resolved', 'contentHash', 'dependencies'}),
    'Transitive': frozenset({'type', 'resolved', 'contentHash', 'dependencies'}),
    'Project': frozenset({'type', 'dependencies'}),
}


@dataclass(frozen=True)
class LockEntry:
    package_name: str
    package_key: str
    kind: str
    requested: str | None
    resolved: str | None
    content_hash: str | None
    dependencies: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class LockSnapshot:
    framework: str
    entries: tuple[LockEntry, ...]


def _identity_map(value: object, findings: ValidationFindings) -> dict:
    """Validate IDs, including aliases, even in unselected closure contexts."""
    if not isinstance(value, dict):
        findings.malformed = True
        return {}
    seen = set()
    for name in value:
        if _PACKAGE_ID.fullmatch(name) is None:
            findings.malformed = True
        key = name.lower()
        if key in seen:
            findings.malformed = True
        seen.add(key)
    return value


def _entry(name: str, value: object, findings: ValidationFindings) -> LockEntry | None:
    if not isinstance(value, dict):
        findings.malformed = True
        return None
    kind = value.get('type')
    if not isinstance(kind, str):
        findings.malformed = True
    elif kind not in _FIELDS:
        findings.unsupported = True
    else:
        findings.unsupported |= bool(set(value) - _FIELDS[kind])

    # Known fields retain their type requirements even in an unsupported kind.
    for field in ('requested', 'resolved', 'contentHash'):
        if field in value and not isinstance(value[field], str):
            findings.malformed = True
    for field in ('requested', 'resolved'):
        if isinstance(value.get(field), str):
            _version_bounds(value[field], findings)
    if kind == 'Direct' and 'requested' not in value:
        findings.malformed = True
    if kind == 'Transitive' and not {'resolved', 'contentHash'} <= set(value):
        findings.malformed = True

    dependencies = ()
    if 'dependencies' in value:
        mapping = _identity_map(value['dependencies'], findings)
        for request in mapping.values():
            if not isinstance(request, str):
                findings.malformed = True
            else:
                _version_bounds(request, findings)
        dependencies = tuple(sorted(mapping.items(), key=lambda pair: pair[0].lower()))

    return LockEntry(name, name.lower(), kind, value.get('requested'),
                     value.get('resolved'), value.get('contentHash'), dependencies)


def _version_bounds(value: str, findings: ValidationFindings) -> None:
    """Bound all lock version text without interpreting requests or selections.

    Closure requests can contain range punctuation, so inspect decimal runs
    without parsing ranges or converting numbers. Record overflow and finish
    structural validation so malformed fields still take precedence.
    """
    if len(value) > MAX_VERSION_LENGTH:
        findings.unsupported = True
    if any(len(match.group()) > MAX_COMPONENT_DIGITS
           for match in _DIGITS.finditer(value)):
        findings.unsupported = True


def parse_lock(source: LocalInput) -> LockSnapshot:
    """Accept the entire lock before returning any entry evidence.

    A different sole literal framework is retained for orchestration's context
    binding check. Extra/RID contexts reject this source. Complete validation of
    every framework still precedes that unsupported disposition, so malformed
    structure always wins independent of object ordering. Version resource bounds
    apply here to every entry and closure request; syntax/hash interpretation
    and declaration association belong to later stages.
    """
    check_count(len(source.data), MAX_LOCK_BYTES)
    try:
        text = source.data.decode('utf-8', errors='strict')
    except UnicodeError:
        raise NuGetInputFailure('malformed') from None
    value = decode_json(text)
    findings = ValidationFindings()
    if not isinstance(value, dict):
        raise NuGetInputFailure('malformed')
    findings.unsupported = bool(set(value) - {'version', 'dependencies'})
    if type(value.get('version')) is not int:
        findings.malformed = True
    elif value['version'] != 1:
        findings.unsupported = True
    contexts = value.get('dependencies')
    if not isinstance(contexts, dict):
        findings.malformed = True
        contexts = {}
    if len(contexts) != 1:
        findings.unsupported = True

    entries = []
    entry_count = 0
    for framework, packages in contexts.items():
        check_count(len(framework), MAX_FRAMEWORK_LENGTH)
        if _FRAMEWORK.fullmatch(framework) is None:
            findings.unsupported = True
        mapping = _identity_map(packages, findings)
        entry_count += len(mapping)
        check_count(entry_count, MAX_LOCK_ENTRIES)
        for name, package in mapping.items():
            entry = _entry(name, package, findings)
            if entry is not None:
                entries.append(entry)
    findings.finish()
    return LockSnapshot(next(iter(contexts)),
                        tuple(sorted(entries, key=lambda entry: entry.package_key)))
