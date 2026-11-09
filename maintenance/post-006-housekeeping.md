# Bounded post-Feature-006 housekeeping

Run **006-0035**, 2026-11-09. One sweep of four commissioned items; Feature 007
and Java remain **NOT STARTED**. This record supplements the
[methodology handoff](../specs/006-nuget-selected-evidence/methodology-handoff.md),
without reopening product semantics or documentation architecture.

## Boundary and observation continuity

Starting local HEAD and both `github` and `cms` remote `main` refs were verified
read-only at **36d7f596c8ccb43038ea513874e43c1845b5dd37**; working tree clean.
This confirms publication, not its actor or time. No push in this sweep.

006-0034 was appended exactly once from its explicitly identified external JSON
handoff, preserving prior ledger bytes and runtime notes/unknown confounding.
Human-supplied enrichment: session 01a1c21d-b40b-73a0-823c-7f3b2e9b23ac,
GPT-6.1-Sol/openai/medium, agent 0.160.0, reported runtime 605 seconds,
credits_after 98. credits_before remains blank: continuity was not confirmed,
and the last ledger reading (92, run0032) precedes substantive run0033.
No missing0033 row, runtime or credit delta was reconstructed. Ledger now has
52 rows, 44 columns and unique IDs. Current0035 is a separate external handoff,
not a ledger append; current runtime/account telemetry remains unobserved.

## 1. Test output — FIXED

Exactly three calls in [test_cli.py](../tests/test_cli.py) emitted incidental
stdout: `test_ca_bundle_is_threaded_to_scan`, `test_explicit_path` and
`test_resolved_snapshot_measurement_gap_is_success`. Focused reproduction showed
two empty reports and the confusing `Measured: 0 / 1 dependencies` / `Coverage:
0.0%` fixture report. These tests check routing/status, not real-target results.
No additional uncaptured CLI stderr path was established. Dedicated CLI/output
tests already assert the 0/1 human wording.

Three local `redirect_stdout(StringIO)` captures retain status/routing assertions.
Status failures include the buffer as the assertion message; stderr stays visible.
No global buffering, harness redesign or production CLI change. Reviewer A's three
deliberately failing-status probes retained each report in failure diagnostics
without stdout leakage. Existing formatter assertions remain unchanged.

Focused CLI/output: **59 PASS**. Ordinary `python3 -m unittest discover -s tests`:
**783 tests in 15.807s, OK, one expected case-alias skip**. Captured full-suite
stdout is **empty**; neither stream contains `Measured:`, `Coverage:`, `Total:`
or `No libyears` report text. Normal unittest progress/result remains on stderr.
This is fixture provenance hygiene, not an OASim measurement correction.

## 2. Actions warnings — FIXED owned uses; UPSTREAM / MONITOR managed Pages

| Use | Ownership and disposition |
| --- | --- |
| Tier2 checkout@v4 | Repository-owned; pin supported v7.0.1, matching existing Python CI |
| Tier2 setup-node@v4 | Repository-owned; pin supported v7.1.0; retain requested Node22 and disable automatic package-manager caching |
| Secrets checkout@v3 | Same action-runtime item; pin v7.0.1, retain fetch-depth:0 and every scanner/configuration/security input |
| Python CI checkout/setup-python | Already pinned current Node24 actions; no change |
| Pages deploy-pages@v5 punycode | Historical successful-deploy warning inside upstream action; monitor, no repository deploy-pages workflow to patch |
| Pages upload-artifact@v4 runtime warning | Newly observed within the same warning investigation; GitHub dynamic managed build, monitor upstream rather than invent a repository Pages workflow |

Exact new pins: checkout `3d3c42e5aac5ba805825da76410c181273ba90b1`,
setup-node `949feb2413d6458794dcd2491c4babbbce0c15c1`. Official
[checkout release](https://github.com/actions/checkout/releases/tag/v7.0.1),
[setup-node release](https://github.com/actions/setup-node/releases/tag/v7.1.0)
and their exact action manifests declare Node24. The
[Node20 transition](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/)
makes supported action runtime maintenance appropriate; changing the installed
Node22 used by repolinter would not fix action runtime declarations.

[Checkout compatibility](https://github.com/actions/checkout/blob/v7.0.1/README.md)
requires runner >=2.327.1; hosted ubuntu-latest is suitable. Credential storage
moved under RUNNER_TEMP; privileged fork-checkout guards do not affect these
push/pull_request triggers. No unsafe override was added. Setup-node's
[migration notes](https://github.com/actions/setup-node/blob/v7.1.0/README.md)
describe ESM, automatic caching and removed dummy authentication fallback.
These workflows use no registry authentication; explicit caching=false preserves
uncached tooling. Full pins strengthen reproducibility over moving major tags.
Permissions, triggers, runner, repolinter0.12.0 and scanner remain unchanged.
No exploit or deployment failure is inferred from a deprecation warning.

Latest observed [deploy-pages v5.0.1](https://github.com/actions/deploy-pages/releases/tag/v5.0.1)
already uses Node24; release notes describe polling/test changes, no punycode fix.
[DEP0040](https://nodejs.org/api/deprecations.html#dep0040-nodepunycode-module)
identifies deprecated built-in API use. Its exact hosted call stack is unknown;
dependency ancestry alone does not prove the warning source. Current dynamic
[Pages run](https://github.com/DSACMS/libyears/actions/runs/42700677422) succeeds.
The build annotation names upload-artifact@v4; deploy has no observed punycode
annotation, which does not prove warning-free logs. No vendoring, patching,
warning suppression or Pages redesign. Reconsider when upstream ships a relevant
fix or an actual deployment failure/owned workflow makes action possible.

Static verification checks exact substitutions against the previously valid
workflows, full SHA pins, indentation and preservation of all other content.
No actionlint/config validator exists in this checkout/environment. Reviewer B
verified exact official release commits/manifests and both executable diffs.
Hosted validation of these **unpublished** edits remains pending; existing green
checks apply only to their exact older candidates.

## 3. Runtime disparity — UNDERSTOOD / DEFERRED optimization

The Windows slowdown is predominantly **inside the offline test step**, not
runner queue/setup. Exact per-test Windows causes remain unproved. Retained
b449c5d testimony reports **751 tests / 159.702s / 51 skips**; public job metadata
independently places the Python3.11 offline step at160s, worker step8s,
checkout6s, setup-python0s. Rounded step times are not unittest's own timer.

Current published36d7f596 metadata further separates those costs:

| Windows Python | Created-to-start interval | Whole job | Offline step | Separate worker step |
| --- | ---: | ---: | ---: | ---: |
| 3.11 | 4s | 184s | 166s | 7s |
| 3.12 | 2s | 188s | 170s | 8s |
| 3.13 | 3s | 130s | 108s | 9s |

Created-to-start intervals are metadata scheduling observations, not an exact
infrastructure cost decomposition. Python setup takes0–1s in those three jobs;
current macOS offline steps are35/44/28s for3.11/3.12/3.13. Hosted machines,
interpreters, native capabilities and test populations differ from local.

Independent current macOS CPython3.11 per-test profiling: **783 tests, 15.813s,
one skip**. Ranked evidence/leads:

1. **Repeated native TLS construction: leading Windows hypothesis.** A narrow
   92-test Ruby instrumentation pass made **771 real ssl.create_default_context
   calls**, totaling0.895s locally despite mocked HTTP. One acceptance test
   accounts for528 calls; lock-permutation scheduling coverage accounts for98.
   This supplies a concrete amplification mechanism. Windows native trust-store
   cost remains unmeasured; it does not establish the reported Ruby30s cause.
2. **Deliberate real-worker witness: demonstrated local cost.** Three real-worker
   tests take5.278s in the profile: suppressed-command negative control5.089s;
   startup and positive blocked/cancellation witnesses about0.094s each.
   The negative control intentionally waits the five-second entry-observation
   bound and must detect an idle worker. It is not an accidental fixed sleep.
   CI repeats these three inside the full suite after the dedicated worker step;
   this repetition is visible and retained, not a160s explanation by itself.
3. **Filesystem/subprocess/native platform and runner load: unresolved contributors.**
   No Windows per-test profile is available. Local module totals: worker5.557s,
   discovery1.217s, Ruby acceptance1.062s, Ruby groups0.495s, Ruby registry0.460s.
   These are local rankings, not a Windows attribution.

Ruby pacing tests use fake clocks; timeout arguments alone do not establish wall
waits. Native FIFO witnesses require capabilities unavailable on Windows and
cannot explain Windows-specific delay. Network responses are mocked; real TLS
setup is distinct from network traffic. Public unauthenticated log download
returned403, so no per-test Windows trace was inspected or invented.

No demonstrated accidental wait justifies changing the harness. Optimization is
**DEFERRED**: all inspected current matrix tests pass, no correctness/deadline
defect is established, and a guessed optimization risks losing useful native
trust/cancellation/refusal evidence. Trigger reconsideration with an exact-candidate
Windows per-test profile plus timed TLS construction/context counts, subprocess
startup and filesystem timings, or repeated durations threatening the20-minute
job budget. Preserve equivalent semantic seams and native witnesses; no removed
tests, matrix changes, shortened refusal assertions or suite repartitioning.

## 4. Hosted evidence — RECONCILED for published boundaries

Public unauthenticated GitHub run/job/step metadata was inspected2026-11-09 with
system curl and normal verified TLS. No credentials/private hosting API access.
Parent independently corroborated the run list and timing arithmetic. Each row
below has all five workflows completed SUCCESS: Python CI, secrets, Tier2,
Push on main (CodeQL), and Pages. Python CI includes nine OS/Python jobs plus
live PyPI smoke; worker/offline/whitespace steps succeeded.

| Exact candidate | Python CI | Secrets / Tier2 / Push / Pages run IDs |
| --- | --- | --- |
| 0eabe303a11a297939b0f8271e47f9e409a4fd49 product | [42693616069](https://github.com/DSACMS/libyears/actions/runs/42693616069) | 42693616154 / 42693615727 / 42693613174 / 42693612083 |
| 0506861761b048e5e5a8d65a75d4c933d124df97 methodology | [42698444280](https://github.com/DSACMS/libyears/actions/runs/42698444280) | 42698443870 / 42698444011 / 42698442611 / 42698441636 |
| 36d7f596c8ccb43038ea513874e43c1845b5dd37 documentation | [42700679868](https://github.com/DSACMS/libyears/actions/runs/42700679868) | 42700680089 / 42700679671 / 42700678929 / 42700677422 |
| b449c5ddbbd2c5c702e03ab112511f89996e0482 prior snapshot | [42675839045](https://github.com/DSACMS/libyears/actions/runs/42675839045) | 42675838691 / 42675838825 / 42675837344 / 42675837018 |
| 72dc9a2 prior population, exact full SHA retained by linked run | [42649479917 attempt2](https://github.com/DSACMS/libyears/actions/runs/42649479917/attempts/2) | 42649479991 / 42649480001 / 42649477837 / 42649476806 |

72dc9a2's initial macOS3.13 job129271620910 had **no runner and zero steps**.
Public annotations explicitly report no hosted runner acquisition and macOS arm64
capacity notices; exact-candidate replacement job129282705782 succeeded. This is
infrastructure/capacity failure, not candidate execution failure. Nonblocking
runtime warnings are separate again. **No genuine candidate failure was found in
the inspected recent candidates.** Historical failed candidates remain historical;
this is no claim to audit every run. No reruns or idle capacity waits occurred.

New housekeeping hosted evidence is **INCOMPLETE until publication/execution**;
that expected future witness is not an unresolved published-product defect.
Local convergence/publication authorization and hosted evidence remain distinct.

## Review, verification and stopping point

Fresh non-author A reviewed output isolation; B reviewed upstream compatibility
and executable workflow diffs; C profiled runtime/portability; D reconciled hosted
evidence. Parent validates findings against code/raw metadata, not majority votes.
Frozen test digest63692c8b…; Tier2 digest93a700d9…; secrets digestf59c21d1… .
A/B executable reviews completed **APPROVE**, no blocking findings. C/D both
completed **REVISE** on the same factual timing error: Windows3.11 setup-python
was1s, not0s. Parent checked the raw timestamps and corrected the prose to0–1s;
the timing table and runtime hypotheses were already accurate. This is one
overlapping finding, not two candidate defects. Fresh focused closure follows
the correction; no executable change was needed.

Fresh C/D reverification of corrected digest389f4719… and unchanged roadmap
digest319c03a6… completed **APPROVE**. No remaining material finding; their
approval covers runtime claims and hosted taxonomy respectively, not new hosted
execution of the local housekeeping commits.

Additional verification: capability-disabled suite **783 tests,13.966s,57 expected
native skips, OK**; standalone real-worker **3 PASS,5.256s**. This capture-only
change requires no filesystem correction; those runs retain the existing portability
witnesses and are not actual Windows evidence. No OASim execution/access, package
manager invocation, product/schema/metric/NuGet semantics or Feature007 changes.

Before the documentation commit: whitespace PASS; changed-document local links
and anchors **91 PASS**; ledger shape/uniqueness/prior-byte checks PASS. Canonical
configured GitLeaks8.30.1 history **332 commits PASS, zero unsuppressed findings**;
new maintenance prose also passed stdin scanning. Final committed-history result,
commit identities, clean-tree check and current observation handoff are reported
at run closure, without inventing hosted results for this candidate.

Exact next human gate: accept/revise this bounded housekeeping candidate and
separately authorize publication; collect actual hosted results for its changed
tests/workflows asynchronously after publication. Separately select and authorize
Feature007's bounded next stage. The deferred profiling and upstream warnings do
not block safely beginning separately authorized feature work.
