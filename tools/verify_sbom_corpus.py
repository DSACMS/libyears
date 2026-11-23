"""Explicit offline acceptance of the previously retained Feature008 corpus.

No acquisition or production transport. Supply the authorized retained directory
and an output directory. Resulting ages use synthetic catalogues and POM dates;
only the original document bytes and document-derived counts are real evidence.
"""

import argparse
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from functools import partial
import io
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from libyears.cli import main as libyears_main
from libyears.maven import MavenCapability
from libyears.maven_input import parse_pom
from libyears.maven_model import MavenReason
from libyears.maven_registry import MavenRepresentation, MavenTarget, MavenPomDate, select_target, pom_date
from libyears.scan import scan_mixed_repository
from libyears.sbom_input import SbomInputReader
from libyears.sbom_model import SbomRequest

# Original public bytes bound in discovery/sbom-corpus-feasibility.md and the
# original007-0047 durable freeze. Never fetch or reconstruct a missing input.
CORPUS = {
    'dt-cyclonedx.json': 'c201f3a64e7b2c510b83fe99dd6e945244030c6484009100b04a257721dba790',
    'dt-pom-pinned.json': 'c2a343d6abc4a7562d04040e99fe94c777924de2dd7f6915472288dff9a198ee',
    'cpython-release.json': 'feba258898139ca77b6421e80cba8fa7edd4cf29809bb545c32aadd404142e36',
    'cpython-sbom.json': '1ef5cc95d8b527b42030636359dd737ed8fcb255f42ea04478b2cd2b1129bb76',
    'commons-lang-github.json': 'afd5dbe6b7bf559ed80331b3744446dfffff73654a73b9b3e11e129651d4a868',
    'requests-github.json': 'f56c65db64f0a1520aa84619b6ac2e9e8d4addd03d1ce7541543862e9e1e26a2',
}
OLD = datetime(2021, 1, 1, tzinfo=timezone.utc)
NEW = OLD + timedelta(days=365.25)
RETRIEVED = datetime(2026, 11, 20, tzinfo=timezone.utc)


class ControlledMetadata:
    """Synthetic fixed-host metadata responses parsed by the existing adapter."""

    def __init__(self, capabilities, *, unavailable=False, ca_bundle=None):
        if any(type(cap) is not MavenCapability for cap in capabilities):
            raise ValueError('unexpected capability type')
        self.capabilities = frozenset(capabilities)
        self.gas = sorted({(cap.group_id, cap.artifact_id) for cap in capabilities})
        self.unavailable = unavailable
        self.targets = {}
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        self.closed = True

    def select_target(self, cap):
        if cap not in self.capabilities:
            raise ValueError('unadmitted metadata operation')
        ga = (cap.group_id, cap.artifact_id)
        if self.unavailable or ga == self.gas[0]:
            reason = MavenReason.METADATA_WORKER_UNAVAILABLE if self.unavailable else MavenReason.CATALOGUE_UNAVAILABLE
            return MavenTarget(*ga, None, RETRIEVED, reason)
        versions = sorted({c.version for c in self.capabilities if (c.group_id, c.artifact_id) == ga} | {'9999.0'})
        body = ('<metadata><groupId>' + cap.group_id + '</groupId><artifactId>' + cap.artifact_id +
                '</artifactId><versioning><versions>' + ''.join('<version>' + escape(v) + '</version>' for v in versions) +
                '</versions></versioning></metadata>').encode()
        target = select_target(*ga, MavenRepresentation(200, body, (), RETRIEVED))
        self.targets[ga] = target.version
        return target

    def pom_date(self, cap, version=None):
        ga = (cap.group_id, cap.artifact_id)
        version = cap.version if version is None else version
        if cap not in self.capabilities or (version != cap.version and version != self.targets.get(ga)):
            raise ValueError('unadmitted metadata operation')
        if len(self.gas) > 1 and ga == self.gas[1] and version == cap.version:
            return MavenPomDate(*ga, version, None, RETRIEVED, MavenReason.TIME_BASIS_UNAVAILABLE)
        body = ('<project><modelVersion>4.0.0</modelVersion><groupId>' + cap.group_id +
                '</groupId><artifactId>' + cap.artifact_id + '</artifactId><version>' + escape(version) +
                '</version></project>').encode()
        date = NEW if version == self.targets[ga] else OLD
        headers = (('Last-Modified', format_datetime(date, usegmt=True)),)
        return pom_date(*ga, version, MavenRepresentation(200, body, headers, RETRIEVED))


def _invoke(root, factory, *options):
    output, errors = io.StringIO(), io.StringIO()
    scanner = partial(scan_mixed_repository, sbom_supervisor_factory=factory)
    with redirect_stdout(output), redirect_stderr(errors):
        code = libyears_main([str(root), *options], scan=scanner)
    if code != 0 or errors.getvalue():
        raise ValueError('offline invocation failed')
    return output.getvalue()


def verify(corpus_directory, output_directory):
    original = {}
    with SbomInputReader(corpus_directory) as reader:
        for name, digest in CORPUS.items():
            snapshot = reader.snapshot(name)
            if snapshot.sha256 != digest:
                raise ValueError('retained corpus digest mismatch')
            original[name] = snapshot.data
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    source = json.loads(original['dt-cyclonedx.json'])
    if len(source['components']) != 201 or len(source.get('services', [])) != 21:
        raise ValueError('retained corpus input counts changed')
    forbidden = partial(ControlledMetadata, unavailable=True)
    negative = {}
    # Test-owned copies preserve exact retained bytes. They are not regenerated
    # documents, target checkouts or new producer assertions.
    with tempfile.TemporaryDirectory() as temporary, patch('socket.socket', side_effect=AssertionError('network forbidden')), \
            patch('subprocess.Popen', side_effect=AssertionError('process forbidden')):
        root = Path(temporary).resolve()
        (root / 'bom.json').write_bytes(original['dt-cyclonedx.json'])
        data = json.loads(_invoke(root, ControlledMetadata, '--json'))
        section = data['sbom']
        expected = {'inventory_records': 200, 'subject_aliases_excluded': 1, 'services_excluded': 21,
                    'members': 200, 'supported_exact': 200, 'relationships': {'direct': 43, 'transitive': 157, 'unknown': 0}}
        if any(section['population'][key] != value for key, value in expected.items()):
            raise ValueError('retained corpus population changed')
        if section['document']['sha256'] != CORPUS['dt-cyclonedx.json'] or len(section['graph']['edges']) != 424:
            raise ValueError('retained corpus binding/graph changed')
        if not (0 < section['summary']['dependencies_measured'] < 200):
            raise ValueError('controlled partial result missing')
        for suffix, flags in (('json', ('--json',)), ('txt', ()), ('verbose.txt', ('--verbose',))):
            text = _invoke(root, ControlledMetadata, *flags)
            if suffix != 'json':
                text = 'VERIFICATION: real retained SBOM bytes; synthetic metadata dates/ages.\n' + text
            (output / ('synthetic-metadata-report.' + suffix)).write_text(text)
        (root / 'unusual.data').write_bytes(original['dt-cyclonedx.json'])
        explicit = json.loads(_invoke(root, ControlledMetadata, '--sbom', 'unusual.data', '--json'))['sbom']
        for key in ('population', 'summary', 'components', 'graph', 'reason_counts'):
            if explicit[key] != section[key]:
                raise ValueError('explicit/automatic projection differs')
        offline = json.loads(_invoke(root, forbidden, '--json'))
        if offline['sbom']['summary']['dependencies_measured'] != 0 or offline['sbom']['summary']['dependencies_discovered'] != 200:
            raise ValueError('offline population not retained')
        (output / 'unavailable-metadata-report.json').write_text(json.dumps(offline, indent=2) + '\n')
        baseline = json.loads(_invoke(root, forbidden, '--no-sbom', '--json'))
        if {k: v for k, v in data.items() if k != 'sbom'} != baseline:
            raise ValueError('legacy projection changed')
        for name in CORPUS:
            if name in ('dt-cyclonedx.json', 'dt-pom-pinned.json'):
                continue
            (root / 'negative.data').write_bytes(original[name])
            refused = json.loads(_invoke(root, forbidden, '--sbom', 'negative.data', '--json'))['sbom']
            if refused['reason'] != 'sbom_unsupported_format' or refused['population'] is not None:
                raise ValueError('unsupported-format corpus witness changed')
            negative[name] = refused['reason']
    # Historical release-POM comparison only. Never feed these declarations into
    # scan admission, current-checkout association or the SBOM denominator.
    pom = parse_pom(original['dt-pom-pinned.json'])
    declarations = pom.elements('dependencies')[0].elements('dependency')
    tests = [row for row in declarations if row.scalar('scope') == 'test']
    inventory_ga = {(row['identity']['group_id'], row['identity']['artifact_id']) for row in section['components'] if row['identity']}
    omitted_tests = sum((row.scalar('groupId'), row.scalar('artifactId')) not in inventory_ga for row in tests)
    direct_ids = {row['id'] for row in section['components'] if row['relationship'] == 'direct'}
    direct_ga = {(row['identity']['group_id'], row['identity']['artifact_id'])
                 for row in section['components'] if row['id'] in direct_ids and row['identity']}
    comparison = [{'group_id': row.scalar('groupId'), 'artifact_id': row.scalar('artifactId'),
                   'scope': row.scalar('scope') or 'compile',
                   'in_inventory': (row.scalar('groupId'), row.scalar('artifactId')) in inventory_ga,
                   'in_subject_edges': (row.scalar('groupId'), row.scalar('artifactId')) in direct_ga}
                  for row in declarations]
    if sum(row['in_inventory'] for row in comparison) != 43 or sum(row['in_subject_edges'] for row in comparison) != 43:
        raise ValueError('historical POM/graph comparison changed')
    if (len(declarations), len(tests), omitted_tests) != (57, 14, 14):
        raise ValueError('historical POM comparison changed')
    result = {'evidence_basis': 'Original retained public documents; synthetic catalogues/POM dates/ages only',
              'bindings': CORPUS, 'input_component_entries': 201, 'population': section['population'],
              'graph_edges': 424, 'synthetic_metadata_summary': section['summary'],
              'synthetic_metadata_reasons': section['reason_counts'],
              'unavailable_metadata_summary': offline['sbom']['summary'],
              'unavailable_metadata_reasons': offline['sbom']['reason_counts'],
              'unsupported_formats': negative, 'historical_pom_only': {'declarations': 57, 'test_declarations': 14, 'omitted_tests': 14, 'inventory_matches': 43, 'subject_edge_matches': 43, 'comparison': comparison},
              'invocations': ['python -m libyears DIRECTORY', 'python -m libyears DIRECTORY --sbom unusual.data', 'python -m libyears DIRECTORY --no-sbom'],
              'execution': 'CLI main with real mixed orchestrator and injected controlled/offline metadata; no standalone live invocation',
              'legacy_projection_equal': True, 'live_metadata_validation': False, 'hosted_platform_execution': False}
    (output / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('corpus_directory')
    parser.add_argument('output_directory')
    args = parser.parse_args(argv)
    try:
        result = verify(args.corpus_directory, args.output_directory)
    except (OSError, ValueError, AssertionError):
        print('Offline retained-corpus verification incomplete; required bytes, capabilities or invariants unavailable.', file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
