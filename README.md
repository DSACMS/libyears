# Libyears

## About the Project

Libyears is a local Python CLI that measures the age of direct Python, npm, RubyGems,
and explicitly selected NuGet
dependencies using release timestamps from their public registries.
It uses only the Python standard library at runtime.

Project website: https://dsacms.github.io/libyears

## Agency Mission

CMS is working to modernize the nation's digital health ecosystem, including
through public infrastructure, improved data sharing and interoperability, and
collaboration that empowers people and improves care.

See the [CMS Health Technology Ecosystem overview](https://www.cms.gov/initiatives/health-technology-ecosystem/overview).

## Team Mission

The function of the CMS Open Source Program Office is to:

> Establish and maintain guidance, policies, practices, and talent pipelines
> that advance access, build trust, and amplify impact across CMS, HHS, and
> Federal Open Source Ecosystems by working and sharing openly.

## Project Mission

Measure the age of direct dependencies using release timestamps from their
public registries through a small local CLI.

## Project Vision

Keep dependency freshness measurement simple, transparent, reproducible, and
maintainable, with human-readable evidence rather than guessed versions or dates.

## Core Team

See [Project Members](COMMUNITY.md#project-members) for project contacts and roles.

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

A directory scan measures supported sources at that directory. Ordinary human
reports also list bounded NuGet / C# project filename candidates below it, with
an explicit notice that no NuGet measurement was performed. Even one candidate
requires selection: point PATH at the chosen project's parent directory and use
`--nuget-project NAME.csproj` (see [NuGet snapshots](#explicit-nuget-project-snapshots)).
Candidate names establish neither supported declarations nor lock/provenance
authority. Other root ecosystems continue measuring normally; candidate counts
never enter dependency counts, coverage or totals. A repository/solution root is
not a combined NuGet scan.

Recognition examines only names/types: exact lowercase `.csproj` regular files,
root depth zero through four directory levels, at most 256 directories, 10,000
entries and 100 candidates. It skips dot-prefixed directories and exact `bin`,
`obj`, `node_modules`, `packages`, `vendor`, `venv`, `__pycache__` directories,
and follows no links/reparse points. Deeper remaining directories, exceeded
limits or filesystem errors give **incomplete**, without a partial list or exact
count. Missing safe directory primitives give **unavailable** (including hosts
without descriptor-relative traversal); this is not evidence of project absence.
Both states explain manual explicit selection. Lists are bounded observations,
not atomic filesystem snapshots. Project/solution contents are never read for
recognition. JSON, explicit NuGet selections and direct-file scans bypass this
human guidance and retain their existing measurement contracts. An empty bounded
search keeps the existing human report; `Ecosystems: none` describes no activated
measurement source there, not repository-wide absence of dependencies.

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

## RubyGems support

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

## Select declared Ruby groups

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

## Explicit NuGet project snapshots

NuGet is opt-in on directory scans. Select exactly one immediate C# project;
even a sole project, lock or assets file does not activate NuGet automatically:

```bash
python -m libyears PATH --nuget-project Example.csproj
python -m libyears PATH --nuget-project Example.csproj --nuget-provenance witness.json
python -m libyears PATH --nuget-project Example.csproj --nuget-provenance witness.json --json
```

The first command reports unavailable measurement authority. Only explicitly
supplying `--nuget-provenance` accepts that file's producer/supplier assertions;
a conventionally named or co-located witness is never trusted automatically.
Supply genuine retained evidence from an independently authorized producer, rather
than inventing assertions to make a scan pass. Libyears does not create it by
running dotnet, NuGet or MSBuild.

Both options require their exact spelling, occur at most once, and accept immediate
filenames with the shown suffixes. Paths, globs, filename lists, unsafe characters,
witness-only requests and direct-file PATH arguments are usage errors (exit 1).
The lock is always root `packages.lock.json`. Multiple co-located projects are
allowed because one is selected explicitly; their populations are never combined.
Python `--resolved`, npm/Yarn arbitration and Ruby group selection keep their
existing independent meanings.

Supported scope is one namespace-free UTF-8 SDK-style `Project Sdk="..."` with
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

The supplied witness is strict version-1 UTF-8 JSON with these required fields:

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
lookup, after decoded lock/witness SHA512 agreement. Public catalog identity and
SHA512 agreement must then pass before dates authorize measurement. No archive,
cache, NuGet.Config, source mapping or credential lookup repairs missing evidence.

H3 requires two bound evidence classes: **native NuGet package provenance** from
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
Matching hashes establish content correspondence. The snapshot does not prove
evaluated MSBuild completeness, successful restore, installed/deployed/runtime
scope or compatibility. Live measurement yield and signed-content hash-domain
fitness remain unvalidated; disagreement fails closed.

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

Schema 3 adds `version_evidence.nuget` only on activation. It records declaration,
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
ordinary reports retain their established output. Verbose JSON is identical.

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

## Current limitations

- Python declarations are read from `requirements.txt`; npm declarations are
  read from the root `package.json`; RubyGems scope comes from root
  `Gemfile.lock` DEPENDENCIES unless `--ruby-group` explicitly selects declared
  Gemfile groups within the closed static subset.
- Direct dependencies only.
- NuGet requires the explicit supported project/lock/witness snapshot above;
  there is no solution, portfolio, general MSBuild or private-feed interpretation.
- The resolved snapshot format is a narrow list of exact `NAME==VERSION`
  entries; repository declarations determine which entries are in scope.
- Libyears does not install or resolve dependencies.
- Transitive dependencies are not measured by default.
- No other package ecosystems are supported.

## Development

### Local Development

See [Getting Started](CONTRIBUTING.md#getting-started) for development setup.

Run the offline test suite with:

```bash
python3 -m unittest discover -s tests -v
```

See [SPEC.md](SPEC.md) for the full behavioral specification and [AGENTS.md](AGENTS.md)
for repository engineering rules.

### Coding Style and Linters

See [Coding Style and Linters](CONTRIBUTING.md#coding-style-and-linters) for
repository coding guidance and configured checks.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution instructions.

## Codeowners

Repository ownership is recorded in [.github/CODEOWNERS](.github/CODEOWNERS).

## Community

See [COMMUNITY.md](COMMUNITY.md) for community principles and roles.

### Community Guidelines

Read the [Community Guidelines](COMMUNITY.md#community-guidelines) and
[Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## Policies

### Open Source Policy
We adhere to the [CMS Open Source Policy](https://github.com/CMSGov/cms-open-source-policy).
If you have any questions, just [shoot us an email](mailto:opensource@cms.hhs.gov).

### Security and Responsible Disclosure Policy
*Submit a vulnerability:* Vulnerability reports can be submitted through [Bugcrowd](https://bugcrowd.com/cms-vdp). Reports may be submitted anonymously. If you share contact information, we will acknowledge receipt of your report within 3 business days.
For more information about our Security, Vulnerability, and Responsible Disclosure Policies, see [SECURITY.md](SECURITY.md).

### Software Bill of Materials (SBOM)
A Software Bill of Materials (SBOM) is a formal record containing the details and supply chain relationships of various components used in building software.
In the spirit of [Executive Order 14028 - Improving the Nation's Cyber Security](https://www.gsa.gov/technology/it-contract-vehicles-and-purchasing-programs/information-technology-category/it-security/executive-order-14028), a SBOM for this repository is provided here: https://github.com/DSACMS/libyears/network/dependencies.
For more information and resources about SBOMs, visit: https://www.cisa.gov/sbom.

## Public Domain
This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/) as indicated in [LICENSE](LICENSE).
All contributions to this project will be released under the CC0 dedication. By submitting a pull request or issue, you are agreeing to comply with this waiver of copyright interest.
