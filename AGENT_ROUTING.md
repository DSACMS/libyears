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
this strategy as Feature 005 supplies prospective observations.

## Evidence and limits

The primary sources are the [Feature 003 retrospective](specs/003-yarn-lock-evidence/retrospective.md)
and Feature 004's [retrospective](specs/004-rubygems-support/retrospective.md),
[review record](specs/004-rubygems-support/reviews.md),
[task evidence](specs/004-rubygems-support/tasks.md), and
[release validation](specs/004-rubygems-support/release-validation.md), read
alongside its discovery, specification, plan, and Git history.

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
positive verdicts is insufficient. Feature 004's task ownership and composed
tests demonstrate useful evidence boundaries; they do not validate decomposed
agent convergence. The hypothesis that smaller composable evidence tasks could
let more accessible models establish the same gate surfaced in Feature 004
but **was not tested**. Decomposition must preserve the standard.

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

## Human attention as a resource

Credits and runtime are only part of the cost. Longer, deeper artifacts also
require human reading and review: the two viable retrospective candidates were
approximately 2,460 and 5,240 words. More detail can preserve valuable reasoning,
but length itself is not a quality measure.

Do not minimize tokens or output at the expense of readability, evidence, or
auditability. Ask: **What is the smallest artifact that preserves the evidence
and decisions a future human needs?** Keep the decision and evidence limits
visible, with links to deeper records instead of repeating them.

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
