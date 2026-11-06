# NuGet repository sources

Candidate specification, run 006-0022. Approval disposition lives in reviews.md.
This separate correction supersedes Feature006 S1's explicit-only activation and
S6's NuGet identity only for ordinary directory measurement. All other Feature006
parser, selection, H3, date, failure, privacy and metric contracts remain binding.
It supersedes 006-0020's human-only recognition on production ordinary scans.
No Feature007, generic analyzer abstraction, or new ecosystem is authorized.

## Human authority

The commissioning human approves source-qualified direct-dependency occurrence
weighting. Every independently supported project is a source. The same package
in two projects counts twice, at independently selected versions. ProjectReference
edges count zero external rows and do not merge populations. Supported direct
test/tool/analyzer/PrivateAssets references remain included. Solutions supply no
population authority. Do not execute targets, dotnet/NuGet/MSBuild or resolvers,
weaken H3, deduplicate across projects, fabricate denominators or change the metric.
The human authorizes the complete SDD lifecycle, local commits, independent reviews
and read-only OASim smoke; push/publication remains unauthorized.

## R1 — Automatic bounded attempt

Ordinary directory scans automatically attempt every candidate in the existing
006-0020 bound: regular .csproj files, depths 0–4 inclusive, hidden/named directory
exclusions, no symlink/reparse traversal, maxima 256 directories/10,000 entries/
100 projects. Depth5 is excluded, not an incomplete search. No recursive sibling
ecosystem discovery, solution interpretation or reference traversal is added.
Discovery incomplete/unavailable discards its partial inventory, records a NuGet
source error (`nuget_discovery_incomplete`/`nuget_discovery_unavailable`), and has
unknown population. A complete empty inventory leaves NuGet absent. Direct-file
scans remain unchanged. Explicit --nuget-project retains its existing one-immediate-
project contract, bypasses discovery, and never includes other projects.
Each candidate is read only within its own parent, with exactly that project,
parent packages.lock.json and any explicitly supplied witness. Candidate paths
must remain contained without following any ancestor link or reparse replacement.
Read failures reject that source; successful siblings survive. No partial parsing
or project-name/type exclusions are permitted.

## R2 — Explicit witness acceptance

Ordinary mode without a witness attempts sources but cannot acquire public lookup
authority from discovery, names, declarations or locks. No conventional witness
is searched or accepted. Add repeatable exact --nuget-witness PROJECT=NAME.json:
PROJECT is the exact POSIX root-relative discovered project identity, NAME.json
one immediate witness in that project's parent. The mapping contains exactly one
literal `=` delimiter; `=` is forbidden within either operand (such projects
remain automatically attempted without testimony and can use the existing
explicit interface). Each mapping explicitly accepts
that file's supplier assertions under unchanged H3. No absolute/dot/dotdot/empty
components, backslashes, globs, control characters or duplicate project mappings;
no packages.lock.json witness. Mapping requires directory ordinary mode and cannot
combine with --nuget-project/--nuget-provenance. Malformed mappings are safe usage
errors before source reads; a valid unmatched mapping is a stable source error
`nuget_witness_project_missing`, with unknown population (never silently ignored).
If discovery fails, report only discovery failure, not invented mapping failures.
Existing explicit --nuget-provenance behavior is unchanged. A supplied witness's
project binding still uses its immediate filename, exact bytes and framework;
public source attribution uses the root-relative source identity separately.

## R3 — Population and composition

Occurrence identity is (nuget, root-relative project path, case-insensitive ID).
Duplicates within one project still reject that source. All same-ID occurrences
across projects remain separate, including identical versions and conflicting
versions. No arithmetic deduplication. Each source applies Feature006 S6: unknown
population gives null N/M/coverage/numerics; known N with unavailable required
whole evidence retains N but null M/coverage/numerics; accepted whole evidence
permits individual failures and truthful M/N, including zero/empty distinctions.
Repository and NuGet N are null if any relevant source population is unknown.
Coverage is null if any relevant source measurement is unavailable. Measured is
null only if all relevant detected sources are unavailable; successful rows and
numerical aggregates survive failed siblings. NuGet total is null when all its
sources are unavailable, otherwise computed from successes; repository total
retains existing 0.0 when no rows. Mean/median/max use measured occurrences only.
An incomplete inventory never masquerades as complete coverage. Existing root
PyPI/npm/Ruby results and evidence remain intact under every NuGet failure.

## R4 — Compatible public source identity

Retain schema_version 3 and existing fields/types/meanings. Explicit single-source
output retains its exact existing shape, including version_evidence.nuget and
immediate per-row project names. Ordinary scans previously produced no NuGet
JSON facts; introduce an optional top-level `nuget_sources` array for this new
mode only. Do not change the singleton into an array or pick a representative.
In ordinary mode version_evidence retains other ecosystems unchanged and omits
the legacy selected-only nuget singleton. `ecosystems` and by_ecosystem include
nuget whenever sources or a discovery failure are present.

Each nuget_sources element contains `source_id` (POSIX root-relative project),
`version_evidence` (existing NuGet singleton fields, project/snapshot/witness
filenames relative to that project's parent), `summary` (existing summary fields),
and `measurement_available` (boolean). It includes failed and empty sources.
A discovery-wide failure has source_id null and declaration_source null; unmatched
mappings use their supplied project identity. Source order is lexical, discovery
failure first. No counts claim projects outside the documented bound.

Ordinary NuGet measured/unmeasurable rows add `source_id` and retain safe staged
nuget_evidence; its project remains the immediate bound filename. Ordinary NuGet
source_errors add `source_id` (null for discovery failure) while existing source
continues to identify the relevant immediate input, or `repository` for discovery.
Thus same-name packages, same project basenames and shared-parent locks remain
unambiguous; occurrence identity does not depend on array order. No fields are
added to other ecosystems' rows/errors. No synthetic package rows for source errors.
This is a proposed additive v3 extension; independent compatibility review is
required. If it cannot preserve released contracts, stop at HUMAN SCHEMA DECISION
with alternatives rather than implementing an incompatible v3 shape.

## R5 — Human output and privacy

Human output names each escaped root-relative source, its known/unknown N and
availability/summary, and associates each NuGet row and source error with that
source. It explains occurrence weighting, bounded discovery, explicit testimony,
H3, first-receipt/listed-stable semantics and limitations already disclosed by
Feature006. Do not tell ordinary users to select a project to request measurement.
Keep --nuget-project documented for precision/debugging. JSON escaping and human
JSON-string framing protect source filenames from controls. Do not disclose raw
hashes, origins, witness contents, baseline, absolute paths or diagnostics. Existing
explicit output privacy and non-NuGet report behavior remain intact.

## R6 — Resource, verification and operational acceptance

All local bounds and required filesystem refusal remain enforced. One supervised
NuGet metadata batch owns scan-wide deadlines/request/rate budgets across all
sources. Repeated occurrences must not overwrite evidence/results even when the
same capability identity appears twice. No target code execution, writes, generated
evidence, archives, caches/config/credentials or public namesake fallback.
Use offline behavioral tests for occurrence isolation, attribution, null semantics,
mappings, failure isolation, bounds and compatibility. Keep injected semantic tests
separate from real filesystem/platform/worker witnesses. Run focused/full suites,
capability-disabled simulation, real worker lifecycle where relevant, diff checks
and canonical GitLeaks history scan. Actual hosted Windows and other CI remain
post-publication witnesses. Capture exact OASim pre/post state (including existing
untracked bytes/modes and ignored inventory/relevant evidence), require equality,
and run ordinary python3 -m libyears OASIM_ROOT from the trusted checkout. No target
execution or evidence production. Record exact stdout/stderr/exit; no coverage
percentage is required. Eight unsupported populations and strict H3 may rightly
produce unknown/null coverage. Convergence requires independent read-only audit
of R1–R6, tests, docs and smoke. Stop only for new consequential authority.
