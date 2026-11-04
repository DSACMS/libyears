# Feature 006 Discovery: Bounded NuGet Selected-Version Evidence

**Status: READY FOR SPECIFICATION. Readiness for specification: YES.**

Human H1–H4 acceptance and specification authorization were supplied on
2026-11-03 for fresh run `006-0002`. The original discovery recommendations,
questions and run `006-0001` review record below are historical; the decision
record at the end supersedes their pending-gate language. Specification remains
a draft until independent review; planning and implementation are not authorized.

Bounded discovery completed on 2026-11-03 in fresh run `006-0001`, starting at
`c389208dda26406646ed42d0384cb83cde1c4a6d` with a clean working tree.
Canonical directory: `specs/006-nuget-selected-evidence/`.

## Human selection and authority

The commissioning human explicitly selected **BOUNDED NUGET SELECTED-VERSION
EVIDENCE** as Feature 006 and approved discovery. The intended outcome is static
association of supported direct .NET/NuGet declarations with exact selected
versions from supported retained/supplied evidence, measuring age only with
sufficient source and publication authority.

**Libyears consumes dependency evidence. It does not perform NuGet restore or
package resolution.** Selection does not approve a specification, an
assets-versus-lock choice, arbitrary generated-artifact trust, name-based public
lookup, general NuGet support, planning, or implementation. Recommendations below
are proposed product boundaries, not approved requirements. H1–H4 need human
resolution before specification. No `spec.md`, `plan.md`, or `tasks.md` is begun.

[ROADMAP](../../ROADMAP.md) records SELECTED with this limited gate. Historical
EXPLORE/unselected statements in [pre-selection discovery](../../discovery/nuget-oasim.md)
remain intact and describe their original authority, superseded by this human
selection rather than retrospectively rewritten.

## Evidence and method

Repository grounding: AGENTS.md, AGENT_ROUTING.md, observations/README.md,
ROADMAP, pre-selection NuGet discovery, prior ecosystem discovery and relevant
Feature [002](../002-npm-support/spec.md),
[003](../003-yarn-lock-evidence/spec.md),
[004](../004-rubygems-support/spec.md), and
[005](../005-gemfile-group-scope/spec.md) evidence contracts; current mixed-scan
availability/reporting behavior in `libyears/scan.py` and `libyears/output.py`.
Git `26fc59d`, `3314cd0`, and `c389208` preserve initial research, the blocked
experiment, and its completed resume. Two fresh research children independently
investigated artifacts/association and source/date semantics. The parent checked
conclusions against repository evidence and current Microsoft documentation.

No OASim access, experiment replay, dotnet execution, restore, package download,
registry package-age measurement, credential/configuration inspection, or product
code change occurred in this run. Public documentation was consulted on
2026-11-03. The committed experiment summary is the empirical source here; raw
temporary evidence was not reopened or revalidated.

### What the retained experiment establishes

The Phase 2 resume records ten separate single-`net10.0` project contexts:
51 explicit direct occurrences, 24 distinct direct ID/version pairs, 229
transitive occurrences and 15 project nodes. Declaration IDs, assets framework
dependencies, lock `Direct` entries and oracle top-level packages agreed with
zero disagreements. Exact selections agreed in assets format 4, lock format 1
and oracle format 1. Each selected version happened to equal its numeric request;
retained selection, not the numeric spelling, established exactness.

Separate producer-reported `.nupkg.metadata` records were hash-bound to all 92
selected closure ID/version pairs and reported nuget.org origin. This is not a
stable interchange-schema commitment or cryptographic provenance. Assets/locks
and oracle all share the NuGet producer; agreement is corroboration, not three
independent resolver implementations. No locked-mode/stale-pair experiment,
publication lookup or measurement was performed. All locks were experimentally
created, not pre-existing adoption evidence. One project family does not establish
general coverage, demand, portability, or a safe rejection rate.

## Selection-evidence comparison

| Candidate | Product merit | Limitation / proposed v1 role |
|---|---|---|
| `project.assets.json` | Restore-selected graph with framework/package/project distinctions; demonstrated direct association | Generated temporary restore state, normally `obj`, path-bearing and not intended for source control. Needs explicit retention/coherence/provenance. Credible alternative if supporting existing restore output is the main workflow. |
| `packages.lock.json` | Durable opt-in full closure, typed direct/requested/resolved evidence and content hashes; demonstrated association | Normal restore can update it; a supplied lock does not prove locked-mode success or current declarations. Needs explicit project binding and separate source authority. Recommended sole initial selection format. |
| Both | Covers more producers/workflows and can corroborate selections | Two parser surfaces and conflict/precedence semantics; agreement does not prove origin/freshness. Do not require or support both initially. |
| Exported `dotnet package list` JSON | Requested/resolved and top-level/transitive diagnostic view, versioned export | Restore-state dependent, implicit top-level references possible, less closure/hash detail. Retain as oracle/diagnostic evidence, exclude as v1 input. |

Microsoft documents the [assets lifecycle](https://learn.microsoft.com/en-us/nuget/concepts/dependency-resolution)
and [restore outputs](https://learn.microsoft.com/en-us/nuget/reference/msbuild-targets#restore-outputs).
The [lock guide](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files#locking-dependencies)
distinguishes persisted closure, normal update and locked-mode validation; a
library's lock does not control consumer resolution. The
[package-list reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-package-list)
documents JSON/output versions and .NET 10 automatic restore unless suppressed.
These describe external evidence producers, never commands for libyears to run.

**H1 recommendation:** declarations plus one per-project lock format 1, with
separate context/coherence and source witnesses. This is the smallest useful
retention-oriented boundary. Prefer assets format 4 instead only if avoiding
external lock production is the chosen user outcome. No fallback, auto-generation,
or opportunistic use of unsupported co-located artifacts is implied.

## Declaration and context boundary

**H2 recommendation:** one explicitly identified SDK-style C# project, one
literal target framework (either TargetFramework or a single-valued
TargetFrameworks), no RID-specific graph, with explicit unconditional literal
`PackageReference Include` and numeric literal `Version` attributes. Count all
supported explicit direct declarations, including tests/tools/analyzers and
PrivateAssets declarations; do not label them production/runtime dependencies.
Exclude transitives, project nodes and SDK/generated implicit packages from that
population. ProjectReference edges may be present but are not traversed or counted.

A bare numeric NuGet version is a minimum request; `[v]` is exact request syntax.
Neither proves a successful selection. Initial numeric requests should be retained
as requests and associated only by a documented bounded textual transformation
(the observed inclusive minimum form) and matching direct identity. No satisfaction
check, resolution, or general semantic equivalence engine is proposed.
[NuGet version rules](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning)
explain ranges, floating requests and normalization. The
[PackageReference reference](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files)
explains conditions, asset metadata and implicit references.

Propose rejecting ranges/floats/bracket-exact forms initially, property-expanded
IDs/versions, Update/Remove/VersionOverride, dependency-affecting conditions,
explicit imports supplying declarations, generated declarations and CPM rather
than silently reading a supported-looking subset. The
[CPM guide](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management)
shows that central versions alone are not membership, with imports, overrides,
global references and transitive pinning adding further context. No
`packages.config`, general MSBuild evaluation or project traversal is proposed.

**Critical completeness qualification:** SDK-style projects already import SDK
behavior; ancestor `Directory.Build.*` can also affect inputs. Absence of Import
in a project is not proof of complete evaluated scope.
[MSBuild directory customization](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory?view=vs-2022)
documents this. Recommend a claim about **supported explicit declarations in
supplied inputs**, not the evaluated restore graph. Require a supplier coherence
assertion identifying project/framework, producer/version, declaration and lock
bytes and relevant input baseline; any known unsupported membership/version
influence rejects the context. Do not search ancestors or caches outside the
supplied boundary. The human must accept this claim/trust limitation in H2 or
require stronger evidence before specification.

Context must bind project identity, sole framework, request/direct population,
exact selection and supplier evidence to the same snapshot. Lock TFMs alone do
not identify a project. Proposed static comparisons detect missing/extra direct
identities, request mismatch, duplicate/ambiguous selections and framework/RID
mismatch. Hashes bind supplied bytes, not truth about their producing history.
Mtime, matching names, matching versions, Git presence or restore timestamp do not
prove freshness. The result describes a supplied coherent snapshot under accepted
assertions, not today's evaluated project, deployment or a reproducible restore.

Multiple TFMs, RID graphs, automatic multi-project selection, solution closure,
union/deduplication across projects and portfolio totals remain out of scope.
Other ecosystems may coexist at the selected location under their existing rules;
NuGet input selection must be explicit if project identity would be ambiguous.

## Source authority independent of selection

**H3 recommendation:** require an explicitly accepted nonsecret supplier/producer
origin witness per selected package ID/version/content hash, bound to project,
framework and selection bytes. Only an assertion identifying the public
`https://api.nuget.org/v3/index.json` authority permits public lookup. Unknown,
private, alternate or conflicting origin blocks lookup for that dependency.
This accepts producer/supplier testimony under an explicit human trust policy;
it does not authenticate an arbitrary generated JSON file.
Recommend also requiring selected content hash agreement with public catalog
package hash before assigning its date. Matching ID/version alone does not
establish correspondence between supplied package content and the public metadata
being dated. The [catalog API](https://learn.microsoft.com/en-us/nuget/api/catalog-resource)
documents package hash and algorithm fields for this comparison.
Unavailable or conflicting hash evidence makes that dependency unmeasurable.

The retained experiment demonstrates a possible witness, not permission for
libyears to inspect global caches or adopt `.nupkg.metadata` as a stable input.
A supplied witness may carry producer-reported values without credential-bearing
paths/configuration. Exact serialization is later design; acceptance of assertions
as authority is a product decision now. A blanket 'use nuget.org' switch without
context/package binding is not the recommendation.

Configured source lists, eligible-source counts, source mapping and public
namesakes are insufficient alone. Microsoft documents that
[source mappings](https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping)
can select multiple sources and do not trigger source lookup for already cached
packages. A content hash establishes content correspondence, not where it came
from. No public lookup should be used to discover whether an unknown/private
package happens to share a public identity.

## Publication dates and latest stable

**H4 recommendation:** use nuget.org's documented catalog `PackageDetails.created`
for both used and latest version dates, qualified as **first receipt by the public
source**, not original upstream release or first availability anywhere. `created`
is optional; although documentation names `published` as fallback, that fallback
is unsuitable for this claim: catalog `published` means last listing, while
`commitTimeStamp` dates a catalog event. Catalog history includes unlist/relist,
updates and deletion; do not substitute its first observed commit for creation.
[Microsoft catalog API](https://learn.microsoft.com/en-us/nuget/api/catalog-resource).

Registration's optional `published` can carry a year-1900 unlisted sentinel.
It alone does not establish an immutable first-publication claim. Registration
can enumerate versions/listing and point to catalog entries; require usable
identity-bound `created`, otherwise unmeasurable. Reject missing, invalid or
sentinel dates, conflicts and unavailable metadata without using modification,
restore or snapshot-generation times. Missing created for the actual latest
candidate must not cause choosing an older dated version.
[Registration API](https://learn.microsoft.com/en-us/nuget/api/registration-base-url-resource).

Recommend latest = greatest NuGet version precedence among currently listed
non-prerelease versions, including SemVer 2 metadata, independent of TFM/RID,
requested range or vulnerability status. The selected used version may be
prerelease or unlisted if authorized identity and usable created remain available.
Deleted/unavailable versions are not reconstructed from archives. Listing changes
can change the comparator; this measures current public metadata, not complete
historical availability. Incomplete enumeration cannot establish latest.
[Registration version rules](https://learn.microsoft.com/en-us/nuget/api/registration-base-url-resource),
[package content API](https://learn.microsoft.com/en-us/nuget/api/package-base-address-resource)
(the latter includes unlisted versions and supplies no publication dates).

Human acceptance of first-receipt and listed-latest semantics remains required;
no change to metric arithmetic is proposed. The formula stays 365.25 days per
year, latest-used identity gives exactly 0.0, anomalous negative date differences
are clamped and flagged. No grace period or compatibility-aware latest is added.

## Failure and incompleteness recommendation

These are proposed semantic categories, not new approved reason codes or schema.

| Evidence failure | Recommended scope/measurement behavior |
|---|---|
| Missing/unreadable/unsupported declaration evidence or unknown membership influences | Source failure; unknown denominator, null coverage; never count recognizable fragments as complete scope. |
| Complete supported declarations, missing selection evidence | Preserve known N; selection source unavailable, null measured/coverage, not fabricated N package failures. |
| Malformed/unsupported selection schema; whole-context stale/mismatched project, framework, RID or supplier binding | Reject selection source; retain N only if declarations independently establish it; no lookup. |
| Accepted context, isolated missing/ambiguous direct association or request mismatch | Dependency unmeasurable; retain known denominator, no lookup for that identity. Extra direct population undermining context coherence rejects the context instead. |
| Unknown/private/conflicting package origin or missing witness | Dependency unmeasurable, known N retained; no public namesake query. Whole-witness corruption may invalidate the witness source. |
| Authorized package, missing used/latest date, incomplete latest enumeration or unusable public response | Dependency unmeasurable; preserve identity and safe selection evidence; exclude from numeric aggregates. |
| Known supported empty population | Zero discovered/measured, null coverage; distinguish from unavailable scope. |

With an accepted measurement source, N>0 coverage is M/N, including 0/N when
all individual dependencies fail. Whole-source unavailability is not 0%.
Successful PyPI/npm/RubyGems results survive NuGet failure. Repository discovered
count is unknown if any detected source denominator is unknown; repository
coverage is null if any source is unavailable. Preserve current mixed-scan
availability semantics rather than inventing NuGet-only aggregates.

## Compatibility and remaining gates

Recommend additive ecosystem-keyed NuGet provenance within existing schema-v3
concepts: declaration, selection format, selected project/framework and safe
source/date claim. Preserve existing Python `--resolved`, npm/Yarn arbitration,
Ruby group behavior, human/JSON separation, exit categories and all existing
fields/metric semantics. Public CLI activation, provenance disclosure and stable
failure identifiers must be settled and approved in the eventual specification;
a breaking schema change would require a separate explicit decision, not planning.
Network remains behind an adapter with verified public authority and TLS;
standard-library runtime and offline deterministic tests remain mandatory.

### MUST RESOLVE BEFORE SPECIFICATION — HUMAN DECISION REQUIRED

1. **H1 — Initial selection artifact:** lock-only (recommended), assets-only,
   or require further discovery of a both-format/export workflow. Lock-only adds
   external producer effort to users without locks; libyears never generates one.
2. **H2 — Population and coherence claim:** accept the proposed conservative
   one-project/one-framework explicit-declaration snapshot, including test/tool
   references, with bounded numeric requests, supplier input/coherence assertions
   and the proposed failure/denominator policy (recommended); or require stronger
   evaluated-scope/coherence evidence before
   proceeding. Rejecting assertions means further discovery, not silent evaluation.
3. **H3 — Source trust:** accept explicitly bound producer/supplier public-origin
   assertions plus public-content hash agreement, with fail-closed unknowns
   (recommended); or require a stronger
   verifiable provenance mechanism through additional discovery. Neither approves
   arbitrary generated artifacts or lookup by name coincidence.
4. **H4 — Date/comparator claim:** accept first nuget.org receipt from catalog
   `created`, currently listed greatest stable as comparator, unlisted/prerelease
   used versions when dates remain available, and unmeasurable missing metadata
   (recommended); or require further date-policy discovery.
   Registration published/catalog commit time are not equivalent alternatives.

No consequential product question is delegated to technical planning. These four
answers would permit the next human gate to consider specification; discovery
completion itself does not authorize it.

### DEFER TO TECHNICAL PLANNING

After approved specification fixes inputs, activation, public fields/reasons,
listing/date semantics and trust assertions: parser/module decomposition,
resource bounds implementation, bounded NuGet identity normalization/ordering,
registry pagination/catalog-link transport and allowlists, witness serialization
implementation, fixture organization and task ordering. Planning cannot choose
a broader format, trust policy, population or date claim.

### OUT OF SCOPE

Product dotnet/NuGet/MSBuild execution, restore/resolution/install, target code
execution, package archives, private endpoints/credentials or caches, additional
ecosystems, general MSBuild/CPM/import/conditional interpretation, multi-TFM/RID,
transitive/project-reference measurement, solution/portfolio aggregation, and
unapproved schema/metric changes. Assets/export support is excluded from the
recommended lock-only v1, but remains an H1 alternative rather than a settled
human rejection.

## Evidence limitations and independent review

No new raw producer evidence or live publication metadata fitness was collected.
OASim's retained positive comparison does not test malformed/adversarial/stale
inputs, range forms, all schema versions or future SDK behavior. Optional catalog
created and origin assertions can reduce coverage; no measurement yield is claimed.
Additional OASim access is unnecessary for these product choices and would not
supply human trust authority. Historical experiment temporary retention is not a
permanent raw archive. Two fresh non-author reviews are required after candidate
freeze; their coverage and parent disposition are recorded below.

### Frozen candidate review and parent disposition

Candidate discovery SHA-256:
`ddb0f0f1024662a8db7238f0b0cab33c72d8a00e397fb4f8c01359ee0356206b`;
ROADMAP SHA-256:
`ecb60ae6fe9c02265f1ddbc054fe38693b63f7245fb829d866299d6c34c13b8f`.
Both reviewers were fresh non-author contexts and verified these exact candidates.

| Reviewer | Completed coverage | Verdict / parent disposition |
|---|---|---|
| `/root/factual_review` (A) | Current Microsoft/NuGet sources; retained experiment summary; selection, declarations, context, source and publication facts | APPROVE WITH ONE MINOR SOURCE-SUPPORT CORRECTION. Unsupported frequency/republication wording removed; content correspondence rationale and catalog hash citation replace it. No material factual/empirical contradiction found. |
| `/root/boundary_review` (B) | Prior ecosystem contracts and current mixed-scan logic; product authority, evidence roles, nullable denominators, compatibility and decision classification | PASS; no material findings. Suggested explicit failure-policy acceptance added to H2. |

The parent validated A's source-support correction against the cited material:
it supports hash comparison but did not substantiate the removed historical claim.
B's missing-lock observation was checked against Feature 005: that feature uses
individual failures for an absent lock. The proposed NuGet whole-source policy
is deliberately a pending product choice, not a claim of identical ecosystem
behavior. H2 now names that choice; H3/H4 summaries also explicitly name the
already proposed hash and unlisted/prerelease-used policies. No recommendation
was promoted to approval. These clarifications and this review record are the
only changes after freeze; the factual correction does not broaden scope.

All four children (two research, two review) used `fork_turns="none"` without
model/effort overrides. Actual child model/effort/resource telemetry was
unavailable. A received B's completion/verdict status while finishing its separate
factual audit, not B's report; each supplied its own completed coverage and verdict.
Neither reviewed raw experimental files or reran a producer. Fresh contexts do
not establish independent resolver ground truth.

Final verification: local links resolve; only ROADMAP and this discovery change;
pre-selection NuGet discovery and the 44-field observations ledger retain their
baseline bytes. No sensitive local paths/credentials were introduced. No product
code, specification, plan or tasks were created or changed. `git diff --check`
passes. Product tests were not run for documentation-only discovery. One coherent
local documentation commit is authorized; no push is performed. Observation
handoff remains temporary and outside Git; this run is not appended to the ledger.

**Next gate:** human decisions H1–H4 and explicit authorization of specification.
Hard stop before Feature 006 specification, planning or implementation.


## Human decisions and reconciliation — 006-0002

**Authority:** the commissioning human explicitly approved H1–H4, recording the
prior observation and drafting the specification in run `006-0002` on 2026-11-03.
The original four questions and their alternatives above remain intact.

| Original question | Human decision / resulting initial boundary |
|---|---|
| H1 — Selection evidence | **ACCEPT.** `packages.lock.json` is the sole supported selected-version product input. `project.assets.json` and exported `dotnet package list` JSON are out of initial product scope. Their successful experiments remain useful research/oracle evidence for possible future expansion; this is no claim that either is unsafe in principle. |
| H2 — Declaration/context | **ACCEPT.** One explicit SDK-style C# project, one literal framework, unconditional literal direct PackageReferences and bounded numeric requested-version forms. Test/tool/analyzer direct references remain included. Transitives, project references and implicit/auto-referenced packages are not measured. Accept qualified supplier-coherence assertions and the documented failure/denominator policy; do not demand stronger historical/evaluated-scope proof. Fail closed outside the supported static subset. |
| H3 — Source authority | **ACCEPT.** Exact ID/version alone never authorizes public lookup. Bind package, project/framework, selected version, content identity/hash and asserted public origin. Require public content-hash agreement before treating public publication metadata as authority. Unknown/private/alternate/conflicting origin remains unmeasurable; never substitute public namesakes. Supplier assertions are accepted testimony, not cryptographic attestation. Libyears never executes NuGet/dotnet to establish this evidence. |
| H4 — Publication/latest | **ACCEPT.** Catalog `created` means first receipt by nuget.org. No catalog-update, listing/unlisting, restore or snapshot-time substitutes. Latest is greatest currently listed stable under a bounded NuGet ordering contract. Missing authoritative dates remain unmeasurable. The accepted discovery policy permits authorized prerelease/unlisted used versions with usable dates. |

**Consequential-question audit:** applying H1–H4 exposes no new consequential
product question. The existing metric, public-source protection and static-input
boundary remain intact. Activation, stable reasons, additive output fields and
the bounded syntax are finalized as proposed product behavior in the draft
[specification](spec.md), subject to independent specification review. Parser
organization, witness serialization mechanics, transport implementation and task
ordering remain later design work, not a new product approval gate.

**Readiness: READY FOR SPECIFICATION.** Drafting is explicitly authorized;
self-audit cannot approve the draft. No technical plan or task decomposition is
begun. The next gate after drafting is **INDEPENDENT SPECIFICATION REVIEW**.

Clerical provenance: `006-0001` is recorded once from its machine handoff, enriched
only with the explicitly authorized human post-run session/model/provider/effort,
agent-version, reported-runtime and two account-level credit readings. The
runtime classification and runtime note remain verbatim; the readings are
continuity observations, not per-run billing. No credit delta is stored.


## Human H3 refinement and empirical reconciliation — 006-0015

On 2026-11-04 the human approves two bound evidence classes for H3: native NuGet
package provenance from the producing dependency operation/context (identity,
selected version, actual origin and content hash), PLUS contemporaneous
producer-side attestation binding that native evidence to supplied project and
lock snapshots, framework/context and the bounded contract's required influence
assertions. The attestation supplies event/context claims native metadata lacks.
Retrospective replay alone MUST NOT satisfy H3, even with identical historical
project/lock bytes; it proves neither original event/context equivalence nor
absence of original unsupported influences. A new event can qualify prospectively
only on its own evidence and attestation, never on behalf of a historical event.

This refines only H3. H1/H2/H4, public namesake prohibition, local/public hash
agreement, no resolution/runtime package-manager execution, metric and all scope
exclusions remain binding. The corrected spec and independent disposition are
in spec.md/reviews.md; original decisions and empirical records above remain.

Historical OASim has no required contemporaneous producer attestation. 006-0013
therefore correctly left T016 incomplete. 006-0014 demonstrates useful isolated
native source/hash retention, but no equivalence to OASim's historical producer
context. Its overall D/BLOCKED result and execution deviation remain; replay
cannot make OASim retrospectively conformant. No historical records are rewritten.
Prospective production requires new exact authority described in release-validation.md;
no producer event or OASim access/modification occurs in this run.
