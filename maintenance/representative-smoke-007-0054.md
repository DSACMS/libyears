# Representative ordinary-user smoke — 007-0054

Live operational validation on 2026-11-24 of candidate
`20b4bf0fac2a127bdd11421910147915f57a2523`. Starting staged, unstaged and
untracked state is empty. Actual github/main and cms/main both match that SHA;
publication is complete at that boundary. No push or hosted job query occurred;
hosted checks remain unobserved here. Product code and tests are unchanged.

## Results

Every available public checkout's origin identity was checked before use.
Ordinary means the no-option `python3 -m libyears ROOT` invocation. Configured
runs are separate; explicit trust is not claimed as default transport success.
The retained management envelope is byte-identical to its earlier accepted input;
production admission checks its current consumer bindings. The established private
CA passes regular-file, owner, size, private-mode and verified TLS-loading checks.
No new trust material, SBOM, model or witness was acquired or accepted.

| Repository / invocation | Population / view | Measured / denominator | Total libyears | Wall seconds | Remaining limit / answer scope |
| --- | --- | --- | ---: | ---: | --- |
| Medicare dashboard / ordinary | npm direct production | 10/10 | 18.703444347637337 | 19.34 | Complete supported direct npm population; not all runtime/transitive software |
| metrics / ordinary | PyPI direct | 0/7 | 0 (empty measured subset) | 0.08 | Seven non-exact versions; no usable age total |
| metrics / ordinary | npm direct production | 0/0 | 0 (empty population) | same scan | No npm age evidence; overall repository denominator unknown |
| dpc-app / ordinary | Maven Declared | 0/unknown | 0 (empty measured subset) | 0.10 | 143 version refusals, 36 policy refusals; bounded discovery incomplete |
| ab2d / ordinary | Maven Declared | 0/unknown | 0 (empty measured subset) | 0.31 | 42 catalogue failures, 46 version and 39 model refusals |
| ab2d / explicit CA only | Maven Declared | 40/unknown | 9.474748459958931 | 21.46 | Measured occurrence subset; denominator/coverage unknown |
| ab2d / explicit CA + accepted management | Maven Declared | 54/unknown | 15.735360420310798 | 31.64 | 39 version, 32 model, 2 catalogue refusals; measured occurrence subset |
| OASim / ordinary | NuGet direct project occurrences | 51/51 | 54.10496311259412 | 209.13 | Complete accepted bounded snapshot population; conventional public correspondence, not deployment |

npm/PyPI use registry publication dates; NuGet uses identity-bound catalog created
(first nuget.org receipt). Maven uses conventional versioned public POM
Last-Modified, not first publication. Maven Observed remains unavailable with null
numerics in every Java invocation. Its totals are never added to Declared or to
SBOM totals. Occurrences repeated across modules/projects remain separately weighted.

## Human output and JSON fidelity

These are actual ordinary output excerpts, not reconstructed successful test labels:

```text
Measured: 10 / 10 dependencies
Coverage: 100.0%
Total:    18.70 libyears
Mean:     1.87
Median:   2.08
Maximum:  2.97
```

```text
npm: unknown coverage; 0 / 0 measured; total 0.00, mean null, median null, max null libyears
pypi: 0.0% coverage; 0 / 7 measured; total 0.00, mean null, median null, max null libyears
```

Both ordinary Java reports display:

```text
No declared ages measured; zero total describes an empty measured subset.
```

All positively found unmeasurable dependencies remain visible: metrics has seven
Python rows, dpc-app 179 Maven rows, ordinary ab2d 127 Maven rows; OASim and the
dashboard have none. No hidden positive unmeasurable dependency was found in these
ordinary runs. Expected source-policy/static-version refusals are not product
defects, but DPC's ordinary journey supplies no age number.

Metrics' npm 0/0 describes its root production scope, not a measured zero-age
repository. Its repository N/coverage are unknown in JSON, while ordinary output
shows only the useful npm/PyPI projections and suppresses discovery-only Maven/
NuGet failures. DPC similarly suppresses discovery-only NuGet. JSON ecosystem keys
in these cases are not positive evidence of ecosystem dependencies. Ordinary
suppression can obscure why the overall repository denominator is unknown; it
must not be reported as complete discovery or absence of those ecosystems.

DPC begins with `Existing source populations (SBOM excluded):` while its SBOM
section is suppressed in ordinary output. JSON records SBOM discovery unavailable,
not an accepted inventory or a measured zero. That incomplete-discovery reason is
not visible in ordinary output. The dashboard has no such heading; its numeric
output matches JSON rounding.
Maven's legacy top-level null scalar summary and its separate partial Declared
zero/subset summary describe different projections; they are not inconsistent
numeric answers. No incompatible projections are combined.

## Integrity and provenance

The retained bounded before/after procedure compares revision, full nonignored
status, index-stage digest, depth/entry/directory-bounded names/stat identities and
supported source-input digests. All five targets compare equal around their runs.
Dashboard, metrics, DPC and AB2D have empty observed Git status; OASim starts and
ends dirty, including existing untracked state. No target is normalized or modified.
This is bounded integrity evidence, not an OS-wide or ignored-content guarantee.

The exact CLI argument vectors, stdout, stderr, status, operational wall durations,
JSON and verbose renderings are private under helper-resolved `D/007-0054/`.
As in the retained methodology, actual production CLI `main` calls the unchanged
mixed scanner through a transparent capture seam; the same report is rendered
with production human/JSON/verbose formatters. No injected registry data or second
live refresh supports presentation verification. Command wall durations are not
agent runtime. Existing bounds and public routes are unchanged.

Original durable 007-0053 ordered 44-key handoff, final-freeze bindings, completion
and principal artifact are validated before a once-only ledger append. Supplied
human status adds 1295 seconds, session, GPT-6.1-Sol/openai/medium, version 0.160.0
and credits-after 202. Original runtime qualifications/unknown confounding and
credits-before 200 remain unchanged. Standing adjacent-run continuity supports
current before 202; no derived credit delta is stored. Current model/effort are
unavailable to this recorder and left blank, separately from prior human telemetry.
Current 007-0054 is not appended to its own ledger.

The historical OASim precision witness is present, but an exact historical digest
binding was not recovered in durable private records. No new acceptance is implied
and that configured precision route is not rerun. No accepted exact Python
snapshot for metrics or configured DPC route was recovered; none is fabricated.

SBOM result, independent review and final closure follow below.

## Separate retained SBOM inventory

The byte-identical previously accepted Dependency-Track 4.13.4 document is scanned
from its retained isolated inventory directory with explicit approved trust.
It is not associated with any of the five checkouts, and no SBOM is generated,
downloaded or newly accepted. Input SHA256 remains
`c201f3a64e7b2c510b83fe99dd6e945244030c6484009100b04a257721dba790`.

Actual current output:

```text
SBOM dependency age
Source: bom.json
Format: CycloneDX 1.5
Subject: dependency-track
Basis: sbom_asserted_unique_component_versions
SBOM population age coverage: 104/200 (0.52)
Measured subset libyears: total=175.66183125459472 mean=1.6890560697557189 median=1.6892302646589095 max=6.976594671331154
```

There are 43 direct and 157 transitive members, with 104 measured and 96 visible
unmeasurable members. The unchanged metadata budget still limits **88 members**;
five have unknown latest eligibility, two unavailable catalogues, one unavailable
date. Current measured-subset total is 175.66183125459472 conventional POM-date
libyears, not the historical 175.4693147134129. Wall duration is 226.18 seconds;
exit 0, empty stderr, input integrity equal. This is 52% of an asserted inventory,
not a complete repository answer. No second batch chases coverage.

## Disposition

All eight invocations exit 0 with empty stderr and equal bounded before/after
integrity. Exit success does not make an unavailable age or partial population a
satisfactory complete repository answer. Complete output, source refusals and exact
commands remain inspectable privately; tracked excerpts omit local operational paths.
No implementation repair is made, and no full product-suite rerun is needed.

The single highest-value next step is a bounded follow-up on SBOM metadata-budget
exhaustion: 88 known, exact inventory members already have accepted identities but
cannot receive an age in one allowed batch. Preserve the budget/safety boundary
until a separately approved remedy establishes more coverage. This offers a larger
concrete known-population gain than polishing the DPC discovery-only heading.

Fresh independent read-only review: COMPLETE; original REVISE for the DPC/dashboard
heading attribution, then focused correction APPROVE with no unresolved material
finding. The original freeze and finding are preserved privately, with the corrected
report and exact command-file digests. Reviewer independently recomputed all259
measured ages and verified row/count/refusal fidelity, evidence separation, original
observation reconciliation and bounded target integrity. Bash/zsh command syntax
and configured current-content security pass. Final committed-history security and
the current helper handoff are retained privately at closure. No full suite rerun,
push, tag, release, target change or hosted-check success claim.
