"""Admission and production supervisor isolation through real mixed scans."""

from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.maven import scan_maven
from libyears.maven_model import MavenReason
from libyears.maven_protocol import available
from libyears.output import report_to_dict
from libyears.scan import scan_mixed_repository
from libyears.maven_supervisor import _DEFERRED
from tests.sbom_fixtures import DocumentReader
from test_maven_worker import WorkerHarness
from test_maven_scan import Reader
from test_maven_project import pom, dependencies, dependency
from test_sbom_document import synthetic_document
from test_sbom_identity import maven_component


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()

    def test_subject_and_cross_variant_namespace_restrictions_before_factory(self):
        private = maven_component(suffix='?repository_url=https:%2F%2Fprivate.invalid%2Fmaven2')
        values = [synthetic_document(components=[private, maven_component(version='2')]),
                  synthetic_document(components=[private, maven_component(suffix='?classifier=sources')]),
                  synthetic_document(metadata={'component': dict(private, **{'bom-ref': 'root'})},
                                     components=[maven_component('unrelated')])]
        for value in values:
            forbidden = Mock(side_effect=AssertionError('metadata'))
            with patch('socket.socket', side_effect=AssertionError('socket')), patch('subprocess.Popen', side_effect=AssertionError('process')):
                report = scan_mixed_repository(self.root, maven_scan=lambda *a, **k: None,
                    sbom_reader_factory=DocumentReader({'bom.json': value}), sbom_supervisor_factory=forbidden)
            section = report_to_dict(report, 'fixture')['sbom']
            self.assertTrue(all(row['reason'] == 'sbom_comparator_refused' for row in section['components']))
            self.assertEqual(section['summary']['dependencies_measured'], 0)
            self.assertEqual(report.source_errors, ())
            forbidden.assert_not_called()

    @unittest.skipUnless(available(), 'native safe protocol primitives unavailable')
    def test_unreaped_ordinary_worker_prevents_second_worker_in_mixed_scan(self):
        self.assertEqual(_DEFERRED, [])
        harness = WorkerHarness(respond=False)
        harness.process.wait = Mock(side_effect=subprocess.TimeoutExpired('trusted', .5))
        ordinary = []
        def supervisor(capabilities, **kwargs):
            instance = harness.supervisor(capabilities, **kwargs)
            ordinary.append(instance)
            return instance
        def maven(root, **kwargs):
            return scan_maven(root, reader_factory=lambda root: Reader({'pom.xml': pom(dependencies(
                dependency('a', '<version>1</version>', group='g')))}), supervisor_factory=supervisor)
        reader = DocumentReader({'bom.json': synthetic_document(components=[maven_component(version='1')])})
        try:
            with patch('libyears.maven_supervisor.tempfile.mkdtemp', wraps=tempfile.mkdtemp) as staged, \
                    patch('socket.socket', side_effect=AssertionError('socket')):
                report = scan_mixed_repository(self.root, maven_scan=maven, sbom_reader_factory=reader)
            self.assertIn(ordinary[0], _DEFERRED)
            self.assertEqual(len(harness.factory_calls), 1)
            self.assertEqual(staged.call_count, 1)
            self.assertEqual(report.sbom.members[0].reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
            self.assertEqual(report.maven.sources[0].declared.rows[0].declared.reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
        finally:
            if ordinary:
                harness.process.returncode = -9
                harness.process.wait = Mock(return_value=-9)
                self.assertTrue(ordinary[0].reap_deferred())
        self.assertEqual(_DEFERRED, [])
