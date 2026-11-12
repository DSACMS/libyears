"""T011 integrated adversarial shapes from retained DPC/AB2D discovery.

Synthetic populations are deliberate small counterexamples, never target counts or
live operational evidence. No real target, build tool, registry or Gradle reader runs.
"""

from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.maven import scan_maven
from libyears.maven_input import MavenInputReader, filesystem_available
from libyears.maven_model import MavenReason
from libyears.maven_registry import select_target, pom_date
from libyears.output import format_human, report_to_dict
from libyears.scan import scan_mixed_repository
from test_maven_project import pom, dependencies, dependency, parent, modules, management
from test_maven_policy import repositories, repo, profiles
from test_maven_scan import Reader, Metadata, row
from test_maven_registry import catalogue, response, POM


def dpc_shape(*, extension=False, uncertain_internal=False):
    # Retained DPC shapes: module inheritance, unread BOMs, explicit runtime
    # classifier/tooling, child file repositories and a build extension.
    shared = dependency('shared', group='external')
    tooling = dependency('tool', '<version>${tool.version}</version><scope>provided</scope>'
                         '<optional>true</optional><classifier>runtime</classifier>', group='external')
    internal = dependency('left', '<version>1</version>', group='g')
    bom = management(dependency('bom', '<version>1</version><type>pom</type><scope>import</scope>', group='external'))
    root = ('<packaging>pom</packaging><properties><tool.version>1</tool.version></properties>'
            + modules('left', 'right') + bom + dependencies(shared, tooling, internal))
    if extension:
        root += '<build><extensions><extension><artifactId>cache</artifactId></extension></extensions></build>'
    left = parent() + repositories(repo('local-eligible', 'file:///never/read'))
    if uncertain_internal:
        left += profiles('<version>2</version>')
    return {'pom.xml': pom(root), 'left/pom.xml': pom(left, artifact='left'),
            'right/pom.xml': pom(parent(), artifact='right')}


class MavenIntegratedAcceptanceTests(unittest.TestCase):
    def scan(self, documents, *, metadata=None, complete=True, reader=None):
        self.reader = reader or Reader(documents, complete=complete)
        self.metadata = metadata or Metadata()
        return scan_maven('fixture', reader_factory=lambda root: self.reader,
                          supervisor_factory=self.metadata)

    def test_dpc_shaped_inheritance_bom_tooling_classifier_and_file_eligibility(self):
        report = self.scan(dpc_shape())
        summary = report.summaries.declared.summary
        self.assertEqual((summary.dependencies_discovered, summary.dependencies_measured,
                          summary.coverage, summary.total_libyears), (6, 3, .5, 3.0))
        self.assertEqual([call for call in self.metadata.calls if call[0] == 'target'],
                         [('target', 'external', 'tool')])
        for source in report.sources:
            rows = source.declared.rows
            self.assertEqual({item.key.model_key.artifact_id for item in rows}, {'shared', 'tool'})
            tool = next(item for item in rows if item.key.model_key.artifact_id == 'tool')
            self.assertEqual((tool.scope, tool.optional, tool.artifact_key.classifier), ('provided', True, 'runtime'))
            self.assertEqual(tool.declared.request, '${tool.version}')
            self.assertIsNone(source.observed.population_count)
            self.assertFalse(source.observed.accepted)

    def test_dpc_shaped_extension_refuses_all_lookup_without_erasing_population(self):
        factory = Mock(side_effect=AssertionError('extension cannot enable metadata'))
        report = scan_maven('fixture', reader_factory=lambda root: Reader(dpc_shape(extension=True)),
                            supervisor_factory=factory)
        summary = report.summaries.declared.summary
        self.assertEqual((summary.dependencies_discovered, summary.dependencies_measured,
                          summary.coverage, summary.total_libyears), (6, 0, 0.0, 0.0))
        factory.assert_not_called()
        for source in report.sources:
            tool = next(item for item in source.declared.rows if item.key.model_key.artifact_id == 'tool')
            self.assertEqual(tool.declared.version, '1')
            self.assertEqual(tool.declared.reason, MavenReason.POLICY_UNKNOWN)

    def test_conditional_internal_version_withholds_n_but_keeps_independent_safe_ages(self):
        report = self.scan(dpc_shape(uncertain_internal=True))
        summary = report.summaries.declared.summary
        self.assertIsNone(summary.dependencies_discovered)
        self.assertIsNone(summary.coverage)
        self.assertEqual((summary.dependencies_measured, summary.total_libyears), (3, 3.0))
        self.assertEqual(len(report.sources), 3)

    def test_all_local_source_checks_finish_before_metadata_batch_is_created(self):
        class Staged(Reader):
            closed = False
            def __exit__(self, *args):
                self.closed = True
        reader = Staged(dpc_shape())
        metadata = Metadata()
        def batch(capabilities, **kwargs):
            self.assertTrue(reader.closed)
            self.assertIn('left/.mvn/maven.config', reader.checks)
            self.assertIn('right/.mvn/settings.xml', reader.checks)
            self.assertTrue(all(cap.artifact_id == 'tool' for cap in capabilities))
            return metadata(capabilities, **kwargs)
        report = scan_maven('fixture', reader_factory=lambda root: reader, supervisor_factory=batch)
        self.assertEqual(report.summaries.declared.summary.dependencies_measured, 3)

    def test_unknown_dependency_field_refuses_affected_key_but_preserves_safe_sibling(self):
        unsupported = dependency('affected', '<version>1</version><futureSelection>2</futureSelection>')
        safe = dependency('safe', '<version>1</version>')
        for unknown in (unsupported, unsupported.replace('<futureSelection>', '<futureSelection xmlns="foreign">')):
            report = self.scan({'pom.xml': pom(dependencies(unknown, safe))})
            summary = report.summaries.declared.summary
            self.assertIsNone(summary.dependencies_discovered)
            self.assertEqual((summary.dependencies_measured, summary.total_libyears), (1, 1.0))
            self.assertEqual([item.key.model_key.artifact_id for item in report.sources[0].declared.rows], ['safe'])
            self.assertFalse(any(call[2] == 'affected' for call in self.metadata.calls))

    def test_unknown_inherited_or_child_dependency_never_revives_convenient_parent_facts(self):
        unknown = dependency('affected', '<version>2</version><futureSelection/>')
        safe = dependency('safe', '<version>1</version>')
        inherited = self.scan({'pom.xml': pom(dependencies(unknown, safe)),
                               'child/pom.xml': pom(parent(), artifact='child')})
        self.assertEqual(inherited.summaries.declared.summary.dependencies_measured, 2)
        self.assertFalse(any(call[2] == 'affected' for call in self.metadata.calls))
        report = self.scan({'pom.xml': pom(dependencies(dependency('affected', '<version>1</version>'), safe)),
                            'child/pom.xml': pom(parent() + dependencies(unknown), artifact='child')})
        child = next(source for source in report.sources if source.context.source_id == 'child/pom.xml')
        self.assertEqual([item.key.model_key.artifact_id for item in child.declared.rows], ['safe'])
        self.assertIsNone(child.declared.population_count)
        self.assertEqual(report.summaries.declared.summary.dependencies_measured, 3)
        self.assertEqual([cap.version for cap in self.metadata.capabilities if cap.artifact_id == 'affected'], ['1'])

    def test_unknown_management_key_blocks_parent_fallback_and_keeps_independent_explicit_fields(self):
        managed = dependency('affected', '<version>1</version>')
        unknown = dependency('affected', '<version>2</version><futureSelection/>')
        direct = dependencies(dependency('affected', '<scope>compile</scope><optional>false</optional>'),
                              dependency('safe', '<version>1</version><scope>compile</scope><optional>false</optional>'))
        report = self.scan({'pom.xml': pom(management(managed)),
                            'child/pom.xml': pom(parent() + management(unknown) + direct, artifact='child')})
        child = next(source for source in report.sources if source.context.source_id == 'child/pom.xml')
        affected = next(item for item in child.declared.rows if item.key.model_key.artifact_id == 'affected')
        self.assertIsNone(affected.declared.version)
        self.assertIsNone(affected.declared.age)
        self.assertEqual(report.summaries.declared.summary.dependencies_measured, 1)
        self.assertFalse(any(call[2] == 'affected' for call in self.metadata.calls))

    def test_bound_selected_credential_settings_refuse_before_batch_and_never_escape_output(self):
        reader = Reader({'pom.xml': pom(dependencies(row()))},
                        controls={'.mvn/maven.config': b'--settings=selected.xml'})
        reader.selected = {'selected.xml': b'<settings><servers><server><password>PRIVATE_SENTINEL</password></server></servers></settings>'}
        factory = Mock(side_effect=AssertionError('credentials cannot create capabilities'))
        maven = scan_maven('fixture', reader_factory=lambda root: reader, supervisor_factory=factory)
        factory.assert_not_called()
        self.assertEqual(maven.sources[0].declared.rows[0].declared.reason, MavenReason.POLICY_UNKNOWN)
        with tempfile.TemporaryDirectory() as directory:
            report = scan_mixed_repository(Path(directory).resolve(), maven_scan=lambda *a, **kw: maven)
        rendered = json.dumps(report_to_dict(report, 'PRIVATE_ABSOLUTE_ROOT')) + format_human(
            report, 'PRIVATE_ABSOLUTE_ROOT', verbose=True)
        self.assertNotIn('PRIVATE_SENTINEL', rendered)
        self.assertNotIn('PRIVATE_ABSOLUTE_ROOT', rendered)
        self.assertNotIn('<settings>', rendered)
        self.assertEqual(report.summary.dependencies_measured, None)
        self.assertEqual(maven.summaries.declared.summary.dependencies_measured, 0)

    def test_pure_registry_refusal_reaches_rows_without_metric_or_older_date_fallback(self):
        class ParsedMetadata(Metadata):
            def select_target(self, cap):
                self.calls.append(('target', cap.group_id, cap.artifact_id))
                return select_target(cap.group_id, cap.artifact_id, response(catalogue(('1', '2'))))
            def pom_date(self, cap, version=None):
                version = version or cap.version
                self.calls.append(('date', cap.group_id, cap.artifact_id, version))
                return pom_date(cap.group_id, cap.artifact_id, version,
                    response(POM.replace(b'<version>1', ('<version>' + version).encode()), headers=()))
        metadata = ParsedMetadata()
        with patch('libyears.metric.libyears_between', side_effect=AssertionError('no admitted dates')):
            report = self.scan({'pom.xml': pom(dependencies(row()))}, metadata=metadata)
        self.assertEqual(report.summaries.declared.summary.coverage, 0.0)
        self.assertEqual(report.sources[0].declared.rows[0].declared.reason, MavenReason.TIME_BASIS_UNAVAILABLE)
        self.assertEqual(metadata.calls, [('target', 'g', 'a'), ('date', 'g', 'a', '2')])

    @unittest.skipUnless(filesystem_available(), 'safe descriptor primitives unavailable')
    def test_ab2d_shaped_maven_gradle_divergence_and_typed_variants_without_gradle_reads(self):
        # Retained AB2D shapes only: external parent, plain/test-jar aliases,
        # ordinary POM dependency and a Gradle request/lock disagreement.
        extra = '<version>1.9</version><scope>test</scope><optional>false</optional>'
        content = parent(path='') + dependencies(
            dependency('common', extra, group='g'),
            dependency('common', extra + '<type>test-jar</type>', group='g'),
            dependency('common', extra + '<classifier>tests</classifier>', group='g'),
            dependency('dependency-pom', extra + '<type>pom</type>', group='g'))
        content += repositories(repo('unassigned', '${environment.repository}'))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / 'pom.xml').write_bytes(pom(content))
            (root / 'build.gradle').write_text('commons-codec:commons-codec:1.9; NEVER_EXECUTE')
            (root / 'gradle.lockfile').write_text('commons-codec:commons-codec:1.21.0=classpath')
            (root / 'settings.xml').write_text('<settings><servers>PRIVATE_UNSELECTED</servers></settings>')
            original = MavenInputReader._snapshot
            with patch.object(MavenInputReader, '_snapshot', autospec=True, side_effect=original) as reads, \
                 patch('subprocess.Popen', side_effect=AssertionError('no external process')), \
                 patch('socket.socket', side_effect=AssertionError('no network')):
                report = scan_maven(root, supervisor_factory=Metadata())
            self.assertEqual({call.args[1] for call in reads.call_args_list}, {'pom.xml'})
        rows = report.sources[0].declared.rows
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(item.declared.version == '1.9' for item in rows))
        self.assertTrue(all(item.observed is None for item in rows))
        self.assertIsNone(report.summaries.declared.summary.dependencies_discovered)
        self.assertIsNone(report.summaries.declared.summary.coverage)
        self.assertEqual(report.summaries.declared.summary.dependencies_measured, 4)
        common = [item for item in rows if item.key.model_key.artifact_id == 'common']
        self.assertEqual(len({item.key for item in common}), 3)
        self.assertEqual([item.artifact_key.classifier for item in common], [None, 'tests', 'tests'])


if __name__ == '__main__':
    unittest.main()
