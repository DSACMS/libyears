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


class SourceEnvelopeTests(unittest.TestCase):
    def test_repeated_sources_preserve_metadata_and_duplicate_specs(self):
        source = ('GEM\n  remote: https://rubygems.org\n  remote: private-value\n'
                  '  specs:\n    rack (unsupported+selection)\n'
                  '      child (arbitrary || requirement)\n      bare\n')
        result = parse_lockfile(source + EMPTY)
        self.assertIsInstance(result, ParsedGemfileLock)
        self.assertEqual(len(result.sources), 2)
        self.assertEqual(result.sources[0].metadata,
                         (('remote', 'https://rubygems.org'), ('remote', 'private-value')))
        self.assertEqual(result.sources[0].specs[0].raw_selection, 'unsupported+selection')
        self.assertEqual(result.sources[0].specs[0].source_index, 0)
        self.assertEqual(result.dependencies, ())

    def test_git_path_allowlists_and_ownership(self):
        git = ('GIT\n  remote: inert-private\n  revision: abc\n  branch: main\n'
               '  ref: ref\n  tag: tag\n  submodules: true\n  glob: *.gemspec\n'
               '  specs:\n    rack (1)\n      child (~> 1)\n')
        path = 'PATH\n  remote: ../inert\n  specs:\n    rack (2)\n'
        result = parse_lockfile(EMPTY + git + path)
        self.assertIsInstance(result, ParsedGemfileLock)
        self.assertEqual([s.kind for s in result.sources], ['GEM', 'GIT', 'PATH'])
        self.assertEqual([s.specs[0].source_index for s in result.sources[1:]], [1, 2])
        for kind in ('GIT', 'PATH'):
            text = f'{kind}\n  remote: one\n  remote: two\n  specs:\n'
            self.assertIsInstance(parse_lockfile(EMPTY + text), LockParseFailure)

    def test_unsafe_source_and_nested_framing(self):
        for body in ('      orphan\n', '    rack (1)\n      child (>= 1\n',
                     '    rack (1)\n      child ((1))\n',
                     '    rack (1)\n      child (1) trailing\n',
                     '    rack (1) trailing\n', '     rack (1)\n',
                     '    rack (1)\n       child\n', '    rack (1)\n      child!\n',
                     '  remote: misplaced\n', '  specs:\n', '\tchild\n'):
            with self.subTest(body=body):
                result = parse_lockfile(EMPTY + 'GEM\n  specs:\n' + body)
                self.assertIsInstance(result, LockParseFailure)
                self.assertEqual(result.reason, 'invalid_lockfile')

    def test_nested_requirements_are_inert(self):
        for requirement in ('>= 1', 'unsupported || syntax', '', '!= 1, < 2'):
            text = EMPTY.replace('  specs:', '  specs:\n    rack (1)\n'
                                 f'      child ({requirement})')
            result = parse_lockfile(text)
            self.assertIsInstance(result, ParsedGemfileLock)
            self.assertEqual(result.dependencies, ())


class RejectionTests(unittest.TestCase):
    def assert_rejected(self, text, reason):
        result = parse_lockfile(text)
        self.assertIsInstance(result, LockParseFailure)
        self.assertEqual(result.reason, reason)
        self.assertFalse(hasattr(result, 'dependencies'))
        self.assertFalse(hasattr(result, 'sources'))
        return result

    def test_unclassifiable_and_unsupported_sections(self):
        for text in ('', ' \n', 'arbitrary text', '  arbitrary text',
                     'UNKNOWN\n  value\n'):
            with self.subTest(text=text):
                self.assert_rejected(text, 'unsupported_lockfile_format')
        for heading in ('CHECKSUMS', 'CONTENT ADDRESSES', 'PLUGIN SOURCE', 'UNKNOWN'):
            for text in (heading + '\n  opaque\n' + EMPTY, EMPTY + heading + '\n  opaque\n'):
                self.assert_rejected(text, 'unsupported_lockfile_format')

    def test_unknown_source_fields_are_unsupported(self):
        for kind in ('GEM', 'GIT', 'PATH'):
            text = EMPTY + f'{kind}\n  future: private-secret\n  specs:\n'
            result = self.assert_rejected(text, 'unsupported_lockfile_format')
            self.assertNotIn('private-secret', repr(result))
        self.assert_rejected(EMPTY + 'PATH\n  branch: main\n  specs:\n',
                             'unsupported_lockfile_format')

    def test_malformed_wins_over_unsupported_in_both_orders(self):
        unsupported = ('CHECKSUMS\n  opaque\n',
                       'GEM\n  future: secret\n  specs:\n')
        malformed = ('DEPENDENCIES\n  rack\n  rack\n',
                     'GEM\n  specs:\n      orphan\n',
                     'GEM\n  specs:\n    rack (1\n',
                     'PLATFORMS\n', 'BUNDLED WITH\n',
                     '<<<<<<< secret\n', '\t\n')
        for extra in unsupported:
            for broken in malformed:
                for text in (EMPTY + extra + broken, EMPTY + broken + extra):
                    with self.subTest(extra=extra, broken=broken):
                        self.assert_rejected(text, 'invalid_lockfile')
        self.assert_rejected(EMPTY + 'GEM\n  future: secret\n  specs:\n      orphan\n',
                             'invalid_lockfile')

    def test_missing_required_structure_and_unsafe_identity(self):
        for text in ('GEM\n  specs:\n', 'DEPENDENCIES\n', 'PLATFORMS\n  ruby\n',
                     EMPTY + '  two names\n', EMPTY + '  (>= 1)\n',
                     EMPTY + '  rack (1) trailing\n', EMPTY + 'trailing syntax\n',
                     EMPTY + '=======\n', EMPTY + '>>>>>>> secret\n',
                     EMPTY + '  rack\r\n  bad\rtext\n'):
            with self.subTest(text=text):
                self.assert_rejected(text, 'invalid_lockfile')

    def test_failure_context_cannot_disclose_unknown_headings_or_values(self):
        for text in (EMPTY + 'PRIVATE SECRET\n  token\n',
                     EMPTY + 'GEM\n  specs:\n    secret (1) trailing\n'):
            result = parse_lockfile(text)
            self.assertNotIn('secret', repr(result).lower())
            self.assertTrue(result.section is None or result.section == 'GEM')

    def test_isolated_unsupported_identities_remain_for_matching(self):
        text = EMPTY.replace('  specs:', '  specs:\n    Odd/Name (1+unsupported)')
        result = parse_lockfile(text + '  Odd/Name (unsupported || expression)\n')
        self.assertIsInstance(result, ParsedGemfileLock)
        self.assertEqual(result.dependencies[0].name, 'Odd/Name')
        self.assertEqual(result.dependencies[0].requirement_text, 'unsupported || expression')
        self.assertEqual(result.sources[0].specs[0].raw_selection, '1+unsupported')
