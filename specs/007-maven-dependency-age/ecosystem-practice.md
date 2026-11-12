# Maven ecosystem date practice — run007-0006

## Run007-0007 human selection following this investigation

The human accepts the narrow MODERATE convention established here and authorizes
its specification as conventional Maven dependency age. The exact claim remains
repository-reported versioned POM representation modification time; it gains no
publication/upstream/first-availability authority. Renovate direct use and
Dependabot fallback remain distinct. [S7](spec.md#s7--maven-comparator-evidence-cascade-and-conventional-time-basis)
now governs disclosure and terminal missing-date behavior; [latest eligibility](latest-policy.md)
remains a human choice. The original investigation below remains unchanged history,
including its then-unselected candidate and stop. No additional date survey ran.


2026-11-12. Final currently authorized evidence rung, following the negative
[publication investigation](publication-history.md) and bounded
[provider investigation](age-evidence-alternatives.md). See [decisions](discovery.md)
and [review disposition](reviews.md#run007-0006-ecosystem-practice-review).

**Finding: MODERATE CONVENTION, narrowly scoped to repository-served POM
modification dates as release-age surrogates in established update tooling.**
Renovate directly uses this field; current Dependabot Maven uses it as a missing-date
fallback. They are unrelated implementations with operational cooldown use, not
independent witnesses of a publication event. This is a credible conventional
candidate for human selection, **not a universal Maven chronology or an approved
libyears time basis**. Other inspected practices are materially different.

The human rejects ecosyste.ms row creation for Feature007 product use: it is
provider bookkeeping and need not date the current GAV's arrival. That truthful
prior finding remains retained; it is not a fallback candidate. No timestamp
previously rejected as publication has acquired new publication semantics.

## Bound and epistemic distinction

The bounded required set is Central UI, MvnRepository, Dependabot, Renovate,
OpenRewrite, Sonatype products, deps.dev and Libraries.io. Two small additional
independent comparisons are Scala Steward cooldowns and a historical Maven Versions
Plugin lookup path. No further provider census or native timestamp hunt ran.

**Contract** means tool/operator documentation; **implementation/tests** means
inspected pinned code and tests, not executed behavior; **observation** means bounded
public extraction/response; **inference** is explicitly limited. Source revision
does not prove deployment. A conventional claim describes established practice;
it cannot establish first Central publication, first availability, upstream release,
acquisition, bytes or producer history. Version basis (Declared/Observed) stays
independent of this time-basis investigation.

## Tool and service evidence

| Tool/service | Date label and underlying fact | Operational use / ordering | Evidence and limitation |
| --- | --- | --- | --- |
| Central UI | Age and DATE PUBLISHED labels; backing derivation unestablished | Human chronology display | Generic exact page shows Age1 year ago; versions table extraction has no dated rows. No exact public event binding follows |
| MvnRepository | Date / Release date; origin field opaque | Human version comparison/history; Latest Versions includes prereleases | Generic3.9.11 displays Jul15 2025, differing from prior Jul12 native/header sample. Correlation or identity of fields not established |
| Renovate | releaseTimestamp from versioned POM Last-Modified, or supported result lastModified | minimumReleaseAge cooldown after version discovery/order | Current pinned implementation and tests plus explicit documentation; direct positive operational practice |
| Dependabot Maven | released_at from repository version-directory listing; missing date may use exact POM HEAD Last-Modified | Cooldown gating; ordinary candidate ordering can operate without dates | Current pinned implementation/tests; POM date is a fallback, not the primary common source |
| OpenRewrite | No per-version date in inspected upgrade-selection path | GA version strings and configured version comparator | Historical pinned8.69.0 plus current selector docs; not a claim that every recipe is date-free |
| Sonatype security/policy products | Age from first cataloging/ingestion/analysis | Quality policy/quarantine decisions | Operator-defined catalogue age, explicitly different from publication; reuse007-0005 access limits |
| deps.dev | API publishedAt asserts authority-reported publication; docs describe version histories | Metadata/version chronology; default version is system-specific | Current UI probe inaccessible; no new Maven collector provenance or operational elapsed-age rule established |
| Libraries.io | published_at derives from POM Last-Modified in retained pinned adapter | Version metadata; current UI unavailable in this pass | Corroborates transformation practice, not a separately proven current UI claim or publication fact |
| Scala Steward | firstSeen from the instance's retained version cache | Configured minimumAge cooldown | Inspected0.38.0 source/release notes explicitly use observation, not repository release date |
| Maven Versions Plugin | No per-version date in inspected lookup/comparison methods | Resolver candidates, ignored-version rules, ArtifactVersion/TreeSet | Historical2.19.1 sample only; current policy defaults must not be inferred from it |

### Renovate: explicit, operational POM-date practice

Current inspected source revision
[d2c60e619b192ea9a11d7e1833f612c9fe9002ec](https://github.com/renovatebot/renovate/tree/d2c60e619b192ea9a11d7e1833f612c9fe9002ec).
Its [Maven datasource](https://github.com/renovatebot/renovate/blob/d2c60e619b192ea9a11d7e1833f612c9fe9002ec/lib/modules/datasource/maven/index.ts)
reads GA metadata for candidates, separately postprocesses a versioned POM GET and
assigns lastModified to releaseTimestamp. The
[HTTP utility](https://github.com/renovatebot/renovate/blob/d2c60e619b192ea9a11d7e1833f612c9fe9002ec/lib/modules/datasource/maven/util.ts)
extracts the response header; [tests](https://github.com/renovatebot/renovate/blob/d2c60e619b192ea9a11d7e1833f612c9fe9002ec/lib/modules/datasource/maven/index.spec.ts)
assert the exact transformation with mocked POM responses. These are code/test
facts, not measurements or event provenance.

[Datasource docs](https://docs.renovatebot.com/modules/datasource/maven/) explicitly
identify Last-Modified/result lastModified. The
[minimum-release-age guide](https://docs.renovatebot.com/key-concepts/minimum-release-age/)
documents per-version cooldown, registry timestamp dependency and missing-date
behavior, with a configurable timestamp-optional exception. The inspected guide
identifies its documentation version as44.236.2. It explicitly requires reliable
Maven modification headers. This is stronger convention evidence than a decorative
date: a mature tool deliberately operationalizes the field. Its public-Central
prepending guidance for custom registries is **not** permission to import that
lookup policy into libyears or to contact alternate registries here.

### Dependabot: directory dates first, POM fallback separately

Current inspected source revision
[2e9740c209afb78cffb2c0bddf599642b527d3a9](https://github.com/dependabot/dependabot-core/tree/2e9740c209afb78cffb2c0bddf599642b527d3a9).
The [shared Maven fetcher](https://github.com/dependabot/dependabot-core/blob/2e9740c209afb78cffb2c0bddf599642b527d3a9/maven/lib/dependabot/maven/shared/shared_package_details_fetcher.rb)
obtains XML version strings with initially absent dates; it parses adjacent text
beside version-directory links in a GA listing and joins those dates by version
string. Those are directory-listing values, **not POM headers**, and are not
established as equivalent physical events.

The [package fetcher](https://github.com/dependabot/dependabot-core/blob/2e9740c209afb78cffb2c0bddf599642b527d3a9/maven/lib/dependabot/maven/package/package_details_fetcher.rb)
retains an existing released_at; when missing, it HEADs the exact POM in the recorded
configured repository, parses Last-Modified and supplies released_at. The
[version finder](https://github.com/dependabot/dependabot-core/blob/2e9740c209afb78cffb2c0bddf599642b527d3a9/maven/lib/dependabot/maven/update_checker/version_finder.rb)
invokes this enrichment for cooldown. [Tests](https://github.com/dependabot/dependabot-core/blob/2e9740c209afb78cffb2c0bddf599642b527d3a9/maven/spec/dependabot/maven/package/package_details_fetcher_spec.rb)
cover fallback, retaining existing dates and repository/version caching.

Its [base selector](https://github.com/dependabot/dependabot-core/blob/2e9740c209afb78cffb2c0bddf599642b527d3a9/maven/lib/dependabot/maven/shared/base_version_finder.rb)
separates ordinary ordering/filtering from cooldown. Current GitHub
[options documentation](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#cooldown)
and [July14 2026 announcement](https://github.blog/changelog/2026-07-14-dependabot-version-updates-introduce-default-package-cooldown/)
describe a default three-day version-update cooldown. That current product behavior
must not be described as necessarily opt-in; source branches without cooldown can
nevertheless select versions without dates. Security-update behavior is separate.
Calendar-like version-string filtering is also distinct from timestamp use.

### Date-free modernization and a genuinely different cooldown

OpenRewrite inspected release8.69.0 at
[a237de36a21ab75ebaf28def6825bedc978339bf](https://github.com/openrewrite/rewrite/tree/a237de36a21ab75ebaf28def6825bedc978339bf).
[MavenDependency.findNewerVersion](https://github.com/openrewrite/rewrite/blob/a237de36a21ab75ebaf28def6825bedc978339bf/rewrite-maven/src/main/java/org/openrewrite/maven/trait/MavenDependency.java)
filters metadata version strings through its configured comparator; it does not
read publication or metadata-update dates in that path. The
[metadata model](https://github.com/openrewrite/rewrite/blob/a237de36a21ab75ebaf28def6825bedc978339bf/rewrite-maven/src/main/java/org/openrewrite/maven/tree/MavenMetadata.java)
stores metadata/snapshot dates without turning them into stable-version dates.
Current [selector documentation](https://docs.openrewrite.org/reference/dependency-version-selectors)
describes version policies, not an elapsed-age requirement. Historical
[Versions Plugin2.19.1 lookup](https://github.com/mojohaus/versions/blob/804a5ab508d512bb44726fa665481cec9342dc91/versions-common/src/main/java/org/codehaus/mojo/versions/api/DefaultVersionsHelper.java)
adds a small independent ordering-only comparison; it does not establish current
plugin defaults or a universal absence of dates elsewhere.

Scala Steward0.38.0, pinned
[cfc35f4e63bef9d4423f375b1fef35caf642e61a](https://github.com/scala-steward-org/scala-steward/tree/cfc35f4e63bef9d4423f375b1fef35caf642e61a),
is a material operational counterexample. Its
[VersionsCache](https://github.com/scala-steward-org/scala-steward/blob/cfc35f4e63bef9d4423f375b1fef35caf642e61a/modules/core/src/main/scala/org/scalasteward/core/coursier/VersionsCache.scala)
records now for newly encountered versions, retaining prior firstSeen where known,
under a dependency/resolver cache key. [CooldownConfig](https://github.com/scala-steward-org/scala-steward/blob/cfc35f4e63bef9d4423f375b1fef35caf642e61a/modules/core/src/main/scala/org/scalasteward/core/repoconfig/CooldownConfig.scala)
filters by that age. [Release notes](https://github.com/scala-steward-org/scala-steward/releases)
explicitly warn that upgrading starts collection and initially no artifacts appear
older than the upgrade point. This is retained instance observation, not a public
historical date service or first-ever global observation. It is not the rejected
ecosyste.ms bookkeeping route, nor a new provider candidate.

### Human displays and other service terminology

On2026-11-12 the generic [Central exact page](https://central.sonatype.com/artifact/org.apache.maven/maven-core/3.9.11)
extraction showed Age1 year ago; its [versions page](https://central.sonatype.com/artifact/org.apache.maven/maven-core/versions)
labeled DATE PUBLISHED but had empty loading rows. The exact-page extraction was
marked crawled two months earlier; direct HTML returned429 after authorized retry.
No backing-field derivation was obtained. This supports terminology practice,
not a newly demonstrated current exact date or event contract.

[MvnRepository exact version](https://mvnrepository.com/artifact/org.apache.maven/maven-core/3.9.11)
showed Date Jul15 2025, its [changes page](https://mvnrepository.com/artifact/org.apache.maven/maven-core/3.9.11/changes)
called it Release date, and the [catalogue](https://mvnrepository.com/artifact/org.apache.maven/maven-core)
included alpha/beta/RC versions under Latest Versions. Extracted pages were marked
crawled one to three months earlier; direct HTML returned403. That displayed date
differs from007-0004's July12 POM/header observation. Cause unknown: do not infer
scraping, correct publication, timezone explanation or a proven service defect.
Its [About page](https://mvnrepository.com/about) does not disclose date derivation;
[Sonatype disclaims a formal relationship or accuracy knowledge](https://central.sonatype.org/faq/mvnrepository/).
Popularity and a release-date label are weak convention evidence on their own.

Sonatype [Age policy](https://help.sonatype.com/en/policy-constraints.html) and
[quarantine documentation](https://help.sonatype.com/en/automatic-quarantine-release.html)
operationalize first cataloging, explicitly not external publication. Its
[2020 OSS Index explanation](https://www.sonatype.com/blog/ossindex-update)
calls catalogue dates a chronology of when Sonatype learns about versions. These
are coherent different purposes, not proof that one common Maven date exists.
deps.dev [documentation](https://docs.deps.dev/api/v3/) retains the publishedAt
assertion and version-history role; exact UI extraction failed, so no new UI label
is claimed. Libraries.io UI extraction likewise failed; its retained007-0005 adapter
evidence is reused without a new provider investigation. Neither service supplies
a newly substantiated publication event or extra independent operational bot vote.

## Convention test and narrow possible claim

The positive route is real: Renovate's direct POM-header use and Dependabot's
explicit POM-header fallback operationalize the **same named field class** through
independent TypeScript/Ruby implementations. Renovate documents the mapping; source
and tests make both transformations inspectable. Libraries.io's retained derivation
corroborates use beyond those bots, without being counted as another independent
historical witness. Retrieval of historical POM headers was already observed in
007-0004 and is not repeated here.

The limits prevent a STRONG or universal-convention claim: Dependabot primarily
uses directory dates; Scala Steward uses instance observation; Sonatype uses
cataloging; OpenRewrite's inspected modernization path does not need dates; Central
and MvnRepository labels do not establish derivation or agreement. The two bots'
existence does not make every Maven timestamp equivalent or prove how long the
current Dependabot fallback has existed. Thus the classification is **MODERATE,
for this narrow repeated POM-date surrogate**, with fragmented wider practice.
This is an evidence judgment, not majority voting or product selection.

The narrowest defensible candidate wording is:

> Maven conventional POM-date age compares versions using their public repository
> POM Last-Modified values, following an established release-age surrogate used
> by Maven dependency-update tools. It does not measure first publication.

This proposed basis selects no implementation or behavior. Its truthful fact is
the repository-reported POM representation modification timestamp; its conventional
role comes from tooling practice. No new event semantics are asserted. It would
be misleading to call it first public availability or general upstream release age.

| Candidate obligation | Established / remaining limitation |
| --- | --- |
| Exact field / retrieval | Last-Modified of the exact versioned public POM; Renovate GET, Dependabot fallback HEAD. No directory/Search/index/ingestion substitution implied |
| Identity | GAV's POM representation, extension=pom; not the dependency's classifier/type artifact date or bytes |
| Historical availability | Old public POM header samples from007-0004; no guarantee for every version, missing POM, migration or immutable historical retention |
| Candidate completeness | Native current GA catalogue may suffice; bots' registry aggregation/fallbacks do not establish libyears completeness or stable policy |
| Operational sustainability | Ordinary fixed public POM requests; bounded per-version availability, status, rate limits, TLS and cache behavior need a later approved contract |
| Disclosure / source authority | Supported coordinates only after existing local comparator admission. Never copy bot private-registry access or public-namesake/prepending policy |
| Known divergence | Existing limited staging testimony challenges publication equivalence; missing/restamped representation dates and history invariance remain limits, not asserted universal failures |
| Version views | Apply an independently admitted exact time fact to each supported Declared/Observed version; never manufacture Observed, combine totals or deduplicate occurrences |

## Latest practice, utility and human gate

Tools agree that version ordering and eligibility are separate from timestamp
enrichment, but their policies differ. Renovate's Maven implementation recognizes
prerelease qualifiers yet [tests](https://github.com/renovatebot/renovate/blob/d2c60e619b192ea9a11d7e1833f612c9fe9002ec/lib/modules/versioning/maven/index.spec.ts)
classify unknown forms such as1-foo and service packs as stable. Dependabot applies
[Maven parser rules](https://github.com/dependabot/dependabot-core/blob/2e9740c209afb78cffb2c0bddf599642b527d3a9/maven/lib/dependabot/maven/version_parser.rb)
plus request/prerelease/date-like-string/ignored-version compatibility filters.
OpenRewrite [LatestRelease](https://github.com/openrewrite/rewrite/blob/a237de36a21ab75ebaf28def6825bedc978339bf/rewrite-core/src/main/java/org/openrewrite/semver/LatestRelease.java)
uses its numeric grammar, recognized prerelease exclusions and explicit metadata
patterns; [comparator upgrade](https://github.com/openrewrite/rewrite/blob/a237de36a21ab75ebaf28def6825bedc978339bf/rewrite-core/src/main/java/org/openrewrite/semver/VersionComparator.java)
retains the first equal-order eligible string through strict-greater replacement.
No one tool's unknown-qualifier, snapshot, milestone, RC, alias or tie policy becomes
libyears policy. No greatest-stable consensus or classifier-availability convention
is inferred;007-0004's unresolved product/technical questions remain.

The candidate could answer: how far apart are my version and the latest eligible
version under the POM-date surrogate used in established update tooling? That is
closer to maintenance chronology than provider-row bookkeeping, but it remains a
different question from publication age. Cooldown usefulness is evidence of an
operational purpose, not proof of accuracy for old-to-new libyears differences.
Older missing POMs, differing variant dates, uncertain staging/history and future
tool behavior make unqualified side-by-side ecosystem totals misleading.
ECOSYSTEMS.md could explain the exact field and limitation in the quoted wording;
whether that explanation is acceptable belongs to the human. No README/ECOSYSTEMS,
metric, schema or sibling change occurs here.

The authorized evidence cascade has reached its final rung. **Stop for human
selection:** accept or reject further product specification of this explicitly
conventional POM-date basis, or defer/redirect Maven age. Acceptance would change
the existing publication-only claim and require its own reviewed contract before
planning; it would not close T1 as a publication-history fact. No specification
approval, plan/tasks, implementation, provider adoption or another timestamp search
follows. A future genuinely new source may supply new authority, but none is
selected or requested now.
