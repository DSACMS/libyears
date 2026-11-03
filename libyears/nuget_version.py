"""Bounded NuGet request minima and selected identities, without resolution."""

from dataclasses import dataclass
import re


MAX_VERSION_LENGTH = 256
MAX_COMPONENT_DIGITS = 32
_SELECTED = re.compile(
    r"([0-9]+(?:\.[0-9]+){1,3})"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)
_REQUEST = re.compile(r"(?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*)){1,3}")


@dataclass(frozen=True, slots=True)
class RequestedMinimum:
    """An inclusive numeric minimum, never an exact selected version."""

    components: tuple[int, int, int, int]
    normalized_version: str


@dataclass(frozen=True, slots=True)
class SelectedIdentity:
    """Safe original spelling and normalized identity; build labels are ignored."""

    original_version: str
    normalized_version: str
    components: tuple[int, int, int, int]
    prerelease: str | None


def _bounded_string(value: object) -> bool:
    return isinstance(value, str) and 0 < len(value) <= MAX_VERSION_LENGTH and value.isascii()


def _numeric_components(core: str) -> tuple[int, int, int, int] | None:
    parts = core.split(".")
    # Check every length before converting any attacker-supplied integer.
    if any(len(part) > MAX_COMPONENT_DIGITS for part in parts):
        return None
    numbers = [int(part) for part in parts]
    numbers.extend([0] * (4 - len(numbers)))
    return (numbers[0], numbers[1], numbers[2], numbers[3])


def _normalized_core(components: tuple[int, int, int, int]) -> str:
    displayed = components if components[3] else components[:3]
    return ".".join(str(component) for component in displayed)


def parse_requested_minimum(value: object) -> RequestedMinimum | None:
    """Parse only bare two-to-four-component minima with canonical digits."""
    if not _bounded_string(value) or _REQUEST.fullmatch(value) is None:
        return None
    components = _numeric_components(value)
    if components is None:
        return None
    return RequestedMinimum(components, _normalized_core(components))


def parse_selected_identity(value: object) -> SelectedIdentity | None:
    """Parse S5 evidence syntax, folding prerelease case and ignoring builds."""
    if not _bounded_string(value):
        return None
    match = _SELECTED.fullmatch(value)
    if match is None:
        return None
    components = _numeric_components(match.group(1))
    if components is None:
        return None
    prerelease = match.group(2)
    if prerelease is not None:
        prerelease = prerelease.lower()
    normalized = _normalized_core(components)
    if prerelease is not None:
        normalized += "-" + prerelease
    return SelectedIdentity(value, normalized, components, prerelease)


def stable_precedence_key(value: object) -> tuple[int, int, int, int] | None:
    """Return numeric precedence only for a supported stable identity."""
    identity = parse_selected_identity(value)
    if identity is None or identity.prerelease is not None:
        return None
    return identity.components
