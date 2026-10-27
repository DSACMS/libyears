# Feature 003 release validation — T009

- **Date:** 2026-10-27 (UTC).
- **Environment:** Darwin arm64, Python 3.11.0; libyears CLI from the local implementation workspace.
- **Target:** `<authorized-checkout>/easi-app` (approved discovery repository).
- **Method:** Read-only inspection of root `package.json` and `yarn.lock`, then `python -m libyears <authorized-checkout>/easi-app` in human and `--json` modes. No repository code, Yarn, npm, Node, package manager, installer, or resolver was run.
- **Preconditions:** Root manifest has 77 production dependencies and no optional-dependency overlap; root lockfile has the canonical `# yarn lockfile v1` header; no root `package-lock.json` exists.
- **Result:** 77 discovered, 77 measured, 100.0% coverage. Cumulative 197.87017578161831 libyears (197.87 human); mean 2.57, median 2.42, maximum 6.35 in human output. No unmeasurable dependencies or source errors; no timestamp anomalies.
- **Evidence:** JSON schema v3 reports npm `declaration_source: package.json`, `snapshot_source: yarn.lock`, and `format: yarn_lock_v1`. All 77 measured dependencies have `version_source: yarn_lock`; their names match the root production scope. Spot checks of `@apollo/client`, `axios`, and `react` confirm exact used versions against their root lock selectors. Normal public npm registry metadata supplied release timestamps and latest stable versions.
- **Human/JSON agreement:** Dependency counts, coverage, and rounded aggregate values agree; human output identifies `yarn.lock` evidence. JSON has no unmeasurable rows or source errors.
- **Network/TLS:** An initial sandboxed run returned registry transport errors because network access was restricted. The authorized live scans succeeded using libyears' normal verified HTTPS transport; TLS verification was not disabled.
- **Target modification:** None by this validation. The root manifest and lockfile SHA-256 hashes were identical before and after scanning.
- **Discrepancies:** None in the successful live validation.
- **T009 acceptance:** COMPLETE. T011 remains unstarted.

## T010 optional live registry smoke

- **Status:** SKIPPED.
- **Reason:** Successful T009 dogfood already exercised the live public npm registry and verified HTTPS path end-to-end across 77 real dependencies. An additional synthetic live smoke would provide no material release evidence.
- **Effect:** Skipping T010 does not affect deterministic correctness or convergence eligibility.

## Final convergence disposition — T011

- **Status:** COMPLETE; final verdict CONVERGED, with 30 / 30 acceptance criteria mapped and satisfied.
- **Disposition:** The initial CONVERGED WITH LOW-SEVERITY FINDINGS verdict identified lost safe malformed-Yarn parser context in human diagnostics. Separate remediation commit `ace9ccf69d259ad6041dd0c19e00bf5df2208309` resolved the finding; narrow independent re-verification confirmed human diagnostic PASS, unchanged stable reason and JSON contract, and no regression concern.
- **Verification:** 187 deterministic tests passing after remediation; architecture conformance and human readability PASS; schema v3 unchanged; package-lock/PyPI/snapshot/TLS regressions PASS.
- **Release evidence:** Existing T009 evidence is sufficient; optional T010 remains intentionally SKIPPED as redundant.
- **Lifecycle:** Post-convergence retrospective PENDING; `retrospective.md` has not been created.
