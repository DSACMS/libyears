# Post-convergence Windows CI portability maintenance — 005-0021

## Investigation synthesis (before repair)

Classification: **TEST_PORTABILITY_DEFECT**. Contract determination: **A**.
No product or CI configuration defect is established.

Three fresh independent investigators read repository evidence without sibling
conclusions: `/root/investigator_a` (authority), `/root/investigator_b` (failure
chain), `/root/investigator_c` (repair design). All completed before synthesis.
The parent independently inspected the contracts, production reader, composed
tests and workflow, and reproduced the supplied Windows totals by removing only
`os.supports_dir_fd` during discovery and execution: **390 tests, 89 failures,
8 errors, 33 skips**. This is a deterministic capability witness on the local
host, not an actual Windows execution.

Approved plan “Filesystem safety and bounded work” explicitly requires refusal
when flags or directory-relative/no-follow operations are unavailable, forbids
unsafe fallback, and requires no platform-specific substitute. T003 and the
005-0011 independent approval repeat that boundary. README and SPEC already
document capability-based refusal. Equivalent functional scoped operation on
Windows is therefore not required. The Windows CI matrix remains appropriate.

The production capability check returns `invalid_gemfile` before consuming input.
The scoped source correctly returns unknown scope, no rows, no lock processing
or lookup. Scan/output/CLI correctly preserve unavailable summaries, sibling
results and completed-report exit 0. Low-level tests guard real descriptor
access, while composed scan/output/CLI/acceptance tests assume successful real
reads. Their downstream failures, including eight empty-row indexing errors,
are consequences of that test coupling.

Authorized repair: use the existing private reader boundary for test fixture
content, keeping real parsers, association, aggregation, adapters, CLI and output.
Run semantic witnesses on every platform. Keep actual descriptor, containment,
replacement, resource and FIFO witnesses separately capability-dependent; add
portable composed production-refusal coverage. No production fallback, contract
revision, broad platform skip or workflow removal is authorized or needed.

Feature 005 converged on the evidence available at T013. Subsequent Windows CI
exposed this additional test issue; its historical convergence record remains
unchanged and does not imply observed Windows success. Feature 006 and NuGet
discovery remain outside this maintenance event. The ledger remains unchanged;
005-0020 was verified exactly once and 005-0021 is handed off outside Git.

## Candidate repair and verification

Implementation children `/root/repair_source_tests` and
`/root/repair_composed_tests` owned disjoint test files; the parent authored
production capability-composition witnesses and integrated the acceptance index.
All used fresh contexts with no requested model/effort overrides; actual child
telemetry is unavailable. No production file or workflow changed.

The fixture seam snapshots only synthetic inputs before injecting reader results.
It asserts exact root/name access and records requests, leaving the actual
parser/source/association/scan/CLI/output chain in place. Source and association
semantic classes no longer skip wholesale. Group-selection acceptance is split
from the real reader allowlist/integrity witness; all four real FIFO replacement
witnesses remain. Capability refusal is tested for both inputs and every required
flag/dir_fd capability; composed refusal preserves unknown versus known scope,
safe reports, sibling success, no opens/reads/lookups and completed exit 0.

Parent verification, before freezing the candidate for independent review:

| Check | Result |
|---|---|
| Focused Ruby source/scan/CLI/output/acceptance/portability modules | 108 tests, no failures/errors/skips |
| `python -m unittest discover -s tests` | LOCAL PASS: 393 tests, no failures/errors/skips |
| Full discovery/execution with `os.supports_dir_fd=set()` | LOCAL PASS: 393 tests, no failures/errors, 18 genuine filesystem skips |
| `git diff --check` | PASS |

Reproduce the capability witness from the repository root with `python -`:

```python
import os
import unittest
from unittest.mock import patch

with patch.object(os, 'supports_dir_fd', set()):
    suite = unittest.defaultTestLoader.discover('tests')
    result = unittest.TextTestRunner().run(suite)
raise SystemExit(not result.wasSuccessful())
```

The disabled-capability run executes semantic tests rather than concealing them
behind broad skips. The 18 remaining skips are actual reader/descriptor/FIFO and
allowlist witnesses. The normal capable-host run exercises them all. These are
local witnesses, not Windows observations. The unchanged Actions Windows job
discovers all repaired modules with its existing full-suite command on Python
3.11–3.13. No mechanism can run the unpushed candidate there within this run's
no-push boundary. Windows disposition is **EXPECTED PASS**, pending actual CI.

Public documentation already states the runtime capability limitation and is
unchanged. Only the test acceptance index explains the repaired test architecture.
Historical convergence/release/retrospective evidence and all ledger bytes remain
unchanged. Independent post-repair review follows the candidate freeze.

## Independent review and final parent determination

Frozen candidate: `69303171b62dd714ae5cef276687e00beb24ff75`, baseline
`461ea0d8761b0e6d972d4ef0913031a88cf37699`. Three fresh non-author reviewers
used `fork_turns="none"`, with no requested model/effort overrides, after both
implementation children completed. None received sibling conclusions; each
read actual repository authority, implementation and the complete candidate diff.
The parent waited for all three before this final synthesis. Actual child
model/effort/resource telemetry is unavailable.

| Reviewer | Scope | Completeness / verdict | Independent checks |
|---|---|---|---|
| `/root/review_security` | Approved contract, filesystem safety, F1/F2 and precedence | COMPLETE / APPROVE; no material findings | Focused 108, full 393/no skips, unavailable-dir_fd 393/18 skips |
| `/root/review_portability` | Windows-relevant capabilities, test architecture and regression sensitivity | COMPLETE / APPROVE; no material findings | Original 390/89 failures/8 errors/33 skips reproduced; candidate full 393/no skips and absent-required-flags plus unavailable-dir_fd 393/18 skips; in-memory removal of refusal and loss of membership detected by repaired tests |
| `/root/review_compatibility` | CLI/output, cross-platform and ecosystem regressions | COMPLETE / APPROVE; no material findings | Focused 108, full 393/no skips, both unavailable-capability configurations 393/18 skips; 27 forbidden CLI abbreviation combinations rejected and exact separate/equals/repeated controls accepted |

All reviewers passed candidate whitespace checks and made no edits. Their local
capability simulations are not Windows executions. Parent validation reconciled
the actual reader check and safe source mapping with plan/T003 authority; checked
that the fixture boundary returns text rather than parsed populations/reports;
inspected retained F1/F2, no-lookup, source ordering, ordinary-mode and C-01
assertions; and confirmed production/workflow/contracts/historical artifacts and
ledger have no diff against the baseline. No material review finding remains.
The established maintenance finding is the test portability defect repaired by
the frozen candidate; review found no additional defect.

Parent additionally passed full discovery/execution with all three required
safe-open flags disabled and dir_fd unavailable: **393 tests, no failures/errors,
18 actual-filesystem skips**. All parent/reviewer results support **LOCAL PASS**
and **WINDOWS-EXPECTED PASS** only. No Windows execution was observed, no remote
job was dispatched and no push occurred. The unchanged Windows Actions matrix
will exercise the architecture when a later separately authorized push reaches
normal CI. That actual Windows observation is the next maintenance gate.

Final disposition: **COMPLETE / APPROVE**, classification
**TEST_PORTABILITY_DEFECT**; product defect **NO**; CI configuration defect **NO**.
Production Windows scoped reads continue to fail closed when required capabilities
are absent. No weaker filesystem model, Windows substitute, feature-contract
change, release, Feature 006 or NuGet discovery was introduced. Public documents
already state the capability limitation; only test documentation and this new
post-convergence record change. Historical Feature 005 convergence is preserved
as evidence from its original gate, without retroactive Windows-success claims.
The observation ledger remains byte-identical; the current run is handed off
as temporary schema-v1 JSON rather than appended.
