# Feature 003 Discovery: Yarn Classic Lock Evidence

## Status

Discovery approved; ready for specification.

Feature 003 is directed toward Yarn Classic v1 exact-version evidence for the existing npm ecosystem. The discovery direction and product decisions below are approved; user-visible behavior and acceptance criteria remain to be defined in `spec.md`.

## Current Libyears Capability

- Measures direct Python/PyPI and npm dependencies.
- Python evidence comes from root `requirements.txt` exact pins and an optional `--resolved` snapshot for declared Python requirements.
- npm declarations come from root `package.json` production dependencies; exact evidence comes from root `package-lock.json` v2 or v3.
- Measurement requires exact repository evidence and public registry release metadata. Registry requests use verified HTTPS.
- Scans are static: libyears does not install dependencies, execute package managers, resolve ranges, or run repository code.
- Direct dependencies are the default scope; unsupported or ambiguous evidence fails closed and affects coverage rather than being guessed.

The README describes the current mixed PyPI/npm behavior. Feature 002's specification, plan, and tasks define npm package-lock behavior and schema v3.

## Initial Repository Inventory

### Method and limitations

The first pass searched dependency-manifest and lock/evidence filenames to depth 6 under only `<local-collection-a>` and `<local-collection-b>`. It pruned `.git`, `node_modules`, vendor and common generated/build directories. Selected Python requirements files and representative Go, Maven, and Yarn files were then read as static metadata. No repository code or package manager was executed.

Counts below are **files**, not repositories, independent products, or validated project units. A monorepo can contain multiple modules and manifests; one lockfile may serve several manifests. The inventory is bounded, does not validate every lockfile or resolve every dependency, and is not a representative statistical sample of CMS repositories.

### Observed evidence

- **Python declarations:** 10 declaration files in `<local-collection-a>` and 1 in `<local-collection-b>`, primarily `requirements.txt`. The sample contained no `pyproject.toml`, Poetry/uv lockfile, or Pipfile evidence. A simple scan of inspected requirements files found exact `==` pins in only two files; that is not a complete measure of Python dependency measurability.
- **npm:** `<local-collection-a>` had 8 `package.json` files paired with 8 `package-lock.json` files. `<local-collection-b>` had 19 `package.json` files and 8 `package-lock.json` files. These are file-pair counts, not a determination that each lock covers every declared production dependency.
- **Yarn:** Three Yarn lockfiles were found in `<local-collection-b>`: `easi-app/yarn.lock`, `design-system/yarn.lock`, and `design-system/packages/design-system-tokens/sketch/cmsds-token-importer/yarn.lock`. All inspected lock headers identify Yarn Classic lockfile v1. `easi-app` has a clear root manifest/lock pairing. The design-system tree has multiple package manifests and a tree-level lockfile; project/workspace boundaries need care. The token importer has a local manifest and lockfile.
- **JVM:** 22 `pom.xml` files in `<local-collection-b>`, including modules under `ab2d` and `dpc-app`. These include aggregator and child POMs, not 22 necessarily independent projects.
- **Go:** 6 `go.mod` files in `<local-collection-b>`, each accompanied by `go.sum` in the inventory. These are module files, not six necessarily independent repositories.
- **Ruby:** Four `Gemfile` files and four matching `Gemfile.lock` files in `<local-collection-b>`.
- **SBOM:** No actual SBOM artifacts were identified. Three filenames matching `*sbom*` were code.gov agency-index JSON records for SBOM-generator projects, not CycloneDX or SPDX bills of materials.
- No Rust or .NET dependency evidence was found in the bounded filename scan.

Representative paths include `<local-collection-a>/metrics/{requirements.txt,package.json,package-lock.json}`; `<local-collection-b>/easi-app/{go.mod,go.sum,package.json,yarn.lock}`; `<local-collection-b>/ab2d/pom.xml`; and `<local-collection-b>/dpc-app/dpc-impl/{package.json,package-lock.json,Gemfile,Gemfile.lock}`.

The initial reach estimate was at least 16 npm manifest/lockfile directory pairs and two requirements files containing a simple exact-pin candidate, subject to actual matching and registry success. This estimate should not be read as a count of fully measurable repositories.

## Initial Candidate Evaluation

The first pass considered these plausible investments:

| Candidate | Evidence and concern |
|---|---|
| Portfolio scanning | Many nested dependency-bearing directories were observed, but cross-project aggregation semantics and user workflow were unestablished. |
| Additional Python evidence | Requirements files were common, but exact pins were uncommon in the inspected files. Broader filenames alone may not improve measurement; lock formats need scope/provenance rules. |
| Yarn lock evidence | Three Yarn v1 lockfiles were observed. A lockfile can provide exact versions for existing npm declarations and reuse npm release metadata. |
| Go modules | Six module files were observed. `go.mod` has concrete requirements, but Go's Minimal Version Selection means a requirement may not be the selected version. |
| Maven/JVM | 22 POM files were observed, but inheritance, properties, dependency management, and BOMs complicate static exact-version evidence. |
| SBOM ingestion | Could span ecosystems, but no actual SBOM artifacts were found in the bounded inventory. |
| Registry caching/offline metadata | May address network friction, but cache freshness, provenance, and observed demand were not established. |
| Dependency-scope controls | Could expose more dependencies, but changing direct-only scope risks changing what the metric means and how reports compare. |
| Portfolio/UX/provenance improvements | Could reduce manual work or ambiguity, but need concrete user workflows and carefully bounded output semantics. |

The first discovery pass recommended portfolio scanning of explicitly supplied local roots. This was a provisional recommendation, not an accepted product decision.

## Human Product Review

Human product review did **not** accept portfolio scanning immediately. The review challenged whether orchestration belongs in libyears: it moves the tool from a single-project metric toward a multi-project analytics layer, and meaningful cross-project aggregation semantics had not been established.

A focused feasibility investigation of Go, Maven, and Yarn was requested. This follow-up compared evidence fitness rather than selecting the candidate with the most manifest files. The initial recommendation was retained in this record so the decision journey remains visible.

## Focused Evidence-Fitness Investigation

The core test was:

> direct dependency declaration + exact repository-local version evidence + authoritative public release timestamp + static interpretation without package-manager execution or dependency resolution

### Go

Representative `go.mod` files contain concrete `require` versions. Entries marked `// indirect` identify indirect requirements. The sample also contains pseudo-versions and one local `replace` directive in `<local-collection-b>/dpc-app/dpc-testing/performance/go.mod`; no `go.work`, `exclude`, or `retract` directives appeared in the inspected modules.

`go.sum` records cryptographic hashes for module versions and module files. It is integrity evidence, not a trustworthy list of currently selected versions; it can contain multiple versions and versions no longer needed by the current build. Go's Minimal Version Selection can select a higher version than an individual `require` line, while `replace` can substitute different source. The public Go module proxy `.info` endpoint can provide version metadata and a creation time, but the official reference says the time is optional and that version metadata is unauthenticated and may change. See the [Go Modules Reference](https://go.dev/ref/mod) and [Go module version numbers](https://go.dev/doc/modules/version-numbers).

**Conclusion:** Go is a valuable future ecosystem candidate, but the observed repository evidence does not safely establish exact selected versions without additional interpretation of the module graph or a separately specified evidence model.

### Maven

Representative POMs showed a mixture of version forms:

- Literal child dependency versions, such as `3.3.1` in `ab2d/api/pom.xml`.
- Property-based versions, such as `${okta-jwt.version}` in that same file.
- Child dependencies with no version, relying on inherited or managed versions.
- Parent `dependencyManagement` entries and an imported BOM in `<local-collection-b>/dpc-app/pom.xml`.
- Aggregator POMs with multiple child modules.

The representative files showed no resolved lockfile evidence. The bounded inventory found no Maven dependency lockfile. The limited sample did not show dynamic version ranges; this is not a claim that none occur in all 22 POMs. Maven Central's Search REST API supports version-specific artifact searches, but its official guide does not establish the `timestamp` field as a canonical release timestamp. The search index can also lag publication. See [Central Search REST API](https://central.sonatype.org/search/rest-api-guide/) and [Sonatype's search-index update note](https://central.sonatype.org/faq/what-happened-to-search-maven-org/).

**Conclusion:** Maven has high observed file prevalence but a useful conservative subset would omit many managed dependencies. Broader coverage would drift toward Maven effective-model and resolution behavior, while canonical timestamp authority remains insufficiently established.

### Yarn Classic v1

Three Yarn lockfiles were observed, and inspected headers identify all as Yarn Classic v1. The `easi-app` root manifest and lockfile provide a representative pairing: `package.json` declares dependencies, while `yarn.lock` has exact `version` entries keyed by package name and requested selector. Scoped selectors appear in quoted lock keys such as `"@apollo/client@^3.10.7"`.

The existing npm registry adapter can supply release timestamps. The npm registry's public metadata describes per-version publication times in the package `time` map ([npm Registry API](https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md)). Yarn Classic lockfiles therefore provide a plausible static exact-version source without running Yarn. Aliases, non-registry protocols, selector ambiguity, and multi-package/workspace layouts still require conservative handling. Yarn Berry/PnP was not observed in the inspected examples and need not be included in a v1 scope. See [Yarn Classic lockfile documentation](https://classic.yarnpkg.com/en/docs/yarn-lock).

**Conclusion:** Yarn Classic v1 has the strongest fit with libyears' existing evidence model. It is another repository-local exact-version evidence source for npm, not a new package ecosystem.

## Decision

Feature 003 direction:

**Yarn Classic v1 exact-version evidence for npm dependencies.**

This adds another repository-local exact-version evidence source for the existing npm ecosystem. It is not a new ecosystem. The direction is selected for specification work; user-visible behavior and acceptance criteria remain to be defined and approved in `spec.md`.

## Why Yarn

- It provides the strongest observed chain from a direct npm declaration to exact repository-local version evidence and public release timestamps.
- The lockfile contains resolution results, so libyears need not execute Yarn or resolve npm ranges.
- Existing npm registry metadata handling can be reused.
- A Yarn Classic v1-only parser is a bounded investigation target; unsupported or ambiguous forms can fail closed.
- It provides useful architectural learning about supporting multiple exact evidence formats within one ecosystem.

Observed reach is modest: three Yarn v1 lockfiles were found in the bounded inventory, with only some project-boundary relationships examined. No adoption or organizational priority is inferred from those files.

## Deferred Alternatives

### Portfolio scanning

Potentially useful later, likely at a higher orchestration layer unless a concrete workflow establishes meaningful cross-project aggregation semantics.

### Go

Promising future ecosystem, contingent on authoritative repository-local selected-version evidence or a deliberately specified interpretation model.

### Maven

Deferred because useful coverage would require substantial Maven model interpretation and timestamp authority remains insufficiently established.

### SBOM

Deferred because the bounded inventory found no actual SBOM artifacts.

### Other candidates

Broader Python lockfile support, registry caching, dependency-scope controls, and additional portfolio/reporting UX remain possible future work, but this discovery did not establish a stronger evidenced problem for them.

## Approved Scope Decisions for Specification

The following decisions are approved for specification:

1. Read root `package.json` and root `yarn.lock` only.
2. Support Yarn Classic lockfile v1 only.
3. Exclude workspace aggregation.
4. Exclude Yarn Berry/PnP.
5. Never execute Yarn.
6. Never resolve npm ranges or selectors during scanning.
7. Fail at the narrowest level justified by the evidence. An individual npm declaration that cannot be safely mapped through Yarn evidence is dependency-level unmeasurable and must not invalidate other measurable npm dependencies. A malformed or unparseable Yarn lockfile is a source-level `invalid_lockfile` error. A valid but unsupported Yarn construct is not an invalid lockfile.
8. Keep the npm registry as the release metadata authority.
9. Use `version_source = yarn_lock` for measured versions.
10. Identify the evidence format as `yarn_lock_v1`.
11. Keep `--resolved` Python-specific; it does not select Yarn evidence.
12. If the root npm project contains both `package-lock.json` and `yarn.lock`, treat this as a source-level resolution-evidence conflict with stable reason `conflicting_resolution_sources`. Do not choose, prioritize, reconcile, or compare the lockfiles, even if their observed versions agree. Root `package.json` direct declarations may still be discovered, but neither lockfile supplies usable exact-version evidence and no registry measurement is performed from either source. npm coverage is null; repository-wide coverage is null for a mixed scan. Successful measurements from other ecosystems survive. Human and JSON output identify the conflict.
13. Null coverage in this conflict case is deliberate. Although the declaration count may be known, reporting `0/N` would misleadingly describe dependency-level measurement failures instead of rejection of the npm resolution-evidence source.

For Yarn evidence failures at the dependency level:

- A supported selector with one unambiguous Yarn v1 entry may supply its exact version.
- An unsupported dependency source or protocol uses `unsupported_dependency_source`.
- A supported declaration with no matching lock entry uses `lock_version_missing`.
- Ambiguous or conflicting evidence for one dependency uses a generic stable conflict reason if the existing taxonomy does not express the semantics precisely. Its exact identifier may be finalized during specification clarification.

## Remaining Discovery Questions

No remaining product question blocks drafting `spec.md`. The exact stable identifier for an individual dependency's ambiguous/conflicting Yarn lock evidence may be finalized during specification clarification.
