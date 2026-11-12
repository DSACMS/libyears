"""Pinned Apache Maven conformance plus independent libyears policy boundaries.

Adapted expected vectors from Apache Maven 3.9.11 ComparableVersionTest,
licensed under Apache-2.0; changed to Python unittest with bounded-input and
libyears-policy cases. See third_party/maven-3.9.11/{README.md,LICENSE,NOTICE}.
"""

import itertools
import json
from pathlib import Path
import unittest

from libyears.maven_version import (
    VersionError, compare_versions, eligibility, is_snapshot, parse_version,
    select_latest,
)


FIXTURE = Path(__file__).parent / "fixtures/maven/comparable-version-3.9.11.json"


class MavenOrderingTests(unittest.TestCase):
    def assertOrder(self, left, right, expected):
        self.assertEqual(compare_versions(left, right), expected, (left, right))
        self.assertEqual(compare_versions(right, left), -expected, (right, left))

    def test_pinned_literal_vectors(self):
        vectors = json.loads(FIXTURE.read_text())
        for key in ("versions_qualifier", "versions_number"):
            for left, right in itertools.combinations(vectors[key], 2):
                self.assertOrder(left, right, -1)
        for left, right in vectors["equal"]:
            self.assertOrder(left, right, 0)
        for left, right in vectors["less"]:
            self.assertOrder(left, right, -1)

    def test_pinned_regressions(self):
        for ordered in (
            ("6.1.0rc3", "6.1.0", "6.1H.5-beta"),  # MNG-5568
            ("20190126.230843", "1234567890.12345",
             "123456789012345.1H.5-beta", "12345678901234567890.1H.5-beta"),
            ("1-0.alpha", "1-0.beta", "1"),  # MNG-6964
        ):
            for left, right in itertools.combinations(ordered, 2):
                self.assertOrder(left, right, -1)
        for qualifier in ("abc", "alpha", "a", "beta", "b", "def", "milestone", "m", "RC"):
            self.assertOrder("1.0.0." + qualifier + "1", "1.0.0-" + qualifier + "2", -1)
            for left, right in itertools.combinations(
                ["2-" + qualifier, "2.0." + qualifier, "2.0.0." + qualifier], 2
            ):
                self.assertOrder(left, right, 0)

    def test_leading_zeroes_and_numeric_widths(self):
        for width in range(1, 129):
            self.assertOrder("0" * (width - 1) + "1", "1", 0)
            self.assertOrder("0" * width, "0", 0)
        for width in (9, 18, 127):
            self.assertOrder("9" * width, "1" + "0" * width, -1)
        # Upstream's all-zero width selects a numeric storage class before
        # normalization. Preserve it when a non-null successor retains the zero.
        self.assertOrder("0.1", "0000000000.1", -1)
        self.assertOrder("0000000000.1", "0000000000000000000.1", -1)

    def test_alias_context_and_nonseparators(self):
        for short, full in (("a", "alpha"), ("b", "beta"), ("m", "milestone")):
            self.assertOrder("1" + short + "1", "1-" + full + "-1", 0)
            self.assertOrder("1-" + full, "1-" + short, -1)
            self.assertOrder("1-" + short + "-1", "1-" + full + "-1", 1)
        self.assertOrder("1_1", "1-1", -1)
        self.assertOrder("1_1", "1.1", -1)
        self.assertOrder("1_1", "1+1", 1)
        self.assertOrder("1..0", "1", 0)
        self.assertOrder("1--0", "1", 0)
        self.assertOrder("1-abcdefghijklmnopqrstuvwxyz", "1-ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0)

    def test_fixed_corpus_order_properties(self):
        corpus = ["0", "1-alpha1", "1-beta", "1-rc2", "1-SNAPSHOT",
                  "1", "1.0", "1-final", "1-sp2", "1-foo", "1_1", "1+1",
                  "1-1", "1.0.1", "2.0", "11m", "6.1H.5-beta"]
        for a, b in itertools.product(corpus, repeat=2):
            self.assertOrder(a, b, compare_versions(a, b))
        for a, b, c in itertools.product(corpus, repeat=3):
            if compare_versions(a, b) <= 0 and compare_versions(b, c) <= 0:
                self.assertLessEqual(compare_versions(a, c), 0, (a, b, c))

    def test_pinned_nested_qualifier_cycle_is_excluded_before_selection(self):
        # The pin is not universally transitive: its list/null and list/string
        # rules differ here. Preserve fidelity rather than silently repairing it.
        self.assertOrder("1-0.alpha", "1", -1)
        self.assertOrder("1", "1-sp2", -1)
        self.assertOrder("1-0.alpha", "1-sp2", 1)
        self.assertEqual(eligibility(parse_version("1-0.alpha")), "excluded")
        for candidates in itertools.permutations(("1-0.alpha", "1", "1-sp2")):
            self.assertEqual(select_latest(candidates).version, "1-sp2")

    def test_exact_lexical_and_resource_refusals(self):
        for value in (None, 1, "", "LATEST", "release", "[1]", "[1,2)", "${v}",
                      "1/2", "1\\2", "1%2", "1:2", " 1", "1\n", "é", "1\x00", "-1"):
            with self.subTest(value=value), self.assertRaises(VersionError):
                parse_version(value)
        for value in ("1" * 257, "1" * 129, "1" + ".0" * 128, "1" + "-" * 128):
            with self.subTest(value=value), self.assertRaises(VersionError):
                parse_version(value)
        parse_version("1" * 128)
        parse_version("1" + ".0" * 127)
        parse_version("1" + "a" * 255)
        self.assertEqual(parse_version("1.0.Final").exact, "1.0.Final")


class MavenEligibilityTests(unittest.TestCase):
    def test_release_whitelist(self):
        for value in ("1", "1.0", "1-0", "1.0.Final", "1.0RELEASE", "1ga", "1GA2",
                      "1.0-sp", "1.0-sp2", "1SP12", "01.00", "1-final0"):
            with self.subTest(value=value):
                self.assertEqual(eligibility(parse_version(value)), "eligible")

    def test_prerelease_tokens_and_context(self):
        for token in ("alpha", "beta", "milestone", "rc", "cr", "a1", "b2", "m3"):
            for value in ("2-" + token, "2." + token, "2" + token, "2-" + token + "-foo"):
                with self.subTest(value=value):
                    self.assertEqual(eligibility(parse_version(value)), "excluded")
        for value in ("2-a", "2-b", "2-m", "2-a-1", "2-preview", "2-alpha_1", "2+rc1"):
            self.assertEqual(eligibility(parse_version(value)), "unknown", value)
        # Eligibility and ordering are separate: a used prerelease remains an
        # orderable exact fact, while its candidacy as a latest target is excluded.
        self.assertLess(compare_versions("2-rc1", "2"), 0)

    def test_snapshot_suffix_token_and_timestamp(self):
        for value in ("2-SNAPSHOT", "2snapshot", "2-sNaPsHoT", "2-snapshot-foo",
                      "2-20261112.120000-1", "2-00000000.999999-01", "snapshot"):
            version = parse_version(value)
            self.assertTrue(is_snapshot(version), value)
            self.assertEqual(eligibility(version), "excluded")
        for value in ("20190126.230843", "2-20261112.12000-1", "2-snapshotish",
                      "2-20261112.120000-1-foo", "2_snapshot-foo"):
            self.assertFalse(is_snapshot(parse_version(value)), value)

    def assertLatest(self, candidates, version=None, reason=None):
        result = select_latest(candidates)
        self.assertEqual((result.version, result.reason), (version, reason))

    def test_unknown_below_equal_above(self):
        self.assertLatest(["1-preview", "2"], "2")
        self.assertLatest(["1", "2-preview"], reason="unknown_latest_eligibility")
        # Safe but not in the whitelist; normalization gives equal Maven order.
        self.assertLatest(["1", "1."], reason="unknown_latest_eligibility")
        self.assertLatest(["1", "1-foo"], reason="unknown_latest_eligibility")
        self.assertLatest(["1-preview"], reason="unknown_latest_eligibility")
        self.assertLatest(["2-alpha", "2-SNAPSHOT"], reason="no_stable_release")
        self.assertLatest([], reason="no_stable_release")

    def test_maximum_ties_and_identical_duplicates(self):
        for pair in (("1", "1.0"), ("1", "1-final"), ("1", "1GA"),
                     ("1-sp1", "1SP1"), ("1", "1-0")):
            self.assertLatest(pair, reason="ambiguous_latest_version")
        self.assertLatest(["1", "1", "1"], "1")
        self.assertLatest(["1", "1.0", "2"], "2")
        self.assertLatest(["1", "1.0", "2-preview"], reason="unknown_latest_eligibility")

    def test_global_target_and_service_packs(self):
        self.assertLatest(["1.9", "2.0", "3-rc1", "3-20261112.120000-1"], "2.0")
        self.assertLatest(["1", "1-sp1", "1-sp2"], "1-sp2")
        self.assertLatest(["1.9", "1.10"], "1.10")

    def test_unorderable_entry_never_dropped(self):
        for value in ("[3]", "LATEST", "1" * 129):
            for candidates in (["2", value], [value, "2"]):
                result = select_latest(candidates)
                self.assertIsNone(result.version)
                self.assertIn(result.reason, ("maven_catalogue_unavailable", "maven_metadata_budget_exceeded"))
        # Even a recognized excluded suffix cannot bypass the ordering budget.
        self.assertLatest(["2", "1" * 129 + "-SNAPSHOT"], reason="maven_metadata_budget_exceeded")

    def test_catalogue_count_before_duplicate_collapse(self):
        self.assertLatest(itertools.repeat("1", 10_000), "1")
        self.assertLatest(itertools.repeat("1", 10_001), reason="maven_metadata_budget_exceeded")

    def test_permutation_determinism(self):
        for catalogue in (("1", "1-preview", "2"), ("1", "1.", "2-rc1"),
                          ("1", "1.0", "1-preview"), ("1", "1.0", "2")):
            expected = select_latest(catalogue)
            for permutation in itertools.permutations(catalogue):
                self.assertEqual(select_latest(permutation), expected)


if __name__ == "__main__":
    unittest.main()
