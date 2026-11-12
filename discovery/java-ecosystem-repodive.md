# Public Java ecosystem repodive

Run **007-0001**, 2026-11-12. **Discovery only; opportunity11 remains EXPLORE.**
Feature007 has not been selected, specified, planned or implemented. This record
recommends a product question; its alternatives require human selection.
[Independent review and verification](java-ecosystem-repodive-review.md) accompanies it.

## Boundary, authority and method

Starting libyears HEAD: `1cd937f2942550c7140e379931d0853a16f7ea1d`, clean.
The human reports both remote mains at that published revision, hosted GitLeaks
and Tier2 PASS, checkout v7/setup-node v7 execution, and exact-candidate macOS
worker3 PASS, deterministic783 PASS/one expected platform skip/49.999s and
whitespace PASS. This is human testimony, not a new log retrieval or full matrix
claim. The [housekeeping follow-up](../maintenance/post-006-housekeeping.md#published-boundary-follow-up--java-discovery-run-007-0001)
supersedes its historical pending state. Ubuntu26 migration is upstream WATCH.
No housekeeping sweep or new CI maintenance was performed.

External authority covers only the explicitly supplied public candidate collection,
called **candidate root** below; absolute checkout topology is deliberately omitted
from durable prose. Exactly seven immediate directories were candidates; nested
Git repositories were not promoted into portfolio candidates. Each tracked inventory
was bounded to fewer than10,000 paths (largest4,466). Inspection selected ordinary
build/dependency metadata and relevant README sections, without reading application
source. Metadata reads were regular files at most1MiB;126 metadata files have retained
local digests captured during inspection for the final integrity check. Git revision/status and tracked-path
inventories are retained outside Git. Ignored/generated local files were not
searched: absence claims below mean **not identified in the tracked inventory**.
This is not a statistical sample of Java, CMSgov, deployments or independent users.

Only Git read operations and static Python/text inspection were used on candidates.
No wrapper, Maven, Gradle, Ant, Java, repository script, resolver, build or test was
executed. No candidate file was generated/modified, no user/machine configuration,
cache, credential store or private repository was accessed. Documentation-only
requests to official Maven/Gradle sites checked semantics; no target coordinate,
source URL or file contents were sent in those requests. No package repository
was contacted, including Maven Central, alternate registries or the Plugin Portal.

The ledger contains52 unique rows/44 columns, ending006-0034. The specifically
expected006-0035 temporary baton is missing; do not reconstruct it from the
housekeeping narrative. No preceding row was appended, no runtime/account boundary
inferred, no credit delta stored. Current007-0001 receives an external44-key handoff
and is not appended by this run. The007 prefix identifies pre-selection discovery,
not authorization of Feature007 support.

## Portfolio and revision inventory

All seven initial porcelain statuses were empty (clean, no untracked entries).
Final revision/status and metadata integrity are recorded in the review companion.
Public revision identifiers make the evidence relocatable without local paths.

| Repository | Inspected revision |
| --- | --- |
| ab2d | [`9c785d41da3f7dd72f5be62cfc42ee7b1bf74459`](https://github.com/CMSgov/ab2d/tree/9c785d41da3f7dd72f5be62cfc42ee7b1bf74459) |
| beneficiary-fhir-data | [`58683caaccd1f311a9db124f2832f4f7a17e07a1`](https://github.com/CMSgov/beneficiary-fhir-data/tree/58683caaccd1f311a9db124f2832f4f7a17e07a1) |
| cms-bb2-java-sdk | [`1d0fd40d1bf06392073172f270d4dd99063407b9`](https://github.com/CMSgov/cms-bb2-java-sdk/tree/1d0fd40d1bf06392073172f270d4dd99063407b9) |
| dpc-app | [`d1e413caff5a80f590682d9055962f8103a9a527`](https://github.com/CMSgov/dpc-app/tree/d1e413caff5a80f590682d9055962f8103a9a527) |
| nimbus-pub-code-scanning-1 | [`3353b6d99e07d82c5bada6aefb8cd622ba2e302b`](https://github.com/CMSgov/nimbus-pub-code-scanning-1/tree/3353b6d99e07d82c5bada6aefb8cd622ba2e302b) |
| nimbus-pub-github-action-poc | [`9d5e4468921cae999e66b79d9e3c23c3c18656e6`](https://github.com/CMSgov/nimbus-pub-github-action-poc/tree/9d5e4468921cae999e66b79d9e3c23c3c18656e6) |
| qpp-conversion-tool | [`8fc113e31ed82c5d3f45505d066d8491102fc543`](https://github.com/CMSgov/qpp-conversion-tool/tree/8fc113e31ed82c5d3f45505d066d8491102fc543) |

Distribution: **four Maven-only, two Gradle-only, one mixed**. No tracked Ant/Ivy,
Kotlin Gradle scripts or version catalogs identified. There are65 project
`pom.xml` files,22 `build.gradle` files, seven `settings.gradle` files and20
`gradle.lockfile` files. An additional vendored version-named `.pom` in DPC is
repository metadata, not a project POM or another application module.

| Repository | Structure / root artifacts | Written direct declarations | Retained selection | Source / static limitations | Candidate role |
| --- | --- | --- | --- | --- | --- |
| dpc-app | Maven root POM +9 children (10 POMs) |198 dependency elements; local properties/management,8 BOM imports | No committed resolution snapshot identified; vendored repository is narrower evidence | Local parent, profiles, build-cache extension, two child file repositories; external BOMs incomplete locally | **Primary**: ordinary multi-module Maven question |
| ab2d | Mixed: root Maven +7 children; five Gradle settings roots,20 Gradle build files |109 Maven elements; Gradle literals/properties/shared and injected declarations, constraints/platforms |20 Gradle locks, configuration-specific; no Maven snapshot identified | External Boot parent,3 Maven BOM imports; Central/local/environment-derived Artifactory; arbitrary Groovy | **Adversarial #1**; locked Gradle alternative primary if selected-snapshot question wins |
| beneficiary-fhir-data | Maven at `apps/pom.xml`,35 POMs total;12 immediate root module entries and deeper aggregators |437 elements;143 management entries across POMs,8 imports | No committed resolution snapshot identified | Deep local inheritance, external BOMs, release/plugin profiles, build extensions; no explicit project repository in counted POMs | **Adversarial #2**: nested root/inheritance/scale |
| qpp-conversion-tool | Root Maven +7 listed children;3 other POMs outside root module list (11 total) |119 elements; profiles, properties,11 BOM imports | No committed resolution snapshot identified | Root and child management, independent auxiliary POMs; no explicit project repository in counted POMs | Secondary Maven boundary witness |
| cms-bb2-java-sdk | Single root POM, no parent/modules | One literal JUnit3.8.1, test scope | Declaration only | No explicit repository; Maven default Central is a convention, no acquisition proof | Simple Maven sanity target, **not representative primary** |
| nimbus-pub-code-scanning-1 | Single Gradle build/settings | Two literals: servlet implementation and JUnit testCompile | No lock identified | Explicit mavenCentral; Java plugin, obsolete testCompile; executable model not evaluated | Simple declaration fixture / no-lock refusal |
| nimbus-pub-github-action-poc | Single Gradle build/settings | Same two literal declarations | No lock identified | Same build text as other Nimbus; wrappers present | Corroborating copy-like example, not independent complexity |

Maven counts are **written immediate project/dependencies/dependency elements**,
including test/internal/optional entries and parent POM dependencies. They exclude
management, plugin dependencies, comments and profiles. No profile-local project
dependency elements were found. Counts are not effective/inherited populations,
unique coordinates, external-only counts or accepted metric denominators.

| Repository | POMs | Elements | Literal version text | Property text | Version absent | Management entries |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ab2d |8|109|30|43|36|13|
| beneficiary-fhir-data |35|437|2|162|273|143|
| cms-bb2-java-sdk |1|1|1|0|0|0|
| dpc-app |10|198|47|18|133|62|
| qpp-conversion-tool |11|119|22|39|58|77|
| Total |65|864|102|262|500|395|

Literal here only means nonempty version text without `${`; it does not certify
an exact stable selection. Management totals include imported BOM entries and do
not imply that those packages are used. Reproduce from Git tracked `pom.xml` files
at the revisions above using the Maven namespace and those exact XML paths; count
nonempty/non-property, property-bearing and absent versions separately. Never count
all descendant dependency elements indiscriminately.

## Maven evidence and its limits

DPC is representative because its root declares nine modules, has ordinary
properties and direct dependencies, and imports management from Jetty, Dropwizard,
Guicey and other BOMs. Its198 written elements include many absent versions and
internal module references. Child POMs inherit a local root parent; an omitted
relativePath has Maven's default parent lookup semantics, unlike AB2D's explicitly
empty root parent relativePath. DPC's root has six profiles (integration-tests,
unit-tests, ci, error-prone, release, debug). Their existence requires examining
what changes, rather than assuming every profile changes dependency membership.
The committed `.mvn/extensions.xml` enables build caching; its code is not evaluated.

AB2D's root parent is external Spring Boot4.1.1 with empty relativePath;
local child inheritance does not supply that missing parent. BFD's root at `apps/`
has no explicit parent and nests model, pipeline and server aggregators; ancestor
paths and `${project.version}` need contextual interpretation. QPP's root lists
seven children; acceptance-tests, generate-race-cpcplus and qrda3-update-measures
have separate POMs outside that list. Its child management and property-activated
profiles demonstrate that finding POMs and traversing one reactor are different
population policies.

A POM naturally retains **requests, management and build model**, not a standard
complete selected dependency lock. A local parent may contribute direct inherited
dependencies; dependencyManagement supplies defaults/constraints, and imported
BOMs supply management without becoming ordinary direct dependencies themselves.
An effective dependency after inheritance/management is still distinct from a
historically resolved selection. User properties, active profiles, external parents,
BOMs, extensions and settings can change effective facts; do not reconstruct them
from machine state. Dependencies nested under build/plugin blocks belong to a separate structural
population. Tooling artifacts can also be explicitly written under project
dependencies: DPC root pom.xml:503–520 declares JaCoCo (runtime classifier) and
pitest-maven in test scope. Their purpose cannot justify silently removing them
from a structurally defined direct population. These distinctions follow the official
[Maven dependency guide](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html).

A bare literal version is a soft requirement, whereas `[x]` is a hard singleton;
neither proves that a successful historical build occurred. SNAPSHOT requests do
not identify immutable timestamped content. Ranges cannot be resolved from today's
registry to manufacture past selection. Maven version ordering/qualifiers are not
SemVer2: copying NuGet ordering or a generic semver parser would be wrong.
See the [POM reference](https://maven.apache.org/pom.html).

A bounded static subset can truthfully expose written dependency identities,
scopes, literal requests, safely attributable local property/management facts and
module/parent relationships. It cannot claim complete effective population when
unsupported inheritance/profile/extension influences remain. A **declared-version
age** policy could compare supported literal requests, with clearly separate basis,
but requires explicit human approval and cannot be labeled resolved-version age.
The portfolio provides no established Maven selected-snapshot intake contract.
A future supplied effective-POM alone would still not be a resolved dependency graph;
a bound direct-resolution export would need separately defined completeness,
module/context association and supplier authority. No such export was generated.

DPC's `dpc-macaroons/pom.xml` and `dpc-testing/pom.xml` declare a repository-local
file repository. Tracked `repo/` contains a fork-coordinate JAR, POM, checksums and
Maven metadata. Only names/ordinary metadata were used, no archive was opened.
That narrow retained artifact evidence does not establish the repository's complete
selected population and must not be replaced by a public Central namesake.
BFD's README points to a hosted dependency/SBOM view: a link is not a committed
bound selection artifact, and the hosted view was not fetched.

## Gradle evidence and its limits

AB2D is five build/settings roots: contracts, events, idr-db-importer, lambdas and
libs. Lambdas includes eight subprojects, libs seven; the two other services and
importer are single settings roots. Its20 build files have20 corresponding project
locks. Five gradlew launchers are present; six wrapper property files include an
extra coverage-counts7.5 distribution setting, while the five main roots name9.2.0.
Both Nimbus repositories have wrappers; no Maven wrapper identified anywhere.
Wrappers are executable supply-chain inputs, not selection evidence.

AB2D uses `apply from` shared Groovy, allprojects/subprojects injection, Spring Boot
and dependency-management plugins, platforms/enforcedPlatform, constraints, forced
versions, annotationProcessor/compileOnly/runtimeOnly/test configurations and
project dependencies. Repository URLs and credentials are obtained from environment
or project/system properties. Reading these expressions did not read those values.
CycloneDX plugins configure generation; no committed BOM JSON/XML was identified.
No dynamic `+`/latest selector was identified in inspected declaration excerpts;
SNAPSHOT, computed properties and versionless managed declarations are present.
This is not a complete syntax certification of every Groovy expression.

`lockAllConfigurations()` enables locking; it does not prove every configuration
was resolved and recorded. Locks record `group:artifact:version=configuration,...`
and empty configurations.
They retain resolved graph versions, including transitives/platforms/tooling;
they do **not** mark directness, supply declaration requests or repository URLs,
or bind themselves cryptographically to current build logic. Per-configuration
association matters: contracts' lock contains different error-prone versions for
compile versus runtime; libs/ab2d-events-client locks commons-codec1.11 for checkstyle
and1.21.0 for classpaths. A single coordinate can have several legitimate selections.
A lock is not evidence that the current build still resolves identically.
The [Gradle locking guide](https://docs.gradle.org/current/userguide/dependency_locking.html)
describes both configuration association and validation during actual resolution.

A concrete declared/selected distinction: libs/ab2d-events-client declares
commons-codec1.9 while its classpath lock records1.21.0. Do not substitute the request
for that retained selection or label every lock entry direct. A static literal
intersection is useful candidate evidence, but unknown injected membership can
make its completeness unestablished. A default all-lock population would change
the metric to include transitive/tool dependencies and requires a separate product
choice. No such expansion is recommended here.

Version catalogs and Kotlin builds are not represented in this sample. Catalog
aliases would retain declared versions, not independently prove selection; platforms,
constraints and plugins may alter it. Gradle is executable Groovy/Kotlin: no regex
subset can promise complete effective dependencies for arbitrary scripts. A future
bounded recognizer must reject unsupported relevant logic, never evaluate it or
execute plugins. The two Nimbus examples contain two readable literals each, but
no locks; their apparent simplicity supplies declaration fixtures, not positive
selected-version fixtures. Their old testCompile syntax was not tested for build
compatibility. They should not determine the Java product boundary.

## Claim chain and public comparator authority

| Stage | Truthful observed evidence | Missing fact / future decision |
| --- | --- | --- |
| Population | Written Maven declarations and Gradle expressions; module/build identities | Written versus effective versus bound resolved direct scope; inherited duplicates, profiles/configurations and internal edges |
| Selected version | AB2D Gradle configuration locks; narrow DPC vendored artifacts | Directness/completeness/current association; no complete Maven selected snapshot identified |
| Public comparator | Nimbus explicit Central; Maven default convention; DPC local source and AB2D alternate/local/configured sources | Central comparison permission, contrary-evidence policy and coordinate disclosure, separately from acquisition |
| Publication dates | No registry metadata examined | Identity-bound authoritative date semantics, completeness, mutable snapshots/relocation/classifiers and stable comparator ordering require later research |
| Libyears | Existing arithmetic is reusable after prerequisites | No Java ages, coverage or successful ordinary scan claimed in discovery |

Maven's default Central does not prove effective settings: repository-local settings
can override IDs and machine mirrors/profiles remain deliberately uninspected.
AB2D's tracked settings.xml activates an Artifactory profile with literal
`central`/`snapshots` IDs, parameterized repository URLs and plugin repositories. Co-location alone does
not prove invocation used that settings file. It is nevertheless relevant contrary/
unknown policy evidence. No mirror definition was identified in inspected tracked
configuration; no claim is made about machine mirrors.

Gradle separates plugin repositories from project repositories, and repository order
influences resolution. AB2D has Central plus mavenLocal and environment-derived
Artifactory; importer/lambdas put local ahead of Central in relevant blocks.
Plugin Portal presence is not project dependency authority. See the official
[Gradle repository guide](https://docs.gradle.org/current/userguide/declaring_repositories_basics.html).
Publishing repositories and SCM/documentation URLs also must not be mistaken for
acquisition repositories. DPC's file repository is positive local-source evidence,
not evidence that every project dependency is private.

Two honest future models remain: explicitly accepted coordinate-specific Central
comparison, or a disclosed Central convention qualified by bounded repository
inspection and defined contrary-evidence refusals. Neither proves acquisition,
byte correspondence or history. Java's ordered repositories, machine mirrors,
local caches and BOM/parent origins mean the NuGet positive-contrary policy does
**not automatically transfer**. Whether unassigned alternate eligibility is a veto
is a human product/risk decision, informed by Java semantics. An HTTP hit cannot
authorize a namesake comparison retroactively. No lookup policy is selected here.

## Recommended ordinary journey and human product gate

**Primary: dpc-app.** It represents a real multi-module Maven application, with
ordinary local inheritance and external management plus a source exception. It
forces the ordinary question early instead of optimizing for a toy pass.
**Adversarial: ab2d**, with BFD as deeper Maven witness. **Sanity: cms-bb2-java-sdk**
for Maven declarations; Nimbus for simple Gradle declaration/no-lock behavior.
These are roles, not promises of measurable yield. If the human selects retained
Gradle selection as the initial product, AB2D becomes the primary target and its
source/directness blockers remain part of that choice.

For a future `python3 -m libyears /path/to/public-java-repo`, a DPC user should
reasonably see Java/Maven sources discovered at the root and its supported modules,
what can be measured and why other sources/rows cannot. Absence of resolution
must not appear as absence of Java dependencies. Do not require expert flags just
to learn that ordinary evidence is unavailable. This is desired behavior for
selection, not an approved contract or an actual command witness.

The following alternatives are consequential and remain open:

- **Population:** written explicit external declarations per module (transparent
  narrower scope), effective direct dependencies including inheritance (closer to
  build model but needs more authority/evidence), or supplied resolved direct scope.
  Recommend excluding management-only entries, dependencies nested in build/plugin
  blocks and reactor project edges unless explicitly selected otherwise. Separately
  decide whether tooling artifacts explicitly written under project dependencies
  count regardless of purpose; do not infer a semantic purpose filter from block
  exclusion. Decide test/provided/optional/system and Gradle configurations;
  do not silently copy npm production or NuGet all-reference scope.
- **Artifact identity:** decide supported type/classifier variants and ordinary
  `type=pom` project dependencies, separately from management imports. AB2D
  api/pom.xml:34 and:93 declares the same common GAV as ordinary and test-jar;
  common/pom.xml:122 declares an AWS dependency POM outside management. DPC's
  explicit runtime classifier is another witness. Maven management identity includes
  type/classifier, not just group/artifact; type may imply a classifier. Occurrence
  identity and any public-history grouping must be separately defined. No classifier
  collapsing, non-JAR exclusion or artifact-specific date policy is selected here.
- **Occurrence and aggregation:** recommend module-qualified occurrences so distinct
  versions/scope contexts survive; unique-coordinate deduplication answers a different
  question. Repeated consumers can increase cumulative age without increasing
  distinct upgrade work: choose declaration-maintenance priority, consumer exposure
  or selected-version freshness as the intended decision. Decide whether inherited
  occurrences count once per consumer and whether
  multiple configurations count independently or use one named classpath. Repository
  totals are meaningful only with disclosed weighting; source totals should survive
  incomplete siblings. Root aggregator dependencies cannot be counted both as written
  parent entries and as inherited consumer entries without an explicit policy.
- **Version basis:** declared-version age (possibly bounded local management), explicitly
  distinct from selection, versus selected-version age requiring retained bound direct
  evidence. The latter currently lacks a ready complete Maven fixture. Neither model
  may silently use the other as a fallback.
- **Coverage:** denominator follows the chosen population, not864 written elements.
  Known declarations with missing versions can remain known-unavailable; unknown
  effective population means unknown N/coverage. Individual failures can use M/N only
  after scope acceptance. Show measured-subset totals as partial; no fabricated0/0
  or0% when scope/evidence is unavailable. For example, DPC dpc-api/pom.xml:28–31
  writes a versionless dropwizard-core dependency: it remains countable under an
  accepted written population even when age is unavailable, whereas unestablished
  effective inheritance may leave N unknown. Exact null/status details await specification.
- **Identity/output:** retain root-relative build/module path plus coordinate and selected
  scope/context. Normal output should identify sources, basis, partiality and safe reasons;
  verbose/JSON should explain limitations and per-source evidence. Decide whether relative
  names themselves may be disclosed; never require raw absolute paths or settings dumps.
- **Comparator/disclosure:** choose explicit accepted Central comparison or a disclosed
  bounded convention; define local/alternate/unknown refusal, and public coordinate exposure.
  Stable-version ordering and authoritative publication timestamps remain specification
  prerequisites, not established by this offline portfolio.

**Recommended bounded direction:** Maven-first ordinary repository reporting of
explicit external declaration occurrences and supported declared-version age,
with DPC as primary and AB2D as the cross-tool counterexample. Label declaration
basis openly; retain unknown inherited/managed selections rather than pretending
to reconstruct Maven. This recommendation needs human acceptance precisely because
it differs from a resolved-selection claim. It would support declaration-maintenance
priorities, not demonstrate selected-version freshness; AB2D's commons-codec
request/lock difference makes that limitation concrete. Success must include a useful partial
DPC explanation, not just the one-dependency SDK producing a number.

**Exact human gate:** select Maven-first declared-version age or retained selected-
snapshot age (and corresponding primary target); approve population/scope (including explicit tooling and artifact type/classifier choices)
and module/configuration weighting; approve Central comparison and coordinate-disclosure
policy. Alternatively request more bounded public evidence. Only after these choices
may Feature007 specification be commissioned. No private-target path/access is needed.

## Privacy and later validation boundary

Public candidate authorization does not carry into the future private target.
That target remains unidentified and inaccessible. Before any later private validation,
Feature007 needs a reviewed outbound/durable-data contract and new explicit authority.

| Surface | Potential disclosure | Prospective boundary to settle before private validation |
| --- | --- | --- |
| Registry request | group/artifact, version, classifier/type or plugin/BOM/parent coordinates; timing/client network identity | Authorize comparator before request; minimize identity set, fixed public destinations, no target-derived redirects/alternate endpoints |
| Source inspection | repository URLs, file paths, credentials embedded in XML/Groovy or user-property expressions | Read only bounded necessary repository metadata; never expand environment values or discover machine configs/credentials; avoid echoing sensitive nodes |
| Normal/JSON/verbose output | module/project names, root-relative or absolute paths, package identities | Explicit field disclosure contract; root-relative paths are still potentially sensitive; concise safe failure reasons |
| Logs/errors | raw XML/build text, parser snippets, HTTP URLs/query strings, stack traces | Fixed sanitized diagnostics and bounded excerpts only if explicitly safe; verbose is not an exemption |
| Durable artifacts/review | public-coordinate lists, internal module topology, exact source URLs, local checkout names | Review/redact before persistence/publication; public evidence here uses public revision/path anchors, not private target policy |
| Parsing/evaluation | DTD/entity fetches, symlink escapes, oversized input, Groovy/Kotlin/plugin execution | Safe bounded regular-file/XML/text handling; refuse lexical/symlink path escapes, external entities/XInclude/schema retrieval; aggregate budgets and safe coordinate encoding; no wrappers/build tools or arbitrary code |

This run copied no credentials or resolved environment values. Repository source
expressions were inspected as text, not used as endpoints. Public build metadata
can still contain secrets; public hosting is not a general disclosure exemption.
Security review concerns the proposed model, not any private repository contents.

## Methodology and architecture observations

| Feature006 lesson | Java classification | Evidence / adaptation |
| --- | --- | --- |
| Ordinary smoke exposes product intent | TRANSFERS WITH ADAPTATION | Define DPC root journey now; no Java implementation exists to smoke and no execution is authorized |
| Contract convergence != useful journey | TRANSFERS DIRECTLY | SDK positive-only success would not answer DPC/AB2D; report partial/unknown explicitly |
| Separate claims before raising floors | TRANSFERS DIRECTLY | Written population, effective model, selection, Central comparator, content/history differ |
| Lowest sufficient truthful floor | TRANSFERS WITH ADAPTATION | Declaration age may be useful only if selected as a separate claim; locks lack directness |
| Stronger assurance need not be age minimum | TRANSFERS DIRECTLY | Acquisition/bytes/history remain independent, never inferred from a Central match |
| Human gates can become durable policy | TRANSFERS DIRECTLY | Scope, weighting and disclosure choices precede code, then belong in repository contracts |
| Positive contrary versus absence | NOT YET KNOWN | Java source-order/mirror/local semantics need a human choice; no automatic NuGet policy transfer |
| Independent review attacks trust boundaries | TRANSFERS DIRECTLY | Six decomposed scopes are assigned factual, semantic, authority, UX and methodology obligations |
| Hosted CI distinct from local convergence | TRANSFERS DIRECTLY | Exact1cd937f testimony reconciled without inventing matrix results or new maintenance |
| Artifacts carry durable policy | TRANSFERS DIRECTLY | Routing/workflow/observations supplied lifecycle without conversational history |
| NuGet Direct lock classification and policy grammar | DOES NOT TRANSFER | Gradle locks lack directness and are configuration-specific; Maven lacks the same retained artifact |

Routing, freeze/correction rules, prior-baton protocol and hard human boundaries
were reusable without new methodology design. New commissioning authority was
still necessary for the exact external public collection, prohibited execution/
network/private access and six specialized review questions. Repository-specific
assumptions surfaced immediately: Maven's inherited population, Gradle's injected
logic and per-configuration selections, and a missing prior temporary baton.

The prompt was long and repeated stable lifecycle/security/observation rules as
well as necessary new authority. Discovery did not require a new constitutional
framework or SKILL.md; exact prompt length/attention savings were not measured.
Review decomposition transfers as a technique, not as proof that six reviewers is
an optimal count. This is within libyears, not evidence of cross-project harness
generality. Opportunity10 remains EXPLORE; retain missing-baton robustness and
narrow delta prompts as future questions, not a generalized harness implementation.

For opportunity8, this investigation observed source enumeration, metadata reading,
population/selection association questions and comparator evidence. Bounded public
metadata and reporting are prospective Java lifecycle stages, not executed Java
measurement. These stages recur in existing ecosystems.
Potential interface pressure includes multiple source identities, known/unknown/
unavailable populations and staged evidence that survives later failure. Exceptions
are substantial: Maven inheritance and separate management; Gradle executable logic,
configurations/variants, platform/constraint versus actual dependencies, and lock
entries without directness. A generic list-of-packages analyzer would conceal those
semantics. Record this as evidence for studying a lifecycle seam, not designing
interfaces or a plugin framework. No architecture was changed.

Prior [Yarn discovery](../specs/003-yarn-lock-evidence/discovery.md) already cautioned
that Maven requirements are not selections; [Ruby discovery](../specs/004-rubygems-support/discovery.md)
showed that actual retained locks, rather than manifest prevalence or hosted SBOM
links, justified a direction. Their old portfolio counts are not reused as current
facts. Ruby lock DEPENDENCIES and NuGet Direct records provide directness that Gradle
locks do not. The [post006 retrospective](../specs/006-nuget-selected-evidence/methodology-retrospective.md)
and [handoff](../specs/006-nuget-selected-evidence/methodology-handoff.md) supply
methodology, not Java product authority.
