import hashlib
import json
import unittest
from unittest.mock import patch

from libyears.sbom_document import accept_document, document_assertions
from libyears.sbom_model import SbomFailure, SbomSnapshot


def synthetic_document(**changes):
    value = {'bomFormat': 'CycloneDX', 'specVersion': '1.5',
             'metadata': {'component': {'name': 'synthetic', 'bom-ref': 'root'}},
             'components': []}
    value.update(changes)
    return value


def snapshot(value):
    data = json.dumps(value).encode()
    return SbomSnapshot('bom.json', data, hashlib.sha256(data).hexdigest())


class DocumentTests(unittest.TestCase):
    def accept(self, value):
        with patch('socket.socket', side_effect=AssertionError('socket')), patch('subprocess.Popen', side_effect=AssertionError('process')):
            return accept_document(snapshot(value))

    def refuse(self, value, reason):
        with self.assertRaises(SbomFailure) as caught:
            self.accept(value)
        self.assertEqual(caught.exception.reason, reason)

    def test_subject_and_format_framing(self):
        self.assertEqual(self.accept(synthetic_document()).records, ())
        for changes in ({'version': True}, {'version': 0}, {'specVersion': '1.6'}, {'unknown': []}, {'components': [1]}, {'services': None}):
            self.refuse(synthetic_document(**changes), 'sbom_unsupported_format')
        for metadata in ({}, {'component': {}}, {'component': {'name': '', 'bom-ref': 'root'}}):
            self.refuse(synthetic_document(metadata=metadata), 'sbom_subject_unavailable')
        doc = self.accept(synthetic_document(metadata={'component': {'name': 'unsafe\x1bname', 'bom-ref': 'r'}}))
        self.assertEqual(doc.subject['name'], 'unsafe\x1bname')

    def test_alias_and_references(self):
        value = synthetic_document()
        subject = value['metadata']['component']
        value['components'] = [subject.copy(), {'bom-ref': 'a'}, {}]
        doc = self.accept(value)
        self.assertEqual(doc.subject_aliases, 1)
        self.assertEqual([index for index, record in doc.records], [1, 2])
        value['components'][0] = {**subject, 'version': 'changed'}
        self.refuse(value, 'sbom_duplicate_reference')
        for records in ([subject, subject], [{'bom-ref': 'a'}, {'bom-ref': 'a'}]):
            self.refuse(synthetic_document(components=records), 'sbom_duplicate_reference')
        self.refuse(synthetic_document(components=[{'bom-ref': 'a'}], services=[{'bom-ref': 'a'}]), 'sbom_duplicate_reference')
        for ref in ('', 0, 'x' * 1025):
            self.refuse(synthetic_document(components=[{'bom-ref': ref}]), 'sbom_unsupported_format')
        self.accept(synthetic_document(components=[{'bom-ref': 'x' * 1024}]))

    def test_nested_and_relevant_containers(self):
        self.refuse(synthetic_document(components=[{'components': [{}]}]), 'sbom_nested_population_unsupported')
        self.refuse(synthetic_document(metadata={'component': {'name': 's', 'bom-ref': 'r', 'components': [{}]}}), 'sbom_nested_population_unsupported')
        self.refuse(synthetic_document(components=[{'properties': {}}]), 'sbom_unsupported_format')
        self.accept(synthetic_document(components=[{'group': [], 'name': {}, 'version': 9}]))

    def test_inventory_graph_budgets(self):
        for key, limit in (('components', 10_000), ('services', 1000)):
            self.accept(synthetic_document(**{key: [{}] * limit}))
            self.refuse(synthetic_document(**{key: [{}] * (limit + 1)}), 'sbom_budget_exceeded')
        self.accept(synthetic_document(dependencies=[{}] * 11_001))
        self.refuse(synthetic_document(dependencies=[{}] * 11_002), 'sbom_budget_exceeded')
        self.accept(synthetic_document(dependencies=[{'dependsOn': ['a'] * 10_000}] * 5))
        self.refuse(synthetic_document(dependencies=[{'dependsOn': ['a'] * 10_000}] * 5 + [{'dependsOn': ['a']}]), 'sbom_budget_exceeded')

    def test_optional_assertions_do_not_reject_population(self):
        value = synthetic_document(serialNumber='invalid', compositions='invalid')
        value['metadata'].update(timestamp='2020-01-01T00:00:00+01:00', tools='malformed')
        serial, created, producer, compositions = document_assertions(self.accept(value))
        self.assertEqual(serial['status'], 'invalid')
        self.assertEqual(created['value'], '2019-12-31T23:00:00Z')
        self.assertEqual(producer['state'], 'redacted')
        self.assertEqual(compositions['state'], 'unsupported')
        value['metadata']['tools'] = [{'name': 'tool', 'version': '1'}] * 33
        self.assertEqual(document_assertions(self.accept(value))[2]['tools_omitted'], 1)

    def test_hostile_optional_assertions_are_scoped(self):
        for aggregate in ([], {}, 1, None):
            doc = self.accept(synthetic_document(compositions=[{'aggregate': aggregate}]))
            self.assertEqual(document_assertions(doc)[3], {'state': 'unsupported', 'aggregates': []})
        for timestamp in ('0001-01-01T00:00:00+01:00', '9999-12-31T23:59:59-01:00'):
            value = synthetic_document()
            value['metadata']['timestamp'] = timestamp
            self.assertEqual(document_assertions(self.accept(value))[1]['status'], 'invalid')

    def test_subject_alias_requires_typed_whole_object_equality(self):
        value = synthetic_document()
        value['metadata']['component']['modified'] = True
        value['components'] = [{**value['metadata']['component'], 'modified': 1}]
        self.refuse(value, 'sbom_duplicate_reference')
