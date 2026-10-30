"""Pure recognition of the closed Gemfile declaration subset; never evaluate Ruby."""

from dataclasses import dataclass
import re


PUBLIC_SOURCE = 'https://rubygems.org'
MAX_GEMFILE_LINE_BYTES = 16 * 1024
_NAME = re.compile(r'[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?\Z')
_VERSION = r'[0-9]+(?:\.[A-Za-z0-9]+)*'
_REQUIREMENT_TERM = re.compile(r'(?:!=|>=|<=|~>|=|>|<)?\s*' + _VERSION + r'\Z')
_SYMBOL = re.compile(r':[A-Za-z_][A-Za-z0-9_]*')
_WORD = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')


def supported_name(name: str) -> bool:
    return bool(_NAME.fullmatch(name) and re.search(r'[A-Za-z]', name))


def supported_requirement(requirement: str | None) -> bool:
    """Check existing Ruby requirement framing, without interpreting constraints."""
    if requirement is None:
        return True
    for term in requirement.split(','):
        if not _REQUIREMENT_TERM.fullmatch(term.strip()):
            return False
    return True


@dataclass(frozen=True, slots=True)
class GemDeclaration:
    name: str
    requirements: tuple[str, ...]
    declared_groups: tuple[str, ...]
    line: int


@dataclass(frozen=True, slots=True)
class ParsedGemfile:
    declarations: tuple[GemDeclaration, ...]
    established_groups: tuple[str, ...]
    public_source_authorized: bool


@dataclass(frozen=True, slots=True)
class GemfileParseFailure:
    reason: str
    line: int | None
    safe_category: str


class _LineFailure(Exception):
    def __init__(self, category: str, *, unsupported: bool = False):
        self.category = category
        self.reason = 'unsupported_gemfile_syntax' if unsupported else 'invalid_gemfile'


class _Cursor:
    """Consume one physical line, preserving literal contents and comment boundaries."""

    def __init__(self, text: str):
        self.text = text
        self.position = 0

    def whitespace(self):
        start = self.position
        while self.position < len(self.text) and self.text[self.position] in ' \t':
            self.position += 1
        return self.position > start

    def at_end(self):
        self.whitespace()
        return self.position == len(self.text) or self.text[self.position] == '#'

    def consume(self, token: str):
        self.whitespace()
        if self.text.startswith(token, self.position):
            self.position += len(token)
            return True
        return False

    def expect(self, token: str):
        if not self.consume(token):
            raise _LineFailure('incomplete declaration framing')

    def word(self):
        self.whitespace()
        match = _WORD.match(self.text, self.position)
        if match is None:
            raise _LineFailure('malformed declaration framing')
        self.position = match.end()
        return match.group()

    def keyword(self, allowed: tuple[str, ...]):
        self.whitespace()
        if self.at_end():
            raise _LineFailure('missing keyword option')
        if _WORD.match(self.text, self.position) is None:
            raise _LineFailure('nonliteral keyword option', unsupported=True)
        key = self.word()
        if key not in allowed:
            raise _LineFailure('unsupported keyword option', unsupported=True)
        if self.position == len(self.text) or self.text[self.position] != ':':
            raise _LineFailure('malformed keyword option')
        self.position += 1
        return key

    def literal(self):
        self.whitespace()
        if self.at_end():
            raise _LineFailure('missing literal')
        quote = self.text[self.position]
        if quote not in "\"'":
            raise _LineFailure('nonliteral declaration value', unsupported=True)
        self.position += 1
        start = self.position
        while self.position < len(self.text):
            character = self.text[self.position]
            if character == quote:
                value = self.text[start:self.position]
                self.position += 1
                return value
            if character == '\\' or (
                character == '#' and self.position + 1 < len(self.text)
                and self.text[self.position + 1] in '{@$'
            ):
                raise _LineFailure('unsupported literal form', unsupported=True)
            self.position += 1
        raise _LineFailure('unterminated literal')

    def symbol(self):
        self.whitespace()
        match = _SYMBOL.match(self.text, self.position)
        if match is None:
            if not self.at_end() and self.text[self.position] not in ':],':
                raise _LineFailure('nonliteral group value', unsupported=True)
            raise _LineFailure('malformed group symbol')
        self.position = match.end()
        return match.group()[1:]

    def groups(self):
        if not self.consume('['):
            return (self.symbol(),)
        groups = [self.symbol()]
        while self.consume(','):
            groups.append(self.symbol())
        self.expect(']')
        return tuple(groups)

    def boolean(self):
        self.whitespace()
        if self.at_end():
            raise _LineFailure('missing boolean option')
        if _WORD.match(self.text, self.position) is None:
            raise _LineFailure('nonliteral boolean option', unsupported=True)
        value = self.word()
        if value not in ('true', 'false'):
            raise _LineFailure('nonliteral boolean option', unsupported=True)

    def finish(self):
        if not self.at_end():
            raise _LineFailure('unsupported trailing syntax', unsupported=True)


def _gem(cursor: _Cursor, block_groups: tuple[str, ...] | None, line: int):
    name = cursor.literal()
    if not supported_name(name):
        raise _LineFailure('unsupported gem name framing', unsupported=True)
    requirements = []
    options = set()
    explicit_groups = ()
    while cursor.consume(','):
        cursor.whitespace()
        if cursor.position < len(cursor.text) and cursor.text[cursor.position] in "\"'":
            if options:
                raise _LineFailure('requirements after options')
            requirement = cursor.literal()
            if not supported_requirement(requirement):
                raise _LineFailure('unsupported requirement framing', unsupported=True)
            requirements.append(requirement)
            continue
        key = cursor.keyword(('group', 'groups', 'require'))
        if key in options or (key in ('group', 'groups') and options & {'group', 'groups'}):
            raise _LineFailure('repeated membership or option')
        options.add(key)
        if key in ('group', 'groups'):
            explicit_groups = cursor.groups()
        else:
            cursor.whitespace()
            if cursor.position < len(cursor.text) and cursor.text[cursor.position] in "\"'":
                cursor.literal()
            else:
                cursor.boolean()
    cursor.finish()
    if not supported_requirement(', '.join(requirements) if requirements else None):
        raise _LineFailure('unsupported joined requirement framing', unsupported=True)
    if block_groups is None:
        groups = explicit_groups or ('default',)
    else:
        groups = block_groups + explicit_groups
    return GemDeclaration(name, tuple(requirements), tuple(sorted(set(groups))), line)


def _group(cursor: _Cursor):
    groups = [cursor.symbol()]
    while cursor.consume(','):
        cursor.whitespace()
        if cursor.position < len(cursor.text) and cursor.text[cursor.position] == ':':
            groups.append(cursor.symbol())
            continue
        cursor.keyword(('optional',))
        cursor.boolean()
        break
    if cursor.word() != 'do':
        raise _LineFailure('missing group block opener')
    cursor.finish()
    return tuple(groups)


def parse_gemfile(text: str) -> ParsedGemfile | GemfileParseFailure:
    """Return complete immutable evidence or one safe failure, never partial scope."""
    declarations = []
    names = set()
    established_groups = {'default'}
    block_groups = None
    source_seen = False
    public_source_authorized = False
    # Split only on LF: other Unicode line separators are not physical newlines.
    lines = text.split('\n')
    for number, physical_line in enumerate(lines, 1):
        line = physical_line
        if number < len(lines) and line.endswith('\r'):
            line = line[:-1]
        try:
            if len(line.encode('utf-8')) > MAX_GEMFILE_LINE_BYTES:
                raise _LineFailure('physical line limit exceeded', unsupported=True)
            if any((ord(character) < 32 and character != '\t')
                   or 127 <= ord(character) <= 159 or character in '\u2028\u2029'
                   for character in line):
                raise _LineFailure('invalid physical line framing')
            cursor = _Cursor(line)
            if cursor.at_end():
                continue
            if _WORD.match(line, cursor.position) is None:
                raise _LineFailure('unsupported statement', unsupported=True)
            statement = cursor.word()
            if statement == 'end':
                cursor.finish()
                if block_groups is None:
                    raise _LineFailure('unmatched group end')
                block_groups = None
                continue
            if statement not in ('source', 'gem', 'group'):
                raise _LineFailure('unsupported statement', unsupported=True)
            if statement == 'group' and block_groups is not None:
                raise _LineFailure('nested group block', unsupported=True)
            if statement == 'source' and block_groups is not None:
                raise _LineFailure('source inside group block', unsupported=True)
            if not cursor.whitespace():
                if cursor.at_end():
                    raise _LineFailure('incomplete declaration framing')
                raise _LineFailure('unsupported call framing', unsupported=True)
            if statement == 'source':
                source = cursor.literal()
                cursor.finish()
                if source_seen:
                    raise _LineFailure('repeated source declaration')
                source_seen = True
                public_source_authorized = source in (PUBLIC_SOURCE, PUBLIC_SOURCE + '/')
                del source
            elif statement == 'group':
                block_groups = _group(cursor)
                established_groups.update(block_groups)
            else:
                declaration = _gem(cursor, block_groups, number)
                if declaration.name in names:
                    return GemfileParseFailure(
                        'duplicate_gemfile_declaration', number, 'duplicate gem declaration')
                names.add(declaration.name)
                declarations.append(declaration)
                established_groups.update(declaration.declared_groups)
        except _LineFailure as failure:
            return GemfileParseFailure(failure.reason, number, failure.category)
        except UnicodeError:
            return GemfileParseFailure('invalid_gemfile', number, 'invalid text encoding')
    if not source_seen:
        return GemfileParseFailure('invalid_gemfile', None, 'missing source declaration')
    if block_groups is not None:
        return GemfileParseFailure('invalid_gemfile', None, 'unclosed group block')
    return ParsedGemfile(
        tuple(declarations), tuple(sorted(established_groups)), public_source_authorized)
