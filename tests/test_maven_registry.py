"""T007 pure representations: no network, resolver, target or fallback service."""

from datetime import datetime, timedelta, timezone
import unittest

from libyears.maven_input import MavenInputFailure, parse_xml
from libyears.maven_model import MavenReason
from libyears.maven_registry import (
    MAX_CATALOGUE_BYTES, MAX_POM_BYTES, MavenRepresentation, RegistryFailure,
    catalogue_path, last_modified, pom_date, pom_path, select_target,
)

UTC = timezone.utc
RETRIEVED = datetime(2026, 11, 12, 22, 0, tzinfo=UTC)
DATE = 'Mon, 02 Jan 2023 03:04:05 GMT'
HEADERS = (('Last-Modified', DATE),)
POM = b'<project><modelVersion>4.0.0</modelVersion><groupId>g</groupId><artifactId>a</artifactId><version>1</version></project>'


def response(body, headers=HEADERS, status=200, retrieved=RETRIEVED):
    return MavenRepresentation(status, body, headers, retrieved)


def catalogue(versions=('1', '2'), extra='', namespace=None):
    attribute = '' if namespace is None else f' xmlns="{namespace}"'
    entries = ''.join('<version>' + version + '</version>' for version in versions)
    return (f'<metadata{attribute}><groupId>g</groupId><artifactId>a</artifactId>'
            '<versioning>' + extra + '<versions>' + entries + '</versions></versioning></metadata>').encode()


class MavenCatalogueTests(unittest.TestCase):
    def target(self, body, **kwargs):
        return select_target('g', 'a', response(body, **kwargs))

    def test_complete_list_not_latest_release_lastupdated_or_dates_selects(self):
        selected = self.target(catalogue(('1', '3', '2'), '<latest>999</latest><release>999</release><lastUpdated>bad</lastUpdated>'),
                               headers=(('Last-Modified', 'not a date'),))
        self.assertEqual((selected.version, selected.reason, selected.retrieved_at), ('3', None, RETRIEVED))
        self.assertEqual(selected.ordering_basis, 'maven_comparable_version_3_9_11')
        self.assertEqual(selected.eligibility_policy, 'maven_conservative_stable_v1')

    def test_exact_namespaces_and_case_sensitive_identity(self):
        for namespace in (None, 'http://maven.apache.org/METADATA/1.1.0'):
            self.assertEqual(self.target(catalogue(namespace=namespace)).version, '2')
        for body in (catalogue(namespace='http://maven.apache.org/METADATA/1.0.0'),
                     catalogue().replace(b'<groupId>g', b'<groupId>G'),
                     catalogue().replace(b'<artifactId>a', b'<artifactId>b'),
                     catalogue().replace(b'<artifactId>', b'<artifactId xmlns="foreign">')):
            self.assertEqual(self.target(body).reason, MavenReason.CATALOGUE_UNAVAILABLE)

    def test_whole_representation_requires_identity_singletons_and_complete_framing(self):
        bodies = (
            catalogue()[:-12], b'<error>not found</error>',
            catalogue().replace(b'<groupId>g</groupId>', b''),
            catalogue().replace(b'<groupId>g</groupId>', b'<groupId>g</groupId><groupId>g</groupId>'),
            catalogue().replace(b'<versioning>', b'<versioning><latest>1</latest><latest>2</latest>'),
            catalogue().replace(b'</versioning>', b'</versioning><versioning/>'),
            catalogue().replace(b'<versions>', b'<versions/><versions>'),
            catalogue().replace(b'<versions>', b'<versions>mixed'),
            catalogue().replace(b'<version>1</version>', b'<version><nested/></version>'),
            catalogue().replace(b'<version>1</version>', b'<version attr="unknown">1</version>'),
            catalogue().replace(b'<versions>', b'<versions><unknown/>'),
            b'<!DOCTYPE metadata [<!ENTITY x "text">]>' + catalogue(),
        )
        for body in bodies:
            with self.subTest(body=body[:80]):
                self.assertEqual(self.target(body).reason, MavenReason.CATALOGUE_UNAVAILABLE)
        for status in (301, 304, 404, 500, True):
            self.assertIsNone(self.target(catalogue(), status=status).version)

    def test_no_versions_list_cannot_be_replaced_by_latest_release(self):
        body = b'<metadata><groupId>g</groupId><artifactId>a</artifactId><versioning><latest>3</latest><release>2</release></versioning></metadata>'
        self.assertEqual(self.target(body).reason, MavenReason.CATALOGUE_UNAVAILABLE)
        self.assertEqual(self.target(catalogue(())).reason, MavenReason.NO_STABLE_RELEASE)

    def test_all_entries_must_be_safe_even_when_another_candidate_is_obviously_greatest(self):
        for version in ('', 'LATEST', 'RELEASE', '[1,2)', '${v}', '../1', '1%2F2', '1:2', '1\\2', 'é', 'x' * 257):
            with self.subTest(version=version):
                self.assertEqual(self.target(catalogue(('999', version))).reason, MavenReason.CATALOGUE_UNAVAILABLE)
        self.assertEqual(self.target(catalogue(('9' * 129, '1'))).reason,
                         MavenReason.METADATA_BUDGET_EXCEEDED)

    def test_catalogue_versions_and_ga_are_never_whitespace_normalized(self):
        for text in (' 1 ', '\u00a01\u00a0', '\t1', '1\n'):
            with self.subTest(text=text):
                self.assertEqual(self.target(catalogue(('1', text))).reason,
                                 MavenReason.CATALOGUE_UNAVAILABLE)
                self.assertEqual(self.target(catalogue(('999', text))).reason,
                                 MavenReason.CATALOGUE_UNAVAILABLE)
        for field, value in (('groupId', 'g'), ('artifactId', 'a')):
            for padding in (' ', '\u00a0'):
                original = f'<{field}>{value}</{field}>'.encode()
                replacement = f'<{field}>{padding}{value}{padding}</{field}>'.encode()
                self.assertEqual(self.target(catalogue().replace(original, replacement)).reason,
                                 MavenReason.CATALOGUE_UNAVAILABLE)

    def test_selected_eligibility_ties_duplicates_and_unknowns(self):
        cases = (
            (('1', '1'), '1', None),
            (('1', '1.0'), None, MavenReason.AMBIGUOUS_LATEST_VERSION),
            (('1-foo', '2'), '2', None),
            (('1', '2-preview'), None, MavenReason.UNKNOWN_LATEST_ELIGIBILITY),
            (('1', '2-RC1', '2-M1', '2-SNAPSHOT', '2-20261112.120000-1'), '1', None),
            (('1', '1-sp2'), '1-sp2', None),
        )
        for versions, expected, reason in cases:
            with self.subTest(versions=versions):
                result = self.target(catalogue(versions))
                self.assertEqual((result.version, result.reason), (expected, reason))

    def test_entry_limit_counts_identical_duplicates_before_collapse(self):
        self.assertEqual(self.target(catalogue(('1',) * 10000)).version, '1')
        self.assertEqual(self.target(catalogue(('1',) * 10001)).reason,
                         MavenReason.METADATA_BUDGET_EXCEEDED)

    def test_response_and_common_structural_budgets(self):
        self.assertEqual(self.target(b'x' * (MAX_CATALOGUE_BYTES + 1)).reason,
                         MavenReason.METADATA_BUDGET_EXCEEDED)
        body = catalogue().replace(b'<versioning>', b'<!--' + b'x' * (1024 * 1024) + b'--><versioning>')
        self.assertEqual(self.target(body).version, '2')
        with self.assertRaises(MavenInputFailure):
            parse_xml(body)  # local XML's default 1MiB limit is unchanged
        deep = b'<x>' * 33 + b'</x>' * 33
        self.assertEqual(self.target(deep).reason, MavenReason.METADATA_BUDGET_EXCEEDED)

    def test_current_catalogue_disappearance_has_no_persisted_maximum(self):
        self.assertEqual(self.target(catalogue(('1', '2'))).version, '2')
        self.assertEqual(self.target(catalogue(('1',))).version, '1')
        self.assertIsNone(self.target(b'not found', status=404).version)


class MavenPomDateTests(unittest.TestCase):
    def date(self, body=POM, **kwargs):
        return pom_date('g', 'a', '1', response(body, **kwargs))

    def test_literal_identity_date_and_retrieval_are_distinct_utc_facts(self):
        result = self.date()
        self.assertEqual(result.last_modified, datetime(2023, 1, 2, 3, 4, 5, tzinfo=UTC))
        self.assertEqual(result.retrieved_at, RETRIEVED)
        self.assertNotEqual(result.last_modified, result.retrieved_at)
        self.assertEqual(result.time_basis, 'maven_conventional_pom_last_modified')
        offset = RETRIEVED.astimezone(timezone(timedelta(hours=-5)))
        self.assertEqual(self.date(retrieved=offset), result)
        for namespace in ('', ' xmlns="http://maven.apache.org/POM/4.0.0"'):
            self.assertIsNotNone(self.date(POM.replace(b'<project>', ('<project' + namespace + '>').encode())).last_modified)

    def test_literal_parent_identity_is_local_to_this_representation_and_never_fetched(self):
        for fields in ('<groupId>g</groupId><version>1</version>', '<groupId>g</groupId>', '<version>1</version>'):
            parent = '<parent><groupId>g</groupId><artifactId>unknown-parent</artifactId><version>1</version><relativePath>/never/read</relativePath></parent>'
            child = ('<project>' + parent + '<artifactId>a</artifactId>' + fields + '</project>').encode()
            self.assertIsNotNone(self.date(child).last_modified)
        body = b'<project><parent><groupId>g</groupId><version>${v}</version></parent><artifactId>a</artifactId></project>'
        self.assertIsNone(self.date(body).last_modified)

    def test_exact_identity_mismatch_unresolved_duplicates_and_relocation_refuse(self):
        bodies = (
            POM.replace(b'<groupId>g', b'<groupId>G'), POM.replace(b'<artifactId>a', b'<artifactId>b'),
            POM.replace(b'<version>1', b'<version>1.0'), POM.replace(b'<version>1', b'<version>${v}'),
            POM.replace(b'<version>1</version>', b'<version>1</version><version>1</version>'),
            POM.replace(b'</project>', b'<distributionManagement><relocation/></distributionManagement></project>'),
            POM.replace(b'</project>', b'<distributionManagement><relocation xmlns="foreign"/></distributionManagement></project>'),
            POM.replace(b'<artifactId>a</artifactId>', b''), POM.replace(b'<project>', b'<project xmlns="foreign">'),
            POM[:-10], b'<error/>', b'<!DOCTYPE project>' + POM,
        )
        for body in bodies:
            with self.subTest(body=body[:100]):
                result = self.date(body)
                self.assertIsNone(result.last_modified)
                self.assertEqual(result.reason, MavenReason.TIME_BASIS_UNAVAILABLE)

    def test_direct_and_parent_pom_identity_text_is_never_normalized(self):
        for field, value in (('groupId', 'g'), ('artifactId', 'a'), ('version', '1')):
            for padding in (' ', '\u00a0'):
                original = f'<{field}>{value}</{field}>'.encode()
                replacement = f'<{field}>{padding}{value}{padding}</{field}>'.encode()
                self.assertIsNone(self.date(POM.replace(original, replacement)).last_modified)
        parent = ('<project><parent><groupId>g</groupId><version>1</version></parent>'
                  '<artifactId>a</artifactId></project>').encode()
        for field, value in (('groupId', 'g'), ('version', '1')):
            for padding in (' ', '\u00a0'):
                original = f'<{field}>{value}</{field}>'.encode()
                replacement = f'<{field}>{padding}{value}{padding}</{field}>'.encode()
                self.assertIsNone(self.date(parent.replace(original, replacement)).last_modified)
        self.assertIsNotNone(self.date(parent).last_modified)

    def test_unrelated_build_dependency_properties_and_bom_parent_references_are_not_evaluated(self):
        extra = b'<build><unknown>${host}</unknown></build><dependencies><arbitrary/></dependencies><properties><v>not-evaluated</v></properties><parent><groupId>not-this</groupId><artifactId>not-fetched</artifactId><version>${unknown}</version></parent>'
        self.assertIsNotNone(self.date(POM.replace(b'</project>', extra + b'</project>')).last_modified)

    def test_missing_duplicate_conflicting_and_fallback_headers_do_not_supply_dates(self):
        for headers in ((), (('Date', DATE),), (('Last-Modified', DATE), ('last-modified', DATE)),
                        (('Last-Modified', DATE), ('LAST-MODIFIED', 'Tue, 03 Jan 2023 03:04:05 GMT')),
                        (('ETag', DATE),), (('Last-Modified', DATE + ', ' + DATE),)):
            with self.subTest(headers=headers):
                self.assertIsNone(self.date(headers=headers).last_modified)
        self.assertIsNotNone(self.date(headers=(('last-modified', DATE), ('Date', 'ignored'))).last_modified)

    def test_strict_imf_fixdate_impossible_dates_weekday_timezone_and_future_refuse(self):
        dates = ('not a date', 'Monday, 02-Jan-23 03:04:05 GMT', 'Mon Jan  2 03:04:05 2023',
                 'Mon, 2 Jan 2023 03:04:05 GMT', 'Mon, 02 Jan 2023 03:04:05',
                 'Mon, 02 Jan 2023 03:04:05 UTC', 'Mon, 02 Jan 2023 03:04:05 +0000',
                 'Tue, 02 Jan 2023 03:04:05 GMT', 'Wed, 31 Feb 2024 03:04:05 GMT',
                 'Mon, 02 Jan 2023 24:04:05 GMT', 'Mon, 02 Jan 2023 03:04:60 GMT',
                 'Fri, 13 Nov 2026 03:04:05 GMT', DATE + '\r\n', ' ' + DATE)
        for date in dates:
            with self.subTest(date=date):
                self.assertIsNone(self.date(headers=(('Last-Modified', date),)).last_modified)
        leap = 'Thu, 29 Feb 2024 12:00:00 GMT'
        self.assertEqual(last_modified((('Last-Modified', leap),), RETRIEVED).day, 29)

    def test_non_200_and_pom_budget_refuse_even_if_body_and_header_look_valid(self):
        for status in (301, 304, 404, 500, True):
            self.assertIsNone(self.date(status=status).last_modified)
        self.assertIsNone(self.date(b'x' * (MAX_POM_BYTES + 1)).last_modified)

    def test_measured_version_absent_from_catalogue_still_has_independent_exact_date(self):
        target = select_target('g', 'a', response(catalogue(('2', '3'))))
        self.assertEqual(target.version, '3')
        self.assertIsNotNone(self.date().last_modified)

    def test_missing_maximum_date_never_selects_older_or_uses_same_version_zero(self):
        selected = select_target('g', 'a', response(catalogue(('1', '2'))))
        maximum = pom_date('g', 'a', selected.version, response(POM.replace(b'<version>1', b'<version>2'), headers=()))
        self.assertEqual(selected.version, '2')
        self.assertIsNone(maximum.last_modified)
        same = select_target('g', 'a', response(catalogue(('1',))))
        self.assertEqual(same.version, '1')
        self.assertIsNone(self.date(headers=()).last_modified)


class MavenRegistryPathTests(unittest.TestCase):
    def test_fixed_paths_preserve_case_and_percent_encode_plus_without_host_input(self):
        self.assertEqual(catalogue_path('Org.Example', 'Artifact'),
                         '/maven2/Org/Example/Artifact/maven-metadata.xml')
        self.assertEqual(pom_path('org.example', 'a', '1+build'),
                         '/maven2/org/example/a/1%2Bbuild/a-1%2Bbuild.pom')
        self.assertEqual(pom_path('g', 'a', '1.Final'), '/maven2/g/a/1.Final/a-1.Final.pom')

    def test_unsafe_coordinates_versions_and_snapshot_paths_refuse_before_transport(self):
        for group, artifact in (('a..b', 'a'), ('g', '..'), ('g/x', 'a'), ('g', 'a%2fsecret'),
                                ('g', 'https://private'), ('é', 'a'), ('g', 'a' * 129)):
            with self.assertRaises(RegistryFailure):
                catalogue_path(group, artifact)
        for version in ('../1', '1/2', '1%2F2', 'LATEST', '[1]', '1-SNAPSHOT', '1-20261112.120000-1'):
            with self.assertRaises(RegistryFailure):
                pom_path('g', 'a', version)

    def test_invalid_retrieval_time_never_becomes_a_date(self):
        for value in (None, datetime(2023, 1, 1), 'now'):
            with self.assertRaises(RegistryFailure):
                pom_date('g', 'a', '1', response(POM, retrieved=value))


if __name__ == '__main__':
    unittest.main()
