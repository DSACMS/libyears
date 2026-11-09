# Feature 006 Retrospective

For the later ordinary-repository journey through published `0eabe303…`, see the
[post-feature methodology retrospective](methodology-retrospective.md) and
[prospective methodology handoff](methodology-handoff.md). The account below
retains its original T018 chapter boundary.

Feature 006 is **CONVERGED through T017/K6**, with 36/36 acceptance obligations
reconciled at `33726aa`. This T018 candidate, run `006-0017`, closes the feature
story and prepares human roadmap review. Independent disposition belongs in
[reviews.md](reviews.md); this candidate is frozen before that review. No release,
next feature, architecture migration or external execution follows from closure.

## Feature Story

Libyears can now consume a deliberately bounded NuGet snapshot: one explicitly
selected SDK C# project, its root schema-1 `packages.lock.json`, and an explicitly
accepted supplied provenance witness. It counts supported direct PackageReferences,
including tests, tools, analyzers and PrivateAssets. It does not evaluate MSBuild,
restore packages or infer deployed dependencies. Ordinary scans do not activate
NuGet. Requests express intent; only the lock's resolved value supplies selection.

This feature began with encouraging selection evidence and ended with a useful
negative measurement result. The pre-selection [OASim experiment](../../discovery/nuget-oasim.md)
corroborated 51 direct associations across ten net10.0 contexts, with assets,
experimental locks and package-list JSON agreeing. These shared a producer;
they were not independent resolvers or evidence of public publication fitness.
The [discovery](discovery.md) compared those artifacts and recommended lock-only
selection. Human H1–H4 accepted conservative declarations, qualified supplier
coherence, bound source/content authority, and catalog-created first-receipt dates
with the greatest currently listed stable comparator.

The resulting chain separates declaration, selection, actual supplying origin,
content correspondence and publication authority. A public package with the same
name and version cannot supply missing provenance. Matching hashes cannot prove
origin, producing history or absence of unsupported influences. Those distinctions
became decisive during validation, rather than remaining abstract warnings.

[Specification review](reviews.md#decomposed-independent-specification-review--006-0003)
found two defects before code existed. F1 replaced raw request spelling with a
bounded normalized-minimum comparison: `1.0` coheres with `[1.0.0, )`, while
unequal minimums never cohere merely because selections match. F2 removed an
unreachable dependency ambiguity reason: duplicates and multivalue selections
already invalidate the whole lock. The approved contract retained 36 stable
criteria with concrete failure oracles.

Technical-plan review then found P1: socket inactivity timeouts and pre-request
checks could not enforce absolute package/scan deadlines. Its correction introduced
one trusted isolated Python metadata worker, parent monotonic supervision and
finite termination/reaping, with 60/300-second budgets. That architecture is
substantial for a small CLI, but follows the approved elapsed-time guarantee.
It permits no target code or package manager in the consumer.

Implementation followed foundations T001–T006, transport/worker/metadata
T007–T009, coherent scan/JSON/human/CLI activation T010–T013, composed offline
acceptance T014, validation preparation T015 and required real-root T016.
Independent gates protected the transitions. Public activation waited until
scope, authority, summaries, both renderers and documentation worked together.
The metric remained unchanged and schema-v3 additions remained ecosystem keyed.

## The validation turn: replay is not contemporaneous evidence

The [006-0013 preflight](validation-006-0013.md) inspected ten authorized candidate
project/lock pairs. All locks passed framing; only two projects fit the declaration
subset, and none had a supplied witness. It preserved twenty exact input byte
comparisons and stopped without a scanner invocation. Eight rejected projects
are evidence of this subset's restriction in one family, not a general rejection
rate or permission to broaden the parser.

The [006-0014 producer experiment](producer-evidence-006-0014.md) retained useful
native package identity/source/hash evidence from an isolated replay. It also
crossed a mandatory authority precondition: copied inputs and disabled directory
imports did not establish original-context equivalence. The overall result remains
**D / BLOCKED**, an execution-scope deviation, even though narrower package evidence
was useful. Both initial reviewers lacked the verbatim source STOP condition;
once supplied, both superseded approval with REVISE. Documentary correction and
fresh verification made the account truthful; they did not authorize past execution.

The human then refined H3 into two bound classes: native producer-time NuGet
package provenance, plus contemporaneous producer attestation binding that evidence
to exact project/lock bytes, framework and required influence assertions. Later
serialization can preserve an existing attestation; replay cannot create one for
a historical event. The consumer still accepts testimony rather than independently
authenticating chronology. Existing envelope and parser mechanisms sufficed;
reporting/help/docs needed a bounded correction, independently approved at `a383440`.

[006-0016](validation-006-0016.md) finally supplied a NEW controlled original-root
producer event under exact new authority. It used MatchRunProfileUpdater/net10.0,
isolated generated state and an explicitly controlled baseline, without claiming
historical/default-context equivalence. Before execution, review caught a PATH
plugin-discovery isolation gap; the corrected plan was frozen and re-reviewed.
Native acquisition records and contemporaneous testimony were captured separately,
linked to the inputs and serialized faithfully into the strict witness. The event
closed, temporary cache/payload/obj state was removed, and 29 retained artifacts
were frozen before consumer use. Four local decoded SHA512 values agreed.

The independent public-expectation helper initially failed DNS/TLS before a response,
while the product's existing verified trust selection worked. Original partial
expectations and captures remain. A bounded preparation correction reused that
existing trust selector, independently parsed public metadata, froze complete
expectations, obtained fresh approval and ran exactly one corrected human/JSON
pair. These were neither blinded observations nor backdated prospective expectations
for the original pair.

The final result was **0/1 measured, coverage 0.0, `content_hash_mismatch`**.
The public catalog SHA512 actually disagreed with native/local content identity.
The product correctly withheld publication and per-row age. Total 0.0 is the empty
sum of measured rows, not a zero-age measurement; mean/median/maximum are null.
A separate raw audit found 55 public versions and latest listed stable 5.0.0,
but its public date could not authorize the mismatching local content. Cause,
generality and signing/hash-domain fitness remain unestablished. Positive live
yield has not been demonstrated.

Fourteen corrected comparisons passed, including scope/selection, safe omissions,
aggregates, human/JSON agreement and three unchanged input bytes plus revision.
Independent producer and final validation audits approved this bounded failure-path
evidence; existing authority imposed no positive-yield threshold. K5 therefore
completed without weakening H3. Three fresh convergence slices covered 18+7+11
accountable criteria, and parent cross-boundary reconciliation established K6.
Scoped integrity checks are not whole-tree invariance or an OS-wide execution trace;
product request URLs were not independently traced. These limits survive closure.

## What independent review changed

The [review history](reviews.md) preserves each rejected candidate, correction,
freeze and focused re-verification. Passing suites did not override counterexamples.

| Finding | Demonstrated gap and bounded closure |
|---|---|
| F1 / F2 specification | Normalize supported producer minimums; remove an impossible ambiguity oracle while retaining whole-lock rejection. |
| P1 architecture | Replace admission-only elapsed checks with killable in-flight supervision and explicit lifecycle witnesses. |
| K1-F1 implementation | Apply version/component bounds to all lock and closure fields before association; reject whole-source overflow without capabilities. |
| T008-V1 verification | The real-worker test passed without publishing a command. Add positive blocking-handler entry evidence and require the no-command mutation to fail. This was a test defect, not proven deadline failure. |
| Windows test portability | Capability-dependent reads and FIFO tests assumed POSIX. Separate real-reader prerequisites, portable synthetic semantics and unskipped fail-closed refusal; retain LF byte bindings. |
| K2-M1 metadata | Two missing alias values were mistaken for equality. Require usable material on every alias before reconciliation; preserve singleton failure reasons. |
| K3-C1 privacy | Capitalized malformed NuGet options escaped sanitization. Fold detection only, preserving exact lowercase activation and ordinary parser behavior. |
| 006-0014 authority | Supply the exact source STOP condition to review; retain the deviation and blocked outcome rather than promoting replay to original evidence. |
| H3 / prospective preparation | Explain the refined trust meaning; fix plugin isolation before production and missing public expectations before the corrected consumer pair. |

Named findings overlap across reviewers and stages; summing ledger finding counts
would not yield a defensible defect total. Parent validation, discriminating
mutations and collateral regressions supplied closure, not majority voting or
reviewer prestige. Focused re-verification did not pretend to repeat whole audits.

## INHERENT COMPLEXITY

NuGet separates minimum requests from selection, supports evaluated declarations,
and allows imported/central/generated influences. Static bounded declarations
therefore need a qualified completeness claim. Source authority differs from
content identity; first receipt differs from listing/update dates; complete
listed-stable enumeration differs from compatibility. These are domain and trust
problems that a cleaner module layout cannot remove. The actual hash disagreement
shows why preserving uncertainty is part of the capability.

## ARCHITECTURAL COMPLEXITY

The feature adds focused project/lock/provenance/version/registry modules and
staged safe records, descriptor-based reads, bounded transport and a process
supervisor/protocol. P1's deadline requirement accounts for much of the process
machinery; it is an explicit guarantee with portability and cleanup costs.
Shared scan/output modules also contain ecosystem-specific availability and
evidence branches. Those are credible pressure points for future modularity
investigation, not proof that a generic plugin or resolver framework is needed.

An **ecosystem-analyzer/modular-monolith seam deserves bounded exploration**.
A useful investigation would map current source-to-lookup-to-summary responsibilities,
locate repeated changes to shared files, and test whether a small explicit interface
preserves each ecosystem's distinct trust and failure semantics. Compare that
with keeping the present explicit source pairs. Stop if abstraction hides domain
rules, adds indirection or has no demonstrated maintenance benefit. No migration,
interface selection or analyzer refactor is authorized here.

## PROCESS COMPLEXITY

Early runs used short human-mediated stage/correction loops. At K1 and T008,
separate correction/continuation prompts were required by then-current authority.
The human later authorized continuation through already-defined internal gates;
`ac13716` clarified the distinction in [SDD_WORKFLOW.md](../../SDD_WORKFLOW.md).
Run 006-0012 proceeded from portability correction through required CI evidence,
metadata correction, integration, K4 and T015, stopping at genuinely new real-root
authority. Run 006-0016 similarly carried production, validation corrections and
convergence internally. Humans still controlled product/trust decisions, exact
external targets, producer exceptions and publication.

The commissioning human's **17K-prompt information-architecture signal** should be
read as qualitative process context, not a measured prompt series: the ledger
contains no prompt character/hash measurements for these sixteen runs. Workflow
commit `1042e62` made lifecycle/review/baton mechanics canonical while routing and
observation schema retained their own owners. Prompts can then carry deltas and new
authority instead of reprinting established state. This improves navigability in
principle; no token, time or attention saving was measured. A growing review record
and historical pending paragraphs still impose navigation work; current disposition
pointers are essential. This run makes only a small demonstrated correction:
review assignments must receive exact exceptional preconditions, prompted by 0014.
No routing-tier mandate or observation-schema change is warranted.

## Human attention, elapsed runtime and observation limits

The canonical [ledger](../../observations/agent-runs.csv) now contains 006-0001–0016
exactly once. This run is handed off separately and is not appended. Of those
sixteen observations, twelve record complete work, three incomplete and one blocked. These are assigned
run completion states, not a product success rate. Fifteen explicitly mark runtime
confounded and one unknown. Reported runtime is absent for 0012. All prompt counts
and hashes are blank. Child telemetry is unavailable; requested fresh forks without
overrides do not prove actual child settings or total resource use.

Account readings include supplied continuity observations, including 45 and 49
for 0016; they are not exact task billing and no credit delta is derived or stored.
An intervening unnumbered recovery run breaks earlier continuity. Runtime includes
approval waits, orchestration and environment effects; it does not measure active
compute. Heterogeneous tasks and changing candidates prevent causal model/effort
or early-loop versus autonomous-run comparisons. No aggregate cost ranking follows.

Internal dispatch removed the need for humans to relay those reviewer messages;
that mechanical change is visible. Net attention minutes, reading effort and
coordination savings were not measured. Human attention also paid for rich evidence,
status enrichment, trust decisions, recovery and review of this synthesis.
The goal is fewer unnecessary relays with equally inspectable authority, rather
than autonomous continuation through unresolved decisions. Feature 004's
[retrospective](../004-rubygems-support/retrospective.md) supplied the initial
hypotheses; Feature 005's [retrospective](../005-gemfile-group-scope/retrospective.md)
demonstrated decomposed gates and prospective logging. Feature 006 extends those
observations without converting them into controlled experiments.

## Testing cost and reusable capabilities

Testing cost may be scaling poorly, but the evidence establishes pressure rather
than a measured scaling law. Feature 004 retained 289 deterministic tests, Feature
005 390, and Feature 006's final correction 632. These cumulative suites cover
different obligations and cannot identify marginal cost per ecosystem. Feature 006
required real-process positive witnesses, mutation checks, fake-clock arithmetic,
platform capability/refusal cases, exact-SHA CI and composed cross-ecosystem output
and availability matrices. Repeated review regressions have resource cost, but
that cost and maintenance hours were not captured.

Observed Windows failures were test portability defects. Corrected `77d66b9`
received explicit lifecycle/offline/whitespace PASS across Windows Python 3.11–3.13
and six POSIX jobs. Unchanged relevant worker/import/workflow bytes retain that
specific evidence; later CLI tests were not thereby executed on Windows. Safe-reader
primitives can still be unavailable there and must fail closed. Configuration of
CI, local success and worker portability are three different claims.

Before changing test architecture, gather which shared changes force which suites,
platform skip/refusal behavior, repeated fixture setup and maintenance effort.
Preserve component, composed and real-process evidence where they prove different
properties. Avoid replacing direct behavioral witnesses with tests that mirror a
new abstraction. Any test consolidation should demonstrate equivalent defect
discrimination and reduce real maintenance burden.

| Capability | Reuse supported now / limitation |
|---|---|
| Existing metric, SourceResult availability and ecosystem-keyed schema | Actually reused unchanged in meaning; NuGet-specific null handling and evidence still required explicit integration. |
| Verified transport and opt-in bounds | Shared transport was extended without changing older defaults; public authority/path and publication policy remain registry specific. |
| Safe-reader technique | Reused from Ruby's descriptor approach, with a NuGet-local reader. Capability refusal and byte binding are reusable techniques, not universal filesystem support. |
| Bounded worker/controller/protocol | Demonstrated NuGet implementation and test patterns. Extraction for other ecosystems is unproven and would require separate design/authority. |
| LocalAuthority and staged safe evidence | Useful separation of permission from observation; origin/date/request rules must remain ecosystem specific. |
| Frozen candidates, focused independent correction, mutation witnesses and observation baton | Demonstrated repository methodology; generalized harness or SKILL.md distribution remains an investigation, not a shipped tool. |
| Producer bundle/attestation discipline | Reusable evidence-capture pattern under explicit producer authority; the product never acquires caches or creates provenance itself. |

## What we would do differently and human handoff

Check the complete provenance/event contract and a prospective producer-capture
route earlier, before treating selection agreement as end-to-end feasibility.
Probe public/native hash correspondence within exact authorized boundaries before
investing further in useful-yield expectations; a mismatch still cannot authorize
a policy workaround. Commission review with verbatim exceptional authority and
STOP conditions. Design tests to prove entry into the operation they claim to
cancel, and run platform capability/refusal separation before the first required
Windows publication. Freeze independent expectations before affected captures and
retain failed attempts when correction is needed.

Use phase-sized authority with internal quality gates when the work is already
determined, while keeping consequential product/security/external actions human
controlled. Retain the smallest readable current disposition and link to deeper
history. Measure attention and maintenance burden prospectively before claiming
that more orchestration, documentation or abstraction is efficient.

After independent retrospective approval, reconcile ROADMAP with completion and
preserve four evidence-gathering opportunities: ecosystem analyzer/modularity,
dependency-metadata providers including ecosyste.ms, a generalized human-centered
agentic-development harness with possible SKILL.md distribution, and the human-requested
Java ecosystem repodive. Human demand for the latter is supplied by this closure
commission, not reconstructed from an earlier repository record. Provider comparison
must test scope, source authority, date/hash fidelity, coverage and reproducibility;
no provider adoption follows from recording it. None selects Feature 007 or grants
research, external access, runtime dependencies or architecture migration.

The separate queued human-table alignment and synthetic GitLeaks maintenance are
authorized after this retrospective approves, with their own frozen changes,
regressions and independent reviews. The historical hosted secret-check failure
remains a limited observation; local synthetic reproduction never established its
entire hosted cause. Maintenance must not weaken scanning or rewrite history.
The feature story is reconstructable from durable contracts, findings and actual
validation, with qualitative prompt context and missing resource telemetry clearly
qualified. **Next product gate: HUMAN ROADMAP SELECTION.**
