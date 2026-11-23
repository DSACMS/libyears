"""Synthetic local files and controlled dates; no real package-age evidence."""

from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.maven_input import filesystem_available
from libyears.maven_model import MavenReason
from libyears.maven_registry import MavenTarget, MavenPomDate
from libyears.sbom import scan_sbom
from libyears.sbom_model import SbomRequest
from libyears.sbom_output import format_sbom, format_sbom_json, sbom_to_dict
from tests.test_sbom_document import synthetic_document, snapshot
from tests.test_sbom_identity import maven_component
from test_maven_scan import Metadata


class InjectedReader:
    def __init__(self, value):
        self.value = snapshot(value)
    def __call__(self, root):
        return self
    def __enter__(self):
        return self
    def __exit__(self, *unused):
        pass
    def snapshot(self, name):
        from dataclasses import replace
        return replace(self.value, source_id=name)


class PipelineTests(unittest.TestCase):
    def scan(self, value, metadata=None):
        with patch('socket.socket', side_effect=AssertionError('socket')), patch('subprocess.Popen', side_effect=AssertionError('process')):
            return scan_sbom('unused', SbomRequest('bom.json'), reader_factory=InjectedReader(value),
                             supervisor_factory=metadata or Metadata())

    def test_portable_summary_table_and_json(self):
        value = synthetic_document(components=[maven_component(version='1'), {}])
        report = self.scan(value)
        section = sbom_to_dict(report)
        self.assertEqual(section['state'], 'partial')
        self.assertEqual((section['summary']['dependencies_discovered'], section['summary']['dependencies_measured'], section['summary']['coverage']), (2, 1, .5))
        self.assertEqual(section['summary']['total_libyears'], 1.0)
        text = format_sbom(report)
        self.assertIn('Unmeasurable', text)
        self.assertIn('sbom_identity_missing', text)
        self.assertIn('org.example:a', text)
        self.assertEqual(json.loads(format_sbom_json(report)), section)
        self.assertNotIn('Observed', text)

    @unittest.skipUnless(filesystem_available(), 'native descriptor primitives unavailable')
    def test_real_regular_file_end_to_end(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            data = json.dumps(synthetic_document(components=[maven_component(version='1'), {}])).encode()
            (root / 'bom.json').write_bytes(data)
            with patch('socket.socket', side_effect=AssertionError('socket')), patch('subprocess.Popen', side_effect=AssertionError('process')):
                report = scan_sbom(root, supervisor_factory=Metadata())
            section = sbom_to_dict(report)
            self.assertEqual(section['document']['sha256'], hashlib.sha256(data).hexdigest())
            self.assertEqual(section['summary']['coverage'], .5)
            self.assertEqual(section['summary']['total_libyears'], 1.0)
            self.assertIn('Unmeasurable', format_sbom(report))
            self.assertIn('"dependencies_measured": 1', format_sbom_json(report))

    def test_all_refused_empty_and_source_refused(self):
        for value, discovered, coverage in ((synthetic_document(), 0, None), (synthetic_document(components=[{}]), 1, 0.0)):
            factory = Mock(side_effect=AssertionError('metadata'))
            section = sbom_to_dict(self.scan(value, factory))
            self.assertEqual(section['summary']['dependencies_discovered'], discovered)
            self.assertEqual(section['summary']['coverage'], coverage)
            self.assertEqual(section['summary']['total_libyears'], 0.0)
            factory.assert_not_called()
        section = sbom_to_dict(self.scan(synthetic_document(specVersion='1.6'), Mock(side_effect=AssertionError('metadata'))))
        self.assertEqual(section['reason'], 'sbom_unsupported_format')
        self.assertIsNone(section['population'])
        self.assertTrue(all(value is None for value in section['summary'].values()))

    def test_representative_corpus_identity_with_synthetic_dates(self):
        # Identity only from retained hash-bound Dependency-Track4.13.4 corpus:
        # c201f3a64e7b2c510b83fe99dd6e945244030c6484009100b04a257721dba790.
        # The controlled dates and comparison version are deliberately synthetic.
        row = {'group': 'us.springett', 'name': 'alpine-common', 'version': '3.2.0',
               'purl': 'pkg:maven/us.springett/alpine-common@3.2.0?type=jar'}
        section = sbom_to_dict(self.scan(synthetic_document(components=[row])))
        self.assertEqual(section['components'][0]['age']['libyears'], 1.0)
        self.assertEqual(section['components'][0]['identity']['version'], '3.2.0')

    def test_late_invalid_framing_prohibits_metadata(self):
        reader = InjectedReader(synthetic_document())
        from dataclasses import replace
        reader.value = replace(reader.value, data=b'{"ignored":{"a":1,"a":2}}')
        factory = Mock(side_effect=AssertionError('metadata'))
        result = scan_sbom('unused', SbomRequest('bom.json'), reader_factory=reader, supervisor_factory=factory)
        self.assertEqual(result.intake.reason, 'sbom_invalid_json')
        factory.assert_not_called()

    def test_disabled_factory_never_constructed(self):
        forbidden = Mock(side_effect=AssertionError('constructed'))
        self.assertIsNone(scan_sbom('unused', SbomRequest(disabled=True), reader_factory=forbidden, supervisor_factory=forbidden))
        forbidden.assert_not_called()

    def test_document_namespace_vetoes_precede_factory_and_preserve_independent_rows(self):
        private = maven_component(version='1', suffix='?repository_url=https:%2F%2Fprivate.invalid%2Fmaven2')
        forbidden = Mock(side_effect=AssertionError('metadata'))
        value = synthetic_document(components=[private, maven_component(version='2')])
        section = sbom_to_dict(self.scan(value, forbidden))
        self.assertEqual(section['summary']['dependencies_discovered'], 2)
        self.assertEqual(section['summary']['dependencies_measured'], 0)
        forbidden.assert_not_called()
        value['components'].append(maven_component('independent', version='1'))
        metadata = Metadata()
        section = sbom_to_dict(self.scan(value, metadata))
        self.assertEqual(section['summary']['dependencies_measured'], 1)
        self.assertEqual([cap.artifact_id for cap in metadata.capabilities], ['independent'])
        value = synthetic_document(metadata={'component': {**private, 'bom-ref': 'root'}},
                                   components=[maven_component('independent')])
        section = sbom_to_dict(self.scan(value, forbidden))
        self.assertEqual(section['components'][0]['reason'], 'sbom_comparator_refused')
        forbidden.assert_not_called()
