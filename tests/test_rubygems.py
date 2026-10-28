import unittest
import os
import tempfile
from pathlib import Path
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from libyears.gemfile_lock import ParsedGemfileLock, parse_lockfile
from libyears.rubygems import authorize_public_selection, match_lock_dependencies, ruby_source_result

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


FIXTURES = Path(__file__).parent / 'fixtures' / 'rubygems'


class RootSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.http = patch('urllib.request.urlopen', side_effect=AssertionError('HTTP prohibited'))
        self.request = self.http.start()
        self.addCleanup(self.http.stop)
        self.addCleanup(self.request.assert_not_called)

    def write_fixture(self, name='direct_scope.lock'):
        data = (FIXTURES / name).read_bytes()
        (self.root / 'Gemfile.lock').write_bytes(data)
        return data

    def assert_rejected(self, result, reason='invalid_lockfile'):
        self.assertTrue(result.source_present)
        self.assertFalse(result.measurement_available)
        self.assertIsNone(result.dependencies_discovered)
        self.assertEqual(result.candidates, ())
        self.assertEqual(result.unmeasurable, ())
        self.assertEqual(result.source_errors[0].reason, reason)
        self.assertEqual(result.source_errors[0].source, 'Gemfile.lock')
        self.assertIsNone(result.evidence.format)

    def test_absent_gemfile_only_nested_alternate_and_direct_file_are_ignored(self):
        self.assertFalse(ruby_source_result(None).source_present)
        self.assertFalse(ruby_source_result(self.root).source_present)
        (self.root / 'Gemfile').mkdir()  # Unreadable as text; never inspected.
        nested = self.root / 'nested'
        nested.mkdir()
        (nested / 'Gemfile.lock').write_bytes((FIXTURES / 'direct_scope.lock').read_bytes())
        (self.root / 'gems.locked').write_text('ignored')
        (self.root / 'sample.gemspec').write_text('ignored')
        self.assertFalse(ruby_source_result(self.root).source_present)
        self.write_fixture()
        self.assertFalse(ruby_source_result(self.root / 'Gemfile.lock').source_present)
        self.assertTrue(ruby_source_result(self.root).source_present)

    def test_lock_only_and_gemfile_presence_have_identical_unchanged_results(self):
        before = self.write_fixture()
        result = ruby_source_result(self.root)
        (self.root / 'Gemfile').write_bytes(b'not Ruby\xff')
        self.assertEqual(ruby_source_result(self.root), result)
        self.assertEqual((self.root / 'Gemfile.lock').read_bytes(), before)
        self.assertEqual((self.root / 'Gemfile').read_bytes(), b'not Ruby\xff')
        self.assertEqual(result.dependencies_discovered, 3)
        self.assertTrue(result.measurement_available)
        self.assertEqual([item.name for item in result.candidates], ['sample'])
        self.assertEqual([item.name for item in result.unmeasurable], ['bundler', 'tzinfo-data'])
        self.assertEqual(result.evidence, SourceEvidence(
            'Gemfile.lock', 'Gemfile.lock', 'gemfile_lock', True,
            'all_direct_locked', 'earliest_admissible_supported_observable',
        ))

    def test_empty_scope_is_available_zero(self):
        self.write_fixture('empty_scope.lock')
        result = ruby_source_result(self.root)
        self.assertEqual(result.dependencies_discovered, 0)
        self.assertTrue(result.measurement_available)
        self.assertTrue(result.source_present)
        self.assertEqual((result.candidates, result.unmeasurable, result.source_errors), ((), (), ()))

    def test_nonregular_broken_link_and_invalid_text_are_present_failures(self):
        path = self.root / 'Gemfile.lock'
        path.mkdir()
        self.assert_rejected(ruby_source_result(self.root))
        path.rmdir()
        path.symlink_to(self.root / 'missing')
        self.assert_rejected(ruby_source_result(self.root))
        path.unlink()
        os.mkfifo(path)
        self.assert_rejected(ruby_source_result(self.root))
        path.unlink()
        path.write_bytes(b'\xff')
        self.assert_rejected(ruby_source_result(self.root))

    def test_unreadable_or_uninspectable_artifact_is_not_absent(self):
        self.write_fixture()
        with patch.object(Path, 'read_text', side_effect=PermissionError('private secret')):
            result = ruby_source_result(self.root)
            self.assert_rejected(result)
            self.assertNotIn('secret', repr(result))
        with patch.object(Path, 'lstat', side_effect=PermissionError('private secret')):
            self.assert_rejected(ruby_source_result(self.root))

    def test_whole_rejection_never_salvages_scope_and_diagnostics_are_safe(self):
        for text, reason in (
            ('arbitrary secret\n', 'unsupported_lockfile_format'),
            ('GEM\n  remote: https://private.invalid/secret\n  specs:\n'
             '    sample (1)\nDEPENDENCIES\n  sample\n', 'invalid_lockfile'),
            ((FIXTURES / 'direct_scope.lock').read_text() + '\nCHECKSUMS\n  secret\n',
             'unsupported_lockfile_format'),
        ):
            (self.root / 'Gemfile.lock').write_text(text)
            result = ruby_source_result(self.root)
            self.assert_rejected(result, reason)
            self.assertNotIn('secret', repr(result))

    def test_only_root_lock_is_read(self):
        self.write_fixture()
        original = Path.read_text
        reads = []

        def read_text(path, *args, **kwargs):
            reads.append(path)
            return original(path, *args, **kwargs)

        with patch.object(Path, 'read_text', read_text):
            result = ruby_source_result(self.root)
        self.assertEqual(reads, [self.root / 'Gemfile.lock'])
        self.assertEqual(result.dependencies_discovered, 3)

    def test_local_failure_retains_count_and_safe_authority_diagnostic(self):
        text = source_block(remotes=('https://private.invalid/secret',))
        text += 'PLATFORMS\n  ruby\nDEPENDENCIES\n  sample\n'
        (self.root / 'Gemfile.lock').write_text(text)
        result = ruby_source_result(self.root)
        self.assertEqual(result.dependencies_discovered, 1)
        self.assertTrue(result.measurement_available)
        self.assertEqual(result.candidates, ())
        self.assertEqual(result.unmeasurable[0].reason, 'unsupported_dependency_source')
        self.assertIn('no public namesake substitution', result.diagnostics[0][1])
        self.assertNotIn('secret', repr(result))

    def test_public_scan_remains_unactivated(self):
        from libyears.scan import scan_mixed_repository

        self.write_fixture()
        report = scan_mixed_repository(self.root)
        self.assertEqual([source.ecosystem for source in report.source_results], ['pypi', 'npm'])
        self.assertFalse(any(source.source_present for source in report.source_results))
        self.assertEqual(report.measurements, ())
        self.assertEqual(report.summary.dependencies_discovered, 0)

    def test_platform_metadata_never_selects_internal_candidates(self):
        self.write_fixture()
        original = ruby_source_result(self.root)
        path = self.root / 'Gemfile.lock'
        path.write_text(path.read_text().replace('  ruby\n  java', '  x86_64-linux'))
        self.assertEqual(ruby_source_result(self.root), original)
