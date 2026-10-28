import unittest
from datetime import datetime, timedelta, timezone

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
