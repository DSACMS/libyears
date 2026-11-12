"""Installed isolated Maven metadata worker; no target imports or execution."""

import sys
from pathlib import Path

if __name__ == '__main__' and not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime, timezone
import time

from libyears.maven_http import MavenHTTPClient
from libyears.maven_model import MavenReason
from libyears.maven_protocol import command, date_text, read_message, result, write_message
from libyears.maven_registry import RegistryFailure


def run_worker():
    directory = Path.cwd()
    ca_file = str(directory / 'trust.pem') if (directory / 'trust.pem').exists() else None
    client = MavenHTTPClient(ca_file)
    write_message(directory / 'ready.json', {'ready': 1})
    sequence = 0
    while True:
        path = directory / f'command-{sequence + 1}.json'
        if not path.exists():
            time.sleep(0.01)
            continue
        request = command(read_message(path))
        if request['sequence'] != sequence + 1:
            raise ValueError('Maven protocol')
        sequence += 1
        operation = request['operation']
        selected = modified = None
        retrieved = datetime.now(timezone.utc)
        reason = None
        try:
            now = time.monotonic()
            if not now < request['deadline'] <= now + 10:
                raise RegistryFailure(MavenReason.METADATA_BUDGET_EXCEEDED)
            parsed = client.lookup(operation, request['group_id'], request['artifact_id'],
                                   request['version'], request['deadline'])
            retrieved = parsed.retrieved_at
            reason = parsed.reason
            if operation == 'select_target':
                selected = parsed.version
            else:
                modified = parsed.last_modified
        except RegistryFailure as failure:
            reason = failure.reason
            if operation == 'pom_date' and reason != MavenReason.METADATA_BUDGET_EXCEEDED:
                reason = MavenReason.TIME_BASIS_UNAVAILABLE
        value = {key: request[key] for key in ('sequence', 'operation', 'group_id', 'artifact_id', 'version')}
        value.update(selected_version=selected, last_modified=date_text(modified) if modified else None,
                     retrieved_at=date_text(retrieved), reason=reason,
                     attempts=client.attempts, body_bytes=client.body_bytes,
                     ordering_basis='maven_comparable_version_3_9_11' if operation == 'select_target' else None,
                     eligibility_policy='maven_conservative_stable_v1' if operation == 'select_target' else None,
                     time_basis='maven_conventional_pom_last_modified' if operation == 'pom_date' else None)
        result(value, request)
        write_message(directory / f'result-{sequence}.json', value)


if __name__ == '__main__':
    run_worker()
