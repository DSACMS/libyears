# Human-Centered SDD Workflow

This is the canonical lifecycle, review and handoff guide for this repository's
spec-driven development (SDD). It makes demonstrated practice reusable; it does
not authorize a feature, stage, external action or exception by itself.

## Where authority lives

| Source | Responsibility |
|---|---|
| [AGENTS.md](AGENTS.md) | Fundamental repository and product rules, engineering boundaries and Git discipline. |
| [AGENT_ROUTING.md](AGENT_ROUTING.md) | Provisional task, model, effort and decomposition guidance. |
| This document | Lifecycle, review, authority and handoff mechanics. |
| [observations/README.md](observations/README.md) | Observation schema, recording rules and provenance protocol. |
| `specs/NNN-*/` | Feature-specific decisions, approved contracts, review history and verification evidence. |

Humans supply consequential product decisions, authorization, judgment, scope
selection and exceptions. Record those decisions durably where they govern the
feature. Agent recommendations and reviewer findings inform human decisions;
they cannot substitute for missing authority.

Approved durable artifacts carry established state. The specification governs
product behavior; the approved technical plan governs architecture within that
contract; the approved task graph governs bounded work and dependencies.
Technical planning authority does not permit changing product requirements.
Task execution additionally requires explicit authorization for the task or
phase, including its checkpoints and stop conditions. An approved graph alone
does not authorize implementation or external validation.

Read frozen artifacts alongside their current approval disposition in
`reviews.md`. Historical pending paragraphs remain evidence of earlier gates.
Agent findings require validation; neither author confidence nor reviewer
prestige overrides approved authority. Stop on conflicting contracts or a missing
decision rather than editing an approved artifact to justify a choice in code.

## Normal lifecycle and gates

The normal substantial-feature progression is:

1. Discovery: establish evidence, alternatives, uncertainty and open decisions.
2. Human selection or decision where required; retain the decision and scope.
3. Specification, then independent specification review.
4. Bounded correction and independent reverification when needed.
5. Technical plan, then independent plan review.
6. Bounded correction and independent reverification when needed.
7. Task graph, then independent task-graph review.
8. Authorized implementation phases with explicit independent checkpoints.
9. Documentation and validation, distinguishing preparation from completed evidence.
10. Read-only convergence across authority, implementation, tests and documentation.
11. Retrospective and human roadmap review.

This is a normal progression, not a requirement to impose every stage on work
whose repository authority explicitly defines a smaller lifecycle. Preserve
acceptance-criteria traceability throughout. A planning witness is a proposed
verification method, not a passed implementation test. Required validation and
optional smoke checks remain distinct; an optional check must not become a
mandatory predecessor by accident.

**A run stops at the next unresolved human authority gate.** Agents do not
continue by momentum into specification, planning, task decomposition,
implementation, external validation or the next feature unless explicitly
authorized. Naming the next gate reports readiness; it grants no permission.
When a prompt authorizes several stages, continue only through resolved gates
within that scope. Never cross an unresolved human authority gate.

**Internal quality gates are not automatic human authority gates.** When durable
authority already determines the permitted next action, APPROVE continues to the
next already-authorized phase; REVISE permits a bounded correction determined by
the approved spec/plan/tasks, regression evidence, freeze and fresh focused
non-author verification; INCOMPLETE permits completing already-authorized review
or evidence. Continue after approval. Humans are not routine message buses for
internal tasks, reviews or correction cycles.

Stop when NEW human authority is required: consequential unresolved product or
security choices, scope expansion, credentials/new trust authority, unauthorized
external-target access or package-manager/target execution, push/release/publication,
or a gate explicitly designated HUMAN by durable authority. Required evidence
and mandatory task predecessors still apply.

## Freeze, independent review and correction

An author's self-audit prepares a candidate; it is not independent approval.
Freeze the candidate before commissioning independent review. Identify the exact
version with a commit or digest and preserve the reviewed bytes and baseline.
Keep later approval dispositions in the review record so the candidate remains
inspectable without an approval-only edit.

Use fresh non-author reviewer contexts where available. Give reviewers the
question, authority, frozen candidate, evidence locations and completion
obligations. Include verbatim exceptional authority preconditions and STOP conditions
when compliance with them is part of the review; an artifact summary can omit a
controlling restriction (Feature 006, run 006-0014). They inspect authority and
evidence directly rather than relying on an author's summary. Recover truncated reads before claiming coverage.
Do not share current sibling conclusions before reviewers complete their work.
Retained historical reviews remain available as historical evidence.

The parent validates material findings against the underlying evidence and
reconciles coverage, omissions, overlaps and cross-boundary behavior after
reports complete. Approval is not majority voting: positive slices cannot
overrule a validated material finding elsewhere.

| Review result | Meaning |
|---|---|
| **APPROVE** | The assigned review completed with sufficient evidence and no unresolved material finding blocking that gate. Approval applies only to the reviewed scope. |
| **REVISE** | Validated findings require correction before approval. State review completeness separately; partial reviews can establish real findings. |
| **INCOMPLETE** | Required review obligations remain unaudited or unsupported. Identify inspected coverage, remaining obligations and blockers. Approval is not established. |

**INCOMPLETE != product defect.** Likewise, a completed review returning REVISE
can be successful audit execution. Keep completion, findings and verdict
separate; environmental failure does not itself establish product failure.

The focused-correction pattern is:

`validated finding -> bounded correction -> freeze -> fresh focused non-author verification -> approval or another explicit gate`

Verify both the finding's closure and relevant collateral obligations. A focused
verification does not claim a new full audit. Do not broaden correction scope
opportunistically. If a new consequential decision is required, stop at that
authority gate. Preserve original findings, incomplete attempts, revisions and
closure evidence in review history.

## Decomposition and human attention

Where delegation is authorized, prefer bounded child assignments when broad
cross-artifact verification has separable obligations, technical surfaces can
be inspected independently, parallel reviews need independent contexts, or
implementation ownership can be disjoint safely. Give each assignment explicit
scope, evidence and completion conditions; parent synthesis must still assess
the whole gate and interactions. Parallel implementation requires explicit
authorization and dependency readiness.

Detailed model and effort choices remain provisional in AGENT_ROUTING.md.
Decomposition is an evidenced option, not a proven universal efficiency gain
or a reason to weaken standards. No specific model is a permanent requirement.

Humans should provide consequential authority and judgment, not act as routine
message buses between automatable stages. When authority permits, one
human-launched run should record the prior observation and perform the next
substantive stage. Authorized orchestration can also collect review reports
internally. Do not combine stages across an unresolved human decision merely
to reduce coordination.

## Observation baton

Follow [observations/README.md](observations/README.md) for the schema and exact
recording protocol; this guide adds no columns or telemetry requirements.
The normal baton is:

`substantive run -> write /tmp handoff before final report -> human /status -> next substantive run records prior handoff plus authorized status enrichment -> next work proceeds`

The commissioning prompt identifies the handoff destination and recording
authority. Verify its keys and run identity before reporting. Before appending,
check for an existing row; verify it rather than duplicating it. Preserve earlier
bytes and all handoff fields except explicitly authorized enrichment, including
runtime notes and confounding classifications. Keep temporary handoffs outside
Git. Do not reconstruct missing observations from memory.

Children do not receive ledger rows; they are orchestration within the parent
observation. Do not invent unavailable child model, effort or resource telemetry
from requested settings or the parent's identity. Account-credit continuity is
provenance, not exact per-run billing; do not derive or store a canonical credit
delta. Runtime-confounded observations are not active-compute measurements.
Clerical-only recorder runs are normally unnecessary when the next substantive
run can safely record the prior baton.

## Commit boundaries and reporting

Make coherent, authorized local commits, normally one per completed SDD task.
Keep unrelated cleanup out. Preserve historical artifacts and findings; do not
amend history merely to make the lifecycle look linear. Apply AGENTS.md's
verification and Git rules. Push, release and publication remain separately
authorized actions.

A normal final report briefly covers the following applicable categories:

- Status/run and artifact or result.
- Authority decisions and review findings or remaining limitations.
- Verification actually performed.
- Local commit and working-tree state.
- Next gate and observation handoff.

Add feature- or stage-specific facts naturally. Avoid giant repeated templates;
never imply a proposed witness ran or a gate was approved when it was not.

## Prompt design

**PROMPTS CARRY DELTAS AND NEW AUTHORITY.**
**THE REPOSITORY CARRIES ESTABLISHED STATE.**

A normal prompt identifies the run/stage, new human decisions or authorization,
prior handoff and status enrichment, exceptional permissions or boundaries,
requested next gate and hard stop. Point to the governing artifacts and current
approval record.

Normally do not repeat the approved specification, complete acceptance lists,
architecture already in `plan.md`, history already in `reviews.md`, stable
observation procedure or standard final-report shape. Materialize any exact
normative input that is otherwise unavailable; a summary cannot replace it.
Brevity is not itself a goal. Complex new authority can require a longer prompt;
human readability, inspectability and auditability govern the amount of detail.

## Evidence basis and limits

Supported lifecycle practice comes from Feature 004's
[review history](specs/004-rubygems-support/reviews.md) and
[retrospective](specs/004-rubygems-support/retrospective.md), especially Feature
005's [retrospective](specs/005-gemfile-group-scope/retrospective.md),
[reviews](specs/005-gemfile-group-scope/reviews.md) and
[task graph](specs/005-gemfile-group-scope/tasks.md), and Feature 006's
[specification and plan correction records](specs/006-nuget-selected-evidence/reviews.md).
Feature 006 corroborates focused correction and frozen approval practice; one
run is not universal evidence.

Model-tier causal comparisons remain weak, actual child telemetry is often
unavailable, and decomposition evidence is observational. Runtime and credit
readings retain their provenance limitations. Phase-sized authorization and
routing choices remain provisional options, with no measured universal savings
in resources or human attention. This canonical workflow preserves demonstrated
mechanics without promoting those hypotheses into permanent requirements.
