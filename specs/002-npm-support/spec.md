# Feature 002: npm Ecosystem Support

**Status:** Approved for implementation
**Target:** post-v0.1  
**Feature:** npm direct-dependency libyears measurement

This feature intentionally extends the Python/PyPI MVP described in the
project's `SPEC.md`.

## 1. Problem

libyears currently measures direct Python dependencies published on PyPI.

Repositories using npm cannot currently be measured.

The goal of this feature is to support direct npm dependencies using repository-local dependency declarations and exact version evidence, while preserving the existing libyears principles:

- static analysis
- no dependency installation
- no dependency resolution
- no database
- no server
- authoritative registry metadata
- explicit measurement coverage
- fail closed when exact evidence is unavailable or ambiguous

## 2. User Outcome

Given a local npm repository containing:

- `package.json`
- and a supported `package-lock.json`

a user can run:

`python3 -m libyears PATH`

and receive a libyears measurement for the repository's supported direct npm dependencies.

The user does not need to:

- run `npm install`
- populate `node_modules`
- invoke npm
- run project code
- provide a database
- provide repository-hosting credentials

## 3. Core Semantic Rule

The npm implementation MUST use the same metric semantics as all other libyears ecosystems.

For each measurable direct dependency:

`libyears = max(latest_stable_release_time - used_release_time, 0) / 365.25 days`

A dependency at its latest stable version MUST produce exactly:

`0.0 libyears`

Ecosystem support MUST NOT introduce ecosystem-specific changes to the core metric.

## 4. Dependency Scope

For this feature, a **direct npm dependency** is a package declared in the
root project's `package.json` `dependencies` object, except when that package
also appears in `optionalDependencies`.

### Included

Packages listed under:

`dependencies`

### Not included in this feature

Packages appearing only under:

- `devDependencies`
- `peerDependencies`
- `peerDependenciesMeta`
- `optionalDependencies`
- bundled dependencies
- transitive dependency entries
- workspace child-package manifests

If a package appears in `optionalDependencies`, it is treated as optional and
excluded from production scope even if it also appears in `dependencies`.
Packages appearing in `devDependencies` or `peerDependencies` do not enter
scope, even when the same name appears in `dependencies`.

Development and other dependency scopes are separate future features.

This feature MUST NOT silently broaden the meaning of "direct dependencies."

## 5. Declaration Evidence

`package.json` defines which direct dependencies are in scope.

Examples:

```json
{
  "dependencies": {
    "express": "^5.1.0",
    "lodash": ">=4.17.0"
  }
}
```

These ranges establish dependency declarations.

They do NOT, by themselves, establish the exact version used by the repository.

libyears MUST NOT resolve these declarations against the npm registry at scan time.

## 6. Exact Version Evidence

For this feature, supported exact npm version evidence comes from:

`package-lock.json`

The lockfile establishes the exact resolved version corresponding to a direct dependency declared in the root `package.json`.

The implementation MUST distinguish between:

- declaration evidence from `package.json`
- exact version evidence from `package-lock.json`

A dependency MUST NOT be measured unless an exact supported version can be established.

## 7. Supported Lockfile Versions

Supported package-lock formats are `lockfileVersion: 2` and
`lockfileVersion: 3`. `lockfileVersion: 1` is explicitly unsupported.
Unknown lockfile versions MUST NOT be guessed. Unsupported v1 and unknown
versions make affected dependencies unmeasurable with reason
`unsupported_lockfile_version`.

A lockfile claiming supported v2 or v3 but missing required structure or
containing malformed required data makes each in-scope npm dependency
unmeasurable with reason `invalid_lockfile`. The manifest still establishes
the discovered dependency set, and other ecosystems continue to be scanned.

The implementation MUST NOT invoke npm to convert or upgrade a lockfile.

## 8. Manifest and Lock Evidence

The root manifest determines scope; the supported lockfile provides resolved
versions. A direct dependency absent from the lockfile is unmeasurable with
reason `lock_version_missing`. A lockfile-only package is ignored for direct
dependency scope.

If no supported lockfile is present, each in-scope direct npm dependency is
unmeasurable with reason `lock_version_missing`.

If the root `package.json` cannot be parsed, npm discovery fails with source
reason `invalid_manifest`. The npm dependency count is unknown; libyears MUST
not invent npm dependencies or create synthetic per-dependency unmeasurable
entries. Successfully discovered and measured dependencies from other
ecosystems remain available.

For a non-exact manifest declaration, the exact lockfile version is accepted
as resolution evidence. libyears does not validate npm range semantics for
caret, tilde, x-range, compound, hyphen, or other range forms.

For an exact manifest version, the lockfile version MUST equal the manifest
version exactly. Otherwise the dependency is unmeasurable with reason
`declaration_lock_conflict`.

## 9. Direct Dependency Matching

Only dependencies declared in the root `package.json` `dependencies` object are candidates for measurement.

The lockfile supplies exact versions for those packages.

Packages appearing only in the lockfile MUST NOT become direct dependencies.

This prevents transitive packages from changing the repository's direct-dependency scope.

For example:

`package.json`

```json
{
  "dependencies": {
    "express": "^5.1.0"
  }
}
```

A lockfile may contain hundreds of packages.

libyears MUST still discover exactly one direct dependency:

`express`

unless another supported direct dependency appears in the root declaration.

## 10. Scoped Packages

Scoped npm packages MUST be supported.

Examples:

`@types/node`

`@babel/core`

`@cms-ds/design-system`

The full scoped name is the package identity.

The implementation MUST preserve scoped names accurately for:

- manifest matching
- lockfile matching
- npm registry lookup
- human output
- JSON output

URL encoding required to query the registry is an implementation detail and MUST NOT alter the displayed package name.

## 11. Unsupported Dependency Sources

Some npm declarations do not refer to ordinary public-registry versions.

Unsupported declaration forms include:

- Git and GitHub references
- `file:` dependencies
- `link:` dependencies
- `workspace:` dependencies
- remote tarball URLs
- npm aliases

The initial npm feature MUST NOT guess how to measure unsupported source forms.

Unsupported dependencies:

- remain part of discovered direct-dependency count when declared under `dependencies`
- remain unmeasurable
- receive stable machine-readable reason `unsupported_dependency_source`
- do not prevent other dependencies from being measured

The original declaration MUST be preserved for diagnostics.

## 12. npm Registry Source

For public npm packages, release metadata MUST be retrieved directly from the public npm registry over HTTPS.

Registry metadata is expected to provide:

- published versions
- publication timestamps
- distribution tags

The implementation MUST NOT depend on the npm CLI or npm client libraries.

The public npm registry is the only registry queried. Private registry
configuration and authentication are out of scope. A package unavailable
from the public registry receives `package_not_found`; libyears MUST NOT
infer that it is private. The existing libyears HTTPS/TLS trust policy
applies.

The official npm registry full package metadata exposes a `time` mapping from package versions to publication timestamps. This mapping is the authoritative timestamp source for npm release dates.

## 13. Used Version Release Date

For an exact lockfile version:

1. locate that exact version in npm registry metadata
2. locate its publication timestamp in the registry `time` metadata
3. use that timestamp as the release time

If the exact version or publication timestamp cannot be found, the dependency is unmeasurable.

Unlike PyPI, npm publishes one canonical package-version publication timestamp in registry metadata, so file-upload timestamp reconciliation is not required.

## 14. Latest Stable Release

The implementation MUST select the newest eligible stable npm release based
on publication time. The newest version number MUST NOT be inferred through
lexical sorting.

Concrete versions confidently identifiable as stable are eligible. Prerelease
versions are excluded. Concrete version strings that are uncertain or cannot
be classified are excluded from latest-stable candidacy rather than guessed.
If no eligible stable release remains, measurement fails with the existing
`no_stable_release` reason. This specification defines behavior, not a version
classification algorithm.

## 15. npm `latest` Dist-Tag

The npm registry provides a `latest` distribution tag.

This feature MUST NOT assume that `dist-tags.latest` alone defines the newest stable release for libyears purposes.

Registry publication timestamps remain the basis of the metric.

The implementation MAY use `dist-tags.latest` as supporting metadata or validation, but metric semantics must remain explicit and reproducible.

## 16. Yanked / Deprecated / Unpublished Concepts

npm lifecycle concepts do not map exactly to PyPI yanked releases.

For this initial feature:

- package deprecation MUST NOT automatically exclude a release from measurement
- an available deprecated release may still be the used version
- unpublished versions absent from registry metadata cannot be measured
- npm-specific lifecycle behavior must not be silently mapped onto PyPI's yanked-release semantics

No additional npm lifecycle eligibility rules are introduced by this feature.

## 17. Measurement Coverage

Coverage semantics remain ecosystem-independent.

For npm:

`coverage = measurable direct npm dependencies / discovered direct npm dependencies`

Example:

```text
Dependencies discovered: 10
Dependencies measured:    8
Coverage:                 80%
```

Unmeasurable npm dependencies remain included in the discovered count. For
each ecosystem, `discovered` is the number of in-scope direct dependencies
found for that ecosystem, and `measured` is the number of those dependencies
with a successful measurement. Ecosystem coverage is `measured / discovered`.
If `discovered` is zero, coverage is `null`.

## 18. Multiple Ecosystems in One Repository

A repository may contain both Python and npm dependency sources.

The feature MUST support measuring supported ecosystems in the same repository without one silently replacing the other.

Example:

```text
requirements.txt
package.json
package-lock.json
```

may yield both:

- PyPI dependencies
- npm dependencies

The output MUST include both repository-wide and per-ecosystem statistics.
Repository-wide discovered and measured counts are sums across all supported
ecosystems. Repository-wide coverage is total measured divided by total
discovered, or `null` when total discovered is zero. Repository-wide
aggregate libyears statistics use all successfully measured dependencies
across ecosystems. Per-ecosystem counts, coverage, and aggregates use only
dependencies belonging to that ecosystem; a zero discovered count has
`null` coverage. Each dependency retains its ecosystem identity.

If a detected ecosystem's dependency discovery fails, its discovered and
measured counts, coverage, and aggregate values are `null` because that
ecosystem's dependency set is unknown. Repository-wide discovered count and
coverage are also `null` because the complete denominator is unknown.
Repository-wide measured count and aggregate libyears statistics may report
successfully measured dependencies from ecosystems whose discovery
succeeded. These aggregates describe only successful measurements and do not
imply complete discovery.

If a detected ecosystem's dependency discovery fails, its discovered and
measured counts, coverage, and aggregate values are `null` because that
ecosystem's dependency set is unknown. Repository-wide discovered count and
coverage are also `null` because the complete denominator is unknown.
Repository-wide measured count and aggregate libyears statistics may report
successfully measured dependencies from ecosystems whose discovery
succeeded. These aggregates describe only successful measurements and do not
imply complete discovery.

## 19. Version Evidence

Every measurable npm dependency MUST identify its version evidence. Existing
Python version evidence values remain unchanged under the ecosystem key.
Feature 002 intentionally changes the JSON contract from schema version 2 to
schema version 3. `version_evidence` is an ecosystem-keyed object. PyPI retains
its existing evidence values; npm uses `declaration_source: "package.json"`
and `snapshot_source: "package-lock.json"`.

Example measurable npm dependency:

```json
{"ecosystem":"npm","name":"express","used_version":"5.1.0","version_source":"package_lock"}
```

## 20. Unmeasurable Reasons

npm support uses stable machine-readable reasons. npm-specific reasons are:

- `lock_version_missing`
- `declaration_lock_conflict`
- `unsupported_lockfile_version`
- `invalid_lockfile`
- `unsupported_dependency_source`

For ecosystem-independent failures, reuse existing reasons when applicable,
including `package_not_found`, `version_not_found`, `release_date_missing`,
`no_stable_release`, `registry_error`, and `invalid_registry_response`.
`invalid_manifest` is a source-level failure for an unparseable root manifest.
`invalid_lockfile` is a dependency-level reason for malformed required data in
a supported v2/v3 lockfile: declarations are known, counted as discovered,
and each affected dependency is unmeasurable.

Do not create synonymous reason identifiers merely because the ecosystem differs.

## 21. Human Output

Human output must identify ecosystem when ambiguity is possible.

For example:

```text
ECOSYSTEM  DEPENDENCY       USED      LATEST    LIBYEARS
npm        express          5.1.0     5.2.0        0.31
pypi       requests         2.34.2    2.34.2       0.00
```

For repositories containing only one ecosystem, the implementation MAY keep output compact if ecosystem identity is otherwise clear.

Human output must continue to distinguish:

- measured dependencies
- unmeasurable dependencies
- coverage
- aggregate statistics
- evidence source where relevant

When npm manifest discovery fails with `invalid_manifest`, human output MUST
clearly state that npm dependency discovery failed because the manifest is
invalid, while still presenting successful results from other ecosystems.

## 22. JSON Output

Feature 002 intentionally introduces JSON schema version 3; compatibility with
schema v2 is not promised. The top-level object retains `metric`,
`dependency_scope`, `ecosystems`, `version_evidence`, `summary`,
`dependencies`, `unmeasurable`, and `source_errors`. `source_errors` is an
array of ecosystem/source-level failures, empty when none occur. Each
dependency object retains an explicit `ecosystem`; each measurable dependency
retains `version_source`.

`version_evidence` is keyed by ecosystem. Summary contains repository-wide
statistics and `by_ecosystem` statistics. Both levels contain
`dependencies_discovered`, `dependencies_measured`, `coverage`,
`total_libyears`, `mean_libyears`, `median_libyears`, and `max_libyears`.
Repository-wide statistics include all supported discovered/measured direct
dependencies; each ecosystem entry includes only that ecosystem. Coverage is
measured divided by discovered, or `null` when discovered is zero. If measured
is zero, total is `0.0` and mean, median, and maximum are `null`.
For an ecosystem whose discovery failed, every count, coverage, and aggregate
field under its `summary.by_ecosystem` entry is `null`. Repository-wide
discovered count and coverage are `null` if any detected ecosystem failed
discovery; repository-wide measured count and aggregates include successful
measurements from ecosystems that were discovered. Source-level errors are
separate from dependency-level `unmeasurable` entries:

```json
{"ecosystem":"npm","source":"package.json","reason":"invalid_manifest"}
```

The following compact examples normatively show the required structure.

PyPI-only:

```json
{"schema_version":3,"metric":"libyears","dependency_scope":"direct","ecosystems":["pypi"],"version_evidence":{"pypi":{"declaration_source":"requirements.txt","snapshot_source":null}},"summary":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":0.0,"mean_libyears":0.0,"median_libyears":0.0,"max_libyears":0.0,"by_ecosystem":{"pypi":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":0.0,"mean_libyears":0.0,"median_libyears":0.0,"max_libyears":0.0}}},"dependencies":[],"unmeasurable":[],"source_errors":[]}
```

npm-only:

```json
{"schema_version":3,"metric":"libyears","dependency_scope":"direct","ecosystems":["npm"],"version_evidence":{"npm":{"declaration_source":"package.json","snapshot_source":"package-lock.json"}},"summary":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":0.0,"mean_libyears":0.0,"median_libyears":0.0,"max_libyears":0.0,"by_ecosystem":{"npm":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":0.0,"mean_libyears":0.0,"median_libyears":0.0,"max_libyears":0.0}}},"dependencies":[],"unmeasurable":[],"source_errors":[]}
```

Mixed PyPI/npm:

```json
{"schema_version":3,"metric":"libyears","dependency_scope":"direct","ecosystems":["npm","pypi"],"version_evidence":{"npm":{"declaration_source":"package.json","snapshot_source":"package-lock.json"},"pypi":{"declaration_source":"requirements.txt","snapshot_source":null}},"summary":{"dependencies_discovered":2,"dependencies_measured":2,"coverage":1.0,"total_libyears":2.0,"mean_libyears":1.0,"median_libyears":1.0,"max_libyears":2.0,"by_ecosystem":{"npm":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":2.0,"mean_libyears":2.0,"median_libyears":2.0,"max_libyears":2.0},"pypi":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":0.0,"mean_libyears":0.0,"median_libyears":0.0,"max_libyears":0.0}}},"dependencies":[],"unmeasurable":[],"source_errors":[]}
```

Mixed repository with a valid PyPI measurement and malformed npm manifest:

```json
{"schema_version":3,"metric":"libyears","dependency_scope":"direct","ecosystems":["npm","pypi"],"version_evidence":{"npm":{"declaration_source":"package.json","snapshot_source":"package-lock.json"},"pypi":{"declaration_source":"requirements.txt","snapshot_source":null}},"summary":{"dependencies_discovered":null,"dependencies_measured":1,"coverage":null,"total_libyears":0.0,"mean_libyears":0.0,"median_libyears":0.0,"max_libyears":0.0,"by_ecosystem":{"npm":{"dependencies_discovered":null,"dependencies_measured":null,"coverage":null,"total_libyears":null,"mean_libyears":null,"median_libyears":null,"max_libyears":null},"pypi":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":0.0,"mean_libyears":0.0,"median_libyears":0.0,"max_libyears":0.0}}},"dependencies":[{"ecosystem":"pypi","name":"requests","used_version":"2.34.2","used_release_time":"2025-01-01T00:00:00Z","latest_stable_version":"2.34.2","latest_stable_release_time":"2025-01-01T00:00:00Z","libyears":0.0,"timestamp_anomaly":false,"version_source":"requirements_exact"}],"unmeasurable":[],"source_errors":[{"ecosystem":"npm","source":"package.json","reason":"invalid_manifest"}]}
```

Existing PyPI dependency-level semantics and evidence values remain unchanged;
the schema v2 to v3 contract change is intentional.

## 23. Network and TLS Policy

npm registry access MUST follow the existing libyears network-security policy.

Requirements include:

- HTTPS only
- certificate verification enabled
- existing explicit CA-bundle support
- existing environment-based certificate support
- existing secure fallback behavior where applicable
- finite request timeout
- safe verbose diagnostics
- no credential disclosure

Private registry authentication is out of scope.

## 24. Failure Isolation

Failure to measure one npm dependency MUST NOT abort measurement of unrelated dependencies.

Failure of npm registry access MUST NOT discard successful PyPI measurements in a mixed repository.

Ecosystem-specific failures should remain isolated wherever meaningful results can still be produced.

## 25. Security Boundary

npm support MUST preserve libyears' static-analysis boundary.

libyears MUST NOT:

- execute `npm`
- run `npm install`
- run lifecycle scripts
- read or execute `node_modules`
- execute repository JavaScript
- fetch package tarballs
- invoke dependency resolvers
- mutate `package.json`
- mutate `package-lock.json`
- modify the user's npm configuration

Only repository metadata and public registry metadata should be required.

## 26. Performance

The implementation SHOULD avoid redundant registry requests for the same package within one scan.

Persistent caching is not required by this feature.

Optimization MUST NOT change metric semantics.

## 27. Existing Behavior

Adding npm support MUST NOT change the meaning of existing PyPI measurements.

Existing Python-only repositories should continue to produce equivalent dependency-level results.

Changes to presentation required for multi-ecosystem output must be intentional and tested.

## 28. Required User Scenarios

### Scenario A — ordinary npm repository

Given:

- `package.json` declares three production dependencies
- `package-lock.json` contains exact matching versions
- all packages exist in the public npm registry

Then:

- three direct npm dependencies are discovered
- all three can be measured
- transitive lockfile packages are ignored for scope
- coverage is 100%

### Scenario B — no lockfile

Given:

- `package.json` declares dependencies
- no supported `package-lock.json` exists

Then:

- dependencies are discovered
- exact versions are not invented
- dependencies remain unmeasurable
- human output explains that exact lock evidence is unavailable

### Scenario C — transitive dependencies

Given:

- `package.json` declares one direct dependency
- `package-lock.json` contains 100 package entries

Then:

- exactly one direct dependency is discovered
- the other 99 entries do not become direct dependencies

### Scenario D — scoped package

Given:

`@example/widgets`

is a direct dependency with exact lockfile evidence.

Then the complete scoped name survives discovery, matching, registry lookup, human output, and JSON output.

### Scenario E — mixed Python/npm repository

Given both supported Python and npm manifests:

- both ecosystems are analyzed
- failures in one ecosystem do not erase successful results from the other
- aggregate output is clearly interpretable

### Scenario F — unsupported npm source

Given a direct dependency using an unsupported Git/local/workspace source:

- it remains discovered
- it is not guessed or resolved
- it is explicitly unmeasurable
- other dependencies continue measuring

### Scenario G — prerelease newer than stable

Given registry metadata where a prerelease was published after the newest stable release:

- the prerelease is excluded
- the stable release remains the comparison version

## 29. Acceptance Criteria

The feature is complete when all of the following are verified with
deterministic offline fixtures:

- [ ] Root production `dependencies` are discovered, excluding names present in `optionalDependencies`; `devDependencies` and `peerDependencies` do not add dependencies.
- [ ] Lockfile v2 resolves exact versions for declared direct dependencies.
- [ ] Lockfile v3 resolves exact versions for declared direct dependencies.
- [ ] Lockfile v1 and unknown versions leave npm dependencies unmeasurable with `unsupported_lockfile_version`.
- [ ] A direct declaration absent from a supported lockfile is unmeasurable with `lock_version_missing`.
- [ ] A malformed supported v2/v3 lockfile uses `invalid_lockfile`; declared in-scope npm dependencies remain discovered and unmeasurable, and other ecosystem measurements survive.
- [ ] An unparseable root `package.json` produces source error `invalid_manifest`, no synthetic npm dependency rows, unknown npm counts/coverage/aggregates, and does not erase valid PyPI results.
- [ ] In a mixed scan with `invalid_manifest`, repository-wide discovered count and coverage are null; successfully measured count and aggregate values reflect successful ecosystem measurements; npm per-ecosystem count, coverage, and aggregate values are null.
- [ ] Human output explicitly reports npm manifest discovery failure for `invalid_manifest`.
- [ ] Schema v3 places manifest failures in `source_errors` with ecosystem, source, and reason; dependency-level lock failures remain in `unmeasurable`.
- [ ] An exact manifest version unequal to lock evidence is unmeasurable with `declaration_lock_conflict`.
- [ ] A non-exact manifest declaration uses lock evidence without npm range validation.
- [ ] Lockfile-only packages do not affect discovered counts.
- [ ] Each listed unsupported source form remains discovered, is unmeasurable with `unsupported_dependency_source`, and retains its original declaration.
- [ ] Scoped package names are preserved in matching, registry lookup, human output, and JSON.
- [ ] Registry publication timestamps determine release age; a prerelease newer than the latest stable is excluded.
- [ ] An unclassifiable concrete registry version is excluded from latest-stable candidacy; if no eligible stable remains, reason is `no_stable_release`.
- [ ] Used version equal to latest stable produces exactly `0.0` libyears.
- [ ] A mixed PyPI/npm fixture reports repository-wide counts, coverage, and aggregate statistics using both ecosystems.
- [ ] The same mixed fixture reports correct per-ecosystem counts, coverage, and aggregate statistics.
- [ ] For a mixed fixture with PyPI discovered/measured `2/1` (measured value `1.0`) and npm `3/2` (measured values `2.0`, `4.0`), repository-wide output is discovered `5`, measured `3`, coverage `0.6`, total `7.0`, mean `7/3`, median `2.0`, maximum `4.0`; PyPI coverage is `0.5`, npm coverage is `2/3`, and each ecosystem's aggregates use only its measured values.
- [ ] PyPI-only, npm-only, and mixed JSON fixtures have schema version 3, ecosystem-keyed `version_evidence`, and repository-wide plus `by_ecosystem` summary statistics matching the normative examples.
- [ ] Measurable and unmeasurable dependency objects carry ecosystem; measurable dependency objects carry `version_source`.
- [ ] Registry failure for one ecosystem does not discard successful measurements from another.
- [ ] Existing PyPI dependency-level results remain equivalent under schema v3.
- [ ] Scanning requires no npm/Node execution, dependency installation, or repository code execution.

## 30. Release Validation

Before release, dogfood at least one real local npm repository and record and
review the observed results. A live npm registry smoke test may exist as a
separate CI job; it is not part of deterministic unit correctness.

## 31. Out of Scope

This feature does not include:

- `devDependencies`
- `peerDependencies`
- optional-only dependencies
- workspaces
- child package manifests
- Yarn lockfiles
- pnpm lockfiles
- private npm registries
- npm authentication
- dependency installation
- npm audit
- vulnerability analysis
- automatic updates
- transitive libyears reporting
- package health scoring
- JavaScript execution

These may become separate future specs.
