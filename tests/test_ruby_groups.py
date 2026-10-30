"""Scoped Ruby filesystem witnesses; source composition is added by T004."""

import errno
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from libyears import rubygems
from libyears.gemfile import GemfileParseFailure, ParsedGemfile, parse_gemfile
from libyears.rubygems import _ScopedReadFailure, _ScopedRubyReader


SAFE_OPEN = all(getattr(os, name, 0) for name in (
    'O_DIRECTORY', 'O_NOFOLLOW', 'O_NONBLOCK',
)) and rubygems._DIRECTORY_OPEN in os.supports_dir_fd


def _fifo_replacement_witness(name):
    """Run in a bounded child: replacement at the hook needs no timing race."""
    check = unittest.TestCase()
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory).resolve()
        target = root / name
        target.write_text('regular validated input', encoding='utf-8')
        reader = _ScopedRubyReader(root)
        real_open = os.open
        real_stat = Path.stat
        real_fstat = os.fstat
        opened = []
        validated = []
        events = []

        def inspect(path, *args, **kwargs):
            result = real_stat(path, *args, **kwargs)
            if path == target and stat.S_ISREG(result.st_mode):
                validated.append(True)
            return result

        def replace_then_open(path, flags, *args, **kwargs):
            if path == name and 'dir_fd' in kwargs:
                check.assertTrue(validated, 'replacement must follow regular validation')
                check.assertEqual(flags, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
                target.unlink()
                os.mkfifo(target)
                events.append('replace')
            descriptor = real_open(path, flags, *args, **kwargs)
            opened.append(descriptor)
            events.append(('open', descriptor))
            return descriptor

        def inspect_descriptor(descriptor):
            events.append(('fstat', descriptor))
            return real_fstat(descriptor)

        with patch.object(Path, 'stat', inspect), \
                patch.object(os, 'open', replace_then_open), \
                patch.object(os, 'fstat', inspect_descriptor), \
                patch.object(os, 'read', side_effect=AssertionError('FIFO content read')) as read:
            result = reader.read(name)
        check.assertIsInstance(result, _ScopedReadFailure)
        expected = 'invalid_gemfile' if name == 'Gemfile' else 'invalid_lockfile'
        check.assertEqual(result.reason, expected)
        check.assertEqual(result.safe_category, 'Scoped input is not regular.')
        read.assert_not_called()
        check.assertEqual(events[-2:], [('open', opened[-1]), ('fstat', opened[-1])])
        check.assertTrue(stat.S_ISFIFO(target.stat().st_mode))
        for descriptor in opened:
            with check.assertRaises(OSError) as failure:
                real_fstat(descriptor)
            check.assertEqual(failure.exception.errno, errno.EBADF)


class ScopedRubyReadTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.reader = _ScopedRubyReader(self.root)

    def assert_reason(self, name, reason):
        result = self.reader.read(name)
        self.assertIsInstance(result, _ScopedReadFailure)
        self.assertEqual(result.reason, reason)
        self.assertNotIn(str(self.root), repr(result))
        return result

    @unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
    def test_exact_names_read_strict_utf8_and_normalize_only_crlf(self):
        for name in ('Gemfile', 'Gemfile.lock'):
            with self.subTest(name=name):
                (self.root / name).write_bytes('café\r\nnext\nlast\r'.encode())
                self.assertEqual(self.reader.read(name), 'café\nnext\nlast\r')
                (self.root / name).write_bytes(b'\xff')
                self.assert_reason(name, 'invalid_gemfile' if name == 'Gemfile' else 'invalid_lockfile')
        for name in ('gemfile', 'Gemfile.other', '../Gemfile', 'nested/Gemfile'):
            with self.assertRaises(ValueError):
                self.reader.read(name)

    @unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
    def test_missing_inputs_ignore_parent_nested_and_alternate_decoys(self):
        nested = self.root / 'nested'
        nested.mkdir()
        for name in ('Gemfile', 'Gemfile.lock'):
            (self.root / (name + '.other')).write_text('alternate')
            (nested / name).write_text('nested')
        with patch.object(Path, 'read_text', side_effect=AssertionError('pathname content read')):
            self.assert_reason('Gemfile', 'gemfile_missing')
            self.assert_reason('Gemfile.lock', 'lockfile_missing')
            nested_reader = _ScopedRubyReader(nested)
            (nested / 'Gemfile').unlink()
            (self.root / 'Gemfile').write_text('parent decoy')
            self.assertEqual(nested_reader.read('Gemfile').reason, 'gemfile_missing')

    @unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
    def test_nonregular_dangling_and_unreadable_are_safe_failures(self):
        for name in ('Gemfile', 'Gemfile.lock'):
            invalid = 'invalid_gemfile' if name == 'Gemfile' else 'invalid_lockfile'
            target = self.root / name
            target.mkdir()
            self.assert_reason(name, invalid)
            target.rmdir()
            target.symlink_to('absent')
            self.assert_reason(name, invalid)
            target.unlink()
            target.write_text('content')
            with patch.object(os, 'open', side_effect=PermissionError('PRIVATE_PATH')) as opened:
                self.assert_reason(name, invalid)
                self.assertEqual(opened.call_count, 1)
            target.unlink()

    @unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
    def test_internal_links_read_only_resolved_contained_file(self):
        nested = self.root / 'nested'
        nested.mkdir()
        (nested / 'evidence').write_text('contained')
        for name in ('Gemfile', 'Gemfile.lock'):
            (self.root / name).symlink_to('nested/evidence')
            self.assertEqual(self.reader.read(name), 'contained')

    @unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
    def test_escaping_links_never_open_or_read_target(self):
        outside = self.root / 'outside'
        outside.mkdir()
        inside = self.root / 'inside'
        inside.mkdir()
        (outside / 'evidence').write_text('DO_NOT_READ')
        reader = _ScopedRubyReader(inside)
        for name in ('Gemfile', 'Gemfile.lock'):
            (inside / name).symlink_to(outside / 'evidence')
            with patch.object(os, 'open', side_effect=AssertionError('outside open')) as opened:
                result = reader.read(name)
            self.assertEqual(result.reason, 'unsafe_gemfile' if name == 'Gemfile' else 'invalid_lockfile')
            opened.assert_not_called()

    def test_missing_capabilities_fail_closed_without_open_or_read(self):
        (self.root / 'Gemfile').write_text('content')
        for name in ('O_DIRECTORY', 'O_NOFOLLOW', 'O_NONBLOCK'):
            with self.subTest(capability=name), patch.object(os, name, 0, create=True), \
                    patch.object(os, 'open') as opened, patch.object(os, 'read') as read:
                self.assert_reason('Gemfile', 'invalid_gemfile')
                opened.assert_not_called()
                read.assert_not_called()
        with patch.object(os, 'supports_dir_fd', set()), patch.object(os, 'open') as opened:
            self.assert_reason('Gemfile.lock', 'invalid_lockfile')
            opened.assert_not_called()

    def test_unresolvable_root_fails_safely_without_open(self):
        reader = _ScopedRubyReader(self.root / 'absent')
        with patch.object(os, 'open') as opened:
            for name in ('Gemfile', 'Gemfile.lock'):
                result = reader.read(name)
                self.assertEqual(result.reason,
                                 'invalid_gemfile' if name == 'Gemfile' else 'invalid_lockfile')
                self.assertNotIn(str(self.root), repr(result))
            opened.assert_not_called()

    @unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
    def test_root_resolves_once_and_reads_leave_supplied_inputs_unchanged(self):
        for name in ('Gemfile', 'Gemfile.lock'):
            (self.root / name).write_bytes(b'evidence\r\n')
        real_resolve = Path.resolve
        root_resolutions = []

        def resolve(path, *args, **kwargs):
            if path == self.root:
                root_resolutions.append(path)
            return real_resolve(path, *args, **kwargs)

        before = {name: (self.root / name).read_bytes()
                  for name in ('Gemfile', 'Gemfile.lock')}
        with patch.object(Path, 'resolve', resolve), \
                patch.object(subprocess, 'run', side_effect=AssertionError('execution forbidden')):
            reader = _ScopedRubyReader(self.root)
            self.assertEqual(reader.read('Gemfile'), 'evidence\n')
            self.assertEqual(reader.read('Gemfile.lock'), 'evidence\n')
        self.assertEqual(root_resolutions, [self.root])
        self.assertEqual(before, {name: (self.root / name).read_bytes() for name in before})

    @unittest.skipUnless(SAFE_OPEN and hasattr(os, 'mkfifo'), 'real FIFO operations unavailable')
    def test_existing_fifo_is_rejected_by_metadata_without_open(self):
        os.mkfifo(self.root / 'Gemfile')
        with patch.object(os, 'open') as opened, patch.object(os, 'read') as read:
            self.assert_reason('Gemfile', 'invalid_gemfile')
            opened.assert_not_called()
            read.assert_not_called()

    @unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
    def test_unsupported_directory_relative_operation_has_no_fallback(self):
        (self.root / 'Gemfile').write_text('content')
        real_open = os.open
        descriptors = []

        def open_relative(path, flags, **kwargs):
            if kwargs:
                raise NotImplementedError('unsupported dir_fd')
            descriptor = real_open(path, flags)
            descriptors.append(descriptor)
            return descriptor

        with patch.object(os, 'open', open_relative), patch.object(os, 'read') as read:
            self.assert_reason('Gemfile', 'invalid_gemfile')
            read.assert_not_called()
        self.assert_closed(descriptors)

    def assert_closed(self, descriptors):
        self.assertTrue(descriptors)
        for descriptor in descriptors:
            with self.assertRaises(OSError) as error:
                os.fstat(descriptor)
            self.assertEqual(error.exception.errno, errno.EBADF)

    @unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
    def test_final_and_directory_symlink_replacements_reject_and_close(self):
        nested = self.root / 'nested'
        nested.mkdir()
        (nested / 'evidence').write_text('validated')
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / 'evidence').write_text('DO_NOT_READ')
        real_open = os.open
        for replace_directory in (False, True):
            target = self.root / 'Gemfile'
            target.symlink_to('nested/evidence')
            opened = []

            def replacement(path, flags, **kwargs):
                if replace_directory and path == 'nested':
                    nested.rename(self.root / 'saved')
                    nested.symlink_to(outside, target_is_directory=True)
                elif not replace_directory and path == 'evidence':
                    (nested / 'evidence').unlink()
                    (nested / 'evidence').symlink_to(outside / 'evidence')
                descriptor = real_open(path, flags, **kwargs)
                opened.append(descriptor)
                return descriptor

            with patch.object(os, 'open', replacement), patch.object(os, 'read') as read:
                self.assert_reason('Gemfile', 'invalid_gemfile')
                read.assert_not_called()
            self.assert_closed(opened)
            target.unlink()
            if not replace_directory:
                (nested / 'evidence').unlink()
                (nested / 'evidence').write_text('validated')

    @unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
    def test_cleanup_after_success_read_failure_and_fstat_failure(self):
        (self.root / 'Gemfile').write_text('content')
        real_open = os.open
        for failure in (None, 'read', 'fstat'):
            opened = []

            def track_open(*args, **kwargs):
                descriptor = real_open(*args, **kwargs)
                opened.append(descriptor)
                return descriptor

            with patch.object(os, 'open', track_open):
                if failure:
                    with patch.object(os, failure, side_effect=OSError('PRIVATE_PATH')):
                        self.assert_reason('Gemfile', 'invalid_gemfile')
                else:
                    self.assertEqual(self.reader.read('Gemfile'), 'content')
            self.assert_closed(opened)

    @unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
    def test_byte_limits_are_exact_and_reads_stop_at_limit_plus_one(self):
        cases = (
            ('Gemfile', rubygems._MAX_GEMFILE_BYTES, 'unsupported_gemfile_syntax'),
            ('Gemfile.lock', rubygems._MAX_SCOPED_LOCK_BYTES, 'invalid_lockfile'),
        )
        real_read = os.read
        for name, limit, excess in cases:
            for over in (0, 1, 200):
                with self.subTest(name=name, excess=over):
                    # Short physical lines keep the file limit independent of line limits.
                    content = (b'#\n' * ((limit + over) // 2) + b'#' * ((limit + over) % 2))
                    (self.root / name).write_bytes(content)
                    counts = []

                    def track_read(descriptor, count):
                        chunk = real_read(descriptor, count)
                        counts.append(len(chunk))
                        return chunk

                    with patch.object(os, 'read', track_read):
                        result = self.reader.read(name)
                    self.assertLessEqual(sum(counts), limit + 1)
                    if over:
                        self.assertEqual(result.reason, excess)
                        self.assertEqual(sum(counts), limit + 1)
                    else:
                        self.assertEqual(result, content.decode())

    @unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
    def test_physical_line_byte_limit_excludes_lf_and_crlf(self):
        for ending in (b'\n', b'\r\n'):
            for excess in (0, 1):
                with self.subTest(ending=ending, excess=excess):
                    content = b'#' * (16 * 1024 + excess)
                    prefix = b'source "https://rubygems.org"' + ending
                    (self.root / 'Gemfile').write_bytes(prefix + content + ending)
                    text = self.reader.read('Gemfile')
                    self.assertIsInstance(text, str)
                    result = parse_gemfile(text)
                    if excess:
                        self.assertEqual(result.reason, 'unsupported_gemfile_syntax')
                        self.assertEqual(result.line, 2)
                    else:
                        self.assertIsInstance(result, ParsedGemfile)
        (self.root / 'Gemfile').write_bytes(('#' + 'é' * (8 * 1024)).encode())
        result = parse_gemfile(self.reader.read('Gemfile'))
        self.assertEqual(result.reason, 'unsupported_gemfile_syntax')

    @unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
    def test_later_line_limit_does_not_hide_first_line_recognition_failure(self):
        (self.root / 'Gemfile').write_text('gem\n' + '#' * (16 * 1024 + 1))
        result = parse_gemfile(self.reader.read('Gemfile'))
        self.assertIsInstance(result, GemfileParseFailure)
        self.assertEqual(result.reason, 'invalid_gemfile')
        self.assertEqual(result.line, 1)

    @unittest.skipUnless(SAFE_OPEN and hasattr(os, 'mkfifo'), 'real FIFO operations unavailable')
    def test_gemfile_regular_to_fifo_replacement_does_not_block(self):
        self.run_fifo_child('Gemfile')

    @unittest.skipUnless(SAFE_OPEN and hasattr(os, 'mkfifo'), 'real FIFO operations unavailable')
    def test_lock_regular_to_fifo_replacement_does_not_block(self):
        self.run_fifo_child('Gemfile.lock')

    def run_fifo_child(self, name):
        script = (
            'import runpy, sys; '
            'module = runpy.run_path(sys.argv[1]); '
            'module["_fifo_replacement_witness"](sys.argv[2]); print("ok")'
        )
        try:
            result = subprocess.run(
                [sys.executable, '-c', script, str(Path(__file__).resolve()), name],
                capture_output=True, text=True, timeout=5, check=False,
            )
        except subprocess.TimeoutExpired:
            self.fail(name + ' replacement blocked waiting for a FIFO writer')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'ok')
