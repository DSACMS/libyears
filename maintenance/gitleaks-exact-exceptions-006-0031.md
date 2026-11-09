# Exact historical GitLeaks exception — 006-0031

Baseline: clean `e7e021d0138acd6f98934455da60eac57eaf28bd`.
The initiating human conditionally authorizes exactly one canonical fingerprint
if independent review establishes documentation/synthetic material, no usable
secret, sufficient exact suppression, no broader suppression or history rewrite,
and continued detection of equivalent new findings elsewhere.

## Finding and independent classification

Canonical `python3 tools/check_gitleaks.py`, GitLeaks 8.30.1, full available-ref
history: exit 1, 315 commits, exactly one finding. Rule: `generic-api-key`.
File: `maintenance/nuget-conventional-comparator/spec.md`, line 35.
Commit: `78e284f10ee10b2049ba30717b6acda0be650354`.
Canonical fingerprint:

```text
78e284f10ee10b2049ba30717b6acda0be650354:maintenance/nuget-conventional-comparator/spec.md:generic-api-key:35
```

The historical line describes rejected XML constructs: “sections, duplicate
sections/keys, computed/environment values or ambiguous case”. It is explanatory
specification prose, with no credential assignment, authentication material or
usable secret. Current prose remains unchanged. Parent repository/history searches
also find related computed/environment wording in the namespace discovery;
that is explanatory prose and creates no additional canonical finding.

Fresh non-author Reviewer A independently reproduced the scan and inspected the
historical file and introducing diff; all six human conditions pass. Parent
validated the classification against the exact historical line and scan. The
existing 006-0019 methodology applies: an exact commit/file/rule/start-line entry,
not a secret digest. Changes in scanner attribution require reassessment, not
broadening. The new entry cannot match a different commit or path.

## Controls and freeze

Disposable local clone, never pushed: append the identical historical prose in a
new file/commit and a different constructed generic API-key-like string. Redacted
reports with no exceptions, prior exceptions, and candidate exceptions contain
5, 3 and 2 findings respectively. Set assertions establish that the two prior
exceptions remove exactly their approved fingerprints, and the new exception
removes exactly the fingerprint above. Both new generic-api-key findings remain.
No real credential is used. Script and redacted reports are retained in the
run's temporary evidence directory outside Git.

Canonical history gate with the candidate ignore: exit 0, zero unsuppressed
findings. Gate unit tests: 4 PASS. `git diff --check`: PASS. Only one fingerprint
is added; scanner config/rules, workflow and historical artifacts are unchanged.
No path/regex/rule suppression, history rewrite or push. Independent final
candidate/control verification and frozen digests are recorded separately in
[gitleaks-exact-exceptions-006-0031-review.md](gitleaks-exact-exceptions-006-0031-review.md).
Phase 2 may begin only after the passing security candidate is committed.
