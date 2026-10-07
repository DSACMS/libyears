# Feature 002 Technical Plan

**Status:** Approved

## Existing Architecture

Current flow:

```text
requirements.txt / optional resolved.txt
    -> requirements.py discovery
    -> scan.py snapshot evidence matching and conflict handling
    -> pypi.py registry lookup and release metadata
    -> metric.py dependency calculation and repository summary
    -> scan.py ScanReport
    -> output.py human text or JSON schema v2
```

`requirements.py` parses direct requirements, normalizes PyPI names, and
returns exact and unmeasurable requirement records. `snapshot.py` parses the
narrow `NAME==VERSION` pip-freeze snapshot; `constraints.py` checks Python
declaration compatibility against snapshot versions. `scan.py` owns repository
discovery, Python evidence reconciliation, registry calls, failure isolation,
and report construction. `pypi.py` returns release metadata or a
`RegistryFailure`; it also owns urllib transport, request headers/timeouts,
diagnostic categorization, and all TLS CA selection. `metric.py` contains
ecosystem-independent arithmetic and builds the single aggregate summary.
`model.py` contains immutable dependency, measurement, summary, and report
dataclasses. `output.py` constructs schema v2 and human output. `cli.py` parses
flags and maps filesystem/usage/systemic failures to exit codes.

Domain models already carry `ecosystem` on measurable dependencies and
unmeasurable requirements, and `Dependency.version_source` already supports
`requirements_exact` and `resolved_snapshot`. The release/result flow is
otherwise PyPI-shaped: the registry result is defined in `pypi.py`, while scan
expects the PyPI adapter/result and requirement-specific data. Registry
failure reason identifiers and concise transport diagnostics are strings.

PyPI-specific coupling is concentrated in `requirements.py` name rules,
`snapshot.py` format, `constraints.py`, `scan.py` discovery/reconciliation,
`pypi.py` lookup plus transport/TLS, and `output.py`'s fixed PyPI evidence,
ecosystems list, human text, and schema version. Reusable behavior includes
the `Dependency` / `DependencyMeasurement` model, UTC normalization,
`measure_dependency`, `calculate_summary`, timestamp formatting, generic
failure isolation, and the CLI TLS option.

`SPEC.md` describes PyPI behavior and schema v2, while README describes a
PyPI-only CLI. Feature 002 intentionally supersedes the ecosystem and JSON
scope for the new release; these documents and the project ecosystem scope in
`AGENTS.md` need synchronized edits during implementation.

## npm Data Model Findings

The root `package.json` production declarations are a JSON object mapping
package names to version specifications. `optionalDependencies` entries
override same-name `dependencies` declarations in npm's manifest semantics;
Feature 002 consequently excludes a name if it appears in that optional map,
even if it also appears in `dependencies`. `devDependencies`,
`peerDependencies`, `peerDependenciesMeta`, child workspaces, and lockfile-only
entries do not determine Feature 002 discovery.

Both supported lockfile versions use the `packages` object as a mapping from
installation location to package metadata. The root package is keyed by the
empty string. The installed top-level package entry is keyed by
`node_modules/<package-name>` and exposes its exact `version`. Scoped names
retain their slash in the path, for example
`node_modules/@types/node`. This convention supports exact direct matching
without recursively finding a same-named transitive package. v2 also carries
legacy nested `dependencies` data; direct resolution should use the package
location map, not that legacy tree. v3 removes the v2 backwards-compatibility
affordance but retains the package-location model. npm documents the format,
version history, and path map in its [`package-lock.json` documentation](https://docs.npmjs.com/files/package-lock.json/).

The manifest's `dependencies` and `optionalDependencies` values can be ranges,
URLs, Git references, local paths, aliases, and other npm package specs. npm
documents the production map and its supported dependency spec forms in
[`package.json`](https://docs.npmjs.com/cli/v10/configuring-npm/package-json/?v=true);
it also states that optional entries override same-name production entries.
Treat recognized Git/GitHub references, `file:`, `link:`, `workspace:`, remote
HTTP(S) tarballs, and `npm:` aliases as `unsupported_dependency_source`,
preserving the exact source string. Recognize plain GitHub shorthand
conservatively (such as `owner/repo` with optional ref) without mistaking
scoped package names: the dependency key identifies the package, while the
declaration value is what is classified.

For supported v2/v3 files, exact direct evidence is the version at the root
installation path for that manifest name. Do not search descendant paths or
match solely by package name, because that can select a transitive copy. If
the direct path is absent, use `lock_version_missing`. Package entries with
non-version/link semantics cannot establish an exact ordinary registry
version and fail closed. Lockfile v1 is rejected before trying to interpret
its legacy tree; unknown versions are rejected with
`unsupported_lockfile_version`.

Authoritative references:

- npm [`package-lock.json`](https://docs.npmjs.com/files/package-lock.json/)
  documents lockfileVersion 2 (npm 7/8), version 3 (npm 9+), the `packages`
  path-keyed map, and v2's legacy `dependencies` map.
- npm [`package.json` dependencies and optionalDependencies](https://docs.npmjs.com/cli/v10/configuring-npm/package-json/?v=true)
  documents range/source forms and the same-name optional override.
- npm [`package-lock.json` v7 docs](https://docs.npmjs.com/cli/v7/configuring-npm/package-lock-json/)
  documents `node_modules` location keys and scoped entries in the lockfile
  package map.

## Proposed Architecture

Add only two ecosystem-facing boundaries, justified by the concrete second
ecosystem:

1. **Dependency source boundary.** Use one static, explicit list of source-and-
   registry-adapter pairs known to the scan coordinator: Python with PyPI and
   npm with npm. Each source returns a common discovery result containing
   candidates, dependency-level unmeasurables, source-level errors, and
   ecosystem evidence metadata. The coordinator iterates the pairs uniformly
   to discover and measure candidates; it does not branch on ecosystem names
   for normal flow. Preserve Python parsing and snapshot reconciliation in
   `requirements.py`, `snapshot.py`, and `constraints.py`; keep npm manifest
   and lock evidence in `npm.py`. Define only the small shared candidate and
   result types needed by these two pairs. Do not add dynamic registration,
   factories, a registry-of-registries, or a plugin framework.
2. **Registry adapter boundary.** Both adapters accept package identity and an
   exact used version and return a common release lookup result or common
   `RegistryFailure`. A result carries used release timestamp and latest
   stable version/timestamp; candidate identity and version source remain in
   the dependency-source record. Registry-specific parsing stays in each
   adapter.

Keep the existing `Dependency`, `DependencyMeasurement`, and core metric
arithmetic. Introduce a report that retains one repository-wide summary and a
summary keyed by ecosystem. Compute each through `calculate_summary`; do not
copy arithmetic into scan or output. Keep human rendering and JSON
serialization separate.

The source protocol should remain narrow: discover from a repository root and
available source-specific evidence; return candidates plus unmeasurable
items and evidence metadata. Do not add generic package graphs, arbitrary
registries, capabilities, lifecycle hooks, or ecosystem plugin loading.

## Data Flow

1. CLI resolves path, `--resolved`, and CA bundle as it does today.
2. The coordinator invokes each configured source/adapter pair independently.
   Missing supported manifests yield empty discovery results. An unparseable
   root `package.json` yields npm source error `invalid_manifest`, with npm
   counts and per-ecosystem summary values unknown; it does not abort Python.
   For a valid manifest and malformed supported lockfile, retain the known
   direct npm dependencies as discovered and mark each affected item
   `invalid_lockfile`. An unsupported lockfile version instead uses
   `unsupported_lockfile_version`. Neither npm condition aborts Python.
3. Python source discovers `requirements.txt`, applies exact-pin and optional
   resolved-snapshot precedence/conflict rules, and emits version sources
   `requirements_exact` or `resolved_snapshot`.
4. npm source reads root `package.json`, filters effective production scope,
   classifies unsupported declaration forms, then uses supported
   `package-lock.json` evidence and emits `package_lock` for measurable
   candidates. It accepts lock versions for non-exact ranges and registry
   tags such as `latest` without npm range/tag evaluation. Exact manifest
   literals require exact textual equality with the lock version. Source-
   changing forms remain unsupported; no complete npm package-spec grammar
   is attempted.
5. Each candidate is sent to its ecosystem's registry adapter. Per-package
   failures become unmeasurable records; one adapter or ecosystem failing
   does not discard another source's results.
6. Common registry results are combined with candidate evidence into existing
   `Dependency` records, and `metric.py` calculates measurements.
7. The report computes repository-wide and per-ecosystem summaries from the
   same measurement set and discovered records.
8. `output.py` renders human or schema v3 JSON.

Python-only scans follow the current evidence and registry path. npm-only
scans use package files and the npm adapter. Mixed scans concatenate source
results, preserve ecosystem identity, and aggregate both.

## Domain Model Changes

- Keep `Dependency` fields, including `ecosystem` and `version_source`;
  supported values become `requirements_exact`, `resolved_snapshot`, and
  `package_lock`.
- Keep `DependencyMeasurement` and the metric formula unchanged.
- Generalize the adapter result currently named `PyPIResult` to a common
  release lookup result (or move its equivalent into `model.py`). Its
  timestamps and latest-version fields already describe both ecosystems.
- Move or define `RegistryFailure` at the common registry boundary so both
  adapters share the exact reason/diagnostic shape.
- Add a discovery candidate/result type sufficient to retain ecosystem,
  original package name, normalized registry identity, original declaration,
  exact used version when available, and evidence source. Keep unmeasurable
  records ecosystem-tagged and retain `declared` as the original npm spec.
- Extend report data with `by_ecosystem` summaries, ecosystem-keyed version
  evidence, and source-level errors. Permit `dependencies_discovered` to be
  unknown when discovery fails. For a failed ecosystem, its discovered and
  measured counts, coverage, and aggregates are null. Repository-wide
  discovered count and coverage are null if any detected ecosystem failed
  discovery; repository-wide measured count and aggregates still summarize
  successful measurements from sources that completed discovery. Keep source
  errors separate from dependency-level unmeasurables.

No change to libyears arithmetic or timestamp rules is needed.

## Registry Design

Keep `PyPIAdapter` and add `NpmAdapter`, both implementing the narrow common
lookup contract. PyPI parsing continues to select its canonical upload time
and apply its current yanked/prerelease rules. npm parsing reads one public
registry package metadata response and uses `versions` plus `time`.

The npm adapter requests public registry full package metadata over HTTPS.
For scoped names, percent-encode the slash for the URL path while retaining
the unencoded identity for output. For the exact used version, require a
matching entry in `versions` and a valid timestamp in `time`. For latest
stable, consider only version keys also present in `versions`, retain those
with valid `time` values and eligible stable classification, then choose the
greatest publication timestamp. If multiple eligible stable versions share
that greatest timestamp, prefer `dist-tags.latest` only if it names one of
those tied versions; otherwise use deterministic lexical ordering solely to
select the reported version. Keep the shared timestamp unchanged, so this tie
rule cannot affect release age or arithmetic. Other dist-tags do not affect
eligibility. Do not infer a version from the packument's modified/created
timestamps.

Use the existing HTTPS request behavior: finite timeout, User-Agent, verified
TLS, selected CA context, HTTP/transport categorization, invalid JSON/shape
handling, and mockable urllib boundary. Factor common request/TLS selection
and concise transport diagnostics from `pypi.py` into one focused shared
transport module; adapters remain responsible for registry payload semantics.
Both registry adapters must receive the same CLI CA-bundle and timeout policy.

## Stable Version Strategy

Use a conservative recognizer for concrete npm registry version strings, not
a general-purpose range parser. Accept only canonical three-component
numeric semantic versions (`MAJOR.MINOR.PATCH`, with no leading zeroes except
zero itself), optionally followed by valid `+build.metadata` identifiers.
Treat a valid prerelease suffix introduced by `-` as prerelease and exclude
it. Reject versions with malformed components, a `v` prefix, unsupported
suffixes, or any other unclassifiable syntax from latest-stable candidacy.
Build metadata does not make a release a prerelease; it remains eligible, and
version selection still uses publication timestamps rather than ordering the
version strings.

This accepts standard stable concrete release forms and standard prerelease
forms while failing closed on npm-specific or malformed forms not needed to
identify stable status confidently. The lockfile's exact used version is
looked up by exact key; the used version need not itself be stable to obtain
its release timestamp. No caret, tilde, x-range, compound, hyphen, alias, or
other range evaluation is performed. The implementation must test this
recognizer against explicit supported and rejected fixtures.

## Mixed-Ecosystem Aggregation

`dependencies_discovered` is the count of all discovered in-scope direct
dependencies, measured plus unmeasurable. `dependencies_measured` is the
number successfully converted to measurements. When all detected sources
complete discovery, repository coverage is measured/discovered, or null when
discovered is zero. If any source fails discovery, repository discovered count
and coverage are null because the denominator is incomplete. Repository-wide
measured count and total/mean/median/max still summarize every successful
measurement. A discovery-failed ecosystem has null for all its count,
coverage, and aggregate fields; a successfully discovered ecosystem with zero
measurements has its known discovered count, zero measured count, its computed
coverage, total `0.0`, and null mean/median/max. `metric.py`'s existing summary
function remains the sole implementation of aggregate arithmetic; adapt its
summary input/result to allow an unknown discovered denominator rather than
reimplementing arithmetic. This may require allowing a nullable discovered
count in the summary model; do not encode discovery failure as zero.

Do not count unsupported source forms outside scope (development, peer,
optional, workspace child) as discovered. In-scope unsupported npm
declarations count as discovered and unmeasurable. A successfully discovered
ecosystem with no dependencies has discovered/measured zero, null coverage,
total zero, and null mean/median/max. Ordering of ecosystem keys should be
deterministic.

## JSON Schema v3 Migration

Schema v3 changes exactly these v2 aspects:

- `schema_version` changes from `2` to `3`.
- `version_evidence` changes from one PyPI-shaped object to an object keyed
  by ecosystem. The existing PyPI evidence values remain nested under
  `pypi`; npm has `declaration_source: "package.json"` and
  `snapshot_source: "package-lock.json"`.
- `summary` retains repository-wide existing statistic names and adds
  `by_ecosystem`, mapping each ecosystem to the same statistic fields.
  Discovery-failed ecosystem fields are null; repository-wide discovered
  count and coverage are null when any detected source fails discovery.
- `source_errors` is a top-level array, empty when no source-level failures
  occur. Each item has `ecosystem`, `source`, and `reason`; malformed npm root
  manifest is `{"ecosystem":"npm","source":"package.json","reason":"invalid_manifest"}`.
  Dependency-level lock failures remain in `unmeasurable`, not `source_errors`.
- `ecosystems` lists every ecosystem with a supported dependency source
  discovered for the scan, in deterministic order.
- Dependency rows retain current fields and add no ecosystem-specific shape;
  all carry `ecosystem`, and measurable rows carry `version_source` with
  `package_lock` for npm.
- Unmeasurable rows retain `ecosystem`, `name`, `declared`, and `reason`;
  npm `declared` preserves its original manifest string.
- A malformed root npm manifest produces top-level
  `source_errors: [{"ecosystem":"npm","source":"package.json","reason":"invalid_manifest"}]`;
  it creates no synthetic dependency rows. In a mixed scan, a valid PyPI
  measurement remains in `dependencies`, npm per-ecosystem counts/coverage/
  aggregates are null, repository discovered count and coverage are null, and
  repository measured count/aggregates include the valid PyPI measurement.

Compact structural examples (timestamps and dependency records abbreviated
only where noted):

PyPI-only:

```json
{"schema_version":3,"metric":"libyears","dependency_scope":"direct","ecosystems":["pypi"],"version_evidence":{"pypi":{"declaration_source":"requirements.txt","snapshot_source":null}},"summary":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":1.0,"mean_libyears":1.0,"median_libyears":1.0,"max_libyears":1.0,"by_ecosystem":{"pypi":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":1.0,"mean_libyears":1.0,"median_libyears":1.0,"max_libyears":1.0}}},"dependencies":[{"ecosystem":"pypi","name":"requests","used_version":"2.31.0","used_release_time":"2023-01-01T00:00:00Z","latest_stable_version":"2.32.0","latest_stable_release_time":"2024-01-01T06:00:00Z","libyears":1.0,"timestamp_anomaly":false,"version_source":"requirements_exact"}],"unmeasurable":[],"source_errors":[]}
```

npm-only:

```json
{"schema_version":3,"metric":"libyears","dependency_scope":"direct","ecosystems":["npm"],"version_evidence":{"npm":{"declaration_source":"package.json","snapshot_source":"package-lock.json"}},"summary":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":1.0,"mean_libyears":1.0,"median_libyears":1.0,"max_libyears":1.0,"by_ecosystem":{"npm":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":1.0,"mean_libyears":1.0,"median_libyears":1.0,"max_libyears":1.0}}},"dependencies":[{"ecosystem":"npm","name":"@example/widgets","used_version":"1.0.0","used_release_time":"2023-01-01T00:00:00Z","latest_stable_version":"2.0.0","latest_stable_release_time":"2024-01-01T06:00:00Z","libyears":1.0,"timestamp_anomaly":false,"version_source":"package_lock"}],"unmeasurable":[],"source_errors":[]}
```

Mixed repository (one npm measurement at 2.0 and one PyPI measurement at 0.0):

```json
{"schema_version":3,"metric":"libyears","dependency_scope":"direct","ecosystems":["npm","pypi"],"version_evidence":{"npm":{"declaration_source":"package.json","snapshot_source":"package-lock.json"},"pypi":{"declaration_source":"requirements.txt","snapshot_source":null}},"summary":{"dependencies_discovered":2,"dependencies_measured":2,"coverage":1.0,"total_libyears":2.0,"mean_libyears":1.0,"median_libyears":1.0,"max_libyears":2.0,"by_ecosystem":{"npm":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":2.0,"mean_libyears":2.0,"median_libyears":2.0,"max_libyears":2.0},"pypi":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":0.0,"mean_libyears":0.0,"median_libyears":0.0,"max_libyears":0.0}}},"dependencies":[{"ecosystem":"npm","name":"left-pad","used_version":"1.0.0","used_release_time":"2024-01-01T00:00:00Z","latest_stable_version":"1.0.1","latest_stable_release_time":"2025-12-31T12:00:00Z","libyears":2.0,"timestamp_anomaly":false,"version_source":"package_lock"},{"ecosystem":"pypi","name":"requests","used_version":"2.31.0","used_release_time":"2025-01-01T00:00:00Z","latest_stable_version":"2.32.0","latest_stable_release_time":"2025-01-01T00:00:00Z","libyears":0.0,"timestamp_anomaly":false,"version_source":"requirements_exact"}],"unmeasurable":[],"source_errors":[]}
```

Mixed scan with valid PyPI measurement and invalid npm manifest:

```json
{"schema_version":3,"metric":"libyears","dependency_scope":"direct","ecosystems":["npm","pypi"],"version_evidence":{"npm":{"declaration_source":"package.json","snapshot_source":"package-lock.json"},"pypi":{"declaration_source":"requirements.txt","snapshot_source":null}},"summary":{"dependencies_discovered":null,"dependencies_measured":1,"coverage":null,"total_libyears":0.0,"mean_libyears":0.0,"median_libyears":0.0,"max_libyears":0.0,"by_ecosystem":{"npm":{"dependencies_discovered":null,"dependencies_measured":null,"coverage":null,"total_libyears":null,"mean_libyears":null,"median_libyears":null,"max_libyears":null},"pypi":{"dependencies_discovered":1,"dependencies_measured":1,"coverage":1.0,"total_libyears":0.0,"mean_libyears":0.0,"median_libyears":0.0,"max_libyears":0.0}}},"dependencies":[{"ecosystem":"pypi","name":"requests","used_version":"2.34.2","used_release_time":"2025-01-01T00:00:00Z","latest_stable_version":"2.34.2","latest_stable_release_time":"2025-01-01T00:00:00Z","libyears":0.0,"timestamp_anomaly":false,"version_source":"requirements_exact"}],"unmeasurable":[],"source_errors":[{"ecosystem":"npm","source":"package.json","reason":"invalid_manifest"}]}
```

Unmeasurable npm declaration:

```json
{"ecosystem":"npm","name":"express","declared":"^5.1.0","reason":"lock_version_missing"}
```

Existing schema v2 callers must be told that v3 is an intentional breaking
contract change; do not emit both schemas or silently keep v2 fields at the
top level.

## Human Output Changes

Preserve the current compact single-ecosystem layout where practical. When
multiple ecosystems are present, add an ecosystem column to measured and
unmeasurable rows, and print repository-wide totals plus a concise per-
ecosystem coverage/aggregate block. Keep existing sorting by descending
libyears, reason explanations, verbose diagnostics, and human/JSON separation.
Do not add human-only diagnostics to JSON.

## Failure Model

Reuse existing identifiers where semantics match:

- `package_not_found`, `version_not_found`, `release_date_missing`,
  `no_stable_release`, `registry_error`, `invalid_registry_response`.
- Python discovery and snapshot identifiers remain unchanged.

Feature 002 adds these identifiers:

- `invalid_manifest` for source-level failure to parse root `package.json`;
  keep it in `source_errors`, not dependency-level `unmeasurable`.
- `invalid_lockfile` for malformed required structure/data in a supported
  v2/v3 lockfile. The manifest still determines the discovered dependencies;
  each affected direct npm dependency remains discovered and unmeasurable,
  while other ecosystems continue.
- `lock_version_missing` for absent lockfile/direct exact path.
- `declaration_lock_conflict` for an exact manifest literal unequal to the
  lock version.
- `unsupported_lockfile_version` for v1 and unknown versions; these are not
  malformed supported lockfiles.
- `unsupported_dependency_source` for approved unsupported declaration
  forms.

`RegistryFailure` continues to carry reason plus optional concise diagnostic.
Bad JSON or a structurally invalid required registry response is
`invalid_registry_response`; ordinary package/version/date misses use their
existing identifiers. Per-package failures stay in the unmeasurable list and
do not abort other dependencies. If npm-wide transport fails, Python lookups
continue independently. Verbose diagnostics and TLS trust details remain
human-only.

## File Changes

Existing files expected to change:

- `libyears/model.py` — shared discovery/report/result types and per-ecosystem
  summaries; retain dependency/measurement semantics.
- `libyears/scan.py` — source and registry orchestration, mixed aggregation,
  failure isolation.
- `libyears/pypi.py` — implement the common adapter result contract and use
  shared transport without changing PyPI eligibility rules.
- `libyears/metric.py` — only if a small helper is needed to build a report
  with the existing summary function; keep all arithmetic here.
- `libyears/output.py` — schema v3, ecosystem evidence, unmeasurable text,
  ecosystem-aware human output and summaries.
- `README.md`, `SPEC.md`, `AGENTS.md` — document npm support, schema v3, and
  the now-approved ecosystem scope.
- Existing tests under `tests/` — preserve and extend PyPI regression coverage
  and exercise the new behavior.

New focused modules proposed:

- `libyears/npm.py` — parse root npm manifests and v2/v3 lock evidence;
  classify sources, optional precedence, exact conflicts, and npm version
  evidence. It is necessary to keep npm format rules out of generic scan code.
- `tests/test_npm.py` — deterministic manifest, lockfile, and evidence cases.
- `tests/test_npm_registry.py` — npm metadata and stable-candidate fixtures.
- `tests/test_mixed_scan.py` — mixed discovery, aggregation, schema, and human
  presentation cases.
- `libyears/registry.py` — shared secure JSON-over-HTTPS transport, TLS trust
  selection, request defaults, and common transport failure diagnostics. It
  is necessary to prevent a second registry adapter from copying the large,
  security-sensitive transport implementation currently embedded in
  `pypi.py`.

Avoid a separate npm semver module unless tests show the small concrete-version
recognizer warrants isolation. Avoid generic manifests, cache layers, adapter
discovery frameworks, and package graph abstractions.

## Testing Strategy

All automated correctness tests use fixtures and mocks; no test requires
network access.

- npm manifest parser: production-only scope; optional-only and optional
  override exclusion; dev/peer exclusion; scoped names; malformed data;
  unsupported source forms preserve the declaration.
- package-lock v2: direct root path and scoped path versions; lockfile-only
  transitive ignored; missing direct path; exact conflict.
- package-lock v3: same cases as v2.
- lockfile v1 and unknown versions: `unsupported_lockfile_version` with no
  registry calls.
- malformed supported v2/v3 lockfiles: `invalid_lockfile` for each known
  in-scope dependency, with discovered count retained and no cross-ecosystem
  abort.
- malformed root `package.json`: source-level `invalid_manifest`, no
  synthetic dependency records, and null discovery-dependent counts/coverage.
- npm registry fixtures: exact used-version lookup, `time` parsing, missing
  package/version/time, malformed response, no stable release, publication
  time rather than lexical version order, deprecation remains eligible.
- Stable classification: ordinary stable forms, prerelease suffixes,
  optional build metadata, malformed/uncertain concrete versions, and
  unclassifiable-only registry result.
- Scoped registry request: correctly encoded URL while preserving displayed
  package identity.
- Mixed scan: Python-only, npm-only, and combined discovery; one registry
  ecosystem failure leaves successful measurements from the other intact.
  Verify `invalid_manifest` produces source_errors/null npm coverage and
  repository-wide null coverage while retaining a successful PyPI measurement.
  Verify `invalid_lockfile` retains known npm discovered counts and does not
  discard successful PyPI measurements.
- End-to-end integration: at least one deterministic offline mixed-repository
  fixture crosses manifest/requirements discovery, lock/snapshot evidence,
  mocked registry responses, metric calculation, repository and per-ecosystem
  aggregation, and both schema-v3 and human output assertions in one flow.
- Aggregation: exact cross-ecosystem and per-ecosystem counts, coverage,
  total, mean, median, max, and empty/zero-measurement cases.
- JSON: schema-v3 PyPI-only, npm-only, mixed structures; evidence-key
  nesting; `package_lock`; ecosystem on measured/unmeasurable entries; stable
  reasons and no diagnostics in JSON.
- Human output: compact single ecosystem, ecosystem column in mixed output,
  repository and per-ecosystem aggregates, unmeasurable explanations.
- PyPI regression: preserve fixtures for yanked releases, timestamps,
  prereleases, transport failures, TLS selection, exact pins, resolved
  snapshots, and current human output semantics.
- TLS/network reuse: verify both adapters use HTTPS, common finite timeout,
  User-Agent, selected verified context, and shared error classification.

## Migration and Compatibility

Schema v2 to v3 is intentionally breaking because `version_evidence` becomes
ecosystem-keyed and summary gains `by_ecosystem`. Existing callers that read
the old flat evidence object or assume schema version 2 need migration
guidance: branch on `schema_version`, read PyPI evidence from
`version_evidence.pypi`, and read repository statistics from the unchanged
top-level summary fields. Measured Python dependency records retain their
fields and values, including `requirements_exact` and `resolved_snapshot`.

Python-only repository metrics and dependency-level results should remain
equivalent. The Python-only JSON envelope changes version and evidence
nestedness intentionally. README and SPEC must replace PyPI-only/schema-v2
claims with Feature 002 support and schema v3 examples. AGENTS ecosystem
scope should acknowledge the approved npm extension. CI remains standard
library/unittest and deterministic offline; an optional live npm smoke test
must be a separate non-unit job.

## Risks

- A bad package path match could accidentally turn a nested/transitive entry
  into direct evidence; require root `node_modules/<name>` matching only.
- Optional override mistakes would misstate production scope; test duplicate
  names across dependencies and optionalDependencies.
- npm's broad package-spec syntax can be misclassified; source recognition
  must be conservative and never fetch/resolve sources.
- A home-grown semantic-version parser can drift toward range support or
  accidentally accept uncertain strings; keep it limited to concrete release
  eligibility and test fail-closed cases.
- Shared transport refactoring could regress careful TLS selection; reuse the
  existing trust-selection behavior verbatim and add adapter-level tests.
- Public registry package absence does not prove private status; emit only
  `package_not_found`.
- Mixed output can mislead if only a combined ratio is shown; always show
  per-ecosystem coverage as well as repository-wide coverage.
- Schema v3 breaks v2 consumers; document migration and keep v3 shape stable.
- Do not execute npm, read `node_modules`, or allow lockfile processing to
  invoke tooling.
- Preserve current PyPI release ordering, yanked treatment, timestamp
  canonicalization, and metric arithmetic.

## Implementation Phases

1. Introduce common result/failure and source/report contracts while keeping
   Python scan outputs and metric behavior stable.
2. Extract the verified HTTP/TLS transport from PyPI into shared code and
   prove PyPI regression coverage against it.
3. Add npm manifest/lock parsing and source evidence for lockfile v2/v3,
   unsupported forms, scope filtering, and conflict behavior.
4. Add the npm public-registry adapter and conservative stable eligibility.
5. Integrate both sources, repository/per-ecosystem aggregates, and schema-v3
   serialization.
6. Update human output and user/project documentation; validate migration,
   run offline regression suite, then perform release dogfooding separately.

These are development phases, not a task checklist.

## Open Technical Questions

None currently block architecture review. The product decisions for
publication-time ties, registry dist-tags/manifest tags, malformed supported
lockfiles, and malformed npm manifests are reflected above.
