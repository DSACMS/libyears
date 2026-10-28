import json
from pathlib import Path
import ssl
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

from libyears.model import RegistryFailure
from libyears.registry import TransportFailure, _RejectRedirects
from libyears.rubygems_registry import MAX_RESPONSE_BYTES, RubyGemsAdapter
from tests.test_registry import BoundedResponse


FIXTURES = Path(__file__).parent / 'fixtures' / 'rubygems'


def artifact(**changes):
    row = dict(number='1.0', platform='ruby', ruby_abi=None, prerelease=False,
               created_at='2020-01-01T00:00:00Z')
    row.update(changes)
    return row


class RegistryTestCase(unittest.TestCase):
    def setUp(self):
        self.prohibit_live = patch('urllib.request.urlopen', side_effect=AssertionError('live HTTP'))
        self.prohibit_live.start()
        self.addCleanup(self.prohibit_live.stop)
        self.opener = Mock()
        opener_patch = patch('libyears.registry.request.build_opener', return_value=self.opener)
        opener_patch.start()
        self.addCleanup(opener_patch.stop)
        self.adapter = RubyGemsAdapter()

    def fetch(self, population=None, identity=None):
        identity = b'{"name":"Sample"}' if identity is None else identity
        population = [artifact()] if population is None else population
        body = population if isinstance(population, bytes) else json.dumps(population).encode()
        self.opener.open.side_effect = [BoundedResponse(identity), BoundedResponse(body)]
        return self.adapter.fetch_population('sample', '1.0')


class RegistryPopulationTests(RegistryTestCase):
    def test_fixed_endpoint_order_case_identity_and_nameless_population(self):
        self.opener.open.side_effect = [
            BoundedResponse((FIXTURES / filename).read_bytes())
            for filename in ('identity.json', 'population.json')
        ]
        records = self.adapter.fetch_population('sample', '1.0')
        self.assertEqual([row.version for row in records], ['1.0', '2.0'])
        self.assertEqual([call.args[0].full_url for call in self.opener.open.call_args_list], [
            'https://rubygems.org/api/v1/gems/sample.json',
            'https://rubygems.org/api/v1/versions/Sample.json',
        ])
        self.assertTrue(all(call.kwargs == {'timeout': 10.0}
                            for call in self.opener.open.call_args_list))
        self.assertEqual(self.adapter.transport.allowed_authority, 'rubygems.org')
        self.assertEqual(self.adapter.transport.max_response_bytes, 16 * 1024 * 1024)
        self.assertEqual(self.adapter.ssl_context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(self.adapter.ssl_context.check_hostname)
        self.assertEqual(self.opener.open.call_args.args[0].get_header('User-agent'), 'libyears/0.1')

    def test_explicit_ca_and_timeout_use_shared_policy(self):
        context = ssl.create_default_context()
        with patch('libyears.registry.select_tls_context', return_value=(context, 'explicit')) as select:
            adapter = RubyGemsAdapter(timeout=2.5, user_agent='test-agent', ca_bundle='chosen.pem')
        select.assert_called_once_with('chosen.pem')
        self.assertIs(adapter.ssl_context, context)
        self.assertEqual((adapter.timeout, adapter.user_agent, adapter.tls_trust),
                         (2.5, 'test-agent', 'explicit'))
        for timeout in (0, -1, float('inf'), float('nan')):
            with self.assertRaises(ValueError):
                RubyGemsAdapter(timeout=timeout)

    def test_input_identity_injection_makes_no_requests(self):
        for name in ('https://rubygems.org', 'a/b', 'a?x', 'a#x', 'a@b', 'a%2fb',
                     'a:b', 'sämple', '123', 'sample\n'):
            self.assertEqual(self.adapter.fetch_population(name, '1').reason,
                             'invalid_registry_response')
        for version in ('1/2', '1?x', '1..0', None):
            self.assertIsInstance(self.adapter.fetch_population('sample', version), RegistryFailure)
        self.opener.open.assert_not_called()

    def test_returned_identity_rejects_punctuation_unicode_and_missing_name(self):
        for name in ('sam_ple', 'sam-ple', 'sample.other', 'ſample', None, 1):
            with self.subTest(name=name):
                self.opener.open.reset_mock()
                result = self.fetch(identity=json.dumps({'name': name}).encode())
                self.assertEqual(result.reason, 'invalid_registry_response')
                self.assertEqual(self.opener.open.call_count, 1)
        for name in ('sam_ple', 'ſample', None):
            self.assertEqual(self.fetch([artifact(name=name)]).reason, 'invalid_registry_response')
        self.assertEqual(len(self.fetch([artifact(name='SAMPLE')])), 1)

    def test_required_fields_types_abi_and_availability(self):
        for field in ('number', 'platform', 'ruby_abi', 'prerelease'):
            row = artifact()
            del row[field]
            self.assertEqual(self.fetch([row]).reason, 'invalid_registry_response')
        for changes in (dict(number=1), dict(number='1..0'), dict(platform=None),
                        dict(platform='ruby/extra'), dict(prerelease=0), dict(prerelease=None),
                        dict(ruby_abi=3.2), dict(ruby_abi='unknown'), dict(yanked=True),
                        dict(yanked=None), dict(yanked=0)):
            with self.subTest(changes=changes):
                self.assertEqual(self.fetch([artifact(**changes)]).reason, 'invalid_registry_response')
        records = self.fetch([artifact(), artifact(ruby_abi='3.2')])
        self.assertEqual(len(records), 1)
        self.assertTrue(records[0].available)
        self.assertIsNone(records[0].yanked)
        self.assertEqual(self.fetch([artifact(ruby_abi='3.2')]), ())

    def test_strict_json_structure_and_duplicates(self):
        for payload in (b'{}', b'null', b'[null]', b'[] trailing', b'\xff',
                        b'[{"number":"1", "number":"2"}]', b'[NaN]'):
            self.assertEqual(self.fetch(payload).reason, 'invalid_registry_response')
        self.assertEqual(len(self.fetch([artifact(), artifact()])), 1)
        for changes in (dict(created_at='2021-01-01T00:00:00Z'), dict(prerelease=True),
                        dict(extra='different')):
            self.assertEqual(self.fetch([artifact(), artifact(**changes)]).reason,
                             'invalid_registry_response')
        self.assertEqual(self.fetch([]), ())
        self.assertEqual(len(self.fetch(b'[{"number":"1.0","number":"1.0",'
                                       b'"platform":"ruby","ruby_abi":null,"prerelease":false}]')), 1)

    def test_typed_failures_absence_and_no_partial_evidence(self):
        failures = [
            (TransportFailure(404, 'HTTP 404'), 'package_not_found'),
            (TransportFailure(None, 'TLS certificate verification failure'), 'registry_error'),
            (TransportFailure(None, 'network timeout'), 'registry_error'),
            (TransportFailure(429, 'HTTP 429'), 'registry_error'),
            (TransportFailure(None, 'large', 'response_too_large'), 'invalid_registry_response'),
            (TransportFailure(None, 'short', 'incomplete_response'), 'invalid_registry_response'),
        ]
        for response, reason in failures:
            for at_population in (False, True):
                self.adapter.transport = Mock()
                self.adapter.transport.get.side_effect = ([b'{"name":"sample"}', response]
                                                          if at_population else [response])
                result = self.adapter.fetch_population('sample', '1.0')
                self.assertEqual(result.reason, reason)
                self.assertIsNone(result.rubygems_evidence)
                self.assertEqual(self.adapter.transport.get.call_count, 2 if at_population else 1)

    def test_mocked_restricted_http_failures(self):
        for error, reason in (
            (HTTPError('https://rubygems.org', 302, 'redirect', {}, None), 'registry_error'),
            (HTTPError('https://rubygems.org', 404, 'absent', {}, None), 'package_not_found'),
            (URLError(ssl.SSLCertVerificationError('secret')), 'registry_error'),
            (TimeoutError('secret'), 'registry_error'),
        ):
            self.opener.open.side_effect = error
            result = self.adapter.fetch_population('sample', '1.0')
            self.assertEqual(result.reason, reason)
            self.assertNotIn('secret', repr(result))

    def test_exact_limit_excess_and_truncation_through_restricted_transport(self):
        identity = b'{"name":"sample"}'
        population = json.dumps([artifact()]).encode()
        for response, expected in (
            (BoundedResponse(population + b' ' * (MAX_RESPONSE_BYTES - len(population))), None),
            (BoundedResponse(b' ' * (MAX_RESPONSE_BYTES + 1)), 'invalid_registry_response'),
            (BoundedResponse(population, {'Content-Length': str(MAX_RESPONSE_BYTES + 1)}),
             'invalid_registry_response'),
            (BoundedResponse(population, {'Content-Length': str(len(population) + 1)}),
             'invalid_registry_response'),
        ):
            self.opener.open.reset_mock()
            self.opener.open.side_effect = [BoundedResponse(identity), response]
            result = self.adapter.fetch_population('sample', '1.0')
            if expected is None:
                self.assertEqual(len(result), 1)
            else:
                self.assertEqual(result.reason, expected)
                self.assertIsNone(result.rubygems_evidence)
            self.assertEqual(self.opener.open.call_count, 2)
            self.assertLessEqual(len(response.read_sizes), 1)

    def test_redirect_handler_rejects_every_supported_redirect_status(self):
        from urllib.request import Request

        handler = _RejectRedirects()
        request = Request('https://rubygems.org/api/v1/gems/sample.json')
        for status in (301, 302, 303, 307, 308):
            for target in ('https://rubygems.org/other', 'https://private.invalid/secret'):
                with self.assertRaises(HTTPError):
                    getattr(handler, 'http_error_' + str(status))(
                        request, None, status, 'redirect', {'Location': target},
                    )

    def test_both_responses_can_reach_the_total_budget_without_extra_requests(self):
        identity = b'{"name":"sample"}'
        population = b'[]'
        self.opener.open.side_effect = [
            BoundedResponse(body + b' ' * (MAX_RESPONSE_BYTES - len(body)))
            for body in (identity, population)
        ]
        self.assertEqual(self.adapter.fetch_population('sample', '1.0'), ())
        self.assertEqual(self.opener.open.call_count, 2)

    def test_duplicate_values_do_not_conflate_booleans_and_numbers(self):
        for population in (
            b'[{"extra":{"flag":true},"extra":{"flag":1}}]',
            [artifact(extra=True), artifact(extra=1)],
        ):
            self.assertEqual(self.fetch(population).reason, 'invalid_registry_response')


class PublicationTests(RegistryTestCase):
    def lookup(self, population, version='1.0'):
        self.opener.open.side_effect = [
            BoundedResponse(b'{"name":"sample"}'),
            BoundedResponse(json.dumps(population).encode()),
        ]
        return self.adapter.lookup('sample', version)

    def test_earliest_across_platforms_retains_every_admissible_contributor(self):
        rows = [artifact(platform='java', created_at='2021-01-01T00:00:00Z'),
                artifact(created_at='2020-01-01T02:00:00.123456+02:00'),
                artifact(platform='x86_64-linux', created_at='invalid'),
                artifact(number='2.0', created_at='2022-01-01T00:00:00Z')]
        original = self.lookup(rows)
        self.assertEqual(original.used_release_time.isoformat(), '2020-01-01T00:00:00.123456+00:00')
        self.assertEqual(original.latest_stable_version, '2.0')
        self.assertEqual([a.platform for a in original.rubygems_evidence.used_publication_artifacts],
                         ['java', 'ruby'])
        self.assertEqual(original, self.lookup(list(reversed(rows))))

    def test_invalid_missing_naive_and_import_day_are_individually_excluded(self):
        for value in (None, '', 'invalid', 123, '2024-01-01T00:00:00',
                      '2009-07-25T00:00:00Z', '2009-07-25T23:59:59.999999Z',
                      '2009-07-24T22:00:00-02:00', '2009-07-26T01:59:59+02:00'):
            with self.subTest(value=value):
                row = artifact(created_at=value, built_at='2024-01-01T00:00:00Z')
                self.assertEqual(self.lookup([row]).reason, 'release_date_missing')
                result = self.lookup([row, artifact(platform='java')])
                self.assertEqual(len(result.rubygems_evidence.used_publication_artifacts), 1)
        row = artifact()
        del row['created_at']
        self.assertEqual(self.lookup([row]).reason, 'release_date_missing')
        for value in ('2009-07-25T00:00:00+00:01', '2009-07-25T23:59:59-00:01'):
            self.assertNotIsInstance(self.lookup([artifact(created_at=value)]), RegistryFailure)

    def test_authoritative_equivalent_times_and_contradictions(self):
        for value in ('2020-01-01T00:00:00Z', '2020-01-01T01:00:00+01:00'):
            self.assertNotIsInstance(self.lookup([artifact(version_created_at=value)]), RegistryFailure)
        row = artifact(version_created_at='2021-01-01T00:00:00Z')
        self.assertEqual(self.lookup([row]).reason, 'invalid_registry_response')
        row = artifact(version_created_at='2020-01-01T00:00:00Z')
        del row['created_at']
        self.assertNotIsInstance(self.lookup([row]), RegistryFailure)
        for value in ('invalid', None, '2020-01-01T00:00:00'):
            self.assertEqual(self.lookup([artifact(version_created_at=value)]).reason,
                             'invalid_registry_response')

    def test_registry_validation_precedes_used_absence_date_and_stable_absence(self):
        cases = [
            ([artifact(number='2.0', prerelease=None)], 'invalid_registry_response'),
            ([artifact(number='2.0')], 'version_not_found'),
            ([artifact(created_at=None, prerelease=True)], 'release_date_missing'),
            ([artifact(prerelease=True)], 'no_stable_release'),
        ]
        for rows, reason in cases:
            self.assertEqual(self.lookup(rows).reason, reason)
        rows = [artifact(number='9.0', prerelease=True),
                artifact(number='9.0', platform='java', prerelease=False)]
        for population in (rows, list(reversed(rows))):
            self.assertEqual(self.lookup(population).reason, 'invalid_registry_response')
        self.assertEqual(self.lookup([]).reason, 'version_not_found')
        self.assertEqual(self.lookup([artifact(ruby_abi='3.2')]).reason, 'version_not_found')

    def test_latest_uses_dates_then_exact_lexical_ties_and_ignores_labels(self):
        rows = [artifact(), artifact(number='10', created_at='2022-01-01T00:00:00Z'),
                artifact(number='2', created_at='2022-01-01T00:00:00Z'),
                artifact(number='99', created_at='2021-01-01T00:00:00Z'),
                artifact(number='3', created_at='2023-01-01T00:00:00Z', prerelease=True),
                artifact(number='4', created_at='invalid'),
                artifact(number='5', created_at='2024-01-01T00:00:00Z', ruby_abi='3.2')]
        for population in (rows, list(reversed(rows))):
            self.assertEqual(self.lookup(population).latest_stable_version, '10')
        rows[-1] = artifact(number='5', created_at='2024-01-01T00:00:00Z')
        self.assertEqual(self.lookup(rows).latest_stable_version, '5')

    def test_prerelease_used_and_failure_keeps_safely_established_contributors(self):
        rows = [artifact(number='1.0.pre', prerelease=True), artifact(number='2.0')]
        result = self.lookup(rows, '1.0.pre')
        self.assertEqual(result.latest_stable_version, '2.0')
        failure = self.lookup(rows[:1], '1.0.pre')
        self.assertEqual(failure.reason, 'no_stable_release')
        self.assertEqual(len(failure.rubygems_evidence.used_publication_artifacts), 1)
        self.assertIsNone(failure.rubygems_evidence.latest_publication_artifacts)

    def test_normalized_yanked_evidence_contributes_but_cannot_be_latest(self):
        from datetime import datetime, timezone
        from libyears.rubygems_registry import RubyArtifactRecord, _resolve_population

        def record(version, platform, year, available, yanked):
            return RubyArtifactRecord(version, platform, datetime(year, 1, 1, tzinfo=timezone.utc),
                                      False, available, yanked)

        rows = (record('1.0', 'ruby', 2020, True, None),
                record('1.0', 'java', 2019, False, True),
                record('2.0', 'ruby', 2022, False, True))
        result = _resolve_population('sample', '2.0', rows)
        self.assertEqual(result.latest_stable_version, '1.0')
        self.assertEqual(result.latest_stable_release_time.year, 2019)
        self.assertTrue(result.rubygems_evidence.used_publication_artifacts[0].yanked)
        self.assertEqual(len(result.rubygems_evidence.latest_publication_artifacts), 2)
        self.assertEqual(_resolve_population('sample', '2.0', rows[-1:]).reason, 'no_stable_release')

    def test_same_version_zero_and_existing_metric_arithmetic(self):
        from libyears.metric import measure_dependency
        from libyears.model import Dependency

        def measure(result):
            return measure_dependency(Dependency(
                'rubygems', result.name, result.used_version, result.used_release_time,
                result.latest_stable_version, result.latest_stable_release_time,
                'gemfile_lock', result.rubygems_evidence,
            ))

        same = self.lookup([artifact(), artifact(platform='java', created_at='2021-01-01T00:00:00Z')])
        self.assertIs(same.rubygems_evidence.used_publication_artifacts,
                      same.rubygems_evidence.latest_publication_artifacts)
        self.assertEqual(measure(same).libyears, 0.0)
        self.assertFalse(measure(same).timestamp_anomaly)
        negative = self.lookup([artifact(prerelease=True, created_at='2024-01-01T00:00:00Z'),
                                artifact(number='2.0')])
        self.assertEqual(measure(negative).libyears, 0.0)
        self.assertTrue(measure(negative).timestamp_anomaly)
        positive = self.lookup([artifact(), artifact(number='2.0', created_at='2021-01-01T00:00:00Z')])
        self.assertAlmostEqual(measure(positive).libyears, 366 / 365.25)
        self.assertFalse(measure(positive).timestamp_anomaly)

    def test_canonical_helper_excludes_naive_and_import_dates_and_sorts_evidence(self):
        from datetime import datetime, timezone
        from libyears.rubygems_registry import RubyArtifactRecord, canonical_publication

        records = tuple(RubyArtifactRecord('1.0', platform, timestamp, False, True)
                        for platform, timestamp in (
                            ('ruby', datetime(2020, 1, 1, tzinfo=timezone.utc)),
                            ('java', datetime(2019, 1, 1, tzinfo=timezone.utc)),
                            ('linux', datetime(2009, 7, 25, tzinfo=timezone.utc)),
                            ('other', datetime(2018, 1, 1)),
                        ))
        publication = canonical_publication(records)
        self.assertEqual(publication.publication_time.year, 2019)
        self.assertEqual([a.platform for a in publication.artifacts], ['java', 'ruby'])
        self.assertEqual(publication, canonical_publication(tuple(reversed(records))))
        self.assertIsNone(canonical_publication(records[2:]))
