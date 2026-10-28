import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from libyears.gemfile_lock import ParsedGemfileLock, parse_lockfile
from libyears.rubygems import authorize_public_selection

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
                lock, lock.dependencies[0], '1.0',
                (SelectedRubyArtifact('1.0', 'ruby', 'https://rubygems.org'),),
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
                        result = authorize_public_selection(lock, lock.dependencies[0], '1.0', ())
                        self.assertIsInstance(result, UnmeasurableDependency)
                        self.assertEqual(result.reason, 'unsupported_dependency_source')
                        self.assertNotIn('secret', repr(result))
            lock = parsed_lock(directs=('sample!',))
            self.assertEqual(authorize_public_selection(lock, lock.dependencies[0], '1.0', ()).reason,
                             'unsupported_dependency_source')
            http.assert_not_called()

    def test_unrelated_private_source_does_not_taint_public_identity(self):
        lock = parsed_lock(source_block() + source_block('PATH', specs=('other (2)',)))
        result = authorize_public_selection(lock, lock.dependencies[0], '1.0', ())
        self.assertIsInstance(result, DependencyCandidate)
