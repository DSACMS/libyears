"""Portable source semantics and separate real anchored-reader witnesses."""

from contextlib import contextmanager
import os
from pathlib import Path
import stat
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from libyears import nuget_sources as sources
from libyears.nuget_discovery import NuGetRecognition, discovery_available
from libyears.nuget_input import LocalInput, NuGetInputFailure, ScopedNuGetReader
from tests.nuget_fixtures import SAFE_SCOPED_READ
from tests.test_nuget_scan import nuget_inputs


@contextmanager
def repository_inputs(root, projects, *, status='complete'):
    """Supply exact fixture inputs at each synthetic parent; no filesystem assumptions."""
    reads = []
    def enter(reader):
        return reader
    def read(reader, name):
        project = str(reader.root.relative_to(root) / next(
            key for key in reader.limits if key.endswith('.csproj')))
        reads.append((project, name))
        files = projects[project]
        if name not in files:
            raise NuGetInputFailure('missing')
        data = files[name]
        return LocalInput(data, data.decode('utf-8'))
    inventory = NuGetRecognition(status, tuple(sorted(projects)) if status == 'complete' else ())
    with patch.object(sources, 'discover_nuget_candidates', return_value=inventory), \
            patch.object(sources.RepositoryNuGetReader, '__enter__', enter), \
            patch.object(sources.RepositoryNuGetReader, '__exit__', return_value=None), \
            patch.object(ScopedNuGetReader, 'read', read):
        yield reads


class RepositorySourceTests(unittest.TestCase):
    def setUp(self):
        self.root = Path('synthetic').absolute()

    def test_all_projects_attempted_without_implicit_witness(self):
        projects = {'a/Witness.csproj': nuget_inputs(),
                    'b/Witness.csproj': nuget_inputs(('alpha', 'beta')),
                    'c/Bad.csproj': {'Bad.csproj': b'broken'}}
        with repository_inputs(self.root, projects) as reads:
            actual = sources.read_repository_sources(self.root)
        self.assertEqual([s.result.source_id for s in actual], sorted(projects))
        self.assertEqual([s.result.dependencies_discovered for s in actual], [1, 2, None])
        self.assertEqual([s.result.source_errors[0].reason for s in actual],
                         ['nuget_provenance_missing'] * 2 + ['invalid_nuget_project'])
        self.assertTrue(all(not s.authorized_candidates for s in actual))
        self.assertTrue(all(name != 'witness.json' for _, name in reads))
        self.assertEqual([s.result.source_errors[0].source_id for s in actual], sorted(projects))

    def test_accepted_source_and_unmatched_mapping_keep_separate_identity(self):
        projects = {'a/Witness.csproj': nuget_inputs(), 'b/Witness.csproj': nuget_inputs()}
        with repository_inputs(self.root, projects) as reads:
            actual = sources.read_repository_sources(self.root,
                [('a/Witness.csproj', 'witness.json'), ('missing/Witness.csproj', 'witness.json')])
        self.assertTrue(actual[0].result.measurement_available)
        row = actual[0].authorized_candidates[0].candidate
        self.assertEqual((row.nuget_evidence.project, row.nuget_evidence.source_id),
                         ('Witness.csproj', 'a/Witness.csproj'))
        self.assertFalse(actual[1].result.measurement_available)
        self.assertEqual(actual[2].result.source_errors[0].reason, 'nuget_witness_project_missing')
        self.assertEqual(actual[2].result.dependencies_discovered, None)
        self.assertEqual([p for p, n in reads if n == 'witness.json'], ['a/Witness.csproj'])

    def test_discovery_failure_suppresses_inventory_and_unmatched_errors(self):
        for status in ('unavailable', 'incomplete'):
            with repository_inputs(self.root, {}, status=status):
                actual, = sources.read_repository_sources(self.root, [('Absent.csproj', 'w.json')])
            self.assertIsNone(actual.result.source_id)
            self.assertIsNone(actual.result.dependencies_discovered)
            self.assertEqual(actual.result.source_errors[0].reason, 'nuget_discovery_' + status)

    def test_mapping_validation_rejects_unsafe_ambiguous_duplicate_operands(self):
        invalid = ('/A.csproj', '../A.csproj', 'a//A.csproj', './A.csproj',
                   'a/../A.csproj', 'a\\A.csproj', 'A\n.csproj', '*.csproj',
                   'A.csproj=B.csproj', 'a:C.csproj', 'A.txt')
        for project in invalid:
            with self.subTest(project=project), self.assertRaises(sources.NuGetRepositoryRequestError):
                sources.validate_witnesses([(project, 'w.json')])
        for witness in ('../w.json', 'packages.lock.json', 'w=x.json', '/w.json', 'w\n.json'):
            with self.subTest(witness=witness), self.assertRaises(sources.NuGetRepositoryRequestError):
                sources.validate_witnesses([('A.csproj', witness)])
        with self.assertRaises(sources.NuGetRepositoryRequestError):
            sources.validate_witnesses([('A.csproj', 'a.json'), ('A.csproj', 'b.json')])
        self.assertEqual(sources.validate_witnesses([('a/Test.csproj', 'w.json')]),
                         {'a/Test.csproj': 'w.json'})

    def test_each_required_capability_refuses_before_any_open(self):
        for name, value in (('supports_dir_fd', set()), ('supports_fd', set()),
                            ('supports_follow_symlinks', set()), ('O_NOFOLLOW', 0),
                            ('O_DIRECTORY', 0), ('O_NONBLOCK', 0)):
            with self.subTest(name=name), patch.object(os, name, value), \
                    patch('os.open') as opened:
                with self.assertRaises(NuGetInputFailure):
                    with sources.RepositoryNuGetReader(self.root, 'a/A.csproj', None):
                        pass
                opened.assert_not_called()


@unittest.skipUnless(discovery_available() and SAFE_SCOPED_READ, 'safe anchored filesystem unavailable')
class AnchoredReaderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'a').mkdir()
        (self.root / 'a/A.csproj').write_bytes(b'<Project/>')

    def reader(self):
        return sources.RepositoryNuGetReader(self.root, 'a/A.csproj', None)

    def test_exact_read_closes_all_descriptors(self):
        reader = self.reader()
        with reader:
            descriptors = [fd for fd, _, _ in reader.chain]
            self.assertEqual(reader.read('A.csproj').data, b'<Project/>')
        self.assertEqual(reader.chain, [])
        for descriptor in descriptors:
            with self.assertRaises(OSError):
                os.fstat(descriptor)

    def test_ancestor_symlink_and_reparse_rejected_without_reading_target(self):
        (self.root / 'link').symlink_to(self.root / 'a', target_is_directory=True)
        with self.assertRaises(NuGetInputFailure):
            with sources.RepositoryNuGetReader(self.root, 'link/A.csproj', None):
                self.fail('entered linked ancestor')
        original = os.stat
        def inspected(path, **kwargs):
            if path == 'a':
                return SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=1024)
            return original(path, **kwargs)
        with patch.object(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 1024, create=True), \
                patch('os.stat', side_effect=inspected):
            with self.assertRaises(NuGetInputFailure):
                with self.reader():
                    self.fail('entered reparse ancestor')

    def test_replacement_after_anchor_read_refuses_and_closes(self):
        reader = self.reader()
        with reader:
            descriptors = [fd for fd, _, _ in reader.chain]
            (self.root / 'a').rename(self.root / 'old')
            (self.root / 'a').symlink_to(self.root / 'old', target_is_directory=True)
            with self.assertRaises(NuGetInputFailure):
                reader.read('A.csproj')
        for descriptor in descriptors:
            with self.assertRaises(OSError):
                os.fstat(descriptor)

    def test_failure_opening_parent_closes_anchor(self):
        original = os.open
        descriptors = []
        def opened(path, flags, **kwargs):
            if path == 'a':
                raise OSError('private diagnostic')
            descriptor = original(path, flags, **kwargs)
            descriptors.append(descriptor)
            return descriptor
        with patch('os.open', side_effect=opened):
            with self.assertRaises(NuGetInputFailure):
                with self.reader():
                    self.fail('entered inaccessible parent')
        self.assertTrue(descriptors)
        for descriptor in descriptors:
            with self.assertRaises(OSError):
                os.fstat(descriptor)

    def test_actual_backslash_filename_is_an_attributed_error_and_sibling_survives(self):
        files = nuget_inputs()
        (self.root / 'a/A.csproj').write_bytes(files['Witness.csproj'])
        (self.root / 'a/packages.lock.json').write_bytes(files['packages.lock.json'])
        (self.root / 'bad\\name.csproj').write_bytes(b'<Project/>')
        actual = sources.read_repository_sources(self.root)
        self.assertEqual([item.result.source_id for item in actual], ['a/A.csproj', 'bad\\name.csproj'])
        self.assertEqual([item.result.dependencies_discovered for item in actual], [1, None])
        self.assertEqual([item.result.source_errors[0].reason for item in actual],
                         ['nuget_provenance_missing', 'invalid_nuget_project'])
