# Post-Feature-006 methodology retrospective

Run **006-0033** closes the chapter at published product candidate
`0eabe303a11a297939b0f8271e47f9e409a4fd49`. It supplements the original
[T018 retrospective](retrospective.md); that account remains correct for its
then-approved contract. This chapter includes the subsequent maintenance and
product-policy journey. It grants no Feature 007, execution or publication authority.

The repository is the primary evidence. Linked records preserve contemporary
claims, refusals, revisions and approval dispositions. This is a reconstruction
from those records, not a transcript of prior conversations. Interpretations are
identified below. Two additional process observations—fresh-parent routing and
pre-push output confusion—come from the commissioning human for this retrospective.
They are labeled as such rather than backdated into earlier run evidence.

## Feature Story: the ordinary command kept asking the product question

A technically literate user wanted a repository answer: run libyears against
OASim and learn how old its dependencies were. NuGet made that apparently simple
question unusually demanding. A project request is not necessarily a resolved
version; a lock is not proof of its producing event; a public package identity is
not proof of where local bytes came from. The work initially tried to establish a
strong chain across all of these claims. The eventual product distinguished them.

The [initial investigation](../../discovery/nuget-oasim.md) found ten SDK C#
projects, 51 literal PackageReference occurrences and 24 distinct IDs. Those were
research facts, not yet an accepted measurement population. A separately authorized
producer experiment later corroborated all 51 selections across ten contexts.
That execution authority never transferred to the consumer CLI.

Feature 006 deliberately implemented an explicit one-project precision interface.
Its completed contract required accepted bound provenance and public content
agreement before age measurement. Specification and architecture review corrected
request normalization and unenforceable elapsed deadlines before implementation.
Later tests and reviews corrected bounds, aliases, privacy and worker witnesses.
The final controlled live result was **0/1, content_hash_mismatch**. That was a
successful refusal under the contract, not demonstrated useful positive yield.
The original retrospective preserves the costly producer-event learning, including
006-0014's authority deviation and subsequent genuinely authorized new event.

The ordinary command then became the recurring human product-intent acceptance
test. Each surprise was classified before changing the contract:

| Chapter / durable evidence | What the ordinary journey established | What it still could not claim |
| --- | --- | --- |
| [006-0018 operational smoke](../../maintenance/operational-smoke-006-0018.md) | Root command: `Ecosystems: none`, **0/0**, null coverage. An explicit nested project activated NuGet but lacked accepted provenance. | Absence of root inputs was not absence of C# dependencies. Contract conformance did not answer the repository question. |
| [006-0020 recognition](../../maintenance/nuget-root-recognition/validation.md) | Listed ten bounded C# candidates, with explicit selection guidance; still **0/0**, no NuGet measurement. | Discovery did not select, aggregate or authorize contents. Initial depth policy suppressed the list; an explicitly reviewed contract correction fixed that policy. |
| [006-0021 investigation](../../discovery/nuget-repository-sources.md), [006-0022 correction](../../maintenance/nuget-repository-sources/validation.md) | The human approved automatic independent project sources and occurrence weighting. Ten attempts: two supported populations with three declarations; eight populations unknown. | Raw inventory 51 was still not an admissible denominator. Solution edges and cross-project deduplication could not define the population. |
| [006-0023 parity](../../discovery/measurement-evidence-parity.md), [006-0024 cascade](../../maintenance/measurement-evidence-cascade/validation.md) | Measurement was separated from historical acquisition/content assurance. Accepted v1/v2 namespace and selection could authorize dates without successful content comparison. | Ordinary no-witness invocation still had eight unsupported populations and two missing whole-evidence sources: no accepted repository N or ages. |
| [006-0025 retained-lock investigation](../../discovery/nuget-population-basis.md), [006-0026 snapshot population](../../maintenance/nuget-snapshot-population/validation.md) | A distinct resolved-snapshot population could be accepted through bound v3 testimony, after unsupported but well-framed declarations. Eight structurally eligible sources represented 48 Direct records. | Actual accepted fallback B remained **zero** without explicit acceptance; ordinary repository N remained unknown. This did not automatically make population 51. |
| [006-0027 acceptance decomposition](../../discovery/nuget-snapshot-acceptance.md), [006-0028 qualified repository snapshot](../../maintenance/nuget-repository-snapshot/validation.md) | Approved current-pair policy B1 established **N=51**: A two sources/three occurrences, B1 eight/48. Full ID/request/framework parity replaced repeated supplier-population acceptance for qualified ordinary pairs. | **M=0**, repository coverage **null**, total 0.0; 48 individual namespace refusals plus two unavailable A sources. “0/51” is journey shorthand, not a claim that coverage was 0%. No historical producer association was recovered. |
| [006-0029 namespace investigation](../../discovery/nuget-namespace-authority.md), [006-0030 conventional comparator](../../maintenance/nuget-conventional-comparator/validation.md) | A disclosed public age comparator convention admitted ordinary qualified A/B1 pairs: **33/51**, coverage 64.70588235294118%, **26.550874794502747 measured-subset libyears**. | Eighteen occurrences in MRCalc/OASim remained `nuget_comparator_ambiguous` because alternate-source eligibility was still a veto. The subset total was not a complete repository result. |
| [006-0031 alternate-source investigation](../../discovery/nuget-alternate-source-comparator.md), [006-0032 positive comparator](../../maintenance/nuget-positive-comparator/validation.md) | Human-selected positive-contrary-evidence policy removed only the unassigned alternate-eligibility veto: **51/51**, 100%, **51.77572640368723** libyears. All 51 use `conventional_public_policy`. | This assumes public-history correspondence. It proves no acquisition, content correspondence, producer history, evaluated completeness, runtime use or deployment. Positive private/conflicting assignment, public exclusion and unknown relevant mapping still refuse before HTTP. |

The final human display rounds to total **51.78**, mean **1.02**, median **1.32**
and maximum **3.63**; exact mean is 1.015210321640926, median
1.3155551897482698 and maximum 3.630960922059979. The retained
[51-occurrence projection](../../maintenance/nuget-positive-comparator/measurement-oasim.csv)
and independent operational review support those numbers. They describe one
bounded target and registry observation, not universal NuGet yield. This run did
not execute OASim, inspect its checkout or contact a registry.

**CODE / CONTRACT CONVERGENCE != SATISFACTORY ORDINARY USER JOURNEY.**

Interpretation: the ordinary command was a stable product question while contracts
evolved around it. A converged implementation could truthfully refuse and still
leave that question unanswered. The human supplied the missing usefulness and
risk judgments; agents supplied investigations, alternatives, implementation and
adversarial evidence. Neither acceptance tests nor reviewers could authorize the
new population or comparator convention themselves.

## Material human interventions

The following **13 grouped interventions** are an analytical decision log, not a
message count or a count derived from `human_intervention`. Initiating questions
are paraphrased from durable consequences where exact wording is unavailable.
Rows 1–11 have linked repository evidence; rows 12–13 also use explicit current
commissioning evidence. Routine submissions, review relays and Git approvals are
not individually counted. “Repeat?” means whether future users must repeat the
same policy choice, not whether future execution needs authorization.

| # / category | Problem and human judgment | Authority changed; durable consequence | Repeat? |
| --- | --- | --- | --- |
| 1 Product scope/trust | Selection evidence was available, but use/selection/origin/date were different claims. Select bounded NuGet and resolve H1–H4. | [Discovery](discovery.md) and approved spec fixed the initial precision contract and explicit producer exceptions. | No for settled contract; new producer/target access remains explicit. |
| 2 Product intent | Why did the ordinary root report no ecosystems / 0/0? Require classification and a useful recognition path. | [0018](../../maintenance/operational-smoke-006-0018.md) preserved expected behavior plus UX gap; [recognition](../../maintenance/nuget-root-recognition/spec.md) selected bounded discovery, not implicit measurement. | No repeated recognition decision. |
| 3 Population semantics | Why require manual project selection for a repository answer? Accept source-qualified occurrence weighting. | [Repository-source authority](../../maintenance/nuget-repository-sources/spec.md) permits independent automatic attempts; repeated membership contributes repeatedly, with independent versions. | No; new portfolio/deduplication semantics would need a decision. |
| 4 Evidence floor | Why make age depend on maximal provenance? Select progressive measurement evidence. | [Cascade](../../maintenance/measurement-evidence-cascade/spec.md) separates namespace/selection/dates from event/content assurance without bypassing contradictions. | No for this approved claim floor. |
| 5 Population alternative | Conservative parsing leaves eight populations unknown despite retained locks. Accept a separately asserted resolved snapshot. | [Snapshot population](../../maintenance/nuget-snapshot-population/spec.md) adds B/v3 after unsupported well-framed A; explicit acceptance is not manufactured. | Policy no; accountable testimony still needs acceptance where used. |
| 6 Reusable snapshot policy | Which acceptance facts can the repository establish, and which are supplier assertions? Select qualified current-pair B1. | [Repository snapshot](../../maintenance/nuget-repository-snapshot/spec.md) authorizes full observable parity without claiming history/evaluation; B2 testimony remains distinct. | No for qualifying pairs; ambiguity/conflicts still matter. |
| 7 Comparator policy | Public age comparison was conflated with acquisition origin. Accept disclosed conventional public comparator and ordinary A floor. | [Comparator](../../maintenance/nuget-conventional-comparator/spec.md) admits bounded policy comparison, preserving stronger testimony/mapping and precision semantics. | No; accepted correspondence risk remains disclosed. |
| 8 Alternate-source policy | 18/51 remained blocked by eligibility alone. Accept private same-ID/version history risk and public identifier disclosure. | [Positive comparator](../../maintenance/nuget-positive-comparator/spec.md) removes only that veto; positive contrary evidence still blocks. | No for existing policy; weakening contrary-evidence rules needs new authority. |
| 9 Workflow | Human relays were repeatedly needed for determined internal corrections. Authorize bounded continuation through internal gates. | [Original process account](retrospective.md#process-complexity) and SDD_WORKFLOW distinguish agent quality gates from new human authority. | No routine message-bussing; unresolved consequential authority stays human. |
| 10 Security | Historical synthetic findings blocked publication. Authorize two exact historical exceptions, then separately authorize each later prose exception. | [0019](../../maintenance/gitleaks-exact-exceptions-006-0019.md), [0031](../../maintenance/gitleaks-exact-exceptions-006-0031-review.md): exact fingerprints and negative controls, no broad suppression. | Yes for a new exception; prior permission is exhausted. |
| 11 Observation | Missing telemetry and intervening maintenance made continuity ambiguous. Correct account-boundary methodology. | [Observation rules](../../observations/README.md), [0027 reconciliation](../../discovery/nuget-snapshot-acceptance-review.md): real bookkeeping work is an account boundary; runtime is not reconstructed. | Continuity attestation is still needed when not directly observable. |
| 12 Publication/evidence | Local readiness and asynchronous hosted evidence were being treated as one gate. Human publishes exact candidate; current assignment confirms publication and requires truthful asynchronous treatment. | Read-only remote verification in this run confirms both mains at `0eabe303…`. Hosted results for it remain unobserved; local readiness is not hosted closure. | Publication remains separately human-authorized; queue completion is not a new product choice. |
| 13 Actor routing | “Fresh parent context” was repeatedly assigned inside agent prompts to an actor unable to create it. Commissioning human identifies the routing defect. | [AGENT_ROUTING](../../AGENT_ROUTING.md#actors-capabilities-and-authority) now assigns parent-context creation to human/orchestrator and separates requested from observed context. | No repeated rule decision; orchestrator must perform and verify it per assignment. |

## Human gates as scaffolding, with limits

The recurring successful pattern was: unknown boundary → explicit human authority
→ evidence gathering → adversarial review → reusable policy → executable tests
→ durable repository knowledge → future human need not repeat the policy choice.
This is an interpretation supported by the linked correction lifecycles, not a
universal rule that every gate should disappear.

Project selection became automatic source attempts after the human chose occurrence
semantics. Explicit snapshot acceptance split into facts current files could
establish and a new qualified current-pair product convention. Comparator
acceptance split from acquisition provenance, then alternate-source eligibility
split from positive contrary assignment. Each step narrowed its claims and retained
refusal controls; none made the repository an oracle about historical acquisition.

Three kinds of gate need different treatment:

1. **Unavailable information:** accountable producer testimony, organizational trust
   or account continuity cannot be invented from local files. The human/supplier
   may still need to provide it; an automatic checkbox adds no evidence.
2. **Locally establishable facts:** current bytes, IDs, request/context agreement
   and source attribution can become bounded automated checks. Repeated human
   confirmation may be scaffolding once policy permits those facts to suffice.
3. **Consequential reusable choice:** occurrence weighting and public-comparator
   risk are product decisions. Evidence informs them; agents cannot make them by
   silently lowering a gate. Once approved, encode the choice so later users do
   not have to rediscover it.

Security exceptions, publication, new external access and new scope remain
inherently authority-bearing here. A human is adding judgment at those boundaries,
not merely forwarding an APPROVE message.

## Lowest sufficient truthful floor

**STRONGER EVIDENCE != MINIMUM EVIDENCE REQUIRED FOR EVERY CLAIM.**

| Claim | Evidence/policy that can support it here | What it does not establish |
| --- | --- | --- |
| Dependency population | Supported declaration A, qualified current snapshot B1, or accepted bound B2 under their distinct rules | Complete evaluated MSBuild or deployed population |
| Selected version | Whole supported lock, exact attributable project/context/request association | Historical acquisition or currently loaded version |
| Public comparator | Accepted exact testimony, closed unique mapping, or disclosed conventional policy after bounded inspection | Public acquisition or local/public byte equality |
| Acquisition provenance | Accepted producer-origin assertions under their historical contract | Independently authenticated history merely because accepted |
| Content correspondence | Actual admissible local/public hash comparison | Supplying source, producing chronology or reproducibility |
| Producer-event history | Contemporaneous bound testimony plus native event evidence | A replay proving an earlier event |
| Deployment/runtime use | Not established by these artifacts | No libyears result supplies this claim |

Original H3 demanded stronger event/content gates for age; the public/local hash
mismatch made the distinction concrete. The cascade retained those facts as
assurance while requiring population, selection, comparator authority, identity-
bound dates and arithmetic for age. B1 and comparator conventions were subsequent
explicit product decisions, not facts that the original cascade already licensed.
The [namespace review](../../discovery/nuget-namespace-authority-review.md) caught
an internal inconsistency in the proposed comparator cascade about absent versus
active/unknown mapping, and overstatement of configuration closure. Separately,
its ordinary-A analysis established that the proposed current-pair floor needed
new human authority; a desirable future floor was not current permission.

For a future ecosystem, write a claim/evidence/refusal table before architecture.
Ask what the number will assert; separate minimum admission from optional stronger
assurance; identify known contradictions that defeat every fallback. Review a
useful ordinary journey early. Never turn “lowest sufficient” into “whatever
produces a number,” infer public authority from successful HTTP, or silently change
existing ecosystem semantics by analogy.

## What review bought, and what it missed

The following are retained findings, not new reproductions in this retrospective.
They show discriminating counterexamples; reviewer count alone shows none.

| Evidence | Material discovery or limit |
| --- | --- |
| [Original review history](reviews.md), [T018 summary](retrospective.md#what-independent-review-changed) | Request normalization/unreachable reason; absolute deadline architecture; lock component bounds; no-command mutation exposing a false positive worker test; alias missing-material bug; malformed-option privacy; Windows setup assumptions. |
| [Repository-source review](../../maintenance/nuget-repository-sources/reviews.md) | Unix backslash path refusal escaped source handling and lost siblings; null wording obscured sibling numerics. Parent found native/POSIX fixture-key mismatch and independent review validated it. |
| [Cascade review](../../maintenance/measurement-evidence-cascade/reviews.md) | Accepted selected assurance was lost on later throwing metadata failure. Bounded staging correction and fresh closure retained facts without inventing dates. |
| [Snapshot review](../../maintenance/nuget-snapshot-population/reviews.md) | v3 accidentally usable on A without its baseline authority; repeated identical framework literals incorrectly refused. Overlapping reviewers found the same spec issue; it is one issue. |
| [Acceptance discovery review](../../discovery/nuget-snapshot-acceptance-review.md) | Empirical property labels were inaccurate; private exploratory predicate missed conflicting child forms. This was discovery/probe repair, not a shipped parser defect. |
| [B1 review](../../maintenance/nuget-repository-snapshot/reviews.md) | Specification incorrectly said accepted B1 without namespace had M=null instead of row-level M=0. Corrected before implementation. Later three implementation scopes confirmed, rather than found material defects. |
| [Namespace review](../../discovery/nuget-namespace-authority-review.md) | Machine defaults survive a normal clear; active/absent/unknown mapping distinctions and cascade consistency mattered. Static repository inspection cannot claim reconstructed effective restore configuration. |
| [Comparator review](../../maintenance/nuget-conventional-comparator/reviews.md) | Exact-ID mapping precedence and missing-record fallback contract gaps; implementation let alternate eligibility downgrade explicit-public exclusion; config reader missed detectable in-place edits with restored mtime. ctime and precedence regressions closed both before live access. |
| [Positive-policy review](../../maintenance/nuget-positive-comparator/reviews.md) | Spec, plan/graph, trust, compatibility and operational scopes completed with no material findings; independent probes/recomputation confirmed the narrow change. This is confirmation, not proof all policy risks disappeared. |
| [Security review](../../maintenance/gitleaks-exact-exceptions-006-0031-review.md) | Initial exact suppression controls confirmed classification, but reviewer missed predictable triggering prose copied into rationale. Post-commit scan/parent detection and fresh review caught it; approval was superseded. |

Parent reconciliation validated findings and their controlling authority, retained
original rejected candidates, bounded corrections, froze revised bytes and sought
fresh focused review with collateral obligations. It did not vote across slices.
006-0014 demonstrates a real failure: reviewers lacked the verbatim exceptional
STOP condition and initially approved; supplying it changed disposition. Independent
contexts cannot repair shared missing authority or guarantee independence of facts.

Decomposition was useful for trust, floor, codec, output and operational obligations
that could be inspected separately. It required synthesis across boundaries, not
merely parallel verdicts. It also cost repeated reads, test runs, freezes and human
reading. No measured net attention/resource saving or causal superiority follows.
A disclosed process deviation in 006-0030—inert drafting during plan review—remains
a deviation; eventual approval does not backdate authority.

## Failure taxonomy and the Windows learning loop

Classify the failed claim before repairing anything. One incident may have several
layers; use unknown when evidence cannot choose a cause.

| Class | Observed example / appropriate response |
| --- | --- |
| Product/semantic | Ordinary root answer unhelpful despite precision-contract convergence; recognition depth policy suppressed all candidates. Revisit product authority, not arbitrary implementation loosening. |
| Implementation | Alias reconciliation, escaped source refusal, comparator exclusion precedence, config mutation checks. Correct against approved behavior and retain discriminating regressions. |
| Test/harness | Worker witness passed without command entry; fixture path keys; semantic tests assumed safe real reads. Repair what the witness actually proves. |
| Platform portability | Feature005 composed reads and Feature006 mixed Ruby coupling failed under missing dir_fd. Separate semantic seams from real filesystem/capability witnesses. |
| Security-tool finding | Historical synthetic/prose GitLeaks hits. Classify the actual line, preserve detection controls, obtain exact exception authority. A false positive still fails the configured gate until authorized treatment. |
| External infrastructure | Restricted-network DNS/transport failures; macOS job got no runner. A job that never executes the candidate is not a candidate test failure. |
| Registry/data reality | Controlled public/local hash disagreement; absent/invalid registry identity/date would be separate data outcomes. Hash mismatch cause/domain fitness remained unknown; do not diagnose it as private origin. |
| Observation/bookkeeping | Missing baton, unreported runtime, wrong continuity assumption, delayed 0024 append. Preserve provenance and missing values; do not normalize history. |
| Orchestration/actor routing | Agent told to create fresh top-level context; incomplete review treated as product failure; humans used as relays for determined corrections. Assign the action to its capable authorized actor. |
| Unknown | Original native/public content mismatch cause, general yield beyond this target, exact active compute/resource attribution. State the missing evidence instead of inventing a repair. |

The [0018 record](../../maintenance/operational-smoke-006-0018.md) ties repeated
Windows failures to the same test coupling observed in Feature005: semantic
composition expected successful real descriptor reads. Bounded repair used existing
injected readers while preserving real-reader tests and unskipped fail-closed
refusal. Capability-disabled local suites became an early invariant check, not
substitute Windows evidence. Later [72dc9a2 Windows](../../maintenance/nuget-snapshot-population/reviews.md#published-candidate-supplied-hosted-evidence--006-0027)
and [b449c5d Windows](../../maintenance/nuget-repository-snapshot/validation.md#published-candidate-supplied-windows-evidence--006-0029)
ran the substantial snapshot changes successfully; no intervening repair for those
features is recorded. The latter ran 751 tests in 159.702 seconds with 51 expected
skips and worker 3 PASS. This supports the learning loop, not a universal guarantee
or a timing diagnosis. Earlier exact Windows failures remain in history.

## Security, publication and asynchronous CI

The security rationale incident was self-referential: explanatory text copied the
lexical form that had triggered a false positive and created another historical
finding. Removing current text could not erase committed history. Preserve
fingerprints, locations, classification and paraphrase instead of unnecessarily
reproducing detector-triggering payloads. Review the representation itself and
scan current proposed documents as well as final committed history. A reviewer's
pre-commit APPROVE did not cover the later history result.

The positive control was authority discipline: the agent recognized one-exception
permission was exhausted and stopped before Phase 2. The human separately approved
the second exact fingerprint; negative controls still detected new equivalent
findings. No broad rule/path suppression or history rewrite followed.

Local convergence and publication authority differ from hosted post-publication
evidence. The pre-push gate must check the committed candidate with actual history
scope/configuration; a clean checkout is insufficient. Already-required platform
or security predecessors cannot be waived to save waiting. When publication is
authorized with local required gates satisfied and hosted jobs necessarily follow
publication, collect them asynchronously and report outstanding evidence. Do not
claim operational closure, merge/release readiness or a pass where a controlling
gate still requires hosted evidence. Correct candidate failures; rerun capacity
failures on the exact candidate rather than changing code without diagnosis.

The [72dc9a2 hosted record](../../maintenance/nuget-snapshot-population/reviews.md#published-candidate-supplied-hosted-evidence--006-0027)
explicitly distinguishes macOS capacity exhaustion (no candidate execution) from
its successful exact-candidate rerun: worker 3 PASS, full 730 PASS in 21.640 seconds.
Pages/Tier2 ultimately passed; runtime/punycode warnings remained separate WATCH
maintenance. Repository evidence supports that final state, not a quantified Pages
queue duration. This commissioning supplies the asynchronous treatment of current
hosted CI; no new hosted results for `0eabe303…` were fetched or inferred.

This run queried both remote main refs read-only: both returned the exact full
candidate digest above. Local remote-tracking refs also agree. That reconciles
publication, not who performed the push or its time. **Push performed here: NO.**

## Observation methodology and descriptive evidence

006-0032 was appended once from its authorized external handoff. Human-supplied
session, GPT-6.1-Sol/openai/medium, agent 0.160.0, reported runtime **1053 seconds**
and credits_after **92** enrich that row. credits_before **91** has explicitly
confirmed continuity. Original runtime notes/confounding remain; a machine-handoff
note saying runtime was unobserved is historical provenance, not a contradictory
claim about later enrichment. No runtime or credit delta was derived.

Snapshot: [canonical ledger](../../observations/agent-runs.csv) through that append,
**51 rows, 44 columns, unique IDs**. Feature005 has 21 rows, including later
retrospective/maintenance; Feature006 has **30 rows**, not 32. 006-0020 and
006-0022 are absent from the ledger; their repository artifacts remain usable
qualitative evidence. Do not fabricate missing rows. 006-0024 was appended after
0025 under explicit protocol reconciliation; preserve that order.

| Feature006 observation | Descriptive result / limit |
| --- | --- |
| Stages | Discovery 7; specification 3; specification_review 1; planning 3; implementation 10; validation 3; closure 1; maintenance 2. Historical labels retained. |
| Completion | Complete 26; incomplete 3; blocked 1. These describe assigned work, not product pass rates. |
| Model/effort | 29 GPT-6.1-Sol/medium, one blank; unavailable actual child settings/resources cannot be inferred. |
| Context | 29 fresh, one continued as recorded; neither proves a context-window size or comparative advantage. |
| Runtime | 28 directly reported values; min 333s, median 590.5s, max 2203s. Two missing (0012,0024). Confounding: 20 yes, 10 unknown; none establish active compute. |
| Account fields | 27 before readings, 30 after readings; account boundaries only. No summed credit “cost.” |
| Prompts | Character counts and hashes blank in all 30. No measured prompt-growth/shrinkage series. |
| Intervention flag | Two yes, 28 no. Initiating authority often lives outside that flag; not a human-decision or attention count. |

Reproduce these descriptive counts with Python's `csv.DictReader(...,
delimiter='|')`, select `feature == '006'`, group exact stored strings, and take
`statistics.median` of nonblank `reported_runtime_s`. No normalization, imputation,
model ranking, finding-count summation or credit subtraction is required.

Runtime is never reconstructed from adjacent timestamps or neighboring runs.
credits_before may inherit the immediately prior directly observed credits_after
only with confirmed no intervening credit-consuming work. Bounded maintenance is
real work even without a substantive row: 0027 correctly uses a bookkeeping
boundary of 78. Account arithmetic is not exact task billing, and changing scopes,
models, child telemetry, sleep, approvals and network waits confound comparisons.
Hosted queue latency and actual test duration are separate measurements.

Prospectively, retain schema v1. Use existing notes/artifact pointers to capture
material initiating authority, exact candidate/job identity, queue-versus-execution
state and requested-versus-observed context when known. Automate exact prompt
count/hash capture only if the exact text is available; leave missing values blank.
A future versioned schema change might separate authority events from in-run
interventions, but this retrospective does not approve or implement one. Human
attention and reading burden remain unmeasured; collecting metadata has its own cost.

## Prompt growth, durable memory and participation

Large prompts enabled exact exceptional authority, hard stops, staged autonomous
work and detailed adversarial assignments. The original retrospective records a
human-supplied **17K** signal. This commissioning adds roughly **20K, 28K and 30K+**
prompt-size observations during trust investigations; their unit and exact prompt
bytes are not supplied here. These are qualitative reports, not ledger character
or token measurements. Token count itself is not a defect. There is no evidence
that prompts began shrinking after policy became durable, and no quantified work-
per-human-intervention ratio can be reconstructed.

There is qualitative evidence of substantial autonomous work: 0012 moved from
portability through integration and validation preparation; 0016 performed bounded
producer/consumer corrections and convergence; 0032 completed an approved policy
lifecycle and all-occurrence operational audit. Internal review relays no longer
needed separate human messages, but trust judgments and reading still consumed
human attention. Some prompt repetition was necessary exceptional authority;
reprinting settled methodology and assigning orchestrator actions to the agent
were accidental costs.

The reusable arrangement is now explicit in [AGENT_ROUTING](../../AGENT_ROUTING.md):
repository owns durable methodology and policy; human/orchestrator owns session,
context/model choices and new authority; prompt carries intent/delta/evidence
pointers; agent reads and executes within authority. Fresh-parent creation is the
orchestrator's action, not an imperative Codex can satisfy from inside that parent.
A requested fresh child is a different capability and not proof of fresh parent
state. Readable source and current disposition pointers matter more than terse
machine-oriented shorthand.

Feature004's [capability comparison](../004-rubygems-support/retrospective.md#model-routing-and-capability-access)
showed a broad audit incomplete at Low and complete at Medium without remediation
of a Low-established defect. It also retained a viable lower-effort retrospective.
Those heterogeneous observations are not a controlled model experiment. They raise
an OSPO participation risk: an opaque premium-model requirement can exclude capable
contributors through resources alone.

Keep the evidence standard, make obligations decomposable, preserve deterministic
gates and permit human/alternate-reviewer completion or appeal of incomplete
coverage. Reproducibility needs frozen candidates, readable witnesses, provenance
and accessible tests, not identical access to one expensive model. Resource limits
alone do not establish that code is defective or may not proceed; an unsatisfied
required gate still needs equivalent evidence. Human override/appeal must state
which authority changes and why; it must not disguise missing verification as a
pass. Actual child costs remain unknown, so an accessible parent is not proof of
an entirely low-resource team.

## Highs, lows and the next boundary

The high was truthful progress: 51 occurrences became measurable without target
execution, private endpoint access, fabricated dates or a claim of acquired public
bytes. Stronger assurance survived separately. Real counterexamples strengthened
contracts/tests before live access. Durable policy removed repeated choices where
local facts and a consciously accepted convention were sufficient.

The low was repeated correct refusal without a satisfactory ordinary answer, plus
expensive provenance/event investigations before the minimum age claim was clear.
The 0014 authority deviation, recurring Windows test coupling, missing observation
handoff and second prose false positive were avoidable process failures. The
source-policy distinctions, identity/date checks, safety boundaries and explicit
risk choices were necessary for the resulting honest claim. Exact marginal time,
credits and human effort for either category were not measured.

A newly reported pre-push hygiene issue is **test-output isolation / evidence
provenance maintenance**, not a product defect: deterministic fixture CLI output
such as `Measured: 0 / 1 dependencies` appeared in the same command-block channel
before the separately labeled real-target `Measured: 51 / 51 dependencies`.
The commissioning human reports this; this run did not reproduce it. Future
housekeeping should isolate/capture fixture stdout and label real-target evidence
with command, candidate and exit. No test/runtime cleanup is implemented here.

The [Feature007 methodology handoff](methodology-handoff.md) lists concrete
preconditions and deferred maintenance. Feature007/Java has **not begun**. The
next human gate is acceptance of these methodology artifacts and separate roadmap
selection/authority for the next work. Current-candidate hosted checks remain
asynchronous outstanding evidence, not an excuse to invent results or wait idly.
Independent retrospective review dispositions are in [reviews.md](reviews.md).
