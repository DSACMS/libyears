# Implementation plan

Use one explicit `sbom_extended` boolean defaulting False at the internal Maven
supervisor/HTTP and protocol seams, rejecting non-booleans. Centralize the two
fixed attempt/scan profiles in a small function in maven_protocol; no arbitrary
numeric budget framework. Existing default protocol calls still reject sequence301.
Extended protocol permits at most600, and result counters stay sequence-bound.

The supervisor passes a closed `--sbom-extended-budget` startup argument only for
extended SBOM workers. The installed isolated worker validates its argv, uses
matching protocol and HTTP limits, and still rejects arbitrary URLs/operations.
All absolute parent deadlines and process kill/reap paths remain in effect.
No shared-source caller opts in; shared code's default behavior is unchanged.

SbomRequest gains a validated profile string. CLI normalizes one budget flag
before scans, rejects disabled/direct-file conflicts privately, and scan.py passes
the opt-in keyword only to the SBOM factory. Preserve existing injected standard
factories and output schema. No reader/parser or metric change.

Tests exercise closed profile/protocol boundaries, actual simulated parent request
accounting and cached failure/success reuse, HTTP attempt/scan limits, deadline
kill/cleanup, admission, repeated-member identity association, and CLI routing.
Add an actual isolated offline worker extended-profile command beyond sequence300
where feasible with deterministic responses; production network is never a unit
fixture. Full suite plus capability-disabled-before-discovery and real-worker
gates run at integration. Existing negative transport/admission tests stay active.

Private live capture uses production main/mixed/default scanner, observation-only
supervisor close/protocol/call accounting and same-report human/JSON/verbose output.
Before starting, pin accepted inventory hash, private trust identity and finite
600attempt/600second/64MiB/60GA/10command ceilings. No retry run to chase yield.
Afterward compare input/trust identity, worker cleanup, all200 member identities,
reasons/ages/statistics and baseline104 rows. Separate changed metadata from newly
measurable members; do not attribute all total growth to the execution correction.
