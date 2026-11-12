"""Injected fixed-public transport: every response is local bytes, no network."""

import io
import http.client
import ssl
import unittest
from unittest.mock import Mock, patch

from libyears.maven_http import MavenHTTPClient, _Response, _PublicConnection, _tls_context
from libyears.maven_model import MavenReason
from libyears.maven_registry import RegistryFailure
from test_maven_registry import catalogue, POM, RETRIEVED, DATE


class TrackedStream(io.BytesIO):
    consumed = 0

    def readline(self, size=-1):
        value = super().readline(size)
        self.consumed += len(value)
        return value


class FakeSocket:
    def __init__(self, data):
        self.stream = TrackedStream(data)

    def makefile(self, *args, **kwargs):
        return self.stream


class FakeConnection:
    def __init__(self, raw):
        self.socket = FakeSocket(raw)
        self.requests = []
        self.closed = False

    def request(self, *args, **kwargs):
        self.requests.append((args, kwargs))

    def getresponse(self):
        response = _Response(self.socket)
        response.begin()
        return response

    def close(self):
        self.closed = True


def raw_response(body, headers=b'', *, status=b'200 OK', length=True):
    size = b'Content-Length: ' + str(len(body)).encode() + b'\r\n' if length else b''
    return b'HTTP/1.1 ' + status + b'\r\n' + size + headers + b'\r\n' + body


def context(unused):
    return Mock(verify_mode=ssl.CERT_REQUIRED, check_hostname=True)


class MavenHTTPTests(unittest.TestCase):
    def client(self, raw, **kwargs):
        self.connections = []
        self.factory_calls = []
        def factory(*args, **options):
            self.factory_calls.append((args, options))
            connection = FakeConnection(raw)
            self.connections.append(connection)
            return connection
        return MavenHTTPClient(connection_factory=factory, context_factory=context,
                               wall_clock=lambda: RETRIEVED, **kwargs)

    def lookup(self, client, operation='select_target', version=None):
        return client.lookup(operation, 'g', 'a', version, client.clock() + 10)

    def test_one_fixed_get_identity_encoding_no_ambient_auth_proxy_or_url(self):
        with patch.dict('os.environ', {'HTTPS_PROXY': 'https://private.invalid', 'SSL_CERT_FILE': '/never/read'}):
            client = self.client(raw_response(catalogue()))
            result = self.lookup(client)
        self.assertEqual(result.version, '2')
        self.assertEqual(client.attempts, 1)
        self.assertEqual(client.body_bytes, len(catalogue()))
        self.assertEqual(self.factory_calls[0][0], ('repo.maven.apache.org',))
        self.assertEqual(self.factory_calls[0][1]['port'], 443)
        args, headers = self.connections[0].requests[0]
        self.assertEqual(args, ('GET', '/maven2/g/a/maven-metadata.xml'))
        self.assertEqual(headers['headers']['Accept-Encoding'], 'identity')
        self.assertEqual(set(headers['headers']), {'Accept-Encoding', 'User-Agent'})
        self.assertTrue(self.connections[0].closed)

    def test_exact_pom_get_plus_is_encoded_and_pom_date_only(self):
        client = self.client(raw_response(POM, b'Last-Modified: ' + DATE.encode() + b'\r\n'))
        result = self.lookup(client, 'pom_date', '1')
        self.assertIsNotNone(result.last_modified)
        self.assertEqual(self.connections[0].requests[0][0][1], '/maven2/g/a/1/a-1.pom')

    def test_all_redirects_and_error_statuses_refuse_without_another_get(self):
        for status in (b'301 Moved', b'302 Found', b'307 Temporary', b'308 Permanent', b'404 Not Found', b'100 Continue'):
            client = self.client(raw_response(catalogue(), b'Location: https://private.invalid\r\n', status=status))
            with self.assertRaises(RegistryFailure):
                self.lookup(client)
            self.assertEqual(client.attempts, 1)
            self.assertEqual(len(self.connections), 1)

    def test_encoding_and_length_ambiguity_short_body_refuse(self):
        for headers in (b'Content-Encoding: gzip\r\n', b'Content-Encoding: br\r\n',
                        b'Content-Length: 1\r\n', b'Transfer-Encoding: chunked\r\n'):
            client = self.client(raw_response(catalogue(), headers))
            with self.assertRaises(RegistryFailure):
                self.lookup(client)
        client = self.client(raw_response(catalogue()).replace(str(len(catalogue())).encode(), b'99999', 1))
        with self.assertRaises(RegistryFailure):
            self.lookup(client)
        self.assertEqual(client.body_bytes, len(catalogue()))

    def test_header_caps_apply_before_accumulation_and_obsfold_is_not_accepted(self):
        for headers in (b'X: ' + b'x' * 65536 + b'\r\n', b'X: x\r\n' * 101,
                        b' folded: value\r\n', b'X: value\x00\r\n'):
            client = self.client(raw_response(catalogue(), headers))
            with self.assertRaises(RegistryFailure):
                self.lookup(client)
            self.assertLessEqual(self.connections[0].socket.stream.consumed, 65537)

    def test_eof_and_chunked_whole_bodies_with_no_content_length_are_bounded(self):
        body = catalogue()
        client = self.client(raw_response(body, length=False))
        self.assertEqual(self.lookup(client).version, '2')
        chunks = hex(len(body))[2:].encode() + b'\r\n' + body + b'\r\n0\r\n\r\n'
        client = self.client(raw_response(chunks, b'Transfer-Encoding: chunked\r\n', length=False))
        self.assertEqual(self.lookup(client).version, '2')
        self.assertEqual(client.body_bytes, len(body))
        bad = chunks[:-2] + b'Last-Modified: ' + DATE.encode() + b'\r\n\r\n'
        client = self.client(raw_response(bad, b'Transfer-Encoding: chunked\r\n', length=False))
        with self.assertRaises(RegistryFailure):
            self.lookup(client)

    def test_scan_attempt_byte_and_wall_budgets_never_reset_for_new_ga(self):
        client = self.client(raw_response(b'not XML'))
        for _ in range(300):
            self.lookup(client)
        with self.assertRaises(RegistryFailure) as failure:
            self.lookup(client)
        self.assertEqual(failure.exception.reason, MavenReason.METADATA_BUDGET_EXCEEDED)
        self.assertEqual(len(self.connections), 300)
        client = self.client(raw_response(catalogue(), length=False))
        with patch('libyears.maven_http.MAX_BYTES', 10):
            with self.assertRaises(RegistryFailure):
                self.lookup(client)
        self.assertEqual(client.body_bytes, 10)
        now = [0.0]
        client = self.client(raw_response(catalogue()), clock=lambda: now[0])
        self.lookup(client)
        now[0] = 60.0
        with self.assertRaises(RegistryFailure):
            self.lookup(client)
        self.assertEqual(client.attempts, 1)
        now[0] = 300.0
        with self.assertRaises(RegistryFailure):
            client.lookup('select_target', 'new', 'a', None, 310)
        self.assertEqual(client.attempts, 1)

    def test_invalid_coordinates_or_snapshot_never_create_connection(self):
        client = self.client(raw_response(catalogue()))
        for group, artifact, version in (('g/escape', 'a', '1'), ('g', 'a', '../1'), ('g', 'a', '1-SNAPSHOT')):
            with self.assertRaises(RegistryFailure):
                client.lookup('pom_date', group, artifact, version, client.clock() + 10)
        self.assertEqual(self.connections, [])
        self.assertEqual(client.attempts, 0)

    def test_partial_chunk_failure_and_invalid_trailers_still_spend_consumed_body_bytes(self):
        body = catalogue()
        chunk = hex(len(body))[2:].encode() + b'\r\n' + body + b'\r\n0\r\nX: forbidden\r\n\r\n'
        client = self.client(raw_response(chunk, b'Transfer-Encoding: chunked\r\n', length=False))
        with self.assertRaises(RegistryFailure):
            self.lookup(client)
        self.assertEqual(client.body_bytes, len(body))
        partial = b'10\r\nshort'
        client = self.client(raw_response(partial, b'Transfer-Encoding: chunked\r\n', length=False))
        with self.assertRaises(RegistryFailure):
            self.lookup(client)
        self.assertEqual(client.body_bytes, 5)

    def test_chunk_delimiters_are_validated_and_payload_bytes_still_count_on_failure(self):
        body = catalogue()
        for delimiter in (b'XX', b'\n\n', b'\rX', b''):
            encoded = hex(len(body))[2:].encode() + b'\r\n' + body + delimiter + b'0\r\n\r\n'
            client = self.client(raw_response(encoded, b'Transfer-Encoding: chunked\r\n', length=False))
            with self.subTest(delimiter=delimiter), self.assertRaises(RegistryFailure):
                self.lookup(client)
            self.assertEqual(client.body_bytes, len(body))

    def test_chunk_size_lexical_grammar_and_unsupported_extensions_refuse(self):
        body = catalogue()
        size = hex(len(body))[2:].encode()
        for invalid in (b'+' + size, b'-' + size, b'0x' + size, size[:1] + b'_' + size[1:],
                        b' ' + size, size + b' ', size + b';name=value',
                        size + b';name=\x00', size + b';=value'):
            encoded = invalid + b'\r\n' + body + b'\r\n0\r\n\r\n'
            client = self.client(raw_response(encoded, b'Transfer-Encoding: chunked\r\n', length=False))
            with self.subTest(size=invalid), self.assertRaises(RegistryFailure):
                self.lookup(client)
            self.assertEqual(client.body_bytes, 0)
        encoded = b'00' + size.upper() + b'\r\n' + body + b'\r\n000\r\n\r\n'
        client = self.client(raw_response(encoded, b'Transfer-Encoding: chunked\r\n', length=False))
        self.assertEqual(self.lookup(client).version, '2')
        self.assertEqual(client.body_bytes, len(body))

    def test_unbuffered_partial_timeout_counts_each_piece_before_failure(self):
        class PartialRaw(io.RawIOBase):
            def __init__(self):
                self.data = b'HTTP/1.1 200 OK\r\nContent-Length: 100\r\n\r\nabcde'
                self.position = 0

            def readable(self):
                return True

            def readinto(self, destination):
                if self.position == len(self.data):
                    raise TimeoutError('trusted fixture timeout')
                count = min(len(destination), len(self.data) - self.position)
                destination[:count] = self.data[self.position:self.position + count]
                self.position += count
                return count

        class Socket:
            def makefile(self, mode, buffering=-1):
                raw = PartialRaw()
                return raw if buffering == 0 else io.BufferedReader(raw)

        connection = Mock()
        def getresponse():
            parsed = _Response(Socket())
            parsed.begin()
            return parsed
        connection.getresponse.side_effect = getresponse
        client = MavenHTTPClient(connection_factory=lambda *args, **kwargs: connection,
                                 context_factory=context)
        with self.assertRaises(RegistryFailure):
            self.lookup(client)
        self.assertEqual(client.body_bytes, 5)
        self.assertEqual(client.attempts, 1)
        connection.close.assert_called_once()

    def test_tls_uses_only_explicit_or_compiled_trust_and_never_insecure_fallback(self):
        defaults = Mock(openssl_cafile='compiled.pem', openssl_capath='compiled-certs')
        trusted = Mock()
        with patch('libyears.maven_http.ssl.SSLContext', return_value=trusted), \
             patch('libyears.maven_http.ssl.get_default_verify_paths', return_value=defaults), \
             patch('libyears.maven_http.os.path.isfile', return_value=True), \
             patch('libyears.maven_http.os.path.isdir', return_value=True), \
             patch.dict('os.environ', {'SSL_CERT_FILE': '/never/read', 'SSL_CERT_DIR': '/never/read'}):
            _tls_context(None)
            trusted.load_verify_locations.assert_called_once_with(cafile='compiled.pem', capath='compiled-certs')
            trusted.reset_mock()
            _tls_context('explicit.pem')
            trusted.load_verify_locations.assert_called_once_with(cafile='explicit.pem')
        create = Mock()
        client = MavenHTTPClient(connection_factory=create, context_factory=lambda unused: Mock(
            verify_mode=ssl.CERT_NONE, check_hostname=False))
        with self.assertRaises(RegistryFailure):
            self.lookup(client)
        create.assert_not_called()
        with self.assertRaises(RegistryFailure):
            self.lookup(client)  # a failed check cannot cache an insecure context
        create.assert_not_called()

    def test_private_dns_answers_refuse_before_socket_connect(self):
        connection = _PublicConnection('repo.maven.apache.org', context=ssl.create_default_context())
        for address in ('127.0.0.1', '10.0.0.1', '169.254.0.1', '100.64.0.1',
                        '224.0.0.1', '::1', 'fc00::1', 'fe80::1', 'ff02::1'):
            with self.subTest(address=address), patch('libyears.maven_http.socket.getaddrinfo',
                    return_value=[(2, 1, 6, '', (address, 443))]), patch('libyears.maven_http.socket.socket') as create:
                with self.assertRaises(RegistryFailure):
                    connection.connect()
            create.assert_not_called()



if __name__ == '__main__':
    unittest.main()
