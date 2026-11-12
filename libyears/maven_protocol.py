"""Closed bounded atomic-file protocol for the trusted Maven metadata worker."""

from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import stat

from .maven_model import MavenReason
from .maven_registry import catalogue_path, pom_path
from .maven_version import eligibility, parse_version

LIMIT = 16 * 1024
MAX_ATTEMPTS = 300
MAX_BYTES = 64 * 1024 * 1024
OPERATIONS = frozenset({'select_target', 'pom_date'})
REASONS = frozenset({
    MavenReason.CATALOGUE_UNAVAILABLE, MavenReason.UNKNOWN_LATEST_ELIGIBILITY,
    MavenReason.AMBIGUOUS_LATEST_VERSION, MavenReason.NO_STABLE_RELEASE,
    MavenReason.TIME_BASIS_UNAVAILABLE, MavenReason.METADATA_BUDGET_EXCEEDED,
    MavenReason.METADATA_WORKER_UNAVAILABLE,
})


def available():
    return bool(getattr(os, 'O_NOFOLLOW', 0) and getattr(os, 'O_NONBLOCK', 0))


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Maven protocol')
        result[key] = value
    return result


def _constant(value):
    raise ValueError('Maven protocol')


def write_message(path, value):
    body = json.dumps(value, allow_nan=False, separators=(',', ':')).encode('utf-8')
    if len(body) > LIMIT:
        raise ValueError('Maven protocol')
    temporary = Path(str(path) + '.tmp')
    with temporary.open('xb') as stream:
        stream.write(body)
    os.replace(temporary, path)


def read_message(path):
    if not available():
        raise ValueError('Maven protocol')
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > LIMIT:
        raise ValueError('Maven protocol')
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        if (not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino, opened.st_size) != (info.st_dev, info.st_ino, info.st_size)):
            raise ValueError('Maven protocol')
        body = stream.read(LIMIT + 1)
    if len(body) > LIMIT:
        raise ValueError('Maven protocol')
    value = json.loads(body, object_pairs_hook=_pairs, parse_constant=_constant)
    if type(value) is not dict:
        raise ValueError('Maven protocol')
    return value


def command(value):
    if type(value) is not dict or set(value) != {'sequence', 'operation', 'group_id', 'artifact_id', 'version', 'deadline'}:
        raise ValueError('Maven protocol')
    if type(value['sequence']) is not int or not 1 <= value['sequence'] <= MAX_ATTEMPTS:
        raise ValueError('Maven protocol')
    if not isinstance(value['operation'], str) or value['operation'] not in OPERATIONS:
        raise ValueError('Maven protocol')
    deadline = value['deadline']
    if type(deadline) not in (int, float) or not math.isfinite(deadline):
        raise ValueError('Maven protocol')
    if value['operation'] == 'select_target':
        if value['version'] is not None:
            raise ValueError('Maven protocol')
        catalogue_path(value['group_id'], value['artifact_id'])
    else:
        pom_path(value['group_id'], value['artifact_id'], value['version'])
    return value


def timestamp(text):
    if not isinstance(text, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z', text):
        raise ValueError('Maven protocol')
    return datetime.fromisoformat(text[:-1] + '+00:00')


def date_text(value):
    return value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def result(value, request):
    fields = {'sequence', 'operation', 'group_id', 'artifact_id', 'version', 'selected_version',
              'last_modified', 'retrieved_at', 'reason', 'attempts', 'body_bytes',
              'ordering_basis', 'eligibility_policy', 'time_basis'}
    if type(value) is not dict or set(value) != fields:
        raise ValueError('Maven protocol')
    for key in ('sequence', 'operation', 'group_id', 'artifact_id', 'version'):
        if type(value[key]) is not type(request[key]) or value[key] != request[key]:
            raise ValueError('Maven protocol')
    if (type(value['attempts']) is not int or not 0 <= value['attempts'] <= MAX_ATTEMPTS
            or type(value['body_bytes']) is not int or not 0 <= value['body_bytes'] <= MAX_BYTES):
        raise ValueError('Maven protocol')
    retrieved = timestamp(value['retrieved_at'])
    reason = value['reason']
    if reason is not None and (not isinstance(reason, str) or reason not in REASONS):
        raise ValueError('Maven protocol')
    if request['operation'] == 'select_target':
        if (value['ordering_basis'] != 'maven_comparable_version_3_9_11'
                or value['eligibility_policy'] != 'maven_conservative_stable_v1'
                or value['time_basis'] is not None or value['last_modified'] is not None):
            raise ValueError('Maven protocol')
        selected = value['selected_version']
        if reason is None:
            if eligibility(parse_version(selected)) != 'eligible':
                raise ValueError('Maven protocol')
        elif selected is not None or reason == MavenReason.TIME_BASIS_UNAVAILABLE:
            raise ValueError('Maven protocol')
    else:
        if (value['selected_version'] is not None or value['ordering_basis'] is not None
                or value['eligibility_policy'] is not None
                or value['time_basis'] != 'maven_conventional_pom_last_modified'):
            raise ValueError('Maven protocol')
        if reason is None:
            modified = timestamp(value['last_modified'])
            if modified.microsecond or modified > retrieved:
                raise ValueError('Maven protocol')
        elif value['last_modified'] is not None or reason not in {
                MavenReason.TIME_BASIS_UNAVAILABLE, MavenReason.METADATA_BUDGET_EXCEEDED,
                MavenReason.METADATA_WORKER_UNAVAILABLE}:
            raise ValueError('Maven protocol')
    return value
