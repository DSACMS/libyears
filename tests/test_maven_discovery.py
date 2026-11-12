"""Read-only native inventory and portable capability-refusal witnesses."""

from pathlib import Path
import os
import stat
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from libyears import maven_discovery as discovery
from libyears import maven_input as inputs
from libyears.maven_input import MavenInputIssue, MavenInputReader, filesystem_available

POM = b'<project><modelVersion>4.0.0</modelVersion></project>'


class MavenCapabilityTests(unittest.TestCase):
    def test_absent_flags_refuse_before_stat_open_scandir_or_read(self):
        for flag in ('O_DIRECTORY', 'O_NOFOLLOW', 'O_NONBLOCK'):
            with self.subTest(flag=flag), patch.object(os, flag, 0, create=True), \
                    patch.object(os, 'stat', side_effect=AssertionError('unsafe stat')), \
                    patch.object(os, 'open', side_effect=AssertionError('unsafe open')), \
                    patch.object(os, 'scandir', side_effect=AssertionError('unsafe enumeration')), \
                    patch.object(os, 'read', side_effect=AssertionError('unsafe read')):
                result = discovery.discover_maven_candidates('unopened')
                self.assertFalse(result.discovery.complete)
                self.assertEqual(result.discovery.source_ids, ())
                self.assertEqual(result.issue, MavenInputIssue.CAPABILITY)

    def test_absent_descriptor_support_refuses_before_io(self):
        with patch.object(os, 'supports_dir_fd', set()), \
                patch.object(os, 'stat', side_effect=AssertionError('stat')), \
                patch.object(os, 'open', side_effect=AssertionError('open')):
            result = discovery.discover_maven_candidates('unopened')
            self.assertEqual(result.issue, MavenInputIssue.CAPABILITY)

    def test_missing_stat_reparse_constant_does_not_break_refusal_setup(self):
        portable_stat = SimpleNamespace(S_ISREG=stat.S_ISREG, S_ISDIR=stat.S_ISDIR)
        with patch.object(inputs, 'stat', portable_stat):
            self.assertTrue(inputs.reparse_point(SimpleNamespace(st_file_attributes=0x400)))
            self.assertFalse(inputs.reparse_point(SimpleNamespace()))
        with patch.object(os, 'O_NOFOLLOW', 0, create=True), \
                patch.object(inputs, 'stat', portable_stat), \
                patch.object(os, 'stat', side_effect=AssertionError('stat')), \
                patch.object(os, 'open', side_effect=AssertionError('open')):
            self.assertEqual(discovery.discover_maven_candidates('unopened').issue,
                             MavenInputIssue.CAPABILITY)


@unittest.skipUnless(filesystem_available(), 'native descriptor primitives unavailable')
class MavenDiscoveryTests(unittest.TestCase):
    def setUp(self):
        base = Path(tempfile.gettempdir()).resolve()
        self.temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def pom(self, name):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(POM)

    def test_exact_root_and_nested_names_order_without_parsing_or_writes(self):
        for name in ('pom.xml', 'b/pom.xml', 'a/pom.xml', 'a/deep/pom.xml'):
            self.pom(name)
        (self.root / 'POM.xml').write_bytes(b'not a candidate')
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with patch.object(os, 'read', side_effect=AssertionError('inventory read contents')):
            result = discovery.discover_maven_candidates(self.root)
        self.assertTrue(result.discovery.complete)
        self.assertEqual(result.discovery.source_ids,
                         ('a/deep/pom.xml', 'a/pom.xml', 'b/pom.xml', 'pom.xml'))
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_absence_is_complete_but_direct_file_does_not_activate_maven(self):
        empty = discovery.discover_maven_candidates(self.root)
        self.assertTrue(empty.discovery.complete)
        self.assertEqual(empty.discovery.source_ids, ())
        self.pom('pom.xml')
        direct = discovery.discover_maven_candidates(self.root / 'pom.xml')
        self.assertTrue(direct.discovery.complete)
        self.assertEqual(direct.discovery.source_ids, ())

    def test_depth_four_is_included_and_depth_five_is_not_followed(self):
        self.pom('a/b/c/d/pom.xml')
        self.pom('a/b/c/d/e/pom.xml')
        original = os.open
        opened = []
        def observe(name, *args, **kwargs):
            opened.append(name)
            return original(name, *args, **kwargs)
        with patch.object(os, 'open', side_effect=observe):
            result = discovery.discover_maven_candidates(self.root)
        self.assertTrue(result.discovery.complete)
        self.assertEqual(result.discovery.source_ids, ('a/b/c/d/pom.xml',))
        self.assertNotIn('e', opened)

    def test_hidden_and_generated_directories_are_excluded_without_enumeration(self):
        for name in discovery.EXCLUDED_DIRECTORIES | {'.git', '.mvn'}:
            self.pom(name + '/pom.xml')
        self.pom('normal/pom.xml')
        result = discovery.discover_maven_candidates(self.root)
        self.assertTrue(result.discovery.complete)
        self.assertEqual(result.discovery.source_ids, ('normal/pom.xml',))

    def test_directory_budget_exactly_256_and_refuses_next_before_open(self):
        self.pom('a/pom.xml')
        for index in range(254):
            (self.root / f'd{index:03}').mkdir()
        exact = discovery.discover_maven_candidates(self.root)
        self.assertTrue(exact.discovery.complete)
        (self.root / 'overflow').mkdir()
        original = os.open
        opened = []
        def observe(name, *args, **kwargs):
            opened.append(name)
            return original(name, *args, **kwargs)
        with patch.object(os, 'open', side_effect=observe):
            result = discovery.discover_maven_candidates(self.root)
        self.assertFalse(result.discovery.complete)
        self.assertEqual(result.issue, MavenInputIssue.LIMIT)
        self.assertEqual(result.discovery.source_ids, ('a/pom.xml',))
        self.assertNotIn('overflow', opened)

    def test_exact_pom_budget_then_deterministic_safe_prefix(self):
        for index in range(100):
            self.pom(f'm{index:03}/pom.xml')
        self.assertTrue(discovery.discover_maven_candidates(self.root).discovery.complete)
        self.pom('m100/pom.xml')
        first = discovery.discover_maven_candidates(self.root)
        second = discovery.discover_maven_candidates(self.root)
        self.assertFalse(first.discovery.complete)
        self.assertEqual(first.issue, MavenInputIssue.LIMIT)
        self.assertEqual(len(first.discovery.source_ids), 100)
        self.assertEqual(first.discovery.source_ids, second.discovery.source_ids)
        self.assertNotIn('m100/pom.xml', first.discovery.source_ids)

    def test_entry_budget_counts_excluded_names_before_any_candidate_contents(self):
        self.pom('pom.xml')
        original = os.scandir
        class Entries:
            def __init__(self, count):
                self.entries = [SimpleNamespace(name='pom.xml')]
                self.entries.extend(SimpleNamespace(name=f'.ignored{i}') for i in range(count - 1))
            def __enter__(self):
                return iter(self.entries)
            def __exit__(self, *unused):
                pass
        with patch.object(os, 'scandir', return_value=Entries(10_000)):
            exact = discovery.discover_maven_candidates(self.root)
        self.assertTrue(exact.discovery.complete)
        self.assertEqual(exact.discovery.source_ids, ('pom.xml',))
        with patch.object(os, 'scandir', return_value=Entries(10_001)):
            overflow = discovery.discover_maven_candidates(self.root)
        self.assertFalse(overflow.discovery.complete)
        self.assertEqual(overflow.issue, MavenInputIssue.LIMIT)
        self.assertEqual(overflow.discovery.source_ids, ())

    def test_refused_pom_shapes_also_consume_candidate_budget(self):
        for index in range(100):
            folder = self.root / f'm{index:03}'
            folder.mkdir()
            (folder / 'pom.xml').symlink_to('missing-never-followed')
        self.pom('z/pom.xml')
        result = discovery.discover_maven_candidates(self.root)
        self.assertFalse(result.discovery.complete)
        self.assertEqual(result.issue, MavenInputIssue.LIMIT)
        self.assertEqual(len(result.candidates), 100)
        self.assertEqual(result.discovery.source_ids, ())

    def test_unreadable_pom_metadata_cannot_bypass_candidate_budget(self):
        self.pom('a/pom.xml')
        for index in range(101):
            self.pom(f'm{index:03}/pom.xml')
        self.pom('z/pom.xml')
        original = os.stat
        safe_inode = (self.root / 'a').stat().st_ino
        last_inode = (self.root / 'z').stat().st_ino
        refused = []
        last_probed = []
        def unreadable(name, *args, **kwargs):
            if name == 'pom.xml':
                directory = os.fstat(kwargs['dir_fd']).st_ino
                if directory == last_inode:
                    last_probed.append(name)
                elif directory != safe_inode:
                    refused.append(name)
                    raise PermissionError('unreadable POM metadata')
            return original(name, *args, **kwargs)
        with patch.object(os, 'stat', side_effect=unreadable):
            result = discovery.discover_maven_candidates(self.root)
        self.assertFalse(result.discovery.complete)
        self.assertEqual(result.issue, MavenInputIssue.LIMIT)
        self.assertEqual(result.discovery.source_ids, ('a/pom.xml',))
        self.assertEqual(len(result.candidates), 100)
        self.assertEqual(len(refused), 99)
        self.assertFalse(last_probed)
        self.assertTrue(all(item.issue == MavenInputIssue.IO for item in result.candidates[1:]))

    def test_read_failure_preserves_safe_preceding_sibling(self):
        self.pom('a/pom.xml')
        (self.root / 'b').mkdir()
        original = os.scandir
        def unreadable(descriptor):
            if os.fstat(descriptor).st_ino == (self.root / 'b').stat().st_ino:
                raise PermissionError('private diagnostic must not escape')
            return original(descriptor)
        with patch.object(os, 'scandir', side_effect=unreadable):
            result = discovery.discover_maven_candidates(self.root)
        self.assertFalse(result.discovery.complete)
        self.assertEqual(result.discovery.source_ids, ('a/pom.xml',))
        self.assertNotIn('private diagnostic', repr(result))

    def test_symlink_pom_refused_and_linked_directory_not_followed(self):
        self.pom('actual/pom.xml')
        (self.root / 'pom.xml').symlink_to(self.root / 'actual/pom.xml')
        (self.root / 'linked').symlink_to(self.root / 'actual', target_is_directory=True)
        original = os.open
        opened = []
        def observe(name, *args, **kwargs):
            opened.append(name)
            return original(name, *args, **kwargs)
        with patch.object(os, 'open', side_effect=observe):
            result = discovery.discover_maven_candidates(self.root)
        self.assertFalse(result.discovery.complete)
        self.assertEqual(result.discovery.source_ids, ('actual/pom.xml',))
        self.assertEqual(result.candidates[-1].issue, MavenInputIssue.UNSAFE)
        self.assertNotIn('linked', opened)
        self.assertNotIn('pom.xml', opened)

    def test_ancestor_symlink_root_refused_before_opening_link(self):
        self.pom('actual/nested/pom.xml')
        (self.root / 'alias').symlink_to(self.root / 'actual', target_is_directory=True)
        original = os.open
        opened = []
        def observe(name, *args, **kwargs):
            opened.append(name)
            return original(name, *args, **kwargs)
        with patch.object(os, 'open', side_effect=observe):
            result = discovery.discover_maven_candidates(self.root / 'alias/nested')
        self.assertFalse(result.discovery.complete)
        self.assertEqual(result.issue, MavenInputIssue.UNSAFE)
        self.assertNotIn('alias', opened)

    def test_simulated_reparse_candidate_refuses_without_platform_stat_constant(self):
        self.pom('pom.xml')
        original = os.stat
        def reparse(name, *args, **kwargs):
            info = original(name, *args, **kwargs)
            if name == 'pom.xml':
                values = {key: getattr(info, key) for key in (
                    'st_dev', 'st_ino', 'st_mode', 'st_size', 'st_mtime_ns', 'st_ctime_ns')}
                return SimpleNamespace(**values, st_file_attributes=0x400)
            return info
        portable_stat = SimpleNamespace(S_ISREG=stat.S_ISREG, S_ISDIR=stat.S_ISDIR)
        with patch.object(os, 'stat', side_effect=reparse), patch.object(inputs, 'stat', portable_stat):
            result = discovery.discover_maven_candidates(self.root)
        self.assertFalse(result.discovery.complete)
        self.assertEqual(result.candidates[0].issue, MavenInputIssue.UNSAFE)

    def test_root_change_during_enumeration_is_incomplete(self):
        self.pom('pom.xml')
        original = os.scandir
        root = self.root
        class ChangingEntries:
            def __enter__(self):
                self.iterator = original(root)
                return self.iterator
            def __exit__(self, *unused):
                self.iterator.close()
                (root / 'new-file').write_bytes(b'changed')
        with patch.object(os, 'scandir', return_value=ChangingEntries()):
            result = discovery.discover_maven_candidates(root)
        self.assertFalse(result.discovery.complete)
        self.assertEqual(result.issue, MavenInputIssue.CHANGED)

    def test_unsafe_root_spelling_is_not_normalized(self):
        with patch.object(os, 'open', side_effect=AssertionError('open')), \
                patch.object(os, 'stat', side_effect=AssertionError('stat')):
            result = discovery.discover_maven_candidates(str(self.root) + '/../elsewhere')
        self.assertFalse(result.discovery.complete)
        self.assertEqual(result.issue, MavenInputIssue.PATH)
