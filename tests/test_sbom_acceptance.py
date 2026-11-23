"""Checkpoint composition/ceiling witnesses; no private corpus or live metadata."""

from contextlib import nullcontext
from dataclasses import replace
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.maven import scan_maven
from libyears.maven_input import filesystem_available
from libyears.maven_model import MavenReason
from libyears.model import NuGetPublication, RegistryResult
from libyears.nuget_supervisor import PackageResult
from libyears.output import format_human, report_to_dict
from libyears.sbom_input import intake_sbom
from libyears.sbom_json import decode_document
from libyears.sbom_model import SbomFailure, SbomRequest
from libyears.scan import NuGetRequest, scan_mixed_repository
from tests.sbom_fixtures import DocumentReader
from tests.nuget_fixtures import fixture_nuget_reads
from tests.test_nuget_sources import repository_inputs
from tests.test_nuget_scan import nuget_inputs
from test_maven_project import pom, dependency, dependencies
from test_maven_scan import Metadata, Reader, OLD, NEW
from test_sbom_document import synthetic_document
from test_sbom_identity import maven_component


class SiblingProjectionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.addCleanup(patch.stopall)
        patch('socket.socket', side_effect=AssertionError('socket')).start()
        patch('subprocess.Popen', side_effect=AssertionError('process')).start()

    def inputs(self, state):
        (self.root / 'requirements.txt').write_text('' if state == 'empty' else 'python-package==1\n')
        (self.root / 'package.json').write_text('{' if state == 'unknown' else json.dumps({'dependencies': {} if state == 'empty' else {'npm-package': '1.0.0'}}))
        (self.root / 'package-lock.json').write_text(json.dumps({'lockfileVersion': 3, 'packages': {} if state == 'empty' else {'node_modules/npm-package': {'version': '1.0.0'}}}))
        (self.root / 'Gemfile.lock').write_text('bad lock' if state == 'unknown' else
            'GEM\n  remote: https://rubygems.org/\n  specs:\n' + ('' if state == 'empty' else '    ruby-package (1.0.0)\n') +
            '\nPLATFORMS\n  ruby\n\nDEPENDENCIES\n' + ('' if state == 'empty' else '  ruby-package\n'))
        files = nuget_inputs(() if state == 'empty' else ('alpha',))
        if state == 'unknown':
            files['Witness.csproj'] = b'broken'
        return files

    def scan(self, files, mode, legacy_state, sbom_state):
        options = {}
        if mode == 'precision':
            context = fixture_nuget_reads(self.root, files)
            options['nuget_request'] = NuGetRequest('Witness.csproj', 'witness.json')
        else:
            context = repository_inputs(self.root, {'a/Witness.csproj': files})
            options.update(nuget_repository=True, nuget_witnesses=(('a/Witness.csproj', 'witness.json'),))
        value = synthetic_document(components=[maven_component(version='1'), {}])
        reader = DocumentReader({} if sbom_state in ('absent', 'disabled') else {'bom.json': value})
        metadata = Metadata()
        if sbom_state == 'partial_exhausted':
            reader = DocumentReader({'bom.json': synthetic_document(components=[maven_component(version='1'), maven_component('b', version='1'), {}])})
            metadata = Metadata(targets={'b': MavenReason.METADATA_BUDGET_EXCEEDED})
        if sbom_state == 'refused':
            reader.documents['bom.json'] = b'{"late":{"x":1,"x":2}}'
        if sbom_state == 'empty':
            reader = DocumentReader({'bom.json': synthetic_document()})
        if sbom_state == 'incomplete':
            reader.complete = False
        if sbom_state == 'exhausted':
            metadata = Metadata(targets={'a': MavenReason.METADATA_BUDGET_EXCEEDED})
        def maven(root, **kwargs):
            body = '' if legacy_state == 'empty' else dependencies(dependency('maven-package', '<version>1</version>', group='g'))
            return scan_maven(root, reader_factory=lambda root: Reader({'pom.xml': pom(body)}, complete=legacy_state != 'unknown'), supervisor_factory=Metadata())
        def lookup(name, version):
            return RegistryResult(name, version, OLD, '2', NEW)
        def nuget_lookup(authorities):
            return tuple((authority, PackageResult(origin_state='public_content_verified', content_hash_state='public_agreement',
                         used_publication=NuGetPublication(authority.normalized_version, OLD, True),
                         latest_publication=NuGetPublication('2.0.0', NEW, True))) for authority in authorities)
        with context:
            report = scan_mixed_repository(self.root, pypi_lookup=lookup, npm_lookup=lookup, rubygems_lookup=lookup,
                nuget_lookup=nuget_lookup, maven_scan=maven, sbom_reader_factory=reader, sbom_supervisor_factory=metadata,
                sbom_request=SbomRequest(disabled=sbom_state == 'disabled'), **options)
        return report

    def test_frozen_full_sibling_projection_matrix(self):
        for mode in ('precision', 'ordinary'):
            for legacy in ('measured', 'empty', 'unknown'):
                files = self.inputs(legacy)
                baseline = self.scan(files, mode, legacy, 'disabled')
                frozen = report_to_dict(baseline, 'selected repository')
                for state in ('absent', 'positive', 'refused', 'empty', 'incomplete', 'exhausted', 'partial_exhausted'):
                    with self.subTest(mode=mode, legacy=legacy, sbom=state):
                        report = self.scan(files, mode, legacy, state)
                        actual = report_to_dict(report, 'selected repository')
                        section = actual.pop('sbom', None)
                        self.assertEqual(actual, frozen)
                        self.assertEqual(report.measurements, baseline.measurements)
                        self.assertEqual(report.unmeasurable, baseline.unmeasurable)
                        self.assertEqual(report.source_errors, baseline.source_errors)
                        self.assertEqual(report.summary, baseline.summary)
                        if state == 'absent':
                            self.assertIsNone(section)
                            self.assertEqual(format_human(report, 'fixture'), format_human(baseline, 'fixture'))
                        else:
                            for verbose in (False, True):
                                self.assertIn(format_human(baseline, 'selected repository', verbose=verbose),
                                              format_human(report, '/private/root', verbose=verbose))
                        if state == 'partial_exhausted':
                            self.assertEqual(section['summary']['dependencies_discovered'], 3)
                            self.assertEqual(section['summary']['dependencies_measured'], 1)
                            self.assertEqual(section['summary']['total_libyears'], 1.0)
                            self.assertEqual(section['components'][1]['reason'], 'maven_metadata_budget_exceeded')
                        if state == 'exhausted':
                            self.assertEqual(section['summary']['dependencies_discovered'], 2)
                            self.assertEqual(section['summary']['dependencies_measured'], 0)
                            self.assertEqual(section['components'][0]['reason'], 'maven_metadata_budget_exceeded')
                if legacy == 'measured':
                    self.assertEqual({m.dependency.ecosystem for m in baseline.measurements}, {'pypi', 'npm', 'rubygems', 'nuget'})
                    self.assertEqual(baseline.maven.summaries.declared.summary.dependencies_measured, 1)
                    self.assertIsNone(baseline.maven.summaries.observed.summary.dependencies_discovered)

    def test_unknown_failure_and_accepted_empty_remain_presentation_relevant(self):
        for state in ('unknown', 'empty'):
            report = self.scan(self.inputs(state), 'ordinary', state, 'positive')
            text = format_human(report, 'fixture')
            self.assertTrue(text.startswith('Existing source populations (SBOM excluded):'))
            self.assertIn('SBOM dependency age', text)
            self.assertNotIn('Libyears: fixture', text)


class FramingBoundaryTests(unittest.TestCase):
    def test_exact_token_and_utf8_string_ceiling(self):
        values = [[0] * 20_000 for unused in range(12)] + [[0] * 9984]
        decode_document(json.dumps({'x': values}).encode())  # 250000 tokens
        values[-1].append(0)
        with self.assertRaises(SbomFailure) as caught:
            decode_document(json.dumps({'x': values}).encode())
        self.assertEqual(caught.exception.reason, 'sbom_budget_exceeded')
        decode_document(json.dumps({'x': 'é' * 8192}).encode())
        with self.assertRaises(SbomFailure):
            decode_document(json.dumps({'x': 'é' * 8193}).encode())


@unittest.skipUnless(filesystem_available(), 'native descriptor primitives unavailable')
class NativeCeilingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()

    def test_actual_entry_ceiling_and_observed_candidate(self):
        (self.root / 'bom.json').write_bytes(b'{}')
        for index in range(9999):
            (self.root / f'entry-{index:05}').touch()
        self.assertIsNotNone(intake_sbom(self.root).snapshot)
        (self.root / 'extra').touch()
        result = intake_sbom(self.root)
        self.assertEqual(result.reason, 'sbom_discovery_unavailable')
        self.assertFalse(result.discovery.search_complete)

    def test_actual_directory_ceiling(self):
        (self.root / 'bom.json').write_bytes(b'{}')
        for index in range(127):
            (self.root / f'd-{index:03}').mkdir()
        self.assertIsNotNone(intake_sbom(self.root).snapshot)
        (self.root / 'overflow').mkdir()
        self.assertEqual(intake_sbom(self.root).reason, 'sbom_discovery_unavailable')

    def test_actual_file_byte_ceiling_and_no_oversize_read(self):
        (self.root / 'bom.json').write_bytes(b' ' * (8 * 1024 * 1024))
        self.assertEqual(len(intake_sbom(self.root).snapshot.data), 8 * 1024 * 1024)
        (self.root / 'bom.json').write_bytes(b' ' * (8 * 1024 * 1024 + 1))
        with patch('os.read', side_effect=AssertionError('oversize read')):
            self.assertEqual(intake_sbom(self.root).reason, 'sbom_budget_exceeded')
