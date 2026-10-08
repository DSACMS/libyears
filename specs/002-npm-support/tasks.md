# Feature 002 Implementation Tasks

**Status:** Ready for implementation
**Specification:** Approved
**Technical plan:** Approved
**Task count:** 17

Tasks follow the approved technical plan while keeping concrete npm evidence
and registry behavior ahead of shared integration contracts. Each completed
task must leave existing Python behavior working and JSON valid under the
currently documented schema. The intentional v3 contract change is atomic
with its tests and public documentation. Automated correctness tests are
offline; release-only network validation is labeled separately.

## Phase 1 — Concrete npm source and lock evidence

### T001 [P] — Parse root npm production dependencies

**Goal:** Add a focused npm source parser for root `package.json` and test its
production dependency scope.

**Depends on:** none

**Expected files:**
- `libyears/npm.py`
- `tests/test_npm.py`

**Acceptance criteria:**
- [x] Root `dependencies` are discovered; names in `optionalDependencies` are excluded, including same-name overrides.
- [x] `devDependencies`, `peerDependencies`, `peerDependenciesMeta`, optional-only entries, workspace children, and other out-of-scope scopes add no discoveries.
- [x] Scoped package names and original manifest declarations are preserved.
- [x] An unparseable or invalid root manifest yields `invalid_manifest` with no synthetic dependency rows.

**Verification:** `python -m unittest tests.test_npm -v`

### T002 — Classify unsupported npm declaration sources

**Goal:** Recognize the specified unsupported npm sources without resolving
them, while retaining them as in-scope unmeasurable declarations.

**Depends on:** T001

**Expected files:**
- `libyears/npm.py`
- `tests/test_npm.py`

**Acceptance criteria:**
- [x] Git/GitHub references, `file:`, `link:`, `workspace:`, remote tarballs, and npm aliases use `unsupported_dependency_source`.
- [x] Each remains discovered and preserves its original declaration.
- [x] Ordinary non-exact declarations can later use exact lock evidence without npm range validation.

**Verification:** `python -m unittest tests.test_npm -v`

**Non-goals:** Complete npm package-spec grammar, npm execution, and semver range evaluation.

### T003 — Resolve package-lock v2 direct versions

**Goal:** Read exact versions for declared direct dependencies from v2 root
installation paths only.

**Depends on:** T002

**Expected files:**
- `libyears/npm.py`
- `tests/test_npm.py`

**Acceptance criteria:**
- [ ] v2 direct and scoped package paths resolve exact versions.
- [ ] Lockfile-only and nested/transitive entries do not affect discovered counts or direct evidence.
- [ ] Missing direct paths use `lock_version_missing`.
- [ ] An exact manifest literal unequal to lock evidence uses `declaration_lock_conflict`.

**Verification:** `python -m unittest tests.test_npm -v`

### T004 — Resolve package-lock v3 direct versions

**Goal:** Apply the same exact root-path rules to v3 lockfiles.

**Depends on:** T003

**Expected files:**
- `libyears/npm.py`
- `tests/test_npm.py`

**Acceptance criteria:**
- [ ] v3 direct and scoped paths resolve exact versions.
- [ ] Lockfile-only and nested/transitive entries remain ignored.
- [ ] Missing paths and exact declaration conflicts use the specified reasons.

**Verification:** `python -m unittest tests.test_npm -v`

### T005 — Classify unsupported and malformed lockfiles

**Goal:** Fail closed for unsupported lockfile versions and malformed required
v2/v3 data while retaining known manifest discoveries.

**Depends on:** T003, T004

**Expected files:**
- `libyears/npm.py`
- `tests/test_npm.py`

**Acceptance criteria:**
- [ ] Lockfile v1 and unknown versions use `unsupported_lockfile_version` and provide no registry candidates.
- [ ] Missing lockfile/direct paths use `lock_version_missing`.
- [ ] Malformed required supported v2/v3 structure/data marks each affected known direct dependency `invalid_lockfile` and retains discovered counts.
- [ ] No npm command is invoked to parse, convert, or upgrade lockfiles.

**Verification:** `python -m unittest tests.test_npm -v`

**Non-goals:** Lockfile v1 parsing, workspaces, and transitive resolution.

## Phase 2 — Registry behavior and narrow transport reuse

### T006 [P] — Extract verified HTTP/TLS transport for PyPI

**Goal:** Extract only reusable verified JSON-over-HTTPS transport behavior
from PyPI, preserving its current registry semantics.

**Depends on:** none

**Expected files:**
- `libyears/registry.py`
- `libyears/pypi.py`
- `tests/test_pypi.py`

**Acceptance criteria:**
- [ ] PyPI retains HTTPS, positive finite timeout, User-Agent, verified TLS, current CA-bundle precedence, and current error classification/diagnostics.
- [ ] PyPI release ordering, yanked handling, timestamp canonicalization, prerelease behavior, and lookup results remain equivalent.
- [ ] The transport boundary is mockable and contains no ecosystem discovery or adapter registration framework.

**Verification:** `python -m unittest tests.test_pypi -v`

**Non-goals:** Changes to TLS policy, PyPI eligibility, scan orchestration, or report models.

### T007 — Read exact npm versions and publication timestamps

**Goal:** Implement public npm registry lookup for an exact used version and
identify stable candidates by npm publication metadata.

**Depends on:** T005, T006

**Expected files:**
- `libyears/npm.py`
- `tests/test_npm_registry.py`

**Acceptance criteria:**
- [ ] Only the public npm registry is queried; exact used-version existence comes from `versions` and release time from its `time` entry.
- [ ] Package/version/timestamp misses use existing reason identifiers; malformed required response data uses `invalid_registry_response`; transport failure uses `registry_error`.
- [ ] Publication timestamps, not lexical version order, select the newest eligible release; deprecated available versions remain eligible.
- [ ] Scoped package lookup encodes the registry URL path while preserving displayed package identity.
- [ ] For equal greatest timestamps, `dist-tags.latest` wins only if tied; otherwise deterministic lexical fallback chooses the reported version.

**Verification:** `python -m unittest tests.test_npm_registry -v`

**Non-goals:** Private registries, authentication, npm CLI/client libraries, or version inference from package modified/created timestamps.

### T008 — Enforce conservative npm stable-version eligibility

**Goal:** Restrict latest-stable candidates to confidently classified
concrete versions and verify metric behavior for npm releases.

**Depends on:** T007

**Expected files:**
- `libyears/npm.py`
- `tests/test_npm_registry.py`
- `tests/test_metric.py` (only if a focused metric assertion belongs there)

**Acceptance criteria:**
- [ ] Canonical three-component stable versions, optionally with valid build metadata, are eligible.
- [ ] Valid prereleases are excluded even when published after stable releases.
- [ ] Malformed, prefixed, unsupported, and unclassifiable versions are excluded; no eligible stable version yields `no_stable_release`.
- [ ] Exact used-version lookup can measure a prerelease used version.
- [ ] When used version equals latest stable, the result is exactly `0.0` libyears.

**Verification:** `python -m unittest tests.test_npm_registry tests.test_metric -v`

**Non-goals:** npm semver range evaluation or lexical/version-number latest selection.

### T009 — Verify PyPI and npm share secure transport settings

**Goal:** Add adapter-level checks that the concrete npm adapter uses the
same verified transport guarantees already preserved for PyPI.

**Depends on:** T007, T008

**Expected files:**
- `tests/test_pypi.py`
- `tests/test_npm_registry.py`
- `libyears/cli.py` (only if needed to pass the existing CA/timeout options)

**Acceptance criteria:**
- [ ] Both adapters use HTTPS, a common finite timeout, User-Agent, and selected verified context.
- [ ] Shared transport failure categories remain stable, and TLS diagnostics remain human-only.
- [ ] Certificate and hostname verification stay enabled.

**Verification:** `python -m unittest tests.test_pypi tests.test_npm_registry tests.test_cli -v`

## Phase 3 — Minimum shared boundary and mixed integration

### T010 — Add minimum shared source and registry contracts

**Goal:** After concrete PyPI and npm source/registry behavior exists, add
only the shared candidate/result and registry-result contracts required to
connect these two known ecosystems.

**Depends on:** T008, T009

**Expected files:**
- `libyears/model.py`
- `libyears/pypi.py`
- `libyears/npm.py`
- focused tests in `tests/test_pypi.py` and `tests/test_npm_registry.py`

**Acceptance criteria:**
- [ ] The concrete PyPI and npm adapters satisfy one narrow common lookup result/failure contract.
- [ ] The concrete Python and npm sources can express candidates, dependency-level unmeasurables, source errors, and source evidence.
- [ ] No dynamic registration, plugin framework, package graph abstraction, or generic resolver is introduced.
- [ ] Existing Python dependency/result semantics remain unchanged and PyPI tests pass.

**Verification:** `python -m unittest tests.test_pypi tests.test_npm tests.test_npm_registry -v`

### T011 — Orchestrate explicit PyPI and npm scans

**Goal:** Connect the two concrete source/adapter pairs in repository scanning
with package-level and ecosystem-level failure isolation.

**Depends on:** T010

**Expected files:**
- `libyears/scan.py`
- `libyears/model.py`
- `tests/test_mixed_scan.py`

**Acceptance criteria:**
- [ ] Python-only, npm-only, and mixed scans discover and measure independently.
- [ ] A registry failure in one ecosystem does not discard successful measurements from another.
- [ ] `invalid_manifest` is a source error with no synthetic dependencies; `invalid_lockfile` remains dependency-level and retains known discoveries.
- [ ] Existing PyPI exact requirement and resolved-snapshot behavior remains unchanged.
- [ ] This task exercises mixed reports internally; it does not switch the CLI's public output path to mixed reports before the atomic schema-v3 migration.
- [ ] Existing CLI behavior and JSON serialization remain valid under the currently documented schema.

**Verification:** `python -m unittest tests.test_mixed_scan tests.test_scan tests.test_cli -v`

### T012 — Calculate repository and per-ecosystem summaries

**Goal:** Use the existing `calculate_summary` arithmetic for repository-wide
and per-ecosystem statistics, including unknown discovery denominators.

**Depends on:** T011

**Expected files:**
- `libyears/model.py`
- `libyears/metric.py`
- `libyears/scan.py`
- `tests/test_mixed_scan.py`

**Acceptance criteria:**
- [ ] Repository and per-ecosystem counts, coverage, total, mean, median, and max handle known, zero, and unknown discovery correctly.
- [ ] The specified PyPI `2/1` value `1.0` plus npm `3/2` values `2.0`, `4.0` yields repository discovered `5`, measured `3`, coverage `0.6`, total `7.0`, mean `7/3`, median `2.0`, max `4.0`; per-ecosystem values use only that ecosystem's measurements.
- [ ] Failed discovery makes that ecosystem's summary fields and repository discovered count/coverage null while retaining successful measured counts and aggregate values.
- [ ] Empty and zero-measurement ecosystem cases follow the approved summary rules.

**Verification:** `python -m unittest tests.test_mixed_scan tests.test_metric -v`

## Phase 4 — Mixed output and atomic schema/documentation migration

### T013 — Expose mixed output and migrate schema/documentation atomically

**Goal:** Make the intentional v2-to-v3 contract change in one coherent
boundary, including implementation, schema tests, and public documentation.

**Depends on:** T012

**Expected files:**
- `libyears/output.py`
- `libyears/cli.py` (only if needed to activate the integrated mixed scan)
- `tests/test_output.py`
- `tests/test_mixed_scan.py`
- `tests/test_cli.py`
- `README.md`
- `SPEC.md`
- `AGENTS.md` (only ecosystem/public-contract statements affected by v3)

**Acceptance criteria:**
- [ ] Implementation emits schema v3 with ecosystem-keyed evidence, repository and `by_ecosystem` summaries, and top-level `source_errors`.
- [ ] Mixed human output identifies ecosystems, shows repository/per-ecosystem coverage and aggregates, retains compact single-ecosystem output, and explains `invalid_manifest` while preserving successful PyPI results.
- [ ] Measurable and unmeasurable rows carry ecosystem; measured rows carry `version_source`, including npm `package_lock`; source errors remain distinct from dependency failures.
- [ ] PyPI-only, npm-only, mixed, and source-failure JSON tests assert the specified v3 structures; JSON parses successfully.
- [ ] README, SPEC, and applicable AGENTS public-contract instructions describe npm scope and schema v3 at the same task boundary.
- [ ] PyPI-only and mixed JSON do not contain human-only diagnostics; Python dependency-level values and evidence names remain unchanged.
- [ ] No committed state from this task emits schema v3 while public documentation still describes schema v2.
- [ ] The CLI begins exposing mixed npm/PyPI results at this same boundary, so no preceding task emits mixed user-facing results through the PyPI-only v2 representation.

**Verification:** `python -m unittest tests.test_output tests.test_mixed_scan tests.test_cli -v`; then review README/SPEC/AGENTS schema statements against emitted v3 and mixed human examples.

**Non-goals:** Changing metric semantics, adding other ecosystems, or combining documentation changes unrelated to the v3/public npm contract.

### T014 — Add deterministic end-to-end mixed fixtures

**Goal:** Verify both ordinary mixed output and malformed npm manifest
failure end to end using local evidence and mocked registry metadata.

**Depends on:** T013

**Expected files:**
- `tests/test_mixed_scan.py`
- `tests/fixtures/` (only if fixture files improve clarity)

**Acceptance criteria:**
- [ ] An offline mixed fixture crosses requirements/manifest discovery, Python snapshot and npm lock evidence, mocked registries, metric calculation, repository/per-ecosystem summaries, JSON v3, and human output.
- [ ] A separate explicit malformed-manifest mixed case has valid Python requirements/evidence and mocked valid PyPI metadata; npm discovery returns `invalid_manifest` with no synthetic npm rows.
- [ ] In that malformed-manifest case, the valid PyPI measurement survives, `source_errors` contains the npm `package.json` failure, npm coverage is null, repository coverage is null, and valid PyPI aggregate values remain reported.
- [ ] Both JSON v3 and human output assert that malformed-manifest state.
- [ ] Tests require no network, npm/Node execution, package installation, or repository-code execution.
- [ ] The complete deterministic unittest suite passes before release validation; existing PyPI behavior, snapshot semantics, TLS/CA behavior, valid JSON, and no-install/no-resolution invariants remain intact.

**Verification:** `python -m unittest discover -s tests -v`

## Phase 5 — Release validation and convergence

### T015 — Dogfood a real local npm repository

**Goal:** Before release, scan and review at least one real local npm
repository and record observed results and discrepancies.

**Depends on:** T014

**Expected files:**
- Release validation record or issue/release notes designated by the project

**Acceptance criteria:**
- [ ] At least one real local npm repository with `package.json` and supported lock evidence is scanned without npm/Node execution, installation, or repository-code execution.
- [ ] Record the repository and environment, discovered/measured counts, coverage, measured results, and unmeasurable reasons; review discrepancies.
- [ ] Discrepancies are reported against the approved spec and plan; dogfooding does not silently change product semantics.
- [ ] This is release validation, not a deterministic automated acceptance test.

**Verification:** Manually run `python -m libyears PATH --json` and `python -m libyears PATH` against the selected local repository; retain the environment and findings in the release validation record.

### T016 — Optionally run live npm registry smoke validation

**Goal:** Provide a separate, explicitly optional and non-deterministic live
registry check after local repository dogfooding.

**Depends on:** T015

**Expected files:**
- Existing CI configuration, if a dedicated optional smoke job is added
- Release validation record or issue/release notes designated by the project

**Acceptance criteria:**
- [ ] If run, validation uses a dedicated optional CI smoke job or an equivalent documented live command against the public npm registry; it is separate from offline unit correctness.
- [ ] Record pass/fail, date, environment, command/job, and registry/network outcome.
- [ ] A network failure alone is not reported as a deterministic unit-test failure and does not make ordinary CI network-dependent.

**Verification:** Optionally run the dedicated smoke job or documented live command; record its result and environment. Skip without affecting deterministic test status when not scheduled or network is unavailable.

**Non-goals:** Making ordinary CI depend on network, private-registry access, or adding third-party runtime dependencies.

### T017 — Read-only spec-conformance convergence audit

**Goal:** Compare the approved feature spec and technical plan with the final
implementation, tests, README, and SPEC, reporting deviations without edits.

**Depends on:** T014, T015, T016

**Expected files:** none (read-only)

**Acceptance criteria:**
- [ ] Audit covers `spec.md`, `plan.md`, implementation, tests, README, and SPEC documentation.
- [ ] Deviations, unresolved issues, or confirmation of no deviation are reported to the release owner.
- [ ] No code, test, or documentation files are modified by this audit.

**Verification:** Read-only comparison against all formal acceptance criteria and approved plan; no modifying commands.

## Traceability Matrix

| Formal acceptance criterion in `spec.md` | Task IDs |
|---|---|
| Root production dependencies; optional exclusion; dev/peer exclusion | T001 |
| Lockfile v2 exact direct resolution | T003 |
| Lockfile v3 exact direct resolution | T004 |
| v1/unknown unsupported lock versions | T005 |
| Missing direct lock path uses `lock_version_missing` | T003, T004, T005 |
| Malformed supported lockfile uses `invalid_lockfile`, retains discoveries and other ecosystem measurements | T005, T011, T014 |
| Invalid manifest source failure, no synthetic rows, unknown npm fields, PyPI survives | T001, T010, T011, T012, T013, T014 |
| Mixed invalid-manifest repository null discovery/coverage and retained valid measurements | T011, T012, T014 |
| Human report for invalid npm manifest | T013, T014 |
| Schema source errors vs dependency lock failures | T013, T014 |
| Exact manifest/lock mismatch uses `declaration_lock_conflict` | T003, T004 |
| Non-exact declaration uses lock without npm range validation | T002, T003, T004 |
| Lockfile-only packages do not affect discovered counts | T003, T004 |
| Unsupported sources retained as discovered and preserve declaration | T002 |
| Scoped identity preserved through matching, registry, human, JSON | T001, T003, T004, T007, T013, T014 |
| Publication times determine release age; later prerelease excluded | T007, T008 |
| Unclassifiable concrete version excluded; empty eligible set is `no_stable_release` | T008 |
| Same used/latest version yields exactly `0.0` | T008 |
| Mixed fixture repository-wide statistics | T012, T014 |
| Mixed fixture per-ecosystem statistics | T012, T014 |
| Specified PyPI `2/1` plus npm `3/2` aggregate values | T012 |
| PyPI-only, npm-only, mixed schema-v3 JSON structures | T013, T014 |
| Ecosystem on all rows and `version_source` on measured rows | T013, T014 |
| One registry ecosystem failure does not discard another | T011, T014 |
| Existing PyPI dependency-level results equivalent under schema v3 | T006, T009, T010, T014 |
| No npm/Node, install, or repository-code execution | T005, T014, T015 |

## Regression Invariants

- Existing PyPI tests and Python dependency-level metric results remain green/equivalent throughout implementation.
- `requirements_exact`, `resolved_snapshot`, PyPI registry behavior, and TLS/CA behavior remain unchanged.
- TLS certificate and hostname verification stay enabled; CA source precedence is preserved.
- No package-manager invocation, dependency installation, environment resolution, or repository code execution is introduced.
- Before T013, the CLI remains on its documented v2/PyPI-only output path; T013 activates mixed output and changes implementation, tests, and public documentation to v3 atomically.
- At every task boundary after T013, schema v3 remains valid and documented.
- Metric arithmetic stays centralized in `metric.py`; unmeasurable dependencies remain excluded from numeric aggregates.
- Automated correctness tests remain deterministic and offline; dogfooding and optional live smoke validation are separate release checks.
