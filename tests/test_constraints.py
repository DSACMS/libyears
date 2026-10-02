import unittest

from libyears.constraints import (
    DECLARED_SNAPSHOT_CONFLICT,
    SNAPSHOT_VERSION_INCOMPATIBLE,
    validate_snapshot_version,
)


class ConstraintTests(unittest.TestCase):
    def assert_compatible(self, declaration, snapshot_version):
        result = validate_snapshot_version(declaration, snapshot_version)
        self.assertTrue(result.compatible)
        self.assertIsNone(result.reason)

    def assert_incompatible(self, declaration, snapshot_version, reason):
        result = validate_snapshot_version(declaration, snapshot_version)
        self.assertFalse(result.compatible)
        self.assertEqual(result.reason, reason)

    def test_bare_name_accepts_any_exact_snapshot_version(self):
        self.assert_compatible("requests", "2.31.0rc1")

    def test_exact_pin_requires_textual_version_equality(self):
        self.assert_compatible("requests==2.31.0", "2.31.0")
        self.assert_incompatible(
            "requests==2.31.0", "2.32.0", DECLARED_SNAPSHOT_CONFLICT
        )

    def test_numeric_minimum_accepts_equal_or_higher_version(self):
        self.assert_compatible("requests>=2.31", "2.31")
        self.assert_compatible("requests>=2.31", "2.31.1")
        self.assert_compatible("requests>=2.31", "3.0")

    def test_numeric_minimum_rejects_lower_version(self):
        self.assert_incompatible(
            "requests>=2.31", "2.30.9", SNAPSHOT_VERSION_INCOMPATIBLE
        )

    def test_numeric_minimum_uses_numeric_not_lexical_comparison(self):
        self.assert_compatible("package>=1.9", "1.10")

    def test_non_numeric_minimum_versions_are_not_guessed(self):
        self.assert_incompatible(
            "package>=1.0rc1", "1.0", SNAPSHOT_VERSION_INCOMPATIBLE
        )
        self.assert_incompatible(
            "package>=1.0", "1.0.post1", SNAPSHOT_VERSION_INCOMPATIBLE
        )

    def test_other_operators_are_unsupported(self):
        for declaration in ("package>1.0", "package<=1.0", "package~=1.0", "package!=1.0"):
            with self.subTest(declaration=declaration):
                self.assert_incompatible(
                    declaration, "1.0", SNAPSHOT_VERSION_INCOMPATIBLE
                )

    def test_malformed_or_unsupported_declarations_are_incompatible(self):
        for declaration in (
            "",
            "package [extra]",
            "package @ https://example.test/package.whl",
            "./local-package",
            "git+https://example.test/repo.git",
        ):
            with self.subTest(declaration=declaration):
                self.assert_incompatible(
                    declaration, "1.0", SNAPSHOT_VERSION_INCOMPATIBLE
                )

    def test_empty_snapshot_version_is_incompatible(self):
        self.assert_incompatible("package", "", SNAPSHOT_VERSION_INCOMPATIBLE)


if __name__ == "__main__":
    unittest.main()
