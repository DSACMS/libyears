# Ecosystem Guide

This guide explains current dependency evidence, examples and limitations across
supported ecosystems. Start with [README](README.md#quick-start) for first use.
[SPEC](SPEC.md) and the approved feature/correction contracts linked below govern
behavior; this explanation does not create new requirements. Historical decisions
remain in their [retrospectives](#history-and-further-reading).

- [Common measurement model](#common-measurement-model)
- [Reporting and registry access](#reporting-and-registry-access)
- [Python / PyPI](#python--pypi)
- [npm and Yarn Classic](#npm-and-yarn-classic)
- [RubyGems](#rubygems)
- [NuGet](#nuget)
- [Maven](#maven)
- [Cross-ecosystem lessons](#cross-ecosystem-lessons)

## Common measurement model

Every measurement needs a supported chain:

```text
dependency population -> accepted version fact -> applicable public comparator
                      -> admitted ecosystem timestamps -> libyears
```

Population answers what counts; version evidence answers which exact version fact
is established. Maven distinguishes a supported declared request from a retained
dependency-system selection; its Observed reader is initially unavailable.
Neither alone proves public source, acquisition, installed bytes or runtime use.
Evidence mechanics differ by ecosystem. A manifest is not automatically a lockfile,
and a lockfile is not automatically authority for every claim.

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


| Ecosystem | Population | Exact version evidence | Public comparison / date basis |
| --- | --- | --- | --- |
| Python / PyPI | Root requirements.txt (or direct file) | Exact pin or supplied resolved snapshot | PyPI metadata; canonical earliest valid file upload per release |
| npm | Root package.json production dependencies, excluding optional names | Root package-lock v2/v3 or Yarn Classic v1 | npm registry version publication times; not dist-tags.latest alone |
| RubyGems | Root lock DEPENDENCIES; optionally statically selected Gemfile groups | Supported associated Gemfile.lock specs | Independently supported public source; earliest admissible supported observable artifact creation |
| NuGet | Each bounded project independently; declarations or qualified/accepted snapshot | Associated schema1 packages.lock.json Direct records | Accepted testimony, closed public mapping or disclosed ordinary-mode convention; nuget.org first receipt |
| Maven | Independent supported local base-model project occurrences | Declared exact request/property/management facts; Observed initially unavailable | Conventional Central comparison; versioned POM Last-Modified surrogate, not publication history |

Python and npm choose eligible stable comparators by publication time; NuGet uses
greatest listed stable SemVer precedence. Ruby's observable-artifact policy is
explained below. Maven uses pinned Maven precedence and a conservative eligibility
policy; its two views never share a denominator by default. None of these comparators promises compatibility with a project's
requested range or runtime.

## Reporting and registry access

### Measurement coverage

Coverage is the number measured divided by the number discovered. `7 discovered
/ 0 measured` means no dependency age could be calculated; `7 discovered / 7
measured` means the aggregate covers every discovered dependency. Their numeric
totals cannot be interpreted as equivalent, even if both are low.

A source discovery failure and a dependency that cannot be measured are different:
`source_errors` records the former; `unmeasurable` records the latter. Unavailable
coverage is not 0%. A low total with incomplete coverage describes only the
measured subset. [SPEC](SPEC.md#13-measurement-coverage) and the ecosystem sections
below define the exact known/unknown/unavailable cases.

### JSON output

JSON schema version 3 reports ecosystem-keyed version evidence, repository and
per-ecosystem summaries, and source discovery errors separately from
dependency-level failures. Maven adds an independent plural subtree and deliberately
unavailable legacy scalar projection; see [Maven output](#maven-output-and-coverage).
The schema v2 to v3 change is intentional. A
synthetic Python-only example (versions and dates illustrate the format; they
are not a live registry observation):

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

### TLS and enterprise environments

Registry requests use HTTPS with certificate verification enabled. Libyears follows
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

### Verbose diagnostics

```bash
python3 -m libyears PATH --verbose
```

Verbose output can identify certificate verification failures, HTTP failures,
timeouts, DNS/network errors, malformed registry responses, and the selected TLS
trust source. Stable JSON reason identifiers remain unchanged.

NuGet's isolated metadata worker uses the shared verified default trust selection;
`--ca-bundle` is validated but is **not forwarded** to that worker. NuGet-active
reports omit raw verbose diagnostics and TLS paths. See [metadata access](#metadata-access-and-supervision).

Maven's worker uses verified compiled system trust or a privately staged explicit
`--ca-bundle`; it does not honor ambient CA/proxy/auth variables or search pip,
Maven caches or home configuration. Missing trust leaves metadata unavailable.
Readiness issues no request and does not prove TLS or registry availability.

## Python / PyPI

Directory scans read root `requirements.txt`; a direct requirements-file argument
is also supported. Repository declarations define direct scope. Exact pins can
provide versions; unconstrained/ranged declarations need supported exact evidence.
`pyproject.toml`, Poetry/uv locks, includes, constraints and environment markers
are outside current support. The CLI never inspects the active environment to
infer versions. [SPEC](SPEC.md#6-dependency-source-precedence) governs Python policy.

### Exact-pinned requirements

Exact pins in `requirements.txt` can be measured directly:

```text
requests==2.34.2
pandas==2.3.3
```

### Resolved snapshot workflow

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

The `pip freeze` command above is an optional user workflow, not an action libyears
performs. Use an environment whose snapshot is appropriate for the question; a new
freeze cannot prove historical repository state. The supported snapshot is a narrow
list of exact `NAME==VERSION` entries, not a general pip requirements interpreter.

PyPI's canonical timestamp is the earliest valid distribution upload for a release.
Latest stable excludes prereleases, wholly yanked candidates and releases without
usable timestamps, then selects by that canonical timestamp. A used yanked version
can still measure. See [date policy](SPEC.md#9-used-version-release-date).
Python's fixed public lookup does not positively verify the local package namespace;
that limitation is distinct from version selection.

## npm and Yarn Classic

For npm repositories, `package.json` root `dependencies` define direct
production scope, excluding names also declared in `optionalDependencies`.
Root `package-lock.json` versions 2 and 3 or root Yarn Classic v1 `yarn.lock`
provide exact used versions. Yarn evidence requires the canonical v1 header and
an exact textual match between the manifest declaration and a lock selector;
libyears does not evaluate ranges or execute Yarn/npm, install packages, or
resolve dependencies.
Development, peer, optional-only, workspace, and transitive dependencies are
outside this feature. Yarn Berry/v2+, PnP, and workspace aggregation are not
supported. `--resolved` remains Python-specific.

If both root lockfiles exist, neither is used, even if their versions agree:
`source_errors` reports `conflicting_resolution_sources`. Malformed supported
Yarn v1 uses `invalid_lockfile`; unsupported or safely unclassifiable Yarn uses
`unsupported_lockfile_format`. These whole-source failures retain the known
npm declaration count, but npm measured count and coverage are null. Mixed
repository coverage is also null; successful Python measurements and their
numeric aggregates survive. An invalid manifest makes npm counts and coverage
unknown.

Missing, unsupported-source, conflicting, or ambiguous dependency evidence
appears in `unmeasurable`, preserves the original declaration, and reduces
ordinary measured/discovered coverage without blocking other dependencies.
Human output identifies `yarn.lock` evidence and explains source failures.
JSON remains schema v3: Yarn measurements use `version_source: "yarn_lock"`,
and `version_evidence.npm` includes `format: "yarn_lock_v1"` and
`snapshot_source: "yarn.lock"`. Rejected unsupported/unclassifiable formats have
null format; simultaneous lockfiles have null format and snapshot source.
Existing package-lock and PyPI evidence representations are unchanged.

For an ordinary root containing `package.json` and one supported lock:

```bash
python3 -m libyears PATH
python3 -m libyears PATH --json
```

Publication dates come from the registry `time` mapping. Latest stable uses eligible
stable publication timestamps, not `dist-tags.latest` alone. Fixed public lookup
does not positively verify the local namespace. See [npm contract](specs/002-npm-support/spec.md)
and [Yarn evidence contract](specs/003-yarn-lock-evidence/spec.md).

## RubyGems

Without `--ruby-group`, a directory scan recognizes exactly the root
`Gemfile.lock`, even without a Gemfile. All direct dependencies recorded in
Gemfile.lock are counted; groups are not interpreted. The report describes the supplied lock snapshot. It does
not certify committed bytes, current Gemfile contents, installed versions, or
runtime compatibility. In this ordinary all-direct mode, Gemfile is never read.
`--resolved` remains Python-specific; direct-file arguments do not activate Ruby discovery.

The supported bounded section format includes GEM, DEPENDENCIES, required
nonempty PLATFORMS, and optional BUNDLED WITH / RUBY VERSION. GIT and PATH
framing only isolates unsupported dependencies. Unknown fields/sections,
including CHECKSUMS, CONTENT ADDRESSES and PLUGIN SOURCE, reject the source.
This intentionally supports a subset of Bundler locks, not every generation.
No Ruby, Bundler, gemspec, installer, or resolver is executed.

Only a literal `https://rubygems.org` remote (optional trailing slash) supplies
public authority. Private, Git, PATH, multiple-remote and explicitly pinned
sources remain unmeasurable; a public namesake is never substituted. Exact
selected specs establish used versions; requirements are retained without
satisfaction or equivalence checks. Missing specs for direct `bundler` or
`tzinfo-data` remain counted. Agreeing distinct generic/platform artifacts
establish one package version and retain provenance; differing versions or
duplicate artifact rows are ambiguous. No host-platform selection occurs.

Ruby publication dates are the earliest admissible authoritative creation times
across supported observable artifacts, independently of locked platforms.
Missing/invalid dates and all 2009-07-25 UTC dates are excluded; build times are
never a fallback. Latest requires currently available stable artifact evidence
and chooses the greatest canonical date, with ascending exact version text for
ties. These dates are observable evidence, not complete historical knowledge.
Missing public records prove neither yanking nor never-existence. Disappearing
records may change future measurements.

JSON stays schema v3. `version_evidence.rubygems` identifies `Gemfile.lock`,
`format: "gemfile_lock"` (null on source rejection), `scope: "all_direct_locked"`,
and `publication_basis: "earliest_admissible_supported_observable"`.
Ruby rows use `version_source: "gemfile_lock"` and additive `rubygems_evidence`
with selected artifacts and admissible used/latest publication contributors.
Safely established evidence survives dependency failures; unavailable publication
arrays are omitted. Existing Python/npm evidence objects are unchanged.

Whole-lock rejection uses `source_errors`, with null Ruby counts, coverage and
numeric aggregates, and no invented rows. Known direct scope survives local or
registry failures, including total outages, in `unmeasurable`. Other ecosystems'
successes survive. Null coverage means unavailable; valid nonempty scope with no
measurements has 0% coverage. Completed partial/empty/source-error scans exit 0.

Ruby metadata requests use verified HTTPS with the existing CA precedence,
reject all redirects, and allow at most two requests per candidate, 16 MiB per
response (32 MiB total), with a default 10-second timeout. One scan-local adapter
paces request starts at least 0.11 seconds apart and respects 429 cooldowns
without retries. Authorized candidates run in exact name/version lexical order.
No archives or private source content are fetched. See the approved
[Feature 004 specification](specs/004-rubygems-support/spec.md) for the full boundary.

### Select declared Ruby groups

Explicitly select groups with repeatable `--ruby-group GROUP` on a directory:

```bash
python3 -m libyears PATH --ruby-group default --ruby-group test
python3 -m libyears PATH --ruby-group default --ruby-group test --json
```

Names are exact and case-sensitive, using ASCII letters/underscores followed by
ASCII letters/digits/underscores. Supply one name per occurrence, without a
colon or comma list; abbreviations of `--ruby-group` are rejected. Repeated names
deduplicate, and several groups select their union, counting each dependency
once. `default` must be requested explicitly. `production` is an ordinary group
name with no special behavior. Python/npm scope and Python-only `--resolved`
remain unchanged. Without this option, ordinary all-direct Ruby behavior above
is unchanged and Gemfile is not inspected.

Only the supplied directory's root `Gemfile` and `Gemfile.lock` participate;
scoped direct-file arguments are usage errors. There is no parent/nested search,
include, gemspec, configuration or environment-based group discovery. Escaping
symlinks are rejected without reading their targets. Ruby and Bundler are never
executed, and no packages are installed or resolved.

The conservative static subset accepts one top-level literal `source`, literal
`gem` declarations with bounded requirement strings, literal `group:`/`groups:`
options, `require:` values, and nonnested `group :name do` blocks (including
literal optional flags). Ungrouped gems belong to default; explicit top-level
groups replace default, and block/option memberships combine. Optionality and
`require:` do not change declared membership. Complete-file recognition is
required: unsupported or ambiguous syntax anywhere, including an unselected
group, fails closed with no partial population. Conditions, interpolation,
escapes, nested groups, duplicate declarations, platform/source blocks,
path/git options and arbitrary Ruby are rejected. Rejection does not mean the
file is invalid Ruby. See the [approved closed subset](specs/005-gemfile-group-scope/spec.md#approved-closed-static-subset)
for canonical syntax details.

For example, this synthetic supplied Gemfile selects only rack for `default`:

```ruby
source "https://rubygems.org"
gem "rack", "~> 3.0"
group :test do
  gem "rake"
end
```

```bash
python3 -m libyears PATH --ruby-group default
python3 -m libyears PATH --ruby-group default --json
```

Human output includes these lines:

```text
RubyGems selected declared groups: default.
Supplied declaration source: Gemfile; supplied version snapshot: Gemfile.lock.
```

If Gemfile.lock is absent, the selected rack is counted but unmeasurable with
`lockfile_missing`: a declaration pin or range never supplies the exact version.
Its JSON row includes this fragment (the unknown `lock_requirement` is omitted):

```json
{
  "ecosystem": "rubygems",
  "name": "rack",
  "declared": "rack (~> 3.0)",
  "reason": "lockfile_missing",
  "gemfile_evidence": {
    "declared_groups": ["default"],
    "declaration_requirements": ["~> 3.0"]
  }
}
```

Gemfile establishes declaration membership; only independently authorized exact
Gemfile.lock evidence establishes a measurable version. Association requires an
exact direct name and identical supported requirement text. Textual differences
produce `declaration_lock_requirement_mismatch` without version association or
lookup: equivalence is not inferred. Transitive matches cannot substitute.
Public authority must be established independently for both files; nonpublic
sources never use public namesakes.

Schema v3 adds scoped `scope: "selected_declared_groups"`, sorted unique
`requested_groups`, and declaration source `Gemfile` under
`version_evidence.rubygems`. Row `gemfile_evidence` keeps full declared memberships
and ordered safe requirements separate from lock-version/publication artifacts.
`lock_requirement` is null for known absence, omitted for missing or unsafe
requirement evidence, and otherwise safe text. Raw source lines, private URLs
and unsupported requirement text are not emitted. Ordinary scans omit these
scoped additions; `--verbose` does not change JSON.

Unknown groups or rejected Gemfiles make the denominator unavailable. A rejected
lock preserves the selected count but makes Ruby measurement/coverage unavailable,
with a source error and no rows. A missing lock with nonempty known scope yields
unmeasurable rows and 0% coverage. An established empty group with absent or
accepted lock has 0 discovered/measured and null coverage. Successful sibling
ecosystems survive. Completed evidence-error reports still exit 0; malformed
requests/path errors exit 1 and systemic failures exit 2.

Results describe supplied-file declaration membership and lock evidence only.
They establish neither historical coherence nor installed, deployed, runtime
loading or compatibility state. Publication history remains incomplete as above.
Scoped bounds are 1 MiB Gemfile, 16 KiB per physical line and 16 MiB lock; platforms
without required safe file-access capabilities fail closed. The
[Feature 005 contract](specs/005-gemfile-group-scope/spec.md) holds canonical
failure/field rules; [validation evidence](specs/005-gemfile-group-scope/release-validation.md)
separates offline correctness from pending authorized real-root validation.

## NuGet

- [Ordinary discovery and witness mappings](#ordinary-discovery-and-witness-mappings)
- [Ordinary public comparator](#ordinary-nuget-version-age-comparator)
- [Precision interface and v1/v2 witnesses](#explicit-nuget-project-snapshots)
- [Qualified current snapshots (B1)](#qualified-current-repository-snapshots)
- [Accepted snapshots (B2 / v3)](#explicitly-accepted-resolved-snapshot-fallback-b2)
- [Dates and versions](#dates-and-versions)
- [Output and assurance](#output-and-assurance)
- [Availability and safe input](#availability-and-safe-input)
- [Enforced bounds](#enforced-bounds)

Ordinary mode attempts projects automatically and may qualify current project/lock
pairs under disclosed product policies. Explicit single-project mode is a precision
interface with its existing testimony requirements. Do not apply ordinary-mode
conventions to that interface. Population, selection, comparator and stronger
assurance are separate facts.

### Ordinary discovery and witness mappings

```bash
python3 -m libyears PATH
```

A directory scan measures supported root PyPI/npm/Ruby sources and automatically
attempts bounded NuGet project sources below it. Each supported project has its
own direct external dependency population. The same package in two projects
counts as two occurrences, with independent versions and libyears measurements.
ProjectReference edges add no external rows; solutions do not define population.
Test/tool/analyzer/PrivateAssets references remain included. No restore or build runs.

NuGet discovery covers exact lowercase `.csproj` regular files, root depth zero
through four directory levels, at most 256 directories, 10,000 entries and 100
projects. It excludes dot-prefixed directories and exact `bin`, `obj`,
`node_modules`, `packages`, `vendor`, `venv`, `__pycache__`, and follows no
links/reparse points. Deeper subtrees are intentionally excluded. Count overflow,
errors or unavailable safe primitives produce an unknown population, never a
partial denominator or false absence. A complete empty search leaves NuGet absent.
Both human and JSON directory reports attempt these sources. Direct-file scans
and explicit single-project selection bypass repository discovery.

Discovery and locks never confer provenance authority. To explicitly accept a
retained supplier witness for one source, use repeatable mappings:

```bash
python3 -m libyears PATH --nuget-witness src/App/App.csproj=witness.json
```

Each project uses its own parent's `packages.lock.json` and the named immediate
witness there. PROJECT is its exact POSIX root-relative identity; the mapping has
exactly one `=`, with no `=` in either filename. Absolute/dot/dotdot/empty path
components, backslashes, globs, controls and duplicate mappings are rejected.
A valid mapped project absent from bounded discovery is a source error. Mapping
cannot combine with `--nuget-project`/`--nuget-provenance` or direct-file PATH.
A found witness is never accepted automatically; evidence requirements below
still apply. Missing required whole-source evidence preserves a known population
but gives null measurement/coverage. An unsupported project gives unknown
population. Any unknown source prevents repository-wide N/coverage; successful
sibling projects and ecosystems remain visible. No coverage percentage is promised.
Use [explicit selection](#explicit-nuget-project-snapshots) for precision/debugging.

### Ordinary NuGet version-age comparator

For ordinary directory scans, qualified selected versions may use nuget.org as a
**conventional public reference** unless supported bounded repository evidence
establishes a contrary/private comparator, exclusion, conflicting mapping/testimony
or unsupported package-specific source semantics. Namespace correspondence is assumed by this disclosed product policy;
it is not independently established. External user/machine/ancestor configuration
is uninspected. Dates describe nuget.org's history, not package acquisition,
content correspondence, producer history, evaluated state or deployment.

Known private/nonpublic assignment, conflicting testimony, active ambiguous mapping,
unsupported/unreadable relevant policy or source-affecting project/import evidence
blocks public lookup. Enabled alternate/local acquisition sources without package
assignment do not by themselves defeat public comparison; they are neither assumed
private nor assumed public mirrors. An undisclosed same-ID/version private fork
may therefore be compared against the wrong public history, and lookup discloses
the identity to nuget.org. These are explicitly accepted metric limitations. Valid
accepted exact public testimony and closed unique public mapping retain stronger
comparator authority. Otherwise the convention
applies only after supported bounded inspection. Public namesake existence never
authorizes lookup. No alternate/private feed is contacted.

Inspection covers only anchored root-to-project ancestors, case-insensitive
NuGet.Config names and presence of Directory.Build.props/targets/Directory.Packages.props.
The initial safe config subset supports source/disable clear/add/remove and closed
source mapping with exact > longest prefix > wildcard precedence. Unsupported
sections (including credential framing), ambiguous aliases, links and excessive
inputs refuse safely. No imported code or outside configuration is read/evaluated.
Dirty/untracked/non-Git current bytes follow the same rules.

Schema3 ordinary rows add comparator_basis (explicit_testimony, repository_mapping,
conventional_public_policy). Conventional rows disclose their assumptions separately
from population/selection and stronger assurance. Automatic policy dates use
measurement_basis public_comparator_version_age, never accepted testimony labels.
The explicit precision interface retains its existing contract and output shape.
See the [positive-contrary-evidence policy](maintenance/nuget-positive-comparator/spec.md)
and its [base contract](maintenance/nuget-conventional-comparator/spec.md).

### Explicit NuGet project snapshots

For precision/debugging or a single source, select exactly one immediate C#
project. This bypasses ordinary repository discovery:

```bash
python -m libyears PATH --nuget-project Example.csproj
python -m libyears PATH --nuget-project Example.csproj --nuget-provenance witness.json
python -m libyears PATH --nuget-project Example.csproj --nuget-provenance witness.json --json
```

The first command reports unavailable measurement authority. Only explicitly
supplying `--nuget-provenance` accepts that file's producer/supplier assertions;
a conventionally named or co-located witness is never trusted automatically.
Supply accountable retained evidence for the accepted claim; never invent
assertions to make a scan pass. A later snapshot/namespace assertion need not
pretend to be a producer-event attestation. Libyears does not create it by
running dotnet, NuGet or MSBuild.

Both options require their exact spelling, occur at most once, and accept immediate
filenames with the shown suffixes. Paths, globs, filename lists, unsafe characters,
witness-only requests and direct-file PATH arguments are usage errors (exit 1).
The lock is always root `packages.lock.json`. Multiple co-located projects are
allowed because one is selected explicitly; their populations are never combined.
Python `--resolved`, npm/Yarn arbitration and Ruby group selection keep their
existing independent meanings.

#### Declaration-first population and lock selection

Declaration-first population (A) supports one namespace-free UTF-8 SDK-style `Project Sdk="..."` with
one unconditional literal `TargetFramework` or single-valued `TargetFrameworks`.
Count immediate unconditional `PackageReference Include="ID" Version="1.0"`
declarations, including test, tool, analyzer and PrivateAssets references, once
per case-insensitive ID. Requests must be bare two-, three- or four-component
decimal minimums without leading zeros. They are not selected pins. Allowed
ancillary metadata is literal PrivateAssets, IncludeAssets, ExcludeAssets and
GeneratePathProperty, once each. Conditions, imports, generated/central package
management, version children/overrides, Update/Remove, duplicate IDs, multiple
frameworks and RIDs reject scope. ProjectReference/FrameworkReference and implicit
SDK packages add no measured dependencies; referenced content is never traversed.

Only lock schema integer `version: 1` with exactly the project's literal framework
is supported. Direct entries provide selection; Transitive/Project entries frame
closure but never enlarge scope. Duplicate JSON identities, non-string selections
and unknown semantic fields reject the whole lock. A declaration `1.0` requires
lock `requested: "[1.0.0, )"`; `1.2.3.0` requires `[1.2.3, )`, while `1.2.3.4`
retains its fourth component. Different minimum bounds disagree even with identical
resolved outcomes. Only `resolved` supplies the exact version; there is no range
solver, satisfaction check, assets/export or package-list fallback.

#### Version-1 producer-event witness

The stronger version-1 witness remains strict UTF-8 JSON with these fields:

```json
{
  "version": 1,
  "project": "Example.csproj",
  "framework": "net10.0",
  "project_sha256": "<64 lowercase hex digits for exact project bytes>",
  "lock_sha256": "<64 lowercase hex digits for exact lock bytes>",
  "producer": {"name": "supplier", "version": "1"},
  "coherent_snapshot": true,
  "baseline": {
    "sdk": "Microsoft.NET.Sdk",
    "sdk_version": "10.0.100",
    "explicit_population_complete": true,
    "unsupported_membership_version_influences": false,
    "unsupported_framework_rid_influences": false,
    "unsupported_source_influences": false
  },
  "packages": [{
    "id": "Example.Package",
    "version": "1.0.0",
    "content_hash": "<standard base64 of the 64-byte SHA512 value>",
    "origins": ["https://api.nuget.org/v3/index.json"]
  }]
}
```

Replace placeholders only with established evidence. The baseline asserts that
SDK/imported/generated/ancestor/central inputs add no unsupported population,
version, framework/RID or source influences. SDK identity must match the literal
project Sdk. Exact byte digests bind the project and lock without newline repair;
mtime, Git presence or equal package names/versions cannot establish coherence.
Unknown/duplicate fields or package identities are rejected. Each origin record
binds its ID, normalized selected version and hash to that envelope. A missing,
private, alternate or conflicting origin causes an individual failure without
querying a public namesake. Only the singleton canonical public URL above permits
lookup. Decoded lock/witness SHA512 comparison and public catalog hash
comparison enrich content assurance; missing or mismatched content evidence no
longer blocks age when selected version, context and applicable namespace hold. In this explicit precision interface, no archive,
cache, NuGet.Config, source mapping or credential lookup repairs missing evidence.

The historical H3 event route, retained by version 1, requires two bound evidence classes: **native NuGet package provenance** from
the producing operation establishes package identity, selected version, actual
supplying origin and content hash; **contemporaneous producer attestation** binds
that evidence to the same event, exact project/lock bytes, framework and required
baseline/input-influence assertions. Retain independently auditable evidence for
both classes and their linkage. In the unchanged version-1 witness, `packages`
carries native-derived assertions; context/digests, `producer`,
`coherent_snapshot` and `baseline` carry the accepted attestation.

Retrospective replay does not substitute for producer attestation of the original
event. A new production event may qualify with its own contemporaneous attestation;
it cannot establish historical provenance. Later serialization may preserve an
existing attestation, but cannot create missing event-time testimony.

These are accepted supplier assertions, not authenticated producing history.
Matching supplied lock/witness/public hashes establish their content correspondence;
libyears does not read installed package bytes. The snapshot does not prove
evaluated MSBuild completeness, successful restore, installed/deployed/runtime
scope or compatibility. For this stronger event/content route, live measurement yield and signed-content
hash-domain fitness remain unvalidated; this does not describe the separately
validated ordinary conventional comparator. Content disagreement withholds content assurance;
known selection/context/namespace disagreement still blocks measurement.

#### Version-2 snapshot and namespace witness

The minimum version-age route accepts an explicitly supplied **version-2 snapshot
witness**. It asserts that the exact retained project/lock pair is coherent, its
supported explicit population/context is complete within the stated bounds, and
each selected package/version belongs to the named public namespace. It asserts
no historical acquisition event or artifact correspondence:

```json
{
  "version": 2,
  "project": "Example.csproj",
  "framework": "net10.0",
  "project_sha256": "<64 lowercase hex digits for exact project bytes>",
  "lock_sha256": "<64 lowercase hex digits for exact lock bytes>",
  "coherent_snapshot": true,
  "baseline": {
    "sdk": "Microsoft.NET.Sdk",
    "explicit_population_complete": true,
    "unsupported_membership_version_influences": false,
    "unsupported_framework_rid_influences": false,
    "unsupported_source_influences": false
  },
  "packages": [{
    "id": "Example.Package",
    "version": "1.0.0",
    "namespace": "https://api.nuget.org/v3/index.json"
  }]
}
```

This is a template, not evidence. Accept it only from an accountable basis for
those assertions. V2 forbids producer, sdk_version, origins and content_hash;
v1 retains their original event meanings. Both routes require deliberate witness
selection, exact byte/context binding and positive package-specific namespace
before lookup. Private, unknown, alternate or conflicting namespace never uses a
public namesake. A lock alone records versions and framework, not project binding,
namespace authority, acquisition, deployed code or reproducible-build assurance.

The cascade uses the strongest accepted facts available but requires only the
minimum evidence for the narrower age claim. Population remains declaration-first
where supported. The separately approved fallback below can establish a narrower
snapshot when A cannot establish population. Qualified current pairs can be
selected automatically under the policy below; no dotnet/NuGet/MSBuild/restore is performed.
The [cascade contract](maintenance/measurement-evidence-cascade/spec.md) governs
namespace and stronger assurance; the [population contract](maintenance/nuget-snapshot-population/spec.md)
governs the explicitly accepted population fallback.

### Qualified current repository snapshots

Ordinary directory scans use **A → B1 → B2 → unknown**. A remains authoritative
when supported. B1 automatically selects the current project/lock pair only when
one attributable project owns the immediate lock candidate, the whole schema-1
lock has a sole supported framework and valid Direct requests/selections, and all
written PackageReference and framework facts can be safely extracted as supported
unconditional literals. Package IDs must equal the entire lock Direct set **in
both directions**, and normalized requests/framework must agree. An added/removed
reference, extra/missing Direct, changed request or known context conflict refuses;
explicit testimony cannot repair known ordinary-mode contradictions.

Unrelated unsupported project syntax may remain uninterpreted: B1 does not require
A to understand complete project semantics. Unextractable relevant facts, known
mutation constructs or ambiguous shared-lock attribution leave B1 unavailable;
explicit B2 remains available within its existing contract. No static grammar
expansion or evaluation occurs. Explicit single-project mode retains its existing
A/B2 precision behavior. A's later lock/witness/namespace failures never retry B.

B1 is a **policy-selected current snapshot**, not a recovered historical producer
association or complete evaluated MSBuild state. A coherent copied pair, dirty
worktree, archive or non-Git directory is eligible; a mismatching copied lock is
refused. Git cleanliness/history never decides B1. The exact safely read current
bytes are the basis. No acquisition, content, deployment, restore or reproducibility
claim follows. Optional explicitly accepted v3 testimony retains its accountable
snapshot association/scope meaning, independent of B1; invalid supplied testimony
is refused rather than ignored. V3 does not authenticate historical production.

Population acceptance authorizes **zero public requests** by itself. Ordinary
sources independently apply the [comparator policy](maintenance/nuget-conventional-comparator/spec.md).
Supported A without a supplied witness may select a uniquely attributable current
pair with the same whole-lock, bidirectional ID/request/context qualification as B1.
It stays declaration_derived and does not establish supplier baseline assertions.
Existing stronger v1/v2 and explicit precision routes remain available; invalid
supplied testimony is never discarded to obtain weaker acceptance.
JSON schema3 adds qualified_repository_snapshot to population_basis and fixed
limitations; B1 trust_basis is repository_snapshot_policy, or
supplied_snapshot_population_assertion when valid explicit v3 is also accepted.
Default human output names the current snapshot basis and real namespace blocker;
verbose/JSON makes limitations inspectable. See the
[qualified repository contract](maintenance/nuget-repository-snapshot/spec.md).

### Explicitly accepted resolved-snapshot fallback (B2)

When well-framed project XML is unsupported by A, explicitly selecting a **v3**
witness through the same witness options may accept population B. V1/v2 are never
reinterpreted as B. Supported A remains first: v3 on A is an invalid witness with
known N retained, and a failed A lock/namespace/metadata gate cannot trigger B.
Malformed, unsafe, over-budget, duplicate or DTD/entity project input cannot be
salvaged. This does not expand static project parsing or evaluate MSBuild.

The v3 JSON envelope has exactly these fields (placeholders describe required
values; this is a format example, not usable target testimony):

```json
{
  "version": 3,
  "project": "Example.csproj",
  "framework": "net10.0",
  "project_sha256": "<64 lowercase hex digits for exact supplied project bytes>",
  "lock_sha256": "<64 lowercase hex digits for exact supplied lock bytes>",
  "coherent_snapshot": true,
  "explicit_external_direct_complete": true,
  "packages": []
}
```

Selecting it accepts the supplier assertion that these exact project/lock bytes
belong together for the named retained framework snapshot, whose complete Direct
set represents explicit external direct packages, excluding implicit SDK references,
project references, other frameworks and RID variants. This assertion needs an
accountable retained evidence basis; libyears never generates it from co-location,
counts, names or hashes. It requires no declaration-completeness proof from A.

B accepts only a whole schema-1 lock with one literal framework and supported
selected versions and canonical numeric minimum requests for **every** Direct
record. Transitive/Project records do not count. Known unconditional literal
framework/identity/request conflicts and duplicate literal IDs refuse the whole B
population. Unknown/conditional/computed constructs stay uninterpreted. Changed
project/lock bytes invalidate binding; unchanged imported/environment state is
not evaluated or certified current. This claim is a retained snapshot, without
current evaluated completeness, acquisition/content correspondence, deployment,
restore success or reproducibility. Each project still owns its own occurrences.

Population acceptance supplies **no public comparator authority** by itself.
Packages may contain existing v2 records {id, version, namespace}; exact accepted
public testimony remains one comparator route. Empty packages supplies no testimony.
Ordinary sources may independently use the repository comparator cascade below;
explicit precision mode still requires exact accepted namespace testimony.
Unknown/private/conflicting testimony never uses public namesakes.

Source and row JSON evidence use population_basis (declaration_derived,
qualified_repository_snapshot, resolved_snapshot or unknown); snapshot source
evidence adds population_limitations.
Its trust_basis is supplied_snapshot_population_assertion; namespace/assurance
remain separate. Default human output marks accepted resolved snapshots; verbose
and JSON expose limitations. Snapshot minima are not current project declarations.
B2 remains available when automatic B1 qualification is unavailable; ordinary
known contradictions are terminal. Current evaluated state remains unestablished.

### Dates and versions

Dates mean first receipt by nuget.org, from identity-bound catalog `created`,
never original upstream release, published/commit/listing/restore/local time.
Latest means the greatest currently listed stable version from complete
SemVer-2 registration, independent of framework or requested compatibility.
An undated actual latest is not replaced by an older dated version. Used
prerelease/unlisted versions can measure; absent public records are not rebuilt
from archives. Listing or record changes may change later measurements.
Missing, invalid, timezone-free, sentinel year-1900 or conflicting creation
evidence is unavailable. Selected/public identities normalize leading core zeros, missing patch/zero
revision, ignored build metadata and case-insensitive prerelease suffixes;
stable ordering compares numeric components. Dates accept aware ISO timestamps
with zero to seven fractional digits, normalize UTC and truncate to microseconds.
The unchanged 365.25-day metric returns exact zero for used=latest and flags
negative timestamp deltas clamped to zero.

### Output and assurance

Explicit selection retains its schema-3 `version_evidence.nuget` singleton. It records declaration,
lock and optional witness filenames, literal framework, accepted lock format,
explicit direct scope, supplied-assertion trust and first-receipt publication
basis. Measured NuGet rows use `version_source: "packages_lock"` and
`nuget_evidence`; unmeasurable rows retain name, declared and reason plus
`nuget_evidence`, without `version_source`.
safe requested/lock-requested/original and normalized selection/publication facts
appear only after their stages establish them. Request mismatches claim no exact
selection. Origin states are unavailable, unsupported, asserted_public and
public_content_verified; hash states are unavailable, mismatch, local_agreement
and public_agreement. The last states require public identity/hash correspondence.
Raw hashes, origins, baseline, XML and diagnostics are omitted. NuGet-active human
reports abstract the root path and omit raw verbose diagnostics/TLS paths;
reports without NuGet sources retain their established output. Verbose JSON is identical.

Rows admitted through accepted namespace testimony add
`measurement_basis: bound_snapshot_namespace`,
`namespace_basis: accepted_producer_origin` or `accepted_snapshot_namespace`, and
`assurance` with producer_event, local_content, public_content and limitations.
V2 origin_state remains unavailable even when namespace-authorized dates measure;
this means acquisition origin was not asserted. V1 preserves asserted_public and
its original successful public_content_verified/public_agreement states. Local
agreement compares supplied lock/witness SHA512 values; public agreement adds
catalog comparison. Missing/mismatched content is inspectable without inventing
verified content. Neither event testimony nor a number proves reproduction or
deployment. Source trust_basis is supplied_producer_assertion for v1 and
supplied_snapshot_assertion for recognized v2. Default human output stays concise;
use --verbose or JSON for evidence, assurance and limitations.

Python/npm/Yarn already measure supported snapshot versions without event/hash
assurance, but do not positively verify the applicable public namespace. Ruby
requires supported public lock source attribution. These different artifact
mechanics are retained; the Python/npm namespace limitation is separate future
work, not permission to weaken NuGet public-source safety.

Ordinary repository mode instead adds top-level `nuget_sources`: a sorted array
of `{source_id, version_evidence, summary, measurement_available}`. Each entry
represents a project, including failed and empty sources. `source_id` is its
POSIX root-relative project path; discovery-wide failure has null identity and
null declaration source. Entry evidence uses the existing NuGet fields with
filenames relative to that project's parent; `summary` uses existing nullable
summary fields. Ordinary measured/unmeasurable NuGet rows and source errors add
`source_id`; row `nuget_evidence.project` remains the immediate bound filename.
The ordinary mode omits the selected-only `version_evidence.nuget` singleton;
other ecosystems' evidence/rows/errors and the explicit singleton shape remain unchanged.
This additive schema-v3 representation preserves same-name packages and same
project basenames without choosing a representative or deduplicating occurrences.
The NuGet aggregate sums source populations only when all are known; measured
count is null only if all its sources are unavailable, and numeric aggregates
retain available rows. Human output quotes source identities and reports per-
project population/availability alongside combined facts. See the independently
reviewed [repository-source contract](maintenance/nuget-repository-sources/spec.md).

### Availability and safe input

Project/population rejection gives an unknown denominator. Accepted declarations
plus an unavailable lock/witness retain known N (even zero), with null measured,
coverage and NuGet numeric aggregates and no fabricated dependency failures.
Accepted nonempty scope uses M/N, including 0% for all individual failures;
validated empty evidence has 0/0, null coverage, total 0.0 and other aggregates
null. Repository coverage is null when any source is unavailable; available
sibling rows/aggregates survive. Whole-source failures use `source_errors`,
individual failures `unmeasurable`. Completed empty/partial/source-error reports,
including an explicitly missing project, exit 0; systemic worker/report failures
exit 2 with fixed safe text. See the [complete failure contract](specs/006-nuget-selected-evidence/spec.md#s6--failure-and-availability-contract).

Inputs are read through bounded descriptor-relative, regular-file checks inside
the selected root; only contained regular-file symlinks are permitted. Replaced,
unsafe or special inputs fail closed. Hosts without the required no-follow,
nonblocking and descriptor-relative primitives refuse source reading, including
Windows environments without those primitives. Windows worker lifecycle CI
success does not imply filesystem-reader support or usable scan coverage.

### Enforced bounds

| Enforced bound | Limit |
|---|---|
| Project / lock / witness bytes | 1 MiB / 16 MiB / 16 MiB |
| XML depth / elements / attributes per element | 32 / 50,000 / 32 |
| JSON depth / local values / local string | 32 / 200,000 / 16 KiB |
| Version text / numeric component | 256 ASCII characters / 32 decimal digits |
| Framework / producer or SDK assertion string | 128 / 256 characters |
| Direct references / lock entries / witness package records | 10,000 / 50,000 / 50,000 |
| Each metadata wire / expanded body | 8 MiB / 32 MiB |
| Aggregate wire / expanded bytes per package | 64 MiB / 128 MiB |
| Metadata JSON depth / values / string | 32 / 500,000 / 1 MiB |
| Pages / versions per package | 256 / 100,000 |
| Requests per package / NuGet scan | 512 / 4096, including service-index discovery |
| Socket operation timeout / package / NuGet metadata scan | at most 10 / 60 / 300 seconds |
| Worker readiness / protocol message | 10 seconds after process creation / 16 KiB |
| Parent polling / cancellation reserve / initial terminate wait | 10 ms ceiling / 0.5 seconds within deadline / at most 0.25 seconds |
| Retries / redirects | zero / zero |

### Metadata access and supervision

Requests use verified HTTPS only on exact `api.nuget.org`: fixed V3 index,
`registration5-gz-semver2` paths for the expected package, and validated linked
`catalog0/data` leaves. No alternate host, credentials, query, fragment, explicit
port or archive request is admitted. Retry-After on 429/503 suppresses later
requests within scan budgets; there is no sleeping retry. The isolated trusted
installed Python helper runs only libyears metadata code, never target code or
a package manager. Absolute parent deadlines cover DNS/connect/TLS/headers/body,
parsing and traversal; cutoff results are discarded, the worker is terminated,
killed/reaped with bounded waits and remaining requests suppressed. Earlier
successes survive. Startup/process creation and OS scheduling are not hard
real-time guarantees for the whole CLI. An unreaped worker is systemic failure,
with deferred cleanup rather than an unbounded wait or synchronous fallback.
The worker uses shared default verified TLS trust selection; the explicit
`--ca-bundle` argument is validated but is not forwarded to this worker.

## Maven

Maven support in this unreleased source checkout follows approved [Feature007](specs/007-maven-dependency-age/spec.md),
its [bounded source policy](specs/007-maven-dependency-age/source-policy.md) and
[metadata contract](specs/007-maven-dependency-age/metadata-contract.md).
[Verification status](specs/007-maven-dependency-age/verification.md) distinguishes
passed offline conformance from the pending authorized DPC operational witness.

Run ordinary directory/JSON/verbose commands; there are no Java-specific options.
A direct POM-file argument does not activate Maven. `--resolved` remains Python-only.

### Maven population and version facts

Each safely discovered project owns its supported local base-model direct external
requirements, including packaging=POM projects and test/provided/optional/tooling/
ordinary dependency-POM rows. Build plugins and their dependencies, management-only
entries and transitive closure do not add population. Gemfile, Gradle, lock exports,
SBOMs or target tools do not supply Maven Observed evidence.

A source is its root-relative POM path. Occurrences keep source/context plus exact
case-sensitive group/artifact/type/classifier model identity. Built-in handlers
supply separate artifact identities: test-jar and jar/tests may map to the same
artifact but remain distinct management/occurrence keys. Explicit empty classifiers,
unknown handlers, duplicates and unsupported relevant syntax refuse dependent facts.
No systemPath is read; system assignment refuses comparison.

Supported local parents merge raw dependency fields, with child-written values
winning and origins retained. Consumer-context literal properties and bounded
builtins can establish requests. Supported management supplies absent fields;
optional is never managed and scope defaults wait until absence is established.
BOM contents are never fetched or read, even when local. Unknown imports may leave
versions/scopes unavailable; independent explicit facts survive. Profiles are
considered as possible changes, with no host activation/evaluation.

An exact bare request or supported hard singleton can provide a Declared version;
it is never evidence of resolver selection. Ranges, dynamic selectors, snapshots,
missing/cyclic/unsupported values remain unavailable. A module's inherited request
counts for that consumer as well as any parent with its own direct requirement.
Totals weight occurrences, not unique package names or distinct upgrade actions.
Aggregation is separate from inheritance/co-location. Internal exclusion requires
an exact supported project GAV in the same unambiguous static aggregation component;
unknown membership/version can make N unknown while independent safe rows survive.

Observed means an accepted retained dependency-system selection bound to the same
source/context/direct identity. It never means loaded, installed, deployed or runtime
state. This version has no accepted Maven Observed reader; it reports that view
unavailable with independent null statistics rather than copying Declared data or
using Gradle locks, effective POMs, arbitrary dependency trees or archives.

### Maven comparator and time basis

Maven compares independently evidenced Declared and Observed versions using the
public repository's versioned POM Last-Modified values as a conventional release-age
surrogate. These dates do not establish first publication or upstream release.
The GA comparison does not establish classifier availability or compatibility.
The initial Observed view remains unavailable for the reader limitation above.

The comparator assumes Central correspondence after bounded local inspection.
Unassigned alternate/file/parameterized repository eligibility alone does not veto
comparison. Nearest unconditional child repository IDs replace whole parent records;
all possibly relevant profile writes are checked. Supported Central exclusion,
redefinition/block, system assignment, conflicting identity and relevant unknown
policy refuse before lookup. No public namesake response authorizes a request.
No supplier/private-assignment reader is invented. Undisclosed private same-ID/version
forks can still be misattributed; queries disclose public coordinate/version IDs.
Acquisition, bytes, producer history, evaluated model and runtime state are not proven.

Only fixed verified HTTPS Central GA catalogues and exact versioned POMs are used.
No alternate/private endpoint, archive, parent/BOM POM, index/search/provider or date
fallback is queried. Selected repository-contained settings/mirrors/launch evidence
use a finite grammar; an ordinary co-located settings.xml alone is not selected.
Credentials, unknown filters/extensions and unsafe relevant policy withhold comparison;
no user/global Maven settings, wrapper, cache or environment property is inspected.

Choose the greatest unique eligible version from the whole current GA catalogue
using pinned ComparableVersion3.9.11. `maven_conservative_stable_v1` admits numeric
forms, release aliases and service packs; recognized prereleases and snapshots are
excluded. Other safe strings are unknown: strictly below the known maximum is
harmless, at/above it or inability to compare refuses. Distinct equivalent maximum
strings such as1/1.0 are ambiguous; response order, lexical order and dates never
break the tie. The target is global GA age, with no request/major/variant compatibility
filter. Current catalogue disappearance can change a future result.

Both dates need exact POM identity and one valid nonfuture IMF-fixdate Last-Modified.
Missing target/used date ends the attempt; an older target, metadata lastUpdated,
HTTP Date, local/retrieval time or provider field cannot replace it. Same exact
version produces0.0 only after its shared date is admitted. Existing365.25-day
arithmetic and flagged negative timestamp clamping remain. Catalogue retrieval UTC
is separate freshness evidence, never a version date.

### Maven output and coverage

Normal output begins with **Conventional Maven dependency age**, paired Declared /
Observed summaries and **Time basis: Maven conventional (versioned public POM
Last-Modified)**. Verbose adds exact date/freshness/basis/origin/limitation details
without raw XML/headers/source URLs/credentials/absolute roots. Unsafe unsupported
request text may be null rather than disclosing a URL or location.

For each view, known N and accepted rows allow M/N, including0% when every age fails.
Total0.0 then describes an empty measured subset, not fresh dependencies. Certified
emptiness has N=M=0, null coverage and total0.0. Unknown population with safe rows has
null N/coverage but partial M/statistics; with no accepted collection, M/numerics are
null. A whole-unavailable sibling also makes coverage null. Means/medians/maxima use
the union of measured occurrences, never averages of source statistics. Views are
never substituted, added, subtracted or turned into a gap metric.

Schema3 retains siblings and adds `version_evidence.maven` plus top-level `maven`:

- `discovery`: complete/unavailable and fixed reason; unavailable can mean unknown
  Maven presence even before any POM was safely observed.
- `sources`: sorted root-relative IDs, safe context/parent identities, basis,
  limitations and independent `views.declared`/`views.observed` summaries.
- `occurrences`: structured model key, supported artifact key, scope/optional and
  independently nullable records with safe request/version/origins, availability,
  reason, limitations and nullable `age`.
- `views`: repository Maven-only populations/availability and the seven existing
  statistic names. Each version record has `version_basis`; its age separately holds
  `comparator_basis`, `time_basis=maven_conventional_pom_last_modified`, ordering/eligibility,
  `measured_version_pom_last_modified`, `comparison_version_pom_last_modified` and
  `catalogue_retrieved_at` (UTC).

Maven has no legacy scalar projection. `maven_plural_projection_unavailable` appears
in `source_errors` per detected POM, or with source_id null for incomplete discovery.
Maven's legacy by-ecosystem statistics are null; legacy repository N/coverage are null
whenever Maven is present/unknown. Successful existing-ecosystem rows/evidence/own
summaries and partial aggregates survive; every legacy source unavailable makes
M/numerics null. An admitted empty sibling can retain measured0/total0 as an explicit
incomplete **legacy subset**. No Maven value enters legacy dependency rows or totals.
Consumers must use the Maven subtree for its two answers. Closed-world consumers
that reject new keys/ecosystems/reasons may reject this additive schema3 extension.

### Maven bounds and availability

| Boundary | Limit / effect |
| --- | --- |
| Directory inventory | Exact regular pom.xml, depth0–4,256directories,10,000entries,100POMs; exclusions/unsafe links do not expand traversal |
| Local XML | 1MiB/document,32MiB distinct total, depth32/50,000elements; DTD/entities/XInclude refused |
| Model | Parent chain16,10,000direct records/POM and expanded scan; finite properties/profiles/policy/path budgets |
| Metadata | 2MiB GA catalogue/10,000entries;1MiB POM;64KiB/100headers |
| Worker | One GET per16KiB command; command10s/GA60s/scan300s,300attempts/64MiB, readiness10s, bounded0.5s cleanup attempts |

The [source policy](specs/007-maven-dependency-age/source-policy.md) defines exact
exclusions/grammar and remaining finite limits. Required no-follow/race-resistant
filesystem and isolated-process capabilities fail closed. On an unsupported host,
Maven discovery itself can remain unknown and make legacy repository coverage null,
even for a directory with no confirmed POM. Native this-host tests and injected
semantics do not establish positive Windows support or an executed hosted matrix.
Final bounded deferred cleanup can finish after metadata command/I/O deadlines;
no unbounded reap, worker restart, synchronous fallback or further metadata I/O is
allowed. Plain hex chunked framing is bounded; extensions/trailers and compressed
responses are refused. No Maven/Gradle/Java/build/restore/resolver/target code executes.

## Cross-ecosystem lessons

Direct scope is an ecosystem contract: npm production declarations, Ruby lock
DEPENDENCIES, selected Ruby groups and per-project NuGet occurrences answer
different questions. A package appearing twice across NuGet projects counts twice;
this is not a count of unique package names. `--resolved` supplies Python evidence
only. Source errors can make a denominator unknown while successful sibling
measurements remain useful and visible.

Exact selection, public comparison and stronger assurance should be read separately.
Python/npm snapshot measurement does not establish public namespace; Ruby requires
supported public lock authority; NuGet's ordinary convention explicitly assumes
correspondence after bounded inspection. These distinctions do not grant permission
to substitute private packages with public namesakes or to change another ecosystem's
rules. Maven adds independent request/retained-selection views and a disclosed
conventional time basis; its module occurrences and totals remain separate from
legacy scalar summaries. Missing evidence is reported rather than resolved, guessed or reconstructed.

### History and further reading

For how the contracts arose, read the [Feature006 methodology retrospective](specs/006-nuget-selected-evidence/methodology-retrospective.md),
its [handoff](specs/006-nuget-selected-evidence/methodology-handoff.md), and the
[earlier NuGet retrospective](specs/006-nuget-selected-evidence/retrospective.md).
The [Python/npm namespace opportunity](ROADMAP.md#15-pythonnpm-positive-public-namespace-authority)
and other radar entries are future investigations, not current support.
