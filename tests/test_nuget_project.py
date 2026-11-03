"""Offline complete-population and parser-boundary witnesses for Feature 006."""

from dataclasses import FrozenInstanceError
import unittest
from unittest.mock import patch

from libyears.nuget_input import LocalInput, NuGetInputFailure
from libyears.nuget_project import parse_project


def project(body='', framework='<TargetFramework>net10.0</TargetFramework>'):
    return ('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>' + framework
            + '</PropertyGroup>' + body + '</Project>')


def reference(name='Example', version='1.0', extra=''):
    return f'<PackageReference Include="{name}" Version="{version}" {extra}/>'


def parse(text):
    data = text.encode('utf-8')
    return parse_project(LocalInput(data, text))


class NuGetProjectTests(unittest.TestCase):
    def rejected(self, text, category='unsupported'):
        with self.assertRaises(NuGetInputFailure) as caught:
            parse(text)
        self.assertEqual(caught.exception.category, category)
        self.assertFalse(hasattr(caught.exception, 'declarations'))
        return str(caught.exception)

    def test_complete_framework_forms_and_empty_population(self):
        for property_name in ('TargetFramework', 'TargetFrameworks'):
            with self.subTest(property_name=property_name):
                context = parse(project(framework=f'<{property_name}>net10.0</{property_name}>'))
                self.assertEqual(context.framework, 'net10.0')
                self.assertEqual(context.sdk, 'Microsoft.NET.Sdk')
                self.assertEqual(context.declarations, ())
                with self.assertRaises(FrozenInstanceError):
                    context.framework = 'other'

    def test_request_minima_are_preserved_without_selection(self):
        for request, normalized in [('1.0', '1.0.0'), ('1.2.3', '1.2.3'),
                                    ('1.2.3.0', '1.2.3'), ('1.2.3.4', '1.2.3.4'),
                                    ('0.0.0.0', '0.0.0')]:
            with self.subTest(request=request):
                row, = parse(project('<ItemGroup>' + reference(version=request) + '</ItemGroup>')).declarations
                self.assertEqual(row.declared_version, request)
                self.assertEqual(row.requested_minimum.normalized_version, normalized)
                self.assertEqual(row.package_key, 'example')
                self.assertFalse(hasattr(row, 'selected_version'))
                with self.assertRaises(FrozenInstanceError):
                    row.package_name = 'Other'

    def test_all_direct_roles_and_metadata_count_once(self):
        body = '''<ItemGroup>
          <PackageReference Include="Tests" Version="1.0" PrivateAssets="all"/>
          <PackageReference Include="Tool" Version="1.0" IncludeAssets="*"/>
          <PackageReference Include="Analyzer" Version="1.0">
            <ExcludeAssets>*</ExcludeAssets>
            <GeneratePathProperty>true</GeneratePathProperty>
          </PackageReference>
          <ProjectReference Include="../../private/Secret.csproj"/>
          <FrameworkReference Include="Microsoft.AspNetCore.App"/>
          <Compile Include="Program.cs"/><None Include="readme.txt"/>
        </ItemGroup>'''
        with patch('builtins.open', side_effect=AssertionError('no file reads')), \
                patch('os.open', side_effect=AssertionError('no file reads')):
            context = parse(project(body))
        self.assertEqual([r.package_name for r in context.declarations], ['Tests', 'Tool', 'Analyzer'])

    def test_literal_inert_table_comments_formatting_and_builtin_escapes(self):
        properties = ''.join(f'<{name}>literal</{name}>' for name in
                             ('OutputType', 'Nullable', 'ImplicitUsings', 'LangVersion',
                              'AssemblyName', 'RootNamespace'))
        text = project('<PropertyGroup>' + properties + '</PropertyGroup><ItemGroup><!-- comment -->'
                       + reference(name='Ex&#97;mple', version='1.&#48;') + '</ItemGroup>')
        row, = parse(text).declarations
        self.assertEqual((row.package_name, row.declared_version), ('Example', '1.0'))

    def test_framework_context_rejections_never_return_partial_population(self):
        cases = ['', '<TargetFramework/>', '<TargetFramework>net8.0;net10.0</TargetFramework>',
                 '<TargetFramework> net10.0</TargetFramework>',
                 '<TargetFramework>$(Framework)</TargetFramework>',
                 '<TargetFramework>@(Framework)</TargetFramework>',
                 '<TargetFramework Condition="true">net10.0</TargetFramework>',
                 '<TargetFramework>net10.0</TargetFramework>' * 2,
                 '<TargetFramework>net10.0</TargetFramework><TargetFrameworks>net10.0</TargetFrameworks>',
                 '<TargetFramework>net10.0</TargetFramework><RuntimeIdentifier>linux-x64</RuntimeIdentifier>',
                 '<TargetFramework>net10.0</TargetFramework><RuntimeIdentifiers/>',
                 '<TargetFramework>néт10</TargetFramework>']
        for framework in cases:
            with self.subTest(framework=framework):
                self.rejected(project('<ItemGroup>' + reference() + '</ItemGroup>', framework))

    def test_unsupported_requests_and_id_grammar(self):
        for version in ('1', '[1.0]', '[1.0, )', '1.*', '1.0-beta', '1.0+build',
                        '01.0', '1.0.0.0.0', ' 1.0', '1.0 ', '$(Version)', '@(Version)', ''):
            with self.subTest(version=version):
                self.rejected(project('<ItemGroup>' + reference(version=version) + '</ItemGroup>'))
        for name in ('', '_Example', '.Example', 'Example;Other', '$(Package)', 'éxample', 'x' * 101):
            with self.subTest(name=name):
                self.rejected(project('<ItemGroup>' + reference(name=name) + '</ItemGroup>'))

    def test_duplicate_ids_have_distinct_failure(self):
        for second in ('Example', 'EXAMPLE'):
            self.rejected(project('<ItemGroup>' + reference() + reference(second) + '</ItemGroup>'), 'duplicate')

    def test_package_affecting_and_unknown_constructs(self):
        bodies = ['<Import Project="outside.props"/>', '<Choose><When Condition="true"/></Choose>',
                  '<Target Name="Generate"><ItemGroup>' + reference() + '</ItemGroup></Target>',
                  '<PropertyGroup><ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally></PropertyGroup>',
                  '<PropertyGroup><RestoreSources>secret</RestoreSources></PropertyGroup>',
                  '<PropertyGroup><Unknown>literal</Unknown></PropertyGroup>',
                  '<ItemGroup><Unknown Include="literal"/></ItemGroup>',
                  '<ItemGroup><PackageVersion Include="Example" Version="1.0"/></ItemGroup>',
                  '<ItemGroup><GlobalPackageReference Include="Example" Version="1.0"/></ItemGroup>',
                  '<ItemGroup Condition="true">' + reference() + '</ItemGroup>',
                  '<PropertyGroup Condition="true"><OutputType>Exe</OutputType></PropertyGroup>',
                  '<ItemGroup><Compile Include="$(Source)"/></ItemGroup>']
        for body in bodies:
            with self.subTest(body=body):
                self.rejected(project(body))
        for extra in ('Condition="true"', 'Update="Example"', 'Remove="Example"',
                      'VersionOverride="1.0"', 'Aliases="global"', 'Unknown="literal"'):
            with self.subTest(extra=extra):
                self.rejected(project('<ItemGroup>' + reference(extra=extra) + '</ItemGroup>'))
        for content in ('<Version>1.0</Version>', '<PrivateAssets>$(Assets)</PrivateAssets>',
                        '<Unknown>literal</Unknown>', '<PrivateAssets>all</PrivateAssets>' * 2,
                        '<PrivateAssets Condition="true">all</PrivateAssets>'):
            self.rejected(project('<ItemGroup><PackageReference Include="Example" Version="1.0">'
                                  + content + '</PackageReference></ItemGroup>'))
        self.rejected(project('<ItemGroup><PackageReference Include="Example" Version="1.0" '
                              'PrivateAssets="all"><PrivateAssets>all</PrivateAssets>'
                              '</PackageReference></ItemGroup>'))
        self.rejected(project('<ItemGroup><PackageReference Include="Example"/></ItemGroup>'))

    def test_complete_framing_precedes_unsupported_and_duplicate(self):
        for body in ('<Import/>', '<ItemGroup>' + reference() * 2 + '</ItemGroup>'):
            self.rejected(project(body)[:-10], 'malformed')
            self.rejected(project(body) + '<extra/>', 'malformed')
        self.rejected('<Project Sdk="a" Sdk="b"/>', 'malformed')

    def test_xml_context_and_external_entities_are_never_loaded(self):
        cases = ['<!DOCTYPE Project><Project Sdk="Microsoft.NET.Sdk"/>',
                 '<!DOCTYPE Project [<!ENTITY secret "canary">]>' + project(),
                 '<!DOCTYPE Project [<!ENTITY secret SYSTEM "file:///private/secret">]>'
                 + project('<PropertyGroup><AssemblyName>&secret;</AssemblyName></PropertyGroup>'),
                 project().replace('<Project ', '<Project xmlns="urn:msbuild" ', 1),
                 project().replace('Sdk="Microsoft.NET.Sdk"', 'Sdk="$(Sdk)"'),
                 project().replace('Sdk="Microsoft.NET.Sdk"', ''),
                 '<?xml version="1.0" encoding="ISO-8859-1"?>' + project()]
        with patch('builtins.open', side_effect=AssertionError('no external read')):
            for text in cases:
                with self.subTest(text=text):
                    self.assertNotIn('canary', self.rejected(text))
        self.assertEqual(parse('<?xml version="1.0" encoding="UTF-8"?>' + project()).framework, 'net10.0')
        with self.assertRaises(NuGetInputFailure) as caught:
            parse_project(LocalInput(b'\xff', 'ignored'))
        self.assertEqual(caught.exception.category, 'malformed')


class NuGetProjectBoundaryTests(unittest.TestCase):
    rejected = NuGetProjectTests.rejected

    def test_direct_reference_cap_and_cap_plus_one(self):
        body = ''.join(reference('Package' + str(i)) for i in range(10_000))
        self.assertEqual(len(parse(project('<ItemGroup>' + body + '</ItemGroup>')).declarations), 10_000)
        self.rejected(project('<ItemGroup>' + body + reference('Extra') + '</ItemGroup>'), 'limit')
        self.rejected(project('<ItemGroup>' + '<PackageReference/>' * 10_001 + '</ItemGroup>'), 'limit')

    def test_framework_sdk_and_component_limits(self):
        self.assertEqual(len(parse(project(framework='<TargetFramework>' + 'x' * 128
                                           + '</TargetFramework>')).framework), 128)
        self.rejected(project(framework='<TargetFramework>' + 'x' * 129 + '</TargetFramework>'), 'limit')
        self.assertEqual(len(parse(project().replace('Microsoft.NET.Sdk', 'x' * 256)).sdk), 256)
        self.rejected(project().replace('Microsoft.NET.Sdk', 'x' * 257), 'limit')
        request = '1' * 32 + '.0'
        self.assertEqual(parse(project('<ItemGroup>' + reference(version=request) + '</ItemGroup>'))
                         .declarations[0].declared_version, request)
        self.rejected(project('<ItemGroup>' + reference(version='1' * 33 + '.0') + '</ItemGroup>'))

    def test_xml_callback_caps_and_cap_plus_one(self):
        # These syntax-inert wrappers remain unsupported semantically, but the
        # boundary itself must finish framing at the cap and stop at cap+1.
        self.rejected('<X>' * 32 + '</X>' * 32)
        self.rejected('<X>' * 33 + '</X>' * 33, 'limit')
        attributes = ' '.join(f'a{i}="v"' for i in range(32))
        self.rejected('<X ' + attributes + '/>')
        self.rejected('<X ' + attributes + ' extra="v"/>', 'limit')
        self.rejected('<X>' + '<Y/>' * 49_999 + '</X>')
        self.rejected('<X>' + '<Y/>' * 50_000 + '</X>', 'limit')
        for value in ('x' * 16_384,):
            self.rejected('<X value="' + value + '"/>')
            self.rejected('<X value="' + value + 'x"/>', 'limit')
            self.rejected('<X>' + value + '</X>')
            self.rejected('<X>' + value + 'x</X>', 'limit')


if __name__ == '__main__':
    unittest.main()
