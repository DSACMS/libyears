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
