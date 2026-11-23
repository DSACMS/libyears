"""Real mixed orchestration and CLI, with explicit offline metadata/input seams."""

from contextlib import redirect_stdout, redirect_stderr
from dataclasses import replace
from functools import partial
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.cli import main
from libyears.maven import MavenCapability, scan_maven
from libyears.maven_input import filesystem_available
from libyears.maven_model import MavenReason
from libyears.maven_supervisor import MavenSupervisor, MavenWorkerFailure
from libyears.output import format_human, report_to_dict
from libyears.sbom_model import SbomRequest, SbomRequestError
from libyears.scan import scan_mixed_repository
from tests.sbom_fixtures import DocumentReader
from test_maven_project import pom, dependencies, dependency
from test_maven_policy import repositories, repo
from test_maven_scan import Metadata, Reader
from test_sbom_document import synthetic_document
from test_sbom_identity import maven_component


def example():
    return synthetic_document(components=[maven_component(version='1'), {}])


class SbomCLITests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.reader = DocumentReader({'bom.json': example()})
        self.metadata = Metadata()
        self.addCleanup(patch.stopall)
        # Ordinary source absence is independently supplied. Native SBOM input
        # and all ecosystem parsers retain their own real-reader tests.
        patch('libyears.scan.read_repository_sources', return_value=()).start()
        patch('socket.socket', side_effect=AssertionError('socket')).start()
        patch('subprocess.Popen', side_effect=AssertionError('process')).start()

    def scanner(self, **options):
        defaults = dict(maven_scan=lambda *a, **k: None, sbom_reader_factory=self.reader,
                        sbom_supervisor_factory=self.metadata)
        defaults.update(options)
        return partial(scan_mixed_repository, **defaults)

    def invoke(self, *args, scan=None):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = main([str(self.root), *args], scan=scan or self.scanner())
        return code, output.getvalue(), errors.getvalue()

    def test_default_real_orchestrator_has_independent_section_and_both_tables(self):
        code, text, errors = self.invoke()
        self.assertEqual((code, errors), (0, ''))
        self.assertTrue(text.startswith('SBOM dependency age\n'))
        self.assertIn('Unmeasurable', text)
        self.assertIn('sbom_identity_missing', text)
        self.assertNotIn(str(self.root), text)
        code, text, errors = self.invoke('--json')
        data = json.loads(text)
        self.assertEqual(data['summary']['dependencies_discovered'], 0)
        self.assertEqual(data['sbom']['summary']['dependencies_discovered'], 2)
        self.assertEqual(data['sbom']['summary']['coverage'], .5)
        self.assertEqual(data['sbom']['summary']['total_libyears'], 1.0)
        self.assertEqual(data['sbom']['document']['source_id'], 'bom.json')
        self.assertNotIn('maven', data)
        self.assertEqual(data['ecosystems'], [])

    def test_explicit_unusual_filename_and_verbose_projection(self):
        self.reader.documents['a/b/c/d/unusual.txt'] = self.reader.documents['bom.json']
        code, text, errors = self.invoke('--sbom', 'a/b/c/d/unusual.txt', '--verbose')
        self.assertEqual((code, errors), (0, ''))
        self.assertEqual(self.reader.reads, ['a/b/c/d/unusual.txt'])
        self.assertIn('"sha256"', text)
        self.assertIn('a/b/c/d/unusual.txt', text)
        self.assertIn('current_checkout_association_not_established', text)

    def test_disable_never_constructs_reader_or_supervisor(self):
        forbidden = Mock(side_effect=AssertionError('SBOM constructed'))
        code, text, errors = self.invoke('--no-sbom', '--json', scan=self.scanner(
            sbom_reader_factory=forbidden, sbom_supervisor_factory=forbidden))
        self.assertEqual(code, 0)
        self.assertNotIn('sbom', json.loads(text))
        forbidden.assert_not_called()

    def test_bad_options_refuse_safely_before_scanning(self):
        for args in (('--sbom', '../unsafe'), ('--sbom', '/private/input'), ('--sbom', 'https://private.invalid'),
                     ('--sbom', 'x', '--sbom', 'y'), ('--sbom', 'x', '--no-sbom'),
                     ('--sbo', '/private/input'), ('--SBOM', '/private/input'), ('--no-sb',),
                     ('--sbom',), ('--no-sbom=private',)):
            scan = Mock(side_effect=AssertionError('scan'))
            code, text, errors = self.invoke(*args, scan=scan)
            with self.subTest(args=args):
                self.assertEqual(code, 1)
                self.assertEqual(text, '')
                self.assertIn('invalid SBOM command line arguments', errors)
                self.assertNotIn('/private/input', errors)
                self.assertNotIn('private.invalid', errors)
                scan.assert_not_called()
        code, text, errors = self.invoke('--j')
        self.assertEqual(code, 0)
        self.assertIn('sbom', json.loads(text))

    def test_explicit_nondirectory_and_direct_file_disable(self):
        target = self.root / 'requirements.txt';target.write_text('')
        forbidden = Mock(side_effect=AssertionError('scan'))
        errors = io.StringIO()
        with redirect_stderr(errors):
            self.assertEqual(main([str(target), '--sbom', 'bom.json'], scan=forbidden), 1)
        forbidden.assert_not_called()
        for options in ([], ['--no-sbom']):
            reader = Mock(side_effect=AssertionError('SBOM reader'))
            output = io.StringIO()
            with redirect_stdout(output):
                code = main([str(target), '--json', *options], scan=self.scanner(sbom_reader_factory=reader))
            self.assertEqual(code, 0)
            self.assertNotIn('sbom', json.loads(output.getvalue()))
            reader.assert_not_called()
        with self.assertRaises(SbomRequestError):
            self.scanner()(target, sbom_request=SbomRequest('bom.json'))

    def test_ambiguous_incomplete_missing_and_malformed_keep_safe_attribution(self):
        self.reader.documents['other.cdx.json'] = b'{}'
        code, text, errors = self.invoke('--json')
        self.assertEqual(json.loads(text)['sbom']['reason'], 'sbom_selection_required')
        self.assertEqual(self.reader.reads, [])
        self.reader.complete = False
        code, text, errors = self.invoke('--json')
        self.assertEqual(json.loads(text)['sbom']['discovery']['candidate_count'], 2)
        self.assertEqual(json.loads(text)['sbom']['reason'], 'sbom_discovery_unavailable')
        for name, reason in (('missing.json', 'sbom_input_unavailable'), ('other.cdx.json', 'sbom_unsupported_format')):
            code, text, errors = self.invoke('--sbom', name, '--json')
            section = json.loads(text)['sbom']
            self.assertEqual(code, 0)
            self.assertEqual(section['reason'], reason)
            self.assertEqual(section['selection']['source_id'], name)
            self.assertIsNone(section['summary']['dependencies_discovered'])

    def test_absent_disabled_and_positive_preserve_every_legacy_json_value(self):
        baseline = self.scanner()(self.root, sbom_request=SbomRequest(disabled=True))
        absent = self.scanner(sbom_reader_factory=DocumentReader())(self.root)
        positive = self.scanner()(self.root)
        self.assertEqual(format_human(baseline, 'fixture'), format_human(absent, 'fixture'))
        data = report_to_dict(positive, 'fixture');data.pop('sbom')
        self.assertEqual(data, report_to_dict(baseline, 'fixture'))
        self.assertEqual(data, report_to_dict(absent, 'fixture'))

    def test_maven_workers_close_before_new_allowance_and_veto_propagates(self):
        documents = {'pom.xml': pom(dependencies(dependency('a', '<version>1</version>', group='g')))}
        ordinary = Metadata()
        def maven(root, **options):
            return scan_maven(root, reader_factory=lambda root: Reader(documents), supervisor_factory=ordinary)
        sbom = Metadata()
        def factory(caps, **options):
            self.assertTrue(ordinary.closed)
            self.assertIsNot(sbom, ordinary)
            return sbom(caps, **options)
        code, text, errors = self.invoke('--json', scan=self.scanner(maven_scan=maven, sbom_supervisor_factory=factory))
        self.assertEqual(code, 0)
        data = json.loads(text)
        self.assertEqual(data['maven']['views']['declared']['summary']['dependencies_measured'], 1)
        self.assertEqual(data['sbom']['summary']['dependencies_measured'], 1)
        self.assertIsNone(data['summary']['dependencies_discovered'])
        self.assertEqual(sbom.options, {'ca_bundle': None})
        self.assertNotIn('_comparator_restrictions', text)
        # A missing-version ordinary policy decision still vetoes the SBOM GA.
        documents['pom.xml'] = pom(dependencies(dependency('a', group='org.example')) + repositories(repo(url='https://private.invalid')))
        forbidden = Mock(side_effect=AssertionError('metadata'))
        code, text, errors = self.invoke('--json', scan=self.scanner(maven_scan=maven, sbom_supervisor_factory=forbidden))
        self.assertEqual(json.loads(text)['sbom']['components'][0]['reason'], 'sbom_comparator_refused')
        forbidden.assert_not_called()

    def test_production_adapter_exact_capabilities_and_failed_start_no_fallback(self):
        wrapped = Mock(wraps=MavenSupervisor)
        with patch('libyears.maven_supervisor.MavenSupervisor', wrapped), patch.object(MavenSupervisor, '_start', side_effect=MavenWorkerFailure()) as start:
            report = self.scanner(sbom_supervisor_factory=None)(self.root, ca_bundle=None)
        self.assertEqual(report.sbom.members[0].reason, MavenReason.METADATA_WORKER_UNAVAILABLE)
        caps = wrapped.call_args.args[0]
        self.assertTrue(all(type(cap) is MavenCapability for cap in caps))
        self.assertEqual(len(caps), 1)
        self.assertEqual(wrapped.call_args.kwargs, {'ca_bundle': None})
        self.assertEqual(start.call_count, 1)
        with patch('libyears.maven_supervisor._DEFERRED', [object()]), patch('libyears.maven_supervisor.available', return_value=True):
            report = self.scanner(sbom_supervisor_factory=None)(self.root)
        self.assertEqual(report.sbom.members[0].reason, MavenReason.METADATA_WORKER_UNAVAILABLE)

    def test_no_admitted_work_never_constructs_production_supervisor(self):
        self.reader.documents['bom.json'] = b'{}'
        with patch('libyears.maven_supervisor.MavenSupervisor', side_effect=AssertionError('constructed')):
            report = self.scanner(sbom_supervisor_factory=None)(self.root)
        self.assertEqual(report.sbom.intake.reason, 'sbom_unsupported_format')
        self.reader.documents['bom.json'] = json.dumps(synthetic_document(components=[{}])).encode()
        with patch('libyears.maven_supervisor.MavenSupervisor', side_effect=AssertionError('constructed')):
            report = self.scanner(sbom_supervisor_factory=None)(self.root)
        self.assertEqual(report.sbom.members[0].reason, 'sbom_identity_missing')

    def test_raw_scan_and_render_errors_are_sanitized(self):
        scan = Mock(side_effect=RuntimeError('/private/root/diagnostic'))
        code, text, errors = self.invoke('--sbom', 'bom.json', scan=scan)
        self.assertEqual(code, 2)
        self.assertNotIn('/private/root', errors)
        with patch('libyears.cli.format_human', side_effect=RuntimeError('/private/render')):
            code, text, errors = self.invoke('--sbom', 'bom.json')
        self.assertEqual(code, 2)
        self.assertNotIn('/private/render', errors)

    @unittest.skipUnless(filesystem_available(), 'native descriptor primitives unavailable')
    def test_native_file_and_explicit_nuget_precision_dispatch(self):
        (self.root / 'bom.json').write_text(json.dumps(example()))
        (self.root / 'App.csproj').write_text('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup></Project>')
        for flags in ([], ['--verbose'], ['--json']):
            code, text, errors = self.invoke('--nuget-project', 'App.csproj', *flags,
                scan=self.scanner(sbom_reader_factory=None))
            self.assertEqual((code, errors), (0, ''))
            if '--json' in flags:
                self.assertIn('nuget', json.loads(text)['ecosystems'])
                self.assertIn('sbom', json.loads(text))
            else:
                self.assertIn('SBOM dependency age', text)
                self.assertIn('NuGet', text)
                self.assertNotIn(str(self.root), text)
