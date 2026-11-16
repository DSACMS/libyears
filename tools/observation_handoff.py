"""Store noncanonical observation JSON in the current checkout's Git directory."""

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def handoff_directory(repository='.'):
    """Resolve through Git, including linked worktrees and separate Git dirs."""
    result = subprocess.run(
        ['git', 'rev-parse', '--is-inside-work-tree', '--absolute-git-dir'],
        cwd=repository, check=True, capture_output=True, text=True,
    )
    inside, git_directory = result.stdout.strip().splitlines()
    if inside != 'true':
        raise ValueError('a Git working tree is required')
    worktree = subprocess.run(
        ['git', 'rev-parse', '--show-toplevel'], cwd=repository,
        check=True, capture_output=True, text=True,
    )
    git_directory = Path(git_directory).resolve()
    root = Path(worktree.stdout.strip()).resolve()
    # A custom Git dir inside the worktree can itself appear as untracked files.
    # Only the reserved .git component excludes an in-tree directory by construction.
    if git_directory.is_relative_to(root) and '.git' not in git_directory.relative_to(root).parts:
        raise ValueError('in-tree Git directory is not excluded from working-tree history')
    return git_directory / 'libyears-harness' / 'observations'


def validate_handoff(data, run_id):
    """Check the current repository's 44-key contract without inventing fields."""
    if re.fullmatch(r'[0-9]{3}-[0-9]{4}', run_id) is None:
        raise ValueError('invalid run ID')
    with (ROOT / 'observations' / 'agent-runs.csv').open(newline='') as handle:
        keys = next(csv.reader(handle, delimiter='|'))
    def unique_keys(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError('duplicate observation key')
            value[key] = item
        return value

    value = json.loads(data, object_pairs_hook=unique_keys)
    if len(keys) != 44 or not isinstance(value, dict) or list(value) != keys:
        raise ValueError('expected all 44 observation keys in header order')
    if value['run_id'] != run_id:
        raise ValueError('handoff run ID does not match destination')


def write_handoff(data, run_id, repository='.'):
    """Validate exact JSON bytes, then atomically replace the final local baton."""
    validate_handoff(data, run_id)
    directory = handoff_directory(repository)
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / (run_id + '.json')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode='wb', dir=directory, prefix='.' + run_id + '.', suffix='.tmp', delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return destination


def migrate_handoff(source, run_id, repository='.'):
    """Copy only existing bytes; missing sources fail before destination creation."""
    data = Path(source).read_bytes()
    validate_handoff(data, run_id)
    destination = handoff_directory(repository) / (run_id + '.json')
    if destination.exists() and destination.read_bytes() != data:
        raise ValueError('different destination handoff already exists')
    destination = write_handoff(data, run_id, repository)
    if hashlib.sha256(data).digest() != hashlib.sha256(destination.read_bytes()).digest():
        raise ValueError('migrated bytes failed verification')
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('directory', help='print the local handoff directory; create nothing')
    writer = commands.add_parser('write', help='atomically write JSON bytes from standard input')
    writer.add_argument('run_id')
    writer.add_argument('source', nargs='?', type=Path, help='optional prepared JSON file instead of stdin')
    migration = commands.add_parser('migrate', help='copy and verify one existing JSON baton')
    migration.add_argument('run_id')
    migration.add_argument('source', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == 'directory':
            destination = handoff_directory()
        elif args.command == 'write':
            data = args.source.read_bytes() if args.source is not None else sys.stdin.buffer.read()
            destination = write_handoff(data, args.run_id)
        else:
            destination = migrate_handoff(args.source, args.run_id)
        print(destination)
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'observation handoff unavailable: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
