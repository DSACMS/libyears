# Retained SBOM execution validation — 007-0055

The single configured production invocation measures **186/200 members (93%)**,
**337.47960139554345 conventional Maven libyears**. All 104 previously measured
ages are unchanged; 82 members become measurable. No metadata-budget refusal remains.
This is the separate retained Dependency-Track4.13.4 asserted inventory, with no
established association to the representative checkouts or evaluated/deployed state.
No totals are combined with Maven Declared/Observed or local source populations.

## Before and after

The before result is original007-0054, not the earlier0052 result. The displayed
SBOM summary uses these raw values verbatim; no rounded total hides a discrepancy.

| Statistic | Before0054 | After0055 |
| --- | ---: | ---: |
| dependencies_discovered | 200 | 200 |
| dependencies_measured | 104 | 186 |
| coverage | 0.52 | 0.93 |
| total_libyears | 175.66183125459472 | 337.47960139554345 |
| mean_libyears | 1.6890560697557189 | 1.8144064591158247 |
| median_libyears | 1.6892302646589095 | 1.6893425038659466 |
| max_libyears | 6.976594671331154 | 8.605880992217406 |

All 200 member identities/variants, order, 43 direct / 157 transitive relationships and
source hash are unchanged. 42 direct and 144 transitive members now measure. Repeated
GAV variants remain two members but share admitted metadata. Every one of the 14
unmeasurable members remains visible in ordinary and JSON output.

| Exact refusal | Before | After |
| --- | ---: | ---: |
| maven_metadata_budget_exceeded | 88 | 0 |
| unknown_latest_eligibility | 5 | 5 |
| maven_catalogue_unavailable | 2 | 5 |
| maven_time_basis_unavailable | 1 | 4 |

Of the 88 formerly budget-refused members, 82 now measure, three receive catalogue
refusals and three receive date refusals. The earlier eight refusals remain in
their original classifications. No previously measured value, comparison version
or returned used/latest POM timestamp changes, so none of this total increase is
attributed to fresh metadata changes in the 104-row overlap. Catalogue retrieval
instants are fresh observations. Date semantics remain versioned POM Last-Modified,
not first publication, classifier availability, acquisition or complete debt.

## Actual bottleneck and correction

Existing SBOM target/date dictionaries and supervisor caches already reuse both
successes and failures after admission. No duplicate operation was found in the
retained0052 worker trace: 300 requests, 112 catalogues / 188 dates, 1,592,793 bytes,
109.09002654100186 seconds; clean close/reap and no cancellation. The 300th request
selected jakarta.ws.rs:jakarta.ws.rs-api 4.0.0; no date for that member was attempted,
and 87 subsequent GAs never received a catalogue request. These are unattempted work,
not absent metadata. Canonical ordering determines this suffix.

The0054 capture retained 226.18369299999904 seconds and identical identities/refusal
frontier, but **no worker request counters**. That supports the count-bottleneck
explanation alongside code and0052 trace; it does not establish direct0054 request
or interruption observations. Neither retained whole-batch duration reaches 300s;
0052's byte ceiling was also distant. No worker/startup/teardown failure is observed.
Per-command/per-GA bounds and unrelated provider/eligibility/date failures remain
independent, rather than being reclassified as global count exhaustion.

There are 199 unique GA/GAV identities among 200 members. At most 597 catalogue/latest/
used-date operations are needed before reuse/failures for this inventory. The
independently reviewed [specification](spec.md), [plan](plan.md) and
[tasks](tasks.md) choose a closed explicit `--sbom-budget extended` profile of
600 requests / 600 scan seconds. Standard remains 300/300; larger documents may exhaust
either profile. The 600s wall allowance is a cost ceiling, not a completion promise.
The 64 MiB cumulative scan body-byte ceiling, 2 MiB catalogue and 1 MiB POM
response limits, 10s command, 60s GA, 10s readiness, 0.5s cleanup, hard process
termination, TLS, fixed-public endpoint, capability, namespace and disclosure
limits are unchanged.
No new cache mechanism, concurrency, retries, persistent/resumable state or sibling
budget increase is introduced. Default requests/output remain unchanged.

## One configured live invocation

The limits were recorded **before** the one batch in private `live-started.json`:
600 attempts, 600 seconds, 64 MiB, 60s GA, 10s command/readiness and 0.5s cleanup. Actual results:

- 543 attempted, 543 completed and 543 unique metadata operations: 199 catalogues / 344 dates.
- All 199 lookup GAs attempted; no interrupted command, cancellation or budget refusal.
- 3,071,595 response bytes; 244.3073433330028 seconds elapsed operational wall time.
- Existing adapter reuse: one catalogue and two dates across distinct member variants;
 32 same-version cases suppress the redundant second date access. Supervisor cache
 reuses 0 additional calls because the adapter already avoids those duplicates.
- Worker closed/reaped, private temporary directory removed, no deferred worker.
- CLI exit 0, empty stderr. Ordinary/JSON/verbose share one production scan; all 186
 ages and aggregate statistics are independently recomputed from returned dates.

Before0054's request count is unobserved; do not substitute0052's observed300
requests as a newly observed0054 counter. Wall times vary with network conditions;
this is not a throughput benchmark or agent-runtime measurement.

## Reproduce the configured command

From the libyears source root, recover the exact accepted input and private CA
reference without printing its location. This runs fresh metadata; it is not needed
merely to inspect the retained result.

```sh
(
  set -o pipefail
  (
    D=$(python3 tools/observation_handoff.py directory) || exit
    ca_bundle=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["destination"])' "$D/007-0029/trust-copy-reference.json") || exit
    python3 -m libyears "$D/007-0052/inventory" --ca-bundle "$ca_bundle" --sbom-budget extended
  ) 2>&1 | tee /dev/tty | pbcopy
)
```

Actual ordinary summary excerpt:

```text
SBOM population age coverage: 186/200 (0.93)
Measured subset libyears: total=337.47960139554345 mean=1.8144064591158247 median=1.6893425038659466 max=8.605880992217406
```

## Remaining limits and evidence

The five eligibility refusals need admissible unambiguous latest-selection metadata
under the unchanged conservative policy; more requests alone cannot override them.
The five catalogue and four date failures are closed provider/metadata-admission
outcomes, not exhaustion. They may reflect availability/transport or inadmissible
metadata; the retained protocol does not expose raw HTTP failure causes. Date rows
need admissible identity-bound POM time evidence. Do not diagnose missing packages,
permanent outages or absent publication from these codes, or turn them into zero.
No additional live retry or evidence investigation is performed in this run.

Original input SHA256 remains
`c201f3a64e7b2c510b83fe99dd6e945244030c6484009100b04a257721dba790`;
before/after safe snapshots match. Existing approved private CA identity remains
unchanged and certificate/hostname verification enabled. No trust search, new
artifact acceptance/acquisition or representative-checkout access occurs.

Raw commands/stdout/stderr, worker protocol outcomes, input digests/integrity checks,
comparison and lifecycle evidence are private under helper-resolved `D/007-0055/`.
Original0054 handoff/completion/artifact and59private bindings are validated before
once-only ledger append with supplied761s/GPT-6.1-Sol/openai/high/Codex0.160.0/session/
context77%left117K475K/account203 telemetry. Original runtime qualifications,
unknown confounding and before202 remain. Standing continuity supports current
before203; no derived credit delta. Current model/effort are unobserved and not
copied from prior status. Current0055 is not appended to its own ledger.

Implementation commit is `d08364b8307c5fa93f033b89a3dfac1298d55ab5`.
Full 1261 PASS / 1 skip, capability-disabled-before-discovery 1261 PASS / 123 skips and actual
offline worker gate 18 PASS; fresh independent implementation convergence APPROVE,
no material findings. Capability simulation is not Windows/hosted evidence.
Live-result independent disposition and final security/commit scope follow in
[reviews](reviews.md). No push, tag, release or hosted success claim.
