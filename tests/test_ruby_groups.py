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


def _fifo_replacement_witness(name, scoped=False):
    """Run in a bounded child: replacement at the hook needs no timing race."""
    check = unittest.TestCase()
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory).resolve()
        target = root / name
        if scoped:
            (root / 'Gemfile').write_text('source "https://rubygems.org"\ngem "rack"\n')
            (root / 'Gemfile.lock').write_text(LOCK)
        else:
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

        real_read = os.read
        def read_regular(descriptor, count):
            check.assertTrue(stat.S_ISREG(real_fstat(descriptor).st_mode), 'FIFO content read')
            return real_read(descriptor, count)

        with patch.object(Path, 'stat', inspect), \
                patch.object(os, 'open', replace_then_open), \
                patch.object(os, 'fstat', inspect_descriptor), \
                patch.object(os, 'read', side_effect=read_regular) as read,                 patch('urllib.request.urlopen', side_effect=AssertionError('network')) as lookup:
            if scoped:
                result = rubygems.scoped_ruby_source_result(root, ('default',))
            else:
                result = reader.read(name)
        expected = 'invalid_gemfile' if name == 'Gemfile' else 'invalid_lockfile'
        if scoped:
            check.assertEqual(result.source_errors[0].reason, expected)
            check.assertEqual(result.source_errors[0].source, name)
            check.assertEqual(result.dependencies_discovered, None if name == 'Gemfile' else 1)
            check.assertFalse(result.measurement_available)
            check.assertEqual((result.candidates, result.unmeasurable), ((), ()))
            check.assertIsNone(result.evidence.format)
            if name == 'Gemfile':
                check.assertEqual(len(opened), 2, 'must not open lock after Gemfile failure')
                read.assert_not_called()
            else:
                check.assertGreater(read.call_count, 0, 'Gemfile must be consumed before lock')
        else:
            check.assertIsInstance(result, _ScopedReadFailure)
            check.assertEqual(result.reason, expected)
            check.assertEqual(result.safe_category, 'Scoped input is not regular.')
            read.assert_not_called()
        lookup.assert_not_called()
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


SOURCE = 'source "https://rubygems.org"\n'
LOCK = ('GEM\n  remote: https://rubygems.org\n  specs:\n    rack (1)\n'
        'PLATFORMS\n  ruby\nDEPENDENCIES\n  rack\n')


@unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
class ScopedSourceAvailabilityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.network = patch('urllib.request.urlopen', side_effect=AssertionError('network'))
        self.lookup = self.network.start()
        self.addCleanup(self.network.stop)
        self.addCleanup(self.lookup.assert_not_called)

    def source(self, gemfile=SOURCE + 'gem "rack"', lock=None, groups=('default',)):
        (self.root / 'Gemfile').write_text(gemfile)
        if lock is not None:
            (self.root / 'Gemfile.lock').write_text(lock)
        return rubygems.scoped_ruby_source_result(self.root, groups)

    def test_union_deduplicates_and_retains_full_memberships_without_default(self):
        gemfile = SOURCE + ('gem "rack"\ngroup :test, :development, optional: true do\n'
                            'gem "rake", group: :extra\nend\ngem "debug", group: :Test\n')
        result = self.source(gemfile, groups=('test', 'development', 'test'))
        self.assertEqual(result.dependencies_discovered, 1)
        self.assertEqual(result.evidence.requested_groups, ('development', 'test'))
        row = result.unmeasurable[0]
        self.assertEqual(row.name, 'rake')
        self.assertEqual(row.gemfile_evidence.declared_groups, ('development', 'extra', 'test'))
        self.assertEqual(self.source(gemfile, groups=('Test',)).unmeasurable[0].name, 'debug')
        self.assertEqual(self.source(gemfile).unmeasurable[0].name, 'rack')

    def test_known_empty_absent_and_accepted_lock_and_rejected_lock(self):
        for groups in (('default',), ('bench',)):
            gemfile = SOURCE + 'group :bench do\nend'
            absent = self.source(gemfile, groups=groups)
            self.assertEqual(absent.dependencies_discovered, 0)
            self.assertTrue(absent.measurement_available)
            self.assertIsNone(absent.evidence.format)
            accepted = self.source(gemfile, LOCK, groups)
            self.assertEqual(accepted.dependencies_discovered, 0)
            self.assertTrue(accepted.measurement_available)
            self.assertEqual(accepted.evidence.format, 'gemfile_lock')
            rejected = self.source(gemfile, 'arbitrary', groups)
            self.assertEqual(rejected.dependencies_discovered, 0)
            self.assertFalse(rejected.measurement_available)
            self.assertEqual((rejected.candidates, rejected.unmeasurable), ((), ()))
            (self.root / 'Gemfile.lock').unlink()

    def test_missing_lock_keeps_pins_as_unmeasurable_safe_declarations(self):
        result = self.source(SOURCE + 'gem "rack", "= 1"\ngem "rake"')
        self.assertEqual(result.dependencies_discovered, 2)
        self.assertTrue(result.measurement_available)
        self.assertEqual(result.candidates, ())
        self.assertEqual([row.reason for row in result.unmeasurable], ['lockfile_missing'] * 2)
        self.assertEqual(result.unmeasurable[0].declared, 'rack (= 1)')
        self.assertFalse(result.unmeasurable[0].gemfile_evidence.include_lock_requirement)

    def test_complete_recognition_then_unknown_group_prevents_lock_read(self):
        real_read = _ScopedRubyReader.read
        for gemfile, groups, reason in (
            (SOURCE + 'gem "rack"\nputs "bad"', ('unknown',), 'unsupported_gemfile_syntax'),
            (SOURCE + 'gem "rack"\ngem "rack"', ('default',), 'duplicate_gemfile_declaration'),
            (SOURCE + 'gem "rack"', ('default', 'missing', 'other'), 'unknown_ruby_group'),
            (SOURCE + 'gem "rack", group: :Test', ('test',), 'unknown_ruby_group'),
            ('gem\n' + '#' * (16 * 1024 + 1), ('default',), 'invalid_gemfile'),
        ):
            reads = []
            def read(reader, name):
                reads.append(name)
                return real_read(reader, name)
            with self.subTest(reason=reason), patch.object(_ScopedRubyReader, 'read', read):
                result = self.source(gemfile, 'bad lock', groups)
            self.assertEqual(reads, ['Gemfile'])
            self.assertEqual(len(result.source_errors), 1)
            self.assertEqual(result.source_errors[0].reason, reason)
            self.assertIsNone(result.dependencies_discovered)
            self.assertFalse(result.measurement_available)
            self.assertIsNone(result.evidence.format)

    def test_safe_read_reasons_map_to_source_without_salvage(self):
        for name, reasons in (
            ('Gemfile', ('gemfile_missing', 'invalid_gemfile', 'unsafe_gemfile',
                         'unsupported_gemfile_syntax')),
            ('Gemfile.lock', ('invalid_lockfile',)),
        ):
            for reason in reasons:
                calls = []
                def read(reader, input_name):
                    calls.append(input_name)
                    if input_name == name:
                        return _ScopedReadFailure(reason, 'Safe category.')
                    return SOURCE + 'gem "rack"'
                with self.subTest(reason=reason), patch.object(_ScopedRubyReader, 'read', read):
                    result = rubygems.scoped_ruby_source_result(self.root, ('default',))
                self.assertEqual(result.source_errors[0].reason, reason)
                self.assertEqual(result.source_errors[0].source, name)
                self.assertEqual(result.dependencies_discovered, None if name == 'Gemfile' else 1)
                self.assertFalse(result.measurement_available)
                self.assertEqual((result.candidates, result.unmeasurable), ((), ()))
                self.assertEqual(calls, ['Gemfile'] if name == 'Gemfile' else ['Gemfile', 'Gemfile.lock'])
                self.assertEqual(result.evidence.declaration_source, 'Gemfile')
                self.assertEqual(result.evidence.snapshot_source, 'Gemfile.lock')
                self.assertEqual(result.evidence.scope, 'selected_declared_groups')
                self.assertTrue(result.source_present)

    def test_rejected_entire_lock_preserves_known_scope_even_for_excluded_rows(self):
        for lock in ('bad', LOCK + 'CHECKSUMS\n',
                     LOCK.replace('  rack\n', '  rack\n  rack\n'),
                     LOCK + '  broken direct (\n'):
            with self.subTest(lock=lock):
                result = self.source(lock=lock)
                self.assertEqual(result.dependencies_discovered, 1)
                self.assertFalse(result.measurement_available)
                self.assertEqual((result.candidates, result.unmeasurable), ((), ()))
                self.assertEqual(result.source_errors[0].source, 'Gemfile.lock')
                self.assertIsNone(result.evidence.format)

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'real FIFO operations unavailable')
    def test_gemfile_fifo_replacement_composes_unknown_scope_and_no_lock_read(self):
        self.run_source_fifo('Gemfile')

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'real FIFO operations unavailable')
    def test_lock_fifo_replacement_composes_known_scope_and_no_rows(self):
        self.run_source_fifo('Gemfile.lock')

    def run_source_fifo(self, name):
        script = ('import runpy, sys; module=runpy.run_path(sys.argv[1]); '
                  'module["_fifo_replacement_witness"](sys.argv[2], scoped=True); print("ok")')
        try:
            result = subprocess.run([sys.executable, '-c', script, str(Path(__file__).resolve()), name],
                                    capture_output=True, text=True, timeout=5, check=False)
        except subprocess.TimeoutExpired:
            self.fail(name + ' source replacement blocked')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'ok')


@unittest.skipUnless(SAFE_OPEN, 'safe descriptor access unavailable')
class ScopedLockAssociationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.network = patch('urllib.request.urlopen', side_effect=AssertionError('network'))
        self.lookup = self.network.start()
        self.addCleanup(self.network.stop)
        self.addCleanup(self.lookup.assert_not_called)

    def source(self, declaration='gem "rack"', direct='rack', specs=('rack (1)',),
               remote='https://rubygems.org', kind='GEM', source=SOURCE, extra=''):
        text = kind + '\n  remote: ' + remote + '\n  specs:\n'
        text += ''.join('    ' + spec + '\n' for spec in specs)
        text += extra + 'PLATFORMS\n  ruby\nDEPENDENCIES\n'
        text += ''.join('  ' + row + '\n' for row in direct.split('\n') if row)
        (self.root / 'Gemfile').write_text(source + declaration)
        (self.root / 'Gemfile.lock').write_text(text)
        return rubygems.scoped_ruby_source_result(self.root, ('default',))

    def assert_failure(self, result, reason):
        self.assertEqual(result.dependencies_discovered, 1)
        self.assertTrue(result.measurement_available)
        self.assertEqual(result.source_errors, ())
        self.assertEqual(result.candidates, ())
        self.assertEqual(len(result.unmeasurable), 1)
        row = result.unmeasurable[0]
        self.assertEqual(row.reason, reason)
        self.assertEqual(result.evidence.format, 'gemfile_lock')
        return row

    def test_exact_direct_candidate_and_full_safe_memberships(self):
        result = self.source('gem "rack", ">= 1", "< 3", groups: [:default, :test]',
                             'rack (>= 1, < 3)', ('rack (1)', 'rack (1-java)'))
        self.assertEqual(result.dependencies_discovered, 1)
        self.assertEqual(result.unmeasurable, ())
        candidate = result.candidates[0]
        self.assertEqual((candidate.name, candidate.registry_name, candidate.used_version,
                          candidate.version_source), ('rack', 'rack', '1', 'gemfile_lock'))
        self.assertEqual(candidate.declared, 'rack (>= 1, < 3)')
        self.assertEqual(candidate.gemfile_evidence.declared_groups, ('default', 'test'))
        self.assertEqual(candidate.gemfile_evidence.declaration_requirements, ('>= 1', '< 3'))
        self.assertEqual(candidate.gemfile_evidence.lock_requirement, '>= 1, < 3')
        self.assertTrue(candidate.gemfile_evidence.include_lock_requirement)
        self.assertEqual(len(candidate.rubygems_evidence.selected_artifacts), 2)

    def test_no_requirement_has_present_null_and_no_semantic_satisfaction_check(self):
        candidate = self.source().candidates[0]
        self.assertTrue(candidate.gemfile_evidence.include_lock_requirement)
        self.assertIsNone(candidate.gemfile_evidence.lock_requirement)
        # Textual identity alone associates even an apparently unsatisfied requirement.
        result = self.source('gem "rack", ">= 9"', 'rack (>= 9)', ('rack (1)',))
        self.assertEqual(result.candidates[0].used_version, '1')

    def test_missing_direct_identity_cannot_use_transitive_spec_or_pin(self):
        for direct in ('rake', 'Rack', ''):
            row = self.assert_failure(self.source('gem "rack", "= 1"', direct),
                                      'lock_dependency_missing')
            self.assertEqual(row.declared, 'rack (= 1)')
            self.assertFalse(row.gemfile_evidence.include_lock_requirement)
            self.assertIsNone(row.rubygems_evidence)

    def test_excluded_and_lock_only_identities_never_become_candidates(self):
        result = self.source('gem "rack"\ngem "debug", group: :test',
                             'rack\ndebug\nlock_only',
                             ('rack (1)', 'debug (2)', 'lock_only (3)'))
        self.assertEqual(result.dependencies_discovered, 1)
        self.assertEqual([row.name for row in result.candidates], ['rack'])
        self.assertEqual(result.unmeasurable, ())

    def test_f1_nonpublic_gemfile_precedes_missing_direct_after_lock_acceptance(self):
        for direct in ('rake', 'rack'):
            row = self.assert_failure(self.source(direct=direct,
                                      source='source "https://PRIVATE_MARKER.invalid"\n'),
                                      'unsupported_dependency_source')
            self.assertIsNone(row.rubygems_evidence)
            self.assertEqual(row.gemfile_evidence.declared_groups, ('default',))
            self.assertEqual(row.gemfile_evidence.include_lock_requirement, direct == 'rack')
            self.assertNotIn('PRIVATE_MARKER', repr(row))

    def test_f2_unsupported_requirement_omits_unsafe_text_and_artifacts(self):
        for direct in ('rack (https://UNSAFE_MARKER.invalid)', 'rack (*)!'):
            row = self.assert_failure(self.source('gem "rack", ">= 1"', direct),
                                      'unsupported_requirement')
            self.assertEqual(row.declared, 'rack (>= 1)')
            self.assertEqual(row.gemfile_evidence.declaration_requirements, ('>= 1',))
            self.assertFalse(row.gemfile_evidence.include_lock_requirement)
            self.assertIsNone(row.gemfile_evidence.lock_requirement)
            self.assertIsNone(row.rubygems_evidence)
            self.assertNotIn('UNSAFE_MARKER', repr(row))

    def test_textual_mismatch_table_preserves_both_safe_values_without_artifacts(self):
        cases = (
            ('', '>= 0', ()),
            (', ">= 0"', None, ('>= 0',)),
            (', ">=1"', '>= 1', ('>=1',)),
            (', " >= 1 "', '>= 1', (' >= 1 ',)),
            (', ">= 1", "< 3"', '< 3, >= 1', ('>= 1', '< 3')),
            (', "= 1"', '1', ('= 1',)),
        )
        for suffix, lock_requirement, expected in cases:
            with self.subTest(suffix=suffix, lock=lock_requirement):
                direct = 'rack' if lock_requirement is None else 'rack (' + lock_requirement + ')'
                # No selected spec: mismatch must precede missing-version failure.
                result = self.source('gem "rack"' + suffix, direct, ())
                row = self.assert_failure(result, 'declaration_lock_requirement_mismatch')
                self.assertEqual(row.gemfile_evidence.declaration_requirements, expected)
                self.assertTrue(row.gemfile_evidence.include_lock_requirement)
                self.assertEqual(row.gemfile_evidence.lock_requirement, lock_requirement)
                self.assertIsNone(row.rubygems_evidence)
                self.assertIn('equivalence not inferred', result.diagnostics[0][1])

    def test_lock_authority_prefix_precedes_mismatch_and_selected_evidence(self):
        for parameters in (
            {'remote': 'https://PRIVATE_MARKER.invalid'},
            {'remote': 'http://rubygems.org'},
            {'remote': 'https://rubygems.org\n  remote: https://rubygems.org'},
            {'kind': 'GIT'}, {'kind': 'PATH'}, {'direct': 'rack!'},
        ):
            with self.subTest(parameters=parameters):
                row = self.assert_failure(self.source('gem "rack", ">= 1"', **parameters),
                                          'unsupported_dependency_source')
                self.assertIsNone(row.rubygems_evidence)
                self.assertTrue(row.gemfile_evidence.include_lock_requirement)
                self.assertNotIn('PRIVATE_MARKER', repr(row))
        for kind in ('GIT', 'PATH', 'GEM'):
            extra = (kind + '\n  remote: https://PRIVATE_MARKER.invalid\n'
                     '  specs:\n    rack (1)\n')
            row = self.assert_failure(self.source(extra=extra), 'unsupported_dependency_source')
            self.assertIsNone(row.rubygems_evidence)

    def test_existing_isolated_selection_failures_keep_scope_and_artifact_rules(self):
        for specs, reason, artifact_count in (
            ((), 'lock_version_missing', 0),
            (('rack (unknown)',), 'unsupported_lock_evidence', 0),
            (('rack (1)', 'rack (unknown)'), 'unsupported_lock_evidence', 1),
            (('rack (1)', 'rack (2-java)'), 'ambiguous_lock_evidence', 2),
            (('rack (1)', 'rack (1)'), 'ambiguous_lock_evidence', 2),
        ):
            with self.subTest(specs=specs):
                row = self.assert_failure(self.source(specs=specs), reason)
                self.assertTrue(row.gemfile_evidence.include_lock_requirement)
                if artifact_count:
                    self.assertEqual(len(row.rubygems_evidence.selected_artifacts), artifact_count)
                else:
                    self.assertIsNone(row.rubygems_evidence)

    def test_nonpublic_gemfile_does_not_override_unavailable_lock_precedence(self):
        private = 'source "https://PRIVATE_MARKER.invalid"\ngem "rack"'
        (self.root / 'Gemfile').write_text(private)
        absent = rubygems.scoped_ruby_source_result(self.root, ('default',))
        self.assertEqual(absent.unmeasurable[0].reason, 'lockfile_missing')
        (self.root / 'Gemfile.lock').write_text('rejected')
        rejected = rubygems.scoped_ruby_source_result(self.root, ('default',))
        self.assertFalse(rejected.measurement_available)
        self.assertEqual(rejected.dependencies_discovered, 1)
        self.assertEqual(rejected.unmeasurable, ())
        self.assertEqual(rejected.source_errors[0].source, 'Gemfile.lock')
