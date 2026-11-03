"""Synthetic local-only NuGet input security and exact boundary witnesses."""

import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch

from libyears import nuget_input as inputs


class InputAssertions(unittest.TestCase):
    def rejected(self, category, function, *arguments):
        with self.assertRaises(inputs.NuGetInputFailure) as caught:
            function(*arguments)
        self.assertEqual(caught.exception.category, category)
        self.assertEqual(str(caught.exception), 'NuGet input rejected: ' + category + '.')


class JSONInputTests(InputAssertions):
    def test_valid_strings_escapes_containers_and_scalars(self):
        value = {'key': ['[ { \\"', {}, None, True, False, -12, 1.25], 'é': '\U0001f600'}
        self.assertEqual(inputs.decode_json(json.dumps(value)), value)

    def test_duplicate_keys_at_every_level_are_malformed(self):
        for text in ('{"a":1,"a":2}', '{"outer":{"a":1,"a":2}}',
                     '{"a":1,"\\u0061":2}', '{"unknown":0,"a":{"x":1,"x":2}}'):
            with self.subTest(text=text):
                self.rejected('malformed', inputs.decode_json, text)

    def test_complete_framing_rejects_malformed_after_unsupported(self):
        for text in ('{"unknown":0,"later":}', '{"unknown":0} trailing',
                     '{"unknown":0,}', '[1,,2]', '/*comment*/{}', '"unterminated',
                     '"\\uQQQQ"', '{', ']', 'true false'):
            with self.subTest(text=text):
                self.rejected('malformed', inputs.decode_json, text)

    def test_nonfinite_constants_and_float_overflow_are_malformed(self):
        for token in ('NaN', 'Infinity', '-Infinity', '1e999', '-1e999'):
            self.rejected('malformed', inputs.decode_json, '[' + token + ']')

    def test_boolean_is_not_schema_integer(self):
        for value in (True, False, 1.0, '1', None, 2):
            self.assertFalse(inputs.schema_version_one(value))
        self.assertTrue(inputs.schema_version_one(inputs.decode_json('1')))

    def test_depth_cap_and_cap_plus_one_before_decoder(self):
        depth = inputs.MAX_JSON_DEPTH
        self.assertEqual(inputs.decode_json('[' * depth + '0' + ']' * depth),
                         json.loads('[' * depth + '0' + ']' * depth))
        with patch.object(inputs.json, 'loads') as decode:
            self.rejected('limit', inputs.decode_json, '[' * (depth + 1) + '0' + ']' * (depth + 1))
        decode.assert_not_called()

    def test_value_cap_and_cap_plus_one_containers_count_keys_do_not(self):
        cap = inputs.MAX_JSON_VALUES
        text = '[' + ','.join('0' for unused in range(cap - 1)) + ']'
        self.assertEqual(len(inputs.decode_json(text)), cap - 1)
        with patch.object(inputs.json, 'loads') as decode:
            self.rejected('limit', inputs.decode_json, text[:-1] + ',0]')
        decode.assert_not_called()
        with patch.object(inputs, 'MAX_JSON_VALUES', 3):
            self.assertEqual(inputs.decode_json('{"a":{},"b":0}'), {'a': {}, 'b': 0})
            self.rejected('limit', inputs.decode_json, '{"a":{},"b":[0]}')

    def test_string_cap_and_cap_plus_one_including_keys_and_escapes(self):
        cap = inputs.MAX_STRING_LENGTH
        for character in ('x', '\\u0061', '\\ud83d\\ude00'):
            text = '"' + character * cap + '"'
            self.assertEqual(len(inputs.decode_json(text)), cap)
            with patch.object(inputs.json, 'loads') as decode:
                self.rejected('limit', inputs.decode_json, text[:-1] + character + '"')
            decode.assert_not_called()
        self.rejected('limit', inputs.decode_json, '{"' + 'k' * (cap + 1) + '":0}')

    def test_digit_cap_and_cap_plus_one_before_decoder(self):
        digits = '1' * inputs.MAX_COMPONENT_DIGITS
        self.assertEqual(inputs.decode_json(digits), int(digits))
        self.assertEqual(inputs.decode_json('-' + digits), -int(digits))
        self.assertIsInstance(inputs.decode_json('0.' + digits), float)
        for token in (digits + '1', '-' + digits + '1', '0.' + digits + '1', '1e' + digits + '1'):
            with patch.object(inputs.json, 'loads') as decode:
                self.rejected('limit', inputs.decode_json, token)
            decode.assert_not_called()

    def test_semantic_findings_prioritize_malformed_regardless_of_order(self):
        for flags in (('unsupported', 'malformed'), ('malformed', 'unsupported')):
            findings = inputs.ValidationFindings()
            for flag in flags:
                setattr(findings, flag, True)
            self.rejected('malformed', findings.finish)
        self.rejected('unsupported', inputs.ValidationFindings(unsupported=True).finish)
        inputs.ValidationFindings().finish()

    def test_shared_count_and_string_limits(self):
        for cap in (inputs.MAX_DIRECT_REFERENCES, inputs.MAX_LOCK_ENTRIES,
                    inputs.MAX_PACKAGE_RECORDS, inputs.MAX_FRAMEWORK_LENGTH,
                    inputs.MAX_ASSERTION_LENGTH, inputs.MAX_STRING_LENGTH):
            inputs.check_count(cap, cap)
            self.rejected('limit', inputs.check_count, cap + 1, cap)
        self.assertTrue(inputs.bounded_string('x' * inputs.MAX_STRING_LENGTH))
        self.assertFalse(inputs.bounded_string('x' * (inputs.MAX_STRING_LENGTH + 1)))
        self.assertFalse(inputs.bounded_string(None))

    def test_xml_depth_elements_and_attributes_caps(self):
        budget = inputs.XMLBudget()
        for unused in range(inputs.MAX_XML_DEPTH):
            budget.start({})
        self.rejected('limit', budget.start, {})
        budget = inputs.XMLBudget()
        for unused in range(inputs.MAX_XML_ELEMENTS):
            budget.start({})
            budget.end()
        self.rejected('limit', budget.start, {})
        budget = inputs.XMLBudget()
        budget.start({str(i): '' for i in range(inputs.MAX_XML_ATTRIBUTES)})
        budget.end()
        self.rejected('limit', budget.start,
                      {str(i): '' for i in range(inputs.MAX_XML_ATTRIBUTES + 1)})
        inputs.XMLBudget().start({'key': 'x' * inputs.MAX_STRING_LENGTH})
        self.rejected('limit', inputs.XMLBudget().start,
                      {'key': 'x' * (inputs.MAX_STRING_LENGTH + 1)})


class ScopedNuGetReaderTests(InputAssertions):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / 'root'
        self.root.mkdir()
        self.project = self.root / 'Selected.csproj'
        self.project.write_bytes(b'<Project/>\r\n')

    def reader(self):
        return inputs.ScopedNuGetReader(self.root, 'Selected.csproj', 'witness.json')

    def test_exact_bytes_and_decoding_without_line_normalization(self):
        data = b'\xef\xbb\xbf<Project>\xc3\xa9</Project>\r\n'
        self.project.write_bytes(data)
        with self.reader() as reader:
            actual = reader.read('Selected.csproj')
        self.assertEqual(actual.data, data)
        self.assertEqual(actual.text, data.decode('utf-8'))
        self.assertIsNone(reader.directory)

    def test_missing_invalid_utf8_and_dangling_link(self):
        with self.reader() as reader:
            self.rejected('missing', reader.read, 'packages.lock.json')
            self.project.write_bytes(b'\xffsecret-canary')
            self.rejected('malformed', reader.read, 'Selected.csproj')
            self.project.unlink()
            self.project.symlink_to('absent')
            self.rejected('malformed', reader.read, 'Selected.csproj')

    def test_all_byte_caps_and_cap_plus_one_reads_at_most_cap_plus_one(self):
        for name, cap in (('Selected.csproj', inputs.MAX_PROJECT_BYTES),
                          ('packages.lock.json', inputs.MAX_LOCK_BYTES),
                          ('witness.json', inputs.MAX_PROVENANCE_BYTES)):
            path = self.root / name
            path.write_bytes(b'x' * cap)
            with self.reader() as reader:
                self.assertEqual(len(reader.read(name).data), cap)
            path.write_bytes(b'x' * (cap + 100))
            read = os.read
            received = []
            def capture(descriptor, amount):
                chunk = read(descriptor, amount)
                received.append(len(chunk))
                return chunk
            with self.reader() as reader, patch.object(inputs.os, 'read', side_effect=capture):
                self.rejected('limit', reader.read, name)
            self.assertEqual(sum(received), cap + 1)

    def test_permits_relative_absolute_and_nested_inside_symlinks(self):
        directory = self.root / 'nested'
        directory.mkdir()
        target = directory / 'bytes'
        target.write_bytes(b'inside')
        for spelling in ('nested/bytes', str(target), 'nested/../nested/bytes'):
            self.project.unlink()
            self.project.symlink_to(spelling)
            with self.reader() as reader:
                self.assertEqual(reader.read('Selected.csproj').data, b'inside')

    def test_rejects_escape_without_inspecting_or_opening_outside(self):
        outside = self.base / 'outside'
        outside.write_bytes(b'secret-canary')
        for spelling in ('../outside', str(outside)):
            self.project.unlink()
            self.project.symlink_to(spelling)
            inspected = []
            original = os.stat
            def capture(path, *args, **kwargs):
                inspected.append(str(path))
                return original(path, *args, **kwargs)
            with self.reader() as reader, patch.object(inputs.os, 'stat', side_effect=capture):
                self.rejected('malformed', reader.read, 'Selected.csproj')
            self.assertNotIn(str(outside), inspected)
            self.assertNotIn('outside', inspected)

    def test_symlink_loop_is_bounded(self):
        self.project.unlink()
        self.project.symlink_to('Selected.csproj')
        with self.reader() as reader:
            self.rejected('malformed', reader.read, 'Selected.csproj')

    def test_fifo_and_directory_rejected_before_open_or_read(self):
        self.project.unlink()
        os.mkfifo(self.project)
        with self.reader() as reader, patch.object(inputs.os, 'read') as read:
            self.rejected('malformed', reader.read, 'Selected.csproj')
        read.assert_not_called()
        self.project.unlink()
        self.project.mkdir()
        with self.reader() as reader:
            self.rejected('malformed', reader.read, 'Selected.csproj')

    def test_device_type_is_rejected_without_open(self):
        with self.reader() as reader:
            original = reader._resolve_target
            def device(name):
                path, info = original(name)
                values = list(info)
                values[0] = stat.S_IFCHR | 0o600
                return path, os.stat_result(values)
            with patch.object(reader, '_resolve_target', side_effect=device), \
                    patch.object(inputs.os, 'open') as opened:
                self.rejected('malformed', reader.read, 'Selected.csproj')
            opened.assert_not_called()

    def test_replacement_between_inspection_and_open_rejected_before_read(self):
        original = os.open
        for replacement in ('regular', 'fifo', 'symlink'):
            self.project.unlink()
            self.project.write_bytes(b'original')
            def replace_at_open(path, flags, *args, **kwargs):
                if path == 'Selected.csproj':
                    self.project.unlink()
                    if replacement == 'regular':
                        self.project.write_bytes(b'changed')
                    elif replacement == 'fifo':
                        os.mkfifo(self.project)
                    else:
                        self.project.symlink_to('missing')
                return original(path, flags, *args, **kwargs)
            with self.reader() as reader, patch.object(inputs.os, 'open', side_effect=replace_at_open), \
                    patch.object(inputs.os, 'read') as read:
                self.rejected('malformed', reader.read, 'Selected.csproj')
            read.assert_not_called()

    def test_mutation_and_replacement_during_read_fail_closed(self):
        original = os.read
        for action in ('rewrite', 'same_size', 'replace', 'retarget'):
            self.project.write_bytes(b'original')
            changed = False
            def mutate(descriptor, amount):
                nonlocal changed
                data = original(descriptor, amount)
                if not changed:
                    changed = True
                    if action in ('rewrite', 'same_size'):
                        before = self.project.stat()
                        data_after = b'changed!' if action == 'same_size' else b'changed-longer'
                        self.project.write_bytes(data_after)
                        os.utime(self.project, ns=(before.st_atime_ns, before.st_mtime_ns + 1))
                    else:
                        self.project.unlink()
                        if action == 'replace':
                            self.project.write_bytes(b'original')
                        else:
                            (self.root / 'other').write_bytes(b'original')
                            self.project.symlink_to('other')
                return data
            with self.reader() as reader, patch.object(inputs.os, 'read', side_effect=mutate):
                self.rejected('malformed', reader.read, 'Selected.csproj')
            self.project.unlink()
            self.project.write_bytes(b'original')

    def test_missing_safety_primitives_fail_closed(self):
        for flag in ('O_DIRECTORY', 'O_NOFOLLOW', 'O_NONBLOCK'):
            with patch.object(inputs.os, flag, 0):
                self.rejected('malformed', self.reader().__enter__)
        with patch.object(inputs.os, 'supports_dir_fd', set()):
            self.rejected('malformed', self.reader().__enter__)
        with patch.object(inputs.os, 'supports_follow_symlinks', set()):
            self.rejected('malformed', self.reader().__enter__)

    def test_only_selected_immediate_filenames_are_admitted(self):
        for name in ('../other.csproj', '/tmp/other.csproj', 'nested/a', 'a\\b', '', '.', '..'):
            with self.assertRaises(ValueError):
                inputs.ScopedNuGetReader(self.root, name)
        with self.reader() as reader, patch.object(inputs.os, 'open') as opened:
            for name in ('Gemfile', 'NuGet.Config', 'Directory.Build.props', 'other.csproj',
                         'project.assets.json', '.nupkg.metadata', '../packages.lock.json'):
                with self.assertRaises(ValueError):
                    reader.read(name)
        opened.assert_not_called()

    def test_io_failures_are_fixed_safe_diagnostics_and_descriptors_close(self):
        with self.reader() as reader:
            descriptor = reader.directory
            with patch.object(inputs.os, 'read', side_effect=OSError('secret-canary')):
                self.rejected('malformed', reader.read, 'Selected.csproj')
        with self.assertRaises(OSError):
            os.fstat(descriptor)


if __name__ == '__main__':
    unittest.main()
