import json
import tempfile
import unittest
from pathlib import Path

from libyears.npm import (
    DECLARATION_LOCK_CONFLICT,
    INVALID_MANIFEST,
    LOCK_VERSION_MISSING,
    UNSUPPORTED_DEPENDENCY_SOURCE,
    INVALID_LOCKFILE,
    UNSUPPORTED_LOCKFILE_VERSION,
    discover_manifest,
    resolve_lockfile,
    resolve_v2_lockfile,
    resolve_v3_lockfile,
)


class NpmManifestTests(unittest.TestCase):
    def discover(self, contents: str):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(contents, encoding="utf-8")
            return discover_manifest(root)

    def discover_with_lock(self, lock_content: str | None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(
                json.dumps({"dependencies": {"alpha": "^1.0.0", "beta": "^2.0.0"}}),
                encoding="utf-8",
            )
            if lock_content is not None:
                (root / "package-lock.json").write_text(
                    lock_content, encoding="utf-8"
                )
            return resolve_lockfile(root, discover_manifest(root))

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

    def test_v2_resolves_only_declared_root_and_scoped_package_paths(self):
        manifest = self.discover(json.dumps({
            "dependencies": {
                "express": "^1.0.0",
                "@types/node": "1.2.3",
            }
        }))
        resolved = resolve_v2_lockfile(
            manifest,
            {
                "": {"name": "fixture"},
                "node_modules/express": {"version": "2.0.0"},
                "node_modules/container/node_modules/express": {"version": "9.0.0"},
                "node_modules/@types/node": {"version": "1.2.3"},
                "node_modules/lockfile-only": {"version": "7.0.0"},
            },
        )

        self.assertEqual(
            [
                (item.name, item.declared, item.used_version, item.reason)
                for item in resolved.dependencies
            ],
            [
                ("express", "^1.0.0", "2.0.0", None),
                ("@types/node", "1.2.3", "1.2.3", None),
            ],
        )

    def test_v2_missing_direct_path_is_unmeasurable(self):
        manifest = self.discover(
            json.dumps({"dependencies": {"express": "^5.1.0"}})
        )
        resolved = resolve_v2_lockfile(manifest, {"": {"name": "fixture"}})

        self.assertEqual(len(resolved.dependencies), 1)
        self.assertEqual(resolved.dependencies[0].reason, LOCK_VERSION_MISSING)
        self.assertIsNone(resolved.dependencies[0].used_version)

    def test_v2_exact_declaration_conflict_and_non_exact_declaration(self):
        manifest = self.discover(json.dumps({
            "dependencies": {
                "pinned": "1.2.3",
                "ranged": "^1.2.3",
                "tagged": "latest",
            }
        }))
        resolved = resolve_v2_lockfile(
            manifest,
            {
                "node_modules/pinned": {"version": "1.2.4"},
                "node_modules/ranged": {"version": "9.0.0"},
                "node_modules/tagged": {"version": "3.0.0"},
            },
        )

        self.assertEqual(
            [(item.name, item.reason, item.used_version) for item in resolved.dependencies],
            [
                ("pinned", DECLARATION_LOCK_CONFLICT, None),
                ("ranged", None, "9.0.0"),
                ("tagged", None, "3.0.0"),
            ],
        )

    def test_v3_resolves_only_declared_root_and_scoped_package_paths(self):
        manifest = self.discover(json.dumps({
            "dependencies": {
                "express": "^1.0.0",
                "@types/node": "1.2.3",
            }
        }))
        resolved = resolve_v3_lockfile(
            manifest,
            {
                "": {"name": "fixture"},
                "node_modules/express": {"version": "2.0.0"},
                "node_modules/container/node_modules/express": {"version": "9.0.0"},
                "node_modules/@types/node": {"version": "1.2.3"},
                "node_modules/lockfile-only": {"version": "7.0.0"},
            },
        )

        self.assertEqual(
            [
                (item.name, item.declared, item.used_version, item.reason)
                for item in resolved.dependencies
            ],
            [
                ("express", "^1.0.0", "2.0.0", None),
                ("@types/node", "1.2.3", "1.2.3", None),
            ],
        )

    def test_v3_missing_path_and_exact_declaration_conflict(self):
        manifest = self.discover(json.dumps({
            "dependencies": {
                "missing": "^1.0.0",
                "pinned": "1.2.3",
            }
        }))
        resolved = resolve_v3_lockfile(
            manifest,
            {"node_modules/pinned": {"version": "1.2.4"}},
        )

        self.assertEqual(
            [(item.name, item.reason, item.used_version) for item in resolved.dependencies],
            [
                ("missing", LOCK_VERSION_MISSING, None),
                ("pinned", DECLARATION_LOCK_CONFLICT, None),
            ],
        )

    def test_missing_lockfile_and_direct_paths_use_lock_version_missing(self):
        without_lock = self.discover_with_lock(None)
        with_missing_paths = self.discover_with_lock(json.dumps({
            "lockfileVersion": 2,
            "packages": {"": {"name": "fixture"}},
        }))

        for result in (without_lock, with_missing_paths):
            with self.subTest(result=result):
                self.assertEqual(len(result.dependencies), 2)
                self.assertEqual(
                    [item.reason for item in result.dependencies],
                    [LOCK_VERSION_MISSING, LOCK_VERSION_MISSING],
                )
                self.assertTrue(all(item.used_version is None for item in result.dependencies))

    def test_v1_unknown_and_missing_lockfile_versions_are_unsupported(self):
        for lockfile in (
            {"lockfileVersion": 1, "packages": {}},
            {"lockfileVersion": 4, "packages": {}},
            {"packages": {}},
        ):
            with self.subTest(lockfile=lockfile):
                result = self.discover_with_lock(json.dumps(lockfile))
                self.assertEqual(len(result.dependencies), 2)
                self.assertEqual(
                    [item.reason for item in result.dependencies],
                    [UNSUPPORTED_LOCKFILE_VERSION, UNSUPPORTED_LOCKFILE_VERSION],
                )
                self.assertTrue(all(item.used_version is None for item in result.dependencies))

    def test_malformed_supported_lockfiles_mark_affected_dependencies(self):
        for version in (2, 3):
            with self.subTest(lockfile_version=version):
                malformed_structure = self.discover_with_lock(
                    json.dumps({"lockfileVersion": version, "packages": None})
                )
                self.assertEqual(
                    [item.reason for item in malformed_structure.dependencies],
                    [INVALID_LOCKFILE, INVALID_LOCKFILE],
                )

        malformed_entry = self.discover_with_lock(json.dumps({
            "lockfileVersion": 3,
            "packages": {
                "": {"name": "fixture"},
                "node_modules/alpha": {"version": None},
                "node_modules/beta": {"version": "2.3.0"},
                "node_modules/unused": None,
            },
        }))
        self.assertEqual(
            [(item.reason, item.used_version) for item in malformed_entry.dependencies],
            [(INVALID_LOCKFILE, None), (None, "2.3.0")],
        )

    def test_malformed_lockfile_json_is_invalid_without_candidates(self):
        for lock_content in ('{"lockfileVersion": 2', '[]'):
            with self.subTest(lock_content=lock_content):
                result = self.discover_with_lock(lock_content)
                self.assertEqual(
                    [item.reason for item in result.dependencies],
                    [INVALID_LOCKFILE, INVALID_LOCKFILE],
                )
                self.assertTrue(
                    all(item.used_version is None for item in result.dependencies)
                )


if __name__ == "__main__":
    unittest.main()
