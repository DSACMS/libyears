"""Literal Maven-only identity; grouping never erases original records or refs."""

import re
from dataclasses import replace
from urllib.parse import unquote_to_bytes

from .maven_version import VersionError, is_snapshot, parse_version
from .sbom_model import SbomIdentity, SbomMember

_GROUP = re.compile(r'[A-Za-z0-9_][A-Za-z0-9_-]*(?:\.[A-Za-z0-9_][A-Za-z0-9_-]*)*', re.ASCII)
_ATOM = re.compile(r'[A-Za-z0-9_][A-Za-z0-9_.-]*', re.ASCII)
_VERSION = re.compile(r'[A-Za-z0-9][A-Za-z0-9._+-]{0,255}', re.ASCII)


def safe_atom(value, *, group=False):
    return (isinstance(value, str) and 1 <= len(value) <= 128
            and bool((_GROUP if group else _ATOM).fullmatch(value)))


def safe_version(value):
    return value if isinstance(value, str) and _VERSION.fullmatch(value) else None


def qualifiers(purl):
    """Restriction values stay private. Decode repository_url exactly once."""
    if '?' not in purl:
        return {}, None
    result = {}
    for part in purl.split('?', 1)[1].split('&'):
        if part.count('=') != 1:
            return {}, 'sbom_variant_unsupported'
        key, value = part.split('=', 1)
        if key not in ('type', 'classifier', 'repository_url') or key in result or not value:
            return {}, 'sbom_variant_unsupported'
        if key == 'repository_url':
            if re.search(r'%(?![0-9a-fA-F]{2})', value):
                return {}, 'sbom_variant_unsupported'
            try:
                value = unquote_to_bytes(value).decode('utf-8')
            except UnicodeError:
                return {}, 'sbom_variant_unsupported'
            if len(value) > 2048:
                return {}, 'sbom_variant_unsupported'
        elif not safe_atom(value):
            return {}, 'sbom_variant_unsupported'
        result[key] = value
    return result, None


def identify(record):
    group, name, version, purl = (record.get(key) for key in ('group', 'name', 'version', 'purl'))
    if group is None or name is None or purl is None:
        return None, 'sbom_identity_missing'
    if not safe_atom(group, group=True) or not safe_atom(name):
        return None, 'sbom_identity_unsupported'
    if (not isinstance(purl, str) or not purl.isascii() or len(purl) > 2048
            or not purl.startswith('pkg:maven/') or '#' in purl):
        return None, 'sbom_identity_unsupported'
    path = purl[len('pkg:maven/'):].split('?', 1)[0]
    if path.count('/') != 1 or path.count('@') > 1:
        return None, 'sbom_identity_unsupported'
    coordinates, separator, purl_version = path.partition('@')
    purl_group, purl_name = coordinates.split('/')
    if not safe_atom(purl_group, group=True) or not safe_atom(purl_name):
        return None, 'sbom_identity_unsupported'
    if (group, name) != (purl_group, purl_name):
        return None, 'sbom_identity_conflict'
    if version is None or not separator or not purl_version:
        return None, 'sbom_version_missing'
    if not isinstance(version, str):
        return None, 'sbom_version_unsupported'
    if version != purl_version:
        return None, 'sbom_identity_conflict'
    try:
        if is_snapshot(parse_version(version)):
            raise VersionError()
    except VersionError:
        return None, 'sbom_version_unsupported'
    values, reason = qualifiers(purl)
    if reason is not None:
        return None, reason
    kind = values.get('type', 'jar')
    if kind not in ('jar', 'pom', 'war'):
        return None, 'sbom_variant_unsupported'
    return SbomIdentity(group, name, version, kind, values.get('classifier')), None


def canonical_members(document):
    members = []
    grouped = {}
    for index, record in document.records:
        identity, reason = identify(record)
        version = safe_version(record.get('version'))
        if identity is not None and identity in grouped:
            position = grouped[identity]
            previous = members[position]
            members[position] = replace(previous, records=previous.records + ((index, record),))
        else:
            if identity is not None:
                grouped[identity] = len(members)
            members.append(SbomMember(index, identity, version, ((index, record),), reason))
    return tuple(members)
