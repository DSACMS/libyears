"""Whole-document JSON framing guard, followed by strict standard decoding."""

import json
import math
import re

from .sbom_model import SbomFailure

MAX_BYTES = 8 * 1024 * 1024
MAX_DEPTH = 32
MAX_TOKENS = 250_000
MAX_STRING_BYTES = 16 * 1024
MAX_NUMBER = 128
MAX_MEMBERS = 256
MAX_ITEMS = 20_000
_NUMBER = re.compile(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?')


def _budget():
    raise SbomFailure('sbom_budget_exceeded')


def _invalid():
    raise SbomFailure('sbom_invalid_json')


def _preflight(text):
    # Stack entries are [container kind, member/item count, expecting array item].
    # Grammar is still checked by json.loads over exactly the same full text.
    stack = []
    tokens = 0
    index = 0
    while index < len(text):
        character = text[index]
        if character in ' \t\r\n':
            index += 1
            continue
        if character in '}]':
            if not stack:
                _invalid()
            stack.pop()
            index += 1
            continue
        if character == ':':
            if stack and stack[-1][0] == '{':
                stack[-1][1] += 1
                if stack[-1][1] > MAX_MEMBERS:
                    _budget()
            index += 1
            continue
        if character == ',':
            if stack:
                stack[-1][2] = True
            index += 1
            continue
        tokens += 1
        if tokens > MAX_TOKENS:
            _budget()
        if stack and stack[-1][0] == '[' and stack[-1][2]:
            stack[-1][1] += 1
            stack[-1][2] = False
            if stack[-1][1] > MAX_ITEMS:
                _budget()
        if character in '{[':
            stack.append([character, 0, True])
            if len(stack) > MAX_DEPTH:
                _budget()
            index += 1
        elif character == '"':
            try:
                value, index = json.decoder.scanstring(text, index + 1, True)
                length = len(value.encode('utf-8'))
            except (ValueError, UnicodeError):
                _invalid()
            if length > MAX_STRING_BYTES:
                _budget()
        elif character in '-0123456789':
            match = _NUMBER.match(text, index)
            if match is None:
                _invalid()
            if match.end() - index > MAX_NUMBER:
                _budget()
            index = match.end()
        else:
            for literal in ('true', 'false', 'null'):
                if text.startswith(literal, index):
                    index += len(literal)
                    break
            else:
                _invalid()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _invalid()
        result[key] = value
    return result


def _float(value):
    number = float(value)
    if not math.isfinite(number):
        _invalid()
    return number


def decode_document(data):
    if type(data) is not bytes:
        _invalid()
    if len(data) > MAX_BYTES:
        _budget()
    try:
        text = data.decode('utf-8')
    except UnicodeError:
        _invalid()
    if text.startswith('\ufeff'):
        _invalid()
    _preflight(text)
    try:
        value = json.loads(text, object_pairs_hook=_pairs, parse_float=_float,
                           parse_constant=lambda unused: _invalid())
    except (ValueError, RecursionError) as error:
        if isinstance(error, SbomFailure):
            raise
        _invalid()
    if not isinstance(value, dict):
        _invalid()
    return value
