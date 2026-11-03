"""Trusted offline lifecycle fixture; no sockets, target imports or descendants."""

import os
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from libyears.nuget_worker import run_worker
from libyears.nuget_supervisor import authority_message, write_message


def block(authority, client):
    # Only the decoded command handler can publish this evidence. All file
    # handles close before publication, including on Windows.
    write_message(Path.cwd() / 'handler-entered.json', {
        'pid': os.getpid(), 'authority': authority_message(authority),
        'package_deadline': client.package_deadline,
        'scan_deadline': client.scan_deadline,
    })
    # Nothing can set this event: the handler has no natural completion path
    # and never consults the supplied deadlines. Only OS termination ends it.
    threading.Event().wait()
    write_message(Path.cwd() / 'handler-returned.json', {'returned': True})


run_worker(block)
