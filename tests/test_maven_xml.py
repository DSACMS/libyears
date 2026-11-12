"""Structural XML checks only; no Maven dependency/model interpretation."""

from dataclasses import FrozenInstanceError
import socket
import unittest
from unittest.mock import patch

from libyears import maven_input as inputs
from libyears.maven_input import MavenInputFailure, MavenInputIssue, parse_pom, parse_xml


class MavenXMLTests(unittest.TestCase):
    def assert_refused(self, data, issue=None, parser=parse_xml):
        with self.assertRaises(MavenInputFailure) as caught:
            parser(data)
        if issue is not None:
            self.assertEqual(caught.exception.issue, issue)

    def test_plain_and_namespaced_pom_formats(self):
        for namespace in ('', ' xmlns="http://maven.apache.org/POM/4.0.0"'):
            with self.subTest(namespace=namespace):
                node = parse_pom(('<project' + namespace + '><modelVersion>4.0.0</modelVersion>'
                                  '<name>example</name></project>').encode())
                self.assertEqual(node.scalar('name'), 'example')
                with self.assertRaises(FrozenInstanceError):
                    node.text = 'changed'

    def test_required_root_namespace_and_format_refuse(self):
        for data in (b'<wrong/>', b'<project xmlns="urn:foreign"><modelVersion>4.0.0</modelVersion></project>',
                     b'<project/>', b'<project><modelVersion>3.0.0</modelVersion></project>',
                     b'<project mode="unknown"><modelVersion>4.0.0</modelVersion></project>'):
            with self.subTest(data=data):
                self.assert_refused(data, MavenInputIssue.XML_UNSUPPORTED, parse_pom)

    def test_malformed_whole_document_never_returns_a_partial_tree(self):
        for data in (b'', b'<project>', b'<project/>trailing', b'<project><a></project>',
                     b'<project a="1" a="2"/>', b'<project>&unknown;</project>'):
            with self.subTest(data=data):
                self.assert_refused(data, MavenInputIssue.XML_MALFORMED)

    def test_duplicate_and_mixed_format_scalars_refuse(self):
        for field in (b'<modelVersion>4.0.0</modelVersion>' * 2,
                      b'<modelVersion><nested/></modelVersion>',
                      b'<modelVersion hint="x">4.0.0</modelVersion>'):
            self.assert_refused(b'<project>' + field + b'</project>',
                                MavenInputIssue.XML_UNSUPPORTED, parse_pom)

    def test_field_access_refuses_duplicate_mixed_and_namespace_confusion(self):
        for field in (b'<name>a</name><name>b</name>', b'<name>a<part/>b</name>',
                      b'<x:name xmlns:x="urn:foreign">a</x:name>'):
            node = parse_xml(b'<project>' + field + b'</project>')
            with self.subTest(field=field), self.assertRaises(MavenInputFailure):
                node.scalar('name')
        node = parse_xml(b'<project><x:container xmlns:x="urn:foreign"/></project>')
        with self.assertRaises(MavenInputFailure):
            node.elements('container')
        attributed = parse_xml(b'<project><container mode="unknown"/></project>')
        with self.assertRaises(MavenInputFailure):
            attributed.elements('container')

    def test_namespace_separator_in_uri_is_refused_by_framing(self):
        self.assert_refused(b'<project><x:name xmlns:x="urn:}foreign">a</x:name></project>',
                            MavenInputIssue.XML_MALFORMED)

    def test_uninterpreted_repeated_fields_are_not_globally_deduplicated(self):
        node = parse_xml(b'<configuration><item>a</item><item>b</item></configuration>')
        self.assertEqual(len(node.elements('item')), 2)
        self.assertIsNone(node.scalar('absent'))

    def test_dtd_and_entity_forms_cannot_resolve_files_or_network(self):
        documents = (
            b'<!DOCTYPE project SYSTEM "file:///forbidden"><project/>',
            b'<!DOCTYPE project [<!ENTITY x SYSTEM "https://example.invalid/secret">]><project>&x;</project>',
            b'<!DOCTYPE project [<!ENTITY a "expand"><!ENTITY b "&a;&a;">]><project>&b;</project>',
            b'<!DOCTYPE project [<!ENTITY % p SYSTEM "file:///forbidden">%p;]><project/>',
        )
        with patch('builtins.open', side_effect=AssertionError('file side effect')), \
                patch.object(inputs.os, 'open', side_effect=AssertionError('OS file side effect')), \
                patch.object(socket, 'socket', side_effect=AssertionError('network side effect')):
            for data in documents:
                with self.subTest(data=data):
                    self.assert_refused(data, MavenInputIssue.XML_UNSUPPORTED)

    def test_xinclude_refuses_without_resolution(self):
        data = b'<project xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include href="file:///forbidden"/></project>'
        with patch('builtins.open', side_effect=AssertionError('file read')):
            self.assert_refused(data, MavenInputIssue.XML_UNSUPPORTED)

    def test_schema_location_and_processing_instruction_are_inert(self):
        data = (b'<?xml-stylesheet href="file:///forbidden"?>'
                b'<project xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                b'xsi:schemaLocation="urn:none https://example.invalid/schema">'
                b'<modelVersion>4.0.0</modelVersion></project>')
        with patch('builtins.open', side_effect=AssertionError('schema read')), \
                patch.object(socket, 'socket', side_effect=AssertionError('network')):
            self.assertEqual(parse_pom(data).name, 'project')

    def test_only_supported_utf8_and_xml_declarations(self):
        valid = b'\xef\xbb\xbf<?xml version="1.0" encoding="UTF-8"?><project/>'
        self.assertEqual(parse_xml(valid).name, 'project')
        for data in ('<project/>'.encode('utf-16'), '<project/>'.encode('utf-16-le'),
                     '<project/>'.encode('utf-16-be'), b'<project>\xff</project>',
                     b'<?xml version="1.0" encoding="ISO-8859-1"?><project/>',
                     b'<?xml version="1.1"?><project/>'):
            with self.subTest(data=data):
                self.assert_refused(data, MavenInputIssue.XML_UNSUPPORTED)

    def test_builtin_escapes_and_character_references_remain_bounded_xml(self):
        node = parse_xml(b'<project><name>&lt;&gt;&amp;&quot;&apos;&#65;</name></project>')
        self.assertEqual(node.scalar('name'), '<>&"\'A')

    def test_exact_raw_byte_limit_and_one_byte_over(self):
        size = inputs.MAX_XML_BYTES
        prefix, suffix = b'<project><!--', b'--></project>'
        data = prefix + b'x' * (size - len(prefix) - len(suffix)) + suffix
        self.assertEqual(len(data), 1024 * 1024)
        self.assertEqual(parse_xml(data).name, 'project')
        self.assert_refused(data + b' ', MavenInputIssue.LIMIT)

    def test_depth_boundary(self):
        self.assertEqual(parse_xml(b'<a>' * 32 + b'</a>' * 32).name, 'a')
        self.assert_refused(b'<a>' * 33 + b'</a>' * 33, MavenInputIssue.LIMIT)

    def test_element_count_boundary(self):
        self.assertEqual(len(parse_xml(b'<a>' + b'<b/>' * 49_999 + b'</a>').children), 49_999)
        self.assert_refused(b'<a>' + b'<b/>' * 50_000 + b'</a>', MavenInputIssue.LIMIT)

    def test_attribute_count_including_namespace_declarations(self):
        valid = '<a ' + ' '.join(f'x{i}="v"' for i in range(32)) + '/>'
        self.assertEqual(len(parse_xml(valid.encode()).attributes), 32)
        extra = valid[:-2] + ' overflow="v"/>'
        self.assert_refused(extra.encode(), MavenInputIssue.LIMIT)
        declarations = '<a ' + ' '.join(f'xmlns:x{i}="urn:x{i}"' for i in range(33)) + '/>'
        self.assert_refused(declarations.encode(), MavenInputIssue.LIMIT)

    def test_scalar_and_attribute_limits_count_utf8_bytes(self):
        self.assertEqual(len(parse_xml(b'<a>' + b'x' * 16_384 + b'</a>').text), 16_384)
        self.assert_refused(b'<a>' + b'x' * 16_385 + b'</a>', MavenInputIssue.LIMIT)
        self.assert_refused(('<a>' + '\u00e9' * 8193 + '</a>').encode(), MavenInputIssue.LIMIT)
        self.assert_refused(b'<a x="' + b'x' * 16_385 + b'"/>', MavenInputIssue.LIMIT)

    def test_container_indentation_is_not_a_scalar(self):
        node = parse_xml(b'<a>' + (b' ' * 10 + b'<b/>') * 2000 + b'</a>')
        self.assertEqual(len(node.children), 2000)
