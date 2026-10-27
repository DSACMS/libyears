# Feature 003 Tasks: Yarn Classic Lock Evidence

## Status

Ready for implementation

Tasks are ordered within the approved implementation phases. Do not mark a task complete until its acceptance criteria and verification pass. Each task is independently reviewable and leaves a coherent repository state.

## Phase 1 — Yarn v1 parser

### T001 — Recognize Yarn Classic v1 lock headers

**Status:** COMPLETE — 5 focused deterministic tests passed; diff reviewed and whitespace checked.

**Outcome:**
A focused parser module recognizes Yarn Classic v1 from its canonical header and classifies explicitly unsupported or safely unclassifiable/contradictory generation evidence, without interpreting lock entries.

**Depends on:**
none.

**Files expected:**
`libyears/yarn.py`; `tests/test_yarn.py`; local parser fixtures under `tests/fixtures/yarn/`.

**Acceptance criteria:**
- Recognition requires the standalone canonical v1 header in the initial comment/header area; leading comments and blank lines are accepted.
- Missing, contradictory, explicitly unsupported, or unclassifiable generation evidence returns `unsupported_lockfile_format`; body syntax never establishes v1.
- Recognition behavior is independently tested for supported, unsupported, and unclassifiable/contradictory generation evidence, including relevant comments and header-area cases.
- The parser remains a focused Yarn Classic v1 parser, with no Yarn execution, network access, or generic YAML framework.

**Verification:**
`python -m unittest tests.test_yarn`

**Regression invariants:**
No implementation or existing ecosystem behavior changes; fixtures and tests are deterministic and offline.

**Suggested commit:**
`feat(yarn): recognize Classic v1 lockfiles`

### T002 — Parse bounded Yarn v1 lock entries

**Status:** COMPLETE — 16 focused deterministic tests passed; diff reviewed and whitespace checked.

**Outcome:**
The parser returns ordered entries with decoded selectors and one usable exact version, preserving distinct entries for later ambiguity checks.

**Depends on:**
T001.

**Files expected:**
`libyears/yarn.py`; `tests/test_yarn.py`; `tests/fixtures/yarn/`.

**Acceptance criteria:**
- Comments, blank lines, supported quoted and unquoted keys, bounded `\\` and `\"` escapes, commas outside quoted/escaped content, and multi-selector entries are handled.
- Each entry requires one concrete exact `version`; other safely bounded entry metadata is ignored as specified by the plan.
- After positive v1 identification, malformed duplicate-key/field structure, dangling escapes, invalid separators, unterminated quotes, and unsafe required structure fail as `invalid_lockfile`.
- Repeated selectors in separate valid entries remain separate; entries are not collapsed into a dictionary.
- Offline fixtures demonstrate supported syntax and malformed cases; no matching or scan orchestration is introduced.

**Verification:**
`python -m unittest tests.test_yarn`

**Regression invariants:**
T001 header classifications remain stable; no semver evaluation or registry behavior is added.

**Suggested commit:**
`feat(yarn): parse bounded Classic v1 entries`

**Phase gate result:** PASS — 16 Yarn tests, 52 existing parser/npm regression tests, and the full 155-test deterministic suite passed; `git diff --check` passed. Phase 2 remains unstarted.

**Phase gate:**
- The independent parser recognizes supported and unsupported generations and emits ordered, structurally validated entries.
- Run `python -m unittest tests.test_yarn` and `git diff --check`.
- Selector matching, source-result model changes, and scan integration remain unstarted.

## Phase 2 — Textual selector evidence

### T003 — Match declarations to decoded Yarn selectors

**Status:** COMPLETE — 10 focused matcher tests and 42 parser/npm tests passed; diff reviewed and whitespace checked.

**Outcome:**
A focused npm evidence matcher maps each declaration to exactly one parsed entry by exact decoded selector text and returns candidate or dependency-level failure results.

**Depends on:**
T002.

**Files expected:**
`libyears/npm.py`; `tests/test_npm.py`.

**Acceptance criteria:**
- Target text is the complete manifest package identity plus `@` plus the original declaration; scoped names stay intact.
- Unscoped, scoped, exact, and ordinary non-exact declarations use textual equality only; no semver matching, selector normalization, or reconciliation occurs.
- Every selector in one multi-selector entry independently maps to that entry; multiple matching entries for the target are ambiguous even when versions agree.
- Zero matches produce `lock_version_missing`; exact literal/version disagreement produces `declaration_lock_conflict`; an unusable single entry or repeated target entries produce `ambiguous_lock_evidence`.
- Unsupported declaration sources remain `unsupported_dependency_source`, preserve the original declaration, and do not match or reach lookup.
- Matching is independently testable using parser results and local fixtures, before scan orchestration.

**Verification:**
`python -m unittest tests.test_yarn tests.test_npm`

**Regression invariants:**
The existing package-lock resolver and registry adapter remain unchanged; package-lock tests continue to pass.

**Suggested commit:**
`feat(npm): match declarations to Yarn selectors`

**Phase gate result:** PASS — 42 parser/npm tests and the full 165-test deterministic suite passed, including existing package-lock and registry regressions; `git diff --check` passed. Phase 3 remains unstarted.

**Phase gate:**
- Parser and matcher jointly cover selector identity, missing evidence, conflicts, and ambiguity with offline tests.
- Run `python -m unittest tests.test_yarn tests.test_npm` and `git diff --check`.
- Shared availability states and runtime Yarn selection remain unstarted.

## Phase 3 — Explicit source-result availability

### T004 — Represent discovery and measurement availability explicitly

**Status:** COMPLETE — 26 focused mixed-scan/metric tests passed; diff reviewed and whitespace checked. Existing shared-model fixtures in `tests/test_pypi.py` and `tests/test_output.py` now supply explicit availability fields. `metric.py` remains unchanged.

**Outcome:**
`SourceResult` represents discovery-unavailable, known-discovery/measurement-unavailable, and measurement-available states without deriving them from source errors.

**Depends on:**
T003.

**Files expected:**
`libyears/model.py`; `libyears/scan.py`; `libyears/metric.py` only if required by the approved narrow summary-construction allowance; `tests/test_mixed_scan.py`; `tests/test_metric.py` only if that input is required.

**Acceptance criteria:**
- The three approved states retain nullable discovered counts and explicit measurement availability; no generic state machine is added.
- Invalid manifest retains unknown npm discovery; known declarations with rejected evidence retain N discovered and null measured/coverage; dependency-level partial measurement retains ordinary M/N coverage.
- In a mixed PyPI success plus rejected npm source, known discoveries and successful measurements remain, repository coverage is null, and successful numeric aggregates are preserved.
- Successful numeric aggregates and empty-total behavior follow the approved summary semantics; metric formulas remain source-agnostic.
- Focused regression tests establish these states before Yarn source selection relies on them.

**Verification:**
`python -m unittest tests.test_mixed_scan tests.test_metric`

**Regression invariants:**
Existing invalid-manifest and package-lock source behavior is preserved; prefer no change to `metric.py` and make no Yarn selection changes here.

**Suggested commit:**
`refactor(scan): model source availability explicitly`

**Phase gate result:** PASS — 26 focused tests and the full 168-test deterministic suite passed, including shared-model, mixed-scan, package-lock, PyPI, snapshot, registry, and output regressions; `git diff --check` passed. Phase 4 / T005 and Yarn integration remain unstarted.

**Phase gate:**
- Existing npm and PyPI scans represent all three states and preserve numeric aggregation.
- Run the focused tests above, `python -m unittest discover -s tests`, and `git diff --check` as the shared model boundary.
- Yarn integration remains unstarted.

## Phase 4 — Single npm evidence selector

### T005 — Centralize internal npm resolution-source selection

**Status:** COMPLETE — 7 direct selector tests and the 46-test focused npm/registry verification passed; diff reviewed and whitespace checked. Yarn dispatch is reserved for T006 and public scans retain the existing package-lock resolver.

**Outcome:**
`npm.resolve_npm_evidence(root, discovery)` becomes the single owner of root lockfile presence checks and dispatches package-lock, conflict, and no-lock behavior.

**Depends on:**
T004.

**Files expected:**
`libyears/npm.py`; `tests/test_npm.py`.

**Acceptance criteria:**
- `npm.resolve_npm_evidence(root, discovery)` checks root package-lock and Yarn lock presence once after successful manifest discovery; invalid manifests stop before lock inspection.
- Package-lock only calls the existing v2/v3 resolver unchanged; neither lock preserves existing missing-evidence behavior.
- Direct selector tests prove both lockfiles produce one internal `conflicting_resolution_sources` result before either is parsed, with known discovery and unavailable measurement.
- The selector exposes a narrow Yarn dispatch boundary that T006 can connect without moving parsing/matching into this task or prematurely claiming Yarn evidence.
- Tests prove existing package-lock v2/v3 and package-lock v1/unknown behavior is unchanged.
- Public scan consumption of the selector begins at T007. T005 does not change `scan.py`, CLI behavior, public source errors, summaries, or output.

**Verification:**
`python -m unittest tests.test_npm tests.test_npm_registry`

**Regression invariants:**
No package-lock reason/output/lookup behavior changes; no npm registry behavior changes; Yarn evidence is not yet activated.

**Suggested commit:**
`refactor(npm): centralize resolution source selection`

**Phase gate result:** PASS — 46 focused npm/registry tests and the full 175-test deterministic suite passed, including package-lock v2/v3, unsupported-version, mixed-scan, and output regressions; `git diff --check` passed. Public Feature 003 activation remains unstarted. Phase 5 / T006 remains unstarted.

**Phase gate:**
- Selector is the sole root lock-presence owner; package-lock and neither-lock paths are regression-tested.
- Run focused tests above, `python -m unittest discover -s tests`, and `git diff --check`.
- Public scan consumption, Yarn CLI behavior, conflict reporting, and summary/output changes remain unstarted.

## Phase 5 — Yarn integration through the selector

### T006 — Connect Yarn parsing and matching behind the selector

**Outcome:**
The npm evidence selector connects the concrete parser and matcher and returns approved candidates, dependency failures, or whole-source failures; scan orchestration does not activate the new path yet.

**Depends on:**
T005.

**Files expected:**
`libyears/npm.py`; `libyears/model.py` only for approved internal evidence/diagnostic metadata; `tests/test_npm.py`.

**Acceptance criteria:**
- The Yarn-only selector branch parses and matches root `yarn.lock`; both-present sources short-circuit regardless of contents; neither-lock and package-lock-only behavior remain intact.
- Source errors distinguish positively identified malformed v1 (`invalid_lockfile`) from unsupported/unclassifiable format (`unsupported_lockfile_format`) and conflict (`conflicting_resolution_sources`).
- Dependency failures include `unsupported_dependency_source`, `lock_version_missing`, `declaration_lock_conflict`, and `ambiguous_lock_evidence`; they preserve declarations and do not call npm lookup.
- Direct selector tests prove unrelated usable declarations yield candidates beside dependency failures and whole-source failures yield no candidates or synthetic dependency rows.
- This task does not wire the new results into repository scans; no public behavior is activated before the complete summary/output contract is ready.

**Verification:**
`python -m unittest tests.test_yarn tests.test_npm`

**Regression invariants:**
No registry URL, TLS/CA, timeout, timestamp, stable-release, or failure semantics change; package-lock-only behavior remains equivalent.

**Suggested commit:**
`feat(npm): use Yarn lock evidence for npm dependencies`

**Phase gate:**
- Selector-level Yarn evidence and all approved source/dependency failure classifications pass deterministic tests.
- Run the focused tests above and `git diff --check`.
- `scan.py` remains unchanged; public scan orchestration, registry lookup through Yarn candidates, summary/output integration, and README migration remain unstarted.

## Phase 6 — Summary, output, and schema integration

### T007 — Activate the complete public Yarn evidence contract

**Outcome:**
This is the first public activation of Feature 003. Repository scans consume `npm.resolve_npm_evidence`; Yarn exact-version evidence, source/dependency failures, count semantics, schema-v3 JSON, human output, and README become coherent together while preserving existing package-lock and PyPI behavior.

**Depends on:**
T006.

**Files expected:**
`libyears/model.py`; `libyears/scan.py`; `libyears/output.py`; `tests/test_mixed_scan.py`; `tests/test_output.py`; `README.md`.

**Acceptance criteria:**
- Measured Yarn dependencies remain ecosystem `npm`, carry `version_source: yarn_lock`, and report `version_evidence.npm.format: yarn_lock_v1` with source `yarn.lock`.
- Unsupported/unclassifiable Yarn and both-lock conflict report the approved null format/source representation; source errors retain only `ecosystem`, `source`, and `reason` in JSON.
- Known discovered counts with rejected whole-source evidence produce null measured count and coverage; mixed repository coverage is null while unaffected measurements and aggregates survive.
- Dependency-level failures retain ordinary M/N coverage; invalid manifest retains existing unknown-count semantics.
- Scan tests prove a Yarn candidate reaches the unchanged npm adapter with the full package identity and locked version, while dependency failures do not call it and source failures preserve successful PyPI results.
- Normal scans expose `conflicting_resolution_sources` when both root lockfiles exist, with the approved null npm measured/coverage and mixed repository coverage semantics.
- Schema remains version 3; package-lock and PyPI JSON representations remain equivalent.
- Human output labels successful Yarn evidence as `yarn.lock`, including npm-only output, and gives concise diagnostics for missing, unsupported-source, ambiguous, malformed-v1, unsupported/unclassifiable-format, and conflicting-lock cases.
- Conflict diagnostics name both paths and state neither supplied evidence; null coverage is displayed as specified. Known parser context is human-only and original declarations remain visible.
- README documents only approved root Yarn Classic v1 static evidence behavior; human output, JSON, and README agree at this boundary.
- No earlier task exposes new selector results through public scans, CLI behavior, source-error output, or summary semantics.

**Verification:**
`python -m unittest tests.test_mixed_scan tests.test_output tests.test_metric`

**Regression invariants:**
Do not patch summary fields in output code; metric arithmetic and existing JSON fields remain unchanged.

**Suggested commit:**
`feat(npm): activate Yarn evidence reporting`

**Phase gate:**
- JSON, human output, and README consistently describe schema-v3 Yarn evidence and source availability.
- Run focused output/mixed/metric tests, `python -m unittest discover -s tests`, and `git diff --check`.
- Deterministic end-to-end regression and release validation remain unstarted.

## Phase 7 — Deterministic end-to-end regression

### T008 — Add end-to-end Yarn and mixed-repository regression fixtures

**Outcome:**
A focused deterministic end-to-end mixed fixture proves the unique full flow from discovery through evidence selection, Yarn parsing/matching, mocked registry lookup, metric and aggregation to JSON and human output.

**Depends on:**
T007.

**Files expected:**
`tests/test_mixed_scan.py`; `tests/test_cli.py` or `tests/test_scan.py` only where needed; bounded fixtures under `tests/fixtures/yarn/`; `CHANGELOG.md` at the phase-boundary documentation checkpoint.

**Acceptance criteria:**
- A new fixture asserts a unique full-flow behavior: root declaration and Yarn selector produce a Yarn-sourced npm measurement, correct evidence metadata, and expected human/JSON output.
- The fixture is mixed or includes a rejected-source case proving source isolation and retained successful aggregates.
- Registry calls are mocked; the test performs no network access and runs no package manager or repository code.
- The fixture adds unique end-to-end behavior beyond T007's focused component and public-contract tests.
- After the T008 phase-boundary full suite passes, update `CHANGELOG.md` once under `Unreleased` using Keep a Changelog categories to describe Yarn Classic v1 exact-version evidence for npm dependencies. Do not add per-task entries.

**Verification:**
`python -m unittest tests.test_mixed_scan`

**Regression invariants:**
Deterministic tests remain offline; no live registry assertion is used as a correctness test. The full suite is run once at the phase boundary.

**Suggested commit:**
`test(yarn): cover end-to-end evidence reporting`

**Phase gate:**
- The feature has unique full-flow regression coverage; after the suite passes, its user-visible capability is recorded in the Unreleased changelog.
- Run `python -m unittest discover -s tests`, then perform the changelog checkpoint and `git diff --check`; do not separately rerun a broad list of modules already covered by the full suite.
- Dogfooding, optional live validation, and convergence remain unstarted.

## Phase 8 — Dogfood, optional live validation, and convergence

### T009 — Dogfood a real Yarn Classic repository read-only

**Outcome:**
A suitable repository from approved discovery is statically confirmed and scanned read-only; human and JSON results and discrepancies are recorded as evidence.

**Depends on:**
T008.

**Files expected:**
`specs/003-yarn-lock-evidence/release-validation.md` (create only when evidence is ready to record).

**Acceptance criteria:**
- Target selection is based on static confirmation of a suitable root manifest and root Yarn Classic lock pairing from the approved discovery set.
- Scanning is read-only; no Yarn/npm execution, package installation, resolver, or repository code execution occurs.
- Human and JSON output are compared; target, environment, discovered/measured counts, coverage, evidence metadata, reasons, and discrepancies are recorded.
- Any discrepancy is reported as a finding; this validation task does not silently modify implementation.

**Verification:**
Run the CLI in human and `--json` modes against the confirmed read-only target; compare the outputs and review the recorded evidence.

**Regression invariants:**
No dependency state is changed and deterministic correctness remains established by T008.

**Suggested commit:**
`docs(yarn): record Classic lock dogfood results`

### T010 — Optional live npm registry smoke validation

**Outcome:**
If approved network policy permits and it adds evidence beyond dogfooding, a separately recorded live lookup confirms Yarn-backed versions use the existing public npm registry path.

**Depends on:**
T008 (optional, independently skippable).

**Files expected:**
`specs/003-yarn-lock-evidence/release-validation.md` if the optional smoke check is performed or if its skipped status must be recorded.

**Acceptance criteria:**
- The check is explicitly optional and separate from deterministic verification.
- It runs no Yarn/npm package manager or installer and relies only on the existing registry adapter behavior.
- It is performed only when network policy permits and it contributes evidence not already established by T009; transient failure is recorded as optional validation status, not a deterministic test failure.
- No implementation or product behavior is changed as part of this check.
- Skipping this task does not block T011 or any required task; record that it was skipped and why in release validation.

**Verification:**
Record the smoke command, target/version, date, and result in release validation when run; otherwise record that it was skipped and why.

**Regression invariants:**
No deterministic test requires network access; no registry behavior changes.

**Suggested commit:**
`docs(yarn): record optional registry smoke result`

### T011 — Complete read-only feature convergence audit

**Outcome:**
A read-only audit checks approved specification, architecture, implementation, tests, documentation, and release evidence for convergence and reports findings without remediation.

**Depends on:**
T009.

**Files expected:**
No files by default; findings may be recorded in `specs/003-yarn-lock-evidence/release-validation.md` only as audit evidence, without changing implementation.

**Acceptance criteria:**
- Audit confirms traceability and behavior for all deterministic acceptance criteria, phase boundaries, stable reasons, schema v3, README behavior, and static execution constraints.
- Audit checks package-lock/PyPI compatibility and confirms optional live validation was kept separate.
- Record whether T010 was completed or skipped, including the skip reason when applicable. Neither outcome is a prerequisite for convergence.
- Include a human-readability review alongside the criterion, regression, and artifact convergence checks.
- Findings are reported read-only; this task does not remediate, re-scope, or silently reopen approved decisions.

**Verification:**
Read-only comparison of approved `spec.md`/`plan.md` with implementation, deterministic test results, README, and available `release-validation.md` evidence.

**Regression invariants:**
No code, tests, schema, or documentation changes are made to resolve findings during the audit.

**Suggested commit:**
No commit unless a review record is explicitly added as audit evidence; any such record uses `docs(yarn): record convergence audit`.

**Phase gate:**
- Deterministic feature behavior and required dogfood evidence are complete; optional live evidence is clearly separated; convergence findings are read-only.
- No further phase begins under this feature plan.

### Post-convergence lifecycle activity (not an implementation task)

After T011 convergence, perform the same fresh-context repository-storytelling retrospective used after Feature 002 and create `specs/003-yarn-lock-evidence/retrospective.md`. Compare Feature 003 storytelling against Feature 002's **MOSTLY** result, specifically evaluating whether `discovery.md` and `reviews.md` preserved the decision journey better. This activity follows convergence and does not block the deterministic implementation DAG or convergence verdict.

## Acceptance Criteria Traceability

| Criterion | Task(s) | Architecture area |
|---|---|---|
| AC-01 | T001, T002, T006 | Yarn v1 recognition/parser; integration |
| AC-02 | T002, T006, T007 | Structural parser behavior; source-result availability; output/schema |
| AC-03 | T001, T002, T006, T007 | Parser; source failures; output/schema |
| AC-04 | T003, T006 | Textual selector evidence; integration |
| AC-05 | T003, T006, T008 | Textual selector evidence; npm lookup; regression |
| AC-06 | T002, T003 | Parser decoding; textual selector evidence |
| AC-07 | T002, T003 | Parser; textual selector evidence |
| AC-08 | T003 | Textual selector evidence |
| AC-09 | T003, T006 | Textual selector evidence; failure isolation |
| AC-10 | T003, T006 | Textual selector evidence; failure isolation |
| AC-11 | T003, T006 | Matcher; dependency failure semantics |
| AC-12 | T002, T003, T006 | Duplicate-preserving parser; ambiguity matching |
| AC-13 | T006, T008 | Yarn integration; mixed regression |
| AC-14 | T005, T006 | npm selector; no-lock behavior |
| AC-15 | T005, T006, T008 | npm evidence selection; package-lock regression |
| AC-16 | T005, T007 | Internal source-selection conflict; public failure semantics and JSON |
| AC-17 | T004, T005, T006, T007 | Source-result availability; selection; summary |
| AC-18 | T004, T007 | Availability and numeric summary behavior |
| AC-19 | T004, T007, T008 | Mixed source availability and regression |
| AC-20 | T003, T006, T007 | Dependency matching and coverage |
| AC-21 | T004, T005, T007 | Invalid manifest availability; selector short-circuit; public behavior |
| AC-22 | T005, T006 | Existing manifest scope and Yarn integration |
| AC-23 | T006, T007, T008 | Evidence selection; schema; human/full flow |
| AC-24 | T001, T006, T007 | Recognition; source error; JSON/human output |
| AC-25 | T001, T002, T006, T007 | Parser failure; source error; JSON/human output |
| AC-26 | T005, T007 | Internal conflict selection; public mixed summary and JSON/human output |
| AC-27 | T004, T006, T007 | Source-result state; failure levels; JSON |
| AC-28 | T007, T008 | Schema v3 compatibility and regression |
| AC-29 | T007, T008 | Human output and full-flow regression |
| AC-30 | T007, T008 | Registry reuse and equality regression |

**Traceability check:** 30 / 30 criteria mapped. No deterministic criterion is mapped only to release validation.

## Dependency Graph

```text
T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009 → T011
                                                    └→ T010 (optional; after T008)
```

T010 is optional and is not on the required path. T011 requires T009, records whether T010 was completed or skipped, and does not depend on either outcome. All required dependencies point forward; no tasks are marked parallelizable because each implementation phase consumes contracts from its predecessor and the approved execution sequence is sequential.

## Safe-Boundary Check

| Task | Tests valid | Public schema/docs coherent | No partial activation contradicts spec |
|---|---|---|---|
| T001 | Yes; recognition-only offline tests | Yes; no public change | Yes; recognition is internal and does not parse entries or wire into scans |
| T002 | Yes; parser tests cover bounded entry behavior | Yes; no public change | Yes; parser remains unintegrated |
| T003 | Yes; matcher tests run against parser output | Yes; no public change | Yes; matching is internal and not selected by scans |
| T004 | Yes; focused availability regressions | Yes; existing public behavior retained | Yes; source states are infrastructure only |
| T005 | Yes; direct selector and package-lock tests | Yes; existing public scans remain unchanged | Yes; selector results remain internal and unconsumed by scans |
| T006 | Yes; parser and npm selector tests | Yes; existing public scans remain unchanged | Yes; no mixed-scan or CLI activation |
| T007 | Yes; mixed/output/metric tests plus phase gate | Yes; schema, human output, and README move together | Yes; complete public activation occurs at this boundary |
| T008 | Yes; unique deterministic mixed full-flow fixture | Yes; changelog records the completed user-visible capability | Yes; only regression evidence and the scheduled changelog are added |
| T009 | Yes; deterministic gate already passed | Yes; release evidence reflects observed outputs | Yes; read-only target use |
| T010 | Yes; optional, independently skippable | Yes; result or skip is recorded separately | Yes; no product behavior change and T011 is not blocked |
| T011 | Yes; audit is read-only | Yes; findings do not alter contract | Yes; records T010 status without depending on it or self-remediating |

**Overall:** Every task leaves deterministic tests valid and avoids a contradictory public state. T005 and T006 keep selector behavior internal. T007 is the first public activation and completes scan, model, summary, output, and README behavior together. T010 may be skipped without blocking T011; the retrospective follows T011.
