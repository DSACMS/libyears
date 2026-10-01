"""Discovery of exact-pinned Python requirements."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


NON_EXACT_VERSION = "non_exact_version"
UNSUPPORTED_REQUIREMENT = "unsupported_requirement"
CONFLICTING_VERSIONS = "conflicting_versions"

_EXACT = re.compile(r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)\s*==\s*(?P<version>\S+)$")
_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def normalize_name(name: str) -> str:
    """Normalize a PyPI project name for identity comparisons."""
    return re.sub(r"[-_.]+", "-", name.strip().lower())


@dataclass(frozen=True, slots=True)
class ExactRequirement:
    """An exact requirement retained for registry measurement."""

    name: str
    normalized_name: str
    version: str
    declared: str
    ecosystem: str = "pypi"


@dataclass(frozen=True, slots=True)
class UnmeasurableRequirement:
    """A discovered requirement that cannot be measured from an exact pin."""

    name: str
    declared: str
    reason: str
    ecosystem: str = "pypi"


@dataclass(frozen=True, slots=True)
class Requirements:
    """The exact requirements and unmeasurable requirements from a file."""

    exact: tuple[ExactRequirement, ...]
    unmeasurable: tuple[UnmeasurableRequirement, ...]

    @property
    def discovered(self) -> int:
        return len(self.exact) + len(self.unmeasurable)


def _without_inline_comment(line: str) -> str:
    for index, character in enumerate(line):
        if character == "#" and (index == 0 or line[index - 1].isspace()):
            return line[:index].rstrip()
    return line.strip()


def _is_unsupported(value: str) -> bool:
    lowered = value.lower()
    return (
        lowered.startswith(("git+", "hg+", "svn+", "bzr+", "http://", "https://", "file://"))
        or " @ " in value
        or lowered.startswith(("-e ", "--editable ", "./", "../", "/", "~/"))
    )


def _display_name(value: str) -> str:
    match = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)", value)
    return match.group(1) if match else value.split()[0] if value.split() else value


def discover_requirements(path: str | Path) -> Requirements:
    """Read *path* and discover direct exact pins without resolving them."""
    exact_by_name: dict[str, list[ExactRequirement]] = {}
    unmeasurable: list[UnmeasurableRequirement] = []

    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = _without_inline_comment(raw_line)
        if not line:
            continue

        if _is_unsupported(line):
            unmeasurable.append(
                UnmeasurableRequirement(_display_name(line), line, UNSUPPORTED_REQUIREMENT)
            )
            continue

        match = _EXACT.fullmatch(line)
        if match is None or not _NAME.fullmatch(match.group("name")):
            unmeasurable.append(
                UnmeasurableRequirement(_display_name(line), line, NON_EXACT_VERSION)
            )
            continue

        requirement = ExactRequirement(
            name=match.group("name"),
            normalized_name=normalize_name(match.group("name")),
            version=match.group("version"),
            declared=line,
        )
        exact_by_name.setdefault(requirement.normalized_name, []).append(requirement)

    exact: list[ExactRequirement] = []
    for requirements in exact_by_name.values():
        versions = {requirement.version for requirement in requirements}
        if len(versions) > 1:
            declared = ", ".join(requirement.declared for requirement in requirements)
            unmeasurable.append(
                UnmeasurableRequirement(
                    requirements[0].name, declared, CONFLICTING_VERSIONS
                )
            )
        else:
            exact.append(requirements[0])

    return Requirements(tuple(exact), tuple(unmeasurable))


discover = discover_requirements

__all__ = [
    "CONFLICTING_VERSIONS",
    "ExactRequirement",
    "NON_EXACT_VERSION",
    "Requirements",
    "UNSUPPORTED_REQUIREMENT",
    "UnmeasurableRequirement",
    "discover",
    "discover_requirements",
    "normalize_name",
]
