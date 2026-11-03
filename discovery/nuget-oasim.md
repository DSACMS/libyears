# NuGet / OASim opportunity discovery

**Disposition: bounded discovery COMPLETE; recommended radar state EXPLORE.**
Research date: 2026-11-03. This is pre-selection opportunity evidence, not
Feature 006 selection or authority to draft its specification or implementation.
OASim demonstrates declarations but **no safely measurable population today**.
The next gate is a human decision about further bounded evidence collection.

## Signal, authority and method

The commissioning human reports that a team is outbounding a .NET/NuGet project
this month. This is a concrete workflow signal, not independently verified
adoption, delivery, demand magnitude or a promise of libyears support.

Read-only access was authorized only to OASim's dependency-related artifacts and
relevant repository metadata. Multiple project files within that root were
permitted. No ancestor/sibling repository, user or machine configuration,
credential store, application code or package cache was inspected. The parent
inspected only dependency-source sections of the two repository NuGet configs;
credential nodes were not inspected and alternate endpoint values are withheld.
No dotnet, NuGet, package manager, restore, build, test, publish or project-code
execution occurred. Nothing was installed, resolved or modified in OASim.

Three fresh researchers independently examined repository evidence, official
ecosystem semantics and libyears evidence-model fit. Parent synthesis followed
all three reports and independently checked important repository and official
documentation claims. Public research used Microsoft Learn; no package metadata
lookup, archive download or alternative-feed request was performed.

## OASim facts at the inspected revision

HEAD was `1e937015e1d242fee5597ea0fbdc4cd5c983f101`; initial and final Git
porcelain status were empty. The solution is
`SRTRMatchRunApplication/SRTRMatchRunApplication.sln`. It lists ten SDK-style C#
projects and one installer project; installer contents were not inspected.
Each C# file has `Sdk="Microsoft.NET.Sdk"`.

Paths below are relative to `SRTRMatchRunApplication/`; the project file is
`NAME/NAME.csproj`. Counts are literal declarations, not evaluated populations.

| Project | PackageReference lines | Count | ProjectReference count |
|---|---|---:|---:|
| MRCalc | 59–67 | 9 | 1 |
| MatchRunBenchmarks | 11–12 | 2 | 2 |
| MatchRunCLI | 16–23 | 8 | 1 |
| MatchRunEngine | 11–14 | 4 | 0 |
| MatchRunProfileUpdater | 9 | 1 | 0 |
| MatchRunProfiling | 11–12 | 2 | 2 |
| MatchRunTests | 10–14 | 5 | 4 |
| OASim | 60–68 | 9 | 2 |
| OASimCLI | 10–18 | 9 | 2 |
| SimulationEngine | 9–10 | 2 | 1 |

The **51 explicit PackageReference occurrences** contain **24 unique package
IDs and 24 unique ID/requirement pairs**. All use literal Include and Version
attributes. Examples are `Avalonia / 0.10.19`, `CoreCLR-NCalc / 3.1.253`,
`Serilog / 4.2.0`, `Microsoft.Extensions.Configuration / 10.0.14` and
`xunit / 2.9.3`. These strings are requirements, not observed selections.
No bracket-exact requirement, floating pattern, dependency condition,
property-based package version, PackageReference Update or VersionOverride was
observed. The xunit runner has PrivateAssets/IncludeAssets metadata; it remains
an explicit reference in its declaring test project.

All ten projects name only `net10.0`. MRCalc and OASim use TargetFrameworks with
that single value; eight use TargetFramework. Three projects contain an older
`Release|netcoreapp3.1|AnyCPU` condition on OutputPath, not dependencies. There
are **15 ProjectReference edges**. Neither these edges nor solution membership
defines one NuGet dependency denominator.

Hidden/ignored-inclusive filename searches found no `packages.config`,
`packages.lock.json`, project-named lockfiles, `project.assets.json`, generated
NuGet props/targets or dgspec, `.deps.json`, `Directory.*` files or `global.json`.
No explicit Import, central-management declaration, custom lock-path property
or lock opt-in was observed in the project files. `.gitignore` excludes obj/bin
and generated NuGet props/targets; ignore rules do not prove that these files
were generated. Absence claims apply to this checkout and searched
artifact families, not arbitrary custom files or external build inputs.

Two tracked configs occur under MRCalc and OASim. Each packageSources section
adds one HTTPS endpoint outside nuget.org, without a clear element; neither
contains packageSourceMapping. This does **not** prove a private origin or that
either config was effective for a particular restore. It does prevent assuming
exclusive nuget.org authority. Other projects have no observed in-root config;
that absence does not establish their effective source set.

All inspected projects, the solution, `.gitignore` and both configs match their
tracked HEAD bytes. The 14-file integrity manifest SHA-256 is
`c21dcac8ed8405194671294b5d2fe6c3d4c647ae927fd7d6e6aad271372ace4c`:
SHA-256 of UTF-8 compact JSON mapping sorted repository-relative paths to their
SHA-256 hashes (`sort_keys=True`, separators `(',', ':')`). Researcher A also
matched before/after hashes for its twelve inspected project/solution/ignore
files. This verifies permitted metadata, not an audit of all application bytes.

**Interpretation:** explicit declarations are discoverable statically; the
effective MSBuild graph is not established. SDK imports and ancestor effects
remain unexamined. A public-sounding package name proves neither source nor
selection. No registry request can repair these missing local facts.

## Authoritative ecosystem semantics

The following general claims come from official documentation retrieved on the
research date; they are separate from the repository observations above.

| Artifact | Evidence meaning and important boundary |
|---|---|
| PackageReference | Declared project requirements. A bare numeric Version is a minimum with lowest-applicable preference, not a resolved pin. Conditions can affect membership. SDKs can add implicit references. PrivateAssets controls propagation, not direct membership in its declaring project. [PackageReference reference](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files) |
| Version syntax | `[1.0]` is exact; `1.0` is an inclusive minimum. Ranges and floating patterns are requests. NuGet normalization and four-part versions require ecosystem-specific care. Even an exact requirement is not evidence of a successful restore. [Version reference](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning) |
| packages.config | Records exact install/restore versions; allowedVersions controls updates. Its targetFramework values may reflect earlier installation contexts. [Schema](https://learn.microsoft.com/en-us/nuget/reference/packages-config). It is a flat direct-and-transitive list, so it alone cannot supply a direct-only population. [Microsoft source-mapping guidance](https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping#manual-onboarding) |
| PackageVersion / CPM | Central version requirements combine with project references; entries alone are not project membership. The nearest Directory.Packages.props is automatically imported; additional parents require imports. Conditions, overrides, global references and transitive pinning complicate scope; pinning can implicitly promote a dependency. [Central Package Management](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management) |
| project.assets.json | Generated resolution graph, normally temporary under obj; not recommended for source control. It records a restore's result, not current-file freshness or successful deployment. [Dependency resolution](https://learn.microsoft.com/en-us/nuget/concepts/dependency-resolution) |
| packages.lock.json | Opt-in, versioned persisted closure including transitives. Normal restore can update it; locked mode restores recorded packages or fails on changed dependencies. A library lock does not control its consumer's resolution. [Locking dependencies](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files#locking-dependencies) |

Freshness conclusions are inferences from those documented lifecycles: neither
committing generated state nor finding a lock proves it matches current inputs.
Floating requests can select from a local cache; querying today's public feed
cannot reconstruct the historical selected version. [Resolution rules](https://learn.microsoft.com/en-us/nuget/concepts/dependency-resolution#floating-versions)

NuGet config settings accumulate across scopes, and project versus solution
invocation can change which configs apply. No such effective environment was
reconstructed here. [Common configurations](https://learn.microsoft.com/en-us/nuget/consume-packages/configuring-nuget-behavior)

## Evidence-chain candidates and rejection boundaries

Libyears already distinguishes declaration scope, exact selection and source
authorization: [Yarn association](../specs/003-yarn-lock-evidence/spec.md),
[Ruby snapshot authority](../specs/004-rubygems-support/spec.md), and
[Gemfile association and limitations](../specs/005-gemfile-group-scope/spec.md).
Those contracts do not authorize a NuGet interpretation by analogy.

1. **Project declarations plus a retained lock:** potentially establish an
   explicitly bounded project/context population and recorded exact versions
   without executing tooling. Preconditions are a supported complete artifact,
   identified project/framework context, distinguishable direct identities,
   consistent declaration/requirement association, documented snapshot origin
   and independent public-source authorization. Actual lock-format witnesses
   and disagreement handling remain unvalidated; no such lock exists here.
2. **Project declarations plus supplied restore assets:** potentially establish
   selected versions for the producing restore. This would need explicit product
   acceptance of supplied restore-state claims, producer/context provenance and
   static association checks. Generated state alone cannot establish coherence
   with current inputs. No such assets exist here.
3. **Exact requirements or packages.config alone:** cannot be relabeled as
   successful selected-version evidence. packages.config additionally loses the
   direct/transitive boundary. A hypothetical declaration-only measurement would
   be a new product choice, not a discovery shortcut.

Association must retain project and framework context; matching an ID anywhere
in a closure does not establish directness. Imported/conditional ambiguity may
make scope unavailable, whereas a known supported direct identity with absent
selection may be unmeasurable. These are candidate evidence distinctions, not
new reason identifiers or approved coverage semantics.

## Public-source and publication-date gates

A public V3 service index and registration API exist. Nuget.org's index is
`https://api.nuget.org/v3/index.json`; resource URLs are advertised there and
can use different hosts. [Service index](https://learn.microsoft.com/en-us/nuget/api/service-index)
An eventual adapter would need approved public authorities and verified HTTPS,
not destinations copied from project config or arbitrary metadata links.

Package IDs/versions are not origin proof. Microsoft documents nondeterminism
when several feeds contain a package. Mappings restrict eligible download
sources, may allow several, and are ignored for already cached packages.
Thus routing policy alone does not prove historical download origin.
[Source mapping](https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping)
A future contract must define sufficient public authority without reading user
credentials or silently substituting public namesakes. The inspected OASim
files do not meet an established such contract. Hash presence alone is not a
decision about source authority.

Registration supports version metadata, pagination and a SemVer-2-capable
resource; published/listed fields have caveats, including year-1900 published
sentinels on nuget.org for unlisted packages.
[Registration API](https://learn.microsoft.com/en-us/nuget/api/registration-base-url-resource)
The flat-container version list includes unlisted releases and supplies no
publication-date field. [Package-content API](https://learn.microsoft.com/en-us/nuget/api/package-base-address-resource)

Catalog metadata distinguishes optional created (first receipt by the source),
published (last listing), and catalog commit time. Deletion events have different
meaning; catalog support is not universal.
[Catalog API](https://learn.microsoft.com/en-us/nuget/api/catalog-resource)
Consequently neither sentinel, relisting nor ingestion time may silently become
original release time. A bounded usable-date policy, missing-date handling and
actual metadata witnesses are still needed. No live timestamp fitness was
verified here. Stable/listed eligibility and latest-version ordering must be
settled for NuGet, without changing the 365.25-day metric or silently interpreting
latest as framework-compatible.

## Context, usefulness and unrepresented cases

**Direct dependencies:** OASim's 51 explicit entries are honestly discoverable
as declarations. They are not a proven complete evaluated graph. SDK-implied
packages, ProjectReferences and transitive packages must not silently enlarge
the denominator. Tests, tools and analyzers require an explicit scope decision;
their names or asset metadata do not mean production.

**Selected versions:** none established. Thus OASim demonstrates **NO measurable
population today**, rather than a measured 0% coverage result. The 24 unique IDs
are not 24 validated measurable packages. Current registry availability cannot
turn the 51 minimum requirements into observed used versions.

**Multiple projects/frameworks:** count-per-project, unique-package counts and
an application closure answer different questions. Shared library resolution
cannot be substituted for the consuming application's context. OASim has one
literal framework per project; it does not validate multi-framework/version
divergence or runtime-specific selection. Repository-wide union/aggregation
would cross the existing deferred portfolio boundary in [ROADMAP](../ROADMAP.md).

Unrepresented cases include actual locks/assets and stale pairs, explicit exact
requirements, ranges/floats, prerelease selections, CPM/conditional references,
imported versions, true multi-targeting, runtime-specific graphs, packages.config,
conflicting feeds/mappings and unlisted/relisted date witnesses. Only one project
family was inspected; outbounding urgency establishes neither broad reach nor
permission to weaken evidence requirements.

## Product questions, deferred technical work and recommendation

Human questions remain open:

- Is the intended outcome supplied-project dependency age, an application
  restore snapshot, or declaration freshness? Which project/context is useful?
- Are test/build/analyzer direct references included? How should repeated package
  identities across projects/frameworks count? No aggregation is selected here.
- Is requiring a team-supplied retained lock/assets snapshot and nonsecret source
  provenance acceptable for the actual workflow?
- What public-source evidence and publication-date claims would be acceptable?
  Should unlisted releases participate in latest stable? Framework-compatible
  freshness would require a separate explicit product choice.

**Recommended radar state: EXPLORE.** The real signal and recognizable declaration
population justify further bounded investigation. WATCH understates the concrete
evidence; DEFER is premature while documented selected-evidence paths remain
plausible. This is **not yet a HUMAN PRODUCT SELECTION CANDIDATE**: there is no
demonstrated declaration-to-selection-to-public-date chain or useful measured
population. No opportunity is marked SELECTED.

Additional evidence that could change this recommendation: an explicitly
authorized, independently interpreted project/lock or project/assets pair from
the team's existing workflow; known producing context and expected direct
population; nonsecret evidence authorizing public metadata; and bounded official
metadata examples establishing usable dates/latest eligibility. Another project
family could test generality, but would require its own access authorization.
Nothing here authorizes generating/restoring artifacts in OASim.

A plausible future product boundary to evaluate is one explicitly supplied
project/context, retained exact evidence, supported literal declaration forms,
direct-only population and authorized public metadata. This remains a discovery
hypothesis. General MSBuild evaluation, solution aggregation, execution/resolution,
private feeds/credentials, package archives, vulnerability/license analysis,
runtime/deployment certification and new metric semantics are explicit non-goals.
Stop if useful coverage requires these, if source/date authority cannot be
established, or if retained artifacts cannot support honest association. If
further bounded evidence repeatedly fails these gates, reconsider DEFER.

Parser organization, XML/JSON limits, lock-format versions, adapter design,
version comparison, CLI/schema contracts and task decomposition are deferred
until a human selects a product direction. Further discovery may test evidence
fitness without beginning any of that implementation work.

## Observation identity and verification boundary

The [observation protocol](../observations/README.md) does not define a numbering
convention for pre-selection cross-feature opportunities. Neither `005-0022`
nor `006-0001` is assigned. Recommend human approval of a prospective namespace
such as `discovery-0001` with lifecycle context `pre-selection`; keep schema v1's
44 fields unchanged. This is a recommendation, not an adopted convention or
ledger append. An approved convention should distinguish a future first numbered
run from retrospective recording of this presently unnumbered discovery.

Only this artifact and the opportunity radar may change. No Feature 006 artifact,
specification, plan, tasks, implementation or new ecosystem is created. Product
tests are not required for this documentation-only discovery; verification
checks evidence integrity, citations, local links, scope and patch whitespace.

## Independent review and orchestration record

Research children were `/root/nuget_repo_research` (OASim facts),
`/root/nuget_semantics_research` (official ecosystem semantics) and
`/root/nuget_fit_research` (libyears contracts). All completed before synthesis;
no sibling conclusions were supplied during their investigations. The parent
independently reproduced project counts and artifact absence, checked permitted
metadata against Git, and verified the key official-source claims. The parent
alone supplemented researcher A's filename-only config evidence with restricted
source-section inspection; no credential nodes or alternate URLs were exposed.

After synthesis, two fresh non-author reviewers audited frozen discovery content
SHA-256 `e6753705de7fb3cdc485ec141f0eaf0236b326a842f0003520fe35ac342e7dd4`
and the ROADMAP diff, without sibling reports:

| Reviewer | Independent scope and verification | Disposition |
|---|---|---|
| `/root/nuget_fact_review` | Current official source support, requirements/selection, generated/locked state, source routing and dates; independently reproduced OASim revision, clean status, project/reference/framework counts | COMPLETE / APPROVE; no findings |
| `/root/nuget_fit_review` | Actual prior libyears contracts, scope/source fidelity, product questions, EXPLORE rationale and pre-selection observation boundary | COMPLETE / APPROVE; no material findings |

The parent waited for both reports and validated their conclusions against the
inspected metadata, official source passages and existing contracts. No repair
was required. Only this review/verification record was appended after freeze.
All five children requested `fork_turns="none"`, with no model/effort overrides;
actual child model/effort/resource telemetry is unavailable. Fresh contexts and
task identifiers establish orchestration, not independent external ground truth.

Final checks preserve the OASim revision, clean status and permitted-file hashes;
no project/tool execution, credential inspection, unrelated repository access or
target write occurred. Local documentation links and `git diff --check` pass.
Implementation, tests, Feature 005 records and the observation ledger remain
unchanged. No Feature 006 artifact exists. The sole repository changes are this
pre-selection discovery and ROADMAP's EXPLORE entry; no push is performed.
