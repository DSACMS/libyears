import unittest
from dataclasses import replace
from unittest.mock import patch

from libyears.sbom_document import accept_document
from libyears.sbom_identity import canonical_members, identify, qualifiers
from tests.test_sbom_document import snapshot, synthetic_document


def maven_component(name='a', version='1.0', suffix='', **changes):
    row = {'group': 'org.example', 'name': name, 'version': version,
           'purl': f'pkg:maven/org.example/{name}@{version}{suffix}'}
    row.update(changes)
    return row


class IdentityTests(unittest.TestCase):
    def reason(self, record, expected):
        identity, reason = identify(record)
        self.assertIsNone(identity)
        self.assertEqual(reason, expected)

    def test_literal_identity_and_variant(self):
        for suffix, kind, classifier in (('', 'jar', None), ('?type=jar', 'jar', None),
                                         ('?classifier=sources&type=pom', 'pom', 'sources'),
                                         ('?type=war', 'war', None)):
            identity, reason = identify(maven_component(suffix=suffix))
            self.assertIsNone(reason)
            self.assertEqual((identity.type, identity.classifier), (kind, classifier))
        # Used versions need not pass conservative latest eligibility.
        self.assertIsNotNone(identify(maven_component(version='1.0-rc1'))[0])

    def test_missing_conflicting_unsupported_and_precedence(self):
        for key in ('group', 'name', 'purl'):
            row = maven_component(); del row[key]
            self.reason(row, 'sbom_identity_missing')
        self.reason(maven_component(name='a', purl='pkg:maven/org.example/A@1.0'), 'sbom_identity_conflict')
        self.reason(maven_component(purl='pkg:maven/org%2Eexample/a@1.0'), 'sbom_identity_unsupported')
        self.reason(maven_component(purl='pkg:npm/a@1.0'), 'sbom_identity_unsupported')
        row = maven_component(); del row['version']
        self.reason(row, 'sbom_version_missing')
        self.reason(maven_component(version='1', purl='pkg:maven/org.example/a@2?type=bad'), 'sbom_identity_conflict')
        for version in ('[1,2)', 'LATEST', 'RELEASE', '${x}', '1-SNAPSHOT', '1-20260101.010101-1', ''):
            self.reason(maven_component(version=version), 'sbom_version_missing' if not version else 'sbom_version_unsupported')
        self.reason(maven_component(version='LATEST', suffix='?type=bad'), 'sbom_version_unsupported')

    def test_closed_qualifier_subset(self):
        for suffix in ('?type=test-jar', '?type=custom', '?type=', '?classifier=', '?type=jar&type=jar',
                       '?Type=jar', '?unknown=x', '?classifier=%61', '#subpath', '?repository_url=%zz'):
            self.reason(maven_component(suffix=suffix), 'sbom_identity_unsupported' if suffix.startswith('#') else 'sbom_variant_unsupported')
        url = 'https://repo.maven.apache.org/maven2/'
        values, reason = qualifiers('pkg:maven/g/a@1?repository_url=https:%2F%2Frepo.maven.apache.org%2Fmaven2%2F')
        self.assertIsNone(reason)
        self.assertEqual(values['repository_url'], url)
        self.assertIn('+', qualifiers('pkg:maven/g/a@1?repository_url=a+b')[0]['repository_url'])
        self.assertEqual(qualifiers('pkg:maven/g/a@1?repository_url=%252F')[0]['repository_url'], '%2F')

    def test_groups_preserve_records_refs_and_variants(self):
        records = [maven_component(**{'bom-ref': 'a'}), maven_component(suffix='?type=jar', **{'bom-ref': 'b'}),
                   maven_component(suffix='?classifier=sources'), maven_component(version='2'), {}, {}]
        doc = accept_document(snapshot(synthetic_document(components=records)))
        with patch('socket.socket', side_effect=AssertionError('socket')), patch('subprocess.Popen', side_effect=AssertionError('process')):
            members = canonical_members(doc)
        self.assertEqual(len(members), 5)
        self.assertEqual(sum(m.identity is not None for m in members), 3)
        self.assertEqual(sum(len(m.records) for m in members), 6)
        self.assertEqual([index for index, record in members[0].records], [0, 1])
        self.assertEqual([record['bom-ref'] for index, record in members[0].records], ['a', 'b'])
        self.assertEqual([member.index for member in members], [0, 2, 3, 4, 5])
