"""Fixed public HTTPS GET client used only inside the isolated Maven worker."""

from datetime import datetime, timezone
import http.client
import ipaddress
import os
import re
import socket
import ssl
import time

from .maven_model import MavenReason
from .maven_protocol import MAX_ATTEMPTS, MAX_BYTES
from .maven_registry import (
    MAX_CATALOGUE_BYTES, MAX_POM_BYTES, MavenRepresentation, RegistryFailure,
    catalogue_path, pom_path, select_target, pom_date,
)

HOST = 'repo.maven.apache.org'
HEADER_BYTES = 64 * 1024
HEADER_FIELDS = 100
_TOKEN = re.compile(rb"[!#$%&'*+.^_`|~0-9A-Za-z-]+")


class _FramingReader:
    """Cap status/headers before HTTPMessage accumulates them; bound chunk framing."""

    def __init__(self, stream):
        self.stream = stream
        self.remaining = HEADER_BYTES
        self.fields = 0
        self.first = True
        self.headers = True
        self.trailers = False
        self.chunked = False
        self.chunk_remaining = 0
        self.terminator_pending = False
        self.on_body = None

    def readline(self, limit=-1):
        size = self.remaining + 1 if limit < 0 else min(limit, self.remaining + 1)
        line = self.stream.readline(size)
        self.remaining -= len(line)
        if self.remaining < 0:
            raise RegistryFailure(MavenReason.METADATA_BUDGET_EXCEEDED)
        if not line.endswith(b'\r\n'):
            raise RegistryFailure()
        if self.first:
            self.first = False
            if not re.fullmatch(rb'HTTP/1\.[01] 200(?: [\x20-\x7e]*)?\r\n', line):
                raise RegistryFailure()
        elif self.headers:
            if line == b'\r\n':
                self.headers = False
            else:
                self.fields += 1
                if self.fields > HEADER_FIELDS:
                    raise RegistryFailure(MavenReason.METADATA_BUDGET_EXCEEDED)
                name, separator, value = line[:-2].partition(b':')
                if not separator or not _TOKEN.fullmatch(name) or any(
                        byte < 32 and byte != 9 or byte == 127 for byte in value):
                    raise RegistryFailure()
                if name.lower() == b'transfer-encoding':
                    self.chunked = value.strip().lower() == b'chunked'
        elif self.trailers:
            if line != b'\r\n':
                raise RegistryFailure()  # no unvalidated representation trailers
        elif self.chunked:
            # Support plain hexadecimal sizes only. Chunk extensions are outside
            # this bounded transport grammar; never let int() accept signs,
            # prefixes, underscores or whitespace as alternative framing.
            size = line[:-2]
            if not re.fullmatch(rb'[0-9A-Fa-f]+', size):
                raise RegistryFailure()
            self.chunk_remaining = int(size, 16)
            self.trailers = self.chunk_remaining == 0
        return line

    def read(self, size=-1):
        # Raw socket reads expose every delivered piece before another read can
        # time out. A BufferedReader can consume bytes and then raise without
        # returning them, which would lose scan accounting on failed responses.
        if size < 0:
            raise RegistryFailure()
        delimiter = self.chunked and self.terminator_pending
        if delimiter and size != 2:
            raise RegistryFailure()
        pieces = []
        remaining = size
        while remaining:
            data = self.stream.read(remaining)
            if not data:
                break
            remaining -= len(data)
            if not self.headers and self.on_body is not None and not delimiter:
                count = min(len(data), self.chunk_remaining) if self.chunked else len(data)
                if self.chunked:
                    self.chunk_remaining -= count
                    self.terminator_pending = self.chunk_remaining == 0
                self.on_body(count)
            pieces.append(data)
        data = b''.join(pieces)
        if delimiter:
            if data != b'\r\n':
                raise RegistryFailure()
            self.terminator_pending = False
        return data

    def readinto(self, buffer):
        data = self.read(len(buffer))
        buffer[:len(data)] = data
        return len(data)

    def __getattr__(self, name):
        return getattr(self.stream, name)


class _UnbufferedSocket:
    def __init__(self, socket):
        self.socket = socket

    def makefile(self, mode):
        return self.socket.makefile(mode, buffering=0)


class _Response(http.client.HTTPResponse):
    def __init__(self, socket, *args, **kwargs):
        super().__init__(_UnbufferedSocket(socket), *args, **kwargs)
        self.fp = _FramingReader(self.fp)


class _PublicConnection(http.client.HTTPSConnection):
    response_class = _Response

    def connect(self):
        # No proxy/tunnel, redirects, ambient auth or alternate DNS destination.
        addresses = socket.getaddrinfo(HOST, 443, type=socket.SOCK_STREAM)
        if not addresses:
            raise RegistryFailure()
        for item in addresses:
            address = ipaddress.ip_address(item[4][0])
            if (not address.is_global or address.is_multicast or address.is_reserved
                    or address.is_unspecified or address.is_loopback or address.is_link_local):
                raise RegistryFailure()
        family, kind, protocol, _, address = addresses[0]
        stream = socket.socket(family, kind, protocol)
        try:
            stream.settimeout(self.timeout)
            stream.connect(address)
            self.sock = self._context.wrap_socket(stream, server_hostname=HOST)
        except BaseException:
            stream.close()
            raise


def _tls_context(ca_file):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    if ca_file is not None:
        context.load_verify_locations(cafile=ca_file)
    else:
        # Select compiled system trust paths, never environment CA overrides.
        defaults = ssl.get_default_verify_paths()
        cafile = defaults.openssl_cafile if os.path.isfile(defaults.openssl_cafile) else None
        capath = defaults.openssl_capath if os.path.isdir(defaults.openssl_capath) else None
        if cafile is None and capath is None:
            raise RegistryFailure()
        context.load_verify_locations(cafile=cafile, capath=capath)
    return context


class MavenHTTPClient:
    """One worker/scan: cumulative clocks and counters never reset by module."""

    def __init__(self, ca_file=None, *, clock=time.monotonic,
                 wall_clock=lambda: datetime.now(timezone.utc), connection_factory=_PublicConnection,
                 context_factory=_tls_context):
        self.clock = clock
        self.wall_clock = wall_clock
        self.connection_factory = connection_factory
        self.ca_file = ca_file
        self.context_factory = context_factory
        self.context = None
        self.started = clock()
        self.ga_started = {}
        self.attempts = 0
        self.body_bytes = 0

    def lookup(self, operation, group, artifact, version, deadline):
        path = catalogue_path(group, artifact) if operation == 'select_target' else pom_path(group, artifact, version)
        limit = MAX_CATALOGUE_BYTES if operation == 'select_target' else MAX_POM_BYTES
        now = self.clock()
        ga = (group, artifact)
        self.ga_started.setdefault(ga, now)
        cutoff = min(deadline, now + 10, self.started + 300, self.ga_started[ga] + 60)
        if now >= cutoff or self.attempts >= MAX_ATTEMPTS or self.body_bytes >= MAX_BYTES:
            raise RegistryFailure(MavenReason.METADATA_BUDGET_EXCEEDED)
        self.attempts += 1
        connection = None
        try:
            if self.context is None:
                context = self.context_factory(self.ca_file)
                if context.verify_mode != ssl.CERT_REQUIRED or not context.check_hostname:
                    raise RegistryFailure()
                self.context = context
            connection = self.connection_factory(HOST, port=443, timeout=cutoff - now, context=self.context)
            connection.request('GET', path, headers={'Accept-Encoding': 'identity', 'User-Agent': 'libyears'})
            representation = connection.getresponse()
            if representation.status != 200:
                raise RegistryFailure()
            headers = tuple(representation.getheaders())
            encodings = [v for k, v in headers if k.lower() == 'content-encoding']
            lengths = [v for k, v in headers if k.lower() == 'content-length']
            transfers = [v for k, v in headers if k.lower() == 'transfer-encoding']
            if (len(encodings) > 1 or (encodings and encodings[0].lower() != 'identity')
                    or len(lengths) > 1 or len(transfers) > 1
                    or (transfers and (transfers[0].lower() != 'chunked' or lengths))
                    or any(k.lower() == 'trailer' for k, v in headers)):
                raise RegistryFailure()
            advertised = None
            if lengths:
                if not re.fullmatch(r'[0-9]{1,10}', lengths[0]):
                    raise RegistryFailure()
                advertised = int(lengths[0])
                if advertised > limit or advertised > MAX_BYTES - self.body_bytes:
                    raise RegistryFailure(MavenReason.METADATA_BUDGET_EXCEEDED)
            chunks = []
            total = 0
            def consume(count):
                nonlocal total
                self.body_bytes += count
                total += count
                if total > limit or self.body_bytes > MAX_BYTES:
                    raise RegistryFailure(MavenReason.METADATA_BUDGET_EXCEEDED)
            reader = getattr(representation, 'fp', None)
            counted = isinstance(reader, _FramingReader)
            if counted:
                reader.on_body = consume
            while True:
                if self.clock() >= cutoff:
                    raise RegistryFailure(MavenReason.METADATA_BUDGET_EXCEEDED)
                remaining = MAX_BYTES - self.body_bytes
                if remaining <= 0:
                    raise RegistryFailure(MavenReason.METADATA_BUDGET_EXCEEDED)
                try:
                    chunk = representation.read(min(64 * 1024, limit - total + 1, remaining))
                except http.client.IncompleteRead as failure:
                    if not counted:
                        consume(len(failure.partial))
                    raise RegistryFailure() from None
                if not counted:
                    consume(len(chunk))
                if not chunk:
                    break
                chunks.append(chunk)
                if advertised is not None and total == advertised:
                    break  # HTTP Content-Length frames the whole representation
            if advertised is not None and total != advertised:
                raise RegistryFailure()
            response = MavenRepresentation(200, b''.join(chunks), headers, self.wall_clock())
            if operation == 'select_target':
                return select_target(group, artifact, response)
            return pom_date(group, artifact, version, response)
        except RegistryFailure:
            raise
        except (OSError, ValueError, http.client.HTTPException):
            raise RegistryFailure() from None
        finally:
            if connection is not None:
                connection.close()
