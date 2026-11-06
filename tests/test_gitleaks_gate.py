"""Offline checks for the security gate's scope and failure propagation."""

import subprocess
import unittest
from unittest.mock import patch

from tools import check_gitleaks


class GitLeaksGateTests(unittest.TestCase):
    def run_gate(self, version='8.30.1', shallow='false', exit_code=0):
        responses = [subprocess.CompletedProcess([], 0, version),
                     subprocess.CompletedProcess([], 0, shallow),
                     subprocess.CompletedProcess([], exit_code)]
        with patch.object(check_gitleaks.subprocess, 'run', side_effect=responses) as run:
            status = check_gitleaks.main()
        return status, run

    def test_history_scope_uses_actual_config_and_preserves_scanner_failure(self):
        status, run = self.run_gate(exit_code=1)
        self.assertEqual(status, 1)
        arguments = run.call_args.args[0]
        self.assertEqual(arguments[-1], 'detect')
        self.assertNotIn('--no-git', arguments)
        self.assertNotIn('--log-opts', arguments)
        self.assertNotIn('--baseline-path', arguments)
        self.assertNotIn('--gitleaks-ignore-path', arguments)
        self.assertEqual(arguments[arguments.index('--config') + 1],
                         str(check_gitleaks.ROOT / '.github' / '.gitleaks.toml'))
        self.assertEqual(arguments[arguments.index('--source') + 1], str(check_gitleaks.ROOT))
        self.assertIn('--redact=100', arguments)

    def test_clean_history_passes(self):
        status, _ = self.run_gate()
        self.assertEqual(status, 0)

    def test_version_mismatch_and_shallow_history_refuse_to_claim_parity(self):
        for options, calls in (({'version': '8.0.0'}, 1), ({'shallow': 'true'}, 2)):
            with self.subTest(options=options), patch('sys.stderr'):
                status, run = self.run_gate(**options)
                self.assertEqual(status, 2)
                self.assertEqual(run.call_count, calls)

    def test_missing_scanner_fails_closed(self):
        with patch.object(check_gitleaks.subprocess, 'run', side_effect=FileNotFoundError), \
                patch('sys.stderr'):
            self.assertEqual(check_gitleaks.main(), 2)
