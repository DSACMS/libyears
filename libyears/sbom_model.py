"""Source-local SBOM facts. These records grant no metadata authority."""

from dataclasses import dataclass

from .maven_input import MavenInputFailure, relative_parts


class SbomRequestError(ValueError):
    def __init__(self):
        super().__init__('invalid SBOM selection')


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
            raise SbomRequestError()
        if self.source_id is not None:
            try:
                relative_parts(self.source_id)
            except MavenInputFailure:
                raise SbomRequestError() from None


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


@dataclass(frozen=True)
class SbomIdentity:
    group_id: str
    artifact_id: str
    version: str
    type: str = 'jar'
    classifier: str | None = None


@dataclass(frozen=True)
class SbomMember:
    index: int
    identity: SbomIdentity | None
    version: str | None
    records: tuple[tuple[int, dict], ...]
    reason: str | None
    relationship: str = 'unknown'
    direct_path: bool | None = None
    transitive_path: bool | None = None
    age: object | None = None

    @property
    def id(self):
        return f'component-{self.index}'


@dataclass(frozen=True)
class SbomReport:
    intake: SbomIntake
    document: object | None = None
    members: tuple[SbomMember, ...] = ()
    graph: object | None = None
    summary: object | None = None
