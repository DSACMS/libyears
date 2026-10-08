# Libyears

Libyears is a local Python CLI that measures the age of direct Python and npm
dependencies using release timestamps from PyPI and the public npm registry.
It uses only the Python standard library at runtime.

## What libyears measures

For each measurable dependency, libyears compares the release timestamp of its
exact used version with the timestamp of the latest stable release:

```text
libyears = max(latest stable release time - used release time, 0) / 365.25 days
```

The report includes total, mean, median, and maximum libyears, plus measurement
coverage. High libyears describes age; by itself, it does not mean a dependency
is vulnerable or unsafe.

## Important concept: version evidence

A dependency declaration says what a project requests, but it may not establish
the exact version used. For example, neither of these identifies an exact
version:

```text
requests
urllib3>=2.6.3
```

Libyears does not silently resolve those declarations against today's registry:
that would measure what might install now, not what the repository evidence
records. An exact repository pin or a resolved snapshot can provide version
evidence.

## Basic usage

Scan a directory (or a `requirements.txt` file directly):

```bash
python3 -m libyears PATH
python3 -m libyears PATH --json
```

## Exact-pinned requirements

Exact pins in `requirements.txt` can be measured directly:

```text
requests==2.34.2
pandas==2.3.3
```

## Resolved snapshot workflow

Create a snapshot and use it while scanning the repository:

```bash
python3 -m pip freeze > resolved.txt
python3 -m libyears PATH --resolved resolved.txt
```

The repository declarations still define direct dependency scope; the snapshot
supplies exact version evidence for those declared dependencies. Snapshot-only
transitive dependencies are ignored. Libyears does not invoke pip or install
dependencies itself. A freshly generated snapshot describes that environment
now, not historical repository state.

## TLS and enterprise environments

PyPI requests use HTTPS with certificate verification enabled. Libyears follows
Python/OpenSSL defaults, including `SSL_CERT_FILE` and `SSL_CERT_DIR`. If the
active interpreter has no usable default CA source, it can fall back to an
existing pip-bundled CA file. An explicit bundle takes precedence:

```bash
python3 -m libyears PATH \
  --resolved resolved.txt \
  --ca-bundle /path/to/approved-ca-bundle.pem
```

Python's standard environment override is also supported:

```bash
SSL_CERT_FILE=/path/to/approved-ca-bundle.pem \
python3 -m libyears PATH --resolved resolved.txt
```

An explicit `--ca-bundle` is authoritative and validated before scanning. If no
trusted CA source is available, requests fail with verification enabled.

> Never use an unverified TLS context merely to make registry requests succeed.

## Verbose diagnostics

```bash
python3 -m libyears PATH --verbose
```

Verbose output can identify certificate verification failures, HTTP failures,
timeouts, DNS/network errors, malformed registry responses, and the selected TLS
trust source. Stable JSON reason identifiers remain unchanged.

## JSON output

JSON schema version 3 reports ecosystem-keyed version evidence, repository and
per-ecosystem summaries, and source discovery errors separately from
dependency-level failures. The schema v2 to v3 change is intentional. A
compact Python-only example:

```json
{
  "schema_version": 3,
  "metric": "libyears",
  "dependency_scope": "direct",
  "ecosystems": ["pypi"],
  "version_evidence": {
    "pypi": {
      "declaration_source": "requirements.txt",
      "snapshot_source": null
    }
  },
  "summary": {
    "dependencies_discovered": 1,
    "dependencies_measured": 1,
    "coverage": 1.0,
    "total_libyears": 0.999315537303217,
    "mean_libyears": 0.999315537303217,
    "median_libyears": 0.999315537303217,
    "max_libyears": 0.999315537303217,
    "by_ecosystem": {
      "pypi": {
        "dependencies_discovered": 1,
        "dependencies_measured": 1,
        "coverage": 1.0,
        "total_libyears": 0.999315537303217,
        "mean_libyears": 0.999315537303217,
        "median_libyears": 0.999315537303217,
        "max_libyears": 0.999315537303217
      }
    }
  },
  "dependencies": [
    {
      "ecosystem": "pypi",
      "name": "requests",
      "used_version": "2.34.2",
      "used_release_time": "2024-06-01T00:00:00Z",
      "latest_stable_version": "2.35.0",
      "latest_stable_release_time": "2025-06-01T00:00:00Z",
      "libyears": 0.999315537303217,
      "timestamp_anomaly": false,
      "version_source": "requirements_exact"
    }
  ],
  "unmeasurable": [],
  "source_errors": []
}
```

## Measurement coverage

Coverage is the number measured divided by the number discovered. `7 discovered
/ 0 measured` means no dependency age could be calculated; `7 discovered / 7
measured` means the aggregate covers every discovered dependency. Their numeric
totals cannot be interpreted as equivalent, even if both are low.

## npm support

For npm repositories, `package.json` root `dependencies` define direct
production scope, excluding names also declared in `optionalDependencies`.
`package-lock.json` lockfile versions 2 and 3 provide exact used versions.
Development, peer, optional-only, workspace, and transitive dependencies are
outside this feature. npm ranges are never resolved during a scan.

## Current limitations

- Python declarations are read from `requirements.txt`; npm declarations are
  read from the root `package.json`.
- Direct dependencies only.
- The resolved snapshot format is a narrow list of exact `NAME==VERSION`
  entries; repository declarations determine which entries are in scope.
- Libyears does not install or resolve dependencies.
- Transitive dependencies are not measured by default.
- No other package ecosystems are supported.

## Development

Run the offline test suite with:

```bash
python3 -m unittest discover -s tests -v
```

See [SPEC.md](SPEC.md) for the full behavioral specification and [AGENTS.md](AGENTS.md)
for repository engineering rules.
