import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from libyears.gemfile_lock import ParsedGemfileLock, parse_lockfile
from libyears.rubygems import authorize_public_selection, match_lock_dependencies

from libyears.model import (
    Dependency, DependencyCandidate, RegistryFailure, RegistryResult,
    RubyGemsEvidence, RubyPublicationArtifact, SelectedRubyArtifact,
    SourceEvidence, UnmeasurableDependency,
)


class RubyEvidenceTests(unittest.TestCase):
    def test_existing_positional_constructors_default_to_no_ruby_evidence(self):
        time = datetime(2024, 1, 1, tzinfo=timezone.utc)
        records = (
            Dependency('pypi', 'a', '1', time, '2', time, 'resolved_snapshot'),
            DependencyCandidate('npm', 'a', 'a', 'a', '1', 'package_lock'),
            UnmeasurableDependency('npm', 'a', 'a', 'lock_version_missing'),
            RegistryResult('a', '1', time, '2', time),
            RegistryFailure('a', '1', 'registry_error', 'safe detail'),
        )
        for record in records:
            with self.subTest(record=type(record).__name__):
                self.assertIsNone(record.rubygems_evidence)
        source = SourceEvidence('package.json', 'yarn.lock', 'yarn_lock_v1', True)
        self.assertIsNone(source.scope)
        self.assertIsNone(source.publication_basis)

    def test_typed_evidence_preserves_optional_publication_and_normalizes_time(self):
        selected = SelectedRubyArtifact('1', 'ruby', 'https://rubygems.org')
        evidence = RubyGemsEvidence((selected,))
        self.assertIsNone(evidence.used_publication_artifacts)
        self.assertIsNone(evidence.latest_publication_artifacts)
        publication = RubyPublicationArtifact(
            '1', 'ruby', datetime(2024, 1, 1, 2, tzinfo=timezone(timedelta(hours=2))),
        )
        self.assertEqual(publication.publication_time,
                         datetime(2024, 1, 1, tzinfo=timezone.utc))
        self.assertIsNone(publication.yanked)
        with self.assertRaises(ValueError):
            RubyPublicationArtifact('1', 'ruby', datetime(2024, 1, 1))


def source_block(kind='GEM', remotes=('https://rubygems.org',), specs=('sample (1.0)',)):
    rows = [kind]
    rows.extend('  remote: ' + remote for remote in remotes)
    rows.append('  specs:')
    rows.extend('    ' + spec for spec in specs)
    return '\n'.join(rows) + '\n\n'


def parsed_lock(blocks=None, directs=('sample',)):
    text = source_block() if blocks is None else blocks
    text += 'PLATFORMS\n  ruby\n\nDEPENDENCIES\n'
    text += ''.join('  ' + direct + '\n' for direct in directs)
    lock = parse_lockfile(text)
    if not isinstance(lock, ParsedGemfileLock):
        raise AssertionError(lock)
    return lock


class PublicAuthorityTests(unittest.TestCase):
    def test_literal_public_sources_authorize_and_preserve_identity(self):
        for remote in ('https://rubygems.org', 'https://rubygems.org/'):
            lock = parsed_lock(source_block(remotes=(remote,)))
            result = authorize_public_selection(
                lock, lock.dependencies[0],
            )
            self.assertIsInstance(result, DependencyCandidate)
            self.assertEqual(result.registry_name, 'sample')
            self.assertEqual(result.version_source, 'gemfile_lock')

    def test_all_associations_and_pin_block_public_namesake_without_http(self):
        rejected = [
            source_block('GIT'), source_block('PATH'), source_block(remotes=()),
            source_block(remotes=('http://rubygems.org',)),
            source_block(remotes=('https://private.invalid/secret',)),
            source_block(remotes=('https://rubygems.org/custom',)),
            source_block(remotes=('https://user:secret@rubygems.org',)),
            source_block(remotes=('https://rubygems.org', 'https://rubygems.org')),
        ]
        with patch('urllib.request.urlopen', side_effect=AssertionError('HTTP prohibited')) as http:
            for block in rejected:
                for blocks in (block, block + source_block(), source_block() + block):
                    with self.subTest(block=block, blocks=blocks):
                        lock = parsed_lock(blocks)
                        result = authorize_public_selection(lock, lock.dependencies[0])
                        self.assertIsInstance(result, UnmeasurableDependency)
                        self.assertEqual(result.reason, 'unsupported_dependency_source')
                        self.assertNotIn('secret', repr(result))
            lock = parsed_lock(directs=('sample!',))
            self.assertEqual(authorize_public_selection(lock, lock.dependencies[0]).reason,
                             'unsupported_dependency_source')
            http.assert_not_called()

    def test_unrelated_private_source_does_not_taint_public_identity(self):
        lock = parsed_lock(source_block() + source_block('PATH', specs=('other (2)',)))
        result = authorize_public_selection(lock, lock.dependencies[0])
        self.assertIsInstance(result, DependencyCandidate)


class DirectMatchingTests(unittest.TestCase):
    def setUp(self):
        self.http = patch('urllib.request.urlopen', side_effect=AssertionError('HTTP prohibited'))
        self.request = self.http.start()
        self.addCleanup(self.http.stop)
        self.addCleanup(self.request.assert_not_called)

    def outcome(self, specs, direct='sample', blocks=None):
        lock = parsed_lock(source_block(specs=specs) if blocks is None else blocks, (direct,))
        return authorize_public_selection(lock, lock.dependencies[0])

    def test_names_preserve_case_and_punctuation_without_lock_normalization(self):
        for name in ('A', 'Sample', 'a-b', 'a_b', 'a.b', '1a2'):
            result = self.outcome((name + ' (1)',), name)
            self.assertEqual((result.name, result.registry_name), (name, name))
        for name in ('123', '_a', 'a-', 'a/b', 'a+b', 'sämple'):
            with self.subTest(name=name):
                self.assertEqual(self.outcome((name + ' (1)',), name).reason,
                                 'unsupported_dependency_name')
        for other in ('Sample', 'sam_ple', 'sam-ple'):
            self.assertEqual(self.outcome((other + ' (1)',)).reason, 'lock_version_missing')

    def test_requirements_are_retained_without_evaluation(self):
        for requirement in (None, '1', '= 9', '!= 1', '> 2', '< 0', '>= 9', '<= 0',
                            '~> 8.1', ' >= 9 , < 1, = 2, = 2 ', '1, 2', '1.pre.1'):
            direct = 'sample' if requirement is None else 'sample (' + requirement + ')'
            result = self.outcome(('sample (1.0)',), direct)
            self.assertIsInstance(result, DependencyCandidate)
            self.assertEqual(result.declared, direct)
            self.assertEqual(result.used_version, '1.0')
        for requirement in ('', '*', '=> 1', '1 || 2', '>= 1,', '1..2', 'latest'):
            self.assertEqual(self.outcome(('sample (1)',), 'sample (' + requirement + ')').reason,
                             'unsupported_requirement')

    def test_ordinary_platform_and_agreeing_variants(self):
        for selection, version, platform in (
            ('1', '1', 'ruby'), ('1.2.pre.1', '1.2.pre.1', 'ruby'),
            ('1.2-x86_64-linux-gnu', '1.2', 'x86_64-linux-gnu'),
        ):
            result = self.outcome(('sample (' + selection + ')',))
            self.assertEqual(result.used_version, version)
            self.assertEqual(result.rubygems_evidence.selected_artifacts,
                             (SelectedRubyArtifact(version, platform, 'https://rubygems.org'),))
        for blocks in (
            source_block(specs=('sample (1.0)', 'sample (1.0-java)')),
            source_block() + source_block(specs=('sample (1.0-java)',)),
        ):
            result = self.outcome((), blocks=blocks)
            self.assertEqual(result.used_version, '1.0')
            self.assertEqual(len(result.rubygems_evidence.selected_artifacts), 2)

    def test_duplicate_and_differing_artifacts_are_ambiguous_across_blocks(self):
        for second in ('sample (1.0)', 'sample (1.0-ruby)', 'sample (2.0-java)'):
            for blocks in (
                source_block(specs=('sample (1.0)', second)),
                source_block() + source_block(specs=(second,)),
            ):
                result = self.outcome((), blocks=blocks)
                self.assertEqual(result.reason, 'ambiguous_lock_evidence')
                self.assertEqual(len(result.rubygems_evidence.selected_artifacts), 2)

    def test_unsupported_selection_and_material_partial_evidence(self):
        for selection in ('v1', '1..2', '1-', '1.0 java', '1.0-java+abi', '1.0/abi'):
            result = self.outcome(('sample (' + selection + ')',))
            self.assertEqual(result.reason, 'unsupported_lock_evidence')
            self.assertIsNone(result.rubygems_evidence)
        result = self.outcome(('sample (1)', 'sample (unknown)'))
        self.assertEqual(result.reason, 'unsupported_lock_evidence')
        self.assertEqual(len(result.rubygems_evidence.selected_artifacts), 1)

    def test_special_directs_missing_specs_and_transitives(self):
        lock = parsed_lock(source_block(specs=('transitive (3)', '  nested (nonsense)')),
                           ('bundler (= 2.5)', 'tzinfo-data', 'sample (= 1)'))
        candidates, failures = match_lock_dependencies(lock)
        self.assertEqual(candidates, ())
        self.assertEqual([item.name for item in failures], ['bundler', 'tzinfo-data', 'sample'])
        self.assertEqual([item.reason for item in failures], ['lock_version_missing'] * 3)

    def test_local_precedence_is_independent_of_occurrence_order(self):
        for specs in (
            ('sample (1)', 'sample (2)', 'sample (unknown)'),
            ('sample (unknown)', 'sample (2)', 'sample (1)'),
        ):
            self.assertEqual(self.outcome(specs).reason, 'ambiguous_lock_evidence')
            private = source_block('PATH', specs=specs)
            public = source_block(specs=specs)
            for blocks in (private + public, public + private):
                self.assertEqual(self.outcome((), blocks=blocks).reason,
                                 'unsupported_dependency_source')
                self.assertEqual(self.outcome((), 'sample (*)!', blocks).reason,
                                 'unsupported_requirement')
        result = self.outcome(('123 (unknown)',), '123 (*)!')
        self.assertEqual(result.reason, 'unsupported_dependency_name')

    def test_repeated_disjoint_blocks_only_match_exact_directs(self):
        blocks = source_block() + source_block(specs=('other (2)',))
        lock = parsed_lock(blocks, ('sample', 'other'))
        candidates, failures = match_lock_dependencies(lock)
        self.assertEqual([item.used_version for item in candidates], ['1.0', '2'])
        self.assertEqual(failures, ())
