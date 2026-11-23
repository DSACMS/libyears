# Offline integration and retained-corpus checkpoint

Run007-0051 implements T008 and verifies T009. The independent C2 disposition and
correction history are in [reviews.md](reviews.md). This record covers local
integration and retained document acceptance; T010/phase C and live V001 remain
separate. Governing behavior is unchanged in spec.md, output-contract.md and plan.md.

## User journey and execution basis

The ordinary interface is now `python -m libyears DIRECTORY`. Exact
`--sbom RELATIVE_FILE` selects one contained document, including an unusual name;
`--no-sbom` disables its discovery, reads and metadata work. Existing direct-file
inputs never activate SBOM. Selection/disable misuse is sanitized before scans.
No offline flag or hosted acquisition interface was added.

The retained acceptance witness invokes the actual CLI `main` through its existing
scan injection seam, using the real mixed orchestrator and an injected controlled
metadata supervisor. It exercises ordinary discovery, explicit `unusual.data`,
disable, normal/verbose/JSON output and unavailable metadata. Test-owned copies are
byte-for-byte copies of the hash-verified originals, never regenerated SBOMs.
`python -m libyears --help` also confirms the real module entry point exposes the
options. No retained-document invocation used live production metadata.

The public report keeps SBOM independent of legacy direct-source fields and Maven
Declared/Observed views. An accepted empty ordinary source and a failed/unknown
ordinary source remain relevant; their existing population and output survive.
SBOM-only output leads with its useful section. Active SBOM output protects the
selected root and raw diagnostics; absence/disable retains the previous route.

## Retained evidence

All six original files are read only from the previously authorized durable
007-0047 corpus location. The verifier binds each exact SHA256 before invocation;
unit tests never require that private directory. Full bindings, safe captures and
reproduction procedures are in helper-resolved `D/007-0051/corpus/`.

| Retained artifact | Result |
| --- | --- |
| Dependency-Track4.13.4 CycloneDX1.5, SHA256 `c201f3a64e7b2c510b83fe99dd6e945244030c6484009100b04a257721dba790` | Accepted:201 original entries; one exact subject alias excluded;200 unique component-version members, all supported exact;21 services excluded |
| Its explicit reference graph |424 edges;43 direct/157 transitive/0 unknown members; graph labels do not establish local directness |
| Hash-bound release POM |57 literal declarations compared individually;43 inventory/subject-edge matches;14 test declarations omitted; this is historical comparison only, never the SBOM denominator |
| CPython3.13.0 full release SPDX and checked-in SPDX-shaped fragment |Both `sbom_unsupported_format`; no population or metadata work |
| commons-lang and requests GitHub SPDX exports |Both `sbom_unsupported_format`; no population or metadata work |

The producer's document population does not establish current-checkout association,
evaluated/resolved direct scope, real-world completeness, public acquisition/content,
installation, runtime or deployment. No target checkout was inspected or executed.

## Controlled metadata and visible failures

Catalogues and POM responses are synthetic and pass the existing Maven selection,
identity and Last-Modified parsers. Controlled dates are2021-01-01T00:00:00Z and
2022-01-01T06:00:00Z, exactly365.25days apart; retrieval time is also synthetic.
The invented catalogue candidate9999.0 is test data, not an asserted real release.
Existing ordering/eligibility policy runs unchanged, including refusal of unknown
latest eligibility. No fallback is introduced to improve coverage.

From the same200-member document, controlled responses yield M=197/coverage0.985,
total196.0 synthetic libyears, mean196/197, median1.0, maximum1.0. The measured
subset includes196 positive ages and one evidence-backed same-version zero.
Three individually unmeasurable rows remain: one `maven_catalogue_unavailable`,
one `maven_time_basis_unavailable` and one `unknown_latest_eligibility`.

Compact excerpt from source `bom.json`, subject Dependency-Track, with **synthetic
metadata dates and ages**:

| Document component | Used | Controlled comparator | Synthetic libyears | Reason |
| --- | --- | --- | --- | --- |
| us.springett:alpine-common |3.2.0|9999.0|1.0|—|
| ch.qos.logback:logback-classic |1.5.18|unavailable|unavailable|maven_catalogue_unavailable|

A separate unavailable-worker response run retains N=200, all200 exact version
facts and all200 unmeasurable rows, M=0/coverage0.0/total0.0. Its zero total describes
an empty measured subset; it does not establish freshness. Source refusal instead
has null population and all-null statistics. No real age yield was measured.

## Reproduction and deterministic coverage

The narrow offline entry point is
`tools/verify_sbom_corpus.py CORPUS_DIRECTORY OUTPUT_DIRECTORY`. Supply the already-
authorized original corpus directory explicitly; the verifier neither searches for
inputs nor retrieves missing bytes. It refuses unavailable primitives, absent or
changed originals and broken invariants. Safe output includes verification.json,
synthetic-metadata-report.json/txt/verbose.txt and unavailable-metadata-report.json.
The durable verification record identifies the exact original input bindings,
controlled evidence basis, CLI seam, all57 POM comparisons, counts and reasons.

Deterministic tests use synthetic documents and controlled metadata only. A42-case
matrix freezes sibling inputs/responses across explicit/ordinary NuGet modes,
measured/empty/unknown ordinary populations and absent/positive/refused/empty/
incomplete/exhausted/partially exhausted SBOM. Dropping sbom preserves every legacy
JSON value, source error, measurement and summary; ordinary/verbose tables retain
the independent existing population. Separate witnesses cover exact CLI errors,
no disabled/direct-file work, namespace vetoes across subjects/versions/variants,
missing-version veto transfer, factory ordering, exact capabilities, no fallback,
production deferred-cleanup refusal and no second worker after an unreaped ordinary
worker. Completed sibling and earlier SBOM ages survive SBOM allowance exhaustion.

Native tests cover actual128-directory/10,000-entry/8MiB ceilings alongside existing
link/race/reparse/special-file/refusal witnesses. Portable framing tests exercise
exact250,000-token and UTF-8 scalar ceilings, all other document/graph limits,
late malformed inert data and strict output projection. Semantic tests inject
stable input/absence where host primitives are not the property under test.

## Actual checks and outstanding evidence

Local execution: Darwin, Python3.11.0. Full deterministic suite:1250 tests PASS,
1 skip. With os.supports_dir_fd empty before discovery:1250 tests PASS,123 skips;
portable/refusal witnesses remain active. Maven worker/protocol/supervisor and
NuGet RealWorkerTests:17 tests PASS. Focused correction regressions:122 PASS.
Configured current-content and final committed-history security/whitespace results
are retained in the durable completion record after the final local commit.

Actual hosted Ubuntu/macOS/Windows × Python3.11/3.12/3.13 execution is **pending**;
local capability simulation is not Windows execution. No hosted state was queried.
Live PyPI smoke, SBOM live V001, new acquisition and publication were not run or
authorized. C2 local review cannot establish live yield or actual hosted-platform
results. No push, tag, release or publication is part of this checkpoint.

## Subsequent authorized real validation

Run007-0052 separately obtained real production metadata after T010/C3 approval:
104/200 members,175.4693147134129 conventional POM Last-Modified libyears,
coverage52%,96 visible refusals. See [the live validation record](live-validation.md)
for exact statistics, inventory limits, blockers, one-batch provenance and replay.
This does not reclassify the synthetic evidence above or establish hosted results.
