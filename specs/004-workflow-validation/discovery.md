# Feature 004 Discovery: Validate the Next User Workflow

## Status

Draft — committed before independent review. This is a recommendation for human
challenge, not an approved product decision. No Feature 004 implementation
direction has been selected.

## Current Capability

Libyears measures direct dependencies when it can connect a declaration to an
exact used version and a public registry release timestamp. It currently
supports Python packages from PyPI and npm packages from the npm registry.

- Python declarations come from `requirements.txt`. Exact `==` pins are
  evidence themselves. Non-exact declarations can use the optional
  `--resolved` snapshot, a narrow `NAME==VERSION` file; declarations determine
  scope and snapshot-only transitive entries are ignored. A snapshot may be
  generated outside libyears, for example with `pip freeze`, but that describes
  the environment used to create it and is not necessarily repository history.
- npm scope is root `package.json` production `dependencies`, excluding names
  also declared in `optionalDependencies`. Root `package-lock.json` v2/v3
  provides selected versions. Feature 003 added root Yarn Classic v1 lockfile
  evidence. If both lockfiles exist, neither is selected. Dev, peer,
  optional-only, workspace, and transitive dependencies remain out of scope.
- A scan can combine Python and npm. Public JSON is schema v3, with
  ecosystem-keyed version evidence and repository plus per-ecosystem summaries.
- A dependency whose version, registry record, or timestamp cannot be safely
  established is listed as `unmeasurable` with a stable reason. A failed,
  malformed, conflicting, or unsupported whole source is represented in
  `source_errors`; where the dependency denominator is known but evidence is
  rejected wholesale, measured count and coverage can be null. This differs
  from an ordinary dependency-level `0/N` result.
- Scanning is static. Libyears does not install packages, execute repository
  code, run package managers, resolve ranges, or calculate a dependency graph.
  Python and npm registry access is isolated in adapters and uses verified
  HTTPS. Without usable registry access, dependencies with exact evidence still
  cannot be assigned release timestamps. The deterministic test suite uses
  local fixtures/mocks; this discovery did not run it.

Deliberate limits include direct-only scope, bounded parsers, no guesses when
evidence is absent or ambiguous, no support for other ecosystems, no generic
resolver or semantic-version engine, and registry dependence for timestamp
authority. README's link to GitHub's dependency page for this repository is not
a repository-local SBOM and does not change those capabilities.

## Inventory Method

The two authorized directory roots were inspected read-only:
`<local-collection-a>` and `<local-collection-b>`. A bounded filename walk
pruned `.git`, `node_modules`, vendor directories, common environments, and
build output; it stopped descending at depth 9 and capped traversal at 250,000
files per root. It counted filenames and selected project-local evidence. It
did not execute repository code or package managers, validate every project,
or inspect dependency contents wholesale. Selected package-lock headers and
versions and selected Python requirements lines were read as metadata.

Counts below distinguish **files** from **project roots**. The two named
directories are the **repository checkouts**; nested project roots are not
independent repositories. A manifest/lock pair suggests a project root but
does not prove that the lock covers every declaration or that a root is an
independent product. Counts are a bounded inventory, not a representative
sample of CMS repositories.

The prior Feature 003 inventory remains useful for its reviewed Go/Maven/Yarn
evidence analysis and recorded 77-dependency dogfood. Some counts differ from
this current walk (for example, it recorded eight <local-collection-b> package-lock files
and 22 POM files; this walk found six package-lock files outside excluded
generated/vendor trees and 21 POM files). This discrepancy is unresolved and
limits exact comparisons. Material format assumptions were rechecked below.

## Repository Evidence

### Current bounded counts

| Evidence | <local-collection-a> files | <local-collection-b> files | Notes |
|---|---:|---:|---|
| `requirements*.txt` / `constraints*.txt` | 9 | 1 | Mostly requirements declarations; not nine/one repositories. |
| `pyproject.toml` | 1 | 0 | `<local-collection-a>/<local-copy-group>/super-changelog/pyproject.toml`; no `uv.lock`, `poetry.lock`, or `Pipfile.lock` found. |
| `package.json` | 8 | 19 | 27 manifest files / candidate roots across the two checkouts. |
| `package-lock.json` paired with a root manifest | 8 | 6 | The inspected locks were npm lockfile v3 in <local-collection-a> (8) and v2 in <local-collection-b> (5), v3 (1). |
| `yarn.lock` | 0 | 3 | `easi-app`, `design-system`, and nested token importer. All have `# yarn lockfile v1` on the second line; the first line alone is a generic generated-file warning. |
| `pnpm-lock.yaml` | 0 | 0 | None found outside pruned generated/vendor trees. |
| `go.mod` / `go.sum` | 0 | 6 / 6 | Six module roots, each with both files; modules are not six repositories. |
| `go.work` / `vendor/modules.txt` | 0 | 0 | Not found in the bounded walk. |
| `pom.xml` | 0 | 21 | Includes parent, aggregator, and child module POMs; not 21 independent projects. |
| Gradle declarations / lockfiles | 0 | 0 | No `build.gradle[.kts]` or `gradle.lockfile` found. |
| `Gemfile` / `Gemfile.lock` | 0 | 4 / 4 | Four same-root pairs under <local-collection-b>/dpc-app. |
| Cargo / .NET project or lock evidence | 0 | 0 | No `Cargo.toml`, `Cargo.lock`, `.csproj`, or `packages.lock.json` found. |
| Candidate SBOM names | 3 | 0 | The three <local-collection-a> matches are code.gov agency-index records naming SBOM-generator projects, not CycloneDX/SPDX artifacts. |

The requirements-file scan found simple exact `==` candidates in two files:
`<local-collection-a>/repo-scaffolder/requirements.txt` and
`<local-collection-a>/<local-copy-group>/repo-scaffolder/requirements.txt` (each contained
`cookiecutter==2.6.0`). These may represent reused or copied project evidence;
they are two files, not two independent deployments. The remaining files did
not yield a simple exact candidate in this text scan; some may contain ranges,
includes, options, or unsupported forms, and were not semantically classified.
The bounded scan does not establish complete Python coverage. The existing
`--resolved` option can fill exact versions for declared packages, but requires
the user to provide a separate snapshot whose relationship to the repository
state must be judged.

Representative paths:

- Python: `<local-collection-a>/repo-scaffolder/requirements.txt`,
  `<local-collection-b>/dpc-app/requirements.txt`, and the lone
  `<local-collection-a>/<local-copy-group>/super-changelog/pyproject.toml`.
- npm: `<local-collection-a>/metrics/{package.json,package-lock.json}` and
  `<local-collection-b>/dpc-app/dpc-impl/{package.json,package-lock.json}`.
- Yarn: `<local-collection-b>/easi-app/{package.json,yarn.lock}`;
  `<local-collection-b>/design-system/yarn.lock` serves a tree with multiple manifests and
  therefore raises project-boundary questions; the nested
  `cmsds-token-importer` has its own manifest and lock.
- Go: `<local-collection-b>/easi-app/{go.mod,go.sum}` and
  `<local-collection-b>/dpc-app/dpc-testing/performance/{go.mod,go.sum}`.
- JVM: `<local-collection-b>/ab2d/pom.xml` and child POMs.
- Ruby: `<local-collection-b>/dpc-app/dpc-impl/{Gemfile,Gemfile.lock}`.

The number of visible project roots is not the number of supported Libyears
repositories. Libyears currently accepts a selected project root and reads
supported root files; it does not recursively scan a checkout and discover
every project boundary.

### Feature 003 reach

Feature 003 changed one material assumption from prior discovery: Yarn Classic
is no longer merely a promising alternative format. Its approved implementation
was exercised against `<local-collection-b>/easi-app`; the Feature 003 release-validation
record says 77 of 77 direct npm dependencies were measured (100% coverage) using
the live npm registry. This is strong evidence that Yarn support added actual
measurement reach for at least one CMS project, not just a parser capability.
It does not show how many of the other two lockfiles are compatible root
projects, nor population-level adoption. The design-system tree still has
workspace/project-boundary ambiguity. Go, Maven, Python, pnpm, and SBOM
assumptions were not changed by Feature 003.

## Observed User Problems

1. **A declaration often does not tell a user what exact release was selected.**
   Python requirements files are common, but simple exact pins were observed in
   only two files. Libyears can use a supplied snapshot, but a user must create
   and retain that evidence and decide whether it represents the repository's
   intended state. This is an observed evidence gap; the inventory does not
   establish how often users need a new Python lock parser.
2. **Many projects in a checkout require explicit root selection.** The
   inventory found multiple manifest roots in both checkouts, while the CLI
   measures a selected root and does not discover a portfolio. A user may need
   repeated invocations or a wrapper. This is a workflow burden, but the right
   project boundaries and cross-project semantics remain unclear.
3. **Registry dependence can prevent a usable measurement.** A valid lock or
   snapshot gives the selected version, but not the authoritative release
   timestamp; scans need the public registry. A live dogfood attempt below
   encountered transport failures. That demonstrates dependence and a failure
   mode in this environment, not that ordinary user environments are commonly
   offline or that a cache is the best remedy.
4. **The current bounded repositories expose a format mismatch between
   prevalence and trustworthy interpretation.** Go and Maven evidence is
   present, but declaration files do not necessarily mean selected versions.
   Adding parsing based on filename prevalence would risk measuring the wrong
   thing.
5. **The next high-value product problem is not established.** Feature 003
   addressed a clear evidence chain and delivered useful reach. This inventory
   did not reveal another comparably strong, low-ambiguity evidence source or
   repeated output defect. Choosing a parser now would mostly be roadmap
   momentum.

No recurring UX defect was established from successful current output. A
network-failed run is not sufficient evidence that reports are generally hard
to interpret. No user-time measurement was made.

## Candidate Directions

The candidates below start with user problems, then consider possible product
responses.

| User problem | Possible direction | Evidence and status |
|---|---|---|
| Users may have Python declarations but no exact selected versions in checked-in files, and snapshot preparation is manual. | Validate a repository-local Python evidence workflow before supporting another Python lock format; possible later support for a format only if present and semantically bounded. | Requirements are common, exact candidates uncommon in this bounded sample; one `pyproject.toml`, no recognized Python lockfile. Need user workflow evidence. |
| Users may need to invoke Libyears separately for each nested project. | Project-root discovery or portfolio orchestration. | Multiple roots observed. Boundary and aggregation semantics unresolved; this may belong in a wrapper or higher-level tool. |
| Existing supported projects cannot get timestamps when registry access fails. | Explicit local metadata cache or offline mode. | All 77 lookups failed in this environment; no user request/cache artifact evidence. Cache provenance, freshness, and security semantics add cost. |
| npm users have exact versions in a common lock source not currently supported. | pnpm evidence. | No pnpm lockfile found in either checkout; no observed reach. Defer. |
| Go users need selected module versions. | Conservative Go module support. | Six `go.mod` + `go.sum` pairs exist, but `go.sum` is integrity evidence and `go.mod` requirements do not alone establish MVS-selected versions. No `go.work`/vendor selected snapshot found. Defer unless a safe local selected-version artifact is evidenced. |
| JVM users need selected artifact versions and timestamps. | Conservative Maven/Gradle evidence. | 21 POMs, no Gradle or dependency lock/report found; inheritance/BOM model ambiguity and timestamp authority remain. Defer. |
| Consumers need interoperable cross-ecosystem dependency evidence. | SBOM ingestion. | No actual SBOM found. Names of SBOM generator projects are not SBOM files. Defer. |
| Downstream automation needs richer trust/provenance. | Expand evidence provenance in schema. | Schema v3 already reports ecosystem, source, version source, counts, and failure reasons. No downstream consumer or missing provenance field was observed. Defer schema change until a real consumer identifies a gap. |
| Users need more direct/indirect coverage or package risk recommendations. | Broaden scope, vulnerability scanning, or update advice. | No observed request or evidence; changes the meaning and boundary of the metric. Reject for this discovery. |
| Users cannot measure a useful project because no validated next need is known. | No-code workflow validation and product clarification. | Supported by the mismatch between many metadata files and few proven evidence chains, plus unresolved project boundaries and no user-demand evidence. Recommended as the next investment. |

## Evidence-Fitness Analysis

The test for a dependency-evidence feature remains:

> direct dependency declaration + exact repository-local selected-version
> evidence + authoritative public release timestamp + static interpretation
> without dependency resolution or package-manager execution

- **Python exact pins:** an exact `==` declaration can supply the used version;
  PyPI supplies release timestamps. Most observed requirements declarations
  did not appear to be exact pins. A generated `pip freeze` file is exact
  environment evidence, not necessarily committed project-resolution
  evidence. It must not silently be treated as historical or project-selected
  truth.
- **Python lock formats:** `pyproject.toml` declarations are not selected
  versions. No `uv.lock`, `poetry.lock`, or `Pipfile.lock` was found in this
  bounded walk. Adding a parser based only on ecosystem popularity would not
  demonstrate reach here. If user evidence later identifies a lock format, its
  declaration-to-lock scope and selected-version semantics need separate
  validation.
- **npm package-lock and Yarn:** direct declarations plus supported lock data
  can provide exact selected versions; the npm registry supplies timestamps.
  Feature 003 dogfood demonstrates this chain for `easi-app`. Its value is
  established, and the remaining Yarn inventory is small and structurally
  ambiguous.
- **pnpm:** no evidence artifact observed. A package-manager lockfile can be
  exact evidence only after format and workspace semantics are specified; its
  existence elsewhere cannot be inferred from npm prevalence.
- **Go:** `go.mod` `require` directives express module requirements, not in
  every case the final selected graph under Minimal Version Selection. `go.sum`
  hashes authenticate content but do not establish the currently selected
  version. The bounded inventory found no `go.work` or `vendor/modules.txt`
  selection evidence. Treating a sum entry as selection would be unsafe.
- **Maven/JVM:** POM literal versions are declarations, while properties,
  parent inheritance, dependency management, and imported BOMs can determine
  effective versions. The inventory found no local resolved report or lock
  artifact to avoid build-model interpretation. The prior discovery also left
  canonical release timestamp authority unresolved. POM presence alone fails
  the evidence test.
- **Ruby:** matched Gemfile/Gemfile.lock pairs were observed, but no Ruby
  ecosystem support or authoritative timestamp model is established by this
  inventory. A pair is a candidate for a future separate investigation, not
  enough to recommend an ecosystem.
- **SBOMs and generated reports:** no actual SBOM or generated resolved
  dependency report was found. The three filename matches are agency-index
  descriptions of SBOM generator projects. An SBOM may contain selected
  versions but its provenance, component scope, and timestamp source would
  still need a carefully bounded evidence model.

Integrity hashes, declared minimums/ranges, and generated evidence are not
interchangeable. This discovery rejects the unsafe shortcuts of interpreting
Go sums as selected versions, POM declarations as effective versions, or a
current environment snapshot as repository history.

## Candidate Comparison

Ratings are qualitative judgments about this bounded evidence, not ROI or
population estimates. Reach is included as evidence strength rather than an
adoption claim.

| Candidate and user problem | Observed evidence / reach | Evidence fitness | Complexity | Semantic risk | Product-boundary fit | Recommendation strength |
|---|---|---|---|---|---|---|
| **Workflow validation (recommended):** the project does not yet know which recurring user problem deserves the next implementation. | Two checkouts; several evidence gaps; one proven Yarn win; no user-demand evidence or user-time measures. | HIGH for learning; no evidence parser is assumed. | LOW–MEDIUM: focused user workflow evidence and a clarified product decision. | LOW. | HIGH: product discovery stays with Libyears maintainers. | MEDIUM; strongest responsible next investment, not an implementation feature. |
| **Python exact-evidence usability:** Python declarations often lack selected versions and snapshots require manual preparation. | 10 requirement/constraint files; simple exact pin candidates in 2; no common lock artifacts observed; one pyproject. | MEDIUM for existing exact pins and supplied snapshot; LOW for a new parser absent identified lock evidence. | MEDIUM–HIGH depending on evidence format and compatibility rules. | MEDIUM: confusion between environment and repository state. | HIGH if narrowly evidence-based. | LOW–MEDIUM; runner-up for validation, not yet for implementation. |
| **Offline/cache support:** users cannot obtain release dates without public registry access. | This run failed 77/77 registry calls; no evidence this is frequent outside the restricted environment. | MEDIUM if cache records authoritative metadata with provenance; freshness and missing timestamps remain. | HIGH: cache format, invalidation, trust, privacy, network behavior. | MEDIUM–HIGH. | MEDIUM; can remain adapter-side but expands state and user expectations. | LOW until user demand is confirmed. |
| **Project-root/portfolio workflow:** users repeat invocations or cannot understand repository boundaries. | 27 npm manifest files, nested Python/Go/JVM/Ruby roots; two repository checkouts. | Not an evidence-chain extension. | MEDIUM–HIGH due to discovery, exclusion, aggregation, and reporting. | HIGH for denominator/aggregation comparability. | LOW inside the core single-project metric; stronger above/beside it. | LOW; defer as Libyears feature. |
| **Go selected-version evidence:** Go users cannot measure dependencies from module evidence. | Six module roots with go.mod/go.sum, no selected graph artifact observed. | LOW for current files; sum is integrity, requirement may differ from selected version. | HIGH for static graph interpretation or additional artifact support. | HIGH. | MEDIUM only with a reliable selected-version artifact. | LOW; reject current evidence shortcut. |
| **JVM selected-version evidence:** POM-heavy projects remain unsupported. | 21 POM files, no lock/reports identified. | LOW: declarations need effective model and canonical timestamp authority remains uncertain. | HIGH. | HIGH. | LOW–MEDIUM; risks build-system interpretation. | LOW. |

## Product-Boundary Analysis

Libyears should remain a small, static, explainable metric tool. It should not
become a dependency resolver, package-manager emulator, build-system
interpreter, portfolio analytics service, vulnerability scanner,
update-recommendation engine, package-health score, or generalized SBOM
platform merely because those tools encounter dependency metadata.

Portfolio invocation may help users, but it adds project detection and
cross-project comparability semantics that the metric has not defined. A
thin external script or orchestration tool can own that workflow while
invoking Libyears once per known root. A future product discovery can revisit
it if users demonstrate a recurring need and propose meaningful boundaries.

Vulnerability and package-health questions require different data and
interpretation than release age. Recommendations can be generated by adjacent
tools that consume Libyears output, but should not be implied by a high age
score. SBOM production/interchange is also broader than reading a narrow,
validated source as evidence for direct dependencies.

## Surprising Findings

- **Yarn materially increased CMS measurement reach.** Feature 003 release
  validation recorded 77/77 measurable direct dependencies in `easi-app`.
  Thus Yarn support was not merely format coverage. The bounded current walk
  confirms three Yarn lock files, but only the `easi-app` pairing is clearly a
  single root; the design-system tree and token importer need boundary review.
- **Another npm evidence source is not yet more valuable than another
  ecosystem.** pnpm did not appear in either bounded checkout. Existing Yarn
  support has a demonstrated 77-dependency result; no comparable pnpm demand
  or artifact was observed.
- **Python remains nominally supported but can be under-measurable from
  declarations.** Requirements files are present, while simple exact pins were
  found in two files. The supported snapshot path can address non-exact
  declarations, but requires a user-supplied environment snapshot and may not
  represent repository state. This makes Python workflow validation stronger
  than speculative parser selection.
- **No repository-local generated Go/Maven evidence solved prior gaps.** The
  bounded walk found six Go module pairs but no workspace or vendor selected
  inventory, and 21 POM files but no Gradle lock or dependency report.
- **No actual SBOM appeared.** The three SBOM-name matches are code.gov agency
  index records for generator projects. The README's GitHub dependency-page
  link is not an SBOM file in these checkouts.
- **Provenance already exists at a useful baseline.** Schema v3 reports
  declaration/evidence sources and per-dependency `version_source`; source
  errors and unmeasurable dependencies are separate. No downstream consumer
  exposed a specific missing provenance field. A schema addition now would be
  speculative.
- **Network dependence is concrete; demand for an offline mode is not.** A
  current scan of the supported `easi-app` root recognized all 77 declarations
  and Yarn lock selections, but measured 0/77 because registry requests failed
  with `registry_error` in this environment. Feature 003's earlier live run
  measured 77/77. Together these confirm that registry access determines
  timestamp availability and that results can differ by environment; they do
  not establish a widespread offline-user problem. No cache or network-free
  timestamp source was present in the inspected repositories.
- **Manual preparation and project-root selection are plausible friction,
  not yet demonstrated user pain.** The evidence inventory exposes multiple
  roots, but did not observe actual user scripts, errors, or requests. There
  was no repeated UX problem in successful Libyears output to justify output
  expansion.
- **Direct-production-only npm scope remains defensible.** The inventory does
  not show that users need dev, peer, optional-only, workspace, or transitive
  dependencies included in the same metric. Expanding it would change the
  denominator and the meaning of comparable reports.

## Recommended Direction

### Problem

The evidence does not currently distinguish a high-value recurring user
problem from several plausible but costly extensions. Existing user metadata
shows gaps, but not which gaps prevent real workflows or what repository
evidence users can provide safely.

### Evidence

The strongest product evidence is the successful Feature 003 result: Yarn
Classic made an existing npm root with 77 direct declarations fully measurable.
Beyond that, the inventory shows Python declarations with few simple exact
pins, many nested project roots, unsupported Go/JVM metadata, and no actual
SBOMs. The current dogfood attempt found all 77 exact Yarn versions but no
timestamps because this environment could not reach the npm registry. None of
those facts alone identifies the next feature.

### User outcome

Users and maintainers can identify whether the next meaningful limitation is
Python version evidence, registry access, repeated project-root selection,
another evidence format, or something not visible in these two checkouts.
That answer would make a subsequent feature smaller and more likely to solve
an observed problem.

### Why now

Feature 003 completed a strong npm evidence extension and made the next
roadmap-shaped choices tempting. The bounded inventory does not support
choosing pnpm, Go, Maven, SBOM, portfolio scanning, or a new schema field by
prevalence alone. A short workflow-validation investment prevents premature
parser and semantic commitments.

### Why this belongs in libyears

This is a product-discovery investment rather than a runtime capability. It
belongs in the Feature 004 discovery/specification process because the core
uncertainty is what Libyears should measure and what evidence users trust. The
result may be a no-code decision, a narrowly evidenced feature, or a conclusion
that an adjacent tool should own the workflow.

### Smallest useful scope

Ask a small number of actual users/maintainers to walk through one recent
measurement attempt and identify: the project root, declaration/evidence
files, whether registry access was available, what result they needed, and
where manual work or ambiguity occurred. Compare responses against existing
README guidance and the observed repository evidence. Record anonymized
patterns and counterexamples, then decide whether any single problem has enough
evidence for a specification. Do not collect package lists, credentials, or
private registry configuration.

### Explicit non-goals

- No new parser, ecosystem, evidence format, dependency scope, or schema field
  is approved by this recommendation.
- Do not infer selection from hashes, declarations, or a transient environment.
- Do not add registry caching, offline timestamp substitution, project
  aggregation, vulnerability findings, or update recommendations during this
  validation.
- Do not treat the bounded CMS inventory as a representative prevalence
  survey.

### Principal risks

- A small qualitative sample can miss important users and over-weight the
  loudest workflow.
- User reports may suggest formats that still fail the exact-evidence or
  static-analysis test.
- The no-code recommendation may defer a demonstrably useful parser if a
  strong user need is already known outside this repository evidence.
- Research itself consumes human attention; keep it bounded and tie every
  follow-up to an observable decision.

### Questions requiring human judgment before specification

- Is there an established user group or known workflow problem not represented
  in these two repositories?
- Which user outcome matters most: exact coverage, repeatable timestamps,
  fewer manual invocations, offline operation, or another goal?
- What evidence do users already produce and trust for Python and other
  ecosystems?
- Are users measuring one selected project root, many roots, or release/build
  environments, and what constitutes the denominator they care about?
- Is the current public registry dependency acceptable for intended use, or is
  offline/reproducible operation a real requirement?
- What is the smallest useful evidence of demand that should trigger a
  substantive Feature 004 specification?

## Runner-Up

Validate and improve Python exact-version evidence usability. This is the most
plausible product capability candidate because requirements files are common,
exact pins were uncommon in this sample, and `--resolved` asks users to supply
environment-derived evidence. It should win over workflow validation if users
confirm that this is a recurring blocker and identify repository-local exact
evidence that is both common and safe to interpret. No specific Python lock
format is recommended from the current inventory.

## Explicitly Deferred

The tempting option is **Go support**, because six `go.mod`/`go.sum` pairs
provide a visible ecosystem footprint. It remains deferred: `go.sum` is
integrity evidence, and the observed `go.mod` requirements do not by themselves
establish the selected versions. Go should move ahead only if user need and a
safe repository-local selected-version artifact or tightly bounded evidence
model are established.

Portfolio scanning is also deferred from Libyears core; repeated invocation
may be better handled by a wrapper. pnpm and SBOM ingestion lack observed local
artifacts. Maven has high file counts but weak static evidence fitness and
unresolved timestamp authority.

## What Would Falsify This Recommendation

The recommendation assumes that no stronger, already-known user need exists
outside the bounded repository evidence; that two CMS checkouts are useful but
not representative; and that user workflow information can be gathered
cheaply enough to affect product choice.

Evidence that would make this recommendation wrong:

- Existing support requests or user interviews already establish one urgent,
  recurring limitation with a clear safe boundary.
- Users consistently identify Python snapshot preparation as the blocking
  task and point to one repository-local lock/evidence format already produced
  by their projects. In that case the Python runner-up should win and proceed
  to evidence-specific discovery.
- Users consistently report registry access restrictions or repeated
  identical scans as the blocker, and can identify an authoritative metadata
  artifact or acceptable cache freshness/provenance model. Then offline/cache
  work may be stronger.
- A broader, authorized inventory finds pnpm or another exact lock source in
  many relevant roots with direct declarations and clear selected versions.
  That could displace Python workflow work, subject to the full evidence test.
- A validated generated Go/JVM report is already produced in repositories and
  records selected versions without executing build systems at scan time. That
  could reopen those ecosystems.
- Users' actual task is repeatedly measuring many nested roots, with clear
  project boundaries and no need for cross-project aggregation. A root-listing
  or orchestration feature could then be useful, though it may still belong
  above the metric core.
- Successful registry-backed output reveals a recurring interpretation or
  provenance failure not found in this scan.

The current 0/77 live measurement is not sufficient on its own to make the
offline candidate win: the earlier 77/77 run on the same root shows the
registry path can work, and this attempt reflects the current execution
environment.

## Process Observations

Prior artifacts made this investigation substantially easier. Feature 003's
discovery preserves its earlier portfolio recommendation, human challenge,
Go/Maven/Yarn evidence comparison, explicit boundaries, and rationale for
deferring SBOM. Its reviews preserve specification, architecture, task-graph,
and convergence findings. Its retrospective points directly to the draft
before review experiment used here. Feature 002's retrospective explains why
that durable decision trail matters.

Missing information included user demand outside these checkouts, how users
currently choose project roots, whether Python snapshots are actually
prepared, and why users would need offline results. The inventory also had a
count discrepancy with Feature 003's original bounded walk. This required
additional repository archaeology to verify lock versions, Yarn headers,
Python pin examples, and whether apparent SBOM hits were artifacts or merely
generator references. No external directories beyond the two authorized roots
were inspected.

The Feature 003 retrospective recommendations appear useful: the discovery and
review artifacts made the initial direction and later challenge reconstructable,
and committing this draft before challenge will preserve its exact reviewed
starting state in Git. That improves process evidence, but does not make the
product recommendation more certain. Independent review has not occurred.
