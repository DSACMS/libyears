"""Concrete SemVer compatibility and bounded ReDoS regression probes."""

import itertools
from pathlib import Path
import subprocess
import sys
import unittest

from libyears.npm import _SEMVER_VERSION, _is_stable_version


class NpmSemverTests(unittest.TestCase):
    def test_valid_stable_versions(self):
        for version in (
            "0.0.0", "1.2.3", "10.20.300", "1.2.3+build.7",
            "1.2.3+00.01.-.a-b", "1.2.3+001", "1.2.3+-",
        ):
            with self.subTest(version=version):
                match = _SEMVER_VERSION.fullmatch(version)
                self.assertIsNotNone(match)
                self.assertIsNone(match.group(1))
                self.assertTrue(_is_stable_version(version))

    def test_valid_prereleases_preserve_capture_and_are_not_stable(self):
        for prerelease in (
            "0", "1", "10", "alpha", "rc.1", "0.alpha.1",
            "01a", "00-", "-", "--", "a-b", "0.--.--.end",
        ):
            for build in ("", "+00.-.build.7"):
                version = "1.2.3-" + prerelease + build
                with self.subTest(version=version):
                    match = _SEMVER_VERSION.fullmatch(version)
                    self.assertIsNotNone(match)
                    self.assertEqual(match.group(1), prerelease)
                    self.assertFalse(_is_stable_version(version))

    def test_invalid_versions(self):
        for version in (
            "", "v4.0.0", "01.2.3", "1.02.3", "1.2.03", "1.2",
            "1.2.3.4", "1.2.3-01", "1.2.3+", "not-a-version",
            "1.2.3-", "1.2.3-00", "1.2.3-a.01", "1.2.3-.a",
            "1.2.3-a.", "1.2.3-a..b", "1.2.3+build.",
            "1.2.3+.build", "1.2.3+a..b", "1.2.3+a+b",
            "1.2.3-a+", "1.2.3-a!", "1.2.3+a_b", "1.2.3-é",
            "１.2.3", "1.2.3-١", " 1.2.3", "1.2.3 ", "1.2.3\n",
        ):
            with self.subTest(version=version):
                self.assertIsNone(_SEMVER_VERSION.fullmatch(version))
                self.assertFalse(_is_stable_version(version))

    def test_short_identifiers_against_independent_language_rules(self):
        # Exercise zero rules and separators without duplicating the regex.
        alphabet = "01a-.!"
        allowed = frozenset("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-")
        for length in range(5):
            for characters in itertools.product(alphabet, repeat=length):
                suffix = "".join(characters)
                identifiers = suffix.split(".")
                valid_build = all(
                    identifier and all(char in allowed for char in identifier)
                    for identifier in identifiers
                )
                valid_prerelease = valid_build and all(
                    not (identifier.isdigit() and len(identifier) > 1
                         and identifier.startswith("0"))
                    for identifier in identifiers
                )
                for separator, expected in (("-", valid_prerelease), ("+", valid_build)):
                    version = "1.2.3" + separator + suffix
                    self.assertEqual(
                        _SEMVER_VERSION.fullmatch(version) is not None,
                        expected,
                        version,
                    )

    def test_adversarial_and_long_valid_inputs_in_guarded_subprocess(self):
        # The guard contains a future regression; acceptance is the oracle.
        # The original pattern takes exponential work on trailing-dot attacks.
        probe = r'''
from libyears.npm import _SEMVER_VERSION, _is_stable_version
for repeats in (8, 16, 32, 128, 1024):
    prefix = "0.0.0-0." + "--." * repeats
    for invalid in (prefix, prefix + "!", "0.0.0-0." + "--" * repeats + "!"):
        assert _SEMVER_VERSION.fullmatch(invalid) is None
        assert not _is_stable_version(invalid)
    valid = prefix + "end+00.build.-"
    assert _SEMVER_VERSION.fullmatch(valid) is not None
    assert not _is_stable_version(valid)
for valid in ("1.2.3+" + "a" * 10000, "1" * 10000 + ".0.0", "1.2.3+" + "a." * 1024 + "0"):
    assert _SEMVER_VERSION.fullmatch(valid) is not None
    assert _is_stable_version(valid)
'''
        result = subprocess.run(
            [sys.executable, "-c", probe],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
