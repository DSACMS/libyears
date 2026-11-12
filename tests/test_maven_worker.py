"""Closed worker protocol and deterministic/native supervisor lifecycle witnesses."""

from datetime import datetime, timezone
from pathlib import Path
import os
import subprocess
import tempfile
import time
import unittest
from unittest.mock import Mock, patch

from libyears.maven import MavenCapability
from libyears.maven_model import MavenReason
from libyears.maven_protocol import (
    available, command, date_text, read_message, result, write_message,
)
from libyears.maven_supervisor import MavenSupervisor, MavenWorkerFailure, _DEFERRED

CAP = MavenCapability('g', 'a', '1')


def request(sequence=1, operation='select_target', version=None):
    return dict(sequence=sequence, operation=operation, group_id='g', artifact_id='a',
                version=version, deadline=10.0)


def reply(req, attempts=1, body_bytes=100):
    selecting = req['operation'] == 'select_target'
    value = {key: req[key] for key in ('sequence', 'operation', 'group_id', 'artifact_id', 'version')}
    value.update(selected_version='2' if selecting else None,
                 last_modified=None if selecting else '2023-01-02T03:04:05Z',
                 retrieved_at=date_text(datetime.now(timezone.utc)), reason=None,
                 attempts=attempts, body_bytes=body_bytes,
                 ordering_basis='maven_comparable_version_3_9_11' if selecting else None,
                 eligibility_policy='maven_conservative_stable_v1' if selecting else None,
                 time_basis=None if selecting else 'maven_conventional_pom_last_modified')
    return value


class MavenProtocolTests(unittest.TestCase):
    def test_closed_commands_reject_sequence_types_urls_paths_and_unknown_fields(self):
        self.assertEqual(command(request()), request())
        for field, value in (('sequence', True), ('sequence', 0), ('sequence', 301),
                             ('operation', 'fetch_url'), ('operation', []),
                             ('group_id', 'g/../private'), ('artifact_id', 'https://private'),
                             ('version', '1'), ('deadline', float('nan')), ('deadline', True)):
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                command({**request(), field: value})
        with self.assertRaises(ValueError):
            command({**request(), 'url': 'https://private'})
        for version in ('1-SNAPSHOT', '../1', '1%2f2'):
            with self.assertRaises(ValueError):
                command(request(operation='pom_date', version=version))

    def test_result_requires_exact_identity_state_bases_counters_and_dates(self):
        req = request()
        self.assertEqual(result(reply(req), req)['selected_version'], '2')
        mutations = {'sequence': 2, 'group_id': 'other', 'version': '1', 'attempts': True,
                     'body_bytes': -1, 'selected_version': '2-preview', 'reason': 'raw private error',
                     'ordering_basis': 'semver', 'eligibility_policy': 'unknown',
                     'time_basis': 'publication', 'last_modified': '2023-01-02T00:00:00Z'}
        for field, value in mutations.items():
            with self.subTest(field=field), self.assertRaises(ValueError):
                result({**reply(req), field: value}, req)
        req = request(operation='pom_date', version='1')
        self.assertIsNone(result(reply(req), req)['selected_version'])
        for field, value in (('last_modified', '9999-01-02T00:00:00Z'),
                             ('last_modified', '2023-01-02T03:04:05.123Z'),
                             ('retrieved_at', 'yesterday'), ('selected_version', '2'),
                             ('ordering_basis', 'maven_comparable_version_3_9_11')):
            with self.subTest(field=field), self.assertRaises(ValueError):
                result({**reply(req), field: value}, req)

    @unittest.skipUnless(available(), 'safe protocol file primitives unavailable')
    def test_atomic_bounded_messages_duplicate_json_special_files_and_nonfinite_refuse(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'message.json'
            write_message(path, request())
            self.assertEqual(read_message(path), request())
            for data in (b'{"x":1,"x":2}', b'{"x":NaN}', b'[]', b'x' * 16385):
                path.write_bytes(data)
                with self.assertRaises(ValueError):
                    read_message(path)
            with self.assertRaises(ValueError):
                write_message(path, {'body': 'x' * 16385})
            path.unlink()
            path.symlink_to(Path(directory) / 'missing')
            with self.assertRaises(ValueError):
                read_message(path)


class FakeProcess:
    def __init__(self):
        self.returncode = None
        self.kills = 0
        self.waits = []

    def poll(self):
        return self.returncode

    def kill(self):
        self.kills += 1

    def wait(self, timeout):
        self.waits.append(timeout)
        self.returncode = -9
        return self.returncode


class WorkerHarness:
    def __init__(self, mutate=None, respond=True):
        self.now = 0.0
        self.process = FakeProcess()
        self.factory_calls = []
        self.requests = []
        self.mutate = mutate
        self.respond = respond
        self.path = None
        self.seen = set()

    def factory(self, args, **kwargs):
        self.factory_calls.append((args, kwargs))
        self.path = Path(kwargs['cwd'])
        write_message(self.path / 'ready.json', {'ready': 1})
        return self.process

    def pause(self, seconds):
        self.now += seconds
        if not self.respond:
            return
        for path in self.path.glob('command-*.json'):
            if path.name in self.seen:
                continue
            self.seen.add(path.name)
            req = read_message(path)
            self.requests.append(req)
            value = reply(req, len(self.requests), 100 * len(self.requests))
            if self.mutate:
                self.mutate(value)
            write_message(self.path / f"result-{req['sequence']}.json", value)

    def supervisor(self, capabilities=(CAP,), **kwargs):
        return MavenSupervisor(capabilities, clock=lambda: self.now, pause=self.pause,
                               process_factory=self.factory, **kwargs)


class MavenSupervisorTests(unittest.TestCase):
    def tearDown(self):
        # Tests of deferred lifecycle explicitly replace fake return state and reap.
        self.assertEqual(_DEFERRED, [])

    def test_all_denied_starts_no_worker_and_nonadmitted_same_ga_cannot_borrow(self):
        harness = WorkerHarness()
        with harness.supervisor(()) as supervisor:
            with self.assertRaises(ValueError):
                supervisor.select_target(CAP)
        self.assertEqual(harness.factory_calls, [])
        with harness.supervisor() as supervisor:
            with self.assertRaises(ValueError):
                supervisor.select_target(MavenCapability('g', 'a', 'denied'))
            with self.assertRaises(ValueError):
                supervisor.pom_date(CAP, 'not-selected')
        self.assertEqual(harness.factory_calls, [])

    @unittest.skipUnless(available(), 'safe protocol file primitives unavailable')
    def test_trusted_spawn_closed_capabilities_target_then_dates_cache_and_counters(self):
        harness = WorkerHarness()
        with harness.supervisor() as supervisor:
            selected = supervisor.select_target(CAP)
            self.assertEqual(selected.version, '2')
            self.assertEqual(supervisor.select_target(CAP), selected)
            self.assertIsNotNone(supervisor.pom_date(CAP).last_modified)
            self.assertIsNotNone(supervisor.pom_date(CAP, '2').last_modified)
            self.assertEqual((supervisor.attempts, supervisor.body_bytes), (3, 300))
            self.assertEqual(len(harness.requests), 3)
            args, options = harness.factory_calls[0]
            self.assertEqual(args[1], '-I')
            self.assertEqual(Path(args[2]), Path(__file__).resolve().parents[1] / 'libyears/maven_worker.py')
            self.assertEqual(options['env'], {})
            self.assertFalse(options['shell'])
            self.assertEqual(options['stdin'], subprocess.DEVNULL)
        self.assertEqual(harness.process.kills, 1)
        self.assertLessEqual(max(harness.process.waits), .5)
        self.assertFalse(harness.path.exists())

    @unittest.skipUnless(available(), 'safe protocol file primitives unavailable')
    def test_failed_representations_cache_and_do_not_admit_arbitrary_target_date(self):
        def failure(value):
            value.update(selected_version=None, reason=MavenReason.NO_STABLE_RELEASE)
        harness = WorkerHarness(mutate=failure)
        with harness.supervisor() as supervisor:
            one = supervisor.select_target(CAP)
            self.assertEqual(one.reason, MavenReason.NO_STABLE_RELEASE)
            self.assertEqual(supervisor.select_target(CAP), one)
            self.assertEqual(len(harness.requests), 1)
            with self.assertRaises(ValueError):
                supervisor.pom_date(CAP, '2')

    @unittest.skipUnless(available(), 'safe protocol file primitives unavailable')
    def test_bad_protocol_death_deadline_never_restart_or_fallback(self):
        for mutate in (lambda v: v.update(group_id='other'), lambda v: v.update(attempts=0),
                       lambda v: v.update(body_bytes=64 * 1024 * 1024),
                       lambda v: v.update(retrieved_at='9999-01-01T00:00:00Z')):
            harness = WorkerHarness(mutate=mutate)
            with harness.supervisor() as supervisor:
                self.assertEqual(supervisor.select_target(CAP).reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
                self.assertEqual(supervisor.pom_date(CAP).reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
                self.assertEqual(len(harness.factory_calls), 1)
                self.assertEqual(len(harness.requests), 1)
        harness = WorkerHarness(respond=False)
        with harness.supervisor() as supervisor:
            self.assertEqual(supervisor.select_target(CAP).reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
            self.assertLessEqual(harness.now, 10.01)
            self.assertTrue(supervisor.cancelled)
            self.assertEqual(harness.process.kills, 1)

    @unittest.skipUnless(available(), 'safe protocol file primitives unavailable')
    def test_cumulative_ga_scan_attempt_byte_budgets_not_reset_per_module(self):
        harness = WorkerHarness()
        other = MavenCapability('other', 'a', '1')
        with harness.supervisor((CAP, other)) as supervisor:
            supervisor.select_target(CAP)
            harness.now = 60.0
            self.assertEqual(supervisor.pom_date(CAP).reason, MavenReason.METADATA_BUDGET_EXCEEDED)
            harness.now = 300.0
            self.assertEqual(supervisor.select_target(other).reason, MavenReason.METADATA_BUDGET_EXCEEDED)
            self.assertEqual(len(harness.requests), 1)
        for field, value in (('attempts', 300), ('body_bytes', 64 * 1024 * 1024)):
            harness = WorkerHarness()
            with harness.supervisor() as supervisor:
                setattr(supervisor, field, value)
                self.assertEqual(supervisor.select_target(CAP).reason, MavenReason.METADATA_BUDGET_EXCEEDED)
                self.assertEqual(harness.factory_calls, [])

    @unittest.skipUnless(available(), 'safe protocol file primitives unavailable')
    def test_success_survives_later_protocol_death_and_invalid_readiness_never_issues_command(self):
        harness = WorkerHarness()
        with harness.supervisor() as supervisor:
            target = supervisor.select_target(CAP)
            harness.mutate = lambda value: value.update(sequence=999)
            self.assertEqual(supervisor.pom_date(CAP).reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
            self.assertEqual(supervisor.select_target(CAP), target)
            self.assertEqual(len(harness.requests), 2)
        harness = WorkerHarness()
        original = harness.factory
        def factory(args, **kwargs):
            child = original(args, **kwargs)
            write_message(harness.path / 'ready.json', {'ready': True})
            return child
        with MavenSupervisor((CAP,), process_factory=factory) as supervisor:
            self.assertEqual(supervisor.select_target(CAP).reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
        self.assertEqual(harness.requests, [])
        self.assertEqual(harness.process.kills, 1)

    @unittest.skipUnless(available(), 'safe protocol file primitives unavailable')
    def test_explicit_ca_special_file_link_and_oversize_are_refused_before_spawn(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            real = base / 'real.pem'
            real.write_bytes(b'fixture')
            linked = base / 'link.pem'
            linked.symlink_to(real)
            empty = base / 'empty.pem'
            empty.write_bytes(b'')
            large = base / 'large.pem'
            large.write_bytes(b'x' * (4 * 1024 * 1024 + 1))
            paths = [linked, empty, large]
            if hasattr(os, 'mkfifo'):
                fifo = base / 'fifo.pem'
                os.mkfifo(fifo)
                paths.append(fifo)
            for path in paths:
                harness = WorkerHarness()
                with harness.supervisor(ca_bundle=path) as supervisor:
                    self.assertEqual(supervisor.select_target(CAP).reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
                self.assertEqual(harness.factory_calls, [])

    def test_missing_native_capability_refuses_without_process_or_permissive_fallback(self):
        harness = WorkerHarness()
        with patch('libyears.maven_supervisor.available', return_value=False), harness.supervisor() as supervisor:
            self.assertEqual(supervisor.select_target(CAP).reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
        self.assertEqual(harness.factory_calls, [])

    @unittest.skipUnless(available(), 'safe protocol file primitives unavailable')
    def test_unreaped_handle_retained_and_forbids_all_further_io_until_nonblocking_reap(self):
        harness = WorkerHarness(respond=False)
        harness.process.wait = Mock(side_effect=subprocess.TimeoutExpired('trusted', .5))
        supervisor = harness.supervisor()
        self.assertEqual(supervisor.select_target(CAP).reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
        self.assertIn(supervisor, _DEFERRED)
        self.assertTrue(harness.path.exists())
        another = WorkerHarness()
        with another.supervisor() as blocked:
            self.assertEqual(blocked.select_target(CAP).reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
        self.assertEqual(another.factory_calls, [])
        self.assertFalse(supervisor.reap_deferred())
        harness.process.returncode = -9
        harness.process.wait = Mock(return_value=-9)
        self.assertTrue(supervisor.reap_deferred())
        self.assertFalse(harness.path.exists())


@unittest.skipUnless(available(), 'safe protocol file primitives unavailable')
class MavenNativeWorkerTests(unittest.TestCase):
    def test_real_blocked_worker_is_killed_and_reaped_with_bounded_command_deadline(self):
        fixture = Path(__file__).resolve().parent / 'fixtures/maven/blocking_worker.py'
        spawned = []
        def factory(args, **kwargs):
            args = [*args[:2], str(fixture)]
            child = subprocess.Popen(args, **kwargs)
            spawned.append(child)
            return child
        with patch('libyears.maven_supervisor.COMMAND_SECONDS', .7):
            with MavenSupervisor((CAP,), process_factory=factory) as supervisor:
                supervisor._start()
                started = time.monotonic()
                answer = supervisor.select_target(CAP)
                self.assertLess(time.monotonic() - started, 3)
                self.assertEqual(answer.reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
                self.assertTrue(supervisor.cancelled)
                self.assertIsNotNone(spawned[0].poll())
                self.assertEqual(supervisor.pom_date(CAP).reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
        self.assertEqual(len(spawned), 1)

    def test_real_readiness_uses_installed_imports_private_cwd_and_only_staged_explicit_ca(self):
        with tempfile.TemporaryDirectory() as directory:
            ca = Path(directory) / 'explicit.pem'
            ca.write_bytes(b'explicit-test-CA-bytes; readiness does not load TLS or issue GETs')
            seen = []
            def factory(args, **kwargs):
                path = Path(kwargs['cwd'])
                (path / 'libyears').mkdir()
                (path / 'libyears/__init__.py').write_text('raise RuntimeError("untrusted cwd import")')
                (path / 'sitecustomize.py').write_text('raise RuntimeError("untrusted site import")')
                self.assertEqual((path / 'trust.pem').read_bytes(), ca.read_bytes())
                self.assertEqual(kwargs['env'], {})
                process = subprocess.Popen(args, **kwargs)
                seen.append(process)
                return process
            with patch.dict('os.environ', {'PYTHONPATH': directory, 'SSL_CERT_FILE': '/never/read',
                                           'HTTPS_PROXY': 'https://private.invalid'}):
                with MavenSupervisor((CAP,), ca_bundle=ca, process_factory=factory) as supervisor:
                    supervisor._start()  # readiness has no command and performs no GET
                    self.assertIsNone(seen[0].poll())
                    self.assertEqual(supervisor.attempts, 0)
                    self.assertFalse(list(supervisor.directory.glob('command-*.json')))
            self.assertIsNotNone(seen[0].poll())


if __name__ == '__main__':
    unittest.main()
