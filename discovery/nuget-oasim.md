# NuGet / OASim opportunity discovery

**Current disposition: Phase 2 resume COMPLETE; HUMAN FEATURE 006 SELECTION CANDIDATE.**
The [resumed evidence record](#phase-2-resume--observed-retained-evidence) supersedes
the historical SDK gate. Radar state remains EXPLORE; Feature 006 is unselected
and unstarted. The earlier BLOCKED attempt is preserved below.

**Phase 1 disposition: bounded discovery COMPLETE; recommended radar state EXPLORE.**
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

## Phase 2 retained-evidence experiment

**Date:** 2026-11-03. **Status:** BLOCKED / experiment incomplete.
**Recommendation:** CONTINUE EXPLORE. **Human Feature 006 selection candidate: NO.**
The environment could not locate `dotnet`; no successful restore, assets, lock
or package-list oracle was produced. This is an execution-environment limit,
not evidence that NuGet retained artifacts are unsuitable. It does not justify
DEFER or product selection. The previous read-only prohibition on generating
OASim evidence was superseded by the human's explicit Phase 2 authorization;
that exception does not change libyears' static-scanning boundary.

### Authority, preflight and declaration view A

The parent began with the supplied task and repository artifacts; two analysis
children received fresh, non-inherited contexts. Authority covered only OASim,
normal installed-dotnet restore against existing sources, disposable evidence,
and experimental locks. No installation, source changes, interactive login,
trust changes, application execution, or unrelated-repository access occurred.

OASim HEAD remains `1e937015e1d242fee5597ea0fbdc4cd5c983f101`.
Initial Git porcelain status was empty. Before attempting tooling, the parent
created `/tmp/nuget-phase2.VgJ3IN`, hashed all 223 tracked files for integrity,
recorded relevant input hashes and safely identified the two in-repository
source additions. No tracked application content was interpreted; its bytes
were hashed only for the required unchanged-content check.

The 14-file dependency/configuration manifest matches Phase 1 exactly:
`c21dcac8ed8405194671294b5d2fe6c3d4c647ae927fd7d6e6aad271372ace4c`.
Its canonicalization remains the compact sorted JSON described above.
Both configs add the source named `AvaloniaCI`, using the same non-nuget.org
HTTPS endpoint. Its URL is withheld; no credential nodes were inspected.
Neither config clears inherited sources or supplies source mapping. Effective
user/machine/ancestor configuration was not inspected or established. These
are configured identities, not proof of the sources effective for a restore.

Hidden/ignored-inclusive metadata inventory and an independent declaration
analysis reconfirmed the Phase 1 table: ten C# projects, all literal `net10.0`,
51 explicit PackageReference occurrences, 24 unique IDs/request pairs, and 15
ProjectReference edges. All package Include/Version values remain literal;
there are no observed dependency conditions, explicit imports, central version
inputs, Update or VersionOverride forms. Three legacy conditional OutputPath
groups do not condition dependencies. SDK/ancestor imports remain outside the
observed static baseline. Bare numeric requests still do not establish selected
versions. PrivateAssets on the xunit runner does not remove its explicit direct
reference. The installer was not treated as an additional C# package context.

`declarations.json` retains the per-project identities, requests, framework
elements and project-reference edges outside Git. Its SHA-256 is
`7eb820c73356ca035b75366ba86a03a735694ebc661ef8731dc2d741045c8eb0`.
No pre-existing obj/bin, assets, locks or generated NuGet artifact names were
found. The declaration population is known statically; the evaluated direct,
implicit and transitive populations remain unknown.

### Execution record and missing views B–D

The parent executed these tool-discovery commands from the authorized checkout:

```sh
dotnet --version
command -v dotnet
```

The first exited **127**, reporting `command not found: dotnet`; the second
exited **1** with no executable location. SDK version is **UNKNOWN**. No restore
was attempted, so there is no restore exit status, source connectivity result,
restore warning/error record, or generated assets location. This is not a failed
NuGet restore and not a credentials/trust failure. The human was asked for an
exact installed executable path; no broader filesystem search or SDK installation
was substituted. `tool-preflight.txt` retains the commands and outcomes.

Git provenance commands were `git rev-parse HEAD`,
`git status --porcelain=v1 --untracked-files=all`, and `git ls-files -z`.
Metadata discovery used `rg --files --hidden --no-ignore`, excluding `.git`,
with project/solution/config/Directory/global/assets/lock/NuGet/dgspec filename
filters. Local standard-library Python scripts hashed tracked bytes, extracted
only source-section identities, serialized XML declarations and compared final
integrity. These were evidence operations, not package tooling or application
execution. No restore, build, run, test, package-list or lock-generation command
was executed. The following documented command is **prospective, not executed**:

```sh
dotnet package list --project <project.csproj> --include-transitive --format json --output-version 1 --no-restore
```

Microsoft documents the noun-first form for .NET 10 and verb-first
`dotnet list package` for earlier SDKs. The installed version must be established
before choosing syntax. The explicit no-restore option is required to avoid
.NET 10 automatic restore. Requested and resolved versions differ; implicit
references also occur. [Package-list reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-package-list)

No oracle JSON exists, so its location/hash and direct/transitive/implicit counts
are **N/A / unknown**, not zero. No assets or lock file exists, so locations and
hashes are **N/A**. Cross-evidence agreement/disagreement is **NOT TESTED**;
there is no frozen empirical comparison to validate. Static declarations were
not rewritten from an oracle. Views B (restore/assets), C (oracle) and D (lock)
remain unavailable; the requested minimum three observed views was not achieved.

### Documentation-supported hypotheses, not experimental results

Assets are generated restore graphs, normally under obj, accompanied by NuGet
props/targets. This supports investigating static selected-version extraction;
it does not validate a parser, association rule, implicit classification or
stale-evidence detection for OASim. [Restore outputs](https://learn.microsoft.com/en-us/nuget/reference/msbuild-targets#restore-outputs)

Locks retain dependency closure including transitives. Normal restore can update
them; locked mode has different consistency behavior. They appear more suitable
for retention than temporary assets, but stronger portability and declaration
association were not demonstrated here. SDK implicit references still require
separation from explicit scope. [PackageReference and locking](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files#locking-dependencies)

The documented restore options include `--use-lock-file` and `--lock-file-path`.
A custom external pathname is a plausible bounded experiment for an individual
project without project references. The documentation does not establish safe
unique destinations when one absolute lock path is propagated through a
multi-project graph; assuming that behavior would be unsafe. No such command was
attempted. [Restore reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-restore)
Project and solution invocation can also use different configuration hierarchies;
a future narrow-project restore must retain that distinction rather than claim
solution equivalence. [Common configurations](https://learn.microsoft.com/en-us/nuget/consume-packages/configuring-nuget-behavior)

### Evidence chain, source authority and synthesis

These classifications describe **potential supplied evidence**, conditional on
future validation; no observed artifact qualifies as a strong candidate.

| Candidate | Classification | Missing evidence / product boundary |
|---|---|---|
| project.assets.json plus declarations/context/provenance | CONDITIONAL CANDIDATE | No actual selection, association, implicit/project distinction, freshness or source-origin comparison |
| packages.lock.json plus declarations/context/provenance | CONDITIONAL CANDIDATE | No lock witness, per-project external-generation validation or consistency comparison |
| Exported package-list JSON plus producer/context/provenance | CONDITIONAL CANDIDATE | Documented oracle mechanism; supplied-snapshot product fitness untested |
| Any candidate alone as authority for OASim public publication lookup | INSUFFICIENT | Public origin/authorization absent |
| Bare requests treated as selected versions, or public namesake substitution | UNSAFE / WRONG SEMANTICS | Violates selection and source-authority boundaries |

Answers to the ten synthesis questions:

1. **Assets:** plausible static selected evidence, suitability unproven here.
2. **Locks:** retention lifecycle is promising; stronger/portable evidence is
   unproven, especially project/framework association and source authority.
3. **Export:** useful as a documented oracle mechanism; no actual oracle obtained.
   Whether to support supplied snapshots remains an unanswered product question.
4. **Declaration → selection:** potentially without resolver reproduction when
   sufficient retained context exists; no OASim association was demonstrated.
5. **Direct/transitive:** documentation distinguishes these concepts; reliable
   explicit-direct versus implicit versus project classification remains untested.
6. **Frameworks:** retain each project/framework independently. Ten single-value
   net10.0 declarations do not validate true multi-targeting, runtime-specific
   graphs, differing selections or cross-project aggregation.
7. **Source authority:** UNKNOWN / public lookup unauthorized. No producing
   restore or effective source context exists, and no package origin was proved.
8. **Inputs together:** investigate declarations, retained exact evidence,
   project/framework and producer/tool context, coherent input provenance and
   independent nonsecret public-source authorization. This is a hypothesis,
   not a selected required-input product contract.
9. **Fail closed:** missing/failed/partial restore, stale or mismatched inputs,
   malformed/unsupported formats, ambiguous ID/selection/context, unknown imports
   or conditions affecting scope, implicit/project population confusion,
   conflicting evidence, and unknown source authority. Unknown scope must not
   become fabricated coverage. No new public error taxonomy is approved.
10. **Selection readiness:** NO. CONTINUE EXPLORE after tool availability is
    resolved; do not select Feature 006 on documentation possibilities alone.

Configuration identifies eligible sources, not necessarily the source of each
selected package. Multiple sources can contain the same identity, and cached
packages bypass mapping/download lookup. Thus source lists or mappings alone
cannot prove historical origin. No OASim publication lookup was performed, and
no public metadata probe was performed. A future experiment may evaluate a
bounded combination of producing restore/configuration evidence, mapping and
supplied nonsecret origin provenance, with cache limitations explicit. Whether
that suffices is a human trust/product decision. [Source-mapping limitations](https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping)

### Verification, review and next gate

Final integrity comparison matched all 223 tracked OASim file hashes. HEAD and
empty porcelain status were unchanged. Generated-artifact inventory remained
empty; no cleanup was necessary and no residual generated state remains. No
project declarations, versions, source configuration, credentials or trust
controls were changed. No application code executed. All raw experiment evidence
remains under the external temporary directory; only this summary enters Git.

The two fresh non-author review dispositions are recorded below after review.
They audit this blocked record and its limits; they cannot replace the missing
empirical comparison. No Feature 006 directory, implementation change, ledger
append or schema change is authorized. ROADMAP remains unchanged: no material
NuGet evidence-fitness result was obtained. Product tests are inapplicable to
this documentation-only change; patch whitespace and scope are checked instead.

**Next human gate:** identify/authorize an installed SDK executable or separately
provide an authorized execution environment, then resume the evidence experiment.
This run grants no installation authority. Source/credentials/trust changes or
interactive authentication still require new human authority. Feature selection
remains a separate later human decision.

**Observation convention:** retain this run in this artifact, with no retroactive
ID for Phase 1 and no ledger append. Recommend prospective `discovery-0001`
with pre-selection lifecycle context only after human adoption; preserve schema
v1's 44 fields.

### Phase 2 independent review record

Analysis children were `/root/declarations` (independent declaration baseline)
and `/root/semantics` (official-document semantics and safe command research).
The parent alone attempted SDK discovery and synthesized the blocked record.
No analysis child generated restore evidence.

After freezing document SHA-256
`9bd0edc2859c62d7a095099b03867ff40cdc9235bd2e021dfe1875c11e630327`,
two fresh non-author contexts completed independent audits:

| Reviewer | Scope | Verdict |
|---|---|---|
| `/root/phase2_fact_review` | NuGet documentation, retained baseline/hashes/counts, missing oracle/assets/lock comparison and factual qualification | COMPLETE / ACCEPT blocked record; no blocking defects |
| `/root/phase2_fit_review` | Prior libyears contracts, declaration/selection/direct/source fidelity, project/framework context and product nonselection | COMPLETE / APPROVE blocked record; no material findings |

Both explicitly confirmed the empirical experiment remains incomplete and that
review acceptance supplies no missing comparison or selection authority. The
parent validated these conclusions against the retained baseline, execution
results and official documentation; no correction was needed. Only this review
record was appended after freeze. All four Phase 2 children used
`fork_turns="none"`, without model/effort overrides; actual resource telemetry
is unavailable. Fresh contexts establish independent assignments, not external
ground truth. Local links resolve, `git diff --check` passes, and only this
discovery document changes. No push occurred.

## Phase 2 resume — observed retained evidence

**Date:** 2026-11-03. **Status:** COMPLETE within the authorized experiment.
**Decision: HUMAN FEATURE 006 SELECTION CANDIDATE.** Recommended opportunity
state remains **EXPLORE** pending human product selection. **Feature 006 selected:
NO.** This section supersedes the blocked SDK gate, without changing the earlier
attempt or Phase 1 observations. It establishes a technically credible bounded
supplied-evidence direction, not a product contract, completed measurement, or
permission to implement NuGet support.

### Continuity and execution boundary

The fresh parent reconstructed state from AGENTS.md, AGENT_ROUTING.md, ROADMAP.md,
this artifact and commits `26fc59d` and `3314cd0`. Independently executed
`/usr/local/share/dotnet/dotnet --version` returned **10.0.403**, exit 0.
`--info` reported **osx-arm64**, MSBuild 18.9.15, host/runtime 10.0.14.
OASim HEAD remains `1e937015e1d242fee5597ea0fbdc4cd5c983f101`; initial
porcelain status was empty. All **223 tracked files** match the prior integrity
manifest. All **14 dependency/configuration inputs** match, including manifest
SHA-256 `c21dcac8ed8405194671294b5d2fe6c3d4c647ae927fd7d6e6aad271372ace4c`.
Thus the declaration baseline was verified, not rediscovered or replaced.
The original `declarations.json` was copied byte-for-byte from
`/tmp/nuget-phase2.VgJ3IN`; its hash remains
`7eb820c73356ca035b75366ba86a03a735694ebc661ef8731dc2d741045c8eb0`.
No product/tool output was used to amend it.

The existing human exception authorized restore, source access and disposable
lock evidence only for the exact OASim root. Sandbox escalation permitted the
two bounded orchestration scripts. No package versions, committed source or
configuration, sources, trust settings or TLS controls were changed. No
interactive option was supplied; no authentication prompt was observed.
No application build/run/test/publish command was invoked. Restore evaluates
MSBuild inputs and generates NuGet imports; this exception is experimental
producer authority, not permission for a future libyears scanner to execute it.
The installer was excluded. Per-project invocation is retained explicitly;
these results are not asserted equivalent to a solution restore.

### Commands and retained evidence

Let `R=/Users/dpjj/code/hhs/OASim`,
`D=/var/folders/33/t96n6m0j5qn7vpzq49gtyl1m0000gp/T/nuget-phase2-resume.w3zgqj_q`,
and `SDK=/usr/local/share/dotnet/dotnet`. All ten project paths are in the
unchanged declaration baseline. For each project `P`, sequentially, the actual
argument vectors were equivalent to:

```sh
"$SDK" restore "$R/$P" --packages "$D/packages" --disable-parallel --verbosity minimal
"$SDK" package list --project "$R/$P" --include-transitive --format json --output-version 1 --no-restore
"$SDK" restore "$R/$P" --packages "$D/packages" --disable-parallel --verbosity minimal --use-lock-file
```

Working directory was `R`; child environment additions were
`DOTNET_CLI_TELEMETRY_OPTOUT=1` and `DOTNET_NOLOGO=1`. Each phase covered ten
projects before proceeding to the next. The package directory was newly created
for this experiment. Existing HTTP-cache behavior was left intact; this is not
a claim that every package was freshly downloaded from the network. No source
or configuration override was used. The SDK's local package-list help, run
outside the sandbox, confirmed the .NET 10 syntax above. A preliminary sandboxed
`--info`/help chain printed SDK information but ended 143 at subsequent help;
the elevated standalone help succeeded. This did not fail a restore.
[Noun-first syntax and no-restore behavior](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-package-list),
[restore switches](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-restore).

All **10 initial restores**, **10 oracle commands**, and **10 lock restores**
exited **0**. First restore emitted a workload-verification advisory; no workload
update was attempted. NU1903/NU1904 vulnerability warnings appeared for MRCalc,
MatchRunTests and OASim. NU1510 warned that MatchRunProfileUpdater's explicit
Microsoft.Win32.Registry reference is unnecessary but **will not be pruned**.
It remains in all four evidence views. These warnings are retained without
changing declarations. Audit traffic is part of ordinary restore, not an
OASim publication-date/age measurement.

Producer scripts and exact command arrays, exit codes and logs are retained in
D: `nuget-resume-run.py`, `nuget-resume-views.py`, `nuget-resume-compare.py`,
`restore-records.json`, and `view-records.json`. For each project name N:

- `D/N.restore.log` retains the initial restore log.
- `D/views/N/before-lock.project.assets.json` and
  `before-lock.project.nuget.cache` freeze initial restore state before locks.
- `D/views/N/oracle.json` and `oracle.stderr` retain the no-restore oracle.
- `D/views/N/lock-restore.log`, `project.assets.json` and `packages.lock.json`
  retain experimental lock production and resulting artifacts.

Raw logs/assets can contain local configuration paths and source endpoints;
they remain outside Git. No credential nodes or user/machine config files were
opened. Nonpublic endpoints are not reproduced here. The evidence directory is
local temporary retention, not permanent archival storage; preserve it separately
if later review requires the full bytes. The committed summary and hashes do
not substitute for unavailable raw evidence.

SHA-256 witnesses (all paths below relative to D):

| Evidence | SHA-256 |
|---|---|
| `evidence-manifest.json` | `b9a0ba773c1dca98090d3e8fec29e4c681984f7cb5e811d30cfcf43664dad0f6` |
| `comparison.json` | `df7762499ab0424116d1f1637ca02ada9e31c7991926066d3bf1df53a1c91997` |
| `association.json` | `91caf0d3c38468f16b8a0ce65f9bfc45c2b6d40cb9b1596d2348dcc931d51990` |
| `origin-provenance.json` | `6de27fd42fce6396b66068ce33a968d9b6999fe33a61ce65144b4b64be2eea31` |
| `restore-records.json` | `9fdfec90e19526db47a934641c7967e9781d6cfe7e1d583fb78b740e6c496af5` |
| `view-records.json` | `64b07fa4a722e2331210adb87ec3b29e81e93d0869d7994529e37fbe1d41bd08` |
| `views/MRCalc/before-lock.project.assets.json` | `f1a5c5c8c7d392159cb2097581d07b78865ef717bfdad92e011369dd093f0ae9` |
| `views/MRCalc/oracle.json` | `e774693b0cc4d53e63952ef18160b264ee31ba5684094545e99aabbc337f10af` |
| `views/MRCalc/packages.lock.json` | `11f1658d4a00e06e8b8509ee86e6648e02bec5a9c702cf6a366a24a616e3ddf1` |

The manifest enumerates all retained non-package evidence files at freeze,
including every project's artifacts and scripts. Package archives/contents were
not manually inspected. Only this experiment's generated `.nupkg.metadata`
JSON was read to extract source/content-hash provenance; no existing home
package cache was inspected. Metadata file hashes are in origin-provenance.json.

### Independent view comparison

Assets format is **4**, lock format **1**, oracle output format **1**.
Each row represents its own project / `net10.0` context, without an explicit RID
restore target. Project node counts are closure entries, not direct-edge counts.

| Project | Baseline direct | Oracle direct | Oracle transitive | Assets project nodes |
|---|---:|---:|---:|---:|
| MRCalc | 9 | 9 | 39 | 1 |
| MatchRunBenchmarks | 2 | 2 | 30 | 2 |
| MatchRunCLI | 8 | 8 | 12 | 1 |
| MatchRunEngine | 4 | 4 | 1 | 0 |
| MatchRunProfileUpdater | 1 | 1 | 0 | 0 |
| MatchRunProfiling | 2 | 2 | 30 | 2 |
| MatchRunTests | 5 | 5 | 60 | 4 |
| OASim | 9 | 9 | 40 | 2 |
| OASimCLI | 9 | 9 | 13 | 2 |
| SimulationEngine | 2 | 2 | 4 | 1 |
| **Occurrence totals** | **51** | **51** | **229** | **15** |

There are **24 distinct direct ID/version pairs**, **83 distinct transitive
ID/version pairs**, and **92 distinct ID/version pairs in the combined closure**.
Direct and transitive sets overlap across contexts. These are descriptive
experiment counts, not an approved repository-wide libyears denominator.

The parent compared each view separately against the preserved declarations,
then reconciled all four; `comparison.json` reports **zero disagreements**:

1. Baseline IDs exactly match assets `project.frameworks.net10.0.dependencies`,
   oracle `topLevelPackages`, and lock entries typed `Direct`, per project.
2. For every declaration, oracle `requestedVersion` equals its original literal
   request. Assets and locks retain the corresponding inclusive minimum
   `[request, )`. This mapping was checked only for the observed literal numeric
   forms; no general range parser or version solver was implemented.
3. Oracle `resolvedVersion`, assets package target ID/version, and lock `resolved`
   agree on all 51 direct occurrences. All happen to equal the numeric request;
   successful retained resolution, not that coincidence, supplies exactness.
4. Oracle top-level plus transitive ID/version maps equal assets targets typed
   `package`. Oracle transitives exactly equal locks typed `Transitive`.
   Project nodes are typed separately and excluded. No extra implicit top-level
   package was observed; the framework reference Microsoft.NETCore.App does not
   become a direct package. This does not validate implicit-package cases.
5. Pre-lock and post-lock assets targets and libraries are identical for every
   project. Lock generation changed restore state/provenance but not the selected
   closure. Locks were generated at each project's normal `packages.lock.json`
   destination, not one shared absolute filename propagated through a graph.
   None existed before; none is tracked. Committed opt-in/configuration was
   unnecessary. No locked-mode consistency or deliberate stale-pair experiment
   was performed. Locks therefore demonstrate useful retention, not inherently
   stronger proof of historical coherence or portability.

For example, MRCalc's explicit `Avalonia / 0.10.19` associates within MRCalc /
net10.0 with assets request `[0.10.19, )`, package target `Avalonia/0.10.19`,
oracle requested/resolved `0.10.19`, and lock Direct requested `[0.10.19, )` /
resolved `0.10.19`. CoreCLR-NCalc, direct in MatchRunEngine, is transitive in
MRCalc. ID-only matching across projects would misclassify it. PrivateAssets
on the test runner does not erase its direct membership in MatchRunTests.

This is independent interpretation of distinct views, not independent resolver
implementations: assets, locks and oracle all depend on the same NuGet producer,
and the oracle consumes restore state. Agreement corroborates field association;
it cannot independently prove NuGet correct or reconstruct historical inputs.
Only the producing run and recorded input integrity bind these particular
snapshots. Arbitrary supplied snapshots still need a coherent provenance claim,
static association checks and fail-closed disagreement handling.

### Source authority — separate from selection

Assets report one configured source for eight projects and two for MRCalc/OASim.
That is eligible-source context, not per-package origin. Neither assets, locks,
source counts, package IDs nor content hashes alone authorize public namesakes.

A separate provenance witness is available here: of **97** generated package
metadata records in the disposable package directory, all record source exactly
`https://api.nuget.org/v3/index.json`. For each of the **92 selected closure
ID/version pairs**, the parent bound that metadata's `contentHash` to both the
assets library `sha512` and lock `contentHash`, with no missing/mismatched record.
The other five metadata records are not counted as selected context packages.
`origin-provenance.json` retains selected IDs/versions, source, content hash and
metadata SHA-256. This is inspected **NuGet producer-reported public provenance
for this run**, not inferred public identity or proof that a network download
occurred rather than HTTP-cache reuse. Microsoft documents the extraction-marker
role of `.nupkg.metadata` and cache behavior; the source/contentHash fields here
are observed SDK output, not a proposed stable interchange schema.
[Cache/extraction lifecycle](https://learn.microsoft.com/en-us/nuget/consume-packages/managing-the-global-packages-and-cache-folders).

This provides a technically credible way to supply separate nonsecret source
provenance. It is not cryptographic attestation, proof about past OASim restores,
or adoption of a libyears trust policy. A future human-selected contract must
decide which producer/supplier assertions authorize public lookup, bind them to
selected context evidence, reject unknown/nonpublic origin and avoid reading
credential-bearing configuration or arbitrary cache locations. Source mapping
alone would still be insufficient, particularly with caches.
[Source-mapping boundaries](https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping).

**OASim publication lookup performed: NO.** No package-age measurement,
registration/catalog publication query, latest-stable selection or libyears
coverage/age total was performed. Ordinary restore package/audit traffic is
separate. Date semantics and latest eligibility remain open as in Phase 1.

### Candidate classifications and decision

| Supplied evidence candidate | Classification after experiment | Boundary |
|---|---|---|
| Declarations + assets + project/framework + producer/input provenance | STRONG BOUNDED SELECTION CANDIDATE | Demonstrated 51 associations; generated, path-bearing snapshot needs explicit retention and coherence policy |
| Declarations + per-project lock + context/provenance | STRONG BOUNDED SELECTION CANDIDATE | Direct/requested/resolved distinction and closure demonstrated; source and historical coherence remain separate |
| Exported package-list JSON + declarations/context/provenance | CONDITIONAL SUPPLIED-EVIDENCE CANDIDATE | Useful oracle, but less closure/hash detail; not an independent resolver or source authority |
| Selection evidence + hash-bound supplied origin witness | CREDIBLE SOURCE-PROVENANCE DIRECTION | Demonstrated producer-reported nuget.org provenance; human acceptance/trust contract required |
| Any assets/lock/oracle alone for public lookup | INSUFFICIENT | No standalone per-package public-source authority |
| Bare requests as selections, cross-project ID matching, public namesake substitution | UNSAFE / WRONG SEMANTICS | Contradicts observed evidence roles |

The decision advances from the blocked attempt to **HUMAN FEATURE 006 SELECTION
CANDIDATE** because a bounded static/supplied contract is technically credible:
literal explicit declarations can associate with exact retained selections in
one project/framework, distinguish transitive/project entries, and carry a
separate hash-bound nonsecret origin witness. It rests on more than printing
versions. It does not claim a complete public-date chain, general MSBuild
interpretation, solution aggregation, or ready-to-ship feature scope.

Human decisions remain: useful project/context and direct population (including
tests/tools/analyzers), accepted supplied artifacts/provenance and public-source
trust boundary, usable publication/latest policy and unsupported-case behavior.
True multi-targeting, RID-specific targets, differing direct selections,
conditional/imported/central versions, source conflicts, stale/malformed evidence,
missing/partial restore and adversarial snapshots remain unvalidated. A future
contract must reject ambiguity and preserve unknown scope rather than fabricate
coverage. No parser architecture, CLI/schema change, spec, plan or task graph was
created. ROADMAP retains EXPLORE while updating its materially changed evidence.

### Integrity, residual state and observation boundary

All 223 tracked OASim files still match the pre-attempt manifest, and HEAD is
unchanged. Final porcelain lists only ten **untracked** per-project lock files.
There are **50 ignored obj files** across the ten projects (including assets,
generated NuGet props/targets, dgspec and cache); no bin output was generated.
D retains disposable packages, scripts, copied baseline, logs and comparison
artifacts. Ordinary SDK/NuGet HTTP-cache/scratch or first-run side effects were
not exhaustively inventoried outside the authorized root. No cleanup, reset or
`git clean` was used. Residual locks are experimental, not silently adopted
committed OASim configuration.

The pre-selection observation namespace is still unadopted. Recommend a human-
approved prospective `discovery-0001` namespace with pre-selection lifecycle;
do not assign IDs retroactively, append a ledger row or change schema v1's 44
fields. No product tests are needed for this documentation-only change.

**Next human gate:** decide whether to select a bounded supplied-evidence NuGet
direction for Feature 006 and settle its product/trust/date questions before
SDD. This experiment neither selects it nor authorizes further implementation.

### Resume independent review and parent validation

After freezing comparison/evidence and discovery SHA-256
`4a06e67ce8b4d2a83e7d4d43de9bd89fd4997aa90725de6cd4efe338d3a090a0`
(ROADMAP `0b6ebe3ed61cd176e2d564f54a14b951db2568228304f41433689ea7ede8dbbd`),
the parent dispatched two fresh non-author reviewers with `fork_turns="none"`
and no model/effort overrides. Neither received the other's report or inherited
the author conversation; both received the frozen artifacts and narrow authority.

| Reviewer | Completed independent coverage | Verdict |
|---|---|---|
| `/root/resume_fact_review` | Recomputed all four raw views, 92 manifest hashes, source/hash bindings, command records/logs, OASim input/tracked integrity and generated-state counts; checked official Microsoft command/cache/source documentation | COMPLETE / APPROVE; no material factual or cross-evidence findings |
| `/root/resume_fit_review` | Recomputed context/direct/request/selection/closure associations and source/hash bindings; verified baseline/manifest; compared Feature 003/004/005 evidence principles and human selection/source-trust boundaries | COMPLETE / PASS; no material evidence-model findings |

Both supported the candidate recommendation only as a bounded supplied-evidence
direction, preserving EXPLORE and human selection. They explicitly did not
validate publication-date measurement, arbitrary snapshot coherence, accepted
trust policy, untested contexts or all producer side effects. Neither ran dotnet,
modified files, inspected archives/credentials or interpreted application code.
SDK preflight remains the parent's producer observation rather than a reviewer
rerun. Actual child model/effort/resource telemetry is unavailable; fresh task
contexts demonstrate orchestration, not independent resolver ground truth.

The parent received both completed reports and validated their findings against
raw associations, selected origin/hash witnesses, unchanged tracked content,
zero bin files, lock/snapshot byte identity and the already verified manifest.
No correction was required. Only this review record was appended after freeze.
Local file links and `git diff --check` pass. The sole libyears changes are this
discovery and ROADMAP's updated EXPLORE rationale; no implementation, test,
Feature 006 artifact, observation ledger or schema change was made. The earlier
BLOCKED attempt remains intact. One local documentation commit is authorized;
no push is performed.
