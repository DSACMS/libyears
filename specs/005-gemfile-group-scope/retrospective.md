# Feature 005 Retrospective

Feature 005 remains **CONVERGED / COMPLETE through T013**, with 28/28
acceptance criteria accounted for. This retrospective, run `005-0020`, follows
baseline `e415d63`; it closes the requested synthesis work without changing the
product or issuing another convergence verdict. The next gate is **HUMAN ROADMAP
REVIEW**. Feature 006 has not begun. No release, tag or push is implied.

## Feature Story

Feature 004 measured all direct Ruby dependencies recorded in a root lockfile.
Feature 005 adds explicit measurement of selected **declared Gemfile groups**.
For example, `--ruby-group test` measures the supported declarations belonging
to `test`, using independently authorized exact lock versions. Repeating the
option selects a union, counting each dependency once. Ordinary scans retain
all-direct lock behavior and do not inspect Gemfile. A group called `production`
has no special meaning; this feature does not reconstruct deployment or runtime
state. Its static recognizer rejects the whole Gemfile when unsupported syntax
prevents establishment of complete scope.

The journey began with uncertainty. [Discovery](discovery.md) in `005-0001`
investigated the Gemfile opportunity and other radar evidence, but stopped at
HUMAN DECISION REQUIRED. Three independent candidates and two blind reviews
were internal work within that one run. Their preference could inform a human;
it could not select a product. The human then selected bounded static group
measurement, accepted conservative rejection and preserved the all-direct
default. Run `005-0002` recorded H1–H3 and renamed the neutral discovery directory
(`2263bae` discovery; `9b77451` selection).

The initial [specification](spec.md) in `005-0003` completed its drafting task
while leaving approval blocked on Q1–Q3. Human clarification supplied the closed
syntax boundary, activation and reporting direction. Q2 materially changed the
draft: differing textual requirement evidence must prevent exact-version
association, rather than merely qualify a measurement. Run `005-0004` reconciled
those decisions into 28 stable criteria. A broad independent audit in `005-0005`
was INCOMPLETE and established no defect. Decomposed review in `005-0006`
completed the gate but returned REVISE for two contract gaps. Correction and a
fresh focused review in `005-0007` approved the specification (`68589b3`).

Technical planning repeated that distinction between incomplete audit and
defective candidate. Run `005-0008` drafted the [plan](plan.md); `005-0009` did
not finish its independent cross-artifact audit. Three bounded reviews and parent
synthesis in `005-0010` completed it and established a possible blocking file
open. Run `005-0011` corrected and independently verified nonblocking safe access
for both inputs, approving the plan (`52109ab`). Runs `005-0012` and `005-0013`
created and independently approved a [13-task graph](tasks.md), with separate
foundation, integration, documentation, real-root and convergence boundaries.

Implementation proceeded under phase authority. Run `005-0014` completed
T001–T005: closed parsing, typed evidence, bounded reads, population selection
and authorized lock association. Three fresh non-author reviewers approved the
foundation; 357 deterministic tests passed. T002/T003 share the related
`bbd5737` commit, an openly recorded exception to the normal one-task/one-commit
pattern. Definitions and verification remained separately inspectable.

Run `005-0015` completed the T006–T010 candidate: mixed scanning, JSON, human
reporting, CLI activation and composed acceptance. Despite 388 passing tests,
independent review found that argparse accepted abbreviated group options.
The checkpoint was REVISE, T009 acceptance reopened, and later tasks stopped.
Run `005-0016` corrected that behavior and independently verified it. An
intermediate correction accidentally allowed `--r` to select `--resolved`;
focused testing caught it before the frozen candidate. The corrected checkpoint
passed 390 tests and restored T009 acceptance (`ecc4924`, `8e9579c`).

T011 in `005-0017` documented the feature and prepared validation; preparation
did not satisfy validation. Explicit later human authorization permitted T012
in `005-0018` to inspect three named roots and only their permitted Ruby inputs
and provenance. Independently frozen expectations preceded product invocation.
[Real-root evidence](release-validation.md#t012-authorized-real-root-evidence--005-0018)
retains A's missing-input INSUFFICIENT EVIDENCE, B's successful population
comparison and C's EXPECTED REJECTION of unsupported syntax. B established
empty default and two test dependencies, including union/deduplication behavior.
Twelve offline cases produced 24 agreeing human/JSON reports. Dates were
synthetic adapter output, not observed publication history; no live registry
smoke was required or performed.

Finally, four fresh independent review slices and parent reconciliation in
`005-0019` established T013 CONVERGED (`b9e2441`), with current 390-test evidence
and every criterion inspected. Earlier INCOMPLETE and REVISE states remain in
[reviews.md](reviews.md). Two stale public validation-status phrases were
recorded as nonmaterial editorial lag; canonical completion records supersede
them. This retrospective leaves those files and all product decisions unchanged.

## Evidence and its limits

The primary prospective methodology evidence is
[the schema-v1 ledger](../../observations/agent-runs.csv), runs `005-0001` through
`005-0019`. All 19 are unique; `005-0019` occurs exactly once. Review and task
records supply the underlying gates, witnesses and correction history. Git
corroborates artifact changes and chronology, not unobserved model settings.
This synthesis read the complete six preexisting Feature 005 artifacts; it did
not reaccess external roots, transient child reports or historical conversations.

Evidence categories matter:

- **Direct observations recorded by agents:** requested child settings, task
  concurrency, inspected artifacts, command results, frozen hashes and reproduced
  counterexamples. These are retained reports, not fresh replication here.
- **Human-supplied observations:** post-run `/status` metadata, context
  reconciliation, timer uncertainty and explicit account-reading continuity.
  They supplement machine handoffs with their own provenance.
- **Repository evidence:** approved contracts, review findings, tests described
  by the review record, task status and commit diffs. Historical next-gate text
  describes its original checkpoint, not necessarily current authority.
- **Reasonable inference:** native orchestration removed some manual reviewer
  dispatch/message relay; readable durable artifacts enabled continuation.
  Neither has a measured attention-saving magnitude.
- **Untested hypotheses:** causal model comparisons, controlled lower-resource
  child configurations and generalization beyond this feature.

The ledger's task-class labels are observations too: `005-0005` and `005-0009`
say `narrow_verification`, while their assignments required broad cross-artifact
reconciliation. Analysis follows the actual obligations; historical rows remain
unchanged. A completed draft with a blocked approval (`005-0003`) is coherent.
A completed review requiring revision is also successful audit execution, not
product approval.

| Descriptive ledger summary | Observation / limitation |
|---|---|
| Completion | 17 complete, 2 incomplete; not a software success rate. |
| Reported parent configurations | 14 GPT-6.1-Sol Medium; 2 GPT-6-Astra Ultra, 1 Medium, 2 Low. Different task shapes and evolving artifacts prevent ranking. |
| Context | 18 fresh, 1 continued; `005-0012` was reconciled from human UI evidence despite a fresh-context request. |
| Runtime classifications | 5 yes, 8 unknown, 6 blank; none explicitly unconfounded. Raw runtime is populated for all 19, but active compute is not established. |
| Environment | 18 normal, 1 degraded (`005-0017`, server restart). Normal does not certify uninterrupted timing. |
| Prompt / execution-mode capture | Prompt count/hash and execution mode blank in all 19. No measured prompt-growth curve is possible. |
| Account readings | All 19 have after readings; only 4 have before readings (`0001`, `0016`, `0018`, `0019`). No exact run-cost claim follows. |

No averages combine discovery, clerical recording, implementation phases and
reviews. No child test counts are added to parent counts to inflate coverage.

## Defects caught by review

These are four material review findings, not the sum of every ledger
`finding_count`: discovery and unresolved decisions also use that field.
The authoritative details and focused closure witnesses are in
[reviews.md](reviews.md).

| Finding / review class | Consequence and correction | What changed |
|---|---|---|
| F1, decomposed specification review `0006`, association slice | Nonpublic Gemfile source plus missing direct lock identity had two possible reasons. `0007` ordered source authority first after whole-lock acceptance; unavailable-lock precedence stayed earlier. | Product contract and AC-28; later plan, implementation and composed tests inherited it. |
| F2, independently overlapping specification slices in `0006`, counted once | An accepted lock could contain an unsupported direct requirement. Copying it was unsafe; null would falsely claim absence. `0007` required omission of `lock_requirement`, safe declaration metadata, known denominator and no lookup, retaining the isolated dependency failure. | Product reporting contract, AC-20/21/28; later typed representation, implementation and redaction/presence tests. |
| P1, decomposed architecture/safety review `0010` | A regular input replaced by a FIFO could block before `fstat`. Child and parent reproduced it. `0011` required nonblocking/no-follow final open, immediate regular-file validation, capability refusal and replacement witnesses for both files. | Technical plan and planned tests; T003/T004 implemented four bounded reader/source witnesses. No product decision changed. |
| C-01, independent CLI/composed-acceptance checkpoint `0015` | Abbreviated options activated scope contrary to the sole-option contract. `0016` rejected prefixes before scan and preserved ordinary behavior. Restoring the old hook in memory made 27 alias subtests fail; 32 ordinary parser invocations matched baseline. | Implementation and tests; T009 status reopened then restored. No spec/plan revision. Methodology: an AC index and green suite cannot replace reading the full contract. |

The incomplete reviews caught none of these as established findings. Decomposed
reviews completed the audits and exposed defects; focused reviews subsequently
closed corrections without claiming fresh full audits. Parent validation mattered:
two specification reviewers overlapped on F2, while positive assessments elsewhere
did not overrule F1, P1 or C-01. Frozen candidates, non-author reviewers, independent
reads and synthesis after reports supplied inspectable independence. Shared
repository context is still shared evidence, not independent ground truth.

## Material Human Interventions

Material human contributions often arrived in the initiating prompt for a later
run. All 19 rows record `human_intervention=no`; under the protocol ordinary
prompt submission does not count as intervention. That field therefore cannot
measure human authority or total coordination. Do not rewrite rows to repair
this analytical limitation.

| Contribution | Material effect / durable source |
|---|---|
| H1–H3 selection before `0002` | Chose measurement of explicitly declared groups, accepted rejection/maintenance tradeoff and preserved compatibility; discovery Human Product Decision and ROADMAP selection. |
| Q1–Q3 before `0004`, especially Q2 | Resolved product ambiguity and changed mismatch from qualified association to refusal; spec decision trace. |
| Commissioning decomposed reviews after incomplete attempts | Changed review methodology in `0006` and `0010`; ledger experiment labels and review structure. Model and decomposition changes were not controlled separately. |
| Phase authority through T005 and T010, then bounded correction | Authorized autonomous task sequences with hard checkpoints and stop conditions; tasks/reviews `0014`–`0016`. This reduced per-task dispatch while preserving human control over continuation. |
| Exact T012 target/input authorization | Permitted three roots, renewed historical baseline access and limited inspection to Ruby evidence/provenance; release-validation record. Prior familiarity granted no access. |
| Status enrichment and continuity attestation | Supplied otherwise unavailable metadata, reconciled `0012` context, and qualified account readings; ledger and observation README change `af01565`. No billing precision was added. |

Routine Git approvals are not counted as substantive interventions. Approval
waits and interruption affected measurement and execution, but approval actors
were often unavailable and are not inferred. Missing `0006` handoff recovery
delayed the `0007` commit despite completed product verification; the ledger
records clerical recovery, without identifying an unsupported actor or authority
change.

## Methodology synthesis

**Routing and task shape.** Both Astra Low broad assignments (`0005`, `0009`)
were incomplete, with no established defect; the latter explicitly records
truncated initial reads and 0/28 independent coverage. Later decomposed reviews
completed on the unchanged respective candidate hashes: Astra Ultra parent
`0006` found F1/F2, and Sol Medium parent `0010` found P1. Sol Medium also
completed the task-graph audit, phase checkpoints and final decomposed convergence.
This supports decomposition as a practical route to sufficient evidence here.
It does not show that Low could never complete those gates, that effort caused
completion, or that decomposition alone explains the difference. Task assignment,
parent configuration, evidence handling and orchestration changed together.

**Native orchestration and access equity.** Sol Medium parent runs demonstrate
native dispatch, bounded child ownership, independent concurrent reviews and
whole-gate synthesis. In final convergence four review slices fit a parent plus
three active-child limit by starting the fourth after one finished. No-overrides
and `fork_turns=none` are requested settings; actual child model/effort/resource
telemetry remained unavailable. The discovery comparison's requested settings
and preference are likewise not controlled capability measurements. An accessible
parent's success cannot certify an entirely lower-resource team. Contributors
without premium access need readable obligations and composable evidence, with
human or alternate reviewers able to continue the same gate. No gate should
silently require a named premium model on this evidence.

**Human attention and authorization.** Runs `0014` and `0015` each covered five
tasks plus review in one human-launched run. Native orchestration carried reviewer
assignments and returned reports internally; humans did not need to act as
message buses between those children. The human still chose scope, commissioned
phases, supplied observations and controlled new target authority. Attention
minutes, manual messages avoided and net savings were not measured. The missing
handoff incident shows observation administration can itself consume attention.
Phase-level authority is promising when dependencies, allowed edits, review
freeze and stopping gates are explicit; there is no controlled per-task comparison.

**Prompt delta and durable context.** Every run was repository-grounded. Approved
decisions and accumulated evidence could be resumed without reopening product
choices, including after interruption. The ledger's artifact counts show the
review record growing from 6,703 words at `0014` to 11,729 at `0019`; the current
six-artifact set totals 3,475 physical lines. These are descriptive artifact sizes,
not context-window measurements or a cause of any incomplete review. Prompt
hashes/counts are absent. Compact future prompts should carry the new assignment,
authority and stop condition, pointing to durable state rather than copying it.
Repository-native context also needs an explicit current approval record so old
pending paragraphs do not cause invented blockers. Read in bounded ranges and
recover truncated reads; merely requesting fresh context does not prove it.

**Observation baton and enrichment.** The temporary JSON handoff separates a
run's machine observations from later human `/status` additions and the eventual
append. It avoided current-run self-recording and supported exact prior-row
checks, but the missing `0006` baton shows it is an operational dependency.
Reliable harness capture can reduce manual transcription; it must distinguish
components when versions differ (`0002`) and preserve supplied confounding notes.
Later status values may enrich fields previously unavailable to the agent, while
notes saying they were unavailable describe the earlier handoff, not a reason to
erase enriched values. Child identities/settings and actual telemetry remain
different categories.

**Credits and runtime.** The README already documents directly observed account
readings and explicit no-intervening-activity continuity. Run `0001` records
175/214; later records include 253/255, 1/3 and 3/5. The discontinuity between
`0016` and `0017` is not explained by the ledger; no reset, purchase, consumption
or cross-gap continuity is inferred. These readings are not exact run receipts.
Five runs explicitly flag runtime confounding: waiting/spinning (`0006`), an
interrupted approval (`0016`), restart (`0017`) and approval waits (`0018`/`0019`).
All other rows are unknown or blank, not proven active-time measurements. No
active-compute or cost-per-finding estimate is justified.

**Environment, safety and stop behavior.** Tool-output truncation is an evidence
acquisition/completeness problem, not a software failure. Restart and sandbox
Git failures are environment/tooling events. Temporary-root canonicalization in
the P1 witness, JSON-format comparison in T011, and absent-copy/summary assertions
in T012 were harness errors corrected without changing product expectations.
C-01 was an implementation defect; A's missing inputs and C's conservative
rejection were not. Required real-root population evidence remained separate from
optional live smoke, and synthetic dates never became publication claims.
Recorded stops preserved selection, clarification, correction, external-access
and phase boundaries. Greater model capability supplied no missing permission.

**Publication hygiene.** Public artifacts retain safe target labels, hashes,
outcomes and decision provenance; exact local mappings and temporary captures
remain nonpublic. This synthesis adds no private paths, trust identifiers or raw
target content. F2 shows publication safety also belongs in schema presence and
omission rules, before implementation. The ledger is append-oriented historical
evidence; neither nicer classifications nor richer telemetry justify rewriting it.

## Routing and observation assessment

These classifications describe the smallest changes justified now. They retain
[AGENT_ROUTING.md](../../AGENT_ROUTING.md)'s provisional status and do not select
permanent model identities.

| Proposed treatment | Classification | Action / basis |
|---|---|---|
| Broad review needs explicit slices, completeness and parent reconciliation; consider decomposition before expensive escalation | SUPPORTED UPDATE | Add Feature 005 gate evidence to principles 3/4. Repeated incomplete attempts and later completed audits support the procedure, not a causal capability ranking. |
| Sol Medium native orchestration as a demonstrated option, reducing human reviewer relay | SUPPORTED UPDATE | Record observed parent runs and telemetry limits. No mandatory model rule or quantified attention saving. |
| Prefer phase-sized authority with hard checkpoints when task readiness permits | PROVISIONAL UPDATE | Offer as an option; five-task phases worked, but per-task overhead was not compared. |
| Keep prompts to assignment delta plus durable authority pointers | SUPPORTED UPDATE | Clarify repository handoff practice and truncated-read recovery; token savings unmeasured. |
| Require actual controlled child settings before claiming lower-resource equivalence | SUPPORTED UPDATE | Make equity limitation explicit alongside the accessible-parent evidence. |
| Raise broad-review effort permanently or require premium models | INSUFFICIENT EVIDENCE | No routing mandate; confounded, small observational series. |
| Replace fresh/continuing-context guidance or existing authority/security gates | NO CHANGE | No comparative evidence warrants replacement; existing boundaries were useful. |
| Change schema v1 or retrospectively relabel task classes/interventions | NO CHANGE | Existing 44 fields suffice for these modest documentation clarifications. |

[observations/README.md](../../observations/README.md) gains a bounded handoff
procedure: verify all 44 ordered keys and persist the baton before reporting;
check uniqueness before authorized append; preserve provenance during status
enrichment; leave actual child telemetry unavailable unless observed. It also
clarifies that initial-prompt authority can matter even when the intervention
field is no. These address observed handoff loss, context reconciliation and
interpretation gaps without a schema change or mandatory extra human capture.

## Open hypotheses and next human gate

- Can decomposition alone reproduce these gates with actual child model/effort
  controlled on accessible configurations? Parent labels cannot answer it.
- What causal differences, if any, follow from model tier or effort when task,
  candidate, prompt and tools are held constant? Nineteen heterogeneous runs are
  not a controlled benchmark.
- Can reliable active-runtime and precise per-run resource accounting be captured
  without disproportionate collection cost? Account continuity is insufficient.
- Do native orchestration and phase authorization save net human attention after
  reading, synthesis and observation administration are included?
- Do the same decomposition boundaries work for other feature shapes or weaker
  repository evidence? This feature does not establish generality.
- Would lightweight handoff validation, automatic harness enrichment or a future
  parent/child telemetry relation improve evidence enough to justify tooling or
  schema evolution? These are future investigations, not implemented requirements.
- How much durable review detail is sufficient before context and human reading
  costs outweigh additional auditability? No prompt-size series was captured.

The next feature should start from explicit human product selection, bounded
authority and a readable current evidence record. This is a method lesson only.
ROADMAP states are unchanged; no opportunity is promoted, selected or investigated
here. **Next gate: HUMAN ROADMAP REVIEW. Do not begin Feature 006.**

## Verification of this synthesis

The starting ledger SHA-256 is
`fabb7c6e70686df1fd1001ffbc474634fdace024178c43fe7e933a93170ed23e`.
Verification checks the same bytes, exactly 19 ordered unique run IDs and 44
fields per row; no `005-0020` row is appended. Claims above trace to the linked
ledger, complete durable artifacts and cited commits. All six preexisting
Feature 005 artifacts, ROADMAP, implementation and tests remain unchanged.
Only this retrospective, provisional routing guidance and observation-method
documentation change. No Feature 006 artifact is created. Product tests and
external validation are not rerun for this prose-only synthesis; the 390-test
result is retained T013 evidence. Local links, scope/integrity assertions and
`git diff --check` are checked before the authorized local commit.
