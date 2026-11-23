"""Synthetic byte inputs only; these tests do not assert SBOM conformance."""

import hashlib
import os
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

from libyears.maven_input import filesystem_available
from libyears.sbom_input import SbomInputReader, intake_sbom
from libyears.sbom_model import (
    SbomDiscovery, SbomFailure, SbomRequest, SbomSnapshot,
)


class SelectionTests(unittest.TestCase):
    def test_invalid_requests(self):
        for name in ('', '/bom.json', '../x', 'x/../a', 'x//a', 'https://x', 'a\\b', '~x', 'x\n'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                SbomRequest(name)
        with self.assertRaises(ValueError):
            SbomRequest('x', disabled=True)

    def test_disabled_constructs_no_reader(self):
        factory = Mock(side_effect=AssertionError('reader constructed'))
        self.assertIsNone(intake_sbom('unused', SbomRequest(disabled=True), reader_factory=factory))
        factory.assert_not_called()

    def test_portable_selection(self):
        for candidates in ((), ('a',), ('a', 'b')):
            reader = Mock()
            reader.__enter__ = Mock(return_value=reader)
            reader.__exit__ = Mock(return_value=False)
            reader.discover.return_value = (SbomDiscovery('automatic', 'complete', len(candidates), True), candidates)
            reader.snapshot.return_value = SbomSnapshot('a', b'{}', hashlib.sha256(b'{}').hexdigest())
            result = intake_sbom('unused', reader_factory=Mock(return_value=reader))
            if not candidates:
                self.assertIsNone(result)
            elif len(candidates) == 1:
                self.assertEqual(result.snapshot.data, b'{}')
            else:
                self.assertEqual(result.reason, 'sbom_selection_required')
            self.assertEqual(reader.snapshot.call_count, int(len(candidates) == 1))

    def test_capability_refusal_before_io_unskipped(self):
        with patch('os.supports_dir_fd', set()), patch('os.open') as opened, patch('os.stat') as inspected:
            result = intake_sbom('unused', SbomRequest('bom.json'))
        self.assertEqual(result.reason, 'sbom_input_unavailable')
        self.assertEqual(result.selection.source_id, 'bom.json')
        opened.assert_not_called()
        inspected.assert_not_called()


@unittest.skipUnless(filesystem_available(), 'native descriptor primitives unavailable')
class NativeInputTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        # macOS /var is an ancestor link; use the canonical temporary root here.
        self.root = Path(self.temporary.name).resolve()

    def write(self, name, data=b'{}'):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_names_exclusions_and_depth(self):
        for directory in ('node_modules', 'vendor', 'packages', 'venv', '__pycache__', 'bin', 'obj', '.hidden'):
            self.write(directory + '/bom.json')
        self.write('a/b/c/d/bom.json')
        self.write('BOM.json')
        self.assertIsNone(intake_sbom(self.root))
        self.write('target/a/b/bom.json', b'raw')
        result = intake_sbom(self.root)
        self.assertEqual(result.snapshot.data, b'raw')
        self.assertEqual(result.discovery.candidate_count, 1)
        self.write('build/result.cdx.json')
        with patch('os.read', side_effect=AssertionError('ambiguous content read')):
            result = intake_sbom(self.root)
        self.assertEqual(result.reason, 'sbom_selection_required')
        self.assertEqual(result.discovery.candidate_count, 2)

    def test_explicit_unusual_depth_and_missing(self):
        name = 'a/b/c/d/e/unusual.txt'
        self.write(name, b'not JSON yet')
        result = intake_sbom(self.root, SbomRequest(name))
        self.assertEqual(result.snapshot.data, b'not JSON yet')
        self.assertEqual(result.discovery.state, 'bypassed')
        result = intake_sbom(self.root, SbomRequest('missing'))
        self.assertEqual(result.reason, 'sbom_input_unavailable')
        self.assertEqual(result.selection.source_id, 'missing')

    def test_candidate_limit_at_and_over(self):
        for n in range(16):
            self.write(f'{n:02}.cyclonedx.json')
        result = intake_sbom(self.root)
        self.assertTrue(result.discovery.search_complete)
        self.assertEqual(result.discovery.candidate_count, 16)
        self.write('99.cdx.json')
        result = intake_sbom(self.root)
        self.assertFalse(result.discovery.search_complete)
        self.assertEqual(result.discovery.candidate_count, 17)

    def test_entry_limit_at_and_over(self):
        self.write('bom.json')
        self.write('ignored')
        with patch('libyears.sbom_input.MAX_ENTRIES', 2):
            self.assertIsNotNone(intake_sbom(self.root).snapshot)
            self.write('third')
            result = intake_sbom(self.root)
        self.assertEqual(result.reason, 'sbom_discovery_unavailable')

    def test_entry_cap_retains_already_observed_candidate_count(self):
        self.write('bom.json')
        self.write('ignored')
        original = os.scandir
        class OrderedEntries:
            def __enter__(self):
                self.iterator = original(self.descriptor)
                return iter(sorted(self.iterator, key=lambda item: item.name))
            def __exit__(self, *unused):
                self.iterator.close()
            def __init__(self, descriptor):
                self.descriptor = descriptor
        with patch('os.scandir', side_effect=OrderedEntries), patch('libyears.sbom_input.MAX_ENTRIES', 1):
            result = intake_sbom(self.root)
        self.assertEqual(result.discovery.candidate_count, 1)
        self.assertEqual(result.reason, 'sbom_discovery_unavailable')

    def test_directory_limit_at_and_over(self):
        self.write('a/bom.json')
        with patch('libyears.sbom_input.MAX_DIRECTORIES', 2):
            self.assertIsNotNone(intake_sbom(self.root).snapshot)
            (self.root / 'b').mkdir()
            self.assertEqual(intake_sbom(self.root).reason, 'sbom_discovery_unavailable')

    def test_byte_limit_and_finite_read(self):
        self.write('bom.json', b'1234')
        real_read = os.read
        with patch('libyears.sbom_input.MAX_BYTES', 4), patch('os.read', wraps=real_read) as read:
            self.assertEqual(intake_sbom(self.root).snapshot.data, b'1234')
            self.assertEqual([call.args[1] for call in read.call_args_list], [4, 1])
            self.write('bom.json', b'12345')
            self.assertEqual(intake_sbom(self.root).reason, 'sbom_budget_exceeded')

    def test_links_and_special_files(self):
        self.write('actual')
        (self.root / 'bom.json').symlink_to('actual')
        self.assertEqual(intake_sbom(self.root).reason, 'sbom_discovery_unavailable')
        self.assertEqual(intake_sbom(self.root, SbomRequest('bom.json')).reason, 'sbom_input_unsafe')
        (self.root / 'alias').symlink_to('.', target_is_directory=True)
        self.assertEqual(intake_sbom(self.root / 'alias', SbomRequest('actual')).reason, 'sbom_input_unsafe')
        self.assertEqual(intake_sbom(self.root, SbomRequest('alias/actual')).reason, 'sbom_input_unsafe')
        os.mkfifo(self.root / 'fifo')
        self.assertEqual(intake_sbom(self.root, SbomRequest('fifo')).reason, 'sbom_input_unsafe')
        (self.root / 'dir.cdx.json').mkdir()
        self.assertEqual(intake_sbom(self.root).reason, 'sbom_discovery_unavailable')

    def test_reparse_refusal(self):
        self.write('bom.json')
        original = os.stat
        def reparse(name, *args, **kwargs):
            info = original(name, *args, **kwargs)
            if name == 'bom.json':
                return types.SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400)
            return info
        with patch('os.stat', side_effect=reparse):
            self.assertEqual(intake_sbom(self.root, SbomRequest('bom.json')).reason, 'sbom_input_unsafe')

    def test_discovery_snapshot_race(self):
        self.write('bom.json')
        with SbomInputReader(self.root) as reader:
            reader.discover()
            self.write('bom.json', b'changed')
            with self.assertRaises(SbomFailure) as caught:
                reader.snapshot('bom.json')
            self.assertEqual(caught.exception.reason, 'sbom_input_changed')

    def test_read_mutation_and_descriptor_cleanup(self):
        path = self.write('bom.json')
        original = os.read
        closed = os.close
        def mutate(descriptor, count):
            data = original(descriptor, count)
            path.write_bytes(b'changed bytes')
            return data
        with patch('os.read', side_effect=mutate), patch('os.close', wraps=closed) as close:
            result = intake_sbom(self.root, SbomRequest('bom.json'))
        self.assertEqual(result.reason, 'sbom_input_changed')
        self.assertGreaterEqual(close.call_count, 2)
        for call in close.call_args_list:
            with self.assertRaises(OSError):
                os.fstat(call.args[0])

    def test_open_race_closes_descriptor(self):
        self.write('bom.json')
        opened = os.open
        closed = os.close
        def change(name, flags, **kwargs):
            descriptor = opened(name, flags, **kwargs)
            if name == 'bom.json':
                self.write('bom.json', b'racing')
            return descriptor
        with patch('os.open', side_effect=change), patch('os.close', wraps=closed) as close:
            result = intake_sbom(self.root, SbomRequest('bom.json'))
        self.assertEqual(result.reason, 'sbom_input_changed')
        for call in close.call_args_list:
            with self.assertRaises(OSError):
                os.fstat(call.args[0])
