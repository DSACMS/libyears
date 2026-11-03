"""Explicit supplier testimony and the local public-lookup authority gate.

No file discovery, configuration inference, registry lookup or producer execution
occurs here. Private records must never be attached to public report objects.
"""

import base64
import binascii
from dataclasses import dataclass, field
import hashlib
import re

from .nuget_input import (
    LocalInput, NuGetInputFailure, check_count, decode_json,
    MAX_ASSERTION_LENGTH, MAX_FRAMEWORK_LENGTH, MAX_PACKAGE_RECORDS,
    MAX_PROVENANCE_BYTES,
)
from .nuget_project import ProjectContext
from .nuget_version import SelectedIdentity, parse_selected_identity


PUBLIC_ORIGIN = 'https://api.nuget.org/v3/index.json'
_PACKAGE_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,99}')
_DIGEST = re.compile(r'[0-9a-f]{64}')
_ENVELOPE = frozenset({'version', 'project', 'framework', 'project_sha256',
                       'lock_sha256', 'producer', 'coherent_snapshot',
                       'baseline', 'packages'})
_BASELINE = frozenset({'sdk', 'sdk_version', 'explicit_population_complete',
                       'unsupported_membership_version_influences',
                       'unsupported_framework_rid_influences',
                       'unsupported_source_influences'})


@dataclass(frozen=True)
class PackageOrigin:
    package_key: str
    normalized_version: str
    content_hash: str | None = field(repr=False)
    origins: tuple[str, ...] = field(repr=False)


@dataclass(frozen=True)
class SupplierContext:
    project_sha256: str = field(repr=False)
    lock_sha256: str = field(repr=False)
    packages: tuple[PackageOrigin, ...] = field(repr=False)


@dataclass(frozen=True)
class LocalAuthority:
    """Internal capability passed to the public adapter, never to serialization."""

    project_sha256: str = field(repr=False)
    lock_sha256: str = field(repr=False)
    package_key: str
    normalized_version: str
    content_hash: bytes = field(repr=False)


@dataclass(frozen=True)
class LocalAuthorityFailure:
    reason: str
    origin_state: str = 'unavailable'
    content_hash_state: str = 'unavailable'


def _object(value: object, required: frozenset, optional: frozenset = frozenset()) -> dict:
    if (not isinstance(value, dict) or not required <= set(value)
            or set(value) - required - optional):
        raise NuGetInputFailure('malformed')
    return value


def _string(value: object, maximum: int = MAX_ASSERTION_LENGTH) -> str:
    if not isinstance(value, str) or not value:
        raise NuGetInputFailure('malformed')
    check_count(len(value), maximum)
    return value


def _boolean(value: object) -> bool:
    if type(value) is not bool:
        raise NuGetInputFailure('malformed')
    return value


def _digest(value: object) -> str:
    if not isinstance(value, str) or _DIGEST.fullmatch(value) is None:
        raise NuGetInputFailure('malformed')
    return value


def _package(value: object) -> PackageOrigin:
    record = _object(value, frozenset({'id', 'version'}),
                     frozenset({'content_hash', 'origins'}))
    name = record['id']
    if not isinstance(name, str) or _PACKAGE_ID.fullmatch(name) is None:
        raise NuGetInputFailure('malformed')
    identity = parse_selected_identity(record['version'])
    if identity is None:
        raise NuGetInputFailure('malformed')
    if 'content_hash' in record and not isinstance(record['content_hash'], str):
        raise NuGetInputFailure('malformed')
    origins = record.get('origins', [])
    if not isinstance(origins, list) or any(not isinstance(origin, str) for origin in origins):
        raise NuGetInputFailure('malformed')
    return PackageOrigin(name.lower(), identity.normalized_version,
                         record.get('content_hash'), tuple(origins))


def parse_provenance(source: LocalInput, *, project_name: str,
                     project_source: LocalInput, lock_source: LocalInput,
                     project: ProjectContext) -> SupplierContext:
    """Accept whole framing before binding bytes and supplier assertions.

    ``malformed``/``limit`` mean invalid witness; ``context_mismatch`` means
    wrong binding/coherence. ``unsupported`` is reserved for asserted unsupported
    influences/incomplete population, which invalidate the discovered denominator.
    Callers retain independently discovered N for the other failures. The caller
    supplies only an explicitly selected witness; this function performs no I/O.
    """
    check_count(len(source.data), MAX_PROVENANCE_BYTES)
    try:
        text = source.data.decode('utf-8', errors='strict')
    except UnicodeError:
        raise NuGetInputFailure('malformed') from None
    value = _object(decode_json(text), _ENVELOPE)
    if type(value['version']) is not int or value['version'] != 1:
        raise NuGetInputFailure('malformed')
    name = _string(value['project'])
    framework = _string(value['framework'], MAX_FRAMEWORK_LENGTH)
    project_digest = _digest(value['project_sha256'])
    lock_digest = _digest(value['lock_sha256'])
    producer = _object(value['producer'], frozenset({'name', 'version'}))
    _string(producer['name'])
    _string(producer['version'])
    coherent = _boolean(value['coherent_snapshot'])
    baseline = _object(value['baseline'], _BASELINE)
    sdk = _string(baseline['sdk'])
    _string(baseline['sdk_version'])
    complete = _boolean(baseline['explicit_population_complete'])
    influences = [_boolean(baseline[key]) for key in (
        'unsupported_membership_version_influences',
        'unsupported_framework_rid_influences', 'unsupported_source_influences')]
    records = value['packages']
    if not isinstance(records, list):
        raise NuGetInputFailure('malformed')
    check_count(len(records), MAX_PACKAGE_RECORDS)
    packages = []
    seen = set()
    for record in records:
        package = _package(record)
        identity = (package.package_key, package.normalized_version)
        if identity in seen:
            raise NuGetInputFailure('malformed')
        seen.add(identity)
        packages.append(package)

    # No semantic decision escapes before every package record is framed.
    if (not coherent or name != project_name or framework != project.framework
            or sdk != project.sdk
            or project_digest != hashlib.sha256(project_source.data).hexdigest()
            or lock_digest != hashlib.sha256(lock_source.data).hexdigest()):
        raise NuGetInputFailure('context_mismatch')
    if not complete or any(influences):
        raise NuGetInputFailure('unsupported')
    return SupplierContext(project_digest, lock_digest, tuple(packages))


def decode_content_hash(value: object) -> bytes | None:
    """Decode strict standard base64 SHA-512 without accepting whitespace."""
    if not isinstance(value, str):
        return None
    try:
        decoded = base64.b64decode(value, validate=True)
    except (ValueError, binascii.Error):
        return None
    if len(decoded) != 64:
        return None
    return decoded


def authorize_package(context: SupplierContext, package_key: str,
                      selected: SelectedIdentity,
                      lock_hash: str | None) -> LocalAuthority | LocalAuthorityFailure:
    """Only exact public supplier origin plus local hash agreement admits lookup."""
    key = package_key.lower()
    matching = [package for package in context.packages
                if package.package_key == key
                and package.normalized_version == selected.normalized_version]
    if len(matching) != 1 or matching[0].origins != (PUBLIC_ORIGIN,):
        return LocalAuthorityFailure('unsupported_dependency_source', 'unsupported')
    lock_content = decode_content_hash(lock_hash)
    witness_content = decode_content_hash(matching[0].content_hash)
    if lock_content is None or witness_content is None:
        return LocalAuthorityFailure('content_hash_unavailable', 'asserted_public')
    if lock_content != witness_content:
        return LocalAuthorityFailure('content_hash_mismatch', 'asserted_public', 'mismatch')
    return LocalAuthority(context.project_sha256, context.lock_sha256, key,
                          selected.normalized_version, lock_content)
