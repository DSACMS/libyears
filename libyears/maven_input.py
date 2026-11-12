"""Bounded Maven-local byte snapshots and XML framing, without Maven evaluation."""

from dataclasses import dataclass, field
from enum import StrEnum
import os
from pathlib import Path
import stat
from xml.parsers import expat

MAX_XML_BYTES = 1024 * 1024
MAX_TOTAL_XML_BYTES = 32 * 1024 * 1024
MAX_CONFIG_BYTES = 64 * 1024
MAX_XML_DEPTH = 32
MAX_XML_ELEMENTS = 50_000
MAX_XML_ATTRIBUTES = 32
MAX_SCALAR_BYTES = 16 * 1024
MAX_PATH_CHARACTERS = 1024
MAX_PATH_COMPONENTS = 32
POM_NAMESPACE = 'http://maven.apache.org/POM/4.0.0'
XSI_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
XINCLUDE_NAMESPACE = 'http://www.w3.org/2001/XInclude'
CONTROL_NAMES = frozenset({'maven.config', 'jvm.config', 'extensions.xml', 'settings.xml'})
_OPEN = os.open
_STAT = os.stat
_SCANDIR = os.scandir


class MavenInputIssue(StrEnum):
    CAPABILITY = 'capability_unavailable'
    NOT_DIRECTORY = 'not_directory'
    PATH = 'unsafe_path'
    MISSING = 'missing'
    UNSAFE = 'unsafe_file'
    CHANGED = 'changed'
    IO = 'io_error'
    LIMIT = 'budget_exceeded'
    UNSELECTED = 'unselected_input'
    XML_MALFORMED = 'xml_malformed'
    XML_UNSUPPORTED = 'xml_unsupported'


class MavenInputFailure(ValueError):
    def __init__(self, issue: MavenInputIssue):
        self.issue = issue
        super().__init__('Maven local input refused: ' + issue.value)


def filesystem_available() -> bool:
    """Check before any stat/open; mocks need not impersonate native functions."""
    return (all(getattr(os, flag, 0) for flag in ('O_DIRECTORY', 'O_NOFOLLOW', 'O_NONBLOCK'))
            and _OPEN in getattr(os, 'supports_dir_fd', ())
            and _STAT in getattr(os, 'supports_dir_fd', ())
            and _STAT in getattr(os, 'supports_follow_symlinks', ())
            and _SCANDIR in getattr(os, 'supports_fd', ()))


def reparse_point(info) -> bool:
    flag = getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400)
    return bool(getattr(info, 'st_file_attributes', 0) & flag)


def directory_identity(info) -> tuple:
    return (info.st_dev, info.st_ino, info.st_mode)


def file_identity(info) -> tuple:
    return (*directory_identity(info), info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def relative_parts(source_id: str) -> tuple[str, ...]:
    if (not isinstance(source_id, str) or not source_id or len(source_id) > MAX_PATH_CHARACTERS
            or '\\' in source_id or ':' in source_id or '$' in source_id or '~' in source_id
            or not source_id.isprintable()):
        raise MavenInputFailure(MavenInputIssue.PATH)
    parts = tuple(source_id.split('/'))
    if len(parts) > MAX_PATH_COMPONENTS or any(part in ('', '.', '..') for part in parts):
        raise MavenInputFailure(MavenInputIssue.PATH)
    return parts


@dataclass(frozen=True, slots=True)
class MavenXMLElement:
    namespace: str | None
    name: str
    attributes: tuple[tuple[str, str], ...]
    text: str
    children: tuple['MavenXMLElement', ...]

    def elements(self, name: str) -> tuple['MavenXMLElement', ...]:
        """Structural field access never silently accepts a foreign namespace."""
        matches = tuple(child for child in self.children if child.name == name)
        if any(child.namespace != self.namespace or child.attributes for child in matches):
            raise MavenInputFailure(MavenInputIssue.XML_UNSUPPORTED)
        return matches

    def scalar(self, name: str) -> str | None:
        """Validate a field on demand; no population/model interpretation here."""
        matches = self.elements(name)
        if not matches:
            return None
        if len(matches) != 1 or matches[0].children or matches[0].attributes:
            raise MavenInputFailure(MavenInputIssue.XML_UNSUPPORTED)
        return matches[0].text


@dataclass(frozen=True, slots=True)
class MavenInputSnapshot:
    source_id: str
    data: bytes
    identity: tuple
    xml: MavenXMLElement | None = None


def _qualified(name):
    if '}' in name:
        return tuple(name.rsplit('}', 1))
    return None, name


@dataclass
class _XMLFrame:
    namespace: str | None
    name: str
    attributes: tuple[tuple[str, str], ...]
    text_parts: list[str] = field(default_factory=list)
    children: list[MavenXMLElement] = field(default_factory=list)


def parse_xml(data: bytes, *, max_bytes: int = MAX_XML_BYTES) -> MavenXMLElement:
    """Whole UTF-8 structural representation, never a partial parser stream."""
    if type(data) is not bytes or len(data) > max_bytes:
        raise MavenInputFailure(MavenInputIssue.LIMIT)
    if b'\x00' in data:
        # Expat autodetects BOM-less UTF-16/32; NUL is never valid UTF-8 XML text.
        raise MavenInputFailure(MavenInputIssue.XML_UNSUPPORTED)
    try:
        data.decode('utf-8-sig')
    except UnicodeError:
        raise MavenInputFailure(MavenInputIssue.XML_UNSUPPORTED) from None
    parser = expat.ParserCreate(namespace_separator='}')
    parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
    stack = []
    root = None
    elements = 0
    namespaces = 0

    def unsupported(*unused):
        raise MavenInputFailure(MavenInputIssue.XML_UNSUPPORTED)

    def declaration(version, encoding, standalone):
        if version != '1.0' or (encoding is not None and encoding.lower() != 'utf-8'):
            unsupported()

    def namespace(prefix, uri):
        nonlocal namespaces
        namespaces += 1
        declaration_name = 'xmlns:' + prefix if prefix else 'xmlns'
        if max(len((uri or '').encode('utf-8')),
               len(declaration_name.encode('utf-8'))) > MAX_SCALAR_BYTES:
            raise MavenInputFailure(MavenInputIssue.LIMIT)

    def start(name, attributes):
        nonlocal elements, namespaces
        elements += 1
        if (len(stack) + 1 > MAX_XML_DEPTH or elements > MAX_XML_ELEMENTS
                or len(attributes) + namespaces > MAX_XML_ATTRIBUTES):
            raise MavenInputFailure(MavenInputIssue.LIMIT)
        namespaces = 0
        uri, local = _qualified(name)
        if uri == XINCLUDE_NAMESPACE:
            unsupported()
        if len(name.encode('utf-8')) > MAX_SCALAR_BYTES:
            raise MavenInputFailure(MavenInputIssue.LIMIT)
        for key, value in attributes.items():
            if max(len(key.encode('utf-8')), len(value.encode('utf-8'))) > MAX_SCALAR_BYTES:
                raise MavenInputFailure(MavenInputIssue.LIMIT)
        stack.append(_XMLFrame(uri, local, tuple(attributes.items())))

    def characters(text):
        if stack:
            stack[-1].text_parts.append(text)

    def end(name):
        nonlocal root
        frame = stack.pop()
        text = ''.join(frame.text_parts)
        if not frame.children and len(text.encode('utf-8')) > MAX_SCALAR_BYTES:
            raise MavenInputFailure(MavenInputIssue.LIMIT)
        node = MavenXMLElement(frame.namespace, frame.name, frame.attributes,
                               text, tuple(frame.children))
        if stack:
            stack[-1].children.append(node)
        else:
            root = node

    parser.XmlDeclHandler = declaration
    parser.StartNamespaceDeclHandler = namespace
    parser.StartElementHandler = start
    parser.CharacterDataHandler = characters
    parser.EndElementHandler = end
    parser.StartDoctypeDeclHandler = unsupported
    parser.EntityDeclHandler = unsupported
    parser.ExternalEntityRefHandler = unsupported
    try:
        for offset in range(0, len(data), 64 * 1024):
            parser.Parse(data[offset:offset + 64 * 1024], False)
        parser.Parse(b'', True)
    except expat.ExpatError:
        raise MavenInputFailure(MavenInputIssue.XML_MALFORMED) from None
    if root is None:
        raise MavenInputFailure(MavenInputIssue.XML_MALFORMED)
    return root


def parse_pom(data: bytes) -> MavenXMLElement:
    root = parse_xml(data)
    if root.name != 'project' or root.namespace not in (None, POM_NAMESPACE):
        raise MavenInputFailure(MavenInputIssue.XML_UNSUPPORTED)
    allowed = {XSI_NAMESPACE + '}schemaLocation', XSI_NAMESPACE + '}noNamespaceSchemaLocation'}
    if any(name not in allowed for name, value in root.attributes):
        raise MavenInputFailure(MavenInputIssue.XML_UNSUPPORTED)
    version = root.scalar('modelVersion')
    if version is None or version.strip() != '4.0.0':
        raise MavenInputFailure(MavenInputIssue.XML_UNSUPPORTED)
    return root


class MavenInputReader:
    """Read only inventoried POMs and exact contained launch/control sentinels."""

    def __init__(self, root: str | Path):
        self.root = os.fspath(root)
        self._root_chain = []
        self.directory = None
        self._candidates = {}
        self._inventoried = False
        self._used = False
        self._directory_ids = {}
        self._cache = {}
        self._failed = {}
        self._xml_bytes = 0

    def __enter__(self):
        if self._used:
            raise RuntimeError('MavenInputReader is single-use')
        if not filesystem_available():
            raise MavenInputFailure(MavenInputIssue.CAPABILITY)
        self._used = True
        try:
            spelling = self.root
            if spelling == '.':
                absolute = os.getcwd()
            elif spelling.startswith('/'):
                absolute = spelling
            else:
                relative_parts(spelling)
                absolute = os.getcwd() + '/' + spelling
            parts = relative_parts(absolute[1:]) if absolute != '/' else ()
            anchor = os.open('/', self._directory_flags())
            try:
                info = os.fstat(anchor)
                if not stat.S_ISDIR(info.st_mode) or reparse_point(info):
                    raise MavenInputFailure(MavenInputIssue.UNSAFE)
                anchor_identity = directory_identity(info)
            except BaseException:
                os.close(anchor)
                raise
            self._root_chain.append((None, None, anchor, anchor_identity))
            parent = anchor
            for index, name in enumerate(parts):
                if index == len(parts) - 1:
                    final = os.stat(name, dir_fd=parent, follow_symlinks=False)
                    if stat.S_ISREG(final.st_mode) and not reparse_point(final):
                        raise MavenInputFailure(MavenInputIssue.NOT_DIRECTORY)
                child, identity = self._open_directory(parent, name)
                self._root_chain.append((parent, name, child, identity))
                parent = child
            self.directory = parent
            self._directory_ids[''] = directory_identity(os.fstat(parent))
            self.check_root()
        except MavenInputFailure:
            self.__exit__()
            raise
        except (OSError, ValueError, NotImplementedError):
            self.__exit__()
            raise MavenInputFailure(MavenInputIssue.IO) from None
        return self

    def __exit__(self, *unused):
        for parent, name, descriptor, identity in reversed(self._root_chain):
            os.close(descriptor)
        self._root_chain.clear()
        self.directory = None

    @staticmethod
    def _directory_flags():
        return os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_NONBLOCK

    def _open_directory(self, parent, name, expected=None):
        info = os.stat(name, dir_fd=parent, follow_symlinks=False)
        if not stat.S_ISDIR(info.st_mode) or reparse_point(info):
            raise MavenInputFailure(MavenInputIssue.UNSAFE)
        if expected is not None and directory_identity(info) != expected:
            raise MavenInputFailure(MavenInputIssue.CHANGED)
        descriptor = os.open(name, self._directory_flags(), dir_fd=parent)
        try:
            opened = os.fstat(descriptor)
            if reparse_point(opened) or directory_identity(opened) != directory_identity(info):
                raise MavenInputFailure(MavenInputIssue.CHANGED)
        except BaseException:
            os.close(descriptor)
            raise
        return descriptor, directory_identity(opened)

    def open_child(self, parent, name, source_directory):
        expected = self._directory_ids.get(source_directory)
        descriptor, identity = self._open_directory(parent, name, expected)
        self._directory_ids[source_directory] = identity
        return descriptor, identity

    def check_root(self):
        if self.directory is None:
            raise RuntimeError('Use MavenInputReader as a context manager')
        for parent, name, descriptor, identity in self._root_chain:
            opened = os.fstat(descriptor)
            if reparse_point(opened) or directory_identity(opened) != identity:
                raise MavenInputFailure(MavenInputIssue.CHANGED)
            if parent is not None:
                info = os.stat(name, dir_fd=parent, follow_symlinks=False)
                if reparse_point(info) or directory_identity(info) != identity:
                    raise MavenInputFailure(MavenInputIssue.CHANGED)

    def inventory(self):
        from .maven_discovery import inventory_reader
        return inventory_reader(self)

    def _register(self, candidates):
        # One inventory defines this reader's immutable input scope.
        if self._inventoried:
            raise RuntimeError('Maven inventory already established')
        self._inventoried = True
        self._candidates.update(candidates)

    def _control_parts(self, source_id):
        parts = relative_parts(source_id)
        if len(parts) < 2 or parts[-2] != '.mvn' or parts[-1] not in CONTROL_NAMES:
            raise MavenInputFailure(MavenInputIssue.UNSELECTED)
        prefix = '/'.join(parts[:-2])
        allowed = set()
        for candidate in self._candidates:
            ancestor = candidate.split('/')[:-1]
            for length in range(len(ancestor) + 1):
                allowed.add('/'.join(ancestor[:length]))
        if prefix not in allowed:
            raise MavenInputFailure(MavenInputIssue.UNSELECTED)
        return parts

    def control_present(self, source_id: str) -> bool:
        parts = self._control_parts(source_id)
        try:
            self._inspect(parts)
            return True
        except MavenInputFailure as failure:
            if failure.issue == MavenInputIssue.MISSING:
                return False
            raise

    def snapshot_control(self, source_id: str) -> MavenInputSnapshot:
        parts = self._control_parts(source_id)
        if parts[-1] == 'settings.xml':
            # T006 must establish an explicit settings selector before any read.
            raise MavenInputFailure(MavenInputIssue.UNSELECTED)
        xml = parts[-1] == 'extensions.xml'
        return self._snapshot(source_id, parts, xml=xml, pom=False)

    def snapshot_selected_settings(self, source_id: str) -> MavenInputSnapshot:
        """Only the policy layer's unique literal root selector calls this route.

        The same descriptor containment, identity and shared XML budgets apply.
        There is no settings discovery or ancestor/home fallback.
        """
        parts = relative_parts(source_id)
        return self._snapshot(source_id, parts, xml=True, pom=False)

    def snapshot_pom(self, source_id: str) -> MavenInputSnapshot:
        parts = relative_parts(source_id)
        if source_id not in self._candidates:
            raise MavenInputFailure(MavenInputIssue.UNSELECTED)
        return self._snapshot(source_id, parts, xml=True, pom=True)

    def _inspect(self, parts):
        """Return regular-file metadata after checking every directory binding."""
        descriptors = []
        bindings = []
        try:
            self.check_root()
            parent = self.directory
            for index, name in enumerate(parts[:-1]):
                prefix = '/'.join(parts[:index + 1])
                child, identity = self.open_child(parent, name, prefix)
                descriptors.append(child)
                bindings.append((parent, name, child, identity))
                parent = child
            info = os.stat(parts[-1], dir_fd=parent, follow_symlinks=False)
            if not stat.S_ISREG(info.st_mode) or reparse_point(info):
                raise MavenInputFailure(MavenInputIssue.UNSAFE)
            self._check_bindings(bindings)
            return info
        except MavenInputFailure:
            raise
        except FileNotFoundError:
            raise MavenInputFailure(MavenInputIssue.MISSING) from None
        except (OSError, ValueError, NotImplementedError):
            raise MavenInputFailure(MavenInputIssue.IO) from None
        finally:
            for descriptor in reversed(descriptors):
                os.close(descriptor)

    def _check_bindings(self, bindings):
        self.check_root()
        for parent, name, descriptor, identity in bindings:
            info = os.stat(name, dir_fd=parent, follow_symlinks=False)
            if (reparse_point(info) or directory_identity(info) != identity
                    or directory_identity(os.fstat(descriptor)) != identity):
                raise MavenInputFailure(MavenInputIssue.CHANGED)

    def _snapshot(self, source_id, parts, *, xml, pom):
        if source_id in self._failed:
            raise MavenInputFailure(self._failed[source_id])
        descriptors = []
        bindings = []
        file_descriptor = None
        try:
            self.check_root()
            parent = self.directory
            for index, name in enumerate(parts[:-1]):
                prefix = '/'.join(parts[:index + 1])
                child, identity = self.open_child(parent, name, prefix)
                descriptors.append(child)
                bindings.append((parent, name, child, identity))
                parent = child
            info = os.stat(parts[-1], dir_fd=parent, follow_symlinks=False)
            if not stat.S_ISREG(info.st_mode) or reparse_point(info):
                raise MavenInputFailure(MavenInputIssue.UNSAFE)
            identity = file_identity(info)
            if pom and identity != self._candidates[source_id]:
                raise MavenInputFailure(MavenInputIssue.CHANGED)
            self._check_bindings(bindings)
            cached = self._cache.get(source_id)
            if cached is not None:
                if cached.identity != identity:
                    raise MavenInputFailure(MavenInputIssue.CHANGED)
                return cached
            limit = MAX_XML_BYTES if xml else MAX_CONFIG_BYTES
            if info.st_size > limit or (xml and self._xml_bytes + info.st_size > MAX_TOTAL_XML_BYTES):
                raise MavenInputFailure(MavenInputIssue.LIMIT)
            flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
            file_descriptor = os.open(parts[-1], flags, dir_fd=parent)
            opened = os.fstat(file_descriptor)
            if reparse_point(opened) or not stat.S_ISREG(opened.st_mode) or file_identity(opened) != identity:
                raise MavenInputFailure(MavenInputIssue.CHANGED)
            self._check_bindings(bindings)
            chunks = []
            remaining = info.st_size
            while remaining:
                chunk = os.read(file_descriptor, min(remaining, 64 * 1024))
                if not chunk or len(chunk) > remaining:
                    raise MavenInputFailure(MavenInputIssue.CHANGED)
                chunks.append(chunk)
                remaining -= len(chunk)
                if xml:
                    self._xml_bytes += len(chunk)
            self._check_bindings(bindings)
            current = os.stat(parts[-1], dir_fd=parent, follow_symlinks=False)
            if (reparse_point(current) or file_identity(current) != identity
                    or file_identity(os.fstat(file_descriptor)) != identity):
                raise MavenInputFailure(MavenInputIssue.CHANGED)
            data = b''.join(chunks)
            if xml:
                representation = parse_pom(data) if pom else parse_xml(data)
            else:
                try:
                    data.decode('utf-8-sig')
                except UnicodeError:
                    raise MavenInputFailure(MavenInputIssue.XML_UNSUPPORTED) from None
                representation = None
            self._check_bindings(bindings)
            final = os.stat(parts[-1], dir_fd=parent, follow_symlinks=False)
            if (reparse_point(final) or file_identity(final) != identity
                    or file_identity(os.fstat(file_descriptor)) != identity):
                raise MavenInputFailure(MavenInputIssue.CHANGED)
            snapshot = MavenInputSnapshot(source_id, data, identity, representation)
            self._cache[source_id] = snapshot
            return snapshot
        except MavenInputFailure as failure:
            self._failed[source_id] = failure.issue
            raise
        except FileNotFoundError:
            self._failed[source_id] = MavenInputIssue.MISSING
            raise MavenInputFailure(MavenInputIssue.MISSING) from None
        except (OSError, ValueError, NotImplementedError):
            self._failed[source_id] = MavenInputIssue.IO
            raise MavenInputFailure(MavenInputIssue.IO) from None
        finally:
            if file_descriptor is not None:
                os.close(file_descriptor)
            for descriptor in reversed(descriptors):
                os.close(descriptor)
