"""Legacy formatter recognition and current ordinary CLI integration witnesses."""

from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from libyears.cli import main
from libyears.nuget_discovery import NuGetRecognition, discovery_available
from libyears.output import format_human, format_json
from libyears.scan import scan_mixed_repository


class RecognitionCompositionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        # Legacy internal API does not request repository NuGet activation.
        self.empty = scan_mixed_repository(self.root)

    def test_zero_candidates_preserves_exact_legacy_human_output(self):
        self.assertEqual(format_human(self.empty, '', nuget_recognition=NuGetRecognition()),
                         format_human(self.empty, ''))

    def test_legacy_formatter_can_still_disclose_unmeasured_filename_candidates(self):
        for names in (('Only.csproj',), ('a/One.csproj', 'b/Two.csproj')):
            output = format_human(self.empty, '', nuget_recognition=NuGetRecognition(candidates=names))
            self.assertIn(f'project candidates: {len(names)}', output)
            self.assertIn('No NuGet measurement was performed.', output)
            self.assertIn('Ecosystems scanned for measurement: none', output)
            for name in names:
                self.assertIn(json.dumps(name), output)

    def test_incomplete_unavailable_and_unsafe_names_are_framed(self):
        for status in ('incomplete', 'unavailable'):
            output = format_human(self.empty, '', nuget_recognition=NuGetRecognition(status))
            self.assertIn('recognition ' + status, output)
            self.assertNotIn('project candidates: 0', output)
        name = 'a/line\n\x1b[31m$(not-a-command)`literal`\u202e.csproj'
        output = format_human(self.empty, '', nuget_recognition=NuGetRecognition(candidates=(name,)))
        self.assertIn(json.dumps(name, ensure_ascii=True), output)
        self.assertNotIn(name, output)
        self.assertEqual([line.strip() for line in output.splitlines() if line.strip().startswith('python3')],
                         ['python3 -m libyears PATH --nuget-project NAME.csproj'])

    def test_legacy_recognition_does_not_mutate_json_or_metric_facts(self):
        before = format_json(self.empty, '')
        for recognition in (NuGetRecognition(candidates=('Only.csproj',)), NuGetRecognition('unavailable')):
            format_human(self.empty, '', nuget_recognition=recognition)
            self.assertEqual(format_json(self.empty, ''), before)
            self.assertEqual(self.empty.summary.dependencies_discovered, 0)


class RecognitionFilesystemIntegrationTests(unittest.TestCase):
    def test_ordinary_cli_attempts_real_candidates_or_reports_capability_refusal(self):
        # Unskipped integration: refusal is a result, not false absence. Real
        # successful traversal/containment witnesses are separately capability gated.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'Only.csproj').write_text('malformed project')
            for disabled in (False, True):
                stdout = io.StringIO()
                with patch('os.supports_dir_fd', set() if disabled else os.supports_dir_fd), \
                        redirect_stdout(stdout):
                    available = discovery_available()
                    self.assertEqual(main([str(root), '--json']), 0)
                data = json.loads(stdout.getvalue())
                self.assertEqual(data['ecosystems'], ['nuget'])
                self.assertIsNone(data['summary']['dependencies_discovered'])
                if available:
                    self.assertEqual(data['nuget_sources'][0]['source_id'], 'Only.csproj')
                    self.assertEqual(data['source_errors'][0]['reason'], 'invalid_nuget_project')
                else:
                    self.assertIsNone(data['nuget_sources'][0]['source_id'])
                    self.assertEqual(data['source_errors'][0]['reason'], 'nuget_discovery_unavailable')
