"""Offline W/S witnesses for the internal selected NuGet source (T006)."""

import base64
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from libyears import nuget_input as inputs
from libyears.nuget import read_nuget_source
from libyears.nuget_provenance import LocalAuthority
from tests.nuget_fixtures import SAFE_SCOPED_READ, fixture_nuget_reads


FIXTURES = Path(__file__).parent / 'fixtures/nuget'
HASH = base64.b64encode(bytes(range(64))).decode()


class NuGetSourceTests(unittest.TestCase):
    def setUp(self):
        self.witness = json.loads((FIXTURES / 'witness-v1.json').read_text())

    def project(self, request='1.0', names=('Example',)):
        references = ''.join('<PackageReference Include="' + name + '" Version="'
                             + request + '" />' for name in names)
        return ('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>'
                '<TargetFramework>net10.0</TargetFramework></PropertyGroup>'
                '<ItemGroup>' + references + '</ItemGroup></Project>').encode()

    def lock(self, requested='[1.0.0, )', names=('Example',)):
        return {'version': 1, 'dependencies': {'net10.0': {
            name: {'type': 'Direct', 'requested': requested,
                   'resolved': '2.0.0', 'contentHash': HASH} for name in names}}}

    def inputs(self, *, request='1.0', requested='[1.0.0, )', names=('Example',)):
        return self.project(request, names), self.lock(requested, names)

    def run_source(self, project=None, lock=None, *, witness_change=None,
                   missing=None, selected_witness=True, guard=True,
                   unrelated=False, stale=False, use_real_reader=False):
        if project is None:
            project = self.project()
        if lock is None:
            lock = self.lock('[1.0.0, )')
        lock_bytes = lock if isinstance(lock, bytes) else json.dumps(lock).encode()
        witness = deepcopy(self.witness)
        witness['project_sha256'] = hashlib.sha256(project).hexdigest()
        witness['lock_sha256'] = hashlib.sha256(lock_bytes).hexdigest()
        if witness_change:
            witness_change(witness)
        witness_bytes = json.dumps(witness).encode()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            files = {'Witness.csproj': project, 'packages.lock.json': lock_bytes,
                     'witness.json': witness_bytes}
            if stale:
                files['Witness.csproj'] += b'\n'
            for name, data in files.items():
                if name != missing:
                    (root / name).write_bytes(data)
            if unrelated:
                (root / '.git').mkdir()
                for name in ('project.assets.json', 'packages.config', 'Directory.Packages.props',
                             'NuGet.Config', 'Other.csproj', 'export.json'):
                    (root / name).write_text('SECRET-UNRELATED')
                # Old/new timestamps and Git presence cannot rebind changed bytes.
                os.utime(root / 'Witness.csproj', (1, 1))
            before = {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()}
            allowed = {'Witness.csproj', 'packages.lock.json'}
            if selected_witness:
                allowed.add('witness.json')
            # Source semantics run independently of host descriptor support.
            # Real reader containment/race behavior has its own filesystem tests.
            fixture_files = {name: data for name, data in files.items() if name != missing}
            opened = []
            real_open = os.open

            def guarded_open(name, flags, *args, **kwargs):
                self.assertTrue(use_real_reader, 'Semantic fixtures must not open files.')
                opened.append(str(name))
                self.assertTrue(Path(name) == root or str(name) in allowed, str(name))
                self.assertFalse(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
                return real_open(name, flags, *args, **kwargs)

            with ExitStack() as stack:
                reads = None
                if not use_real_reader:
                    reads = stack.enter_context(fixture_nuget_reads(root, fixture_files))
                if guard:
                    stack.enter_context(patch('os.open', side_effect=guarded_open))
                    for target in ('subprocess.Popen', 'subprocess.run', 'os.system',
                                   'socket.socket', 'urllib.request.urlopen', 'os.write'):
                        stack.enter_context(patch(target, side_effect=AssertionError(target)))
                result = read_nuget_source(root, 'Witness.csproj',
                                           'witness.json' if selected_witness else None)
            after = {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()}
            self.assertEqual(before, after)
            requested_names = ([call.args[1] for call in reads.call_args_list]
                               if reads is not None else opened)
            self.assertTrue(set(requested_names) <= allowed | {str(root)})
            if not selected_witness:
                self.assertNotIn('witness.json', requested_names)
            return result

    def assert_reason(self, source, reason, *, count=1, level='dependency'):
        result = source.result
        self.assertEqual(result.dependencies_discovered, count)
        self.assertEqual(result.candidates, ())
        self.assertEqual(source.authorized_candidates, ())
        rows = result.source_errors if level == 'source' else result.unmeasurable
        self.assertEqual([row.reason for row in rows], [reason])
        self.assertEqual(result.measurement_available, level != 'source')
        if level == 'source':
            self.assertEqual(result.unmeasurable, ())
        else:
            self.assertEqual(result.source_errors, ())

    @unittest.skipUnless(SAFE_SCOPED_READ, 'safe descriptor access unavailable')
    def test_real_reader_composes_bound_inputs_on_supported_hosts(self):
        source = self.run_source(use_real_reader=True, unrelated=True)
        self.assertEqual(source.result.source_errors, ())
        self.assertEqual(source.result.unmeasurable, ())
        self.assertTrue(source.result.measurement_available)
        self.assertEqual(len(source.authorized_candidates), 1)
        self.assertIsInstance(source.authorized_candidates[0].authority, LocalAuthority)

    def test_five_canonical_pairs_and_different_selected_version(self):
        for request, requested in (('1.0', '[1.0.0, )'), ('1.2.3', '[1.2.3, )'),
                                   ('1.2.3.0', '[1.2.3, )'), ('1.2.3.4', '[1.2.3.4, )'),
                                   ('0.0.0.0', '[0.0.0, )')):
            with self.subTest(request=request):
                source = self.run_source(*self.inputs(request=request, requested=requested))
                self.assertEqual(source.result.dependencies_discovered, 1)
                self.assertTrue(source.result.measurement_available)
                self.assertEqual(source.result.unmeasurable, ())
                pair, = source.authorized_candidates
                self.assertIsInstance(pair.authority, LocalAuthority)
                self.assertEqual(source.result.candidates, (pair.candidate,))
                self.assertEqual(pair.candidate.used_version, '2.0.0')
                self.assertEqual(pair.authority.package_key, 'example')
                evidence = pair.candidate.nuget_evidence
                self.assertEqual((evidence.origin_state, evidence.content_hash_state),
                                 ('asserted_public', 'local_agreement'))
                self.assertEqual(evidence.lock_requested, requested)
                self.assertEqual(evidence.normalized_version, '2.0.0')

    def test_exact_byte_binding_for_lf_and_crlf_without_normalization(self):
        for newline in (b'\n', b'\r\n'):
            with self.subTest(newline=newline):
                project = self.project() + newline
                lock = json.dumps(self.lock()).encode() + newline
                source = self.run_source(project, lock)
                self.assertEqual(len(source.authorized_candidates), 1)
                self.assert_reason(self.run_source(project, lock, stale=True),
                                   'nuget_context_mismatch', level='source')

    def test_all_s3_noncanonical_negative_requests_and_stage_omissions(self):
        negatives = ['[1.0.1, )', '[1.0, )', '[1.0.0.0, )', '[1.0.0,)',
                     '[1.0.0]', '(1.0.0, )', '[1.0.0, 2.0.0)', '1.*',
                     '[1.0.0-alpha, )', ' [1.0.0, )', '[01.0.0, )',
                     '[1.0.0, ) ']
        for requested in negatives:
            with self.subTest(requested=requested):
                project, lock = self.inputs(requested=requested)
                lock['dependencies']['net10.0']['Example']['resolved'] = 'SECRET-SELECTED'
                source = self.run_source(project, lock)
                self.assert_reason(source, 'declaration_lock_requirement_mismatch')
                evidence = source.result.unmeasurable[0].nuget_evidence
                if 'alpha' not in requested:
                    self.assertEqual(evidence.lock_requested, requested)
                self.assertIsNone(evidence.selected_version)
                self.assertIsNone(evidence.normalized_version)
                self.assertIsNone(evidence.selection_source)
                self.assertEqual(evidence.origin_state, 'unavailable')
        source = self.run_source(*self.inputs(request='1.2.3.4', requested='[1.2.3, )'))
        self.assert_reason(source, 'declaration_lock_requirement_mismatch')
        for requested in ('[1.2.3.0, )', '[1.2.3,)', '[1.2.3]', '(1.2.3, )',
                          '[1.2.3, 2.0.0)', '[1.2.*, )', '[1.2.3-alpha, )'):
            source = self.run_source(*self.inputs(request='1.2.3', requested=requested))
            self.assert_reason(source, 'declaration_lock_requirement_mismatch')

    def test_association_missing_transitive_namesake_and_selection(self):
        for kind in ('absent', 'Transitive', 'Project'):
            lock = self.lock('[1.0.0, )')
            entries = lock['dependencies']['net10.0']
            entry = entries.pop('Example')
            if kind != 'absent':
                entry.pop('requested')
                entry['type'] = kind
                if kind == 'Project':
                    entry = {'type': kind}
                entries['Example'] = entry
            self.assert_reason(self.run_source(lock=lock), 'lock_dependency_missing')
        for value, reason in ((None, 'lock_version_missing'), ('', 'unsupported_lock_evidence'),
                              ('1', 'unsupported_lock_evidence'),
                              ('https://user:SECRET@private/x', 'unsupported_lock_evidence')):
            lock = self.lock('[1.0.0, )')
            entry = lock['dependencies']['net10.0']['Example']
            if value is None:
                del entry['resolved']
            else:
                entry['resolved'] = value
            source = self.run_source(lock=lock)
            self.assert_reason(source, reason)
            evidence = source.result.unmeasurable[0].nuget_evidence
            self.assertEqual(evidence.selected_version, '1' if value == '1' else None)
            self.assertIsNone(evidence.normalized_version)
            self.assertNotIn('SECRET', repr(source.result))

    def test_whole_lock_failures_precede_individual_failures(self):
        for field in ('requested', 'resolved'):
            for bad in (None, [], {}, False):
                lock = self.lock('mismatch')
                lock['dependencies']['net10.0']['Example'][field] = bad
                self.assert_reason(self.run_source(lock=lock), 'invalid_lockfile', level='source')
        lock = self.lock('[1.0.0, )')
        del lock['dependencies']['net10.0']['Example']['requested']
        self.assert_reason(self.run_source(lock=lock), 'invalid_lockfile', level='source')
        for duplicate in ('"Example": {}, "Example": {}', '"Example": {}, "EXAMPLE": {}',
                          '"Example": {"type":"Direct","requested":"bad",'
                          '"resolved":"1.0","resolved":"2.0"}'):
            raw = ('{"version":1,"dependencies":{"net10.0":{' + duplicate + '}}}').encode()
            self.assert_reason(self.run_source(lock=raw), 'invalid_lockfile', level='source')
        lock = self.lock('[1.0.0, )')
        lock['dependencies']['net9.0'] = {}
        self.assert_reason(self.run_source(lock=lock), 'unsupported_lockfile_format', level='source')

    def test_k1_exact_direct_and_transitive_overflows_reject_whole_source(self):
        cases = (
            ('Direct', '1.2+' + 'a' * 253),
            ('Direct', '1.' + '9' * 33),
            ('Transitive', '1.0-' + 'a' * 253),
            ('Transitive', '1.' + '1' * 33),
        )
        for kind, resolved in cases:
            for reverse in (False, True):
                with self.subTest(kind=kind, resolved=resolved, reverse=reverse):
                    lock = self.lock()
                    entries = lock['dependencies']['net10.0']
                    if kind == 'Direct':
                        entries['Example']['resolved'] = resolved
                    else:
                        entries['Helper'] = {'type': kind, 'resolved': resolved,
                                             'contentHash': HASH}
                    if reverse:
                        lock['dependencies']['net10.0'] = dict(reversed(list(entries.items())))
                    source = self.run_source(lock=lock)
                    self.assert_reason(source, 'unsupported_lockfile_format', level='source')
                    self.assertEqual(source.result.source_errors[0].source, 'packages.lock.json')
                    self.assertIsNone(source.result.evidence.format)

    def test_k1_closure_requests_and_direct_requests_cannot_bypass_bounds(self):
        for text in ('x' * 257, '[1.' + '9' * 33 + '.0, )'):
            for kind in ('Direct', 'Transitive', 'Project'):
                lock = self.lock()
                entry = {'type': kind, 'dependencies': {'Helper': text}}
                if kind != 'Project':
                    entry.update(resolved='1.0.0', contentHash=HASH)
                if kind == 'Direct':
                    entry['requested'] = '[1.0.0, )'
                    lock['dependencies']['net10.0']['Example'] = entry
                else:
                    lock['dependencies']['net10.0']['Closure'] = entry
                self.assert_reason(self.run_source(lock=lock), 'unsupported_lockfile_format',
                                   level='source')
            lock = self.lock(text)
            self.assert_reason(self.run_source(lock=lock, missing='witness.json'),
                               'unsupported_lockfile_format', level='source')
        for reverse in (False, True):
            lock = self.lock()
            entries = lock['dependencies']['net10.0']
            entries['Example']['resolved'] = '1.' + '9' * 33
            entries['Malformed'] = {'type': 'Transitive', 'resolved': None,
                                    'contentHash': HASH}
            if reverse:
                lock['dependencies']['net10.0'] = dict(reversed(list(entries.items())))
            self.assert_reason(self.run_source(lock=lock), 'invalid_lockfile', level='source')

    def test_k1_transitive_boundaries_preserve_unrelated_direct_authority(self):
        for resolved in ('1.0-' + 'a' * 252, '1.' + '1' * 32, 'ordinary unsupported syntax'):
            lock = self.lock()
            lock['dependencies']['net10.0']['Helper'] = {
                'type': 'Transitive', 'resolved': resolved, 'contentHash': HASH}
            source = self.run_source(lock=lock)
            self.assertEqual(source.result.source_errors, ())
            self.assertEqual(source.result.unmeasurable, ())
            self.assertTrue(source.result.measurement_available)
            self.assertEqual(len(source.authorized_candidates), 1)

    def test_context_failures_extra_direct_framework_and_stale_bytes(self):
        lock = self.lock('[1.0.0, )', ('Example', 'Extra'))
        self.assert_reason(self.run_source(lock=lock), 'nuget_context_mismatch', level='source')
        lock = self.lock('[1.0.0, )')
        lock['dependencies']['net9.0'] = lock['dependencies'].pop('net10.0')
        self.assert_reason(self.run_source(lock=lock), 'nuget_context_mismatch', level='source')
        for key, value in (('project', 'Other.csproj'), ('framework', 'net9.0'),
                            ('project_sha256', '0' * 64), ('lock_sha256', '0' * 64)):
            source = self.run_source(witness_change=lambda w: w.update({key: value}))
            self.assert_reason(source, 'nuget_context_mismatch', level='source')
        self.assert_reason(self.run_source(stale=True, unrelated=True, guard=True),
                           'nuget_context_mismatch', level='source')

    def test_no_implicit_witness_or_forbidden_fallback_reads_and_input_unchanged(self):
        source = self.run_source(selected_witness=False, unrelated=True, guard=True)
        self.assert_reason(source, 'nuget_provenance_missing', level='source')
        source = self.run_source(guard=True, unrelated=True)
        self.assertEqual(len(source.authorized_candidates), 1)

    def test_whole_witness_precedes_association_and_invalidates_population_only_when_asserted(self):
        project, lock = self.inputs(requested='mismatch')
        for changes, reason, count in (
            (lambda w: w.update(version=2), 'invalid_nuget_provenance', 1),
            (lambda w: w.update(project='Wrong.csproj'), 'nuget_context_mismatch', 1),
            (lambda w: w['baseline'].update(explicit_population_complete=False),
             'unsupported_nuget_project', None)):
            source = self.run_source(project, lock, witness_change=changes)
            self.assert_reason(source, reason, count=count, level='source')

    def test_combined_failures_and_reordered_whole_source_precedence(self):
        # Later unavailable inputs never manufacture extra source errors.
        source = self.run_source(project=b'<Project', lock=b'{', missing='witness.json')
        self.assert_reason(source, 'invalid_nuget_project', count=None, level='source')
        self.assertEqual(source.result.source_errors[0].source, 'Witness.csproj')
        source = self.run_source(lock=b'{', missing='witness.json')
        self.assert_reason(source, 'invalid_lockfile', level='source')
        self.assertEqual(source.result.source_errors[0].source, 'packages.lock.json')
        for reverse in (False, True):
            lock = self.lock('mismatch')
            entry = lock['dependencies']['net10.0']['Example']
            entry.update(unknown=True, resolved=[])
            if reverse:
                lock = dict(reversed(list(lock.items())))
                lock['dependencies']['net10.0']['Example'] = dict(reversed(list(entry.items())))
            source = self.run_source(lock=lock, missing='witness.json')
            self.assert_reason(source, 'invalid_lockfile', level='source')
            self.assertIsNone(source.result.evidence.format)
        for reverse in (False, True):
            def changes(w):
                w['framework'] = 'net9.0'
                w['packages'] = [{'id': 'Good', 'version': '1.0'},
                                 {'id': 'Bad', 'version': '1.0', 'origins': False}]
                if reverse:
                    w['packages'].reverse()
            source = self.run_source(lock=self.lock('mismatch'), witness_change=changes)
            self.assert_reason(source, 'invalid_nuget_provenance', level='source')
            self.assertEqual(source.result.evidence.format, 'packages_lock_v1')
        # Association also wins over a nonpublic origin and absent hash, without
        # ever admitting a capability for the identity.
        source = self.run_source(lock=self.lock('mismatch'),
                                 witness_change=lambda w: w['packages'][0].update(origins=[]))
        self.assert_reason(source, 'declaration_lock_requirement_mismatch')

    def test_rejected_source_stage_evidence_is_only_what_was_established(self):
        project_failure = self.run_source(missing='Witness.csproj').result
        self.assertIsNone(project_failure.evidence.framework)
        self.assertIsNone(project_failure.evidence.format)
        lock_failure = self.run_source(missing='packages.lock.json').result
        self.assertEqual(lock_failure.evidence.framework, 'net10.0')
        self.assertIsNone(lock_failure.evidence.format)
        witness_failure = self.run_source(selected_witness=False).result
        self.assertEqual(witness_failure.evidence.format, 'packages_lock_v1')
        self.assertIsNone(witness_failure.evidence.provenance_source)
        self.assertEqual(witness_failure.source_errors[0].source, 'Witness.csproj')

    def test_validated_empty_differs_from_known_empty_rejected_sources(self):
        project, lock = self.inputs(names=())
        source = self.run_source(project, lock)
        self.assertEqual(source.result.dependencies_discovered, 0)
        self.assertTrue(source.result.measurement_available)
        self.assertEqual(source.result.source_errors, ())
        for missing, reason in (('packages.lock.json', 'lockfile_missing'),
                                ('witness.json', 'nuget_provenance_missing')):
            self.assert_reason(self.run_source(project, lock, missing=missing), reason,
                               count=0, level='source')
        self.assert_reason(self.run_source(project, b'{'), 'invalid_lockfile',
                           count=0, level='source')
        self.assert_reason(self.run_source(project, lock,
                                          witness_change=lambda w: w.update(version=2)),
                           'invalid_nuget_provenance', count=0, level='source')

    def test_sorted_results_independent_of_declaration_lock_and_witness_order(self):
        results = []
        for names in (('Zulu', 'alpha'), ('alpha', 'Zulu')):
            project, lock = self.inputs(names=names)
            def witnesses(w):
                w['packages'] = [dict(w['packages'][0], id=name) for name in names]
            source = self.run_source(project, lock, witness_change=witnesses)
            self.assertEqual([c.name for c in source.result.candidates], ['alpha', 'Zulu'])
            results.append(source.result)
        self.assertEqual(results[0], results[1])
        for names in (('Zulu', 'alpha'), ('alpha', 'Zulu')):
            source = self.run_source(*self.inputs(names=names, requested='mismatch'))
            self.assertEqual([r.name for r in source.result.unmeasurable], ['alpha', 'Zulu'])

    def test_safe_evidence_omits_arbitrary_request_and_private_witness_values(self):
        def private(w):
            w['producer']['name'] = 'SECRET-PRODUCER'
            w['packages'][0]['origins'] = ['https://user:SECRET@private/x']
        lock = self.lock('https://user:SECRET@private/x')
        source = self.run_source(lock=lock, witness_change=private)
        self.assert_reason(source, 'declaration_lock_requirement_mismatch')
        self.assertIsNone(source.result.unmeasurable[0].nuget_evidence.lock_requested)
        self.assertNotIn('SECRET', json.dumps(asdict(source.result)))
        self.assertNotIn(HASH, json.dumps(asdict(source.result)))

    def test_local_s6_reason_trigger_table(self):
        table = json.loads((FIXTURES / 'local-reason-triggers.json').read_text())
        triggered = set()
        scenarios = [
            ('nuget_project_missing', dict(missing='Witness.csproj'), None),
            ('invalid_nuget_project', dict(project=b'<Project'), None),
            ('unsupported_nuget_project', dict(project=b'<Project />'), None),
            ('duplicate_nuget_declaration', dict(project=self.project(names=('Example', 'EXAMPLE'))), None),
            ('lockfile_missing', dict(missing='packages.lock.json'), 1),
            ('invalid_lockfile', dict(lock=b'{'), 1),
            ('unsupported_lockfile_format', dict(lock={'version': 2, 'dependencies': {}}), 1),
            ('nuget_context_mismatch', dict(stale=True), 1),
            ('nuget_provenance_missing', dict(selected_witness=False), 1),
            ('invalid_nuget_provenance', dict(witness_change=lambda w: w.update(version=2)), 1),
        ]
        for reason, kwargs, count in scenarios:
            self.assert_reason(self.run_source(**kwargs), reason, count=count, level='source')
            triggered.add(('source', reason))
        for reason, change in (
            ('lock_dependency_missing', lambda e: e.clear()),
            ('declaration_lock_requirement_mismatch', lambda e: e['Example'].update(requested='mismatch')),
            ('lock_version_missing', lambda e: e['Example'].pop('resolved')),
            ('unsupported_lock_evidence', lambda e: e['Example'].update(resolved='*')),
            ('content_hash_unavailable', lambda e: e['Example'].pop('contentHash')),
            ('content_hash_mismatch', lambda e: e['Example'].update(contentHash=base64.b64encode(b'x' * 64).decode())),
        ):
            lock = self.lock('[1.0.0, )')
            change(lock['dependencies']['net10.0'])
            source = self.run_source(lock=lock)
            if reason.startswith('content_hash_'):
                # Historical S6 fixture retained; these now describe assurance.
                self.assertEqual(len(source.authorized_candidates), 1)
                state = 'mismatch' if reason.endswith('mismatch') else 'unavailable'
                self.assertEqual(source.authorized_candidates[0].authority.local_content_state, state)
            else:
                self.assert_reason(source, reason)
            triggered.add(('dependency', reason))
        source = self.run_source(witness_change=lambda w: w['packages'][0].update(origins=[]))
        self.assert_reason(source, 'unsupported_dependency_source')
        triggered.add(('dependency', 'unsupported_dependency_source'))
        self.assertEqual(triggered, {(row['level'], row['reason']) for row in table})
        self.assertTrue(all(row['test'] == 'test_local_s6_reason_trigger_table' for row in table))


class NuGetSourcePlatformRefusalTests(unittest.TestCase):
    def test_missing_safety_primitives_reject_source_before_reads_or_authority(self):
        # This uses the real production context manager, never the fixture seam.
        for capability in ('O_DIRECTORY', 'O_NOFOLLOW', 'O_NONBLOCK',
                           'supports_dir_fd', 'supports_follow_symlinks'):
            unavailable = set() if capability.startswith('supports_') else 0
            with self.subTest(capability=capability), ExitStack() as stack:
                stack.enter_context(patch.object(inputs.os, capability, unavailable, create=True))
                opened = stack.enter_context(patch.object(inputs.os, 'open'))
                read_bytes = stack.enter_context(patch.object(inputs.os, 'read'))
                scoped_read = stack.enter_context(patch.object(inputs.ScopedNuGetReader, 'read'))
                authorize = stack.enter_context(patch('libyears.nuget.authorize_measurement'))
                for target in ('subprocess.Popen', 'subprocess.run', 'os.system',
                               'socket.socket', 'urllib.request.urlopen', 'os.write'):
                    stack.enter_context(patch(target, side_effect=AssertionError(target)))
                source = read_nuget_source(Path.cwd(), 'Witness.csproj', 'witness.json')
                self.assertEqual(source.result.dependencies_discovered, None)
                self.assertFalse(source.result.measurement_available)
                self.assertEqual(source.result.candidates, ())
                self.assertEqual(source.result.unmeasurable, ())
                self.assertEqual(source.authorized_candidates, ())
                self.assertEqual([(row.source, row.reason) for row in source.result.source_errors],
                                 [('Witness.csproj', 'invalid_nuget_project')])
                for operation in (opened, read_bytes, scoped_read, authorize):
                    operation.assert_not_called()


if __name__ == '__main__':
    unittest.main()
