"""Explicit accepted static management field proofs, never a Maven evaluator.

Composition facts are pinned to Maven 3.9.11; see the prospective contract in
maintenance/maven-external-intake and the Apache attribution in third_party.
External models never enter the repository discovery/population/policy graph.
"""

import base64
import binascii
from dataclasses import dataclass, replace
import hashlib
import json
from pathlib import Path
import re

from .maven_input import MavenInputFailure, MavenInputReader, MavenInputSnapshot, parse_pom, relative_parts
from .maven_model import MavenFieldBasis, MavenFieldOrigin, MavenModelKey, MavenReason
from .maven_project import (
    ModelIssue, _PROJECT_ELEMENTS, _container, _edge_target, _literal,
    _parse_project, _records,
)
from .maven_properties import PropertyFailure, ScalarProperty, expand_scalar, read_properties

BASIS = 'restricted_static_maven_3_9_11_v1'
SCOPE_BASIS = 'accepted_external_management_static_v1'
LIMITATIONS = ('external_applicability_explicitly_accepted', 'static_model_incomplete',
               'successful_build_not_established', 'historical_resolution_not_established',
               'observed_selection_not_established')
MAX_BUILDS = 128
MAX_TOTAL_BUILDS = 10000
_HASH = re.compile('[0-9a-f]{64}', re.ASCII)


class MavenManagementRequestError(ValueError):
    def __init__(self):
        super().__init__('invalid Maven management evidence')


class ProofFailure(ValueError):
    """A refused field proof, with no supplied diagnostic payload."""


@dataclass(frozen=True)
class AcceptedDocument:
    gav: tuple[str, str, str]
    roles: tuple[str, ...]
    project: object


@dataclass(frozen=True)
class ConsumerGrant:
    source_id: str
    bindings: tuple[tuple[str, str], ...]
    keys: tuple[MavenModelKey, ...]


@dataclass(frozen=True)
class AcceptedManagement:
    documents: tuple[AcceptedDocument, ...]
    consumers: tuple[ConsumerGrant, ...]


def _object(value, keys):
    if type(value) is not dict or set(value) != set(keys):
        raise MavenManagementRequestError()


def _hash(value):
    if type(value) is not str or not _HASH.fullmatch(value):
        raise MavenManagementRequestError()
    return value


def _source(value):
    if type(value) is not str or not value.endswith('.xml'):
        raise MavenManagementRequestError()
    relative_parts(value)
    return value


def _gav(value):
    if type(value) is not list or len(value) != 3:
        raise MavenManagementRequestError()
    for text, kind in zip(value, ('groupId', 'artifactId', 'version')):
        if type(text) is not str or _literal(text, kind) != text:
            raise MavenManagementRequestError()
    return tuple(value)


def _unique_members(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise MavenManagementRequestError()
        result[key] = value
    return result


def _invalid_constant(unused):
    raise MavenManagementRequestError()


def _json(data):
    if type(data) is not bytes or len(data) > 4 * 1024 * 1024:
        raise MavenManagementRequestError()
    text = data.decode('utf-8')
    # Check nesting before the JSON decoder can recurse. Brackets inside strings
    # have no structural meaning; malformed escaping is subsequently rejected.
    depth = 0
    quoted = escaped = False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in '[{':
            depth += 1
            if depth > 16:
                raise MavenManagementRequestError()
        elif char in ']}':
            depth -= 1
    value = json.loads(text, object_pairs_hook=_unique_members,
                       parse_constant=_invalid_constant)
    pending = [value]
    nodes = 0
    while pending:
        item = pending.pop()
        if type(item) in (dict, list):
            nodes += 1
            pending.extend(item.values() if type(item) is dict else item)
            if type(item) is dict:
                pending.extend(item.keys())
        elif type(item) is str and len(item.encode('utf-8')) > 3 * 1024 * 1024:
            raise MavenManagementRequestError()
        if nodes > 20000:
            raise MavenManagementRequestError()
    return value


def decode_management(data: bytes) -> AcceptedManagement:
    """Validate a whole supplied envelope; never read a referenced file or URL."""
    try:
        value = _json(data)
        _object(value, ('schema_version', 'basis', 'documents', 'consumers'))
        if type(value['schema_version']) is not int or value['schema_version'] != 1 or value['basis'] != BASIS:
            raise MavenManagementRequestError()
        documents = value['documents']
        consumers = value['consumers']
        if (type(documents) is not list or not 1 <= len(documents) <= 64
                or type(consumers) is not list or not 1 <= len(consumers) <= 100):
            raise MavenManagementRequestError()
        accepted = []
        identities = set()
        total = 0
        for index, document in enumerate(documents):
            _object(document, ('gav', 'roles', 'sha256', 'content_base64'))
            gav = _gav(document['gav'])
            roles = document['roles']
            if (type(roles) is not list or not roles or any(type(r) is not str for r in roles)
                    or len(set(roles)) != len(roles) or not set(roles) <= {'parent', 'bom'}
                    or gav in identities or type(document['content_base64']) is not str):
                raise MavenManagementRequestError()
            identities.add(gav)
            raw = base64.b64decode(document['content_base64'], validate=True)
            total += len(raw)
            if total > 2 * 1024 * 1024 or hashlib.sha256(raw).hexdigest() != _hash(document['sha256']):
                raise MavenManagementRequestError()
            source = f'_external/{index}.xml'
            project = _parse_project(source, MavenInputSnapshot(source, raw, (), parse_pom(raw)))
            identity = project.identity
            inherited = project.parent.identity if project.parent else None
            actual = (identity.group_id or (inherited.group_id if inherited else None),
                      identity.artifact_id, identity.version or (inherited.version if inherited else None))
            if actual != gav or any(p.issue == ModelIssue.IDENTITY for p in project.problems):
                raise MavenManagementRequestError()
            accepted.append(AcceptedDocument(gav, tuple(roles), project))
        grants = []
        sources = set()
        count = 0
        for consumer in consumers:
            _object(consumer, ('source_id', 'context_id', 'bindings', 'keys'))
            source = _source(consumer['source_id'])
            if source in sources or consumer['context_id'] != 'base_model':
                raise MavenManagementRequestError()
            sources.add(source)
            bindings = consumer['bindings']
            if type(bindings) is not dict or not 1 <= len(bindings) <= 16:
                raise MavenManagementRequestError()
            bindings = tuple((_source(k), _hash(v)) for k, v in bindings.items())
            keys = consumer['keys']
            if type(keys) is not list or not keys:
                raise MavenManagementRequestError()
            parsed = []
            for key in keys:
                _object(key, ('group_id', 'artifact_id', 'type', 'classifier'))
                for name, kind in (('group_id', 'groupId'), ('artifact_id', 'artifactId'), ('type', 'type')):
                    if type(key[name]) is not str or _literal(key[name], kind) != key[name]:
                        raise MavenManagementRequestError()
                classifier = key['classifier']
                if classifier is not None and (type(classifier) is not str or _literal(classifier, 'classifier') != classifier):
                    raise MavenManagementRequestError()
                parsed.append(MavenModelKey(**key))
            count += len(parsed)
            if len(set(parsed)) != len(parsed) or count > 10000:
                raise MavenManagementRequestError()
            grants.append(ConsumerGrant(source, bindings, tuple(parsed)))
        return AcceptedManagement(tuple(accepted), tuple(grants))
    except (ValueError, TypeError, KeyError, UnicodeError, binascii.Error, MavenInputFailure, RecursionError):
        raise MavenManagementRequestError() from None


def load_management(path) -> AcceptedManagement:
    """Read exactly the nominated regular file with existing safe host primitives."""
    try:
        selected = Path(path)
        with MavenInputReader(selected.parent) as reader:
            snapshot = reader.snapshot_evidence(selected.name)
        return decode_management(snapshot.data)
    except (OSError, ValueError, MavenInputFailure):
        raise MavenManagementRequestError() from None


@dataclass(frozen=True)
class ScopeProof:
    scope: str
    comparison_allowed: bool


class ManagementProofs:
    """Bounded, per-occurrence dominance proofs. No positive-result cache."""

    def __init__(self, graph, accepted):
        self.projects = {p.source_id: p for p in graph.projects}
        self.documents = {d.gav: d for d in accepted.documents}
        self.grants = {g.source_id: g for g in accepted.consumers}
        self.total_builds = 0
        self.builds = 0

    def requested(self, row):
        grant = self.grants.get(row.key.source_id)
        return grant is not None and row.key.model_key in grant.keys

    def _budget(self):
        self.builds += 1
        self.total_builds += 1
        if self.builds > MAX_BUILDS or self.total_builds > MAX_TOTAL_BUILDS:
            raise ProofFailure()

    def _lineage(self, project, bindings, trail=()):
        self._budget()
        if project.source_id in trail or len(trail) >= 16 or project.snapshot is None:
            raise ProofFailure()
        external = project.source_id.startswith('_external/') and project not in self.projects.values()
        if not external and bindings.get(project.source_id) != hashlib.sha256(project.snapshot.data).hexdigest():
            raise ProofFailure()
        if not project.parent_supported:
            raise ProofFailure()
        if project.parent is None:
            return [project]
        reference = project.parent
        gav = reference.identity.gav
        if gav is None:
            raise ProofFailure()
        candidate = None
        if not external and reference.relative_path != '':
            path = reference.relative_path if reference.relative_path is not None else '../pom.xml'
            target = _edge_target(project.source_id, path)
            if target not in self.projects:
                target = _edge_target(project.source_id, path, directory=True)
            candidate = self.projects.get(target)
        if candidate is None:
            document = self.documents.get(gav)
            if document is None or 'parent' not in document.roles:
                raise ProofFailure()
            candidate = document.project
        identity = candidate.identity
        parent = candidate.parent.identity if candidate.parent else None
        actual = (identity.group_id or (parent.group_id if parent else None), identity.artifact_id,
                  identity.version or (parent.version if parent else None))
        if actual != gav:
            raise ProofFailure()
        return [project, *self._lineage(candidate, bindings, (*trail, project.source_id))]

    def _context(self, chain, key):
        properties = {}
        blocked = set()
        for project in reversed(chain):
            root = project.snapshot.xml
            if (any(c.name not in _PROJECT_ELEMENTS for c in root.children)
                    or any(p.issue not in (ModelIssue.ARTIFACT,) for p in project.problems)):
                raise ProofFailure()
            props, bad, unknown = read_properties(_container(root, 'properties'), project.source_id)
            if unknown:
                raise ProofFailure()
            properties.update(props)
            blocked.difference_update(props)
            blocked.update(bad)
            for name in bad:
                properties.pop(name, None)
            profiles = _container(root, 'profiles')
            if profiles is not None:
                if len(profiles.children) > 128 or any(c.name != 'profile' for c in profiles.children):
                    raise ProofFailure()
                for profile in profiles.children:
                    allowed = {'id', 'activation', 'dependencies', 'build', 'repositories',
                               'pluginRepositories', 'distributionManagement', 'modules', 'reports', 'reporting'}
                    if profile.text.strip() or any(c.name not in allowed for c in profile.children):
                        raise ProofFailure()
                    records, ambiguous, issues = _records(_container(profile, 'dependencies'), project.source_id)
                    if ambiguous or issues or any(r.key == key for r in records):
                        raise ProofFailure()
        builtins = {}
        for name, lineage in (('project.version', chain), ('project.parent.version', chain[1:])):
            value = next((p.identity.version for p in lineage if p.identity.version is not None), None)
            builtins[name] = None if value is None else ScalarProperty(
                value, MavenFieldOrigin(chain[0].source_id, name, MavenFieldBasis.DEFAULT))
        return lambda text: expand_scalar(text, properties, builtins, blocked)[0]

    def _management(self, chain):
        records = {}
        for project in chain:
            for record in project.management:
                records.setdefault(record.key, record)
        return tuple(records.values())

    def _winner(self, project, key, bindings, trail=()):
        if project.source_id in trail or len(trail) >= 16:
            raise ProofFailure()
        chain = self._lineage(project, bindings)
        expand = self._context(chain, key)
        records = self._management(chain)
        # A whole winning key shields even uninterpretable losing imports.
        for record in records:
            if record.key == key:
                field = record.field('scope')
                scope = expand(field.value) if field else None
                if not (record.key.type == 'pom' and scope == 'import'):
                    return True, scope
        imports = []
        for record in records:
            if record.key.type == 'pom':
                field = record.field('scope')
                scope = expand(field.value) if field else None
                if scope == 'import':
                    imports.append(record)
        for record in imports:
            field = record.field('version')
            if field is None or record.key.classifier is not None:
                raise ProofFailure()
            gav = (record.key.group_id, record.key.artifact_id, expand(field.value))
            document = self.documents.get(gav)
            if document is None or 'bom' not in document.roles:
                raise ProofFailure()
            found, scope = self._winner(document.project, key, bindings, (*trail, project.source_id))
            if found:
                return found, scope
        return False, None

    def scope(self, row):
        self.builds = 0
        if (not self.requested(row) or row.key.context_id != 'base_model'
                or row.scope is not None or row.artifact_key is None or row.optional is None
                or row.declared is None or row.declared.version is None
                or row.declared.reason != MavenReason.UNSUPPORTED_MODEL):
            return None
        try:
            grant = self.grants[row.key.source_id]
            bindings = dict(grant.bindings)
            chain = self._lineage(self.projects[row.key.source_id], bindings)
            expand = self._context(chain, row.key.model_key)
            ordinary = [r for p in chain for r in p.dependencies if r.key == row.key.model_key]
            if len(ordinary) != 1 or ordinary[0].field('scope') is not None:
                raise ProofFailure()
            version = ordinary[0].field('version')
            if version is None or expand(version.value) != row.declared.version:
                raise ProofFailure()
            _, scope = self._winner(chain[0], row.key.model_key, bindings)
            # A successful traversal with no key proves absence only because every
            # earlier import was examined. An absent document always raises above.
            scope = scope or 'compile'
            if scope not in ('compile', 'runtime', 'test', 'provided', 'system'):
                raise ProofFailure()
            allowed = True
            for project in chain:
                if project in self.projects.values():
                    continue
                root = project.snapshot.xml
                if root.elements('repositories'):
                    allowed = False
                profiles = _container(root, 'profiles')
                if profiles and any(p.elements('repositories') for p in profiles.children):
                    allowed = False
            return ScopeProof(scope, allowed)
        except (ValueError, MavenInputFailure, KeyError, PropertyFailure):
            return None


def apply_management(graph, sources, accepted):
    """Fill only eligible listed scopes; retain all other facts and populations."""
    proofs = ManagementProofs(graph, accepted)
    results = []
    for source in sources:
        rows = []
        for row in source.declared.rows:
            if proofs.requested(row):
                proof = proofs.scope(row)
                if proof is None:
                    row = replace(row, management_status='refused')
                else:
                    reason = (MavenReason.TIME_BASIS_UNAVAILABLE if proof.comparison_allowed
                              else MavenReason.POLICY_UNKNOWN)
                    row = replace(row, scope=proof.scope, management_status='accepted',
                                  declared=replace(row.declared, reason=reason))
            rows.append(row)
        results.append(replace(source, declared=replace(source.declared, rows=tuple(rows))))
    return tuple(results)
