import unittest
from unittest.mock import patch

from libyears.nuget_version import (
    parse_requested_minimum, parse_selected_identity, stable_precedence_key,
)


class NuGetVersionTests(unittest.TestCase):
    def test_five_supported_request_minima(self):
        pairs = [
            ("1.0", "1.0.0", (1, 0, 0, 0)),
            ("1.2.3", "1.2.3", (1, 2, 3, 0)),
            ("1.2.3.0", "1.2.3", (1, 2, 3, 0)),
            ("1.2.3.4", "1.2.3.4", (1, 2, 3, 4)),
            ("0.0.0.0", "0.0.0", (0, 0, 0, 0)),
        ]
        for original, normalized, components in pairs:
            with self.subTest(original=original):
                minimum = parse_requested_minimum(original)
                self.assertEqual(minimum.normalized_version, normalized)
                self.assertEqual(minimum.components, components)

    def test_request_minima_do_not_compare_selected_outcomes(self):
        self.assertNotEqual(parse_requested_minimum("1.0"), parse_requested_minimum("1.0.1"))
        self.assertNotEqual(parse_requested_minimum("1.2.3.4"), parse_requested_minimum("1.2.3"))

    def test_requests_reject_evidence_only_and_range_syntax(self):
        for value in ["01.2", "1.02.3", "1.2-beta", "1.2+build", "[1.2.3]",
                      "[1.2.3, )", "1.*", "$(Version)", " 1.2", "1.2\n"]:
            with self.subTest(value=value):
                self.assertIsNone(parse_requested_minimum(value))

    def test_selected_normalization_preserves_safe_original(self):
        pairs = [("01.002", "1.2.0"), ("01.002.0003.00", "1.2.3"),
                 ("01.2.3.004", "1.2.3.4"),
                 ("1.2-RC.01+Build.9", "1.2.0-rc.01"),
                 ("1.2.3+build", "1.2.3")]
        for original, normalized in pairs:
            with self.subTest(original=original):
                identity = parse_selected_identity(original)
                self.assertEqual(identity.original_version, original)
                self.assertEqual(identity.normalized_version, normalized)

    def test_identity_equivalence_ignores_build_and_prerelease_case(self):
        first = parse_selected_identity("01.2-RC.1+one")
        second = parse_selected_identity("1.2.0.0-rc.1+TWO")
        self.assertEqual(first.normalized_version, second.normalized_version)
        self.assertEqual(first.components, second.components)
        self.assertEqual(first.prerelease, second.prerelease)

    def test_numeric_stable_order_includes_revision(self):
        self.assertGreater(stable_precedence_key("1.10.0"), stable_precedence_key("1.9.0"))
        self.assertGreater(stable_precedence_key("1.0.0.1"), stable_precedence_key("1.0.0"))
        self.assertEqual(stable_precedence_key("01.2+build"), stable_precedence_key("1.2.0.0"))
        self.assertIsNone(stable_precedence_key("99.0-rc"))
        self.assertIsNone(stable_precedence_key("[1.2.3, )"))

    def test_unsupported_selected_forms(self):
        for value in [None, True, 1, "", "1", "v1.2", "1.2.3.4.5", "-1.2",
                      "1..2", "1.2-", "1.2-a..b", "1.2+", "1.2+a..b",
                      "1.2+one+two", "1.2_3", "１.2", "1.2-β", "1.2 ", "1.2\n"]:
            with self.subTest(value=value):
                self.assertIsNone(parse_selected_identity(value))
                self.assertIsNone(stable_precedence_key(value))

    def test_length_bounds_precede_integer_conversion(self):
        for parser in [parse_requested_minimum, parse_selected_identity, stable_precedence_key]:
            with self.subTest(parser=parser.__name__):
                with patch("libyears.nuget_version.int", side_effect=AssertionError("converted"), create=True):
                    self.assertIsNone(parser("1." + "9" * 33))
                    self.assertIsNone(parser("1." + "9" * 10000))
                    self.assertIsNone(parser("1.2+" + "a" * 253))

    def test_exact_length_boundaries(self):
        value = "9" * 32 + ".0"
        self.assertEqual(parse_selected_identity(value).components[0], 10 ** 32 - 1)
        self.assertIsNotNone(parse_requested_minimum(value))
        self.assertIsNotNone(parse_selected_identity("1.2+" + "a" * 252))
        self.assertIsNone(parse_selected_identity("1.2+" + "a" * 253))


if __name__ == "__main__":
    unittest.main()
