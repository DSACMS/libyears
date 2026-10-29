# Feature 005: Bounded Static Gemfile Group Scope

## Status

DRAFT — HUMAN DECISION REQUIRED before specification approval.

Run: `005-0003`; parent: `005-0002`. No independent approval, plan, task graph,
or implementation is implied. H1–H3 in [discovery.md](discovery.md#human-product-decision)
are settled. Questions Q1–Q3 below concern the remaining observable contract.
Normative requirements inherited from those decisions apply unconditionally.
New proposals explicitly marked Q1–Q3 are reviewable candidates, not silently
approved requirements. Acceptance criteria for those proposals are conditional
on their resolution and must be reconciled before approval.

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
Exact option spelling is Q3, not an implementation decision.

Only the supplied directory's exactly named root `Gemfile` and `Gemfile.lock`
participate. No recursive discovery, parent search, alternate file names,
Gemfile inclusion, gemspec reading, config inspection, or environment-derived
membership is permitted. Direct-file requests MUST NOT activate Ruby; Q3
proposes rejecting group selection with a direct-file argument as usage error.
Scoped reads MUST remain within the supplied root; Q1 proposes rejecting
symlinks resolving outside it, without reading their targets. This does not
retroactively change ordinary Feature 004 scanning.

The completeness rule is unconditional: unsupported or ambiguous constructs
that can materially affect requested membership MUST prevent reporting a
partial population as complete. Familiar gem lines inside an unknown program
are not sufficient evidence. No Ruby/Bundler execution may establish scope.

### Q1 proposed closed static subset

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
  this initial proposal rather than assigned speculative semantics.
- No other statements or expressions are supported: notably conditions,
  assignments, method definitions/calls, loops, platform blocks/options,
  install_if, eval_gemfile, gemspec, Ruby directives, source blocks, path/git
  options or blocks, and arbitrary Ruby. Rejection does not assert invalid Ruby.

Malformed framing and unsupported syntax both make scoped population
unavailable; diagnostics distinguish malformed evidence from an unsupported
construct. Parsing must consume the complete file before claiming completeness.
A resource-limit rejection likewise cannot return partial scope.

| Scoped input state | Required result / proposed Q2 detail |
|---|---|
| Gemfile missing, unreadable, unsafe, or rejected | Scope unavailable, source error, no Ruby rows or lookup. |
| Complete Gemfile, requested name not established | Requested scope unavailable; no partial union of other requested groups. |
| Complete Gemfile, established empty selection | Known empty population, not unknown scope. |
| Complete Gemfile, lock absent | Q2: retain known selected names as unmeasurable; never derive exact versions from declaration pins. |
| Complete Gemfile, lock rejected | Q2: preserve known selected denominator but measurement unavailable; source error, no fabricated dependency failures. |

## S2 — Membership and selection

Bundler's [official group guide](https://guides.rubygems.org/groups/) documents
ungrouped default membership, overlapping groups, literal group options, and
optional groups. Its installation/configuration and loading behavior is separate
from declaration membership. The version-pinned
[3.6.9 DSL](https://raw.githubusercontent.com/rubygems/rubygems/v3.6.9/bundler/lib/bundler/dsl.rb)
provides semantic evidence, not permission to evaluate Ruby or copy its full
language. Sources verified 2026-10-29.

Q1 proposes these exact membership rules for the subset:

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

Q1 proposes rejecting duplicate gem declarations anywhere in the file, even
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

Q2 proposes the following association policy:

| Evidence | Result |
|---|---|
| Selected declaration, matching direct lock row and authorized selection | Measure exact lock version with retained provenance. |
| Selected declaration absent from DEPENDENCIES | Count once, unmeasurable; no transitive spec or declaration pin fallback. |
| Matching direct row lacks selected spec | Existing lock_version_missing. |
| Lock-only name or declaration outside selected groups | No scoped row, count, or lookup. Still validate entire lock structure. |
| Different declaration/lock requirement text | Retain both, identify textual difference, do not evaluate satisfaction or claim consistency. |
| Duplicate direct lock identities / rejected lock structure | Existing whole-lock rejection; no partial lock salvage. |
| Isolated ambiguous/unsupported selection | Existing dependency-level reason; selected denominator remains known. |

Equal name sets or requirement text MUST NOT assert that files came from one
resolution, commit, or historical moment. Selected versions establish package
version, not runtime compatibility. Publication and arithmetic remain Feature
004's supported observable history and existing metric, including exact 0.0
for used=latest and flagged clamping for timestamp anomalies.

Q2 proposes failure precedence: unavailable Gemfile scope, then unknown requested
group, then unavailable lock, then existing lock-local/registry precedence.
Missing lock with known nonempty scope yields one missing-evidence failure per
selected name. A rejected lock yields a source error and unavailable measurement,
including for a known empty selection; an absent lock with known empty selection
needs no measurement and yields an ordinary empty report. These distinctions
require explicit approval because H1–H3 do not settle them.

## S4 — Public reporting contract

Human output MUST name selected declared groups and supplied Gemfile/lock
sources; distinguish empty, unavailable, and wholly unmeasurable populations;
explain unsupported evidence safely; and state that declaration membership does
not establish installed/deployed/runtime scope or historical coherence.
Feature 004's observable-publication limitation remains visible. Diagnostics
MUST NOT expose private URLs, credentials, arbitrary source text, or traces.

Schema v3 MUST preserve existing fields and meanings for ordinary scans.
Scoped reports MUST distinguish membership evidence from version evidence.
Q3 proposes additive `version_evidence.rubygems` metadata:
`declaration_source: Gemfile`, `snapshot_source: Gemfile.lock`,
`scope: selected_declared_groups`, and sorted unique `requested_groups`.
Existing `format` describes lock recognition, not Gemfile recognition;
`publication_basis` remains unchanged. Rows retain `version_source: gemfile_lock`
and existing Ruby artifact provenance. Add declared memberships and declaration
and lock requirement evidence without replacing existing artifact fields.
Exact field names, null/omission rules, failure reason identifiers, and rejected
input provenance MUST be settled under Q3 before approval, not left to planning.
Verbose diagnostics MUST remain outside JSON.

Known complete scope counts selected identities only. Unmeasurable dependencies
remain in its denominator, excluded from numerical aggregates. For N>0 available
measurement, coverage is M/N, including 0%. Empty available scope has counts
0/0, null coverage, total 0.0, and null mean/median/max. Unavailable discovery
has null counts/coverage and Ruby aggregates. Q2's known-scope rejected-lock
case retains N but null measured/coverage and unavailable Ruby aggregates.
Repository successful sibling rows/aggregates survive; any unavailable source
makes repository coverage null, and any unknown denominator makes repository
discovered null. Repository measured count is null only if every detected source
is unavailable, following Feature 004. Group selection explicitly requests Ruby
reporting even when its inputs are missing; it cannot silently disappear.

Completed reports, including source errors, retain exit 0. Usage/path errors
retain exit 1; systemic failures retain exit 2. No coverage percentage alone
changes exit status. Q3 must fix invalid selection syntax as a usage error.

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
Q references explicitly identify proposed expectations awaiting resolution.

- [ ] **AC-01:** No group request produces the existing all-direct Ruby result whether Gemfile is absent, invalid, or present; it is not read.
- [ ] **AC-02:** A supported simple public declaration in a selected group associates with its direct lock selection and produces the expected age (Q1).
- [ ] **AC-03:** Ungrouped declarations belong to default; selecting another group does not implicitly include default (Q1).
- [ ] **AC-04:** One declaration in multiple groups is included once when any selected membership matches (Q1).
- [ ] **AC-05:** Selecting multiple groups produces their union, with repeated selections having no effect (Q1).
- [ ] **AC-06:** An established empty block or empty default yields known zero counts and null coverage, not an unknown-group error (Q1/Q2).
- [ ] **AC-07:** One unknown requested group makes the entire requested scope unavailable, without reporting a partial union (Q1/Q2).
- [ ] **AC-08:** Unsupported Ruby, interpolation, conditional declarations, trailing syntax, and unsupported code inside unselected groups reject completeness; recognized lines do not produce partial rows (Q1).
- [ ] **AC-09:** Optional declarations use declared membership without consulting installation settings; nested groups are rejected (Q1).
- [ ] **AC-10:** Duplicate declarations reject scope rather than double count or merge; duplicate lock identities retain Feature 004 rejection (Q1/Q2).
- [ ] **AC-11:** Missing/unreadable/unsafe Gemfile reports unavailable selected scope and performs no Ruby lookup.
- [ ] **AC-12:** Missing lock retains known selected names as unmeasurable; declaration pins never substitute for exact lock evidence (Q2).
- [ ] **AC-13:** A selected declaration absent from lock direct scope is counted and unmeasurable even if a transitive spec matches (Q2).
- [ ] **AC-14:** Lock-only and unselected names produce no scoped rows or lookups; requirement disagreement is retained without satisfaction or coherence claims (Q2).
- [ ] **AC-15:** A rejected lock preserves known declaration count but makes measurement unavailable; unsupported isolated selection preserves the denominator with a dependency failure (Q2).
- [ ] **AC-16:** Private, pinned, GIT/PATH, uncertain, or multiple-remote evidence cannot use a public namesake; a nonpublic declaration source cannot be overridden by a public lock.
- [ ] **AC-17:** Known wholly unmeasurable selected scope reports 0% coverage; empty and unavailable reports remain observably distinct.
- [ ] **AC-18:** A failing scoped Ruby source preserves successful Python/npm rows and applies existing repository unknown-denominator rules.
- [ ] **AC-19:** Ordinary PyPI, package-lock, Yarn Classic conflict/evidence, and mixed identity behavior remain unchanged.
- [ ] **AC-20:** Human output names selected groups, evidence sources and limitations, explains safe failures, and agrees with JSON counts and values.
- [ ] **AC-21:** Schema v3 distinguishes Gemfile membership from lock version evidence, retains publication artifacts, and adds no verbose human diagnostics (Q3).
- [ ] **AC-22:** No report labels production as deployed state or claims supplied-file historical coherence, installation, or runtime compatibility.
- [ ] **AC-23:** Scans execute no Ruby/Bundler/project code, install/resolve nothing, read no credentials, and leave targets unchanged.
- [ ] **AC-24:** Only root supplied files participate; nested/parent files, includes, gemspecs and out-of-root symlink targets are not read; direct-file arguments do not activate Ruby (Q1/Q3).
- [ ] **AC-25:** Existing TLS verification, trust precedence, public authority, redirect and transport limits remain enforced.
- [ ] **AC-26:** Scoped ages preserve Feature 004 dates, latest selection, arithmetic, same-version zero and flagged anomaly rules.
- [ ] **AC-27:** Completed empty/partial/source-error reports exit 0; invalid activation/path errors exit 1 and systemic failures exit 2 (Q3).
- [ ] **AC-28:** Source failures and dependency failures use distinct machine-readable records with safely known provenance and deterministic precedence (Q2/Q3).

Before convergence, acceptance evidence must include deterministic offline cases
for every criterion and an explicitly authorized real-root supplied-file example
whose expected selected population is independently established. Record rejected
constructs and evidence limitations without claiming general application coverage.
No particular external repository is authorized here. Optional live registry
smoke is separate from deterministic correctness and cannot replace it.

## Product questions and decision traceability

### MUST RESOLVE BEFORE SPEC REVIEW CAN APPROVE

- **Q1 — Exact static product envelope:** Approve or revise the closed subset,
  whole-file rejection, duplicate policy, nested-group rejection, implicit empty
  default and root/symlink policy above. These determine which real files users
  can measure; H3 accepts conservatism but does not select this exact envelope.
- **Q2 — Association and availability:** Approve or revise name-based supplied
  association without requirement satisfaction checks; missing versus rejected
  lock treatment; unknown-group behavior; and failure precedence. In particular,
  should textual requirement disagreement remain qualified evidence or prevent
  measurement? No historical compatibility claim is available in either case.
- **Q3 — Public interface:** Choose explicit CLI spelling/cardinality/error
  syntax and finalize the proposed additive schema-v3 fields, stable reasons,
  and missing/rejected-input provenance. The product-level shape is explicit
  group selection on directory scans; exact syntax is not yet authorized.

These are three unresolved decision families, not a request to reconsider H1–H3.
The draft cannot be approved or implemented until their answers are incorporated.

### IMPLEMENTATION / PLANNING QUESTION

Parser organization, internal records, module ownership, bounded resource
implementation, fixture layout, test decomposition and task ordering belong to
planning after approval. They must not decide Q1–Q3 by implementation accident.
No architecture is selected here.

| Requirement family | Authority / unresolved origin | Acceptance |
|---|---|---|
| Selected declared measurement and limited claims | Human H1/H2; discovery F2/F3 | AC-02–07, AC-20, AC-22 |
| Completeness and static safety | Human H3; subset details Q1 | AC-08–11, AC-23–24 |
| Membership/duplicates | Discovery S2; proposed Q1 | AC-03–10 |
| Association/failures | Human authority boundary; Feature 004; proposed Q2 | AC-12–18, AC-28 |
| Default and ecosystem compatibility | Human compatibility decision; SPEC and Features 002–004 | AC-01, AC-18–19 |
| Public interface/provenance | Discovery S4; schema-v3 baseline; proposed Q3 | AC-20–21, AC-27–28 |
| Coverage | SPEC/Feature 004; Q2 for new missing-input cases | AC-06–07, AC-12–18 |
| Security and arithmetic | AGENTS, SPEC, Feature 004 | AC-16, AC-23–26 |

Author check: H1–H3 preserved; no deployment claim or Ruby/Bundler execution;
all-direct default preserved; unsupported scope fails closed; criteria have
stable identifiers; new product decisions remain explicit proposals. No roadmap
coherence defect identified. This is an author audit, not independent review.
