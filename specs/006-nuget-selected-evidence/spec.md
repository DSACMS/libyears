# Feature 006: Bounded NuGet Selected-Version Evidence

## Status and authority

**Specification approval and next gate:** see the latest disposition in
[reviews.md](reviews.md). Written on 2026-11-03 in fresh run `006-0002`;
F1/F2 corrected in `006-0004`; human-approved H3 refinement corrected and
frozen for independent verification in `006-0015`.
This product/behavioral contract grants no permission to begin implementation.
The frozen specification is not edited to record the subsequent review verdict.

The human selected Feature 006, accepted H1–H4 and authorized this draft. The
[canonical discovery](discovery.md#human-decisions-and-reconciliation--006-0002)
retains the original questions and binding decisions. H1 selects lock-only
selection; H2 accepts conservative declarations and qualified supplier coherence;
H3 requires native NuGet package provenance plus contemporaneous producer
attestation, bound together as specified in S4, and public hash agreement; H4 accepts
first nuget.org receipt and greatest currently listed stable. No additional
consequential product question was identified by reconciliation.

## Outcome and evidence limits

A user supplies one C# project's declarations, retained lock and nonsecret
producer/supplier evidence. Libyears measures supported explicit direct
PackageReferences only when all necessary evidence is available:

```text
supported SDK-style project + packages.lock.json
  + witness binding native NuGet provenance and contemporaneous producer attestation
  -> direct PackageReference -> exact selected version
  -> authorized public nuget.org identity and matching content hash
  -> authoritative publication timestamp -> existing libyears age metric
```

This describes a supplied coherent snapshot under accepted supplier assertions.
It does not establish evaluated MSBuild completeness, installed/deployed/runtime
scope, current restore success, compatibility or cryptographic provenance.
Hashes bind bytes; they cannot prove producing history or make a false assertion
true. Conservative rejection is intentional and does not declare valid NuGet
inputs invalid in general.

The durable [OASim experiment](../../discovery/nuget-oasim.md#phase-2-resume--observed-retained-evidence)
corroborates 51 direct associations across ten separate contexts, with lock
format 1, assets format 4 and oracle format 1 agreeing. The 229 transitive
occurrences and project nodes were separate. Supplier-reported origin/hash
witnesses covered 92 selected closure identities. These are evidence for a
bounded workflow, not portfolio scope, independent resolver ground truth, live
publication fitness or promised coverage. No experiment measured package age.
Assets and package-list JSON remain useful research/oracle evidence for future
expansion; they are outside this initial product scope, without any claim that
they are unsafe in principle.

## S1 — Activation and project boundary

NuGet is explicitly activated on a directory scan by the exact option
`--nuget-project NAME.csproj`. NAME.csproj must name one immediate file in PATH,
with no directory components, absolute path, glob or list. There is no recursive
project discovery, solution traversal, implicit project choice or portfolio
aggregation. Even a sole `.csproj`, lock, assets or export does not activate
NuGet in an ordinary scan. Multiple co-located projects are allowed only because
the user explicitly selects one; their dependencies are not combined.

`--nuget-provenance NAME.json` optionally names one immediate supplied witness
in the same directory. Supplying it explicitly means the user accepts the
producer/supplier assertions in that file under S4. A file found by convention
is never implicitly trusted. Without this option, NuGet is activated but lacks
measurement authority; the failure policy in S6 applies. Witness-only activation,
repeated options, abbreviated spellings, direct-file PATH with these options,
non-filename option values or malformed/missing argument values are usage errors.
Inputs are read only within the selected root; symlink escapes are source errors.
The lock input is exactly root `packages.lock.json`; no custom lock search,
ancestor search or fallback is supported.

Existing PyPI/npm/Yarn/RubyGems sources at PATH follow their existing rules.
Python `--resolved` supplies no NuGet evidence; Ruby group options retain their
own scope. Existing direct-file scans and ordinary scans remain unchanged.
Completed empty, partial and source-error reports exit 0; usage/path errors
remain exit 1 and unexpected systemic failures exit 2. An explicitly named
missing project is a reported NuGet source error, not an absent ecosystem.

## S2 — Supported declarations and scope

The complete UTF-8 XML project must be SDK-style C#, with root `Project` and a
literal `Sdk` attribute, no XML namespace, DTD or entity declarations. SDK identity
is recorded in the supplier baseline; its imported behavior is asserted, never
loaded or evaluated. Exactly one unconditional `TargetFramework`, or one
single-valued `TargetFrameworks`, is allowed in an unconditional PropertyGroup;
both, duplicates, empty values, semicolon lists, property/item expansion and
conditional framework definitions are unsupported. A framework is one nonempty
ASCII alphanumeric/dot/hyphen identifier, beginning alphanumeric, compared
literally to the lock context. It is a context identifier, not a compatibility
interpretation. RuntimeIdentifier/RuntimeIdentifiers and RID lock contexts are
unsupported.

Supported dependencies are immediate `PackageReference` children of unconditional
ItemGroup elements, each with one literal `Include` package ID and one literal
`Version` attribute. Version child elements, absent versions, Update, Remove,
VersionOverride, aliases, property/item expansion, wildcards, semicolon identity
lists, conditions on the reference or containing groups, and generated
PackageReferences are unsupported. Allowed ancillary reference metadata is
literal `PrivateAssets`, `IncludeAssets`, `ExcludeAssets` or `GeneratePathProperty`,
as attributes or child elements, once per name. It never changes membership.
Other reference metadata is unsupported. Comments/formatting do not change scope.

Package IDs contain 1–100 ASCII letters, digits, dots, hyphens or underscores,
beginning alphanumeric. Matching is ASCII case-insensitive; preserve declared
spelling for display. Duplicate IDs, including case aliases and identical
repetitions, reject declaration scope rather than deduplicating ambiguity.

A requested version is a bare numeric literal of two, three or four dot-separated
nonnegative decimal components, each without leading zeros except `0`. Leading
or trailing whitespace is not part of supported literal values. Requests such
as `1.0`, `1.2.3`, `1.2.3.4` are inclusive minimum requests, never selected pins.
Bracket-exact `[v]`, ranges, floats, prerelease requests, metadata requests and
other forms are unsupported initially. S3 compares only the numeric minimum
bounds of this subset after documented NuGet normalization; it does not test
whether a selected version satisfies a request or evaluate general range
equivalence. This bounded request subset is narrower than NuGet's full grammar.

All supported explicit direct references count once, including test, tool,
analyzer and PrivateAssets references. They are not labeled production-only.
ProjectReference edges may be present but are neither followed nor counted;
FrameworkReference and SDK implicit/auto-referenced packages are not counted.
Unrelated literal project properties/items may be present if they do not define
or modify package membership, versions, framework, restore context or provenance.
Unknown constructs that could influence those facts reject context, including
Choose/When, Targets generating declarations, explicit imports, central package
management/PackageVersion/GlobalPackageReference and package-affecting properties.
There is no evaluation to guess which branch applies.

SDK imports and ancestor Directory.Build/Directory.Packages behavior are not
made safe merely by absence of an explicit Import. S4 requires a supplier
assertion of the relevant baseline and absence of unsupported influences. Known
contradictions reject context. Do not search ancestors, imports or SDKs to
reconstruct evaluated scope. The claim is bounded explicit declarations in
supplied inputs, not all evaluated restore dependencies.

## S3 — Lock selection and coherence

Support only `packages.lock.json` JSON schema `version: 1` (integer), with root
`dependencies` mapping and exactly one framework key equal to S2's sole literal
framework. Additional frameworks, RID-specific keys, unknown schema/semantic
fields and unsupported entry kinds reject the lock source. Duplicate JSON object
keys, including case-colliding package IDs, malformed structure and merge-conflict
content reject it; no partial salvage from a rejected lock.

Under that framework, supported entry kinds are `Direct`, `Transitive` and
`Project`. Direct entries have `type`, `requested`, `resolved`, `contentHash` and
optional `dependencies`; missing selected-version/hash values in otherwise
attributable Direct entries follow the isolated failure rules below rather
than invalidating the population. Transitive entries have `type`, `resolved`, `contentHash`
and optional `dependencies`; Project entries have `type` and optional
`dependencies`. Dependency maps contain literal IDs and string request values,
retained only as framing of closure evidence. They are never resolved or used
to add measured dependencies. A Project node cannot satisfy a PackageReference.
Transitive/project closure entries are not required to become public-authorized
or measurable merely to measure supported direct entries.

Associate a declaration only with its unique same-ID `Direct` entry in the
selected framework. The declaration remains authority for direct dependency
intent; the lock supplies selected-version evidence. For request coherence,
compare only inclusive numeric minimum bounds with no upper bound:

- Normalize the supported S2 declaration by supplying a zero patch when absent
  and omitting a zero fourth component; retain a nonzero fourth component.
- Lock `requested` must be exactly `[w, )`, where `w` is the normalized numeric
  spelling: three components, or four with a nonzero fourth, no leading zeros,
  suffixes or surrounding whitespace. This is the supported serialized form,
  not an extension of the declaration grammar to range expressions.
- Coherence requires equality of the declaration and lock numeric bounds with
  absent patch/revision treated as zero. Different bounds are a disagreement,
  even if both requests happen to select the same `resolved` version.

| Declaration request | Coherent lock `requested` |
|---|---|
| `1.0` | `[1.0.0, )` |
| `1.2.3` | `[1.2.3, )` |
| `1.2.3.0` | `[1.2.3, )` |
| `1.2.3.4` | `[1.2.3.4, )` |
| `0.0.0.0` | `[0.0.0, )` |

For declaration `1.0`, `[1.0.1, )` disagrees even when both snapshots select
`2.0.0`. For declaration `1.2.3.4`, `[1.2.3, )` disagrees. Noncanonical lock
strings such as `[1.0, )`, `[1.2.3.0, )` or `[1.2.3,)`, and unsupported forms
such as `[1.2.3]`, `(1.2.3, )`, `[1.2.3, 2.0.0)`, floating or prerelease bounds,
are request disagreements in an otherwise attributable Direct entry; no general
range interpretation or whitespace repair is promised. Non-string/missing
`requested` is malformed lock structure. Unsupported declaration forms still
reject scope under S2, regardless of lock contents.

NuGet's [lock serializer](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.ProjectModel/ProjectLockFile/PackagesLockFileFormat.cs)
writes normalized requested ranges; its
[range formatter](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Versioning/VersionRangeFormatter.cs)
and [version formatter](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Versioning/VersionFormatter.cs)
define this bounded spelling. A selected version may differ from the request;
only `resolved` establishes selection. No selection, request-satisfaction check
or shared selected outcome can replace request coherence. Preserve both original
safe request strings for output; the declaration is never a selected-version
fallback.

An extra Direct identity absent from declarations undermines whole-context
coherence and rejects the lock. A missing Direct entry, isolated request mismatch,
missing/unsupported resolved string is dependency unmeasurability after
whole-structure acceptance. A Transitive entry with the same ID does not fill a
missing Direct entry. Duplicate object identities reject the source, not just
that dependency. With one accepted framework, one case-insensitive package key
and one scalar `resolved` string, multiple candidate Direct selections for one
declaration are structurally impossible. Repeated keys (including `resolved`),
case aliases and non-string `resolved` values, including arrays/objects, are
malformed lock structure (`invalid_lockfile`); additional frameworks remain
`unsupported_lockfile_format`. An absent `resolved` remains the isolated
`lock_version_missing` case. There is no dependency-level ambiguity reason or
accepted multi-selection shape. A missing hash is isolated S4 failure
when entry identity/framing remains attributable; malformed hash strings never
authorize measurement.

Supplier evidence must bind project/framework, declaration bytes, lock bytes,
producer and input baseline to the same supplied snapshot. Wrong byte digests,
project/framework disagreement, known stale pairing and unsupported population
influences reject context. Mtime, Git presence, identical ID/version values and
restore-generation timestamps are insufficient. Libyears neither checks
locked-mode success nor updates/generates a lock.

## S4 — Supplied source authority and content identity

H3 requires two distinct, bound evidence classes:

1. **Native NuGet package provenance:** evidence from the producing dependency
   operation/context establishes the relevant package identity, selected version,
   actual supplying source/origin and content identity/hash. Retain the native
   semantics needed for the public-source and content-hash checks below. Source
   eligibility or an independently matching public package is not actual origin.
2. **Contemporaneous producer attestation:** producer-side testimony created
   during that dependency production event binds the native package provenance
   to the supplied project identity/exact bytes, lock identity/exact bytes, sole
   framework/context and required influence assertions below. It supplies the
   producer-event/context claims that native package metadata does not retain.

Together these form the supplied provenance authority. Package ID/selected
identity/hash must link native evidence to the attested event, and the attestation
must bind that event to exact project/lock bytes and framework. A digest alone
proves neither event identity nor contemporaneity. Retained producer evidence
must allow an independent audit of both classes and their linkage; native
package evidence alone or an ungrounded later envelope is insufficient.

**Replay prohibition:** a later restore may yield useful native source/hash
observations for its own event. Retrospective replay alone MUST NOT satisfy H3:
it proves neither the original event nor equivalent original semantics/context,
absence of unsupported influences, or production of the supplied historical
project/lock snapshot under the replay context. A genuinely new event may qualify
only with its own contemporaneous attestation; it cannot attest an earlier event.

The version-1 witness carries the native-derived package assertions and the
contemporaneous context attestation under explicit supplier acceptance. This is
an evidence/attestation obligation, not a requirement for libyears to authenticate
producing history, inspect native artifacts/caches or execute a producer. No new
product input format or cryptographic trust mechanism is introduced.

The explicitly accepted witness has a versioned, bounded nonsecret logical
contract. Its serialization mechanics belong to planning; these required meanings
and rejection rules may not be weakened there. Required context evidence is:

- witness contract version 1; selected project filename and sole framework;
- SHA-256 digests of exact supplied project and lock bytes;
- producer name/version and an explicit contemporaneous coherence assertion that
  the bound native package evidence, project and lock belong to that producing
  event/snapshot;
- a baseline assertion covering SDK identity/version and relevant imported,
  generated, ancestor and central inputs: supported explicit declarations are
  the complete population claimed here, with no unsupported membership/version,
  framework/RID or source influence. No private paths/configuration are required.

Each package-origin assertion binds that context and lock digest to package ID,
exact selected-version identity, and base64 SHA-512 content hash. Only an explicit
origin assertion identifying `https://api.nuget.org/v3/index.json` permits lookup.
Records for unselected/transitive packages confer no measurement authority.
A missing package record is not inferred from a blanket public default.

This contract accepts supplier testimony grounded in both evidence classes;
it does not authenticate arbitrary JSON or certify historical downloads. The
CLI must explain this trust meaning. Raw `.nupkg.metadata`, global caches,
NuGet.Config/source mapping, configured source counts, namesakes and hashes alone
are not accepted witnesses. Libyears never opens them to synthesize provenance.
Unknown, private, alternate or conflicting per-package origin yields
`unsupported_dependency_source` without any public query for that identity.
A structurally corrupt or wrongly context-bound whole witness makes the witness
source unavailable. No private source endpoint or credential is contacted.

Before using public selected-version dates, the lock hash and accepted witness
hash must agree as decoded 64-byte SHA-512 values. A local disagreement causes
`content_hash_mismatch` without lookup. After origin authorization and local
agreement, require matching ID/normalized version and matching catalog
`packageHash` with `packageHashAlgorithm: SHA512`. Public hash mismatch is also
`content_hash_mismatch`, with no measurement. Absent/unsupported hash evidence
is `content_hash_unavailable`. No package archive is fetched to repair evidence.
A matching public hash establishes content correspondence, not origin by itself.

## S5 — Public metadata, versions and metric

Public lookups use verified HTTPS nuget.org V3 metadata only. Registration must
include SemVer 2 versions and all relevant pages; partial enumeration cannot
establish latest. Supported registration listing defaults apply: absent `listed`
means listed, false means unlisted; wrong types or conflicting listing evidence
are invalid responses. Never infer listing from the availability of an archive.
The [registration contract](https://learn.microsoft.com/en-us/nuget/api/registration-base-url-resource)
defines listing defaults and its SemVer-2-capable hive.

For selected and latest versions, require identity-bound catalog PackageDetails
`created`, an aware valid timestamp normalized to UTC with supported precision.
The claim is **first receipt by nuget.org**, not original upstream release.
Missing, invalid, timezone-free, sentinel year-1900 or contradictory creation
evidence is unavailable. Never substitute catalog `published`, registration
`published`, catalog commit/update time, listing/unlisting time, restore/snapshot
time or local file times. Microsoft defines first-receipt and hash fields in the
[catalog contract](https://learn.microsoft.com/en-us/nuget/api/catalog-resource).

Latest is the greatest currently listed stable version by bounded NuGet version
precedence, regardless of framework, requested constraint, runtime, vulnerability
or compatibility. Determine the actual greatest candidate before checking its
creation date; an undated latest cannot be replaced by an older dated release.
No stable candidate yields `no_stable_release`. Missing/incomplete enumeration
or unsupported potentially eligible version syntax yields unmeasurability, not
a smaller apparently supported latest. Used prerelease/unlisted versions may be
measured when authorized content identity and creation evidence remain available.
Missing/deleted package/version records are not reconstructed from archives and
prove neither never-existence nor original publication time. Listing/record
changes can change future results; this is current public metadata.

Selected/public version syntax accepts two to four decimal numeric components
(with leading zeros permitted in evidence), optionally followed by a hyphen and
nonempty dot-separated ASCII alphanumeric/hyphen prerelease identifiers and/or
`+` with equivalent nonempty build identifiers. Missing patch/revision is zero;
leading zeros in numeric core are ignored, zero revision is omitted in normalized
display, the normalized numeric core has at least three components, and build
metadata does not distinguish package identity or precedence.
Prerelease identity matching is ASCII case-insensitive. Preserve safe original
selected spelling separately. This follows the necessary bounded differences
in [NuGet version semantics](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning).
One-component and other legacy spellings remain unsupported in this feature.

Stable means no prerelease suffix. Stable ordering compares the four numeric
components as integers, not strings or dates; e.g. `1.10.0 > 1.9.0`, and
`1.0.0.1 > 1.0.0`. Build labels do not change stable ordering. No ordering among
prereleases is needed: they are excluded from latest and used only for exact
normalized identity. Equivalent duplicate public identities may collapse only
when material hash, listing and creation evidence agrees; conflicting aliases
are invalid responses, never arbitrary tie-breaking. No generic semver framework,
range evaluation or NuGet resolver is promised.

Metric semantics are unchanged: `(latest_created - used_created) / 365.25 days`,
no grace period; used identity equal to latest gives exactly `0.0`. Negative
values from anomalous timestamp ordering are clamped to zero and flagged under
the existing metric contract. Numeric summaries use measured rows only.

## S6 — Failure and availability contract

Whole-source failure records are `source_errors` with ecosystem `nuget`, safe
input filename and stable reason. They do not create fabricated package failures.
Known-dependency failures are `unmeasurable` rows with identity, safe declared
request, established evidence and reason. No local failure permits lookup.

| Condition | Level / stable reason |
|---|---|
| Explicit project missing | Source / `nuget_project_missing` |
| Unreadable, unsafe, malformed or non-UTF-8 project | Source / `invalid_nuget_project` |
| Unsupported project/context/declaration syntax or input limit | Source / `unsupported_nuget_project` |
| Duplicate declaration identity | Source / `duplicate_nuget_declaration` |
| Lock missing | Source / `lockfile_missing` |
| Unreadable, unsafe, malformed lock or duplicate JSON identities | Source / `invalid_lockfile` |
| Unsupported lock schema/context/semantic fields or input limit | Source / `unsupported_lockfile_format` |
| Extra Direct population, wrong project/framework binding or stale byte binding | Source / `nuget_context_mismatch` |
| Witness option/file absent | Source / `nuget_provenance_missing` |
| Unreadable, unsafe, malformed, unsupported or over-limit witness | Source / `invalid_nuget_provenance` |
| Known unsupported influence asserted by witness | Source / `unsupported_nuget_project` |
| Missing matching Direct lock entry | Dependency / `lock_dependency_missing` |
| Isolated request disagreement under S3's bounded normalized-minimum comparison | Dependency / `declaration_lock_requirement_mismatch` |
| Missing selected version | Dependency / `lock_version_missing` |
| Unsupported selected syntax | Dependency / `unsupported_lock_evidence` |
| Missing/unknown/private/alternate/conflicting package origin | Dependency / `unsupported_dependency_source` |
| Missing, invalid or unsupported hash evidence | Dependency / `content_hash_unavailable` |
| Local or authorized-public hash disagreement | Dependency / `content_hash_mismatch` |
| Authorized public package / used version absent | Dependency / `package_not_found` / `version_not_found` respectively |
| Missing usable used or actual latest creation timestamp | Dependency / `release_date_missing` |
| Complete enumeration with no listed stable | Dependency / `no_stable_release` |
| Malformed/conflicting public identity, classification, pagination or unsupported candidate | Dependency / `invalid_registry_response` |
| TLS/transport/timeout/service/rate-limit or request-budget exhaustion | Dependency / `registry_error` |

Precedence is project availability/complete scope, whole-lock acceptance, whole
witness/context acceptance, then local association, origin, local hash, registry
structure/identity, public hash, used-version availability/date, and latest/date.
Malformed whole structure takes precedence over unsupported structure in the
same input. Report the earliest applicable stage, independent of input iteration
order; do not invent errors for unprocessed later sources. Within association,
missing Direct precedes request mismatch, missing version and unsupported
version. Structural duplicate/multi-value failures are whole-lock failures,
never a later dependency ambiguity stage. Public absence is identified before
hash/date validation of an absent record. Unsupported origin always prevents public lookup even if
another failure would take display precedence.

| Availability | NuGet summary |
|---|---|
| Not activated | NuGet entirely absent from rows, evidence and summaries |
| Project/context cannot establish supported explicit population | discovered=null, measured=null, coverage=null; numeric aggregates null |
| Complete declarations establish N, but lock/witness source unavailable | discovered=N, measured=null, coverage=null; numeric aggregates null |
| Accepted evidence, individual failures | discovered=N, measured=M; coverage=M/N for N>0; numeric aggregates from successes |
| Supported empty declarations and accepted context/lock/witness | discovered=0, measured=0, coverage=null, total=0.0; other aggregates null |

Unsupported known membership influences invalidate the denominator. Missing
selection/witness alone does not erase independently established bounded explicit
declarations. Even known N=0 with a rejected required source remains measurement
unavailable, distinct from validated empty evidence. With accepted sources and
N>0, all individual failures give M=0 and coverage=0.0. Never reinterpret whole
source unavailability as 0% coverage.

Repository discovered count is null if any activated source denominator is
unknown. Coverage is null if any source is measurement-unavailable. Measured
count is null only if every detected source is unavailable; otherwise it counts
successful rows, including zero. Repository numeric aggregates always retain
available rows (total=0.0 and other aggregates=null if none). Sibling sources,
rows and their per-ecosystem summaries survive NuGet failures. No-source behavior
is unchanged. Identity is `(ecosystem, case-insensitive NuGet ID)` for NuGet;
identically named packages in different ecosystems remain separate.

## S7 — Public output

Retain schema version 3, top-level direct scope and existing fields/meanings.
NuGet adds ecosystem key `nuget` only when activated. Measured rows have
`ecosystem: nuget`, `version_source: packages_lock`, existing name/version/date/
libyears fields, and `nuget_evidence`. Unmeasurable rows retain existing `name`,
`declared` and `reason` and add the same evidence object for safely known facts.
`declared` is the safe package ID followed by its numeric request in parentheses,
not arbitrary XML. Source errors retain only existing ecosystem/source/reason
fields. Diagnostics remain human-only; verbose JSON has identical content.

`version_evidence.nuget` always contains `declaration_source` (selected filename),
`snapshot_source: packages.lock.json`, `provenance_source` (selected witness
filename or null if not supplied), `scope: explicit_direct_packagereference`,
`format` (`packages_lock_v1` only after whole-lock acceptance, otherwise null),
`framework` (supported literal once established, otherwise null),
`trust_basis: supplied_producer_assertion`, and
`publication_basis: nuget_org_first_receipt_created`. These identify the requested
claim, not a claim that all rows passed it.

Per-row `nuget_evidence` has the following additive fields:

| Field | Presence and meaning |
|---|---|
| `project`, `framework`, `requested` | Always present on a known dependency; safe declaration/context values |
| `lock_requested` | Present only when safe request text is established in an accepted matching Direct entry, including a mismatch |
| `selected_version` | Original safe resolved spelling, only after unique successful request/Direct association |
| `normalized_version` | Supported normalized selected identity, only after its syntax validates |
| `selection_source` | `packages.lock.json`, only with associated selected version |
| `origin_state` | Always one of `unavailable`, `unsupported`, `asserted_public`, `public_content_verified`; never a private URL |
| `content_hash_state` | Always `unavailable`, `mismatch`, `local_agreement` or `public_agreement` |
| `publication_basis` | Always `nuget_org_first_receipt_created` |
| `used_publication`, `latest_publication` | Present only when established: objects with normalized `version`, UTC `created`, and `listed` boolean |

Fields not established are omitted except explicitly specified nulls; no
mismatch row claims exact selected provenance. `public_content_verified` requires
all S4 checks; `asserted_public` alone does not imply public date authority.
Do not expose raw witness content, producer-local paths, baseline details,
private endpoints, hashes or arbitrary source lines in either output. Context
fingerprints may be retained internally but are not required public fields.

Human output names the selected project/framework, declaration/lock/witness
filenames, all-direct test/tool-inclusive scope, snapshot/supplier limitations,
first-receipt date claim and listed-stable comparator. It explains missing,
unsupported, mismatch, authority and metadata failures with safe text, shows
known requested/selected values where established, and distinguishes unavailable
coverage from zero and empty populations. It agrees with JSON on identities,
counts, reasons, dates, values and evidence states. Existing metric anomaly
flags remain visible. Ordinary reports without NuGet preserve their established
output; no extra warnings are introduced there.

## S8 — Resource and security boundaries

Libyears MUST NOT execute dotnet, NuGet, MSBuild, target/repository code or any
package manager; restore/install packages; resolve graphs; evaluate targets,
conditions or imports; fetch package archives; inspect caches, credentials or
private source configuration; traverse ProjectReference content; or write inputs.
Python 3.11+ and standard library only remain mandatory. Registry network access
stays behind an adapter interface. Deterministic tests use fixtures/mocks offline.
External producers may create inputs separately under their own authority;
that never grants execution permission to libyears.

Input bytes, XML/JSON depth, element/entry/string counts, numeric component
lengths, response/compressed-expansion bytes, pagination, request counts, retries
and timeouts must have finite enforced bounds. Numeric limits and transport
mechanics belong to planning and must be documented and fixture-verifiable.
Exceeding local bounds rejects the affected whole source without partial scope;
public response/expansion/structure limits yield `invalid_registry_response`,
request/time budgets yield `registry_error`. No unbounded catalog history crawl
or filesystem search is permitted. Limits cannot silently truncate latest.

Only approved public nuget.org metadata authorities may be contacted. Service
index resources, catalog links and redirects require verified HTTPS, approved
hosts/path purposes and no embedded credentials; arbitrary linked/private URLs,
HTTP downgrade, local addresses and TLS bypass are prohibited. Do not follow
source URLs supplied by untrusted artifacts to discover authority. Planning
must enumerate the narrow metadata destinations; it cannot add private-feed or
archive access. Honor rate limits/Retry-After within finite budgets or fail;
no alternate-host evasion. Identical fixed inputs/responses must yield the same
result regardless of ordering. Unsafe/nonregular/replaced input files must
fail closed without escaping the root or blocking on special files.

## Acceptance criteria

Each criterion is a stable, independently testable obligation for later review
and implementation. None is marked satisfied by drafting this specification.

- [ ] **AC-01:** Exact NuGet project activation selects one root C# project; ordinary scans with co-located .NET artifacts remain unchanged and omit NuGet.
- [ ] **AC-02:** Witness-only, repeated/abbreviated/malformed options, direct-file activation and non-filename values fail with exit 1; explicit missing project reports a source error with exit 0.
- [ ] **AC-03:** A supported project with one TargetFramework or single-valued TargetFrameworks establishes its explicit direct population and literal context.
- [ ] **AC-04:** Multiple/conditional/computed/duplicate frameworks, RID declarations and unsupported SDK-style/XML context reject scope without partial counting.
- [ ] **AC-05:** Supported unconditional Include/Version references count test/tool/analyzer/PrivateAssets dependencies once; ProjectReference, FrameworkReference and implicit packages do not count or cause traversal.
- [ ] **AC-06:** Two-, three- and four-component bare numeric requests retain inclusive-minimum meaning; S3's examples accept omitted-patch and zero-revision normalization while preserving nonzero revision. Ranges, bracket-exact, floats, property expansion and prerelease declarations still reject scope without guessed pins.
- [ ] **AC-07:** Duplicate or case-aliased declarations reject scope; conditional/generated/imported/CPM/Update/Remove/VersionOverride or unknown package-affecting constructs fail closed.
- [ ] **AC-08:** Lock schema 1 with exactly matching sole framework supports Direct/Transitive/Project framing; no transitive/project row supplies measured membership.
- [ ] **AC-09:** Unsupported schema, extra framework/RID, unknown semantic fields, malformed structure and duplicate JSON identities reject the whole lock, preserving independently known N.
- [ ] **AC-10:** A unique same-ID Direct with S3's coherent normalized numeric minimum yields the retained resolved version, including a version differing from its request. All five positive S3 examples associate; different minimum bounds never associate merely because their selected outcome agrees. No resolution or satisfaction check occurs.
- [ ] **AC-11:** Missing Direct, S3 request disagreement (including its negative examples), absent selected value and unsupported selected string syntax use their specified individual reasons without lookup or transitive fallback. Duplicate/case-aliased keys and non-string selections reject the whole lock as invalid_lockfile; additional frameworks use unsupported_lockfile_format, never a dependency ambiguity reason.
- [ ] **AC-12:** Extra Direct identities, project/framework disagreement and stale project/lock digest bindings reject context; mtime and Git presence cannot repair it.
- [ ] **AC-13:** Explicitly supplied version-1 witness binds native producer-time package ID/selected version/actual origin/content hash to contemporaneous producer attestation of exact project/lock bytes, framework and required producer/baseline assertions. Independently retained event evidence must substantiate both classes and their binding; native evidence alone or retrospective replay alone does not satisfy H3. A found-but-unselected witness confers no authority.
- [ ] **AC-14:** Missing/rejected whole witness produces unavailable-source behavior; a known unsupported membership influence also invalidates the denominator.
- [ ] **AC-15:** Missing/unknown/private/alternate/conflicting per-package origin produces unsupported_dependency_source and zero requests for that identity, even with a matching public namesake.
- [ ] **AC-16:** A blanket public switch, configured source list, source mapping, cache marker or ID/version/hash alone cannot authorize public lookup. Later replay source/hash evidence cannot substitute for the original event's contemporaneous producer attestation, even when supplied historical project/lock bytes match.
- [ ] **AC-17:** Local lock/witness SHA-512 disagreement prevents lookup and yields content_hash_mismatch; invalid/missing hashes yield content_hash_unavailable.
- [ ] **AC-18:** Authorized origin/local agreement permits public metadata lookup, but measurement requires public catalog ID/version and SHA512 hash agreement; public mismatch or missing hash is unmeasurable.
- [ ] **AC-19:** Selected and latest dates use identity-bound catalog created as first nuget.org receipt; listing, catalog commit/update, restore and snapshot times never replace it.
- [ ] **AC-20:** Missing/invalid/naive/sentinel/conflicting created for used or actual latest yields release_date_missing or invalid_registry_response for structural conflicts, with no older-candidate fallback.
- [ ] **AC-21:** Complete SemVer-2-inclusive current enumeration chooses greatest listed stable by numeric precedence; prereleases/unlisted candidates are excluded and listing defaults follow S5.
- [ ] **AC-22:** Incomplete pagination, unsupported potentially eligible versions and conflicting duplicate public identities cannot yield partial latest; complete absence of listed stable yields no_stable_release.
- [ ] **AC-23:** Authorized unlisted/prerelease used versions remain measurable with matching content and usable created; missing public package/version uses the specified absence reasons without archive reconstruction.
- [ ] **AC-24:** Supported normalization handles leading numeric zeros, omitted patch/zero revision, nonzero fourth components, case-insensitive prerelease identity and ignored build metadata; stable ordering is numeric and independent of dates/framework/requests.
- [ ] **AC-25:** Metric uses 365.25 days, exact zero for used=latest, flagged negative-date clamping and measured-only aggregates; no grace or compatibility filter is introduced.
- [ ] **AC-26:** Missing/unsupported project gives unknown denominator; missing/rejected lock with known declarations preserves N but gives null measured/coverage, no fabricated N package failures.
- [ ] **AC-27:** Accepted nonempty scope with individual failures uses M/N including 0%; validated empty and source-unavailable states remain distinct, with S6 null/zero aggregates.
- [ ] **AC-28:** Mixed scans preserve sibling ecosystem identities, sources, rows, evidence and summaries through NuGet failure; repository counts/coverage/available-row aggregates follow S6.
- [ ] **AC-29:** Schema v3 adds only specified NuGet evidence, with deterministic presence/null/omission and safe partial evidence; ordinary reports remain compatible and verbose JSON unchanged.
- [ ] **AC-30:** Human and JSON reports agree on scope, identity, requests/selections, context, authority/hash states, publication dates, failures and aggregates; human output explains accepted supplier limitations.
- [ ] **AC-31:** Every retained source/dependency reason has a reachable S6 trigger and deterministic precedence under reordered inputs/responses. S3 structural duplicates/multi-value selections reject the whole lock before dependency association; no ambiguous_lock_evidence result, unprocessed-source error or exact-selection claim on request mismatch is fabricated.
- [ ] **AC-32:** No product path executes dotnet/NuGet/MSBuild/target code, restore/install/resolution or reads cache/config/credentials; scans leave target bytes unchanged and deterministic tests are offline.
- [ ] **AC-33:** Input size/depth/count/numeric limits and unsafe/nonregular/replaced-file cases fail closed, bounded in work, without partial scope or root escape.
- [ ] **AC-34:** Public metadata transport enforces HTTPS authority/redirect restrictions, finite pagination/byte/expansion/request/time/retry bounds and rate-limit handling; no private endpoint, archive or unbounded history fallback occurs.
- [ ] **AC-35:** Neither output discloses credentials, private source details, unsafe paths, raw witness/config/XML text or hashes; safe filenames and bounded identity/context evidence remain readable.
- [ ] **AC-36:** Assets/package-list exports, packages.config, general imports/CPM, conditionals, multiple frameworks/RIDs, private feeds and portfolio aggregation cannot supply fallback measurement evidence.

## Author self-audit and next gate

Author audit against discovery, H1–H4, the durable OASim summary, Feature 004/005
availability/output principles and the existing metric found no new consequential
product question. H1 maps to S1/S3; H2 to S2/S3/S6; H3 to S4/S8; H4 to S5.
The draft fixes activation, trust acceptance, public fields/reasons and bounded
version behavior for independent review. It preserves supplier-testimony limits,
source/dependency failure separation and sibling compatibility.

Checked exclusions: no assets or package-list product input, CPM/general-import
interpretation, conditional references, multiple frameworks/RIDs, transitive
measurement, private feeds, dotnet/NuGet execution, portfolio aggregation or
metric change. Public semantics were narrowly rechecked against the linked
Microsoft version, registration and catalog references on 2026-11-03; no live
package-age or yield claim was made. No external checkout/raw temporary experiment
was accessed. No product code/tests, plan or tasks were changed or created.

The `006-0004` correction audit preserves H1–H4, the exclusions and all 36 AC
identifiers; only F1/F2 association/failure obligations and their acceptance
wording changed. This self-audit is not independent approval. The latest disposition and next gate are recorded in [reviews.md](reviews.md).
Technical planning and implementation remain unstarted.


### H3 refinement self-audit — 006-0015

The human approves the two-class H3 model and replay prohibition above. Stable
AC-01–36 identifiers remain; only AC-13 and AC-16 wording changes. S4 defines
native package provenance separately from contemporaneous producer testimony,
their package/event/byte/context binding and the independently auditable replay
negative. No new serialized field or consumer history-authentication claim is
implied. S1 explicit acceptance and S3 lock selection/coherence remain intact.

All 36 obligations were re-audited: AC-01–12 preserve activation, bounded scope,
F1/F2 and lock association; AC-13/16 express the refinement; AC-14/15/17/18 retain
source availability, no namesakes and local/public hash gates; AC-19–24 preserve
H4 dates, enumeration and version semantics; AC-25–30 retain metric, coverage,
sibling compatibility and output; AC-31–36 retain reasons, P1/no-resolution,
limits, privacy and exclusions. H1/H2/H4 and all closed findings are unchanged.
This audit is not independent approval or new executed acceptance evidence.

Historical OASim lacks the required contemporaneous attestation. The
[006-0013 preflight](validation-006-0013.md) correctly left T016 incomplete.
[006-0014](producer-evidence-006-0014.md) demonstrates useful isolated native
source/hash retention, not equivalence to OASim's historical producer context;
its overall blocked result remains the negative empirical replay witness.
OASim cannot become retrospectively conformant by relabeling that replay.
Approval and downstream disposition belong in reviews.md after independent review.
