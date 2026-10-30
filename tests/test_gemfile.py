"""The static Gemfile subset is exhaustive, not general Ruby interpretation."""

from dataclasses import FrozenInstanceError
from pathlib import Path
import unittest
from unittest.mock import patch

from libyears.gemfile import (
    GemfileParseFailure, MAX_GEMFILE_LINE_BYTES, ParsedGemfile, parse_gemfile,
    supported_name, supported_requirement,
)


SOURCE = 'source "https://rubygems.org"\n'
FIXTURES = Path(__file__).parent / 'fixtures' / 'ruby_groups'


class GemfileParserTests(unittest.TestCase):
    def accepted(self, text):
        result = parse_gemfile(text)
        self.assertIsInstance(result, ParsedGemfile)
        return result

    def rejected(self, text, reason, line=None):
        result = parse_gemfile(text)
        self.assertIsInstance(result, GemfileParseFailure)
        self.assertEqual(result.reason, reason)
        self.assertEqual(result.line, line)
        self.assertFalse(hasattr(result, 'declarations'))
        return result

    def test_all_literal_and_require_options_preserve_requirements(self):
        for quote in ("'", '"'):
            for option in ('', ', require: true', ', require: false',
                           ', require: "rack/core#loader"', ", require: 'rack/core'"):
                with self.subTest(quote=quote, option=option):
                    text = SOURCE + f'gem {quote}rack{quote}, {quote} >= 1.0 {quote}, {quote}< 3{quote}' + option
                    row = self.accepted(text).declarations[0]
                    self.assertEqual(row.name, 'rack')
                    self.assertEqual(row.requirements, (' >= 1.0 ', '< 3'))
                    self.assertEqual(row.declared_groups, ('default',))
                    self.assertEqual(row.line, 2)

    def test_single_literal_can_retain_multiple_requirement_terms(self):
        row = self.accepted(SOURCE + 'gem "rack", ">= 1, < 3"').declarations[0]
        self.assertEqual(row.requirements, ('>= 1, < 3',))

    def test_all_group_option_forms_and_orderings(self):
        for key in ('group', 'groups'):
            for value, expected in ((':test', ('test',)),
                                    ('[:test]', ('test',)),
                                    ('[:test, :default, :test]', ('default', 'test'))):
                for require_first in (False, True):
                    options = f'{key}: {value}, require: false'
                    if require_first:
                        options = f'require: true, {key}: {value}'
                    with self.subTest(key=key, value=value, first=require_first):
                        result = self.accepted(SOURCE + 'gem "rack", ' + options)
                        self.assertEqual(result.declarations[0].declared_groups, expected)
                        self.assertEqual(result.established_groups, tuple(sorted({'default', *expected})))

    def test_block_membership_unions_and_optional_flags(self):
        for optional in ('', ', optional: true', ', optional: false'):
            with self.subTest(optional=optional):
                result = self.accepted(SOURCE + 'group :test, :development' + optional + ' do\n'
                                       ' gem "rack", groups: [:test, :bench], require: false\nend')
                self.assertEqual(result.declarations[0].declared_groups,
                                 ('bench', 'development', 'test'))
                self.assertEqual(result.established_groups,
                                 ('bench', 'default', 'development', 'test'))

    def test_empty_blocks_and_empty_implicit_default_are_established(self):
        result = self.accepted(SOURCE + 'group :bench do\n # empty\nend')
        self.assertEqual(result.declarations, ())
        self.assertEqual(result.established_groups, ('bench', 'default'))
        self.assertEqual(self.accepted(SOURCE).established_groups, ('default',))

    def test_explicit_default_group_is_an_ordinary_membership(self):
        result = self.accepted(SOURCE + 'group :default, :production do\n'
                               'gem "rack", group: :test\nend\ngem "rake", group: :production')
        self.assertEqual(result.declarations[0].declared_groups, ('default', 'production', 'test'))
        self.assertEqual(result.declarations[1].declared_groups, ('production',))

    def test_exact_name_and_group_case_and_punctuation(self):
        result = self.accepted(SOURCE + 'gem "Rack", groups: [:Test, :_custom_2]\n'
                               'gem "rack", group: :test\ngem "a.b-c_d2"')
        self.assertEqual([row.name for row in result.declarations], ['Rack', 'rack', 'a.b-c_d2'])
        self.assertEqual(result.established_groups, ('Test', '_custom_2', 'default', 'test'))

    def test_whitespace_comments_lf_crlf_and_no_final_newline(self):
        text = '\t# heading\n\n  source\t"https://rubygems.org/" # authority\n'
        text += '\tgroup\t:test, :Test, optional: false do # group\n'
        text += '\tgem\t"rack",require: "# inert, not a comment" # declaration\n end # done'
        for newline in ('\n', '\r\n'):
            for suffix in ('', newline):
                with self.subTest(newline=newline, suffix=suffix):
                    result = self.accepted(text.replace('\n', newline) + suffix)
                    self.assertEqual(result.declarations[0].line, 5)
                    self.assertEqual(result.declarations[0].declared_groups, ('Test', 'test'))

    def test_only_exact_public_authority_is_retained_and_raw_source_is_discarded(self):
        for source, public in (
            ('https://rubygems.org', True), ('https://rubygems.org/', True),
            ('http://rubygems.org', False), ('https://RUBYGEMS.org', False),
            ('https://rubygems.org//', False), ('', False),
            ('https://user:PRIVATE_MARKER@example.invalid/#fragment', False),
        ):
            with self.subTest(source=source):
                result = self.accepted(f'source "{source}"\ngem "rack"')
                self.assertEqual(result.public_source_authorized, public)
                self.assertNotIn('PRIVATE_MARKER', repr(result))
                self.assertFalse(hasattr(result, 'source'))
        self.assertTrue(self.accepted("source 'https://rubygems.org' # public").public_source_authorized)

    def test_source_may_follow_declarations_but_must_be_top_level(self):
        result = self.accepted('gem "rack"\n' + SOURCE)
        self.assertEqual(result.declarations[0].line, 1)
        self.rejected(SOURCE + 'group :test do\nsource "https://rubygems.org"\nend',
                      'unsupported_gemfile_syntax', 3)

    def test_unsupported_statement_families_never_return_partial_scope(self):
        statements = (
            'if true', 'unless false', 'else', 'x = 1', '@x = 1', '$x = 1',
            'def gems', 'while true', 'for x in []', 'loop do', 'puts "hello"',
            'platforms :ruby do', 'platform :ruby do', 'install_if true do',
            'eval_gemfile "other"', 'gemspec', 'ruby "3.3.0"',
            'path "vendor" do', 'git "https://example.invalid" do',
            'BEGIN { puts "hello" }', '=begin', '__END__',
        )
        for statement in statements:
            with self.subTest(statement=statement):
                self.rejected(SOURCE + 'gem "rack"\n' + statement,
                              'unsupported_gemfile_syntax', 3)

    def test_unsupported_calls_options_expressions_and_trailing_tokens(self):
        statements = (
            'gem("rack")', 'source("https://rubygems.org")',
            'gem "rack"; gem "rake"', 'gem "rack" \\',
            'gem "rack" if true', 'gem "rack" extra', 'end; puts "bad"',
            'source "https://rubygems.org" do', 'source "x", "y"',
            'gem name', 'gem "rack", requirement',
            'gem "rack", path: "vendor"', 'gem "rack", git: "url"',
            'gem "rack", platforms: :ruby', 'gem "rack", unknown: false',
            'gem "rack", require: loader', 'gem "rack", require: nil',
            'gem "rack", group: selected', 'gem "rack", groups: %i[test]',
            'gem "rack", **options', 'group :test, optional: flag do',
            'group :test, unknown: true do',
        )
        for statement in statements:
            with self.subTest(statement=statement):
                result = parse_gemfile(SOURCE + statement)
                self.assertIsInstance(result, GemfileParseFailure)
                self.assertEqual(result.reason, 'unsupported_gemfile_syntax')
                self.assertEqual(result.line, 2)

    def test_malformed_recognized_forms(self):
        statements = (
            'source', 'source # missing value', 'source "unterminated',
            'gem', 'gem # missing name', 'gem "rack', 'gem "rack",',
            'gem "rack", group: []', 'gem "rack", group: [:test,]',
            'gem "rack", group: [:test', 'gem "rack", group: :',
            'gem "rack", group: :2test', 'gem "rack", group : :test',
            'gem "rack", require : true', 'group', 'group :', 'group :test',
            'group :test, optional true do',
        )
        for statement in statements:
            with self.subTest(statement=statement):
                result = parse_gemfile(SOURCE + statement)
                self.assertIsInstance(result, GemfileParseFailure)
                self.assertEqual(result.reason, 'invalid_gemfile')
                self.assertEqual(result.line, 2)

    def test_boolean_and_literal_option_boundaries(self):
        for statement in (
            'gem "rack", require: true_extra', 'gem "rack", require: false()',
            'gem "rack", require: "loader".call', 'gem "rack", require: 1',
            'group :test, optional: true_extra do', 'group :test, optional: do',
            'group :test, optional: "true" do',
        ):
            with self.subTest(statement=statement):
                self.rejected(SOURCE + statement, 'unsupported_gemfile_syntax', 2)

    def test_repeated_options_and_requirements_after_options_reject(self):
        for options in ('group: :test, group: :test', 'groups: :test, groups: :test',
                        'group: :test, groups: :test', 'groups: :test, group: :test',
                        'require: true, require: false', 'require: true, ">= 0"'):
            with self.subTest(options=options):
                self.rejected(SOURCE + 'gem "rack", ' + options, 'invalid_gemfile', 2)

    def test_literals_reject_escapes_interpolation_and_newlines(self):
        for literal in ('"ra\\ck"', '"ra#{code}ck"', '"ra#@code"', '"ra#$code"',
                        "'ra\\ck'", "'ra#{code}ck'"):
            for prefix in ('source ', 'gem "rack", require: '):
                with self.subTest(literal=literal, prefix=prefix):
                    self.rejected(SOURCE + prefix + literal, 'unsupported_gemfile_syntax', 2)
        self.rejected(SOURCE + 'gem "ra\nck"', 'invalid_gemfile', 2)

    def test_unsupported_identity_and_requirement_framing_reject_scope(self):
        for name in ('', '123', '-rack', 'rack-', 'rack/name', 'r ack', 'räck'):
            with self.subTest(name=name):
                self.rejected(SOURCE + f'gem "{name}"', 'unsupported_gemfile_syntax', 2)
        for requirement in ('', '*', 'latest', '>=', '>= 1 || < 3', '1 (unsafe)', '1,,2'):
            with self.subTest(requirement=requirement):
                self.rejected(SOURCE + f'gem "rack", "{requirement}"',
                              'unsupported_gemfile_syntax', 2)

    def test_duplicates_anywhere_reject_without_merging(self):
        for second in ('gem "rack"', 'gem "rack", ">= 2"',
                       'group :test do\ngem "rack"\nend'):
            with self.subTest(second=second):
                line = 4 if second.startswith('group') else 3
                self.rejected(SOURCE + 'gem "rack"\n' + second,
                              'duplicate_gemfile_declaration', line)

    def test_nested_blocks_and_unselected_code_reject(self):
        self.rejected(SOURCE + 'group :unselected do\ngroup :nested do\nend\nend',
                      'unsupported_gemfile_syntax', 3)
        self.rejected(SOURCE + 'group :unselected do\neval_gemfile "other"\nend',
                      'unsupported_gemfile_syntax', 3)

    def test_first_physical_line_defect_precedes_completion_defects(self):
        self.rejected('group :test do\ngem "rack"\nputs "bad"\ngem "rack"',
                      'unsupported_gemfile_syntax', 3)
        self.rejected('gem "rack"\ngem "rack"\nputs "bad"',
                      'duplicate_gemfile_declaration', 2)
        self.rejected(SOURCE + 'source "other"\nputs "bad"', 'invalid_gemfile', 2)
        self.rejected('end\nputs "bad"', 'invalid_gemfile', 1)
        self.rejected('gem "rack"', 'invalid_gemfile')
        self.rejected(SOURCE + 'group :test do', 'invalid_gemfile')

    def test_control_and_nonphysical_line_separator_rejection(self):
        for control in ('\r', '\x00', '\v', '\f', '\x1b', '\x7f', '\x85', '\u2028', '\u2029'):
            with self.subTest(control=control):
                self.rejected(SOURCE + '# comment' + control, 'invalid_gemfile', 2)

    def test_physical_line_byte_limit_exact_one_over_and_crlf(self):
        for newline in ('\n', '\r\n'):
            line = '#' + 'x' * (MAX_GEMFILE_LINE_BYTES - 1)
            self.accepted(SOURCE + line + newline)
            self.rejected(SOURCE + line + 'x' + newline, 'unsupported_gemfile_syntax', 2)
        # UTF-8 bytes, rather than code points, establish the boundary.
        line = '#' + 'é' * ((MAX_GEMFILE_LINE_BYTES - 2) // 2) + 'x'
        self.assertEqual(len(line.encode('utf-8')), MAX_GEMFILE_LINE_BYTES)
        self.accepted(SOURCE + line)
        self.rejected(SOURCE + line + 'é', 'unsupported_gemfile_syntax', 2)
        self.rejected('puts "bad"\n' + line + 'x', 'unsupported_gemfile_syntax', 1)

    def test_records_are_immutable_and_failures_retain_only_safe_categories(self):
        result = self.accepted(SOURCE + 'gem "rack"')
        for record, field in ((result, 'declarations'), (result.declarations[0], 'name')):
            with self.assertRaises(FrozenInstanceError):
                setattr(record, field, None)
        failure = self.rejected(SOURCE + 'gem "rack", git: "UNSAFE_MARKER"',
                                'unsupported_gemfile_syntax', 2)
        self.assertNotIn('UNSAFE_MARKER', repr(failure))
        with self.assertRaises(FrozenInstanceError):
            failure.reason = 'changed'

    def test_parser_does_not_access_files_network_or_execute_code(self):
        with patch('builtins.open', side_effect=AssertionError('filesystem access')), \
             patch('socket.socket', side_effect=AssertionError('network access')), \
             patch('subprocess.run', side_effect=AssertionError('execution')), \
             patch('builtins.eval', side_effect=AssertionError('evaluation')), \
             patch('builtins.exec', side_effect=AssertionError('execution')):
            self.accepted(SOURCE + 'gem "rack"')
            self.rejected(SOURCE + 'eval_gemfile "other"', 'unsupported_gemfile_syntax', 2)

    def test_annotated_fixtures(self):
        result = self.accepted((FIXTURES / 'memberships.Gemfile').read_text(encoding='utf-8'))
        self.assertEqual([(row.name, row.declared_groups) for row in result.declarations], [
            ('rack', ('default',)), ('rake', ('development', 'test')),
            ('debug', ('Test', 'development', 'test')),
        ])
        self.assertEqual(result.established_groups, ('Test', 'bench', 'default', 'development', 'test'))
        self.rejected((FIXTURES / 'duplicate.Gemfile').read_text(encoding='utf-8'),
                      'duplicate_gemfile_declaration', 5)
        self.rejected((FIXTURES / 'unsupported.Gemfile').read_text(encoding='utf-8'),
                      'unsupported_gemfile_syntax', 5)


class RubyFramingValidatorTests(unittest.TestCase):
    def test_existing_name_and_requirement_framing(self):
        for name in ('rack', 'Rack', 'a.b-c_d', '2fa'):
            self.assertTrue(supported_name(name), name)
        for name in ('', '123', '-rack', 'rack-', 'rack/name', 'räck'):
            self.assertFalse(supported_name(name), name)
        for requirement in (None, '1', '>= 1.0', '<= 3', '~> 1.0', '!= 2', '=1', '>1', '<3',
                            '>= 1, < 3', ' 1.0.rc1 ', '\t>= 1\t'):
            self.assertTrue(supported_requirement(requirement), requirement)
        for requirement in ('', '*', 'latest', '>=', '>= 1 || < 3', '1,,2'):
            self.assertFalse(supported_requirement(requirement), requirement)


if __name__ == '__main__':
    unittest.main()
