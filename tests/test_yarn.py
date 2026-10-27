from pathlib import Path
import tempfile
import unittest

from libyears.yarn import (
    INVALID_LOCKFILE,
    UNSUPPORTED_LOCKFILE_FORMAT,
    YarnEntry,
    YarnFailure,
    parse_lockfile,
    recognize_v1,
)


FIXTURES = Path(__file__).parent / "fixtures" / "yarn"


class YarnRecognitionTests(unittest.TestCase):
    def test_canonical_header_fixture(self):
        text = (FIXTURES / "classic-header.lock").read_text(encoding="utf-8")
        self.assertIsNone(recognize_v1(text))

    def test_leading_comments_and_blank_lines(self):
        text = '\n# local comment\n\n# yarn lockfile v1\n\nalpha@^1:\n'
        self.assertIsNone(recognize_v1(text))

    def test_recognition_does_not_parse_entries(self):
        self.assertIsNone(recognize_v1('# yarn lockfile v1\ninvalid body "'))

    def test_unsupported_missing_and_contradictory_headers(self):
        cases = [
            '',
            '# ordinary comment\nalpha@^1:\n  version "1.0.0"\n',
            'alpha@^1:\n# yarn lockfile v1\n',
            '# example: # yarn lockfile v1\n',
            '# yarn lockfile v1 trailing text\n',
            ' # yarn lockfile v1\n',
            '# yarn lockfile v2\n',
            '# yarn lockfile v1\n# yarn lockfile v2\n',
            '# yarn lockfile v2\n# yarn lockfile v1\n',
            '# yarn lockfile v1\n# Yarn Berry\n',
            '# yarn lockfile v1\n__metadata:\n  version: 8\n',
            (FIXTURES / 'berry.lock').read_text(encoding='utf-8'),
        ]
        for text in cases:
            with self.subTest(text=text):
                failure = recognize_v1(text)
                self.assertEqual(failure.reason, UNSUPPORTED_LOCKFILE_FORMAT)
                self.assertTrue(failure.diagnostic)

    def test_ordinary_comments_do_not_contradict_header(self):
        text = '# yarn lockfile v1\n# generated with yarn install\n'
        self.assertIsNone(recognize_v1(text))


class YarnEntryTests(unittest.TestCase):
    def parse(self, body):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'yarn.lock'
            path.write_text('# yarn lockfile v1\n' + body, encoding='utf-8')
            return parse_lockfile(path)

    def test_supported_entries_fixture_preserves_order_and_decoded_text(self):
        entries = parse_lockfile(FIXTURES / 'entries.lock')
        self.assertEqual(entries, (
            YarnEntry(('alpha@^1.0.0', 'alpha@~1.2.0'), '1.2.3'),
            YarnEntry(('@scope/widget@^2.0.0',), '2.4.0-beta.1+build'),
            YarnEntry(('escaped@a\\b"c,d', 'plain@1.0.0'), '1.0.0'),
            YarnEntry(('alpha@^1.0.0',), '1.2.3'),
        ))
        self.assertIsNot(entries[0], entries[3])

    def test_quoted_content_is_not_normalized(self):
        entries = self.parse('" alpha@>=1 <2 ":\n  version "1.2.0"\n')
        self.assertEqual(entries[0].selectors, (' alpha@>=1 <2 ',))

    def test_empty_header_only_file_has_no_entries(self):
        self.assertEqual(self.parse('\n# comment\n'), ())

    def test_missing_or_unusable_version_retained_for_later_ambiguity(self):
        entries = self.parse(
            'alpha@^1:\n  resolved "https://example.org/alpha.tgz"\n'
            'beta@^1:\n  version "^1.0.0"\n'
            'gamma@^1:\n  version ""\n'
        )
        self.assertEqual([entry.version for entry in entries], [None, '^1.0.0', ''])

    def test_metadata_cannot_supply_a_version(self):
        entries = self.parse('alpha@^1:\n  dependencies:\n    version "1.0.0"\n')
        self.assertIsNone(entries[0].version)

    def test_comments_and_blank_lines_inside_entries(self):
        entries = self.parse('alpha@^1:\n\n  # explanation\n  version "1.0.0"\n')
        self.assertEqual(entries, (YarnEntry(('alpha@^1',), '1.0.0'),))

    def test_malformed_fixture_files(self):
        for filename in ('duplicate-version.lock', 'unterminated-key.lock'):
            with self.subTest(filename=filename):
                failure = parse_lockfile(FIXTURES / filename)
                self.assertEqual(failure.reason, INVALID_LOCKFILE)
                self.assertIn('line ', failure.diagnostic)

    def test_malformed_key_structure_rejects_whole_file(self):
        keys = [
            'alpha@^1,', ',alpha@^1:', 'alpha@^1,, beta@^1:',
            'alpha@^1, :', 'alpha@^1', 'alpha@^1: garbage',
            '"alpha@^1" "beta@^1":', '"alpha@^1",:',
            'alpha@^1, "alpha@^1":', '"":',
            'alpha@^1 "extra":', '"alpha@^1": extra:',
            'alpha@file:../path:', 'alpha@[1]:',
            '"alpha@unterminated:', '"alpha@dangling' + chr(92),
            '"alpha@bad' + chr(92) + 'n":',
            'alpha@bad' + chr(92) + 'escape:',
        ]
        for key in keys:
            with self.subTest(key=key):
                failure = self.parse(key + '\n  version "1.0.0"\n')
                self.assertIsInstance(failure, YarnFailure)
                self.assertEqual(failure.reason, INVALID_LOCKFILE)

    def test_malformed_field_structure_rejects_whole_file(self):
        bodies = [
            '  version "1.0.0"\n',
            'alpha@^1:\n version "1.0.0"\n',
            'alpha@^1:\n\tversion "1.0.0"\n',
            'alpha@^1:\n    version "1.0.0"\n',
            'alpha@^1:\n  version:\n    child "1.0.0"\n',
            'alpha@^1:\n  version\n',
            'alpha@^1:\n  version "1.0.0" extra\n',
            'alpha@^1:\n  version "unterminated\n',
            'alpha@^1:\n  version "1.0.0"\n  version "1.0.0"\n',
            'alpha@^1:\n  dependencies:\n  dependencies:\n',
            'alpha@^1:\n  dependencies:\n    child "1"\n    child "2"\n',
            'alpha@^1:\n  dependencies:\n    child:\n      version "1"\n',
            'alpha@^1:\n  version [1.0.0]\n',
            'alpha@^1:\n  version "bad' + chr(92) + 't"\n',
        ]
        for body in bodies:
            with self.subTest(body=body):
                failure = self.parse(body)
                self.assertIsInstance(failure, YarnFailure)
                self.assertEqual(failure.reason, INVALID_LOCKFILE)

    def test_format_failure_precedes_body_validation(self):
        failure = parse_lockfile(FIXTURES / 'berry.lock')
        self.assertEqual(failure.reason, UNSUPPORTED_LOCKFILE_FORMAT)

    def test_unreadable_or_undecodable_generation_is_unclassifiable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'yarn.lock'
            self.assertEqual(parse_lockfile(path).reason, UNSUPPORTED_LOCKFILE_FORMAT)
            path.write_bytes(bytes([255]))
            self.assertEqual(parse_lockfile(path).reason, UNSUPPORTED_LOCKFILE_FORMAT)


if __name__ == "__main__":
    unittest.main()
