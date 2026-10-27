"""Bounded, static Yarn Classic v1 lockfile parsing."""

from dataclasses import dataclass
import re


UNSUPPORTED_LOCKFILE_FORMAT = "unsupported_lockfile_format"
_CANONICAL_HEADER = "# yarn lockfile v1"
_GENERATION_MARKER = re.compile(r"#\s*yarn\s+(?:lockfile|berry|pnp|v\d)", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class YarnFailure:
    """A stable failure reason with optional human-only context."""

    reason: str
    diagnostic: str


def recognize_v1(text: str) -> YarnFailure | None:
    """Require an uncontradicted canonical header before any lock entries.

    Recognition deliberately does not validate entries. Body syntax cannot
    establish the generation, even when it resembles a Classic lockfile.
    """
    found_header = False
    for line in text.splitlines():
        if not line.strip():
            continue
        if not line.startswith("#"):
            # Berry's metadata marker contradicts a claimed Classic header.
            if line.startswith("__metadata:"):
                return YarnFailure(
                    UNSUPPORTED_LOCKFILE_FORMAT, "unsupported Yarn metadata format"
                )
            break
        if line == _CANONICAL_HEADER:
            found_header = True
        elif _GENERATION_MARKER.match(line):
            return YarnFailure(
                UNSUPPORTED_LOCKFILE_FORMAT,
                "unsupported or contradictory Yarn generation header",
            )
    if not found_header:
        return YarnFailure(
            UNSUPPORTED_LOCKFILE_FORMAT, "could not identify Yarn Classic v1"
        )
    return None
