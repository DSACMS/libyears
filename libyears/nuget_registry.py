"""Restricted NuGet metadata access; used only inside the supervised worker.

Admission checks bound work between operations. Absolute in-flight cancellation
belongs to the NuGet supervisor, not this client's socket timeout.
"""

import base64
import json
import math
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urlsplit

from .model import NuGetPublication
from .nuget_version import SelectedIdentity, parse_selected_identity
from .registry import TransportFailure, VerifiedJSONTransport

SERVICE_INDEX = 'https://api.nuget.org/v3/index.json'
REGISTRATION_BASE = 'https://api.nuget.org/v3/registration5-gz-semver2/'
MAX_WIRE_BYTES = 8 * 1024 * 1024
MAX_EXPANDED_BYTES = 32 * 1024 * 1024
MAX_PACKAGE_WIRE_BYTES = 64 * 1024 * 1024
MAX_PACKAGE_EXPANDED_BYTES = 128 * 1024 * 1024
MAX_JSON_DEPTH = 32
MAX_JSON_VALUES = 500_000
MAX_JSON_STRING = 1024 * 1024
MAX_PAGES = 256
MAX_VERSIONS = 100_000
MAX_PACKAGE_REQUESTS = 512
MAX_SCAN_REQUESTS = 4096
_PACKAGE_ID = re.compile(r'[a-z0-9][a-z0-9._-]{0,99}\Z')
_PATH_COMPONENT = re.compile(r'[A-Za-z0-9._+-]+\Z')


class NuGetRegistryFailure(ValueError):
    """Safe internal failure; never carries a URL, body or exception message."""

    def __init__(self, reason='invalid_registry_response', status=None):
        self.reason = reason
        self.status = status
        super().__init__(reason)


def validate_url(url, package_id, purpose='registration'):
    """Validate a link for its purpose before any transport or scheduling work."""
    if (not isinstance(url, str) or not url.isascii() or len(url) > 4096
            or any(ord(c) <= 32 or ord(c) >= 127 for c in url)
            or any(c in url for c in ('%', '\\', '?', '#'))):
        raise NuGetRegistryFailure()
    try:
        parsed = urlsplit(url)
    except ValueError:
        raise NuGetRegistryFailure() from None
    if parsed.scheme != 'https' or parsed.netloc != 'api.nuget.org':
        raise NuGetRegistryFailure()
    if purpose == 'index':
        valid = url == SERVICE_INDEX
    elif purpose == 'registration':
        prefix = '/v3/registration5-gz-semver2/' + package_id + '/'
        valid = bool(_PACKAGE_ID.fullmatch(package_id) and parsed.path.startswith(prefix))
        tail = parsed.path[len(prefix):] if valid else ''
        components = tail.split('/')
        valid = valid and _json_components(components)
    elif purpose == 'catalog':
        components = parsed.path.split('/')
        valid = (len(components) == 6 and components[:4] == ['', 'v3', 'catalog0', 'data']
                 and _json_components(components[4:]))
    else:
        valid = False
    if not valid:
        raise NuGetRegistryFailure()
    return url


def _json_components(components):
    return bool(components and components[-1].endswith('.json')
                and all(c not in ('.', '..') and _PATH_COMPONENT.fullmatch(c)
                        for c in components))


def sorted_urls(urls, package_id, purpose='registration'):
    """Validate every link before sorting; callers never issue a partial prefix."""
    result = [validate_url(url, package_id, purpose) for url in urls]
    if len(set(result)) != len(result):
        raise NuGetRegistryFailure()
    return sorted(result)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise NuGetRegistryFailure()
        result[key] = value
    return result


def _finite_float(text):
    result = float(text)
    if not math.isfinite(result):
        raise NuGetRegistryFailure()
    return result


def _invalid_constant(unused):
    raise NuGetRegistryFailure()


def decode_metadata(body):
    """Guard nesting, strings and value work before recursive JSON decoding."""
    try:
        text = body.decode('utf-8', errors='strict')
        index = depth = values = 0
        while index < len(text):
            char = text[index]
            if char in ' \t\r\n,:':
                index += 1
                continue
            if char == '"':
                value, index = json.decoder.scanstring(text, index + 1, True)
                if len(value) > MAX_JSON_STRING:
                    raise NuGetRegistryFailure()
                following = index
                while following < len(text) and text[following] in ' \t\r\n':
                    following += 1
                if following == len(text) or text[following] != ':':
                    values += 1
            elif char in '{[':
                depth += 1
                values += 1
                if depth > MAX_JSON_DEPTH:
                    raise NuGetRegistryFailure()
                index += 1
            elif char in '}]':
                depth -= 1
                index += 1
            else:
                while index < len(text) and text[index] not in ' \t\r\n,:[]{}':
                    index += 1
                values += 1
            if values > MAX_JSON_VALUES:
                raise NuGetRegistryFailure()
        return json.loads(text, object_pairs_hook=_pairs, parse_float=_finite_float,
                          parse_constant=_invalid_constant)
    except (UnicodeError, ValueError, RecursionError, OverflowError):
        raise NuGetRegistryFailure() from None


class NuGetMetadataClient:
    """One scan's counters, rate suppression and verified byte/JSON boundary."""

    def __init__(self, transport=None, clock=time.monotonic, wall_clock=time.time):
        self.transport = transport
        self.clock = clock
        self.wall_clock = wall_clock
        self.scan_deadline = None
        self.scan_requests = 0
        self.cooldown_until = 0.0
        self.package_id = None
        self.registration_ready = False
        self.registration_failure = None

    def begin_package(self, package_id, *, package_deadline=None, scan_deadline=None):
        if not isinstance(package_id, str) or not _PACKAGE_ID.fullmatch(package_id):
            raise NuGetRegistryFailure()
        now = self.clock()
        if self.scan_deadline is None:
            self.scan_deadline = min(now + 300, scan_deadline) if scan_deadline is not None else now + 300
        elif scan_deadline is not None:
            self.scan_deadline = min(self.scan_deadline, scan_deadline)
        self.package_deadline = min(now + 60, package_deadline) if package_deadline is not None else now + 60
        self.package_id = package_id
        self.package_requests = 0
        self.wire_bytes = self.expanded_bytes = 0
        self.pages = self.versions = 0
        self.failed = False

    def _fail(self, reason='invalid_registry_response', status=None):
        self.failed = True
        raise NuGetRegistryFailure(reason, status)

    def count_page(self, count=1):
        if type(count) is not int or count < 0:
            self._fail()
        self.pages += count
        if self.pages > MAX_PAGES:
            self._fail()

    def count_versions(self, count):
        if type(count) is not int or count < 0:
            self._fail()
        self.versions += count
        if self.versions > MAX_VERSIONS:
            self._fail()

    def _rate_limit(self, header):
        # Invalid/missing Retry-After suppresses this authority for the scan.
        delay = None
        if isinstance(header, str) and len(header) <= 128:
            if header.isascii() and header.isdecimal():
                delay = int(header)
            else:
                try:
                    date = parsedate_to_datetime(header)
                    if date.tzinfo is not None:
                        delay = max(0, date.timestamp() - self.wall_clock())
                except (ValueError, TypeError, OverflowError):
                    pass
        if delay is None or not math.isfinite(delay):
            self.cooldown_until = float('inf')
        else:
            self.cooldown_until = max(self.cooldown_until, self.clock() + delay)

    def get_json(self, url, *, purpose='registration'):
        validate_url(url, self.package_id or '', purpose)
        if self.package_id is None:
            raise NuGetRegistryFailure('registry_error')
        now = self.clock()
        remaining = min(self.package_deadline, self.scan_deadline) - now
        if (self.failed or remaining <= 0 or now < self.cooldown_until
                or self.package_requests >= MAX_PACKAGE_REQUESTS
                or self.scan_requests >= MAX_SCAN_REQUESTS):
            self._fail('registry_error')
        if self.transport is None:
            self.transport = VerifiedJSONTransport(
                max_response_bytes=MAX_WIRE_BYTES, allowed_authority='api.nuget.org',
                max_decompressed_bytes=MAX_EXPANDED_BYTES, retry_after_statuses=(429, 503))
        if isinstance(self.transport, VerifiedJSONTransport):
            self.transport.timeout = min(10.0, remaining)
        self.package_requests += 1
        self.scan_requests += 1
        try:
            body = self.transport.get(url)
        except Exception:
            self._fail('registry_error')
        if self.clock() >= min(self.package_deadline, self.scan_deadline):
            self._fail('registry_error')
        if isinstance(body, TransportFailure):
            if body.status in (429, 503):
                self._rate_limit(body.retry_after)
            reason = 'invalid_registry_response' if body.bounded_failure else 'registry_error'
            # Absence has resource-specific meaning in traversal. It does not
            # invalidate the connection or suppress other required catalog leaves.
            if body.status == 404 and not body.bounded_failure:
                raise NuGetRegistryFailure(reason, body.status)
            self._fail(reason, body.status)
        if not isinstance(body, bytes):
            self._fail()
        wire = getattr(body, 'wire_bytes', len(body))
        self.wire_bytes += wire
        self.expanded_bytes += len(body)
        if (wire > MAX_WIRE_BYTES or len(body) > MAX_EXPANDED_BYTES
                or self.wire_bytes > MAX_PACKAGE_WIRE_BYTES
                or self.expanded_bytes > MAX_PACKAGE_EXPANDED_BYTES):
            self._fail()
        try:
            return decode_metadata(body)
        except NuGetRegistryFailure:
            self._fail()


@dataclass(frozen=True)
class PublicVersion:
    identity: SelectedIdentity
    listed: bool
    catalog_url: str
    assertions: tuple[dict, ...]


def _object(value):
    if not isinstance(value, dict):
        raise NuGetRegistryFailure()
    return value


def _items(value):
    value = _object(value)
    items = value.get('items')
    count = value.get('count')
    if (not isinstance(items, list) or type(count) is not int
            or count != len(items)):
        raise NuGetRegistryFailure()
    return items


def _identity(value, package_id):
    value = _object(value)
    name = value.get('id')
    identity = parse_selected_identity(value.get('version'))
    if (not isinstance(name, str) or not name.isascii()
            or name.lower() != package_id or identity is None):
        raise NuGetRegistryFailure()
    if 'isPrerelease' in value:
        flag = value['isPrerelease']
        if type(flag) is not bool or flag != (identity.prerelease is not None):
            raise NuGetRegistryFailure()
    return identity


def _listed(value):
    flag = value.get('listed', True)
    if type(flag) is not bool:
        raise NuGetRegistryFailure()
    return flag


def _created(value):
    if not isinstance(value, str) or not re.fullmatch(
            r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}'
            r'(?:\.[0-9]{1,7})?(?:Z|[+-][0-9]{2}:[0-9]{2})', value):
        return None
    if not value.endswith('Z') and (int(value[-5:-3]) > 23 or int(value[-2:]) > 59):
        return None
    try:
        # fromisoformat consistently truncates the seventh fractional digit.
        date = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if date.year == 1900:
            return None
        date = date.astimezone(timezone.utc)
        return date if date.year != 1900 else None
    except (ValueError, OverflowError):
        return None


def _hash(value):
    if value.get('packageHashAlgorithm') != 'SHA512':
        return None
    text = value.get('packageHash')
    if not isinstance(text, str) or len(text) > 128:
        return None
    try:
        digest = base64.b64decode(text, validate=True)
    except (ValueError, UnicodeError):
        return None
    return digest if len(digest) == 64 else None


def _service_index(client):
    if client.registration_ready:
        return
    if client.registration_failure is not None:
        raise NuGetRegistryFailure(client.registration_failure)
    try:
        _discover_registration(client)
    except NuGetRegistryFailure as failure:
        client.registration_failure = failure.reason
        raise
    client.registration_ready = True


def _discover_registration(client):
    value = _object(client.get_json(SERVICE_INDEX, purpose='index'))
    resources = value.get('resources')
    if not isinstance(resources, list):
        raise NuGetRegistryFailure()
    selected = []
    for resource in resources:
        resource = _object(resource)
        if resource.get('@type') == 'RegistrationsBaseUrl/3.6.0':
            selected.append(resource.get('@id'))
    if not selected or any(url != REGISTRATION_BASE for url in selected):
        raise NuGetRegistryFailure()


def _page_url(page, package_id):
    url = page.get('@id')
    if isinstance(url, str) and '#' in url and 'items' in page:
        # nuget.org names inline pages with fragments. They are identifiers,
        # never request destinations; only this exact bounded shape is accepted.
        prefix = REGISTRATION_BASE + package_id + '/index.json#page/'
        if not url.startswith(prefix) or len(url) > 4096:
            raise NuGetRegistryFailure()
        parts = url[len(prefix):].split('/')
        if (len(parts) != 2 or parts != [page.get('lower'), page.get('upper')]
                or any(parse_selected_identity(part) is None for part in parts)):
            raise NuGetRegistryFailure()
        return url
    return validate_url(url, package_id)


def _bound(page, key):
    identity = parse_selected_identity(page.get(key))
    if identity is None:
        raise NuGetRegistryFailure()
    return identity


def _core_bound(identity):
    # Prereleases precede their stable core. Their mutual order is unnecessary
    # for stable selection and deliberately remains uninterpreted.
    return identity.components, identity.prerelease is None


def _registration(client, package_id):
    index_url = REGISTRATION_BASE + package_id + '/index.json'
    try:
        index = client.get_json(index_url)
    except NuGetRegistryFailure as failure:
        if failure.status == 404 and failure.reason == 'registry_error':
            raise NuGetRegistryFailure('package_not_found') from None
        raise
    if '@id' in _object(index) and index['@id'] != index_url:
        raise NuGetRegistryFailure()
    pages = _items(index)
    client.count_page(len(pages))
    descriptors = {}
    for page in pages:
        page = _object(page)
        url = _page_url(page, package_id)
        if url in descriptors or type(page.get('count')) is not int or page['count'] < 1:
            raise NuGetRegistryFailure()
        _bound(page, 'lower')
        _bound(page, 'upper')
        descriptors[url] = page
    versions = []
    registration_urls = set()
    ranges = []
    for url in sorted(descriptors):
        descriptor = descriptors[url]
        page = descriptor
        if 'items' not in page:
            try:
                page = _object(client.get_json(url))
            except NuGetRegistryFailure as failure:
                if failure.status == 404:
                    raise NuGetRegistryFailure() from None
                raise
            if page.get('@id') != url:
                raise NuGetRegistryFailure()
            if any(page.get(key) != descriptor.get(key) for key in ('count', 'lower', 'upper')):
                raise NuGetRegistryFailure()
        if 'parent' in page and page['parent'] != index_url:
            raise NuGetRegistryFailure()
        lower, upper = _bound(page, 'lower'), _bound(page, 'upper')
        if _core_bound(lower) > _core_bound(upper):
            raise NuGetRegistryFailure()
        entries = _items(page)
        client.count_versions(len(entries))
        page_identities = set()
        for leaf in entries:
            leaf = _object(leaf)
            leaf_url = validate_url(leaf.get('@id'), package_id)
            if leaf_url in registration_urls:
                raise NuGetRegistryFailure()
            registration_urls.add(leaf_url)
            entry = _object(leaf.get('catalogEntry'))
            identity = _identity(entry, package_id)
            if not _core_bound(lower) <= _core_bound(identity) <= _core_bound(upper):
                raise NuGetRegistryFailure()
            page_identities.add(identity.normalized_version)
            listed = _listed(entry)
            if 'listed' in leaf and _listed(leaf) != listed:
                raise NuGetRegistryFailure()
            if 'isPrerelease' in leaf:
                _identity(dict(leaf, id=package_id, version=identity.normalized_version), package_id)
            catalog_url = validate_url(entry.get('@id'), package_id, 'catalog')
            versions.append(PublicVersion(identity, listed, catalog_url, (entry, leaf)))
        if lower.normalized_version not in page_identities or upper.normalized_version not in page_identities:
            raise NuGetRegistryFailure()
        ranges.append((lower.components, upper.components))
    # Numeric overlap is decidable without introducing prerelease ordering.
    # Equal numeric boundaries can split prereleases sharing a numeric core.
    ranges.sort(key=lambda item: (item[0], item[1]))
    for earlier, later in zip(ranges, ranges[1:]):
        if earlier[1] > later[0]:
            raise NuGetRegistryFailure()
    grouped = {}
    for version in versions:
        grouped.setdefault(version.identity.normalized_version, []).append(version)
    for aliases in grouped.values():
        if len({alias.listed for alias in aliases}) != 1:
            raise NuGetRegistryFailure()
    return grouped


def _catalog(client, record):
    try:
        value = client.get_json(record.catalog_url, purpose='catalog')
    except NuGetRegistryFailure as failure:
        if failure.status == 404 and failure.reason == 'registry_error':
            return None
        raise
    value = _object(value)
    identity = _identity(value, client.package_id)
    kinds = value.get('@type')
    if isinstance(kinds, str):
        kinds = [kinds]
    if (not isinstance(kinds, list) or not all(isinstance(kind, str) for kind in kinds)
            or not any(kind in ('PackageDetails', 'nuget:PackageDetails') for kind in kinds)
            or any(kind in ('PackageDelete', 'nuget:PackageDelete') for kind in kinds)
            or identity.normalized_version != record.identity.normalized_version
            or ('@id' in value and value['@id'] != record.catalog_url)):
        raise NuGetRegistryFailure()
    if 'listed' in value and _listed(value) != record.listed:
        raise NuGetRegistryFailure()
    return value


def _reconcile_material(records, documents):
    hashes, dates = set(), set()
    alias_material = set()
    for record in records:
        document = documents[record.catalog_url]
        if document is None:
            if len(records) > 1:
                raise NuGetRegistryFailure()
            continue
        digest = _hash(document)
        created = _created(document.get('created'))
        # Unavailable values cannot establish agreement between aliases.
        # Single records retain their later hash/date-specific failure reasons.
        if len(records) > 1 and (digest is None or created is None):
            raise NuGetRegistryFailure()
        alias_material.add((digest, created))
        for assertion in (*record.assertions, document):
            if 'created' in assertion:
                dates.add(_created(assertion['created']))
            if 'packageHash' in assertion or 'packageHashAlgorithm' in assertion:
                hashes.add(_hash(assertion))
    if len(hashes) > 1 or len(dates) > 1 or len(alias_material) > 1:
        raise NuGetRegistryFailure()


def lookup_authorized_package(authority, client):
    """Worker-only handler: complete enumeration before any measurement claim."""
    from .nuget_supervisor import PackageResult, authority_message
    authority_message(authority)
    if client.package_id != authority.package_key:
        raise NuGetRegistryFailure()
    _service_index(client)
    grouped = _registration(client, authority.package_key)
    used = grouped.get(authority.normalized_version)
    if used is None:
        return PackageResult(reason='version_not_found')
    stable = [key for key, aliases in grouped.items()
              if aliases[0].listed and aliases[0].identity.prerelease is None]
    latest_key = max(stable, key=lambda key: grouped[key][0].identity.components) if stable else None
    needed = set((authority.normalized_version,))
    if latest_key is not None:
        needed.add(latest_key)
    needed.update(key for key, aliases in grouped.items() if len(aliases) > 1)
    by_url = {}
    for key in sorted(needed):
        for record in grouped[key]:
            previous = by_url.get(record.catalog_url)
            if previous and previous.identity.normalized_version != key:
                raise NuGetRegistryFailure()
            by_url[record.catalog_url] = record
    documents = {url: _catalog(client, by_url[url]) for url in sorted(by_url)}
    if any(documents[record.catalog_url] is None for record in used):
        return PackageResult(reason='version_not_found')
    for key in sorted(needed):
        _reconcile_material(grouped[key], documents)
    # Catalog hash authority cannot be supplied by a registration assertion.
    hashes = [_hash(documents[record.catalog_url]) for record in used]
    if any(digest is None for digest in hashes):
        return PackageResult(reason='content_hash_unavailable', content_hash_state='unavailable')
    if any(digest != authority.content_hash for digest in hashes):
        return PackageResult(reason='content_hash_mismatch', content_hash_state='mismatch')
    verified = dict(origin_state='public_content_verified', content_hash_state='public_agreement')
    used_dates = [_created(documents[record.catalog_url].get('created')) for record in used]
    if any(date is None for date in used_dates):
        return PackageResult(reason='release_date_missing', **verified)
    used_publication = NuGetPublication(authority.normalized_version, used_dates[0], used[0].listed)
    verified['used_publication'] = used_publication
    if latest_key is None:
        return PackageResult(reason='no_stable_release', **verified)
    latest = grouped[latest_key]
    latest_dates = [_created(documents[record.catalog_url].get('created'))
                    if documents[record.catalog_url] is not None else None for record in latest]
    if any(date is None for date in latest_dates):
        return PackageResult(reason='release_date_missing', **verified)
    return PackageResult(latest_publication=NuGetPublication(latest_key, latest_dates[0], True), **verified)


class NuGetRegistryAdapter:
    """Parent-side scan lifetime; all production lookup work is supervised."""

    def __init__(self, supervisor=None):
        if supervisor is None:
            from .nuget_supervisor import NuGetSupervisor
            supervisor = NuGetSupervisor()
        self.supervisor = supervisor

    def lookup_all(self, authorities):
        from .nuget_supervisor import authority_message
        authorities = list(authorities)
        for authority in authorities:
            authority_message(authority)
        authorities.sort(key=lambda item: (item.package_key, item.normalized_version))
        try:
            return tuple((authority, self.supervisor.lookup(authority)) for authority in authorities)
        finally:
            self.supervisor.close()
