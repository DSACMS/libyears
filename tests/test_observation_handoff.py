"""Local working batons remain separate from canonical repository history."""

import csv
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools import observation_handoff as handoffs


@unittest.skipUnless(shutil.which('git'), 'Git is required for Git-local handoffs')
class ObservationHandoffTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.repository = self.base / 'repository'
        self.repository.mkdir()
        # Test repositories must not read user configuration or run user hooks.
        environment = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
        environment.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
        self.environment = patch.dict(os.environ, environment, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.git('init', '--quiet')
        (self.repository / 'observations').mkdir()
        self.ledger = self.repository / 'observations/agent-runs.csv'
        self.ledger.write_text('canonical history\n')
        self.history = self.repository / 'history.md'
        self.history.write_text('Historical baton: /tmp/libyears-observations/007-0014.json\n')
        self.git('add', 'observations/agent-runs.csv', 'history.md')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '--quiet', '-m', 'fixture')
        with (handoffs.ROOT / 'observations' / 'agent-runs.csv').open(newline='') as handle:
            self.keys = next(csv.reader(handle, delimiter='|'))
        self.value = dict.fromkeys(self.keys)
        self.value['run_id'] = '007-0021'
        self.data = (json.dumps(self.value, indent=4) + '\r\n').encode()

    def git(self, *arguments):
        return subprocess.check_output(['git', *arguments], cwd=self.repository, text=True).strip()

    def test_directory_uses_resolved_git_dir_and_does_not_create_state(self):
        directory = handoffs.handoff_directory(self.repository)
        self.assertEqual(directory, self.repository / '.git/libyears-harness/observations')
        nested = self.repository / 'nested'
        nested.mkdir()
        self.assertEqual(handoffs.handoff_directory(nested), directory)
        self.assertFalse(directory.exists())

    def test_separate_git_dir_is_not_assumed_to_be_dot_git_directory(self):
        other = self.base / 'separate'
        other.mkdir()
        git_dir = self.base / 'metadata'
        subprocess.run(['git', 'init', '--quiet', '--separate-git-dir', str(git_dir), str(other)], check=True)
        self.assertTrue((other / '.git').is_file())
        self.assertEqual(handoffs.handoff_directory(other), git_dir / 'libyears-harness/observations')
        destination = handoffs.write_handoff(self.data, '007-0021', other)
        self.assertEqual(destination.read_bytes(), self.data)

    def test_linked_worktree_uses_its_own_git_dir(self):
        linked = self.base / 'linked'
        self.git('worktree', 'add', '--quiet', '--detach', str(linked))
        self.assertTrue((linked / '.git').is_file())
        directory = handoffs.handoff_directory(linked)
        self.assertNotEqual(directory, handoffs.handoff_directory(self.repository))
        expected = subprocess.check_output(['git', 'rev-parse', '--absolute-git-dir'], cwd=linked, text=True).strip()
        self.assertEqual(directory, Path(expected) / 'libyears-harness/observations')
        handoffs.write_handoff(self.data, '007-0021', linked)
        self.assertEqual(subprocess.check_output(['git', 'status', '--porcelain'], cwd=linked), b'')

    def test_unprotected_custom_git_dir_inside_worktree_is_refused(self):
        other = self.base / 'in-tree'
        other.mkdir()
        git_dir = other / 'metadata'
        subprocess.run(['git', 'init', '--quiet', '--separate-git-dir', str(git_dir), str(other)], check=True)
        before = subprocess.check_output(['git', 'status', '--porcelain'], cwd=other)
        with self.assertRaisesRegex(ValueError, 'not excluded'):
            handoffs.write_handoff(self.data, '007-0021', other)
        self.assertFalse((git_dir / 'libyears-harness').exists())
        self.assertEqual(subprocess.check_output(['git', 'status', '--porcelain'], cwd=other), before)

    def test_local_write_preserves_json_history_ledger_and_clean_tree(self):
        before = self.ledger.read_bytes(), self.history.read_bytes()
        destination = handoffs.write_handoff(self.data, '007-0021', self.repository)
        self.assertEqual(json.loads(destination.read_bytes()), self.value)
        self.assertEqual(self.git('status', '--porcelain'), '')
        self.assertEqual(self.git('ls-files'), 'history.md\nobservations/agent-runs.csv')
        self.assertEqual((self.ledger.read_bytes(), self.history.read_bytes()), before)

    def test_final_replacement_sees_complete_closed_sibling_temporary_file(self):
        destination = handoffs.write_handoff(self.data, '007-0021', self.repository)
        changed = dict(self.value, notes='new human-readable observation')
        updated = (json.dumps(changed, indent=2) + '\n').encode()
        real_replace = os.replace
        def inspect(source, target):
            self.assertEqual(source.parent, destination.parent)
            self.assertNotEqual(source, target)
            self.assertEqual(source.read_bytes(), updated)
            self.assertEqual(destination.read_bytes(), self.data)
            real_replace(source, target)
        with patch.object(handoffs.os, 'replace', side_effect=inspect) as replacement:
            handoffs.write_handoff(updated, '007-0021', self.repository)
        replacement.assert_called_once()
        self.assertEqual(destination.read_bytes(), updated)
        self.assertEqual(list(destination.parent.iterdir()), [destination])

    def test_interrupted_replace_preserves_existing_final_baton(self):
        destination = handoffs.write_handoff(self.data, '007-0021', self.repository)
        with patch.object(handoffs.os, 'replace', side_effect=OSError('interrupted')):
            with self.assertRaises(OSError):
                handoffs.write_handoff(self.data, '007-0021', self.repository)
        self.assertEqual(destination.read_bytes(), self.data)
        self.assertEqual(list(destination.parent.iterdir()), [destination])

    def test_migration_preserves_exact_bytes_including_whitespace(self):
        source = self.base / 'source.json'
        source.write_bytes(self.data)
        destination = handoffs.migrate_handoff(source, '007-0021', self.repository)
        self.assertEqual(source.read_bytes(), destination.read_bytes())
        self.assertEqual(destination.read_bytes(), self.data)
        self.assertEqual(handoffs.migrate_handoff(source, '007-0021', self.repository), destination)

    def test_missing_source_is_not_reconstructed(self):
        with self.assertRaises(FileNotFoundError):
            handoffs.migrate_handoff(self.base / 'missing.json', '007-0021', self.repository)
        self.assertFalse(handoffs.handoff_directory(self.repository).exists())

    def test_migration_refuses_different_existing_baton(self):
        source = self.base / 'source.json'
        source.write_bytes(self.data)
        existing = json.dumps(dict(self.value, notes='existing')).encode()
        destination = handoffs.write_handoff(existing, '007-0021', self.repository)
        with self.assertRaises(ValueError):
            handoffs.migrate_handoff(source, '007-0021', self.repository)
        self.assertEqual(destination.read_bytes(), existing)

    def test_invalid_json_keys_or_identity_never_create_a_final_baton(self):
        duplicate = self.data.replace(b'"run_id": "007-0021"',
                                      b'"run_id": "007-0014", "run_id": "007-0021"')
        for data, run_id in ((b'{', '007-0021'), (b'{}', '007-0021'),
                             (self.data, '007-0022'), (self.data, '../escape'),
                             (duplicate, '007-0021')):
            with self.subTest(run_id=run_id, data=data[:10]), self.assertRaises(ValueError):
                handoffs.write_handoff(data, run_id, self.repository)
        self.assertFalse(handoffs.handoff_directory(self.repository).exists())

    def test_cli_directory_and_prepared_file_write(self):
        source = self.base / 'prepared.json'
        source.write_bytes(self.data)
        command = [sys.executable, str(handoffs.ROOT / 'tools/observation_handoff.py')]
        directory = subprocess.check_output(command + ['directory'], cwd=self.repository, text=True).strip()
        written = subprocess.check_output(command + ['write', '007-0021', str(source)],
                                          cwd=self.repository, text=True).strip()
        destination = handoffs.handoff_directory(self.repository) / '007-0021.json'
        self.assertEqual(destination.read_bytes(), self.data)
        self.assertEqual(directory, str(destination.parent))
        self.assertEqual(written, str(destination))

    def test_bare_git_directory_is_refused(self):
        bare = self.base / 'bare'
        subprocess.run(['git', 'init', '--bare', '--quiet', str(bare)], check=True)
        with self.assertRaises(ValueError):
            handoffs.write_handoff(self.data, '007-0021', bare)
        self.assertFalse((bare / 'libyears-harness').exists())


if __name__ == '__main__':
    unittest.main()
