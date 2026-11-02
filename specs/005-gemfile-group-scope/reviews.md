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

## Independent post-T005 implementation checkpoint — 005-0014

**Date:** 2026-10-30. **Completion:** COMPLETE. **Verdict:** APPROVE.
**Completed boundary:** T001–T005. **Material findings:** 0.
**Foundation status:** Safe to use for T006 under later explicit human continuation.
**STOP:** T006–T013 remain unstarted; this approval does not commission them.

Reviewed baseline: `7099669`; frozen product implementation: `09be9fb`.
Task commits: `4e6f7b4` (T001), `bbd5737` (T002/T003), `e4c5f01` (T004),
`09be9fb` (T005). Final phase verification in tasks.md was frozen before review;
only lifecycle/review records change afterward. No checkpoint remediation occurred.
Approved spec/plan and all prior review history remain unchanged.

### Reviewer structure and independence

Three fresh native children were commissioned after implementation and phase
verification froze, with `fork_turns="none"` and no model/effort overrides.
They were separate from all implementation authors and ran concurrently.
Each independently read repository authority, history/diff, relevant code/tests
and task evidence. No reviewer received sibling conclusions or author reasoning;
no cross-review communication occurred. Actual child model/effort/resource
telemetry was unavailable. Children are orchestration details of this one
human-launched run, not separate observation rows.

| Reviewer | Primary slice | Completion / verdict |
|---|---|---|
| `/root/checkpoint_parser` | T001 closed grammar, completeness, validators; T002 compatibility; later-interface boundary | COMPLETE / APPROVE |
| `/root/checkpoint_filesystem` | T003 bounded reads/P1, both FIFO replacements; T004 composed availability | COMPLETE / APPROVE |
| `/root/checkpoint_association` | T004 scope/availability; T005 authority, association, F1/F2 and safe evidence | COMPLETE / APPROVE |

The parent reconciled all reports with the approved contracts, implementation
and phase evidence. Approval rests on inspected obligations and witnesses,
not a majority vote. No material finding or missing checkpoint obligation was
identified. Reviewers made no repository edits.

### Findings and completed-task acceptance evidence

- **T001:** The closed static language consumes complete physical lines/files.
  Positive forms, comments/quotes, ordered requirements, default/explicit groups,
  full membership unions, established empty groups, optional membership,
  duplicates/nesting, unsupported unselected code and first-line/completion
  precedence are covered by substantive tables/fixtures. No partial population
  or evaluation occurs. Extracted validators preserve ordinary Ruby framing/order.
- **T002:** Trailing optional fields preserve old positional/default construction.
  Typed evidence distinguishes omitted, present-null and safe textual lock
  requirements; it does not alter registry types or public serialization.
- **T003/P1:** Both inputs use real nonblocking/no-follow final opens and
  immediate regular-file fstat before content reads. Containment, descriptor
  traversal, capability refusal without fallback, strict decoding, limit+1 file
  bounds and cleanup match the plan. Physical-line limits remain in the pure
  parser, composed after reading to preserve earlier-line failure precedence.
  Four real replacement witnesses cover reader and source paths for BOTH
  filenames. Each replaces a validated regular input at final open with no
  writer/sleeps, asserts production flags, no FIFO consumption and descriptor
  closure, under a five-second subprocess guard. Portable capability mocks remain.
- **T004:** Complete recognition precedes exact group validation and lock access.
  Union/case/default/empty/unknown distinctions, no lock read after earlier
  failure, whole-lock rejection and missing/rejected lock availability preserve
  known versus unknown N. Gemfile FIFO replacement gives invalid_gemfile/unknown
  N/no lock access; lock replacement follows consumed declarations and gives
  invalid_lockfile/N=1/no rows. Both forbid lookup.
- **T005/F1/F2:** Exact direct identities alone authorize association; pins or
  matching transitive specs cannot substitute. Nonpublic Gemfile authority wins
  over missing direct identity only after whole-lock acceptance. Existing
  name→requirement→source order and private/GIT/PATH/pinned/multiple-remote
  prohibitions survive. Unsupported direct requirements retain N and safe
  declaration metadata while omitting unsafe lock text and selected artifacts.
  Supported requirement text compares exact null/order/spacing/operator values
  before version selection, without semantic satisfaction/equivalence inference.
  Mismatch has no version artifacts/candidate/lookup. Authorized isolated
  selection failures preserve ordinary artifact rules.

Task-level evidence in tasks.md accounts for the assigned portions of
AC-02–16, AC-21, AC-23/24/28. This is not a claim of completed public acceptance
criteria whose scan/output/CLI portions belong to later tasks. Ordinary Ruby
source/authorization behavior remains compatible. Diff/history inspection shows
no changes to scan, CLI, output, registry transport or metric implementations.
No unauthorized network/external access, target/Ruby/Bundler/package-manager
execution, credentials access, release or push occurred.

### Independent verification, limitations and next gate

Each reviewer independently ran the full deterministic suite: **357 passed,
no skips**. Parser reviewer additionally ran `test_gemfile*.py` (47 passed).
Filesystem reviewer ran `test_ruby_groups.py` (35), `test_rubygems*.py` (53)
and `test_gemfile.py` (26); association reviewer ran `test_ruby_groups.py` (35)
and `test_rubygems*.py` (53). Commands use
`python -m unittest discover -s tests -p 'PATTERN'`; full command is
`python -m unittest discover -s tests`. All independently passed
`git diff --check`. Exact parent phase commands/results are recorded in tasks.md.

No external or real-root validation occurred. Future propagation, aggregation,
serialization, human reporting, CLI activation, composed full-feature acceptance
and authorized real-root evidence remain unverified/unimplemented later work.
No reviewer model/effort or resource metrics can be inferred from this verdict.

Prior observation 005-0013 was already committed at run start in `7099669`.
It exactly matches the supplied handoff and authorized status additions; all
005-0001–005-0013 occur once with 44 fields, earlier bytes unchanged. No duplicate
was appended and no new observation-only commit was created. Current run has
only its temporary 44-field handoff, not a ledger row.

**Next gate:** Later human continuation may authorize T006 after this APPROVE.
This run stops here regardless of approval; no T006 work is begun.


## Independent post-T010 implementation checkpoint — 005-0015

**Date:** 2026-10-30. **Completion:** COMPLETE. **Verdict:** REVISE.
**Executed candidate boundary:** T001–T010. **Material findings:** 1 (C-01).
**Integrated foundation status:** NOT APPROVED pending correction and independent
verification. The previously approved T001–T005 foundation remains intact.
**Next gate:** correction of validated finding C-01. T011–T013 remain unstarted.

Starting approved checkpoint: `cb69795`. Frozen candidate:
`efc231d549fbe754bc51895c4f17c5a3aeb49158`.
Task commits: `a0dbf23` (T006), `e3c4f72` (T007), `7c1d58a` (T008),
`ca6613a` (T009), `efc231d` (T010). Product implementation and tests froze
before reviewers were commissioned. Only review/lifecycle records change after
freeze; no finding was repaired. Approved spec, plan, discovery, prior review
history and T001–T005 product files remain unchanged.

### Reviewer structure and independence

Three fresh native children used `fork_turns="none"`, no model/effort overrides,
and ran concurrently after freeze. None authored implementation. Each read
repository authority and actual code/tests independently; none received sibling
conclusions or communicated across slices. The parent synthesized after all
three completed. Actual child model/effort/resource telemetry is unavailable.
Children are orchestration details of this one human-launched observed run.

| Reviewer | Assigned slice | Completion / verdict |
|---|---|---|
| `/root/checkpoint_scan` | T006 propagation, aggregation, mixed availability/coverage, ordinary compatibility and preserved foundation/wiring | COMPLETE / APPROVE |
| `/root/checkpoint_output` | T007/T008 JSON/human reporting, provenance, safe omission/null, normal/verbose single/mixed branches | COMPLETE / APPROVE |
| `/root/checkpoint_acceptance` | T009/T010 CLI, composed acceptance, independent 28/28 AC reconciliation and scope/regression boundaries | COMPLETE / REVISE, C-01 |

Approval was not decided by majority vote. The parent independently inspected
the implementation/tests and acceptance index, checked unchanged foundation and
contracts, ran the ordered verification below, and reproduced the retained
finding directly against the frozen candidate.

### Validated material finding C-01 — abbreviated scoped option spellings

**Location:** `libyears/cli.py:22` (parser construction), option at line 25;
`tests/test_cli.py:423` (malformed-value tests).
**Authority:** spec S1, lines 61–65: sole `--ruby-group GROUP` option and no alias;
the execution prompt also prohibits unapproved aliases/convenience behavior.
**Owner:** T009; associated activation/usage verification boundary AC-27.

Argparse option abbreviation remains enabled. The reviewer reproduced:
`main([".", "--ruby-g", "test"], scan=Mock(return_value=empty_report()))`
returns **0** and calls `scan(".", ruby_groups=("test",))`.
The parent independently reproduced both `--ruby-g` and `--ruby`, each returning
0 and activating scoped scanning; the canonical `--ruby-group` control did too.
The witness uses an injected empty report and reads no target inputs or registry.
These undocumented spellings violate the approved sole-option/no-alias boundary.

Existing CLI tests reject malformed values, missing values, comma lists, files
and invalid paths, but do not reject abbreviated option spellings. Thus the
passing deterministic suite cannot establish this S1 obligation. This is a
bounded public activation/test defect, not a missing product or architecture
decision and not an authorization to alter ordinary CLI semantics.

**Required subsequent correction:** reject abbreviated scoped-option spellings,
add exit-1/no-scan witnesses, preserve canonical activation and ordinary CLI
behavior, and independently verify the correction. No remediation is performed
in this run. T009's completion checkbox is reopened; its original candidate
execution evidence remains historical. T010 verification remains recorded with
this discovered coverage limitation; the integrated candidate is not approved.

### Acceptance and whole-gate synthesis

**28/28 ACs independently audited; 28/28 have deterministic test evidence.**
The explicit per-AC assertion index is in
`tests/fixtures/ruby_groups/README.md`. Test/module references were validated
against actual repository definitions, including corrected index spellings
before freeze. This is neither full S1 acceptance nor final convergence:
C-01 remains an additional S1 activation obligation adjacent to AC-27.

- AC-01–05: ordinary no-Gemfile-read compatibility, exact public CLI age and
  case, explicit default/production, unique overlapping/multiple/repeated unions.
- AC-06–10: empty versus unknown scope, complete closed-language positive and
  separate negative tables, unsupported unselected code, optional membership,
  duplicates/nesting and whole-lock rejection.
- AC-11–16: safe/missing inputs, both P1 input replacements, no pin/transitive
  fallback, exact textual mismatch, whole-source versus isolated failures,
  private/pinned/GIT/PATH/multiple-remotes and F1 authority ordering.
- AC-17–19: known wholly-unmeasurable 0%, empty/unavailable distinctions,
  sibling numerical survival/count availability, Python-only snapshots,
  three-ecosystem identity and existing PyPI/npm/Yarn/all-direct Ruby regressions.
- AC-20–22: exact scoped schema-v3 dictionaries and omission/null behavior,
  full/requested groups, safe declaration/lock distinction, retained selected/
  publication artifacts, F2 redaction, paired human branches/verbosity/counts,
  supplied-file and observable-publication limitations.
- AC-23–26: guarded reads/execution/archive access, root/decoy/link/containment
  tests, target integrity, four bounded real FIFO witnesses with no writer,
  fixed verified public transport/trust/limits/pacing, canonical platform dates,
  latest stable/arithmetic, exact zero and flagged clamping.
- AC-27–28: tested exit categories and full composed precedence from recognition
  through registry, F1/F2 safe provenance and no-lookup, sibling survival and
  ordinary omissions. C-01 exposes the additional no-abbreviation test gap.

Scan and reporting reviewers found no material defects in their assigned slices.
The parent validated the unavailable known-N and unknown-N summaries, sibling
preservation, explicit scoped serialization, F2 safe omission and ordinary
branches against code and tests. These positive results do not close C-01.

### Deterministic verification and limitations

Parent verification ran focused composed acceptance first, affected ecosystem
regressions second, then the full deterministic suite:

| Exact command | Result |
|---|---|
| `python -m unittest tests.test_ruby_group_acceptance` | 3 passed |
| `python -m unittest tests.test_pypi tests.test_npm tests.test_npm_registry tests.test_yarn tests.test_rubygems tests.test_rubygems_registry tests.test_registry tests.test_metric tests.test_mixed_scan tests.test_scan` | 215 passed |
| `python -m unittest discover -s tests` | 388 passed, no skips |
| `git diff --check` | Passed |

The T010 author independently ran focused acceptance (3), affected feature/
ecosystem tests (352), and full suite (388, no skips), all passing.
Reviewer A ran `python -m unittest tests.test_scoped_scan tests.test_mixed_scan
tests.test_ruby_group_acceptance tests.test_ruby_groups tests.test_gemfile_evidence
tests.test_rubygems tests.test_rubygems_registry tests.test_registry tests.test_metric`
— 166 passed. Reviewer B ran `python -m unittest tests.test_output
tests.test_scoped_scan tests.test_mixed_scan tests.test_ruby_group_acceptance`
— 70 passed. Reviewer C ran the full suite — 388 passed/no skips — and
`python -m unittest tests.test_cli tests.test_ruby_group_acceptance
tests.test_scoped_scan` — 38 passed. Every reviewer passed `git diff --check`
and observed a clean frozen tree. Passing tests are distinguished from the
negative C-01 read-only witness.

No network/live smoke, external/real-root validation, Ruby/Bundler/package
manager/target-code execution, credential/config/archive content access,
release, tag or push occurred. Only synthetic temporary inputs and mocked
registry responses were used. Documentation, required authorized real-root
corroboration and final convergence remain T011–T013; none began. No child
telemetry or resource outcome is inferred from completion/verdicts.

Prior observation 005-0014 was appended in the first coherent implementation
commit from its JSON handoff plus authorized human status additions. Runs
005-0001–005-0014 occur exactly once with 44 fields; preceding bytes are preserved,
credits_before remains blank and no credit delta is derived. Current run has
only its temporary handoff and no ledger row. The candidate remains frozen;
**REVISE** means correction of C-01 is the next gate, with no T011 authorization.


## Focused independent post-T010 C-01 verification — 005-0016

**Date:** 2026-10-30. **Completion:** COMPLETE. **Verdict:** APPROVE.
**Post-T010 implementation checkpoint:** APPROVED. **Material findings:** 0.
C-01 is closed; T009 completion/acceptance is restored and T010 acceptance is
complete for the corrected candidate. The prior 005-0015 REVISE checkpoint and
all earlier review history remain byte-preserved above. This is focused
correction verification, not T013 convergence or real-root validation.
**Next gate:** T011 under later execution authority. T011–T013 remain unstarted.

### Frozen correction and independence

The parent corrected only C-01 in the existing CLI parser subclass and added
two deterministic CLI regression methods plus narrow task evidence. Exact
option matching is unchanged; abbreviation candidates involving `--ruby-group`
are rejected. Ordinary option abbreviations remain compatible, and `--r` stays
a usage error. No aliases, new parsing framework or unrelated behavior changes
were introduced. The complete correction diff was inspected and
`git diff --check` passed before the local freeze commit:
`ecc492407e1e6fd6a3947142b72f9e50ecca423b` (baseline `99dcaf4`).

One fresh native child, `/root/c01_verification`, was commissioned after freeze
with `fork_turns="none"`, no explicit model/effort overrides, and no authorship
participation. It independently read repository authority, approved spec/plan/
tasks, relevant post-T005/post-T010 history, the complete correction diff,
CLI/tests, integration/acceptance witnesses and the 28-criterion assertion index.
It made no edits, repairs or commits and spawned no children. Actual child
model/effort/resource telemetry is unavailable. It is orchestration within this
observed run, not a separate ledger observation.

### Focused evidence and parent synthesis

The child returned COMPLETE / APPROVE, with no material findings. Every proper
long-option prefix from `--r` to `--ruby-grou`, including `--ruby` and `--ruby-g`,
is exercised with separate and equals values and alongside a canonical request:
exit 1, no stdout and no scan. Exact canonical activation, repeated requests,
case sensitivity, sorted deduplication, direct-file rejection and malformed
values remain passing. Its independent canonical equals/repeated control passed;
restoring the former abbreviation hook only in memory made the new regression
fail on 27 alias subtests, demonstrating detection of the original defect.

The parent independently inspected the frozen code/diff, forbidden-prefix
assertions and canonical/repeated controls, reconciled the child result with
S1 and the prior checkpoint, and compared 32 ordinary exact/prefix parser
invocations against baseline `99dcaf4`: identical parsed results/exit codes.
The implementation diff is solely CLI abbreviation handling. Scoped scan
semantics, JSON, human output, source authority, coverage, transport and metric
code are unchanged. The reviewer confirmed T001–T005 implementation/foundation
tests match approved `09be9fb`; parent scope checks confirm no foundation-file
changes. T006–T010 acceptance evidence remains credible with the C-01 gap closed.
Approval rests on these witnesses and unchanged boundaries, not just the verdict.
No new finding was repaired.

Both parent (before freeze) and child independently ran, in order:

| Exact command | Result for each |
|---|---|
| `python -m unittest tests.test_cli tests.test_ruby_group_acceptance` | 32 passed |
| `python -m unittest tests.test_scoped_scan tests.test_mixed_scan tests.test_scan tests.test_output tests.test_ruby_groups tests.test_gemfile tests.test_gemfile_evidence tests.test_gemfile_lock tests.test_pypi tests.test_npm tests.test_npm_registry tests.test_yarn tests.test_rubygems tests.test_rubygems_registry tests.test_registry tests.test_metric` | 335 passed |
| `python -m unittest discover -s tests` | 390 passed, no skips |
| `git diff --check` | Passed |

The child also passed `git diff --check ecc4924^ ecc4924`. Product/tests stayed
frozen throughout review and parent synthesis; only lifecycle/review records
changed afterward. No network services, external validation targets, real-root
scans, Ruby/Bundler/package managers, credentials or target code were accessed.
No T011 documentation/preparation, T012 evidence or T013 convergence began.
No push occurred.

Prior observation 005-0015 is appended exactly once from its JSON handoff plus
only the authorized human /status additions. Runs 005-0001–005-0015 each occur
once with 44 fields; earlier ledger bytes remain unchanged. Credits_before is
blank and no credit delta is derived. Current run 005-0016 is handed off as
44-field temporary JSON and is not appended to the ledger.


## T013 independent convergence review — 005-0019

**Date:** 2026-11-02. **Review completeness:** COMPLETE.
**Final verdict:** CONVERGED. **Independent acceptance accounting:** 28/28.
**Material findings:** none (0). **Missing required evidence:** none.
**T013:** COMPLETE. **Feature 005:** CONVERGED / COMPLETE through T001–T013.
**Next gate:** FEATURE 005 RETROSPECTIVE / ROADMAP REVIEW. That work has not
begun; no Feature 006, release, tag, publication or push is authorized or begun.

Reviewed HEAD: `87007a21f5f513387074146b56e012bab28d4907`. The working tree
was clean at run start. Explicit human authority commissioned only this final
read-only gate, the prior 005-0018 observation, and review/lifecycle evidence.
All six current Feature 005 artifacts, AGENTS.md, AGENT_ROUTING.md, observation
protocol/ledger, ROADMAP.md, SPEC.md, README.md and CHANGELOG.md were read.
The approved specification/plan/task graph, prior reviews, implementation history,
actual code/test assertions and durable T012 record supply the evidence.

### Independent decomposition and orchestration

Four fresh native child reviewers used `fork_turns="none"`, with no explicit
model or effort overrides. Primary responsibilities were distinct; cross-cutting
AC/security checks provided corroboration. No child received sibling conclusions,
read sibling reports or communicated across slices. The parent read the complete
reports and synthesized only after all four finished. Temporary reports remain
outside the repository; the durable evidence needed to review this gate is here.

| Child task | Primary responsibility | Completion / result | Independent execution |
|---|---|---|---|
| `/root/review_a` | Product authority, H1–H3/Q1–Q3, spec/plan/task completeness, dependencies and scope | COMPLETE / PASS | 93 focused tests passed, no skips |
| `/root/review_b` | Actual implementation, P1/F1/F2, security, compatibility, C-01 and regressions | COMPLETE / PASS | 306 + 37 focused/regression tests passed, no skips |
| `/root/review_c` | Public CLI, output/schema, safe provenance and documentation coherence | COMPLETE / PASS | 62 CLI/output/acceptance tests passed, no skips |
| `/root/review_d` | Independent all-AC trace and required T012/validation sufficiency | COMPLETE / PASS, 28/28 | 138 focused and 390 full-suite tests passed, no skips |

The harness allows four concurrent agents including the parent. A/B/D ran
concurrently; C started after B finished, while the remaining reviews were
finishing. Peak reviewer concurrency was three (four agents including parent).
Actual child model/effort/resource telemetry is UNAVAILABLE; requested settings
and task identifiers are observed orchestration facts, not measured telemetry.
Children are internal audit work and receive no ledger rows. This one run does
not establish a causal model/resource comparison or general decomposition claim.

### Parent independent synthesis and task completeness

Convergence is based on inspected evidence, not votes. After every child
completed, the parent reconciled all reports, directly rechecked the authority,
source flow, parser, safe reader, CLI/scan/output boundaries and substantive
assertions, and independently checked historical prefixes and frozen files.
The acceptance index was a locator, never proof by itself.

T001–T012 are complete and dependency-ready in their recorded order:
T001 parser `4e6f7b4`; T002 typed evidence and T003 safe reads `bbd5737`;
T004 scope/availability `e4c5f01`; T005 association `09be9fb`; independent
foundation approval `cb69795`; T006 mixed scan `a0dbf23`; T007 JSON `e3c4f72`;
T008 human output `7c1d58a`; T009 CLI `ca6613a`; T010 composed acceptance
`efc231d`; C-01 correction `ecc4924` and focused approval `8e9579c`; T011
documentation/preparation `0974c56`; T012 authorized offline real-root evidence
`87007a2`. T002/T003's shared related foundation commit is openly documented;
separate definitions and evidence remain reviewable. The graph is acyclic:
T004 requires T001/T002/T003, T009 requires T006/T007/T008, and T013 requires
T010/T011/T012. Both output formats existed before public activation. T011
followed corrected checkpoint approval and T012 followed explicit root authority.

The parent verified every T001–T012 completion record and its required evidence,
not just checkbox totals. Approved spec.md equals its `68589b3` contents;
approved plan.md equals `52109ab`. Foundation product/test files equal
`09be9fb`; all product/tests equal corrected `ecc4924` at current HEAD. No
contract was rewritten to obtain this verdict.

- **P1 CLOSED:** both final inputs open with O_RDONLY/O_NOFOLLOW/O_NONBLOCK,
  immediately undergo regular-file fstat, and read only that descriptor.
  Four real regular-to-FIFO replacement witnesses (reader/source × both files)
  ran without skips, with no writer, pre-read rejection, closed descriptors and
  five-second guards. Capability refusal has no unsafe fallback.
- **F1 CLOSED:** after whole-lock acceptance nonpublic Gemfile authority precedes
  absent direct identity; N survives, unsupported_dependency_source wins and no
  public lookup occurs. Missing/rejected-lock precedence remains earlier.
- **F2 CLOSED:** unsupported direct requirement remains a dependency failure;
  safe declaration metadata/N survive, lock_requirement and selected artifacts
  are omitted, unsupported text never reaches human/JSON, and lookup is absent.
- **C-01 CLOSED:** only exact --ruby-group activates scope. All proper long-option
  prefixes reject before scan with exit 1, including equals/combined requests;
  ordinary option abbreviations and canonical repeated controls remain compatible.
- **Ordinary regressions PASS:** absent-request all-direct Ruby never inspects
  Gemfile; Python/npm/Yarn scopes, mixed ecosystem identities, Python-only
  snapshots, transport and metric behavior remain intact. Full suite passed.
- **Security/resources PASS:** complete closed-file recognition, exact root inputs,
  contained descriptor reads/no-follow replacement handling, 1 MiB/16 KiB/16 MiB
  bounds, strict decoding, exact direct association and independent public source
  gates fail closed. No transitive/pin/public-namesake substitution or semantic
  requirement resolution exists. Existing verified TLS, fixed metadata authority,
  redirect rejection, request/byte limits and pacing remain unchanged. No new
  runtime dependency, ecosystem, metric, resolver or general framework was added.
- **Reporting PASS:** schema 3 remains additive and scoped-only; unknown omitted,
  known absent null and accepted-format states agree with human reports. Known
  empty, wholly unmeasurable and unavailable populations and sibling aggregates
  remain distinct. Safe provenance and supplied-file limitations are explicit.

### Independent 28/28 acceptance accounting

The authoritative requirement for **each** row is approved spec.md S5's matching
AC identifier, together with S1–S4/security qualifications cited by its behavior.
Implementation owners below are reconciled against the task Change/Evidence
clauses and actual code. This table preserves D's independently derived trace;
the parent independently validated the relevant implementation/assertion bodies
and current test results before accepting each row. It is not copied from the
repository's preexisting AC matrix. Every final T013 assessment is PASS.

Test abbreviations: GF=test_gemfile, RG=test_ruby_groups, SS=test_scoped_scan,
CLI=test_cli, OUT=test_output, ACC=test_ruby_group_acceptance,
GE=test_gemfile_evidence (all under tests/). Method names omit `test_`.
R7/R11/R13/R14/R15/R16 denote review records 005-0007/0011/0013/0014/0015/0016
above; R15 is retained REVISE, qualified by R16's corrected approval. Applicable
current independent review is A/B/C/D as assigned above, plus this parent T013
assessment. T012 entries refer to release-validation.md's durable record; a
criterion without a relevant real-root case is satisfied deterministically and
is not falsely attributed to T012.

| AC | Requirement and actual implementation / task owners | Independently inspected deterministic witnesses | Review and T012 corroboration | Result |
|---|---|---|---|---|
| 01 | Ordinary all-direct scans ignore Gemfile; T006/T009. scan_mixed_repository branches on ruby_groups=None to ruby_source_result, which reads only lock. | SS.ordinary_path_never_opens_gemfile_and_retains_source_call covers absent, valid, invalid Gemfile; OUT.ordinary_ruby_shape_is_unchanged_and_scoped_serializer_is_explicit; ordinary Ruby root tests. | R13/R15/R16. T012 is scoped only and makes no ordinary-mode claim. | PASS |
| 02 | Exact public selected declaration associates and measures; case-sensitive groups. T005/T006/T009: _associate_scoped_declarations exact direct index, validate_ruby_groups, real scan/metric call. | RG.exact_direct_candidate_and_full_safe_memberships; CLI.explicit_exact_groups_union_duplicates_and_expected_age compares names/ages/lookups for test/Test/default; ACC.real_adapter_population_reaches_scoped_cli_with_platform_dates. | R14/R15/R16; T012 B independently froze json_schemer 2.5.0 and rspec 3.13.2 in test, then compared exact direct public artifacts and CLI rows. | PASS |
| 03 | Only ungrouped declarations get implicit default; selection explicit. T001/T004/T009: _gem default branch versus explicit groups and selection intersection. | GF.explicit_default_group_is_an_ordinary_membership; RG.union_deduplicates_and_retains_full_memberships_without_default; CLI.explicit_exact_groups_union_duplicates_and_expected_age; ACC.root_read_allowlist_integrity_and_no_implicit_production_or_default. | R14/R15/R16; B empty default versus nonempty test, no default auto-addition. | PASS |
| 04 | Overlapping memberships yield one identity. T001/T004/T006: sorted set memberships; select each declaration once. | GF.block_membership_unions_and_optional_flags; RG.union_deduplicates_and_retains_full_memberships_without_default; CLI exact-groups test checks rows/count/lookups. | R14/R15; B union/repetition demonstrates population identity deduplication, though its individual declarations each have only test membership. | PASS |
| 05 | Multi-group union and repeated request deduplication. T004/T006/T009 canonical sorted(set(...)), declaration intersection. | RG.union_deduplicates_and_retains_full_memberships_without_default; SS.scoped_request_is_canonical_and_chooses_only_scoped_source; CLI canonical forwarding and exact-groups tests. | R14/R15/R16; B default+test and test+default+test yield same two names and one lookup each. | PASS |
| 06 | Established empty block/default gives known zero/null coverage; rejected lock exception retained. T004/T006: parse establishes default/block groups; known count precedes lock. | GF.empty_blocks_and_empty_implicit_default_are_established; RG.known_empty_absent_and_accepted_lock_and_rejected_lock; SS.availability_matrix_with_and_without_successful_siblings; OUT.empty_scopes_keep_requested_inputs_and_recognition_state. | R14/R15; B default 0/0/0 in both scenarios, null coverage, total 0.0. | PASS |
| 07 | Any unknown group stops entire union before lock. T004: issubset check after complete parse before lock read. | RG.complete_recognition_then_unknown_group_prevents_lock_read checks one error/no partial count and only Gemfile read; SS availability matrix. | R14/R15. No T012 unknown-group case required; deterministic witness supplies obligation. | PASS |
| 08 | Whole closed subset recognized; arbitrary/unselected/trailing syntax rejected with no partial population and bounded resource work. T001/T003 parse_gemfile anchored cursor, first defect, byte/line limits. | GF.unsupported_statement_families_never_return_partial_scope; unsupported_calls_options_expressions_and_trailing_tokens; literals_reject_escapes_interpolation_and_newlines; nested_blocks_and_unselected_code_reject; physical-line limit; RG byte/line boundary tests. | R11/R14/R15; C git_source at line 2 rejects full scope; later familiar declarations do not salvage population. | PASS |
| 09 | Optional flags do not change membership/config; nesting rejected. T001 parser validates/discards optional, rejects second active block. | GF.block_membership_unions_and_optional_flags; nested_blocks_and_unselected_code_reject; ACC root allowlist forbids configuration reads with optional:false declaration. | R14/R15. T012 B simple block is not claimed to cover optional/nested cases. | PASS |
| 10 | Duplicate declarations reject, duplicate lock direct identities reject whole lock. T001/T004 seen-name set and existing whole-lock parser. | GF.duplicates_anywhere_reject_without_merging; RG.rejected_entire_lock_preserves_known_scope_even_for_excluded_rows, including duplicate direct; existing lock parser duplicate assertions. | R14/R15. B independently records unique identities, not general duplicate evidence. | PASS |
| 11 | Missing/unreadable/unsafe Gemfile means unknown scope/no lookup. T003/T004 _ScopedRubyReader and early failure return. | RG.nonregular_dangling_and_unreadable_are_safe_failures; escaping_links_never_open_or_read_target; safe_read_reasons_map_to_source_without_salvage; four P1 witnesses include Gemfile reader/source FIFO replacement. | R11/R14/R15; A absent Gemfile => gemfile_missing, N/M null, no rows/lookup/lock processing. | PASS |
| 12 | Missing lock keeps known selected names unmeasurable; declaration pin cannot supply version. T004 missing-lock branch builds only declaration failures. | RG.missing_lock_keeps_pins_as_unmeasurable_safe_declarations; known_empty_absent_and_accepted_lock_and_rejected_lock; OUT.missing_lock_and_missing_direct_omit_unknown_requirement. | R14/R15. A does not cover this because its Gemfile is also absent; do not invent a denominator for A. | PASS |
| 13 | Absent direct identity cannot use transitive spec/pin. T005 direct-name index and lock_dependency_missing. | RG.missing_direct_identity_cannot_use_transitive_spec_or_pin uses rake/Rack/empty direct list despite rack spec; OUT missing-direct exact row/no-lookup assertion; ACC precedence missing-direct stage. | R14/R15; B excludes all transitive specs and uses only two direct identities. | PASS |
| 14 | Excluded names absent; textual mismatch safe two-value evidence with no version/lookup or semantic inference. T005 comparison before selected version. | RG.excluded_and_lock_only_identities_never_become_candidates; textual_mismatch_table_preserves_both_safe_values_without_artifacts covers absence/order/spacing/operator; OUT.mismatch_preserves_both_literal_values_without_version_artifacts and human safe failures; ACC mismatch stage. | R7/R14/R15; B confirms transitive exclusions and absence-equals-absence, no coherence claim. Mismatch itself covered offline. | PASS |
| 15 | Rejected lock retains N but measurement unavailable/no salvaged rows; isolated failures retain N. T004/T005/T006 whole parse then association/availability. | RG.rejected_entire_lock_preserves_known_scope_even_for_excluded_rows; known_empty...; existing_isolated_selection_failures_keep_scope_and_artifact_rules; SS availability matrix. | R14/R15. C is Gemfile failure, not lock rejection; no T012 substitution asserted. | PASS |
| 16 | Independent public authority; private/pin/GIT/PATH/multiple-remotes cannot obtain namesake. T005 _has_public_authority, authorization prefix, Gemfile authority first only after accepted lock. | RG.lock_authority_prefix_precedes_mismatch_and_selected_evidence; f1_nonpublic_gemfile_precedes_missing_direct_after_lock_acceptance; nonpublic_gemfile_does_not_override_unavailable_lock_precedence; ACC F1/local-authority stages. | R7/R14/R15; B independently validates single public remote/unpinned direct names and exact generic specs. C never reaches lock authority. | PASS |
| 17 | Empty, unavailable and wholly unmeasurable remain distinct; latter coverage 0%. T006/T008 aggregation plus disclosure branches. | SS.availability_matrix_with_and_without_successful_siblings; OUT.human_empty_unavailable_and_wholly_unmeasurable_remain_distinct. | R15; A/C null unknown states versus B default 0/0/null and B missing-date 2/0/2/0%. | PASS |
| 18 | Scoped source failure preserves sibling measurements/unknown denominator rules. T006 separate source pairs and availability summaries. | SS.availability_matrix_with_and_without_successful_siblings checks full MetricSummary states; ACC.cli_precedence_stages_safe_output_and_successful_siblings repeats all 11 stages with/without siblings and checks preserved pypi/npm rows and totals. | R15. T012 intentionally mocks Python/npm sources absent to respect root authorization; makes no sibling claim. | PASS |
| 19 | Ordinary Python/npm/Yarn/mixed identity unchanged. T006/T009 absent keyword branch; Python-only snapshot; no adapter/parser redesign. | SS.three_ecosystems_keep_same_name_and_snapshot_python_only; CLI.resolved_remains_python_only_and_verbose_json_is_identical; full deterministic existing PyPI/npm/Yarn/mixed tests. | R15/R16 ordinary abbreviation/control comparisons and broad regression. T012 explicitly does not inspect sibling content. | PASS |
| 20 | Safe paired human/JSON names, sources, requirements, counts/limitations; unsupported text absent. T007/T008/T011 explicit serialization and scoped disclosures. | OUT.human_measured_scope_and_evidence_match_json_in_both_branches; human_failures_retain_safe_metadata_and_omit_unsupported_text; human_source_reasons_are_contextual_and_safe; ACC 11-stage normal/verbose human/JSON. | R7/R15; T011 docs/examples; all 24 T012 reports paired and reconciled on population, full memberships, counts, source recognition, limitations and safe evidence. | PASS |
| 21 | Schema 3 additive evidence, exact presence/null/omission and selected/publication artifacts; ordinary unchanged. T002/T005/T006/T007 model trailing defaults, safe construction/propagation and explicit dictionaries. | GE omitted/null/text and compatibility tests; OUT.source_evidence_presence_and_null_format_across_unavailable_states; measured_evidence_keeps_full_memberships_requirement_order_and_artifacts; known_absent_requirement_is_null_on_success_local_and_registry_failure; f1_and_f2_preserve_safe_evidence_and_never_echo_unsafe_text; mismatch/scoped-failure/ordinary tests. | R7/R14/R15; T012 A/C requested evidence and null format; B accepted format, [] declaration requirements, present null lock requirement, selected artifacts only, no invented publication artifacts. | PASS |
| 22 | No production/deployed/runtime/history certification. T007/T008/T011 scoped labels/disclosure and docs. | OUT human-measured test asserts literal non-certification and publication limits; ACC separate test/default/production rows; README/SPEC/change note describe supplied-file scope. | R15; T012 explicitly limits application coverage, actual history, runtime/deployment, pair coherence and integrity claims. | PASS |
| 23 | No execution/install/resolve/credentials/target mutation. T001/T003/T004 pure parser and root-only read pipeline. | GF.parser_does_not_access_files_network_or_execute_code; ACC execution/archive guards, builtins/io/open allowlist, credential/config/include/gemspec decoys and before/after bytes; RG unchanged inputs. | R14/R15; T012 socket/urllib/subprocess guards and permitted-input before/after manifests. No real-root reaccess in this review. | PASS |
| 24 | Only supplied root inputs; no outside target/included/nested/parent/alternate files; scoped direct-file usage error. T003/T004/T009 reader containment and request validator. | RG missing-decoy/internal/escaping/dangling/replacement tests; both final symlink/directory replacement and both FIFO reader/source witnesses; ACC allowlist; CLI.scoped_direct_file_and_invalid_paths_are_usage_errors. | R11/R14/R15; A no descendant substitute; B/C only authorized root inputs plus authorized provenance; C no search to recover unavailable revision. | PASS |
| 25 | Existing verified TLS/trust/authority/redirect/transport limits. T006 reuses RubyGemsAdapter; no transport changes. | SS.scoped_default_adapter_retains_ca_bundle_and_trust; ACC.real_adapter_population_reaches_scoped_cli_with_platform_dates asserts fixed URLs, authority, timeout, byte bound, CERT_REQUIRED/hostname verification and pacing; existing registry/Ruby registry tests in 390 suite. | R15/R16. T012 intentionally uses injected synthetic results and cannot prove live transport; optional smoke not required. | PASS |
| 26 | Existing canonical observable dates/latest/arithmetic/exact zero/flagged clamp. T006 reuses measure_dependency and publication results. | ACC.real_adapter_population_reaches_scoped_cli_with_platform_dates checks 731/365.25 and earliest admissible platform dates/excluded prerelease; SS.same_version_zero_and_flagged_timestamp_clamping; full metric/registry regression tests. | R15; B synthetic same used/latest 2020-01-01 => exact 0.0; this is adapter-output validation, not actual release history. | PASS |
| 27 | Completed evidence reports 0; usage/path 1; systemic 2; sole exact option. T009 validate before scan and parser errors; C-01 hook rejects abbreviation candidate sets. | CLI malformed/missing/comma, direct-file/path, evidence-failure/empty completed reports, request/systemic mapping; abbreviated_group_options_are_usage_errors_before_scan covers every proper prefix in separate/equal/canonical combination; ordinary_option_spellings_and_abbreviations_remain_compatible. | R15 recorded C-01 REVISE, R16 closes it and restores T009/T010; all 24 T012 evidence reports exit 0 with empty stderr. | PASS |
| 28 | Safe distinct source/dependency failures and deterministic precedence including F1/F2/P1. T003/T004/T005/T006/T007/T008 safe early returns, authorization order and serialization. | ACC.cli_precedence_stages_safe_output_and_successful_siblings checks 11 stages through registry, safe markers and lookups; RG f1/f2, unavailable-lock precedence, unknown-before-lock and both composed FIFO witnesses; OUT exact omission/safe metadata tests. | R7 F1/F2; R11 P1; R14/R15 implementation reviews; A and C show higher-priority Gemfile errors/no lock processing/lookup, B registry missing-date is dependency-level known population. | PASS |


### Required T012 assessment and validation separation

The parent independently reconciled the durable T012 procedure, chronology,
expectation hash, input provenance, selected identities, counts, lookup sets and
integrity statements. Existing evidence is sufficient; no original root or
nonpublic transient capture was accessed again. This is audit of durable recorded
observations, not a fresh external reproduction.

- **A — iv-cbv-payroll: INSUFFICIENT EVIDENCE.** Both exactly named inputs were
  absent. The default probe establishes no population. Gemfile/gemfile_missing,
  unknown N/M, null format, no rows/lookup/later lock processing agree across
  formats. Absence/provenance integrity is preserved. This is not counted as a
  successful population comparison and no denominator is fabricated.
- **B — price-transparency-guide: PASS.** Independently frozen full-input
  interpretation establishes empty default and test={json_schemer, rspec}, exact
  public direct versions 2.5.0/3.13.2, no requirements (absence equals absence),
  unpinned identities and one authorized public remote. Transitives are excluded.
  default gives N/M/U=0/0/0 and null coverage; test, default+test and repeated
  test+default+test give the same two identities and one lookup each per report.
  Supplied mocks yield 2/2/0, coverage 1.0, exact 0.0 ages; missing dates yield
  2/0/2, coverage 0.0, release_date_missing. Safe membership/null requirement/
  selected-artifact evidence and human/JSON values agree. Input/Git manifests
  match before/after. Supplied 2020 timestamps are explicitly synthetic adapter
  output, not publication observations; publication artifacts are not invented.
- **C — dpc-admin: EXPECTED REJECTION.** git_source at physical line 2 lies
  outside the closed language, so complete-file recognition rejects despite
  familiar later declarations. unsupported_gemfile_syntax, unknown N/M, null
  format, no rows/lookup or product lock processing agree across formats.
  Independent lock inspection is explicitly distinct from product acceptance.
  Input manifests match; unavailable revision/status remain unavailable, and no
  whole-checkout or clean-tree claim is inferred.

T012's 12 offline cases/24 paired CLI reports account for all targets and scenarios
(4 A + 16 B + 4 C reports), exit 0 and matching safe evidence. The expectation was
frozen before product invocation; two harness-only assertion/printer corrections
are preserved without changing that population oracle. Ruby-only sibling source
isolation and socket/urllib/subprocess guards respect the authorized boundary.
No network, Ruby/Bundler/package manager, target code or target mutation occurred.
B supplies the required successful real-root population comparison. A/C follow
approved missing-input/conservative-rejection behavior; B compensates for no
defect and neither other outcome is disguised as success.

Required deterministic verification and required authorized real-root evidence
are COMPLETE. Optional live registry smoke is NOT REQUIRED, not commissioned
and not performed. It has no outgoing mandatory dependency and cannot replace
either required gate. No fresh external access was needed by this review.

### Public documentation, history and limitations

README/SPEC/CHANGELOG describe the exact implemented activation, supported static
subset, conservative rejection, all-direct compatibility, safe additive evidence,
coverage distinctions, resource limits and supplied-file claims. T011's checked
synthetic examples and actual paired output assertions agree. No installed,
deployed, runtime, historical-coherence, complete-publication-history or broad
application-coverage claim is introduced.

**Nonmaterial stale lifecycle wording, left unchanged:** README.md:397–398 calls
real-root validation pending; SPEC.md:810–812 calls it future. These T011-era
cross-reference descriptions lag completed T012. The linked canonical validation
disposition and detailed T012 record, independently corroborated by tasks.md,
unambiguously establish completion and all three outcomes. The phrases change
no product contract, authorization, evidence sufficiency or success claim. They
are recorded as editorial lifecycle lag, not a material finding or missing gate;
a later authorized retrospective/roadmap review may consider them. No repair is
performed. AGENTS.md's older Feature 004 no-Gemfile language is qualified by its
explicit approved-feature precedence rule; public docs state the scoped exception.
Historical next-gate text is preserved under later approval/completion records.

Historical integrity is verified: original discovery uncertainty; deliberate
human selection H1–H3; draft clarification and Q1–Q3 resolution; initial incomplete
spec review; decomposed F1/F2 REVISE and focused correction/approval; initial
incomplete plan review; P1 REVISE and focused correction/approval; approved task
graph; post-T005 approval; original post-T010 C-01 REVISE; correction/focused
approval (including intermediate --r failure); T011 preparation; all T012 outcomes.
The parent compared nine historical review versions (`b8a52bb`, `68589b3`,
`591da21`, `d8a6e19`, `52109ab`, `63f6135`, `cb69795`, `99dcaf4`, `8e9579c`)
as exact byte prefixes of pre-T013 reviews.md. This is not a fictional straight-line
success story. No incomplete attempt is converted into a product defect or pass.

Limits: finite closed-subset tests do not prove arbitrary Ruby support; a passing
real-root population comparison does not establish general application coverage.
This review relies on sufficient durable T012 evidence, with its explicit absent
inputs, synthetic dates, unavailable C revision and permitted-input integrity
boundary. It did not inspect transient captures or reaccess targets. Child actual
telemetry and run-level timer/account readings are unavailable. No causal
performance or billing conclusion is made.

### Current verification, observation and lifecycle boundary

New parent verification in this run, distinct from historical 005-0016 evidence:

| Command | Current result |
|---|---|
| `python -m unittest tests.test_cli tests.test_ruby_group_acceptance tests.test_ruby_groups` | 67 passed, no skips |
| `python -m unittest discover -s tests` | 390 passed, no skips |
| `git diff --check` | Passed before recording; repeated on final evidence diff |

Retained historical results remain 357 post-T005, 388 original post-T010 (with
C-01 still open), 390 corrected post-T010, and T011 62 focused/six example
checks. They are not relabeled as new runs. Independent child results are listed
above and do not inflate the parent count.

005-0018 is appended exactly once from its JSON handoff plus authorized human
/status fields and account continuity: credits_before=1, credits_after=3. These
are account-level observations, not exact per-run billing; no delta is derived or
stored. runtime_confounded=yes and the existing Git approval-wait runtime note
remain unchanged. All 005-0001–005-0018 occur exactly once with 44 fields, earlier
ledger bytes preserved. Current 005-0019 and children are not appended.

Only observations/agent-runs.csv, this appended review, and narrow T013/task
lifecycle status change. All implementation, tests, spec, plan, discovery,
README/SPEC/CHANGELOG and T012 evidence remain unchanged. All prior review bytes
remain a prefix. One coherent local review-evidence commit is authorized; no
push/tag/release/publication, remediation or Feature 006 work occurred.
Feature 005 is CONVERGED / COMPLETE through T013. Retrospective/roadmap review
remains the next separate human gate; no full retrospective lifecycle closure or
release is claimed here.
