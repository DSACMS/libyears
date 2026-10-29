# Feature 005 Implementation Task Graph

## Status and authority

**DRAFT / READY FOR INDEPENDENT TASK-GRAPH REVIEW** — run `005-0012`,
2026-10-29. **Implementation: NOT AUTHORIZED.** All tasks below are unstarted.
Creating this graph does not approve implementation or commission its reviews.
Next gate: INDEPENDENT TASK-GRAPH REVIEW, followed by explicit execution authority.

The [approved specification](spec.md) and [approved technical plan](plan.md)
govern. [Reviews](reviews.md) record specification approval in 005-0007 and plan
approval in 005-0011, closing F1/F2 and P1 respectively. Earlier pending and
rejected records remain historical. This graph decomposes those decisions;
it neither revises their contracts nor authorizes an external target or network.

## Dependencies and execution rules

There are 13 tasks, including verification, documentation and convergence.
Every predecessor listed below must be complete; table order alone grants no
readiness. The graph is acyclic. Execute sequentially unless a later prompt
explicitly authorizes parallel execution. No task is currently executable.

| Task | Work unit | Predecessors | Phase |
|---|---|---|---|
| T001 | Closed Gemfile parser and declaration records | None | Foundations |
| T002 | Typed scoped evidence | None | Foundations |
| T003 | Bounded safe reads and replacement regressions | T001 | Foundations |
| T004 | Scoped selection and source availability | T001, T002, T003 | Scoped source |
| T005 | Authorized lock association and safe row evidence | T004 | Scoped source |
| T006 | Mixed scan propagation and aggregation | T005 | Integration |
| T007 | Additive scoped JSON serialization | T006 | Integration |
| T008 | Scoped human reporting | T007 | Integration |
| T009 | Public CLI activation | T006, T007, T008 | Integration |
| T010 | Composed acceptance and regression verification | T009 | Verification |
| T011 | Documentation and real-root validation preparation | T010 | Documentation |
| T012 | Required authorized real-root evidence | T011 | Validation |
| T013 | Read-only convergence review | T010, T011, T012 | Convergence |

Add behavioral tests with each code change, not only in T010. Each task should
be independently reviewable and normally one local commit when an execution
prompt authorizes commits. Do not bundle unrelated cleanup. Use unittest and
unittest.mock, synthetic fixtures and injected registry results; deterministic
tests never require network, package managers or target code execution.
Run the narrow affected modules first, broader regressions at phase boundaries,
and `git diff --check` before task completion. Record exact commands/results
and evidence locations against each completed task; unchecked tasks are not
acceptance evidence. Stop for an actual missing decision rather than expanding
the approved static subset, source authority, schema or platform design.

## Task definitions

### T001 — Closed Gemfile parser and declaration records

- [ ] Complete. **Predecessors:** None.
- **Authority:** spec S1/S2 and security; plan “Static recognition and declaration
  records” and Gemfile physical-line bound. AC-03/04/08/09/10/23.
- **Change:** Add pure `libyears/gemfile.py` recognition with the approved
  physical-line cursor, immutable declaration/parsed/failure records, exact
  identities, ordered requirements, full sorted memberships and established
  groups. Implement exhaustive positive forms, default versus explicit groups,
  block/option union, optional membership, duplicate/nested rejection, complete
  consumption and first-line-before-completion failure precedence. Discard raw
  source values after authority comparison; diagnostics contain safe categories.
  Move only the existing Ruby name/requirement framing validators here and
  import them from rubygems.py without changing ordinary authorization semantics.
- **Evidence:** `tests/test_gemfile.py` tables exercise every S1 positive form
  and negative syntax family, LF/CRLF, quotes/comments, malformed trailing tokens,
  unsupported unselected code, duplicate identities, empty/default groups,
  case sensitivity and physical-line boundary/one-over. No partial result,
  evaluator, filesystem or registry access. Existing Ruby source/authorization
  regressions pass after validator extraction. Start small annotated fixtures
  under `tests/fixtures/ruby_groups/` with expected populations/rejection reasons.

### T002 — Typed scoped evidence

- [ ] Complete. **Predecessors:** None.
- **Authority:** spec S4; plan “Evidence propagation and safe output”. AC-21.
- **Change:** Add GemfileEvidence and optional trailing row fields to candidate,
  measured and unmeasurable models, plus optional requested_groups in source
  evidence. Preserve defaults and positional callers. Represent omitted
  lock_requirement separately from present null with the planned inclusion flag.
  Do not add registry-result fields or serialize raw parser records.
- **Evidence:** Focused construction/compatibility assertions demonstrate old
  callers and all three requirement states (omitted, present null, safe text).
  Existing model consumers and ordinary output tests pass; scoped serialization
  is deliberately owned by T007, not assumed from these model checks.

### T003 — Bounded safe reads and replacement regressions

- [ ] Complete. **Predecessors:** T001.
- **Authority:** spec S1/S4/security; plan “Filesystem safety and bounded work”
  and P1 verification paragraph; review 005-0011. AC-08/11/23/24/28.
- **Change:** Add the private scoped Ruby root reader in rubygems.py. Resolve
  root once, restrict exact input names, validate link containment before open,
  walk resolved relative components using directory descriptors/no-follow, and
  open BOTH final components with `O_RDONLY | O_NOFOLLOW | O_NONBLOCK`.
  Immediately `fstat`/`S_ISREG` before wrapping or reading; consume only that
  descriptor. Fail closed when required capabilities are absent, with no unsafe
  fallback. Close descriptors on every path. Apply strict UTF-8, CRLF handling,
  1 MiB Gemfile/16 KiB physical line/16 MiB lock caps and limit+1 reads; preserve
  approved safe reasons and ordinary Feature 004 reads.
- **Evidence:** `test_ruby_groups.py` covers missing/unreadable/nonregular,
  dangling/internal/escaping links, root/parent/nested/alternate decoys,
  replacement symlinks, invalid UTF-8, exact/one-over bounds and cleanup.
  Separate Gemfile AND Gemfile.lock tests validate a regular input, replace it
  with a FIFO at the final-open hook AFTER metadata/containment validation,
  then invoke real open with production flags and no writer. Assert prompt
  nonregular rejection before any content read and descriptor closure. A bounded
  subprocess guards hangs; use hook synchronization, no sleeps. A pre-existing
  FIFO alone is insufficient. Skip only real FIFO witnesses on incapable
  platforms; mocks still prove safe capability failure/no fallback. T004 adds
  composed source-state/no-lookup assertions to these same replacement cases.

### T004 — Scoped selection and source availability

- [ ] Complete. **Predecessors:** T001, T002, T003.
- **Authority:** spec S1–S4; plan source-flow steps 1–4 and availability matrix.
  AC-03/04/05/06/07/10/11/12/15/23/24/28.
- **Change:** Add scoped_ruby_source_result with always-present scoped source
  evidence, requested names and initially null format. Fully recognize Gemfile
  before exact group validation; unknown names prevent partial union and lock
  reads. Select unique declarations and establish N before lock access. Reuse
  entire existing lock parsing; missing nonempty lock produces lockfile_missing
  rows without pin fallback; absent/accepted empty is available empty, whereas
  rejected lock retains N (including zero), unavailable measurement and no rows.
  Accepted locks establish format even for empty selection. Keep this path
  unconnected to ordinary scanning until T006; T005 completes accepted-lock rows.
- **Evidence:** Scoped source tests assert selected union, full memberships,
  exact case, empty/default/unknown states, no lock reads after earlier failure,
  all safe read reasons, duplicate/malformed whole-lock rejection, scope counts
  and no registry calls. Compose BOTH T003 FIFO replacements through the source:
  Gemfile gives invalid_gemfile/unknown N/no lock read; lock is replaced only
  after Gemfile establishes scope and gives invalid_lockfile/known N/no rows.
  Both return promptly, close descriptors, consume no FIFO content and lookup
  nothing. Ordinary all-direct no-Gemfile-read tests remain unchanged.

### T005 — Authorized lock association and safe row evidence

- [ ] Complete. **Predecessors:** T004.
- **Authority:** spec S3/S4; plan source-flow steps 5–9 and evidence construction;
  approved F1/F2. AC-02/13/14/15/16/21/28.
- **Change:** Finish accepted-lock rows using an exact direct-name index, with
  no transitive substitution or excluded rows. Check nonpublic Gemfile authority
  before missing direct identity (F1), after whole-lock acceptance. Factor only
  the existing name/requirement/source authorization prefix, preserving ordinary
  order and artifact rules. Compare supported requirement evidence text exactly
  before selected-version checks; mismatch yields its stable reason, both safe
  values and no version association. Build candidates only after all authority
  gates; retain existing isolated selection failures. F2 retains
  unsupported_requirement and N, omits unsafe lock_requirement and selected
  artifacts, and derives safe declared text from Gemfile on every scoped failure.
- **Evidence:** Source tables cover each stable reason and composed precedence,
  missing-direct despite transitive match, mismatch null/order/whitespace/operator
  cases, equal multiple literals, no excluded lookup, and private/pinned/GIT/PATH/
  multiple-remote public-namesake prohibitions. Explicit F1 missing-direct and F2
  unsupported-lock-requirement witnesses assert known N, no candidate/lookup,
  safe declaration metadata and required omission. Ordinary Ruby authorization
  regressions pass after shared helper extraction. No semantic requirement check.

### T006 — Mixed scan propagation and aggregation

- [ ] Complete. **Predecessors:** T005.
- **Authority:** spec baseline/S1/S3/S4; plan “CLI, mixed scanning and aggregation”
  and evidence propagation. AC-01/02/04/05/06/15/17/18/19/21/25/26/28.
- **Change:** Accept optional validated ruby_groups, dedicated scoped-request
  error and canonical tuple before source reads; choose exactly one Ruby path.
  Absent request retains existing call behavior and never reads Gemfile. Carry
  declaration evidence and safe declared text through success/RegistryFailure
  without changing registry types or selected/publication artifact merging.
  Apply scoped unavailable null aggregates at the ecosystem boundary, retaining
  known N and successful sibling measurements. Preserve repository unknown
  denominator/coverage rules and Python-only resolved evidence.
- **Evidence:** Mixed tests cover every approved availability row, rejected lock
  at N=0 and N>0, wholly unmeasurable 0%, empty null coverage/0.0 total, successful
  siblings and no siblings. Inject canonical registry outcomes to assert expected
  age, platform/date provenance, exact same-version zero and flagged clamping.
  Spies confirm one source path and authorized lookup counts; existing transport/
  TLS and ecosystem regressions protect unchanged adapter wiring and identity.

### T007 — Additive scoped JSON serialization

- [ ] Complete. **Predecessors:** T006.
- **Authority:** spec S4; plan “Evidence propagation and safe output”. AC-20/21/22/28.
- **Change:** Explicitly serialize scoped source and measured/unmeasurable
  Gemfile evidence in output.py, schema_version=3. Preserve ordinary keys,
  values and omissions. Keep full sorted memberships, ordered requirements,
  recognized format versus null, and absent versus null lock_requirement.
- **Evidence:** Exact dictionary/key-presence tests cover all S4 states, missing
  inputs/direct rows, rejected lock, F1/F2, mismatch, local and registry failures,
  retained artifacts and ordinary omission. Distinct synthetic unsafe markers
  never appear; verbose mode adds no human diagnostics to JSON. Labels assert
  supplied-file evidence only. Extend test_output.py alongside these changes.

### T008 — Scoped human reporting

- [ ] Complete. **Predecessors:** T007.
- **Authority:** spec S4; plan human-output paragraphs. AC-17/20/22/28.
- **Change:** Render scoped sources, requested/full declared groups, safely
  available requirements, safe reasons and recognition availability in both
  single and mixed branches. Preserve ordinary wording. State supplied-file and
  observable-publication limitations; use the approved mismatch explanation and
  safely explain nonpublic authority without printing its value.
- **Evidence:** Paired human/JSON fixtures for measured, local/registry failure,
  empty, unavailable and wholly unmeasurable cases assert matching counts and
  evidence in normal/verbose output. F2/raw private values never echo. A group
  named production remains an ordinary name; no deployment/runtime/history claim.

### T009 — Public CLI activation

- [ ] Complete. **Predecessors:** T006, T007, T008.
- **Authority:** spec S1/S4; plan CLI validation and compatibility. AC-01/02/03/05/19/24/27.
- **Change:** Add repeatable --ruby-group GROUP with the exact ASCII name
  validation, sort/deduplication, no implicit default and directory-only target
  validation. Pass the new keyword only when requested. Map dedicated request
  errors to 1, completed source-error reports to 0 and systemic errors to 2.
- **Evidence:** test_cli.py covers real CLI→mixed scan→mock registry results,
  expected selected age, Test/test, repeated/multiple groups, malformed/empty/
  missing/comma values, file/invalid paths, all exit categories, --resolved
  remaining Python-only and unchanged injected ordinary scan calls. Public
  activation lands only after both report formats support scoped evidence.

### T010 — Composed acceptance and regression verification

- [ ] Complete. **Predecessors:** T009.
- **Authority:** spec S5/security; plan full deterministic matrix and compatibility.
  Verification owner for AC-01 through AC-28, supplementing earlier task tests.
- **Change:** Complete composed witnesses across parser→source→scan→CLI/output,
  including precedence from Gemfile/unknown group through rejected lock, F1,
  local validation, mismatch, selection and registry. Fill actual coverage gaps,
  not duplicate every unit test. Maintain explicit AC-to-test assertions in
  feature acceptance evidence; keep negative parser and precedence tables distinct.
- **Evidence:** Every plan matrix witness has a concrete test location and
  passing result. Assert P1 for both inputs, F1/F2 safe output, ordinary no-read,
  three-ecosystem same-name isolation, sibling survival, fixed public transport
  wiring, no target mutation/execution/config/credential/archive access and exact
  metric results. Fixture README states expected groups, populations and rejection
  reasons without application-coverage claims. Run focused affected modules then
  `python -m unittest discover -s tests` and `git diff --check`; record results.
  Product correctness remains offline, using mocks/fixtures only.

### T011 — Documentation and real-root validation preparation

- [ ] Complete. **Predecessors:** T010.
- **Authority:** spec user outcome/S1–S5; plan component documentation and later
  validation gate. AC-20/22, plus S5 acceptance-evidence preparation.
- **Change:** At this documentation checkpoint update README.md, SPEC.md and
  curated CHANGELOG.md Unreleased/Added for explicit group activation, closed
  subset/rejections, all-direct compatibility, safe provenance, limits and
  supplied-file claims. Create feature release-validation evidence with the
  deterministic AC/test/results index and a real-root validation procedure.
- **Evidence:** Examples match implemented CLI and both report formats; no
  inferred deployment or complete-publication-history claims. The procedure
  requires future permission naming a target or permitted supplied evidence,
  independent expected selected population, exact input/revision provenance,
  observed recognition/rejections, denominator/measurement distinction and
  before/after target integrity. Preparation alone does not satisfy T012.
  No target is selected, inspected or authorized by this task graph.

### T012 — Required authorized real-root evidence

- [ ] Complete. **Predecessors:** T011. **Additional condition:** explicit later
  human authorization for the particular target or permitted supplied evidence.
- **Authority:** spec S5 and plan later-validation gate. Acceptance corroboration
  for selected population/claims (AC-02/22); cannot replace T010 offline coverage.
- **Change:** Once authorized, carry out the prepared supplied-file example with
  independently established expected groups/population, using permitted local
  evidence and mocked/supplied registry results unless network is separately
  authorized. Record inputs, expected versus observed selection, limitations and
  unsupported constructs accurately. Never execute Ruby/Bundler or alter targets.
- **Evidence:** Required real-root example and population comparison are recorded
  with provenance and authorization scope; distinguish supplied human attestation
  from independently inspected facts. An unsupported example or absent permission
  cannot be marked successful by substituting a synthetic fixture or optional
  live smoke. If evidence is unavailable, leave this task pending and convergence
  gated; earlier deterministic work can remain complete.

### T013 — Read-only convergence review

- [ ] Complete. **Predecessors:** T010, T011, T012.
- **Authority:** spec S5; plan compatibility/verification/validation gates and
  AGENTS.md SDD convergence. Review owner for all ACs and source boundaries.
- **Change:** Independently reconcile approved spec, plan, task completion,
  implementation, tests, documentation and required real-root evidence. Perform
  no remediation inside the review. Report completeness separately from verdict;
  record missing evidence/findings and return corrections to their owning tasks.
- **Evidence:** Read-only review accounts for 28/28 ACs, all task dependencies,
  P1/F1/F2, ordinary regressions, resource/security boundaries and required versus
  optional validation. No convergence claim if T012 is pending or deterministic
  evidence is incomplete. No release, tag, push or publication is authorized.

## Acceptance ownership

Implementation/behavior owners below build the observable; T010 verifies the
composed result and T013 audits every criterion. Multiple owners reflect actual
boundaries rather than extra tasks. All evidence remains planned, not passed.

| AC | Implementation / behavior owners | Verification owners |
|---|---|---|
| AC-01 | T006, T009 | T010, T013 |
| AC-02 | T005, T006, T009 | T010, T012, T013 |
| AC-03 | T001, T004, T009 | T010, T013 |
| AC-04 | T001, T004, T006 | T010, T013 |
| AC-05 | T004, T006, T009 | T010, T013 |
| AC-06 | T004, T006 | T010, T013 |
| AC-07 | T004 | T010, T013 |
| AC-08 | T001, T003 | T010, T013 |
| AC-09 | T001 | T010, T013 |
| AC-10 | T001, T004 | T010, T013 |
| AC-11 | T003, T004 | T010, T013 |
| AC-12 | T004 | T010, T013 |
| AC-13 | T005 | T010, T013 |
| AC-14 | T005 | T010, T013 |
| AC-15 | T004, T005, T006 | T010, T013 |
| AC-16 | T005 | T010, T013 |
| AC-17 | T006, T008 | T010, T013 |
| AC-18 | T006 | T010, T013 |
| AC-19 | T006, T009 | T010, T013 |
| AC-20 | T007, T008, T011 | T010, T013 |
| AC-21 | T002, T005, T006, T007 | T010, T013 |
| AC-22 | T007, T008, T011 | T010, T012, T013 |
| AC-23 | T001, T003, T004 | T010, T013 |
| AC-24 | T003, T004, T009 | T010, T013 |
| AC-25 | T006 | T010, T013 |
| AC-26 | T006 | T010, T013 |
| AC-27 | T009 | T010, T013 |
| AC-28 | T003, T004, T005, T006, T007, T008 | T010, T013 |

## Review checkpoints and validation separation

Natural independent review checkpoints, to commission under later execution
authority, are after T005 (closed parser, safe reads/P1, association/F1/F2 and
ordinary Ruby compatibility), after T010 (public integration, all 28 deterministic
witnesses and full regression suite), and T013 (final convergence including
documentation and required real-root evidence). These identify useful review
boundaries without claiming a review has happened or changing the approved design.

Optional live registry smoke is outside the required dependency graph. It needs
separate target/network authorization, may follow public integration, and has
no outgoing dependency to T010–T013 or any mandatory task. Record its result or
environmental failure separately; it cannot substitute for deterministic tests
or independently established real-root selected population. Do not weaken TLS
or run a package manager to obtain evidence. No optional smoke is commissioned.

## Current gate — independent task-graph review

**STOP: INDEPENDENT TASK-GRAPH REVIEW REQUIRED.** Review ordering, bounded task
scope, dependency readiness, every AC owner, FIFO replacement witnesses, F1/F2,
ordinary compatibility, and conditional validation boundaries against the
approved artifacts. This draft is not implementation approval. No task has
begun, no external validation is authorized, and no product code was changed.
