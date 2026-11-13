"""Real filename traversal and portable fail-closed capability witnesses."""

from contextlib import ExitStack
import os
from pathlib import Path
import stat
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from libyears import nuget_discovery as discovery
from libyears.nuget_discovery import NuGetRecognition, discover_nuget_candidates


class DiscoveryCapabilityTests(unittest.TestCase):
    def test_each_missing_primitive_refuses_without_open_or_scan(self):
        for target, value in (
            ('supports_dir_fd', set()), ('supports_fd', set()),
            ('supports_follow_symlinks', set()),
            ('O_DIRECTORY', 0), ('O_NOFOLLOW', 0), ('O_NONBLOCK', 0),
        ):
            with self.subTest(target=target), patch.object(os, target, value, create=True), \
                    patch.object(os, 'open') as opened, patch.object(os, 'scandir') as scanned:
                self.assertEqual(discover_nuget_candidates('unused'), NuGetRecognition('unavailable'))
                opened.assert_not_called()
                scanned.assert_not_called()

    def test_reparse_metadata_is_recognized_without_platform_dependency(self):
        with patch.object(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 1024, create=True):
            self.assertTrue(discovery._reparse_point(SimpleNamespace(st_file_attributes=1024)))
            self.assertFalse(discovery._reparse_point(SimpleNamespace(st_file_attributes=0)))


@unittest.skipUnless(discovery.discovery_available(), 'requires safe directory enumeration')
class DiscoveryFilesystemTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def candidate(self, relative, content='malformed project text'):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def test_zero_one_many_sorted_without_content_reads_or_execution(self):
        self.assertEqual(discover_nuget_candidates(self.root), NuGetRecognition())
        first = self.candidate('z/Z.csproj')
        first.chmod(0)
        self.addCleanup(first.chmod, 0o600)
        self.assertEqual(discover_nuget_candidates(self.root).candidates, ('z/Z.csproj',))
        self.candidate('A.csproj', '<Project Sdk="unsupported"/>')
        self.candidate('ignored.CSPROJ')
        self.candidate('ignored.vbproj')
        with ExitStack() as stack:
            guards = [stack.enter_context(patch(target)) for target in (
                'builtins.open', 'pathlib.Path.open', 'subprocess.Popen',
                'subprocess.run', 'socket.socket', 'urllib.request.urlopen',
            )]
            result = discover_nuget_candidates(self.root)
            self.assertEqual(result, NuGetRecognition(candidates=('A.csproj', 'z/Z.csproj')))
            for guard in guards:
                guard.assert_not_called()

    def test_exact_depth_and_exclusions(self):
        self.candidate('a/b/c/d/Deep.csproj')
        for name in (*discovery.EXCLUDED_DIRECTORIES, '.git', '.hidden'):
            self.candidate(f'{name}/Ignored.csproj')
            self.candidate(f'a/b/c/d/{name}/Ignored.csproj')
        self.assertEqual(discover_nuget_candidates(self.root).candidates, ('a/b/c/d/Deep.csproj',))
        self.candidate('a/b/c/d/e/Pruned.csproj')
        with patch.object(os, 'open', wraps=os.open) as opened, \
                patch.object(os, 'scandir', wraps=os.scandir) as scanned:
            self.assertEqual(discover_nuget_candidates(self.root).candidates, ('a/b/c/d/Deep.csproj',))
            self.assertEqual([call.args[0] for call in opened.call_args_list],
                             [self.root, 'a', 'b', 'c', 'd'])
            self.assertEqual(scanned.call_count, 5)

    def test_candidate_cap_and_cap_plus_one(self):
        for index in range(discovery.MAX_CANDIDATES):
            self.candidate(f'{index:03}.csproj')
        result = discover_nuget_candidates(self.root)
        self.assertEqual((result.status, len(result.candidates)), ('complete', 100))
        self.candidate('overflow.csproj')
        self.assertEqual(discover_nuget_candidates(self.root), NuGetRecognition('incomplete', positive_local_evidence=True))

    def test_directory_cap_and_cap_plus_one(self):
        for index in range(discovery.MAX_DIRECTORIES - 1):
            (self.root / f'd{index:03}').mkdir()
        self.assertEqual(discover_nuget_candidates(self.root), NuGetRecognition())
        (self.root / 'overflow').mkdir()
        self.assertEqual(discover_nuget_candidates(self.root), NuGetRecognition('incomplete'))

    def test_entry_cap_and_cap_plus_one_includes_skipped_entries(self):
        for index in range(discovery.MAX_ENTRIES):
            (self.root / f'f{index:05}').touch()
        self.assertEqual(discover_nuget_candidates(self.root), NuGetRecognition())
        (self.root / '.ignored').mkdir()
        self.assertEqual(discover_nuget_candidates(self.root), NuGetRecognition('incomplete'))

    def test_budgets_are_global_across_directories(self):
        self.candidate('a/One.csproj')
        self.candidate('b/Two.csproj')
        with patch.object(discovery, 'MAX_CANDIDATES', 1):
            self.assertEqual(discover_nuget_candidates(self.root), NuGetRecognition('incomplete', positive_local_evidence=True))
        # Root has two entries; each child adds another, so a per-directory cap
        # would miss this overflow.
        with patch.object(discovery, 'MAX_ENTRIES', 3):
            self.assertEqual(discover_nuget_candidates(self.root), NuGetRecognition('incomplete', positive_local_evidence=True))

    def test_symlinks_and_special_files_are_not_candidates_or_followed(self):
        self.candidate('real/Actual.csproj')
        (self.root / 'file.csproj').symlink_to('real/Actual.csproj')
        (self.root / 'loop').symlink_to('.', target_is_directory=True)
        # Escaping links point to a fixture outside the scanned root, never read.
        with tempfile.TemporaryDirectory() as outside:
            (Path(outside) / 'Outside.csproj').touch()
            (self.root / 'escape').symlink_to(outside, target_is_directory=True)
            if hasattr(os, 'mkfifo'):
                os.mkfifo(self.root / 'pipe.csproj')
            self.assertEqual(discover_nuget_candidates(self.root).candidates, ('real/Actual.csproj',))
        self.assertEqual(discover_nuget_candidates(self.root / 'loop'), NuGetRecognition('incomplete'))

    def test_reparse_directories_and_files_are_omitted(self):
        self.candidate('skip/Hidden.csproj')
        self.candidate('Hidden.csproj')
        with patch.object(discovery, '_reparse_point', return_value=True), \
                patch.object(os, 'open', wraps=os.open) as opened:
            self.assertEqual(discover_nuget_candidates(self.root), NuGetRecognition())
            self.assertEqual(opened.call_count, 1)

    def test_open_and_enumeration_failures_close_all_handles_and_hide_details(self):
        self.candidate('child/Found.csproj')
        original_open = os.open
        descriptors = []

        def record_open(*args, **kwargs):
            descriptor = original_open(*args, **kwargs)
            descriptors.append(descriptor)
            return descriptor

        for error in (OSError('private diagnostic'), NotImplementedError('private diagnostic'),
                      ValueError('private diagnostic')):
            with self.subTest(error=type(error).__name__), \
                    patch.object(os, 'open', side_effect=record_open), \
                    patch.object(os, 'scandir', side_effect=error):
                self.assertEqual(discover_nuget_candidates(self.root), NuGetRecognition('incomplete'))
            for descriptor in descriptors:
                with self.assertRaises(OSError):
                    os.fstat(descriptor)

    def test_replaced_child_is_rejected_before_descent_and_closed(self):
        (self.root / 'child').mkdir()
        original_open = os.open
        original_scandir = os.scandir
        descriptors = []

        def replace_open(path, flags, **kwargs):
            if path == 'child':
                (self.root / 'child').rename(self.root / 'old')
                (self.root / 'child').mkdir()
            descriptor = original_open(path, flags, **kwargs)
            descriptors.append(descriptor)
            return descriptor

        with patch.object(os, 'open', side_effect=replace_open), \
                patch.object(os, 'scandir', wraps=original_scandir) as scanned:
            self.assertEqual(discover_nuget_candidates(self.root), NuGetRecognition('incomplete'))
            self.assertEqual(scanned.call_count, 1)
        for descriptor in descriptors:
            with self.assertRaises(OSError):
                os.fstat(descriptor)

    def test_mutation_during_walk_invalidates_population(self):
        self.candidate('child/Found.csproj')
        original_stat = os.stat

        def mutate_stat(path, **kwargs):
            if path == 'child':
                (self.root / 'new.txt').touch()
            return original_stat(path, **kwargs)

        with patch.object(os, 'stat', side_effect=mutate_stat):
            self.assertEqual(discover_nuget_candidates(self.root),
                             NuGetRecognition('incomplete', positive_local_evidence=True))

    def test_success_closes_directory_handles_and_scan_iterators(self):
        self.candidate('child/Found.csproj')
        original_open, original_scandir = os.open, os.scandir
        descriptors, iterators = [], []

        def record_open(*args, **kwargs):
            descriptor = original_open(*args, **kwargs)
            descriptors.append(descriptor)
            return descriptor

        def record_scan(descriptor):
            iterator = original_scandir(descriptor)
            iterators.append(iterator)
            return iterator

        with patch.object(os, 'open', side_effect=record_open), \
                patch.object(os, 'scandir', side_effect=record_scan):
            self.assertEqual(discover_nuget_candidates(self.root).candidates, ('child/Found.csproj',))
        self.assertEqual(len(descriptors), 2)
        for descriptor in descriptors:
            with self.assertRaises(OSError):
                os.fstat(descriptor)
        for iterator in iterators:
            self.assertEqual(list(iterator), [])
