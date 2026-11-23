"""Verifier behavior only; deterministic tests never read private retained bytes."""

from contextlib import redirect_stderr
from dataclasses import replace
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from libyears.maven import MavenCapability
from libyears.maven_input import filesystem_available
from libyears.maven_model import MavenReason
from libyears.sbom_document import accept_document
from libyears.sbom_identity import canonical_members
from libyears.sbom_measure import measure_members
from tools.verify_sbom_corpus import ControlledMetadata, CORPUS, main
from test_sbom_document import snapshot, synthetic_document
from test_sbom_identity import maven_component


class CorpusToolTests(unittest.TestCase):
    def test_controlled_metadata_uses_existing_parsers_with_visible_failures(self):
        document = accept_document(snapshot(synthetic_document(components=[maven_component(name, version='1') for name in ('a', 'b', 'c')])))
        members = canonical_members(document)
        with patch('socket.socket', side_effect=AssertionError('socket')), patch('subprocess.Popen', side_effect=AssertionError('process')):
            rows = measure_members(members, supervisor_factory=ControlledMetadata)
        self.assertEqual([row.reason for row in rows], [MavenReason.CATALOGUE_UNAVAILABLE, MavenReason.TIME_BASIS_UNAVAILABLE, None])
        self.assertEqual(rows[2].age.libyears, 1.0)
        self.assertEqual(rows[2].age.comparison_version, '9999.0')
        with self.assertRaises(ValueError):
            ControlledMetadata([object()])

    @unittest.skipUnless(filesystem_available(), 'native descriptor primitives unavailable')
    def test_missing_or_corrupt_original_is_incomplete_without_invocation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            for corrupt in (False, True):
                if corrupt:
                    (root / next(iter(CORPUS))).write_bytes(b'not original')
                errors = io.StringIO()
                with patch('tools.verify_sbom_corpus.libyears_main', side_effect=AssertionError('invocation')) as invoke, redirect_stderr(errors):
                    result = main([str(root), str(root / 'output')])
                self.assertEqual(result, 1)
                self.assertNotIn(str(root), errors.getvalue())
                self.assertFalse((root / 'output').exists())
                invoke.assert_not_called()
