"""Bounded, static Yarn Classic v1 lockfile parsing."""

from dataclasses import dataclass
from pathlib import Path
import re


UNSUPPORTED_LOCKFILE_FORMAT = "unsupported_lockfile_format"
INVALID_LOCKFILE = "invalid_lockfile"
_CANONICAL_HEADER = "# yarn lockfile v1"
_GENERATION_MARKER = re.compile(r"#\s*yarn\s+(?:lockfile|berry|pnp|v\d)", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class YarnFailure:
    """A stable failure reason with optional human-only context."""

    reason: str
    diagnostic: str


def recognize_v1(text: str) -> YarnFailure | None:
    """Require an uncontradicted canonical header before any lock entries.

    Recognition deliberately does not validate entries. Body syntax cannot
    establish the generation, even when it resembles a Classic lockfile.
    """
    found_header = False
    for line in text.splitlines():
        if not line.strip():
            continue
        if not line.startswith("#"):
            # Berry's metadata marker contradicts a claimed Classic header.
            if line.startswith("__metadata:"):
                return YarnFailure(
                    UNSUPPORTED_LOCKFILE_FORMAT, "unsupported Yarn metadata format"
                )
            break
        if line == _CANONICAL_HEADER:
            found_header = True
        elif _GENERATION_MARKER.match(line):
            return YarnFailure(
                UNSUPPORTED_LOCKFILE_FORMAT,
                "unsupported or contradictory Yarn generation header",
            )
    if not found_header:
        return YarnFailure(
            UNSUPPORTED_LOCKFILE_FORMAT, "could not identify Yarn Classic v1"
        )
    return None


@dataclass(frozen=True, slots=True)
class YarnEntry:
    """One entry; repeated selectors in other entries retain their identity."""

    selectors: tuple[str, ...]
    version: str | None


def _read_string(text: str, start: int) -> tuple[str, int]:
    """Read a bounded quoted string, returning its value and next position."""
    position = start + 1
    characters = []
    while position < len(text):
        character = text[position]
        if character == '"':
            return "".join(characters), position + 1
        if character == "\\":
            position += 1
            if position == len(text) or text[position] not in ('"', "\\"):
                raise ValueError("unsupported or dangling string escape")
            character = text[position]
        if ord(character) < 32:
            raise ValueError("control character in string")
        characters.append(character)
        position += 1
    raise ValueError("unterminated quoted string")


def _parse_selectors(line: str) -> tuple[str, ...]:
    """Consume a complete top-level key without normalizing selector text."""
    selectors = []
    position = 0
    while position < len(line):
        if line[position] == '"':
            selector, position = _read_string(line, position)
        else:
            start = position
            while position < len(line) and line[position] not in ',:':
                character = line[position]
                if character.isspace() or character in '"\\#{}[]':
                    raise ValueError("unsafe unquoted selector")
                position += 1
            selector = line[start:position]
        if not selector or selector in selectors:
            raise ValueError("empty or duplicate selector in entry key")
        selectors.append(selector)
        while position < len(line) and line[position] == ' ':
            position += 1
        if line[position:] == ':':
            return tuple(selectors)
        if position == len(line) or line[position] != ',':
            raise ValueError("expected selector separator or final colon")
        position += 1
        while position < len(line) and line[position] == ' ':
            position += 1
    raise ValueError("incomplete entry key")


def _parse_field(text: str) -> tuple[str, str | None]:
    """Read a scalar field or a subtree heading; no values become evidence here."""
    if text.startswith('"'):
        name, position = _read_string(text, 0)
    else:
        position = 0
        while position < len(text) and text[position] not in ' :':
            if text[position] in '"\\,#{}[]' or text[position].isspace():
                raise ValueError("unsafe field name")
            position += 1
        name = text[:position]
    if not name:
        raise ValueError("empty field name")
    remainder = text[position:]
    if remainder == ':':
        return name, None
    if not remainder.startswith(' '):
        raise ValueError("expected field value")
    value_text = remainder.lstrip(' ')
    if not value_text:
        raise ValueError("missing field value")
    if value_text.startswith('"'):
        value, end = _read_string(value_text, 0)
        if end != len(value_text):
            raise ValueError("trailing text after field value")
    else:
        if any(character.isspace() or character in '"\\,#{}[]' for character in value_text):
            raise ValueError("unsafe scalar field value")
        value = value_text
    return name, value


def _parse_entries(text: str) -> tuple[YarnEntry, ...] | YarnFailure:
    entries = []
    selectors = None
    version = None
    fields = set()
    nested_fields = None
    line_number = 0
    try:
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip() or line.lstrip(' ').startswith('#'):
                continue
            if any(ord(character) < 32 for character in line):
                raise ValueError("control character in entry")
            indentation = len(line) - len(line.lstrip(' '))
            if indentation == 0:
                if selectors is not None:
                    entries.append(YarnEntry(selectors, version))
                selectors = _parse_selectors(line)
                version = None
                fields = set()
                nested_fields = None
                continue
            if selectors is None:
                raise ValueError("field outside an entry")
            if indentation == 2:
                name, value = _parse_field(line[2:])
                if name in fields:
                    raise ValueError("duplicate entry field")
                fields.add(name)
                nested_fields = set() if value is None else None
                if name == 'version':
                    if value is None:
                        raise ValueError("version must be a scalar")
                    version = value
            elif indentation == 4 and nested_fields is not None:
                name, value = _parse_field(line[4:])
                if name in nested_fields or value is None:
                    raise ValueError("duplicate or nested subtree field")
                nested_fields.add(name)
            else:
                raise ValueError("unsafe entry indentation")
        if selectors is not None:
            entries.append(YarnEntry(selectors, version))
    except ValueError as error:
        return YarnFailure(INVALID_LOCKFILE, f"line {line_number}: {error}")
    return tuple(entries)


def parse_lockfile(path: Path) -> tuple[YarnEntry, ...] | YarnFailure:
    """Read only this file and return ordered entries or a typed failure.

    Missing/non-exact versions remain visible for dependency-level ambiguity.
    The npm evidence boundary applies its existing exact-version rule; this
    syntax parser does not evaluate versions or resolve declarations.
    """
    try:
        text = path.read_text(encoding='utf-8')
    except (OSError, UnicodeError):
        return YarnFailure(
            UNSUPPORTED_LOCKFILE_FORMAT, "could not read Yarn generation evidence"
        )
    failure = recognize_v1(text)
    if failure is not None:
        return failure
    return _parse_entries(text)
