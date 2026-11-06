"""Synthetic public metadata, content/date authority and supervised composition."""

import base64
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timezone
import json
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from libyears import nuget_registry as registry
from libyears.nuget_provenance import LocalAuthority
from libyears.nuget_supervisor import (NuGetSupervisor, PackageResult, read_message,
                                      write_message, result_message, decode_result)
from libyears.registry import TransportFailure

AUTHORITY = LocalAuthority('a' * 64, 'b' * 64, 'example', '1.0.0', b'x' * 64)
INDEX = registry.REGISTRATION_BASE + 'example/index.json'
HASH = base64.b64encode(b'x' * 64).decode('ascii')
DATE = '2020-01-01T00:00:00Z'


def catalog_url(version, tag=''):
    return 'https://api.nuget.org/v3/catalog0/data/2020.01.01/example.' + version + tag + '.json'


def leaf(version, *, listed=True, tag=''):
    entry = {'@id': catalog_url(version, tag), 'id': 'Example', 'version': version}
    if listed is not None:
        entry['listed'] = listed
    return {'@id': registry.REGISTRATION_BASE + 'example/' + version + tag + '.json',
            'catalogEntry': entry, 'packageContent': 'https://private.invalid/SECRET.nupkg'}


def page(leaves, lower=None, upper=None, tag=''):
    lower = lower or leaves[0]['catalogEntry']['version']
    upper = upper or leaves[-1]['catalogEntry']['version']
    return {'@id': INDEX + '#page/' + lower + '/' + upper if not tag else
            registry.REGISTRATION_BASE + 'example/page' + tag + '.json',
            'count': len(leaves), 'lower': lower, 'upper': upper, 'items': leaves}


def fixture(versions=('1.0.0', '2.0.0')):
    leaves = [leaf(version) for version in versions]
    documents = {registry.SERVICE_INDEX: {'resources': [
        {'@type': 'RegistrationsBaseUrl/3.6.0', '@id': registry.REGISTRATION_BASE}]},
        INDEX: {'count': 1, 'items': [page(leaves)]}}
    for item in leaves:
        entry = item['catalogEntry']
        documents[entry['@id']] = dict(entry, **{'@type': ['PackageDetails'],
            'packageHash': HASH, 'packageHashAlgorithm': 'SHA512', 'created': DATE,
            'published': '2030-01-01T00:00:00Z', 'catalog:commitTimeStamp': '2040-01-01T00:00:00Z'})
    return documents


class Transport:
    def __init__(self, documents):
        self.documents = documents
        self.urls = []

    def get(self, url):
        self.urls.append(url)
        value = self.documents[url]
        if isinstance(value, TransportFailure):
            return value
        if isinstance(value, Exception):
            raise value
        return json.dumps(value).encode('utf-8')


class RegistryTests(unittest.TestCase):
    def lookup(self, documents=None, authority=AUTHORITY, **options):
        self.transport = Transport(documents if documents is not None else fixture())
        self.client = registry.NuGetMetadataClient(transport=self.transport, clock=lambda: 100)
        self.client.begin_package(authority.package_key)
        for key, value in options.items():
            setattr(self.client, key, value)
        try:
            result = registry.lookup_authorized_package(authority, self.client)
        except registry.NuGetRegistryFailure as failure:
            result = PackageResult(reason=failure.reason)
        # Every result must fit the actual worker's typed privacy boundary.
        self.assertEqual(decode_result(result_message(result)), result)
        return result

    def test_created_only_success_and_default_listing(self):
        docs = fixture()
        del docs[INDEX]['items'][0]['items'][0]['catalogEntry']['listed']
        result = self.lookup(docs)
        self.assertIsNone(result.reason)
        self.assertEqual(result.origin_state, 'public_content_verified')
        self.assertEqual(result.content_hash_state, 'public_agreement')
        self.assertEqual(result.used_publication.created, datetime(2020, 1, 1, tzinfo=timezone.utc))
        self.assertEqual(result.latest_publication.version, '2.0.0')
        self.assertTrue(all('SECRET' not in url for url in self.transport.urls))

    def test_readable_registration_catalog_fixture(self):
        path = Path(__file__).parent / 'fixtures/nuget/registry-public.json'
        result = self.lookup(json.loads(path.read_text()))
        self.assertIsNone(result.reason)
        self.assertEqual(result.latest_publication.version, '2.0.0')

    def test_selected_identity_type_and_classification_matrix(self):
        for field, values in {'id': ['other', None], 'version': ['2.0.0', '1'],
                              '@type': [None, 'PackageDelete', ['PackageDetails', 'PackageDelete']],
                              'isPrerelease': [True, 'false']}.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    docs = fixture()
                    docs[catalog_url('1.0.0')][field] = value
                    self.assertEqual(self.lookup(docs).reason, 'invalid_registry_response')

    def test_public_hash_matrix_and_hash_before_date(self):
        for changes, expected, state in [
            ({'packageHash': None}, 'content_hash_unavailable', 'unavailable'),
            ({'packageHash': 'bad'}, 'content_hash_unavailable', 'unavailable'),
            ({'packageHashAlgorithm': 'SHA256'}, 'content_hash_unavailable', 'unavailable'),
            ({'packageHash': base64.b64encode(b'y' * 64).decode()}, 'content_hash_mismatch', 'mismatch')]:
            docs = fixture()
            docs[catalog_url('1.0.0')].update(changes, created=None)
            result = self.lookup(docs)
            self.assertEqual((result.reason, result.content_hash_state), (expected, state))
            self.assertIsNone(result.used_publication)

    def test_absent_package_used_and_catalog_before_hash_dates(self):
        for location, expected in [(INDEX, 'package_not_found'),
                                   (catalog_url('1.0.0'), 'version_not_found')]:
            docs = fixture()
            docs[location] = TransportFailure(404, 'SECRET')
            self.assertEqual(self.lookup(docs).reason, expected)
        result = self.lookup(fixture(('2.0.0',)))
        self.assertEqual(result.reason, 'version_not_found')
        self.assertEqual(self.transport.urls, [registry.SERVICE_INDEX, INDEX])

    def test_timestamp_fraction_offset_matrix(self):
        for digits in range(8):
            fraction = '.' + '1234567'[:digits] if digits else ''
            docs = fixture()
            docs[catalog_url('1.0.0')]['created'] = '2020-01-01T01:30:00' + fraction + '+01:30'
            result = self.lookup(docs)
            self.assertIsNone(result.reason)
            self.assertEqual(result.used_publication.created.hour, 0)
            self.assertEqual(result.used_publication.created.microsecond,
                             int(('1234567'[:digits] + '000000')[:6]))

    def test_missing_invalid_sentinel_naive_used_and_latest_no_fallback(self):
        for version in ('1.0.0', '2.0.0'):
            for date in (None, '', DATE[:-1], '1900-01-01T00:00:00Z',
                         '2020-02-31T00:00:00Z', '2020-01-01T00:00:00.12345678Z'):
                docs = fixture()
                docs[catalog_url(version)]['created'] = date
                result = self.lookup(docs)
                self.assertEqual(result.reason, 'release_date_missing')
                self.assertIsNone(result.latest_publication)
                self.assertEqual(result.used_publication is None, version == '1.0.0')
        docs = fixture()
        docs[catalog_url('2.0.0')] = TransportFailure(404, 'SECRET')
        self.assertEqual(self.lookup(docs).reason, 'release_date_missing')

    def test_creation_conflict_is_invalid_response(self):
        docs = fixture()
        docs[INDEX]['items'][0]['items'][0]['catalogEntry']['created'] = '2021-01-01T00:00:00Z'
        self.assertEqual(self.lookup(docs).reason, 'invalid_registry_response')

    def test_latest_numeric_revision_and_listing_independent_of_dates(self):
        for versions, expected in [(('1.0.0', '1.9.0', '1.10.0'), '1.10.0'),
                                   (('1.0.0', '1.0.0.1'), '1.0.0.1'),
                                   (('1.0.0', '2.0.0-beta.1', '3.0.0'), '3.0.0')]:
            docs = fixture(versions)
            self.assertEqual(self.lookup(docs).latest_publication.version, expected)
        docs = fixture(('1.0.0', '2.0.0', '9.0.0'))
        docs[INDEX]['items'][0]['items'][-1]['catalogEntry']['listed'] = False
        docs[catalog_url('2.0.0')]['created'] = '2019-01-01T00:00:00Z'
        self.assertEqual(self.lookup(docs).latest_publication.version, '2.0.0')

    def test_unlisted_prerelease_used_and_no_stable(self):
        docs = fixture(('1.0.0-BETA+build', '2.0.0'))
        docs[INDEX]['items'][0]['items'][0]['catalogEntry']['listed'] = False
        docs[catalog_url('1.0.0-BETA+build')]['listed'] = False
        result = self.lookup(docs, replace(AUTHORITY, normalized_version='1.0.0-beta'))
        self.assertIsNone(result.reason)
        self.assertFalse(result.used_publication.listed)
        docs = fixture(('1.0.0',))
        docs[INDEX]['items'][0]['items'][0]['catalogEntry']['listed'] = False
        docs[catalog_url('1.0.0')]['listed'] = False
        self.assertEqual(self.lookup(docs).reason, 'no_stable_release')

    def test_catalog_type_alias_and_normalized_identity(self):
        docs = fixture(('01.0+BUILD',))
        docs[catalog_url('01.0+BUILD')]['@type'] = ['nuget:PackageDetails', 'OtherMetadata']
        result = self.lookup(docs)
        self.assertIsNone(result.reason)
        self.assertEqual(result.used_publication.version, '1.0.0')
        self.assertEqual(result.used_publication, result.latest_publication)

    def test_registration_structure_count_bounds_flags_matrix(self):
        mutations = [
            lambda d: d[INDEX].update(count=True),
            lambda d: d[INDEX].update(count=2),
            lambda d: d[INDEX]['items'][0].update(count=3),
            lambda d: d[INDEX]['items'][0].update(lower='0.1.0'),
            lambda d: d[INDEX]['items'][0].update(upper='0.1.0'),
            lambda d: d[INDEX]['items'][0]['items'][0]['catalogEntry'].update(id='other'),
            lambda d: d[INDEX]['items'][0]['items'][0]['catalogEntry'].update(version='1'),
            lambda d: d[INDEX]['items'][0]['items'][1]['catalogEntry'].update(listed='true'),
            lambda d: d[INDEX]['items'][0]['items'][1]['catalogEntry'].update(isPrerelease=True),
            lambda d: d[INDEX]['items'][0]['items'][1].update(listed=False),
            lambda d: d[INDEX]['items'].append(deepcopy(d[INDEX]['items'][0])),
        ]
        for mutation in mutations:
            docs = fixture()
            mutation(docs)
            self.assertEqual(self.lookup(docs).reason, 'invalid_registry_response')

    def test_service_resource_missing_conflicting_and_no_legacy_fallback(self):
        for resources in ([], [{'@type': 'RegistrationsBaseUrl/3.4.0', '@id': registry.REGISTRATION_BASE}],
                          [{'@type': 'RegistrationsBaseUrl/3.6.0', '@id': 'https://private.invalid/SECRET'}]):
            docs = fixture()
            docs[registry.SERVICE_INDEX]['resources'] = resources
            self.assertEqual(self.lookup(docs).reason, 'invalid_registry_response')
            self.assertEqual(self.transport.urls, [registry.SERVICE_INDEX])

    def test_external_pages_sorted_complete_and_reordering_invariant(self):
        docs = fixture(('1.0.0', '2.0.0'))
        leaves = docs[INDEX]['items'][0]['items']
        pages = [page([item], tag=str(index)) for index, item in enumerate(leaves)]
        for item in pages:
            docs[item['@id']] = deepcopy(item)
        docs[INDEX] = {'count': 2, 'items': [{k: v for k, v in item.items() if k != 'items'} for item in pages]}
        first = self.lookup(docs)
        schedule = self.transport.urls
        docs[INDEX]['items'].reverse()
        self.assertEqual(self.lookup(docs), first)
        self.assertEqual(self.transport.urls, schedule)
        self.assertEqual(schedule[2:4], sorted(item['@id'] for item in pages))
        del docs[pages[1]['@id']]['items']
        self.assertEqual(self.lookup(docs).reason, 'invalid_registry_response')

    def test_equivalent_aliases_require_material_agreement(self):
        docs = fixture(('1.0.0', '01.0+build', '2.0.0'))
        self.assertIsNone(self.lookup(docs).reason)
        for field, value in [('created', '2021-01-01T00:00:00Z'),
                             ('packageHash', base64.b64encode(b'y' * 64).decode()), ('listed', False)]:
            changed = deepcopy(docs)
            changed[catalog_url('01.0+build')][field] = value
            self.assertEqual(self.lookup(changed).reason, 'invalid_registry_response')
        # Even aliases outside used/latest need material reconciliation.
        docs = fixture(('1.0.0', '2.0.0', '02.0+build', '3.0.0'))
        docs[catalog_url('02.0+build')]['created'] = '2021-01-01T00:00:00Z'
        self.assertEqual(self.lookup(docs).reason, 'invalid_registry_response')

    def test_missing_alias_document_or_material_cannot_prove_agreement(self):
        for value in (TransportFailure(404, 'SECRET'), None):
            docs = fixture(('1.0.0', '2.0.0', '02.0+build', '3.0.0'))
            if value is None:
                del docs[catalog_url('02.0+build')]['created']
            else:
                docs[catalog_url('02.0+build')] = value
            self.assertEqual(self.lookup(docs).reason, 'invalid_registry_response')

    def alias_fixture(self, role):
        aliases = {'used': ('1.0.0', '01.0+build'),
                   'middle': ('2.0.0', '02.0+build'),
                   'latest': ('3.0.0', '03.0+build')}[role]
        versions = ['1.0.0', '2.0.0', '3.0.0']
        versions.insert(versions.index(aliases[0]) + 1, aliases[1])
        return fixture(versions), aliases

    def test_both_aliases_need_usable_hash_algorithm_and_creation_material(self):
        mutations = [
            ('missing_hash', {'packageHash': None}, {'packageHash': None}),
            ('missing_algorithm', {'packageHashAlgorithm': None}, {'packageHashAlgorithm': None}),
            ('missing_created', {'created': None}, {'created': None}),
            ('missing_all', {'packageHash': None, 'packageHashAlgorithm': None, 'created': None},
             {'packageHash': None, 'packageHashAlgorithm': None, 'created': None}),
            ('invalid_hash', {'packageHash': 'bad'}, {'packageHash': 'bad'}),
            ('different_invalid_hash', {'packageHash': 'bad'}, {'packageHash': 'also-bad'}),
            ('short_hash', {'packageHash': base64.b64encode(b'x').decode()},
             {'packageHash': base64.b64encode(b'y').decode()}),
            ('invalid_algorithm', {'packageHashAlgorithm': 'SHA256'}, {'packageHashAlgorithm': 'SHA256'}),
            ('different_invalid_algorithm', {'packageHashAlgorithm': 'SHA256'},
             {'packageHashAlgorithm': 'sha512'}),
            ('invalid_created', {'created': 'invalid'}, {'created': 'invalid'}),
            ('different_invalid_created', {'created': 'invalid'}, {'created': 'also-invalid'}),
            ('naive_created', {'created': DATE[:-1]}, {'created': DATE[:-1]}),
            ('sentinel_created', {'created': '1900-01-01T00:00:00Z'},
             {'created': '1900-01-01T00:00:00Z'}),
        ]
        for role in ('used', 'middle', 'latest'):
            for name, first_changes, second_changes in mutations:
                with self.subTest(role=role, material=name):
                    docs, aliases = self.alias_fixture(role)
                    for version, changes in zip(aliases, (first_changes, second_changes)):
                        document = docs[catalog_url(version)]
                        for field, value in changes.items():
                            if value is None:
                                del document[field]
                            else:
                                document[field] = value
                    result = self.lookup(docs)
                    self.assertEqual(result, PackageResult(reason='invalid_registry_response'))
                    schedule = self.transport.urls
                    docs[INDEX]['items'][0]['items'].reverse()
                    docs = {url: dict(reversed(list(value.items())))
                            for url, value in reversed(list(docs.items()))}
                    self.assertEqual(self.lookup(docs), result)
                    self.assertEqual(self.transport.urls, schedule)

    def test_valid_equal_and_conflicting_alias_material_at_every_position(self):
        for role in ('used', 'middle', 'latest'):
            with self.subTest(role=role):
                docs, aliases = self.alias_fixture(role)
                # Different timestamp spellings still establish the same UTC date.
                docs[catalog_url(aliases[1])]['created'] = '2020-01-01T01:00:00+01:00'
                result = self.lookup(docs)
                self.assertIsNone(result.reason)
                self.assertEqual(result.latest_publication.version, '3.0.0')
                for field, value in [('created', '2021-01-01T00:00:00Z'),
                                     ('packageHash', base64.b64encode(b'y' * 64).decode()),
                                     ('listed', False)]:
                    with self.subTest(field=field):
                        changed = deepcopy(docs)
                        changed[catalog_url(aliases[1])][field] = value
                        self.assertEqual(self.lookup(changed),
                                         PackageResult(reason='invalid_registry_response'))

    def test_singleton_unavailable_material_preserves_reason_and_evidence_stages(self):
        for field in ('packageHash', 'packageHashAlgorithm', 'created'):
            for missing in (True, False):
                with self.subTest(field=field, missing=missing):
                    docs = fixture()
                    if missing:
                        del docs[catalog_url('1.0.0')][field]
                    else:
                        docs[catalog_url('1.0.0')][field] = 'invalid'
                    result = self.lookup(docs)
                    if field == 'created':
                        self.assertEqual(result, PackageResult(reason='release_date_missing',
                            origin_state='public_content_verified', content_hash_state='public_agreement'))
                    else:
                        self.assertEqual(result, PackageResult(reason='content_hash_unavailable',
                                                              content_hash_state='unavailable'))
                    docs[catalog_url('1.0.0')] = TransportFailure(404, 'SECRET')
                    self.assertEqual(self.lookup(docs), PackageResult(reason='version_not_found'))
        for field in ('packageHash', 'packageHashAlgorithm', 'created'):
            with self.subTest(latest_field=field):
                docs = fixture()
                del docs[catalog_url('2.0.0')][field]
                result = self.lookup(docs)
                if field == 'created':
                    self.assertEqual(result.reason, 'release_date_missing')
                    self.assertIsNotNone(result.used_publication)
                    self.assertIsNone(result.latest_publication)
                    self.assertEqual(result.origin_state, 'public_content_verified')
                    self.assertEqual(result.content_hash_state, 'public_agreement')
                else:
                    # A singleton latest needs no binding to a local artifact.
                    self.assertIsNone(result.reason)
                    self.assertEqual(result.latest_publication.version, '2.0.0')

    def test_shared_catalog_document_still_requires_usable_duplicate_material(self):
        for role in ('used', 'middle', 'latest'):
            for field in ('packageHash', 'packageHashAlgorithm', 'created'):
                with self.subTest(role=role, field=field):
                    docs, aliases = self.alias_fixture(role)
                    leaves = docs[INDEX]['items'][0]['items']
                    for item in leaves:
                        if item['catalogEntry']['version'] == aliases[1]:
                            item['catalogEntry']['@id'] = catalog_url(aliases[0])
                    self.assertIsNone(self.lookup(docs).reason)
                    self.assertEqual(self.transport.urls.count(catalog_url(aliases[0])), 1)
                    del docs[catalog_url(aliases[0])][field]
                    self.assertEqual(self.lookup(docs), PackageResult(reason='invalid_registry_response'))

    def test_used_absence_precedes_unavailable_duplicate_material(self):
        for absent in ('registration', 'catalog'):
            with self.subTest(absent=absent):
                docs, aliases = self.alias_fixture('middle')
                for version in aliases:
                    del docs[catalog_url(version)]['created']
                    del docs[catalog_url(version)]['packageHash']
                if absent == 'registration':
                    leaves = docs[INDEX]['items'][0]['items'][1:]
                    docs[INDEX]['items'] = [page(leaves)]
                else:
                    docs[catalog_url('1.0.0')] = TransportFailure(404, 'SECRET')
                self.assertEqual(self.lookup(docs), PackageResult(reason='version_not_found'))

    def test_prereleases_can_span_equal_numeric_page_boundaries(self):
        versions = ('1.0.0-a', '1.0.0-b', '2.0.0')
        docs = fixture(versions)
        leaves = docs[INDEX]['items'][0]['items']
        docs[INDEX] = {'count': 3, 'items': [page([item]) for item in leaves]}
        result = self.lookup(docs, replace(AUTHORITY, normalized_version='1.0.0-a'))
        self.assertIsNone(result.reason)
        self.assertEqual(result.latest_publication.version, '2.0.0')

    def test_missing_external_page_and_overlap_reject_complete_latest(self):
        docs = fixture()
        original = docs[INDEX]['items'][0]
        url = registry.REGISTRATION_BASE + 'example/page.json'
        docs[INDEX]['items'][0] = {k: v for k, v in original.items() if k != 'items'}
        docs[INDEX]['items'][0]['@id'] = url
        docs[url] = TransportFailure(404, 'SECRET')
        self.assertEqual(self.lookup(docs).reason, 'invalid_registry_response')
        docs = fixture(('1.0.0', '2.0.0', '3.0.0', '4.0.0'))
        leaves = docs[INDEX]['items'][0]['items']
        docs[INDEX] = {'count': 2, 'items': [page([leaves[0], leaves[2]]), page([leaves[1], leaves[3]])]}
        self.assertEqual(self.lookup(docs).reason, 'invalid_registry_response')

    def test_hostile_links_never_fetched_including_inline_page_identifier(self):
        for location in ('page', 'leaf', 'catalog'):
            docs = fixture()
            target = docs[INDEX]['items'][0]
            if location == 'leaf':
                target = target['items'][0]
            elif location == 'catalog':
                target = target['items'][0]['catalogEntry']
            target['@id'] = 'https://private.invalid/SECRET'
            self.assertEqual(self.lookup(docs).reason, 'invalid_registry_response')
            self.assertTrue(all('SECRET' not in url for url in self.transport.urls))

    def test_page_version_request_limits_and_no_partial_latest(self):
        for limit, value in [('MAX_PAGES', 0), ('MAX_VERSIONS', 1), ('MAX_PACKAGE_REQUESTS', 2)]:
            with patch.object(registry, limit, value):
                result = self.lookup()
            expected = 'registry_error' if limit == 'MAX_PACKAGE_REQUESTS' else 'invalid_registry_response'
            self.assertEqual(result.reason, expected)
            self.assertIsNone(result.latest_publication)

    def test_service_index_cached_and_cooldown_scan_counters_retained(self):
        transport = Transport(fixture())
        client = registry.NuGetMetadataClient(transport=transport, clock=lambda: 100)
        for unused in range(2):
            client.begin_package('example')
            self.assertIsNone(registry.lookup_authorized_package(AUTHORITY, client).reason)
        self.assertEqual(transport.urls.count(registry.SERVICE_INDEX), 1)
        self.assertEqual(client.scan_requests, 7)
        transport.documents[INDEX] = TransportFailure(429, 'SECRET', retry_after='10')
        client.begin_package('example')
        with self.assertRaises(registry.NuGetRegistryFailure):
            registry.lookup_authorized_package(AUTHORITY, client)
        count = len(transport.urls)
        client.begin_package('example')
        with self.assertRaises(registry.NuGetRegistryFailure):
            registry.lookup_authorized_package(AUTHORITY, client)
        self.assertEqual(len(transport.urls), count)

    def test_registry_reason_trigger_table(self):
        table = json.loads((Path(__file__).parent / 'fixtures/nuget/registry-reason-triggers.json').read_text())
        observed = {}
        cases = [
            ('package_not_found', INDEX, TransportFailure(404, 'SECRET')),
            ('version_not_found', catalog_url('1.0.0'), TransportFailure(404, 'SECRET')),
            ('registry_error', INDEX, TimeoutError('SECRET')),
            ('invalid_registry_response', INDEX, {}),
        ]
        for reason, url, value in cases:
            docs = fixture()
            docs[url] = value
            observed[reason] = self.lookup(docs).reason
        docs = fixture(('1.0.0',))
        docs[INDEX]['items'][0]['items'][0]['catalogEntry']['listed'] = False
        docs[catalog_url('1.0.0')]['listed'] = False
        observed['no_stable_release'] = self.lookup(docs).reason
        for reason, field, value in [('content_hash_unavailable', 'packageHash', None),
                                      ('content_hash_mismatch', 'packageHash', base64.b64encode(b'y'*64).decode()),
                                      ('release_date_missing', 'created', None)]:
            docs = fixture()
            docs[catalog_url('1.0.0')][field] = value
            observed[reason] = self.lookup(docs).reason
        self.assertEqual(set(observed), {row['reason'] for row in table})
        self.assertTrue(all(reason == actual for reason, actual in observed.items()))

    def test_reordered_alias_leaves_objects_and_dates_keep_schedule_and_result(self):
        docs = fixture(('1.0.0', '01.0+build', '2.0.0'))
        first = self.lookup(docs)
        schedule = self.transport.urls
        docs[INDEX]['items'][0]['items'].reverse()
        for url, value in list(docs.items()):
            docs[url] = dict(reversed(list(value.items())))
        self.assertEqual(self.lookup(docs), first)
        self.assertEqual(self.transport.urls, schedule)

    def test_no_secret_response_exception_or_hash_crosses_result_boundary(self):
        canary = 'SECRET-private-origin-credential'
        for value in (TimeoutError(canary), {'count': canary, 'items': []}):
            docs = fixture()
            docs[INDEX] = value
            result = self.lookup(docs)
            serialized = json.dumps(result_message(result))
            self.assertNotIn(canary, serialized)
            self.assertNotIn(HASH, serialized)
        docs = fixture()
        docs[catalog_url('1.0.0')]['description'] = canary
        serialized = json.dumps(result_message(self.lookup(docs)))
        self.assertNotIn(canary, serialized)
        self.assertNotIn(HASH, serialized)

    def test_root_page_identity_and_unlisted_classification_conflicts(self):
        docs = fixture()
        docs[INDEX]['@id'] = 'https://private.invalid/SECRET'
        self.assertEqual(self.lookup(docs).reason, 'invalid_registry_response')
        docs = fixture()
        docs[INDEX]['items'][0]['items'][0]['catalogEntry']['listed'] = False
        self.assertEqual(self.lookup(docs).reason, 'invalid_registry_response')

    def test_catalog_deleted_latest_never_uses_older_dated_release(self):
        docs = fixture()
        docs[catalog_url('2.0.0')]['@type'] = 'PackageDelete'
        result = self.lookup(docs)
        self.assertEqual(result.reason, 'invalid_registry_response')
        self.assertIsNone(result.latest_publication)


class AdapterTests(unittest.TestCase):
    def test_sorted_authority_only_supervision_and_cleanup(self):
        supervisor = Mock()
        supervisor.lookup.return_value = PackageResult(reason='registry_error')
        authorities = [replace(AUTHORITY, package_key='z'), AUTHORITY]
        results = registry.NuGetRegistryAdapter(supervisor).lookup_all(authorities)
        self.assertEqual([a.package_key for a, r in results], ['example', 'z'])
        self.assertEqual([call.args[0].package_key for call in supervisor.lookup.call_args_list], ['example', 'z'])
        supervisor.close.assert_called_once_with()
        with self.assertRaises(ValueError):
            registry.NuGetRegistryAdapter(Mock()).lookup_all(['example'])

    def test_caller_interruption_closes_supervisor(self):
        supervisor = Mock()
        supervisor.lookup.side_effect = KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):
            registry.NuGetRegistryAdapter(supervisor).lookup_all([AUTHORITY])
        supervisor.close.assert_called_once_with()


class ComposedSupervisionTests(unittest.TestCase):
    def test_actual_handler_client_protocol_supervisor_success_and_late_discard(self):
        # The fake OS seam runs the real worker handler and byte client. Clock
        # arithmetic and cancellation belong to the real parent controller.
        from tests.test_nuget_worker import Clock, Process
        for stall in (None, registry.SERVICE_INDEX, INDEX, catalog_url('1.0.0')):
            with self.subTest(stall=stall):
                clock = Clock()
                transport = Transport(fixture())
                client = registry.NuGetMetadataClient(transport=transport, clock=clock)
                process_holder = []
                def spawn(command, **options):
                    path = Path(options['cwd'])
                    process = Process(clock, path, ignore_terminate=True)
                    process_holder.append(process)
                    write_message(path / 'ready.json', {'ready': 1})
                    return process
                supervisor = NuGetSupervisor(clock=clock, pause=clock.pause, process_factory=spawn)
                original_get = transport.get
                def get(url):
                    if url == stall:
                        # Completion at the cutoff, even a safe worker failure,
                        # cannot enter the accepted result stream.
                        clock.now = 159.5
                    return original_get(url)
                transport.get = get
                def complete():
                    command_path = supervisor.path / 'command.json'
                    if not command_path.exists():
                        return
                    command = read_message(command_path)
                    command_path.unlink()
                    client.begin_package('example', package_deadline=command['package_deadline'],
                                         scan_deadline=command['scan_deadline'])
                    try:
                        result = registry.lookup_authorized_package(AUTHORITY, client)
                    except registry.NuGetRegistryFailure as failure:
                        result = PackageResult(reason=failure.reason)
                    write_message(supervisor.path / 'result.json', {
                        'sequence': command['sequence'], 'result': result_message(result)})
                clock.callback = complete
                try:
                    result = registry.NuGetRegistryAdapter(supervisor).lookup_all([AUTHORITY])[0][1]
                    self.assertEqual(result.reason, 'registry_error' if stall else None)
                    self.assertEqual(supervisor.cancelled, stall is not None)
                    self.assertFalse(process_holder[0].alive)
                    self.assertFalse(supervisor.path.exists())
                    if stall:
                        self.assertIsNone(result.latest_publication)
                        before = len(transport.urls)
                        self.assertEqual(supervisor.lookup(AUTHORITY).reason, 'registry_error')
                        self.assertEqual(len(transport.urls), before)
                        self.assertEqual(len(process_holder), 1)
                finally:
                    supervisor.close()

    def test_lazy_installed_worker_handler_uses_real_adapter_handler(self):
        from libyears.nuget_worker import _lookup
        transport = Transport(fixture())
        client = registry.NuGetMetadataClient(transport=transport, clock=lambda: 100)
        client.begin_package('example')
        self.assertIsNone(_lookup(AUTHORITY, client).reason)

    def test_failed_discovery_cached_for_entire_scan(self):
        for failure in ({}, TransportFailure(503, 'SECRET', retry_after='0'),
                        TransportFailure(404, 'SECRET')):
            docs = fixture()
            docs[registry.SERVICE_INDEX] = failure
            transport = Transport(docs)
            client = registry.NuGetMetadataClient(transport=transport, clock=lambda: 100)
            reasons = []
            for unused in range(2):
                client.begin_package('example')
                try:
                    registry.lookup_authorized_package(AUTHORITY, client)
                except registry.NuGetRegistryFailure as error:
                    reasons.append(error.reason)
            self.assertEqual(reasons[0], reasons[1])
            self.assertEqual(transport.urls, [registry.SERVICE_INDEX])

    def test_bounded_404_is_invalid_response_not_absence(self):
        docs = fixture()
        docs[INDEX] = TransportFailure(404, 'synthetic diagnostic', bounded_failure='body_limit')
        transport = Transport(docs)
        client = registry.NuGetMetadataClient(transport=transport, clock=lambda: 100)
        client.begin_package('example')
        with self.assertRaises(registry.NuGetRegistryFailure) as raised:
            registry.lookup_authorized_package(AUTHORITY, client)
        self.assertEqual(raised.exception.reason, 'invalid_registry_response')


if __name__ == '__main__':
    unittest.main()
