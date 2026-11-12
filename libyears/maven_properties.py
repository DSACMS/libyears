"""Bounded repository-only scalar substitutions for Maven declared facts."""

from dataclasses import dataclass
import re

from .maven_model import MavenFieldBasis, MavenFieldOrigin

MAX_PROPERTIES = 4096
MAX_EXPANSION_DEPTH = 16
MAX_SUBSTITUTIONS = 1024
MAX_EXPANDED_BYTES = 64 * 1024
_NAME = re.compile(r'[A-Za-z][A-Za-z0-9_.-]{0,127}', re.ASCII)
_EXPRESSION = re.compile(r'\$\{([^{}]*)\}')
_RESERVED = ('project.', 'pom.', 'env.', 'system.', 'settings.', 'user.', 'session.')
_RESERVED_NAMES = frozenset(name[:-1] for name in _RESERVED) | {'basedir', 'baseUri'}


class PropertyFailure(ValueError):
    def __init__(self):
        super().__init__('unsupported Maven scalar attribution')


@dataclass(frozen=True, slots=True)
class ScalarProperty:
    value: str
    origin: MavenFieldOrigin


def read_properties(container, source):
    """Return values, blocked keys and whole-container uncertainty; no lookup."""
    values = {}
    blocked = set()
    unknown = False
    if container is None:
        return values, blocked, unknown
    if container.text.strip() or len(container.children) > MAX_PROPERTIES:
        return values, blocked, True
    for child in container.children:
        key = child.name
        if not _NAME.fullmatch(key):
            unknown = True
            continue
        if (child.namespace != container.namespace or child.attributes or child.children
                or key in values or key in blocked):
            values.pop(key, None)
            blocked.add(key)
            continue
        # This expression has consumer/filesystem context in Maven. Never
        # inherit or resolve a repository-written namesake as that builtin.
        if key == 'project.directory':
            continue
        values[key] = ScalarProperty(child.text.strip(),
                                     MavenFieldOrigin(source, key, MavenFieldBasis.PROPERTY))
    return values, blocked, unknown


def expand_scalar(text, values, builtins, blocked=frozenset(), *, unknown=False, trusted=frozenset()):
    """Expand only supported local expressions, collecting their actual origins.

    builtins maps the two explicitly supported model names to ScalarProperty or
    None. No ambient environment, path, CLI, settings or system access exists.
    """
    substitutions = 0
    origins = []

    def expand(value, trail):
        nonlocal substitutions
        if len(trail) > MAX_EXPANSION_DEPTH:
            raise PropertyFailure()
        fragments = []
        cursor = 0
        size = 0
        for match in _EXPRESSION.finditer(value):
            name = match.group(1)
            substitutions += 1
            if substitutions > MAX_SUBSTITUTIONS or not _NAME.fullmatch(name) or name in trail:
                raise PropertyFailure()
            if name in builtins:
                prop = builtins[name]
            elif (name.startswith(_RESERVED) or name in _RESERVED_NAMES
                  or name in blocked or (unknown and name not in trusted)):
                raise PropertyFailure()
            else:
                prop = values.get(name)
            if prop is None:
                raise PropertyFailure()
            origins.append(prop.origin)
            replacement = expand(prop.value, (*trail, name))
            literal = value[cursor:match.start()]
            size += len(literal.encode('utf-8')) + len(replacement.encode('utf-8'))
            if size > MAX_EXPANDED_BYTES:
                raise PropertyFailure()
            fragments.extend((literal, replacement))
            cursor = match.end()
        fragments.append(value[cursor:])
        result = ''.join(fragments)
        if '$' in result or len(result.encode('utf-8')) > MAX_EXPANDED_BYTES:
            raise PropertyFailure()
        return result

    result = expand(text, ())
    return result, tuple(dict.fromkeys(origins))
