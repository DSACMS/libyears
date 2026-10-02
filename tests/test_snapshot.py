import tempfile
import unittest
from pathlib import Path

from libyears.snapshot import (
    SNAPSHOT_FORMAT,
    SNAPSHOT_VERSION_CONFLICT,
    parse_snapshot,
    parse_snapshot_text,
)


class SnapshotTests(unittest.TestCase):
    def test_exact_entries_preserve_spelling_version_and_source_line(self):
        snapshot = parse_snapshot_text("Requests_Security==1.2.3 # installed\n")
        self.assertEqual(len(snapshot.entries), 1)
        entry = snapshot.entries[0]
        self.assertEqual(entry.name, "Requests_Security")
        self.assertEqual(entry.normalized_name, "requests-security")
        self.assertEqual(entry.version, "1.2.3")
        self.assertEqual(entry.source_line, "Requests_Security==1.2.3 # installed")
        self.assertEqual(entry.line_number, 1)
        self.assertEqual(entry.format, SNAPSHOT_FORMAT)

    def test_blank_lines_comments_and_trailing_comments_are_ignored(self):
        snapshot = parse_snapshot_text(
            "\n  # comment\nrequests==2.31.0 # trailing comment\n"
        )
        self.assertEqual([(entry.name, entry.version) for entry in snapshot.entries], [("requests", "2.31.0")])
        self.assertEqual(snapshot.rejected, ())

    def test_identical_duplicate_entries_are_harmless(self):
        snapshot = parse_snapshot_text("foo==1.0\nFOO==1.0\n")
        self.assertEqual(len(snapshot.entries), 1)
        self.assertEqual(snapshot.conflicts, ())

    def test_conflicting_versions_use_normalized_identity(self):
        snapshot = parse_snapshot_text("Foo-Bar==1.0\nfoo_bar==2.0\n")
        self.assertEqual(snapshot.entries, ())
        self.assertEqual(len(snapshot.conflicts), 1)
        conflict = snapshot.conflicts[0]
        self.assertEqual(conflict.name, "Foo-Bar")
        self.assertEqual(conflict.normalized_name, "foo-bar")
        self.assertEqual(conflict.versions, ("1.0", "2.0"))
        self.assertEqual(conflict.reason, SNAPSHOT_VERSION_CONFLICT)
        self.assertEqual([entry.line_number for entry in conflict.entries], [1, 2])

    def test_non_exact_and_unsupported_lines_are_rejected_as_evidence(self):
        snapshot = parse_snapshot_text(
            "requests\n"
            "requests>=2.0\n"
            "https://example.test/requests.whl\n"
            "git+https://example.test/repo.git\n"
            "./local-package\n"
            "-e ./editable\n"
            "malformed ==\n"
        )
        self.assertEqual(snapshot.entries, ())
        self.assertEqual(snapshot.conflicts, ())
        self.assertEqual([line.line_number for line in snapshot.rejected], list(range(1, 8)))

    def test_parse_snapshot_uses_tempfile(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "resolved.txt"
            path.write_text("requests==2.31.0\n", encoding="utf-8")
            snapshot = parse_snapshot(path)
        self.assertEqual(snapshot.entries[0].version, "2.31.0")
        self.assertEqual(snapshot.format, SNAPSHOT_FORMAT)


if __name__ == "__main__":
    unittest.main()
