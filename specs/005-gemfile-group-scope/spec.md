# Feature 005: Bounded Static Gemfile Group Scope

## Status

APPROVED — focused independent verification completed in run `005-0007`.
Next gate: TECHNICAL PLANNING.

Drafted in run `005-0003` (parent `005-0002`); reconciled in run `005-0004`
(parent `005-0003`) on 2026-10-29 after human product authority resolved Q1–Q3.
The original draft required those decisions; this revision incorporates them,
including Q2's material change from qualified textual disagreement to refusal
to associate an exact version. H1–H3 in
[discovery.md](discovery.md#human-product-decision) remain settled and preserved.
Independent approval is recorded in [reviews.md](reviews.md) for run `005-0007`.
No plan, task graph, or implementation has begun.

## Problem and user outcome

All-direct lock measurement cannot answer which declared groups a dependency
belongs to. A user explicitly selects one or more declared Gemfile groups and
obtains dependency ages using the supplied root Gemfile and Gemfile.lock.
The result describes these supplied files only. It MUST NOT claim historical
coherence, installed/deployed dependencies, runtime loading, or a reconstructed
Bundler environment. A group named `production` has no special meaning.
There is no implicit production mode or automatic inclusion of `default`.

H1 selects bounded static group scope; H2 selects measurement rather than merely
annotation; H3 accepts conservative rejection. No general Ruby interpretation,
additional ecosystem, private registry support, resolver, or metric change is
part of this feature.

## Current baseline and regression boundary

[ SPEC.md ](../../SPEC.md) and approved Features
[002](../002-npm-support/spec.md), [003](../003-yarn-lock-evidence/spec.md), and
[004](../004-rubygems-support/spec.md) remain governing outside explicitly
requested scoped Ruby behavior.

| Area | Contract preserved |
|---|---|
| Python/PyPI | requirements declarations; exact pins or supplied resolved snapshot; snapshot-only names do not enlarge scope. |
| npm | Root package.json dependencies excluding optional overlap; package-lock v2/v3 exact evidence. |
| Yarn Classic | Existing v1 evidence and simultaneous-lock conflict policy; no expanded npm scope. |
| Ordinary Ruby | Root Gemfile.lock all-direct DEPENDENCIES; Gemfile absent, present, or invalid has no effect and is not inspected. Direct-file arguments do not activate Ruby. |
| Mixed scanning | Independent ecosystems, distinct same-name identities, successful sibling rows survive source failures. |
| Authority | Feature 004 public-source gate, platform identity, observable publication history, verified TLS and request limits. |
| Reporting | Schema v3, source_errors versus unmeasurable, known versus unknown denominators, existing human explanations and exit categories. |

Inspected witnesses: `ruby_source_result` and public authorization in
`libyears/rubygems.py` (also documented in discovery); mixed orchestration and
aggregation in `libyears/scan.py`; CLI exits in `libyears/cli.py`;
`test_lock_only_and_gemfile_presence_have_identical_unchanged_results`,
`test_only_root_lock_is_read`, and the mixed availability matrix tests.
This draft does not claim that tests were executed.

## S1 — Activation, inputs, and completeness

Explicit group selection MUST be required. Without it, all existing behavior
MUST remain unchanged. A scoped request applies only to Ruby in a directory
scan; Python and npm retain their scopes. `--resolved` remains Python-only.
The sole selection option is repeatable `--ruby-group GROUP`. Each occurrence
supplies one exact case-sensitive group name in the supported symbol-name
alphabet defined below; empty or malformed values and missing values are usage errors.
Duplicate requested names deduplicate. There is no comma-separated mini-language,
alias, implicit default selection, or production mode. `default` must be selected
explicitly, as any other group.

Examples: `python -m libyears . --ruby-group default` and
`python -m libyears . --ruby-group default --ruby-group production`.

Only the supplied directory's exactly named root `Gemfile` and `Gemfile.lock`
participate. No recursive discovery, parent search, alternate file names,
Gemfile inclusion, gemspec reading, config inspection, or environment-derived
membership is permitted. Direct-file requests MUST NOT activate Ruby; group
selection with a direct-file argument is a usage error.
Scoped reads MUST remain within the supplied root; symlinks resolving outside
it are rejected without reading their targets. This does not
retroactively change ordinary Feature 004 scanning.

The completeness rule is unconditional: unsupported or ambiguous constructs
that can materially affect requested membership MUST prevent reporting a
partial population as complete. Familiar gem lines inside an unknown program
are not sufficient evidence. No Ruby/Bundler execution may establish scope.

### Approved closed static subset

The following is an exhaustive positive boundary, not a list of suggestive
examples. Everything outside it rejects the entire scoped Gemfile, even in an
unselected group. This deliberately avoids claims of proving arbitrary Ruby
irrelevant. A later expansion requires specification review.

- UTF-8 text with LF or CRLF, horizontal whitespace, blank lines, and `#`
  comments outside strings. One statement per physical line; indentation is
  cosmetic. No semicolons, continuation, parenthesized calls, or multiline strings.
- Literals: single- or double-quoted strings without escapes, interpolation,
  embedded newlines, or delimiter characters. Group symbols are colon followed
  by an ASCII letter/underscore and then ASCII letters/digits/underscores.
  Group identity is exact and case-sensitive. Empty names are rejected.
- One top-level `source STRING` declaration is required. Its literal is inert
  authority evidence, never a request destination. A nonpublic value is
  recognizable but cannot authorize measurement.
- `gem STRING` optionally followed by comma-separated requirement strings and
  then recognized keyword options. Names and requirement strings must satisfy
  Feature 004's bounded identity and requirement framing. No satisfaction or
  equivalence evaluation occurs.
- Recognized gem options: `group:` or `groups:` with one symbol or a nonempty
  bracketed comma-separated list of symbols; `require:` with true, false, or
  a literal string. Repeated keys, simultaneous group/groups, unknown keys,
  and nonliteral values reject scope. `require:` does not change membership.
- `group SYMBOL [, SYMBOL ...] [, optional: true|false] do` begins a block;
  a standalone `end` closes it. Only gem declarations, comments, and blank
  lines occur inside. Empty blocks are valid. Nested groups are rejected in
  this initial feature rather than assigned speculative semantics.
- No other statements or expressions are supported: notably conditions,
  assignments, method definitions/calls, loops, platform blocks/options,
  install_if, eval_gemfile, gemspec, Ruby directives, source blocks, path/git
  options or blocks, and arbitrary Ruby. Rejection does not assert invalid Ruby.

Malformed framing and unsupported syntax both make scoped population
unavailable; diagnostics distinguish malformed evidence from an unsupported
construct. Parsing must consume the complete file before claiming completeness.
A resource-limit rejection likewise cannot return partial scope.

| Scoped input state | Required result |
|---|---|
| Gemfile missing, unreadable, unsafe, or rejected | Scope unavailable, source error, no Ruby rows or lookup. |
| Complete Gemfile, requested name not established | Requested scope unavailable; no partial union of other requested groups. |
| Complete Gemfile, established empty selection | Known empty population, not unknown scope. |
| Complete Gemfile, lock absent | Retain known selected names as unmeasurable; never derive exact versions from declaration pins. |
| Complete Gemfile, lock rejected | Preserve known selected denominator but measurement unavailable; source error, no fabricated dependency failures. |

## S2 — Membership and selection

Bundler's [official group guide](https://guides.rubygems.org/groups/) documents
ungrouped default membership, overlapping groups, literal group options, and
optional groups. Its installation/configuration and loading behavior is separate
from declaration membership. The version-pinned
[3.6.9 DSL](https://raw.githubusercontent.com/rubygems/rubygems/v3.6.9/bundler/lib/bundler/dsl.rb)
provides semantic evidence, not permission to evaluate Ruby or copy its full
language. Sources verified 2026-10-29.

The approved membership rules are:

| Declaration | Membership |
|---|---|
| Top-level gem without group options | default |
| Top-level gem with explicit groups | Exactly those groups; default is not added. |
| Gem inside group block | Block groups union any explicit gem groups. |
| Optional group | Same declared membership; selection does not consult installation configuration. |

Selecting several groups takes their union. A dependency is counted once even
if several selected memberships match. Repeated requested names do not inflate
counts. `default` is always an established implicit group after complete static
recognition, including when empty. Other names are established by a supported
block header (even empty) or gem group option. An unknown requested name is not
an empty group. A group whose dependencies all lack measurements is nonempty
with zero measured, not empty or unknown.

Duplicate gem declarations anywhere in the file MUST be rejected, even
identical ones or ones in separate groups. Distinct declarations cannot silently
merge incompatible requirements or sources. This is a conservative product
boundary, not a claim that Bundler always rejects duplicates.

Example: ungrouped `rack`, `rake` in `group :test, :development`, and an empty
`:bench` block yield `{rack}` for default, `{rake}` for test, `{rack, rake}`
for default+development, empty for bench, and unavailable for unknown `prod`.

## S3 — Supplied evidence association and failures

Gemfile membership MUST NOT authorize a lock source. Exact case-sensitive
names associate declarations with direct `DEPENDENCIES` and selected specs;
no punctuation normalization, fuzzy matching, or transitive-only substitution
is allowed. Existing Feature 004 authorization and ambiguity rules apply
independently. Private/GIT/PATH/multiple-remotes/explicit pins MUST NOT obtain
public namesake metadata, even if another public spec shares the name.
A nonpublic Gemfile source also cannot be rehabilitated by a public lock.

The approved association policy is:

| Evidence | Result |
|---|---|
| Selected declaration, matching direct lock row, identical requirement evidence and authorized selection | Measure exact lock version with retained provenance. |
| Selected declaration with public Gemfile source absent from DEPENDENCIES | Count once, unmeasurable; no transitive spec or declaration pin fallback. |
| Matching direct row lacks selected spec | Existing lock_version_missing. |
| Lock-only name or declaration outside selected groups | No scoped row, count, or lookup. Still validate entire lock structure. |
| Different declaration/lock requirement text | Count once as unmeasurable with declaration_lock_requirement_mismatch; do not associate the exact lock version or perform registry lookup. Retain both safe requirement values; infer no equivalence or semantic incompatibility. |
| Duplicate direct lock identities / rejected lock structure | Existing whole-lock rejection; no partial lock salvage. |
| Isolated ambiguous/unsupported selection | Existing dependency-level reason; selected denominator remains known. |

Equal name sets or requirement text MUST NOT assert that files came from one
resolution, commit, or historical moment. Selected versions establish package
version, not runtime compatibility. Publication and arithmetic remain Feature
004's supported observable history and existing metric, including exact 0.0
for used=latest and flagged clamping for timestamp anomalies.

Failure precedence is: unavailable Gemfile scope, then unknown requested
group, then unavailable lock. After whole-lock acceptance, nonpublic Gemfile
source authority precedes missing direct lock identity: report
`unsupported_dependency_source`, retain the known selected denominator and make
no lookup, even when the selected name has no direct lock row. Otherwise existing
lock-local validation precedence applies.
Once both requirement values
have supported framing and public source authority is established, textual
mismatch precedes selected-spec/version and registry failures. Missing direct
lock identity precedes mismatch (there is no pair to compare). Existing
unsupported name/requirement/source failures precede mismatch; the Feature 004
ordering among those failures is preserved. No local failure permits lookup.
Missing lock with known nonempty scope yields one missing-evidence failure per
selected name. A rejected lock yields a source error and unavailable measurement,
including for a known empty selection; an absent lock with known empty selection
needs no measurement and yields an ordinary empty report. These distinctions
are approved by human Q2.

## S4 — Public reporting contract

Human output MUST name selected declared groups and supplied Gemfile/lock
sources; distinguish empty, unavailable, and wholly unmeasurable populations;
explain unsupported evidence safely; and state that declaration membership does
not establish installed/deployed/runtime scope or historical coherence.
Feature 004's observable-publication limitation remains visible. Diagnostics
MUST NOT expose private URLs, credentials, arbitrary source text, or traces.

Schema v3 MUST preserve existing fields and meanings for ordinary scans.
Scoped-only fields below are omitted entirely for ordinary scans. Scoped
activation always includes `rubygems` in evidence and ecosystem summaries,
even when inputs are unavailable. Existing top-level structures are unchanged.

`version_evidence.rubygems` has these deterministic values:

| Field | Scoped presence/value |
|---|---|
| declaration_source | Always `Gemfile`; identifies the requested input, not successful recognition. |
| snapshot_source | Always `Gemfile.lock`; identifies the requested input, even if missing. |
| scope | Always `selected_declared_groups`; denotes requested scope, not completeness. |
| requested_groups | Always sorted unique requested names, exact case preserved. |
| format | Always present; `gemfile_lock` only after whole-lock acceptance, otherwise null. No lock recognition claim if processing stops at a higher-priority failure. |
| publication_basis | Existing `earliest_admissible_supported_observable`, unchanged. |

No new generic status structure is added: source_errors, nullable summaries,
format and row reasons identify unavailable evidence. A Gemfile/unknown-group
failure prevents lock processing; no lock error is invented in that case.

Each scoped row in `dependencies` or `unmeasurable` adds a `gemfile_evidence`
object with `declared_groups` (sorted unique full memberships, including any
unselected memberships) and `declaration_requirements` (ordered array of the
bounded literal requirement string contents). `lock_requirement` is included
in that same object only for a matching direct row in an accepted lock with
supported safe requirement framing; it is its bounded requirement text, or null
when that row has no explicit requirement. An existing direct requirement that
fails supported safe framing retains dependency-level `unsupported_requirement`,
the known denominator and no-lookup behavior; omit `lock_requirement` and never
copy or echo the unsupported text into scoped JSON or human output. Preserve
safely reportable declaration metadata. Do not reject the whole lock for this
isolated failure. Null remains reserved for known absence.
No requirements yields `declaration_requirements: []`, which means known absence,
not unavailable evidence. Missing lock/direct row omits `lock_requirement`.
Rejected lock produces no rows and thus no salvaged requirement evidence.
These fields contain no arbitrary source lines, options, or private URLs.

For comparison only, declaration requirement strings are joined in supplied
order with literal `, `; zero strings corresponds to absent requirement (null).
Compare this value with the direct lock requirement text extracted by existing
bounded lock framing, without additional whitespace, operator, term-order, or
version normalization. Null equals null only. Array order and literal contents
are preserved. Even apparently equivalent `>= 0` and absence differ: report
`declaration_lock_requirement_mismatch`, never a semantic conflict or failed
satisfaction claim. Both safe values remain in `gemfile_evidence`; no exact
version provenance or selected artifacts are attached to a mismatch row.
Existing `declared` on scoped unmeasurable rows is the safe gem name, optionally
followed by the joined declaration requirements in parentheses, following the
lock declaration framing. It is not a copy of arbitrary Gemfile text.

Authorized measured rows retain `version_source: gemfile_lock` and existing
`rubygems_evidence` selected/publication artifacts. Other unmeasurable rows
retain existing Feature 004 artifact rules only after authorized association;
scoped declaration metadata never substitutes for exact-version evidence.

Stable new failure identifiers and locations are:

| Condition | Record / reason |
|---|---|
| Missing Gemfile | source_errors, source `Gemfile`, `gemfile_missing` |
| Unreadable, nonregular, invalid UTF-8 or malformed Gemfile | source_errors, source `Gemfile`, `invalid_gemfile` |
| Out-of-root Gemfile target | source_errors, source `Gemfile`, `unsafe_gemfile` |
| Unsupported constructs, nested groups or resource-limit rejection | source_errors, source `Gemfile`, `unsupported_gemfile_syntax` |
| Duplicate gem declarations | source_errors, source `Gemfile`, `duplicate_gemfile_declaration` |
| Any unknown requested group | source_errors, source `Gemfile`, `unknown_ruby_group` |
| Missing lock, nonempty known scope | unmeasurable, each selected name, `lockfile_missing` |
| Selected name with public Gemfile source absent from accepted direct lock scope | unmeasurable, `lock_dependency_missing` |
| Differing supported requirement evidence | unmeasurable, `declaration_lock_requirement_mismatch` |

Rejected/unreadable/nonregular/unsafe lock uses existing Feature 004 source
reasons (`invalid_lockfile` for unsafe access), source `Gemfile.lock`. Other
lock-local and registry reasons remain unchanged. Nonpublic Gemfile source
produces `unsupported_dependency_source` for each selected identity after
whole-lock acceptance, including when its direct lock identity is missing,
without public lookups. Human output explains that the Gemfile source is
nonpublic and unsupported without exposing its value. Unavailable-lock
precedence remains unchanged. Whole-file recognition errors precede unknown group; for
multiple recognition defects the first physical-line defect wins, with
whole-file completion defects reported after line defects. Unknown group yields
one source error irrespective of how many requested names are unknown. Later
input errors are not reported when earlier precedence prevents their inspection.

Human output names the same selected groups, memberships and safely available
requirement evidence, and explains mismatch as “textual requirement evidence
differs; equivalence not inferred.” It does not say requirements conflict or
are semantically incompatible. Missing/rejected sources are labeled unavailable,
not accepted or empty. Human counts, reasons and provenance agree with JSON;
verbose safe diagnostics remain outside JSON.

Known complete scope counts selected identities only. Unmeasurable dependencies
remain in its denominator, excluded from numerical aggregates. Requirement
mismatch therefore counts as discovered but not measured, just like other
dependency-level failures; a population consisting only of mismatches has
zero measured and 0% coverage. For N>0 available
measurement, coverage is M/N, including 0%. Empty available scope has counts
0/0, null coverage, total 0.0, and null mean/median/max. Unavailable discovery
has null counts/coverage and Ruby aggregates. The known-scope rejected-lock
case retains N but null measured/coverage and unavailable Ruby aggregates.
Repository successful sibling rows/aggregates survive; any unavailable source
makes repository coverage null, and any unknown denominator makes repository
discovered null. Repository measured count is null only if every detected source
is unavailable, following Feature 004. Group selection explicitly requests Ruby
reporting even when its inputs are missing; it cannot silently disappear.

Completed reports, including source errors, retain exit 0. Usage/path errors
retain exit 1; systemic failures retain exit 2. No coverage percentage alone
changes exit status. Invalid selection syntax or a direct-file scoped target
is a usage error.
Valid activation followed by evidence problems is a completed reporting outcome,
not a usage error.

## Security and authority

Static analysis only: MUST NOT execute Ruby, Bundler, Gemfile, gemspecs or other
repository code, install/resolve packages, inspect credentials/configuration,
fetch private content/archives, or modify targets. Standard-library-only runtime
and registry adapter isolation remain mandatory. Verified HTTPS, certificate
and hostname verification, explicit trust precedence, fixed public authority,
redirect rejection, request limits and pacing remain Feature 004's contract.
No environment-specific operational details or new trust exceptions are added.

## S5 — Acceptance criteria

Unchecked criteria describe future observable acceptance, not completed tests.
All criteria describe approved observable behavior; none await Q1–Q3 decisions.

- [ ] **AC-01:** No group request produces the existing all-direct Ruby result whether Gemfile is absent, invalid, or present; it is not read.
- [ ] **AC-02:** A supported simple public declaration in a selected group associates with its direct lock selection and produces the expected age through `--ruby-group GROUP`; names are case-sensitive (`test` does not select `Test`).
- [ ] **AC-03:** Ungrouped declarations belong to default; only explicit `--ruby-group default` selects default; no selection implicitly includes default or production.
- [ ] **AC-04:** One declaration in multiple groups is included once when any selected membership matches.
- [ ] **AC-05:** Selecting multiple groups produces their union, with repeated selections having no effect.
- [ ] **AC-06:** An established empty block or empty default yields known zero counts and null coverage, not an unknown-group error.
- [ ] **AC-07:** One unknown requested group makes the entire requested scope unavailable, without reporting a partial union.
- [ ] **AC-08:** Unsupported Ruby, interpolation, conditional declarations, trailing syntax, and unsupported code inside unselected groups reject completeness; recognized lines do not produce partial rows.
- [ ] **AC-09:** Optional declarations use declared membership without consulting installation settings; nested groups are rejected.
- [ ] **AC-10:** Duplicate declarations reject scope rather than double count or merge; duplicate lock identities retain Feature 004 rejection.
- [ ] **AC-11:** Missing/unreadable/unsafe Gemfile reports unavailable selected scope and performs no Ruby lookup.
- [ ] **AC-12:** Missing lock retains known selected names as unmeasurable; declaration pins never substitute for exact lock evidence.
- [ ] **AC-13:** A selected declaration absent from lock direct scope is counted and unmeasurable even if a transitive spec matches.
- [ ] **AC-14:** Lock-only and unselected names produce no scoped rows or lookups; textual requirement mismatch counts once as unmeasurable with `declaration_lock_requirement_mismatch`, preserves both bounded values, associates no exact version and makes no lookup, satisfaction, equivalence, incompatibility or coherence claim.
- [ ] **AC-15:** A rejected lock preserves known declaration count but makes measurement unavailable; unsupported isolated selection preserves the denominator with a dependency failure.
- [ ] **AC-16:** Private, pinned, GIT/PATH, uncertain, or multiple-remote evidence cannot use a public namesake; a nonpublic declaration source cannot be overridden by a public lock.
- [ ] **AC-17:** Known wholly unmeasurable selected scope reports 0% coverage; empty and unavailable reports remain observably distinct.
- [ ] **AC-18:** A failing scoped Ruby source preserves successful Python/npm rows and applies existing repository unknown-denominator rules.
- [ ] **AC-19:** Ordinary PyPI, package-lock, Yarn Classic conflict/evidence, and mixed identity behavior remain unchanged.
- [ ] **AC-20:** Human output names selected groups, evidence sources and limitations, explains safe failures without echoing unsupported direct requirement text, preserves safe declaration metadata, and agrees with JSON counts and values.
- [ ] **AC-21:** Schema v3 distinguishes Gemfile membership from lock version evidence, retains publication artifacts, obeys every scoped field presence/omission rule in S4 (including missing/rejected inputs and omission of `lock_requirement` for unsupported safe framing, with null reserved for known absence), retains both safe mismatch values, leaves ordinary JSON unchanged and adds no verbose human diagnostics.
- [ ] **AC-22:** No report labels production as deployed state or claims supplied-file historical coherence, installation, or runtime compatibility.
- [ ] **AC-23:** Scans execute no Ruby/Bundler/project code, install/resolve nothing, read no credentials, and leave targets unchanged.
- [ ] **AC-24:** Only root supplied files participate; nested/parent files, includes, gemspecs and out-of-root symlink targets are not read; direct-file arguments do not activate Ruby.
- [ ] **AC-25:** Existing TLS verification, trust precedence, public authority, redirect and transport limits remain enforced.
- [ ] **AC-26:** Scoped ages preserve Feature 004 dates, latest selection, arithmetic, same-version zero and flagged anomaly rules.
- [ ] **AC-27:** Completed empty/partial/source-error reports exit 0; missing/malformed option values, comma lists, direct-file scoped targets and path errors exit 1 and systemic failures exit 2.
- [ ] **AC-28:** Source failures and dependency failures use distinct machine-readable records with safely known provenance and deterministic precedence. Evidence includes an accepted lock missing a selected nonpublic-source declaration’s direct identity (`unsupported_dependency_source`, known denominator, no lookup), and an accepted lock with a matching direct requirement failing safe framing (`unsupported_requirement`, known denominator, no lookup, omitted `lock_requirement`, no unsupported text in scoped JSON/human output, safe declaration metadata retained). Unavailable-lock precedence and ordinary all-direct output remain unchanged.

Before convergence, acceptance evidence must include deterministic offline cases
for every criterion and an explicitly authorized real-root supplied-file example
whose expected selected population is independently established. Record rejected
constructs and evidence limitations without claiming general application coverage.
No particular external repository is authorized here. Optional live registry
smoke is separate from deterministic correctness and cannot replace it.

## Product questions and decision traceability

### RESOLVED human decisions — 2026-10-29

Human product authority supplied these decisions in the initial prompt for
`005-0004`, after the completed `005-0003` draft. They supersede that draft's
proposal markers without changing the historical discovery record.

- **Q1 — RESOLVED:** Closed static subset, whole-file consumption/rejection,
  duplicate and nested-group rejection, exact memberships, implicit membership
  in default (explicit selection required), and root/symlink boundaries approved.
  Conservative rejection is accepted; expansion needs new evidence/spec review.
- **Q2 — RESOLVED WITH REVISION:** Association, availability and failure ordering
  approved, except differing textual requirement evidence MUST prevent exact
  association and yield a dependency-level unmeasurable result. S3/S4 specify
  the stable mismatch reason, retained evidence and precedence. No semantic
  satisfaction or compatibility evaluation is authorized.
- **Q3 — RESOLVED:** Repeatable `--ruby-group GROUP`, directory-only activation,
  exact names, deduplication, explicit default and no production mode approved.
  Additive schema-v3 direction approved; S4 finalizes field names, nesting,
  omission/null rules, reasons and unavailable-input provenance under that authority.

Remaining consequential product questions: none identified.
Specification readiness: **APPROVED** after focused independent verification
in run `005-0007`; next gate **TECHNICAL PLANNING**.

### IMPLEMENTATION / PLANNING QUESTION

Parser organization, internal records, module ownership, bounded resource
implementation, fixture layout, test decomposition and task ordering belong to
planning after approval. They must implement the resolved Q1–Q3 contract
without broadening it.
No architecture is selected here.

| Requirement family | Authority / decision origin | Acceptance |
|---|---|---|
| Selected declared measurement and limited claims | Human H1/H2; discovery F2/F3 | AC-02–07, AC-20, AC-22 |
| Completeness and static safety | Human H3; approved Q1 | AC-08–11, AC-23–24 |
| Membership/duplicates | Discovery S2; approved Q1 | AC-03–10 |
| Association/failures | Human authority boundary; Feature 004; approved Q2 with mismatch revision | AC-12–18, AC-28 |
| Default and ecosystem compatibility | Human compatibility decision; SPEC and Features 002–004 | AC-01, AC-18–19 |
| Public interface/provenance | Discovery S4; schema-v3 baseline; approved Q3; finalized S4 | AC-20–21, AC-27–28 |
| Coverage | SPEC/Feature 004; approved Q2 for new missing-input cases | AC-06–07, AC-12–18 |
| Security and arithmetic | AGENTS, SPEC, Feature 004 | AC-16, AC-23–26 |

Author check: H1–H3 preserved; no deployment claim or Ruby/Bundler execution;
all-direct default preserved; unsupported scope fails closed; criteria have
stable identifiers; Q1–Q3 resolved and public fields finalized; no consequential
product question remains. No roadmap
coherence defect identified. This is an author audit, not independent review.
