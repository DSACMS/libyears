"""Pure, bounded Gemfile.lock syntax; no resolution or source authorization."""

from dataclasses import dataclass
import re


@dataclass(frozen=True, slots=True)
class LockDependency:
    name: str
    declared: str
    requirement_text: str | None
    source_pinned: bool
    line: int


@dataclass(frozen=True, slots=True)
class LockSpec:
    name: str
    raw_selection: str
    source_index: int
    line: int


@dataclass(frozen=True, slots=True)
class LockSource:
    kind: str
    metadata: tuple[tuple[str, str], ...]
    specs: tuple[LockSpec, ...]
    line: int


@dataclass(frozen=True, slots=True)
class ParsedGemfileLock:
    sources: tuple[LockSource, ...]
    dependencies: tuple[LockDependency, ...]
    platforms: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LockParseFailure:
    reason: str
    section: str | None
    line: int | None
    safe_category: str


# Identity semantics belong to matching. Here a name must only be separable.
_ROW = re.compile(r'([^\s()!]+)(?: \(([^()]*)\))?(!?)\Z')
_PLATFORM = re.compile(r'[A-Za-z0-9_.-]+\Z')


def _row(text: str, *, spec: bool = False) -> tuple[str, str | None, bool]:
    match = _ROW.fullmatch(text)
    if match is None:
        raise ValueError('unsafe row framing')
    name, value, pin = match.groups()
    if spec and (not value or pin):
        raise ValueError('invalid selected row')
    return name, value, bool(pin)


_METADATA_KEYS = {
    'GEM': {'remote'},
    'PATH': {'remote'},
    'GIT': {'remote', 'revision', 'branch', 'ref', 'tag', 'submodules', 'glob'},
}


def _parse_source(section, rows, heading_line, source_index):
    metadata = []
    keys = set()
    specs = []
    in_specs = False
    for number, text in rows:
        if text == '  specs:':
            if in_specs:
                raise ValueError('repeated specs field')
            in_specs = True
        elif text.startswith('  ') and not text.startswith('   '):
            if in_specs:
                raise ValueError('metadata after specs')
            key, separator, value = text[2:].partition(': ')
            if not separator or not value.strip():
                raise ValueError('invalid metadata framing')
            if key not in _METADATA_KEYS[section]:
                raise ValueError('unsupported source field')
            if key in keys and not (section == 'GEM' and key == 'remote'):
                raise ValueError('duplicate source field')
            keys.add(key)
            metadata.append((key, value))
        elif text.startswith('    ') and not text.startswith('     ') and in_specs:
            name, selection, _ = _row(text[4:], spec=True)
            specs.append(LockSpec(name, selection, source_index, number))
        elif text.startswith('      ') and not text.startswith('       ') and in_specs:
            if not specs:
                raise ValueError('orphan nested row')
            _, _, pin = _row(text[6:])
            if pin:
                raise ValueError('nested source pin')
        else:
            raise ValueError('invalid source framing')
    if not in_specs:
        raise ValueError('missing specs field')
    return LockSource(section, tuple(metadata), tuple(specs), heading_line)


def _parse_section(section, rows, heading_line, source_index):
    """Validate a complete section before exposing any of its records."""
    if section in ('GEM', 'GIT', 'PATH'):
        return _parse_source(section, rows, heading_line, source_index)
    if section == 'DEPENDENCIES':
        dependencies = []
        names = set()
        for number, text in rows:
            if not text.startswith('  ') or text.startswith('   '):
                raise ValueError('invalid direct indentation')
            name, requirement, pin = _row(text[2:])
            if name in names:
                raise ValueError('duplicate direct identity')
            names.add(name)
            dependencies.append(LockDependency(name, text[2:], requirement, pin, number))
        return tuple(dependencies)
    if section == 'PLATFORMS':
        platforms = []
        for number, text in rows:
            if not text.startswith('  ') or not _PLATFORM.fullmatch(text[2:]):
                raise ValueError('invalid platform framing')
            if text[2:] in platforms:
                raise ValueError('duplicate platform')
            platforms.append(text[2:])
        if not platforms:
            raise ValueError('empty platforms')
        return tuple(platforms)
    if section in ('BUNDLED WITH', 'RUBY VERSION'):
        if len(rows) != 1:
            raise ValueError('invalid metadata row count')
        text = rows[0][1]
        if not text.startswith('   ') or text.startswith('    ') or not text[3:].strip():
            raise ValueError('invalid metadata indentation')
        if section == 'BUNDLED WITH' and any(c.isspace() for c in text[3:]):
            raise ValueError('invalid tool token')
        return None
    raise ValueError('unsupported section')


def parse_lockfile(text: str) -> ParsedGemfileLock | LockParseFailure:
    """Parse decoded text, returning no partial scope on rejection."""
    sections = []
    section = None
    rows = []
    heading_line = 0
    for number, line in enumerate(text.replace('\r\n', '\n').split('\n'), 1):
        if not line.strip():
            continue
        if any(ord(c) < 32 for c in line):
            return LockParseFailure('invalid_lockfile', section, number, 'control character')
        if not line.startswith(' '):
            if section is not None:
                sections.append((section, rows, heading_line))
            section, rows, heading_line = line, [], number
        else:
            rows.append((number, line))
    if section is not None:
        sections.append((section, rows, heading_line))
    sources = []
    dependencies = ()
    platforms = ()
    seen = set()
    for section, rows, number in sections:
        try:
            if section not in _METADATA_KEYS and section in seen:
                raise ValueError('repeated singleton section')
            seen.add(section)
            result = _parse_section(section, rows, number, len(sources))
            if section in _METADATA_KEYS:
                sources.append(result)
            elif section == 'DEPENDENCIES':
                dependencies = result
            elif section == 'PLATFORMS':
                platforms = result
        except ValueError as error:
            return LockParseFailure('invalid_lockfile', section, number, str(error))
    if not sources or not {'DEPENDENCIES', 'PLATFORMS'} <= seen:
        return LockParseFailure('invalid_lockfile', None, None, 'missing required section')
    return ParsedGemfileLock(tuple(sources), dependencies, platforms)
