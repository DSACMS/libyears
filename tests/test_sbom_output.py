"""Safe output and committed section-shape witnesses from synthetic inputs."""

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import unittest
from unittest.mock import Mock

from libyears.maven_model import MavenReason
from libyears.sbom import scan_sbom
from libyears.sbom_input import intake_sbom
from libyears.sbom_model import SbomDiscovery, SbomIntake, SbomReport, SbomSelection, SbomRequest
from libyears.sbom_measure import summarize_members
from libyears.sbom_output import format_sbom, sbom_to_dict
from tests.test_sbom_document import synthetic_document
from tests.test_sbom_identity import maven_component
from tests.test_sbom_pipeline import InjectedReader
from test_maven_scan import Metadata


class OutputTests(unittest.TestCase):
    def scan(self, value, metadata=None):
        return scan_sbom('unused', SbomRequest('bom.json'), reader_factory=InjectedReader(value),
                         supervisor_factory=metadata or Metadata())

    def test_committed_example_shapes_from_matching_inputs(self):
        record = {'group': 'example', 'name': 'component', 'version': '1.0',
                  'purl': 'pkg:maven/example/component@1.0', 'bom-ref': 'member'}
        value = synthetic_document(metadata={'component': {'name': 'Synthetic fixture', 'bom-ref': 'root'}}, components=[record],
                                   dependencies=[{'ref': 'root', 'dependsOn': ['member']}, {'ref': 'member', 'dependsOn': []}])
        from test_maven_scan import RETRIEVED
        from libyears.maven_registry import MavenTarget
        old = datetime(2021, 1, 1, tzinfo=timezone.utc)
        new = old + timedelta(days=365.25)
        retrieved = datetime(2026, 11, 20, tzinfo=timezone.utc)
        metadata = Metadata(dates={('component', '1.0'): old, ('component', '2.0'): new})
        metadata.select_target = lambda cap: MavenTarget(cap.group_id, cap.artifact_id, '2.0', retrieved)
        actual = sbom_to_dict(self.scan(value, metadata))
        path = Path('specs/008-local-sbom-age/examples')
        expected = json.loads((path / 'accepted.json').read_text())
        # Placeholder digest is intentionally not asserted to be a real hash.
        self.assertNotEqual(actual['document']['sha256'], expected['document']['sha256'])
        actual['document']['sha256'] = expected['document']['sha256']
        self.assertEqual(actual, expected)
        del value['dependencies']
        actual = sbom_to_dict(self.scan(value, Metadata(targets={'component': MavenReason.CATALOGUE_UNAVAILABLE})))
        expected = json.loads((path / 'partial.json').read_text())
        actual['document']['sha256'] = expected['document']['sha256']
        self.assertEqual(actual, expected)
        intake = SbomIntake(SbomDiscovery('explicit', 'bypassed', None, None), SbomSelection('explicit', 'selected', 'bom.json'), reason='sbom_invalid_json')
        actual = sbom_to_dict(SbomReport(intake, summary=summarize_members(None)))
        self.assertEqual(actual, json.loads((path / 'refused.json').read_text()))

    def test_safe_projection_withholds_hostile_assertions_and_raw_refs(self):
        value = synthetic_document(metadata={'component': {'name': 'bad\x1bsubject@example.invalid', 'bom-ref': 'https://subject.invalid'},
                                             'tools': [{'name': '/absolute/path', 'version': 'who@example.invalid'}]},
                                   components=[{'name': '/absolute/path', 'bom-ref': 'https://ref.invalid'},
                                               maven_component(version='1', **{'bom-ref': 'https://coord.invalid'})],
                                   dependencies=[{'ref': 'https://subject.invalid', 'dependsOn': ['https://coord.invalid']}],
                                   externalReferences=[{'type': 'distribution', 'url': 'https://never.invalid'}])
        report = self.scan(value)
        for text in (json.dumps(sbom_to_dict(report)), format_sbom(report), format_sbom(report, verbose=True)):
            for forbidden in ('\x1b', 'https://', '/absolute/path', '@example.invalid', 'who@'):
                self.assertNotIn(forbidden, text)
        self.assertIn('component #0', format_sbom(report))
        self.assertIn('sbom_assertion_redacted', sbom_to_dict(report)['limitations'])

    def test_variants_and_escaped_table_widths(self):
        report = self.scan(synthetic_document(components=[maven_component(version='1', suffix='?type=pom'),
                                                         maven_component(version='1', suffix='?classifier=sources'),
                                                         {'name': 'long"quoted"label', 'version': '1'}]))
        text = format_sbom(report)
        self.assertIn('org.example:a:pom', text)
        self.assertIn('org.example:a:sources', text)
        self.assertIn('long\\"quoted\\"label', text)
        lines = text.split('Unmeasurable\n')[1].splitlines()
        self.assertEqual(lines[0].index('VERSION'), lines[1].index('1'))

    def test_unselected_and_discovery_status_shapes(self):
        for discovery, selection, reason in (
            (SbomDiscovery('automatic', 'complete', 2, True), SbomSelection('automatic', 'required'), 'sbom_selection_required'),
            (SbomDiscovery('automatic', 'incomplete', 1, False, 'sbom_discovery_unavailable'), SbomSelection('automatic', 'unavailable'), 'sbom_discovery_unavailable')):
            report = SbomReport(SbomIntake(discovery, selection, reason=reason), summary=summarize_members(None))
            section = sbom_to_dict(report)
            self.assertIsNone(section['population'])
            self.assertEqual(section['graph']['reason'], None)
            self.assertEqual(section['reason_counts']['graph'], [])
            self.assertIn(reason, format_sbom(report))
