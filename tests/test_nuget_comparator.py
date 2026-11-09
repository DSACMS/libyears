"""Public comparison policy is decided offline, before any metadata capability."""

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from libyears.nuget_comparator import parse_repository_policy
from libyears.nuget_input import LocalInput
from libyears.nuget_provenance import PUBLIC_ORIGIN
from tests.nuget_fixtures import SAFE_SCOPED_READ
from libyears.nuget_discovery import discovery_available


PROJECT = b'<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup><ItemGroup><PackageReference Include="Foo" Version="1.0" /></ItemGroup></Project>'


def local(value):
    data = value.encode() if isinstance(value, str) else value
    return LocalInput(data, data.decode())


def config(sources='', mappings=None, disabled='', *, closed=False):
    clear = '<clear />' if closed else ''
    text = '<configuration><packageSources>'+clear+sources+'</packageSources>'
    text += '<disabledPackageSources>'+clear+disabled+'</disabledPackageSources>'
    if mappings is not None:
        text += '<packageSourceMapping>'+clear+mappings+'</packageSourceMapping>'
    return text+'</configuration>'


def source(key='public', value=PUBLIC_ORIGIN):
    return f'<add key="{key}" value="{value}" />'


def mapping(key, *patterns):
    return '<packageSource key="'+key+'">'+''.join(
        '<package pattern="'+p+'" />' for p in patterns)+'</packageSource>'


class ComparatorPolicyTests(unittest.TestCase):
    def decide(self, *configs, project=PROJECT, name='foo'):
        with patch('socket.socket', side_effect=AssertionError('offline authority')), \
                patch('urllib.request.urlopen', side_effect=AssertionError('no namesake lookup')):
            return parse_repository_policy(tuple(local(c) for c in configs), local(project)).decide(name)

    def test_no_config_and_only_public_are_explicit_convention(self):
        for configs in ((), (config(source()),), (config(source(), closed=True),)):
            decision = self.decide(*configs)
            self.assertEqual(decision.basis, 'conventional_public_policy')
            self.assertIsNone(decision.reason)

    def test_alternate_and_local_eligibility_are_ambiguous_not_private(self):
        for endpoint in ('https://alternate.invalid/v3/index.json', '/local/feed', 'C:\\feed'):
            for entries in (source('other', endpoint), source()+source('other', endpoint)):
                decision = self.decide(config(entries))
                self.assertEqual(decision.reason, 'nuget_comparator_ambiguous')
                self.assertTrue(decision.testimony_can_resolve)

    def test_closed_unique_mapping_to_public_and_private(self):
        entries = source()+source('private', 'https://private.invalid')
        for key, basis, reason in [('public', 'repository_mapping', None),
                                   ('private', None, 'nuget_comparator_private')]:
            decision = self.decide(config(entries, mapping(key, 'Foo'), closed=True))
            self.assertEqual((decision.basis, decision.reason), (basis, reason))

    def test_exact_private_beats_longer_public_prefix_and_wildcard(self):
        entries = source()+source('private', 'https://private.invalid')
        maps = mapping('private', 'Foo')+mapping('public', 'Foo*', '*')
        decision = self.decide(config(entries, maps, closed=True))
        self.assertEqual(decision.reason, 'nuget_comparator_private')
        self.assertFalse(decision.testimony_can_resolve)
        maps = mapping('private', 'F*')+mapping('public', 'Fo*')
        self.assertEqual(self.decide(config(entries, maps, closed=True)).basis, 'repository_mapping')

    def test_active_mapping_cannot_fall_through(self):
        entries = source()+source('private', 'https://private.invalid')
        variants = [mapping('public', 'Foo')+mapping('private', 'Foo'),
                    mapping('public', 'Other'), mapping('missing', 'Foo')]
        for maps in variants:
            decision = self.decide(config(entries, maps, closed=True))
            self.assertIsNone(decision.basis)
            self.assertFalse(decision.testimony_can_resolve)
        self.assertEqual(self.decide(config(entries, mapping('public','Foo'))).reason,
                         'nuget_comparator_unknown')

    def test_disabled_public_empty_clear_removal_and_unresolved_disabling_refuse(self):
        for text in (config(source(), disabled='<add key="public" value="true" />'),
                     config('', closed=True), config('<remove key="public" />'),
                     config(source(), disabled='<add key="missing" value="false" />')):
            self.assertIsNone(self.decide(text).basis)

    def test_whole_framing_unsupported_grammar_never_salvages_prefix(self):
        valid = config(source())
        invalid = [valid[:-1], '<!DOCTYPE configuration>'+valid,
                   valid.replace('</configuration>', '<unknown /></configuration>'),
                   valid.replace('<packageSources>', '<packageSources unexpected="x">'),
                   config(source()+source('PUBLIC')),
                   config(source(), disabled='<add key="public" value="maybe" />'),
                   config(source(), mapping('public','F?o'), closed=True),
                   config(source(), mapping('public','Foo','foo'), closed=True),
                   config(source('public', '%PRIVATE%')),
                   config(source()).replace('</configuration>', '<packageSourceCredentials><secret /></packageSourceCredentials></configuration>')]
        for text in invalid:
            with self.subTest(text=text):
                self.assertEqual(self.decide(text).reason, 'nuget_comparator_unknown')

    def test_source_affecting_project_constructs_refuse_without_evaluation(self):
        for node in ('<RestoreSources>https://private.invalid</RestoreSources>',
                     '<RestoreAdditionalProjectSources>$(Feed)</RestoreAdditionalProjectSources>',
                     '<RestoreConfigFile>x</RestoreConfigFile>', '<NuGetSomething>x</NuGetSomething>',
                     '<Import Project="x" />', '<Target Name="x" />', '<Choose />'):
            self.assertEqual(self.decide(project=PROJECT.replace(b'</Project>', node.encode()+b'</Project>')).reason,
                             'nuget_comparator_unknown')

    def test_root_to_project_overrides_and_collection_clear(self):
        root = config(source('private','https://private.invalid'), mapping('private','Foo'), closed=True)
        child = config(source(), mapping('public','Foo'), closed=True)
        self.assertEqual(self.decide(root,child).basis, 'repository_mapping')
        child = config(source('private',PUBLIC_ORIGIN))
        self.assertEqual(self.decide(root,child).basis, 'repository_mapping')
        with patch('libyears.nuget_comparator.MAX_PROJECT_BYTES', 1):
            self.assertEqual(self.decide(root).reason, 'nuget_comparator_unknown')
        self.assertEqual(self.decide(*([root]*6)).reason, 'nuget_comparator_unknown')


@unittest.skipUnless(SAFE_SCOPED_READ and discovery_available(), 'safe anchored filesystem unavailable')
class ComparatorReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'child').mkdir()
        (self.root/'child'/'A.csproj').write_bytes(PROJECT)

    def decide(self):
        from libyears.nuget_sources import RepositoryNuGetReader
        with RepositoryNuGetReader(self.root, 'child/A.csproj', None) as reader:
            return reader.comparator_policy(reader.read('A.csproj')).decide('foo')

    def test_non_git_and_untracked_current_config_are_read_without_execution(self):
        self.assertEqual(self.decide().basis, 'conventional_public_policy')
        path = self.root/'NuGet.Config'
        path.write_text(config(source('private', '/local/feed')))
        self.assertEqual(self.decide().reason, 'nuget_comparator_ambiguous')
        path.write_text(config(source()))
        self.assertEqual(self.decide().basis, 'conventional_public_policy')

    def test_policy_links_and_automatic_import_families_refuse(self):
        for name in ('NuGet.Config','Directory.Build.props','Directory.Build.targets','Directory.Packages.props'):
            path = self.root/name
            path.symlink_to('unavailable-input')
            self.assertEqual(self.decide().reason, 'nuget_comparator_unknown')
            path.unlink()

    def test_case_aliases_refuse_on_case_sensitive_filesystem(self):
        first = self.root/'NuGet.Config'; second = self.root/'nuget.config'
        first.write_text(config(source()))
        second.write_text(config(source()))
        if len([p for p in self.root.iterdir() if p.name.lower()=='nuget.config']) != 2:
            self.skipTest('filesystem folds case aliases')
        self.assertEqual(self.decide().reason, 'nuget_comparator_unknown')

    def test_directory_mutation_during_enumeration_refuses(self):
        original = os.scandir
        def changed(directory):
            (self.root/'child'/'NuGet.Config').write_text(config(source('private','/local')))
            return original(directory)
        with patch('os.scandir', side_effect=changed):
            self.assertEqual(self.decide().reason, 'nuget_comparator_unknown')

    def test_dirty_tracked_config_uses_current_bytes(self):
        import shutil
        import subprocess
        if shutil.which('git') is None:
            self.skipTest('Git only constructs the dirty-config witness')
        path = self.root/'NuGet.Config'
        path.write_text(config(source()))
        subprocess.run(['git', 'init', '--quiet', str(self.root)], check=True)
        subprocess.run(['git', '-C', str(self.root), 'add', 'NuGet.Config'], check=True)
        path.write_text(config(source('other', '/local/feed')))
        before = subprocess.check_output(['git', '-C', str(self.root), 'status', '--porcelain'])
        with patch('subprocess.Popen', side_effect=AssertionError('no runtime Git')):
            self.assertEqual(self.decide().reason, 'nuget_comparator_ambiguous')
        self.assertEqual(subprocess.check_output(['git', '-C', str(self.root), 'status', '--porcelain']), before)
