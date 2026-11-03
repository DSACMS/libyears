"""Offline NuGet transport bounds; no public activation or live requests."""

import gzip
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError

from libyears import nuget_registry as nuget
from libyears.registry import DecodedResponse, TransportFailure, VerifiedJSONTransport


INDEX = nuget.REGISTRATION_BASE + 'example/index.json'
CATALOG = 'https://api.nuget.org/v3/catalog0/data/2026.01.01/example.1.0.0.json'


class Response:
    def __init__(self, body, encoding='identity', headers=None):
        self.body = body
        self.headers = {'Content-Encoding': encoding, **(headers or {})}
        self.sizes = []

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        pass

    def read(self, size):
        self.sizes.append(size)
        return self.body[:size]


class BytesTransport:
    def __init__(self, body=b'{}'):
        self.body = body
        self.urls = []

    def get(self, url):
        self.urls.append(url)
        return self.body


class NuGetTransportTests(unittest.TestCase):
    def fetch(self, response, wire=1000, expanded=10):
        opener = Mock()
        opener.open.return_value = response
        with patch('libyears.registry.request.build_opener', return_value=opener):
            transport = VerifiedJSONTransport(max_response_bytes=wire,
                                             max_decompressed_bytes=expanded,
                                             allowed_authority='api.nuget.org',
                                             retry_after_statuses=(429, 503))
        return transport.get(INDEX), opener

    def test_identity_and_incremental_gzip_exact_cap_and_wire_accounting(self):
        for encoding, body in [('identity', b'0123456789'),
                               ('gzip', gzip.compress(b'0123456789'))]:
            result, opener = self.fetch(Response(body, encoding))
            self.assertEqual(result, b'0123456789')
            self.assertEqual(result.wire_bytes, len(body))
            self.assertEqual(opener.open.call_args.args[0].get_header('Accept-encoding'), 'gzip, identity')
        # More than one compressed input chunk must pass through the decoder.
        import random
        data = random.Random(1).randbytes(200_000)
        result, unused = self.fetch(Response(gzip.compress(data), 'gzip'), 210_000, 200_000)
        self.assertEqual(result, data)

    def test_bad_encoding_expansion_truncation_crc_and_concatenation(self):
        encoded = gzip.compress(b'0123456789')
        for body, encoding, maximum in [
            (b'0' * 11, 'identity', 10), (gzip.compress(b'0' * 100000), 'gzip', 10),
            (encoded[:-1], 'gzip', 10), (encoded[:-8] + b'badcrc!!', 'gzip', 10),
            (encoded + encoded, 'gzip', 20), (encoded + b'junk', 'gzip', 10),
            (encoded, 'br', 10), (b'bad', 'gzip', 10), (b'', 'gzip', 10),
        ]:
            with self.subTest(encoding=encoding, length=len(body), maximum=maximum):
                result, unused = self.fetch(Response(body, encoding), expanded=maximum)
                self.assertIsInstance(result, TransportFailure)
                self.assertIsNotNone(result.bounded_failure)

    def test_wire_cap_and_declared_truncation(self):
        for response in [Response(b'123456'), Response(b'1', headers={'Content-Length': '3'}),
                         Response(b'1', headers={'Content-Length': '9' * 5000})]:
            result, unused = self.fetch(response, wire=5)
            self.assertIsInstance(result, TransportFailure)
            self.assertIsNotNone(result.bounded_failure)

    def test_503_retry_after_is_an_opt_in_with_safe_header_filtering(self):
        for status in (429, 503):
            for header, expected in [('10', '10'), ('private\nsecret', None), ('x' * 129, None)]:
                with patch('libyears.registry.request.build_opener') as build:
                    transport = VerifiedJSONTransport(allowed_authority='api.nuget.org',
                                                     retry_after_statuses=(429, 503))
                build.return_value.open.side_effect = HTTPError(INDEX, status, 'secret', {'Retry-After': header}, None)
                result = transport.get(INDEX)
                self.assertEqual(result.retry_after, expected)
                self.assertNotIn('secret', result.diagnostic)
        with patch('libyears.registry.request.urlopen', side_effect=HTTPError(INDEX, 503, '', {'Retry-After': '10'}, None)):
            self.assertIsNone(VerifiedJSONTransport().get(INDEX).retry_after)

    def test_rejected_urls_never_reach_transport(self):
        transport = BytesTransport()
        client = nuget.NuGetMetadataClient(transport)
        client.begin_package('example')
        for url in [
            INDEX.replace('https:', 'http:'), INDEX.replace('api.nuget.org', 'localhost'),
            INDEX.replace('api.nuget.org', 'api.nuget.org:443'), INDEX.replace('api.nuget.org', 'user:secret@api.nuget.org'),
            INDEX + '?', INDEX + '#', INDEX + '?key=secret', INDEX + '#fragment',
            INDEX.replace('example', 'other'), INDEX.replace('index.json', '../index.json'),
            INDEX.replace('index.json', '%2findex.json'), INDEX.replace('index.json', '%252findex.json'),
            INDEX.replace('index.json', 'a\\index.json'), INDEX.replace('index.json', 'package.nupkg'),
            INDEX.replace('index.json', 'a//index.json'), INDEX.replace('index.json', '\nindex.json'),
            'https://api.nuget.org/v3-flatcontainer/example/1.0/example.nupkg',
        ]:
            with self.subTest(url=url), self.assertRaises(nuget.NuGetRegistryFailure) as failure:
                client.get_json(url)
            self.assertEqual(failure.exception.reason, 'invalid_registry_response')
        self.assertEqual(transport.urls, [])

    def test_fixed_purposes_and_sorted_validated_page_schedule(self):
        self.assertEqual(nuget.validate_url(nuget.SERVICE_INDEX, 'example', 'index'), nuget.SERVICE_INDEX)
        self.assertEqual(nuget.validate_url(CATALOG, 'example', 'catalog'), CATALOG)
        pages = [INDEX.replace('index.json', name) for name in ['b.json', 'a.json']]
        self.assertEqual(nuget.sorted_urls(pages, 'example'), sorted(pages))
        for links in [pages + [pages[0]], pages + ['https://private.example/data']]:
            with self.assertRaises(nuget.NuGetRegistryFailure):
                nuget.sorted_urls(links, 'example')
        with self.assertRaises(nuget.NuGetRegistryFailure):
            nuget.validate_url(CATALOG.replace('catalog0', 'catalog1'), 'example', 'catalog')

    def client(self, body=b'{}', clock=None):
        transport = BytesTransport(body)
        client = nuget.NuGetMetadataClient(transport, clock=clock or (lambda: 0), wall_clock=lambda: 0)
        client.begin_package('example')
        return client, transport

    def test_get_url_only_double_and_error_classes_and_no_retry(self):
        for body, reason in [(b'{}', None), (b'not JSON', 'invalid_registry_response'),
                             (TransportFailure(None, 'safe'), 'registry_error'),
                             (TransportFailure(None, 'safe', 'response_too_large'), 'invalid_registry_response'),
                             (TransportFailure(404, 'safe'), 'registry_error')]:
            client, transport = self.client(body)
            if reason:
                with self.assertRaises(nuget.NuGetRegistryFailure) as failure:
                    client.get_json(INDEX)
                self.assertEqual(failure.exception.reason, reason)
                self.assertEqual(failure.exception.status, getattr(body, 'status', None))
            else:
                self.assertEqual(client.get_json(INDEX), {})
            self.assertEqual(transport.urls, [INDEX])

    def test_json_depth_values_strings_and_invalid_framing(self):
        for body in [b'NaN', b'1e9999', b'"\xff"', b'{"x":1,"x":2}', b'[' * 33 + b']' * 33]:
            with self.subTest(body=body), self.assertRaises(nuget.NuGetRegistryFailure):
                nuget.decode_metadata(body)
        self.assertIsInstance(nuget.decode_metadata(b'[' * 32 + b']' * 32), list)
        for limit_name, good, bad in [('MAX_JSON_VALUES', b'[0,0]', b'[0,0,0]'),
                                      ('MAX_JSON_STRING', b'"abc"', b'"abcd"')]:
            with patch.object(nuget, limit_name, 3):
                nuget.decode_metadata(good)
                with self.assertRaises(nuget.NuGetRegistryFailure):
                    nuget.decode_metadata(bad)
        # Production values and string caps are tested at their actual boundary.
        nuget.decode_metadata(b'"' + b'a' * nuget.MAX_JSON_STRING + b'"')
        with self.assertRaises(nuget.NuGetRegistryFailure):
            nuget.decode_metadata(b'"' + b'a' * (nuget.MAX_JSON_STRING + 1) + b'"')
        nuget.decode_metadata(b'[' + b'0,' * (nuget.MAX_JSON_VALUES - 2) + b'0]')
        with self.assertRaises(nuget.NuGetRegistryFailure):
            nuget.decode_metadata(b'[' + b'0,' * (nuget.MAX_JSON_VALUES - 1) + b'0]')

    def test_page_version_request_and_aggregate_caps(self):
        for method, maximum in [('count_page', nuget.MAX_PAGES), ('count_versions', nuget.MAX_VERSIONS)]:
            client, unused = self.client()
            getattr(client, method)(maximum)
            with self.assertRaises(nuget.NuGetRegistryFailure) as failure:
                getattr(client, method)(1)
            self.assertEqual(failure.exception.reason, 'invalid_registry_response')
        for counter, maximum in [('package_requests', nuget.MAX_PACKAGE_REQUESTS), ('scan_requests', nuget.MAX_SCAN_REQUESTS)]:
            client, transport = self.client()
            setattr(client, counter, maximum - 1)
            client.get_json(INDEX)
            with self.assertRaises(nuget.NuGetRegistryFailure) as failure:
                client.get_json(INDEX)
            self.assertEqual(failure.exception.reason, 'registry_error')
            self.assertEqual(len(transport.urls), 1)
        for counter, maximum in [('wire_bytes', nuget.MAX_PACKAGE_WIRE_BYTES), ('expanded_bytes', nuget.MAX_PACKAGE_EXPANDED_BYTES)]:
            client, transport = self.client()
            setattr(client, counter, maximum - 2)
            client.get_json(INDEX)
            with self.assertRaises(nuget.NuGetRegistryFailure) as failure:
                client.get_json(INDEX)
            self.assertEqual(failure.exception.reason, 'invalid_registry_response')
        for body in [DecodedResponse(b'{}', nuget.MAX_WIRE_BYTES + 1), b' ' * (nuget.MAX_EXPANDED_BYTES + 1)]:
            client, unused = self.client(body)
            with self.assertRaises(nuget.NuGetRegistryFailure):
                client.get_json(INDEX)

    def test_rate_limit_cooldown_persists_across_packages_and_never_sleeps(self):
        for status in (429, 503):
            for header in ('10', 'Thu, 01 Jan 1970 00:00:10 GMT', None, 'bad', '-1', '1.5'):
                now = [0]
                client, transport = self.client(TransportFailure(status, 'safe', retry_after=header), lambda: now[0])
                with patch('time.sleep', side_effect=AssertionError('retry sleep')):
                    with self.assertRaises(nuget.NuGetRegistryFailure):
                        client.get_json(INDEX)
                    transport.body = b'{}'
                    client.begin_package('example')
                    with self.assertRaises(nuget.NuGetRegistryFailure):
                        client.get_json(INDEX)
                    self.assertEqual(len(transport.urls), 1)
                    now[0] = 10
                    client.begin_package('example')
                    if header in ('10', 'Thu, 01 Jan 1970 00:00:10 GMT'):
                        self.assertEqual(client.get_json(INDEX), {})
                    else:
                        with self.assertRaises(nuget.NuGetRegistryFailure):
                            client.get_json(INDEX)

    def test_deadline_admission_and_scan_not_reset(self):
        now = [0]
        client, transport = self.client(clock=lambda: now[0])
        now[0] = 60
        with self.assertRaises(nuget.NuGetRegistryFailure):
            client.get_json(INDEX)
        self.assertEqual(transport.urls, [])
        client.begin_package('example')
        self.assertEqual(client.get_json(INDEX), {})
        now[0] = 299
        client.begin_package('example')
        self.assertEqual(client.scan_deadline, 300)
        now[0] = 300
        with self.assertRaises(nuget.NuGetRegistryFailure):
            client.get_json(INDEX)
        self.assertEqual(len(transport.urls), 1)

    def test_injected_absolute_cutoff_caps_socket_timeout_and_discards_late_bytes(self):
        now = [0]
        with patch('libyears.registry.request.build_opener') as build:
            transport = VerifiedJSONTransport(max_response_bytes=100,
                                             max_decompressed_bytes=100,
                                             allowed_authority='api.nuget.org')
        build.return_value.open.return_value = Response(b'{}')
        client = nuget.NuGetMetadataClient(transport, clock=lambda: now[0])
        client.begin_package('example', package_deadline=2, scan_deadline=5)
        self.assertEqual(client.get_json(INDEX), {})
        self.assertEqual(build.return_value.open.call_args.kwargs['timeout'], 2)
        def late(url):
            now[0] = 2
            return b'{}'
        transport.get = late
        with self.assertRaises(nuget.NuGetRegistryFailure) as failure:
            client.get_json(INDEX)
        self.assertEqual(failure.exception.reason, 'registry_error')
