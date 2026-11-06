# Feature 006 post-convergence operational closure

**Operational-smoke loop: COMPLETE.** Published candidate:
`c3ef8e78b14cdf19fbcb66187e9925f0fd06a889`.

This clerical closure records the commissioning human's post-publication hosted
observations and publication confirmation. Hosted logs were supplied by the human,
not independently retrieved in this closure run. Earlier pending/failing states
in the [operational review](operational-smoke-006-0018-review.md) and
[security review](gitleaks-exact-exceptions-006-0019-review.md) remain historical
evidence; this record supersedes their operational gate status only. Feature 006's
historical convergence record and product semantics remain unchanged.

## Pre-push verification and publication

The 006-0019 handoff records final committed-candidate deterministic verification:
**640 PASS, zero skips**, dedicated real NuGet worker witnesses **3 PASS**, and
`git diff --check` **PASS**. The hosted-equivalent canonical GitLeaks 8.30.1
history gate returned **exit 0, zero unsuppressed findings, 259 commits scanned**.
This used actual repository configuration and full available local history;
local and hosted available refs explain differing scan counts, not equivalent
commit counts. These are retained prior-run results, not tests rerun for this
clerical closure.

The commissioning human confirms publication of the exact candidate to both
canonical remotes, `github` and `cms`. Publication preceded the hosted evidence
below. No push is performed by this closure run.

## Actual Windows CI

**ACTUAL WINDOWS CI PASS** on exact commit
`c3ef8e78b14cdf19fbcb66187e9925f0fd06a889`:

- Microsoft Windows Server 2025; image `windows-2025-vs2026`; Python 3.11.
- Dedicated real NuGet worker witnesses: **3 PASS**.
- Full deterministic suite: **640 PASS; 32 expected platform-capability skips**.
- Previously failing
  `test_each_nuget_source_failure_preserves_siblings_in_both_ruby_modes`:
  **PASS on actual Windows**.
- `git diff --check`: **PASS**.

This closes the corrected composed-test's actual Windows evidence gap. It is
distinct from the earlier local capability simulation and establishes only the
runner/interpreter results supplied here, not additional unreported matrix jobs.

## Actual hosted GitLeaks and Tier 2

**ACTUAL HOSTED GITLEAKS PASS** on the same exact published commit:

- Actual GitHub Actions job using `gacts/gitleaks@v1`, GitLeaks **8.30.1**.
- `fetch-depth: 0` / full repository history, repository
  `.github/.gitleaks.toml`, `detect` mode.
- **202 commits**, approximately **2.84 MB** scanned; **no leaks found**;
  job **PASS**.

The two approved exact historical fingerprint exceptions cleared the known
synthetic findings without history rewrite or broader suppression. The earlier
negative controls remain the evidence that new same-file, other-path and
other-rule findings are still detected; the hosted pass does not replace those
controls. **Tier 2 checks were also observed PASS for the published candidate.**

## Preserved opportunities and stop boundary

The OASim repository-root finding remains the already-classified project-root
discovery/listing opportunity in [ROADMAP.md](../ROADMAP.md#3-project-root-discoverylisting).
This closure does not repair or select that product work. No OASim access or
modification is performed.

Deferred, nonblocking CI-maintenance note: the supplied GitHub Actions evidence
included a **Node 20 deprecation warning**. Retain it here in the existing
maintenance record convention for future bounded action/runtime compatibility
review. No failing check is attributed to this warning, no specific action is
inferred as its source, and no action-version maintenance is performed now.

Observation **006-0019** is recorded once from its machine handoff plus authorized
human `/status` enrichment. Runtime provenance/confounding is preserved; the later
account reading **56** supersedes **55**, with continuity readings **54/56** and no
derived credit delta or exact task-billing claim. No observation or handoff is
created for this clerical closure. No product implementation, Feature 007, Java
research, release, history rewrite or push is performed.
