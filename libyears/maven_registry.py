"""Pure whole-representation Maven metadata parsers; no transport or fallback.

Only admitted GA/version identities construct paths. POM modification timestamps
are conventional representation facts, never publication or acquisition events.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re
from urllib.parse import quote

from .maven_input import MavenInputFailure, POM_NAMESPACE, parse_xml
from .maven_model import MavenReason
from .maven_version import VersionError, is_snapshot, parse_version, select_latest

MAX_CATALOGUE_BYTES = 2 * 1024 * 1024
MAX_POM_BYTES = 1024 * 1024
MAX_VERSIONS = 10_000
METADATA_NAMESPACE = 'http://maven.apache.org/METADATA/1.1.0'
_GROUP = re.compile(r'[A-Za-z0-9_][A-Za-z0-9_-]*(?:\.[A-Za-z0-9_][A-Za-z0-9_-]*)*', re.ASCII)
_ARTIFACT = re.compile(r'[A-Za-z0-9_][A-Za-z0-9_.-]*', re.ASCII)
_HTTP_DATE = re.compile(
    r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun), ([0-9]{2}) '
    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) '
    r'([0-9]{4}) ([0-9]{2}):([0-9]{2}):([0-9]{2}) GMT', re.ASCII,
)
_WEEKDAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
_MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')


class RegistryFailure(ValueError):
    def __init__(self, reason=MavenReason.CATALOGUE_UNAVAILABLE):
        self.reason = reason
        super().__init__(reason.value)


@dataclass(frozen=True, slots=True)
class MavenRepresentation:
    status: int
    body: bytes
    headers: tuple[tuple[str, str], ...]
    retrieved_at: datetime


@dataclass(frozen=True, slots=True)
class MavenTarget:
    group_id: str
    artifact_id: str
    version: str | None
    retrieved_at: datetime
    reason: MavenReason | None = None
    ordering_basis: str = field(init=False, default='maven_comparable_version_3_9_11')
    eligibility_policy: str = field(init=False, default='maven_conservative_stable_v1')


@dataclass(frozen=True, slots=True)
class MavenPomDate:
    group_id: str
    artifact_id: str
    version: str
    last_modified: datetime | None
    retrieved_at: datetime
    reason: MavenReason | None = None
    time_basis: str = field(init=False, default='maven_conventional_pom_last_modified')


def _ga(group_id, artifact_id):
    if (not isinstance(group_id, str) or not 1 <= len(group_id) <= 128
            or not _GROUP.fullmatch(group_id) or not isinstance(artifact_id, str)
            or not 1 <= len(artifact_id) <= 128 or not _ARTIFACT.fullmatch(artifact_id)):
        raise RegistryFailure()


def _exact(version):
    try:
        parsed = parse_version(version)
        if is_snapshot(parsed):
            raise VersionError()
    except VersionError:
        raise RegistryFailure() from None


def catalogue_path(group_id, artifact_id):
    _ga(group_id, artifact_id)
    return '/maven2/' + group_id.replace('.', '/') + '/' + quote(artifact_id, safe='') + '/maven-metadata.xml'


def pom_path(group_id, artifact_id, version):
    _ga(group_id, artifact_id)
    _exact(version)
    artifact = quote(artifact_id, safe='')
    exact = quote(version, safe='')
    return ('/maven2/' + group_id.replace('.', '/') + '/' + artifact + '/' + exact
            + '/' + artifact + '-' + exact + '.pom')


def _utc(value):
    if not isinstance(value, datetime) or value.utcoffset() is None:
        raise RegistryFailure()
    return value.astimezone(timezone.utc)


def _body(response, limit):
    if type(response.status) is not int or response.status != 200:
        raise RegistryFailure()
    if type(response.body) is not bytes:
        raise RegistryFailure()
    if len(response.body) > limit:
        raise RegistryFailure(MavenReason.METADATA_BUDGET_EXCEEDED)
    return parse_xml(response.body, max_bytes=limit)


def _root(node, name, namespaces):
    if node.name != name or node.namespace not in namespaces:
        raise RegistryFailure()
    allowed = {'http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
               'http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation'}
    if any(key not in allowed for key, value in node.attributes):
        raise RegistryFailure()
    if node.text.strip():
        raise RegistryFailure()


def _one(node, name, *, required=False):
    entries = node.elements(name)
    if len(entries) > 1 or (required and not entries):
        raise RegistryFailure()
    if not entries:
        return None
    if entries[0].text.strip():
        raise RegistryFailure()
    return entries[0]


def _fields(node, names):
    if node.text.strip() or any(child.name not in names or child.namespace != node.namespace
                                or child.attributes for child in node.children):
        raise RegistryFailure()


def _scalar(node, name):
    # Remote identity text is exact evidence, never a normalization opportunity.
    return node.scalar(name)


def select_target(group_id, artifact_id, response):
    """Select the complete current catalogue's maximum before consulting any date."""
    _ga(group_id, artifact_id)
    retrieved = _utc(response.retrieved_at)
    try:
        root = _body(response, MAX_CATALOGUE_BYTES)
        _root(root, 'metadata', (None, METADATA_NAMESPACE))
        _fields(root, {'groupId', 'artifactId', 'version', 'versioning'})
        if _scalar(root, 'groupId') != group_id or _scalar(root, 'artifactId') != artifact_id:
            raise RegistryFailure()
        _scalar(root, 'version')  # irrelevant optional singleton, never the maximum
        versioning = _one(root, 'versioning', required=True)
        _fields(versioning, {'latest', 'release', 'lastUpdated', 'versions'})
        for name in ('latest', 'release', 'lastUpdated'):
            _scalar(versioning, name)  # validate framing, never use as evidence
        versions = _one(versioning, 'versions', required=True)
        _fields(versions, {'version'})
        if len(versions.children) > MAX_VERSIONS:
            raise RegistryFailure(MavenReason.METADATA_BUDGET_EXCEEDED)
        candidates = []
        for entry in versions.children:
            if entry.children:
                raise RegistryFailure()
            candidates.append(entry.text)
        selected = select_latest(candidates)
        reason = MavenReason(selected.reason) if selected.reason is not None else None
        return MavenTarget(group_id, artifact_id, selected.version, retrieved, reason)
    except MavenInputFailure as failure:
        reason = (MavenReason.METADATA_BUDGET_EXCEEDED if failure.issue.value == 'budget_exceeded'
                  else MavenReason.CATALOGUE_UNAVAILABLE)
    except RegistryFailure as failure:
        reason = failure.reason
    return MavenTarget(group_id, artifact_id, None, retrieved, reason)


def last_modified(headers, retrieved_at):
    """Strict IMF-fixdate, unique even for identical duplicate header values."""
    retrieved = _utc(retrieved_at)
    if type(headers) is not tuple:
        raise RegistryFailure(MavenReason.TIME_BASIS_UNAVAILABLE)
    values = []
    for header in headers:
        if (type(header) is not tuple or len(header) != 2
                or not all(isinstance(value, str) for value in header)):
            raise RegistryFailure(MavenReason.TIME_BASIS_UNAVAILABLE)
        name, value = header
        if name.lower() == 'last-modified':
            values.append(value)
    if len(values) != 1:
        raise RegistryFailure(MavenReason.TIME_BASIS_UNAVAILABLE)
    match = _HTTP_DATE.fullmatch(values[0])
    if match is None:
        raise RegistryFailure(MavenReason.TIME_BASIS_UNAVAILABLE)
    weekday, day, month, year, hour, minute, second = match.groups()
    try:
        timestamp = datetime(int(year), _MONTHS.index(month) + 1, int(day), int(hour),
                             int(minute), int(second), tzinfo=timezone.utc)
    except ValueError:
        raise RegistryFailure(MavenReason.TIME_BASIS_UNAVAILABLE) from None
    if _WEEKDAYS[timestamp.weekday()] != weekday or timestamp > retrieved:
        raise RegistryFailure(MavenReason.TIME_BASIS_UNAVAILABLE)
    return timestamp


def pom_date(group_id, artifact_id, version, response):
    """Associate only this versioned POM; never follow its parent/BOM/dependencies."""
    _ga(group_id, artifact_id)
    _exact(version)
    retrieved = _utc(response.retrieved_at)
    try:
        root = _body(response, MAX_POM_BYTES)
        _root(root, 'project', (None, POM_NAMESPACE))
        if _scalar(root, 'artifactId') != artifact_id:
            raise RegistryFailure()
        actual_group = _scalar(root, 'groupId')
        actual_version = _scalar(root, 'version')
        if actual_group is None or actual_version is None:
            parent = _one(root, 'parent', required=True)
            if actual_group is None:
                actual_group = _scalar(parent, 'groupId')
            if actual_version is None:
                actual_version = _scalar(parent, 'version')
        if actual_group != group_id or actual_version != version:
            raise RegistryFailure()
        distribution = _one(root, 'distributionManagement')
        if distribution is not None and distribution.elements('relocation'):
            raise RegistryFailure()
        timestamp = last_modified(response.headers, retrieved)
        return MavenPomDate(group_id, artifact_id, version, timestamp, retrieved)
    except (MavenInputFailure, RegistryFailure):
        return MavenPomDate(group_id, artifact_id, version, None, retrieved,
                            MavenReason.TIME_BASIS_UNAVAILABLE)
