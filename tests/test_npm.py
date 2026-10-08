import json
import tempfile
import unittest
from pathlib import Path

from libyears.npm import (
    INVALID_MANIFEST,
    UNSUPPORTED_DEPENDENCY_SOURCE,
    discover_manifest,
)


class NpmManifestTests(unittest.TestCase):
    def discover(self, contents: str):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(contents, encoding="utf-8")
            return discover_manifest(root)

    def test_discovers_production_dependencies_and_excludes_optional_override(self):
        result = self.discover(json.dumps({
            "dependencies": {
                "express": "^5.1.0",
                "optional-override": "^1.0.0",
                "@types/node": "^22.0.0",
            },
            "optionalDependencies": {
                "optional-only": "^3.0.0",
                "optional-override": "^2.0.0",
            },
            "devDependencies": {"dev-only": "^1.0.0"},
            "peerDependencies": {"peer-only": "^1.0.0"},
            "peerDependenciesMeta": {"peer-only": {"optional": True}},
            "bundledDependencies": ["bundled-only"],
        }))

        self.assertIsNone(result.reason)
        self.assertEqual(
            [(item.name, item.declared) for item in result.dependencies],
            [("express", "^5.1.0"), ("@types/node", "^22.0.0")],
        )

    def test_empty_or_missing_manifest_has_no_discoveries(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(discover_manifest(root).dependencies, ())
            (root / "package.json").write_text("{}", encoding="utf-8")
            self.assertEqual(discover_manifest(root).dependencies, ())

    def test_workspace_child_manifest_is_not_scanned(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(
                json.dumps({"workspaces": ["packages/*"]}), encoding="utf-8"
            )
            child = root / "packages" / "app"
            child.mkdir(parents=True)
            (child / "package.json").write_text(
                json.dumps({"dependencies": {"child-only": "^1.0.0"}}),
                encoding="utf-8",
            )

            self.assertEqual(discover_manifest(root).dependencies, ())

    def test_malformed_json_is_invalid_manifest_without_synthetic_rows(self):
        result = self.discover('{"dependencies": {"ghost": "1.0.0"')
        self.assertEqual(result.reason, INVALID_MANIFEST)
        self.assertEqual(result.dependencies, ())

    def test_invalid_root_and_dependency_maps_are_invalid_manifest(self):
        for contents in (
            "[]",
            '{"dependencies": []}',
            '{"optionalDependencies": null}',
            '{"dependencies": {"express": null}}',
        ):
            with self.subTest(contents=contents):
                result = self.discover(contents)
                self.assertEqual(result.reason, INVALID_MANIFEST)
                self.assertEqual(result.dependencies, ())


    def test_unsupported_sources_remain_discovered_with_original_declarations(self):
        declarations = {
            "git-https": "git+https://github.com/acme/widget.git#main",
            "git-ssh": "git+ssh://git@example.test/acme/widget.git",
            "git-protocol": "git://example.test/acme/widget.git",
            "ssh": "ssh://git@example.test/acme/widget.git",
            "git-at": "git@example.test:acme/widget.git",
            "github-prefix": "github:acme/widget#main",
            "github-shorthand": "acme/widget#main",
            "file": "file:../widget",
            "link": "link:../widget",
            "workspace": "workspace:*",
            "tarball": "https://example.test/widget-1.0.0.tgz",
            "alias": "npm:other-widget@^1.0.0",
        }
        result = self.discover(json.dumps({"dependencies": declarations}))

        self.assertIsNone(result.reason)
        self.assertEqual(len(result.dependencies), len(declarations))
        for dependency in result.dependencies:
            with self.subTest(name=dependency.name):
                self.assertEqual(
                    dependency.reason, UNSUPPORTED_DEPENDENCY_SOURCE
                )
                self.assertEqual(dependency.declared, declarations[dependency.name])

    def test_registry_ranges_and_scoped_package_identity_are_not_reclassified(self):
        result = self.discover(json.dumps({
            "dependencies": {
                "express": "^5.1.0",
                "@types/node": "^22.0.0",
                "tagged": "latest",
            }
        }))

        self.assertEqual(
            [(item.name, item.declared, item.reason) for item in result.dependencies],
            [
                ("express", "^5.1.0", None),
                ("@types/node", "^22.0.0", None),
                ("tagged", "latest", None),
            ],
        )

if __name__ == "__main__":
    unittest.main()
