"""T006 source authority witnesses, with disabled/injected metadata only."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from libyears.maven import admit_sources, admitted_lookups
from libyears.maven_input import (
    MavenInputReader, MavenInputSnapshot, MavenInputFailure, MavenInputIssue,
    filesystem_available, parse_pom, parse_xml,
)
from libyears.maven_model import MavenDiscovery, MavenReason
from libyears.maven_policy import central_url, source_policy
from libyears.maven_project import build_project_graph
from libyears.maven_results import summarize_sources
from test_maven_project import pom, dependency, dependencies, parent

PUBLIC = 'https://repo.maven.apache.org/maven2'
ROW = dependencies(dependency(extra='<version>1</version>'))


def repo(identity='central', url=PUBLIC, extra=''):
    return f'<repository><id>{identity}</id><url>{url}</url>{extra}</repository>'


def repositories(*records):
    return '<repositories>' + ''.join(records) + '</repositories>'


def profiles(body, identity='p'):
    return f'<profiles><profile><id>{identity}</id>{body}</profile></profiles>'


def mirror(expression='*', extra='', identity='m', url='https://mirror.invalid/maven'):
    return (f'<mirror><id>{identity}</id><url>{url}</url><mirrorOf>{expression}</mirrorOf>'
            + extra + '</mirror>')


def settings(body='', namespace=None):
    attribute = f' xmlns="{namespace}"' if namespace else ''
    return f'<settings{attribute}>{body}</settings>'.encode()


class StagedReader:
    """Only exact sentinels/explicit selection may be read in semantic fixtures."""

    def __init__(self, controls=None, selected=None):
        self.controls = controls or {}
        self.selected = selected or {}
        self.reads = []
        self.checks = []

    def control_present(self, path):
        self.checks.append(path)
        return path in self.controls

    def snapshot_control(self, path):
        self.reads.append(path)
        data = self.controls[path]
        return MavenInputSnapshot(path, data, ('safe-fixture',),
                                  parse_xml(data) if path.endswith('.xml') else None)

    def snapshot_selected_settings(self, path):
        self.reads.append(path)
        if path not in self.selected:
            raise MavenInputFailure(MavenInputIssue.MISSING)
        data = self.selected[path]
        return MavenInputSnapshot(path, data, ('safe-fixture',), parse_xml(data))


def graph(documents):
    snapshots = {name: MavenInputSnapshot(name, data, ('safe-fixture',), parse_pom(data))
                 for name, data in documents.items()}
    return build_project_graph(MavenDiscovery(True, tuple(documents)), snapshots.__getitem__)


class MavenPolicyTests(unittest.TestCase):
    def decision(self, body='', controls=None, selected=None):
        return source_policy(graph({'pom.xml': pom(ROW + body)}), 'pom.xml',
                             StagedReader(controls, selected))

    def settings_decision(self, body='', namespace=None):
        return self.decision(controls={'.mvn/maven.config': b'--settings=policy.xml'},
                             selected={'policy.xml': settings(body, namespace)})

    def test_no_policy_and_unassigned_alternates_admit_without_reading_endpoints(self):
        for body in ('', repositories(repo('private', 'file:///secret')),
                     repositories(repo('other', '${private.url}')),
                     repositories(repo('central2', 'http://example.invalid')),
                     profiles(repositories(repo('alternate', '${unknown}'))),
                     '<pluginRepositories>' + repo(url='file:///private') + '</pluginRepositories>',
                     '<distributionManagement>' + repo(url='file:///private') + '</distributionManagement>'):
            with self.subTest(body=body):
                self.assertTrue(self.decision(body).admitted)

    def test_literal_central_recognition(self):
        for url in (PUBLIC, PUBLIC + '/', 'https://REPO1.MAVEN.ORG:443/maven2'):
            self.assertTrue(central_url(url))
        for url in ('http://repo.maven.apache.org/maven2', PUBLIC + '?', PUBLIC + '#',
                    PUBLIC + '/extra', 'https://repo.maven.apache.org.attacker/maven2',
                    'https://name:secret@repo.maven.apache.org/maven2', PUBLIC + ':80',
                    'https://repo.maven.apache.org:444/maven2', '${central}'):
            with self.subTest(url=url):
                self.assertFalse(central_url(url))
                self.assertFalse(self.decision(repositories(repo(url=url))).admitted)

    def test_central_exclusions_and_malformed_relevant_policy(self):
        for extra in ('<releases><enabled>false</enabled></releases>',
                      '<layout>legacy</layout>', '<layout>${layout}</layout>',
                      '<releases><enabled>${flag}</enabled></releases>',
                      '<releases><enabled>true</enabled><enabled>false</enabled></releases>',
                      '<unknown/>', '<url>https://other.invalid</url>'):
            with self.subTest(extra=extra):
                self.assertFalse(self.decision(repositories(repo(extra=extra))).admitted)
        for body in (repositories(repo(), repo()), '<repositories><repository><url>x</url></repository></repositories>',
                     '<repositories><repository><id>${id}</id></repository></repositories>',
                     '<repositories><repository xmlns="foreign"><id>central</id></repository></repositories>'):
            self.assertFalse(self.decision(body).admitted)

    def test_child_whole_record_dominates_parent_without_field_merge(self):
        g = graph({'pom.xml': pom(repositories(repo(extra='<releases><enabled>false</enabled></releases>'))),
                   'child/pom.xml': pom(parent() + ROW + repositories(repo()), artifact='child')})
        self.assertTrue(source_policy(g, 'child/pom.xml', StagedReader()).admitted)
        self.assertFalse(source_policy(g, 'pom.xml', StagedReader()).admitted)
        g = graph({'pom.xml': pom(repositories(repo())),
                   'child/pom.xml': pom(parent() + ROW + repositories(repo(url='${url}')), artifact='child')})
        self.assertFalse(source_policy(g, 'child/pom.xml', StagedReader()).admitted)

    def test_duplicate_repository_records_refuse_only_effective_or_possible_central(self):
        alternate_duplicates = repositories(repo('other', 'file:///never/read'), repo('other', '${url}'))
        self.assertTrue(self.decision(alternate_duplicates).admitted)
        self.assertTrue(self.decision(profiles(alternate_duplicates)).admitted)
        self.assertTrue(self.settings_decision(profiles(alternate_duplicates)).admitted)
        duplicate_central = repositories(repo(), repo(url='https://private.invalid'))
        g = graph({'pom.xml': pom(ROW + duplicate_central),
                   'child/pom.xml': pom(parent() + repositories(repo()), artifact='child')})
        admission = admit_sources(g, StagedReader())
        lookup = Mock(return_value='fixed-result')
        results = admitted_lookups(admission, lookup)
        self.assertEqual([key.source_id for key, result in results], ['child/pom.xml'])
        self.assertEqual(lookup.call_count, 1)
        self.assertEqual([s.declared.population_count for s in admission.sources], [1, 1])
        self.assertFalse(self.decision(duplicate_central).admitted)
        self.assertFalse(self.decision(profiles(duplicate_central)).admitted)
        self.assertFalse(self.settings_decision(profiles(duplicate_central)).admitted)
        # Parent profile possibilities remain relevant despite a child override.
        g = graph({'pom.xml': pom(profiles(duplicate_central)),
                   'child/pom.xml': pom(parent() + ROW + repositories(repo()), artifact='child')})
        self.assertFalse(source_policy(g, 'child/pom.xml', StagedReader()).admitted)

    def test_every_possible_profile_is_checked_without_activation(self):
        for central in (repo(url='https://private.invalid'), repo(extra='<releases><enabled>false</enabled></releases>')):
            g = graph({'pom.xml': pom(profiles(repositories(central))),
                       'child/pom.xml': pom(parent() + ROW + repositories(repo()), artifact='child')})
            self.assertFalse(source_policy(g, 'child/pom.xml', StagedReader()).admitted)
        self.assertTrue(self.decision(profiles(repositories(repo()))).admitted)
        self.assertFalse(self.decision(profiles('') + profiles('')).admitted)

    def test_missing_external_parent_does_not_veto_independent_safe_rows(self):
        g = graph({'pom.xml': pom(parent(path='') + dependencies(dependency(
            extra='<version>1</version><scope>compile</scope><optional>false</optional>')))})
        result = admit_sources(g, StagedReader())
        self.assertEqual(len(result.capabilities), 1)
        self.assertIsNone(result.sources[0].declared.population_count)

    def test_colocated_settings_never_opened_or_trusted(self):
        reader = StagedReader(selected={'settings.xml': b'credential sentinel'})
        decision = source_policy(graph({'pom.xml': pom(ROW)}), 'pom.xml', reader)
        self.assertTrue(decision.admitted)
        self.assertEqual(reader.reads, [])
        self.assertNotIn('settings.xml', reader.checks)
        decision = self.decision(controls={'.mvn/settings.xml': b'credential sentinel'})
        self.assertFalse(decision.admitted)

    def test_supported_unique_settings_selectors(self):
        for config in (b'-s\npolicy.xml', b'--settings\npolicy.xml', b'--settings=policy.xml'):
            reader = StagedReader({'.mvn/maven.config': config}, {'policy.xml': settings()})
            result = source_policy(graph({'pom.xml': pom(ROW)}), 'pom.xml', reader)
            self.assertTrue(result.admitted)
            self.assertEqual(reader.reads, ['.mvn/maven.config', 'policy.xml'])
        self.assertTrue(self.decision(controls={'.mvn/maven.config': b'--settings=.mvn/settings.xml',
                                               '.mvn/settings.xml': settings()},
                                      selected={'.mvn/settings.xml': settings()}).admitted)

    def test_escaping_competing_missing_or_unsupported_selectors_refuse_without_open(self):
        for config in (b'-s\n../outside.xml', b'--settings=/outside.xml', b'--settings=C:/x',
                       b'--settings=${path}', b'--settings=one\n-s\ntwo', b'-s',
                       b'-s one', b'-gs\npolicy.xml', b'@arguments', b'-f\nother.xml'):
            reader = StagedReader({'.mvn/maven.config': config})
            result = source_policy(graph({'pom.xml': pom(ROW)}), 'pom.xml', reader)
            self.assertFalse(result.admitted)
            self.assertEqual(reader.reads, ['.mvn/maven.config'])
        self.assertFalse(self.decision(controls={'.mvn/maven.config': b'-s\nmissing.xml'}).admitted)

    def test_nested_inert_launch_allowed_but_selector_conflict_refused(self):
        g = graph({'child/pom.xml': pom(ROW)})
        controls = {'.mvn/maven.config': b'-B\n-Dmaven.repo.local=/private/cache',
                    'child/.mvn/maven.config': b'-q\n-P\n+public,!other\nverify'}
        self.assertTrue(source_policy(g, 'child/pom.xml', StagedReader(controls)).admitted)
        controls['child/.mvn/maven.config'] = b'--settings=policy.xml'
        reader = StagedReader(controls, {'policy.xml': settings()})
        self.assertFalse(source_policy(g, 'child/pom.xml', reader).admitted)
        self.assertNotIn('policy.xml', reader.reads)

    def test_harmless_launch_and_jvm_properties_never_interpolate_values(self):
        controls = {'.mvn/maven.config': b'# comment\n-B\n-U\n-Dmaven.repo.local=/never/read\n-Dversion=2\n-Doutput=secret\nverify',
                    '.mvn/jvm.config': b'-Xms128m -Xmx2G -XX:MaxMetaspaceSize=256m -XX:MetaspaceSize=64m -XX:ReservedCodeCacheSize=32m -XX:MaxDirectMemorySize=128m -Dtransport.tuning=1'}
        self.assertTrue(self.decision(controls=controls).admitted)
        self.assertFalse(self.decision(controls={'.mvn/maven.config': b'-o'}).admitted)
        for value in (b'-javaagent:secret', b'-XX:Unknown=1', b'-cp secret', b'-Xmx"2g"'):
            self.assertFalse(self.decision(controls={'.mvn/jvm.config': value}).admitted)

    def test_relevant_filter_and_source_properties_refuse_without_values(self):
        keys = ('maven.repo.central', 'maven.settings', 'maven.user.settings', 'maven.global.settings',
                'maven.ext.class.path', 'maven.multiModuleProjectDirectory', 'user.home', 'maven.home',
                'aether.remoteRepositoryFilter.groupId', 'maven.resolver.remoteRepositoryFilter.prefixes')
        for key in keys:
            for file in ('.mvn/maven.config', '.mvn/jvm.config'):
                self.assertFalse(self.decision(controls={file: ('-D' + key + '=secret').encode()}).admitted)
            self.assertFalse(self.decision(f'<properties><{key}>secret</{key}></properties>').admitted)
        self.assertFalse(self.decision(repositories(repo(url='${unreferenced}')),
                                       controls={'.mvn/maven.config': b'-Dunreferenced=public'}).admitted)

    def test_extensions_are_never_executed(self):
        for ns in (None, 'http://maven.apache.org/EXTENSIONS/1.0.0', 'http://maven.apache.org/EXTENSIONS/1.1.0'):
            attribute = '' if ns is None else f' xmlns="{ns}"'
            self.assertTrue(self.decision(controls={'.mvn/extensions.xml': f'<extensions{attribute}/>'.encode()}).admitted)
        for data in (b'<extensions><extension/></extensions>', b'<unknown/>', b'<extensions xmlns="other"/>'):
            self.assertFalse(self.decision(controls={'.mvn/extensions.xml': data}).admitted)
        for body in ('<build><extensions><extension/></extensions></build>',
                     '<build><plugins><plugin><extensions>true</extensions></plugin></plugins></build>',
                     '<build><plugins><plugin><extensions>${flag}</extensions></plugin></plugins></build>'):
            self.assertFalse(self.decision(body).admitted)

    def test_selected_settings_namespaces_offline_and_credentials(self):
        for ns in (None, *(f'http://maven.apache.org/SETTINGS/1.{n}.0' for n in range(3))):
            self.assertTrue(self.settings_decision(namespace=ns).admitted)
        for body in ('<offline>true</offline>', '<offline>${offline}</offline>',
                     '<servers><server><password>sentinel</password></server></servers>',
                     '<proxies><proxy/></proxies>', '<unknown/>',
                     '<offline>false</offline><offline>false</offline>'):
            self.assertFalse(self.settings_decision(body).admitted)
        self.assertTrue(self.settings_decision('<localRepository>/never/read</localRepository><servers/><proxies/>').admitted)
        self.assertTrue(self.settings_decision(profiles(repositories(repo('alternate', '${url}')))).admitted)
        self.assertFalse(self.settings_decision(profiles(repositories(repo(url='${url}')))).admitted)

    def test_mirror_exact_preference_and_pattern_order(self):
        blocked = '<blocked>true</blocked>'
        def check(entries, expected):
            self.assertEqual(self.settings_decision('<mirrors>' + ''.join(entries) + '</mirrors>').admitted, expected)
        check([mirror('*', blocked), mirror('central', identity='exact')], True)
        check([mirror('*'), mirror('central', blocked, identity='exact')], False)
        check([mirror('*'), mirror('external:*', blocked, identity='second')], True)
        check([mirror('external:*', blocked), mirror('*', identity='second')], False)
        for pattern in ('!central,*', 'external:http:*', 'other', 'other,!central,*'):
            check([mirror(pattern, blocked)], True)
        for pattern in ('central', '*', 'external:*', 'other,central', '*,central'):
            check([mirror(pattern, blocked)], False)
        check([mirror('*', blocked + '<mirrorOfLayouts>!default,*</mirrorOfLayouts>')], True)
        check([mirror('*', blocked + '<mirrorOfLayouts>legacy</mirrorOfLayouts>')], True)
        check([mirror('*', blocked + '<mirrorOfLayouts>default</mirrorOfLayouts>')], False)

    def test_unknown_relevant_mirror_grammar_refuses_and_unrelated_fields_do_not_poison(self):
        for pattern in ('', 'central,', 'central, bad', 'cent*', '${match}', 'central,??'):
            self.assertFalse(self.settings_decision('<mirrors>' + mirror(pattern) + '</mirrors>').admitted)
        for extra in ('<blocked>${flag}</blocked>', '<layout>legacy</layout>', '<unknown/>'):
            self.assertFalse(self.settings_decision('<mirrors>' + mirror('*', extra) + '</mirrors>').admitted)
            self.assertTrue(self.settings_decision('<mirrors>' + mirror('!central,*', extra) + '</mirrors>').admitted)
        self.assertFalse(self.settings_decision('<mirrors>' + mirror() + mirror(identity='m') + '</mirrors>').admitted)

    def test_all_refused_rows_keep_population_zero_measurement_and_zero_lookup_calls(self):
        g = graph({'pom.xml': pom(dependencies(dependency(extra='<version>1</version>'),
            dependency('second', '<version>2</version>')) + repositories(repo(url='https://private.invalid')))})
        admission = admit_sources(g, StagedReader())
        lookup = Mock()
        self.assertEqual(admitted_lookups(admission, lookup), ())
        lookup.assert_not_called()
        result = summarize_sources(admission.sources)
        self.assertEqual((result.declared.summary.dependencies_discovered, result.declared.summary.dependencies_measured,
                          result.declared.summary.coverage, result.declared.summary.total_libyears), (2, 0, 0.0, 0.0))
        row = admission.sources[0].declared.rows[0]
        self.assertEqual((row.declared.version, row.declared.reason), ('1', MavenReason.COMPARATOR_REFUSED))

    def test_denied_same_ga_sibling_cannot_borrow_capability_and_system_is_row_local(self):
        g = graph({'pom.xml': pom(ROW),
                   'denied/pom.xml': pom(ROW + repositories(repo(url='https://private.invalid')), artifact='denied')})
        admission = admit_sources(g, StagedReader())
        lookup = Mock(return_value='fixed-result')
        results = admitted_lookups(admission, lookup)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0].source_id, 'pom.xml')
        capability = lookup.call_args.args[0]
        self.assertEqual((capability.group_id, capability.artifact_id, capability.version),
                         ('external', 'library', '1'))
        self.assertEqual(capability.__slots__, ('group_id', 'artifact_id', 'version'))
        g = graph({'pom.xml': pom(dependencies(dependency(extra='<version>1</version>'), dependency('system', '<version>1</version><scope>system</scope><systemPath>/never/read</systemPath>')))})
        admission = admit_sources(g, StagedReader())
        self.assertEqual(len(admission.capabilities), 1)
        self.assertEqual(len(admission.sources[0].declared.rows), 2)

    def test_unsupported_occurrence_facts_never_mint_capabilities(self):
        for body in (
            dependencies(dependency(extra='<version>1</version><scope>${runtime.scope}</scope>')),
            ROW + profiles(dependencies(dependency(extra='<scope>system</scope>'))),
            dependencies(dependency(extra='<version>1</version><optional>${optional}</optional>')),
            dependencies(dependency(extra='<version>1</version><scope>unknown</scope>')),
        ):
            with self.subTest(body=body):
                admission = admit_sources(graph({'pom.xml': pom(body)}), StagedReader())
                lookup = Mock()
                self.assertEqual(admitted_lookups(admission, lookup), ())
                lookup.assert_not_called()
                collection = admission.sources[0].declared
                self.assertEqual(collection.population_count, 1)
                self.assertEqual(collection.rows[0].declared.version, '1')
                self.assertEqual(collection.rows[0].declared.reason, MavenReason.UNSUPPORTED_MODEL)

    def test_unknown_root_build_profile_and_parent_policy_cannot_authorize_lookup(self):
        unknowns = (
            '<repositoryPolicy><central>false</central></repositoryPolicy>',
            '<build><remoteRepositoryFilter><groupId>x</groupId></remoteRepositoryFilter></build>',
            profiles('<build><repositoryPolicy/></build>'),
            '<build><pluginManagement><remoteRepositoryFilter/></pluginManagement></build>',
        )
        for unknown in unknowns:
            for inherited in (False, True):
                with self.subTest(unknown=unknown, inherited=inherited):
                    documents = {'pom.xml': pom(ROW + unknown)}
                    if inherited:
                        documents['child/pom.xml'] = pom(parent(), artifact='child')
                    admission = admit_sources(graph(documents), StagedReader())
                    lookup = Mock()
                    self.assertEqual(admitted_lookups(admission, lookup), ())
                    lookup.assert_not_called()
                    for source in admission.sources:
                        self.assertEqual(len(source.declared.rows), 1)
                        self.assertEqual(source.declared.rows[0].declared.version, '1')
                        self.assertEqual(source.declared.rows[0].declared.reason, MavenReason.POLICY_UNKNOWN)

    def test_unrelated_build_resource_filters_and_plugin_configuration_stay_inert(self):
        body = ('<build><sourceDirectory>/never/read</sourceDirectory>'
                '<filters><filter>/never/read</filter></filters>'
                '<plugins><plugin><configuration><repositoryPolicy>arbitrary</repositoryPolicy>'
                '</configuration></plugin></plugins></build>'
                '<reporting><arbitrary/></reporting>')
        self.assertTrue(self.decision(body).admitted)

    def test_mirror_pattern_whitespace_is_not_normalized_to_supported_syntax(self):
        for pattern in (' central ', 'central ', ' central', 'central, other', 'central,other\t'):
            self.assertFalse(self.settings_decision('<mirrors>' + mirror(pattern) + '</mirrors>').admitted)
        for layout in (' default ', 'default ', ' default', 'default, legacy'):
            self.assertFalse(self.settings_decision('<mirrors>' + mirror('*',
                '<mirrorOfLayouts>' + layout + '</mirrorOfLayouts>') + '</mirrors>').admitted)
        self.assertTrue(self.settings_decision('<mirrors>' + mirror('central',
            '<mirrorOfLayouts>default</mirrorOfLayouts>') + '</mirrors>').admitted)

    def test_profile_mirror_and_argument_budgets_fail_closed(self):
        many_profiles = '<profiles>' + ''.join(f'<profile><id>p{n}</id></profile>' for n in range(129)) + '</profiles>'
        self.assertEqual(self.decision(many_profiles).reason, MavenReason.POLICY_BUDGET_EXCEEDED)
        many_mirrors = '<mirrors>' + ''.join(mirror('other', identity=f'm{n}') for n in range(65)) + '</mirrors>'
        self.assertEqual(self.settings_decision(many_mirrors).reason, MavenReason.POLICY_BUDGET_EXCEEDED)
        for data in (b'-B\n' * 1025, b'-Dkey=' + b'x' * 2049):
            self.assertEqual(self.decision(controls={'.mvn/maven.config': data}).reason,
                             MavenReason.POLICY_BUDGET_EXCEEDED)
        with patch('libyears.maven_policy.MAX_POLICY_RECORDS', 1):
            g = graph({'pom.xml': pom(repositories(repo('parent'))),
                       'child/pom.xml': pom(parent() + ROW + repositories(repo('child')), artifact='child')})
            self.assertEqual(source_policy(g, 'child/pom.xml', StagedReader()).reason,
                             MavenReason.POLICY_BUDGET_EXCEEDED)

    def test_budget_and_input_failures_are_sanitized_and_keep_safe_population(self):
        with patch('libyears.maven_policy.MAX_POLICY_RECORDS', 1):
            self.assertEqual(self.decision(repositories(repo('a'), repo('b'))).reason,
                             MavenReason.POLICY_BUDGET_EXCEEDED)
        for issue in (MavenInputIssue.CAPABILITY, MavenInputIssue.UNSAFE, MavenInputIssue.CHANGED):
            reader = StagedReader()
            reader.control_present = Mock(side_effect=MavenInputFailure(issue))
            decision = source_policy(graph({'pom.xml': pom(ROW)}), 'pom.xml', reader)
            self.assertEqual(decision.reason, MavenReason.POLICY_INPUT_UNAVAILABLE)
        self.assertEqual(self.decision(controls={'.mvn/maven.config': b'x' * 65537}).reason,
                         MavenReason.POLICY_BUDGET_EXCEEDED)
        self.assertEqual(self.decision(controls={'.mvn/jvm.config': b'\x00secret'}).reason,
                         MavenReason.POLICY_UNKNOWN)


@unittest.skipUnless(filesystem_available(), 'safe descriptor primitives unavailable')
class MavenPolicyNativeTests(unittest.TestCase):
    def test_selected_settings_uses_contained_nofollow_snapshots_and_shared_budgets(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root).resolve()
            (path / 'pom.xml').write_bytes(pom(ROW))
            (path / '.mvn').mkdir()
            (path / '.mvn/maven.config').write_bytes(b'--settings=policy.xml')
            (path / 'policy.xml').write_bytes(settings())
            with MavenInputReader(path) as reader:
                g = build_project_graph(reader.inventory().discovery, reader.snapshot_pom)
                self.assertTrue(source_policy(g, 'pom.xml', reader).admitted)
                (path / 'policy.xml').write_bytes(settings('<offline>true</offline>'))
                self.assertFalse(source_policy(g, 'pom.xml', reader).admitted)
            (path / 'policy.xml').unlink()
            (path / 'policy.xml').symlink_to(path / 'pom.xml')
            with MavenInputReader(path) as reader:
                g = build_project_graph(reader.inventory().discovery, reader.snapshot_pom)
                self.assertEqual(source_policy(g, 'pom.xml', reader).reason,
                                 MavenReason.POLICY_INPUT_UNAVAILABLE)


if __name__ == '__main__':
    unittest.main()
