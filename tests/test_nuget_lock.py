"""Offline whole-lock framing and F2 witnesses; no dependency association."""

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from libyears.nuget_input import (
    LocalInput, NuGetInputFailure, MAX_LOCK_ENTRIES, MAX_STRING_LENGTH,
)
from libyears.nuget_lock import parse_lock
from libyears.nuget_project import parse_project
from libyears.nuget_version import MAX_COMPONENT_DIGITS, MAX_VERSION_LENGTH


def direct(**changes):
    value = {'type': 'Direct', 'requested': '[1.0.0, )',
             'resolved': '2.0.0', 'contentHash': 'not-yet-validated'}
    value.update(changes)
    return value


def lock(packages=None):
    return {'version': 1, 'dependencies': {'net10.0': packages or {}}}


def parse(value):
    text = value if isinstance(value, str) else json.dumps(value)
    return parse_lock(LocalInput(text.encode('utf-8'), text))


class NuGetLockTests(unittest.TestCase):
    def rejected(self, value, category='malformed'):
        with self.assertRaises(NuGetInputFailure) as caught:
            parse(value)
        self.assertEqual(caught.exception.category, category)
        self.assertFalse(hasattr(caught.exception, 'entries'))
        return str(caught.exception)

    def test_schema_one_fixture_retains_closure_without_population(self):
        path = Path(__file__).parent / 'fixtures/nuget/lock-v1.json'
        snapshot = parse(path.read_text())
        self.assertEqual(snapshot.framework, 'net10.0')
        self.assertEqual([entry.kind for entry in snapshot.entries],
                         ['Direct', 'Transitive', 'Project'])
        entry = snapshot.entries[0]
        self.assertEqual((entry.package_name, entry.package_key), ('Example', 'example'))
        self.assertEqual((entry.requested, entry.resolved), ('[1.0.0, )', '2.0.0'))
        self.assertEqual(entry.dependencies, (('Helper', '[2.0.0, )'),))
        self.assertFalse(hasattr(snapshot, 'declarations'))
        for record in (snapshot, entry):
            with self.assertRaises(FrozenInstanceError):
                record.framework = 'changed'

    def test_empty_framework_and_wrong_single_literal_are_retained(self):
        self.assertEqual(parse(lock()).entries, ())
        self.assertEqual(parse({'version': 1, 'dependencies': {'net9.0': {}}}).framework,
                         'net9.0')

    def test_schema_requires_integer_and_root_required_fields(self):
        for version in (True, False, None, '1', 1.0, [], {}):
            with self.subTest(version=version):
                self.rejected({'version': version, 'dependencies': {'net10.0': {}}})
        self.rejected({'dependencies': {'net10.0': {}}})
        self.rejected({'version': 1})
        self.rejected({'version': 2, 'dependencies': {'net10.0': {}}}, 'unsupported')

    def test_all_envelope_and_entry_containers_have_strict_types(self):
        for value in ([], None, True, 'lock', 1):
            self.rejected(value if not isinstance(value, str) else json.dumps(value))
            self.rejected({'version': 1, 'dependencies': value})
            self.rejected({'version': 1, 'dependencies': {'net10.0': value}})
            self.rejected(lock({'Example': value}))

    def test_unknown_fields_and_kinds_are_unsupported(self):
        value = lock()
        value['unknown'] = 1
        self.rejected(value, 'unsupported')
        for kind in ('Direct', 'Transitive', 'Project'):
            entry = direct(type=kind, unknown=True)
            self.rejected(lock({'Example': entry}), 'unsupported')
        self.rejected(lock({'Example': {'type': 'Future'}}), 'unsupported')
        for kind in (None, 1, True, [], {}):
            self.rejected(lock({'Example': {'type': kind}}))
        self.rejected(lock({'Example': {}}))

    def test_project_and_transitive_do_not_accept_direct_only_fields(self):
        self.rejected(lock({'Example': {'type': 'Project', 'resolved': '1.0.0'}}),
                      'unsupported')
        self.rejected(lock({'Example': direct(type='Transitive')}), 'unsupported')

    def test_direct_requested_is_required_string(self):
        entry = direct()
        del entry['requested']
        self.rejected(lock({'Example': entry}))
        for value in (None, 1, True, [], {}):
            self.rejected(lock({'Example': direct(requested=value)}))

    def test_missing_direct_selection_and_hash_are_retained_for_later_failure(self):
        entry, = parse(lock({'Example': {'type': 'Direct', 'requested': '[1.0.0, )'}})).entries
        self.assertIsNone(entry.resolved)
        self.assertIsNone(entry.content_hash)

    def test_transitive_requires_selection_and_hash(self):
        for entry in ({'type': 'Transitive'},
                      {'type': 'Transitive', 'resolved': '1.0.0'},
                      {'type': 'Transitive', 'contentHash': 'hash'}):
            self.rejected(lock({'Example': entry}))

    def test_present_nonstring_selection_and_hash_reject_whole_lock(self):
        for field in ('resolved', 'contentHash'):
            for value in (None, True, 1, [], ['1.0.0'], {}, {'version': '1.0.0'}):
                with self.subTest(field=field, value=value):
                    self.rejected(lock({'Good': direct(), 'Bad': direct(**{field: value})}))

    def test_arbitrary_string_interpretation_is_deferred(self):
        for field in ('requested', 'resolved', 'contentHash'):
            for value in ('', 'unsupported syntax', 'secret\ncanary'):
                entry, = parse(lock({'Example': direct(**{field: value})})).entries
                attribute = 'content_hash' if field == 'contentHash' else field
                self.assertEqual(getattr(entry, attribute), value)

    def test_dependency_maps_validate_id_string_pairs_for_every_kind(self):
        for kind in ('Direct', 'Transitive', 'Project'):
            base = {'type': kind} if kind == 'Project' else direct(type=kind)
            if kind == 'Transitive':
                del base['requested']
            for dependencies in (None, [], 'x', {'Helper': None}, {'Helper': {}},
                                 {'Helper': '1', 'helper': '2'}, {'bad/id': '1'}):
                self.rejected(lock({'Example': dict(base, dependencies=dependencies)}))
            entry, = parse(lock({'Example': dict(base, dependencies={'Helper': 'any range'})})).entries
            self.assertEqual(entry.dependencies, (('Helper', 'any range'),))

    def test_invalid_and_case_aliased_package_ids_are_malformed(self):
        for name in ('', '.Example', 'bad/id', 'a b', 'é', 'a' * 101):
            self.rejected(lock({name: direct()}))
        self.rejected(lock({'Example': direct(), 'example': direct()}))
        self.assertEqual(parse(lock({'A' * 100: direct()})).entries[0].package_key, 'a' * 100)

    def test_repeated_keys_at_every_level_reject_whole_lock(self):
        cases = [
            '{"version":1,"version":1,"dependencies":{"net10.0":{}}}',
            '{"version":1,"dependencies":{"net10.0":{},"net10.0":{}}}',
            '{"version":1,"dependencies":{"net10.0":{"A":{"type":"Project"},"A":{"type":"Project"}}}}',
            '{"version":1,"dependencies":{"net10.0":{"A":{"type":"Direct","requested":"[1.0.0, )","resolved":"1.0.0","resolved":"2.0.0"}}}}',
            '{"version":1,"dependencies":{"net10.0":{"A":{"type":"Project","dependencies":{"B":"1","B":"2"}}}}}',
        ]
        for text in cases:
            self.rejected(text)

    def test_extra_empty_and_rid_contexts_are_unsupported(self):
        for contexts in ({}, {'net10.0': {}, 'net9.0': {}},
                         {'net10.0/linux-x64': {}}, {'': {}}, {'net 10': {}}):
            self.rejected({'version': 1, 'dependencies': contexts}, 'unsupported')

    def test_malformed_wins_over_unsupported_in_every_object_order(self):
        for contexts in ({'net10.0': {}, 'net9.0': {'Bad': direct(resolved=None)}},
                         {'net9.0': {'Bad': direct(resolved=None)}, 'net10.0': {}}):
            value = {'unknown': True, 'version': 2, 'dependencies': contexts}
            for ordered in (value, dict(reversed(list(value.items())))):
                self.rejected(ordered)
        for packages in ({'Unsupported': {'type': 'Future'}, 'Bad': direct(resolved=[])},
                         {'Bad': direct(resolved=[]), 'Unsupported': {'type': 'Future'}}):
            self.rejected(lock(packages))

    def test_invalid_json_utf8_and_safe_error(self):
        for text in ('', '{', '<<<<<<< conflict', '{"private-canary": NaN}', '{} trailing'):
            self.assertNotIn('private-canary', self.rejected(text))
        with self.assertRaises(NuGetInputFailure) as caught:
            parse_lock(LocalInput(b'\xff', 'safe'))
        self.assertEqual(caught.exception.category, 'malformed')

    def test_rejection_does_not_change_independently_known_population(self):
        text = ('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>'
                '<TargetFramework>net10.0</TargetFramework></PropertyGroup>'
                '<ItemGroup><PackageReference Include="Example" Version="1.0"/>'
                '</ItemGroup></Project>')
        context = parse_project(LocalInput(text.encode(), text))
        self.rejected(lock({'Example': direct(resolved=None)}))
        self.assertEqual(len(context.declarations), 1)
        self.assertEqual(context.declarations[0].package_name, 'Example')

    def test_entry_count_boundary_includes_all_contexts(self):
        with patch('libyears.nuget_lock.MAX_LOCK_ENTRIES', 2):
            self.assertEqual(len(parse(lock({'A': {'type': 'Project'},
                                            'B': {'type': 'Project'}})).entries), 2)
            self.rejected(lock({name: {'type': 'Project'} for name in ('A', 'B', 'C')}), 'limit')
            self.rejected({'version': 1, 'dependencies': {
                'net10.0': {'A': {'type': 'Project'}},
                'net9.0': {'B': {'type': 'Project'}, 'C': {'type': 'Project'}}}}, 'limit')

    def test_actual_entry_count_cap_and_cap_plus_one(self):
        packages = {f'Package{index}': {'type': 'Project'}
                    for index in range(MAX_LOCK_ENTRIES)}
        self.assertEqual(len(parse(lock(packages)).entries), MAX_LOCK_ENTRIES)
        packages['OneTooMany'] = {'type': 'Project'}
        self.rejected(lock(packages), 'limit')

    def test_general_string_and_framework_length_boundaries(self):
        self.assertEqual(parse(lock({'Example': direct(contentHash='x' * MAX_STRING_LENGTH)}))
                         .entries[0].content_hash, 'x' * MAX_STRING_LENGTH)
        self.rejected(lock({'Example': direct(contentHash='x' * (MAX_STRING_LENGTH + 1))}), 'limit')
        self.assertEqual(parse({'version': 1, 'dependencies': {'n' * 128: {}}}).framework,
                         'n' * 128)
        self.rejected({'version': 1, 'dependencies': {'n' * 129: {}}}, 'limit')

    def test_version_bounds_cover_direct_transitive_and_all_closure_requests(self):
        at_cap = ('1.2+' + 'a' * (MAX_VERSION_LENGTH - 4),
                  '1.' + '9' * MAX_COMPONENT_DIGITS)
        over_cap = ('1.2+' + 'a' * (MAX_VERSION_LENGTH - 3),
                    '1.' + '9' * (MAX_COMPONENT_DIGITS + 1))
        fields_by_kind = {
            'Direct': ('requested', 'resolved', 'dependencies'),
            'Transitive': ('resolved', 'dependencies'),
            'Project': ('dependencies',),
        }
        for kind, fields in fields_by_kind.items():
            for field in fields:
                for text in at_cap + over_cap:
                    with self.subTest(kind=kind, field=field, text=text):
                        entry = {'type': kind}
                        if kind != 'Project':
                            entry.update(resolved='1.0.0', contentHash='hash')
                        if kind == 'Direct':
                            entry['requested'] = '[1.0.0, )'
                        entry[field] = {'Helper': text} if field == 'dependencies' else text
                        value = lock({'Example': entry})
                        if text in at_cap:
                            self.assertEqual(len(parse(value).entries), 1)
                        else:
                            self.rejected(value, 'unsupported')

    def test_component_bound_applies_inside_requested_ranges(self):
        for digits in (MAX_COMPONENT_DIGITS, MAX_COMPONENT_DIGITS + 1):
            request = '[1.' + '9' * digits + '.0, 2.0.0)'
            value = lock({'Example': direct(requested=request)})
            if digits == MAX_COMPONENT_DIGITS:
                self.assertEqual(parse(value).entries[0].requested, request)
            else:
                self.rejected(value, 'unsupported')

    def test_version_overflow_does_not_mask_malformed_structure_in_any_order(self):
        oversized = direct(resolved='1.' + '9' * 33)
        malformed = direct(resolved=None)
        for packages in ({'Oversized': oversized, 'Bad': malformed},
                         {'Bad': malformed, 'Oversized': oversized}):
            self.rejected(lock(packages))
        for contexts in ({'net10.0': {'Oversized': oversized}, 'net9.0': {'Bad': malformed}},
                         {'net9.0': {'Bad': malformed}, 'net10.0': {'Oversized': oversized}}):
            self.rejected({'version': 1, 'dependencies': contexts})

    def test_byte_limit_uses_exact_bytes_and_does_not_trust_cached_text(self):
        data = json.dumps(lock()).encode()
        with patch('libyears.nuget_lock.MAX_LOCK_BYTES', len(data)):
            self.assertEqual(parse_lock(LocalInput(data, 'not json')).entries, ())
            with self.assertRaises(NuGetInputFailure) as caught:
                parse_lock(LocalInput(data + b' ', 'not json'))
            self.assertEqual(caught.exception.category, 'limit')


if __name__ == '__main__':
    unittest.main()
