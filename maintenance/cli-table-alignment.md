# Human dependency-table alignment

Queued maintenance authorized in the Feature 006 post-convergence closure commission,
executed in run006-0017 after independently approved T018 at657e8a9. This is separate
maintenance, not a Feature006 product task, metric change or architecture migration.

## Candidate and verification

All three human table paths (legacy Python, single ecosystem and mixed ecosystems)
now share a small rendered-cell formatter. Widths include headers, names, versions,
formatted two-decimal libyears and optional ecosystem/source cells. Text is left
aligned, numeric values right aligned, with spaces only and no trailing padding.
Ordering, row evidence details, summary/failure sections and JSON serialization
retain their existing behavior. Unmeasurable dependencies remain in their reason
sections without invented versions/ages. No third-party table dependency is added.
CHANGELOG Unreleased Fixed describes the visible alignment improvement.

Four focused regressions cover legacy optional source columns, all four ecosystems,
long names/versions and large/zero values, mixed ecosystem/source columns,
evidence details and unmeasurable-only reports. Initial new fixtures used generic
SourceEvidence for NuGet; that test-setup error was corrected before freeze to use
NuGetSourceEvidence. No product contract changed to accommodate the fixture.

Focused `python -m unittest tests.test_table_output tests.test_output tests.test_nuget_output`:
**50 PASS**. Full `python -m unittest discover -s tests`: **636 PASS**.
`git diff --check` PASS. Parent inspects complete formatter diff; JSON/metric/model/
scan/registry/parser paths are unchanged. Existing output snapshots and broader
suite remain passing; no network, real-root validation or new Windows execution.

Frozen candidate relative657e8a9:

| File | SHA256 |
|---|---|
| libyears/output.py | 549616bafe86dc1b2d13a7ec218165194881e3010fcb53366f558c4a5f841076 |
| tests/test_table_output.py | fe7a8f7f7010d0e610d06514067c7f4613e5f5a937c16a630317eb77d230a224 |
| CHANGELOG.md | 3ed41bd631bfe5b894138e5d9f637d3b0ffb72fe7e16f54f56a6de6c7163b0a6 |

Candidate bytes remain frozen for fresh non-author independent review; disposition
is recorded below after review. Private freeze/report paths are under
`/tmp/libyears-observations/006-0017`. No push is authorized or performed.

## Independent disposition

Fresh non-author `/root/table_review`, fork_turns=none without overrides, directly
inspects authority, complete diff and all three rendering paths. **COMPLETE /
APPROVE; material findings NONE.** It verifies frozen digests before/after, runs
50 focused output tests PASS and38 in-memory baseline comparisons under ordinary
and verbose modes. JSON bytes, human token/detail ordering and source labels match
baseline; text starts/numeric ends align for long and header-dominated values,
all four ecosystems, mixed/source-error, empty and failure-only cases.
Private report: `/tmp/libyears-observations/006-0017/table-review.md`.
Actual child configuration/resource telemetry is unavailable.

Parent validates the complete diff, output branches, report evidence and unchanged
frozen hashes against the explicit grant. Existing null/failure handling remains
separate from measured tables. Full636 and focused50 PASS supply regression
coverage. **Maintenance COMPLETE / APPROVED.** This is local rendering evidence,
not new live or platform validation. No product schema/metric/ecosystem change,
new dependency, push, release or next-feature work occurs.
