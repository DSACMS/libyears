"""Portable text fixtures for scoped Ruby composition tests.

This seam supplies synthetic fixture contents, not filesystem safety behavior.
Reader safety, containment, bounds, and races must use the production reader.
"""

from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from libyears.rubygems import _ScopedReadFailure, _ScopedRubyReader


@contextmanager
def fixture_scoped_reads(root: Path):
    """Snapshot the two fixture inputs, then spy on exact scoped reader requests."""
    root = root.resolve(strict=True)
    inputs = {}
    for name in ('Gemfile', 'Gemfile.lock'):
        try:
            inputs[name] = (root / name).read_bytes().decode('utf-8').replace('\r\n', '\n')
        except FileNotFoundError:
            reason = 'gemfile_missing' if name == 'Gemfile' else 'lockfile_missing'
            inputs[name] = _ScopedReadFailure(reason, 'Scoped input is missing.')
        except UnicodeDecodeError:
            reason = 'invalid_gemfile' if name == 'Gemfile' else 'invalid_lockfile'
            inputs[name] = _ScopedReadFailure(reason, 'Fixture input is not UTF-8.')

    def read(reader, name):
        assert reader.root == root, 'Scoped reader must use the synthetic fixture root.'
        assert name in inputs, 'Only exact scoped input names are fixture-supported.'
        return inputs[name]

    with patch.object(_ScopedRubyReader, 'read', autospec=True, side_effect=read) as reads:
        yield reads
