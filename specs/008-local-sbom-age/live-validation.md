# Real retained-inventory age validation — 007-0052

Measured **104/200 SBOM inventory members: 175.4693147134129 libyears** on
`maven_conventional_pom_last_modified`. These are actual production metadata
results, obtained 2026-11-23, not the synthetic dates in the earlier
[offline C2 record](validation.md). V001's independent review/disposition is in
[reviews.md](reviews.md).

| Statistic | Actual result |
| --- | ---: |
| Accepted inventory members | 200 |
| Measured / unmeasurable | 104 / 96 |
| SBOM population age coverage | 52% |
| Measured-subset total libyears | 175.4693147134129 |
| Mean | 1.6872049491674321 |
| Median | 1.6892302646589095 |
| Maximum | 6.976594671331154 |

## Which inventory this describes

The original retained public Dependency-Track 4.13.4 CycloneDX JSON 1.5 document,
SHA256 `c201f3a64e7b2c510b83fe99dd6e945244030c6484009100b04a257721dba790`,
was recovered from the exact durable C2 corpus reference and verified before and
after validation. A byte-identical isolated local copy named `bom.json` was scanned;
it is an input staging directory, not a current Dependency-Track checkout.
No target checkout, build, resolver, package manager or new SBOM acquisition ran.

The document has201 original component entries; one exact subject alias is excluded,
leaving200 unique external component-version members. All200 have supported exact
Maven identities. The21 services remain excluded. The424-edge graph labels43 members
direct and157 transitive, relative to the subject's represented paths. Of those,
17 direct and87 transitive members measured. No scope filter, local occurrence
weighting or additional deduplication changed the approved population. Alias/record
multiplicity and distinct variants remain represented by the established contract.

**Current-checkout association is not established.** Document completeness outside
this projection is unknown. This is neither complete repository technical debt nor
an installed/runtime/deployed/current-build inventory. It is independent of Maven
Declared/Observed populations and their totals, and of legacy direct-source totals.
The actual ordinary output leads with SBOM and never adds its ages to those views.

## One bounded production batch

T010/C3 approved before this invocation. The human's007-0052 grant authorizes the
retained public coordinates and existing fixed Central routes, finite budgets and
recovery/staging of the exact previously approved private trust copy. That copy
loaded successfully, with certificate and hostname verification enabled throughout.
No alternate trust, private trust details, machine configuration or credentials
were discovered or retained in the result artifacts.

The actual CLI `main` ran ordinary discovery against the isolated directory with
`--ca-bundle` supplied privately. Its transparent scan capture calls the real mixed
orchestrator with every default metadata factory. The existing MavenSupervisor,
installed isolated worker and MavenHTTPClient performed the metadata work. No
injected metadata/provider or parallel age calculator produced these results.
A close observer retained only validated worker protocol outcomes before the normal
cleanup, without changing admission, requests, transport or measurement.

Exactly one worker batch made300 attempts and consumed1,592,793 body bytes, within
its300-attempt/64MiB/300-second limits and unchanged per-command/per-GA bounds.
The batch exhausted the attempt allowance, not the time or byte allowance; captured
scan wall time was109.09002654100186seconds, an operational duration, not agent runtime.
Within-batch admitted caching remained enabled. No retries, redirects, new endpoint
routes, date fallback or second corpus batch chased improved coverage. The worker
closed, was reaped and removed its temporary directory; no deferred worker remains.

Ordinary, verbose and schema3 JSON views come from **the same scan result**, rendered
by production formatters. Exact compared versions, safe identities/relationships,
POM timestamps, catalogue retrieval times, anomaly flags and refusals are retained.
For example, transitive `com.fasterxml.jackson.core:jackson-annotations`2.18.3
compares to2.23: POM dates2025-02-28T23:25:04Z and2026-11-07T23:58:48Z yield
1.6893180723502421libyears; catalogue retrieval2026-11-23T20:46:30.985502Z.
These dates are real evidence, unlike the clearly synthetic contract examples.

The comparator remains `sbom_maven_central_convention`, Maven ordering3.9.11 and
`maven_conservative_stable_v1`. Central correspondence is assumed; an undisclosed
private fork/namesake could receive a wrong public comparison. Dates describe
identity-checked GAV POM representation modification, not first publication,
classifier availability, acquisition or content. No missing date becomes zero.

## Remaining rows

Every unmeasurable row appears individually with its exact version and fixed
reason in ordinary output and JSON. The supported diagnostic granularity is:

| Reason | Members | Established blocker |
| --- | ---: | --- |
| maven_metadata_budget_exceeded | 88 | The fixed300-attempt allowance was exhausted; no further lookup attempted |
| unknown_latest_eligibility | 5 | Whole-catalogue selection cannot establish a latest stable candidate under the unchanged conservative policy |
| maven_catalogue_unavailable | 2 | The bounded production catalogue operation supplied no admissible catalogue result |
| maven_time_basis_unavailable | 1 | Required identity-bound POM modification-time evidence was unavailable |

| Non-budget refusal identity | Exact inventory version | Reason |
| --- | --- | --- |
| jakarta.inject:jakarta.inject-api | 2.0.1 | unknown_latest_eligibility |
| com.google.guava:guava | 32.0.1-jre | unknown_latest_eligibility |
| com.google.guava:listenablefuture | 9999.0-empty-to-avoid-conflict-with-guava | unknown_latest_eligibility |
| com.microsoft.sqlserver:mssql-jdbc | 12.10.0.jre11 | unknown_latest_eligibility |
| com.google.apis:google-api-services-sqladmin | v1beta4-rev20250310-2.0.0 | unknown_latest_eligibility |
| commons-io:commons-io | 2.18.0 | maven_catalogue_unavailable |
| commons-logging:commons-logging | 1.2 | maven_catalogue_unavailable |
| jakarta.mail:jakarta.mail-api | 2.1.3 | maven_time_basis_unavailable |

The protocol does not retain underlying HTTP/schema
failure diagnostics, so these three failures are not attributed to TLS, a specific
status code or missing headers. No extra requests were made to diagnose them.

## Durable output, audit and reproduction

Resolve `D` with `python3 tools/observation_handoff.py directory`. Under
`D/007-0052/`, inspect:

- `ordinary.txt`, `verbose.txt`, `report.json`: real production result views.
- `metadata-provenance.json`:300 validated worker outcomes with exact operations,
  coordinates, versions, dates, retrieval times and cumulative resource counters.
- `comparisons.json`: all200 rows and derived fixed public metadata routes;
  `validation-audit.json`: reconciled population, reasons, arithmetic and lifecycle.
- `live-result-freeze.json`: exact SHA256 bindings for twelve result/input/procedure
  artifacts; original bytes are `inventory/bom.json`.
- `live.py`: guarded one-batch procedure using the existing private preparation
  reference, with no actual trust path or contents stored in this result record.
- `reproduce.py`: integrity-checked output replay; no network or recalculation.

The audit binds every measured row to its successful target and two accepted POM
date outcomes, recalculates ages and all unrounded summary values, and reconciles
all reason counts. Original HTTP bodies are not retained; replay of raw catalogue/
POM parsing is therefore not claimed. Production parsing/identity enforcement has
the independently reviewed deterministic coverage. An initial audit comparison
used an algebraically equivalent floating-point division order; matching the
established days-then-years order closes the audit discrepancy without changing
any result, metric or runtime code. No synthetic replacement metadata was used.

Replay the exact ordinary CLI output from the libyears checkout; the whole command's
stdout/stderr reaches the terminal and clipboard. Add `--json` or `--verbose` to
`reproduce.py` for the corresponding same-scan view:

```sh
(
  set -o pipefail
  (
    run_dir="$(python3 tools/observation_handoff.py directory)" &&
    python3 "$run_dir/007-0052/reproduce.py"
  ) 2>&1 | tee /dev/tty | pbcopy
)
```

Replay is distinguished from a fresh measurement: the original supported invocation
was `python3 -m libyears DIRECTORY --ca-bundle APPROVED_PRIVATE_COPY`. Both operational
arguments were supplied privately by the retained procedure. Future fresh metadata
runs may differ and require their own bounded disclosure/access authority; this
run deliberately performs no second batch. Git-directory evidence survives ordinary
restart but is local working storage, not tracked history or a backup.

## Verification and outstanding gate

C3's complete independent AC01–AC14 review and fresh correction verification approve
phase C. Run0052 full deterministic1250 tests PASS/1 skip and actual offline worker
checks17 PASS. No runtime defect was exposed by this batch; the one prose correction
and local audit operation-order correction introduce no behavior changes.
Documentation/link/anchor/sensitivity/security/whitespace checks and the actual V001
independent result review are recorded at closure in reviews.md and durable evidence.
Actual hosted Ubuntu/macOS/Windows × Python3.11/3.12/3.13 evidence remains pending;
local tests/simulations do not establish it. Next consequential gate is human
publication and subsequent actual hosted evidence, if desired. No push, tag, release
or publication was performed.
