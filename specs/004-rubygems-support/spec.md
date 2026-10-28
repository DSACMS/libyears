# Feature 004: Bounded RubyGems Support

## Status

Clarified draft — ready for narrow verification review

Human clarification H1–H8 and canonicalization decisions are authoritative.
The adversarial review is recorded in reviews.md. This revision is an author
clarification, not independent verification or specification approval.
Implementation is not approved. No plan or tasks are authorized by this draft.

## Problem

Repositories retain exact RubyGems dependency selections in `Gemfile.lock`,
but libyears cannot currently measure them. Requiring a different evidence
artifact loses the value of the repository's retained lock snapshot.

## User Outcome

A user can point libyears at a supported Ruby project root and obtain dependency
age measurements for conservatively supported direct RubyGems dependencies,
using only retained lock evidence and public RubyGems release metadata.

The result describes the committed lock snapshot supplied to the scan, not the
currently evaluated Gemfile, production-only dependencies, installed or runtime
environment, or what a fresh Bundler resolution would select. As with existing
local scans, libyears reads the supplied working-tree artifact; it does not
certify that its bytes are committed, clean, or build-consumed. Source archives
and ordinary directories remain usable without Git history inspection.

## Goals

- Use `Gemfile.lock DEPENDENCIES` as recorded direct scope and supported lock
  specs as exact selected-version evidence.
- Measure all recorded direct dependencies that have defensible public source,
  version, and publication-time evidence.
- Report missing or unsupported evidence honestly and preserve unaffected
  measurements in RubyGems, PyPI, and npm.
- Preserve static analysis, source availability semantics, metric arithmetic,
  and schema v3 compatibility.

## Non-Goals

Gemfile evaluation; group or production reconstruction; general Bundler
compatibility; transitive measurement; installed-environment inspection;
platform resolution; Git/PATH/private registry measurement; dependency
installation/resolution; recursive root discovery; portfolio orchestration;
and new runtime dependencies are outside this feature.

## Ecosystem Identity

The conceptual identity is **RubyGems** and the machine identifier is
`rubygems` in rows, evidence, source errors, and ecosystem summaries. Bundler
produces the evidence; it is not the ecosystem identifier. This deliberately
parallels `pypi` and `npm` without conflating the Ruby runtime with its registry.

## Evidence Model

The evidence chain is:

```text
root Gemfile.lock DEPENDENCIES -> recorded direct identities
root Gemfile.lock source/spec records -> exact selected versions
public RubyGems.org metadata -> eligible release identities and timestamps
existing libyears arithmetic -> measured rows and aggregates
```

**Repository observation:** [discovery.md](discovery.md) and
[reviews.md](reviews.md) record four DPC application roots, ordinary public
RubyGems lock evidence, missing ordinary specs for `bundler` and `tzinfo-data`,
and one generic/platform variant case. The reported 238/247 direct occurrences
are static evidence fitness before registry lookup, not measured coverage or
four independent users. No external repository was re-inspected for this draft.

Git `df7aee60446795f67da321331f778c3d1457fea7` preserves initial discovery, `67b7d89ca6f1c48bc92dcd128b19bb478a6ba969` its evidence refinement,
and `a16145f5ed88be66e8591c91dd57df0ffc8b7fab` the authoritative human selection. Ruby-versus-root-listing
selection is settled; it is not a question for this specification.

**Documented semantics:** the official
[lockfile guide](https://guides.rubygems.org/gemfile-lock/) describes direct
names in `DEPENDENCIES`, selected specs in source blocks, nested requirements,
and tool metadata. The version-pinned
[Bundler lock parser](https://raw.githubusercontent.com/rubygems/rubygems/v3.6.9/bundler/lib/bundler/lockfile_parser.rb)
corroborates indentation, source association, platform suffixes, and optional
sections. These establish evidence meaning, not approval to copy Bundler's
permissive parsing, deduplication, or platform selection.

## Source Recognition

Only an exactly named root `Gemfile.lock` can supply RubyGems evidence. No
nested lock, `gems.locked`, `.gemspec`, installed gem, or Gemfile declaration
substitutes for it. A direct-file CLI argument does not gain a new Ruby mode;
the feature activates through a directory scan.

| Root files | Observable behavior |
|---|---|
| Neither | No RubyGems source, rows, lookup, evidence, or ecosystem summary. |
| Gemfile only | Same no-source result; do not interpret or count declarations. |
| Gemfile.lock only | Activate bounded lock-snapshot discovery. |
| Both | Attempt bounded lock discovery; Gemfile contents have no effect. |
| Recognized lock unreadable, not a regular readable artifact, or invalid text | Source-level `invalid_lockfile`; no Ruby lookup. |
| Recognized lock malformed or unsupported | Failure Model applies; no recovery through Gemfile. |

Gemfile is neither required nor inspected nor evaluated, including when both
files exist. Recognition asserts only a supported recorded root lock snapshot,
not commit status or runtime relevance.

## Supported Gemfile.lock Boundary

The initial supported format is a bounded sectioned Bundler lock snapshot,
identified as `gemfile_lock` in evidence metadata. This is a libyears format
identifier, not a claim that Bundler has a numbered lock schema.

Positive recognition requires section framing consistent with the following
subset: at least one recognized source block, exactly one `DEPENDENCIES`, and
exactly one `PLATFORMS`. `BUNDLED WITH` is optional, as it was introduced after
the original section format. Its version alone neither certifies nor rejects
a lock generation. Require the supported structure rather than guessing from
the filename or accepting every file produced by a listed Bundler version.

The bounded syntax is:

- UTF-8 text, LF or CRLF, blank separator lines permitted. Section headings
  start in column one and are uppercase names listed here. Tabs, conflict
  markers, orphan nested lines, trailing unparsed syntax, and inconsistent
  indentation are rejected.
- `GEM`: two-space `remote: VALUE` and `specs:` fields; four-space spec rows
  `NAME (VERSION)` or `NAME (VERSION-PLATFORM)`; six-space nested dependency
  rows containing a name and optional parenthesized requirement text. Fields
  precede specs; nested rows belong to the immediately preceding spec.
- `DEPENDENCIES`: two-space name rows, optional parenthesized requirement
  text, optional trailing `!`. Preserve the row text excluding its structural
  indentation as `declared`. Empty scope is valid. Duplicate direct names,
  even identical rows, reject the whole source rather than inflate counts.
- `PLATFORMS`: required exactly once, with at least one two-space nonempty
  ASCII platform token (letters, digits, underscores, periods, hyphens). Empty,
  repeated sections, duplicate tokens, or malformed entries are invalid. These
  record snapshot coverage and never choose the scanning machine's platform.
- Optional singleton `BUNDLED WITH`: one indented tool-version token;
  optional singleton `RUBY VERSION`: one indented runtime-description line.
  Neither contributes dependency or selected-version evidence.
- Recognize `GIT` and `PATH` envelopes only to isolate unsupported sources:
  two-space metadata fields followed by `specs:`, with the same four/six-space
  row framing. Allowed metadata keys are `remote` for PATH and `remote`,
  `revision`, `branch`, `ref`, `tag`, `submodules`, `glob` for GIT. Values are
  inert nonempty text. No paths, revisions, URLs, or code are followed.
- Distinct source blocks are allowed. Repeated singleton sections, repeated
  metadata keys (except multiple GEM remotes as below) are malformed.
  Separate spec rows remain visible to matching; they
  are never silently collapsed.

Repeated GEM blocks are supported when each independently establishes the same
public remote and their evidence is compatible: disjoint specs or distinct
supported artifacts agreeing on selected version text. Different versions for
a direct name are dependency-level `ambiguous_lock_evidence`; identical artifact
rows, within or across blocks, are also ambiguous even if versions agree.
Different remotes remain separate authorities: safely attributable nonpublic
sources are dependency-level unsupported sources. A name spanning conflicting
or uncertain authorities cannot fall back to its public namesake. Repeated
blocks with unsafe boundaries are source-level `invalid_lockfile`.
A missing remote or insufficient source metadata yields dependency-level
`unsupported_dependency_source` when spec ownership and direct scope remain
safe; otherwise reject the whole lock as `invalid_lockfile`.

Nested six-space requirements are framing evidence only. Supported requirement
forms below apply without semantic evaluation. Unsupported but safely delimited
nested text does not expand scope or invalidate a direct selection; malformed
nested framing preventing safe interpretation is `invalid_lockfile`.

Names and selected-version tokens must be separable without inference. The
initial ordinary selected-version spelling is digits followed by zero or more
period-separated nonempty ASCII alphanumeric segments (for example `1`,
`1.2.0`, `1.2.pre.1`). A suffix after the first hyphen is platform evidence,
not part of that ordinary version. Supported platform spelling uses nonempty
ASCII letters, digits, underscores, periods and hyphens, with no extra identity
qualifier; inseparable version/platform/extra identity fails closed rather than
being split by guesswork. No version sorting or equivalence is
implied. A recognizable spec row with an unsupported version spelling fails
that direct dependency with `unsupported_lock_evidence`; broken row framing
is source-level `invalid_lockfile`.

Supported requirement framing is an optional nonempty parenthesized list of
comma-separated terms: optional `=`, `!=`, `>`, `<`, `>=`, `<=`, or `~>` followed
by a version token. Bare version terms are exact requirements. Surrounding term whitespace is
permitted; repeated terms and exact terms within compound lists are framing,
not consistency checks. Framing does
not evaluate satisfaction. Unrecognized requirement syntax on an otherwise
isolated direct row is `unsupported_requirement`; if the row's name/boundary
cannot be recovered safely, discovery fails at source level. Transitive
requirements are recognized only to delimit rows, never resolved.

A recognized but unsupported section, including `PLUGIN SOURCE`, `CHECKSUMS`,
or `CONTENT ADDRESSES`, rejects the whole source with
`unsupported_lockfile_format` in this initial subset. So do unknown fields
that could alter interpretation. This intentionally excludes some valid newer
locks; it does not label them malformed. Expanding that subset requires an
explicit specification change. Empty/arbitrary files without positive
section identity are unsupported/unclassifiable; recognizable sectioned files
missing required sections are invalid.

For GEM authority, accept only the literal public remote
`https://rubygems.org` with optional trailing slash. A different remote,
including HTTP, a mirror, credentials, a custom path, or private authority,
cannot supply a public measurement. A single identifiable nonpublic source is
isolated at dependency level. Multiple remotes in one GEM block cannot
attribute each spec to an authority; reject those dependencies, not other
well-attributed blocks. No fallback to another public spec with the same name.

## Direct Dependency Scope

Every distinct name in a supported `DEPENDENCIES` set contributes once to
discovered count, even if unsupported, missing a spec, or unmeasurable at the
registry. All recorded direct dependencies are included; development, test,
and default group membership is not reconstructed or filtered.

Specs absent from `DEPENDENCIES` are transitive-only for this measurement and
produce no dependency row or registry request. A spec's nested requirements
never enlarge direct scope. `BUNDLED WITH` is not a dependency declaration.

## Dependency Identity

**Documented semantics:** the
[naming guide](https://guides.rubygems.org/name-your-gem/) distinguishes hyphens
and underscores. RubyGems.org's
[name validation](https://raw.githubusercontent.com/rubygems/rubygems.org/master/lib/name_format_validator.rb)
restricts characters, while its
[package model](https://raw.githubusercontent.com/rubygems/rubygems.org/master/app/models/rubygem.rb)
uses case-insensitive uniqueness and case-insensitive lookup fallback. Registry
lookup convenience does not prove that differently cased lock entries are the
same selected evidence.

Preserve lock spelling and compare lock identities exactly, case-sensitively.
After public source authority is independently established, registry identity
may differ only by ASCII letter case. This contract is endpoint-independent:
identity must be established even if an endpoint omits a package-name field.
No punctuation normalization, hyphen/underscore equivalence, period substitution,
Unicode case folding, fuzzy matching, typo correction, or public-namesake
substitution is permitted. Failure to establish identity under this contract is
`invalid_registry_response`. Typosquatting detection is outside scope.

Accept ASCII letters, digits, periods, underscores, and hyphens, with an
alphanumeric first and last character and at least one letter. This is a
bounded identity syntax, not replication of every server-side naming/reserved
word policy. Invalid or unsupported isolated direct names use
`unsupported_dependency_name` with no lookup. Structurally unparseable names
invalidate discovery. URL quoting is transport encoding only: it must not
change identity or permit path/query/host injection.

## Lock Evidence Matching

For each direct name, inspect only spec rows with exactly that name. Source
ownership must be established before accepting any version. A name belonging
to Git/PATH/nonpublic/multiple-remote evidence, or marked `!`, is
`unsupported_dependency_source`, even if a public namesake also exists.
This deliberately rejects explicit source pins even when a public block could
be inferred; source-pin interpretation is outside the supported subset.

| Evidence for an otherwise supported direct name | Outcome before registry lookup |
|---|---|
| One supported generic or platform-qualified public spec | Accept exact selected package version; retain artifact provenance. |
| No selected spec | `lock_version_missing`; requirement/tool text never substitutes. |
| Distinct supported public artifacts all agreeing on exact version text | Accept one dependency; retain every selected artifact. |
| Different selected version text or identical duplicate artifact rows | `ambiguous_lock_evidence`. |
| Conflicting/uncertain source association | `unsupported_dependency_source`; no public fallback. |
| Isolated unsupported version or required artifact identity | `unsupported_lock_evidence`. |
| Broken framing or unsafe attribution | Whole-source `invalid_lockfile`. |

Trust selected evidence for unconstrained, bare exact, `=` exact, ranges, and
compound requirements. Preserve requirement text; do not evaluate satisfaction,
Ruby version equivalence, or resolution. Neither textual equality nor inequality
establishes semantic compatibility. Unsupported isolated direct framing remains
`unsupported_requirement`; unsafe framing rejects the source.

## Platform Policy

A single supported platform-qualified record and agreeing multi-variant records
establish package version, not runtime compatibility. Never infer host/runtime
platform or select variants from PLATFORMS, build files, environment variables,
or force_ruby_platform. Do not restrict latest comparison to locked platforms.
Version plus platform is not universally complete artifact identity: additional
identity such as ruby_abi exists. No ABI/runtime resolution is authorized.
Required lock identity outside the bounded generic/platform model fails closed;
identifiable unsupported registry classes are treated as specified below.

## Special Dependencies

`bundler` in `DEPENDENCIES` is counted like any direct name. Without an ordinary
supported selected spec it is `lock_version_missing`; `BUNDLED WITH` never
supplies its used version. With a supported ordinary spec it follows the same
rules as other gems. No special inference or exclusion applies.

`tzinfo-data` without a selected spec is likewise counted and
`lock_version_missing`; do not evaluate Gemfile platform conditions to drop it.

Git/PATH/private/explicit-source dependencies remain discovered but
unmeasurable when their names and source ownership are safely isolated. Never
fetch those sources or use public metadata for their namesakes. Unsafe framing
that prevents isolation is a whole-source error, not fabricated dependency rows.

## RubyGems Registry Authority

Only public RubyGems.org metadata may establish RubyGems publication history.
Requests must use verified HTTPS, certificate and hostname verification, a
positive finite timeout, and an identifying User-Agent. Preserve existing CA
selection: explicit `--ca-bundle`, then Python/OpenSSL defaults and environment,
then the existing local pip-bundled fallback only when appropriate. An unusable
explicit bundle fails validation; verification must never be disabled.

Construct request URLs from fixed authority and safely encoded identity. Do
not use repository remote URLs as request destinations, credentials, project
configuration, gem download URLs, or metadata-supplied links. Redirects must
not escape the supported HTTPS authority. Network access remains isolated
behind a registry adapter boundary; arithmetic receives established dates.

Required evidence is exact version identity, platform identity, authoritative
prerelease classification, defensible publication time, and availability for
latest candidates. Any returned name must agree with the accepted identity
policy. Missing or contradictory required metadata cannot produce a guess.
Do not use a server's numerically latest response as timestamp-based latest.

Endpoint selection belongs in planning. Supported observable response population
must be obtained without silent truncation, but ordinary public APIs do not
establish complete historical or yanked publication visibility. Missing metadata
proves neither yanking nor never-existence. Required identity evidence cannot
depend on whether a chosen endpoint happens to return a name field.

## Publication Timestamp Policy

This is the single normative canonicalization definition for used and latest
roles. The population is supported generic and platform-specific public
RubyGems artifact records for the exact package-version text whose full required
identity is understood by Feature 004. It is independent of locked platforms.
Identifiable unsupported classes, including additional ruby_abi identity, are
excluded without poisoning otherwise supported records. Contradictory identity,
conflicting source association, malformed metadata, or unclassifiable required
identity fails the dependency with `invalid_registry_response`. No qualifying
records yields `version_not_found` for used evidence.

Supported observable yanked artifacts may contribute publication timestamps.
Missing records are neither presumed yanked nor reconstructed. For each
qualifying record, use authoritative version creation time (`created_at` or
an authoritatively equivalent `version_created_at`), parsed as a valid aware
timestamp, normalized to UTC with precision preserved. Exclude missing, invalid,
or historically inadmissible timestamp evidence. Every timestamp on 2009-07-25
UTC is inadmissible. Never use built_at as authority, fallback, or rehabilitation;
package times, lock times, commit times, and scan time are also inadmissible.
An unusable timestamp alone does not poison other admissible records.
Contradictory authoritative timestamp fields remain `invalid_registry_response`.

The canonical package-version publication date is the EARLIEST admissible
authoritative publication timestamp across qualifying supported observable
records, including observable yanked records. No remaining timestamp yields
`release_date_missing` for used evidence and excludes the version from latest.
Used and latest apply this identical rule.

Canonical date means “earliest admissible supported observable publication
evidence,” not first-ever historical publication or complete historical
knowledge. Missing historical records are not inferred. Future record
disappearance may change future measurements. The website/import predicate is
a heuristic, not historical attestation; other dates remain observable evidence,
not proof of historical certainty.

## Stable Release Eligibility

A version requires supported currently available stable artifact evidence with
authoritative prerelease=false, plus its canonical date, to qualify as latest.
A version represented only by yanked artifacts may be measurable as used but
cannot be latest. Do not infer prerelease or availability from spelling or
absence. Missing/contradictory required classification is
`invalid_registry_response`. Prerelease used versions may be measured.
Requirements, Ruby compatibility, host platform, and numeric version ordering
do not filter latest. Choose the eligible version with greatest canonical date;
equal-date different-version ties use ascending exact version text, not semantic
ordering. No eligible candidate yields `no_stable_release`.
Byte-equivalent duplicate registry records may collapse; conflicting duplicates
are invalid. Response order never determines canonicalization or selection.

## Used-Version Semantics

`package_not_found` means supported public metadata reports package absence;
`version_not_found` means no qualifying supported observable exact used-version
record. Neither claims never-existence or known yanking. No yank-specific missing
reason is introduced. Missing dates use `release_date_missing`. Requirements or
similar versions never repair absence.

Arithmetic remains UTC elapsed seconds / (86400 * 365.25), no grace period.
Same used/latest exact version identity yields exactly 0.0 using the shared
canonical date. Negative differences clamp to zero with timestamp_anomaly=true;
otherwise false. Aggregate only measured rows with existing sum/mean/median/max.

## Failure Model

Reasons below are stable identifiers for this clarified draft. Existing identifiers are reused
where their ecosystem-neutral meanings fit; human wording must name RubyGems or
Gemfile.lock rather than PyPI/package-lock/Yarn. No new Ruby-prefixed aliases
are needed. No requirement-conflict, yank-missing, typo, or platform-specific reason is added.

| Reason | Origin | Level / meaning | Availability class |
|---|---|---|---|
| `invalid_lockfile` | Reused | Unreadable or malformed recognized lock; structural conflicts | S-unknown |
| `unsupported_lockfile_format` | Reused | Unclassifiable lock, unsupported sections/semantics | S-unknown |
| `unsupported_dependency_name` | New | Isolated direct identity outside supported syntax | D-local |
| `unsupported_requirement` | Reused | Isolated direct requirement outside supported framing | D-local |
| `lock_version_missing` | Reused | Direct name lacks selected spec | D-local |
| `ambiguous_lock_evidence` | Reused | Different selected version texts or identical duplicate artifact rows | D-local |
| `unsupported_lock_evidence` | New | Isolated selected evidence cannot be interpreted under bounded version/platform policy | D-local |
| `unsupported_dependency_source` | Reused | Git/PATH/nonpublic/explicit pin or unattributable multiple-remotes source | D-local |
| `package_not_found` | Reused | Supported public metadata reports package absence, not never-existence | D-registry |
| `version_not_found` | Reused | No qualifying supported observable exact used-version record | D-registry |
| `release_date_missing` | Reused | Used publication timestamp missing or unsafe | D-registry |
| `no_stable_release` | Reused | No eligible stable release remains | D-registry |
| `registry_error` | Reused | Transport, TLS, timeout, HTTP/service/rate-limit failure | D-registry |
| `invalid_registry_response` | Reused | Unusable response structure, identity/classification, or contradictory metadata | D-registry |

For **every S-unknown reason**, Ruby discovered count and measured count are
null; no Ruby lookup or synthetic dependency rows occur. No Ruby dependency
continues because the sole scope artifact is untrusted. Other ecosystems
continue. This is deliberately different from Yarn's independent valid
package.json denominator: even a plausible DEPENDENCIES substring in a rejected
Ruby lock is not trusted as a complete scope. All per-Ruby numeric fields are
null. Repository aggregates still retain successful rows as below.

For **every D-local reason**, discovered count N remains known, measured count
M remains available, and the failing dependency makes no registry request.
For **every D-registry reason**, N and M remain available and lookup has been
attempted; the failure contributes no measured row. For both classes, other
Ruby dependencies and other ecosystems continue normally; ordinary M/N coverage
applies. A service-wide outage produces individual failures for candidates,
not loss of an already known denominator. No registry reason is promoted to a
source error merely because many dependencies fail.

Failure precedence is independent of parser order: malformed supported structure
(including conflict markers) takes precedence over unsupported whole-source
sections/fields; both precede dependency-level interpretation. Structural failure
preventing safe attribution always rejects the whole source. An otherwise
unclassifiable file is `unsupported_lockfile_format`. Once structure is safe,
precedence is isolated name, direct requirement framing, unsupported source,
missing/ambiguous selection, unsupported selected identity, then registry failure.
Registry validation precedes missing used record, missing used date, and lack of
stable candidates. Narrow dependency failures never become source errors merely
because all dependencies fail.

## Coverage Semantics

| Case | RubyGems summary | Repository consequence |
|---|---|---|
| A. No Ruby source | Omitted entirely | Existing detected ecosystems determine results; no artificial zero Ruby entry. |
| B. Whole Ruby source rejected | Discovered=null, measured=null, coverage=null; all Ruby numeric aggregates null | Discovered=null and coverage=null; retain available measurements and their aggregates. |
| C. Valid scope with local failures | Discovered=N, measured=M, coverage=M/N for N>0 | Combine known scope and successful rows normally. |
| D. One registry failure | Same as C; failing row remains in N | Preserve other successes. |
| E. All three valid ecosystems | Each retains its own N, M, and coverage | Sum discovered counts and measured rows across ecosystems; coverage is total M/total N. |
| F. Ruby rejected, others succeed | Same as B | Successful PyPI/npm rows, measured count, and numeric aggregates remain available. |

With no detected sources at all, ecosystems/evidence are empty, discovered=0,
measured=0, coverage=null, total=0.0, and mean/median/maximum=null.
If there are detected sources and every detected source is unavailable, repository measured count is null.
If at least one detected source has measurement available, repository measured
count is the number of successful rows, including zero. Repository discovered
count is null if any detected denominator is unknown; coverage is null if any
source rejects measurement or discovery, including existing npm known-N source
rejections. Do not convert unknown counts to zero.

For a valid empty Ruby scope: N=0, M=0, coverage=null, total=0.0, and
mean/median/maximum=null. For valid N>0 with no measured rows: M=0,
coverage=0.0, total=0.0, and other aggregates=null. Repository numeric aggregates
always use available successful rows; with none, total=0.0 and other aggregates
null, even when repository counts are unavailable. These preserve the current
Feature 003 distinction between an unknown per-source summary and the
repository's aggregation of available rows. Parsing never enters metric math.

## Mixed-Ecosystem Behavior

PyPI, npm, and RubyGems can coexist in one selected root. Identity is
(ecosystem, package name); matching names in different ecosystems are separate
rows. Ruby evidence failures must not change Python/npm source selection,
versions, reasons, registry rules, or evidence representation. Preserve
package-lock v2/v3, Yarn Classic, Python exact pins, and Python snapshots.

Repository aggregates combine measurable rows; per-ecosystem summaries and
provenance remain distinct. No dynamic plugin system or cross-root aggregate
is part of the product. Failure isolation follows the smallest safe boundary
specified above, including Ruby source failure alongside successful ecosystems.

## JSON Schema

Retain **schema version 3**; additive representation suffices, with no structural incompatibility. Existing ecosystem-keyed objects,
`version_source`, nullable counts, `unmeasurable`, and `source_errors` represent
the bounded feature without structural reinterpretation. Human diagnostics
are not currently serialized in schema v3 and remain human-only.

Measured Ruby rows use `ecosystem: "rubygems"` and
`version_source: "gemfile_lock"`. Both `declaration_source` and
`snapshot_source` are `Gemfile.lock`; `format` is `gemfile_lock` on accepted
bounded evidence and null for rejected whole-source evidence. Add
`scope: "all_direct_locked"` to the Ruby evidence object to make its all-group
snapshot scope machine-readable; top-level `dependency_scope` remains `direct`.
This is additive ecosystem evidence, not a change to existing npm/PyPI objects.

Unmeasurable rows retain exact name and recorded `declared` row text. Source
errors retain the existing fields `ecosystem`, `source`, and `reason`; source
is `Gemfile.lock`. Do not add exception/credential details. Normal and verbose
JSON have the same structure and values.

These are **partial JSON examples**, not complete reports. Package names and
timestamps are illustrative, not live lookup results. The successful fragment
illustrates ordinary generic evidence; the additive provenance contract below
also applies to platform-qualified and multi-variant selections.

```json
{
  "schema_version": 3,
  "dependency_scope": "direct",
  "ecosystems": [
    "rubygems"
  ],
  "version_evidence": {
    "rubygems": {
      "declaration_source": "Gemfile.lock",
      "snapshot_source": "Gemfile.lock",
      "format": "gemfile_lock",
      "scope": "all_direct_locked",
      "publication_basis": "earliest_admissible_supported_observable"
    }
  },
  "dependencies": [
    {
      "ecosystem": "rubygems",
      "name": "example_gem",
      "used_version": "1.0.0",
      "used_release_time": "2024-01-01T00:00:00Z",
      "latest_stable_version": "1.0.0",
      "latest_stable_release_time": "2024-01-01T00:00:00Z",
      "libyears": 0.0,
      "timestamp_anomaly": false,
      "version_source": "gemfile_lock",
      "rubygems_evidence": {
        "selected_artifacts": [
          {
            "version": "1.0.0",
            "platform": "ruby",
            "source": "https://rubygems.org"
          }
        ],
        "used_publication_artifacts": [
          {
            "version": "1.0.0",
            "platform": "ruby",
            "publication_time": "2024-01-01T00:00:00Z",
            "yanked": false
          }
        ],
        "latest_publication_artifacts": [
          {
            "version": "1.0.0",
            "platform": "ruby",
            "publication_time": "2024-01-01T00:00:00Z",
            "yanked": false
          }
        ]
      }
    }
  ],
  "unmeasurable": [],
  "source_errors": []
}
```

Partial failure rows for a valid scope (the names remain in discovered count):

```json
{
  "unmeasurable": [
    {
      "ecosystem": "rubygems",
      "name": "bundler",
      "declared": "bundler (~> 2.0)",
      "reason": "lock_version_missing"
    },
    {
      "ecosystem": "rubygems",
      "name": "example_native",
      "declared": "example_native",
      "reason": "ambiguous_lock_evidence"
    }
  ]
}
```

Partial mixed report: rejected Ruby discovery and one successful PyPI row with
1.0 libyears (row and unchanged PyPI evidence omitted):

```json
{
  "summary": {
    "dependencies_discovered": null,
    "dependencies_measured": 1,
    "coverage": null,
    "total_libyears": 1.0,
    "mean_libyears": 1.0,
    "median_libyears": 1.0,
    "max_libyears": 1.0,
    "by_ecosystem": {
      "pypi": {
        "dependencies_discovered": 1,
        "dependencies_measured": 1,
        "coverage": 1.0,
        "total_libyears": 1.0,
        "mean_libyears": 1.0,
        "median_libyears": 1.0,
        "max_libyears": 1.0
      },
      "rubygems": {
        "dependencies_discovered": null,
        "dependencies_measured": null,
        "coverage": null,
        "total_libyears": null,
        "mean_libyears": null,
        "median_libyears": null,
        "max_libyears": null
      }
    }
  },
  "source_errors": [
    {
      "ecosystem": "rubygems",
      "source": "Gemfile.lock",
      "reason": "invalid_lockfile"
    }
  ]
}
```

Add `publication_basis: "earliest_admissible_supported_observable"` to
version_evidence.rubygems. Each measured Ruby row adds `rubygems_evidence` with:
- `selected_artifacts`: array retaining every selected artifact as `version`
  and `platform` (generic is `ruby`), and `source: "https://rubygems.org"`;
- `used_publication_artifacts` and `latest_publication_artifacts`: arrays of
  supported records contributing admissible timestamps, each with `version`,
  `platform`, `publication_time`, and `yanked` where authoritatively known.

Existing used/latest release time fields contain canonical dates; version fields
remain package-version text, never platform-encoded identity. On unmeasurable
rows retain safely established selected artifact evidence where material, using
the same additive object without fabricated publication arrays. No parser
internals are serialized. The basis value explicitly denotes observable history,
not complete historical publication knowledge; normal human output must state
that limitation and that future disappearance can change measurements.

## Human Output

Identify RubyGems and `Gemfile.lock` for scope and selected versions. Whenever
Ruby evidence is detected, explain concisely: “All direct dependencies recorded
in Gemfile.lock; groups are not interpreted.” Do not call this production scope
or assert current Gemfile/runtime equivalence or verified Git commit status.

Show measured rows and summaries in the existing presentation. Failures must
be readable as missing exact lock evidence, unsupported identity/requirement,
unsupported source, ambiguous/platform evidence, malformed/unsupported whole
lock, or registry/timestamp failure as applicable. Do not describe a known
single unsupported platform as ambiguous merely to reuse wording. Name the
source file for whole-source failures; show null coverage as unavailable,
never 0%. Include original direct text on dependency failures. Explain source
authority failures as inability to establish supported public RubyGems evidence;
state that a public namesake is not substituted, without disclosing private URLs.

Keep normal output concise. Verbose diagnostics may supply safe line/section
context or explain timestamp uncertainty, source rejection, and registry
failure category. Do not disclose private remote values, credentials, raw
exceptions, or repository code. Human output must agree with JSON counts and
measurement values; formatting is not a stable API.

## CLI Behavior

`python -m libyears PATH` detects supported root Ruby evidence alongside
existing ecosystems. No Ruby-specific flag is required or introduced.
`--resolved` remains Python-specific and cannot supply missing Ruby evidence.
`--json`, `--verbose`, and `--ca-bundle` retain their meanings.

Completed scans, including Ruby source errors, partial/zero measurement, or no
source, return 0 with report data. Invalid CLI arguments or selected root path
retain exit 1; unexpected systemic failure retains exit 2. An unreadable root
lock is a reportable Ruby source failure rather than discarding another
ecosystem's results.

## Security Boundary

Parsing is static. Never execute Ruby, Bundler, repository code, gemspecs, or
Gemfile; install gems; resolve dependencies; inspect the installed environment;
or fetch Git/PATH/private dependency content. Do not read referenced PATH
content or private registry credentials. No package manager or additional
runtime dependency is introduced. Ruby network access is metadata-only to the
supported public authority under the verified TLS policy above; no gem archive
or arbitrary linked URL is fetched. Scans do not modify the target.

## Performance and Network Behavior

Requests and response sizes must be bounded: a finite request budget per direct
candidate, finite positive request timeout, and finite response-byte limit.
Exceeding a response limit yields `invalid_registry_response`; exhausting a
network/request budget yields `registry_error`, not a partial-history metric.
The concrete limits belong in planning, with fixture-verifiable boundaries.
No cache or concurrency is required. Transitive rows and locally rejected
direct rows cause no requests. No uncontrolled retry loop is allowed.

The official [rate-limit guidance](https://guides.rubygems.org/rubygems-org-rate-limits/)
states a general API limit of 10 requests per second. A scan must pace Ruby
requests at or below that guidance and respect rate-limit responses: do not
retry before a supplied Retry-After, and either defer within a finite budget
or fail affected lookups. Do not evade limits through alternate hosts or
credentials. Results and failure isolation for fixed inputs and responses must
not depend on request completion order. This adds bounded Ruby behavior;
it does not claim the current transport already enforces byte/rate limits.

## Release Validation

After specification, architecture, and tasks are approved, future validation
should use deterministic offline fixtures/mocks for every approved acceptance
criterion and product-question disposition. Cover parser failures, registry
records, source and dependency availability, mixed reports, CLI, TLS, bounds,
and preservation of existing behavior. No live network in correctness tests.

Dogfood against one explicitly authorized real Ruby project, without executing
its tooling. Compare human and JSON counts, evidence, reasons, and arithmetic;
record environment and limits; verify target files unchanged. An optional live
RubyGems smoke is useful only if dogfood does not establish the same evidence.
Do not treat environmental registry failures as offline correctness failures.
The convergence audit remains independent and read-only.

At eventual public activation, README, SPEC, CHANGELOG, and applicable AGENTS
ecosystem scope must migrate coherently at the approved documentation/release
checkpoint. This draft task changes none of them, performs no release
validation, and creates no plan or task graph.

## Deferred Work

Gemfile interpretation and production/default/group reconstruction remain the
separate EXPLORE opportunity in [ROADMAP.md](../../ROADMAP.md). Arbitrary Ruby
evaluation, general Bundler compatibility, Git/PATH/private registry support,
platform resolution, installation/resolution, and portfolio orchestration are
not approved by this feature. Supporting recorded artifacts does not authorize
resolving a platform. New lock sections and historical metadata
reconstruction also require explicit scope decisions, not parser guesswork.

## Acceptance Criteria

Criteria cover normative outcomes; numbering is not an implementation task graph.

- [ ] **AC-01:** Root Gemfile.lock alone activates directory discovery; Gemfile alone or neither file does not. Gemfile is never inspected or evaluated, including when present alongside the lock.
- [ ] **AC-02:** Nested locks, alternate filenames, gemspecs, and direct-file arguments do not activate Ruby discovery; supplied local lock bytes are usable without inspecting Git history or installed state.
- [ ] **AC-03:** Supported section structure positively identifies `gemfile_lock`; optional BUNDLED WITH presence/version does not independently certify or reject a generation.
- [ ] **AC-04:** Malformed supported framing, conflict markers, duplicate direct/singleton structure, missing required sections, unreadable/nonregular artifacts, or invalid text reject the source with invalid_lockfile and no partial Ruby results.
- [ ] **AC-05:** Unclassifiable content, unknown sections/fields, and recognized unsupported sections produce source-level `unsupported_lockfile_format`, without silently ignoring evidence that could alter scope or source interpretation.
- [ ] **AC-06:** Every supported DEPENDENCIES identity contributes once to direct discovered count regardless of group, local evidence failure, or registry failure; no group filter is reconstructed.
- [ ] **AC-07:** Specs and nested requirements not named in DEPENDENCIES create neither direct rows nor registry requests; tool/runtime metadata creates no dependency scope.
- [ ] **AC-08:** Lock spelling is preserved and lock comparisons remain exact; after independent public-source authority, registry identity permits only ASCII letter-case differences, endpoint-independently, with no punctuation/Unicode/fuzzy substitutions.
- [ ] **AC-09:** An isolated direct name outside the specified ASCII identity syntax is `unsupported_dependency_name` with no lookup; structurally unrecoverable identity rejects discovery.
- [ ] **AC-10:** One supported generic or platform-qualified public spec establishes exact package version and retains selected artifact provenance without runtime claims.
- [ ] **AC-11:** A direct name without a selected spec is `lock_version_missing` with no lookup; exact requirement text cannot substitute for the spec.
- [ ] **AC-12:** Distinct supported public artifacts agreeing on exact version text establish one counted dependency; differing version text or identical duplicate artifact rows produce ambiguous_lock_evidence without lookup.
- [ ] **AC-13:** Git/PATH/nonpublic/multiple-remote/explicitly pinned direct evidence yields `unsupported_dependency_source` without public namesake substitution, even when another public spec shares the name; human diagnostics explain this authority boundary without exposing private URLs.
- [ ] **AC-14:** Unsupported required selected version/artifact identity yields unsupported_lock_evidence when isolated; unsafe framing rejects the source.
- [ ] **AC-15:** Unconstrained, bare exact, = exact, range, compound, repeated, and whitespace-framed supported requirements retain evidence without satisfaction/equivalence checks; textual agreement/disagreement does not establish compatibility. Unsupported isolated direct framing is unsupported_requirement.
- [ ] **AC-16:** Host/platform/build configuration cannot select among lock or registry variants, change direct scope, or influence measurement results.
- [ ] **AC-17:** Direct bundler and tzinfo-data without ordinary selected specs remain counted and `lock_version_missing`; BUNDLED WITH and Gemfile conditions never replace or remove that evidence.
- [ ] **AC-18:** Ruby requests use only safely constructed public RubyGems.org HTTPS metadata URLs; repository/metadata links, redirects to other authorities, and credentials cannot redirect a lookup or alter identity.
- [ ] **AC-19:** Ruby requests enforce certificate and hostname verification, the existing CA selection precedence, positive finite timeout, and User-Agent; unusable trust never falls back to unverified TLS.
- [ ] **AC-20:** Metadata must establish full supported artifact identity and required classification; contradictory identity/source, unclassifiable identity, malformed evidence, or conflicting duplicate metadata yields invalid_registry_response; byte-equivalent duplicates may collapse.
- [ ] **AC-21:** Only aware authoritative version creation timestamps establish publication evidence, normalized to UTC with precision; built_at and all other fallback dates are prohibited.
- [ ] **AC-22:** Missing/invalid timestamps and every 2009-07-25 UTC timestamp are excluded individually without poisoning admissible records; contradictory authoritative fields fail invalid_registry_response. No admissible used date yields release_date_missing.
- [ ] **AC-23:** Canonical date is earliest admissible authoritative timestamp over supported observable generic/platform artifacts, independent of locked platforms; identifiable unsupported classes such as ruby_abi are excluded, and no qualifying used records yields version_not_found.
- [ ] **AC-24:** Latest requires supported currently available authoritative stable artifact evidence and a canonical date; only-yanked versions cannot be latest. Missing classification is invalid_registry_response; requirements/runtime/platform do not filter candidates.
- [ ] **AC-25:** Latest uses greatest canonical date, then ascending exact-version lexical tie-break, independently of response order, numeric version order, or server latest labels.
- [ ] **AC-26:** No eligible stable candidate yields `no_stable_release`, even when exact used-version evidence exists.
- [ ] **AC-27:** Supported observable yanked and prerelease used evidence may be measured; observable yanked records may contribute canonical dates. Missing metadata is neither reconstructed nor assumed yanked; absence reasons make no never-existence claim.
- [ ] **AC-28:** Ruby age uses UTC elapsed seconds divided by (86400 * 365.25) with no grace period; same-version identity uses one canonical time and yields exactly 0.0.
- [ ] **AC-29:** Negative timestamp differences clamp to zero and set timestamp_anomaly; nonnegative differences do not set it.
- [ ] **AC-30:** Numerical aggregates use only successful rows and preserve sum, mean, median, and maximum arithmetic; unmeasurable rows never enter those calculations.
- [ ] **AC-31:** Local and registry dependency failures retain N and available M, preserve unrelated Ruby and other-ecosystem results, and use M/N coverage for N>0; registry outages do not invalidate known scope.
- [ ] **AC-32:** Whole rejected Ruby sources produce no lookup or synthetic dependency rows and have null discovered/measured/coverage and all per-Ruby numeric aggregates, including when a plausible DEPENDENCIES substring exists.
- [ ] **AC-33:** Any detected unknown denominator makes repository discovered count null; any rejected source makes repository coverage null, while available successful measurements and aggregate values survive.
- [ ] **AC-34:** Repository measured count is null only when every detected source is measurement-unavailable; otherwise it equals successful row count, including zero. Absent sources are omitted rather than counted as rejected or empty ecosystems.
- [ ] **AC-35:** Valid empty scope yields discovered=0, measured=0, coverage=null, total=0.0, other aggregates=null; valid nonempty wholly unmeasurable scope yields coverage=0.0. Empty repository measurement aggregates remain total=0.0 and other aggregates=null even when counts are unavailable.
- [ ] **AC-36:** Three valid ecosystems coexist with distinct identities/provenance and per-ecosystem denominators; repository counts combine known direct scope and successful rows without merging same-name packages across ecosystems.
- [ ] **AC-37:** Adding RubyGems preserves existing PyPI/npm versions, source selection, reasons, registry semantics, and serialized evidence, including Python snapshots and npm lock conflicts.
- [ ] **AC-38:** Schema v3 retains existing meanings and adds Ruby scope/source metadata, publication_basis, selected artifacts and contributing used/latest publication artifacts as specified, including material safely known evidence for failures.
- [ ] **AC-39:** Failures use the specified stable reasons and precedence, with direct text in unmeasurable and whole-source path/reason in source_errors; verbosity does not add JSON diagnostics or expose sensitive details.
- [ ] **AC-40:** Normal human output states all-direct lock snapshot scope, uninterpreted groups, observable-history limitation and possible measurement changes after record disappearance, without production/current Gemfile/runtime/verified-commit claims; values agree with JSON.
- [ ] **AC-41:** Human failure output distinguishes the specified missing, unsupported, ambiguous/platform, malformed, registry, and timestamp cases, names whole-source paths, and renders unavailable coverage distinctly from 0%; verbose detail remains safe.
- [ ] **AC-42:** Normal directory CLI scanning requires no new Ruby flag, and --resolved cannot supply Ruby versions; completed partial, empty, and source-error reports exit 0 while existing usage/path and systemic exit categories remain 1 and 2.
- [ ] **AC-43:** Scanning never executes Ruby/Bundler/Gemfile/gemspec/repository code, installs or resolves dependencies, fetches Git/PATH/private content, reads private credentials, or modifies the target; runtime remains standard-library-only.
- [ ] **AC-44:** Ruby lookups enforce finite request/response budgets and timeouts; oversized/truncated history never produces a partial-history metric and uses the specified failure reason.
- [ ] **AC-45:** Ruby requests obey the documented API pacing limit and rate-limit responses without early Retry-After retries, unbounded retries, or alternate-authority evasion; fixed evidence/responses yield order-independent results.
- [ ] **AC-46:** Repeated GEM blocks with independently established same public remote and compatible disjoint or agreeing distinct-artifact evidence are supported without duplicate dependencies; conflicting versions and duplicate artifact rows remain ambiguous.
- [ ] **AC-47:** Different/missing/multiple remote or uncertain source evidence never authorizes public lookup; isolate unsupported_dependency_source only when ownership and direct scope remain safe, otherwise invalid_lockfile.
- [ ] **AC-48:** PLATFORMS is required once and nonempty; duplicate entries, repeated/empty section and malformed tokens are invalid_lockfile; platform entries never select runtime.
- [ ] **AC-49:** Nested requirements never enlarge scope or receive semantic evaluation; safely delimited unsupported text is inert, while unsafe malformed framing rejects the source.
- [ ] **AC-50:** Malformed supported structure takes precedence over unsupported whole-source evidence, which precedes local failures; local and registry precedence follows Failure Model independent of parser order.
- [ ] **AC-51:** Canonical publication is supported observable evidence, not complete historical knowledge: missing public records prove neither yank nor never-existence, outside-import-day times are not historically attested, and disappearing records may change future measurements.
- [ ] **AC-52:** With no detected sources, report empty ecosystems/evidence, discovered=0, measured=0, coverage=null, total=0.0 and null mean/median/max; Gemfile alone has this result absent other ecosystems.

### Bidirectional acceptance audit

Result: 52 numbered criteria, revised from 45. Every criterion maps to a
normative rule family below, and every normative behavioral family maps back
to criteria. Examples of the same rule are combined; independently consequential
outcomes are separate. Process obligations are excluded. This author audit is
not independent verification or approval.

| Normative rule family | Criteria (bidirectional) |
|---|---|
| Recognition and snapshot meaning | AC-01–02, AC-40, AC-52 |
| Lock structure, repeated sources, nested framing, PLATFORMS | AC-03–05, AC-09, AC-14–15, AC-46–50 |
| Direct scope and special dependencies | AC-06–07, AC-11, AC-17 |
| Lock/registry identity, source authority and platform policy | AC-08–10, AC-12–16, AC-18, AC-46–47 |
| Registry authority and metadata validation | AC-18–20, AC-44–45 |
| Canonical population, dates, observable history and availability | AC-20–28, AC-51 |
| Arithmetic and aggregates | AC-28–30 |
| Failure taxonomy and precedence | AC-04–05, AC-09, AC-11–15, AC-20, AC-22, AC-26–27, AC-39, AC-47–50 |
| Coverage, empty sets and mixed ecosystems | AC-31–37, AC-52 |
| Schema and provenance | AC-38–39 |
| Human output | AC-40–41 |
| CLI | AC-01–02, AC-42 |
| Security, performance and deferred boundaries | AC-07, AC-13, AC-16, AC-18–19, AC-43–45 |

## Product Questions

NONE. H1–H8 and all canonicalization sub-decisions are resolved. No newly
discovered product questions. Endpoint selection, bounded transport limits,
parser organization and fixture organization belong to technical planning after
narrow verification and specification approval; they do not reopen product policy.
