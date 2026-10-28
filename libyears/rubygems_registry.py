"""Bounded public RubyGems metadata; no repository or resolver access."""

from dataclasses import dataclass
from datetime import date, datetime, timezone
import json
import re
from urllib.parse import quote

from .model import RegistryFailure, RegistryResult, RubyGemsEvidence, RubyPublicationArtifact
from .registry import TransportFailure, VerifiedJSONTransport


MAX_RESPONSE_BYTES = 16 * 1024 * 1024
_NAME = re.compile(r'[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?\Z')
_VERSION = re.compile(r'[0-9]+(?:\.[A-Za-z0-9]+)*\Z')
_PLATFORM = re.compile(r'[A-Za-z0-9_.-]+\Z')
_ABI = re.compile(r'[0-9]+\.[0-9]+\Z')


@dataclass(frozen=True, slots=True)
class RubyArtifactRecord:
    """Validated ordinary artifact from the observable published population."""

    version: str
    platform: str
    publication_time: datetime | None
    prerelease: bool
    available: bool
    yanked: bool | None = None


def _supported_name(value):
    return (isinstance(value, str) and _NAME.fullmatch(value) is not None
            and re.search(r'[A-Za-z]', value) is not None)


def _same_name(value, expected):
    # Both operands are bounded ASCII, so lower() changes only ASCII case.
    return _supported_name(value) and value.lower() == expected.lower()


def _metadata_text(value):
    """Compare JSON values without Python's bool/int equality coercion."""
    return json.dumps(value, sort_keys=True, ensure_ascii=True)


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result and _metadata_text(result[key]) != _metadata_text(value):
            raise ValueError('conflicting JSON keys')
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError('non-JSON constant')


def _decode(body):
    return json.loads(body.decode('utf-8'), object_pairs_hook=_object,
                      parse_constant=_reject_constant)


def _timestamp(value):
    if not isinstance(value, str):
        return None
    try:
        timestamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            return None
        return timestamp.astimezone(timezone.utc)
    except (ValueError, OverflowError):
        return None


def _creation_time(row):
    created = _timestamp(row.get('created_at'))
    equivalent = _timestamp(row.get('version_created_at'))
    if 'created_at' in row and 'version_created_at' in row:
        if created != equivalent:
            raise ValueError('conflicting publication times')
    return created if 'created_at' in row else equivalent


def _population(payload, name):
    if not isinstance(payload, list):
        raise ValueError('expected artifact array')
    seen = {}
    records = []
    for row in payload:
        if not isinstance(row, dict):
            raise ValueError('expected artifact object')
        if 'name' in row and not _same_name(row['name'], name):
            raise ValueError('artifact identity mismatch')
        version = row.get('number')
        platform = row.get('platform')
        if not isinstance(version, str) or not _VERSION.fullmatch(version):
            raise ValueError('unclassifiable version')
        if not isinstance(platform, str) or not _PLATFORM.fullmatch(platform):
            raise ValueError('unclassifiable platform')
        if 'ruby_abi' not in row:
            raise ValueError('missing ABI classification')
        abi = row['ruby_abi']
        if abi is not None and (not isinstance(abi, str) or not _ABI.fullmatch(abi)):
            raise ValueError('unclassifiable ABI')
        if type(row.get('prerelease')) is not bool:
            raise ValueError('missing prerelease classification')
        # This endpoint contains published/indexed records, not yank history.
        if 'yanked' in row and row['yanked'] is not False:
            raise ValueError('contradictory published availability')
        key = (version, platform, abi)
        if key in seen:
            if seen[key] != _metadata_text(row):
                raise ValueError('conflicting artifact records')
            continue
        seen[key] = _metadata_text(row)
        timestamp = _creation_time(row)
        if abi is None:
            records.append(RubyArtifactRecord(
                version, platform, timestamp, row['prerelease'], True, row.get('yanked'),
            ))
    return tuple(records)


@dataclass(frozen=True, slots=True)
class CanonicalPublication:
    """One version date and every admissible supported contributor."""

    publication_time: datetime
    artifacts: tuple[RubyPublicationArtifact, ...]


def canonical_publication(records: tuple[RubyArtifactRecord, ...]) -> CanonicalPublication | None:
    """Use earliest admissible observable creation, including known yanked rows."""
    artifacts = []
    for record in records:
        timestamp = record.publication_time
        if timestamp is None or timestamp.tzinfo is None or timestamp.utcoffset() is None:
            continue
        timestamp = timestamp.astimezone(timezone.utc)
        if timestamp.date() == date(2009, 7, 25):
            continue
        artifacts.append(RubyPublicationArtifact(
            record.version, record.platform, timestamp, record.yanked,
        ))
    if not artifacts:
        return None
    artifacts.sort(key=lambda artifact: (
        artifact.version, artifact.platform, artifact.publication_time,
    ))
    return CanonicalPublication(
        min(artifact.publication_time for artifact in artifacts), tuple(artifacts),
    )


def _resolve_population(name, used_version, records):
    """Select package versions using one shared canonical result per version."""
    versions = {}
    for record in records:
        versions.setdefault(record.version, []).append(record)
    # Classification is a version property even across distinct platforms.
    for group in versions.values():
        if len({record.prerelease for record in group}) != 1:
            return RegistryFailure(name, used_version, 'invalid_registry_response',
                                   'contradictory prerelease classification')
    if used_version not in versions:
        return RegistryFailure(name, used_version, 'version_not_found',
                               'used version not publicly observable in supported artifacts')
    publications = {
        version: canonical_publication(tuple(group)) for version, group in versions.items()
    }
    used = publications[used_version]
    if used is None:
        return RegistryFailure(name, used_version, 'release_date_missing',
                               'no admissible observable used publication date')
    evidence = RubyGemsEvidence((), used.artifacts)
    eligible = []
    for version, group in versions.items():
        publication = publications[version]
        if publication is not None and any(
            record.available and not record.prerelease and record.yanked is not True
            for record in group
        ):
            eligible.append(version)
    if not eligible:
        return RegistryFailure(name, used_version, 'no_stable_release',
                               'no supported available stable publication', evidence)
    # Sort lexical ties first; max() retains that first version on equal dates.
    latest_version = max(sorted(eligible), key=lambda version: publications[version].publication_time)
    latest = publications[latest_version]
    return RegistryResult(
        name, used_version, used.publication_time, latest_version, latest.publication_time,
        RubyGemsEvidence((), used.artifacts, latest.artifacts),
    )


class RubyGemsAdapter:
    """Fetch independent identity then complete bounded public population."""

    def __init__(self, *, timeout=10.0, user_agent='libyears/0.1', ca_bundle=None):
        self.transport = VerifiedJSONTransport(
            timeout=timeout, user_agent=user_agent, ca_bundle=ca_bundle,
            max_response_bytes=MAX_RESPONSE_BYTES, allowed_authority='rubygems.org',
        )
        self.timeout = self.transport.timeout
        self.user_agent = self.transport.user_agent
        self.ssl_context = self.transport.ssl_context
        self.tls_trust = self.transport.tls_trust

    def fetch_population(self, name, used_version):
        """Admit only complete validated evidence, or return a safe failure."""
        def failure(reason, message):
            return RegistryFailure(name, used_version, reason, message)

        if (not _supported_name(name) or not isinstance(used_version, str)
                or not _VERSION.fullmatch(used_version)):
            return failure('invalid_registry_response', 'unsupported registry identity')
        registry_name = name
        total_bytes = 0
        for endpoint in ('gems', 'versions'):
            url = f'https://rubygems.org/api/v1/{endpoint}/{quote(registry_name, safe="")}.json'
            body = self.transport.get(url)
            if isinstance(body, TransportFailure):
                if body.bounded_failure in ('response_too_large', 'incomplete_response'):
                    return failure('invalid_registry_response', 'incomplete or oversized metadata')
                if body.status == 404:
                    return failure('package_not_found', 'package not publicly observable')
                return failure('registry_error', body.diagnostic)
            if not isinstance(body, bytes):
                return failure('invalid_registry_response', 'invalid metadata bytes')
            total_bytes += len(body)
            if len(body) > MAX_RESPONSE_BYTES or total_bytes > 2 * MAX_RESPONSE_BYTES:
                return failure('invalid_registry_response', 'oversized metadata')
            try:
                payload = _decode(body)
                if endpoint == 'gems':
                    if not isinstance(payload, dict) or not _same_name(payload.get('name'), name):
                        raise ValueError('package identity mismatch')
                    registry_name = payload['name']
                else:
                    return _population(payload, registry_name)
            except (ValueError, TypeError, UnicodeError, RecursionError):
                return failure('invalid_registry_response', 'invalid registry metadata')

    def lookup(self, name: str, used_version: str) -> RegistryResult | RegistryFailure:
        """Resolve used/latest timestamps solely from admitted public evidence."""
        records = self.fetch_population(name, used_version)
        if isinstance(records, RegistryFailure):
            return records
        return _resolve_population(name, used_version, records)
