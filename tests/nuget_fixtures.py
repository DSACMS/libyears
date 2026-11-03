"""Exact-byte fixture reads for NuGet source semantics on every platform.

This seam supplies bounded synthetic inputs only. Filesystem safety, containment
and races are tested separately against the production descriptor reader.
"""

from contextlib import contextmanager
import os
from pathlib import Path
from unittest.mock import patch

from libyears import nuget_input as inputs
from libyears.nuget_input import LocalInput, NuGetInputFailure, ScopedNuGetReader


SAFE_SCOPED_READ = (
    all(getattr(os, flag, 0) for flag in ('O_DIRECTORY', 'O_NOFOLLOW', 'O_NONBLOCK'))
    and os.stat in getattr(os, 'supports_follow_symlinks', ())
    and all(function in getattr(os, 'supports_dir_fd', ())
            for function in (inputs._DIRECTORY_OPEN, os.stat, os.readlink))
)


@contextmanager
def fixture_nuget_reads(root: Path, files: dict[str, bytes]):
    """Inject only the selected reader's permitted, bounded fixture bytes."""
    def enter(reader):
        assert reader.root == root, 'Reader must use the synthetic fixture root.'
        return reader

    def read(reader, name):
        assert reader.root == root, 'Reader must use the synthetic fixture root.'
        assert name in reader.limits, 'Only explicitly selected inputs may be read.'
        if name not in files:
            raise NuGetInputFailure('missing')
        data = files[name]
        if len(data) > reader.limits[name]:
            raise NuGetInputFailure('limit')
        try:
            return LocalInput(data, data.decode('utf-8', errors='strict'))
        except UnicodeError:
            raise NuGetInputFailure('malformed') from None

    with patch.object(ScopedNuGetReader, '__enter__', autospec=True, side_effect=enter), \
            patch.object(ScopedNuGetReader, '__exit__', autospec=True, return_value=None), \
            patch.object(ScopedNuGetReader, 'read', autospec=True, side_effect=read) as reads:
        yield reads
