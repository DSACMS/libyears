"""NuGet-local bounded input primitives; no discovery, evaluation or network."""

from dataclasses import dataclass
import json
import math
import os
from pathlib import Path
import re
import stat


MAX_PROJECT_BYTES = 1024 * 1024
MAX_LOCK_BYTES = 16 * 1024 * 1024
MAX_PROVENANCE_BYTES = 16 * 1024 * 1024
MAX_XML_DEPTH = 32
MAX_XML_ELEMENTS = 50_000
MAX_XML_ATTRIBUTES = 32
MAX_JSON_DEPTH = 32
MAX_JSON_VALUES = 200_000
MAX_STRING_LENGTH = 16 * 1024
MAX_COMPONENT_DIGITS = 32
MAX_DIRECT_REFERENCES = 10_000
MAX_LOCK_ENTRIES = 50_000
MAX_PACKAGE_RECORDS = 50_000
MAX_FRAMEWORK_LENGTH = 128
MAX_ASSERTION_LENGTH = 256
_DIRECTORY_OPEN = os.open
_DIGITS = re.compile(r'[0-9]+')


class NuGetInputFailure(ValueError):
    """A private classification, mapped to the consuming source's S6 reason."""

    def __init__(self, category: str):
        self.category = category
        super().__init__('NuGet input rejected: ' + category + '.')


@dataclass(frozen=True)
class LocalInput:
    data: bytes
    text: str


def check_count(count: int, maximum: int) -> None:
    if count > maximum:
        raise NuGetInputFailure('limit')


def bounded_string(value: object, maximum: int = MAX_STRING_LENGTH) -> bool:
    return isinstance(value, str) and len(value) <= maximum


def schema_version_one(value: object) -> bool:
    """JSON booleans are not schema integers, despite Python's int subclassing."""
    return type(value) is int and value == 1


@dataclass
class ValidationFindings:
    """Finish a whole semantic pass before choosing malformed over unsupported."""

    malformed: bool = False
    unsupported: bool = False

    def finish(self) -> None:
        if self.malformed:
            raise NuGetInputFailure('malformed')
        if self.unsupported:
            raise NuGetInputFailure('unsupported')


@dataclass
class XMLBudget:
    depth: int = 0
    elements: int = 0

    def start(self, attributes: dict[str, str]) -> None:
        self.depth += 1
        self.elements += 1
        check_count(self.depth, MAX_XML_DEPTH)
        check_count(self.elements, MAX_XML_ELEMENTS)
        check_count(len(attributes), MAX_XML_ATTRIBUTES)
        for name, value in attributes.items():
            check_count(len(name), MAX_STRING_LENGTH)
            check_count(len(value), MAX_STRING_LENGTH)

    def end(self) -> None:
        self.depth -= 1


def _identity(info: os.stat_result) -> tuple:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size, info.st_mtime_ns)


class ScopedNuGetReader:
    """Use as a context manager, reading only the three explicitly allowed names."""

    def __init__(self, root: Path, project_name: str, provenance_name: str | None = None):
        names = [project_name, 'packages.lock.json']
        if provenance_name is not None:
            names.append(provenance_name)
        for name in names:
            if (not isinstance(name, str) or not name or name in ('.', '..')
                    or '/' in name or '\\' in name or '\x00' in name):
                raise ValueError('NuGet input requires immediate filenames.')
        if len(set(names)) != len(names):
            raise ValueError('NuGet input filenames must be distinct.')
        self.root = Path(root)
        self.root_spelling = self.root.absolute()
        self.limits = {project_name: MAX_PROJECT_BYTES,
                       'packages.lock.json': MAX_LOCK_BYTES}
        if provenance_name is not None:
            self.limits[provenance_name] = MAX_PROVENANCE_BYTES
        self.directory = None

    def __enter__(self):
        flags = ('O_DIRECTORY', 'O_NOFOLLOW', 'O_NONBLOCK')
        if (any(not getattr(os, flag, 0) for flag in flags)
                or os.stat not in getattr(os, 'supports_follow_symlinks', ())
                or any(function not in getattr(os, 'supports_dir_fd', ())
                       for function in (_DIRECTORY_OPEN, os.stat, os.readlink))):
            raise NuGetInputFailure('malformed')
        try:
            self.root = self.root.resolve(strict=True)
            self.directory = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            self.root_identity = _identity(os.fstat(self.directory))
        except (OSError, RuntimeError, NotImplementedError):
            if self.directory is not None:
                os.close(self.directory)
                self.directory = None
            raise NuGetInputFailure('malformed') from None
        return self

    def __exit__(self, *unused):
        if self.directory is not None:
            os.close(self.directory)
            self.directory = None

    def _root_unchanged(self) -> bool:
        return (_identity(self.root.stat()) == self.root_identity
                and _identity(self.root_spelling.stat()) == self.root_identity)

    def _resolve_target(self, name: str) -> tuple[Path, os.stat_result]:
        """Follow contained symlinks without inspecting an outside target."""
        pending = [name]
        components = []
        directories = [self.directory]
        links = 0
        try:
            while pending:
                component = pending.pop(0)
                if component in ('', '.'):
                    continue
                if component == '..':
                    if not components:
                        raise NuGetInputFailure('malformed')
                    components.pop()
                    os.close(directories.pop())
                    continue
                inspected = os.stat(component, dir_fd=directories[-1], follow_symlinks=False)
                if stat.S_ISLNK(inspected.st_mode):
                    links += 1
                    if links > 40:
                        raise NuGetInputFailure('malformed')
                    target = Path(os.readlink(component, dir_fd=directories[-1]))
                    if target.is_absolute():
                        try:
                            target = target.relative_to(self.root)
                        except ValueError:
                            target = target.relative_to(self.root_spelling)
                        while len(directories) > 1:
                            os.close(directories.pop())
                        components.clear()
                    pending = list(target.parts) + pending
                    continue
                components.append(component)
                if not pending:
                    return self.root.joinpath(*components), inspected
                if not stat.S_ISDIR(inspected.st_mode):
                    raise NuGetInputFailure('malformed')
                directory = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                    dir_fd=directories[-1])
                directories.append(directory)
                if _identity(os.fstat(directory)) != _identity(inspected):
                    raise NuGetInputFailure('malformed')
            raise NuGetInputFailure('malformed')
        finally:
            for directory in reversed(directories[1:]):
                os.close(directory)

    def read(self, name: str) -> LocalInput:
        if name not in self.limits:
            raise ValueError('Only selected NuGet input filenames may be read.')
        if self.directory is None:
            raise RuntimeError('Use the NuGet reader as a context manager.')
        try:
            inspected_link = os.stat(name, dir_fd=self.directory, follow_symlinks=False)
        except FileNotFoundError:
            raise NuGetInputFailure('missing') from None
        except OSError:
            raise NuGetInputFailure('malformed') from None
        descriptors = []
        try:
            resolved, inspected = self._resolve_target(name)
            relative = resolved.relative_to(self.root)
            if not stat.S_ISREG(inspected.st_mode):
                raise NuGetInputFailure('malformed')
            directory = self.directory
            flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
            for component in relative.parts[:-1]:
                directory = os.open(component, flags, dir_fd=directory)
                descriptors.append(directory)
            descriptor = os.open(relative.parts[-1],
                                 os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                 dir_fd=directory)
            descriptors.append(descriptor)
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode) or _identity(before) != _identity(inspected):
                raise NuGetInputFailure('malformed')
            remaining = self.limits[name] + 1
            chunks = []
            while remaining:
                chunk = os.read(descriptor, min(remaining, 64 * 1024))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            data = b''.join(chunks)
            final_path, final_info = self._resolve_target(name)
            if (_identity(os.fstat(descriptor)) != _identity(before)
                    or final_path != resolved
                    or _identity(final_info) != _identity(inspected)
                    or _identity(os.stat(name, dir_fd=self.directory, follow_symlinks=False))
                    != _identity(inspected_link)
                    or not self._root_unchanged()):
                raise NuGetInputFailure('malformed')
        except (OSError, RuntimeError, ValueError, NotImplementedError) as error:
            if isinstance(error, NuGetInputFailure):
                raise
            raise NuGetInputFailure('malformed') from None
        finally:
            for descriptor in reversed(descriptors):
                os.close(descriptor)
        check_count(len(data), self.limits[name])
        try:
            return LocalInput(data, data.decode('utf-8', errors='strict'))
        except UnicodeError:
            raise NuGetInputFailure('malformed') from None


def _string_end(text: str, start: int) -> tuple[int, int]:
    """Count decoded characters without constructing attacker-controlled strings."""
    index = start + 1
    length = 0
    while index < len(text):
        character = text[index]
        if character == '"':
            return index + 1, length
        if character == '\\':
            index += 1
            if index >= len(text):
                break
            if text[index] == 'u':
                digits = text[index + 1:index + 5]
                if len(digits) != 4 or any(c not in '0123456789abcdefABCDEF' for c in digits):
                    raise NuGetInputFailure('malformed')
                index += 4
                # Python's JSON decoder combines an escaped UTF-16 surrogate pair.
                if 0xD800 <= int(digits, 16) <= 0xDBFF and text[index + 1:index + 3] == '\\u':
                    low = text[index + 3:index + 7]
                    if (len(low) == 4 and all(c in '0123456789abcdefABCDEF' for c in low)
                            and 0xDC00 <= int(low, 16) <= 0xDFFF):
                        index += 6
        length += 1
        check_count(length, MAX_STRING_LENGTH)
        index += 1
    raise NuGetInputFailure('malformed')


def _guard_json(text: str) -> None:
    index = 0
    depth = 0
    values = 0
    while index < len(text):
        character = text[index]
        if character.isspace() or character in ',:':
            index += 1
            continue
        if character in '{[':
            depth += 1
            values += 1
            check_count(depth, MAX_JSON_DEPTH)
            index += 1
        elif character in '}]':
            depth -= 1
            index += 1
        elif character == '"':
            index, unused = _string_end(text, index)
            following = index
            while following < len(text) and text[following].isspace():
                following += 1
            if following == len(text) or text[following] != ':':
                values += 1
        else:
            end = index
            while end < len(text) and not text[end].isspace() and text[end] not in ',:[]{}':
                end += 1
            token = text[index:end]
            if token[:1] in '-0123456789':
                for digits in _DIGITS.finditer(token):
                    check_count(len(digits.group()), MAX_COMPONENT_DIGITS)
            values += 1
            index = end
        check_count(values, MAX_JSON_VALUES)


def _pairs(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise NuGetInputFailure('malformed')
        result[key] = value
    return result


def _integer(text: str) -> int:
    check_count(len(text.lstrip('-')), MAX_COMPONENT_DIGITS)
    return int(text)


def _float(text: str) -> float:
    value = float(text)
    if not math.isfinite(value):
        raise NuGetInputFailure('malformed')
    return value


def _constant(unused: str):
    raise NuGetInputFailure('malformed')


def decode_json(text: str) -> object:
    """Guard resources lexically, then reject malformed framing and duplicate keys.

    Consumers validate the complete returned structure, accumulating type failures
    before unsupported semantics with ValidationFindings. No parser may salvage
    rows before that complete validation succeeds.
    """
    _guard_json(text)
    try:
        return json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant,
                          parse_int=_integer, parse_float=_float)
    except (ValueError, RecursionError) as error:
        if isinstance(error, NuGetInputFailure):
            raise
        raise NuGetInputFailure('malformed') from None
