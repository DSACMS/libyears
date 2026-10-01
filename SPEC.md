# Libyears MVP Specification

## 1. Goal

Implement a dependency-free Python CLI that calculates the CHAOSS Libyears metric for a local source repository.

The MVP supports Python dependencies published on PyPI.

It must work equally well for public repositories, private repositories, source archives, and ordinary local directories.

The repository host is irrelevant.

## 2. Non-goals

The MVP does not:

- clone repositories
- use GitHub or GitLab APIs
- maintain a database
- run as a server
- perform vulnerability scanning
- assess whether an old dependency is unsafe
- automatically update dependencies
- resolve arbitrary version constraints
- inspect transitive dependencies
- support private package registries
- support ecosystems other than PyPI

## 3. Definition

For one measurable dependency:

`age_days = latest_stable_release_time - used_release_time`

`libyears = max(age_days, 0) / 365.25`

Repository cumulative libyears is the sum of dependency libyears.

All calculations use UTC timestamps.

## 4. Dependency Scope

The MVP measures direct Python dependencies only.

Dependency discovery and exact-version resolution are separate concepts.

A dependency is measurable only when an exact package version can be established.

## 5. Dependency Source Precedence

Initial MVP support:

1. Exact pins in `requirements.txt`

Examples that are measurable:

`requests==2.31.0`

`flask==3.0.2`

Examples that are not measurable:

`requests>=2.28`

`flask~=3.0`

`django`

`requests @ git+https://...`

Local filesystem dependencies are not measurable.

If multiple supported dependency files declare the same normalized package name at conflicting exact versions, mark the dependency unmeasurable rather than selecting one.

Lockfile support is intentionally deferred to later milestones.

## 6. Package Name Normalization

Normalize PyPI project names according to PyPI name normalization semantics for comparison:

- lowercase
- runs of `-`, `_`, and `.` are treated equivalently

Preserve the original spelling for display where practical.

## 7. PyPI Data Source

Retrieve package metadata directly from PyPI's public JSON API over HTTPS using Python standard-library networking.

No PyPI client library may be used.

HTTP behavior must:

- use a finite timeout
- identify the application with an appropriate User-Agent
- handle HTTP failures without terminating the entire repository scan
- handle invalid JSON
- handle missing package versions
- handle releases without usable upload timestamps

Network behavior must be mockable in tests.

## 8. Used Version Release Date

For the exact version used by the project:

1. Locate the matching release in PyPI metadata.
2. Examine release files with valid upload timestamps.
3. Use the earliest valid upload timestamp for that release.

If no valid release timestamp exists, mark the dependency unmeasurable.

## 9. Latest Stable Version

"Latest stable" means the newest non-prerelease release suitable for general use.

For the MVP:

- exclude obvious prerelease versions such as alpha, beta, release candidate, dev, and preview releases
- exclude releases with no usable release timestamp
- exclude releases PyPI identifies as yanked
- determine newest stable by release timestamp, not lexical version ordering

The selected latest stable release is the eligible stable release with the newest valid release timestamp.

This deliberately avoids requiring a third-party semantic-version parser.

## 10. Yanked Releases

A release is considered unavailable as the latest stable candidate when all usable distribution files for that release are yanked.

A project's currently used version may still be measured if it is yanked.

The output may flag that condition.

## 11. Clock / Metadata Anomalies

If the selected latest-stable timestamp predates the used-version timestamp:

- set libyears to `0`
- attach an anomaly indicator
- do not produce a negative metric

## 12. Measurement Coverage

Repository output must distinguish discovery from successful measurement.

Example:

- dependencies discovered: 20
- dependencies measured: 18
- coverage: 90%

Coverage:

`measured / discovered`

If zero dependencies are discovered, coverage is `null`, not 0%.

## 13. Aggregate Statistics

Calculate aggregates only from successfully measured dependencies:

- cumulative libyears
- arithmetic mean
- median
- maximum

If zero dependencies are measurable, numerical aggregates are `null` except cumulative libyears, which may be `0`.

Individual dependencies should be sorted from highest libyears to lowest in human-readable output.

## 14. Unmeasurable Reasons

Use stable machine-readable reason identifiers.

Initial reasons:

- `non_exact_version`
- `unsupported_requirement`
- `conflicting_versions`
- `package_not_found`
- `version_not_found`
- `release_date_missing`
- `no_stable_release`
- `registry_error`
- `invalid_registry_response`

A human-readable explanation may accompany the identifier.

## 15. JSON Output

Top-level shape:

```json
{
  "schema_version": 1,
  "metric": "libyears",
  "dependency_scope": "direct",
  "ecosystems": ["pypi"],
  "summary": {
    "dependencies_discovered": 0,
    "dependencies_measured": 0,
    "coverage": null,
    "total_libyears": 0.0,
    "mean_libyears": null,
    "median_libyears": null,
    "max_libyears": null
  },
  "dependencies": [],
  "unmeasurable": []
}
```

A measurable dependency:

```json
{
  "ecosystem": "pypi",
  "name": "requests",
  "used_version": "2.31.0",
  "used_release_time": "2023-05-22T15:12:42Z",
  "latest_stable_version": "2.32.5",
  "latest_stable_release_time": "2025-08-18T20:46:02Z",
  "libyears": 2.24
}
```

An unmeasurable dependency:

```json
{
  "ecosystem": "pypi",
  "name": "requests",
  "declared": ">=2.28",
  "reason": "non_exact_version"
}
```

Do not make JSON consumers parse human-oriented strings.

## 16. Human Output

Example:

```text
Libyears: .

DEPENDENCY       USED       LATEST       LIBYEARS
requests         2.31.0     2.32.5          2.24
urllib3          1.26.18    2.5.0           1.88

Measured: 2 / 3 dependencies (66.7%)
Total:    4.12 libyears
Mean:     2.06
Median:   2.06
Maximum:  2.24

Unmeasurable:
  flask >=2.0    non_exact_version
```

Exact formatting is not part of the stable API.

## 17. Exit Codes

- `0`: scan completed, even if some dependencies were unmeasurable
- `1`: CLI usage or filesystem error
- `2`: scan could not produce meaningful results because of a systemic failure

An individual registry lookup failure does not cause a nonzero exit code if the rest of the scan succeeds.

## 18. Testing Philosophy

Tests must be deterministic and offline.

Fixture PyPI responses should cover at minimum:

- ordinary releases
- multiple files for a release
- prereleases
- yanked releases
- missing timestamps
- nonexistent used version
- no stable releases
- malformed registry response
- HTTP failure
- latest stable equal to used version
- timestamp anomaly
- conflicting requirement pins
- normalized package names

Metric arithmetic should be tested independently of HTTP and requirements parsing.

## 19. Future Milestones

Not part of MVP:

- filesystem cache
- `pyproject.toml`
- `uv.lock`
- Poetry lockfiles
- pip-tools
- environment markers
- requirements file inclusion
- npm
- Maven
- Go
- Cargo
- transitive dependencies
- SBOM input
- private registry adapters

Each should be implemented as an independently testable extension without changing the core metric model.
