import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

from libyears.model import (
    Dependency,
    DependencyCandidate,
    GemfileEvidence,
    RubyGemsEvidence,
    SelectedRubyArtifact,
    SourceEvidence,
    UnmeasurableDependency,
)


class GemfileEvidenceTests(unittest.TestCase):
    def row_arguments(self):
        timestamp = datetime(2024, 1, 1, tzinfo=timezone.utc)
        return (
            (DependencyCandidate,
             ("rubygems", "rack", "rack", "rack", "3.0.0", "gemfile_lock")),
            (Dependency,
             ("rubygems", "rack", "3.0.0", timestamp, "3.0.0", timestamp,
              "gemfile_lock")),
            (UnmeasurableDependency,
             ("rubygems", "rack", "rack", "lockfile_missing")),
        )

    def test_old_row_callers_default_to_no_scoped_evidence(self):
        ruby_evidence = RubyGemsEvidence(
            (SelectedRubyArtifact("3.0.0", "ruby", "rubygems.org"),)
        )
        for model, arguments in self.row_arguments():
            with self.subTest(model=model.__name__):
                row = model(*arguments)
                self.assertIsNone(row.rubygems_evidence)
                self.assertIsNone(row.gemfile_evidence)

                row = model(*arguments, ruby_evidence)
                self.assertIs(row.rubygems_evidence, ruby_evidence)
                self.assertIsNone(row.gemfile_evidence)

        timestamp = datetime(2024, 1, 1, tzinfo=timezone.utc)
        dependency = Dependency("pypi", "example", "1.0", timestamp, "1.0", timestamp)
        self.assertEqual(dependency.version_source, "requirements_exact")
        self.assertIsNone(dependency.gemfile_evidence)

    def test_scoped_row_field_follows_existing_ruby_evidence(self):
        ruby_evidence = RubyGemsEvidence(())
        evidence = GemfileEvidence(("default", "test"), ("~> 3.0",))
        for model, arguments in self.row_arguments():
            with self.subTest(model=model.__name__):
                row = model(*arguments, ruby_evidence, evidence)
                self.assertIs(row.rubygems_evidence, ruby_evidence)
                self.assertIs(row.gemfile_evidence, evidence)

                keyword_row = model(*arguments, gemfile_evidence=evidence)
                self.assertIsNone(keyword_row.rubygems_evidence)
                self.assertIs(keyword_row.gemfile_evidence, evidence)

    def test_lock_requirement_distinguishes_omitted_null_and_text(self):
        omitted = GemfileEvidence(("default",), ())
        known_absent = GemfileEvidence(
            ("default",), (), lock_requirement=None, include_lock_requirement=True
        )
        safe_text = GemfileEvidence(
            ("default",), ("~> 3.0",), "~> 3.0", True
        )
        self.assertEqual(
            [(item.include_lock_requirement, item.lock_requirement)
             for item in (omitted, known_absent, safe_text)],
            [(False, None), (True, None), (True, "~> 3.0")],
        )
        self.assertNotEqual(omitted, known_absent)

    def test_evidence_preserves_full_memberships_and_ordered_literal_requirements(self):
        evidence = GemfileEvidence(
            ("Test", "default", "test"), ("< 4", ">= 3.0"), "< 4, >= 3.0", True
        )
        self.assertEqual(evidence.declared_groups, ("Test", "default", "test"))
        self.assertEqual(evidence.declaration_requirements, ("< 4", ">= 3.0"))
        self.assertEqual(evidence.lock_requirement, "< 4, >= 3.0")
        self.assertEqual(GemfileEvidence(("default",), ()).declaration_requirements, ())

    def test_evidence_is_immutable(self):
        evidence = GemfileEvidence(("default",), ())
        with self.assertRaises(FrozenInstanceError):
            evidence.include_lock_requirement = True

    def test_source_evidence_preserves_old_positional_fields_and_defaults(self):
        ordinary = SourceEvidence("requirements.txt", None)
        self.assertIsNone(ordinary.requested_groups)
        source = SourceEvidence(
            "Gemfile.lock", "Gemfile.lock", "gemfile_lock", True,
            "all_direct_locked", "earliest_admissible_supported_observable",
        )
        self.assertEqual(source.format, "gemfile_lock")
        self.assertTrue(source.include_format)
        self.assertEqual(source.scope, "all_direct_locked")
        self.assertEqual(source.publication_basis, "earliest_admissible_supported_observable")
        self.assertIsNone(source.requested_groups)

    def test_source_evidence_retains_requested_group_case_and_null_format(self):
        source = SourceEvidence(
            "Gemfile", "Gemfile.lock", None, True, "selected_declared_groups",
            "earliest_admissible_supported_observable", ("Test", "test"),
        )
        self.assertEqual(source.requested_groups, ("Test", "test"))
        self.assertIsNone(source.format)
        self.assertTrue(source.include_format)


if __name__ == "__main__":
    unittest.main()
