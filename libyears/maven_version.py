"""Bounded Maven 3.9.11 precedence, separate from libyears eligibility.

Derived from Apache Maven ComparableVersion and ArtifactUtils (Apache-2.0).
ComparableVersion authors: Kenney Westerhof and Hervé Boutemy; ASF contributors.
Changed for Python: immutable items, finite ASCII/input budgets, no Java numeric
storage limits, and a separate libyears selection policy. See
third_party/maven-3.9.11/README.md, LICENSE and NOTICE for provenance/attribution.
"""

from dataclasses import dataclass
import re


ORDERING_BASIS = "maven_comparable_version_3_9_11"
ELIGIBILITY_POLICY = "maven_conservative_stable_v1"
_EXACT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,255}", re.ASCII)
_STABLE = re.compile(
    r"[0-9]+(?:[.-][0-9]+)*(?:[.-]?(?:ga|final|release|sp)[0-9]*)?",
    re.ASCII | re.IGNORECASE,
)
_TIMESTAMP = re.compile(r".*-[0-9]{8}\.[0-9]{6}-[0-9]+", re.ASCII)
_QUALIFIERS = ("alpha", "beta", "milestone", "rc", "snapshot", "", "sp")
_ALIASES = {"ga": "", "final": "", "release": "", "cr": "rc"}
_PRERELEASE = frozenset(("alpha", "beta", "milestone", "rc"))


class VersionError(ValueError):
    """A closed refusal reason; never includes untrusted version text."""

    def __init__(self, reason="maven_catalogue_unavailable"):
        self.reason = reason
        super().__init__(reason)


@dataclass(frozen=True)
class _Number:
    value: int
    storage_rank: int


@dataclass(frozen=True)
class _String:
    value: str


@dataclass(frozen=True)
class _List:
    items: tuple


def _qualifier_key(value):
    if value in _QUALIFIERS:
        return str(_QUALIFIERS.index(value))
    return "7-" + value


def _compare(left, right):
    """Pinned item comparison, including missing-item and nested-list rules."""
    if left is None:
        return 0 if right is None else -_compare(right, None)
    if isinstance(left, _Number):
        if right is None:
            return (left.value > 0) - (left.value < 0)
        if isinstance(right, _Number):
            if left.storage_rank != right.storage_rank:
                return (left.storage_rank > right.storage_rank) - (
                    left.storage_rank < right.storage_rank
                )
            return (left.value > right.value) - (left.value < right.value)
        return 1
    if isinstance(left, _String):
        key = _qualifier_key(left.value)
        if right is None:
            other = _qualifier_key("")
        elif isinstance(right, _String):
            other = _qualifier_key(right.value)
        else:
            return -1
        return (key > other) - (key < other)
    if isinstance(right, _Number):
        return -1
    if isinstance(right, _String):
        return 1
    if right is None:
        for item in left.items:
            result = _compare(item, None)
            if result:
                return result
        return 0
    for index in range(max(len(left.items), len(right.items))):
        a = left.items[index] if index < len(left.items) else None
        b = right.items[index] if index < len(right.items) else None
        result = _compare(a, b)
        if result:
            return result
    return 0


def _is_null(item):
    if isinstance(item, _Number):
        return item.value == 0
    if isinstance(item, _String):
        return item.value == ""
    return not item.items


@dataclass(frozen=True)
class MavenVersion:
    exact: str
    _items: _List
    _qualifiers: tuple[str, ...]


def parse_version(exact):
    """Parse safe exact text; bound work before zero/list normalization.

    Dots and hyphens are separators; underscore and plus remain string content.
    The root is not an item. Every scalar and child list counts toward 128 items;
    list depth, including the root, is separately limited to 128.
    """
    if not isinstance(exact, str) or not _EXACT.fullmatch(exact):
        raise VersionError()
    if exact.upper() in ("LATEST", "RELEASE"):
        raise VersionError()
    text = exact.lower()
    root = []
    stack = [root]
    current = root
    qualifiers = []
    count = 0

    def append(item):
        nonlocal count
        count += 1
        if count > 128:
            raise VersionError("maven_metadata_budget_exceeded")
        current.append(item)

    def child():
        nonlocal current
        nested = []
        append(nested)
        stack.append(nested)
        if len(stack) > 128:
            raise VersionError("maven_metadata_budget_exceeded")
        current = nested

    def scalar(value, digit, followed_by_digit=False):
        if digit:
            if len(value) > 128:
                raise VersionError("maven_metadata_budget_exceeded")
            # Upstream retains the width of an all-zero segment. Its numeric
            # storage class can matter when that zero is not normalized away.
            stripped = value.lstrip("0") or value
            rank = 0 if len(stripped) <= 9 else 1 if len(stripped) <= 18 else 2
            append(_Number(int(value), rank))
        else:
            if followed_by_digit:
                value = {"a": "alpha", "b": "beta", "m": "milestone"}.get(value, value)
            value = _ALIASES.get(value, value)
            qualifiers.append(value)
            append(_String(value))

    digit = False
    start = 0
    for index, character in enumerate(text):
        if character in ".-":
            if index == start:
                append(_Number(0, 0))
            else:
                scalar(text[start:index], digit)
            start = index + 1
            if character == "-":
                child()
        elif "0" <= character <= "9":
            if not digit and index > start:
                if current:
                    child()
                scalar(text[start:index], False, followed_by_digit=True)
                start = index
                child()
            digit = True
        else:
            if digit and index > start:
                scalar(text[start:index], True)
                start = index
                child()
            digit = False
    if len(text) > start:
        if not digit and current:
            child()
        scalar(text[start:], digit)

    # Normalize deepest lists first. A nonempty child does not stop the scan:
    # upstream also removes null items immediately before a trailing child.
    frozen = {}
    for mutable in reversed(stack):
        items = [frozen[id(item)] if isinstance(item, list) else item for item in mutable]
        for index in range(len(items) - 1, -1, -1):
            if _is_null(items[index]):
                del items[index]
            elif not isinstance(items[index], _List):
                break
        frozen[id(mutable)] = _List(tuple(items))
    return MavenVersion(exact, frozen[id(root)], tuple(qualifiers))


def compare_versions(left, right):
    """Return -1, 0 or 1 under the pinned ordering, without identity folding."""
    return _compare(parse_version(left)._items, parse_version(right)._items)


def is_snapshot(version):
    """ArtifactUtils suffix/timestamp rule plus the selected snapshot token rule."""
    return (
        version.exact.lower().endswith("snapshot")
        or _TIMESTAMP.fullmatch(version.exact) is not None
        or "snapshot" in version._qualifiers
    )


def eligibility(version):
    """Return eligible, excluded or unknown; ordering alone never proves stable."""
    if is_snapshot(version) or _PRERELEASE.intersection(version._qualifiers):
        return "excluded"
    if _STABLE.fullmatch(version.exact):
        return "eligible"
    return "unknown"


@dataclass(frozen=True)
class LatestSelection:
    version: str | None
    reason: str | None


def select_latest(candidates):
    """Select a global GA maximum from a whole accepted catalogue, before dates.

    No request, classifier, compatibility or date filter is accepted here. Callers
    still own XML/GA/whole-response validation. Entries count before deduplication.
    """
    eligible = []
    unknown = []
    seen = set()
    try:
        for count, exact in enumerate(candidates, 1):
            if count > 10_000:
                raise VersionError("maven_metadata_budget_exceeded")
            version = parse_version(exact)
            if exact in seen:
                continue
            seen.add(exact)
            state = eligibility(version)
            if state == "eligible":
                eligible.append(version)
            elif state == "unknown":
                unknown.append(version)
        if not eligible:
            reason = "unknown_latest_eligibility" if unknown else "no_stable_release"
            return LatestSelection(None, reason)
        maximum = eligible[0]
        ties = 1
        for version in eligible[1:]:
            order = _compare(version._items, maximum._items)
            if order > 0:
                maximum = version
                ties = 1
            elif order == 0:
                ties += 1
        if any(_compare(version._items, maximum._items) >= 0 for version in unknown):
            return LatestSelection(None, "unknown_latest_eligibility")
        if ties > 1:
            return LatestSelection(None, "ambiguous_latest_version")
        return LatestSelection(maximum.exact, None)
    except VersionError as error:
        return LatestSelection(None, error.reason)
