"""Bounded snapshot population and known-conflict checks; never evaluate MSBuild."""

import re

from .nuget_input import (
    LocalInput, NuGetInputFailure, check_count, MAX_ASSERTION_LENGTH,
    MAX_DIRECT_REFERENCES, MAX_PROJECT_BYTES,
)
from .nuget_lock import LockSnapshot
from .nuget_project import (
    DirectDeclaration, ProjectContext, _FRAMEWORK, _PACKAGE_ID, _literal, _reference,
    _simple_value, _xml_pass,
)
from .nuget_version import parse_requested_minimum, parse_selected_identity


def snapshot_population(source: LocalInput, lock: LockSnapshot) -> ProjectContext:
    """Validate the whole snapshot and all statically known contradictions.

    The returned iteration context comes from lock Direct records. It is usable
    only together with separately accepted v3 testimony; this function establishes
    neither acceptance nor static declaration completeness.
    """
    check_count(len(source.data), MAX_PROJECT_BYTES)
    try:
        text = source.data.decode('utf-8', errors='strict')
    except UnicodeError:
        raise NuGetInputFailure('malformed') from None
    _, forbidden = _xml_pass(text, False)
    root, _ = _xml_pass(text, True)
    if (forbidden or root.name != 'Project'
            or not _literal(root.attributes.get('Sdk', ''))):
        raise NuGetInputFailure('unsupported')
    sdk = root.attributes['Sdk']
    check_count(len(sdk), MAX_ASSERTION_LENGTH)

    direct = {}
    declarations = []
    for entry in lock.entries:
        if entry.kind != 'Direct':
            continue
        match = re.fullmatch(r'\[([0-9.]+), \)', entry.requested or '')
        minimum = parse_requested_minimum(match[1]) if match else None
        if (minimum is None or minimum.normalized_version != match[1]
                or parse_selected_identity(entry.resolved) is None):
            raise NuGetInputFailure('unsupported')
        direct[entry.package_key] = entry
        declarations.append(DirectDeclaration(entry.package_name, entry.package_key,
                                               minimum.normalized_version, minimum))
    check_count(len(declarations), MAX_DIRECT_REFERENCES)

    # Detect duplicate literal identities even when A reported an unrelated
    # unsupported construct first. Conditional occurrences are not evaluated.
    identities = set()
    reference_count = 0
    pending = [root]
    while pending:
        element = pending.pop()
        pending.extend(element.children)
        if element.name != 'PackageReference':
            continue
        reference_count += 1
        check_count(reference_count, MAX_DIRECT_REFERENCES)
        name = element.attributes.get('Include', '')
        if _PACKAGE_ID.fullmatch(name):
            key = name.lower()
            if key in identities:
                raise NuGetInputFailure('duplicate')
            identities.add(key)

    frameworks = []
    for group in root.children:
        if 'Condition' in group.attributes:
            continue
        for element in group.children:
            if 'Condition' in element.attributes:
                continue
            if group.name == 'PropertyGroup' and element.name in (
                    'TargetFramework', 'TargetFrameworks'):
                value = element.text
                if not element.children and _literal(value):
                    # A literal list is a known multi-framework contradiction.
                    if ';' in value:
                        raise NuGetInputFailure('context_mismatch')
                    if _FRAMEWORK.fullmatch(value):
                        frameworks.append(value)
            if group.name == 'ItemGroup' and element.name == 'PackageReference':
                name = element.attributes.get('Include', '')
                if _PACKAGE_ID.fullmatch(name) is None:
                    continue
                entry = direct.get(name.lower())
                if entry is None:
                    raise NuGetInputFailure('context_mismatch')
                minimum = parse_requested_minimum(element.attributes.get('Version'))
                if minimum is not None and entry.requested != (
                        '[' + minimum.normalized_version + ', )'):
                    raise NuGetInputFailure('context_mismatch')
    if any(value != lock.framework for value in frameworks):
        raise NuGetInputFailure('context_mismatch')
    return ProjectContext(sdk, lock.framework, tuple(declarations))


# These constructs need interpretation or accepted supplier context. They do not
# prevent known literal facts elsewhere from revealing a contradiction.
_REPOSITORY_MUTATIONS = frozenset(name.lower() for name in (
    'Import', 'Target', 'Choose', 'PackageVersion', 'GlobalPackageReference',
    'ManagePackageVersionsCentrally', 'CentralPackageVersionOverrideEnabled',
    'CentralPackageTransitivePinningEnabled', 'RuntimeIdentifier', 'RuntimeIdentifiers',
))


def repository_snapshot_population(source: LocalInput, lock: LockSnapshot) -> ProjectContext | None:
    """Qualify current bytes by policy, never claim evaluated/producer history.

    None means insufficient observable facts, allowing explicit B2 testimony.
    A raised failure means unsafe evidence or a known contradiction, never a
    reason to try another route. Full literal reference equality is checked even
    when another fact makes automatic qualification unavailable.
    """
    population = snapshot_population(source, lock)
    root, _ = _xml_pass(source.data.decode('utf-8'), True)
    eligible = (set(root.attributes) == {'Sdk'} and not root.text.strip())
    references_complete = True
    references = {}
    frameworks = []
    direct = {entry.package_key: entry for entry in lock.entries if entry.kind == 'Direct'}
    pending = [(root, None, None, False)]
    while pending:
        element, parent, grandparent, conditioned = pending.pop()
        conditioned = conditioned or 'Condition' in element.attributes
        pending.extend((child, element, parent, conditioned) for child in element.children)
        name = element.name.lower()
        if name in _REPOSITORY_MUTATIONS:
            eligible = False
        if name in ('targetframework', 'targetframeworks'):
            value = _simple_value(element)
            if not conditioned and value is not None:
                if ';' in value or (_FRAMEWORK.fullmatch(value) and value != lock.framework):
                    raise NuGetInputFailure('context_mismatch')
            if (conditioned or element.name not in ('TargetFramework', 'TargetFrameworks')
                    or parent is None or parent.name != 'PropertyGroup'
                    or grandparent is not root or parent.attributes or parent.text.strip()
                    or value is None or _FRAMEWORK.fullmatch(value) is None):
                eligible = False
            else:
                frameworks.append(value)
        if name != 'packagereference':
            continue
        reference = _reference(element) if element.name == 'PackageReference' else None
        if (conditioned or parent is None or parent.name != 'ItemGroup'
                or grandparent is not root or parent.attributes or parent.text.strip()
                or reference is None):
            references_complete = False
            eligible = False
        else:
            if reference.package_key in references:
                raise NuGetInputFailure('duplicate')
            references[reference.package_key] = reference
        # A supported literal identity/request is a known fact even if other
        # attributes/metadata make this occurrence ineligible for automatic B1.
        key = element.attributes.get('Include', '').lower()
        minimum = parse_requested_minimum(element.attributes.get('Version'))
        if not conditioned and _PACKAGE_ID.fullmatch(key):
            if key not in direct:
                raise NuGetInputFailure('context_mismatch')
            if minimum is not None and direct[key].requested != (
                    '[' + minimum.normalized_version + ', )'):
                raise NuGetInputFailure('context_mismatch')
            for child in element.children:
                if child.name == 'Version':
                    child_minimum = parse_requested_minimum(_simple_value(child))
                    if (minimum is not None and child_minimum is not None
                            and minimum != child_minimum):
                        raise NuGetInputFailure('context_mismatch')
    if references_complete and set(references) != set(direct):
        raise NuGetInputFailure('context_mismatch')
    if not eligible or not references_complete or len(frameworks) != 1:
        return None
    return population
