# SBOM metadata execution budget correction

## Authority and scope

Run007-0055 authorizes specification, independent review, implementation,
convergence and one actual configured invocation of the already accepted retained
Dependency-Track inventory. This correction supersedes only Feature008 S5/P5's
mandatory300-request/300-second SBOM ceiling when explicitly configured below.
All other Feature008 population, admission, time, privacy and output contracts
remain binding. No current-checkout association or complete software inventory
claim follows. No new provider, acquisition, concurrency, persistent cache, resume,
package-manager execution or sibling-budget expansion is authorized.

## Evidence and requirement

The retained007-0052 same-inventory worker trace has exactly300 distinct request
keys:112 catalogues and188 GAV POM dates,1,592,793 response bytes,109.09s and clean
worker closure. No redundant metadata operation is present. Existing SBOM GA/date
maps and supervisor caches already reuse successes and failures after admission.
Run007-0054 retains104/200 measured,175.66183125459472 total,88 budget refusals,
five unknown eligibility, two catalogue unavailable and one unavailable date;
wall226.18369299999904 seconds. Its original capture has no worker counters, so
exact attempted/interrupted requests in that run are not directly observed.
Same identities/reasons/frontier and current code corroborate count exhaustion,
not absent registry metadata. Neither whole scan exceeded300seconds. In0052,
one budget member has a selected catalogue but no attempted date;87 subsequent
GAs have no attempted catalogue. Other eight failures are separately classified;
no underlying HTTP cause is inferred from the closed unavailable reasons.

There are200 inventory members and199 unique GAV/GA identities: distinct variants
remain separate members. Three requests per GA/GAV (catalogue, latest date, used
date) bound this inventory by597 before reuse/failures; equal versions share a date.
Canonical ordering explains which suffix lacks measurements, not intrinsic age.
Request-count exhaustion is not a unique-coordinate ceiling. Startup/cleanup are
included in the scan clock, but the retained trace shows neither cancellation nor
worker failure. Per-request10s and per-GA60s may still independently refuse work.

## User contract

Add directory-only `--sbom-budget {standard,extended}`. Omission and explicit
standard retain300 attempts/300 scan seconds. Explicit extended permits at most
600 attempts/600 scan seconds for the separate SBOM metadata worker only. This
corpus-sized upper bound is not a promise for all supported documents.600seconds
allows roughly twice the observed300-request226-second workload with headroom;
network variation, per-GA/time/byte/policy failures may still leave partial results.
Expose both profiles' costs in CLI help and usage documentation. Reject repeated
budget flags, unknown values, direct-file use and combination with --no-sbom with
fixed privacy-safe argument errors before scanning. Explicit SBOM file selection
and ordinary automatic directory discovery both support the profile.

Keep64MiB scan body bytes, per-response bounds,10s command/readiness,60s per-GA,
0.5s cleanup reserve, worker kill/reap/deferred guard and fixed public verified TLS
unchanged. No retries, redirects or concurrent work. Worker and parent independently
apply the same closed profile. Budget exhaustion retains successful ages and all
remaining members with existing reasons. No JSON fields, metric/time semantics,
identity/latest eligibility/order, weighting, sibling requests or totals change.

## Acceptance

- AC1: default and sibling execution remain300/300; extended only changes SBOM's
  attempt/scan ceilings to600/600 with bounded hard cancellation.
- AC2: parent, worker and HTTP accounting enforce the same selected ceilings;
  malformed profile/protocol counters refuse. Cached results do not spend requests.
- AC3: repeated identities/variants reuse metadata after independent admission
  without merging members; failures associate deterministically and partial ages
  survive exhaustion. No cross-run reuse or stale persistent state is introduced.
- AC4: namespace, endpoint, TLS, byte/response limits, refusal visibility and
  independent Declared/Observed/SBOM populations remain unchanged.
- AC5: deterministic full/capability-disabled/real-worker checks and independent
  security/resource convergence pass; one finite configured live result preserves
  original inputs and reports exact statistics, requests/reuse/refusals and changes
  to previously measured values, without promising yield or hosted success.
