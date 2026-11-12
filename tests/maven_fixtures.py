"""Explicit Maven absence for independent pre-Maven sibling semantics fixtures.

These fixtures certify absence as test input; they do not exercise native inventory.
Maven integration/security tests must use real discovery or their own staged readers.
"""

import unittest
from unittest.mock import patch


def declare_maven_absent():
    inventory = patch('libyears.scan.scan_maven', return_value=None)
    inventory.start()
    unittest.addModuleCleanup(inventory.stop)
