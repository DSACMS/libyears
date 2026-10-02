import tempfile
import unittest
from pathlib import Path

from libyears.requirements import (
    CONFLICTING_VERSIONS,
    NON_EXACT_VERSION,
    UNSUPPORTED_REQUIREMENT,
    discover_requirements,
    normalize_name,
)


class RequirementsTests(unittest.TestCase):
    def discover(self, content: str):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "requirements.txt"
            path.write_text(content, encoding="utf-8")
            return discover_requirements(path)

    def test_exact_pin_and_name_normalization(self):
        result = self.discover("Requests_Security==1.2.3\n")
        self.assertEqual(result.exact[0].name, "Requests_Security")
        self.assertEqual(result.exact[0].normalized_name, "requests-security")
        self.assertEqual(result.exact[0].version, "1.2.3")

    def test_blank_lines_comments_and_inline_comments(self):
        result = self.discover("\n# comment\nrequests==2.31.0 # keep this\n")
        self.assertEqual(len(result.exact), 1)
        self.assertEqual(result.exact[0].declared, "requests==2.31.0")

    def test_non_exact_requirements(self):
        result = self.discover("requests>=2.0\nflask~=3.0\ndjango\n")
        self.assertEqual([item.reason for item in result.unmeasurable], [NON_EXACT_VERSION] * 3)

    def test_urls_and_local_requirements_are_unsupported(self):
        result = self.discover(
            "thing @ https://example.test/thing.whl\n"
            "git+https://example.test/repo.git\n"
            "./local-package\n"
        )
        self.assertEqual([item.reason for item in result.unmeasurable], [UNSUPPORTED_REQUIREMENT] * 3)

    def test_vcs_ssh_and_windows_paths_are_unsupported(self):
        result = self.discover(
            "git://example.test/repo.git\n"
            "ssh://example.test/repo.git\n"
            "C:\\work\\package\n"
            "\\\\server\\share\\package\n"
        )
        self.assertEqual(
            [item.reason for item in result.unmeasurable],
            [UNSUPPORTED_REQUIREMENT] * 4,
        )

    def test_conflicting_exact_versions_are_unmeasurable(self):
        result = self.discover("Foo-Bar==1.0\nfoo_bar==2.0\n")
        self.assertEqual(result.exact, ())
        self.assertEqual(result.unmeasurable[0].reason, CONFLICTING_VERSIONS)
        self.assertIn("Foo-Bar==1.0", result.unmeasurable[0].declared)

    def test_duplicate_same_exact_version_is_one_dependency(self):
        result = self.discover("foo==1.0\nFOO==1.0\n")
        self.assertEqual(len(result.exact), 1)

    def test_normalize_name_collapses_pypi_separators(self):
        self.assertEqual(normalize_name("My_Package.Name"), "my-package-name")


if __name__ == "__main__":
    unittest.main()
