"""Closed SBOM-only profiles: request accounting, reuse and hard cancellation."""
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.cli import main
from libyears.maven import MavenCapability
from libyears.maven_http import MavenHTTPClient
from libyears.maven_model import MavenReason
from libyears.maven_protocol import available, command, result, execution_limits
from libyears.maven_supervisor import MavenSupervisor, _DEFERRED
from libyears.maven_worker import worker_profile
from libyears.sbom_document import accept_document
from libyears.sbom_identity import canonical_members
from libyears.sbom_measure import measure_members, summarize_members
from libyears.sbom_model import SbomRequest, SbomRequestError
from libyears.sbom_policy import admit_members
import test_maven_worker as worker_fixtures
import test_maven_http as http_fixtures
from test_maven_registry import catalogue
from test_sbom_document import snapshot, synthetic_document
from test_sbom_identity import maven_component


class BudgetContractTests(unittest.TestCase):
    def test_closed_profiles_and_worker_arguments(self):
        self.assertEqual(execution_limits(), (300, 300.0))
        self.assertEqual(execution_limits(True), (600, 600.0))
        for invalid in (1, 0, 'extended', None):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                execution_limits(invalid)
        self.assertFalse(worker_profile([]))
        self.assertTrue(worker_profile(['--sbom-extended-budget']))
        for args in (['extended'], ['--sbom-extended-budget'] * 2, ['--url', 'https://private.invalid']):
            with self.assertRaises(ValueError):
                worker_profile(args)
        for invalid in ('unknown', True, []):
            with self.assertRaises(SbomRequestError):
                SbomRequest(budget=invalid)
        with self.assertRaises(SbomRequestError):
            SbomRequest(disabled=True, budget='extended')

    def test_protocol_profile_boundaries_and_strict_counters(self):
        for extended, limit in ((False, 300), (True, 600)):
            req = worker_fixtures.request(sequence=limit)
            self.assertEqual(command(req, sbom_extended=extended), req)
            self.assertEqual(result(worker_fixtures.reply(req, attempts=limit), req,
                                    sbom_extended=extended)['attempts'], limit)
            with self.assertRaises(ValueError):
                command({**req, 'sequence': limit + 1}, sbom_extended=extended)
            with self.assertRaises(ValueError):
                result(worker_fixtures.reply(req, attempts=limit + 1), req, sbom_extended=extended)
        with self.assertRaises(ValueError):
            command(worker_fixtures.request(sequence=301))

    def test_cli_closed_option_routing_and_private_rejections(self):
        with tempfile.TemporaryDirectory() as directory:
            for profile in ('standard', 'extended'):
                scan = Mock(side_effect=RuntimeError('captured'))
                # Capture the normalized request before any reader or transport.
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    main([directory, '--sbom-budget', profile], scan=scan)
                self.assertEqual(scan.call_args.kwargs['sbom_request'], SbomRequest(budget=profile))
            target = Path(directory) / 'requirements.txt';target.write_text('')
            bad = [([directory, '--sbom-bud', 'extended']),
                   ([directory, '--sbom-budget', 'private-value']),
                   ([directory, '--sbom-budget', 'extended', '--sbom-budget', 'standard']),
                   ([directory, '--sbom-budget', 'standard', '--no-sbom']),
                   ([str(target), '--sbom-budget', 'extended'])]
            for args in bad:
                scan = Mock();errors = io.StringIO()
                with redirect_stderr(errors):
                    self.assertEqual(main(args, scan=scan), 1)
                scan.assert_not_called()
                self.assertIn('invalid SBOM command line arguments', errors.getvalue())
                self.assertNotIn('private-value', errors.getvalue())

    def test_http_extended_request_and_scan_caps_without_sibling_expansion(self):
        fixture = http_fixtures.MavenHTTPTests()
        for extended, limit in ((False, 300), (True, 600)):
            client = fixture.client(http_fixtures.raw_response(b'not XML'), sbom_extended=extended)
            for _ in range(limit):
                fixture.lookup(client)
            with self.assertRaises(http_fixtures.RegistryFailure) as failure:
                fixture.lookup(client)
            self.assertEqual(failure.exception.reason, MavenReason.METADATA_BUDGET_EXCEEDED)
            self.assertEqual(client.attempts, limit)
            self.assertEqual(len(fixture.connections), limit)
        now = [0.0]
        client = fixture.client(http_fixtures.raw_response(catalogue()),
                                sbom_extended=True, clock=lambda: now[0])
        now[0] = 300.0
        client.lookup('select_target', 'new', 'a', None, 310)
        now[0] = 600.0
        with self.assertRaises(http_fixtures.RegistryFailure):
            client.lookup('select_target', 'other', 'a', None, 610)
        self.assertEqual(client.attempts, 1)

    def test_http_extended_retains_tls_and_endpoint_admission(self):
        connections = Mock(side_effect=AssertionError('network'))
        for context in (Mock(verify_mode=0, check_hostname=True),
                        Mock(verify_mode=2, check_hostname=False)):
            client = MavenHTTPClient(sbom_extended=True, connection_factory=connections,
                                     context_factory=lambda unused: context)
            with self.assertRaises(http_fixtures.RegistryFailure):
                client.lookup('select_target', 'g', 'a', None, client.clock() + 10)
        client = MavenHTTPClient(sbom_extended=True, connection_factory=connections)
        with self.assertRaises(http_fixtures.RegistryFailure):
            client.lookup('select_target', 'https://private', 'a', None, client.clock() + 10)
        connections.assert_not_called()


@unittest.skipUnless(available(), 'safe protocol file primitives unavailable')
class BudgetSupervisorTests(unittest.TestCase):
    def tearDown(self):
        self.assertEqual(_DEFERRED, [])

    def test_real_accounted_commands_through600_and_cache_after_exhaustion(self):
        capabilities = tuple(MavenCapability('g', 'a' + str(i), '1') for i in range(601))
        harness = worker_fixtures.WorkerHarness()
        with harness.supervisor(capabilities, sbom_extended=True) as supervisor:
            first = supervisor.select_target(capabilities[0])
            for capability in capabilities[1:600]:
                self.assertIsNone(supervisor.select_target(capability).reason)
            self.assertEqual(supervisor.attempts, 600)
            self.assertEqual(supervisor.select_target(capabilities[600]).reason,
                             MavenReason.METADATA_BUDGET_EXCEEDED)
            self.assertIs(supervisor.select_target(capabilities[0]), first)
            self.assertEqual(len(harness.requests), 600)
            self.assertEqual(harness.factory_calls[0][0][-1], '--sbom-extended-budget')
        self.assertEqual(harness.process.kills, 1)

    def test_extended_scan_ga_and_command_deadlines_remain_bounded(self):
        caps = (worker_fixtures.CAP, MavenCapability('other', 'a', '1'))
        harness = worker_fixtures.WorkerHarness()
        with harness.supervisor(caps, sbom_extended=True) as supervisor:
            first = supervisor.select_target(caps[0])
            harness.now = 60
            self.assertEqual(supervisor.pom_date(caps[0]).reason, MavenReason.METADATA_BUDGET_EXCEEDED)
            harness.now = 600
            self.assertEqual(supervisor.select_target(caps[1]).reason, MavenReason.METADATA_BUDGET_EXCEEDED)
            self.assertIs(supervisor.select_target(caps[0]), first)
        harness = worker_fixtures.WorkerHarness(respond=False)
        with harness.supervisor(sbom_extended=True) as supervisor:
            self.assertEqual(supervisor.select_target(caps[0]).reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
            self.assertLessEqual(harness.now, 10.01)
            self.assertEqual(harness.process.kills, 1)
            self.assertTrue(supervisor.closed)
            self.assertFalse(harness.path.exists())

    def test_repeated_variants_keep_rows_and_success_survives_budget_failure(self):
        records = [maven_component('z', version='1'), maven_component('a', version='1'),
                   maven_component('a', version='1', suffix='?type=pom')]
        doc = accept_document(snapshot(synthetic_document(components=records)))
        members = admit_members(doc, canonical_members(doc))
        harness = worker_fixtures.WorkerHarness()
        def factory(capabilities):
            supervisor = harness.supervisor(capabilities, sbom_extended=True)
            supervisor.attempts = 597
            # The harness starts at result number1; offset cumulative HTTP accounting.
            harness.mutate = lambda value: value.update(attempts=value['attempts'] + 597)
            return supervisor
        result_rows = measure_members(members, supervisor_factory=factory)
        self.assertEqual(len(result_rows), 3)
        self.assertEqual(result_rows[0].reason, MavenReason.METADATA_BUDGET_EXCEEDED)
        self.assertTrue(all(row.age is not None for row in result_rows[1:]))
        self.assertEqual(len(harness.requests), 3)
        self.assertEqual(summarize_members(result_rows).dependencies_measured, 2)

    def test_installed_extended_worker_accepts301_offline_tls_failures(self):
        # Invalid explicit CA fails before connection creation in the isolated worker.
        # No server, resolver, package manager or network fixture is needed.
        caps = tuple(MavenCapability('g', 'a' + str(i), '1') for i in range(301))
        with tempfile.TemporaryDirectory() as directory:
            ca = Path(directory) / 'invalid-test-ca.pem';ca.write_text('invalid test CA')
            with MavenSupervisor(caps, ca_bundle=ca, sbom_extended=True) as supervisor:
                for cap in caps:
                    self.assertEqual(supervisor.select_target(cap).reason, MavenReason.CATALOGUE_UNAVAILABLE)
                self.assertEqual(supervisor.attempts, 301)
                self.assertFalse(supervisor.cancelled)
            self.assertTrue(supervisor.closed)
            self.assertIsNone(supervisor.directory)
