from dataclasses import replace
import unittest
from unittest.mock import patch

from libyears.maven import admit_sources, scan_maven
from libyears.maven_model import MavenReason
from libyears.sbom_document import accept_document
from libyears.sbom_identity import canonical_members
from libyears.sbom_policy import admit_members
from tests.test_sbom_document import snapshot, synthetic_document
from tests.test_sbom_identity import maven_component
from test_maven_policy import graph, StagedReader, repositories, repo
from test_maven_project import pom, dependencies, dependency
from test_maven_scan import Reader, Metadata


class PolicyTests(unittest.TestCase):
    def admit(self, records=None, vetoes=(), **changes):
        doc = accept_document(snapshot(synthetic_document(components=records or [maven_component()], **changes)))
        members = canonical_members(doc)
        with patch('builtins.open', side_effect=AssertionError('file')), patch('socket.socket', side_effect=AssertionError('socket')), patch('subprocess.Popen', side_effect=AssertionError('process')):
            return admit_members(doc, members, vetoes)

    def test_standalone_no_assertion_required_and_distribution_not_assignment(self):
        self.assertIsNone(self.admit()[0].reason)
        self.assertIsNone(self.admit([maven_component(externalReferences=[{'type': 'distribution', 'url': 'https://alternate.invalid'}])])[0].reason)
        public = '?repository_url=https:%2F%2Frepo.maven.apache.org%2Fmaven2%2F'
        self.assertIsNone(self.admit([maven_component(suffix=public)])[0].reason)

    def test_global_alias_and_known_restrictions_union(self):
        for changes in ({'properties': [{}]}, {'formulation': [{}]},
                        {'metadata': {'component': {'name': 's', 'bom-ref': 'r', 'modified': True}}},
                        {'metadata': {'component': {'name': 's', 'bom-ref': 'r'}, 'properties': [{}]}}):
            self.assertEqual(self.admit(**changes)[0].reason, 'sbom_policy_unknown')
        for changes in ({'properties': [{}]}, {'evidence': {'identity': {}}}, {'pedigree': {'notes': 'x'}}, {'modified': True}, {'modified': 1}):
            self.assertEqual(self.admit([maven_component(), maven_component(**changes)])[0].reason, 'sbom_policy_unknown')
        private = maven_component(suffix='?repository_url=https:%2F%2Fprivate.invalid%2Fmaven2')
        self.assertEqual(self.admit([maven_component(), private])[0].reason, 'sbom_comparator_refused')
        for reason in (MavenReason.COMPARATOR_REFUSED, MavenReason.POLICY_UNKNOWN, MavenReason.POLICY_INPUT_UNAVAILABLE, MavenReason.POLICY_BUDGET_EXCEEDED):
            result = self.admit(vetoes=(('org.example', 'a', reason),))[0]
            self.assertEqual(result.reason, 'sbom_comparator_refused' if reason == MavenReason.COMPARATOR_REFUSED else 'sbom_policy_unknown')

    def test_missing_version_still_conveys_source_veto(self):
        body = dependencies(dependency('a', group='g')) + repositories(repo(url='https://private.invalid'))
        admission = admit_sources(graph({'pom.xml': pom(body)}), StagedReader())
        self.assertEqual(admission.capabilities, ())
        self.assertEqual(admission._comparator_restrictions, (('g', 'a', MavenReason.COMPARATOR_REFUSED),))
        report = scan_maven('unused', reader_factory=lambda root: Reader({'pom.xml': pom(body)}), supervisor_factory=Metadata())
        self.assertEqual(report._comparator_restrictions, admission._comparator_restrictions)
        self.assertEqual(self.admit([maven_component(group='g', purl='pkg:maven/g/a@1.0')], report._comparator_restrictions)[0].reason, 'sbom_comparator_refused')

    def test_system_assignment_and_metadata_failure_are_distinct(self):
        body = dependencies(dependency('a', '<scope>system</scope>', group='g'))
        admission = admit_sources(graph({'pom.xml': pom(body)}), StagedReader())
        self.assertEqual(admission._comparator_restrictions, (('g', 'a', MavenReason.COMPARATOR_REFUSED),))
        body = dependencies(dependency('a', '<version>1</version>', group='g'))
        report = scan_maven('unused', reader_factory=lambda root: Reader({'pom.xml': pom(body)}), supervisor_factory=Metadata())
        self.assertEqual(report._comparator_restrictions, ())
