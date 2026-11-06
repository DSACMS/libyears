"""Run the published GitLeaks history check; never install or suppress anything."""

from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
# Observed hosted version. Reconcile this with hosted logs when the action updates.
EXPECTED_VERSION = '8.30.1'


def main():
    try:
        version = subprocess.run(
            ['gitleaks', 'version'], check=True, capture_output=True, text=True,
        ).stdout.strip()
        if version != EXPECTED_VERSION:
            print(f'Require GitLeaks {EXPECTED_VERSION}; found {version}.', file=sys.stderr)
            return 2
        shallow = subprocess.run(
            ['git', 'rev-parse', '--is-shallow-repository'], cwd=ROOT,
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        if shallow != 'false':
            print('Require complete Git history; shallow checkout refused.', file=sys.stderr)
            return 2
        # Match hosted detect mode without --no-git or a restricted --log-opts.
        # Its default scans full history across available refs, not checkout files.
        with tempfile.TemporaryDirectory(prefix='libyears-gitleaks-') as temporary:
            result = subprocess.run(
                ['gitleaks', '--config', str(ROOT / '.github' / '.gitleaks.toml'),
                 '--verbose', '--redact=100', '--report-format', 'sarif',
                 '--report-path', str(Path(temporary) / 'gitleaks.sarif'),
                 '--source', str(ROOT), 'detect'], cwd=ROOT,
            )
        return result.returncode
    except (OSError, subprocess.CalledProcessError) as error:
        print(f'History check could not run: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
