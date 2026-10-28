# Feature 004: Draft task graph

## Status and authority

**Ready for narrow task-graph verification**

**Implementation remains NOT APPROVED.** All tasks below are pending. This
artifact is task decomposition only. The independent task-graph review returned
REVISE; the two material findings are corrected below and recorded in reviews.md.
The next gate is narrow task-graph verification, followed by explicit implementation
approval. Do not begin a phase on the authority of this draft.

Authority: approved spec.md, plan.md (8b4bf8fb6535bad524fc02bdfdcc5e1beea79a92), approval records in reviews.md,
and repository AGENTS.md. Historical pending status in the plan is superseded by
the narrow architecture verification recorded in reviews.md. Discovery and
ROADMAP supply context, not additional implementation scope. This graph neither
changes approved decisions nor authorizes external repository access.

## Execution and stopping rules

Execute sequentially by default, in the numbered order below. No tasks are
marked parallelizable: the parser/matcher, shared model/transport, adapter and
activation boundaries benefit from serial review. Dependencies below are explicit;
phase order is preserved even where a module could technically be developed alone.
Each task is one independently reviewable local commit when execution is later
authorized. Include its tests with its behavior, update this task's status only
after acceptance and verification pass, and run git diff --check before committing.
All task commits may include tasks.md for status/evidence bookkeeping.

Every stopping condition also requires focused verification to pass and the
repository to remain valid. T001–T014 must leave public scan source pairs and
public output unchanged. Ruby source results and adapter calls are internal only;
defaulted evidence fields must add nothing to existing serialized ecosystems.
Only T015 activates directory scanning, with the entire public contract and docs.
If activation is too large for a bounded review, prepare additional internal work
without activating it and return the graph for review; do not split public coherence.

No task permits Ruby/Bundler/package-manager/repository code execution,
installation, dependency resolution, private requests, credentials, public-namesake
fallback, metric changes, new flags, or generic parser/resolver/registry frameworks.
Only authorize_public_selection may construct Ruby candidates after complete
structural validation and all-occurrence authority checks. Rejected evidence must
never reach HTTP. The registry API accepts identities, never repository URLs.

All correctness verification uses unittest, local fixtures/mocks, injected HTTP
and clock/sleep; new source/scan/CLI fixtures must prohibit live requests. Fixtures
live under tests/fixtures/rubygems/ and accompany their owning task. Commands below
use module names (python -m unittest MODULE...); no verbose output by default.
Live dogfood belongs only to Phase 7 and cannot satisfy deterministic AC ownership.
Expected files are bounded implementation targets, not permission for unrelated
cleanup. Existing metric.py, ecosystem policy modules and cli.py remain unchanged
as specified by the plan. Stop and report any genuine product/architecture gap.

## Phase and gate structure

| Phase | Approved objective | Tasks | Gate |
|---|---|---|---|
| 1 | Bounded syntax | T001–T003 | Parser suite at T003 |
| 2 | Authority/matching and typed evidence | T004–T007 | Parser/source/output compatibility at T007 |
| 3 | Bounded shared transport | T008–T010 | Transport and existing adapter regressions, full deterministic suite at T010 |
| 4 | Registry and canonicalization | T011–T014 | Adapter/source/parser suites at T014; no activation |
| 5 | Coherent public activation | T015 | Mixed/output/CLI then full deterministic suite |
| 6 | Deterministic convergence preparation | T016–T017 | Unique end-to-end cases then full deterministic suite at T017 |
| 7 | Authorized dogfood and independent convergence | T018–T021 | Release evidence, independent review, completion and retrospective |

Full deterministic command at T010, T015 and T017 is
`python -m unittest discover -s tests`. These are transport/model integration,
public activation and final deterministic gates, respectively. Do not repeat the
full suite for small edits without a diagnostic reason. Existing unchanged
regression suites cover Python declarations/snapshot/constraints/legacy scan,
PyPI/npm registry semantics, package-lock/Yarn selection, metric, mixed reports,
output and CLI. No deterministic tests are run merely to create this draft.

## Tasks

### T001 — Parse supported lock structure

- **Status:** Pending; **Phase:** 1; **Parallelizable:** No.
- **Objective and approved scope:** Build the pure line-oriented parser and immutable lock records from the plan. Consume supported GEM, direct, platform and optional tool/runtime framing, LF/CRLF and blank separators; preserve raw selections, declarations, metadata order and duplicate spec occurrences. Do not perform matching or I/O.
- **Expected files:** libyears/gemfile_lock.py; tests/test_gemfile_lock.py; parser fixtures.
- **Acceptance criteria mapped:** 03, 07, 48.
- **Dependencies:** None.
- **Focused deterministic verification:** tests.test_gemfile_lock: ordinary/empty scope, required/missing/repeated/empty/duplicate/malformed PLATFORMS, optional tool/runtime sections and non-scope metadata.
- **Safe stopping condition:** Pure internal parser handles the supported subset; public scan unchanged.
- **Suggested commit:** `feat(rubygems): parse bounded lock snapshot structure`.

### T002 — Isolate source envelopes and nested rows

- **Status:** Pending; **Phase:** 1; **Parallelizable:** No.
- **Objective and approved scope:** Extend syntax handling for repeated GEM and allowed GIT/PATH envelopes, exact indentation and nested ownership. Preserve multiple GEM remotes and unsupported isolated selection tokens. Validate nested framing without evaluating safely delimited requirements.
- **Expected files:** libyears/gemfile_lock.py; tests/test_gemfile_lock.py; parser fixtures.
- **Acceptance criteria mapped:** 04, 49.
- **Dependencies:** T001.
- **Focused deterministic verification:** tests.test_gemfile_lock: source metadata allowlists/duplicates, repeated blocks, nested supported/inert unsupported/unsafe text, orphan rows, tabs and broken parentheses.
- **Safe stopping condition:** Source ownership is retained or whole-source failure returned; no partial scope escapes.
- **Suggested commit:** `feat(rubygems): preserve lock source and nested framing`.

### T003 — Classify whole-lock rejection deterministically

- **Status:** Pending; **Phase:** 1; **Parallelizable:** No.
- **Objective and approved scope:** Complete positive recognition and malformed versus unsupported classification, collecting findings so malformed supported structure wins. Cover arbitrary/empty content, unknown fields/sections, recognized unsupported sections, conflict markers and trailing syntax.
- **Expected files:** libyears/gemfile_lock.py; tests/test_gemfile_lock.py; parser fixtures.
- **Acceptance criteria mapped:** 05, 50 (structural precedence).
- **Dependencies:** T002.
- **Focused deterministic verification:** tests.test_gemfile_lock (Phase 1 gate), including permutations of malformed plus unsupported evidence and unrecoverable identity.
- **Safe stopping condition:** Every rejected parse exposes no partial scope and only safe section/line/category context; no public changes.
- **Suggested commit:** `feat(rubygems): reject unsupported and malformed lock evidence`.

### T004 — Add defaulted typed Ruby evidence

- **Status:** Pending; **Phase:** 2; **Parallelizable:** No.
- **Objective and approved scope:** Add the three output-facing Ruby records and optional evidence fields to candidate/dependency/failure/registry outcomes; add optional source scope/publication basis. Preserve positional constructors and old serialization; do not serialize Ruby publicly yet.
- **Expected files:** libyears/model.py; tests/test_rubygems.py; tests/test_output.py.
- **Acceptance criteria mapped:** 38 (domain preparation), 37 (model compatibility).
- **Dependencies:** T003.
- **Focused deterministic verification:** tests.test_rubygems and tests.test_output: optional-field defaults, existing constructors and exact existing ecosystem evidence; no new serializer behavior.
- **Safe stopping condition:** Shared model remains backwards compatible and exposes no new existing-output fields.
- **Suggested commit:** `feat(rubygems): add optional typed provenance records`.

### T005 — Establish sole public-source candidate gate

- **Status:** Pending; **Phase:** 2; **Parallelizable:** No.
- **Objective and approved scope:** Implement authorize_public_selection with all exact-name occurrences and pin marker. Only independently authorized literal public GEM blocks may contribute. Reject GIT/PATH/private/missing/multiple remotes and public namesakes; keep remote values out of diagnostics.
- **Expected files:** libyears/rubygems.py; tests/test_rubygems.py; authority fixtures.
- **Acceptance criteria mapped:** 13, 47.
- **Dependencies:** T004.
- **Focused deterministic verification:** tests.test_rubygems: every rejected authority/pin/public-namesake combination makes no lookup/candidate; unsafe ownership remains parser failure.
- **Safe stopping condition:** No candidate can bypass positive public authority; internal API only.
- **Suggested commit:** `feat(rubygems): gate candidates on public source authority`.

### T006 — Match direct identities and selected artifacts

- **Status:** Pending; **Phase:** 2; **Parallelizable:** No.
- **Objective and approved scope:** Implement exact lock matching, bounded names and direct requirements, version/platform interpretation, missing specs, agreeing variants, duplicate/differing ambiguity and local failure precedence. Preserve material selected evidence, direct text and special-dependency counting; never evaluate requirements or select host variants.
- **Expected files:** libyears/rubygems.py; tests/test_rubygems.py; matching fixtures.
- **Acceptance criteria mapped:** 08 (lock identity), 09–12, 14–17, 46, 50 (local precedence).
- **Dependencies:** T005.
- **Focused deterministic verification:** tests.test_rubygems: name/case, requirements forms, unsupported isolated tokens, ordinary/platform/agreeing/differing/duplicate artifacts across blocks, bundler/tzinfo-data, combined-reason permutations; rejected directs produce no requests.
- **Safe stopping condition:** Only authorized exact supported selections become candidates; failures retain known direct scope.
- **Suggested commit:** `feat(rubygems): match direct lock snapshot evidence`.

### T007 — Build internal root source results

- **Status:** Pending; **Phase:** 2; **Parallelizable:** No.
- **Objective and approved scope:** Read only root Gemfile.lock, distinguish absence from present broken-link/nonregular/unreadable/invalid-text artifacts, and return SourceResult availability/evidence/diagnostics. Gemfile and nested/alternate artifacts are never inspected. Whole rejection returns no candidates or synthetic dependency rows.
- **Expected files:** libyears/rubygems.py; tests/test_rubygems.py; source fixtures.
- **Acceptance criteria mapped:** 01–02 (internal discovery), 04 (reader), 06–07, 32 (source result), 43 (local boundary).
- **Dependencies:** T006.
- **Focused deterministic verification:** tests.test_gemfile_lock tests.test_rubygems tests.test_output (Phase 2 gate): artifact presence matrix, invalid text, local counts and zero scope, no-call rejection, untouched target, exact old-output compatibility.
- **Safe stopping condition:** Internally callable source works; scan still has only Python/npm source pairs.
- **Suggested commit:** `feat(rubygems): discover internal root lock source results`.

### T008 — Lock down existing transport compatibility

- **Status:** Pending; **Phase:** 3; **Parallelizable:** No.
- **Objective and approved scope:** Add focused characterization assertions before bounded transport changes, preserving default urlopen, timeout/context/User-Agent, no-argument read and injected get(url) doubles. Reuse current tests where sufficient.
- **Expected files:** tests/test_registry.py; possibly tests/test_pypi.py and tests/test_npm_registry.py.
- **Acceptance criteria mapped:** 19, 37 (transport compatibility).
- **Dependencies:** T007.
- **Focused deterministic verification:** tests.test_registry tests.test_pypi tests.test_npm_registry; assert existing trust precedence and failures without requiring headers, opener or sized-read support from old doubles.
- **Safe stopping condition:** Old default/injected paths are protected by passing tests before opt-in changes.
- **Suggested commit:** `test(registry): preserve default and injected transport contracts`.

### T009 — Add opt-in verified bounded responses

- **Status:** Pending; **Phase:** 3; **Parallelizable:** No.
- **Objective and approved scope:** Add optional max_response_bytes/allowed_authority with a separate verified opener rejecting redirects. Keep default path untouched. Detect oversize using limit+1/declared length and truncation including IncompleteRead/short EOF; return typed bounded failures without partial bytes.
- **Expected files:** libyears/registry.py; tests/test_registry.py.
- **Acceptance criteria mapped:** 18–19 (transport), 44 (bounded transport).
- **Dependencies:** T008.
- **Focused deterministic verification:** tests.test_registry tests.test_pypi tests.test_npm_registry: exact limit, excess, declared length, incomplete read, redirect rejection, verified context and old no-argument read/get behavior.
- **Safe stopping condition:** Opt-in path is finite and fail closed; default behavior unchanged; Ruby not activated.
- **Suggested commit:** `feat(registry): add opt-in bounded verified transport`.

### T010 — Expose safe rate-limit failure metadata and integration gate

- **Status:** Pending; **Phase:** 3; **Parallelizable:** No.
- **Objective and approved scope:** Add defaulted optional Retry-After failure metadata and preserve ordinary error classifications and existing consumers. Finish shared-transport/model integration regressions before the Ruby adapter depends on them.
- **Expected files:** libyears/registry.py; tests/test_registry.py.
- **Acceptance criteria mapped:** 45 (transport metadata), 37 (shared regression).
- **Dependencies:** T009.
- **Focused deterministic verification:** tests.test_registry tests.test_pypi tests.test_npm_registry tests.test_yarn tests.test_mixed_scan, then full deterministic suite (Phase 3 transport/model gate).
- **Safe stopping condition:** Shared transport is independently reviewable and compatible; no Ruby scan or adapter coupling.
- **Suggested commit:** `feat(registry): retain safe rate-limit response metadata`.

### T011 — Enforce Ruby transport and validate registry population

- **Status:** Pending; **Phase:** 4; **Parallelizable:** No.
- **Objective and approved scope:** Build internal RubyGemsAdapter identity-then-population requests only through T009’s opt-in verified transport, with fixed supported HTTPS authority rubygems.org, all redirects rejected, 16 MiB per response, two requests/32 MiB per candidate and default positive 10-second timeout. Consume shared controls without duplicating their implementation; preserve CA precedence and User-Agent. Map typed response_too_large/incomplete_response to invalid_registry_response without partial evidence; ordinary transport/TLS/timeout failures remain registry_error. Defensively validate identity/quoting and establish endpoint-independent ASCII case-only identity even when population records omit names; reject punctuation/Unicode substitutions. Apply strict JSON/required field/ABI/full-artifact validation. Use the pinned upstream source chain to document fixtures. Handle equivalent versus contradictory duplicates and public absence without inventing history.
- **Expected files:** libyears/rubygems_registry.py; tests/test_rubygems_registry.py; registry fixtures and fixture documentation.
- **Acceptance criteria mapped:** 08 (endpoint-independent registry identity), 18–19 (Ruby transport enforcement), 20, 27 (absence), 44 (Ruby budgets and bounded-failure mapping).
- **Dependencies:** T010.
- **Focused deterministic verification:** tests.test_rubygems_registry: fixed two endpoints/order and supported authority, input/link/credential injection, redirect rejection, exact/excess byte and request limits, typed oversize/incomplete mapping versus ordinary registry_error, no partial evidence, verified TLS/CA/timeout/User-Agent; identity endpoint case-only agreement followed by nameless population, punctuation/Unicode mismatch rejection; required types/classification, ABI excluded vs unclassifiable, duplicate keys/records, 404 and empty populations. Use mocked HTTP through the restricted transport as well as injected typed failures; no live requests.
- **Safe stopping condition:** Every executable Ruby request uses the approved transport boundary from its introduction; only complete validated population evidence may reach T012. No public activation.
- **Suggested commit:** `feat(rubygems): validate public registry identity and artifacts`.

### T012 — Canonicalize publication and select stable evidence

- **Status:** Pending; **Phase:** 4; **Parallelizable:** No.
- **Objective and approved scope:** Implement canonical_publication and shared per-version canonical results only over T011 evidence that has passed Ruby transport enforcement and population validation. Retain every admissible contributor; apply UTC precision/import-day exclusion, supported observable artifact rules, latest eligibility/ties and registry failure precedence. Use existing metric calls for zero/anomaly arithmetic.
- **Expected files:** libyears/rubygems_registry.py; tests/test_rubygems_registry.py; publication fixtures.
- **Acceptance criteria mapped:** 21–29, 51 (publication semantics), 50 (registry precedence).
- **Dependencies:** T011.
- **Focused deterministic verification:** tests.test_rubygems_registry plus tests.test_metric: offset/import-day boundaries, missing/invalid/naive/conflicting dates, earlier yanked, one valid/all inadmissible, prerelease used/stable latest, only-yanked, lexical ties/reordering, same-version zero and negative/nonnegative metric calls.
- **Safe stopping condition:** Used/latest share one canonical policy and typed contributor evidence; metric.py unchanged.
- **Suggested commit:** `feat(rubygems): canonicalize observable publication evidence`.

### T013 — Add scan-local pacing and cooldown

- **Status:** Pending; **Phase:** 4; **Parallelizable:** No.
- **Objective and approved scope:** Retain T011’s enforced transport/budgets and add per-scan sequential 0.11-second request-start pacing and 429 cooldown, seconds/date Retry-After, missing/invalid header closure, no retry or long cooldown sleep.
- **Expected files:** libyears/rubygems_registry.py; tests/test_rubygems_registry.py.
- **Acceptance criteria mapped:** 45 (scan-local pacing/cooldown).
- **Dependencies:** T012.
- **Focused deterministic verification:** tests.test_rubygems_registry tests.test_registry: injected time/sleep and HTTP responses; assert request-start spacing, seconds/date Retry-After, missing/invalid header closure, cooldown suppression and no retries/alternate hosts; retain T011’s transport enforcement while adding scan-local state.
- **Safe stopping condition:** Finite internal adapter preserves safe failure evidence; no public discovery.
- **Suggested commit:** `feat(rubygems): pace registry requests and enforce cooldown`.

### T014 — Prepare deterministic candidate scheduling

- **Status:** Pending; **Phase:** 4; **Parallelizable:** No.
- **Objective and approved scope:** Provide the plan's internal pre-measurement lexical (exact name, exact version) scheduling boundary for Ruby candidates. Exercise source-to-adapter composition internally with one scan-local adapter and fixed per-request responses; do not add a public source pair.
- **Expected files:** libyears/rubygems.py; tests/test_rubygems.py; tests/test_rubygems_registry.py.
- **Acceptance criteria mapped:** 45 (order independence), 43 (authority before HTTP).
- **Dependencies:** T013.
- **Focused deterministic verification:** tests.test_gemfile_lock tests.test_rubygems tests.test_rubygems_registry (Phase 4 gate): permute dependency/source order under 429 valid/missing Retry-After with injected time; identical schedules, outcomes and evidence; all rejected source/direct cases make zero requests.
- **Safe stopping condition:** Internal scheduling and adapter composition are ready; released scan/output remain unchanged.
- **Suggested commit:** `feat(rubygems): schedule authorized candidates deterministically`.

### T015 — Activate complete public RubyGems contract

- **Status:** Pending; **Phase:** 5; **Parallelizable:** No.
- **Objective and approved scope:** In one coherent change add the third explicit source pair and one local sources tuple, injectable Ruby lookup/adapter and CA propagation; merge provenance on successes/failures before existing metric calls. Activate all availability summaries, explicit additive schema-v3 serialization, contextual safe human output/disclosures and CLI behavior. Update README/SPEC/CHANGELOG Unreleased Added/AGENTS ecosystem scope together. Preserve all existing ecosystem paths, evidence and flags.
- **Expected files:** libyears/scan.py; libyears/output.py; tests/test_mixed_scan.py; tests/test_output.py; tests/test_cli.py; tests/fixtures/rubygems/; README.md; SPEC.md; CHANGELOG.md; AGENTS.md.
- **Acceptance criteria mapped:** 01–02 (public discovery), 30–42, 43 (public static boundary), 45 (public scheduling), 51 (disclosure), 52.
- **Dependencies:** T014.
- **Focused deterministic verification:** tests.test_mixed_scan tests.test_output tests.test_cli: three ecosystems, same-name isolation, unknown/known/empty/outage/null matrix, rejected sources zero lookup, contributor/failure provenance, exact prior evidence, scope/history disclosures, safe diagnostics and precedence, normal/verbose JSON equality, --resolved isolation, --ca-bundle/trust, exits 0/1/2, root vs direct-file and Gemfile-only/no-source; fixed-response order permutations assert identical rows/reasons/evidence/summaries. Then full deterministic suite (Phase 5 gate); manually compare docs to observable output.
- **Safe stopping condition:** Complete public contract and documentation agree; no intermediate partial Ruby scan is committed. Changelog checkpoint complete; existing PyPI/npm/Yarn behavior passes.
- **Suggested commit:** `feat(rubygems): activate coherent lock snapshot scanning`.

### T016 — Close unique end-to-end verification gaps

- **Status:** Pending; **Phase:** 6; **Parallelizable:** No.
- **Objective and approved scope:** Add only cross-boundary cases not already established by component and activation tests: combined structural/local/registry precedence, authority-to-no-HTTP guarantees, canonical contributors through serialization, artifact population failures through CLI and unchanged targets. Audit all AC ownership against actual test assertions; do not duplicate component tables or introduce behavior.
- **Expected files:** tests/test_mixed_scan.py; tests/test_output.py; tests/test_cli.py; tests/fixtures/rubygems/; tasks.md.
- **Acceptance criteria mapped:** 04, 13, 32, 38–39, 43–45, 50 (cross-boundary verification).
- **Dependencies:** T015.
- **Focused deterministic verification:** Run only added/affected test methods first, then affected mixed/output/CLI modules. Assert typed oversized and incomplete histories cannot become public metrics, private namesakes never reach HTTP, and deterministic response-order/cooldown outcomes survive output.
- **Safe stopping condition:** Unique full-path cases pass; any real product/architecture gap is reported rather than fixed by reinterpretation.
- **Suggested commit:** `test(rubygems): verify cross-boundary evidence failures`.

### T017 — Run final deterministic integration and traceability gate

- **Status:** Pending; **Phase:** 6; **Parallelizable:** No.
- **Objective and approved scope:** Reconcile the bidirectional AC-to-test/task record and documentation coherence, verify unchanged regression boundaries, and record deterministic results separately from future release evidence. No new runtime behavior.
- **Expected files:** tasks.md; test files only if a demonstrated deterministic coverage gap requires an approved case.
- **Acceptance criteria mapped:** 01–52 (verification audit; primary ownership below).
- **Dependencies:** T016.
- **Focused deterministic verification:** Full deterministic suite (Phase 6 final gate), git diff --check; inspect test assertions for all 52 ACs, all offline; compare README/SPEC/CHANGELOG/AGENTS to activated behavior. Re-run only justified affected checks if a gap is corrected.
- **Safe stopping condition:** All deterministic AC obligations have actual passing evidence; ready for separately authorized real-root validation.
- **Suggested commit:** `test(rubygems): record final deterministic integration gate`.

### T018 — Validate an authorized real Ruby root

- **Status:** Pending; **Phase:** 7; **Parallelizable:** No.
- **Objective and approved scope:** Use one explicitly authorized real root, inspecting only necessary root evidence; discovery paths grant no permission. Run normal verified human/JSON CLI without tooling execution; compare scope/counts/reasons/arithmetic/provenance/disclosures and record environment/limits. Verify target unchanged. Record discrepancies without remediation inside validation. In the same release-validation record assign separate live-smoke disposition: PERFORMED when a separate smoke supplied nonredundant evidence; REDUNDANT when authorized dogfood already exercised the same live path; UNAVAILABLE when useful smoke evidence could not be obtained; or DEFERRED when explicitly postponed with rationale. Run a separate bounded verified smoke only when useful; record its rationale/outcome without requiring it to permit convergence. Authorized real-root dogfood remains required; smoke disposition does not waive it.
- **Expected files:** specs/004-rubygems-support/release-validation.md; tasks.md.
- **Acceptance criteria mapped:** Release validation of approved contract; no exclusive AC ownership.
- **Dependencies:** T017; explicit authorization of the specific external root if outside workspace.
- **Focused deterministic verification:** No new deterministic suite: cite T017. Compare human/JSON real-root results and target before/after; keep environmental/network failures distinct from correctness. Check that the release-validation record includes one justified smoke disposition and any available smoke evidence.
- **Safe stopping condition:** Required dogfood evidence and smoke disposition are recorded; if dogfood is blocked, record the blocker and do not complete this task. No invented success or unauthorized external inspection; a separate smoke is never required to complete the record.
- **Suggested commit:** `docs(rubygems): record authorized repository validation`.

### T019 — Obtain independent convergence review

- **Status:** Pending; **Phase:** 7; **Parallelizable:** No.
- **Objective and approved scope:** Obtain fresh-context independent read-only convergence against approved spec/plan/tasks, implementation, tests, docs and release evidence. Record findings and verdict separately; do not silently remediate or mark completion while material findings remain.
- **Expected files:** specs/004-rubygems-support/reviews.md; tasks.md.
- **Acceptance criteria mapped:** Plan Release Validation and artifact lifecycle; review all ACs without replacing deterministic ownership.
- **Dependencies:** T018.
- **Focused deterministic verification:** Independent artifact/test-evidence audit; no routine full-suite repetition. Supply T017 deterministic evidence and T018 release-validation record, including required dogfood, smoke disposition and available evidence. Evaluate whether that evidence is sufficient; a separate smoke is never a prerequisite for convergence. Any required remediation needs bounded approved follow-up and re-convergence before T020.
- **Safe stopping condition:** Independent convergence verdict is recorded; only a satisfactory convergence with resolved material findings unblocks completion.
- **Suggested commit:** `docs(rubygems): record independent convergence review`.

### T020 — Complete feature bookkeeping and radar reconciliation

- **Status:** Pending; **Phase:** 7; **Parallelizable:** No.
- **Objective and approved scope:** After satisfactory convergence, finalize task statuses and completion references; reconcile ROADMAP's SELECTED entry using its existing lifecycle conventions and preserve separate interpreted-Gemfile EXPLORE scope. Do not invent a delivered radar state, tag, release or push.
- **Expected files:** specs/004-rubygems-support/tasks.md; ROADMAP.md; reviews.md or release-validation.md only for completion references.
- **Acceptance criteria mapped:** Plan Documentation and Artifact Lifecycle; no new product behavior.
- **Dependencies:** T019 (satisfactory convergence).
- **Focused deterministic verification:** Cross-check completion references, existing radar states/scope, recorded gate outcomes; git diff --check. No test rerun for bookkeeping alone.
- **Safe stopping condition:** Completion is accurately recorded without changing approved spec/plan or inventing radar semantics.
- **Suggested commit:** `docs(rubygems): reconcile feature completion records`.

### T021 — Write post-convergence retrospective

- **Status:** Pending; **Phase:** 7; **Parallelizable:** No.
- **Objective and approved scope:** Create retrospective after convergence and completion reconciliation, including evidence about whether committed pre-review drafts improved durable reconstruction; distinguish observation from causal claims. Finish task bookkeeping and confirm clean tree after final authorized commit.
- **Expected files:** specs/004-rubygems-support/retrospective.md; tasks.md.
- **Acceptance criteria mapped:** Plan Documentation and Artifact Lifecycle.
- **Dependencies:** T020.
- **Focused deterministic verification:** Check chronology and links to draft/review/convergence evidence; git diff --check and clean-tree check after commit. No deterministic rerun for prose only.
- **Safe stopping condition:** Retrospective exists after convergence; lifecycle complete, no release/tag/push.
- **Suggested commit:** `docs(rubygems): record post-convergence retrospective`.

## Bidirectional acceptance audit

The table assigns primary deterministic ownership, rather than mapping every AC
again to every integration gate. Component preparation mappings in task entries
identify portions of a contract completed at public activation; they do not claim
that an internal helper alone satisfies a public AC. T017 audits actual passing
assertions for every row. Phase 7 owns release/process evidence only.

| AC identifiers | Primary implementation / deterministic verification owner |
|---|---|
| AC-01–02 | T007 internal discovery; T015 public recognition and exclusion matrix |
| AC-03 | T001 |
| AC-04 | T002 framing; T007 reader; T015 whole-source public outcome |
| AC-05 | T003 |
| AC-06–07 | T007 (T001 frames non-scope sections) |
| AC-08 | T006 lock identity; T011 independent registry identity |
| AC-09–12 | T006 |
| AC-13 | T005 authority; T015 safe human authority explanation |
| AC-14–17 | T006; T012 also verifies registry population ignores locked/host platform for AC-16 |
| AC-18 | T009 shared transport restriction; T011 Ruby fixed-authority/redirect enforcement and safe URLs |
| AC-19 | T008 default compatibility; T009 bounded verified path; T011 Ruby opt-in trust |
| AC-20 | T011 |
| AC-21–29 | T012 |
| AC-30–36 | T015 |
| AC-37 | T004 model compatibility; T008/T010 transport regression; T015 full ecosystem compatibility |
| AC-38 | T004 typed preparation; T015 complete public serialization |
| AC-39–42 | T015 |
| AC-43 | T007 local static boundary; T014 authority before HTTP; T015 public no-execution/unchanged-target assertions |
| AC-44 | T009 bounded failure production; T011 Ruby budgets/mapping before canonicalization; T016 full-path no-partial-metric assertion |
| AC-45 | T010 rate metadata; T013 pacing/cooldown; T014 scheduling; T015 observable permutation invariance |
| AC-46 | T006 |
| AC-47 | T005 |
| AC-48 | T001 |
| AC-49 | T002 |
| AC-50 | T003 structural; T006 local; T012 registry precedence; T016 composed boundary |
| AC-51 | T012 observable-date/absence semantics; T015 public history disclosures |
| AC-52 | T015 |

Coverage audit: **52/52 AC identifiers mapped**. Every deterministic behavioral
AC has component or public integration verification scheduled before release
validation. No criterion relies exclusively on dogfood, smoke or convergence.
The multiple boundaries above are intentional: authority is checked locally and
again at the actual request boundary; transport failure production is distinct
from adapter/public reason mapping; model preparation differs from serialization;
lock identity differs from registry identity; arithmetic reuses existing metric
verification but Ruby dates must reach it correctly. Structural/local/registry
precedence requires both individual and composed assertions. History semantics
require both date behavior and user disclosure. Full-suite gates verify regression
integration and do not replace focused ownership. T016 adds only unique composed
cases, while T017 audits coverage rather than duplicating all tests.

Every task traces back to a named approved phase and its plan boundary: T001–T003
parser; T004–T007 evidence/authority/matching/source results; T008–T010 shared
transport; T011–T014 registry/canonicalization/scheduling; T015 public scan/output
and documentation checkpoint; T016–T017 deterministic convergence preparation;
T018–T021 release validation and artifact lifecycle. No task adds a product rule
or architecture beyond those boundaries.

## Dependency audit and activation invariant

Explicit edges form the chain:

`T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009 → T010 → T011 → T012 → T013 → T014 → T015 → T016 → T017 → T018 → T019 → T020 → T021`.

All edges point to a larger ID: the graph is acyclic, with this chain as its
topological order. Serial phase ordering is deliberate; Phase 4 cannot precede
Phase 2 authority/model or Phase 3 transport. T015 requires all internal tasks
and their gates. T018 additionally requires any necessary external-root permission;
T020 additionally requires satisfactory independent convergence. These conditions
are gates, not presumed approvals or cycles. No tasks are parallelizable.

T009 supplies shared restricted transport; T011 consumes and verifies it before
introducing any Ruby requests. T012 only canonicalizes evidence admitted through
that boundary. Scan-local pacing/cooldown stays in T013 and deterministic
candidate scheduling in T014, both before public activation. T018 combines
required dogfood and optional smoke disposition in one release record; T019
consumes that record and judges evidence sufficiency without requiring a separate
smoke task or smoke execution.

**Public activation: T015 only.** Until that commit the released two-source scan
and serializer behavior remain intact. Internal source tests may call Ruby
discovery; no earlier task adds Ruby to scan source pairs. T015 owns scan,
summaries, provenance transfer, human/JSON output, CLI verification and all four
required user-facing documentation files together. No half-coherent public Ruby
state is an allowed stopping point.

## Artifact lifecycle audit and draft checks

- T015: documentation coherence and CHANGELOG Unreleased Added checkpoint.
- T017: final offline integration/regression and actual AC traceability evidence.
- T018: release-validation.md, required authorized real-root human/JSON dogfood,
  unchanged-target evidence and PERFORMED/REDUNDANT/UNAVAILABLE/DEFERRED smoke
  disposition with rationale; separate smoke cannot block convergence. Discovery’s
  historical paths are not authorization.
- T019: independent fresh-context read-only convergence recorded in reviews.md;
  findings are separate from remediation and block completion where material.
- T020: final feature bookkeeping and ROADMAP reconciliation within existing
  lifecycle conventions, with no new radar state or interpreted-Gemfile scope.
- T021: retrospective.md after convergence, including the committed-draft
  experiment; final authorized commit and clean-tree check. No push/tag/release.

Revision self-checks (not independent narrow verification): 21 tasks, seven approved
phases, 52/52 mapped identifiers, acyclic explicit graph, safe stopping condition
for every task, offline correctness, phase-5-only public activation, independently
reviewable shared transport and complete artifact lifecycle. No product or
architecture gap identified by these corrections. The initial independent
task-graph verdict was REVISE; narrow verification is pending. Implementation
remains NOT APPROVED.
