"""Bounded snapshot population and known-conflict checks; never evaluate MSBuild."""

import re

from .nuget_input import (
    LocalInput, NuGetInputFailure, check_count, MAX_ASSERTION_LENGTH,
    MAX_DIRECT_REFERENCES, MAX_PROJECT_BYTES,
)
from .nuget_lock import LockSnapshot
from .nuget_project import (
    DirectDeclaration, ProjectContext, _FRAMEWORK, _PACKAGE_ID, _literal, _xml_pass,
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
    if len(frameworks) > 1 or any(value != lock.framework for value in frameworks):
        raise NuGetInputFailure('context_mismatch')
    return ProjectContext(sdk, lock.framework, tuple(declarations))
