"""Trusted offline lifecycle fixture; no sockets, target imports or descendants."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from libyears.nuget_worker import run_worker


def block(authority, client):
    import time
    # Remain inside the command handler without checking any supplied deadline.
    while True:
        time.sleep(3600)


run_worker(block)
