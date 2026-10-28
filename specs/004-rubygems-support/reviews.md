# Feature 004 Reviews

**Discovery review status:** APPROVED FOR SPECIFICATION

Implementation is not approved. Earlier review statuses below are historical.

## Initial Discovery Review

**Initial draft commit:** df7aee60446795f67da321331f778c3d1457fea7
**Initial recommendation:** no-code workflow validation
**Review verdict:** CONTINUE DISCOVERY

### Material findings

- The sandbox/network result was environment-confounded. The `0/77` result is
  agent-environment evidence, not a demonstrated offline/cache product need.
- Workflow validation was too vague to be Feature 004; it is continued discovery.
- Python exact-evidence compatibility needed bounded testing against existing
  repository-local artifacts and current `--resolved` behavior.
- Broad human research was premature while technical evidence remained cheap
  to investigate.
- Root identification should remain separate from portfolio aggregation.

### Disposition

Continue discovery with the bounded Python evidence-compatibility experiment:
at least two distinct project roots must demonstrate supported non-exact direct
declarations plus already-produced local exact selected-version evidence that
cannot be consumed unchanged by current `--resolved`. No parser or product
capability was approved by this experiment selection.

This record preserves the independent review findings supplied for this
revision, not a reconstructed transcript or a new review of the revised draft.

## Deep Evidence Investigation

The completed read-only investigation is summarized with paths, counts,
limitations, and candidate comparisons in [discovery.md](discovery.md).

- **Python threshold: NOT MET.** Ten metadata-bearing roots represent eight
  conservatively grouped project families. The 28 requirements entries contain
  two copies of the same exact pin and 26 non-exact declarations.
- **No repeated retained Python evidence incompatibility.** The dominant gap
  is absence of retained exact evidence, not incompatibility with `--resolved`.
  One local environment has relevant installed metadata but lacks demonstrated
  project/build attribution; even counting it would not meet the two-root test.
- **Project-root multiplicity demonstrated; user pain not demonstrated.** Build
  and workspace systems encode roots, but no Libyears selection failure or
  recurring user burden was established. Listing is distinct from aggregation.
- **Ruby evidence materially strengthened.** Four DPC application pairs have
  build-consumed locks and strong ordinary declaration/lock alignment. Public
  timestamp metadata appears available; groups, platforms, special entries,
  useful scope, and demand remain unresolved. Evidence fitness is MEDIUM-HIGH;
  demand confidence is LOW-MEDIUM. Neither is implementation approval.
- **Go/JVM: NO MATERIAL EVIDENCE DELTA.**
- **Provenance: NO DEMONSTRATED PROBLEM.**
- **Offline/cache: PLAUSIBLE BUT UNDEMONSTRATED.** Codex sandbox failures are
  excluded from product evidence.

**Status at `67b7d89ca6f1c48bc92dcd128b19bb478a6ba969`:** READY FOR FOCUSED RUBY FEASIBILITY REVIEW

**Feature 004 product direction remains unapproved.** Bounded Ruby evidence
support ranks first for investigation, followed by project-root listing and
Python pyproject declaration discovery. One focused Ruby feasibility/product-
scope review should precede a human Feature 004 decision. No specification,
plan, task graph, Ruby implementation, or definitive feature selection is
approved by this status.

## Git-before-review experiment

The initial discovery was committed before review as `df7aee60446795f67da321331f778c3d1457fea7`
(`df7aee60446795f67da321331f778c3d1457fea7`,
`docs(discovery): draft Feature 004 direction`). That commit is unchanged.
`67b7d89ca6f1c48bc92dcd128b19bb478a6ba969` (`docs(discovery): refine Feature 004 evidence`) preserves the
post-review/deep-evidence state separately: Ruby was the strongest candidate,
but remained unapproved. Git retains exact before/after discovery artifacts
without preserving chat transcripts. The subsequent human decision below is
recorded in a separate change, alongside the normal directory rename to
`specs/004-rubygems-support/`. Neither earlier commit is rewritten.

## Ruby Feasibility Review

This concise record preserves the completed review findings supplied for this
human decision; it does not claim a new independent review or registry lookup.

**Verdict:** RUBY IS READY FOR HUMAN PRODUCT SELECTION

- **Bounded static model:** `Gemfile.lock DEPENDENCIES` -> direct scope;
  lock specs -> exact versions; RubyGems.org -> release metadata.
- Gemfile evaluation is unnecessary for the selected all-direct lock scope.
- Observed strict static evidence retains **238/247 direct occurrences** before
  registry lookup; this is not a registry-backed measurement result.
- The security/no-execution boundary is preservable.
- **Parser complexity:** MEDIUM when bounded.
- **Maintenance burden:** HIGH relative to the small CLI.
- Demand breadth remains limited to one observed project family.
- Production/group interpretation would materially change the proposition.

## Human Product Decision

**Decision:** SELECTED FOR SPECIFICATION

**Feature 004:** Bounded RubyGems lock-snapshot support

The human accepted all-direct lock-snapshot scope, including development/test
dependencies where present; the third-ecosystem maintenance cost; and deferred
interpreted-Gemfile/group/production scope. Gemfile.lock supplies recorded direct
scope and exact selected-version evidence; RubyGems.org is the intended public
release-metadata authority. No Gemfile evaluation, Ruby/Bundler execution, gem
installation, or dependency resolution is authorized. Unsupported or ambiguous
evidence fails closed.

The result describes the committed lock snapshot, not the currently evaluated
Gemfile, production-only scope, an installed environment, or a runtime environment.
The detailed behavioral questions listed in
[discovery.md](discovery.md#human-product-decision) remain for specification.

**Discovery review status:** APPROVED FOR SPECIFICATION

This approves specification work only, not implementation. The next gate is a
Feature 004 specification draft followed by clarification/review; no `spec.md`
is created by this decision record.

## Specification Review

**Reviewed draft:** `c761b113ea19988e7e9ea5ca16b373c1e2c526fb`
**Verdict:** REVISE

This record preserves the supplied completed independent Feature 004
Adversarial Specification Review, not a new review or product clarification.
The committed first draft remains unchanged as the pre-review baseline.

### What the draft got right

- The approved all-direct lock-snapshot product boundary was preserved.
- No Gemfile evaluation or package-manager execution was introduced.
- Coverage/source isolation and special-dependency handling were substantially
  coherent.
- Security boundary: PASS. Discovery conformance: PASS.
- No hidden scope expansion was found.
- All three JSON examples parsed; no requirement for schema v4 was demonstrated.
- The failure taxonomy was largely reusable without reason inflation.

### Material findings

#### F1 — Canonical release policy is under-decomposed

Q3 combines comparison domain, canonical timestamp population, artifact
availability, incomplete historical visibility, and eligibility. A package-level
freshness decision alone does not resolve these separate policies.

**Classification:** PRODUCT DECISION REQUIRED

#### F2 — Yank/history visibility was overstated

Ordinary public RubyGems endpoints expose currently public records but do not
establish complete historical/yanked visibility. Missing ordinary public records
alone cannot establish a known yank, a never-existing package/version, or
complete historical publication evidence.

**Classification:** AUTHORITATIVE SEMANTICS CORRECTION

#### F3 — Lock boundary does not uniquely determine failure level

Clarify repeated/same-remote GEM blocks, missing remote, unsupported nested
requirement framing, empty/repeated PLATFORMS, simultaneous malformed and
unsupported evidence, and source-error precedence. These affect count
availability and failure isolation.

**Classification:** SPEC CORRECTION

#### F4 — Registry case identity is a product decision

Endpoint choice must not change whether case-only identity differences are
accepted. Promote the previous MAY question to a before-approval product
decision.

**Classification:** PRODUCT DECISION REQUIRED

#### F5 — Version + platform is not always complete artifact identity

RubyGems may expose additional artifact identity such as `ruby_abi`. Feature 004
need not support those artifact classes, but must recognize that they cannot
silently collapse into ordinary version/platform evidence.

**Classification:** AUTHORITATIVE SEMANTICS CORRECTION

#### F6 — Historical import predicate is only a heuristic

The observable RubyGems import-day predicate does not attest that all other
creation timestamps are historically authoritative. Separate technical
detection from acceptable product uncertainty.

**Classification:** AUTHORITATIVE SEMANTICS CORRECTION

#### F7 — Exact-requirement comparison needs a bounded syntax

Clarify bare exact versions, `=` exact terms, whitespace, repeated terms, and
exact terms inside compound requirements. Do not create a general Ruby
requirement evaluator.

**Classification:** SPEC CORRECTION

#### F8 — Same-version platform variants need explicit ratification

Unconditional rejection is conservative but is a product policy, especially if
package-level freshness is selected.

**Classification:** PRODUCT DECISION REQUIRED

### Acceptance Criteria Audit

| Review category | Count |
|---|---:|
| Draft count | 45 |
| Clearly testable | 29 |
| Ambiguous | 6 |
| Redundant | 0 |
| Process-only | 0 |
| Contradict spec | 0 |
| Depend on unresolved questions | 10 |

The reviewer found no evidence that the draft criterion count was inflated
merely by the absence of a numerical cap. Criterion count remains emergent and
may change after clarification; 45 is not a target.

### Schema Assessment

**Schema v3:** AMBIGUOUS, but no v4 requirement demonstrated.

Ordinary RubyGems evidence appears additive. Final compatibility depends on
resolving artifact/canonicalization provenance without reinterpreting existing
schema fields.

### Human Clarification Packet

All eight decisions below remain pending human judgment; no option is selected
by this review record.

#### H1 — Lock-only recognition

- A. Root Gemfile.lock alone activates Ruby discovery.
- B. Companion Gemfile presence is required.

#### H2 — Single platform-qualified lock evidence

- A. Reject initially.
- B. Accept explicit platform-qualified evidence without host-platform inference.

#### H3 — Freshness comparison domain

- A. Compare a defined artifact class.
- B. Compare package versions across supported artifacts.

If A, generic-only versus exact recorded platform class remains a product choice.

#### H4 — Observable history versus historical certainty

If package-level comparison is chosen:

- A. Use a defined canonical date over supported currently observable records,
  while explicitly disclosing the limitation.
- B. Decline measurement where required historical publication time cannot be
  established.

Availability and timestamp uncertainty still need explicit participation rules.

#### H5 — Same-version public platform variants

If package-level comparison is chosen:

- A. Continue rejecting multiple variants.
- B. Accept one package version established by same-version supported variants.

Different-version and uncertain-source evidence remains fail-closed.

#### H6 — Historical timestamp uncertainty threshold

- A. Reject the whole identified import-day interval or another justified broad
  interval.
- B. Reject only records meeting a narrower documented heuristic.

Missing auxiliary metadata needs an explicit conservative result.

#### H7 — Exact requirement disagreement

- A. Trust selected lock evidence.
- B. Require literal extracted-version agreement for the deliberately supported
  exact-term syntax.

Do not characterize textual disagreement as proven semantic incompatibility.

#### H8 — Registry case-only identity

- A. Require exact spelling.
- B. Permit ASCII case-only agreement at the registry boundary.

Punctuation normalization remains excluded.

### Clarification order

1. Correct authoritative facts about artifact identity, public-history
   visibility, absence, case lookup, and historical-import semantics.
2. Resolve freshness comparison domain and dependent canonicalization/history
   policy.
3. Resolve platform-qualified evidence and same-version variant treatment.
4. Resolve historical uncertainty threshold.
5. Resolve lock-only recognition, exact-requirement consistency, and case
   identity.
6. Clarify parser/failure precedence, provenance fields, acceptance criteria,
   and schema compatibility.
7. Perform a narrow independent verification review before specification
   approval.

### Status

**Specification status:** REVISE — awaiting human product clarification

**Implementation status:** NOT APPROVED

**Next gate:** Human clarification of H1–H8


## Human Product Clarification

The completed human clarification supersedes the pending alternatives in the
historical review above. Outcomes:

- H1: root Gemfile.lock alone activates; Gemfile is neither required, inspected,
  nor evaluated; Gemfile alone does not activate.
- H2: accept a single supported platform-qualified selected record, retaining
  artifact provenance without runtime/platform compatibility claims.
- H3: measure package-version freshness across supported artifacts.
- H4: accept bounded supported observable history, not first-ever historical
  publication; disappearance can change future measurements.
- H5: agreeing distinct supported public variants establish one dependency;
  differing version text, unsafe source/identity and duplicate structure fail
  closed at the specified boundary.
- H6: all authoritative publication times on 2009-07-25 UTC are inadmissible;
  built_at is never authority, fallback, or rehabilitation.
- H7: trust selected lock evidence across supported requirement forms; no
  satisfaction/equivalence evaluation or textual consistency test.
- H8: after independent public source authority, registry identity allows only
  ASCII case differences, endpoint-independently. Lock comparisons remain exact.

Canonicalization includes fully understood generic/platform public artifact
records independently of locked platforms; identifiable unsupported classes
(including ruby_abi) are excluded, unsafe identity/metadata fails closed.
Observable yanked records may contribute dates; missing records are not inferred
or presumed yanked. Missing, invalid, import-day timestamps are individually
excluded; contradictions remain metadata failures. The earliest admissible
supported observable authoritative timestamp is canonical for both used/latest.
No admissible date prevents measurement/candidacy; latest additionally requires
supported currently available stable artifact evidence. Only-yanked versions
cannot be latest. Other dates are observable evidence, not historical certainty.

Supply-chain boundary: establish supported public source authority before lookup;
never substitute public namesakes for private/Git/PATH/unsupported/ambiguous
sources. No fuzzy normalization, ABI/runtime resolution or malicious-package
detection is introduced.

Newly discovered product questions: NONE.
Clarification status: READY TO REVISE SPECIFICATION.

## Specification Clarification

H1–H8 and all canonicalization sub-decisions are incorporated. Corrected claims
about ordinary API historical/yank visibility, version/platform identity
completeness, import heuristics and endpoint-dependent identity. Absence reasons
now describe observable evidence without asserting never-existence or yanking.

Repeated GEM blocks, missing remotes, nested framing, PLATFORMS and conflict
markers have explicit outcomes. Malformed supported structure precedes unsupported
whole-source evidence, which precedes local failures, independent of parser order;
unsafe attribution rejects the source, safely isolated failures preserve scope.
Known denominators survive individual/all registry failures; mixed ecosystem
success survives Ruby source rejection. Empty-source semantics are explicit.

Acceptance criteria revised from 45 to 52. The fresh bidirectional author audit
maps all normative behavioral families to criteria and every criterion back to
normative rules; redundant examples are grouped and process obligations excluded.
Schema v3 is retained: additive Ruby publication basis and artifact provenance
suffice without overloading existing fields. Two new draft reasons remain
unsupported_dependency_name and unsupported_lock_evidence; existing reasons are
reused with clarified boundaries. No yank/typo/platform-specific reasons added.

Validation: all three JSON examples parse; all 52 formal criteria are uniquely
and consecutively numbered. Compared the revision against committed pre-review
baseline c761b113ea19988e7e9ea5ca16b373c1e2c526fb; retained static all-direct snapshot scope, execution/security
boundaries, metric arithmetic, existing ecosystem behavior and schema-v3 shape.
The original draft and review remain preserved in Git without rewriting history.
Only spec.md and reviews.md are changed; no plan, tasks or implementation added.

Remaining product questions: NONE.
Specification status: Clarified draft — ready for narrow verification review.
Implementation status: NOT APPROVED.
Next gate: independent narrow verification review, before specification approval.

## Specification Verification

**Clarified specification:** `3b315696e4d03b5e7aac325b47a800abbade70e0`
**Verification verdict:** APPROVE
**Specification status:** APPROVED FOR TECHNICAL PLANNING

The completed independent narrow verification found:

- F1–F8 resolved; H1–H8 faithfully incorporated and internally coherent.
- Canonicalization: PASS.
- Supply-chain/source-authority boundary: PASS.
- Failure taxonomy: PASS.
- Coverage/availability: PASS.
- Schema: SCHEMA V3 COMPATIBLE.
- Security boundary: PASS.
- Acceptance criteria: 52/52 clearly testable; no ambiguous, redundant,
  process-only, contradictory, or unresolved-product-question-dependent criteria.
- No missing material behavioral cases or unresolved product questions.
- Discovery conformance: PASS; no hidden scope expansion.
- No material findings remain.

## Git-Before-Review Process Result

**USEFUL BEFORE/AFTER EVIDENCE**

The repository preserves:

- `c761b113ea19988e7e9ea5ca16b373c1e2c526fb` — committed pre-review specification.
- `5c5b69adb810827cd4c8e74d1bbbeef44bd34465` — adversarial review findings.
- Human clarification of H1–H8 and canonicalization, recorded above.
- `3b315696e4d03b5e7aac325b47a800abbade70e0` — clarified specification.

The independent verifier found this history materially useful for reconstructing
what review and clarification changed. This is evidence from this review, not
proof of the broader process hypothesis.

## Status

**Specification-review status:** APPROVED FOR TECHNICAL PLANNING

**Implementation status:** NOT APPROVED

**Next gate:** Draft technical plan, commit it before independent architecture review.
