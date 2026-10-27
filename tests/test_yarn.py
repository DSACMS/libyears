from pathlib import Path
import unittest

from libyears.yarn import UNSUPPORTED_LOCKFILE_FORMAT, recognize_v1


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


if __name__ == "__main__":
    unittest.main()
