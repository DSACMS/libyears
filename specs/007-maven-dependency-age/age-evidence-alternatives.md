# Maven age-evidence alternatives — run007-0005

## Run007-0007 later product decision

No provider repaired publication authority. The human's rejection of ecosyste.ms
row creation remains binding. The later selected basis is direct versioned public
POM Last-Modified, explicitly conventional; it is not provider adoption or a date
fallback. Missing POM/date terminates measurement. See [current S7](spec.md#s7--maven-comparator-evidence-cascade-and-conventional-time-basis).
The following provider investigation and its then-pending selection remain history.


Human007-0006 **rejects ecosyste.ms created_at for Feature007 product use**: a
surviving-row bookkeeping date does not answer the required maintenance question
and may predate current-GAV association. The investigated fact below is retained,
not adopted. The [final ecosystem-practice rung](ecosystem-practice.md) separately
examines conventional tool date use; publication authority remains unestablished.

2026-11-12. Read with the [publication-history boundary](publication-history.md),
[human decisions](discovery.md), [draft specification](spec.md) and
[review disposition](reviews.md#run007-0005-alternative-age-evidence-review).

**Existing publication claim remains unsupported. A different narrow date fact is
publicly available: ecosyste.ms current version-record creation time.** This is
an alternative for human evaluation, not a selected age basis or a recommendation
to adopt it. It dates the provider's surviving record, not Central publication,
first public availability or necessarily first-ever provider observation.
The row's creation need not even date its association with the current GAV:
integrity-based reuse can update its version number. Sonatype
first cataloging has an authoritative definition and product API, but no anonymous
public historical date route was established in this bounded pass.

No provider, time basis, fallback, schema change, Java implementation or permanent
deferral is selected. T1 remains open and the whole specification unapproved.

## Bound, authority and evidence classes

The human accepts007-0004 and authorizes one bounded alternative-evidence pass.
The serious third-party set is **ecosyste.ms, Google deps.dev, Libraries.io and
Socket**. These have relevant metadata contracts or inspectable Maven derivations;
this is not a census of sites displaying dates. A brief Software Heritage check
is retained as a negative identity/claim comparison. Branch B examines current
Sonatype cataloging/API documentation and the current OSS Index/Guide interface.
The completed Central timestamp investigation and Maven ordering work are reused,
not repeated. Generic probes use org.apache.maven:maven-core:3.9.11, selected from
official Maven documentation in the prior run, never a target manifest.

**Contract** below means published provider/operator documentation; **implementation**
means inspected pinned source; **observation** means a bounded response; **inference**
and **unknown** confer no extra authority. Inspected source is not proof that its
exact revision is deployed. A reputable provider's publication label is affirmative
evidence of what it asserts; it does not alone substantiate the underlying Maven
event when the derivation remains unknown.

## Decision table

Historical retrieval and granularity are stated at the level actually established.
More detailed coverage, provenance, operational and privacy limits follow.

| Evidence source | Date/event; authority and provenance | Historical retrieval / identity | Coverage / operational limits | Truthful claim | T1 publication-compatible? / disposition |
| --- | --- | --- | --- | --- | --- |
| ecosyste.ms published_at | POM modification date transformed by open adapter; API also falls back to row creation | Public historical GAV response200; registry-specific GA/version, no classifier key | Mixed semantics, relocation path, no raw-event discriminator; no immutable history/SLA | Provider-reported field with conditional derivation | **No**; convenient but insufficient, no adoption |
| ecosyste.ms created_at | Current provider row creation; schema/model/ingestion implementation plus response | Public historical GAV response with separate date-time field | Row can change version identity; not current-GAV arrival or first-ever observation; imports/recreation preservation unknown | **Current ecosyste.ms version-record creation age** | **No**; different truthful candidate, HUMAN selection required |
| ecosyste.ms updated_at / package sync time | Provider record update / package processing | Public record fields, different identity levels | Mutable bookkeeping, not a historical first event | Current record freshness/processing time | No; not established as a useful version-age basis |
| Google deps.dev publishedAt | Provider contract asserts authority-reported publication; Maven derivation not inspectable in examined sources | Public v3 historical GAV response200; registries separately listed | Multi-registry coverage, missing dates, no all-ever guarantee | Provider-asserted publication date, unverified underlying event | **Not established**; no independent tier admitted |
| Libraries.io published_at | POM Last-Modified inserted as publishedAt by pinned adapter | Historical version model; live API docs403, no API data probe | Relocation may change date GAV; removal behavior; current API terms/quota unverified | Transformed repository modification date | **No**; rejected for publication |
| Socket publishedAt | Documented minimum of Central index file modification dates, with rollups/backfill | Maven package/version use documented; no live API probe | File versus package rollups; backfill can lower dates; account/quota implications | Derived index-modification fact | **No**; inspectable derivation does not change its event |
| Sonatype catalogDate / Cataloged | Operator-defined first catalog ingestion/analysis; IQ API example | Historical component API inside IQ, exact GAV+extension/classifier; authenticated instance | Public anonymous date route, retention and migration invariance unestablished | Sonatype first-cataloged age | **No**; coherent different claim, access/coverage not established for public CLI |
| Current Guide / OSS Index compatibility | Current public schema has no specified catalog-date event field | Public docs/schema; service routes require authentication | Migration, plans/credits, incomplete detail schema | No admitted historical component-date fact | Unavailable as date evidence in this pass |
| Historical Central availability Age / operator audit | Prior operator concept / support-assisted audit | No new current public field binding; audit requires support interaction | Prior007-0004 boundary preserved, not disproved | Potential Central-availability claim if future binding supplied | Still unestablished; no new timestamp search or support message |
| Software Heritage origin visit | Documented archive-origin observation | Origin-visit history, no inspected Maven GAV association | Archive/source identity differs from package publication | Archive visit time | No; no sufficient GAV-bound alternative established |

## ecosyste.ms: inspectable derivation and a distinct record date

Pinned packages source: revision
[60bcf257e094078dd060e28f6b47bfd3cf381d55](https://github.com/ecosyste-ms/packages/tree/60bcf257e094078dd060e28f6b47bfd3cf381d55),
observed current2026-11-12. The
[Maven adapter](https://github.com/ecosyste-ms/packages/blob/60bcf257e094078dd060e28f6b47bfd3cf381d55/app/models/ecosystem/maven.rb)
fetches a POM, inserts a synthetic publishedAt using its response modification
header, then parses that into version metadata. Source comments distinguish Google
mirror bucket-arrival dates from x-goog-meta-last-modified and missing bulk-import
metadata. The [backfill worker](https://github.com/ecosyste-ms/packages/blob/60bcf257e094078dd060e28f6b47bfd3cf381d55/app/sidekiq/maven_central_published_at_worker.rb)
returns to Central POM HEAD Last-Modified. These are implementation/comment facts,
not a new operator publication contract. No Google mirror or alternate repository
was contacted. An [open provider issue](https://github.com/ecosyste-ms/packages/issues/657)
also discusses incorrect Maven dates; the derivation, rather than the issue label,
is the decisive evidence here.

The [Version model](https://github.com/ecosyste-ms/packages/blob/60bcf257e094078dd060e28f6b47bfd3cf381d55/app/models/version.rb)
returns stored published_at when present, otherwise created_at. The
[API serializer](https://github.com/ecosyste-ms/packages/blob/60bcf257e094078dd060e28f6b47bfd3cf381d55/app/views/api/v1/versions/_version.json.jbuilder)
exposes that accessor and separate created_at/updated_at, with no explicit raw-null
or date-origin discriminator. Equality of dates would not prove which route ran.
The public published_at field therefore cannot silently become either publication
or first observation.

[Schema](https://github.com/ecosyste-ms/packages/blob/60bcf257e094078dd060e28f6b47bfd3cf381d55/db/schema.rb),
[ingestion model](https://github.com/ecosyste-ms/packages/blob/60bcf257e094078dd060e28f6b47bfd3cf381d55/app/models/package.rb)
and [OpenAPI](https://github.com/ecosyste-ms/packages/blob/60bcf257e094078dd060e28f6b47bfd3cf381d55/openapi/api/v1/openapi.yaml)
support the narrower current version-row creation interpretation: created_at is
a database timestamp exposed as date-time, with ordinary ingestion creating version
records. No inspected contract establishes first-ever provider observation or
preservation through imports, restoration, reset or record recreation. The current
row's timestamp is retrievable; its first creation is not an immutable observation
ledger. Accepting this narrow fact would require trusting the provider's timestamp
and implementation, not pretending to have independently witnessed ingestion.

Fresh review adds an important identity limit from that same ingestion method:
when integrity is present, update_versions can reuse a matching row and assign new
metadata including number; the Maven adapter supplies artifact SHA1 integrity.
Thus created_at can precede the row's association with its current GAV. This is an
inspected code path, not a reproduced production event. The candidate fact is only
the provider-reported creation timestamp of the surviving row, never when the
provider first learned or recorded this exact version. Keeping row identity and
current version association separate is essential even for the alternative claim.

Identity and audit limits matter independently. The Maven adapter follows POM
relocation in get_pom before extracting the date, while separately retaining original
POM packaging/relocation metadata. A relocated GAV date can therefore accompany an
original version record in that code path; this was not reproduced as a live defect.
GA/version keys and PURLs do not separate classifier/extension histories. Registry,
download and documentation links help locate sources but are not retained raw
POM/header snapshots or an immutable date-provenance record. Optional repository
tags do not establish Central publication.

Catalogue ingestion uses native metadata, HTML fallback, version filtering and POM
availability, with discovery feeds that acknowledge sibling gaps and a former feed
stopping. Ordinary updates do not make every absent version a deletion; package
removal/status and destruction can remove or mark associated records. No all-ever
or immutable-deletion-history guarantee was found. The
[versions controller](https://github.com/ecosyste-ms/packages/blob/60bcf257e094078dd060e28f6b47bfd3cf381d55/app/controllers/api/v1/versions_controller.rb)
defaults to date-based ordering; [pagination configuration](https://github.com/ecosyste-ms/packages/blob/60bcf257e094078dd060e28f6b47bfd3cf381d55/config/initializers/pagy.rb)
uses page/per_page, default100/cap1000. It does not replace the unapproved Maven
greatest-stable selector or demonstrably improve native candidate completeness.

## Other serious provider routes

**Google deps.dev** offers an affirmative, documented publication assertion. Its
[v3 contract](https://docs.deps.dev/api/v3/) defines publishedAt as authority-reported
publication time when available; GetVersion provides historical version lookup,
and GetPackage lists available versions. Maven names are GA with version separately;
registry links distinguish Central from its additional Maven registries. A default
version flag has system-specific meaning, not an approved greatest-stable policy.
The [pinned public schema](https://github.com/google/deps.dev/blob/ccc876faeb8fdcfd2b638804d544f90ff959632f/api/v3/api.proto)
supplies the assertion and representation, not the Maven timestamp collector.

The [FAQ](https://docs.deps.dev/faq/) describes feed/background-scan freshness and
a non-open underlying platform. No inspected Maven derivation or retained original
timestamp record binds the assertion to Central publication/first availability.
The probe's agreement with prior Search/Last-Modified is correlation: it proves
neither reuse nor independence. Trusting this as an evidence tier would require
accepting the provider's unsubstantiated Maven event interpretation; that decision
is not made here. No public per-version first-observed timestamp was identified.
Historical/deleted-version retention and date corrections remain unestablished.

**Libraries.io** is inspectable at
[b2990526b7441c2581c264763e0efd53807d86ca](https://github.com/librariesio/libraries.io/blob/b2990526b7441c2581c264763e0efd53807d86ca/app/models/package_manager/maven.rb).
Its Maven adapter explicitly inserts HTTP Last-Modified as publishedAt and parses
that into published_at. It follows relocation while preserving the original sync
version in output, creating a separate identity-binding concern. The
[Central subclass](https://github.com/librariesio/libraries.io/blob/b2990526b7441c2581c264763e0efd53807d86ca/app/models/package_manager/maven/maven_central.rb)
uses directory enumeration and MissingVersionRemover; neither is an immutable
publication ledger. Its latest selection is not adopted as Maven ordering.
Multiple Maven sources are supported, so an ecosystem/name alone does not certify
Central. API documentation/terms access failed; no current account/quota/data-license
or retention guarantee is asserted from repository code licensing.

**Socket** documents provenance explicitly in its
[cool-down policy](https://docs.socket.dev/docs/cool-down-policy): Maven publishedAt
comes from Central index artifact modification dates, with minimum rollups across
files and package versions; maintenance backfill only lowers stored dates. This
is a deterministic derivation from modification evidence, not a new publication
event. The [API introduction](https://docs.socket.dev/reference/introduction-to-socket-api)
describes account/usage functions; no Socket account, scan, manifest upload or API
data request was needed once the derivation failed T1. These Socket rules are not
libyears arithmetic or permission to change sibling ecosystem date policies.

The brief [Software Heritage journal comparison](https://docs.softwareheritage.org/devel/journal.html)
provides origin-visit events rather than a demonstrated Maven GAV history. No archive
consumer or source-commit substitution was investigated or authorized.

## Sonatype-native alternatives: event versus access

New current operator documentation precisely defines cataloging. The
[Component Details Page](https://help.sonatype.com/en/component-details-page.html)
describes the component version's first record in Sonatype's catalog, through
upstream or fallback sources, and first ingestion/analysis; it explicitly warns
that this can differ from upstream publication/release. The
[automatic quarantine documentation](https://help.sonatype.com/en/automatic-quarantine-release.html)
independently separates cataloging from external repository publication.

The [IQ Component Details API](https://help.sonatype.com/en/component-details-rest-api.html)
documents POST api/v2/components/details, with Maven/PURL/hash input and an example
historical catalogDate associated with exact GAV, extension/classifier and match
state. This is an IQ-instance product interface, with authenticated examples,
not an anonymous Central date API. The [versions API](https://help.sonatype.com/en/component-versions-rest-api.html)
enumerates known versions, not guaranteed complete Central history. No IQ instance
or authenticated endpoint was contacted. The response's truncated hash is an
identifier, explicitly not a checksum.

A [2020 OSS Index operator update](https://www.sonatype.com/blog/ossindex-update)
describes catalog dates/version history and when Sonatype learned about versions.
It is historical evidence of an actual product concept. The current
[Guide API reference](https://help.sonatype.com/en/guide-api-reference.html) links a
[public OpenAPI artifact](https://sonatype.github.io/sonatype-documentation/api/guide/latest/guide-api.json).
Its component-detail schema declares only malware; versions has a publishedWindow
filter without a defined component-date event; publishedAt in vulnerability details
does not date component versions. OSS Index compatibility schemas expose coordinates,
description, reference and vulnerabilities, not catalogDate. These schema omissions
do not prove production can never return other fields. They do not supply the
missing date contract either.

[Migration documentation](https://help.sonatype.com/en/oss-index-migration-to-sonatype-guide.html)
and [steps](https://help.sonatype.com/en/oss-index-migration-steps.html) describe
authenticated Guide routing, April28 2026 migration, December31 2026 legacy sunset,
plans/credits. [Anonymous Guide access](https://help.sonatype.com/en/anonymous-access-to-sonatype-guide.html)
is a public research UI, not an established anonymous historical catalog-date API.
Catalog-date invariance across reingestion/migration/corrections, fallback-source
timing relative to Central, deleted-version coverage and cross-product date equality
remain unknown. No universal before/after bound on Central availability is inferred.

Historical Nexus2 availability Age and support-assisted publication audits retain
their007-0004 meanings. No new current public binding to first Central availability
was established. No operator was messaged and no repeated Central field hunt ran.

## Bounded probes and operational/privacy accounting

Two generic per-version data probes were sufficient; no full candidate catalogue
was fetched. Public provider documentation/source/schema requests are separate.

| Endpoint | Observed response | Limit |
| --- | --- | --- |
| [ecosyste.ms GET](https://packages.ecosyste.ms/api/v1/registries/repo1.maven.org/packages/org.apache.maven%3Amaven-core/versions/3.9.11) | HTTP200, response Date2026-11-12T18:25:54Z; number3.9.11; published_at2025-07-12T18:32:32.000Z; created_at2025-07-16T12:01:27.566Z; updated_at2026-08-13T12:11:47.395Z; exact PURL; tag/integrity null | One surviving GAV row, not catalogue/history completeness or deployment-revision proof |
| [deps.dev GET](https://api.deps.dev/v3/systems/maven/packages/org.apache.maven%3Amaven-core/versions/3.9.11) | Exact identity; publishedAt2025-07-12T18:32:32Z; registry https://repo.maven.apache.org/maven2/ | Matches prior native observations; no derivation inference |

ecosyste.ms response Last-Modified2026-11-12T10:25:29Z is API representation
freshness, separate from all three JSON dates. Its observed anonymous rate-limit
header advertised5000 requests; [pricing](https://home.ecosyste.ms/pricing)
advertises free300/hour and no SLA, with paid tiers. Keep that discrepancy rather
than promising an allowance. [Authentication docs](https://docs.ecosyste.ms/docs/usage/authentication/)
describe anonymous and contact-email polite access; no email/key/account was supplied.
Provider-stated API data licensing is CC BY-SA4.0 and code AGPL, with alternate
commercial licensing; these are reported terms, not legal advice or adoption
approval. The [privacy policy](https://ecosyste.ms/privacy) describes IP/page/time
logging. Source links are inspectable, but future evidence intake would still need
bounded fixed destinations, provenance discrimination, identity checks and terms
review. No provider code or metadata-directed download URL was executed/followed.

deps.dev [API versions](https://docs.deps.dev/api/) distinguish v3 stability from
alpha; its v3 data/terms section permits caching and distinguishes upstream terms
from generated CC-BY4.0 data and Google API terms. This strengthens operational
credibility, not timestamp authority. Libraries.io current API terms/quota remain
unverified after403. Socket account/quota and Sonatype product authentication/credits
would add production dependencies; this run establishes no entitlement or SLA.

Any future provider request discloses coordinates/versions, IP and timing to another
operator; PURL/hash queries disclose those values too. Existing Central disclosure
authority cannot silently transfer to a provider. Only generic public research
identities were queried here. Initial tool/DNS failures were retried with required
escalation and distinguished from service responses. No credentials, manifests,
target-derived coordinates, private/alternate repository, archive, Java/Maven/Gradle,
package installation or target code was accessed/executed. No TLS bypass.

The Guide schema snapshot is56955 bytes, SHA256
af1e19af8fe61671facf6d94c9bc5df822b074538ad45f178cfd6aa7c86045d1;
this preserves the inspected public schema, not a production response guarantee.

## Maintenance utility and independent evidence dimensions

| Time basis | Maintenance question | Utility and misleading-risk analysis |
| --- | --- | --- |
| Public publication/availability | How does my version compare within the ecosystem's public version chronology? | Preferred existing claim; no new sufficient source here; comparable only within each adapter's disclosed event |
| Sonatype first cataloging | How do versions compare in when Sonatype first ingested/analyzed them? | Coherent catalogue/security-observation question, but public access and historical stability unestablished; not Central release chronology |
| ecosyste.ms current version-record creation | How do versions compare in when their surviving ecosyste.ms records were created? | Public and inspectable narrow fact; limited upgrade-age utility. Backfill/import/recreation can plausibly dominate ordering; no first-ever/continuous-history guarantee. This is a limitation, not a reproduced reset event |
| Provider first observation | How long has a provider known about the version? | Potentially understandable, but no examined public field establishes immutable first-ever observation for these Maven versions |
| Repository/index modification | How do provider/native file-modification values compare? | Inspectable derivations exist, but original event, variant and history limits remain; does not answer publication-age question |

No date label makes every truthful fact a useful libyears metric. Current provider
record creation would need conspicuous wording in README/ECOSYSTEMS and output;
calling it release age would mislead. Its comparability with sibling publication
bases is weak, and collection waves could produce ties or reverse version-date
order. For example, releases years apart ingested together could have near-zero
record-date difference; this is a hypothetical utility counterexample, not a live
measurement. Integrity-based row reuse further prevents treating creation as the
current GAV's arrival date. No arithmetic/anomaly policy is changed to accommodate
these possibilities.
Sonatype cataloging is conceptually stronger as a named observation event, but its
product access boundary remains real. Neither is chosen for the human.

Retain the prospective distinction: **version basis** (Declared/Observed) is
independent of **time basis** (publication/availability/cataloging/provider record
or observation). Either accepted version fact would need its own exact identity
join to an accepted time fact. A provider dependency graph cannot manufacture the
repository's Observed view. Independent coverage and non-additive totals remain;
time-basis evidence grants no local population, source correspondence, acquisition,
content, resolver or runtime authority. This is useful future product/methodology
evidence, not a generalized architecture, schema axis or sibling retrofit.

## Stop for human selection

**Different truthful age basis available — HUMAN SELECTION REQUIRED**, narrowly:
the creation time reported for the current ecosyste.ms version record. This is
technically retrievable evidence, not approved production fitness or an immutable
first-observation claim. The human may reject its maintenance utility. Sonatype
cataloging remains a defined but access-limited alternative; deps.dev publication
remains an assertion without inspected Maven derivation. No source closes T1.

Human selection must decide whether any different claim merits further bounded
product specification, whether stronger provenance/access evidence should be sought
for a named route, or whether to defer/redirect Java. No open-ended timestamp search,
provider adoption, proxy relabeling, plan/tasks or implementation follows here.
