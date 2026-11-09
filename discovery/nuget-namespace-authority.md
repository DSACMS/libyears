# NuGet publication comparator authority — 006-0029

Status: frozen discovery candidate; disposition in [independent review](nuget-namespace-authority-review.md).
**HUMAN PRODUCT / NAMESPACE-AUTHORITY DECISION REQUIRED.** No new authority is
selected and no runtime change is implemented. Starting candidate is
`b449c5ddbbd2c5c702e03ab112511f89996e0482`, initially clean.

## Decision in view

Choosing nuget.org asserts that its package identity and publication timeline are
the applicable reference history for this attributable selected P/V occurrence.
It is a relationship between a dependency and a publication namespace, not merely
a choice of HTTP server. The package name alone does not establish that relationship.

Recommend investigating a **current repository comparator policy**, with positive,
closed repository source assignment and refusal of known conflicts, plus the
existing explicitly accepted namespace route. Do not require actual acquisition,
public artifact equality, producer chronology or deployment for this narrower
claim. Do not call a merely eligible source the unique applicable history.
A private feed may carry a different package with the same P/V; public existence
cannot disambiguate it. Conversely a public package acquired through a mirror
can truthfully use the public history if independent evidence establishes that
namespace relationship. Mirror configuration alone does not establish it.

The smallest useful conventional repository evidence is a safely read, applicable
NuGet configuration with a closed mapping policy assigning the identity uniquely
to an enabled canonical nuget.org source. A repository-only sole-public policy
without mapping is another, weaker convention requiring explicit product acceptance;
repository clears alone cannot prove the effective source universe on arbitrary hosts. This establishes **current
repository policy**, not the source of a historical restore. Accepting that policy
for an already selected snapshot is itself a consequential human product decision.
No upstream specification says that it authenticates the historical namespace of
an arbitrary retained lock. If that historical claim is required, configuration
alone is insufficient and bound accountable evidence remains necessary.

OASim does not meet this proposed floor: **0/51 comparator-authorized by repository
configuration or mapping**. Eight projects have no config; two only add an alternate
feed, without clear or mapping. No names were sent to nuget.org. The investigation
therefore does not deliver a debt number or promise 51/51 after a parser change.

## Durable authority and inspected evidence

The original [Feature006 contract](../specs/006-nuget-selected-evidence/spec.md),
[plan](../specs/006-nuget-selected-evidence/plan.md),
[review history](../specs/006-nuget-selected-evidence/reviews.md) and
[retrospective](../specs/006-nuget-selected-evidence/retrospective.md) preserve H1–H4:
lock selection, bounded declaration population, original producer/event/hash
requirements, and first-receipt catalog dates. Historical replay and zero-age
experiments are not reclassified. [OASim Phase2](nuget-oasim.md#source-authority--separate-from-selection)
records producer-reported source/hash evidence for that experiment, not universal
policy or implicit acceptance in ordinary scans.

[Repository sources](../maintenance/nuget-repository-sources/spec.md) establish
independent source-qualified occurrences, bounded discovery and unknown/unavailable
coverage. [Parity](measurement-evidence-parity.md) and its
[review](measurement-evidence-parity-review.md) led to the approved
[cascade C1–C6](../maintenance/measurement-evidence-cascade/spec.md): namespace
before lookup; event/content assurance optional. [Population discovery](nuget-population-basis.md)
and [review](nuget-population-basis-review.md), [snapshot acceptance](nuget-snapshot-acceptance.md)
and [review](nuget-snapshot-acceptance-review.md), plus the approved
[snapshot population](../maintenance/nuget-snapshot-population/spec.md) and
[repository snapshot](../maintenance/nuget-repository-snapshot/spec.md) contracts,
plans/tasks/reviews/validation retain A, then ordinary B1, then explicit B2.
Their population decisions do not decide namespace. This discovery supersedes none.

Current implementation inspected: nuget.py, nuget_provenance.py,
nuget_population.py, nuget_project.py, nuget_lock.py, nuget_input.py,
nuget_sources.py/discovery, nuget_registry.py, nuget_supervisor.py, nuget_worker.py,
registry transport; sibling requirements.py/snapshot, npm.py/Yarn and rubygems.py.
No private retained Phase2 bundle, cache or user/machine config was accessed.

## Exact current authority and claim decomposition

A requires an explicitly selected whole v1/v2 witness before constructing rows.
V1 binds project/lock/framework/SDK baseline and retains actual-origin and event
assertions. A singleton exact `https://api.nuget.org/v3/index.json` origins tuple
for matching case-insensitive ID/normalized selected version authorizes public
namespace; local hash failures no longer prevent age after independent namespace.
V2 binds the same snapshot/context, coherent_snapshot=true, complete explicit
population and false unsupported membership/version, framework/RID and source
influences. Its package record has id, version, namespace; namespace must equal
that exact URL. V2 asserts no acquisition event. Missing/private/unknown/multiple
or conflicting authority cannot use a public namesake.

B2 requires selected v3 byte/name/framework/coherent/external-Direct-complete
snapshot testimony. B1 can establish population/selection without testimony;
selected v3, if supplied, must fully validate and cannot be ignored on failure.
V3 packages reuse v2 namespace semantics, may be empty, and grant no authority
for omitted P/Vs. V1/v2 cannot be grafted onto B without their A baseline. There is
one selected witness per source, no merging contradictory envelopes, no discovery
or automatic acceptance. Explicit precision mode remains separate and unchanged.

LocalAuthority is an internal capability, not a public assertion blob. The worker
accepts validated protocol facts; it cannot infer authority from names. One
supervised metadata batch uses restricted TLS public endpoints, bounded responses,
complete SemVer2 registration and identity-bound catalog-created dates; greatest
listed stable is selected without compatibility filtering. Content comparisons
enrich assurance. Authority alone supplies neither a date nor a numerical age.
Source identity, occurrence weighting, metadata and arithmetic remain independent.

| Claim | What would establish it | What does not follow |
| --- | --- | --- |
| A Comparator | Accepted applicable namespace relationship for P/V plus valid public identity/dates | Actual supplying endpoint or public bytes |
| B Acquisition | Accountable event/source evidence about obtaining selected bytes | Public history from existence alone; deployment |
| C Content correspondence | Accepted identity/domain-bound content comparison | Where or when bytes were obtained |
| D Producer history | Bound testimony/records of a particular operation and baseline | Reproducible operation or runtime use |
| E Deployment/runtime | Separate deployment/execution evidence | Never follows from lock/config/package metadata |

B/C/D can corroborate A when their semantics actually bind to this occurrence.
They are sufficient evidence routes in some cases, not logical prerequisites for
all A claims. Even current testimony is accepted testimony, not authentication.
Human judgment is mixed: inherently needed to select the metric's comparator
policy and accept residual uncertainty; per-run testimony is scaffolding where
a reusable bounded repository policy can establish the deliberately narrower claim.

## Field and assertion decomposition

Classes use the requested numbers: 1 objective repository; 2 package-manager
configuration; 3 derived coherence; 4 historical acquisition; 5 content;
6 producer event; 7 human intent/policy; 8 public registry; 9 stronger assurance;
10 other. Multiple classes are explicit. “Necessary” means for A's narrow claim,
not merely currently mandatory implementation. H = human judgment, not parsing.

| Field/assertion/check | Claim protected | Class | Evidence source | Establish without execution? | Necessary for comparator? | Only stronger assurance? | Conflict/staleness risk | H actually required? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_id/project immediate name | Occurrence attribution | 1,3 | safe discovery/reader | yes current | association yes | no | shared/copied lock | policy once |
| exact project_sha256/lock_sha256 | Same supplied byte objects | 1,3 | bytes and digest comparison | yes | binding on testimony route | no | identical bytes do not prove history | no |
| version 1/2/3 envelope | Select assertion meanings | 10,7 | explicit file framing | yes | interpretation yes | no | old contract misread | policy once |
| framework | Selected context association | 1,3 | project/sole lock/witness | yes bounded | yes | no | imports/other contexts | policy once |
| sdk | Supported A baseline identity | 1,3 | literal Sdk + testimony | literal yes; imported behavior no | A contract today; not registry selector | no | implicit imports | accepted baseline judgment |
| sdk_version v1 | Historical baseline | 6,9 | supplier assertion | validate string only | no intrinsic source choice | yes | false/old event | supplier |
| producer name/version v1 | Particular producing tool | 6,9 | supplier assertion | validate only | no | yes | not authenticated | supplier |
| coherent_snapshot | Pair belongs to accepted snapshot | 3,7; v1 also6 | supplier; B1 current policy/parity | current coherence yes; history no | attributable selection yes | historical part stronger | copied coherent pair | route policy/supplier |
| explicit_population_complete | A's complete explicit scope | 3,7 | v1/v2 baseline | testimony only for hidden influences | population prerequisite, not source selection | no | hidden evaluated changes | supplier today |
| unsupported_membership_version_influences=false | No hidden population/version effects | 3,7 | baseline testimony | bounded visible facts only | population prerequisite | no | unchanged bytes/imports | supplier today |
| unsupported_framework_rid_influences=false | Sole supported context | 3,7 | baseline testimony | bounded visible facts only | context prerequisite | no | environment/imports | supplier today |
| unsupported_source_influences=false | No unsupported source influence | 2,7 | v1/v2 testimony | assertion validation only | source conflict exclusion yes; testimony not inherent | no | config/command overrides | supplier today |
| explicit_external_direct_complete v3 | Retained external Direct scope | 3,7 | accepted v3 | validate only; B1 has policy/parity | population, not namespace | no | SDK implicit/stale records | supplier/B1 policy |
| full ID/request/framework parity B1 | Current pair qualification | 1,3,7 | strict literal project + whole lock | yes | selection/context, not namespace | no | cannot prove producer | policy once |
| packages[].id | Bind package identity | 1,3 | witness/lock association | yes | yes | no | case aliases/duplicates | no |
| packages[].version | Bind selected identity | 1,3 | bounded normalization | yes | yes | no | unrelated public version | no |
| packages[].namespace v2/v3 | Applicable publication history | 7 | accepted package-specific testimony | validate, cannot discover truth | yes relationship; format not inherent | no | false/stale attribution | supplier today |
| packages[].origins v1 singleton public | Actual supplying source, used for namespace | 4,7,9 | accepted native/event account | not independently | one existing route; actual acquisition not necessary | acquisition part yes | copied/replayed/falsely asserted | supplier |
| explicit CLI witness acceptance | Accept supplied assertions | 7 | invocation | yes intent | current route yes; not inherent per run | no | discovered file is not consent | yes today |
| lock contentHash | Recorded selected hash | 1,5 | lock | yes record only | no | yes | hash domain/algorithm | no identity-policy judgment |
| witness content_hash/local equality | Lock/supplier content agreement | 5,9 | strict SHA512 decode/compare | yes comparison | no | yes | agreement not acquisition | no |
| public hash/equality/mismatch | Public artifact correspondence | 5,8,9 | catalog + accepted local hash | metadata only | no | yes | mismatch alone not private identity | no |
| origin_state/namespace_basis/measurement_basis | Honest staged claim labeling | 3,10 | accepted gates | yes | inspectability, not new evidence | no | overloaded origin meaning | policy once |
| assurance producer_event_asserted | Supplier event claim retained | 6,9 | v1 assertion | validate only | no | yes | unverified chronology | supplier |
| repository packageSources/key/disabled | Current eligible source policy | 1,2 | config bytes | yes bounded subset | potential new route, not sufficient when open/ambiguous | no | inheritance/override/key alias | policy once |
| source mapping winning patterns | Current identity-to-source assignment | 2,3 | closed config chain | yes bounded | potential sufficient route with conflict checks | no | equal winners/inherited map/cache | policy once |
| public P/V existence | That registry has a namesake | 8 | authorized public metadata only | network metadata, no target execution | necessary later, insufficient authority | no | private/public collision | never permission alone |
| catalog identity/created/listing | Date and latest stable in chosen history | 8,3 | registry adapter | yes metadata | required downstream | no | missing/alias/date conflict | existing date policy |
| deployment/reproducibility assertions | Executed/repeatable system | 6,9 | absent independent evidence | no here | no | yes | not derivable from above | separate authority |

## Repository configuration: facts and limits

[Microsoft configuration hierarchy](https://learn.microsoft.com/en-us/nuget/consume-packages/configuring-nuget-behavior)
loads defaults, machine, user and directory layers; collection sections combine,
closer values override keys and section-local clear discards earlier values.
Project versus solution invocation changes the applicable directory. Explicit
--configfile uses only that file. Environment expansion exists. No outside layer
was inspected here; absent in-repo config is unknown policy, not public authority.

[Configuration reference](https://learn.microsoft.com/en-us/nuget/reference/nuget-config-file)
defines source keys as aliases, values as URLs/paths, disabled sources separately,
and package credentials/API keys in other sections. Source order supplies no
PackageReference restore priority. A key named nuget.org can point anywhere;
endpoint identity must be checked. Clear resets its section, not every section.
The canonical v3 index is the supported endpoint. Local paths and relative
sources do not identify a public namespace. Authentication settings are not
comparator evidence and must never be emitted, expanded or used to access a feed.

[Settings implementation](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Configuration/Settings/Settings.cs)
checks case-sensitive-filesystem names in order nuget.config, NuGet.config,
NuGet.Config; case-insensitive systems use one spelling. A portable bounded
product should reject multiple colliding spellings rather than silently yield
different policies. Source provider uses its own source-name comparisons; XML
keys, source aliases and package IDs must not be conflated into one case rule.
[Source provider](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Configuration/PackageSource/PackageSourceProvider.cs)
combines configured/default sources and disabled settings. In particular,
AddDefaultPackageSources re-adds unmatched machine NuGetDefaults.Config sources
after normal settings, even after repository packageSources clear. Therefore clears
do not prove host-wide effective sole-public status. This is an upstream dev-source
observation, not a claim about a particular historical OASim client or host. No
external configuration was inspected to try to resolve it.

Removing a known key cannot remove arbitrary unseen inherited sources. A future
subset could support validated remove for supported sections, or refuse it;
unknown remove behavior must not be approximated as clear. Unknown ancestor
mapping/disabled entries can affect even a public-only packageSources section.
A conservative repository-only convention resets all relevant ordinary sections
in a repository anchor, then safely applies supported descendants. It must disclose
that machine default-source injection remains outside that convention. Unique
closed mapping can make additional unmapped default sources irrelevant for X; this
requires a resolved enabled public alias and closed mapping precedence, not a claim
that no other source exists. Without mapping, sole-public means sole in the bounded
repository policy, not proven sole effective NuGet source. A stronger effective-source
claim remains unknown without separately authorized external evidence.
Solution/project context ambiguity must refuse, or explicitly select a new
project-anchored comparator convention without calling it the historical invocation.

## Package Source Mapping

[Microsoft mapping rules](https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping)
assign IDs by exact pattern first, then longest prefix, then *. Equal winning
patterns can identify multiple sources. A more-specific private match defeats a
public wildcard; a more-specific public match defeats a private wildcard. Unmapped
IDs do not get an implicit public fallback. Both direct and transitive packages
need mappings for restore, but this tool must not add transitive populations.
Mapping applies on download; a cached package may bypass it. It proves no acquisition.

[SearchTree](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Configuration/PackageSourceMapping/SearchTree.cs)
normalizes pattern/package matching case and returns source keys for the winning
node; [mapping model](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Configuration/PackageSourceMapping/PackageSourceMapping.cs)
separates that result from source resolution. A candidate product must resolve
keys to enabled canonical endpoints, not accept the text of a source alias.
Disabled or unresolved winning sources are not positive public authority. Reject
ambiguous mapping/alias collisions; do not treat every textual overlap as conflict
when NuGet specificity deterministically picks one winner. Unique public assignment
is sufficient only for the proposed current-policy claim, after inheritance and
source-affecting conflict checks. It is not the current approved testimony route.

## Project, lock, generated and retained evidence

[Restore property reference](https://learn.microsoft.com/en-us/nuget/reference/msbuild-targets#restore-properties)
identifies RestoreSources, RestoreAdditionalProjectSources, RestoreConfigFile,
RestoreFallbackFolders and additional fallback properties. Project, props/targets,
Directory.Build files, environment and command-line values can affect these.
[NuGet.targets](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Build.Tasks/NuGet.targets)
collects settings and per-framework additional sources. They must be treated as
conflicts/unknowns in a static source policy, not evaluated to force an answer.
No observed literal property is not proof about every imported/SDK/environment fact.
A source-policy convention must state its current repository boundary and exclude
claims about effective restore execution. Unknown explicit imports or computed
source/config paths should block automatic policy, without following external paths.

[Lock documentation](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files#locking-dependencies)
and current whole-lock parser show schema1 framework, Direct/request/resolved/hash
records, not an endpoint or per-package source assignment. Direct does not confer
namespace. Coherent copied/dirty locks remain eligible population under B1 and
supply no historical config association. Current config changed after snapshot
can select a current comparator only under the proposed explicit convention;
it cannot authenticate the old source or override a known contrary namespace.

[ProjectRestoreMetadata](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.ProjectModel/ProjectRestoreMetadata.cs)
has Sources, ConfigFilePaths and fallback folders. Assets/dgspec/generated restore
output may retain eligible-source context, not necessarily per-package origin.
They are future optional bound evidence candidates, not ordinary authority now.
No ignored/generated assets were interpreted in this audit. Existing Phase2 native
metadata source/content records could support stronger accepted testimony if
available, adequately bound and explicitly authorized; no new restore is needed
merely to make v2 namespace testimony, but its author needs an accountable basis.
The Updater retained v1 is not automatically selected. Neither historical
experiment narrative nor another project's witness grants sibling authority.

Nuget.org is conventional and often configured by tooling. That is an ecosystem
or package-manager default fact, not evidence that this repository selected its
publication namespace. Public metadata can validate an authorized P/V, not grant
permission to disclose an unknown/private identity. Neither convention nor public
existence repairs explicit alternate/private evidence. No endpoint probing,
redirect discovery or private-feed request belongs in authority selection.

## Bounded static interpretation, if separately selected

This is a proposal, not an implementation plan or approved grammar. Reuse bounded
no-follow contained discovery/reads, with an explicitly chosen root-to-project
scope, finite config count/bytes/depth/entries/string/pattern limits. Do not search
outside the repository or follow symlinks/reparse points; unavailable primitives,
unreadable relevant configs or budget exhaustion make authority unknown.

Require framed XML, exact configuration root, refuse DTD/entities, unknown relevant
nodes/attributes, duplicate keys/sections, nested impostor sections, malformed
booleans, computed/environment values, and alias ambiguity. Explicitly specify
supported clear/add/remove order per section before coding. It is safe to support
less than NuGet; unsupported syntax must refuse, not be silently ignored. Known
unrelated sections require a reviewed allowlist and privacy handling, not a global
ignore-everything rule. Credentials/API keys/URL userinfo/query tokens should cause
safe refusal initially; never print raw values or use secrets. This trades yield
for a small reviewable parser; credentials on another source prove neither private
origin nor public comparator and could later be handled separately.

Initially recognize only the exact canonical v3 endpoint; future URL equivalence
could admit scheme/host casing and default443 after strict parsing. Path casing,
trailing slash, percent-encoding, query/fragment, redirects, CNAME/custom domains
and v2 endpoints are not automatically interchangeable. Equivalent-looking URLs
must not turn arbitrary hosts into nuget.org. Existing witness exact-URL contract
stays unchanged. Fix cross-platform casing behavior; use no filesystem source
traversal or credential resolution. Multi-source mapping deserves its own negative
controls. A repository-only public subset can be useful under an explicitly selected
convention; closed unique mapping is stronger identity assignment without emulating
all NuGet or proving acquisition.

## Policy alternatives

All authorization below is hypothetical pending human selection. P0 and P6 are
the same authority mechanism, separated to compare keeping it exclusively versus
preserving it within a new cascade. None proves acquisition without extra evidence.

| Policy | Truthfulness/private namesakes and ambiguity | Inheritance/staleness/mapping | Usability, burden, complexity and parity |
| --- | --- | --- | --- |
| P0 keep testimony only | Exact accepted P/V namespace; false testimony residual | bound bytes/context; historical truth still supplier responsibility | offline/local archives/non-Git work; high human burden, existing code |
| P1 public namesake | Existence cannot select namespace; private collision fatal | ignores source/mapping/conflicts | easy but disallowed; online disclosure before authority; not Ruby parity |
| P2 ecosystem default | A new assumed comparator, not established repository relation | absence/defaults conceal private source; explicit negative evidence must refuse | low burden, simple, works archives; copies Python/npm limitation; reject |
| P3 repository config | Sole public in closed repository-only policy supports a deliberately bounded convention, not effective-host exclusivity | additive public entry insufficient; ordinary sections closed; machine default injection remains external | inspectable/offline/non-Git; moderate subset work; Ruby-like source semantics |
| P4 mapping | Unique winning public assignment can disambiguate multi-feed and exclude unmapped machine defaults for X | mapping inheritance, aliases, enabled public source and specificity must be closed | lower per-package testimony burden; more parser complexity; no acquisition claim |
| P5 config + mapping | unique public mapping first; optional repository-only sole-public convention if mapping conclusively absent | unknown mapping inheritance blocks; machine-default limit disclosed; no downgrade after private/ambiguous/unmapped/conflicting evidence | useful conservative cascade; explicit unavailable state; cross-platform tests needed |
| P6 retained testimony | Existing v1 acquisition, v2/v3 namespace meanings retained | validate independently; no repair by merging contradictions | accountable fallback/stronger enrichment, not discovery trust |
| P7 cross-evidence | Accepted population/selection + P5 or P6; contradictions terminal | current comparator policy distinguished from historical namespace testimony | recommended direction; preserve occurrence/metadata gates, address A separately |
| P8 explicit comparator-only declaration | Deliberate repository policy assigning history without pretending restore config | needs new schema/selection/conflict and snapshot semantics decisions | potentially smallest text for maintainers, but new bespoke format and human intent; investigate only if conventional subset is insufficient |

P3–P5 require human acceptance of current policy for dating retained selected
versions. They do not assert that all packages physically obtained from an eligible
source are its public identity. A configuration with public and private feeds and
no unique assignment supplies eligibility only, insufficient comparator selection.
A broader “any applicable configured source” policy would knowingly allow
competing same-P/V histories; reject it for this metric. Public dates remain dates
in the chosen history, not necessarily original upstream release or deploy age.

## Configuration and adversarial decision matrix

Codes: Y = proposed positive authority; U = unknown, no lookup; R = known contrary
or unsupported evidence, no lookup. P0/P6 require valid explicitly accepted testimony
T in every case, subject to the no-conflict rule; otherwise U. P1 would authorize
on public existence even where wrong; no such query was made. P2 could assume
public on absence, a reason it is not recommended. P8 authorizes only a future
valid explicit declaration, never from these cases alone. Thus the table evaluates
all policies without suggesting unsupported implementations exist.

| Configuration case / adversarial case | P3 sole-public config | P4 unique mapping | P5/P7 repository branch | P1/P2 danger or necessary caveat |
| --- | --- | --- | --- | --- |
| A/1 explicitly only public, inheritance open | U | U without mapping | U | one entry is not entire source universe |
| C/2 unique public winning map, closed config | U if multiple enabled feeds | Y | Y | alias must resolve to public |
| B/3 public + private, no mapping | U | U | U | first/fastest feed not priority authority |
| D/4 private winning map | R | R | R | no public fallback |
| E/5 equal public/private winners | U | U | U | genuine ambiguity, not all overlap |
| M,N/6 public exists, config points private | R | R | R | namesake cannot repair |
| F/7 no repository config | U | U | U | P2 assumes what is missing |
| G/8 clear sources then only public | Y for repository-only convention with relevant ordinary sections closed; effective-host status U | Y only with unique closed map | same deliberately bounded claim | section-local clear cannot remove injected machine defaults |
| H/9 relies on user/machine defaults | U | U | U | do not read outside config |
| J/10 source-affecting project property | U/R | U/R | U/R | safe unknown or known contradiction; no evaluation |
| K/11 malformed/ambiguous/unsupported config | R | R | R | no fallback to defaults/testimony to hide conflict |
| 12 public version possibly acquired privately | Y if independently closed public comparator policy | Y if independently assigned | Y only for current-policy claim | acquisition remains unknown |
| 13 private mirror carries public package | U/R | U/R if mapped mirror | U/R without separate accepted identity evidence | mirror not canonical public URL |
| L/14 config changed after lock | Y only for qualified current-policy claim | same | no historical claim; known contrary facts R | history not recovered by hashes |
| 15 dirty/untracked coherent config | same as clean | same as clean | eligible current policy; disclose boundary | Git tracking not source identity |
| 16 equivalent canonical spelling | U if outside exact initial subset | U | U unless separately supported normalization | safer refusal not a private-source claim |
| 17 redirect/alias endpoint elsewhere | R | R | R | never follow to discover authority |
| 18 credentials in config | R initial subset | R | R | refuse without disclosure; not proof of private origin |
| I/19 local filesystem source | U/R | Y only if closed unique public map excludes it for X | same | local namesake not public identity |
| 20 public-looking ID, authority unknown | U | U | U | spelling proves nothing |

R can mean unsupported syntax rather than a proven private namespace. A future
spec must preserve that diagnostic distinction. Invalid supplied testimony is not
silently discarded; accepted testimony plus known contrary namespace is terminal.
Ambiguous config cannot be bypassed by default-public or weaker evidence. A separate
accountable claim may explain a mirror/current-versus-historical distinction only
under an explicitly designed contract, not informal override in this discovery.

## OASim all-occurrence empirical audit

The [51-row CSV](nuget-namespace-authority-oasim.csv) records every project path,
package identity, selected version, population basis, framework, config/mapping,
visible source properties, inheritance uncertainty and P0–P8 result. Identity is
source-qualified; the same ID in different projects remains separate. All sole
contexts are net10.0. Current parser results and selected identities were checked
against each exact project/lock pair, not assumed from the north star.

| Project | Basis | Occurrences | Repository source evidence | Mapping | Proposed P3–P5/P7 authority |
| --- | --- | ---: | --- | --- | --- |
| MRCalc | B1 | 9 | additive alternate HTTPS feed, no clear | absent | unknown |
| MatchRunBenchmarks | B1 | 2 | no config | absent | unknown |
| MatchRunCLI | B1 | 8 | no config | absent | unknown |
| MatchRunEngine | B1 | 4 | no config | absent | unknown |
| MatchRunProfileUpdater | A | 1 | no config; retained unselected v1 | absent | unknown |
| MatchRunProfiling | A | 2 | no config | absent | unknown |
| MatchRunTests | B1 | 5 | no config | absent | unknown |
| OASim | B1 | 9 | additive alternate HTTPS feed, no clear | absent | unknown |
| OASimCLI | B1 | 9 | no config | absent | unknown |
| SimulationEngine | B1 | 2 | no config | absent | unknown |
| Total | A2/3 + B1 8/48; B2=0 | 51 | zero unique public assignments | none | 0/51 |

The two configs contain only packageSources/add, one noncanonical source alias
AvaloniaCI each; no credentials, disabled sources, clear/remove or mapping.
They do not demonstrate private acquisition, nor assign every package to that
alternate source; inherited additional policy remains unknown. Eight absent
configs supply neither public nor private assignments. Within tracked/nonignored
repository inputs, no Directory.Build.props/targets, Directory.Packages.props,
other props/targets or literal source-affecting project properties/explicit Imports
were found. Existing SDK and unknown external inputs remain uninterpreted.
No config outside target, private feed, generated asset or cache was interpreted.
P2 would assume public for 33 occurrences with no config while refusing 18 with
alternate evidence; that is an unsafe policy projection, not empirical authority.
P1 public existence is deliberately untested. P0/P6 accept zero ordinary mappings;
Updater's retained v1 is not accepted by ordinary invocation and not universalized.

Trusted ordinary CLI main entry, human/JSON/verbose-JSON, executed with socket and
subprocess creation denied: all exit0, stderr empty, zero attempted network/process
calls; verbose JSON byte-equal JSON. Actual repository N51/M0, coverage null,
total0.0, other aggregate numerics null; 48 selected B1 unmeasurable namespace rows,
two A source_errors nuget_provenance_missing. These are no measured ages.
No package manager, target program/tests or restore was executed.

## Why A stops earlier than B1

A's complete static grammar is stronger visible population interpretation, but
parse_provenance still demands supplier baseline/completeness/context before any
row selection. B1's newer human policy independently qualifies a current pair,
so its loop can stage 48 selected versions with context=None and refuse namespace
per row. The two A sources know N=1 and N=2 and locally have selected versions;
ordinary output does not stage those three selected rows before whole testimony.
Do not misreport them as three ordinary selected rows today.

There is a real additional fact in A's testimony: assertions about imported/SDK
membership/context/source influences, not merely acquisition. A's static parser
does not establish those hidden facts. Thus removing the whole witness under the
unchanged A claim is not a factual correction. The asymmetry is historical contract
layering plus a later narrower B1 policy choice, not proof that declaration-derived
age intrinsically requires stronger acquisition assurance. The smallest future
correction would extend **qualified current-pair population/selection policy** to
supported ordinary A, using equally strict whole-lock/ID/request/framework parity
and no known source/context conflicts, then apply the same independent comparator
floor. Keep population_basis declaration_derived, disclose current-policy versus
supplier-baseline claim, and preserve explicit precision semantics unless separately
approved. Do not route A through B, accept v3 on A or fake absent baseline testimony.
This requires new human authority and prospective contract/output review; it is
separate from selecting a namespace route and cannot by itself measure the three.

## Narrow sibling parity

Python accepts exact requirements, plus optional requirements/snapshot matching,
and uses fixed PyPI metadata. Exact pins need no snapshot and may survive an
optional snapshot that omits their name. URL/VCS/local forms are refused, but no positive source
assignment from pip configuration is required; it does not prove acquisition.
npm production manifest + lock/Yarn selections use fixed registry.npmjs.org.
Recognizable URLs, aliases, links, local/VCS/workspace forms are unsupported;
registry-shaped scoped IDs are accepted without inspecting .npmrc or scoped registry
policy, and lock resolved/integrity do not gate namespace. Alternate registries
can therefore leave an attribution gap. This existing limitation is not NuGet
authority and no sibling rewrite is selected.

Ruby's Gemfile.lock supplies supported GEM source blocks and exact direct/spec
associations. Every relevant same-name spec source must have a singleton literal
https://rubygems.org remote (optional trailing slash); private/GIT/PATH/multiple
remotes or explicit ! pins refuse. Missing selection cannot become measurement.
Gemfile is not evaluated or used for ordinary source authority. This is repository
source semantics, without acquisition/producer proof, and the closest precedent.
NuGet locks lack this embedded source relationship, a concrete ecosystem difference.
NuGet therefore needs another positive route, but not necessarily supplier history:
closed config/mapping could supply the narrower current policy if approved.
No weakening of NuGet or strengthening siblings is justified merely by symmetry.

## Recommended prospective cascade and human gate

1. Establish population and exact selection under approved A/B1/B2. Keep all safety,
   context, whole-evidence and known-conflict checks. A-floor correction is separate.
2. Validate every explicitly selected witness under its existing meaning; retain
   accepted namespace and stronger facts. Invalid or conflicting evidence is terminal,
   never downgraded. Existing v1/v2/v3 admission rules are not changed here.
3. For sources lacking accepted namespace, optionally apply a newly approved closed
   **current repository comparator policy**: safely interpreted sections/chain,
   no unsupported source influences, mapping winner first when active. Unknown inherited mapping state blocks.
   When mapping is conclusively absent in the bounded repository policy, only the
   separately accepted repository-only sole-public convention may qualify; machine
   default injection means this is not effective-host exclusivity. When mapping is
   active, an unmapped identity, private winner or equal competing winners never
   falls through to sole-public/default inference.
4. If automatic facts are insufficient, existing valid explicit testimony remains
   an accountable fallback subject to conflict refusal. This is logical fallback,
   not witness auto-discovery or combining incompatible contracts. Preserve the
   distinction between current policy and accepted historical/source testimony.
5. Only after positive authority issue public metadata capability. Apply existing
   complete identity/listing/date/latest/metric checks. Enrich assurance separately.

This precedence is a recommended decision shape, not an approved algorithm.
A future specification must define conflict reconciliation and relevant input
closure, supported config subset, current policy disclosure and A admission before
planning. Two sources can legitimately embody different publication namespaces;
never aggregate a private namesake into public debt by convenience.

**Exact next human gate:** accept or reject current repository comparator policy
as sufficient for dating a selected retained version, without claiming its historical
source. If accepted, authorize bounded specification and independent review for
closed unique mapping plus retained explicit testimony, with a separate explicit
choice about the weaker repository-only sole-public/no-mapping convention, and
separately decide whether to extend current-pair acceptance to ordinary A. Neither
choice is an authorization to implement now. If historical namespace is essential,
keep explicit accountable bound testimony. For present OASim, identify accountable
existing namespace evidence or intentionally supply durable comparator policy;
configuration parser work alone establishes no new authority on these bytes.

Unknowable here: actual acquisition endpoint/event, exact public-content equality,
producer chronology/baseline beyond accepted assertions, effective external config,
complete evaluated imports/environment, deployment and reproducibility. Public
metadata might still be unsuitable after future authority; 51/51 is not guaranteed.

## Verification, integrity, hosted evidence and methodology

Before target interpretation, capture recorded HEAD/full NUL Git status/index digest,
223 tracked and12 nonignored untracked files' bytes/modes/size/mtime and50 ignored
names. No ignored relevant config/props/targets input was present. Baseline HEAD
1e937015e1d242fee5597ea0fbdc4cd5c983f101; manifest SHA256
7a8e1746c356ef502adfef9c10e4c911e74d4180a167001815d57aa192a1f26f.
Exact final equality and review verification are recorded in the review artifact.
Ignored unrelated bytes and OS-wide atomic invariance are not claimed. No cleanup.

Supplied Windows evidence for exact b449c5d is recorded prospectively in the
[validation record](../maintenance/nuget-repository-snapshot/validation.md): Windows
Server2025/windows-2025-vs2026/CPython3.11.9, worker3 PASS, full751 in159.702s,
OK with51 expected skips, diff check and prior/new portability witnesses PASS.
Other hosted results remain unobserved; no job completion is inferred. Runtime
warnings/capacity and test-performance opportunities stay separate; no CI changes.

006-0028 is appended exactly once from its authorized original baton and supplied
session/model/provider/effort/version/runtime1142 and account81/83. Original runtime
provenance/confounding remains unknown, no derived delta. This run006-0029 inherits
credits_before83 under human-confirmed continuity. Current runtime/after counter
are unknown; current run/children are not appended. Handoff is outside Git.

ROADMAP17 is refined, remains EXPLORE, separates comparator, stronger assurance,
A-floor, parser, evaluated MSBuild, CI and performance. Human gates may scaffold
unknown trust boundaries; claim decomposition can identify unnecessary stronger
floors. Hosted validation is asynchronous evidence; product authority is still a
synchronous human gate. Ordinary smoke isolates the product blocker. These are
retrospective inputs, not a reusable framework. No metric/schema/output/runtime,
parser, test, changelog or historical-contract changes. No commits or push authorized
by this discovery; changes remain reviewable in the working tree.
