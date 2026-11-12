# Feature 007: Maven plural dependency-age views

## Status and authority

**Run007-0008 review candidate.** The human selects conservative latest eligibility
following007-0007. Unknown qualifiers refuse only when they could affect the eligible
maximum; unfamiliar versions are not declared invalid. The conventional time basis,
H1=NO, plural views and occurrence population remain selected. Publication authority
remains **not established**; [historical investigations](publication-history.md),
[provider alternatives](age-evidence-alternatives.md) and [practice](ecosystem-practice.md)
retain the chain and its limitations. Current approval disposition is in [reviews](reviews.md).

Normative companions are [selected latest policy](latest-policy.md#selected-policy--run007-0008),
[bounded local/source policy](source-policy.md) and [metadata transport/time](metadata-contract.md).
They complete the technical subset and fixed budgets; historical alternatives and
pending paragraphs in evidence records are superseded by their current decisions.
Only whole-specification approval permits the already authorized plan/review and
sequential tasks/review stages. Runtime implementation, live target validation,
private access and Git publication remain separately unauthorized.

## S1 — Outcome and invariant

An ordinary directory invocation discovers bounded supported Maven project sources
and presents **Declared** and **Observed** dependency age side by side. Each view
has independent evidence, scope, availability, numerator, denominator, coverage,
statistics and limitations. An absent view remains visibly unavailable. Neither
replaces the other, and their totals are never added or subtracted into a new
metric. Existing libyears arithmetic, timestamp anomaly rules, exact zero for equal
versions and exclusion of unmeasurable rows from numerical aggregates remain.

Declared means a request version fact established from supported repository model
text and attributable local indirection. A bare Maven literal is a request, not a
proof of resolution. Observed means an exact version established by an accepted
**retained dependency-system selection record**, bound to the occurrence/context.
It never means runtime loading, deployment, installed state, telemetry or fresh
execution. An observed fact describes the selection represented by accepted retained
evidence, not a successful build or identical current resolution. A differing
request/selection is not intrinsically a contradiction.

Initial scope is Maven project dependencies. Gradle support, generated exports,
resolver/effective-model execution, parent/BOM fetching, dependency installation,
archive inspection, plugin execution, sibling-view retrofits, gap/intersection
metrics and new metric arithmetic are excluded. DPC is the primary public
proving ground; AB2D challenges assumptions without enabling Gradle ingestion.

## S2 — Terminology, facts and occurrence association

Use **declared / observed**, with machine evidence explicitly identifying
`retained_dependency_system_selection` when an observed fact exists, and
`supported_local_base_model_request` for the initial declared basis. The terminology alternatives retained from
earlier review explain the selected terms:

| Pair | Benefit | Risk / disposition proposed |
| --- | --- | --- |
| declared / observed | Human questions are clear; does not force one resolver model | Retain with the bounded definition above; never runtime shorthand |
| declared / resolved | Familiar build terminology | May imply a current resolver execution; not preferred |
| requested / selected | Precise fact vocabulary | Useful evidence labels; less direct as user-facing age headings |
| declared / retained-selection | Most explicit retention boundary | Precise machine basis/documentation term; cumbersome heading |

A source identity is the safe POSIX root-relative POM path, not its artifact name
or absolute checkout path. A base-model context distinguishes a particular source
and supported local-parent chain; no profile/configuration is inferred from the host.
Maven occurrence identity is source + context + the case-sensitive model key
(groupId, artifactId, type, classifier). Default type is jar, classifier absent.
Scope and optional are attributes; version is a fact, not part of this identity.
Different request and observed versions therefore can belong to one occurrence.

Keep original type/classifier and a separately derived artifact key (group,
artifact, extension, effective classifier). Known built-in handlers only may map
between these keys. test-jar has an implicit tests classifier unless explicitly
overridden; it must not collapse into ordinary jar. Model-key matching for local
management must follow Maven's type/classifier rules, not an extension-only alias.
An explicitly empty classifier is unsupported, not silently equivalent to absent.
Absent versus explicit jar type share a model key; test-jar/absent, jar/tests and
test-jar/explicit tests have distinct model keys but map to the same jar/tests
artifact. Never use artifact aliases for cross-key management defaults or automatic
observed joins. Same-key duplicates differing only in version/scope/optional remain
ambiguous; refusing them is this bounded contract's rule, not a claim that Maven
always rejects those inputs. Unknown/custom handlers are unsupported artifact identity; never
execute an extension to infer the mapping. No case-folding or generic SemVer
normalization of Maven coordinates/versions is permitted.

Public comparator and time identity are specified at S7. At minimum retain
case-sensitive group/artifact/version and supported artifact variant. The selected
GAV POM-representation time basis must disclose that granularity and must not certify
classifier-specific publication, availability or bytes. Matching public metadata cannot establish
occurrence identity or authorize a join.

A join requires: accepted retained format/authority; explicit binding to the same
current source/model inputs and context; matching direct dependency model/artifact
identity through supported mapping; directness, and unambiguous association.
A hash binds bytes, not producer history or evaluated completeness. Coordinate
similarity, a shared basename, co-location, same version or a request-range match
alone never suffices. Competing selections in different contexts remain separate;
ambiguous association is unavailable, never an arbitrary match.

The model can express declared-only, observed-only, paired and unknown-population
cases. Observed-only requires retained direct-population authority; transitives
cannot be promoted to direct because they lack a matching declaration. Unknown
population is a source/view state, not an invented anonymous dependency row.
Initial Maven has no accepted observed reader (S5); model capacity is not an
intake or execution feature.

## S3 — Maven population and bounded local model

Discover independent safe repository-contained project POMs within a finite scan
boundary. Root aggregator and parent roles do not create traversal authority;
modules listed outside the selected root are not followed. Nested project sources
may be recognized independently; root-relative identity distinguishes them.
The fixed discovery/input/XML/parent-chain/expansion budgets and fail-closed
boundary behavior in [source-policy.md](source-policy.md) apply; no unbounded traversal.

The initial declared basis is **supported local base-model direct requests**,
not a complete evaluated Maven build. Inspect ordinary project/dependencies;
merge supported local parent contributions by Maven model identity. One same-key
child occurrence replaces a second inherited occurrence, but its fields are merged:
child-explicit fields win, absent child fields inherit, then supported management
fills only fields Maven manages. Scope defaults apply after management; optional
is never managed and defaults false after ordinary dependency inheritance. Do not
default either field before its applicable inheritance/management stages; keep per-field origin and consumer/source POM separately.
A parent version1.0/scope=test plus child version2.0 with omitted scope gives one
child occurrence with version2.0 and inherited test scope. This does not certify
an evaluated build. Parent aggregation is not inheritance:
a module without that parent relationship inherits nothing merely by being listed.

Each supported POM, including packaging=pom, owns its own base-model requirements.
A parent with its own direct requirements is one source; supported children inherit
those requirements as independent child occurrences. The resulting total weights
project-model requirements, not distinct upgrade work or runtime consumers. Five
consumer modules sharing a request produce five occurrences; do not deduplicate
across sources. A root parent's own occurrence is not copied a second time within
that same source. Distinct type/classifier keys remain distinct. Duplicate or
conflicting same-key written declarations are ambiguous, not countable repetitions.

Internal-project exclusion requires a **static aggregation association**, not merely
repository co-location or matching coordinates. An unconditional literal modules
edge binds its aggregator to a safely contained child POM; recursively supported
nested aggregators form one associated component. Independent roots form separate
components even if coordinates match. Parent edges alone do not join components.
Self/cyclic/escaping/missing or profile/property-dependent module edges leave the
affected association unknown; never search ancestors/outside root to repair them.
A project reached by incompatible roots or duplicate project GAVs is ambiguous.
These are supported repository associations, not proof of actual reactor execution.

Exclude a dependency as internal only if its exact supported GAV uniquely names a
project in the same unambiguous component. Model type/classifier variants retain
that project-owner association; this does not assert attached artifact availability.
A different version is not excluded merely by group/artifact equality. Never exclude
an organizational prefix or coordinate from an unrelated discovered root. If unknown
membership/project identity/version could change this classification, affected
external population is unknown. Unrelated sources and clearly external GA identities
remain usable. No project edge adds transitive closure population, and no vendored
repository is read to construct the graph.

| Construct | Initial declared treatment |
| --- | --- |
| Ordinary project dependency | Count one external occurrence after supported identity and local-model association |
| Local parent direct dependency | Inherit once per supported child model; preserve origin and override trace |
| dependencyManagement | Never adds population; supported exact-key local management can supply missing request fields |
| Imported BOM | Management only; no network fetch. An unresolved BOM leaves relevant managed facts unavailable, not fabricated. Explicit request facts survive if not dependent on that management |
| Version properties | Supported literal local/parent properties, finite expansion, child override and project built-ins only where Maven context is established; unresolved/cyclic/environment/system/CLI values remain unavailable |
| Profiles | No host activation. Consider the source and its local ancestors: membership/module/identity changes, or versions/properties that can change internal attribution, make affected external population unknown. Fixed external membership with variant requests withholds only affected facts. Unrelated plugin/test-execution profiles preserve independent base facts |
| Optional | Included; optional controls propagation to consumers, not existence as this project's direct requirement |
| compile/runtime/test/provided | Included; no arbitrary production-only or name exclusions |
| system | Count known external direct identity; never follow systemPath or assume Central correspondence; age unavailable under source refusal |
| Explicit tooling artifact under project dependencies | Included under the same scope rules, regardless of artifact name/purpose |
| build plugins / their nested dependencies | Separate build-tool population, excluded; coordinates alone do not make them project dependencies |
| Ordinary type=pom dependency | Included as a project dependency when attributable, unlike a BOM import under management |
| Custom type/extension or unknown relevant model semantics | Refuse the dependent fact/population claim at the smallest safe scope; no evaluation |

Read only contained local parent POMs whose relativePath/default lookup and parent
GAV match; do not substitute an arbitrary file or search caches. Explicit empty
relativePath/external parent is not local evidence. No complete inherited population
is claimed when a missing parent could contribute direct requirements. Known local
rows may still have useful facts/ages; complete N and coverage remain unknown.

Literal group/artifact/type/classifier identity is the initial identity subset.
Unsupported identity indirection is a population limitation, never a guessed ID.
Missing inherited population does not erase safely attributable local rows. Unsafe
framing rejects the source; a missing fact rejects only dependent facts. Unknown
complete population is represented as S6 requires, with safe rows preserved.

Supported local attribution order is deliberately narrower than an effective model:

1. Bind a contained parent chain using literal matching parent GAV and supported
   relativePath (including Maven's default). Local project group/version may inherit
   literal values from that chain; unresolved project identity remains unknown.
2. Merge raw ordinary dependency and local management records by exact model key,
   retaining explicit versus absent fields. Child fields take precedence; missing
   child fields inherit. Duplicate same-key records at one level are ambiguous,
   never an order-based choice. Key defaults (jar/absent classifier) identify records;
   scope defaults wait until after management. Optional is not managed; its false
   default follows ordinary dependency inheritance and is unaffected by BOMs.
3. Merge scalar repository properties parent-to-child, with child values winning.
   Supported version substitutions are `${name}` where name is an ASCII letter
   followed by letters/digits/underscore/dot/hyphen, plus `${project.version}` and
   `${project.parent.version}` only with known literal local project/parent versions.
   Reserved model expressions take precedence over ordinary properties: only the
   two explicitly supported project builtins above may resolve, from their known
   model fields, never from same-named properties. All other project./pom. expressions,
   project.directory, basedir/baseUri and env/system/settings/user/session namespaces
   are unsupported here, with no repository-property fallback or host read.
   Exclude project.directory from inherited scalar properties; any request using it
   is unsupported even when a local text value exists. Expand inherited raw expressions in the consumer's supported property context, with finite
   depth/size, cycle/duplicate-property refusal and per-field origin trace. No XML
   subtree/expression evaluation, CLI/host property override or arbitrary builtin.
4. An explicit dependency version remaining after inheritance beats management,
   including management newly written in a child. For absent dependency versions,
   an unambiguous ordinary management **field written on the consumer** may supply
   its supported version; child-local explicit fields beat inherited matching fields.
   Without any imports in the local chain, unambiguous inherited ordinary management
   may also supply absent fields. With unresolved imports anywhere in that chain,
   do not use inherited management fields as fallback past that uncertainty. The
   consumer-local exception applies per field, not to an entire merged record:
   child management writing only scope=test cannot make an inherited parent version
   admissible through an unresolved import. Independently supported consumer-written
   management fields and direct explicit facts still survive. This is a
   conservative supported subset, not a claim about every import precedence case.
5. Local **and** external imported BOM contents are not read initially. Missing
   management-derived version/scope facts stay unavailable. Never apply compile
   across unknown management that could supply scope; default only after absence
   is established. Optional is not management-derived: inherited direct optional
   survives, otherwise false, even if matching management writes optional=true. Known explicit versions survive even
   when another fact is unavailable; count known external identities independently.
6. No profile activation is evaluated. Inspect possible relevant writes in source
   and ancestor profiles because activated ancestor effects may be inherited even
   though profile definitions themselves are not. Dependency version/property changes
   that cross a matching project GAV, project GAV/module changes and unknown module
   membership can change **external population**, not just age. Withhold that complete
   denominator; independently safe rows/facts survive. A profile changing only an
   external version leaves its identity counted while its age fact is unavailable.

Per-field provenance distinguishes dependency, inherited dependency, property,
consumer-local management, inherited management and supported default. Examples
required by AC04/05/07/08 include partial overrides, inherited explicit version versus
child management, inherited property expressions affected by child properties,
competing management, unresolved imports and a profile changing internal/external
classification. Existing Maven model-building and dependency documentation determine
these technical constraints; they are not new human product gates.

Arbitrary plugin/extension effects and machine contributions are not evaluated.
The basis is a disclosed static repository projection, not effective completeness.

## S4 — Declared age facts

For each countable occurrence preserve the raw safe request and attribution chain:
written POM, local property/management origin where used, type/classifier, scope,
optional and model limitations. A supported bare exact version text or hard singleton
[x] can supply a declared candidate version. Singleton unwrapping preserves the
original request and never claims observed selection. Unsupported ranges, LATEST /
RELEASE aliases and SNAPSHOT do not become exact release ages. Missing/unsupported
version facts leave the known occurrence count intact.

Initially accept only finite ASCII version strings with safe coordinate encoding;
no inferred range endpoint, dynamic selector, timestamped SNAPSHOT or host-property
fallback. The ordering contract in S7 is Maven-specific; the eligibility decision in
[latest-policy.md](latest-policy.md#selected-policy--run007-0008) is human-selected. Maven ordering is not NuGet SemVer2. No unknown actual latest may be silently
replaced by an older dated candidate. Used-version and latest-version dates need
identity-bound conventional time evidence under S7 for each view. Successful date acquisition is
not public namespace permission.

## S5 — Observed evidence and availability

**No Maven observed-artifact reader or new observation CLI option is selected for
initial Feature007.** DPC supplied none and libyears must not manufacture one.
For detected Maven sources report: Observed unavailable: this release has no
accepted Maven retained-selection reader. This is a capability limitation, not a
claim that every possible artifact was searched or absent. It is not measured0/N.
Do not copy declared N, versions, coverage or statistics into that view.

Potential later evidence includes a retained direct-resolution graph/export with
module, dependency type/classifier, applicable context, direct-edge classification,
exact versions and accountable source/input association. An effective POM describes
an expanded request model, not necessarily selected versions. A plain dependency
text/tree without bound context/directness/completeness is insufficient; a vendored
JAR or POM proves no complete selection population; a generic SBOM needs independent
scope/association evidence. These are research candidates, not accepted formats.
Accepting a new reader or supplier-assertion route requires separately approved
scope and review. AB2D Gradle locks inform context and non-equality rules only.

An absent observed reader does not prevent a useful initial declared report. The
logical model must retain observed-only capability without exposing a fake intake.
A later observed population may differ from declared; the denominator for that
view must derive independently from its accepted evidence, not the union/intersection.

## S6 — Independent summaries and human output

### View admission and row failures

Admission concerns the repository version-evidence **collection**, not whether any
row has a usable version, comparator or date. Initial Declared collection is
accepted when bounded safe model extraction establishes at least one countable
external occurrence identity, or certifies complete empty population. Its completeness
may remain unknown while safe occurrence records survive. Every such known occurrence
gets a declared record, even with null request/version/age and a fixed failure reason.

Missing/unsupported versions (including all versions depending on unread BOMs),
system assignment, source-policy refusal/uncertainty (including every occurrence
refusing before HTTP), catalogue/eligibility/date failures and worker unavailability
are **row failures after collection acceptance**. They keep known N; M counts actual
measured rows, including0. With complete known N>0 and no whole-collection-unavailable
sibling, coverage is M/N even when0; no measurements gives total0.0 and null
mean/median/maximum. Zero with coverage0 means no age measured, never fresh dependencies.

A whole view collection is unavailable when no accepted version-evidence collection
exists: initially Observed has no accepted reader; an unreadable/unsafe primary model
or unsupported population with no safe occurrence records supplies no Declared
collection. Its M/coverage/numerics are null; N survives only if independently known
for that same view. Unknown population **with** safe rows permits partial collection
acceptance; unknown population with no safe rows is not accepted emptiness. Missing
external inheritance does not by itself erase an accepted local collection.

Availability is `unavailable` without an accepted collection, `partial` for an
accepted collection with unknown population or any row failure, otherwise `available`
(including certified empty). Repository availability is partial if accepted sources
coexist with unknown discovery, partial or unavailable sources; it is unavailable
when none has an accepted collection. S6 numeric composition below remains independent
of that label. Complete discovery with no Maven sources omits the Maven section.

For example, a safely extracted N=2 source whose two versions require an unread BOM
has M=0/coverage0/total0.0. A supported N=2 source with both comparisons refused by
Central policy has the same numeric state, with different row reasons and zero HTTP.
Adding an admitted N=1/M=1 sibling yields N=3/M=1/coverage1/3 in either case.
By contrast, an independently known N=2 **whole-collection-unavailable** source plus
that sibling yields N=3/M=1/coverage null under the composition table. Initial Observed
remains all-null because neither its population nor its collection is established.


The paired summaries in this section are **Maven-only**. Existing siblings retain
their existing single-view contracts. For each Maven view and source, preserve population state (known/unknown), evidence
availability and per-row fact/age availability separately. A known row may survive
an unknown complete source population. Safe measured rows may contribute a clearly
partial total, but unknown N means null coverage; partial numbers are never a
complete repository answer. One source's failure must not erase a successful sibling.

| State | Counts / coverage / statistics |
| --- | --- |
| Known nonempty population, accepted collection, some/all row failures | Known N; actual M including0; M/N coverage; statistics over measured subset only |
| Complete population unknown, safe rows survive | N/coverage null; actual established measured subset count and partial statistics may survive; disclose incompleteness |
| Known population, whole view collection unavailable | N only if independently established for that same view; M, coverage and numerics null |
| No accepted observed population/evidence (initial Maven) | Observed N/M/coverage/numerics null, explicit unavailable reason, no fabricated rows |
| Accepted empty view | N=M=0, coverage null, total0.0, other statistics null; requires evidence of emptiness |

A zero measured subset has total0.0 only after collection acceptance and per-row
measurement admission/refusal was evaluated; an HTTP attempt is not required. Whole
collection unavailability never becomes a zero total.
Compose each Maven view across sources with these rules. N is summed only when
every source population is known; otherwise N is null. M counts the established
measured subset only: it is null if no source has an accepted collection,
otherwise the number of safe measured occurrences, explicitly partial if any source
is unavailable or has unknown population. Coverage is null if any population is
unknown or any whole-source collection is unavailable; otherwise M/N for N>0.

| Source combination within one view | Repository result |
| --- | --- |
| All complete/admitted; some row failures | Sum N and actual M; M/N; union of measured rows for statistics |
| One admitted sibling plus known-N whole-unavailable sibling | Sum known N; actual admitted measured-subset M; coverage null; retain partial statistics |
| One admitted sibling plus unknown-population sibling | N/coverage null; safe measured-subset M/statistics survive, marked partial |
| Every source whole-unavailable | M/coverage/numerics null; N only if independently known for that view |
| Accepted emptiness plus an admitted source | Empty source adds0 to N/M; other source controls rows; ordinary M/N if N>0 |
| Every source accepted empty | N=M=0, coverage null, total0.0; other statistics null |
| Some admitted sources but zero measured rows | M=0 and total0.0 for attempted subset; coverage0 only when all N/evidence known and N>0; otherwise null |

For example, an admitted N=2/M=1 source plus N=4 whole-unavailable source yields
N=6, measured-subset M=1, **null coverage**, and that one occurrence's partial
statistics; never1/6 coverage. Mean/median/maximum operate over the union of measured
occurrences, never averages of source means/medians. No view or sibling total is
substituted into these Maven summaries. No single unqualified Java total is emitted.

Normal output identifies Maven sources and the static declared basis, then compares
Declared / Observed measured counts, coverage, total, mean, median and maximum.
Use unavailable/unknown wording instead of misleading0/N; include a concise reason
for missing observed authority, plus concise declared limitations (unresolved
management versus source/comparator refusal). Explain that a shared inherited
request can count for several modules, not several distinct upgrade actions. Detailed
per-occurrence facts, origin/context and limitations belong in verbose/JSON; verbose
must not expose raw XML, absolute local paths, credentials or source URLs. The human's sample
numbers/format are illustrative only; no literal table/arithmetic is approved.

## S7 — Maven comparator evidence cascade and conventional time basis

### Claims and accepted authority

The human007-0003 decision resolves H1=**NO**. Unassigned alternate/file repository
eligibility alone is not a veto. Strongest accepted evidence and lowest sufficient
truthful authority are distinct. The comparison assumes correspondence to the public
Central version catalogue and conventional time basis; it proves neither acquisition, bytes, producer event, resolution,
installed/deployed/runtime use nor complete evaluated Maven state. Version facts
(Declared/Observed) remain independent of comparator and date authority.

Before any public request, accept only a supported occurrence/version fact inside
the explicitly authorized disclosure boundary. Preserve accepted contrary evidence;
no failed high tier may be silently ignored in favor of a weaker number-producing
route. A lookup/date failure is not a reason to change authority or identity.

Initial cascade:

1. **Occurrence-specific accepted facts first.** Apply any stronger accepted identity /
   comparator assertion for the same occurrence/version/context; a conflict refuses.
   Acquisition-only origin evidence is not an assertion that Central comparison is
   wrong. No new Maven supplier testimony, cache-origin reader or retained-selection
   intake is created by this tier. Initial Feature007 has none of those readers;
   do not synthesize them from file presence or hashes.
2. **Applicable repository-contained Maven policy and contrary identity evidence.**
   Supported facts may establish explicit Central exclusion, system/local assignment,
   identity substitution or relevant policy uncertainty. Refuse the affected comparison
   when that narrower claim cannot safely use Central. Do not invent NuGet-style
   packageSourceMapping: ordinary Maven repository lists establish ordered eligibility,
   not package-specific origin or ownership. Positive assignment must be attributable
   to the occurrence/context, never guessed from names or organizational prefixes.
3. **Bounded conventional Central comparison.** If stronger accepted facts provide no
   contradictory assignment/exclusion and no relevant unsafe/unknown semantics,
   use the conventional Central comparator. Additional repositories, file/local eligibility,
   missing acquisition proof and absent content/event assurance alone do not veto it.
   Record comparator_basis=conventional_central and fixed limitations: correspondence
   assumed; acquisition/content/producer/evaluated/runtime facts not established;
   uninspected machine settings may affect acquisition. No Central namesake hit
   retroactively authorizes disclosure or comparison.
4. **Independent time and latest gates.** After comparator admission, establish the
   complete accepted current GA catalogue, unique greatest eligible exact version
   and the exact versioned public POM representation dates below. Comparator
   permission does not establish a date, stable eligibility, acquisition or identity
   correspondence. Missing evidence ends the affected age attempt.

Use/refuse the strongest *accepted claim-specific* evidence; an unaccepted file is
not testimony. Valid stronger assurance may enrich a future accepted result but is
not a prerequisite for this narrower convention. The actual initial positive route
is the convention after supported contrary checks, not fictional stronger readers.

### Maven-native distinctions and refusal scope

| Evidence | Comparator consequence |
| --- | --- |
| Mere additional/file/local repository, including a parameterized additional URL | Eligibility only; no automatic veto, URL evaluation or alternate endpoint access |
| Attributable positive private/fork/substitution or conflicting comparator identity | Refuse affected occurrence; preserve supported request/population facts |
| system dependency | Occurrence-specific local assignment; refuse Central age, never read systemPath |
| Explicit applicable public Central release exclusion/block/redefinition | Refuse affected comparisons; a repository ID alone never proves its URL is public Central |
| Mirror routing to another server | Acquisition route alone does not prove a fork; blocked applicable Central mirror is different. !central excludes that mirror match, not Central itself |
| Known applicable identity relocation | Do not silently rewrite or merge histories; unsupported relocation refuses the affected comparison |
| Applicable Central group/prefix filter with unknown semantics/version/input | Refuse affected comparison until safely interpreted; do not read machine caches or execute Resolver to repair it |
| Allowlist on an alternate repository | Does not imply Central excludes those coordinates |
| Raw local artifact presence, checksum or suggestive fork name | Neither acquisition nor private namespace assignment by itself; no inferred positive testimony |
| Plugin repository, SCM/project URL or ordinary publishing repository | Not a project-dependency comparator assignment; artifact-POM relocation is a separate identity mechanism |

Repository order, same-ID settings precedence and mirrors affect acquisition; none
alone proves bytes or public-history correspondence. Native Resolver filtering is
version-sensitive; its prefix/groupId mechanisms must not be replaced with a made-up
Maven mapping grammar or interpreted using another Resolver version's defaults.

The exact supported local inputs, repository-ID precedence, Central recognition,
profile/settings/mirror/filter refusal rules and parser/complexity budgets are in
[source-policy.md](source-policy.md). Its supported selection is deliberately narrow;
co-location is not settings authority. No host/global/user configuration is inspected.
Unknown policy that can exclude/change Central refuses at the smallest safe scope;
unassigned alternate eligibility remains non-vetoing. No effective-model/resolver
execution or target-directed endpoint follows.

Recognizable local contrary facts must refuse **before** any public request. If later
admitted public metadata supplies a conflicting identity/relocation, stop the affected
age rather than retry a different identity or weaker policy. No arbitrary target URL,
private endpoint, authentication, artifact archive or parent/BOM fetch is permitted.

### Selected time fact and terminal behavior

The human007-0007 decision adopts **Conventional Maven age**. Its exact evidence
claim is **the public repository's reported modification time for the versioned
POM representation**, used as an **explicitly conventional Maven release-age
surrogate**. Independent version facts and comparator admission remain prerequisites.
This is not upstream release, first Central publication/receipt/upload, first public
availability, artifact-byte or classifier publication, acquisition/content
correspondence, producer/resolver history, deployment or runtime use.

The publication-only T1 investigation remains negative. Provider alternatives did
not repair publication authority; ecosyste.ms row creation remains rejected.
007-0006 established moderate tooling convention (Renovate direct use; Dependabot
fallback), not event authority. The later human choice changes the supported claim,
not the historical findings. See [practice](ecosystem-practice.md).

For each independently supported measured and target exact version, use only the
HTTP Last-Modified of its successful versioned public POM representation at the
fixed Central repository. Require safe exact GAV/path binding, successful response
for that representation, and exactly one valid supported HTTP date normalized to UTC under
[metadata-contract.md](metadata-contract.md).
Malformed/duplicate-conflicting dates, error representations, missing POM/header,
unsafe redirection, identity/relocation conflict, exhausted budgets and HTTP failure
leave that age unavailable. Validate calendar/timezone and reject a future value
relative to retrieval; do not use a response Date as replacement evidence. The fixed
transport limits and refusal/conformance surface are defined in that companion.

The cascade terminates: no Central Search timestamp, metadata lastUpdated, index
mtime, provider published_at/created_at/publishedAt, Libraries.io, Socket, Sonatype
catalogDate, webhook, arbitrary observation, filesystem or Git date fallback.
No older dated target may replace the greatest eligible version. Select the target
before inspecting dates. Different exact versions need both dates. Exact same-version
zero is 0.0 only after the same date admission succeeds; absent time evidence does
not become a measured zero. Existing365.25-day arithmetic and flagged negative-date
clamping remain unchanged. Ordering-equivalent different strings are not exact equality.

Date failure is occurrence/view-local when its version facts/population were safely
established: keep known N, report the row reason, exclude it from numerics. A shared
failed catalogue/target date affects all dependent rows; an attempted admitted source
with all rows failing has M=0 under S6, not a fabricated successful age. Whole-source
version-evidence unavailability and unknown population retain their separate S6
null semantics. Initial Observed remains unavailable for lack of an accepted reader.

### Current catalogue and technical ordering

Use the complete bounded `versioning/versions/version` list of Central GA
`maven-metadata.xml`, at an approved fixed public destination, with matching exact
case-sensitive group/artifact. It is the repository's current available-version
catalogue, not all-ever history, atomic world state or classifier availability.
Require successful whole-document retrieval/parsing and identity/shape validation;
truncation, unsafe strings, unsupported range/selector entries, over-budget input,
conflicts or an absent/empty usable list cannot establish a greatest candidate.
Collapse only byte-identical duplicate strings. Do not substitute Search/index,
provider, directory enumeration, `<latest>` or `<release>`; the last two are
last-added fields. Disappearance/correction can change a later measurement.
Retain retrieval time as freshness evidence, never as a version date.

Use **Apache Maven maven-artifact ComparableVersion3.9.11** precedence, reproduced
faithfully with pinned upstream tests as later conformance obligations. This names
a conventional Maven artifact ordering, not an evaluated Maven/Resolver result.
GenericVersionScheme is a distinct range-resolution mechanism; no silent interchange,
SemVer, lexical sort or host Maven invocation is permitted. Case-insensitive ordering
and aliases do not normalize exact repository version identities.

[Selected latest policy](latest-policy.md#selected-policy--run007-0008) specifies the
conservative eligibility rule and repository-wide maximum. Unknown strictly below
the greatest known-eligible version does not affect it; unknown at/above it or an
unorderable relevant value makes latest unavailable. Eligibility is separate from
ordering. Under the selected rule, multiple distinct strings at an eligible maximum mean
`ambiguous_latest_version`: no lexical/date/list-order tie-break, even if dates agree.
A successful exact maximum must not be replaced after a date failure. No candidate
is selected by its modification timestamp. GA catalogue plus exact GAV POM dates is
sufficient for this narrow conventional claim, including supported type/classifier
occurrences; neither target nor measured variant availability/history/compatibility
is certified. Original model/artifact keys and handler refusals remain unchanged.

### Human, verbose and machine disclosure

Ordinary Maven output uses **Conventional Maven dependency age**, with Declared /
Observed columns and one section-level line: **Time basis: Maven conventional
(versioned public POM Last-Modified)**. Keep independent S6 summaries/reasons and
label existing-ecosystem partial summaries separately. No repeated paragraph per row
is needed; no single unqualified cross-ecosystem dependency-age total is introduced.

Verbose output expands once: public repository-reported modification time of each
versioned POM representation is used as a conventional release-age surrogate; first
publication, upstream release and classifier availability are not established.
Per row show exact versions, UTC representation-modification dates, independent
version basis, comparator basis, eligibility policy identifier and limitations.
Never expose source URLs, raw headers/XML, credentials or absolute paths.

In S8's Maven-only subtree, keep `version_basis`, `comparator_basis` and `time_basis`
separate. Each age result carries `time_basis=maven_conventional_pom_last_modified`,
`measured_version_pom_last_modified` and `comparison_version_pom_last_modified`
(UTC timestamps), plus fixed limitations `publication_history_not_established` and
`variant_availability_not_established`. Source/view evidence also discloses the
basis when no row measures; unavailable dates remain null with stable reasons.
Do not name these fields release_date, published_at or first_available_at. Include
`ordering_basis=maven_comparable_version_3_9_11`, current catalogue retrieval time,
and `eligibility_policy=maven_conservative_stable_v1`. No generic cross-ecosystem basis matrix
or sibling field reinterpretation is authorized.

At the later approved documentation checkpoint, ECOSYSTEMS.md must explain:
“Maven compares independently evidenced Declared and Observed versions using the
public repository's versioned POM Last-Modified values as a conventional release-age
surrogate. These dates do not establish first publication or upstream release.
The GA comparison does not establish classifier availability or compatibility.”
The guide must distinguish this basis from siblings' stronger date authority and
explain static module occurrence weighting and unavailable Observed. This is future
documentation wording, not a claim that Maven support ships today.

### Disclosure and unchanged plural model

Human authority covers supported public coordinates only during the authorized
PUBLIC proving-ground lifecycle. The007-0003 assignment permits bounded T1 public
research, not live DPC measurement. Private access/networked validation requires a
separate disclosure decision for coordinates, source URLs, names/paths, diagnostics,
artifacts, reviewer context, observations and sanitization. Do not identify that target.

An eventual adapter must use explicitly approved fixed public metadata destinations,
verified TLS, safe encoding and finite budgets, with no target-directed host/redirect /
private endpoint/archive fetch. Errors remain sanitized; no raw XML, settings,
credentials, absolute roots or source URL diagnostics. Only accepted safe facts and
basis/limitations enter the already selected Maven views. Dates cannot manufacture
Observed evidence from a declaration, and no view total may enter the other.

## S8 — Additive machine output, schema3

H2's initial incompatibility concern has a compatible representation: retain schema3
and add **maven** as an independent plural-result section. No new schema version or
existing-field reinterpretation is selected. Complete discovery with no Maven candidates leaves non-Maven output unchanged.
Incomplete discovery reports unknown Maven presence through discovery failure;
it does not certify absence or an empty population.
This is a specification contract; independent whole-specification disposition
is in reviews.md. It is not runtime code.

For Maven-active reports:

- Add maven to detected `ecosystems` and add `version_evidence.maven` describing
  plural mode and supported local base-model scope. Do not invent a singleton POM
  or resolution file for a multi-source repository.
- Add top-level `maven` containing `discovery`, `sources`, `occurrences` and `views`.
  Discovery states complete/unavailable with a sanitized reason; incomplete discovery
  forces repository Maven N/coverage null even when safe source results survive.
  A discovery-level legacy error has source_id null, never a fabricated source path.
  With no safely accepted sources, Maven M/numerics are null, not an empty summary.
  Sources are sorted by root-relative `source_id`. Each source records safe context, basis,
  limitations and independent `views.declared` / `views.observed`. Top-level Maven
  views summarize those sources under S6; they never summarize siblings.
- Each occurrence contains a structured occurrence key (source_id, context_id,
  group_id, artifact_id, type, classifier), supported artifact key and independently
  nullable declared/observed records. A present record has independently nullable
  safe request and exact version fields, `version_basis`, evidence origin/context,
  availability/reason, limitations and an independently nullable age result. Known
  occurrence identity with no supported request/version keeps a present declared
  record with both fields null and a fixed failure reason, as required by S6;
  record presence alone never asserts an available version fact. A present age records comparison_version,
  libyears and timestamp_order_anomaly plus the exact S7 time evidence/bases.
  A null counterpart is explained by source/view
  availability, never copied. Unknown population is a source/view state, not a row.
- View records carry population_state (known/unknown), availability (available/partial/
  unavailable), fixed limitations/reason and summary with the existing seven statistic
  field names. Null fields follow S6. Evidence-to-context/input bindings are required
  internally for any future accepted observed join; no raw hashes/URLs/absolute paths
  need be exposed. There is no initial observed-intake option or source format.
- Maven has **no available legacy scalar projection**. Emit stable source reason
  `maven_plural_projection_unavailable` for each detected Maven source (or a discovery-
  level source failure), accurately identifying representation unavailability, not
  a parsing/registry failure. Do not put Maven rows into legacy `dependencies` or
  `unmeasurable`, or either Maven view into legacy scalar statistics. Actual Maven
  failures and per-view rows are preserved within the Maven section.
- Set Maven's legacy by_ecosystem summary and legacy contribution's N/M/coverage/
  numerics null. Legacy repository N and coverage become null whenever Maven is
  detected: no single accepted Maven denominator exists for this scalar projection.
  Existing successful sibling rows, evidence, per-ecosystem summaries and measured-
  subset aggregates remain intact under current unavailable-source rules. If every
  detected legacy source is unavailable (Maven-only included), its M and numerics
  are null; an admitted empty sibling may retain M=0/total0.0 as a clearly partial
  **legacy subset**, never as Java or complete repository age.

The legacy repository summary remains an explicitly incomplete single-view answer,
not silently scoped to non-Java with known coverage. Old consumers honoring source
errors/null coverage see unavailability; those reading only a number can misread a
partial total, as with existing failed sources. New consumers read Maven's two views.
Closed-world consumers rejecting new keys/ecosystems/reasons may reject additive
changes; no false universal compatibility claim follows. Human normal output renders
the paired Maven section plus separately labeled existing-ecosystem subset; it does
not lead with an unqualified legacy0/0 when Maven is present.

Required compatibility witnesses cover Maven-only, successful siblings for each of
four existing ecosystems, empty siblings, unknown Maven population and prospective
paired differing versions. No Java value may enter legacy scalar rows/statistics;
no sibling is relabeled declared/observed. If later implementation needs actual
incompatible behavior, stop for human schema authority instead of weakening this
contract. Current runtime remains unchanged.

## S9 — Acceptance obligations and proving-ground contract

These obligations govern the complete specification and its normative companions.
Specification approval does not claim executed acceptance; these are future
witnesses, not passed implementation tests or a task graph.

| ID | Required witness |
| --- | --- |
| AC01 | Declared-only, observed-only, paired differing versions and unknown-population model cases remain distinguishable; initial Maven observed remains unavailable |
| AC02 | Pairing requires source/context/direct-identity association; coordinate-only, context mismatch and ambiguous selections never join |
| AC03 | Both Maven views retain independent populations and seven summary fields; test every S6 source-composition row, all-missing BOM versions, all-policy-refused rows and their successful sibling compositions; partial M versus null coverage; no cross-view arithmetic |
| AC04 | Partial dependency-field inheritance and delayed defaults preserve origins; absent optional defaults false despite management optional=true; repeated modules persist; co-location/parent edges alone do not establish one reactor |
| AC05 | Management/import-only adds no population; optional is not managed; field-local versus inherited management (including scope-only child plus unknown import), direct versions and unresolved imports follow S3 without fallback |
| AC06 | Scope/optional/tooling/POM inclusion, handler alias pairs, exact model-key nonmatching, empty classifier refusal and version/scope-only duplicate collisions follow S2/S3; no systemPath/custom-handler execution |
| AC07 | Field provenance, consumer property context and partial merges obey S3; reserved project.version cannot be shadowed; inherited project.directory requests refuse; missing/cyclic/ranged/SNAPSHOT facts fail locally |
| AC08 | Missing parent, ambiguous aggregation, unknown identity and ancestor profile changes to internal/external attribution preserve safe rows but never fabricate external N or age facts |
| AC09 | No Maven observed result is inferred from a declaration, effective POM, archive or unbound tree/SBOM |
| AC10 | Positive private/conflicting source refuses before any public request; the cascade distinguishes alternate eligibility from attributable contrary evidence before HTTP |
| AC11 | Exact conventional claim/disclosure, terminal missing-date rules, current GA catalogue, pinned Maven precedence, selected eligibility and ambiguous-max refusal have witnesses; arithmetic unchanged |
| AC12 | Human paired layout distinguishes source-composed unknown/unavailable/zero, partial M/statistics and null coverage, with reasons for both views; no raw sensitive diagnostics |
| AC13 | S8 additive3 legacy-projection unavailability passes Maven-only, four successful/empty sibling and unknown-population witnesses; neither Java view enters scalar legacy results; non-Java output unchanged |
| AC14 | DPC ordinary root journey discovers supported modules, reports attributable declared facts/limitations and observed unavailable honestly, without promising198/N or positive measured yield |
| AC15 | AB2D challenges missing external parent, typed dependencies, alternate policy and Gradle request/lock divergence without Gradle ingestion |
| AC16 | Read-only public target integrity, no package-manager/code/private access, disclosure controls, bounded inputs/network and offline deterministic verification remain required |
| AC17 | Exact source-policy grammar covers child-ID precedence, Central identity/release exclusion, alternate eligibility, relevant profiles, selected settings/mirrors/filter uncertainty and local configuration refusal before HTTP |
| AC18 | Discovery/XML/model/expansion/coordinate/version/HTTP budgets reject overages without claiming complete population or losing admitted sibling results |
| AC19 | Supervisor enforces blocked-DNS/body deadlines, isolated trusted imports, closed capabilities/protocol, no redirects/proxy/auth/alternate URLs, no synchronous fallback, and capability refusal across platforms |
| AC20 | Unknown-below does not poison a unique maximum; unknown-equal/above or relevant inability to compare refuses; aliases/service packs/prereleases/timestamped snapshots and exact-string ties follow the selected pinned policy |

The DPC journey is `python3 -m libyears PATH` and its JSON form, without special
flags to discover Java or fake an observed column. The eventual DPC usefulness witness must show an attributable request and an
understandable declared limitation, without demanding positive live measured yield.
Verify declared reporting is useful even with unmeasurable managed versions and
local-source exclusions. Capture
revision/status and explain source limitations before any separately authorized
live measurement. No performance, yield or complete effective-model claim follows
from this specification. Useful ordinary journey and contract convergence remain
separate required later witnesses.

## S10 — Next gate

H1, conventional time basis and conservative eligibility are human-selected; do not
reopen them. Complete fresh whole-specification review across S1–S10 and all three
normative companions, reconcile every material finding and obtain fresh focused
verification for corrections. Publication-only authority is not a prerequisite for
the selected conventional claim. Record approval separately in reviews.md without
editing a frozen candidate merely to announce approval.

Only an independently approved whole specification advances to the already
authorized plan/review stage; only an approved plan advances to sequential tasks /
review. Stop before runtime implementation even after reviewed tasks. Unknown new
product/security/schema decisions require human authority. Existing ecosystem
semantics, target repositories, private-target boundary and publication stay unchanged.
