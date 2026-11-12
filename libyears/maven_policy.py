"""Bounded local Central convention admission; never repository acquisition.

The grammar is Feature 007 source-policy B3–B5, not an effective Maven model.
Only safe staged XML and the exact local sentinel reader supply evidence here.
No URL, property value or settings diagnostic escapes this module.
"""

from dataclasses import dataclass
import re
from urllib.parse import urlsplit

from .maven_input import MavenInputFailure, MavenInputIssue
from .maven_model import MavenReason

MAX_POLICY_RECORDS = 1024
MAX_PROFILES = 128
MAX_MIRRORS = 64
_ID = re.compile(r'[A-Za-z0-9_.-]{1,128}', re.ASCII)
_SETTINGS_NS = (None, *(f'http://maven.apache.org/SETTINGS/1.{n}.0' for n in range(3)))
_EXTENSIONS_NS = (None, 'http://maven.apache.org/EXTENSIONS/1.0.0',
                  'http://maven.apache.org/EXTENSIONS/1.1.0')
# Apache Maven 3.9.11 model-reference field names, ASF / Apache-2.0.
# Extracted facts and attribution: third_party/maven-3.9.11/policy-facts.json.
_BUILD_ELEMENTS = frozenset({
    'sourceDirectory', 'scriptSourceDirectory', 'testSourceDirectory', 'outputDirectory',
    'testOutputDirectory', 'extensions', 'defaultGoal', 'resources', 'testResources',
    'directory', 'finalName', 'filters', 'pluginManagement', 'plugins',
})
_PROFILE_ELEMENTS = frozenset({
    'id', 'activation', 'build', 'modules', 'distributionManagement', 'properties',
    'dependencyManagement', 'dependencies', 'repositories', 'pluginRepositories',
    'reports', 'reporting', 'groupId', 'artifactId', 'version',
})



class PolicyFailure(ValueError):
    def __init__(self, reason=MavenReason.POLICY_UNKNOWN):
        self.reason = reason
        super().__init__(reason.value)


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    reason: MavenReason | None = None

    @property
    def admitted(self):
        return self.reason is None


@dataclass
class _Budget:
    records: int = 0

    def add(self, count=1):
        self.records += count
        if self.records > MAX_POLICY_RECORDS:
            raise PolicyFailure(MavenReason.POLICY_BUDGET_EXCEEDED)


def _container(node, name):
    items = node.elements(name)
    if len(items) > 1:
        raise PolicyFailure()
    if not items:
        return None
    if items[0].text.strip():
        raise PolicyFailure()
    return items[0]


def _fields(node, names):
    if node.text.strip() or any(c.namespace != node.namespace or c.attributes
                                or c.name not in names for c in node.children):
        raise PolicyFailure()


def _scalar(node, name):
    value = node.scalar(name)
    return value.strip() if value is not None else None


def _boolean(value, default):
    if value is None:
        return default
    if value not in ('true', 'false'):
        raise PolicyFailure()
    return value == 'true'


def central_url(value):
    """Recognize only literal public identity; the URL is never a request target."""
    if not value or len(value) > 2048 or any(c.isspace() for c in value):
        return False
    try:
        parsed = urlsplit(value)
        return (parsed.scheme == 'https' and parsed.hostname is not None
                and parsed.hostname.lower() in ('repo.maven.apache.org', 'repo1.maven.org')
                and parsed.username is None and parsed.password is None
                and parsed.netloc.lower() in ('repo.maven.apache.org', 'repo.maven.apache.org:443',
                                             'repo1.maven.org', 'repo1.maven.org:443')
                and parsed.port in (None, 443) and not parsed.query and not parsed.fragment
                and '?' not in value and '#' not in value
                and parsed.path in ('/maven2', '/maven2/'))
    except ValueError:
        return False


def _repositories(node, budget):
    container = _container(node, 'repositories')
    if container is None:
        return {}
    _fields(container, {'repository'})
    records = {}
    for record in container.children:
        budget.add()
        identity = _scalar(record, 'id')
        if identity is None or not _ID.fullmatch(identity):
            raise PolicyFailure()
        # Retain ambiguity at this ID. Only effective/possible Central can veto;
        # a child whole-record replacement can also suppress an ancestor ambiguity.
        records[identity] = None if identity in records else record
    return records


def _central_record(record):
    if record is None:
        raise PolicyFailure()
    _fields(record, {'id', 'url', 'name', 'layout', 'releases', 'snapshots'})
    if not central_url(_scalar(record, 'url')):
        raise PolicyFailure(MavenReason.COMPARATOR_REFUSED)
    if _scalar(record, 'layout') not in (None, 'default'):
        raise PolicyFailure()
    # Name and both policy blocks must have supported scalar framing.
    _scalar(record, 'name')
    for name in ('releases', 'snapshots'):
        policy = _container(record, name)
        if policy is None:
            continue
        _fields(policy, {'enabled', 'updatePolicy', 'checksumPolicy'})
        enabled = _boolean(_scalar(policy, 'enabled'), True)
        _scalar(policy, 'updatePolicy')
        _scalar(policy, 'checksumPolicy')
        if name == 'releases' and not enabled:
            raise PolicyFailure(MavenReason.COMPARATOR_REFUSED)


def _profiles(node, budget):
    container = _container(node, 'profiles')
    if container is None:
        return ()
    _fields(container, {'profile'})
    if len(container.children) > MAX_PROFILES:
        raise PolicyFailure(MavenReason.POLICY_BUDGET_EXCEEDED)
    seen = set()
    for profile in container.children:
        budget.add()
        identity = _scalar(profile, 'id')
        # Maven's absent profile ID is the literal default; duplicates remain unknown.
        identity = 'default' if identity is None else identity
        if not _ID.fullmatch(identity) or identity in seen:
            raise PolicyFailure()
        seen.add(identity)
    return container.children


def _known_children(node, names):
    # Names only: unrelated plugin/reporting/descriptive subtrees stay inert.
    # Interpreted fields receive their own namespace/attribute/scalar checks.
    if node.text.strip() or any(child.name not in names for child in node.children):
        raise PolicyFailure()


def _extensions(node):
    build = _container(node, 'build')
    if build is None:
        return
    _known_children(build, _BUILD_ELEMENTS)
    extensions = _container(build, 'extensions')
    if extensions is not None and extensions.children:
        raise PolicyFailure()
    parents = [build]
    managed = _container(build, 'pluginManagement')
    if managed is not None:
        _known_children(managed, {'plugins'})
        parents.append(managed)
    for parent in parents:
        plugins = _container(parent, 'plugins')
        if plugins is None:
            continue
        _fields(plugins, {'plugin'})
        for plugin in plugins.children:
            if _boolean(_scalar(plugin, 'extensions'), False):
                raise PolicyFailure()


def _policy_properties(node, budget):
    from .maven_launch import relevant_property

    properties = _container(node, 'properties')
    if properties is not None:
        for child in properties.children:
            if relevant_property(child.name):
                budget.add()
                raise PolicyFailure()


def _model_policy(roots, budget):
    from .maven_project import _PROJECT_ELEMENTS

    effective = {}
    for root in roots:  # nearest consumer first; repository records never field merge
        _known_children(root, _PROJECT_ELEMENTS)
        for identity, record in _repositories(root, budget).items():
            effective.setdefault(identity, record)
        _extensions(root)
        _policy_properties(root, budget)
        for profile in _profiles(root, budget):
            _known_children(profile, _PROFILE_ELEMENTS)
            _extensions(profile)
            _policy_properties(profile, budget)
            possible = _repositories(profile, budget)
            if 'central' in possible:
                _central_record(possible['central'])
    if 'central' in effective:
        _central_record(effective['central'])


def _pattern(value, target, *, layouts=False):
    """Pinned explicit include/exclude precedence, not shell/regex matching."""
    if value is None or len(value) > 2048:
        raise PolicyFailure()
    tokens = value.split(',')
    for token in tokens:
        if token == '*' or (not layouts and token in ('external:*', 'external:http:*')):
            continue
        identity = token[1:] if token.startswith('!') else token
        if not _ID.fullmatch(identity):
            raise PolicyFailure()
    result = False
    for token in tokens:
        if token == target:
            return True
        if token == '!' + target:
            return False
        if token == '*' or (not layouts and token == 'external:*'):
            result = True
    return result



def _mirrors(settings, budget):
    container = _container(settings, 'mirrors')
    if container is None:
        return
    _fields(container, {'mirror'})
    if len(container.children) > MAX_MIRRORS:
        raise PolicyFailure(MavenReason.POLICY_BUDGET_EXCEEDED)
    seen = set()
    possible = []
    for mirror in container.children:
        budget.add()
        identity = _scalar(mirror, 'id')
        if identity is None or not _ID.fullmatch(identity) or identity in seen:
            raise PolicyFailure()
        seen.add(identity)
        expression = mirror.scalar('mirrorOf')
        if not _pattern(expression, 'central'):
            continue  # unrelated URL/block/layout cannot affect Central
        layouts = mirror.scalar('mirrorOfLayouts')
        if not _pattern('default,legacy' if layouts is None else layouts,
                        'default', layouts=True):
            continue
        possible.append((expression == 'central', mirror))
    # Exact whole ID wins over patterns, otherwise retain declaration order.
    exact = next((mirror for is_exact, mirror in possible if is_exact), None)
    selected = exact if exact is not None else next((m for _, m in possible), None)
    if selected is None:
        return
    _fields(selected, {'id', 'name', 'url', 'layout', 'mirrorOf', 'mirrorOfLayouts', 'blocked'})
    url = _scalar(selected, 'url')
    if not url or len(url) > 2048 or '${' in url:
        raise PolicyFailure()
    if _scalar(selected, 'layout') not in (None, 'default'):
        raise PolicyFailure()
    _scalar(selected, 'name')
    if _boolean(_scalar(selected, 'blocked'), False):
        raise PolicyFailure(MavenReason.COMPARATOR_REFUSED)


def _settings(root, budget):
    if root.name != 'settings' or root.namespace not in _SETTINGS_NS:
        raise PolicyFailure()
    _root_attributes(root)
    _fields(root, {'mirrors', 'profiles', 'activeProfiles', 'pluginGroups',
                   'localRepository', 'interactiveMode', 'usePluginRegistry',
                   'offline', 'servers', 'proxies'})
    for name in ('servers', 'proxies'):
        container = _container(root, name)
        if container is not None and container.children:
            raise PolicyFailure()  # do not inspect credential-bearing contents
    for name in ('localRepository', 'interactiveMode', 'usePluginRegistry'):
        _scalar(root, name)
    for name, child_name in (('activeProfiles', 'activeProfile'), ('pluginGroups', 'pluginGroup')):
        container = _container(root, name)
        if container is not None:
            _fields(container, {child_name})
            for child in container.children:
                budget.add()
                if child.children:
                    raise PolicyFailure()
    if _boolean(_scalar(root, 'offline'), False):
        raise PolicyFailure(MavenReason.COMPARATOR_REFUSED)
    for profile in _profiles(root, budget):
        _fields(profile, {'id', 'activation', 'properties', 'repositories', 'pluginRepositories'})
        _policy_properties(profile, budget)
        records = _repositories(profile, budget)
        if 'central' in records:
            _central_record(records['central'])
    _mirrors(root, budget)


def _root_attributes(root):
    allowed = {'http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
               'http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation'}
    if any(name not in allowed for name, value in root.attributes):
        raise PolicyFailure()


def _sentinel_extensions(root):
    if root.name != 'extensions' or root.namespace not in _EXTENSIONS_NS:
        raise PolicyFailure()
    _root_attributes(root)
    if root.children or root.text.strip():
        raise PolicyFailure()


def _ancestors(source_ids):
    directories = {''}
    for source in source_ids:
        parts = source.split('/')[:-1]
        directories.update('/'.join(parts[:i]) for i in range(1, len(parts) + 1))
    return sorted(directories)


def source_policy(graph, source_id, reader):
    """Evaluate staged consumer/accepted-parent and exact local launch evidence.

    Reader access is restricted to presence checks, fixed sentinels and the single
    explicitly selected contained settings snapshot. No arbitrary file is opened.
    """
    from .maven_launch import launch_arguments, jvm_arguments

    try:
        models = {model.context.source_id: model for model in graph.models}
        projects = {project.source_id: project for project in graph.projects}
        model = models[source_id]
        sources = (source_id, *model.context.parent_sources)
        roots = []
        for source in sources:
            snapshot = projects[source].snapshot
            if snapshot is None:
                raise PolicyFailure()
            roots.append(snapshot.xml)
        budget = _Budget()
        _model_policy(roots, budget)
        selected = None
        settings_sentinels = []
        for directory in _ancestors(sources):
            prefix = directory + '/' if directory else ''
            config = prefix + '.mvn/maven.config'
            if reader.control_present(config):
                snapshot = reader.snapshot_control(config)
                path = launch_arguments(snapshot.data, allow_settings=not directory)
                if path is not None:
                    selected = path
            jvm = prefix + '.mvn/jvm.config'
            if reader.control_present(jvm):
                jvm_arguments(reader.snapshot_control(jvm).data)
            extensions = prefix + '.mvn/extensions.xml'
            if reader.control_present(extensions):
                _sentinel_extensions(reader.snapshot_control(extensions).xml)
            settings = prefix + '.mvn/settings.xml'
            if reader.control_present(settings):
                settings_sentinels.append(settings)
        if any(path != selected for path in settings_sentinels):
            raise PolicyFailure()
        if selected is not None:
            snapshot = reader.snapshot_selected_settings(selected)
            if snapshot.source_id != selected or snapshot.xml is None:
                raise PolicyFailure()
            _settings(snapshot.xml, budget)
        return PolicyDecision()
    except PolicyFailure as failure:
        return PolicyDecision(failure.reason)
    except MavenInputFailure as failure:
        if failure.issue == MavenInputIssue.LIMIT:
            return PolicyDecision(MavenReason.POLICY_BUDGET_EXCEEDED)
        return PolicyDecision(MavenReason.POLICY_INPUT_UNAVAILABLE)
