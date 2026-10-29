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


## Decomposed independent technical plan review — 005-0010

**Date:** 2026-10-29. **Completion:** COMPLETE. **Verdict:** REVISE.
**Plan approval:** NOT APPROVED. **Decomposition result:** SUFFICIENT to
complete this review gate. **Next gate:** PLAN CORRECTION AND INDEPENDENT
VERIFICATION. No task decomposition or implementation may begin on this verdict.

Reviewed baseline: `591da218c1627d9ef79cfd38dc89001dff368e03`.
Plan SHA-256: `03bb48ce5bbe1d18b4346b8adb08f7f5fadb1c61e74d3765bca73e224922ad79`.
Plan bytes remain unchanged. The approved specification remains authoritative.
The prior 005-0009 INCOMPLETE attempt established neither a finding nor approval;
its record and all prior specification-review history remain unchanged.

### Independent evidence and parent synthesis

Three fresh native children used `fork_turns="none"`, with no explicit model or
effort overrides. All three were observed running concurrently. Each read its
repository evidence independently; no current reviewer conclusions were supplied
to another reviewer. Each confirmed this barrier in its final report. Actual
child model/effort telemetry is unavailable. Children are orchestration details
of one human-launched observation, not ledger rows.

| Child | Assigned slice | Completed result |
|---|---|---|
| `/root/review_a` | Architecture, closed parser, groups, root safety, bounds and foundation sequencing | MATERIAL FINDINGS: A-01 |
| `/root/review_b` | Association, F1/F2 authority, provenance, compatibility, aggregation and integration sequencing | PASS |
| `/root/review_c` | CLI/output, deterministic verification, regressions, whole-plan traceability and sequencing | PASS |

Temporary reports are `review-a.md`, `review-b.md`, `review-c.md` under the
external temporary directory `/tmp/libyears-005-plan-review/`; none is committed.
After all three finished, the parent read all reports, reconciled their claims
against the approved S1–S4 contract and candidate plan, and independently
reproduced A-01 with a bounded offline synthetic FIFO experiment. This is not
a majority vote: B/C's positive assessments do not close A's filesystem gap.

Ownership otherwise fits existing source/model/scan/output boundaries. Pure
closed recognition, complete-file rejection, group representation and sequencing
are implementable using the standard library. The existing Ruby authorization
prefix can be extracted without changing ordinary precedence. F1 is explicitly
before missing direct identity after whole-lock acceptance; F2 omits unsafe
requirements while retaining safe declaration metadata. Scope, version and
publication evidence remain distinct. The source availability matrix preserves
known N on rejected locks, sibling aggregates and ordinary behavior. CLI and
explicit scoped serializer omission preserve schema v3. Parser/evidence → safe
association → scan propagation → public activation → composed verification is
a coherent dependency order. No approved product behavior needs revision.

### Validated material finding P1 — blocking open before nonregular rejection

**Location:** plan.md lines 97–103, “Filesystem safety and bounded work”; related
bounds at 105–115 and reason mappings at 117–120. **Origin:** A-01.
**Approved obligations:** S1 safe scoped inputs; S4 nonregular Gemfile/lock
failure reporting; AC-11, AC-24 and AC-28.

The plan prescribes directory-descriptor traversal and no-follow open followed
by `fstat`, but does not require a nonblocking final open. After regular-file
validation, replacement of the final component by a FIFO makes ordinary
read-only open block waiting for a writer. No-follow prevents a symlink traversal,
but cannot reject a FIFO before open returns. Neither `fstat` nor byte limits
can run while open is blocked. Thus this concrete planned sequence can hang
instead of returning `invalid_gemfile` or `invalid_lockfile`, delaying sibling
reporting as well. This is a bounded-access defect, not a parser style preference.

The parent independently created and validated a synthetic regular Gemfile in
a temporary directory, replaced it with a FIFO and executed a read-only
no-follow open in a separate Python process with a 0.5-second timeout. It timed
out before `fstat`. Adding `O_NONBLOCK` allowed immediate nonregular detection
without reading. The child separately reproduced the same result. No target
code, Ruby, Bundler, package manager or network was executed.

**Smallest correction:** explicitly require nonblocking plus no-follow final
component access, then regular-file `fstat` before reading; fail closed if safe
access is unsupported. Keep containment, descriptor cleanup, ordinary Feature
004 behavior and reason mappings. Plan replacement-to-FIFO cases for both root
inputs, asserting prompt source failure, zero content reads and no lookup.
Correct the plan in a later run, then independently verify this correction and
its collateral boundaries before task decomposition.

### Whole-plan acceptance accounting

**28/28 ACs accounted for.** This is review coverage and planned verification,
not implementation acceptance or passed feature tests. The plan's named
witnesses are sufficient except for P1's missing replacement-to-FIFO variant.
The following parent reconciliation retains every criterion explicitly:

| AC | Planned evidence / parent assessment |
|---|---|
| AC-01 | Ordinary Gemfile absent/valid/invalid no-read regression; adequate. |
| AC-02 | CLI, exact direct identity, case-sensitive groups and mocked age; adequate. |
| AC-03 | Explicit default selection and no production inference; adequate. |
| AC-04 | Overlapping memberships count/lookup once; adequate. |
| AC-05 | Repeated/multiple groups deduplicated union; adequate. |
| AC-06 | Empty default/block with absent/accepted/rejected lock distinction; adequate. |
| AC-07 | Unknown request prevents partial union and lock read; adequate. |
| AC-08 | Positive subset and negative syntax/complete-file/bounds tables; adequate. |
| AC-09 | Optional membership, no configuration, nested rejection; adequate. |
| AC-10 | Declaration and direct-lock duplicate rejection; adequate. |
| AC-11 | Safe input reason/count/no-lookup matrix; P1 requires FIFO replacement variant. |
| AC-12 | Missing lock/pins and empty exception; adequate. |
| AC-13 | Missing direct despite transitive spec; adequate. |
| AC-14 | Excluded names and exact textual mismatch/provenance matrix; adequate. |
| AC-15 | Rejected lock at zero/positive N; isolated selection failures; adequate. |
| AC-16 | Private/pinned/GIT/PATH/multiple-remote/F1 authority matrix; adequate. |
| AC-17 | Empty/unavailable/wholly unmeasurable aggregate matrix; adequate. |
| AC-18 | Sibling success and repository availability matrix; adequate. |
| AC-19 | PyPI/npm/Yarn/mixed and resolved-snapshot regressions; adequate. |
| AC-20 | Paired safe human/JSON single/mixed/verbose cases including F2; adequate. |
| AC-21 | Exact scoped dictionaries, omission/null and artifact checks; adequate. |
| AC-22 | Supplied-file limitations and ordinary production group; adequate. |
| AC-23 | Target snapshots, execution/read spies and allowlist; adequate. |
| AC-24 | Root/link/decoy/replacement/direct-file tests; P1 extends replacement coverage. |
| AC-25 | Registry/TLS and scoped wiring regression; adequate. |
| AC-26 | Canonical publication/platform/zero/clamping composition; adequate. |
| AC-27 | Reporting/usage/systemic exit matrix; adequate. |
| AC-28 | Precedence/F1/F2 and safe provenance composition; P1 adds safe-read failure witness. |

All S1–S4 families have planned offline verification. The required later authorized
real-root population example remains separate from optional live registry smoke.
No external target access is authorized by this review. No product suite or
feature acceptance was run; only synthetic FIFO witnesses were executed.

### Verification and observation

The ledger appends only 005-0009 from its handoff plus the explicitly authorized
human status metadata. Runs 005-0001 through 005-0009 occur exactly once, with
44 fields each; earlier ledger bytes are unchanged. Credits_before stays blank;
no credit delta is derived. 005-0010 is handed off externally, not appended.

Plan/spec/discovery bytes and prior review history are preserved. Only this
review artifact and the prior-run ledger row change. No tasks.md, implementation
or other feature artifacts were created. Temporary reports remain outside the
repository. Ledger/hash/scope assertions and `git diff --check` pass. One local
review-evidence commit is authorized; no push. Decomposition completed the audit
but does not establish a causal model/resource comparison or general sufficiency.

## Focused independent technical plan verification — 005-0011

**Date:** 2026-10-29. **Completion:** COMPLETE. **Verdict:** APPROVE.
**Plan approval:** APPROVED. **Next gate:** TASK DECOMPOSITION.
No tasks or product implementation began.

Only validated 005-0010 finding P1 and its regression/traceability consequences
were corrected. The parent inspected the plan diff and passed `git diff --check`
before freezing candidate SHA-256:
`e588024ada3a9b59c20de94490e979b81b59e9826af880469b40f8352b58bb48`.
One fresh native child, `/root/fifo_plan_verification`, was commissioned after
freeze with `fork_turns="none"`, no model/effort overrides and no participation
in authorship. Actual child model/effort telemetry is unavailable. It read the
approved specification, current plan, relevant 005-0010 finding and correction
diff directly, matched the frozen hash, and returned COMPLETE / APPROVE. Its
temporary report is outside the repository and is not a separate ledger row.

### Focused evidence and parent synthesis

Both scoped inputs now require final-component `os.open` with
`O_RDONLY | O_NOFOLLOW | O_NONBLOCK`, immediately followed by `os.fstat` and
`stat.S_ISREG` before wrapping or consuming content. A replacement FIFO cannot
wait for a writer at this open and is rejected before reading. Content is read
only from the same validated descriptor. Existing containment, directory-relative
no-follow traversal, descriptor cleanup, byte/line limits, strict decoding and
source reasons remain intact. Missing safe-open capabilities fail closed through
existing source failures; no blocking/unchecked fallback or new dependency is
introduced. Ordinary all-direct Feature 004 access remains unchanged.

Planned separate regressions begin with regular Gemfile and Gemfile.lock inputs,
replace the selected path with a FIFO AFTER validation at the final-open hook,
and call the real open without a writer. They assert flags, pre-read rejection,
closure, prompt completion, correct unknown/known scope, source reasons and zero
lookups. The lock case first establishes Gemfile scope. A bounded subprocess
contains a potential hang; hook synchronization avoids nondeterministic races.
Capability mocks cover fail-closed platforms even when real FIFO tests skip.
These witnesses extend AC-11, AC-24 and AC-28; all 28 AC mappings remain intact.

The parent read the complete child report and independently checked the diff,
unchanged sections, failure/availability rules and traceability. A bounded offline
synthetic experiment independently validated a regular file, replaced it with a
FIFO, and confirmed nonblocking/no-follow open plus nonregular `fstat` rejection
without content reads for EACH filename. The first harness attempt failed its
temporary-root containment assertion because the root was not canonicalized;
resolving the temporary root corrected the harness and both witnesses passed.
This is a syscall-sequence witness, not a product implementation or feature test.
No product suite, external checkout, Ruby/Bundler execution or network was used.

No material collateral architecture or product changes were found. Parser,
group semantics, F1/F2, authority, schema, aggregation, resource bounds and metric
contracts are unchanged. The earlier 005-0009 INCOMPLETE and 005-0010 REVISE
records, including their historical status, remain byte-preserved. This focused
verification closes P1 against the prior whole-plan review; it does not claim
passed implementation acceptance. Only plan approval/status text changed after
candidate freeze. Final approved plan SHA-256:
`6d6bb924b1c0ca3adc50b916f648ec0ffd237df24c9ab0b0d85ef9bce018c3be`.

The ledger appends exactly 005-0010 from its JSON handoff plus authorized human
status additions. Runs 005-0001 through 005-0010 occur once with 44 fields each;
earlier bytes are unchanged, credits_before remains blank and no credit delta
is derived. 005-0011 is handed off externally, not appended. Final verification
covers narrow scope, 28/28 traceability, preserved history, no tasks/implementation
artifacts and `git diff --check`. One local commit; no push.

## Independent task-graph review — 005-0013

**Date:** 2026-10-29. **Completion:** COMPLETE. **Verdict:** APPROVE.
**Task-graph approval:** APPROVED for implementation under a subsequent explicit
execution instruction. **Next gate:** IMPLEMENTATION, NOT BEGUN.
**Material findings:** 0. No task, external validation or network work is
commissioned by this review. The unchanged tasks.md draft-status paragraphs
describe its submission state; this later review records the approval.

Reviewed repository baseline: `b87a88a1d6f5e1b8430857f71d05129b1c80e205`.
Reviewed tasks.md SHA-256:
`633821844a2a761693e3316e6d8ee093dd68b897af546f48656be766c73bace6`.
The approved specification and approved technical plan remain authoritative;
their earlier next-gate statements are historical. All five current Feature 005
artifacts, repository instructions/routing, observation protocol and ledger were
read. This fresh review independently reconciles task definitions with S1–S5,
the plan's component responsibilities, source-flow ordering, availability matrix
and deterministic witnesses. The task graph's own AC matrix is not the proof.
No authorship context or child-agent review was used.

### Dependency and task-boundary assessment

All 13 identities T001–T013 are unique and stable, with explicit predecessors
consistent between the graph table and individual definitions. The complete
predecessor graph is:

```text
T001: none                 T002: none
T003: T001                 T004: T001, T002, T003
T005: T004                 T006: T005
T007: T006                 T008: T007
T009: T006, T007, T008      T010: T009
T011: T010                 T012: T011 + later human target/evidence authorization
T013: T010, T011, T012
```

Every edge points forward in numeric order, proving acyclicity. Transitive
dependencies supply the parser, typed model and safe-reader foundations before
association or scan integration. The T003/T004 split lets safe reads be tested
before source-state composition. T004 explicitly defers accepted-lock rows to
T005 and remains disconnected from scanning: its intermediate state does not
expose an incomplete public path. T006 propagates completed source evidence;
both output formats land before T009 activates the CLI. T002 is independently
constructible using trailing defaults; it does not require parser records or
serialization. No implementation prerequisite is assigned after its consumer.

The decomposition is proportional. T001 owns the closed parser as one coherent
contract, with table-driven tests and narrowly authorized validator extraction.
T003 contains the coupled filesystem protections and descriptor lifecycle;
splitting these could obscure the safety invariant. T005 keeps authority,
association and safe provenance together where their ordering matters. T006
owns scan propagation and the availability boundary. JSON, human output and CLI
have separate reviewable changes. T010 supplements each task's behavioral tests
with composed acceptance and regressions rather than postponing all verification.
Documentation, conditional real evidence and read-only convergence are distinct.
No task requires unrelated cleanup, a new ecosystem/framework, metric changes,
Ruby execution, package management or new registry behavior.

### Independent acceptance ownership — 28/28

Each row below was derived from the approved AC observable and the actual task
Change/Evidence clauses. The owners include both behavior and concrete planned
verification. T010 additionally requires every plan-matrix witness and full
offline regressions; T013 independently audits every AC at convergence. These
are future obligations, not claims that implementation tests have passed.

| AC | Behavior ownership and sufficient verification obligation |
|---|---|
| AC-01 | T006 retains exactly one ordinary Ruby path with no Gemfile read; T009 preserves absent-keyword scan calls. Their spies plus T010's ordinary no-read regression cover absent, valid and invalid Gemfiles. |
| AC-02 | T005 builds authorized exact direct candidates; T006 measures injected canonical releases; T009 tests CLI→scan→registry age and Test/test selection. T012 later corroborates the real selected population. |
| AC-03 | T001 assigns default only when implicit and establishes explicit memberships; T004 selects exact names; T009 validates explicit requests without automatic default. Parser/source/CLI tests cover these distinctions. |
| AC-04 | T001 stores full sorted membership unions; T004 selects unique declarations; T006 verifies count and lookup multiplicity. Overlapping block/option memberships cannot duplicate a row. |
| AC-05 | T004 selects the declaration union, T006 canonicalizes requests and T009 sorts/deduplicates CLI names. Source and CLI tests compare repeated/multiple requests and stable evidence. |
| AC-06 | T001 establishes empty/default groups; T004 owns absent/accepted empty lock states and the rejected-lock exception; T006's availability tests assert zero counts, null coverage and the correct totals. |
| AC-07 | T004 validates every requested group after full recognition, before lock reads. Its tests assert one source error, no partial union and no lock access or lookup. |
| AC-08 | T001 consumes the entire closed subset and rejects every negative syntax family, including unselected code; T003 enforces byte/line limits. Positive/negative tables and boundary tests prohibit partial results. |
| AC-09 | T001 recognizes optional flags without changing membership and rejects nesting. Its tests cover true/false; T010 adds forbidden configuration-read checks. |
| AC-10 | T001 rejects duplicate names anywhere; T004 reuses whole-lock parsing and tests duplicate/malformed rejection. T010 composes these distinct source failures. |
| AC-11 | T003 owns safe reads and reason mapping; T004 maps Gemfile failure to unknown scope with no later access/lookup. Both own regular-to-FIFO replacement witnesses and resource cleanup assertions. |
| AC-12 | T004 builds missing-lock failures for known nonempty selection without pin fallback, with the empty exception. Its source tests explicitly cover counts and no candidates/registry calls. |
| AC-13 | T005 indexes direct identities only and owns lock_dependency_missing. Its transitive-match counterexample verifies one unmeasurable row and no public lookup. |
| AC-14 | T005 excludes unselected/lock-only names and compares supported requirement text before version association. Its mismatch tables test null/order/whitespace/operators, retained safe values, no selected artifacts/lookup; T007/T008 verify safe nonsemantic reporting. |
| AC-15 | T004 rejects the entire malformed lock while retaining N, including zero; T005 keeps isolated selection failures as rows; T006 verifies unavailable versus dependency-failure aggregation. |
| AC-16 | T005 preserves the existing authority prefix and checks nonpublic Gemfile authority first after lock acceptance. Private/pinned/GIT/PATH/multiple-remote and missing-direct F1 tests forbid public namesake lookups. |
| AC-17 | T006 implements the availability matrix, including wholly unmeasurable 0%, empty and unavailable states. T008's paired report fixtures verify that human distinctions agree with JSON. |
| AC-18 | T006 owns sibling preservation and repository known/unknown denominator rules. Its failure matrix covers successful Python/npm siblings and no siblings, including rejected lock at zero/positive N. |
| AC-19 | T006 preserves existing adapters, identities and Python-only resolved evidence; T009 tests resolved forwarding and ordinary calls. T010 explicitly requires existing regressions and three-ecosystem same-name isolation, including the plan's Yarn witnesses. |
| AC-20 | T007 serializes safe evidence; T008 renders groups/sources/requirements and limitations in single/mixed and normal/verbose branches; T011 documents the behavior. Paired fixtures and distinctive unsafe-marker tests cover F2 and count agreement. |
| AC-21 | T002 distinguishes omitted/null/text requirements with compatible defaults; T005 constructs safe metadata; T006 carries it through success/registry failure; T007 tests exact schema-v3 keys, artifacts, formats and ordinary omissions, including F1/F2/mismatch. |
| AC-22 | T007/T008 restrict evidence labels and explanations to supplied-file claims; T011 aligns examples and limitations. Report tests treat production as ordinary and reject deployment/runtime/history claims; T012 preserves real-evidence limitations. |
| AC-23 | T001 is pure recognition; T003 bounds permitted reads; T004 uses only the accepted scoped pipeline. T010 explicitly owns before/after target integrity and forbidden execution/config/credential/archive-access assertions. |
| AC-24 | T003 restricts exact root names, containment and safe descriptor access; T004 verifies source-level early stops; T009 rejects scoped file targets. Root/parent/nested/alternate decoys, link replacement and BOTH FIFO replacements have named witnesses. |
| AC-25 | T006 reuses the existing isolated fixed-public adapter without transport changes. Its wiring checks and T010's full plan-matrix obligation retain existing TLS/trust/redirect/pacing/limit regression coverage. |
| AC-26 | T006 reuses measurement/publication behavior and tests canonical dates/platform artifacts, expected age, exact used=latest zero and flagged clamping. T010 requires corresponding metric/registry regression witnesses. |
| AC-27 | T009 implements the dedicated request-error mapping and existing reporting/systemic exit categories. Its CLI matrix covers missing/malformed/comma values, invalid/file paths and all exit classes. |
| AC-28 | T003/T004 own safe source reasons/early termination; T005 owns F1/F2/local/mismatch precedence and safe declaration-derived failures; T006 propagates registry failures; T007/T008 test safe provenance in both reports. T010 composes the complete precedence chain and ordinary regression. |

No missing or circular AC ownership was found. No verification-only obligation
lacks a behavior owner; preserved registry/metric behavior appropriately uses
existing implementation plus wiring/regression ownership. No owner is too late
to shape dependent implementation: each code task requires tests before
completion, with composed verification before documentation and convergence.
The reverse check covers every planned component and S1–S4 contract, resource
limits, stable source/dependency reasons and S5 validation obligations.

### Safety, checkpoints and authorization boundary

T003 explicitly owns nonblocking/no-follow final opens for BOTH files, immediate
regular-file fstat, descriptor-only bounded reads, strict decoding, cleanup and
capability failure without fallback. Its two FIFO tests replace validated regular
inputs at the final-open hook, invoke real production flags without a writer,
and use bounded subprocess guards with no sleeps. T004 adds source-state and
no-lookup assertions: Gemfile failure leaves unknown N and prevents lock access;
lock failure follows established scope and retains N without rows. T010 requires
the composed P1 evidence. Pre-existing FIFO fixtures alone cannot satisfy them.

T005 owns F1's nonpublic-source-before-missing-direct ordering after whole-lock
acceptance and F2's unsupported_requirement, safe omission, denominator and
no-lookup policy. T007/T008 verify both public representations. These preserve
the approved product/architecture decisions and ordinary authorization ordering.

Checkpoints after T005 and T010 inspect useful completed contracts: safe scoped
evidence before integration, then public behavior and all deterministic witnesses.
T013 is a separate read-only convergence gate after documentation and required
real-root evidence. T012 requires later explicit human authorization naming the
target or permitted supplied evidence; no external access occurs in this review.
Unavailable authorization leaves T012 pending and T013 gated. Optional live smoke
has no mandatory successor, needs separate authority and cannot substitute for
offline correctness or independently established real-root selected population.

### Observation and verification

Only prior run 005-0012 is appended. Its machine handoff is preserved except for
the authorized human /status metadata and explicit context reconciliation:
context=continued because the observed session matches 005-0011 despite the
fresh-context request. Its context_note retains repository grounding and approved
specification/plan. This is observational provenance, not a product finding;
005-0011 is not changed. Credits_before remains blank and no delta is derived.

Verification confirms 005-0001–005-0012 exactly once, 44 fields per record,
earlier ledger bytes unchanged, tasks.md byte-unchanged, 13 stable acyclic tasks,
all 28 independently traced ACs, and earlier review history preserved as a byte
prefix. Only the ledger and this appended review record change. No product code,
implementation, feature tests, external target access, network or push occurred.
`git diff --check` passes. One local review-evidence commit is authorized.
