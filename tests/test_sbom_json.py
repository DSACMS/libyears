import json
import unittest
from unittest.mock import patch

from libyears.sbom_json import decode_document
from libyears.sbom_model import SbomFailure


class JsonTests(unittest.TestCase):
    def refuse(self, data, reason='sbom_invalid_json'):
        with self.assertRaises(SbomFailure) as caught:
            decode_document(data)
        self.assertEqual(caught.exception.reason, reason)
        self.assertNotIn('payload', str(caught.exception))

    def test_whole_strict_json(self):
        for data in (b'\xef\xbb\xbf{}', b'{}{}', b'{"x":1,"x":2}', b'{"ignored":{"x":0,"x":1}}',
                     b'{"x":NaN}', b'{"x":Infinity}', b'{"x":1e999}', b'{"x":"\\ud800"}',
                     b'{"x":"\xff"}', b'{"ignored":[1,]}', b'[]', b'{"x":01}', b'{"x":true false}'):
            with self.subTest(data=data):
                self.refuse(data)
        self.assertEqual(decode_document(b'{"a":[true,false,null,1.25,-2e1,"\\ud83d\\ude00"]}')["a"][-1], '😀')

    def test_depth_at_and_over(self):
        decode_document(b'{"x":' + b'[' * 31 + b'0' + b']' * 31 + b'}')
        self.refuse(b'{"x":' + b'[' * 32 + b'0' + b']' * 32 + b'}', 'sbom_budget_exceeded')

    def test_string_and_key_utf8_limits(self):
        for key in (False, True):
            for size in (16_384, 16_385):
                text = 'a' * size
                data = json.dumps({text: 0} if key else {'x': text}).encode()
                if size == 16_384:
                    decode_document(data)
                else:
                    self.refuse(data, 'sbom_budget_exceeded')
        self.refuse(json.dumps({'x': 'é' * 8193}).encode(), 'sbom_budget_exceeded')

    def test_number_at_and_over(self):
        decode_document(b'{"n":' + b'1' * 128 + b'}')
        self.refuse(b'{"n":' + b'1' * 129 + b'}', 'sbom_budget_exceeded')

    def test_members_items_and_tokens(self):
        decode_document(json.dumps({str(i): 0 for i in range(256)}).encode())
        self.refuse(json.dumps({str(i): 0 for i in range(257)}).encode(), 'sbom_budget_exceeded')
        decode_document(json.dumps({'x': [0] * 20_000}).encode())
        self.refuse(json.dumps({'x': [0] * 20_001}).encode(), 'sbom_budget_exceeded')
        # root + member name + array + three scalar items = six tokens.
        with patch('libyears.sbom_json.MAX_TOKENS', 6):
            decode_document(b'{"x":[0,0,0]}')
            self.refuse(b'{"x":[0,0,0,0]}', 'sbom_budget_exceeded')
        values = {'x': [[0] * 19_000 for i in range(13)]}
        decode_document(json.dumps(values).encode())
        values['x'].append([0] * 4000)
        self.refuse(json.dumps(values).encode(), 'sbom_budget_exceeded')

    def test_byte_limit(self):
        decode_document(b'{}' + b' ' * (8 * 1024 * 1024 - 2))
        self.refuse(b'{}' + b' ' * (8 * 1024 * 1024 - 1), 'sbom_budget_exceeded')
