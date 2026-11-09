# Agent Routing

Different engineering tasks benefit from different combinations of model
capability, reasoning effort, fresh versus continuing context, decomposition,
independent review, repository-grounded evidence, and human authority. The goal
is not to maximize model capability on every task. It is to obtain sufficient,
inspectable evidence with proportionate resources while preserving human control
and accessibility.

**PROVISIONAL WORKING STRATEGY** — for human contributors structuring
agent-assisted repository work. This is neither permanent policy nor a benchmark
report or vendor/model leaderboard. Existing [AGENTS.md](AGENTS.md), approved
feature contracts, and human authorization continue to govern the work. Revise
this strategy as further prospective observations become available.

For canonical lifecycle, review, authority and handoff mechanics, see
[SDD_WORKFLOW.md](SDD_WORKFLOW.md). This document retains provisional routing
guidance and its supporting observations.

## Evidence and limits

The primary sources are the [Feature 003 retrospective](specs/003-yarn-lock-evidence/retrospective.md)
and Feature 004's [retrospective](specs/004-rubygems-support/retrospective.md),
[review record](specs/004-rubygems-support/reviews.md),
[task evidence](specs/004-rubygems-support/tasks.md), and
[release validation](specs/004-rubygems-support/release-validation.md), read
alongside its discovery, specification, plan, and Git history.

Feature 005 adds the [prospective ledger](observations/agent-runs.csv), runs
005-0001–005-0019, its [retrospective](specs/005-gemfile-group-scope/retrospective.md)
and [review history](specs/005-gemfile-group-scope/reviews.md). The retrospective
classifies updates and limitations; historical model identities below remain
observations, not required configurations.

Feature 003 preserved decision summaries but lacked some exact reviewed drafts
and prospectively recorded routing. Feature 004 retained draft/revision history;
several reviewers explicitly found repository context sufficient. These support
inspectable handoffs, without proving time savings or a universally best workflow.
The repeated optional-smoke dependency mistake also shows that preserving a lesson
does not guarantee its application.

The commissioning human supplied additional process observations for this draft:
implementation/narrow-review routing, retrospective resource use and synthesis
length, and lessons from the subsequent completed public-history sanitization.
These are labeled below; they are not independently reconstructed measurements
from Git. This document preserves generalized lessons without reproducing private
remediation inputs or sanitized operational details. No statistical significance
or causal model comparison is claimed.

## Eight routing principles

### 1. Route by cognitive shape, not prestige

First identify the evidence the task must produce. Bounded implementation
translates an approved contract into behavior and tests. Deterministic
transformation applies exact rules with assertions. Narrow verification checks
specified changes; broad cross-artifact verification reconciles requirements,
architecture, implementation, tests, documentation, and release evidence.

Ambiguous or adversarial reasoning must expose competing interpretations and
missing decisions. Synthesis and retrospective work must distinguish facts,
interpretations, and uncertainty while remaining readable. Security/privacy
review examines disclosure and trust boundaries. Authenticated or other
authority-bearing actions additionally require permission and an appropriate
execution environment. One model need not be best for all these shapes.

Feature 004's separate specification, architecture, task-graph, implementation,
and convergence gates illustrate why the assignment matters. A capable author
does not automatically supply independent verification or publication authority.

### 2. Use the least capability that can establish the required evidence

Start with accessible, lower-resource configurations when they can meet the same
quality gate. Define completion and required witnesses before selecting a model.
For implementation, that includes behavioral tests and relevant regressions;
for review, it includes inspected obligations and unresolved findings.

Cheaper does not mean worse; more expensive does not mean better. Longer runtime
does not establish better reasoning, shorter prompts do not establish faster
execution, and higher reasoning effort does not guarantee correctness. Escalate
because the task's shape or demonstrated insufficiency warrants it. Preserve
failed or incomplete attempts as evidence rather than silently replacing them
with the eventual successful result.

### 3. Decompose before escalating where practical

When a broad audit cannot complete, consider smaller independently verifiable
reviews: contract-to-test coverage, source-authority enforcement, compatibility,
output coherence, and release-evidence sufficiency, for example. Give each a
bounded question, evidence locations, and explicit completion conditions.

Then synthesize the results against the whole gate, checking omissions,
contradictions, and behavior crossing component boundaries. A collection of
positive verdicts is insufficient. Feature 004 raised decomposition as an untested
hypothesis. Feature 005 subsequently completed decomposed specification and plan
reviews after incomplete broad attempts, then decomposed implementation checkpoints
and final convergence. Bounded slices, frozen candidates, independent reads and
parent reconciliation supplied the required evidence, including REVISE findings.
This supports trying decomposition before expensive escalation where practical;
it does not isolate decomposition from model, effort or harness effects.
Decomposition must preserve the standard.

### 4. Review completeness is not review verdict

Record separately whether the software failed review, whether the reviewer
found a defect, whether the required audit completed, and whether the environment
prevented completion. These dimensions can overlap; a partial review can find a
real defect while still leaving other obligations unaudited.

Feature 004 T019's initial NOT CONVERGED result meant the independent audit was
incomplete and established no product defect. The subsequent completed audit
supplied missing review evidence without remediating a finding from that attempt.
A future handoff should identify inspected coverage, unaudited obligations,
findings, and blockers rather than relying on a verdict label alone.

Feature 005 repeated this distinction in 005-0005/005-0009: incomplete broad
audits established no defect. Later complete reviews found actual contract/plan
gaps. Their ledger task_class labels say narrow_verification; route future work
by its actual cross-artifact obligations. Recover truncated reads before claiming
coverage, and preserve incomplete attempts separately from later verdicts.

### 5. Fresh context for independence, not as ritual

Use fresh contexts when independence is materially valuable: author to reviewer,
implementation to convergence, candidate construction to independent audit, or
competing experimental authors and reviewers. Provide the actual artifacts and
gate, so the reviewer can challenge the author's account.

Continuing context may better serve tightly related execution steps when
independence is not the objective. Feature 004 used sequential approved tasks
and separate review gates; neither approach implies fresh context is inherently
better. A fresh context also cannot repair missing evidence or supply authority.

### 6. Repository context is the normal durable handoff

Let agents reconstruct product and engineering state from readable repository
artifacts. Compact prompts should identify role, task/gate, authority, stop
conditions, and relevant artifact locations, including the baseline and current
approval record. Avoid restating the whole project. Historical pending text
should be read alongside the records that supersede it.

Treat the prompt as the assignment delta over durable repository state. Feature
005 supports this handoff practice, but captured no prompt counts/hashes or
context-window sizes and therefore establishes no quantitative token savings.

The post-004 sanitization operation supplies an important exception: if a
downstream agent requires an exact normative artifact to execute safely, an
artifact existing only in another conversation is **not a sufficient handoff**.
Materialize it explicitly. A summary of intended transformations cannot replace
the exact authorized transformation manifest.

Durable does not always mean public or committed. Sensitive remediation inputs
may need a durable-but-**NONPUBLIC** handoff outside Git, such as an explicitly
authorized temporary file available for the necessary handoff period. Identify
which artifact governs execution and verify it is available before proceeding.
Do not recover missing inputs by searching unrelated private locations or putting
sensitive material into public documentation for convenience.

### 7. Fail closed at authority and evidence boundaries

Stop rather than invent product authority, trust authority, missing normative
transformations, publication authorization, remote state, credentials, or evidence
the agent cannot inspect. BLOCKED, REVISE, and INCOMPLETE are useful outcomes
when they precisely identify what is missing and what would permit continuation.

For deterministic transformation, an exact manifest and assertions constrain
execution; any mismatch calls for a stop, not a plausible replacement rule.
For review, absent evidence remains absent. For remote actions, a local candidate
or prepared command does not establish the remote result. Greater capability
does not turn an unobservable fact into evidence.

### 8. Preserve meaningful human authority

Keep unresolved product decisions, organizational trust decisions, authorization
of real validation targets, acceptance of human-supplied evidence, publication
and privacy judgments, and authenticated remote-history replacement explicitly
human-authorized where applicable. Approved decisions should remain readable so
later agents can execute within them without repeatedly reopening them.

Feature 004's product clarification and trust authorization demonstrate distinct
human responsibilities. Its subsequent sanitization operation also demonstrated
that inability to automate an authenticated action does not itself justify
giving an agent sensitive credentials. Prepare and verify the bounded work;
let the human perform the authenticated step when that avoids unnecessarily
expanding authority. Safe scoped authentication may permit authorized automation,
but this strategy grants neither credentials nor permission.

## Observed routing evidence

Names below identify historical configurations, not permanent routing choices.
**R** denotes retained Feature 004 records; **H** denotes the commissioning
human's additional observations. R includes human-supplied results recorded in
the repository, not independent replication of every run.

| Assignment/configuration | Observation and limit |
|---|---|
| GPT-6.1-Sol Medium — implementation and deterministic transformations (H; task outcomes retained in R) | Repeatedly handled implementation phases and deterministic repository transformations successfully. Git does not independently identify every run's model. |
| GPT-6-Astra Low — bounded/narrow reviews (H; review outcomes retained in R) | Successfully handled several bounded reviews; this does not establish broad-audit completion. |
| GPT-6-Astra Low — broad T019 (R) | NOT CONVERGED: required independent audit incomplete; no product defect established. |
| GPT-6-Astra Medium — broad T019 (R) | Completed audit: CONVERGED, 52/52 acceptance coverage, no material findings. Effort alone is not established as the cause. |
| T021 authors: GPT-6-Astra Low / XHigh (R) | Viable ~2,460-word candidate / deeper ~5,240-word candidate. Neither was found materially factually defective or to contain unsupported causal claims. |
| T021 blind reviewers: GPT-6-Astra Low / XHigh (R) | Low judged candidates complementary; XHigh judged the XHigh-authored candidate materially stronger. Low flagged one follow-up attribution as independently unsubstantiated. |
| Canonical GPT-6-Astra XHigh synthesis (R/H) | ~2,899 words, combining Low's accessibility/concision with deeper analysis; synthesis, not accumulation of both drafts. |
| GPT-6-Astra XHigh resource observations (H) | Materially greater observed runtime/credit use in this small sample; no causal or general cost-performance conclusion. |
| Sol history-reconstruction run (H) | Reported long elapsed duration included a locked/unattended workstation interval; confounded, not active-compute evidence. |
| Feature 005 GPT-6.1-Sol Medium parent — native orchestration (prospective ledger 005-0010/0014/0015/0019) | Completed decomposed plan review, two implementation phases/checkpoints and final convergence; verdicts included REVISE. Child dispatch/report collection occurred internally. Fresh forks and no overrides were requested; actual child model/effort/resource telemetry was unavailable. |

This is a compact historical reference, not an observational ledger. These
observations do not isolate model, effort, context, environment, or task effects.

## Provisional routing guide

Use these as starting strategies subject to the actual gate and available access.
Reasoning settings are adjustable; exact model names are deliberately absent.

| Task shape | Starting strategy | Escalation signal |
|---|---|---|
| Bounded implementation | Implementation-oriented capable model, medium reasoning; approved task and focused tests. | Unresolved cross-boundary ambiguity; return missing decisions to the appropriate authority. |
| Narrow verification | Accessible reviewer, lower reasoning, explicit obligations and fresh context where independence matters. | Cannot complete the audit; decompose or escalate without reducing coverage. |
| Broad convergence | Decompose where practical, with synthesis; otherwise use stronger synthesis/review capability. | Incomplete evidence coverage or unresolved interactions. |
| Ambiguous/adversarial reasoning | Reviewer able to compare interpretations and identify consequential counterexamples. | Missing product/trust decision needs human resolution; reasoning gaps may warrant capability escalation. |
| Deterministic history/data transformation | Implementation-oriented model with exact authorized manifest and assertions. | Stop on any manifest mismatch or missing normative input. |
| Retrospective/synthesis | Capable synthesis model with readability and causal-claim constraints. | Independent review when the artifact becomes durable authority; unresolved evidence conflicts. |
| Security/privacy/publication review | Independent reviewer, explicit scope, fail closed. | Human decision at publication or authority boundary. |
| Authenticated external action | Agent prepares/verifies; human performs when credential exposure would unnecessarily expand authority. | Automate only with authorization and a safe scoped credential mechanism. |

## Capability and access equity

Open-source quality gates should not silently require access to premium or
higher-capability models. Financial and resource constraints are participation
constraints. The response is not to weaken quality standards. Prefer decomposition,
composable evidence, accessible starting configurations, explicit escalation
criteria, and readable artifacts that another reviewer, model, or human can use
to continue the work.

Feature 004 showed a materially different Low/Medium completion outcome for one
broad convergence task; it did not prove effort level alone caused it. The
retrospective experiment also showed Low could produce a viable sophisticated
artifact while XHigh added depth at materially greater observed resource cost.
Neither observation supports a blanket premium-model requirement. Contributors
need routes to equivalent evidence, with remaining uncertainty made explicit.

Feature 005 demonstrates an accessible parent configuration orchestrating completed
gates; unavailable actual child telemetry prevents claiming an entirely
lower-resource team. Controlled child configurations remain an open experiment,
not a reason to require premium access or weaken acceptance.

## Human attention as a resource

Credits and runtime are only part of the cost. Longer, deeper artifacts also
require human reading and review: the two viable retrospective candidates were
approximately 2,460 and 5,240 words. More detail can preserve valuable reasoning,
but length itself is not a quality measure.

Do not minimize tokens or output at the expense of readability, evidence, or
auditability. Ask: **What is the smallest artifact that preserves the evidence
and decisions a future human needs?** Keep the decision and evidence limits
visible, with links to deeper records instead of repeating them.

Feature 005's five-task implementation runs used native child dispatch and review
collection, reducing the need for humans to relay reviewer messages. Net attention
savings were not measured. Provisionally consider phase-level authorization with
explicit dependencies, allowed edits, review freeze and hard stops; retain human
authority over new scope, corrections and external targets. There was no controlled
comparison with per-task authorization.

## Environment parity and authority

An agent execution environment can differ from the human host in networking,
OS identity/account services, trust configuration, authentication, and access
to external systems. Test required parity early when live external validation
is necessary, within authorized access boundaries.

Feature 004's release record distinguishes trust failures from later agent
resolution failures; it establishes no common cause or product defect from
those environmental attempts. When parity is unavailable, distinguish product
failure from harness/environment failure. Permit explicitly accepted
human-executed evidence handoff, retaining what the agent inspected and what
rests on human attestation. The successful T018 raw JSON was not independently
audited in full by the agent. Do not weaken TLS/security controls or grant broad
credential access merely to maximize automation.

## Experimental discipline

For intentional comparisons, keep prompts and tasks as constant as practical,
record relevant differences, and blind reviewers to model identity when useful.
Do not force a scalar quality score when the candidates have complementary
strengths. Preserve raw observations in an appropriately authorized location,
respecting privacy; distinguish outcome from causal explanation. Treat n=1
comparisons as hypothesis-generating.

Use the [prospective agent observation ledger](observations/README.md) beginning
with Feature 005; record unknowns honestly, including interruptions and uncertainty
about active runtime. This methodology infrastructure does not authorize Feature
005 discovery, specification, planning, or implementation.

## Stop/escalate checklist

Before escalating capability, ask:

- Is the task actually incomplete, or did the software fail?
- What evidence is missing?
- Can the task be decomposed?
- Is required context durably available?
- Is the blocker authority rather than intelligence?
- Is the blocker environment parity?
- Would escalation materially improve the evidence?
- What additional human attention and resource cost will escalation create?

## Non-goals

AGENT_ROUTING.md does not guarantee model behavior, rank vendors/models
universally, replace human judgment, authorize credentials or publication,
weaken existing review/acceptance gates, require premium model access, or replace
prospective observational logging. It remains a revisable working strategy.

## Actors, capabilities and authority

The [post-Feature006 retrospective](specs/006-nuget-selected-evidence/methodology-retrospective.md)
supports this reusable lens. It extends routing guidance; lifecycle authority
remains in SDD_WORKFLOW, observation rules in observations/README, and product
policy in approved contracts. The matrix describes roles, not a new permission
grant. One person or system may occupy several roles, but the responsibilities
must remain distinguishable.

**Capability** is what an actor can do. **Authority** is what it is permitted to
decide or authorize. **Evidence** is what it can establish from observations.
**Action** changes or inspects state. **Verification** checks a specific claim.
**Durable memory** preserves decisions and evidence for another reader. None
substitutes for another: access does not grant permission; a passing test does
not authorize policy; an approved plan does not prove execution.

| Actor | What can it observe? | What can it decide / authorize? | What can it act upon? | What can it verify? | What should become durable? / wrong assignment failure |
| --- | --- | --- | --- | --- | --- |
| Human / product owner | User intent, organizational facts, displayed telemetry, review evidence | Consequential scope, acceptable risk, trust exceptions, external access and publication within their own authority | Select work, supply testimony/authority, perform or authorize external actions | Whether the ordinary journey answers the intended question; accept bounded evidence with limits | Decision, scope, rationale, residual risks. Making the human relay determined internal gates wastes attention; asking agents to invent these choices changes policy silently. |
| ChatGPT / orchestrator | User request, available harness controls, session metadata where exposed, agent reports | Route work and select session/context/model within human authority; cannot invent trust or publication permission | Create a new top-level session where the harness supports it, assign prompts, collect reports | Actual requested setup where observable, coverage and stopping gates | Setup/request provenance and handoff. Assigning orchestrator-only actions inside a worker prompt makes desired state unenforceable. |
| Prompt (assignment artifact) | Nothing independently; it carries supplied observations and instructions | Conveys attributed new authority; is not an independent authority holder | Directs a capable authorized actor; does not execute or create context | Nothing by itself; claims need evidence | Intent, delta, exact exceptional restrictions, relevant evidence pointers. Treating copied prose as proof or restating stale state can override current contracts accidentally. |
| Codex parent agent | Authorized repository/files/tool results and available harness state | Routine implementation and bounded correction determined by approved authority; stop on new consequential choices | Read, edit, test, orchestrate authorized reviews and make authorized commits/actions | Findings against raw authority/evidence; cross-scope reconciliation; actual verification within access | Code/tests or docs, decisions attributed to owners, review disposition and baton. Parent confidence is not independent approval or permission to create provenance. |
| Codex reviewer / subagent | Frozen candidate, governing authority, independently inspected evidence within assigned access | Findings and a scoped completed/incomplete verdict; cannot authorize changed product/security policy | Read and run authorized bounded probes; edits only if separately commissioned | Assigned obligations and collateral boundaries; cannot certify unaudited scope | Coverage, counterexample, candidate identity, limits and verdict. Counting votes or sharing sibling answers as ground truth masks omissions and correlated mistakes. |
| Repository | Retained files/history, not outside reality | Carries established authority when approved and current; does not select new work | Supplies inspectable durable state to authorized actors | Enables byte/history/reference checks; existence alone authenticates no claim | Readable current disposition plus preserved history. Treating all historical prose as current creates false blockers or stale permission. |
| Specification / plan / tasks | Recorded requirements, architecture and dependency graph | Carry approved product / architecture / bounded-work decisions respectively | Govern implementation after execution authorization | Define required witnesses; cannot prove they ran | Traceable scope, criteria, predecessors, hard stops and review disposition. Letting code rewrite approved requirements conceals scope drift. |
| Tests | Fixture inputs and actual observed behavior under stated harness assumptions | No new product or trust authority; executable contract witnesses | Exercise code and permitted seams | Their assertions on the candidate/platform actually executed; mutation may test witness discrimination | Behavioral regressions, input assumptions and results. Fixture success is not real-target evidence, and skipped native tests are not platform success. |
| Real target repository | Supplies current authorized bytes and metadata | No implicit execution, witness acceptance or public-comparator authority from mere presence | Can be inspected only within explicit access; target code is not automatically executable | Supplies ordinary-user acceptance evidence when authorized; cannot certify its own history | Bounded inputs/results, integrity scope and limitations in validation records. Familiarity with a path is not renewed permission. |
| Security tooling | Inputs/history/rules/configuration actually scanned | Findings under configured rules; no authority to classify away or suppress its own hits | Scan authorized scope and return results | Configured detection and negative controls, not universal absence of secrets | Version, scope, redacted findings, classification and exact authorized exceptions. Copying triggering payloads into rationale can create new history findings. |
| Hosted CI | Candidate/job/platform actually scheduled and executed | Configured gate results; no new scope or publication authority | Execute workflows after their trigger | Actual candidate behavior on actual runners; queue failure proves no candidate test result | Exact SHA, job identity, executed/pending state, result provenance. Declaring local simulation hosted PASS or capacity failure product FAIL misroutes repair. |
| External package registry | Its current identity, listing, version and date metadata | Authoritative metadata within the approved adapter/claim; no authority over local population or acquisition | Answer permitted public requests after local admission | Public record consistency, not local source/content/producer/deployment history | Adapter rules, fixtures and bounded validation evidence. A successful namesake query cannot retroactively authorize disclosure or comparison. |
| Observation ledger | Recorded machine observations plus attributed human enrichment | Protocol-defined provenance, not quality scores or billing authority | Retain authorized rows and unknowns | Shape, uniqueness and supplied provenance; cannot reconstruct absent runtime | Raw boundaries, confounding, candidate/artifact pointers. Treating counters as task billing or intervention flags as decision counts manufactures precision. |

### Assign the action to the actor that can perform it

For each workflow requirement, state five things: **who observes it, who decides
it, who acts, who verifies it, and where the result becomes durable**. If any is
missing, repair the assignment before treating the requirement as satisfied.

The commissioning human for run006-0033 reports a recurring defect: prompts said
a task “should run in a fresh context” as though the already-running Codex parent
could create a fresh top-level context. Correct desired state != correct actor
assignment. The human/orchestrator must create that context before dispatch, then
record requested versus observed setup when available. The agent can report its
limits or request a suitable handoff; it cannot claim to have replaced its parent
context. A fresh child reviewer, where supported, is a distinct action and does
not establish fresh-parent state. Earlier ledger requests are not proof of setup.

Apply the same reasoning to credentials, publication, CI reruns, security
exceptions and telemetry: asking the wrong actor more insistently does not add
capability or authority. Put harness setup metadata in orchestration and its
observation record, rather than making it an impossible agent completion obligation.

### Retire repetition only after authority has become policy

Classify a human gate before proposing automation:

- Information unavailable locally still needs an accountable supplier or human;
  agents must not fabricate it.
- Facts the repository can establish may become executable checks once approved
  policy says those facts suffice.
- Consequential reusable choices need explicit human judgment; after approval,
  record the choice and its limits so subsequent agents execute without reopening it.

Feature006's automatic sources, qualified current snapshots and comparator
conventions illustrate different instances, not a universal mandate to remove
human gates. Known contradictions remain terminal where contracts require it;
stronger assurance remains separately visible. New security exceptions, scope,
external access and publication still require their controlling authority.

Within already-authorized work, route determined corrections internally:
validated finding → bounded fix → freeze → fresh focused non-author review with
collateral checks → parent reconciliation. Never use positive sibling reviews to
overrule a validated finding. Use decomposition to make coverage inspectable,
not to manufacture confidence from reviewer count. Required standards remain
accessible to human or alternate reviewers; model price is not an acceptance gate.

### Put durable knowledge in the right home

Repository: established methodology, accumulated product policy and current
approval pointers. Human/orchestrator: session/context/model setup and new
authority. Prompt: new intent, delta, evidence locations and exact exceptional
restrictions. Agent: read that state and perform authorized work, preserving
observations and unresolved gates. This is a division of responsibility, not a
prompt-length target. Long prompts may be necessary for new consequential
boundaries; readable sources and inspectable authority take precedence over
model-token efficiency.
