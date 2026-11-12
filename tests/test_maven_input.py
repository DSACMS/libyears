"""Native no-follow snapshot tests; all targets are test-owned temporary files."""

from dataclasses import FrozenInstanceError
from pathlib import Path
import os
import stat
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from libyears import maven_input as inputs
from libyears.maven_input import MavenInputFailure, MavenInputIssue, MavenInputReader, filesystem_available

POM = b'<project><modelVersion>4.0.0</modelVersion></project>'


@unittest.skipUnless(filesystem_available(), 'native descriptor primitives unavailable')
class MavenSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve())
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write(self, name, data=POM):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def assert_issue(self, issue, function, *args):
        with self.assertRaises(MavenInputFailure) as caught:
            function(*args)
        self.assertEqual(caught.exception.issue, issue)
        self.assertNotIn(str(self.root), str(caught.exception))

    def test_exact_bom_crlf_bytes_and_separate_immutable_xml(self):
        data = (b'\xef\xbb\xbf<?xml version="1.0" encoding="UTF-8"?>\r\n'
                b'<project><modelVersion>4.0.0</modelVersion>\r\n<name>A&amp;B</name></project>')
        path = self.write('pom.xml', data)
        before = path.stat()
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            snapshot = reader.snapshot_pom('pom.xml')
            self.assertEqual(snapshot.source_id, 'pom.xml')
            self.assertEqual(snapshot.data, data)
            self.assertEqual(snapshot.xml.scalar('name'), 'A&B')
            self.assertEqual(reader.snapshot_pom('pom.xml'), snapshot)
            with self.assertRaises(FrozenInstanceError):
                snapshot.data = b'changed'
        after = path.stat()
        self.assertEqual(path.read_bytes(), data)
        self.assertEqual((before.st_mode, before.st_mtime_ns, before.st_ctime_ns),
                         (after.st_mode, after.st_mtime_ns, after.st_ctime_ns))
        self.assertEqual({p.name for p in self.root.iterdir()}, {'pom.xml'})

    def test_uninventoried_and_unsafe_paths_refuse_before_any_io(self):
        self.write('pom.xml')
        with MavenInputReader(self.root) as reader:
            for name in ('pom.xml', '../pom.xml', '/pom.xml', 'a//pom.xml', 'a/./pom.xml',
                         'a\\pom.xml', 'C:/pom.xml', '$HOME/pom.xml', 'x\x00/pom.xml'):
                with self.subTest(name=name), patch.object(os, 'stat', side_effect=AssertionError('stat')), \
                        patch.object(os, 'open', side_effect=AssertionError('open')), \
                        patch.object(os, 'read', side_effect=AssertionError('read')):
                    with self.assertRaises(MavenInputFailure):
                        reader.snapshot_pom(name)
            reader.inventory()
            with patch.object(os, 'stat', side_effect=AssertionError('stat')):
                self.assert_issue(MavenInputIssue.UNSELECTED, reader.snapshot_pom, 'unknown/pom.xml')

    def test_safe_relative_path_length_and_component_bounds(self):
        self.assertEqual(len(inputs.relative_parts('a/' * 31 + 'pom.xml')), 32)
        self.assertEqual(inputs.relative_parts('x' * 1024), ('x' * 1024,))
        for name in ('a/' * 32 + 'pom.xml', 'x' * 1025):
            with self.subTest(name=name), self.assertRaises(MavenInputFailure):
                inputs.relative_parts(name)

    def test_inventory_is_single_even_when_empty(self):
        with MavenInputReader(self.root) as reader:
            self.assertTrue(reader.inventory().discovery.complete)
            with self.assertRaises(RuntimeError):
                reader.inventory()

    def test_reader_is_single_use_and_descriptors_close_on_exit(self):
        self.write('pom.xml')
        reader = MavenInputReader(self.root)
        original = os.open
        descriptors = []
        def observe(*args, **kwargs):
            descriptor = original(*args, **kwargs)
            descriptors.append(descriptor)
            return descriptor
        with patch.object(os, 'open', side_effect=observe):
            with reader:
                reader.inventory()
                reader.snapshot_pom('pom.xml')
        for descriptor in set(descriptors):
            with self.assertRaises(OSError):
                os.fstat(descriptor)
        with self.assertRaises(RuntimeError):
            reader.__enter__()

    def test_failed_anchor_inspection_closes_descriptor(self):
        original = os.open
        opened = []
        def observe(*args, **kwargs):
            descriptor = original(*args, **kwargs)
            opened.append(descriptor)
            return descriptor
        with patch.object(os, 'open', side_effect=observe), \
                patch.object(os, 'fstat', side_effect=OSError('unavailable')):
            with self.assertRaises(MavenInputFailure):
                with MavenInputReader(self.root):
                    self.fail('root unexpectedly accepted')
        self.assertEqual(len(opened), 1)
        with self.assertRaises(OSError):
            os.fstat(opened[0])

    def test_cached_bytes_are_not_reread_or_double_charged(self):
        self.write('pom.xml')
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            first = reader.snapshot_pom('pom.xml')
            charged = reader._xml_bytes
            with patch.object(os, 'read', side_effect=AssertionError('reread')):
                self.assertIs(reader.snapshot_pom('pom.xml'), first)
            self.assertEqual(reader._xml_bytes, charged)

    def test_cached_snapshot_refuses_later_file_changes(self):
        path = self.write('pom.xml')
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            reader.snapshot_pom('pom.xml')
            path.write_bytes(POM + b' ')
            with patch.object(os, 'read', side_effect=AssertionError('changed file read')):
                self.assert_issue(MavenInputIssue.CHANGED, reader.snapshot_pom, 'pom.xml')

    def test_inventory_identity_change_refuses_before_file_open(self):
        path = self.write('pom.xml')
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            path.write_bytes(POM + b' ')
            with patch.object(os, 'open', side_effect=AssertionError('changed file open')):
                self.assert_issue(MavenInputIssue.CHANGED, reader.snapshot_pom, 'pom.xml')

    def test_symlink_and_fifo_replacement_refuse_before_open_or_read(self):
        path = self.write('pom.xml')
        self.write('other.xml')
        for kind in ('symlink', 'fifo'):
            if kind == 'fifo' and not hasattr(os, 'mkfifo'):
                continue
            path.unlink(missing_ok=True)
            path.write_bytes(POM)
            with MavenInputReader(self.root) as reader:
                reader.inventory()
                path.unlink()
                if kind == 'symlink':
                    path.symlink_to(self.root / 'other.xml')
                else:
                    os.mkfifo(path)
                with self.subTest(kind=kind), patch.object(os, 'open', side_effect=AssertionError('unsafe open')), \
                        patch.object(os, 'read', side_effect=AssertionError('unsafe read')):
                    self.assert_issue(MavenInputIssue.UNSAFE, reader.snapshot_pom, 'pom.xml')
        path.unlink(missing_ok=True)

    def test_open_race_to_symlink_fails_without_content_read(self):
        path = self.write('pom.xml')
        other = self.write('other.xml', b'not selected')
        original = os.open
        def replace(name, flags, **kwargs):
            if name == 'pom.xml':
                path.unlink()
                path.symlink_to(other)
            return original(name, flags, **kwargs)
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            with patch.object(os, 'open', side_effect=replace), \
                    patch.object(os, 'read', side_effect=AssertionError('followed symlink')):
                self.assert_issue(MavenInputIssue.IO, reader.snapshot_pom, 'pom.xml')
        self.assertEqual(other.read_bytes(), b'not selected')

    def test_opened_reparse_file_refuses_before_read(self):
        self.write('pom.xml')
        original = os.fstat
        def changed(descriptor):
            info = original(descriptor)
            if stat.S_ISREG(info.st_mode):
                values = {key: getattr(info, key) for key in (
                    'st_dev', 'st_ino', 'st_mode', 'st_size', 'st_mtime_ns', 'st_ctime_ns')}
                return SimpleNamespace(**values, st_file_attributes=0x400)
            return info
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            with patch.object(os, 'fstat', side_effect=changed), \
                    patch.object(os, 'read', side_effect=AssertionError('unsafe read')):
                self.assert_issue(MavenInputIssue.CHANGED, reader.snapshot_pom, 'pom.xml')

    def test_read_race_cannot_admit_changed_bytes(self):
        path = self.write('pom.xml')
        original = os.read
        def change(descriptor, count):
            data = original(descriptor, count)
            path.write_bytes(POM + b' ')
            return data
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            with patch.object(os, 'read', side_effect=change):
                self.assert_issue(MavenInputIssue.CHANGED, reader.snapshot_pom, 'pom.xml')

    def test_change_during_parse_refuses_before_admission(self):
        path = self.write('pom.xml')
        original = inputs.parse_pom
        def change(data):
            node = original(data)
            path.write_bytes(POM + b' ')
            return node
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            with patch.object(inputs, 'parse_pom', side_effect=change):
                self.assert_issue(MavenInputIssue.CHANGED, reader.snapshot_pom, 'pom.xml')

    def test_replaced_parent_directory_refuses_before_child_open_even_with_same_file(self):
        path = self.write('module/pom.xml')
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            path.parent.rename(self.root / 'old-module')
            path.parent.mkdir()
            os.link(self.root / 'old-module/pom.xml', path)
            with patch.object(os, 'open', side_effect=AssertionError('changed directory open')):
                self.assert_issue(MavenInputIssue.CHANGED, reader.snapshot_pom, 'module/pom.xml')

    def test_replaced_root_refuses_before_any_candidate_open(self):
        self.write('selected/pom.xml')
        selected = self.root / 'selected'
        with MavenInputReader(selected) as reader:
            reader.inventory()
            selected.rename(self.root / 'old-selected')
            selected.symlink_to(self.root / 'old-selected', target_is_directory=True)
            with patch.object(os, 'open', side_effect=AssertionError('changed root open')), \
                    patch.object(os, 'read', side_effect=AssertionError('read')):
                self.assert_issue(MavenInputIssue.CHANGED, reader.snapshot_pom, 'pom.xml')

    def test_oversized_file_refuses_before_file_open(self):
        self.write('pom.xml', b'x' * (inputs.MAX_XML_BYTES + 1))
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            with patch.object(os, 'open', side_effect=AssertionError('oversized open')):
                self.assert_issue(MavenInputIssue.LIMIT, reader.snapshot_pom, 'pom.xml')

    def test_total_xml_budget_counts_distinct_snapshots_once(self):
        self.assertEqual(inputs.MAX_TOTAL_XML_BYTES, 32 * 1024 * 1024)
        for name in ('a/pom.xml', 'b/pom.xml', 'c/pom.xml'):
            self.write(name)
        with MavenInputReader(self.root) as reader, patch.object(inputs, 'MAX_TOTAL_XML_BYTES', 2 * len(POM)):
            reader.inventory()
            first = reader.snapshot_pom('a/pom.xml')
            self.assertIs(reader.snapshot_pom('a/pom.xml'), first)
            reader.snapshot_pom('b/pom.xml')
            original = os.open
            def reject_file(name, *args, **kwargs):
                if name == 'pom.xml':
                    raise AssertionError('over-budget file opened')
                return original(name, *args, **kwargs)
            with patch.object(os, 'open', side_effect=reject_file):
                self.assert_issue(MavenInputIssue.LIMIT, reader.snapshot_pom, 'c/pom.xml')

    def test_failed_xml_cannot_be_repaired_mid_snapshot(self):
        path = self.write('pom.xml', b'<project>')
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            self.assert_issue(MavenInputIssue.XML_MALFORMED, reader.snapshot_pom, 'pom.xml')
            path.write_bytes(POM)
            with patch.object(os, 'open', side_effect=AssertionError('reopened failed input')):
                self.assert_issue(MavenInputIssue.XML_MALFORMED, reader.snapshot_pom, 'pom.xml')

    def test_control_reads_are_exact_contained_and_settings_presence_only(self):
        self.write('module/pom.xml')
        self.write('.mvn/maven.config', b'-B\n')
        self.write('module/.mvn/extensions.xml', b'<extensions/>')
        self.write('.mvn/settings.xml', b'NEVER_READ')
        self.write('settings.xml', b'ALSO_NOT_SELECTED')
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            self.assertEqual(reader.snapshot_control('.mvn/maven.config').data, b'-B\n')
            self.assertEqual(reader.snapshot_control('module/.mvn/extensions.xml').xml.name, 'extensions')
            self.assertFalse(reader.control_present('.mvn/jvm.config'))
            self.assertTrue(reader.control_present('.mvn/settings.xml'))
            for name in ('.mvn/settings.xml', 'settings.xml', '../settings.xml', '.mvn/other.xml',
                         'unrelated/.mvn/maven.config'):
                with self.subTest(name=name), patch.object(os, 'stat', side_effect=AssertionError('stat')), \
                        patch.object(os, 'open', side_effect=AssertionError('unselected open')):
                    with self.assertRaises(MavenInputFailure):
                        reader.snapshot_control(name)

    def test_control_symlink_directory_is_refused_without_following(self):
        self.write('pom.xml')
        self.write('actual/maven.config', b'-B')
        (self.root / '.mvn').symlink_to(self.root / 'actual', target_is_directory=True)
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            with patch.object(os, 'open', side_effect=AssertionError('linked control open')):
                self.assert_issue(MavenInputIssue.UNSAFE, reader.snapshot_control, '.mvn/maven.config')

    def test_configuration_byte_limit_before_file_open(self):
        self.write('pom.xml')
        self.write('.mvn/maven.config', b'x' * (inputs.MAX_CONFIG_BYTES + 1))
        with MavenInputReader(self.root) as reader:
            reader.inventory()
            original = os.open
            def reject_file(name, *args, **kwargs):
                if name == 'maven.config':
                    raise AssertionError('oversized config opened')
                return original(name, *args, **kwargs)
            with patch.object(os, 'open', side_effect=reject_file):
                self.assert_issue(MavenInputIssue.LIMIT, reader.snapshot_control, '.mvn/maven.config')
