# NuGet root recognition review history

Run `006-0020`. Review candidates are frozen by SHA-256 before commissioning;
subsequent dispositions belong here, without approval-only candidate edits.
Fresh non-author reviewers inspect governing authority and frozen evidence
directly. No publication or OASim execution/modification is authorized.

## Specification gate

Discovery SHA256 `d38970805a963c5c1b3764212730c5c1bccd1e256a86a3fcc398cbcfc50add2a`;
spec SHA256 `662700c4975449117e9a04ac7fc7144e48c983dbbc3587220b77eb51454cc753`.
Fresh `/root/spec_review`, fork_turns=none without overrides, independently
verified both and inspected authority, closed operational history and current
CLI/scan/output seams. COMPLETE / APPROVE, no material findings; R1–R6 testable.
Parent validates separation of candidate recognition from SourceResult and JSON,
bounded incomplete states, exact explicit selection and platform refusal.
Specification APPROVED. Private full report: `spec-review.md` in the run evidence
directory. No implementation or passed acceptance is implied by this gate.

## Architecture gate

Plan SHA256 `33f6be47a2902c1f45f90159bfd80ecb1f3bb2c6b4bc860cb92a119eb32698b4`.
Fresh `/root/plan_review`, fork_turns=none without overrides, verified spec/plan
digests and directly inspected relevant source and portability history.
COMPLETE / APPROVE, no material findings; R1–R6 architectural obligations covered.
Parent validates finite descriptor traversal, independent human evidence and
zero JSON/measurement changes. Plan APPROVED; task decomposition may proceed.

## Task-graph gate

Tasks SHA256 `7a3a51a9ca43c3ec0c2fce6f49aff7275ecabf54450149febaf41ab0ff9f5839`.
Fresh `/root/task_review`, fork_turns=none without overrides, verified all three
contract digests and inspected canonical workflow and boundaries. COMPLETE /
APPROVE, no material findings. Parent reconciles sequential C1→C2→C3→K1,
R1–R6 ownership, accompanying tests, freeze/review and separate task commits.
Task graph APPROVED; execution proceeds under the commissioning prompt.
These three reviews establish no actual Windows/hosted or acceptance results.
Actual child configuration/resource telemetry is unavailable; no child ledger rows.

## C1 execution

Typed recognition and metadata-only descriptor traversal implemented in
`libyears/nuget_discovery.py`; scan/model/adapters remain unchanged. Fourteen
focused tests PASS, including production cap/cap+1 values, global budgets,
exact depth/exclusions, malformed/unreadable project content without reads,
link/FIFO/reparse exclusion, replacement/mutation, handle/iterator cleanup and
unskipped capability refusal. Author verification, not independent convergence.
`git diff --check` PASS. C1 COMPLETE; C2 dependency-ready.

## C2 execution

CLI invokes recognition only for unselected human directory reports. Optional
human evidence is separate from measurement sources and JSON. Output lists
escaped candidate paths or explicit uncertainty, no NuGet measurement, parent/
filename selection and remaining lock/provenance eligibility requirements.
README/SPEC/AGENTS/CHANGELOG and the existing ROADMAP opportunity are reconciled;
Feature 006 artifacts and historical operational closure remain unchanged.

Focused CLI/output/mixed/recognition regressions: **115 PASS**. Full deterministic
suite: **663 PASS**, zero skips. Full discovery with dir_fd disabled beforehand:
**663 PASS / 44 genuine filesystem skips**. This is local simulation, not Windows.
After a behavior-equivalent explicit-control-flow readability edit, focused
discovery/recognition is rerun; final committed-candidate checks follow C3.
Tests inject recognition for semantic composition, including three real measurable
sibling sources with dir_fd disabled and exact counts/rows; JSON bytes, empty
human output and explicit/direct-file bypass remain covered. `git diff --check`
PASS. C2 COMPLETE, pending independent convergence; C3 dependency-ready.
