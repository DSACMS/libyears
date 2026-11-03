"""Complete, conservative explicit PackageReference scope; never evaluate MSBuild."""

from dataclasses import dataclass, field
import re
from xml.parsers import expat

from .nuget_input import (
    LocalInput, NuGetInputFailure, XMLBudget, check_count,
    MAX_ASSERTION_LENGTH, MAX_DIRECT_REFERENCES, MAX_FRAMEWORK_LENGTH,
    MAX_PROJECT_BYTES, MAX_STRING_LENGTH,
)
from .nuget_version import RequestedMinimum, parse_requested_minimum


_PACKAGE_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,99}')
_FRAMEWORK = re.compile(r'[A-Za-z0-9][A-Za-z0-9.-]*')
_PROPERTIES = frozenset({'OutputType', 'Nullable', 'ImplicitUsings', 'LangVersion',
                         'AssemblyName', 'RootNamespace'})
_ITEMS = frozenset({'Compile', 'None', 'ProjectReference', 'FrameworkReference'})
_METADATA = frozenset({'PrivateAssets', 'IncludeAssets', 'ExcludeAssets',
                       'GeneratePathProperty'})


@dataclass(frozen=True)
class DirectDeclaration:
    package_name: str
    package_key: str
    declared_version: str
    requested_minimum: RequestedMinimum


@dataclass(frozen=True)
class ProjectContext:
    sdk: str
    framework: str
    declarations: tuple[DirectDeclaration, ...]


@dataclass
class _Element:
    name: str
    attributes: dict[str, str]
    children: list = field(default_factory=list)
    text: str = ''


def _literal(value: str) -> bool:
    # No property/item/metadata expansion or wildcard interpretation is attempted.
    return bool(value) and value == value.strip() and not any(
        marker in value for marker in ('$(', '@(', '%(', '*', '?'))


def _metadata_literal(value: str) -> bool:
    # Asset metadata is retained only as literal ancillary information. A star
    # here does not select package identities or change the counted population.
    return bool(value) and value == value.strip() and not any(
        marker in value for marker in ('$(', '@(', '%('))


def _xml_pass(text: str, collect: bool) -> tuple[_Element | None, bool]:
    parser = expat.ParserCreate()
    budget = XMLBudget()
    stack = []
    lengths = []
    root = None
    unsupported = False

    def reject_construct(*unused):
        nonlocal unsupported
        unsupported = True

    def declaration(version, encoding, standalone):
        if encoding is not None and encoding.lower() != 'utf-8':
            reject_construct()

    def start(name, attributes):
        nonlocal root
        budget.start(attributes)
        check_count(len(name), MAX_STRING_LENGTH)
        lengths.append(0)
        if collect:
            element = _Element(name, attributes)
            if stack:
                stack[-1].children.append(element)
            else:
                root = element
            stack.append(element)

    def characters(value):
        if lengths:
            lengths[-1] += len(value)
            check_count(lengths[-1], MAX_STRING_LENGTH)
        if collect and stack:
            stack[-1].text += value

    def end(name):
        lengths.pop()
        if collect:
            stack.pop()
        budget.end()

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.CharacterDataHandler = characters
    parser.XmlDeclHandler = declaration
    parser.StartDoctypeDeclHandler = reject_construct
    parser.EntityDeclHandler = reject_construct
    parser.CommentHandler = lambda value: check_count(len(value), MAX_STRING_LENGTH)
    parser.ProcessingInstructionHandler = lambda target, value: (
        check_count(len(target), MAX_STRING_LENGTH),
        check_count(len(value), MAX_STRING_LENGTH))
    # A DefaultHandler prevents expansion of declared general entities. External
    # entities are acknowledged without opening anything; all DTD input is rejected.
    parser.DefaultHandler = lambda value: None
    parser.ExternalEntityRefHandler = lambda *unused: 1
    try:
        parser.Parse(text, True)
    except expat.ExpatError:
        raise NuGetInputFailure('malformed') from None
    return root, unsupported


def _simple_value(element: _Element) -> str | None:
    if element.attributes or element.children or not _literal(element.text):
        return None
    return element.text


def _reference(element: _Element) -> DirectDeclaration | None:
    attributes = element.attributes
    if set(attributes) - ({'Include', 'Version'} | _METADATA):
        return None
    name = attributes.get('Include', '')
    version = attributes.get('Version', '')
    minimum = parse_requested_minimum(version)
    if _PACKAGE_ID.fullmatch(name) is None or minimum is None or element.text.strip():
        return None
    seen = set(attributes) & _METADATA
    if any(not _metadata_literal(attributes[key]) for key in seen):
        return None
    for child in element.children:
        if child.name not in _METADATA or child.name in seen:
            return None
        if child.attributes or child.children or not _metadata_literal(child.text):
            return None
        seen.add(child.name)
    return DirectDeclaration(name, name.lower(), version, minimum)


def _inert_item(element: _Element) -> bool:
    # Even excluded reference paths remain opaque strings; nothing follows them.
    return (set(element.attributes) == {'Include'} and not element.children
            and not element.text.strip() and _literal(element.attributes['Include']))


def parse_project(source: LocalInput) -> ProjectContext:
    """Accept the complete bounded project or raise a safe private category.

    Framing is checked before any supported-context decisions, so malformed XML
    always wins over an earlier unsupported declaration. No partial population
    escapes this function, and requests never become selected-version evidence.
    """
    check_count(len(source.data), MAX_PROJECT_BYTES)
    # The reader strictly decodes UTF-8. Keep this seam equally safe for callers
    # supplying LocalInput directly rather than going through the reader.
    try:
        text = source.data.decode('utf-8', errors='strict')
    except UnicodeError:
        raise NuGetInputFailure('malformed') from None
    unused, unsupported_xml = _xml_pass(text, False)
    root, unused = _xml_pass(text, True)
    if unsupported_xml:
        raise NuGetInputFailure('unsupported')
    if (root.name != 'Project' or set(root.attributes) != {'Sdk'}
            or not _literal(root.attributes.get('Sdk', '')) or root.text.strip()):
        raise NuGetInputFailure('unsupported')
    sdk = root.attributes['Sdk']
    check_count(len(sdk), MAX_ASSERTION_LENGTH)
    frameworks = []
    declarations = []
    identities = set()
    unsupported = False
    duplicate = False
    reference_count = 0
    for group in root.children:
        if group.attributes or group.text.strip():
            unsupported = True
        if group.name == 'PropertyGroup':
            for element in group.children:
                value = _simple_value(element)
                if element.name in ('TargetFramework', 'TargetFrameworks'):
                    if (value is None or _FRAMEWORK.fullmatch(value) is None):
                        unsupported = True
                    else:
                        check_count(len(value), MAX_FRAMEWORK_LENGTH)
                        frameworks.append(value)
                elif element.name not in _PROPERTIES or value is None:
                    unsupported = True
        elif group.name == 'ItemGroup':
            for element in group.children:
                if element.name == 'PackageReference':
                    # Count encountered references even if their syntax is rejected.
                    reference_count += 1
                    check_count(reference_count, MAX_DIRECT_REFERENCES)
                    reference = _reference(element)
                    if reference is None:
                        unsupported = True
                    else:
                        duplicate |= reference.package_key in identities
                        identities.add(reference.package_key)
                        declarations.append(reference)
                elif element.name not in _ITEMS or not _inert_item(element):
                    unsupported = True
        else:
            unsupported = True
    if unsupported or len(frameworks) != 1:
        raise NuGetInputFailure('unsupported')
    if duplicate:
        raise NuGetInputFailure('duplicate')
    return ProjectContext(sdk, frameworks[0], tuple(declarations))
