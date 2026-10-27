# Feature 003 Retrospective

## Status

Feature 003 is complete: 11/11 tasks closed; 30/30 acceptance criteria
satisfied; 187 deterministic tests passing after final remediation; real
repository dogfood measured 77/77 dependencies at 100% coverage; optional live
smoke intentionally skipped as redundant; final convergence verdict
**CONVERGED**; human readability **PASS**; fresh-eyes storytelling verdict
**MOSTLY**. These completion results are recorded in `tasks.md` and
`release-validation.md`.

## Method

A fresh Luna Medium agent, without development-chat context, attempted to
reconstruct Feature 003 from durable repository evidence. This intentionally
repeated Feature 002's repository-storytelling experiment. The purpose was to
test whether `discovery.md` and `reviews.md` better preserved the products of
human attention. The verdict and observations below are fresh-agent findings;
they are not additional correctness testing.

## What Improved from Feature 002

Feature 002 also received **MOSTLY**, but that categorical equality masks a
substantial qualitative improvement. The fresh agent reconstructed the initial
portfolio-scanning recommendation, the human challenge to that product
boundary, the Go/Maven/Yarn follow-up investigation, why Yarn won, and which
alternatives were deferred. It also reconstructed the initial specification
REVISE verdict and its major findings and decisions; architecture-review
findings and resulting design; task-graph findings and corrections; the
internal T005 versus public T007 activation boundary; optional T010 semantics;
the implementation sequence; dogfood evidence; and the convergence finding,
remediation, and re-verification. These records appear chiefly in
`discovery.md`, `reviews.md`, `tasks.md`, `release-validation.md`, and Feature
003 Git history.

Feature 002's retrospective specifically found that much of its review and
decision journey was not durable (`specs/002-npm-support/retrospective.md`,
“What the Repository Did Not Preserve Well”). Feature 003's discovery and
review records directly address that gap. This is a material improvement in
reconstruction, though the result did not become YES.

## What Remains Missing

Exact before/after reviewed drafts are not always reconstructable: the first
committed specification, plan, and task graph often appear after
clarification or approval, rather than preserving the draft reviewed. Some
fine-grained rationale is summarized in review outcomes rather than tied to a
specific text change. Model-to-phase routing was not durably recorded during
development. These are gaps in durable development context; missing chat
transcripts are not a goal.

## Review Before Code

Durable review records show this lifecycle pattern:

- **Before implementation:** specification review recorded six material
  findings, architecture review five, and task-graph review seven. These counts
  describe each record's enumerated findings; they are not directly comparable
  in severity. (`reviews.md`, “Specification Clarification Review,”
  “Architecture Review,” and “Task-Graph Review.”)
- **During implementation:** no durable evidence records an implementation-
  time design escalation. Phase work proceeded through the approved task
  boundaries, from parser and matcher through source selection and public
  activation. (`tasks.md`, T001–T008; Feature 003 implementation commits.)
- **After implementation:** convergence found one low-severity human
  diagnostic issue. Commit `ace9ccf69d259ad6041dd0c19e00bf5df2208309` changed two production/test files,
  `libyears/npm.py` and `tests/test_mixed_scan.py`; independent narrow
  re-verification returned CONVERGED. (`reviews.md`, “Convergence Review”;
  `release-validation.md`, “Final convergence disposition”; commit `ace9ccf69d259ad6041dd0c19e00bf5df2208309`.)

This pattern is consistent with the hypothesis that resolving ambiguity
earlier can reduce implementation churn. It does not prove that the review
sequence caused the limited remediation observed.

## Human Attention

The experiment preserves two emerging hypotheses:

> Agentic software engineering should conserve human attention.

> Conserve human attention, but preserve the products of human attention.

Feature 003 adds a refinement:

> Spend human attention where ambiguity is expensive; automate where the
> decision boundary is already clear.

Human/product judgment is most visible around product direction, evidence
semantics, architecture boundaries, task/public-activation boundaries, and
whether release-validation evidence was sufficient. (`discovery.md`, “Human
Product Review” and “Decision”; `reviews.md`; `tasks.md`, T005–T011.) Automation
carried most bounded implementation and deterministic verification. The
repository records no human-time measurements, so no time savings are claimed.

## Model-Routing Experiment

**RETROSPECTIVE EXPERIMENTAL METADATA — reconstructed from the development
session, not independently recoverable from repository evidence.** This
routing information was not durably recorded during development and must not
be represented as evidence recoverable from Git.

The approximate routing was:

- Bounded parser/matching work: GPT-6.1 Sol, medium.
- Shared source-availability semantics: GPT-6 Astra, medium.
- Internal evidence selection/integration: GPT-6.1 Sol, medium.
- Public-contract activation: GPT-6 Astra, medium.
- Deterministic end-to-end work: GPT-6 Sol, medium.
- Dogfooding/release bookkeeping: GPT-6 Sol, medium.
- Final convergence audit: GPT-6 Astra, medium.
- Convergence remediation: GPT-6.1 Sol, medium.
- Remediation verification: GPT-6 Astra, medium.
- Fresh-eyes retrospective: GPT-6 Luna, medium.

Observed result: all implementation phases completed without recorded design
escalation; final convergence found one low-severity issue. This does not show
that model routing caused that result. The routing list is experimental
metadata supplied for this retrospective, not a repository-derived finding.

## Process Changes for Feature 004

### 1. Commit drafts before independent review

For substantial SDD artifacts, commit the draft, conduct independent review,
then commit the clarified/approved artifact. Apply the same sequence to
`plan.md` and `tasks.md` where useful. Git can then preserve exact before/after
review changes without duplicate review artifacts or transcripts;
`reviews.md` should continue to preserve concise findings and rationale.

### 2. Record model routing only for explicit experiments

Do not add model names to normal commits, product documentation, or task
metadata by default. When routing is intentionally evaluated, preserve a small
experimental ledger in the retrospective or another explicitly experimental
artifact. This is not mandatory project ceremony.

## Practices to Preserve

Preserve discovery before specification when product direction is uncertain;
concise `reviews.md` decision records; independent review gates before
implementation; a coherent public-activation boundary; phase-level autonomous
implementation; evidence-driven optional live validation; fresh-context
convergence; and a post-convergence fresh-eyes retrospective. These practices
are supported by Feature 003's decision record, task sequence, and release
validation; this list adds no new process rules.

## Repository Storytelling Result

**MOSTLY.** Feature 003 materially improved reconstruction despite retaining
Feature 002's categorical verdict. The remaining gap is no longer primarily
“what decisions/reviews happened”; it is finer-grained before/after evidence
and experimental execution metadata. The verdict is the fresh-agent
retrospective finding; the comparison is a human interpretation of that result
against Feature 002's retrospective.

## Future Experiment

For Feature 004, commit substantial draft artifacts before review, continue
`reviews.md`, and repeat the same fresh-eyes storytelling test. Determine
whether exact Git before/after evidence moves the result from MOSTLY toward YES
without adding substantial documentation burden.

## Evidence Discipline

Completion counts, validation results, review dispositions, and commit file
changes above are durable repository evidence (`tasks.md`, `reviews.md`,
`release-validation.md`, and Git history). The storytelling verdict and
reconstruction observations are fresh-agent retrospective findings. The
attention interpretation and proposed Feature 004 changes are human
interpretation. Model routing is reconstructed experimental metadata supplied
from the development session, not independently verifiable repository
evidence. No missing history has been invented, and this retrospective does
not alter the feature's discovery, review, specification, plan, task, or
release-validation records.
