"""Explicit stable SBOM input/absence for portable composition witnesses."""

import hashlib
import json

from libyears.sbom_model import SbomDiscovery, SbomFailure, SbomSnapshot


class DocumentReader:
    """A supplied filename inventory, independent of host filesystem capabilities."""

    def __init__(self, documents=None, *, complete=True):
        self.documents = {name: (json.dumps(value).encode() if isinstance(value, dict) else value)
                          for name, value in (documents or {}).items()}
        self.complete = complete
        self.reads = []
        self.constructed = 0

    def __call__(self, root):
        self.constructed += 1
        return self

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        pass

    def discover(self):
        return (SbomDiscovery('automatic', 'complete' if self.complete else 'incomplete',
                              len(self.documents), self.complete,
                              None if self.complete else 'sbom_discovery_unavailable'),
                tuple(sorted(self.documents)) if self.complete else ())

    def snapshot(self, name):
        self.reads.append(name)
        if name not in self.documents:
            raise SbomFailure('sbom_input_unavailable')
        data = self.documents[name]
        return SbomSnapshot(name, data, hashlib.sha256(data).hexdigest())


def declare_sbom_absent():
    """Supply absence for pre-SBOM sibling semantics, never native intake tests."""
    import unittest
    from unittest.mock import patch
    inventory = patch('libyears.scan.scan_sbom', return_value=None)
    inventory.start()
    unittest.addModuleCleanup(inventory.stop)
