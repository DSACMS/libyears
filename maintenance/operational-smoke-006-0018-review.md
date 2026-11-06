# Independent review and parent disposition — 006-0018

Subsequent disposition: the [post-publication closure](operational-smoke-closure.md)
records actual Windows, hosted GitLeaks and Tier 2 PASS for exact published commit
`c3ef8e78b14cdf19fbcb66187e9925f0fd06a889`; operational-smoke loop **COMPLETE**.
The review and pending gates below describe the historical 006-0018 state.

Baseline: `db24c03a03085d684b207d9f9a1b57de4d877f10`, initially clean.
Eight substantive files were frozen before review by SHA256 in
`/tmp/libyears-observations/006-0018/freeze.json`: README.md, ROADMAP.md,
SDD_WORKFLOW.md, tests/test_mixed_scan.py, tools/check_gitleaks.py,
tests/test_gitleaks_gate.py, maintenance/pre-push-checks.md and the
[classification/evidence record](operational-smoke-006-0018.md).
All four reviewers independently verified all eight hashes. No substantive
candidate changes followed review commissioning. This disposition is subsequent
review evidence, not a change to the frozen classifications or repairs.

Each reviewer was a fresh non-author context (`fork_turns=none`, no requested
model/effort overrides), with bounded read-only scope, actual authority/evidence
locations and hard stops supplied. Current sibling conclusions were withheld
until their independent reports completed. Actual child configuration/resource
telemetry is unavailable; children receive no observation-ledger rows.

| Reviewer | Assigned coverage | Completion / verdict | Independent evidence |
|---|---|---|---|
| A `/root/review_a` | A product/activation contract, ordinary/mixed behavior, README and ROADMAP | COMPLETE / APPROVE; no material findings | Ten known target project filenames and absent root source markers independently checked; NuGet CLI 13 PASS; selected-project observation audited against staging, not independently replayed |
| B `/root/review_b` | B causal reproduction, Windows/test portability, approved safety, fixture repair and regression sensitivity | COMPLETE / APPROVE; no material findings | In-memory baseline with dir_fd absent: exactly 11 failures/zero errors; focused 50 PASS; full 640 PASS; capability-disabled full 640 PASS/32 skips; common-mode Ruby-loss mutation: 22 expected failures/zero errors |
| C `/root/review_c` | C historical provenance, scan scope, exact proposed mechanism/security gate, canonical command and negative controls | COMPLETE / APPROVE for tooling/analysis only; no material findings | Direct historical source review; upstream implementation; gate tests 4 PASS; active history exit1/two; temporary proposal exit0/zero; controls exit1/six -> exit1/four, only old fingerprints removed |
| D `/root/review_d` | Methodology proportionality, authority/optional predecessors, test-pattern evidence, local/hosted claims | COMPLETE / APPROVE; no material findings | Existing workflow/history and all candidate prose audited; retained test logs and exact before/after fingerprint sets independently checked; no platform execution claimed |

Full reports are retained as reviewer-a.md through reviewer-d.md under the private
evidence directory above. C's initial optional report-to-/dev/stdout attempt was
rejected before scanning; subsequent redacted scans completed and supply the
reported evidence. This is not a passed scan or scanner correctness defect.

## Parent reconciliation

The parent read every report and checked underlying obligations rather than
counting verdicts. S1/AC-01/T013 explicitly require NuGet opt-in; AC-28 requires
preserving available siblings, not changing Ruby safe-read availability. The
six-line test diff uses the existing exact-text boundary and retains every
assertion. Production readers, refusal witnesses, workflow/platform coverage,
spec/plan/tasks and historical convergence/closure bytes are unchanged.

Parent focused 44 plus gate 4 PASS; full **640 PASS**, zero skips; full discovery
with dir_fd disabled **640 PASS/32 filesystem skips**. Parent independent mutation
removing Ruby only on NuGet-active results triggers **22 expected failures/zero
errors**. B additionally removes Ruby from baseline and candidate and confirms
the explicit three-row/count assertions still catch common-mode loss. These are
local semantic/capability results; corrected Windows remains UNOBSERVED.

Historical synthetic source and its quotation, actual config, full-history source
semantics and both exact fingerprint sets were directly checked. Active policy
still finds two. The external proposed-ignore experiment and synthetic clone
controls establish conditional behavior only. No active .gitleaksignore,
baseline, allowlist, configuration/workflow change, history rewrite or trust
exception is installed. A supplemental current-tree scan finds zero, explicitly
separate from the history gate's exit1/two.

README corrects the root-only interpretation without ordinary-output changes;
ROADMAP EXPLORE preserves unproven recurring demand and requires future human
selection. Workflow adds one operational evidence distinction and one linked
local checklist; it neither reopens historical K6 nor authorizes publishing or
optional-predecessor expansion. Frozen hashes and whitespace are checked again
before committing. No material review finding requires correction/re-review.

**Bounded local maintenance: COMPLETE / APPROVED. Operational closure: PENDING.**
The exact historical fingerprint acknowledgment still requires **HUMAN
SECURITY-POLICY DECISION**. Future listing implementation still requires **HUMAN
PRODUCT SELECTION**. Publication is separately human-authorized, followed by
actual supported OS/Python, real-worker, live PyPI and hosted GitLeaks checks on
the published candidate. The existing hosted findings remain failures until
observed otherwise. No push, release/tag, Feature 007, OASim execution/modification,
unsafe fallback, broad test refactor or weakened secret scanning occurred.
