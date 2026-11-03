"""Absolute isolated entry point for the installed NuGet-only worker."""

# -I excludes cwd, PYTHONPATH and user site. Insert only this installed code root.
import sys
from pathlib import Path

if __name__ == '__main__' and not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import math
import time

from libyears.nuget_registry import NuGetMetadataClient, NuGetRegistryFailure
from libyears.nuget_supervisor import (
    PackageResult, decode_authority, read_message, result_message, write_message,
)


def _lookup(authority, client):
    # T009 owns traversal; startup and readiness never import or call its handler.
    from libyears.nuget_registry import lookup_authorized_package
    return lookup_authorized_package(authority, client)


def run_worker(handler=_lookup):
    directory = Path.cwd()
    client = NuGetMetadataClient()
    write_message(directory / 'ready.json', {'ready': 1})
    sequence = 0
    while True:
        command_path = directory / 'command.json'
        if not command_path.exists():
            time.sleep(0.01)
            continue
        command = read_message(command_path)
        command_path.unlink()
        if set(command) != {'sequence', 'authority', 'package_deadline', 'scan_deadline'}:
            raise ValueError('protocol')
        if type(command['sequence']) is not int or command['sequence'] != sequence + 1:
            raise ValueError('protocol')
        sequence = command['sequence']
        authority = decode_authority(command['authority'])
        for key in ('package_deadline', 'scan_deadline'):
            deadline = command[key]
            if type(deadline) not in (int, float) or not math.isfinite(deadline):
                raise ValueError('protocol')
        try:
            client.begin_package(authority.package_key,
                                 package_deadline=command['package_deadline'],
                                 scan_deadline=command['scan_deadline'])
            if time.monotonic() >= min(command['package_deadline'], command['scan_deadline']):
                raise NuGetRegistryFailure('registry_error')
            result = handler(authority, client)
        except NuGetRegistryFailure as failure:
            result = PackageResult(reason=failure.reason)
        write_message(directory / 'result.json', {
            'sequence': sequence, 'result': result_message(result)})


if __name__ == '__main__':
    run_worker()
