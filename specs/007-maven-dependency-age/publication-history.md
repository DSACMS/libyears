# Maven publication-history authority — T1 investigation

## Run007-0007 later product decision — historical finding preserved

The human accepts a different, explicitly conventional claim: the versioned public
POM representation's reported Last-Modified as a Maven release-age surrogate.
This does **not** establish the publication/availability history investigated here.
No timestamp/provider investigation is repeated or admitted retroactively. The
negative007-0003/0004 evidence below remains the historical publication boundary.
Current contract is [S7](spec.md#s7--maven-comparator-evidence-cascade-and-conventional-time-basis);
remaining latest eligibility alternatives are [separate](latest-policy.md).


Run007-0005 separately investigates [alternative providers and date claims](age-evidence-alternatives.md).
It does not change this publication-history disposition or admit a previously
rejected timestamp. The current narrow alternative concerns provider record
creation and requires human selection; no time-basis policy is adopted.

**Current disposition: run007-0004, [focused investigation](#run007-0004-focused-publication-history-investigation):
NOT ESTABLISHED — HUMAN PRODUCT DIRECTION REQUIRED.** The007-0003 record below
is preserved as the prior stopping point. No publication event or latest-selection
policy has been admitted.

Run **007-0003**, 2026-11-12. Read with the [specification](spec.md),
[human decision](discovery.md) and [review disposition](reviews.md).
**T1 is not established:** the inspected evidence does not supply a complete,
identity-bound public release-publication date contract suitable for the selected
version-age claim. This is not proof that no such evidence exists anywhere.
No publication timestamp, latest policy or Java age is approved by this record.

The human resolves H1=**NO**: unassigned alternate/file repository eligibility alone
is not a comparator veto. That resolves a policy choice, not the independent date
prerequisite. Do not repeat H1 or lower the date floor until a number appears.

## Bound and method

The parent examined primary Apache Maven/Indexer implementation and Sonatype
Central documentation, publisher-state/webhook definitions, search guidance and
one generic Central component page. Two independent researchers separately
examined source-policy semantics and version/identity/order/completeness. No public
candidate, private target, machine configuration, cache or credentials were read.
No target build, package tool, resolver, Java, archive or script was executed.

The generic page was `org.apache.maven:maven-core:3.9.11`, selected from official
Maven documentation rather than a target manifest. Its extracted page exposed
coordinate/POM data but no usable publication-event date. One bounded public Search
API request for that same coordinate returned a tool-access error and no usable
response; this is access evidence, not proof of missing Central data or bad semantics.
No target coordinates were queried and no DPC measurement occurred. Documentation
navigation failures were recovered with tagged official source where possible.
No authenticated publisher endpoint, upload/status request, webhook or alternate
repository was contacted. Search results outside primary sources were not used
as measurement authority.

## Date/event evidence

| Candidate | What authoritative evidence establishes | Why it does not close T1 |
| --- | --- | --- |
| GA metadata lastUpdated | Time the metadata was updated; UTC second-format text | It dates mutable metadata, not each release's publication |
| SNAPSHOT timestamp / updated | Deployment timestamp for a snapshot / snapshot information update | It is not immutable release history and cannot date ordinary stable versions |
| Apache Indexer lastModified | File modification time of a POM/artifact in the inspected implementation | No demonstrated mapping to Central first receipt/publication, or to the Search API timestamp |
| Central Search timestamp | API documents coordinate/version search, but inspected guide supplies no event definition for timestamp | Millisecond-looking values or familiar field names cannot establish the event |
| Portal PUBLISHED status | Deployment successfully uploaded to Central | State is documented, but the public version-history timestamp/lookup contract is absent from that example |
| Portal webhook timestamp | Notification time, with deployment/PURL/path association and publishing state | Notification is not the exact publication instant; PUBLISHED messages may be absent/duplicated; no complete public retrospective history is supplied |
| HTTP modification / directory dates | At most response/file metadata unless a stronger contract is shown | No supported publication-event meaning; never a silent fallback |
| Project/SCM/build time | Upstream/project events or producer choices | Not Central publication/receipt evidence |

The [versioned Maven metadata model](https://maven.apache.org/ref/3.9.11/maven-repository-metadata/repository-metadata.html#versioning)
explicitly separates metadata update, snapshot deployment and available-version
fields. Its second-level text formats do not imply publication accuracy. Schema
location or XML parsing success cannot add a missing release event.

[Apache Indexer7.1.6 source](https://raw.githubusercontent.com/apache/maven-indexer/maven-indexer-7.1.6/indexer-core/src/main/java/org/apache/maven/index/creator/MinimalArtifactInfoIndexCreator.java)
uses POM file modification at Java line170 and artifact file modification at235;
lines137–142 label its field last modified. File.lastModified is an epoch-millisecond
representation, not a guarantee of event precision. This establishes that field's
implementation semantics only. It does **not** prove Central's current Search API
uses the same code or derives its timestamp identically. Reindexing or storage-copy
hypotheses are not asserted as observed causes.

[Central's Search API guide](https://central.sonatype.org/search/rest-api-guide/)
documents GA/GAV and packaging/classifier queries, limits and all-version search;
it does not define timestamp as first receipt, artifact upload, upstream release
or publication. Sonatype's separate [index explanation](https://central.sonatype.org/faq/what-happened-to-search-maven-org/)
describes indexing after publication and different update behavior between services.
That defeats equating indexing with publication by assumption, not every potential
operator-reported date contract.

The [Publisher API](https://central.sonatype.org/publish/publish-portal-api/)
documents a real PUBLISHED event/state and authenticated publishing operations.
Its illustrated status response associates deployment and package URLs but supplies
no historical per-version publication timestamp. Its HTTP Date examples date
responses, not publication. No authenticated operation was attempted.

The [Portal guide](https://central.sonatype.org/publish/publish-portal-guide/#webhook-request-details)
defines webhook timestamp as notification time and documents missing/duplicate
PUBLISHED notifications. The table calls the timestamp a long without establishing
an exact historical release-date precision contract. A retained producer notification
might support a separately specified observation claim; it is neither the selected
public metadata route nor permission to create a supplier-intake feature.

## Identity and version candidates

Repository artifact identity includes exact group/artifact/version text, extension
and classifier; dependency type can supply extension/classifier through a handler.
See [repository artifacts](https://maven.apache.org/repositories/artifacts.html),
[layout](https://maven.apache.org/repositories/layout.html) and
[3.9.11 handlers](https://maven.apache.org/ref/3.9.11/maven-core/artifact-handlers.html).
Keep the already reviewed source/context/model occurrence key separate. GA metadata
lists versions without proving that each classifier/extension exists at every one
of those versions, was published simultaneously or shares artifact bytes. No new
classifier-availability constraint is selected merely to obtain dates.

The metadata model's latest/release fields describe last additions, not a greatest
stable comparator. [Maven3.9.11 VersionsMetadata](https://maven.apache.org/ref/3.9.11/maven-resolver-provider/xref/org/apache/maven/repository/internal/VersionsMetadata.html)
sets release for a non-snapshot and merges version strings; it does not perform
universal prerelease classification. This is client code, not proof of Central's
server-side generation implementation.

The [POM version-order documentation](https://maven.apache.org/pom.html#version-order-specification)
and [ComparableVersion3.9.11](https://maven.apache.org/ref/3.9.11/maven-artifact/xref/org/apache/maven/artifact/versioning/ComparableVersion.html)
show Maven-specific comparison, recognized qualifiers, aliases and case-insensitive
order. Distinct strings can compare equally while naming distinct repository paths.
Equality of ordering is not permission to merge identities or substitute dates.
Unknown qualifiers' position in an ordering is not an assertion of stability.

Maven3.9.11's [DefaultVersionRangeResolver](https://maven.apache.org/ref/3.9.11/maven-resolver-provider/xref/org/apache/maven/repository/internal/DefaultVersionRangeResolver.html)
uses Resolver GenericVersionScheme. That [scheme's documentation](https://maven.apache.org/resolver/maven-resolver-util/apidocs/org/eclipse/aether/util/version/GenericVersionScheme.html)
acknowledges differences from ComparableVersion. A future comparator must name its
ordering authority and bound, not implement an unspecified generic SemVer framework
or claim to reproduce evaluated Maven resolution.

Central [coordinate guidance](https://central.sonatype.org/publish/requirements/coordinates/)
does not impose a universal version convention. Non-SNAPSHOT therefore cannot mean
stable: alpha/beta/milestone/RC versions can be release artifacts. The existing
Feature007 request subset continues to withhold ranges/aliases/SNAPSHOT ages; latest
must exclude prereleases/snapshots. Unknown stability cannot silently become stable
or be skipped to make an older candidate appear latest. No complete eligibility /
equal-order-maximum contract is frozen while the date prerequisite is unestablished.

## Completeness, disappearance and change

The positive documented metadata claim is versions currently available for a GA,
not an immutable log of every version ever published. Apache documents
[metadata correction](https://maven.apache.org/repository/central-metadata.html).
Central's [immutability policy](https://central.sonatype.org/faq/can-i-change-a-component/)
protects released contents; it does not establish atomic catalogue completeness,
universal stable classification or the meanings of all timestamps.

A future claim may use a fully bounded current catalogue rather than prove all
historical publication, but must state its scope and establish adequate freshness,
complete pagination and identity coherence. This investigation found neither a
particular target catalogue defect nor the complete contract needed for that claim.
Missing/deleted/changed metadata must remain unavailable/conflicting evidence;
absence is not proof of never-publication, private origin or permission to switch
identities/dates. No cached historical reconstruction, older dated maximum or
alternative/private endpoint may rescue the result.

## T1 acceptance accounting and stopping point

| Requested obligation | Result of this bounded investigation |
| --- | --- |
| Relevant public version | Exact repository coordinates identified; comparison-equivalent spellings are not interchangeable |
| Available date/event/authority | Modification, snapshot deployment and notification events identified; suitable public stable-release publication-date contract **not established** |
| Precision | Metadata text uses UTC seconds; Indexer uses a long file timestamp; event accuracy/precision of a suitable release date remains unestablished |
| Type/classifier granularity | Model versus artifact versus GA catalogue separated; variant publication/availability not certified |
| Latest candidate | Last-added metadata cannot substitute for greatest stable; actual admission contract remains unapproved |
| Stable/prerelease/snapshot | Snapshot and recognized qualifier semantics documented; arbitrary publisher stability not established |
| Ordering | Maven comparators and equal-order distinct identities documented; no unnamed generic comparator accepted |
| Candidate completeness | Current availability lists/search pagination identified; no complete truthful latest-history admission demonstrated |
| Missing/deleted/changed records | No fabrication, identity substitution or date fallback; absence means unavailable evidence |
| Visible limitations | Static projection, assumed comparator correspondence, catalogue/event limitations and independent view availability remain explicit |

**Stop before specification approval, planning, tasks or age implementation.**
A date field's format, successful HTTP or usefulness does not supply its authority.
No acquisition, content or producer-history minimum is being imposed on the age
claim: the missing fact is the meaning of the public date itself.

H1 needs no repeated human vote. To resume T1, obtain an operator/implementation
contract binding a public per-version timestamp to a suitable publication event,
including granularity, history scope and retrieval/completeness behavior, or propose
a separately authorized different date claim. Human acceptance cannot make an
undocumented timestamp true. This record chooses no proxy metric and does not
claim Maven is permanently nonviable. No request to an operator was sent.

## Run007-0004 focused publication-history investigation

2026-11-12. This fresh parent recovered the uncommitted007-0001–0003 artifacts,
including prior corrections and H1=NO. The human/orchestrator created the new
context after reporting approximately89% utilization; Codex did not initiate that
transition. The assignment supplies dedicated external research authority and
separates two questions: historical publication/availability dates and the current
latest comparator. Neither answer supplies the other. Earlier evidence is retained,
not reset or rewritten into a successful admission.

**Result: Outcome C.** A suitable, publicly retrievable historical timestamp-to-event
binding remains **unestablished**. Current-catalogue and ordering facts below are
positive technical findings, but no complete latest-stable policy is approved.
T1 stays open; whole specification remains unapproved; no plan, task graph or
implementation follows. No Java-specific proxy date is selected.

### Evidence classes and question1 event accounting

Here **contract** means documented interface semantics, **implementation** means
inspected versioned code, **historical** limits older documentation to its context,
**observation** means a bounded request, and **inference/unknown** is not admission.
Primary operator explanations and maintainer testimony are labeled separately.
All references were accessed in this run unless explicitly identified as retained
prior evidence. No secondary article or search snippet establishes authority.

| Interface / date | Exact established event and evidence class | Historical retrieval / identity | Sufficient for publication age? |
| --- | --- | --- | --- |
| GA metadata lastUpdated | Metadata update, UTC seconds; Maven model contract | One mutable GA metadata date, not a date per listed GAV | No |
| V-level SNAPSHOT timestamp / updated | Snapshot deployment / snapshot-information update; model contract | Snapshot-specific records can include extension/classifier; not stable-release history | No |
| Search GAV timestamp | Public response contains a numeric field; observation. Inspected guide does not define its event | One historical generic GAV retrieved; p and ec describe packaging/associated files, without per-file dates | No event binding admitted |
| Search GA latestVersion / its timestamp | Search result for a latest version; historical operator explanation calls displayed date last update | GA result is not a date catalogue for every historical version | No first-publication guarantee |
| Repository artifact/POM Last-Modified | Origin's belief about last change of selected representation; HTTP contract. Central production derivation unknown | Historical exact file URL can expose it; observations below | No established Central publication/write-event binding or migration invariance |
| Directory listing / response Date | Listing/file metadata / response origination, respectively | A directory or response is a different representation from an artifact | No |
| Index FILE_MODIFIED | Artifact/POM filesystem modification; Indexer7.1.6 implementation | Artifact identity includes GAV, classifier and extension; observable records only | No Central availability-event bridge |
| Index REC_MODIFIED / index generation | Index addition/removal / index generation or update | Supports synchronizing index records, not first-ever publication history | No |
| Historical Nexus2 Advanced Search Age | Time component has been available on Central; historical operator documentation | Documented one row per GAV, but no demonstrated mapping to today's public field, precision or retrieval contract | Suitable concept; usable timestamp route unestablished |
| Current Sonatype policy Age/AgeInDays | First Sonatype cataloging of component version; current product documentation | Policy-product data, not a documented public Central Search field mapping | Cataloging is not silently publication |
| Publisher PUBLISHED | Successful publication/upload to Central; operator state contract | Authenticated deployment status with PURLs; illustrated response has no historical per-GAV date | Suitable event exists, public historical timestamp route unestablished |
| Portal webhook timestamp | Notification time; operator contract | Deployment/package association; no complete public retrospective history; missing/duplicate PUBLISHED notices documented | No |
| Portal component Age / internal browse data | Relative UI age observed; backing event not defined by inspected public interface documentation | Exact GAV/PURL page exists; internal versions probe403, API-doc extraction only navigation | No |
| Operator deployment audit | Sonatype offers support-assisted details on who published and when | Visible deployment cleanup after90 days; no public automated retrospective interface established | Credible lead, not admitted public metadata authority |

The [Maven3.9.11 metadata model](https://maven.apache.org/ref/3.9.11/maven-repository-metadata/repository-metadata.html#versioning)
is explicit about metadata and snapshot events; these are not release-date gaps
to fill by interpretation. [Sonatype's2011 Search introduction](https://www.sonatype.com/blog/2011/06/you-dont-need-a-browser-to-use-maven-central)
describes a last-update display. Its [architecture explanation](https://www.sonatype.com/blog/2011/06/maven-central-search-architecture-overview)
describes changed index schemas/contents; neither identifies today's timestamp
as first Central availability. The [current Search guide](https://central.sonatype.org/search/rest-api-guide/)
documents queries, including GAV and packaging/classifier, without defining that
event. Familiar epoch units cannot supply it.

The [archived official Nexus2 UI source](https://github.com/sonatype/nexus-book/blob/master/chapter-using-nexus-ui.asciidoc)
and [Nexus2 Help, page103](https://download.sonatype.com/nexus/2/Sonatype%20Nexus%20Repository%202%20Help.pdf)
are affirmative operator evidence for a Central-availability-age concept. That
concept is narrower than upstream release and could suit the metric. The missing
bridge is an identifiable public historical field with that meaning. Meanwhile,
[current Sonatype policy constraints](https://help.sonatype.com/en/policy-constraints.html)
define Age from first cataloging. These products and dates must not be conflated.

The [Publisher API](https://central.sonatype.org/publish/publish-portal-api/)
documents state transitions and authenticated status, not the required public
history endpoint. [Webhook definitions](https://central.sonatype.org/publish/publish-portal-guide/#webhook-request-details)
date notification. The [deployment-retention FAQ](https://central.sonatype.org/faq/what-happened-to-my-deployments/)
says cleanup of deployments older90 days began2024-10-25 and offers support-assisted
publication audits. This prevents claiming operator history does not exist. No
support message, authenticated call or new supplier-evidence intake was attempted.

### HTTP Last-Modified and the staging counterexample

[RFC9110 section8.8.2, June2022](https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8.2)
defines representation modification and leaves its derivation to implementation.
HTTP-date supplies seconds, not publication-event accuracy. An authoritative
Central-specific mapping could make a header usable; this research found none.
No inspected Sonatype contract guarantees preservation through migration,
replication, historical synchronization or republication. This is **unknown**, not
a claim that any such operation demonstrably reset a timestamp. Central's
[immutability policy](https://central.sonatype.org/faq/can-i-change-a-component/)
does not by itself prove the original meaning or permanence of a header.

New adverse primary evidence: Apache Maven maintainer Hervé Boutemy's
[2026-10-31 statement](https://github.com/apache/tooling-trusted-releases/issues/1799#issuecomment-6545431482)
attributes Central's timestamp in the ASF release workflow to staging before the
release vote. The issue compares Enforcer3.7.0's Central, distribution and release
catalogue dates. This is **maintainer testimony about that workflow**, not a
universal Sonatype field specification or an independently reproduced release
timeline. It directly challenges the convenient inference that Central's displayed
date always marks first public availability. It does not establish an alternative
timestamp for libyears, nor require upstream-vote completion for a Central age claim.

### Central index field and completeness distinctions

[Apache's Central index documentation](https://maven.apache.org/repository/central-index.html)
describes weekly full indexes and incremental updates. It links Indexer as their
format; this is not a completeness/freshness SLA or permanent publication ledger.
The tagged7.1.6 [Record definition](https://raw.githubusercontent.com/apache/maven-indexer/maven-indexer-7.1.6/indexer-reader/src/main/java/org/apache/maven/index/reader/Record.java)
separates file modification from record addition/removal. [RecordExpander](https://raw.githubusercontent.com/apache/maven-indexer/maven-indexer-7.1.6/indexer-reader/src/main/java/org/apache/maven/index/reader/RecordExpander.java)
reads FILE_MODIFIED from the second component of raw i at line101, while raw m
becomes REC_MODIFIED at84/120. A terse raw-field description must not override
these distinctions. [MinimalArtifactInfoIndexCreator](https://raw.githubusercontent.com/apache/maven-indexer/maven-indexer-7.1.6/indexer-core/src/main/java/org/apache/maven/index/creator/MinimalArtifactInfoIndexCreator.java)
takes POM/artifact mtime at170/235 and encodes it inside i at261–274.

The format can represent classifier/extension and removal records. It does not
prove every historical/deleted variant is retained, that restamping is impossible,
or that Central production uses this tag unchanged. Repeated add/remove records
are index history, not proof of republication. No index archive was downloaded,
no consumer implemented, and no Java/Lucene tool executed. The documented workflow
uses a large repository-wide index and Java tooling; that is an operational cost
and boundary issue, independently of the missing event semantics. A theoretical
standard-library reader would not repair those semantics.

### Question2: catalogue, ordering and product eligibility

**Established technical portion:** [GA metadata](https://maven.apache.org/repositories/metadata.html)
is documented available-version discovery. A complete accepted response can support
the narrower current-GA-catalogue claim; all-ever history and atomic world-state
knowledge are not prerequisites. The versioned model's latest/release are last-added
fields, including/excluding snapshots respectively; neither is greatest stable.
Search core=gav documents all-version search, with rows limiting results. A single
page is insufficient. Indexes offer another delayed catalogue. No Portal internal
browse completeness contract was established. Metadata, Search and index must not
silently replace one another after a failure to obtain a convenient maximum.

Missing/deleted records prove neither never-publication nor private origin.
Maven documents [metadata correction and historical missing POMs](https://maven.apache.org/repository/central-metadata.html).
Changed catalogues can change future results. Complete bounded retrieval, exact
GA coherence, freshness disclosure, pagination/budget exhaustion and missing/conflicting
candidate behavior still require a concrete adapter contract. A current catalogue
does not reconstruct vanished history; this is a limitation, not a reason to demand
an impossible universal history. No target catalogue defect was found or asserted.

**Ordering is technically available, but must be named and versioned.** Tagged
[ComparableVersion3.9.11 source](https://raw.githubusercontent.com/apache/maven/maven-3.9.11/maven-artifact/src/main/java/org/apache/maven/artifact/versioning/ComparableVersion.java)
and [tests](https://raw.githubusercontent.com/apache/maven/maven-3.9.11/maven-artifact/src/test/java/org/apache/maven/artifact/versioning/ComparableVersionTest.java)
establish numeric/alphabetic transitions, separator effects, numeric component
comparison and case-insensitive qualifier ordering. The recognized order is
alpha < beta < milestone < rc < snapshot < empty < sp, followed by unknown
qualifiers lexically. cr aliases rc; ga/final/release alias empty; a/b/m expansion
in that implementation depends on a following digit. Tests equate spellings such
as1,1.0,1.0.0 and1-0. Ordering equivalence never merges exact repository paths/dates.

Maven3.9.11 [range-resolution implementation](https://raw.githubusercontent.com/apache/maven/maven-3.9.11/maven-resolver-provider/src/main/java/org/apache/maven/repository/internal/DefaultVersionRangeResolver.java)
uses GenericVersionScheme, not ComparableVersion. The inspected
[Resolver2.0.24 API](https://maven.apache.org/resolver/maven-resolver-util/apidocs/org/eclipse/aether/util/version/GenericVersionScheme.html)
documents its own segmentation, padding and qualifier rules and acknowledges
comparison differences. This URL is a moving documentation location;2.0.24 is
the version observed during this run. Maven4.0.0-rc-5's
[versioned API index](https://maven.apache.org/ref/4.0.0-rc-5/apidocs/allclasses-index.html)
identifies MavenVersionScheme as a GenericVersionScheme provider. This establishes
no all-revision Maven3/4 equivalence; detailed Maven4 implementation equivalence
was not recovered. A future bounded Python reproduction could explicitly adopt
one pinned Maven implementation with conformance witnesses; none was chosen,
implemented or executed here. SemVer, lexical order or another ecosystem's parser
cannot substitute. Comparator choice is a technical contract to name, not evidence
that no Maven-native ordering exists.

**Remaining consequential eligibility choice:** Central
[does not mandate a universal version convention](https://central.sonatype.org/publish/requirements/coordinates/).
Ordering defines precedence, not a universal stable predicate. Maven release
repository membership excludes ordinary SNAPSHOT publication but admits release
artifacts bearing alpha/beta/milestone/RC and arbitrary qualifiers; non-SNAPSHOT
cannot satisfy libyears' stable requirement. The smallest future alternatives are
an explicit conservative eligibility subset (with unknown potentially eligible
maxima refusing), or a separately accepted broader qualifier classification with
its limitations. Handling service packs, unknown qualifiers and equal-order maxima
must be explicit. Exclude prereleases/snapshots from latest; do not pick a tied
spelling by convenient date or substitute an older dated version. No eligibility
vote is requested now because it cannot repair question1. No universal Maven stable
flag or compatibility filtering was invented.

### Identity and the narrower GA-version claim

The existing S2 occurrence/model/artifact distinction remains. Dependency type and
POM packaging are different concepts; supported handlers map type to extension
and sometimes classifier. [Repository artifacts](https://maven.apache.org/repositories/artifacts.html),
[layout](https://maven.apache.org/repositories/layout.html) and
[3.9.11 handlers](https://maven.apache.org/ref/3.9.11/maven-core/artifact-handlers.html)
bind a concrete file using exact GAV plus extension/classifier. GA metadata enumerates
version strings; Search GAV records may expose packaging and an associated-file
list. Neither supplies each classifier's own publication timestamp. Index variant
identity does not convert file mtime into publication.

If an authoritative GAV date becomes available, a truthful claim could compare
**the public GA version history for the exact measured version and greatest eligible
version**, while retaining each occurrence's original type/classifier, artifact key
and limitations. It would certify neither variant availability at either date nor
variant compatibility, bytes, acquisition or evaluated selection. This does not
reopen the withdrawn H3 gate or choose an artifact-specific metric. At present no
GAV publication event is admitted, so this conditional claim cannot produce age.

### Bounded live probes and operational limits

All metadata probes used generic org.apache.maven:maven-core coordinates selected
from Maven documentation, never target manifests. Date:2026-11-12. Researcher
observations were reconciled by the parent; no target was contacted.

| Endpoint / method | Observed response | What it does and does not prove |
| --- | --- | --- |
| [Search exact3.9.11 GAV, GET](https://search.maven.org/solrsearch/select?q=g%3Aorg.apache.maven%20AND%20a%3Amaven-core%20AND%20v%3A3.9.11&core=gav&rows=2&wt=json) | numFound1, exact g/a/v, p=jar, timestamp1752345152000, ec listing POM/JAR/sources/javadoc/CycloneDX | Historical record retrievable; interpreted epoch value2025-07-12T18:32:32Z; event unspecified, no full catalogue tested |
| [3.9.11 POM, HEAD](https://repo.maven.apache.org/maven2/org/apache/maven/maven-core/3.9.11/maven-core-3.9.11.pom) | HTTP200, Last-Modified Sat,12 Jul2025 18:32:32 GMT | Matches Search exactly in one sample; correlation, not event authority |
| [3.0.5 POM, HEAD](https://repo.maven.apache.org/maven2/org/apache/maven/maven-core/3.0.5/maven-core-3.0.5.pom) | HTTP200, Last-Modified Tue,19 Feb2013 13:52:09 GMT | Older URL retains a date; two file samples cannot prove cross-migration invariance or universal coverage |
| [3.9.11 tests classifier, HEAD](https://repo.maven.apache.org/maven2/org/apache/maven/maven-core/3.9.11/maven-core-3.9.11-tests.jar) | HTTP404, NoSuchKey; error response also has Last-Modified11 Oct2025 | GAV existence does not certify arbitrary variant availability; an error representation date must never date an absent artifact; absence now proves no never-history |
| [Portal3.9.11 page](https://central.sonatype.com/artifact/org.apache.maven/maven-core/3.9.11) | PURL/POM and relative Age1 year ago in extraction | Exact identity and display observed; no exact event-date definition |
| [Internal Portal versions, GET](https://central.sonatype.com/api/internal/browse/component/versions?sortField=normalizedVersion&sortDirection=desc&page=0&size=5&filter=namespace%3Aorg.apache.maven%2Cname%3Amaven-core) | HTTP403 after authorized retry | No usable catalogue/date payload; not proof of absent service or data |
| [Portal API docs](https://central.sonatype.com/api-doc), attempted schema paths; [GA metadata](https://repo.maven.apache.org/maven2/org/apache/maven/maven-core/maven-metadata.xml) via browsing | Navigation-only extraction / access failures | No machine schema/date meaning or catalogue acquired; not semantic disproof |

Initial tool access/DNS failures were kept separate from successful curl responses;
sandbox-related network failures were retried with required escalation. TLS was not
disabled. HEAD fetched no archive/POM body; no index, Java, Maven, Gradle, resolver,
target code, machine configuration, credentials or private/alternate repository was
accessed. No raw cookies/large payloads need retention. Search API schema observations
do not establish indefinite service support.

The [Sonatype migration FAQ](https://central.sonatype.org/faq/what-happened-to-search-maven-org/)
distinguishes browser retirement from API continuation and describes index lag.
Its2023/24 intentions do not prove the deployed backend or a current deprecation
date. The legacy API is not rejected merely for age; unknown field semantics,
cross-index lag,429/rate limits, internal-interface instability and historical
retention are separate operational concerns. No operational concern supplies or
negates publication authority by itself.

### Reconciled stop

Question1: **not established**. Question2: current catalogue semantics and concrete
Maven ordering implementations are established comparison points; a complete
latest-stable admission policy is **not approved**. These partial facts are preserved
without calling the required publication-age mechanism partially successful.

The exact technical gap is a public, retrievable, historical per-version date with
authoritative publication/availability meaning and adequate identity/granularity,
including known staging/synchronization and historical-ingestion limitations.
No guarantee of an exact physical instant, content identity, upstream release,
or all-ever history is being demanded. A documented ecosystem-native Central
availability event would suffice at its stated precision and limitations.

The next HUMAN product direction is to defer Java, authorize investigation of a
different truthful date claim, or select another explicitly bounded direction.
H1 remains settled. No human can make an undocumented timestamp true by preference.
No proxy, source admission, specification approval, plan/tasks or implementation
is authorized by this negative research result.
