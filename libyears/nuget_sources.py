"""Bounded independent repository NuGet sources; no graph or resolver authority."""

from collections import Counter
from dataclasses import replace
import os
from pathlib import Path
import stat

from .model import SourceError, SourceResult
from .nuget import NuGetSource, NuGetSourceEvidence, read_nuget_source
from .nuget_discovery import discover_nuget_candidates, discovery_available, _reparse_point
from .nuget_input import NuGetInputFailure, ScopedNuGetReader, _identity


class NuGetRepositoryRequestError(ValueError):
    """Safe request classification; never retain rejected option text."""


def _filename(value: str, suffix: str) -> bool:
    return (isinstance(value, str) and bool(value) and value.endswith(suffix)
            and value.isprintable() and value not in ('.', '..')
            and not any(character in value for character in '/\\:*?[]{};,='))


def validate_witnesses(witnesses) -> dict[str, str]:
    """Validate explicit project/witness pairs before any source is read."""
    result = {}
    for pair in witnesses:
        if not isinstance(pair, (tuple, list)) or len(pair) != 2:
            raise NuGetRepositoryRequestError('invalid NuGet witness mapping')
        project, witness = pair
        if not isinstance(project, str):
            raise NuGetRepositoryRequestError('invalid NuGet witness mapping')
        components = project.split('/')
        if (not all(_filename(component, '') for component in components)
                or not components[-1].endswith('.csproj')
                or not _filename(witness, '.json') or witness == 'packages.lock.json'
                or project in result):
            raise NuGetRepositoryRequestError('invalid NuGet witness mapping')
        result[project] = witness
    return result


class RepositoryNuGetReader(ScopedNuGetReader):
    """Anchor every parent to held no-follow descriptors, including after reads."""

    def __init__(self, repository: Path, project: str, witness: str | None):
        components = project.split('/')
        if (not components or not project.endswith('.csproj')
                or any(not part or part in ('.', '..') or '\\' in part
                       for part in components)):
            raise NuGetInputFailure('malformed')
        self.repository = Path(repository).absolute()
        self.parents = components[:-1]
        self.chain = []
        super().__init__(self.repository.joinpath(*self.parents), components[-1], witness)

    def __enter__(self):
        if not discovery_available() or os.readlink not in os.supports_dir_fd:
            raise NuGetInputFailure('malformed')
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_NONBLOCK
        try:
            inspected = os.stat(self.repository, follow_symlinks=False)
            if not stat.S_ISDIR(inspected.st_mode) or _reparse_point(inspected):
                raise NuGetInputFailure('malformed')
            descriptor = os.open(self.repository, flags)
            self.chain.append((descriptor, None, inspected))
            if _identity(os.fstat(descriptor)) != _identity(inspected):
                raise NuGetInputFailure('malformed')
            for name in self.parents:
                inspected = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
                if not stat.S_ISDIR(inspected.st_mode) or _reparse_point(inspected):
                    raise NuGetInputFailure('malformed')
                descriptor = os.open(name, flags, dir_fd=descriptor)
                self.chain.append((descriptor, name, inspected))
                if _identity(os.fstat(descriptor)) != _identity(inspected):
                    raise NuGetInputFailure('malformed')
            self.directory = descriptor
            self.root_identity = _identity(os.fstat(descriptor))
            return self
        except (OSError, ValueError, NotImplementedError):
            self.__exit__()
            raise NuGetInputFailure('malformed') from None

    def _root_unchanged(self):
        for index, (descriptor, name, before) in enumerate(self.chain):
            if _identity(os.fstat(descriptor)) != _identity(before):
                return False
            if index == 0:
                current = os.stat(self.repository, follow_symlinks=False)
            else:
                current = os.stat(name, dir_fd=self.chain[index - 1][0], follow_symlinks=False)
            if _reparse_point(current) or _identity(current) != _identity(before):
                return False
        return True

    def __exit__(self, *unused):
        for descriptor, _, _ in reversed(self.chain):
            os.close(descriptor)
        self.chain.clear()
        self.directory = None


def _unavailable(source_id: str | None, reason: str) -> NuGetSource:
    name = 'repository' if source_id is None else source_id.rsplit('/', 1)[-1]
    evidence = NuGetSourceEvidence(name if source_id else None, 'packages.lock.json',
                                  include_format=True, scope='explicit_direct_packagereference',
                                  publication_basis='nuget_org_first_receipt_created')
    return NuGetSource(SourceResult('nuget', (), (),
        (SourceError('nuget', name, reason, source_id),), evidence, None, False,
        source_id=source_id))


def _attribute_source(source: NuGetSource, source_id: str) -> NuGetSource:
    def attribute(item):
        return replace(item, nuget_evidence=replace(item.nuget_evidence, source_id=source_id))
    authorized = tuple(replace(item, candidate=attribute(item.candidate))
                       for item in source.authorized_candidates)
    result = replace(source.result, source_id=source_id,
        candidates=tuple(item.candidate for item in authorized),
        unmeasurable=tuple(attribute(item) for item in source.result.unmeasurable),
        source_errors=tuple(replace(item, source_id=source_id)
                            for item in source.result.source_errors))
    return NuGetSource(result, authorized)


def read_repository_sources(root: Path, witnesses=()) -> tuple[NuGetSource, ...]:
    """Discover then independently attempt sources without implicitly accepting testimony."""
    mapping = validate_witnesses(witnesses)
    inventory = discover_nuget_candidates(root)
    if inventory.status != 'complete':
        return (_unavailable(None, 'nuget_discovery_' + inventory.status),)
    sources = []
    parent_counts = Counter(project.rpartition('/')[0] for project in inventory.candidates)
    for project in inventory.candidates:
        parent = root.joinpath(*project.split('/')[:-1])
        name = project.rsplit('/', 1)[-1]
        witness = mapping.get(project)
        try:
            reader = RepositoryNuGetReader(root, project, witness)
        except (NuGetInputFailure, ValueError):
            # Discovery observes filesystem names, which can be outside the
            # scoped reader's filename contract. Refusal belongs to this source.
            sources.append(_unavailable(project, 'invalid_nuget_project'))
            continue
        source = read_nuget_source(parent, name, witness, reader=reader,
            repository_snapshot=True,
            unambiguous_snapshot=parent_counts[project.rpartition('/')[0]] == 1)
        sources.append(_attribute_source(source, project))
    for project in sorted(mapping.keys() - set(inventory.candidates)):
        sources.append(_unavailable(project, 'nuget_witness_project_missing'))
    return tuple(sorted(sources, key=lambda item: item.result.source_id))
