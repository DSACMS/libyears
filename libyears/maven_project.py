"""Bounded local Maven graphs, raw fields and supported declared facts.

Only an inventoried T002 snapshot reader supplies bytes. Raw models remain distinct
from final declared collections. No resolver, Observed reader or age is inferred.
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
    MavenArtifactKey, MavenCollection, MavenContext, MavenDiscovery, MavenFieldBasis,
    MavenFieldOrigin, MavenModelKey, MavenOccurrence, MavenOccurrenceKey,
    MavenReason, MavenSource, MavenVersionBasis, MavenVersionFact, MavenView,
)
from .maven_properties import PropertyFailure, ScalarProperty, expand_scalar, read_properties
from .maven_version import VersionError, is_snapshot, parse_version

MAX_PARENT_CHAIN = 16
MAX_RECORDS = 10_000
MAX_MODULES = 100
MAX_PROFILES = 128
_GROUP = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_-]*(?:\.[A-Za-z0-9_][A-Za-z0-9_-]*)*", re.ASCII)
_ATOM = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", re.ASCII)
_VERSION = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]*", re.ASCII)
_FIELDS = ('version', 'scope', 'optional')
# Names from the pinned 3.9.11 model reference, retained in model-facts.json.
# Recognizing a container name does not evaluate its contents.
_PROJECT_ELEMENTS = frozenset({
    'modelVersion', 'parent', 'groupId', 'artifactId', 'version', 'packaging',
    'name', 'description', 'url', 'inceptionYear', 'organization', 'licenses',
    'developers', 'contributors', 'mailingLists', 'prerequisites', 'modules',
    'scm', 'issueManagement', 'ciManagement', 'distributionManagement',
    'properties', 'dependencyManagement', 'dependencies', 'repositories',
    'pluginRepositories', 'build', 'reports', 'reporting', 'profiles',
})
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
                # Reject this known key through the existing blocked-key path:
                # unknown semantics cannot admit its facts or revive a parent.
                raise ValueError('unsupported dependency field')
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


@dataclass
class _FactContext:
    properties: dict
    blocked_properties: set
    property_unknown: bool
    trusted_properties: set
    builtins: dict
    direct_variants: set
    managed_variants: set
    unknown_profile: bool
    extra_population: bool
    association_variable: bool
    imports_unknown: bool
    management_unknown: bool
    identity_variants: set

    def expand(self, value):
        return expand_scalar(value, self.properties, self.builtins,
                             self.blocked_properties, unknown=self.property_unknown,
                             trusted=self.trusted_properties)


def _version_builtin(graph, model):
    projects = {project.source_id: project for project in graph.projects}
    for source in (model.context.source_id, *model.context.parent_sources):
        root = projects[source].snapshot.xml
        if not _absent(root, 'version'):
            try:
                value = _literal(root.scalar('version'), 'version')
            except MavenInputFailure:
                return None
            if value is None:
                return None
            return ScalarProperty(value, MavenFieldOrigin(source, 'project.version', MavenFieldBasis.DEFAULT))
    return None


def _profile_effects(root, source, model, context, imports):
    profiles = _container(root, 'profiles')
    if profiles is None:
        return
    if any(child.name != 'profile' for child in profiles.children):
        raise ValueError('unsupported profiles')
    entries = profiles.elements('profile')
    if len(entries) > MAX_PROFILES:
        raise ValueError('profile budget')
    ids = set()
    base = {record.key: record for record in model.dependencies}
    for profile in entries:
        relevant = any(child.name in ('modules', 'properties', 'dependencies', 'dependencyManagement')
                       for child in profile.children)
        allowed = {'id', 'activation', 'build', 'modules', 'distributionManagement', 'properties',
                   'dependencyManagement', 'dependencies', 'repositories', 'pluginRepositories',
                   'reports', 'reporting'}
        identity_writes = {'groupId', 'artifactId', 'version'}
        context.identity_variants.update(child.name for child in profile.children if child.name in identity_writes)
        if profile.text.strip() or any(child.name not in allowed | identity_writes for child in profile.children):
            raise ValueError('unsupported profile shape')
        identity = profile.scalar('id')
        if identity is None:
            identity = 'default'
        if relevant and (not identity or identity in ids):
            raise ValueError('ambiguous profile')
        if identity:
            ids.add(identity)
        props, blocked, unknown = read_properties(_container(profile, 'properties'), source)
        context.blocked_properties.update(props)
        context.blocked_properties.update(blocked)
        context.property_unknown |= unknown
        if unknown:
            context.trusted_properties.clear()
        if profile.elements('modules'):
            context.association_variable = True
        records, ambiguous, issues = _records(_container(profile, 'dependencies'), source)
        if ambiguous or any(problem.issue != ModelIssue.ARTIFACT for problem in issues):
            raise ValueError('unsupported profile dependencies')
        for record in records:
            if record.key not in base:
                context.extra_population = True
            for field in record.fields:
                current = base.get(record.key)
                previous = current.field(field.origin.field_name) if current else None
                if previous is None or previous.value != field.value:
                    context.direct_variants.add((record.key, field.origin.field_name))
        owner = _container(profile, 'dependencyManagement')
        if owner is not None and any(child.name != 'dependencies' for child in owner.children):
            raise ValueError('unsupported profile management')
        records, ambiguous, issues = _records(
            _container(owner, 'dependencies') if owner else None, source, True,
        )
        if any(problem.issue not in (ModelIssue.ARTIFACT, ModelIssue.DUPLICATE) for problem in issues):
            context.management_unknown = True
        context.managed_variants.update((key, name) for key in ambiguous for name in ('version', 'scope'))
        context.imports_unknown |= any(key.type == 'pom' for key in ambiguous)
        for record in records:
            imports.append(record)
            context.managed_variants.update((record.key, field.origin.field_name) for field in record.fields)


def _fact_context(graph, model):
    projects = {project.source_id: project for project in graph.projects}
    models = {item.context.source_id: item for item in graph.models}
    source = model.context.source_id
    parent = models[model.context.parent_sources[0]] if model.context.parent_sources else None
    context = _FactContext(
        properties={}, blocked_properties=set(), property_unknown=False, trusted_properties=set(),
        builtins={'project.version': _version_builtin(graph, model),
                  'project.parent.version': _version_builtin(graph, parent) if parent else None},
        direct_variants=set(), managed_variants=set(), unknown_profile=False,
        extra_population=False, association_variable=False,
        imports_unknown=not model.parent_chain_complete, management_unknown=False,
        identity_variants=set(),
    )
    imports = []
    for identity in (*reversed(model.context.parent_sources), source):
        project = projects[identity]
        root = project.snapshot.xml
        if identity == source and 'version' in context.identity_variants:
            context.builtins['project.parent.version'] = None
        for name in ('groupId', 'artifactId', 'version'):
            if not _absent(root, name):
                context.identity_variants.discard(name)
        try:
            props, blocked, unknown = read_properties(_container(root, 'properties'), identity)
            context.properties.update(props)
            context.blocked_properties.difference_update(props)
            context.blocked_properties.update(blocked)
            context.property_unknown |= unknown
            if unknown:
                context.trusted_properties.clear()
            elif context.property_unknown:
                context.trusted_properties.update(props)
            for key in blocked:
                context.properties.pop(key, None)
        except (MavenInputFailure, ValueError):
            context.property_unknown = True
            context.trusted_properties.clear()
        # A child-written field masks an ancestor profile's same-field write.
        for record in project.dependencies:
            for field in record.fields:
                context.direct_variants.discard((record.key, field.origin.field_name))
        for record in project.management:
            for field in record.fields:
                context.managed_variants.discard((record.key, field.origin.field_name))
        imports.extend(project.management)
        try:
            owner = _container(root, 'dependencyManagement')
            if owner is not None:
                if any(child.name != 'dependencies' for child in owner.children):
                    context.management_unknown = True
                _, ambiguous, issues = _records(_container(owner, 'dependencies'), identity, True)
                context.management_unknown |= any(
                    problem.issue not in (ModelIssue.ARTIFACT, ModelIssue.DUPLICATE) for problem in issues)
                context.managed_variants.update((key, name) for key in ambiguous for name in ('version', 'scope'))
                context.imports_unknown |= any(key.type == 'pom' for key in ambiguous)
        except (MavenInputFailure, ValueError):
            context.management_unknown = True
        try:
            _profile_effects(root, identity, model, context, imports)
        except (MavenInputFailure, ValueError):
            context.unknown_profile = True
            context.extra_population = True
            context.identity_variants.update(('groupId', 'artifactId', 'version'))
    if 'version' in context.identity_variants:
        context.builtins['project.version'] = None
    context.imports_unknown |= context.management_unknown
    for record in imports:
        if record.key.type == 'pom' and record.field('scope') is not None:
            try:
                scope, _ = context.expand(record.field('scope').value)
                context.imports_unknown |= scope == 'import'
            except PropertyFailure:
                context.imports_unknown = True
    return context


def _selected_field(record, managed, name, context):
    field = record.field(name)
    if field is not None:
        return field
    source = record.consumer_source
    if name == 'optional':
        return RawField('false', MavenFieldOrigin(source, name, MavenFieldBasis.DEFAULT))
    if managed is not None and not context.management_unknown:
        scope = managed.field('scope')
        try:
            ordinary = scope is None or context.expand(scope.value)[0] != 'import'
        except PropertyFailure:
            ordinary = False
        candidate = managed.field(name)
        if ordinary and candidate is not None and (
                not context.imports_unknown or (candidate.origin.source_id == source
                and candidate.origin.basis == MavenFieldBasis.CONSUMER_MANAGEMENT)):
            return candidate
    if name == 'scope' and not context.imports_unknown and not context.management_unknown:
        return RawField('compile', MavenFieldOrigin(source, name, MavenFieldBasis.DEFAULT))
    return None


def _safe_request(text):
    if text and text.isprintable() and len(text.encode('utf-8')) <= 16 * 1024:
        return text
    return None


def _declared_occurrence(record, managed, context):
    values = {}
    origins = []
    request = None
    for name in _FIELDS:
        field = _selected_field(record, managed, name, context)
        if name == 'version' and field is not None:
            request = _safe_request(field.value)
        if field is None:
            values[name] = None
            continue
        origins.append(field.origin)
        variant = ((record.key, name) in context.direct_variants or (
            record.field(name) is None and name != 'optional'
            and (record.key, name) in context.managed_variants))
        try:
            if context.unknown_profile or variant:
                raise PropertyFailure()
            values[name], property_origins = context.expand(field.value)
            origins.extend(property_origins)
        except PropertyFailure:
            values[name] = None
    version = values['version']
    identity_version = None
    if version is not None:
        if version.startswith('[') and version.endswith(']'):
            version = version[1:-1]
        try:
            parsed = parse_version(version)
            identity_version = parsed.exact
            if is_snapshot(parsed):
                version = None
        except VersionError:
            version = None
    scope = values['scope']
    if scope not in ('compile', 'runtime', 'test', 'provided', 'system'):
        scope = None
    optional = {'true': True, 'false': False}.get(values['optional'])
    reason = MavenReason.TIME_BASIS_UNAVAILABLE
    if version is None:
        reason = MavenReason.UNSUPPORTED_VERSION
    elif record.artifact_key is None or scope is None or optional is None:
        reason = MavenReason.UNSUPPORTED_MODEL
    fact = MavenVersionFact(MavenVersionBasis.DECLARED, request, version,
                            tuple(dict.fromkeys(origins)), reason=reason)
    row = MavenOccurrence(MavenOccurrenceKey(record.consumer_source, 'base_model', record.key),
                          record.artifact_key, scope, optional, declared=fact)
    return row, identity_version


def _population_supported(graph, model):
    if not model.parent_chain_complete:
        return False
    projects = {project.source_id: project for project in graph.projects}
    expected_keys = set()
    for source in (model.context.source_id, *model.context.parent_sources):
        root = projects[source].snapshot.xml
        try:
            if any(child.name not in _PROJECT_ELEMENTS for child in root.children):
                return False
            _, ambiguous, issues = _records(_container(root, 'dependencies'), source)
            if ambiguous or any(problem.issue != ModelIssue.ARTIFACT for problem in issues):
                return False
            expected_keys.update(record.key for record in projects[source].dependencies)
        except (MavenInputFailure, ValueError):
            return False
    expected_keys.difference_update(model.ambiguous_dependencies)
    return len(expected_keys) == len(model.dependencies)


def _possible_associations(graph):
    """Retain incoming conditional module edges without activating profiles.

    Unknown paths can name any observed source. Missing literal targets add an
    unknown member only to the affected possible component. Neither case changes
    the independently certified emptiness of a source with no requirements.
    """
    sources = {project.source_id for project in graph.projects}
    neighbours = {source: set() for source in sources}
    uncertain = set()
    unknown_members = set()
    for component in graph.aggregations:
        for source in component.source_ids:
            neighbours[source].update(set(component.source_ids) - {source})
        if not component.complete:
            uncertain.update(component.source_ids)
    for project in graph.projects:
        source = project.source_id
        if project.snapshot is None:
            continue
        root = project.snapshot.xml
        try:
            containers = [(root, False)]
            profiles = _container(root, 'profiles')
            if profiles is not None:
                if any(child.name != 'profile' for child in profiles.children):
                    raise ValueError('unsupported possible modules')
                containers.extend((profile, True) for profile in profiles.elements('profile'))
            for owner, conditional in containers:
                container = _container(owner, 'modules')
                if container is None:
                    continue
                if conditional:
                    uncertain.add(source)
                if any(child.name != 'module' for child in container.children):
                    raise ValueError('unsupported possible module')
                for entry in container.elements('module'):
                    if entry.children:
                        raise ValueError('unsupported possible module')
                    target = _edge_target(source, entry.text.strip(), directory=True)
                    if target is None:
                        raise ValueError('unknown possible module path')
                    if target in sources:
                        neighbours[source].add(target)
                        neighbours[target].add(source)
                    else:
                        uncertain.add(source)
                        unknown_members.add(source)
        except (MavenInputFailure, ValueError):
            neighbours[source].update(sources - {source})
            for other in sources - {source}:
                neighbours[other].add(source)
            uncertain.add(source)
            unknown_members.add(source)
    result = {}
    remaining = set(sources)
    while remaining:
        pending = [min(remaining)]
        members = set()
        while pending:
            source = pending.pop()
            if source not in members:
                members.add(source)
                pending.extend(neighbours[source] - members)
        remaining -= members
        for source in members:
            result[source] = (tuple(sorted(members)), not bool(members & uncertain),
                              bool(members & unknown_members))
    return result


def declared_sources(graph: MavenProjectGraph) -> tuple[MavenSource, ...]:
    """Establish supported external occurrences; no source admission or HTTP.

    Unknown population retains safely attributable rows. Version/policy/date
    refusal never turns an otherwise known external identity into a missing row.
    """
    models = {model.context.source_id: model for model in graph.models}
    contexts = {model.context.source_id: _fact_context(graph, model) for model in graph.models
                if next(project for project in graph.projects
                        if project.source_id == model.context.source_id).snapshot is not None}
    associations = _possible_associations(graph)
    sources = []
    for model in graph.models:
        source = model.context.source_id
        project = next(project for project in graph.projects if project.source_id == source)
        if project.snapshot is None:
            collection = MavenCollection(MavenView.DECLARED, None, (), False, MavenReason.UNSUPPORTED_MODEL)
            sources.append(MavenSource(model.context, collection))
            continue
        context = contexts[source]
        complete = _population_supported(graph, model) and not context.extra_population
        # Uncertain membership considers all observed project candidates; an
        # unrelated complete component never excludes a co-located namesake.
        candidates, association_certain, unknown_member = associations[source]
        managed = {record.key: record for record in model.management}
        rows = []
        for record in model.dependencies:
            row, identity_version = _declared_occurrence(record, managed.get(record.key), context)
            possible = []
            for identity in candidates:
                candidate = models[identity].identity
                candidate_context = contexts.get(identity)
                if candidate_context is not None:
                    changes = {name: None for name, field in (
                        ('group_id', 'groupId'), ('artifact_id', 'artifactId'), ('version', 'version'))
                        if field in candidate_context.identity_variants}
                    candidate = replace(candidate, **changes)
                if (candidate.group_id in (None, record.key.group_id)
                        and candidate.artifact_id in (None, record.key.artifact_id)):
                    possible.append(candidate)
            if unknown_member:
                possible.append(ProjectIdentity(None, None, None))
            if possible:
                if identity_version is None or any(identity.version is None for identity in possible):
                    complete = False
                    continue
                if any(identity.version == identity_version for identity in possible):
                    if not association_certain:
                        complete = False
                    continue
            rows.append(row)
        collection = MavenCollection(MavenView.DECLARED, len(rows) if complete else None,
                                     tuple(rows), bool(rows) or complete,
                                     None if complete else MavenReason.POPULATION_UNKNOWN)
        sources.append(MavenSource(model.context, collection))
    return tuple(sources)
