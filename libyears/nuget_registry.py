"""Restricted NuGet metadata access; used only inside the supervised worker.

Admission checks bound work between operations. Absolute in-flight cancellation
belongs to the NuGet supervisor, not this client's socket timeout.
"""

import json
import math
import re
import time
from email.utils import parsedate_to_datetime
from urllib.parse import urlsplit

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
