import unittest
from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone

from libyears.model import (
    Dependency, DependencyCandidate, NuGetEvidence, NuGetPublication,
    RegistryFailure, RegistryResult, UnmeasurableDependency,
)


class NuGetModelTests(unittest.TestCase):
    def test_existing_positional_constructors_default_to_no_nuget_evidence(self):
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        records = [
            Dependency("pypi", "example", "1", now, "2", now),
            RegistryResult("example", "1", now, "2", now),
            RegistryFailure("example", "1", "registry_error"),
            DependencyCandidate("pypi", "example", "example", "example==1", "1", "requirements_exact"),
            UnmeasurableDependency("pypi", "example", "example", "non_exact_version"),
        ]
        for record in records:
            with self.subTest(record=type(record).__name__):
                self.assertIsNone(record.nuget_evidence)

    def test_staged_evidence_contains_only_safe_public_facts(self):
        evidence = NuGetEvidence("Example.csproj", "net10.0", "1.0")
        self.assertEqual(evidence.origin_state, "unavailable")
        self.assertEqual(evidence.content_hash_state, "unavailable")
        self.assertEqual(evidence.publication_basis, "nuget_org_first_receipt_created")
        for name in ["selected_version", "normalized_version", "selection_source",
                     "lock_requested", "used_publication", "latest_publication"]:
            self.assertIsNone(getattr(evidence, name))
        self.assertFalse({"content_hash", "baseline", "producer", "source_url"} &
                         {field.name for field in fields(evidence)})
        with self.assertRaises(FrozenInstanceError):
            evidence.origin_state = "asserted_public"

    def test_publication_normalizes_aware_time_to_utc(self):
        local = datetime(2026, 1, 1, 2, tzinfo=timezone(timedelta(hours=2)))
        publication = NuGetPublication("1.0.0", local, False)
        self.assertEqual(publication.created, datetime(2026, 1, 1, tzinfo=timezone.utc))
        self.assertIs(publication.created.tzinfo, timezone.utc)
        self.assertFalse(publication.listed)
        evidence = NuGetEvidence("Example.csproj", "net10.0", "1.0", used_publication=publication)
        self.assertIs(evidence.used_publication, publication)
        with self.assertRaises(ValueError):
            NuGetPublication("1.0.0", datetime(2026, 1, 1), True)


if __name__ == "__main__":
    unittest.main()
