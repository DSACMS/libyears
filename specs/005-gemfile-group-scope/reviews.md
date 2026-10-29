# Feature 005 Reviews

## Independent specification review — 005-0005

**Date:** 2026-10-29. **Completion:** INCOMPLETE.
**Finding status:** not_assessed. No product verdict was established.

This historical attempt is recorded from the machine handoff and authorized
human post-run observations supplied to run `005-0006`; it is not reconstructed
as a completed audit. The requested independent specification review did not
complete its cross-contract and 28-acceptance-criterion coverage, including
incomplete reading. It established no material product finding. Incompleteness
alone is neither approval nor evidence of a specification defect.

Reviewed target: `spec.md`, SHA-256
`f4d973cb24ad63f2f7abfd2430694504260524c223ba6090f47e87d94060cbd6`.
The specification was unchanged. Run `005-0005` appended and verified the
prior `005-0004` observation but created no commit. Its authorized post-run
configuration was GPT-6-Astra, low effort; this identifies the supplied
observation and does not establish a cause of incompleteness.

The separate later review below must be assessed on its own evidence.

## Decomposed independent specification review — 005-0006

**Date:** 2026-10-29. **Completion:** COMPLETE. **Verdict:** REVISE.
**Specification approval:** NOT APPROVED; revision and independent verification
required before technical planning. **Material findings:** 2.
**Decomposition result:** DECOMPOSITION SUFFICIENT for completing this review
gate, not for approving this draft.

Experiment: `005-spec-review-decomposition-01`.
Comparison group: `ultra-native-decomposition` (the commissioned label, not
measured model/effort telemetry). Parent observed run: `005-0005`.
Reviewed repository baseline: `9e7a0ef5dac7d0eaa58b64f164e0a42466ea3312`.
Reviewed specification SHA-256:
`f4d973cb24ad63f2f7abfd2430694504260524c223ba6090f47e87d94060cbd6`.
The specification remains byte-unchanged, including its historical draft status.

### Independent evidence and synthesis method

Three native child tasks were commissioned with fresh contexts
(`fork_turns="none"`), no explicit model/effort overrides, and separate primary
responsibilities. Each read the repository authority directly. No reviewer
received another reviewer's conclusions or read its report. All three were
observed running concurrently; the parent synthesized only after all finished.
Their temporary reports are non-canonical and are not committed. The evidence
needed to continue the review is retained here.

| Child task | Primary boundary | Result |
|---|---|---|
| `/root/review_a` | H1–H3/Q1 authority, activation, closed static envelope, complete-file recognition, filesystem/execution boundaries and group semantics | PASS; assigned slice complete, no material findings. |
| `/root/review_b` | Declaration/lock association, source authority, failures/precedence, denominators, sibling survival and metric/publication preservation | MATERIAL FINDINGS; assigned slice complete, B-01 and B-02. |
| `/root/review_c` | CLI, schema, safe provenance, human correspondence, regressions, readability and all 28 ACs | MATERIAL FINDINGS; assigned slice complete, C-01; every AC explicitly assessed. |

B-02 and C-01 independently identify the same issue and are counted once as F2.
The parent validated both retained findings against S3/S4 and Feature 004's
requirement-framing, matching and failure contracts; agreement alone was not
used as proof. C's general precedence assessment is narrowed by B-01's concrete
combined case, independently validated below.

The parent read AGENTS.md, AGENT_ROUTING.md, the observation protocol/ledger,
ROADMAP.md and all current Feature 005 artifacts. The review evidence includes
SPEC.md and applicable Feature 002–004 contracts, with Feature 004 review and
completion records resolving its historical draft-status text. For F2, the
parent also inspected `libyears/gemfile_lock.py`, `libyears/rubygems.py` and
existing unsupported-requirement assertions. One offline baseline witness
confirmed that a structurally accepted lock with an isolated URL-shaped direct
requirement yields `unsupported_requirement`. No registry access occurred.
This establishes the inherited case, not future Feature 005 implementation.

### Validated material findings

#### F1 — Missing direct identity versus nonpublic Gemfile source precedence

**Locations:** [spec.md](spec.md), S3 failure precedence (lines 194–201), S4
`lock_dependency_missing` condition (line 277), and nonpublic Gemfile-source
rule (lines 282–284). Origin: B-01. Acceptance impact: AC-28; composed case also
exercises AC-13 and AC-16.

A supported Gemfile can select `rack` under a nonpublic source while an accepted
lock records only `rake` in DEPENDENCIES. S4 then assigns both
`lock_dependency_missing` for the missing direct identity and
`unsupported_dependency_source` for each identity under a nonpublic Gemfile
source. S3 places both before mismatch but does not order them against each
other. Feature 004's inherited source-before-missing-selection rule concerns
missing specs for an existing direct row; it has neither a Gemfile source nor
a missing direct-row step, so it does not settle this new combination.

Both implementations would keep N=1, make no lookup and report an unmeasurable
dependency, but checking association first versus declaration authority first
produces different stable reasons and human explanations. The no-public-
namesake boundary is intact; the defect is the promised deterministic reason.

**Smallest correction:** explicitly order nonpublic Gemfile authority and
missing direct identity after whole-lock acceptance, qualifying the S4 reason
rules consistently. Preserve the already specified unavailable-lock precedence.
Include this composed case in AC-28 evidence. This review does not select the
missing policy or modify the specification.

#### F2 — Unsupported direct requirement has no defined safe scoped provenance

**Locations:** [spec.md](spec.md), S4 `gemfile_evidence.lock_requirement`
(lines 237–246), safe human correspondence (lines 290–295), and S3's preserved
unsupported-requirement precedence (lines 194–201). Governing baseline:
Feature 004 specification, supported requirement framing (lines 182–190) and
Failure Model (lines 398–438). Origins: B-02 and C-01. Acceptance impact:
AC-20, AC-21 and AC-28.

Whole-lock acceptance does not establish supported requirement text for every
direct row. A supported public Gemfile selecting `rack` can be paired with an
accepted lock containing the safely delimited direct row
`rack (https://example.invalid/opaque)`. The inherited result is dependency-level
`unsupported_requirement`, preceding mismatch, with a known denominator.
The parent confirmed this baseline distinction offline.

S4 defines text for a matching direct row in an accepted lock, null for a known
absent requirement, and omission for a missing lock/direct row. It does not
define representation for this existing but unsupported requirement. Copying
URL-shaped content violates the new field's safety rule; null falsely states
absence. Omitting or redacting it without a specified rule yields incompatible
public output. The phrase “bounded requirement text” restricts admissible
content but does not settle this missing presence/omission case or its matching
human rendering.

**Smallest correction:** explicitly omit `lock_requirement` when the matching
direct requirement fails supported safe framing; retain null only for known
absence, safe declaration metadata, the dependency-level reason, denominator
and no-lookup behavior. Human output must not echo the unsupported content.
Alternatively specify another exact safe representation before approval.
Include the case in AC-21/AC-28 evidence. Do not reject the entire lock merely
to avoid serialization or change ordinary all-direct output as part of this fix.

### Acceptance coverage and whole-gate assessment

**28/28 criteria reviewed and explicitly accounted for.** Coverage means review
coverage, not passed implementation tests. AC-20, AC-21 and AC-28 are not fully
auditable until the findings are resolved. All other stated observables are
determinate; AC-13's stable-reason interaction is captured under AC-28/F1.

| Criterion | Normative evidence / observable contract | Assessment |
|---|---|---|
| AC-01 | Baseline/S1: ordinary all-direct scan never reads Gemfile | Auditable |
| AC-02 | S1–S3: explicit selected public declaration, exact case-sensitive association and age | Auditable |
| AC-03 | S1/S2: implicit default membership, explicit default selection, no production mode | Auditable |
| AC-04 | S2: block plus explicit memberships; count one identity | Auditable |
| AC-05 | S1/S2: multiple selected groups union; repeated requests deduplicate | Auditable |
| AC-06 | S2/S4: established empty/default has 0/0 and null coverage; S3's rejected-lock exception applies | Auditable with AC-15 |
| AC-07 | S1/S3/S4: any unknown group prevents partial union and lock processing | Auditable |
| AC-08 | S1: exhaustive subset, complete consumption, unsupported unselected syntax rejects | Auditable |
| AC-09 | S1/S2: optional declared membership; nested groups reject | Auditable |
| AC-10 | S2/S3: duplicate declarations and duplicate lock identities reject their sources | Auditable |
| AC-11 | S1/S4: missing/unreadable/unsafe Gemfile gives unavailable scope, no lookup | Auditable |
| AC-12 | S1/S3/S4: missing lock retains known nonempty names; pins never substitute; empty exception | Auditable |
| AC-13 | S3/S4: absent direct identity counts once, unmeasurable; no transitive substitution | Auditable population; combined reason tracked in F1/AC-28 |
| AC-14 | S3/S4: excluded names omitted; supported mismatch retains two safe values, no version/lookup or semantic inference | Auditable |
| AC-15 | S1/S3/S4: rejected lock retains N, null measurement and no rows; isolated failures retain denominator | Auditable |
| AC-16 | S3 and Feature 004: no private/pinned/GIT/PATH/uncertain/multiple-remote public fallback | Auditable authority; combined reason tracked in F1/AC-28 |
| AC-17 | S2/S4: nonempty wholly unmeasurable 0%, empty null coverage, unavailable null measurement | Auditable |
| AC-18 | Baseline/S4: sibling survival and repository unknown-count/coverage rules | Auditable |
| AC-19 | Baseline/S1 and Features 002–004: Python/npm/Yarn/mixed identity unchanged | Auditable |
| AC-20 | S4: matching human sources, groups, safe requirements, counts and limitations | Gap F2 |
| AC-21 | S4: additive v3, deterministic scoped fields and ordinary omission, accepted/null format and retained artifacts | Gap F2 |
| AC-22 | Outcome/S3/S4: no deployed, installed, runtime-compatibility or historical-coherence claims | Auditable |
| AC-23 | S1/security: no execution, installation, resolution, credentials or target mutation | Auditable |
| AC-24 | S1: exact root inputs, no includes/parent/nested/outside-root target reads; direct-file usage error | Auditable |
| AC-25 | Security and Feature 004: TLS/trust/public authority/redirect/transport limits preserved | Auditable |
| AC-26 | S3 and Feature 004: canonical dates/latest/arithmetic, exact zero and flagged clamping | Auditable |
| AC-27 | S1/S4: reporting exit 0, usage/path exit 1, systemic exit 2 | Auditable |
| AC-28 | S3/S4: distinct failure records, safe provenance and deterministic precedence | Gaps F1/F2 |

Reverse traceability is complete: S1 maps to activation, syntax, filesystem and
failure ACs; S2 to AC-03–10; S3 to association/availability and metric ACs;
S4 to reporting, coverage, provenance and exit ACs; security to AC-16/23–25.
The explicit future convergence requirement adds offline evidence for every AC
and an authorized real-root example with independently established population.
It grants no external-checkout access and makes live smoke optional.

Independent synthesis found H1–H3/Q1–Q3 fidelity, the closed static envelope,
group semantics, source-authority prohibition, known/unknown coverage distinction,
sibling isolation and regression boundaries otherwise coherent. In particular,
absent lock plus empty scope is available empty, while a rejected lock preserves
N=0 but makes measurement unavailable; the specific S3 rule qualifies AC-06.
Scoped activation retains Ruby evidence even when unavailable; higher-priority
Gemfile/unknown-group failures prevent lock recognition. Ordinary schemas and
metric/publication policies remain governing. The specification is readable
without a conversation and defers parser/module/fixture/task decisions openly;
no premature implementation architecture was found.

The approval gate fails on the two validated public-contract defects, not on
missing review coverage. **REVISE**, rather than INCOMPLETE, is therefore the
final verdict. Correct the contract in a subsequent authorized run and obtain
independent verification before planning.

### Observation, verification and limitations

The ledger records exactly runs `005-0001` through `005-0005`, each once and with
44 fields. Earlier committed bytes and the existing `005-0004` row were
preserved; both prior rows were checked against the supplied handoffs/status
additions. Run `005-0005` remains incomplete/not_assessed with blank outcome.
No inferred credits or credit-delta column was added. Run `005-0006` and its
children have no ledger rows in this commit.

This is one human-launched prospective observation. Decomposition completed
this review gate with two validated findings; it does not establish a causal
model/effort comparison, prove that decomposition is generally sufficient, or
show that a lower-resource configuration would produce the same result. Actual
child model/effort/resource telemetry was unavailable. Fresh contexts and
concurrent task identifiers are directly observed orchestration metadata only.

No product suite, application scan, live registry smoke, upstream-documentation
refresh or external-checkout validation was performed. The one offline baseline
witness is narrower than feature acceptance testing. Other counterexamples are
contract analyses. Planning, tasks and implementation were not begun; no
specification corrections were applied. Temporary child reports remain outside
the repository. Only the prior observation ledger and this review record are
included in the local review-evidence commit; no push is authorized.

Verification passed: ledger identities/44-field shape and preserved bytes;
unchanged specification bytes/hash (3,815 words); all 28 AC entries; separate
incomplete history; temporary reports outside the repository; and absence of
planning, implementation or unrelated changes. `git diff --check` passed.
The final diff was inspected before the local commit.

## Focused independent specification verification — 005-0007

**Date:** 2026-10-29. **Completion:** COMPLETE. **Verdict:** APPROVE.
**Specification approval:** APPROVED. **Next gate:** TECHNICAL PLANNING.
No planning, tasks or implementation began.

The parent corrected only validated F1/F2 and their acceptance evidence, then
inspected the diff and passed `git diff --check` before freezing the candidate:
`13ec1e8853a4013b40c6023aa8760a2144f95c0416657d2136b625e82bf094d1`.
The earlier INCOMPLETE and REVISE records above remain unchanged historically.

One native independent child, `/root/focused_verification`, was commissioned
only after candidate freeze with `fork_turns="none"`, no explicit model or effort
overrides, and no author reasoning beyond the authoritative findings and
corrected repository state. Actual child model/effort telemetry was unavailable.
It read AGENTS.md, Feature 005 discovery/spec/reviews, the full correction diff,
and relevant Feature 004 requirement/source/failure/coverage contracts directly.
Its report was stored outside the repository. This child is orchestration detail
within observed run 005-0007, not a separate ledger observation.

### Focused evidence and parent synthesis

- **F1 resolved; AC-28 auditable.** After whole-lock acceptance, a selected
  nonpublic-source `rack` absent from direct identities in a lock containing only
  `rake` yields `unsupported_dependency_source`, N=1, M=0, 0% coverage and no
  lookup. S3 and S4 qualify missing-direct identity consistently. Human output
  safely explains unsupported nonpublic authority. Missing/rejected-lock
  precedence remains ahead of this decision and unchanged.
- **F2 resolved; AC-20/AC-21/AC-28 auditable.** A matching direct row with
  unsupported safe requirement framing retains `unsupported_requirement`, known
  denominator and no lookup. Scoped JSON omits `lock_requirement`; null remains
  known absence. Neither scoped JSON nor human output may echo unsupported lock
  text. Safely reportable declaration metadata remains available, including safe
  declaration-derived `declared`. The isolated failure cannot reject the whole
  lock merely for serialization. Ordinary all-direct output remains unchanged.
- **No material collateral changes found.** The reviewed diff preserves Q1's
  static envelope, group/default/union semantics, repeatable group option,
  all-direct compatibility, coverage arithmetic, unrelated failure ordering,
  Python/npm/Yarn behavior, security/no-execution boundaries and all AC identifiers.

The parent inspected the child's complete report and rechecked its conclusions
against the corrected diff and inherited Feature 004 framing/failure contract.
The evidence supports APPROVE. The original 28/28 review coverage is retained;
this verification closes only F1/F2 and the collateral boundary, without claiming
another full audit or passed implementation tests. Only approval/status text
changed after candidate review; the reviewed behavioral contract stayed frozen.

No product suite, live registry smoke or application scan was run for this
specification-only correction. The witnesses are contract analyses; future
acceptance evidence remains required. No external checkout was inspected.

## Independent technical plan review — 005-0009

**Date:** 2026-10-29. **Completion:** INCOMPLETE. **Verdict:** INCOMPLETE.
**Plan approval:** NOT GRANTED. **Next gate:** complete independent technical plan review.

Reviewed candidate SHA-256: `03bb48ce5bbe1d18b4346b8adb08f7f5fadb1c61e74d3765bca73e224922ad79`. Plan bytes unchanged.

The attempted review inspected the plan and its proposed 28-criterion verification
matrix, but did not complete independent reconciliation of all current discovery,
specification and review history with the existing implementation. Initial bulk
reads were truncated; the missing evidence was not fully recovered and audited.
Consequently no acceptance criterion is claimed independently verified (0/28).
AC-01 through AC-28 remain pending independent technical review.

Architecture/ownership, complete static recognition and filesystem safety, F1/F2
association, mixed integration, public output, implementation sequencing and scope
discipline remain unaudited as a complete gate. The plan's proposed test mappings
are not independent acceptance evidence. No material technical defect is
established; incompleteness is a review outcome, not a product finding. Approved
product decisions and prior specification approval remain intact.

Prior observation 005-0008 was appended from its machine handoff with only the
authorized human metadata additions. Runs 005-0001 through 005-0008 each occur
once with 44 fields; earlier ledger bytes and previous review history are
preserved. No tasks, implementation, product tests, live validation or push.
