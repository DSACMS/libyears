"""Trusted lifecycle witness: readiness then block forever after first command."""
import json
from pathlib import Path
import time

Path('ready.json').write_text(json.dumps({'ready': 1}))
while not Path('command-1.json').exists():
    time.sleep(0.005)
time.sleep(3600)
