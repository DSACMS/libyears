"""Bounded local Maven graphs and raw fields, not evaluated dependency facts.

Only an inventoried T002 snapshot reader supplies bytes. These records deliberately
have no external-population count, resolved version, Observed record or age.
Artifact mappings are facts from Apache Maven 3.9.11's handler reference, credited
to Hervé Boutemy / The Apache Software Foundation. See the extracted facts and
Apache LICENSE/NOTICE in third_party/maven-3.9.11/artifact-handlers.json.
"""

from dataclasses import dataclass, replace
from enum import StrEnum
import re

from .maven_input import (
    MavenInputFailure, MavenInputSnapshot, MavenXMLElement, relative_parts,
)
from .maven_model import (
    MavenArtifactKey, MavenContext, MavenDiscovery, MavenFieldBasis,
    MavenFieldOrigin, MavenModelKey,
)

MAX_PARENT_CHAIN = 16
MAX_RECORDS = 10_000
MAX_MODULES = 100
MAX_PROFILES = 128
_GROUP = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_-]*(?:\.[A-Za-z0-9_][A-Za-z0-9_-]*)*", re.ASCII)
_ATOM = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", re.ASCII)
_VERSION = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]*", re.ASCII)
_FIELDS = ('version', 'scope', 'optional')
_HANDLERS = {
    'pom': ('pom', None), 'jar': ('jar', None), 'test-jar': ('jar', 'tests'),
    'maven-plugin': ('jar', None), 'ejb': ('jar', None),
    'ejb-client': ('jar', 'client'), 'war': ('war', None), 'ear': ('ear', None),
    'rar': ('rar', None), 'java-source': ('jar', 'sources'),
    'javadoc': ('jar', 'javadoc'),
}


class ModelIssue(StrEnum):
    INPUT = 'input_unavailable'
    STRUCTURE = 'unsupported_structure'
    IDENTITY = 'unsupported_identity'
    KEY = 'unsupported_dependency_key'
    DUPLICATE = 'ambiguous_dependency_key'
    ARTIFACT = 'unsupported_artifact_handler'
    PARENT_EXTERNAL = 'external_parent'
    PARENT_PATH = 'unsupported_parent_path'
    PARENT_MISSING = 'missing_parent'
    PARENT_MISMATCH = 'parent_gav_mismatch'
    PARENT_CYCLE = 'parent_cycle'
    PARENT_DEPTH = 'parent_depth_exceeded'
    MODULE_PATH = 'unsupported_module_path'
    MODULE_MISSING = 'missing_module'
    MODULE_CYCLE = 'module_cycle'
    DUPLICATE_GAV = 'duplicate_project_gav'
    ROOTS = 'incompatible_aggregation_roots'
    LIMIT = 'model_budget_exceeded'


@dataclass(frozen=True, slots=True)
class ModelProblem:
    source_id: str
    issue: ModelIssue


@dataclass(frozen=True, slots=True)
class ProjectIdentity:
    group_id: str | None
    artifact_id: str | None
    version: str | None

    @property
    def gav(self):
        if None in (self.group_id, self.artifact_id, self.version):
            return None
        return self.group_id, self.artifact_id, self.version


@dataclass(frozen=True, slots=True)
class RawField:
    value: str
    origin: MavenFieldOrigin


@dataclass(frozen=True, slots=True)
class RawDependency:
    consumer_source: str
    declaration_source: str
    key: MavenModelKey
    fields: tuple[RawField, ...] = ()

    def field(self, name: str) -> RawField | None:
        return next((item for item in self.fields if item.origin.field_name == name), None)

    @property
    def artifact_key(self):
        return artifact_for(self.key)


@dataclass(frozen=True, slots=True)
class RawParent:
    identity: ProjectIdentity
    # None means Maven's default ../pom.xml; empty means explicitly external.
    relative_path: str | None


@dataclass(frozen=True, slots=True)
class RawProject:
    source_id: str
    snapshot: MavenInputSnapshot | None
    identity: ProjectIdentity
    parent: RawParent | None = None
    dependencies: tuple[RawDependency, ...] = ()
    management: tuple[RawDependency, ...] = ()
    ambiguous_dependencies: tuple[MavenModelKey, ...] = ()
    ambiguous_management: tuple[MavenModelKey, ...] = ()
    modules: tuple[str, ...] = ()
    modules_complete: bool = True
    problems: tuple[ModelProblem, ...] = ()
    parent_supported: bool = True


@dataclass(frozen=True, slots=True)
class RawModel:
    context: MavenContext
    identity: ProjectIdentity
    dependencies: tuple[RawDependency, ...]
    management: tuple[RawDependency, ...]
    parent_chain_complete: bool
    problems: tuple[ModelProblem, ...]
    # A duplicate blocks inheritance at the same key as well as local selection.
    ambiguous_dependencies: tuple[MavenModelKey, ...] = ()
    ambiguous_management: tuple[MavenModelKey, ...] = ()


@dataclass(frozen=True, slots=True)
class Aggregation:
    source_ids: tuple[str, ...]
    roots: tuple[str, ...]
    complete: bool
    problems: tuple[ModelProblem, ...] = ()


@dataclass(frozen=True, slots=True)
class MavenProjectGraph:
    discovery: MavenDiscovery
    projects: tuple[RawProject, ...]
    models: tuple[RawModel, ...]
    aggregations: tuple[Aggregation, ...]


def _literal(value, kind):
    if value is None:
        return None
    value = value.strip()
    pattern = _GROUP if kind == 'groupId' else _VERSION if kind == 'version' else _ATOM
    maximum = 256 if kind == 'version' else 128
    if (not 1 <= len(value) <= maximum or not pattern.fullmatch(value)
            or value in ('.', '..')
            or (kind == 'version' and value.upper() in ('LATEST', 'RELEASE'))):
        return None
    return value


def artifact_for(key: MavenModelKey) -> MavenArtifactKey | None:
    """Map a supported literal key without changing the management model key."""
    if (_literal(key.group_id, 'groupId') != key.group_id
            or _literal(key.artifact_id, 'artifactId') != key.artifact_id
            or (key.classifier is not None
                and _literal(key.classifier, 'classifier') != key.classifier)):
        return None
    handler = _HANDLERS.get(key.type)
    if handler is None:
        return None
    extension, default_classifier = handler
    classifier = key.classifier if key.classifier is not None else default_classifier
    return MavenArtifactKey(key.group_id, key.artifact_id, extension, classifier)


def _container(element, name):
    children = element.elements(name)
    if len(children) > 1:
        raise ValueError('unsupported Maven container')
    if not children:
        return None
    if children[0].text.strip():
        raise ValueError('mixed Maven container')
    return children[0]


def _identity(element):
    return ProjectIdentity(*(
        _literal(element.scalar(name), name) for name in ('groupId', 'artifactId', 'version')
    ))


def _records(container, source, management=False):
    """Only the specified direct container; no recursive dependency search."""
    if container is None:
        return (), (), ()
    records = {}
    ambiguous = set()
    problems = []
    if any(child.name != 'dependency' for child in container.children):
        problems.append(ModelProblem(source, ModelIssue.STRUCTURE))
    # Validate candidates individually: one unsupported entry must not erase
    # independent safe siblings. Its refusal still consumes a record slot.
    entries = tuple(child for child in container.children if child.name == 'dependency')
    for index, entry in enumerate(entries):
        if not management and index >= MAX_RECORDS:
            problems.append(ModelProblem(source, ModelIssue.LIMIT))
            break
        key = None
        try:
            if entry.namespace != container.namespace or entry.attributes or entry.text.strip():
                raise ValueError('mixed dependency')
            group = _literal(entry.scalar('groupId'), 'groupId')
            artifact = _literal(entry.scalar('artifactId'), 'artifactId')
            raw_type = entry.scalar('type')
            kind = 'jar' if raw_type is None else _literal(raw_type, 'type')
            raw_classifier = entry.scalar('classifier')
            classifier = None if raw_classifier is None else _literal(raw_classifier, 'classifier')
            if group is None or artifact is None or kind is None or (
                    raw_classifier is not None and classifier is None):
                problems.append(ModelProblem(source, ModelIssue.KEY))
                continue
            key = MavenModelKey(group, artifact, kind, classifier)
            allowed = {'groupId', 'artifactId', 'type', 'classifier', *_FIELDS,
                       'systemPath', 'exclusions'}
            if any(child.name not in allowed for child in entry.children):
                problems.append(ModelProblem(source, ModelIssue.STRUCTURE))
            fields = []
            for name in _FIELDS:
                value = entry.scalar(name)
                if value is not None:
                    basis = (MavenFieldBasis.CONSUMER_MANAGEMENT if management
                             else MavenFieldBasis.DEPENDENCY)
                    fields.append(RawField(value.strip(), MavenFieldOrigin(source, name, basis)))
            record = RawDependency(source, source, key, tuple(fields))
            if key in records or key in ambiguous:
                records.pop(key, None)
                ambiguous.add(key)
                problems.append(ModelProblem(source, ModelIssue.DUPLICATE))
            else:
                records[key] = record
            if record.artifact_key is None:
                problems.append(ModelProblem(source, ModelIssue.ARTIFACT))
        except (MavenInputFailure, ValueError):
            if key is not None:
                records.pop(key, None)
                ambiguous.add(key)
            problems.append(ModelProblem(source, ModelIssue.STRUCTURE))
    return tuple(records.values()), _sorted_keys(ambiguous), tuple(problems)


def _sorted_keys(keys):
    return tuple(sorted(keys, key=lambda key: (
        key.group_id, key.artifact_id, key.type, key.classifier or '',
    )))


def _parse_project(source, snapshot):
    if snapshot.source_id != source or snapshot.xml is None:
        raise ValueError('unbound Maven snapshot')
    root = snapshot.xml
    problems = []
    identity = ProjectIdentity(None, None, None)
    try:
        identity = _identity(root)
        if (identity.artifact_id is None or any(
                root.scalar(name) is not None and _literal(root.scalar(name), name) is None
                for name in ('groupId', 'version'))):
            problems.append(ModelProblem(source, ModelIssue.IDENTITY))
    except MavenInputFailure:
        problems.append(ModelProblem(source, ModelIssue.IDENTITY))
    parent = None
    parent_supported = True
    try:
        node = _container(root, 'parent')
        if node is not None:
            if any(child.name not in ('groupId', 'artifactId', 'version', 'relativePath')
                   for child in node.children):
                raise ValueError('unknown parent field')
            parent = RawParent(_identity(node), node.scalar('relativePath'))
            if parent.identity.gav is None:
                problems.append(ModelProblem(source, ModelIssue.IDENTITY))
    except (MavenInputFailure, ValueError):
        parent_supported = False
        problems.append(ModelProblem(source, ModelIssue.STRUCTURE))
    lists = []
    ambiguous_lists = []
    for management in (False, True):
        try:
            owner = _container(root, 'dependencyManagement') if management else root
            if management and owner is not None and any(
                    child.name != 'dependencies' for child in owner.children):
                problems.append(ModelProblem(source, ModelIssue.STRUCTURE))
            container = _container(owner, 'dependencies') if owner is not None else None
            records, ambiguous, issues = _records(container, source, management)
            problems.extend(issues)
        except (MavenInputFailure, ValueError):
            records, ambiguous = (), ()
            problems.append(ModelProblem(source, ModelIssue.STRUCTURE))
        lists.append(records)
        ambiguous_lists.append(ambiguous)
    modules = ()
    modules_complete = True
    try:
        container = _container(root, 'modules')
        if container is not None:
            if any(child.name != 'module' for child in container.children):
                raise ValueError('unknown module element')
            entries = container.elements('module')
            if len(entries) > MAX_MODULES:
                modules_complete = False
                problems.append(ModelProblem(source, ModelIssue.LIMIT))
            values = []
            for entry in entries[:MAX_MODULES]:
                if entry.children:
                    raise ValueError('mixed module')
                values.append(entry.text.strip())
            modules = tuple(values)
        # Do not evaluate profiles. Potential module writes cannot establish an
        # unconditional complete association; other profile semantics await T005.
        profiles = _container(root, 'profiles')
        if profiles is not None:
            if any(child.name != 'profile' for child in profiles.children):
                raise ValueError('unknown profile element')
            entries = profiles.elements('profile')
            if len(entries) > MAX_PROFILES:
                modules_complete = False
                problems.append(ModelProblem(source, ModelIssue.LIMIT))
            if any(entry.elements('modules') for entry in entries):
                modules_complete = False
                problems.append(ModelProblem(source, ModelIssue.MODULE_PATH))
    except (MavenInputFailure, ValueError):
        modules_complete = False
        problems.append(ModelProblem(source, ModelIssue.STRUCTURE))
    return RawProject(source, snapshot, identity, parent, lists[0], lists[1],
                      ambiguous_lists[0], ambiguous_lists[1], modules,
                      modules_complete, tuple(problems), parent_supported)


def _edge_target(source, value, *, directory=False):
    """Normalize a contained logical edge; never inspect a filesystem path."""
    if (not value or len(value) > 1024 or not value.isprintable()
            or any(char in value for char in ('\\', ':', '$', '~'))
            or value.startswith('/') or len(value.split('/')) > 32):
        return None
    parts = source.split('/')[:-1]
    for part in value.split('/'):
        if part == '..':
            if not parts:
                return None
            parts.pop()
        elif part not in ('', '.'):
            parts.append(part)
    if directory:
        parts.append('pom.xml')
    target = '/'.join(parts)
    try:
        relative_parts(target)
    except MavenInputFailure:
        return None
    return target


def _inherit(records, consumer, management):
    basis = (MavenFieldBasis.INHERITED_MANAGEMENT if management
             else MavenFieldBasis.INHERITED_DEPENDENCY)
    inherited = []
    for record in records:
        fields = tuple(replace(item, origin=replace(item.origin, basis=basis))
                       for item in record.fields)
        inherited.append(replace(record, consumer_source=consumer, fields=fields))
    return inherited


def _merge(parent_records, local_records, parent_ambiguous, local_ambiguous,
           consumer, management):
    blocked = set(parent_ambiguous) | set(local_ambiguous)
    merged = {record.key: record for record in _inherit(parent_records, consumer, management)
              if record.key not in blocked}
    for local in local_records:
        if local.key in blocked:
            continue
        inherited = merged.get(local.key)
        if inherited is not None:
            fields = {item.origin.field_name: item for item in inherited.fields}
            fields.update({item.origin.field_name: item for item in local.fields})
            local = replace(local, fields=tuple(fields[name] for name in _FIELDS if name in fields))
        merged[local.key] = local
    return tuple(merged.values()), _sorted_keys(blocked)


def _absent(element, name):
    try:
        return element.scalar(name) is None
    except MavenInputFailure:
        return False


def _resolve_model(source, projects, trail=()):
    project = projects[source]
    problems = list(project.problems)
    identity = project.identity
    parent_model = None
    complete = project.snapshot is not None and project.parent_supported
    if project.parent is not None:
        reference = project.parent
        path = '../pom.xml' if reference.relative_path is None else reference.relative_path.strip()
        issue = None
        if path == '':
            issue = ModelIssue.PARENT_EXTERNAL
        elif reference.identity.gav is None:
            issue = ModelIssue.IDENTITY
        else:
            target = _edge_target(source, path)
            # A literal directory can identify only its already discovered POM.
            if target not in projects:
                directory_target = _edge_target(source, path, directory=True)
                if directory_target in projects:
                    target = directory_target
            if target is None:
                issue = ModelIssue.PARENT_PATH
            elif target not in projects or projects[target].snapshot is None:
                issue = ModelIssue.PARENT_MISSING
            elif target in (*trail, source):
                issue = ModelIssue.PARENT_CYCLE
            elif len(trail) + 1 >= MAX_PARENT_CHAIN:
                issue = ModelIssue.PARENT_DEPTH
            else:
                candidate = _resolve_model(target, projects, (*trail, source))
                if candidate.identity.gav != reference.identity.gav:
                    issue = ModelIssue.PARENT_MISMATCH
                elif any(problem.issue in (ModelIssue.PARENT_CYCLE, ModelIssue.PARENT_DEPTH)
                         for problem in candidate.problems):
                    problems.extend(candidate.problems)
                    complete = False
                else:
                    parent_model = candidate
        if issue is not None:
            complete = False
            problems.append(ModelProblem(source, issue))
        elif parent_model is None:
            complete = False
    if parent_model is None:
        return RawModel(MavenContext(source), identity, project.dependencies, project.management,
                        complete, tuple(problems), project.ambiguous_dependencies,
                        project.ambiguous_management)
    complete = complete and parent_model.parent_chain_complete
    # Only absence inherits. An explicit unsupported identity never falls back.
    root = project.snapshot.xml
    if _absent(root, 'groupId'):
        identity = replace(identity, group_id=parent_model.identity.group_id)
    if _absent(root, 'version'):
        identity = replace(identity, version=parent_model.identity.version)
    dependencies, ambiguous_dependencies = _merge(
        parent_model.dependencies, project.dependencies, parent_model.ambiguous_dependencies,
        project.ambiguous_dependencies, source, False,
    )
    management, ambiguous_management = _merge(
        parent_model.management, project.management, parent_model.ambiguous_management,
        project.ambiguous_management, source, True,
    )
    if len(dependencies) > MAX_RECORDS:
        dependencies = dependencies[:MAX_RECORDS]
        problems.append(ModelProblem(source, ModelIssue.LIMIT))
    return RawModel(
        MavenContext(source, parent_sources=(parent_model.context.source_id,
                     *parent_model.context.parent_sources)), identity, dependencies, management,
        complete, tuple([*problems, *parent_model.problems]), ambiguous_dependencies,
        ambiguous_management,
    )


def _aggregations(projects, models):
    adjacency = {source: set() for source in projects}
    problems = {source: [] for source in projects}
    for source, project in projects.items():
        if project.snapshot is None or not project.modules_complete:
            problems[source].append(ModelProblem(source, ModelIssue.STRUCTURE))
        for path in project.modules:
            target = _edge_target(source, path, directory=True)
            if target is None:
                issue = ModelIssue.MODULE_PATH
            elif target not in projects or projects[target].snapshot is None:
                issue = ModelIssue.MODULE_MISSING
            elif target == source or target in adjacency[source]:
                issue = ModelIssue.MODULE_CYCLE
            else:
                adjacency[source].add(target)
                continue
            problems[source].append(ModelProblem(source, issue))
    neighbours = {source: set(targets) for source, targets in adjacency.items()}
    for source, targets in adjacency.items():
        for target in targets:
            neighbours[target].add(source)
    components = []
    remaining = set(projects)
    while remaining:
        pending = [min(remaining)]
        members = set()
        while pending:
            source = pending.pop()
            if source not in members:
                members.add(source)
                pending.extend(neighbours[source] - members)
        remaining -= members
        sources = tuple(sorted(members))
        issues = [problem for source in sources for problem in problems[source]]
        incoming = {source: 0 for source in sources}
        for source in sources:
            for target in adjacency[source]:
                incoming[target] += 1
        roots = tuple(sorted(source for source in sources if incoming[source] == 0))
        if len(roots) > 1:
            issues.append(ModelProblem(sources[0], ModelIssue.ROOTS))
        pending = list(roots)
        visited = 0
        while pending:
            source = pending.pop()
            visited += 1
            for target in adjacency[source]:
                incoming[target] -= 1
                if incoming[target] == 0:
                    pending.append(target)
        if visited != len(sources):
            issues.append(ModelProblem(sources[0], ModelIssue.MODULE_CYCLE))
        gavs = set()
        for source in sources:
            gav = models[source].identity.gav
            if gav is not None:
                if gav in gavs:
                    issues.append(ModelProblem(source, ModelIssue.DUPLICATE_GAV))
                gavs.add(gav)
        components.append(Aggregation(sources, roots, not issues, tuple(issues)))
    return tuple(components)


def build_project_graph(discovery: MavenDiscovery, snapshot_pom) -> MavenProjectGraph:
    """Stage discovered snapshots once; never expand discovery through an edge.

    snapshot_pom is the T002 reader method (or an injected safe-snapshot fixture).
    The caller retains that reader's scope/lifecycle and discovery completeness.
    """
    projects = {}
    for source in sorted(discovery.source_ids):
        try:
            snapshot = snapshot_pom(source)
            project = _parse_project(source, snapshot)
        except (MavenInputFailure, ValueError):
            project = RawProject(source, None, ProjectIdentity(None, None, None),
                                 modules_complete=False,
                                 problems=(ModelProblem(source, ModelIssue.INPUT),))
        projects[source] = project
    models = {}
    remaining = MAX_RECORDS
    for source in projects:
        model = _resolve_model(source, projects)
        if len(model.dependencies) > remaining:
            model = replace(model, dependencies=model.dependencies[:remaining],
                            problems=(*model.problems, ModelProblem(source, ModelIssue.LIMIT)))
        remaining -= len(model.dependencies)
        models[source] = model
    return MavenProjectGraph(discovery, tuple(projects.values()), tuple(models.values()),
                             _aggregations(projects, models))
