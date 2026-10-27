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
