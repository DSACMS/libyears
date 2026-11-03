"""T014 public-path composition using only exact synthetic bytes and metadata.

The injected lookup runs the real metadata client/handler and typed protocol.
Process cancellation is separately exercised by the retained controller and
real-worker witnesses; this seam never opens a socket or launches a process.
"""

from contextlib import ExitStack, redirect_stderr, redirect_stdout
import base64
from copy import deepcopy
import hashlib
import io
import json
import os
from pathlib import Path
import re
import socket
import tempfile
import unittest
from unittest.mock import patch

from libyears.cli import main
from libyears import nuget_registry as registry
from libyears.nuget_supervisor import PackageResult, decode_result, result_message
from libyears.registry import TransportFailure
from libyears.scan import scan_mixed_repository
from tests.nuget_fixtures import SAFE_SCOPED_READ, fixture_nuget_reads
from tests.test_nuget_scan import nuget_inputs, HASH


CANARY = 'PRIVATE_ACCEPTANCE_CANARY'
REPOSITORY = Path(__file__).resolve().parents[1]


def metadata(names):
    documents = {registry.SERVICE_INDEX: {'resources': [{
        '@type': 'RegistrationsBaseUrl/3.6.0', '@id': registry.REGISTRATION_BASE}]}}
    for name in names:
        leaves = []
        for version, created in (('1.0.0', '2020-01-01T00:00:00Z'),
                                 ('2.0.0', '2020-12-31T06:00:00Z')):
            url = ('https://api.nuget.org/v3/catalog0/data/2020.01.01/'
                   + name + '.' + version + '.json')
            entry = {'@id': url, 'id': name, 'version': version}
            leaves.append({'@id': registry.REGISTRATION_BASE + name + '/' + version + '.json',
                           'catalogEntry': entry,
                           'packageContent': 'https://user:' + CANARY + '@private.invalid/a.nupkg'})
            documents[url] = dict(entry, **{'@type': 'PackageDetails',
                'packageHash': HASH, 'packageHashAlgorithm': 'SHA512', 'created': created,
                'published': CANARY, 'catalog:commitTimeStamp': CANARY})
        index = registry.REGISTRATION_BASE + name + '/index.json'
        documents[index] = {'count': 1, 'items': [{
            '@id': index + '#page/1.0.0/2.0.0', 'lower': '1.0.0',
            'upper': '2.0.0', 'count': 2, 'items': leaves}]}
    return documents


def reversed_objects(value):
    if isinstance(value, dict):
        return {key: reversed_objects(item) for key, item in reversed(list(value.items()))}
    if isinstance(value, list):
        return [reversed_objects(item) for item in reversed(value)]
    return value


class NuGetAcceptanceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='libyears-acceptance-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve() / (CANARY + '-root')
        self.root.mkdir()

    def exercise(self, files, documents=None, *, extra=('--json',), real_reader=False,
                 selected=True):
        """Guard public CLI, actual parsers/metric/renderers and fixture byte I/O."""
        # Repeated scenarios share this test's temporary root; missing fixture
        # inputs must also be absent on disk, rather than left by an earlier case.
        for name in ('Witness.csproj', 'packages.lock.json', 'witness.json'):
            path = self.root / name
            if name not in files and path.exists():
                path.unlink()
        for name, data in files.items():
            (self.root / name).write_bytes(data)
        before = {path.name: path.read_bytes() for path in self.root.iterdir() if path.is_file()}
        urls, authorities, opened, scan_errors = [], [], [], []
        forbidden_guards, descriptor_calls = [], []
        documents = documents if documents is not None else metadata(('alpha', 'beta'))

        class Transport:
            def get(inner, url):
                urls.append(url)
                self.assertIn(url, documents, 'Only fixed offline responses are permitted.')
                response = documents[url]
                if isinstance(response, Exception):
                    raise response
                if isinstance(response, TransportFailure):
                    return response
                return json.dumps(response).encode()

        def lookup_all(values):
            client = registry.NuGetMetadataClient(transport=Transport(), clock=lambda: 100)
            result = []
            for authority in values:
                authorities.append(authority.package_key)
                client.begin_package(authority.package_key)
                try:
                    package = registry.lookup_authorized_package(authority, client)
                except registry.NuGetRegistryFailure as failure:
                    package = PackageResult(reason=failure.reason)
                result.append((authority, decode_result(result_message(package))))
            return tuple(result)

        def scan(path, **kwargs):
            def unrelated_lookup(*unused):
                self.fail('No sibling dependency was supplied.')
            try:
                return scan_mixed_repository(path, nuget_lookup=lookup_all,
                    pypi_lookup=unrelated_lookup, npm_lookup=unrelated_lookup,
                    rubygems_lookup=unrelated_lookup, **kwargs)
            except AssertionError as error:
                scan_errors.append(error)
                raise

        original_open = os.open
        allowed = {'Witness.csproj', 'packages.lock.json', 'witness.json'}

        def descriptor_open(name, flags, *args, **kwargs):
            descriptor_calls.append((name, flags))
            self.assertTrue(real_reader, 'Portable fixtures must not open descriptors.')
            self.assertTrue(Path(name) == self.root or str(name) in allowed, str(name))
            self.assertFalse(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
            opened.append(str(name))
            return original_open(name, flags, *args, **kwargs)

        options = [str(self.root)]
        if selected:
            options += ['--nuget-project', 'Witness.csproj', '--nuget-provenance', 'witness.json']
        options += list(extra)
        stdout, stderr = io.StringIO(), io.StringIO()
        with ExitStack() as stack:
            reads = None
            if not real_reader:
                reads = stack.enter_context(fixture_nuget_reads(self.root, files))
            for target in ('builtins.open', 'io.open', 'os.write', 'os.system',
                           'os.execve', 'os.spawnv', 'subprocess.Popen', 'subprocess.run',
                           'socket.socket', 'socket.create_connection', 'socket.getaddrinfo',
                           'urllib.request.urlopen'):
                forbidden_guards.append(stack.enter_context(
                    patch(target, side_effect=AssertionError(target))))
            stack.enter_context(patch('os.open', side_effect=descriptor_open))
            with redirect_stdout(stdout), redirect_stderr(stderr):
                status = main(options, scan=scan)
            self.read_names = [call.args[1] for call in reads.call_args_list] if reads else opened
        # Product error sanitization may catch AssertionError as an ordinary
        # transport failure. Assert attempted operations independently after main
        # has returned, so an expected registry_error cannot hide forbidden I/O.
        for operation in forbidden_guards:
            operation.assert_not_called()
        for name, flags in descriptor_calls:
            self.assertTrue(real_reader, 'Portable fixtures must not open descriptors.')
            self.assertTrue(Path(name) == self.root or str(name) in allowed, str(name))
            self.assertFalse(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
        self.assertEqual(before, {path.name: path.read_bytes()
                                 for path in self.root.iterdir() if path.is_file()})
        if scan_errors:
            raise scan_errors[0]
        output, error = stdout.getvalue(), stderr.getvalue()
        self.assertNotIn(CANARY, output + error)
        self.assertNotIn(HASH, output + error)
        self.assertNotIn('Traceback', output + error)
        return status, output, error, urls, authorities, opened

    def test_public_path_permutations_preserve_requests_evidence_and_summaries(self):
        baseline = None
        for reverse in (False, True):
            names = ('beta', 'alpha') if reverse else ('alpha', 'beta')
            files = nuget_inputs(names)
            docs = metadata(names)
            if reverse:
                # Rebind the exact permuted lock; witness records and reference
                # order also change, while all domain facts stay fixed.
                lock = reversed_objects(json.loads(files['packages.lock.json']))
                files['packages.lock.json'] = json.dumps(lock).encode()
                witness = reversed_objects(json.loads(files['witness.json']))
                witness['lock_sha256'] = hashlib.sha256(files['packages.lock.json']).hexdigest()
                files['witness.json'] = json.dumps(witness).encode()
                docs = reversed_objects(docs)
            status, output, error, urls, authorities, _ = self.exercise(files, docs)
            self.assertEqual((status, error, authorities), (0, '', ['alpha', 'beta']))
            data = json.loads(output)
            self.assertEqual(data['summary']['coverage'], 1.0)
            self.assertEqual(data['summary']['total_libyears'], 2.0)
            self.assertEqual(urls.count(registry.SERVICE_INDEX), 1)
            facts = (data, urls)
            if baseline is None:
                baseline = facts
            self.assertEqual(facts, baseline)
            for extra in (('--json', '--verbose'), (), ('--verbose',)):
                result = self.exercise(files, docs, extra=extra)
                self.assertEqual((result[0], result[2], result[3]), (0, '', urls))
                if '--json' in extra:
                    self.assertEqual(json.loads(result[1]), data)
                else:
                    for fact in ('alpha', 'beta', '2020-12-31', 'public_content_verified',
                                 'public_agreement', 'supplied producer/supplier assertions'):
                        self.assertIn(fact, result[1])

    def test_combined_earliest_stages_retain_only_safe_established_evidence(self):
        cases = [
            (dict(project_change=lambda b: b.replace(b'net10.0', b'net10.0;net9.0'),
                  lock_change=lambda d: d.update(version=2),
                  witness_change=lambda d: d.update(project_sha256='0' * 64)),
             'unsupported_nuget_project', None, None),
            (dict(lock_change=lambda d: d.update(version=2),
                  witness_change=lambda d: d.update(project_sha256='0' * 64)),
             'unsupported_lockfile_format', 1, None),
            (dict(lock_change=lambda d: d['dependencies']['net10.0']['alpha'].update(requested='[2.0.0, )'),
                  witness_change=lambda d: d.update(project_sha256='0' * 64)),
             'nuget_context_mismatch', 1, 'packages_lock_v1'),
        ]
        for changes, reason, count, lock_format in cases:
            for reverse in (False, True):
                files = nuget_inputs(**changes)
                if reverse:
                    witness = reversed_objects(json.loads(files['witness.json']))
                    files['witness.json'] = json.dumps(witness).encode()
                result = self.exercise(files)
                data = json.loads(result[1])
                self.assertEqual((result[0], result[2], result[3], result[4]), (0, '', [], []))
                self.assertEqual([row['reason'] for row in data['source_errors']], [reason])
                self.assertEqual(data['dependencies'], [])
                self.assertEqual(data['unmeasurable'], [])
                summary = data['summary']['by_ecosystem']['nuget']
                self.assertEqual(summary['dependencies_discovered'], count)
                self.assertIsNone(summary['dependencies_measured'])
                self.assertIsNone(summary['coverage'])
                self.assertEqual(data['version_evidence']['nuget']['format'], lock_format)
                expected_reads = ['Witness.csproj']
                if reason != 'unsupported_nuget_project':
                    expected_reads.append('packages.lock.json')
                if reason == 'nuget_context_mismatch':
                    expected_reads.append('witness.json')
                self.assertEqual(self.read_names, expected_reads)

    def test_isolated_association_origin_hash_and_public_failures_compose(self):
        files = nuget_inputs(('alpha', 'beta', 'gamma'),
            lock_change=lambda d: d['dependencies']['net10.0']['alpha'].update(requested='[2.0.0, )'),
            witness_change=lambda d: d['packages'][1].update(origins=['https://user:' + CANARY + '@private.invalid']))
        docs = metadata(('gamma',))
        used_url = next(url for url in docs if '/catalog0/' in url and '1.0.0' in url)
        docs[used_url]['packageHash'] = base64.b64encode(b'z' * 64).decode()
        docs[used_url]['created'] = CANARY
        for extra in (('--json',), ('--json', '--verbose'), (), ('--verbose',)):
            result = self.exercise(files, docs, extra=extra)
            self.assertEqual((result[0], result[2], result[4]), (0, '', ['gamma']))
            if '--json' not in extra:
                continue
            data = json.loads(result[1])
            rows = {row['name']: row for row in data['unmeasurable']}
            self.assertEqual({name: row['reason'] for name, row in rows.items()}, {
                'alpha': 'declaration_lock_requirement_mismatch',
                'beta': 'unsupported_dependency_source', 'gamma': 'content_hash_mismatch'})
            self.assertNotIn('selected_version', rows['alpha']['nuget_evidence'])
            self.assertNotIn('used_publication', rows['gamma']['nuget_evidence'])
            self.assertEqual(data['summary']['coverage'], 0.0)
            self.assertEqual(data['summary']['dependencies_discovered'], 3)

    def test_response_exception_and_local_secret_canaries_across_output_modes(self):
        files = nuget_inputs(witness_change=lambda d: d['producer'].update(name=CANARY))
        for mode in ('xml', 'witness', 'response', 'exception'):
            supplied, docs = deepcopy(files), metadata(('alpha',))
            if mode == 'xml':
                supplied['Witness.csproj'] = ('<Project>' + CANARY).encode()
            elif mode == 'witness':
                supplied['witness.json'] = ('{"' + CANARY + '":').encode()
            else:
                index = registry.REGISTRATION_BASE + 'alpha/index.json'
                docs[index] = RuntimeError(CANARY) if mode == 'exception' else {'items': CANARY}
            for extra in ((), ('--verbose',), ('--json',), ('--json', '--verbose')):
                result = self.exercise(supplied, docs, extra=extra)
                self.assertEqual((result[0], result[2]), (0, ''))
                self.assertIn('invalid_' if mode != 'exception' else 'registry_error', result[1])

    def test_swallowed_forbidden_io_attempts_still_fail_acceptance_guards(self):
        original_get = registry.NuGetMetadataClient.get_json
        for operation in (lambda: socket.socket(), lambda: open(CANARY)):
            def forbidden_get(client, *args, **kwargs):
                try:
                    operation()
                except Exception:
                    pass
                return original_get(client, *args, **kwargs)
            docs = metadata(('alpha',))
            docs[registry.REGISTRATION_BASE + 'alpha/index.json'] = TimeoutError(CANARY)
            # The public report would otherwise be an expected registry_error.
            # Only post-main call-history assertions discriminate the mutation.
            with self.subTest(operation=operation), \
                    patch.object(registry.NuGetMetadataClient, 'get_json', forbidden_get), \
                    self.assertRaisesRegex(AssertionError, 'to not have been called'):
                self.exercise(nuget_inputs(), docs)

    def test_excluded_artifacts_cannot_repair_missing_or_rejected_authority(self):
        excluded = ('project.assets.json', 'export.json', 'packages.config', 'NuGet.Config',
                    'Directory.Packages.props', 'Other.csproj', 'Child.csproj', 'target.py',
                    '.nupkg.metadata', 'credentials.json')
        for name in excluded:
            (self.root / name).write_text(CANARY)
        for missing in ('packages.lock.json', 'witness.json'):
            files = nuget_inputs(project_change=lambda b: b.replace(b'</ItemGroup>',
                b'<ProjectReference Include="Child.csproj" /></ItemGroup>'))
            del files[missing]
            result = self.exercise(files)
            self.assertEqual((result[0], result[2], result[3]), (0, '', []))
            self.assertIn('lockfile_missing' if missing.startswith('packages')
                          else 'nuget_provenance_missing', result[1])
        result = self.exercise(nuget_inputs(), selected=False)
        self.assertEqual((result[0], result[2], result[3]), (0, '', []))
        self.assertNotIn('nuget', result[1])

    @unittest.skipUnless(SAFE_SCOPED_READ, 'safe descriptor access unavailable')
    def test_actual_reader_public_path_preserves_bytes_and_never_traverses_references(self):
        (self.root / 'Child.csproj').write_text(CANARY)
        files = nuget_inputs(project_change=lambda b: b.replace(b'</ItemGroup>',
            b'<ProjectReference Include="Child.csproj" /></ItemGroup>'))
        result = self.exercise(files, metadata(('alpha',)), real_reader=True)
        self.assertEqual((result[0], result[2], result[4]), (0, '', ['alpha']))
        self.assertEqual(set(result[5]), {str(self.root), *files})
        self.assertEqual(json.loads(result[1])['summary']['coverage'], 1.0)

    def test_retained_s6_reasons_exactly_match_reachable_trigger_tables(self):
        spec = (REPOSITORY / 'specs/006-nuget-selected-evidence/spec.md').read_text()
        table = spec.split('| Condition | Level / stable reason |', 1)[1].split('\n\n', 1)[0]
        expected = set()
        for line in table.splitlines():
            level = 'source' if '| Source /' in line else 'dependency' if '| Dependency /' in line else None
            if level:
                expected.update((level, reason) for reason in re.findall(r'`([a-z_]+)`', line))
        observed = set()
        for filename in ('local-reason-triggers.json', 'registry-reason-triggers.json'):
            rows = json.loads((REPOSITORY / 'tests/fixtures/nuget' / filename).read_text())
            for row in rows:
                observed.add((row['level'], row['reason']))
                module = 'test_nuget_source.py' if filename.startswith('local') else 'test_nuget_registry.py'
                self.assertIn('def ' + row['test'] + '(', (REPOSITORY / 'tests' / module).read_text())
        self.assertEqual(expected, observed)
        self.assertNotIn(('dependency', 'ambiguous_lock_evidence'), observed)


if __name__ == '__main__':
    unittest.main()
