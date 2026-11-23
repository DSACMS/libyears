"""Source-local SBOM facts. These records grant no metadata authority."""

from dataclasses import dataclass

from .maven_input import MavenInputFailure, relative_parts


class SbomFailure(ValueError):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


@dataclass(frozen=True)
class SbomRequest:
    source_id: str | None = None
    disabled: bool = False

    def __post_init__(self):
        if type(self.disabled) is not bool or (self.disabled and self.source_id is not None):
            raise ValueError('invalid SBOM request')
        if self.source_id is not None:
            try:
                relative_parts(self.source_id)
            except MavenInputFailure:
                raise ValueError('unsafe SBOM selection') from None


@dataclass(frozen=True)
class SbomDiscovery:
    mode: str
    state: str
    candidate_count: int | None
    search_complete: bool | None
    reason: str | None = None


@dataclass(frozen=True)
class SbomSelection:
    mode: str
    state: str
    source_id: str | None = None


@dataclass(frozen=True)
class SbomSnapshot:
    source_id: str
    data: bytes
    sha256: str


@dataclass(frozen=True)
class SbomIntake:
    discovery: SbomDiscovery
    selection: SbomSelection
    snapshot: SbomSnapshot | None = None
    reason: str | None = None
