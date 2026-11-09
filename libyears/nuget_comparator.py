"""Repository-bounded public reference policy, never acquisition evidence."""

from dataclasses import dataclass
import re

from .nuget_input import LocalInput, NuGetInputFailure, check_count, MAX_PROJECT_BYTES
from .nuget_project import _xml_pass
from .nuget_provenance import PUBLIC_ORIGIN


@dataclass(frozen=True)
class ComparatorDecision:
    basis: str | None = None
    reason: str | None = None
    testimony_can_resolve: bool = False


UNKNOWN = ComparatorDecision(reason='nuget_comparator_unknown')
PRIVATE = ComparatorDecision(reason='nuget_comparator_private')
AMBIGUOUS = ComparatorDecision(reason='nuget_comparator_ambiguous')
ELIGIBILITY = ComparatorDecision(reason='nuget_comparator_ambiguous', testimony_can_resolve=True)
CONVENTIONAL = ComparatorDecision(basis='conventional_public_policy', testimony_can_resolve=True)
MAPPED = ComparatorDecision(basis='repository_mapping', testimony_can_resolve=True)


@dataclass(frozen=True)
class RepositoryComparatorPolicy:
    sources: dict
    disabled: dict
    mappings: dict
    closed: frozenset = frozenset()
    mapping_active: bool = False
    removed: bool = False
    unknown: bool = False

    def decide(self, package_key: str) -> ComparatorDecision:
        if self.unknown:
            return UNKNOWN
        if self.mapping_active:
            if self.closed != frozenset(('packageSources', 'disabledPackageSources', 'packageSourceMapping')):
                return UNKNOWN
            winners = set()
            best = (-1, -1)
            for key, patterns in self.mappings.items():
                for pattern in patterns:
                    prefix = pattern[:-1] if pattern.endswith('*') else None
                    if prefix is None:
                        rank = (2, 0) if pattern == package_key else None
                    else:
                        rank = (1, len(prefix)) if package_key.startswith(prefix) else None
                    if rank is None:
                        continue
                    if rank > best:
                        best, winners = rank, {key}
                    elif rank == best:
                        winners.add(key)
            if len(winners) != 1:
                return AMBIGUOUS
            key = next(iter(winners))
            if key not in self.sources or self.disabled.get(key, False):
                return UNKNOWN
            return MAPPED if self.sources[key] == PUBLIC_ORIGIN else PRIVATE
        if self.removed or any(key not in self.sources for key in self.disabled):
            return UNKNOWN
        enabled = {key: value for key, value in self.sources.items()
                   if not self.disabled.get(key, False)}
        if any(value != PUBLIC_ORIGIN for value in enabled.values()):
            return ELIGIBILITY
        if any(self.disabled.get(key, False) and value == PUBLIC_ORIGIN
               for key, value in self.sources.items()):
            return PRIVATE
        if 'packageSources' in self.closed and not enabled:
            return PRIVATE
        return CONVENTIONAL


def unknown_policy() -> RepositoryComparatorPolicy:
    return RepositoryComparatorPolicy({}, {}, {}, unknown=True)


def _xml(source: LocalInput):
    check_count(len(source.data), MAX_PROJECT_BYTES)
    text = source.data.decode('utf-8', errors='strict')
    _, forbidden = _xml_pass(text, False)
    if forbidden:
        raise NuGetInputFailure('unsupported')
    root, _ = _xml_pass(text, True)
    return root


def _literal(value):
    if (not value or value != value.strip() or not value.isprintable()
            or any(marker in value for marker in ('$', '%', '@(', '*', '?'))):
        raise NuGetInputFailure('unsupported')
    return value


def _empty(element):
    if element.children or element.text.strip():
        raise NuGetInputFailure('unsupported')


def parse_repository_policy(configs: tuple[LocalInput, ...], project: LocalInput):
    """Validate all bounded inputs before returning any package decisions."""
    try:
        check_count(len(configs), 5)
        check_count(sum(len(item.data) for item in configs), 5 * MAX_PROJECT_BYTES)
        root = _xml(project)
        pending = [root]
        while pending:
            element = pending.pop()
            pending.extend(element.children)
            name = element.name.lower()
            if name.startswith(('restore', 'nuget')) or name in ('import', 'target', 'choose'):
                return unknown_policy()
        sources, disabled, mappings = {}, {}, {}
        collections = {'packageSources': sources, 'disabledPackageSources': disabled,
                       'packageSourceMapping': mappings}
        closed = set()
        mapping_active = removed = False
        for config in configs:
            root = _xml(config)
            if root.name != 'configuration' or root.attributes or root.text.strip():
                return unknown_policy()
            sections = set()
            for section in root.children:
                name = section.name
                if name not in collections or name in sections or section.attributes or section.text.strip():
                    return unknown_policy()
                sections.add(name)
                target = collections[name]
                if name == 'packageSourceMapping':
                    mapping_active = True
                seen = set()
                for index, operation in enumerate(section.children):
                    if operation.name == 'clear':
                        _empty(operation)
                        if index != 0 or operation.attributes:
                            return unknown_policy()
                        target.clear()
                        closed.add(name)
                        continue
                    key = _literal(operation.attributes.get('key', '')).lower()
                    if key in seen:
                        return unknown_policy()
                    seen.add(key)
                    if name == 'packageSourceMapping':
                        if (operation.name != 'packageSource' or set(operation.attributes) != {'key'}
                                or operation.text.strip() or not operation.children):
                            return unknown_policy()
                        patterns = []
                        for child in operation.children:
                            _empty(child)
                            pattern = child.attributes.get('pattern', '').lower()
                            if (child.name != 'package' or set(child.attributes) != {'pattern'}
                                    or len(pattern) > 100
                                    or re.fullmatch(r'(?:[a-z0-9][a-z0-9._-]*\*?|\*)', pattern) is None
                                    or pattern in patterns):
                                return unknown_policy()
                            patterns.append(pattern)
                        target[key] = tuple(patterns)
                        continue
                    _empty(operation)
                    if operation.name == 'remove' and set(operation.attributes) == {'key'}:
                        removed = True
                        target.pop(key, None)
                    elif operation.name == 'add':
                        allowed = {'key', 'value'}
                        if name == 'packageSources' and operation.attributes.get('protocolVersion') == '3':
                            allowed.add('protocolVersion')
                        if set(operation.attributes) != allowed:
                            return unknown_policy()
                        value = _literal(operation.attributes.get('value', ''))
                        if name == 'disabledPackageSources':
                            if value.lower() not in ('true', 'false'):
                                return unknown_policy()
                            value = value.lower() == 'true'
                        target[key] = value
                    else:
                        return unknown_policy()
        return RepositoryComparatorPolicy(sources, disabled, mappings, frozenset(closed),
                                          mapping_active, removed)
    except (NuGetInputFailure, UnicodeError, ValueError):
        return unknown_policy()
