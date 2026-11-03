"""Offline process/controller witnesses for the P1 NuGet boundary."""

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import tempfile
import io
import threading
import time
import unittest
from unittest.mock import patch

from libyears.model import NuGetPublication
from libyears.nuget_provenance import LocalAuthority
import libyears.nuget_supervisor as supervision
from libyears.nuget_supervisor import (
    NuGetSupervisor, NuGetWorkerFailure, PackageResult, PROTOCOL_LIMIT,
    authority_message, decode_authority, decode_result, read_message,
    result_message, write_message,
)

AUTHORITY = LocalAuthority('a' * 64, 'b' * 64, 'example', '1.0.0', b'x' * 64)
FAILURE = result_message(PackageResult(reason='registry_error'))


class Clock:
    def __init__(self):
        self.now = 100.0
        self.waits = []
        self.callback = None

    def __call__(self):
        return self.now

    def pause(self, seconds):
        if seconds < 0 or seconds > .010001:
            raise AssertionError('unbounded poll')
        self.waits.append(seconds)
        self.now += seconds
        if self.callback:
            self.callback()


class BodySource:
    """Simulated worker-side in-flight operation, independent of its deadlines."""

    def __init__(self, stage):
        self.stage = stage
        self.bytes_read = 0
        self.last_byte_time = 0
        self.read_times = []
        self.blocked = stage != 'drip'

    def progress(self, elapsed):
        # A body drip emits one byte per second, far below every T007 byte cap
        # and the 10-second inactivity timeout. Other stages remain blocked.
        if self.stage == 'drip' and elapsed >= self.last_byte_time + 1:
            self.last_byte_time += 1
            self.bytes_read += len(self.read())
            self.read_times.append(self.last_byte_time)

    def read(self):
        return b'x'



class Process:
    def __init__(self, clock, path, *, ignore_terminate=False, unreapable=False):
        self.clock = clock
        self.path = path
        self.ignore_terminate = ignore_terminate
        self.unreapable = unreapable
        self.alive = True
        self.calls = []
        self.waits = []
        self.stdin = io.BytesIO()
        self.stdout = io.BytesIO()
        self.stderr = io.BytesIO()
        self._handle = unittest.mock.Mock()

    def poll(self):
        return None if self.alive else 0

    def terminate(self):
        self.calls.append('terminate')
        if not self.ignore_terminate:
            self.alive = False

    def kill(self):
        self.calls.append('kill')
        if not self.unreapable:
            self.alive = False

    def wait(self, timeout):
        self.waits.append(timeout)
        if self.alive:
            self.clock.now += timeout
            raise subprocess.TimeoutExpired('trusted worker', timeout)
        return 0


class ControllerTests(unittest.TestCase):
    def make_supervisor(self, *, ready=True, **options):
        self.clock = Clock()
        self.spawn_calls = []
        def spawn(command, **kwargs):
            self.spawn_calls.append((command, kwargs))
            self.path = Path(kwargs['cwd'])
            self.process = Process(self.clock, self.path, **options)
            if ready:
                write_message(self.path / 'ready.json', {'ready': 1})
            return self.process
        self.supervisor = NuGetSupervisor(clock=self.clock, pause=self.clock.pause,
                                          process_factory=spawn)
        self.addCleanup(self.supervisor.close)
        return self.supervisor

    def publish(self):
        command = read_message(self.path / 'command.json')
        (self.path / 'command.json').unlink()
        write_message(self.path / 'result.json', {
            'sequence': command['sequence'], 'result': FAILURE})
        return command

    def test_bootstrap_offline_readiness_and_fixed_command_deadlines(self):
        supervisor = self.make_supervisor()
        commands = []
        def complete():
            commands.append(self.publish())
        self.clock.callback = complete
        self.assertEqual(supervisor.lookup(AUTHORITY).reason, 'registry_error')
        command, options = self.spawn_calls[0]
        self.assertEqual(command[1], '-I')
        self.assertTrue(Path(command[2]).is_absolute())
        self.assertFalse(options['shell'])
        self.assertEqual([options[k] for k in ('stdin', 'stdout', 'stderr')],
                         [subprocess.DEVNULL] * 3)
        self.assertEqual(commands[0]['package_deadline'], 159.5)
        self.assertEqual(commands[0]['scan_deadline'], 399.5)
        self.assertEqual(decode_authority(commands[0]['authority']), AUTHORITY)
        supervisor.close()
        self.assertFalse(self.path.exists())
        self.assertFalse(self.process.alive)
        self.assertTrue(self.process.stdin.closed)
        self.assertTrue(self.process.stdout.closed)
        self.assertTrue(self.process.stderr.closed)
        self.process._handle.Close.assert_called_once()

    def test_blocked_stages_and_drip_progress_cannot_extend_deadline(self):
        # Each model never consults the parent clock; drip progress is below all
        # byte/socket caps. An admission-only or socket-only mutation leaves it alive.
        for stage in ('dns', 'connect', 'tls', 'headers', 'body', 'parsing', 'traversal', 'drip', 'index'):
            with self.subTest(stage=stage):
                supervisor = self.make_supervisor(ignore_terminate=True)
                source = BodySource(stage)
                admitted = self.clock()
                self.clock.callback = lambda: source.progress(self.clock() - admitted)
                result = supervisor.lookup(AUTHORITY)
                self.assertEqual(result.reason, 'registry_error')
                self.assertEqual(self.process.calls, ['terminate', 'kill'])
                self.assertLessEqual(self.clock(), 160)
                self.assertLessEqual(self.process.waits[0], .25)
                self.assertFalse(self.process.alive)
                self.assertFalse(self.path.exists())
                if stage == 'drip':
                    self.assertGreater(source.bytes_read, 50)
                    self.assertLess(source.bytes_read, 100)
                    self.assertTrue(all(b - a == 1 for a, b in zip(source.read_times, source.read_times[1:])))
                else:
                    self.assertTrue(source.blocked)
                    self.assertEqual(source.bytes_read, 0)
                self.assertEqual(supervisor.lookup(AUTHORITY).reason, 'registry_error')
                self.assertEqual(len(self.spawn_calls), 1)

    def test_scan_cutoff_wins_preserving_earlier_result_and_exhaustion(self):
        supervisor = self.make_supervisor(ignore_terminate=True)
        self.clock.callback = self.publish
        first = supervisor.lookup(AUTHORITY)
        self.clock.now = 390
        self.clock.callback = None
        self.assertEqual(supervisor.lookup(AUTHORITY).reason, 'registry_error')
        self.assertEqual(first.reason, 'registry_error')
        self.assertLessEqual(self.clock(), 400)
        self.assertEqual(len(self.spawn_calls), 1)

    def test_success_exact_late_and_post_validation_cutoff(self):
        for completion in ('early', 'exact', 'late', 'validation'):
            with self.subTest(completion=completion):
                supervisor = self.make_supervisor()
                def complete():
                    self.publish()
                    if completion in ('exact', 'late'):
                        self.clock.now = 159.5 + (completion == 'late')
                self.clock.callback = complete
                original = supervision.decode_result
                def decode(value):
                    result = original(value)
                    if completion == 'validation':
                        self.clock.now = 159.5
                    return result
                with patch.object(supervision, 'decode_result', side_effect=decode):
                    supervisor.lookup(AUTHORITY)
                self.assertEqual(supervisor.cancelled, completion != 'early')
                supervisor.close()

    def test_earlier_success_survives_later_cutoff_and_no_restart(self):
        supervisor = self.make_supervisor(ignore_terminate=True)
        publication = NuGetPublication('1.0.0', datetime(2020, 1, 1, tzinfo=timezone.utc), True)
        success = PackageResult(None, 'public_content_verified', 'public_agreement', publication, publication)
        def complete():
            command = read_message(self.path / 'command.json')
            (self.path / 'command.json').unlink()
            write_message(self.path / 'result.json', {
                'sequence': command['sequence'], 'result': result_message(success)})
        self.clock.callback = complete
        first = supervisor.lookup(AUTHORITY)
        self.clock.now = 390
        self.clock.callback = None
        second = supervisor.lookup(AUTHORITY)
        self.assertEqual(first, success)
        self.assertEqual(second.reason, 'registry_error')
        self.assertEqual(supervisor.lookup(AUTHORITY).reason, 'registry_error')
        self.assertEqual(len(self.spawn_calls), 1)

    def test_socket_only_admission_mutation_fails_blocking_witness(self):
        # Execute a deliberate admission-only mutant against the same fake blocked
        # worker. Progress always happens before a socket inactivity timeout, so
        # only the supervisor's independent parent cutoff can satisfy the witness.
        supervisor = self.make_supervisor(ignore_terminate=True)
        supervisor._start()
        admitted = self.clock()
        source = BodySource('drip')
        self.clock.callback = lambda: source.progress(self.clock() - admitted)
        def socket_only_mutant():
            self.assertLess(self.clock(), admitted + 60)  # sole admission check
            for unused in range(6100):
                self.clock.pause(.01)  # below inactivity/byte caps; never EOF
        socket_only_mutant()
        self.assertGreaterEqual(source.bytes_read, 60)
        self.assertLess(source.bytes_read, 100)
        with self.assertRaises(AssertionError):
            self.assertFalse(self.process.alive)
        with self.assertRaises(AssertionError):
            self.assertLessEqual(self.clock(), admitted + 60)
        supervisor.close()

    def test_already_exhausted_scan_does_not_publish_command(self):
        supervisor = self.make_supervisor()
        supervisor._start()
        supervisor.scan_deadline = self.clock() + .5
        supervisor.lookup(AUTHORITY)
        self.assertEqual(supervisor.sequence, 0)
        self.assertFalse(self.process.alive)

    def test_corrupt_oversized_and_abrupt_death_fail_closed(self):
        for mode in ('corrupt', 'oversized', 'death', 'duplicate', 'wrong_sequence'):
            with self.subTest(mode=mode):
                supervisor = self.make_supervisor()
                def break_worker():
                    if mode == 'death':
                        self.process.alive = False
                    elif mode == 'wrong_sequence':
                        write_message(self.path / 'result.json', {'sequence': True, 'result': FAILURE})
                    else:
                        body = {'corrupt': b'{', 'oversized': b' ' * (PROTOCOL_LIMIT + 1),
                                'duplicate': b'{"sequence":1,"sequence":1}'}[mode]
                        (self.path / 'result.json').write_bytes(body)
                self.clock.callback = break_worker
                self.assertEqual(supervisor.lookup(AUTHORITY).reason, 'registry_error')
                self.assertTrue(supervisor.cancelled)
                self.assertFalse(self.path.exists())
                self.assertFalse(self.process.alive)

    def test_interruption_cleans_up_and_propagates(self):
        supervisor = self.make_supervisor(ignore_terminate=True)
        def interrupt():
            raise KeyboardInterrupt()
        self.clock.callback = interrupt
        with self.assertRaises(KeyboardInterrupt):
            supervisor.lookup(AUTHORITY)
        self.assertFalse(self.process.alive)
        self.assertFalse(self.path.exists())

    def test_kill_and_reap_os_fault_is_systemic_and_deferred(self):
        supervisor = self.make_supervisor(ignore_terminate=True)
        supervisor._start()
        with patch.object(self.process, 'kill', side_effect=OSError('SECRET')):
            with self.assertRaises(NuGetWorkerFailure) as raised:
                supervisor.lookup(AUTHORITY)
        self.assertNotIn('SECRET', str(raised.exception))
        self.assertTrue(self.path.exists())
        self.assertFalse(self.process.stdin.closed)
        self.process.alive = False
        supervisor.reap_deferred()
        self.assertTrue(self.process.stdin.closed)

    def test_startup_failure_is_safe_systemic_without_fallback(self):
        supervisor = self.make_supervisor()
        supervisor.process_factory = unittest.mock.Mock(side_effect=OSError('SECRET'))
        with self.assertRaises(NuGetWorkerFailure) as raised:
            supervisor.lookup(AUTHORITY)
        self.assertEqual(str(raised.exception), 'NuGet worker unavailable')
        self.assertTrue(supervisor.cancelled)
        self.assertIsNone(supervisor.directory)
        self.assertEqual(supervisor.sequence, 0)

    def test_protocol_bad_enum_types_and_ready_bool_are_rejected(self):
        supervisor = self.make_supervisor()
        def invalid():
            command = read_message(self.path / 'command.json')
            value = dict(FAILURE, reason=['SECRET'])
            write_message(self.path / 'result.json', {'sequence': command['sequence'], 'result': value})
        self.clock.callback = invalid
        self.assertEqual(supervisor.lookup(AUTHORITY).reason, 'registry_error')
        self.assertFalse(self.path.exists())
        supervisor = self.make_supervisor(ready=False)
        original = supervisor.process_factory
        def spawn(*args, **kwargs):
            process = original(*args, **kwargs)
            write_message(self.path / 'ready.json', {'ready': True})
            return process
        supervisor.process_factory = spawn
        with self.assertRaises(NuGetWorkerFailure):
            supervisor.lookup(AUTHORITY)

    def test_readiness_timeout_is_systemic_and_no_command(self):
        supervisor = self.make_supervisor(ready=False)
        with self.assertRaises(NuGetWorkerFailure):
            supervisor.lookup(AUTHORITY)
        self.assertLessEqual(self.clock(), 110.5)
        self.assertEqual(supervisor.sequence, 0)
        self.assertFalse(self.path.exists())

    def test_unreaped_process_retains_path_then_nonblocking_reap(self):
        supervisor = self.make_supervisor(ignore_terminate=True, unreapable=True)
        with self.assertRaises(NuGetWorkerFailure):
            supervisor.lookup(AUTHORITY)
        self.assertTrue(self.path.exists())
        self.assertIn(supervisor, supervision._DEFERRED)
        self.assertLessEqual(self.clock(), 160)
        self.assertEqual(supervisor.lookup(AUTHORITY).reason, 'registry_error')
        with self.assertRaises(NuGetWorkerFailure):
            supervisor.reap_deferred()
        self.assertEqual(self.process.waits[-1], 0)
        self.process.alive = False
        supervisor.reap_deferred()
        self.assertFalse(self.path.exists())
        self.assertNotIn(supervisor, supervision._DEFERRED)


class ProtocolTests(unittest.TestCase):
    def test_authority_round_trip_and_no_raw_diagnostics(self):
        self.assertEqual(decode_authority(authority_message(AUTHORITY)), AUTHORITY)
        with self.assertRaises(ValueError):
            authority_message(object())
        with self.assertRaises(ValueError):
            decode_result({'reason': 'SECRET'})

    def test_typed_success_and_staged_failure_round_trip(self):
        publication = NuGetPublication('1.0.0', datetime(2020, 1, 1, tzinfo=timezone.utc), False)
        for result in (PackageResult(None, 'public_content_verified', 'public_agreement', publication, publication),
                       PackageResult('release_date_missing', 'public_content_verified', 'public_agreement', publication),
                       PackageResult('content_hash_mismatch', 'asserted_public', 'mismatch')):
            self.assertEqual(decode_result(result_message(result)), result)
        with self.assertRaises(ValueError):
            result_message(PackageResult(None))

    def test_bounded_regular_files_atomic_publication_and_closed_handles(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'message.json'
            write_message(path, {'value': 'x'})
            self.assertEqual(read_message(path), {'value': 'x'})
            path.unlink()  # Windows also requires the read handle to be closed.
            path.write_bytes(b'x' * (PROTOCOL_LIMIT + 1))
            with self.assertRaises(ValueError):
                read_message(path)
            path.unlink()
            path.mkdir()
            with self.assertRaises(ValueError):
                read_message(path)


class WorkerHandlerTests(unittest.TestCase):
    def test_socket_inactivity_failure_maps_to_registry_error(self):
        from libyears.nuget_registry import NuGetMetadataClient, NuGetRegistryFailure
        transport = unittest.mock.Mock()
        transport.get.side_effect = TimeoutError('SECRET')
        client = NuGetMetadataClient(transport=transport, clock=lambda: 100)
        client.begin_package('example', package_deadline=159.5, scan_deadline=399.5)
        with self.assertRaises(NuGetRegistryFailure) as raised:
            client.get_json('https://api.nuget.org/v3/registration5-gz-semver2/example/index.json')
        self.assertEqual(raised.exception.reason, 'registry_error')
        self.assertEqual(str(raised.exception), 'registry_error')
        self.assertEqual(client.scan_requests, 1)

    def test_worker_retains_one_client_and_uses_parent_working_deadlines(self):
        from libyears import nuget_worker
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            commands = [
                {'sequence': number, 'authority': authority_message(AUTHORITY),
                 'package_deadline': 159.5 + number, 'scan_deadline': 399.5}
                for number in (1, 2)]
            clients = []
            calls = []
            def handler(authority, client):
                self.assertTrue((path / 'ready.json').exists())
                self.assertEqual(authority, AUTHORITY)
                clients.append(client)
                if len(clients) == 2:
                    raise KeyboardInterrupt()
                client.scan_requests = 7
                return PackageResult(reason='registry_error')
            def read(unused):
                return commands.pop(0)
            def publish(unused, value):
                calls.append(value)
            from libyears.nuget_registry import NuGetMetadataClient
            client = NuGetMetadataClient(clock=lambda: 100)
            client.begin_package = unittest.mock.Mock(wraps=client.begin_package)
            with patch.object(nuget_worker.Path, 'cwd', return_value=path), \
                    patch.object(nuget_worker, 'NuGetMetadataClient', return_value=client), \
                    patch.object(nuget_worker, 'read_message', side_effect=read), \
                    patch.object(nuget_worker, 'write_message', side_effect=publish), \
                    patch.object(nuget_worker.Path, 'exists', return_value=True), \
                    patch.object(nuget_worker.Path, 'unlink'), \
                    patch.object(nuget_worker.time, 'monotonic', return_value=100):
                with self.assertRaises(KeyboardInterrupt):
                    nuget_worker.run_worker(handler)
            self.assertEqual(calls[0], {'ready': 1})
            self.assertIs(clients[0], clients[1])
            self.assertEqual(client.scan_requests, 7)
            self.assertEqual(client.begin_package.call_args_list, [
                unittest.mock.call('example', package_deadline=160.5, scan_deadline=399.5),
                unittest.mock.call('example', package_deadline=161.5, scan_deadline=399.5)])



class RealWorkerTests(unittest.TestCase):
    def test_isolated_installed_worker_ready_without_handler_or_network(self):
        supervisor = NuGetSupervisor()
        try:
            supervisor._start()
            path = supervisor.path
            self.assertIsNone(supervisor.scan_deadline)
            self.assertFalse((path / 'command.json').exists())
        finally:
            supervisor.close()
        self.assertIsNotNone(supervisor.process.poll())
        self.assertFalse(path.exists())

    def test_offline_blocked_worker_cancelled_with_outer_watchdog(self):
        fixture = Path(__file__).parent / 'fixtures' / 'nuget' / 'blocking_worker.py'
        supervisor = NuGetSupervisor(worker_entry=fixture)
        watchdog_fired = threading.Event()
        def watchdog():
            watchdog_fired.set()
            if supervisor.process is not None and supervisor.process.poll() is None:
                supervisor.process.kill()
        timer = threading.Timer(15, watchdog)
        timer.start()
        try:
            supervisor._start()
            # Preserve the real bootstrap witness, then control metadata time.
            # Entry is observed, never inferred from a short startup sleep.
            clock = Clock()
            clock.now = time.monotonic()
            admitted = clock()
            cutoff = admitted + supervision.PACKAGE_SECONDS - supervision.CLEANUP_SECONDS
            entry_observation_limit = time.monotonic() + 5
            polling = threading.Event()
            def pause(seconds):
                self.assertGreaterEqual(seconds, 0)
                self.assertLessEqual(seconds, supervision.POLL_SECONDS)
                if ((supervisor.path / 'handler-entered.json').exists()
                        or time.monotonic() >= entry_observation_limit):
                    # Advance to the original cutoff, without resetting either
                    # deadline. The real-time limit only bounds missing evidence.
                    clock.now = cutoff
                else:
                    polling.wait(seconds)
            supervisor.clock = clock
            supervisor.pause = pause
            observations = []
            terminate = supervisor.process.terminate
            def observe_termination():
                entry = supervisor.path / 'handler-entered.json'
                observations.append({
                    'entry': read_message(entry) if entry.exists() else None,
                    'alive': supervisor.process.poll() is None,
                    'command_pending': (supervisor.path / 'command.json').exists(),
                    'result': (supervisor.path / 'result.json').exists(),
                    'returned': (supervisor.path / 'handler-returned.json').exists(),
                    'cutoff': clock(),
                })
                terminate()
            with patch.object(supervisor.process, 'terminate', side_effect=observe_termination) as stopped, \
                    patch.object(supervisor.process, 'wait', wraps=supervisor.process.wait) as waited:
                self.assertEqual(supervisor.lookup(AUTHORITY).reason, 'registry_error')
            self.assertEqual(len(observations), 1)
            observation = observations[0]
            self.assertIsNotNone(observation['entry'], 'blocking handler was not entered')
            self.assertEqual(observation['entry'], {
                'pid': supervisor.process.pid, 'authority': authority_message(AUTHORITY),
                'package_deadline': cutoff,
                'scan_deadline': admitted + supervision.SCAN_SECONDS - supervision.CLEANUP_SECONDS,
            })
            self.assertTrue(observation['alive'])
            self.assertFalse(observation['command_pending'])
            self.assertFalse(observation['result'])
            self.assertFalse(observation['returned'])
            self.assertEqual(observation['cutoff'], cutoff)
            self.assertEqual(supervisor.scan_deadline, admitted + supervision.SCAN_SECONDS)
            stopped.assert_called_once_with()
            self.assertGreaterEqual(waited.call_count, 1)
            self.assertLessEqual(waited.call_args_list[0].kwargs['timeout'], .25)
            for call in waited.call_args_list:
                self.assertGreaterEqual(call.kwargs['timeout'], 0)
                self.assertLessEqual(call.kwargs['timeout'], supervision.CLEANUP_SECONDS)
            self.assertTrue(supervisor.cancelled)
            self.assertIsNotNone(supervisor.process.returncode)
            self.assertIsNotNone(supervisor.process.poll())
            self.assertFalse(supervisor.path.exists())
            self.assertFalse(watchdog_fired.is_set())
        finally:
            timer.cancel()
            timer.join(timeout=1)
            supervisor.close()

    def test_suppressing_command_fails_real_blocking_handler_witness(self):
        original = supervision.write_message
        suppressed = []
        def suppress_command(path, value):
            if path.name == 'command.json':
                suppressed.append(path)
                return
            original(path, value)
        # Exercise exactly the positive witness with only command publication
        # removed. An idle ready worker must fail its entry assertion.
        with patch.object(supervision, 'write_message', side_effect=suppress_command):
            with self.assertRaisesRegex(AssertionError, 'blocking handler was not entered'):
                self.test_offline_blocked_worker_cancelled_with_outer_watchdog()
        self.assertEqual(len(suppressed), 1)


if __name__ == '__main__':
    unittest.main()
