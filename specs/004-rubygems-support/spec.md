# Feature 004: Bounded RubyGems Support

## Status

Draft — committed before independent specification review

Feature 004 is selected for specification. Implementation is not approved.
This first draft preserves unresolved product choices for independent review;
it is not an approved implementation contract. No independent specification
review has occurred. The drafting checks and acceptance coverage audit below
are author checks, not that independent review.

Unless marked **documented semantics**, **repository observation**, or **open
choice**, behavioral requirements below are **proposed Feature 004 product
policy**. They do not assert general Bundler compatibility. Alternatives in
Product Questions are not defaults and must not be implemented by inference.

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
| Gemfile.lock only | **Open Q1:** recognize the snapshot, or require companion Gemfile presence. |
| Both | Attempt bounded lock discovery; Gemfile contents have no effect. |
| Recognized lock unreadable, not a regular readable artifact, or invalid text | Source-level `invalid_lockfile`; no Ruby lookup. |
| Recognized lock malformed or unsupported | Failure Model applies; no recovery through Gemfile. |

Q1 is a product choice, not a Bundler fact. Lock-only recognition fits snapshot
scope; companion-file recognition fits a stricter root convention. Neither
requires opening or evaluating Gemfile. In both cases, root recognition does
not certify commit status or runtime relevance.

## Supported Gemfile.lock Boundary

The proposed initial format is a bounded sectioned Bundler lock snapshot,
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
- `PLATFORMS`: two-space nonempty platform tokens; these record snapshot
  coverage and do not choose the scanning machine's platform.
- Optional singleton `BUNDLED WITH`: one indented tool-version token;
  optional singleton `RUBY VERSION`: one indented runtime-description line.
  Neither contributes dependency or selected-version evidence.
- Recognize `GIT` and `PATH` envelopes only to isolate unsupported sources:
  two-space metadata fields followed by `specs:`, with the same four/six-space
  row framing. Allowed metadata keys are `remote` for PATH and `remote`,
  `revision`, `branch`, `ref`, `tag`, `submodules`, `glob` for GIT. Values are
  inert nonempty text. No paths, revisions, URLs, or code are followed.
- Distinct source blocks are allowed. Repeated singleton sections, repeated
  metadata keys (except multiple GEM remotes as below), or duplicated source
  blocks are malformed. Separate spec rows remain visible to matching; they
  are never silently collapsed.

Names and selected-version tokens must be separable without inference. The
initial ordinary selected-version spelling is digits followed by zero or more
period-separated nonempty ASCII alphanumeric segments (for example `1`,
`1.2.0`, `1.2.pre.1`). A suffix after the first hyphen is platform evidence,
not part of that ordinary version. No version sorting or equivalence is
implied. A recognizable spec row with an unsupported version spelling fails
that direct dependency with `unsupported_lock_evidence`; broken row framing
is source-level `invalid_lockfile`.

Supported requirement framing is an optional nonempty parenthesized list of
comma-separated terms: optional `=`, `!=`, `>`, `<`, `>=`, `<=`, or `~>` followed
by a version token. Bare version terms are exact requirements. Framing does
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

Proposed conservative policy: preserve spelling and compare lock names exactly,
case-sensitively; never fold case, replace hyphens/underscores/periods, or import
PyPI normalization. Match returned registry identity exactly where a name is
returned; case-only response differences remain open under Q6.

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
| Exactly one ordinary public spec | Exact candidate, subject to Q3 platform/registry record policy and Q5 exact-requirement policy. |
| No selected spec | `lock_version_missing`; neither requirement nor tool version substitutes. |
| Multiple versions | `ambiguous_lock_evidence`. |
| Duplicate ordinary spec rows, even same version | `ambiguous_lock_evidence`. |
| Multiple platform variants, even same version | `ambiguous_lock_evidence`; no platform resolution. |
| One platform-qualified spec | **Open Q2**, subject to registry policy Q3 if accepted. |
| Isolated unsupported version syntax | `unsupported_lock_evidence`. |
| Broken spec framing or unsafe source boundaries | Whole-source failure. |

Missing or ambiguous evidence is never repaired from registry data. Requirement
text is retained but does not select a used version. Non-exact requirements
(including unconstrained, minimum, pessimistic, and compound ranges) are not
checked for satisfaction. For a single exact requirement, text equality can
confirm literal agreement; inequality does not prove Ruby semantic conflict.
**Open Q5** determines whether to trust the selected spec or conservatively
reject differing exact text. No Ruby version engine is authorized.

**Documented semantics:** Ruby's
[Gem::Version](https://raw.githubusercontent.com/rubygems/rubygems/master/lib/rubygems/version.rb)
compares canonical segments and transforms hyphenated version notation; textual
inequality is not semantic inequality (for example, trailing zero precision).
This is why an npm-style literal-conflict rule cannot be imported silently.

## Platform Policy

Reject multiple selected spec rows as ambiguous, including generic plus native
variants of the same version. Do not infer selection from host OS/architecture,
Dockerfile, `PLATFORMS`, environment variables, or `force_ruby_platform`.

**Open Q2:** a single platform-qualified lock record could be rejected by the
smallest generic-only subset, or accepted as an explicitly recorded artifact
without claiming it runs on the host. The latter still needs Q3.

**Open Q3:** RubyGems can expose multiple records for one version. The API's
platform selector establishes artifact identity, not a unique package-level
publication date. Generic-only comparison, same-artifact-class comparison, and
package-level canonicalization have different outcomes. No earliest/latest
cross-platform timestamp rule is selected implicitly. Ordinary locks are not
permission to pick the first registry record.

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

**Documented semantics:** the
[API reference](https://guides.rubygems.org/rubygems-org-api/) exposes version
numbers, platforms, prerelease flags, creation/build timestamps, and
version-specific metadata including yank state. A platform parameter selects a
specific record. Endpoint choice is not frozen by this draft; it must establish
those facts, including completeness for latest selection. An unrecognized or
truncated response is not a complete release history.

## Publication Timestamp Policy

Use version-record creation time (`created_at`, or an authoritatively equivalent
`version_created_at`) as the proposed ordinary publication timestamp. Parse
only valid timezone-aware timestamps, normalize to UTC, and preserve precision.
Do not use package creation/update time, lock mtime, gemspec date, `built_at`,
commit dates, or scan time as fallback. If equivalent authoritative fields
contradict each other, fail the dependency with `invalid_registry_response`.

**Documented semantics:** RubyGems.org's
[version model](https://raw.githubusercontent.com/rubygems/rubygems.org/master/app/models/version.rb)
assigns `built_at` from `spec.date` and contains special handling for the
2009-07-25 import date. This supports the ordinary creation-time candidate and
identifies a historical exception; it does not prove all creation dates are
original publication times. The website's authored-date fallback is not adopted
as publication authority.

Known uncertain publication time is unusable: the used record gets
`release_date_missing`; an uncertain latest candidate is excluded. If no eligible
stable candidate remains, use `no_stable_release`. This does not substitute a
different platform record unless Q3 explicitly authorizes canonicalization.

**Open Q4:** define the exact historical/import uncertainty predicate before
approval. No arbitrary cutoff or evidence-free historical exception is adopted.
The creation date alone on the import day cannot be assumed to be publication.
**Open Q3** also governs any same-version cross-platform timestamp mapping.

## Stable Release Eligibility

An eligible latest candidate must have supported identity/platform evidence,
authoritative `prerelease: false`, public availability (not yanked/unavailable),
and a usable publication timestamp under Q3/Q4. Prereleases never become latest
stable. Do not guess missing prerelease flags from version spelling. Do not
apply Gemfile requirements, Ruby compatibility, host platform, or version
ordering to filter latest candidates.

For the accepted record class/canonicalization selected by Q3, latest stable
is the eligible release with the greatest authoritative timestamp. Equal-time
different-version ties use lexicographically ascending exact version text as
a deterministic tie-break, not a version-order claim. Same-version record
multiplicity must be settled by Q3 before this tie-break applies.

Well-identified candidates lacking timestamps are ineligible. Missing or
invalid required identity, platform, prerelease, or availability semantics that
prevent safe classification make the package response
`invalid_registry_response`. Conflicting duplicate metadata for the same record
also fails that dependency; byte-equivalent duplicate records may be collapsed.
An empty eligible set is `no_stable_release`. A successful response must
establish a complete eligible history; response limits must never silently
select latest from a partial prefix.

## Used-Version Semantics

The exact locked version is repository evidence independently of today's
availability. A prerelease or now-yanked used version may be measured when its
exact accepted record and defensible historical timestamp remain available.
It does not thereby become a latest-stable candidate. This permission does not
require inventing a history-recovery mechanism or fetching a gem archive.

When the package is authoritatively absent, use `package_not_found`; when the
package exists but the exact used record cannot be found, use
`version_not_found`. Absent metadata cannot be reconstructed from requirement
text or a semantically similar version. If authoritative available metadata
exists but its time is missing/unsafe, use `release_date_missing`.
Multiple records for the used version are governed by Q3, not response order.

Arithmetic remains centralized and ecosystem-agnostic: timestamp difference
in seconds divided by `86400 * 365.25`, no grace period. Use the same canonical
timestamp for a version in used and latest roles. Identical used/latest version
identity produces exactly `0.0`; differing platform timestamps must not create
age for that identity. Negative timestamp anomalies clamp to zero and set
`timestamp_anomaly`; otherwise no anomaly is asserted. Aggregate only measured
rows, using existing sum, mean, median, and maximum semantics.

## Failure Model

Reasons below are proposed stable identifiers. Existing identifiers are reused
where their ecosystem-neutral meanings fit; human wording must name RubyGems or
Gemfile.lock rather than PyPI/package-lock/Yarn. No new Ruby-prefixed aliases
are needed. Q2/Q3/Q5 may narrow which cases use the proposed identifiers.

| Reason | Origin | Level / meaning | Availability class |
|---|---|---|---|
| `invalid_lockfile` | Reused | Unreadable or malformed recognized lock; structural conflicts | S-unknown |
| `unsupported_lockfile_format` | Reused | Unclassifiable lock, unsupported sections/semantics | S-unknown |
| `unsupported_dependency_name` | New | Isolated direct identity outside supported syntax | D-local |
| `unsupported_requirement` | Reused | Isolated direct requirement outside supported framing | D-local |
| `lock_version_missing` | Reused | Direct name lacks selected spec | D-local |
| `ambiguous_lock_evidence` | Reused | Multiple selected records or versions, including duplicate/platform variants | D-local |
| `unsupported_lock_evidence` | New | Isolated selected evidence cannot be interpreted under bounded version/platform policy | D-local |
| `unsupported_dependency_source` | Reused | Git/PATH/nonpublic/explicit pin or unattributable multiple-remotes source | D-local |
| `package_not_found` | Reused | Public authority establishes package absence | D-registry |
| `version_not_found` | Reused | Exact accepted used record absent | D-registry |
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

Precedence is structural source failure first, then isolated name/requirement
framing failure, unsupported source, selected-spec absence/multiplicity,
unsupported selected spelling/platform, and registry failure. Within metadata
validation, invalid response structure precedes missing used record, missing
used time, and lack of stable candidate. Diagnostic detail may clarify causes
without multiplying stable reasons. Q5's exact-text outcome remains unsettled;
this draft does not assert a semantic `declaration_lock_conflict` for Ruby.

## Coverage Semantics

| Case | RubyGems summary | Repository consequence |
|---|---|---|
| A. No Ruby source | Omitted entirely | Existing detected ecosystems determine results; no artificial zero Ruby entry. |
| B. Whole Ruby source rejected | Discovered=null, measured=null, coverage=null; all Ruby numeric aggregates null | Discovered=null and coverage=null; retain available measurements and their aggregates. |
| C. Valid scope with local failures | Discovered=N, measured=M, coverage=M/N for N>0 | Combine known scope and successful rows normally. |
| D. One registry failure | Same as C; failing row remains in N | Preserve other successes. |
| E. All three valid ecosystems | Each retains its own N, M, and coverage | Sum discovered counts and measured rows across ecosystems; coverage is total M/total N. |
| F. Ruby rejected, others succeed | Same as B | Successful PyPI/npm rows, measured count, and numeric aggregates remain available. |

If every detected source is unavailable, repository measured count is null.
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

Propose retaining **schema version 3**. Existing ecosystem-keyed objects,
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
assumes ordinary generic records with no platform multiplicity or historical
uncertainty, where the choices below agree.

```json
{
  "schema_version": 3,
  "dependency_scope": "direct",
  "ecosystems": ["rubygems"],
  "version_evidence": {
    "rubygems": {
      "declaration_source": "Gemfile.lock",
      "snapshot_source": "Gemfile.lock",
      "format": "gemfile_lock",
      "scope": "all_direct_locked"
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
      "version_source": "gemfile_lock"
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

Q3 may require additional artifact/platform evidence fields if artifact-level
comparison is selected. Additive fields can still fit v3, but their exact
contract must be specified before approval; the current examples do not
silently encode an artifact identity in `used_version`.

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
never 0%. Include original direct text on dependency failures.

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
not approved by this feature. Supporting a recorded single artifact (Q2) would
not authorize resolving a platform. New lock sections and historical metadata
reconstruction also require explicit scope decisions, not parser guesswork.

## Acceptance Criteria

These criteria test defined draft rules. They do not settle the alternative
outcomes in Q1–Q6. Affected criteria explicitly name the open decision; final
approval requires replacing those gaps with concrete outcome cases. Numbers
are stable draft references, not implementation tasks.

- [ ] **AC-01:** Directory scans with neither root Ruby file or Gemfile alone produce no RubyGems source, rows, requests, or summary; both files activate bounded lock discovery without interpreting Gemfile. Lock-only activation remains Q1.
- [ ] **AC-02:** Nested locks, alternate filenames, gemspecs, and direct-file arguments do not activate Ruby discovery; supplied local lock bytes are usable without inspecting Git history or installed state.
- [ ] **AC-03:** Supported section structure positively identifies `gemfile_lock`; optional BUNDLED WITH presence/version does not independently certify or reject a generation.
- [ ] **AC-04:** Unreadable/invalid text, malformed supported framing, conflict markers, duplicate singleton/source sections, duplicate direct rows, or missing required sections produce source-level `invalid_lockfile`, without partial Ruby measurements.
- [ ] **AC-05:** Unclassifiable content, unknown sections/fields, and recognized unsupported sections produce source-level `unsupported_lockfile_format`, without silently ignoring evidence that could alter scope or source interpretation.
- [ ] **AC-06:** Every supported DEPENDENCIES identity contributes once to direct discovered count regardless of group, local evidence failure, or registry failure; no group filter is reconstructed.
- [ ] **AC-07:** Specs and nested requirements not named in DEPENDENCIES create neither direct rows nor registry requests; tool/runtime metadata creates no dependency scope.
- [ ] **AC-08:** Package spelling is preserved and lock identity comparisons are exact; case, hyphen, underscore, and period variants are not silently aliased. Returned registry case differences remain Q6.
- [ ] **AC-09:** An isolated direct name outside the specified ASCII identity syntax is `unsupported_dependency_name` with no lookup; structurally unrecoverable identity rejects discovery.
- [ ] **AC-10:** One supported ordinary public selected spec supplies its exact version to lookup without resolving requirements or selecting another version; ordinary single-record metadata permits measurement when other requirements are met. Q3/Q5 govern their stated exceptional cases.
- [ ] **AC-11:** A direct name without a selected spec is `lock_version_missing` with no lookup; exact requirement text cannot substitute for the spec.
- [ ] **AC-12:** Multiple matching selected specs yield `ambiguous_lock_evidence` without lookup, including differing versions, identical duplicate rows, and same-version platform variants.
- [ ] **AC-13:** Git/PATH/nonpublic/multiple-remote/explicitly pinned direct evidence yields `unsupported_dependency_source` without public namesake substitution, even when another public spec shares the name.
- [ ] **AC-14:** Isolated unsupported selected-version spelling yields `unsupported_lock_evidence`; broken spec framing is a source error. Single platform-qualified evidence remains Q2.
- [ ] **AC-15:** Non-exact supported requirement text is preserved without satisfaction evaluation; unsupported isolated requirement syntax is `unsupported_requirement` with no lookup. Differing exact text is not asserted to be semantic incompatibility; its outcome remains Q5.
- [ ] **AC-16:** Host/platform/build configuration cannot select among lock or registry variants, change direct scope, or influence measurement results.
- [ ] **AC-17:** Direct bundler and tzinfo-data without ordinary selected specs remain counted and `lock_version_missing`; BUNDLED WITH and Gemfile conditions never replace or remove that evidence.
- [ ] **AC-18:** Ruby requests use only safely constructed public RubyGems.org HTTPS metadata URLs; repository/metadata links, redirects to other authorities, and credentials cannot redirect a lookup or alter identity.
- [ ] **AC-19:** Ruby requests enforce certificate and hostname verification, the existing CA selection precedence, positive finite timeout, and User-Agent; unusable trust never falls back to unverified TLS.
- [ ] **AC-20:** Successful metadata interpretation requires exact release identity, platform, authoritative prerelease status, latest availability, and complete eligible history; malformed or contradictory required metadata produces `invalid_registry_response`.
- [ ] **AC-21:** Publication time uses valid aware version-record creation timestamps in UTC with precision preserved; built_at, package-level times, lock dates, and scan time never substitute.
- [ ] **AC-22:** A known unsafe/missing used publication time produces `release_date_missing`; unsafe/missing candidate times are excluded. The historical uncertainty predicate remains Q4.
- [ ] **AC-23:** Multiple platform records for one version are never selected by response order or silently assigned a package timestamp; the accepted record class and canonicalization remain Q3.
- [ ] **AC-24:** Prerelease and yanked/unavailable records are excluded from latest stable; no local spelling heuristic substitutes for missing classification, and declared ranges/runtime compatibility do not filter latest.
- [ ] **AC-25:** Within the accepted Q3 record policy, latest uses greatest authoritative eligible timestamp, with ascending exact-version lexical tie-break; numeric version order and server latest labels do not override time.
- [ ] **AC-26:** No eligible stable candidate yields `no_stable_release`, even when exact used-version evidence exists.
- [ ] **AC-27:** A prerelease or yanked used version remains measurable when exact accepted metadata and a defensible timestamp exist; missing package or used record yields `package_not_found` or `version_not_found` respectively, without historical fabrication.
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
- [ ] **AC-38:** Schema remains v3 with Ruby ecosystem rubygems, measured version_source gemfile_lock, both artifact fields Gemfile.lock, accepted format gemfile_lock/rejected format null, and scope all_direct_locked, without changing existing field meanings.
- [ ] **AC-39:** Failures use the specified stable reasons and precedence, with direct text in unmeasurable and whole-source path/reason in source_errors; verbosity does not add JSON diagnostics or expose sensitive details.
- [ ] **AC-40:** Human output identifies RubyGems lock-snapshot/all-direct scope and uninterpreted groups without asserting production, current Gemfile, runtime, or verified-commit equivalence; counts and values agree with JSON.
- [ ] **AC-41:** Human failure output distinguishes the specified missing, unsupported, ambiguous/platform, malformed, registry, and timestamp cases, names whole-source paths, and renders unavailable coverage distinctly from 0%; verbose detail remains safe.
- [ ] **AC-42:** Normal directory CLI scanning requires no new Ruby flag, and --resolved cannot supply Ruby versions; completed partial, empty, and source-error reports exit 0 while existing usage/path and systemic exit categories remain 1 and 2.
- [ ] **AC-43:** Scanning never executes Ruby/Bundler/Gemfile/gemspec/repository code, installs or resolves dependencies, fetches Git/PATH/private content, reads private credentials, or modifies the target; runtime remains standard-library-only.
- [ ] **AC-44:** Ruby lookups enforce finite request/response budgets and timeouts; oversized/truncated history never produces a partial-history metric and uses the specified failure reason.
- [ ] **AC-45:** Ruby requests obey the documented API pacing limit and rate-limit responses without early Retry-After retries, unbounded retries, or alternate-authority evasion; fixed evidence/responses yield order-independent results.

### Draft bidirectional coverage audit

**Result: 45 numbered criteria.** Every defined normative behavioral rule has
coverage below; each criterion derives from the listed normative section(s).
Goals/non-goals restate the boundary rather than adding hidden behavior.
Unresolved alternatives are explicitly not claimed as complete acceptance
coverage: Q1–Q6 require outcome criteria during clarification before approval.

| Normative sections / rule family | Acceptance criteria (reverse mapping as well) |
|---|---|
| User Outcome; Source Recognition: snapshot meaning, root matrix, local artifacts | AC-01–02, AC-40 |
| Supported Gemfile.lock Boundary: recognition, framing, unsupported syntax | AC-03–05, AC-09, AC-14–15 |
| Direct Dependency Scope | AC-06–07 |
| Dependency Identity | AC-08–09, AC-18 |
| Lock Evidence Matching | AC-10–15, AC-39 |
| Platform Policy | AC-12, AC-14, AC-16, AC-23 |
| Special Dependencies | AC-13, AC-17 |
| Registry Authority | AC-18–20, AC-24, AC-44 |
| Publication Timestamp Policy | AC-21–23 |
| Stable Release Eligibility | AC-20, AC-24–26 |
| Used-Version Semantics and arithmetic | AC-27–30 |
| Failure Model | AC-04–05, AC-09, AC-11–15, AC-20, AC-22, AC-26–27, AC-31–34, AC-39 |
| Coverage Semantics | AC-30–36 |
| Mixed-Ecosystem Behavior | AC-31, AC-33, AC-36–37 |
| Ecosystem Identity; JSON Schema | AC-36, AC-38–39 |
| Human Output | AC-40–41 |
| CLI Behavior | AC-01–02, AC-19, AC-42 |
| Security Boundary; Non-Goals; Deferred Work | AC-02, AC-07, AC-13, AC-16, AC-18–19, AC-43 |
| Performance and Network Behavior | AC-07, AC-11–15, AC-20, AC-44–45 |

The author audit separates independently consequential rules (for example,
same-version zero versus negative-anomaly flagging, or per-source versus
repository availability). Multiple examples of the same outcome remain grouped.
Release testing, documentation migration, dogfood, commit sequencing, and
independent review are process obligations outside formal acceptance criteria.
No count target was used. This audit is not specification approval or an
independent review.

## Product Questions

### MUST RESOLVE BEFORE SPEC REVIEW CAN APPROVE

**Q1 — Does a root lock alone activate discovery?**

- Choice A: accept Gemfile.lock alone. Both scope and selection are retained
  there, and the selected human boundary measures a snapshot. Consequence:
  useful source archives/orphaned locks can be measured without Gemfile, but
  recognition makes no assertion of a currently runnable Ruby project.
- Choice B: require a companion root Gemfile solely as a presence marker.
  Discovery's observed projects had both files; this is a stricter root
  convention. Consequence: a sufficient snapshot may be ignored when Gemfile
  is absent; Gemfile contents still cannot define scope.
- Smallest human decision: accept lock-only roots or require companion presence.
  Both-present and Gemfile-only behavior is already defined. No ecosystem fact
  uniquely dictates this CLI recognition policy.

**Q2 — What happens to one platform-qualified selected spec?**

- Choice A: reject it with `unsupported_lock_evidence`. Ordinary generic records
  dominate discovery and this is the smallest supported subset. Consequence:
  lower coverage even where one artifact is unambiguous.
- Choice B: accept its explicit version/platform as retained artifact evidence,
  subject to Q3. Official lock/API semantics distinguish that artifact without
  host selection. Consequence: larger supported evidence/metadata contract,
  without permission to claim runtime applicability.
- Smallest human decision: generic-only lock acceptance or single-artifact
  acceptance. Multiple selected variants remain rejected under either choice.

**Q3 — What is the registry record class and canonical publication date?**

- Choice A: measure only `ruby` records for accepted generic locks; reject
  unsupported used record classes. This avoids cross-platform timestamp
  canonicalization and fits most observations. Consequence: latest means
  latest generic eligible release, not package-wide across native artifacts.
  Supporting Q2-B would require either extending this policy or choosing B/C.
- Choice B: measure an explicitly accepted used artifact against stable records
  of the same exact recorded platform class. The API can identify platforms.
  Consequence: artifact-specific freshness and output provenance are required;
  compatibility across platform spellings must not be inferred.
- Choice C: define a package-version date, such as earliest defensible
  publication across available platform records, and compare package versions.
  The user outcome is package age and no runtime selection is necessary.
  Consequence: an explicit canonicalization/availability rule is needed,
  including incomplete/yanked record sets; a late artifact must not silently
  redefine the version's first publication. Equal-version zero must survive.
- Smallest human decision: generic-class, exact-artifact-class, or package-level
  freshness. For C also decide whether incomplete same-version platform
  history is unmeasurable or whether available records suffice. Official API
  record identity does not uniquely establish package-level canonical time.
  If no class can be identified safely, fail closed; the concrete registry
  ambiguity outcome/reason must be finalized with this decision.

**Q4 — Which historical timestamps are unsafe?**

- Choice A: reject all creation timestamps whose UTC date is 2009-07-25 (and
  any explicitly uncertain record); accept other ordinary creation times.
  Source identifies that import day. Consequence: conservative rejection may
  also exclude genuine publications that day; it does not prove no other
  migration anomaly exists.
- Choice B: use the narrower official import condition (creation date equals
  import date and build date is on/before it) only to identify uncertainty,
  never as a fallback timestamp. Consequence: fewer rejections, but missing or
  suspect build dates need a defined conservative outcome.
- Choice C: reject the whole historical era through the import date unless
  separate public publication evidence proves otherwise. Consequence: strongest
  historical caution, reduced coverage, and no authorized archive scraping or
  invented timestamp recovery.
- Smallest human decision: approve an explicit uncertainty predicate and its
  missing-data behavior. All choices retain creation-time authority for ordinary
  records and prohibit built_at substitution. Research established the
  exception, not a uniquely justified product cutoff.

**Q5 — How should differing exact requirement text affect a selected spec?**

- Choice A: trust the lock selection for exact requirements as for ranges,
  retaining requirement text without consistency checking. The selected scope
  is the snapshot, and Ruby equivalence is not text equality. Consequence:
  genuine hand-edited conflicts may still be measured as recorded selections.
- Choice B: require literal agreement for a single exact requirement; otherwise
  report `unsupported_lock_evidence`, explaining that consistency was not
  established. Consequence: legitimate equivalent spellings can be rejected,
  but no semantic mismatch is falsely asserted and no version engine is needed.
- Smallest human decision: selection-only authority or conservative exact-text
  agreement. General satisfaction/equivalence evaluation is outside scope;
  `declaration_lock_conflict` is not proposed without a defensible conflict test.

### MAY RESOLVE DURING CLARIFICATION

**Q6 — May a case-only registry response name be accepted?**

- Choice A: require exact returned spelling. It matches the conservative lock
  identity rule and needs no aliasing. Consequence: a valid server lookup using
  its documented-in-source case-insensitive fallback can become
  `invalid_registry_response`.
- Choice B: allow ASCII case-only agreement at the public registry boundary,
  preserving lock spelling in output. Official server uniqueness/lookup logic
  supports this limited equivalence. Consequence: extra identity rule to test;
  lock-to-lock comparisons remain exact and punctuation never normalizes.
- Smallest human decision: strict response spelling or case-only registry
  equivalence. This does not block meaningful draft review, but must be settled
  before final approval. The naming guide alone is not a normalization rule.

### TECHNICAL / BELONGS IN PLAN.MD

Observable requirements above leave these implementation choices open:
endpoint selection and availability proof (including whether a bounded extra
used-version request is needed), finite byte/request limits and pacing
mechanism, static parsing/error-isolation structure, transport integration,
and fixture organization. No classes/modules, parser framework, cache, or
concurrency design is approved here. Implementation research that reveals a
new observable policy gap must return to specification rather than deciding
it in the plan or code.
