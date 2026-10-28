"""Offline examples of the supported lock framing."""
from dataclasses import FrozenInstanceError
from pathlib import Path
import unittest

from libyears.gemfile_lock import LockParseFailure, ParsedGemfileLock, parse_lockfile


ORDINARY = (Path(__file__).parent / 'fixtures/rubygems/ordinary.lock').read_text()
EMPTY = 'GEM\n  specs:\n\nPLATFORMS\n  ruby\n\nDEPENDENCIES\n'


class StructureTests(unittest.TestCase):
    def test_preserves_rows_without_promoting_specs_or_metadata_to_scope(self):
        result = parse_lockfile(ORDINARY)
        self.assertIsInstance(result, ParsedGemfileLock)
        self.assertEqual([d.name for d in result.dependencies], ['rack'])
        dependency = result.dependencies[0]
        self.assertEqual(dependency.declared, 'rack (~> 3.0)!')
        self.assertEqual(dependency.requirement_text, '~> 3.0')
        self.assertTrue(dependency.source_pinned)
        self.assertEqual(dependency.line, 13)
        self.assertEqual([s.raw_selection for s in result.sources[0].specs],
                         ['3.0.0', '1.0', '3.0.0'])
        self.assertEqual(result.platforms, ('ruby', 'x86_64-linux'))
        with self.assertRaises(FrozenInstanceError):
            dependency.name = 'changed'

    def test_empty_scope_line_endings_and_optional_metadata(self):
        for text in (EMPTY, EMPTY.replace('\n', '\r\n'),
                     EMPTY + '\nBUNDLED WITH\n   arbitrary-token\n',
                     EMPTY + '\nRUBY VERSION\n   ruby 3.2.0p0\n'):
            with self.subTest(text=text):
                result = parse_lockfile(text)
                self.assertIsInstance(result, ParsedGemfileLock)
                self.assertEqual(result.dependencies, ())

    def test_required_platform_and_singleton_boundaries(self):
        for platform in ('', 'PLATFORMS\n', 'PLATFORMS\n  ruby\n  ruby\n',
                         'PLATFORMS\n  ruby\nPLATFORMS\n  java\n',
                         'PLATFORMS\n   ruby\n', 'PLATFORMS\n  ruby linux\n',
                         'PLATFORMS\n  rübÿ\n'):
            with self.subTest(platform=platform):
                result = parse_lockfile(EMPTY.replace('PLATFORMS\n  ruby\n', platform))
                self.assertIsInstance(result, LockParseFailure)
                self.assertEqual(result.reason, 'invalid_lockfile')

    def test_malformed_tool_runtime_and_duplicate_directs(self):
        for suffix in ('BUNDLED WITH\n', 'BUNDLED WITH\n   1\n   2\n',
                       'BUNDLED WITH\n   1 2\n', 'RUBY VERSION\n  ruby 3\n',
                       'DEPENDENCIES\n', 'BUNDLED WITH\n   1\nBUNDLED WITH\n   1\n'):
            with self.subTest(suffix=suffix):
                self.assertIsInstance(parse_lockfile(EMPTY + suffix), LockParseFailure)
        self.assertIsInstance(parse_lockfile(EMPTY + '  rack\n  rack\n'), LockParseFailure)
