# Libyears Specification v1.1

## 1. Goal

Implement a dependency-free CLI that calculates the CHAOSS Libyears metric for a local source repository.

The current implementation supports direct Python, npm, RubyGems, bounded NuGet
project snapshots and bounded Maven plural dependency-age views.
The original MVP sections below describe Python policy; the ecosystem extensions
in section 26 and the Maven extension below govern ecosystem-specific version/time
claims without changing PyPI behavior. Maven declares supported requests and uses
conventional POM modification dates; it does not claim retained selection/publication.

It must work equally well for public repositories, private repositories, source archives, and ordinary local directories.

The repository host is irrelevant.

The tool performs static analysis of dependency metadata present in the repository. It does not construct, install, or resolve a new runtime environment.

## 2. Core Principle: Measure Repository Evidence

Libyears measures dependency versions that can be established from repository evidence.

Use the strongest available accepted evidence, but require only evidence necessary
for the claim actually being made. The measurement claim concerns attributable
version facts and the relevant ecosystem-specific time evidence. Maven's separate
declared/observed and conventional POM-time contract is defined below. Acquisition, artifact content,
reproducible builds and actual deployment require independent evidence; none follows
from a number. Evidence mechanics remain ecosystem-specific. Current Python/npm
positive namespace limitations are recorded separately rather than silently changed.

The tool MUST distinguish between:

- a dependency being declared
- a dependency version being exactly established
- a dependency being successfully measured

For example:

`requests`

declares a dependency but does not establish which version is used.

Likewise:

`requests>=2.28`

declares an acceptable version range but does not establish which version is used.

Neither is sufficient for a reproducible libyears measurement.

An exact dependency version may come from:

- an exact pin
- a supported lockfile
- another supported repository artifact that records the resolved version

Support for these sources is ecosystem-specific.

The absence of an exact version is valid measurement information and MUST NOT be treated as a tool failure.

## 3. Non-goals

The MVP does not:

- clone repositories
- use GitHub or GitLab APIs
- maintain a database
- run as a server
- perform vulnerability scanning
- assess whether an old dependency is unsafe
- automatically update dependencies
- resolve arbitrary version constraints
- install project dependencies
- execute package managers to discover current versions
- construct virtual environments
- inspect the currently active Python environment
- infer versions from the developer's machine
- inspect transitive dependencies
- support private package registries
- support ecosystems beyond the explicitly approved PyPI, npm, RubyGems, bounded NuGet and Maven scope

The tool MUST NOT turn an unresolved dependency declaration into an exact version by resolving it against the package registry at scan time.

For example, given:

`requests>=2.28`

the tool MUST NOT resolve that constraint today and treat the resulting version as the version used by the repository.

Doing so would answer "what would install today?" rather than "what dependency version is evidenced by this repository?"

## 4. Definition

For one measurable dependency:

`age_days = latest_stable_release_time - used_release_time`

`libyears = max(age_days, 0) / 365.25`

Repository cumulative libyears is the sum of dependency libyears.

All calculations use UTC timestamps.

"Used version" means the exact dependency version established from supported repository evidence.

It does not mean:

- the newest version satisfying a declared constraint
- the version currently installed on the machine running libyears
- the version a package manager would resolve today

## 5. Dependency Scope

The Python scope is direct dependencies from requirements.txt; section 26 defines
additional ecosystem scopes.

Dependency discovery and exact-version resolution are separate concepts.

A dependency may therefore be:

1. discovered and measurable
2. discovered but unmeasurable
3. not discovered because its dependency source is unsupported

A discovered dependency is measurable only when:

- an exact package version can be established
- the relevant registry metadata can be retrieved
- release timestamps required by the metric are available

## 6. Dependency Source Precedence

Initial MVP support:

1. Exact pins in `requirements.txt`

Examples that are measurable:

`requests==2.31.0`

`flask==3.0.2`

Examples that are discovered but not measurable:

`requests`

`requests>=2.28`

`flask~=3.0`

Examples that are unsupported:

`requests @ git+https://...`

`git://...`

`ssh://...`

local filesystem dependencies

If multiple supported dependency sources eventually establish the same normalized package name, the most authoritative resolved-version source SHOULD take precedence according to ecosystem-specific rules.

If equally authoritative supported sources declare conflicting exact versions, mark the dependency unmeasurable rather than selecting one.

Lockfile support is ecosystem-specific as defined in section 26.

## 7. Package Name Normalization

Normalize PyPI project names according to PyPI name normalization semantics for comparison:

- lowercase
- runs of `-`, `_`, and `.` are treated equivalently

Preserve the original spelling for display where practical.

## 8. PyPI Data Source

Retrieve package metadata directly from PyPI's public JSON API over HTTPS using Python standard-library networking.

No PyPI client library may be used.

HTTP behavior must:

- use a positive, finite timeout
- identify the application with an appropriate User-Agent
- handle HTTP failures without terminating the entire repository scan
- distinguish invalid registry responses from transport/registry failures
- handle invalid JSON
- handle missing package versions
- handle releases without usable upload timestamps

Network behavior must be mockable in tests.

### TLS trust policy

Registry requests MUST use HTTPS with certificate and hostname verification
enabled. Without an explicit CA bundle, the application uses Python's normal
`ssl.create_default_context()` behavior, including the standard
`SSL_CERT_FILE` and `SSL_CERT_DIR` environment variables and OpenSSL defaults.
If that default context has no usable CA source, libyears MAY use an existing,
readable pip-vendored certifi CA file associated with the active Python
installation. This fallback is local only and does not import pip or certifi.

An explicit `--ca-bundle FILE` takes precedence over all other sources and is
validated before scanning. The source precedence is therefore: explicit bundle;
Python/OpenSSL defaults and environment overrides; then the pip-bundled fallback
when Python has no usable default CA source. If none is usable, TLS verification
fails closed. Libyears MUST NOT disable verification, download trust material,
or alter the system trust store.

With `--verbose`, human output may identify the selected TLS trust source and
show concise registry diagnostic categories. These details MUST NOT change
stable machine-readable reason identifiers or the JSON schema.

## 9. Used Version Release Date

For any PyPI release, its canonical release timestamp is the earliest valid
upload timestamp among its distribution files. This same timestamp MUST be used
when the release is evaluated as the repository's used version or as a latest
stable candidate.

For the exact version established by repository evidence:

1. Locate the matching release in PyPI metadata.
2. Examine release files with valid upload timestamps.
3. Use that canonical release timestamp.

If no valid release timestamp exists, mark the dependency unmeasurable.

## 10. Latest Stable Version

"Latest stable" means the newest non-prerelease release suitable for general use.

For the MVP:

- exclude obvious prerelease versions such as alpha, beta, release candidate, dev, and preview releases
- exclude releases with no usable release timestamp
- exclude releases PyPI identifies as yanked
- determine newest stable by release timestamp, not lexical version ordering

The selected latest stable release is the eligible stable release with the
newest canonical release timestamp.

This deliberately avoids requiring a third-party semantic-version parser.

## 11. Yanked Releases

A release is considered unavailable as the latest stable candidate when all usable distribution files for that release are yanked.

A project's currently used version may still be measured if it is yanked.

The output may flag that condition.

## 12. Clock / Metadata Anomalies

If the selected latest-stable timestamp predates the used-version timestamp:

- set libyears to `0`
- attach an anomaly indicator
- do not produce a negative metric

## 13. Measurement Coverage

Repository output MUST distinguish dependency discovery from successful measurement.

Example:

- dependencies discovered: 20
- dependencies measured: 18
- coverage: 90%

Coverage:

`measured / discovered`

If zero dependencies are discovered, coverage is `null`, not 0%.

Coverage is part of the interpretation of the metric.

A repository with:

- 100 dependencies
- 95 measured
- 5 unmeasurable

has a substantially different measurement quality from one with:

- 100 dependencies
- 10 measured
- 90 unmeasurable

Consumers SHOULD consider coverage alongside aggregate libyears values.

A 0% coverage result is valid and MUST NOT be represented as a scan failure when dependencies were successfully discovered but could not be measured.

## 14. Zero-Measurement Cases

The tool MUST distinguish between at least these cases.

### 14.1 No supported dependencies discovered

Example:

A JavaScript repository scanned by a PyPI-only implementation.

Human output SHOULD explain:

`No supported dependency manifests or dependencies were found.`

It SHOULD identify currently supported ecosystems.

This is not an error.

### 14.2 Dependencies discovered but no exact versions available

Example:

`requirements.txt` contains:

`requests`
`pandas`
`urllib3>=2.6.3`

Human output SHOULD explain that dependencies were found but their exact versions cannot be established.

Recommended message:

`All discovered dependencies lack exact versions.`

`Libyears requires exact dependency versions to produce a reproducible measurement.`

If appropriate:

`No supported lockfile or exact-pinned dependency source was found.`

This is not an error.

### 14.3 Exact versions exist but registry metadata cannot be measured

Examples:

- package not found
- version not found
- missing release timestamp
- registry request failure

Human output SHOULD identify the specific reasons.

A partial or zero measurement caused by individual package failures does not automatically make the repository scan itself fail.

## 15. Aggregate Statistics

Calculate aggregates only from successfully measured dependencies:

- cumulative libyears
- arithmetic mean
- median
- maximum

If zero dependencies are measurable:

- cumulative libyears is `0.0`
- mean is `null`
- median is `null`
- maximum is `null`

Individual dependencies should be sorted from highest libyears to lowest in human-readable output.

Aggregate values MUST NOT silently include unmeasurable dependencies.

## 16. Unmeasurable Reasons

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

Reason identifiers are part of the machine-readable contract.

Human-readable output SHOULD translate identifiers into understandable explanations rather than requiring users to know their internal meaning.

For example:

`non_exact_version`

may be displayed as:

`exact version not available`

## 17. JSON Output

JSON is intended for automation and SHOULD remain factual rather than advisory.
The current stable machine-readable contract is schema version 3. The v2 to v3
change is intentional.

The top-level object includes `schema_version`, `metric`, `dependency_scope`,
`ecosystems`, ecosystem-keyed `version_evidence`, `summary`, `dependencies`,
`unmeasurable`, and `source_errors`. `summary` contains repository-wide
statistics and `by_ecosystem` with the same statistic fields. Discovery failure
is represented by null counts and coverage, never by zero. `source_errors`
contains source-level failures; dependency-level failures remain in
`unmeasurable` for the existing scalar projection. Maven has its own plural subtree
and deliberately unavailable legacy projection, as specified below.

Each measurable or unmeasurable dependency carries its `ecosystem`. Measurable
dependencies carry `version_source`; Python values remain `requirements_exact`
and `resolved_snapshot`. npm uses `package_lock`. Python evidence is nested
under `version_evidence.pypi`; npm evidence is nested under
`version_evidence.npm` and identifies `package.json` and `package-lock.json`.

A malformed npm manifest produces a source error with ecosystem `npm`, source
`package.json`, and reason `invalid_manifest`, without synthetic npm rows.
Successful measurements from another ecosystem remain in the report.

Do not make JSON consumers parse human-oriented strings. Human-oriented
diagnostics SHOULD NOT be added to the JSON schema merely to improve CLI
presentation. Verbose registry diagnostics do not add fields to JSON.

## 18. Human Output

Human output is intended to explain both the metric and its measurement quality.

When measurable dependencies exist:

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
  flask >=2.0    exact version not available
```

When dependencies are discovered but none are measurable:

```text
Libyears: .

Dependencies discovered: 7
Dependencies measured:   0
Coverage:                0%

No libyears measurement could be calculated.

All discovered dependencies lack exact versions.
Libyears requires exact dependency versions to produce a reproducible
measurement.

Unmeasurable:
  requests              exact version not available
  pygal                 exact version not available
  pandas                exact version not available
  pytest                exact version not available
  pylint                exact version not available
  urllib3 >=2.6.3       exact version not available
```

When no supported dependencies are discovered:

```text
Libyears: .

No supported dependencies were discovered.

Supported ecosystems:
  PyPI

No libyears measurement was calculated.
```

Exact whitespace, table formatting, and line wrapping are not part of the stable API.

## 19. Human Diagnostic Principles

Human output SHOULD answer these questions without requiring the user to inspect JSON:

1. Did the scan find dependencies?
2. How many could actually be measured?
3. Why could the others not be measured?
4. How trustworthy/complete is the aggregate metric?
5. What repository evidence would make the measurement more complete?

Diagnostics SHOULD be concise.

The CLI SHOULD NOT:

- dump internal exceptions during ordinary measurement failures
- imply that an unmeasurable dependency is erroneous
- imply that an old dependency is vulnerable
- recommend upgrading solely because a dependency has high libyears
- resolve dependencies merely to improve coverage

Where useful, the CLI MAY provide neutral next-step guidance such as:

`Exact versions may be available in a supported lockfile or exact-pinned dependency file.`

Guidance MUST NOT imply that users should pin dependencies solely to satisfy the metric.

## 20. Exit Codes

- `0`: scan completed, including:
  - successful measurement
  - partial measurement
  - zero measurable dependencies
  - no supported dependencies discovered
- `1`: CLI usage or filesystem/path error
- `2`: systemic scan failure

Individual registry lookup failures do not cause a nonzero exit code if the repository scan itself completes.

Measurement coverage is data, not process success.

Therefore:

`coverage == 0`

does not imply:

`exit != 0`

## 21. Testing Philosophy

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
- unconstrained dependencies
- ranged dependencies
- unsupported VCS dependencies
- unsupported local dependencies

Metric arithmetic should be tested independently of HTTP and requirements parsing.

CLI tests SHOULD additionally cover:

- no dependencies discovered
- dependencies discovered but zero measurable
- partial measurement
- full measurement
- human-readable explanations for unmeasurable reasons
- zero coverage still returning exit code 0
- JSON remaining unchanged by human-output diagnostics

## 22. Reproducibility Policy

A libyears result SHOULD be reproducible from:

1. repository dependency evidence
2. package-registry release metadata

The tool MUST NOT improve apparent measurement coverage by silently introducing a third source of state such as:

- the caller's installed environment
- a newly created virtual environment
- a freshly resolved dependency graph
- globally installed packages

When repository evidence is insufficient, report that insufficiency.

Prefer missing data over invented precision.

## 23. Security Boundary

Static repository analysis is preferred over executing project tooling.

The tool SHOULD NOT need to:

- execute repository code
- install repository packages
- execute package build scripts
- import the analyzed project
- create a virtual environment

Registry access should consist of metadata retrieval only.

This boundary is intentional and should be preserved as ecosystem support expands.

## 24. Future Milestones

Not part of MVP:

- filesystem metadata cache
- `pyproject.toml`
- `uv.lock`
- Poetry lockfiles
- pip-tools / compiled requirements
- constraints files
- environment markers
- requirements file inclusion
- Maven retained-selection readers and broader model support beyond Feature007
- Go
- Cargo
- transitive dependencies
- SBOM input
- private registry adapters

Each should be implemented as an independently testable extension without changing the core metric model.

When a second ecosystem is implemented, revisit the existing PyPI-specific orchestration boundary and introduce only the minimum abstraction justified by two concrete ecosystem implementations.

## 25. Future Input-Source Principle

Future dependency-source support should distinguish between:

### Declaration sources

Describe desired or acceptable dependencies.

Examples:

- unconstrained `requirements.txt`
- version ranges in `pyproject.toml`

These are useful for dependency discovery but may not establish measurable versions.

### Resolution sources

Record exact versions selected for a repository/environment.

Examples may include:

- lockfiles
- compiled/frozen requirements

These are preferred when establishing the "used version" for libyears.

Adding support for a new file format MUST explicitly define whether that source provides:

- dependency discovery
- exact version evidence
- or both

The tool MUST NOT assume that every dependency manifest is a resolution artifact.

## 26. Current ecosystem extensions

npm scope and package-lock v2/v3 behavior are defined by approved
[Feature 002](specs/002-npm-support/spec.md); Yarn Classic evidence and lock
conflicts follow [Feature 003](specs/003-yarn-lock-evidence/spec.md). npm scope
remains root package.json dependencies excluding optionalDependencies names.
Python snapshot behavior and existing registry policies remain unchanged.

RubyGems follows the approved [Feature 004](specs/004-rubygems-support/spec.md).
Without a group request, directory scans read only root Gemfile.lock, without
requiring or inspecting Gemfile. Direct-file scans remain Python-only. Every
DEPENDENCIES name counts,
including bundler/tzinfo-data without selected specs. This is all-direct locked
snapshot scope, with no group interpretation or certification of commit status,
current Gemfile, installed environment, or runtime compatibility.

The bounded format supports GEM, DEPENDENCIES, required nonempty PLATFORMS,
optional BUNDLED WITH and RUBY VERSION, and inert GIT/PATH envelopes for source
isolation. Unknown fields/sections (including CHECKSUMS, CONTENT ADDRESSES and
PLUGIN SOURCE) reject the source. Malformed supported structure precedes
unsupported format. No partial scope is salvaged from a rejected lock.

Only independently established literal public RubyGems.org authority permits
lookup. Private/GIT/PATH/multiple-remotes/explicit pins cannot fall back to a
public namesake. Exact lock identities and selected version text are preserved;
registry identity permits ASCII case differences only after source authority.
Supported requirements are retained without evaluation. Distinct agreeing
platform artifacts establish one version with provenance; duplicate artifacts
or differing versions are ambiguous. Host platforms never select evidence.

Canonical publication is the earliest admissible authoritative creation timestamp
across supported observable artifacts, including observable yanked contributors,
independently of locked platforms. Identifiable unsupported ABI classes are
excluded; unsafe identity or contradictory metadata fails closed. Missing/invalid
and 2009-07-25 UTC timestamps are excluded individually; built_at never supplies
a fallback. Latest requires currently available stable evidence and a canonical
date; select greatest date then ascending exact-version text. Used and latest
share canonicalization and existing metric arithmetic, including exact 0.0 for
the same version. Observable history is incomplete: absence proves neither yank
nor never-existence, and disappearing records may change future measurements.

Schema v3 adds version_evidence.rubygems with declaration_source and
snapshot_source Gemfile.lock, format gemfile_lock (null for whole rejection),
scope all_direct_locked and publication_basis
earliest_admissible_supported_observable. Ruby rows use ecosystem rubygems and
version_source gemfile_lock. Their rubygems_evidence contains selected_artifacts
(version/platform/public source) and established used_publication_artifacts /
latest_publication_artifacts (version/platform/UTC publication_time, plus yanked
only when known). Failures retain material safely known artifacts and original
direct text; unavailable publication populations are omitted. Human diagnostics
are excluded from JSON, including with --verbose.

Ruby whole-source errors use source_errors with source Gemfile.lock and null
per-Ruby counts, coverage and numeric aggregates. Local/registry dependency
failures use unmeasurable and preserve known scope and available measured count.
Repository unknown denominators or rejected sources null coverage while retaining
successful rows and aggregates. Every detected source unavailable makes repository
measured count null; otherwise it is successful row count, including zero.
Absent sources are omitted. Empty valid scope has 0 discovered/measured, null
coverage, total 0.0 and null mean/median/max. Nonempty wholly unmeasurable scope
has 0% coverage. No-source reports have empty ecosystems/evidence and the same
empty aggregate values. Matching names across ecosystems remain separate rows.

Normal Ruby human output identifies Gemfile.lock, all-direct scope, uninterpreted
groups and observable-history limitations. It distinguishes unavailable coverage
from 0%, preserves direct failure text and safely explains source authority
without revealing remotes or substituting public namesakes. Verbose output may
add safe parser/registry categories. --resolved remains Python-specific; existing
flags and exit categories 0/1/2 remain unchanged. Completed source-error scans
return 0.

Ruby requests are metadata-only to fixed verified HTTPS rubygems.org, rejecting
all redirects and preserving CA precedence/User-Agent. Limits are two requests
per candidate, 16 MiB per response / 32 MiB total, default 10-second timeout,
and at least 0.11 seconds between request starts. Oversize/truncation is
invalid_registry_response; ordinary transport/rate-limit failure is registry_error.
One scan-local adapter enforces Retry-After cooldowns without retries; missing or
invalid Retry-After closes Ruby requests for that scan. Authorized candidates
are scheduled in exact name/version lexical order. Static scans never execute
Ruby/Bundler/Gemfile/gemspecs, install, resolve, inspect private credentials,
fetch private content/archives, or modify the target.

### Explicit Ruby declared-group scope (Feature 005)

The approved [Feature 005 specification](specs/005-gemfile-group-scope/spec.md)
S1–S4 is canonical for activation, the exhaustive static subset, association,
failure precedence and additive schema-v3 fields. It supersedes the all-direct
policy above only when repeatable `--ruby-group GROUP` is explicitly requested:

```bash
python -m libyears PATH --ruby-group default --ruby-group test
python -m libyears PATH --ruby-group default --ruby-group test --json
```

PATH MUST be a directory. Only its exactly named root Gemfile/Gemfile.lock
participate, within the supplied root; no recursive/parent search, includes,
gemspecs, config or environment-derived membership. Direct-file scoped requests
are usage errors. Group names are exact case-sensitive ASCII symbol names
without the colon (`[A-Za-z_][A-Za-z0-9_]*`). Each occurrence supplies one name;
comma lists, malformed/missing values and abbreviated option spellings reject.
Repeated names deduplicate; multiple names select the union once per dependency.
Default membership is implicit for ungrouped gems, but selection of default is
explicit. Explicit top-level gem groups replace default; block/option groups
union. Empty blocks establish groups. Optional flags and require options do not
change membership. Production has no special meaning. With no request, preserve
ordinary all-direct lock behavior without reading Gemfile; Python/npm/Yarn
behavior and Python-only --resolved remain unchanged.

The closed conservative subset permits literal source/gem/group/end forms,
bounded literal requirements and recognized literal group/groups/require options,
comments and one statement per physical line. Complete-file recognition is
mandatory. Unsupported/ambiguous constructs anywhere, even in unselected groups,
reject all scope; no partial rows are salvaged. Duplicate declarations, nesting,
conditions, interpolation/escapes, platform/source blocks, path/git options and
arbitrary Ruby are outside the subset. This does not assert invalid Ruby.
Limits are 1 MiB Gemfile, 16 KiB physical lines and 16 MiB scoped lock. Safe
contained regular-file access is required; unsupported capabilities fail closed.
Never execute Ruby/Bundler/project code, install/resolve, inspect credentials or
configuration, fetch archives/private content or modify targets.

Gemfile establishes the selected declaration denominator, never exact versions,
even for pins. Measurement requires an exact direct lock identity, independent
public authority for both files, identical supported textual requirements and
supported exact lock selection. No transitive/public-namesake fallback is allowed.
Requirement comparison joins declaration literals in order with `, `, with none
as null; it infers neither satisfaction nor equivalence. Mismatch counts once as
unmeasurable (`declaration_lock_requirement_mismatch`), retaining both safe values
without exact-version artifacts or lookup. Existing publication/metric policy
remains unchanged.

Scoped schema-v3 evidence always names Gemfile/Gemfile.lock, scope
`selected_declared_groups`, sorted unique requested_groups and the existing
publication_basis. Format is gemfile_lock only after whole-lock acceptance,
otherwise null. Rows add gemfile_evidence: full sorted declared_groups, ordered
declaration_requirements and lock_requirement only when safely known (null for
known absence; omitted for missing or unsupported evidence). Authorized measured
rows retain version_source gemfile_lock and Ruby artifact provenance. Unsupported
lock requirement text and raw source/private values MUST NOT be echoed; safe
declaration metadata remains. Ordinary JSON omits scoped additions; verbose
human diagnostics remain outside JSON.

Gemfile/unknown-group source failures leave unknown denominator and prevent lock
processing. Rejected locks retain known selected N, null Ruby measurement/coverage
and numeric aggregates, with no rows. Missing locks with N>0 yield N unmeasurable
lockfile_missing rows, M=0 and 0% coverage. Empty scope with absent/accepted lock
has 0/0, null coverage, total 0.0 and null mean/median/max. Dependency failures
retain the denominator; successful ecosystem siblings survive unavailable Ruby
sources under existing repository summary rules. Completed evidence failures
exit 0; request/path errors exit 1; systemic failures exit 2.

Human output names selected declared groups, supplied files, safe memberships
and requirements, recognition state and coverage distinctions, consistently with
JSON. Results are bounded supplied-file claims: no installed/deployed/runtime
scope, compatibility, historical coherence or complete-publication-history claim.
The [release-validation record](specs/005-gemfile-group-scope/release-validation.md)
indexes deterministic acceptance separately from required future explicitly
authorized real-root evidence and optional separately authorized live smoke.

### Explicit NuGet selected-version snapshots (Feature 006)

Current ordinary directory behavior is governed by the independently approved
[repository-source correction](maintenance/nuget-repository-sources/spec.md),
[plan](maintenance/nuget-repository-sources/plan.md) and
[review record](maintenance/nuget-repository-sources/reviews.md). It supersedes
Feature006's explicit-only activation and the prior human-only
[root recognition](maintenance/nuget-root-recognition/spec.md), preserving their
frozen historical artifacts. Ordinary human/JSON scans automatically attempt all
bounded independently admissible projects: depth0–4, 256 directories/10,000 entries/
100 candidates; existing hidden/named exclusions, no link/reparse traversal.
Depth5 is intentionally excluded; incomplete/unavailable discovery makes the
population unknown. Direct-file and explicit selection bypass this discovery.
Each source is independently attributable by root-relative project identity;
external direct PackageReference occurrences count separately across projects.
No package deduplication, solution population or ProjectReference aggregation.
All supported direct test/tool/analyzer/PrivateAssets references remain included.

Repeatable exact --nuget-witness PROJECT=NAME.json explicitly accepts per-project
supplier testimony in ordinary mode. Exactly one equals delimiter; neither operand
contains equals. PROJECT is exact root-relative POSIX identity with no empty/dot/
dotdot/absolute/glob/control/backslash components; NAME.json is immediate in that
project's parent, never packages.lock.json. Duplicate mappings and mixing with
explicit selection or direct-file paths are usage errors before input reads.
Unmatched mappings produce nuget_witness_project_missing/unknown population;
failed discovery instead reports nuget_discovery_incomplete/unavailable, with no
invented mapping errors. No implicit witness acceptance occurs; the prospective
evidence cascade below governs measurement admission.

The approved [Feature 006 specification](specs/006-nuget-selected-evidence/spec.md),
[plan](specs/006-nuget-selected-evidence/plan.md) and
[tasks](specs/006-nuget-selected-evidence/tasks.md) retain historical/base NuGet
contracts. The approved [evidence cascade](maintenance/measurement-evidence-cascade/spec.md)
prospectively supersedes mandatory event/content gates for version-age measurement. The
[ecosystem workflow](ECOSYSTEMS.md#explicit-nuget-project-snapshots) documents the exact
witness schema, supported inputs and enforced numeric limits. This extension
does not change Python/npm/Yarn/Ruby policy or the 365.25-day metric.

Exact directory-only `--nuget-project NAME.csproj` selects one immediate source
and bypasses ordinary repository discovery. Optional
exact `--nuget-provenance NAME.json` accepts the supplied producer/supplier
assertions; no found witness is implicitly trusted. Both occur at most once.
Witness-only, repeated/abbreviated flags, non-filename/path/glob/list values,
direct-file PATH and invalid roots fail usage before source content is read.
Missing explicitly selected projects instead yield completed source-error reports.
Explicit selection adds no other projects. Solutions/references supply no
population authority and portfolio scope remains excluded.

Declaration-first A static scope is one supported namespace-free UTF-8 SDK-style project,
one unconditional literal framework, and all immediate unconditional literal
Include/Version PackageReferences, including test/tool/analyzer/PrivateAssets.
Duplicate case-insensitive IDs, conditions, version children/overrides,
Update/Remove, imports, generated/central influences, multiple TFMs and RIDs
reject scope. Project/Framework references and implicit SDK packages are excluded,
without following reference content. Only two-to-four-component canonical numeric
minimum requests are supported. A request is never an exact-version fallback.

Root packages.lock.json schema integer 1 must contain exactly that framework.
Direct selection is associated only with a unique same-ID declaration and a
canonical normalized minimum request: `1.0` maps to `[1.0.0, )`, zero revision
is omitted and nonzero revision retained. Different minimums disagree even with
the same resolved selection. Missing Direct/version and unsupported selected
strings are isolated failures; duplicate identities, non-string selections,
unknown semantic fields and extra contexts reject the entire lock. Transitive
and Project entries provide closure framing, not measured population.

The measurement floor requires attributable supported direct population, exact
project/lock selection with request/context/byte binding, applicable public
namespace before lookup, and authoritative identities/dates. Event acquisition,
content correspondence, reproducibility and deployment are distinct stronger
claims; a number establishes none of them by itself. Use the strongest available
accepted evidence and retain its facts, but require only the age claim's floor.

Version1 retains native NuGet provenance plus contemporaneous producer testimony,
its exact byte/context/producer/SDK/baseline bindings and replay prohibition.
Its accepted canonical public-origin assertion supports namespace authority.
Local decoded lock/witness SHA512 and public catalog comparisons enrich assurance;
absence/disagreement alone no longer blocks age with independent namespace and
selection. Known private/unknown/conflicting namespace still blocks all lookup.

Version2 explicitly accepts later retained snapshot association and package-specific
namespace testimony. Exact fields: version2, project/framework/project_sha256/
lock_sha256/coherent_snapshot; baseline sdk, explicit_population_complete and
three unsupported influence booleans; packages with id/version/namespace. It omits
producer, sdk_version, origins and content_hash, retaining the same complete
framing, byte/context/completeness checks and input bounds. Namespace is exactly
canonical https://api.nuget.org/v3/index.json, never inferred from public existence,
configuration, hashes or discovered files. See [the ecosystem guide](ECOSYSTEMS.md#explicit-nuget-project-snapshots) for exact templates.
Unsupported population influences invalidate N; stale/malformed whole evidence
retains independently known N with unavailable measurement. No v1/v2 merge repairs
contradictions. Lock Direct population alone is never acceptance authority.
The separate approved [snapshot-population correction](maintenance/nuget-snapshot-population/spec.md)
adds explicitly accepted B2 after unsupported well-framed A, through a selected v3
witness. The later [qualified repository correction](maintenance/nuget-repository-snapshot/spec.md)
adds ordinary-mode B1 before B2: choose the exact current pair by policy after whole
schema1/sole-context/Direct validation, unambiguous immediate-project attribution,
strict unconditional literal extraction and FULL bidirectional ID/normalized-request
equality. Relevant unextractable facts make B1 unavailable; unrelated syntax remains
uninterpreted. Known current conflicts are terminal across ordinary B routes.
No A grammar expansion, complete evaluated semantics or historical production
inference occurs. Dirty/copied/non-Git coherent current pairs qualify without Git.
B1 optional explicitly accepted v3 retains supplier association/scope and namespace;
invalid supplied testimony refuses measurement with B1 N retained. No testimony
means known B1 N; ordinary comparator admission is now separately governed below.
Explicit precision mode preserves its A/B2 contract. A retains v1/v2 baseline gates; v3 on A refuses with known N and unavailable
measurement. No fallback after A establishes population or after its later gates fail.

V3 exact keys: version3, project, framework, project_sha256, lock_sha256,
coherent_snapshot, explicit_external_direct_complete, packages. Both booleans must
be true; exact current supplied bytes/name/sole lock framework must bind. The
assertion establishes the complete explicit external Direct set for the accepted
retained snapshot, not complete/current evaluated declarations. No A baseline/
SDK-import completeness proof or producing event is required by B. Whole schema1
lock framing, supported requests/selections for every Direct, duplicate refusal
and known literal framework/ID/request contradiction checks precede B count/rows.
Malformed/unsafe/limit/DTD project input cannot fall back. Transitive/Project and
implicit SDK references are outside the accepted explicit scope. Same-byte imported
or environment drift is not detectable; no evaluated currentness claim follows.

Packages uses existing v2 id/version/namespace records. Empty is valid and grants
zero public capability. Unknown/private/conflicting namespace fails per occurrence
after whole B acceptance; public namesakes never repair it. Existing dates/worker/
occurrence/metric/aggregation rules remain unchanged. Additive schema3 source/row
population_basis is declaration_derived, qualified_repository_snapshot,
resolved_snapshot or unknown; snapshot source
population_limitations and supplied_snapshot_population_assertion trust_basis
identify retained snapshot limits independently of assurance/namespace. Human
output marks B concisely; verbose/JSON inspects limitations. No acquisition,
content correspondence, deployment, restore/reproducibility or current evaluated
completeness claim; no target/producer execution or automatic namespace
acceptance. B1 trust_basis repository_snapshot_policy and fixed limitations identify
policy selection; accepted v3 retains supplied_snapshot_population_assertion.
Namespace and stronger assurance remain distinct from population basis. See [the ecosystem guide](ECOSYSTEMS.md#explicitly-accepted-resolved-snapshot-fallback-b2) for the v3 format and complete correction for refusal rules.

Complete SemVer-2 registration determines greatest currently listed stable by
numeric precedence, independently of request/framework/date compatibility.
Supported selected/public spellings normalize two-to-four numeric components,
leading zeros, omitted patch/zero revision, ignored build and case-insensitive
prerelease identity. Used prerelease/unlisted versions may measure. Only aware
catalog PackageDetails `created` supplies first nuget.org receipt, normalized
UTC with up to seven fraction digits truncated to microseconds. Missing, naive,
invalid, sentinel-1900 or conflicting dates never use published/commit/local time
or an older dated comparator. Missing records are not reconstructed from archives.
Used=latest is exactly 0.0; negative deltas clamp to zero and remain flagged.

Schema 3/direct scope is retained. Explicitly selected NuGet adds required
version_evidence.nuget source keys (including null witness/framework/format where
specified), packages_lock version_source on measured rows and staged safe
nuget_evidence on measured/unmeasurable rows. Unmeasurable rows retain name,
declared and reason without version_source.
Only established requests, original/normalized selection, authority/hash states
and UTC version/created/listed publications appear; request mismatch claims no
selected provenance. Source errors and dependency failures remain distinct.
Human reporting consumes the same typed facts, explains supplier/snapshot and
publication/comparator limits, and preserves anomaly flags. Raw XML, witness,
origins, hashes, baseline, unsafe paths and diagnostics are never disclosed;
NuGet-active root headers are abstracted and raw verbose diagnostics omitted.
Admitted rows add measurement_basis bound_snapshot_namespace, namespace_basis
accepted_producer_origin or accepted_snapshot_namespace, and an assurance object
with producer_event, local_content, public_content and limitations. V2 has
unavailable acquisition origin/content states plus separate accepted namespace;
v1 retains its literal origin/hash meanings and producer-event assertions.
Public content verification still requires the original successful comparison
chain. Missing/mismatched content does not imply a namespace conflict by itself.
Source trust_basis names the requested producer or snapshot assertion contract.
Human default is concise; verbose/JSON exposes detailed facts and limitations.
Reports without NuGet sources remain unchanged; verbose JSON is identical.
Ordinary mode adds top-level nuget_sources entries (source_id, existing per-source
version_evidence, existing nullable summary, measurement_available). Root-relative
source_id is also added to ordinary NuGet rows and source errors; discovery-wide
failure uses null. Per-row project stays the immediate witness-bound filename.
The selected-only version_evidence.nuget singleton is omitted in ordinary mode;
other ecosystems and explicit output retain existing shapes. Failed/empty sources
are retained, equal basenames are distinct, and no representative is selected.
All occurrences enter existing arithmetic independently. One supervised metadata
batch shares all scan budgets across sources; repeated equal capabilities retain
independent results. Per-source summaries compose known/unknown N and any/all
availability without overwriting sibling facts.

For each individual NuGet source (also the explicit single-source report), unknown
population yields null counts, coverage and numeric aggregates. Known N with
rejected lock/witness retains N, even zero, but null measurement, coverage and
numerics without fabricated rows. Accepted nonempty populations
use M/N including zero coverage; accepted empty uses 0/0, null coverage, total
0.0 and other numerics null. Repository discovered is unknown if any denominator
is unknown; coverage is unavailable if any source is unavailable; measured is
null only when every detected source is unavailable. The combined NuGet summary
likewise has null N/coverage if any project population is unknown, but retains
measured count and numeric aggregates from available sibling projects; M and
NuGet numerics are null only if all NuGet sources are unavailable. Available sibling rows and
repository numeric aggregates survive all NuGet failures.

Finite local bounds reject complete sources without partial salvage. Metadata
limits reject incomplete latest rather than truncate. Verified HTTPS uses only
fixed api.nuget.org index/SemVer-2 registration and validated linked catalog
paths, with zero redirects/retries, bounded incremental gzip and rate-limit
suppression. The installed isolated trusted Python metadata helper is the sole
new process: no dotnet/NuGet/MSBuild/target/package-manager execution, evaluation,
restore/install/resolution, archive or private-content access occurs. Parent
absolute 60/300-second package/metadata-scan budgets cover blocking I/O and
parsing, reserve 0.5 seconds for bounded terminate/kill/reap, reject cutoff results
and suppress remaining requests after cancellation. Startup/OS scheduling is not
a hard real-time whole-CLI guarantee; unreaped workers are systemic failures with
deferred cleanup. Worker verified trust uses shared defaults, without forwarding
the explicit --ca-bundle argument. Source readers refuse hosts lacking required
descriptor-relative/no-follow/nonblocking primitives, independently of successful
POSIX/Windows worker lifecycle evidence.

Completed empty/partial/source-error reports exit 0, request/path errors exit 1,
and unexpected systemic failures exit 2. NuGet argument/exception/rendering errors
use fixed safe messages. Snapshot assertions do not establish evaluated scope,
runtime compatibility, current restore or cryptographic provenance. Useful live
yield and hash-domain fitness remain unverified; real-root validation requires
separate explicit target/network authority. Assets/exports/packages.config,
general MSBuild/CPM, private feeds and portfolio aggregation remain out of scope.

## Ordinary NuGet conventional comparator correction

The approved [comparator contract](maintenance/nuget-conventional-comparator/spec.md)
supersedes ordinary namespace admission above. It permits a deliberately conventional
nuget.org reference after supported bounded repository inspection finds no contrary
assignment or unsupported package-specific ambiguity. Correspondence is assumed by policy, not established;
external configuration, acquisition/content/producer/evaluated/deployed state remain
unestablished. The subsequent human-approved
[positive-contrary correction](maintenance/nuget-positive-comparator/spec.md) permits
unassigned alternate/local source eligibility alone: it is acquisition policy, not
private comparator assignment. Undisclosed private namesakes/forks may receive the
wrong public history; public queries disclose their IDs. These residual metric
risks are explicitly accepted, not proof of public identity. Exact accepted testimony, then closed unique public mapping,
then convention apply only absent stronger contradictions/unknown relevant syntax.
No public namesake grants capability. Private/unknown occurrences make no HTTP call.

Ordinary no-witness A additionally may qualify a uniquely attributable current pair
under B1-strength whole-lock/ID/request/framework/selected identity checks, retaining
declaration_derived and explicit missing supplier baseline limitations. No baseline
or witness is synthesized; stronger accepted witness and precision routes retain
meaning. Schema3 ordinary rows add comparator_basis and fixed conventional
comparator_limitations; policy namespace/measurement values remain distinct from
testimony. Metric, stable/date policy, worker/transport budgets and sibling semantics
are unchanged. See C1–C6 for exact bounded grammar, refusal and precedence rules.


## Maven plural dependency-age views (Feature 007)

The approved [Feature007 specification](specs/007-maven-dependency-age/spec.md),
[source policy](specs/007-maven-dependency-age/source-policy.md),
[latest policy](specs/007-maven-dependency-age/latest-policy.md#selected-policy--run007-0008)
and [metadata contract](specs/007-maven-dependency-age/metadata-contract.md) govern
this extension and supersede original MVP single-view/release-date assumptions for
Maven only. [Deterministic verification](specs/007-maven-dependency-age/verification.md)
records conformance and the still-pending separately authorized operational witness.

Ordinary directory scans discover bounded regular pom.xml sources with no Java
flags; direct files do not activate Maven. Each consuming source owns independent
supported static base-model external direct occurrences. Local parent/field/property/
management facts are bounded, profiles are not activated, BOMs are not read/fetched,
and internal exclusion requires exact GAV in an unambiguous static aggregation.
Test/provided/optional/tooling/ordinary-POM rows count; plugins/management/transitives
do not create population. Type/classifier model keys and artifact aliases stay separate.
Repeated modules weight totals independently. Unknown relevant syntax refuses at the
smallest dependent scope, masking unsafe same-key inherited fallback; safe siblings
survive with honest unknown population. No target tooling executes.

Declared records use supported_local_base_model_request, an exact request fact rather
than selection. Observed would require bound retained_dependency_system_selection;
there is no accepted Maven reader/option initially. Both views have independent
populations, availability, coverage and seven statistics. Missing Observed is all-null,
never copied or replaced by Declared/Gradle/effective-POM/runtime data. Model-only
paired differing-version capacity creates no new intake.

After local contrary checks, conventional_central assumes correspondence; alternate/
file eligibility alone does not veto it. Supported system assignment, Central
exclusion/redefinition/block, identity conflict and relevant unknown policy refuse
before lookup. Only fixed verified HTTPS public GA metadata/exact versioned POMs are
permitted; no auth/proxy/redirect/archive/private/parent/BOM/provider route follows.
A trusted installed isolated Python worker enforces closed commands, budgets and
bounded cleanup with no restart/fallback. Missing native safety capabilities or TLS
trust leaves evidence unavailable. An explicit CA bundle is staged privately;
Maven honors no ambient CA/proxy settings or pip/Maven configuration fallback.

Maven time_basis is maven_conventional_pom_last_modified: the public repository's
reported modification time for each versioned POM representation, used as an
explicit conventional release-age surrogate. It is not first publication/upstream
release or acquired bytes/classifier/runtime history. Require exact representation
identity and a unique supported nonfuture Last-Modified. Catalogue retrieval time
is independent freshness, never a replacement version timestamp. Missing either
date is terminal, including same-version zero; no older candidate or fallback field.
Existing365.25-day arithmetic and negative timestamp anomaly clamping remain.

Ordering is pinned maven_comparable_version_3_9_11, separately from
maven_conservative_stable_v1 eligibility: numeric/release-alias/service-pack forms,
known prerelease/snapshot exclusion, unknown strictly below harmless versus unknown
at/above/unorderable refusal, and distinct equivalent maximum-string ambiguity.
The comparison is the global current GA maximum, never compatible-upgrade advice.

Schema3 adds version_evidence.maven (plural mode/static scope/no Observed reader)
and maven.discovery/sources/occurrences/views. Structured source/context/model and
artifact keys retain nullable request/version/origins/availability/reason/age.
Ages expose comparison_version, libyears, timestamp_order_anomaly, separate bases/
ordering/eligibility, measured_version_pom_last_modified,
comparison_version_pom_last_modified, catalogue_retrieved_at and fixed limitations.
Source/views disclose basis/limitations when no row measures; unsafe raw request,
URLs/headers/XML/credentials/absolute roots/hashes are not emitted.

Known accepted N permits M/N including0, with measured-subset total0.0 when M0;
certified empty N=M0 has null coverage/total0.0. Unknown N with safe rows preserves
partial M/statistics with null coverage; no accepted collection leaves M/numerics
null. A whole-unavailable sibling also nulls coverage. Statistics use occurrence
unions, and the two views are never added/subtracted/substituted.

Maven has no legacy scalar projection: per-source maven_plural_projection_unavailable
errors (discovery-level source_id null), all-null Maven by_ecosystem statistics,
and null legacy repository N/coverage. Successful sibling rows/evidence/per-ecosystem
summaries and partial numeric subset remain; every legacy source unavailable makes
M/numerics null. Admitted empty siblings may retain0/total0.0 only as a labeled
incomplete legacy subset. Maven-only legacy counts/numerics are all-null. No Maven
row enters legacy dependencies/unmeasurable or scalar arithmetic. Complete Maven
absence leaves old output unchanged; unknown discovery cannot certify absence.

Human output leads with paired Conventional Maven dependency age and one section
time-basis line. Verbose shows exact dates/bases/origins/limits without raw evidence.
Existing CLI exit categories remain0/1/2. Public coordinate disclosure and undisclosed
private namesake/fork misattribution are accepted limitations; stronger acquisition,
producer/evaluated/runtime claims never follow. Live target validation, private access
and publication remain separate lifecycle permissions, not implied by offline tests.
