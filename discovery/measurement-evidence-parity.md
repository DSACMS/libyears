# Cross-ecosystem measurement-evidence parity — 006-0023

## Decision and authority

**Discovery candidate; HUMAN PRODUCT / TRUST-BOUNDARY DECISION.** Independent
review disposition belongs in [the review record](measurement-evidence-parity-review.md).
Fresh repository-grounded investigation at published
`1ba915f73af81164330ef2355101e5244c21932f`, initially clean. This is prospective
product discovery, not a correction of historical Feature 006 authority.

**Finding:** NuGet combines a necessary selection/context/source problem with
a stronger historical acquisition/content-provenance contract. The latter is
not inherently necessary for a package-version publication-age measurement.
Recommend a minimum measurement H3: accepted, attributable project/lock snapshot
selection plus package-specific public namespace/history authority; retain
bounded context validation and authoritative dates. Historical producer-event
and content correspondence assurances should not be mandatory for that claim.
This recommendation changes the trust boundary and requires human approval.

Nothing here weakens current H3, changes runtime/schema/metric/parser/source
policy, implements an assurance tier, or alters original Feature 006 records.
Published behavior truthfully implements its approved stronger contract.

## Evidence basis and distinctions

The product foundation is [SPEC §§2,4–10,22,25](../SPEC.md): “used” means exact
version established from supported repository evidence, not installed/deployed
state or a new resolution. Current extensions are governed by Features
[002](../specs/002-npm-support/spec.md),
[003](../specs/003-yarn-lock-evidence/spec.md),
[004](../specs/004-rubygems-support/spec.md),
[005](../specs/005-gemfile-group-scope/spec.md),
[006](../specs/006-nuget-selected-evidence/spec.md) and the
[repository-source correction](../maintenance/nuget-repository-sources/spec.md).
Their plans, tests, retrospective and review evidence explain implementation and
historical disposition; old draft status paragraphs do not override later approvals.

Keep four levels separate:

1. **Actual enforcement:** parsers, association, authority gates and adapters below.
2. **Durable obligation:** accepted artifact meanings, including supplier testimony
   that code cannot independently authenticate.
3. **Package-manager capability:** documented artifacts can retain more facts than
   libyears consumes; their existence does not make those facts product requirements.
4. **Stronger assurance:** exact acquisition history, artifact correspondence,
   evaluated build completeness and reproducible restore are distinct claims.

Claim A is: **this accepted source snapshot records direct package P at V**.
Claim B is: **these exact bytes came from R in this historical production event**.
A needs attributable selection and applicable namespace. B additionally needs
content and historical-event evidence. Neither an arbitrary JSON assertion nor
a matching digest authenticates a historical event. Current NuGet accepts testimony
about B and checks bindings/content; it does not independently prove B.

## Current implementation matrix

“Required” below means on the production path before a measured row. Registry
success is also required; accepted local evidence alone never produces an age.
Ruby columns describe ordinary all-direct locks; scoped Feature 005 differences
follow. NuGet describes both explicit and ordinary source modes unless stated.

| Evidence / claim | PyPI / Python | npm, including Yarn Classic | RubyGems / Ruby | NuGet |
|---|---|---|---|---|
| Dependency identity | requirements name; lowercase and collapse `-_.` | Full manifest key including scope; exact lock path/selector | Exact case-sensitive direct/spec name; registry may differ only in ASCII case | Literal bounded ID; ASCII case-insensitive association; safe original spelling |
| Directness | Entries in root requirements.txt are treated as direct | Root dependencies minus names in optionalDependencies; no dev-only/peer-only/workspace/transitive scope | Lock DEPENDENCIES, all groups uninterpreted | Supported explicit unconditional PackageReferences, including tests/tools/analyzers/PrivateAssets; no implicit/project/transitive rows |
| Selected/used version | Exact `==` declaration; or accepted supplied freeze entry for supported non-exact declaration | package-lock v2/v3 root node_modules/name version; or one exact Yarn selector match with concrete version | Supported source spec(s) for direct name, all agreeing on version text | Matching framework Direct entry's resolved, never bare numeric project request |
| Selection association | Normalize name; snapshot conflict and supported constraint validation; exact declaration may stand alone | Exact pins must equal lock version; general ranges not evaluated; Yarn matches full name@declaration | Exact direct/spec association; ordinary requirement satisfaction not checked | Whole project/lock acceptance; same ID/Direct; normalized numeric request-minimum coherence; no range resolution |
| Repository/source association | Root requirement artifact; supplied snapshot need not be byte/event bound | Co-located root manifest/lock; no byte/event binding | Root lock itself; no proof it is committed/build-consumed | Exact project/lock SHA256, project filename, framework and accepted coherence/baseline witness; ordinary source_id identifies project occurrence |
| Public registry identity | Fixed PyPI adapter; excludes recognizable URL/VCS/local declarations; no positive origin evidence | Fixed public npm adapter; excludes recognizable nonregistry declaration forms and link entries; ignores lock resolved URL/integrity as origin proof | Every relevant spec source must have singleton literal public rubygems.org GEM remote; private/GIT/PATH/multiple-remotes/`!` cannot use public namesake | Explicitly accepted package-specific singleton canonical nuget.org origin assertion, context/ID/version/hash bound; no public query without LocalAuthority |
| Selected publication date | Earliest usable upload timestamp for exact public version, including yanked files | Exact public version exists and usable time[version] | Earliest admissible creation across supported observable generic/platform artifacts for exact version; import-day exclusion; no built_at | Identity-bound public catalog created, first nuget.org receipt; local/public hash gates first; no listing/update/restore-time substitute |
| Latest eligible stable | Newest canonical date, heuristic prerelease exclusion; reject all-usable-files-yanked candidates | Newest dated canonical stable SemVer; latest tag only breaks date ties; deprecation not exclusion | Newest canonical date with available nonprerelease supported artifact; lexical date-tie break; no runtime/platform filter | Greatest numeric stable precedence among complete currently listed SemVer2-inclusive registration; no compatibility/request filter |
| Latest publication date | Same earliest-upload rule | Same time mapping | Same canonical observable creation rule | Catalog created for actual greatest listed stable; missing date does not select an older candidate |
| Content hash required | No | No, including no public integrity agreement | No; CHECKSUMS section actually outside supported lock grammar | Yes: decoded 64-byte SHA512 lock/witness equality before lookup, selected catalog SHA512 equality before dates |
| Contemporaneous producer attestation | No | No; Yarn header recognizes format, not event | No; BUNDLED WITH is not event attestation | Required by S4/AC13/16; explicit testimony acceptance; chronology/native-event truth not authenticated by parser |
| Lock/freeze/snapshot | Exact requirement sufficient; --resolved supplies optional narrow pip_freeze_exact artifact | Supported package-lock or Yarn v1 required even for exact declarations; both present reject source | Supported Gemfile.lock required; ordinary scan ignores Gemfile | Schema1 packages.lock.json plus supported project plus explicitly accepted witness required |
| Network | PyPI metadata after candidate accepted | Public npm metadata after candidate accepted | Public identity and bounded versions metadata after local authorization | One supervised public metadata batch after per-package local authority; complete registration and needed catalog leaves; no archives |
| Unavailable evidence | Known declaration without version/date becomes individual unmeasurable; missing root requirements means absent source | Missing/malformed package-lock normally individual failures with known N; rejected Yarn/both-lock conflict is whole-source unavailable, N retained; invalid manifest N unknown | Rejected ordinary lock makes N unknown; isolated spec/source/date failures retain N | Unsupported project/influences N unknown; missing/rejected whole lock/witness retains independently known N but M/coverage/numerics null; individual failures only after whole acceptance |
| Partial-coverage denominator | Discovered requirement identities, not freeze-only extras | Known in-scope manifest set | Accepted direct lock set (or established selected Gemfile declarations in scoped mode) | Per-project supported direct occurrences; same ID across projects counts repeatedly; unknown population anywhere makes combined N/coverage unknown; unavailable source makes coverage null; successful siblings survive |

Implementation anchors: [requirements.py](../libyears/requirements.py),
[snapshot.py](../libyears/snapshot.py),
[scan._python_source_result / composition](../libyears/scan.py),
[npm discovery, selection and adapter](../libyears/npm.py),
[Yarn parser](../libyears/yarn.py),
[Ruby source authorization](../libyears/rubygems.py),
[Ruby registry](../libyears/rubygems_registry.py),
[NuGet association](../libyears/nuget.py),
[provenance gate](../libyears/nuget_provenance.py),
[public hash/date gate](../libyears/nuget_registry.py),
[ordinary sources](../libyears/nuget_sources.py).

Python directness is an input convention, not proof that a requirements file
contains no compiled/frozen transitives. A supplied freeze is intersected with
declarations; freeze-only entries do not expand scope. Libyears neither proves
PyPI supplied the installation nor binds freeze bytes to an install event.

Scoped Ruby requires complete supported Gemfile group declarations, public
Gemfile source, direct lock identity and identical requirement text, then ordinary
lock source authorization. Feature 005 S3 explicitly disclaims historical
coherence from equal names/requirements. Missing lock with known selected names
is individual failure; rejected lock is unavailable. That differs deliberately
from NuGet missing-witness policy, not from metric arithmetic.

Python/npm do **not** establish positive public origin. Private packages sharing
public P/V can receive public dates under today's accepted forms: Python does
not inspect index configuration; npm does not consult lock resolved/integrity
for authority. This is a real namespace-attribution limitation, not evidence
those packages in any inspected repository are private. Ruby's explicit lock
remote is the closest sibling precedent for positive namespace authority.
Parity must not copy Python/npm's weaker source assumptions into NuGet.

## Ecosystem facts versus necessity

Official pip documentation says freeze reports installed packages rather than
computing a solver result. Libyears accepts the narrow text, not authenticated
producer history. [pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/).

npm documents path-keyed package records, resolved locations and integrity.
Those fields can support stronger checks; libyears currently uses selected
version/path and ignores those origin/content fields for this purpose.
[npm lock reference](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/).

Ruby's lock format separates source blocks, selected specs, platforms and direct
DEPENDENCIES. That permits attribution without a contemporaneous Bundler witness;
libyears accepts only its documented bounded subset, not every modern format.
[RubyGems lock guide](https://guides.rubygems.org/gemfile-lock/).

NuGet locks persist project dependency closure by framework. A library lock does
not determine a consuming application's resolved versions. A bare project version
is a request; lock resolved records selection. Locks are not actual-source/event
certificates. Project identity, request/context association and qualified scope
still matter. [Microsoft PackageReference/locks](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files#locking-dependencies).

NuGet source mapping constrains eligibility, not necessarily actual acquisition;
cached packages bypass lookup and several sources may contain the same identity.
That prevents treating configuration or public-name coincidence as origin proof.
It does not establish that an age measurement must prove historical origin.
[Microsoft source mapping](https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping).

Catalog created describes first receipt by that registry; published describes
listing history. Applicable public namespace plus identity-bound created supports
a **public package-version date**. Hash equality is additionally needed for
the current **content-correspondence** claim, not for reading the public identity's
date. [Microsoft catalog](https://learn.microsoft.com/en-us/nuget/api/catalog-resource).

Thus NuGet is fundamentally different in static project evaluation/context and
available source fields, but not uniquely different in needing age evidence.
Imports/SDK/CPM/conditions/RIDs must not disappear from the completeness analysis.
Project-local snapshot ages and consuming-application resolution are distinct.
The same restraint applies to sibling lock snapshots versus deployed versions.

## How Feature 006 reached H3

| Durable stage | What it establishes / limit |
|---|---|
| Pre-selection OASim discovery and blocked Phase2 | Minimum requests were insufficient; initial producer failure established no selections. |
| Phase2 resume | Shared NuGet-produced assets/experimental locks/oracle agreed on 51 direct occurrences, 229 transitive occurrences, 15 project nodes; 92 closure identities had separate native source/hash records. Corroboration, not independent resolvers or age measurements. |
| 006-0001/0002 | Discovery recommended lock-only selection, bounded snapshot/coherence, bound origin plus public hash, and first-receipt/listed-greatest policy. Human H1–H4 accepted them. |
| 0003–0007 | F1 normalized supported request minima; F2 removed impossible individual ambiguity; P1 added enforceable in-flight deadlines; plan/task reviews retained H3. Hash-domain fitness already recorded as unverified, not a defect waiver. |
| 0008–0012 | K1 lock bounds, T008 positive worker-entry witness, Windows fixture/capability separation, K2 alias-material checks and K3 argument privacy corrected. K4 covered 36 obligations; no live useful yield established. |
| 0013 | Ten locks framed; only two supported projects, three references, no accepted supplied witnesses; validation incomplete. |
| 0014 | Isolated replay retained useful native origin/hash facts but failed original-context authority precondition. Overall D/BLOCKED and execution deviation remain; not historical provenance. |
| 0015 | Human explicitly refined H3 into native producer-time provenance PLUS contemporaneous attestation; replay cannot attest original context even with identical project/lock bytes. Parser already accepted testimony; no chronology-authentication implementation introduced. |
| 0016/0017 | New controlled original-root event captured both evidence classes; local hashes agreed, public catalog hash disagreed. 0/1 measured, content_hash_mismatch, no row age. Required failure-path validation and 36/36 convergence approved; retrospective closed. Cause/general hash-domain fitness unresolved. |
| 0018–0020 | Operational/portability/security and bounded human root recognition maintenance did not weaken evidence. Recognition reduced absence confusion, not measurement gates. |
| 0021 | Separated source occurrence weighting/output from discovery; ten projects/51 raw references did not authorize N=51. Human population decision required. |
| 0022 / published baseline | Human approved independent per-project occurrences; bounded automatic attempts and explicit witness mappings implemented/converged. Eight unknown populations, two known N=1/N=2 with missing accepted testimony remain. H3 unchanged. |

Sources: [pre-selection history](nuget-oasim.md),
[006 discovery/decisions](../specs/006-nuget-selected-evidence/discovery.md),
[complete review chronology](../specs/006-nuget-selected-evidence/reviews.md),
[0014 experiment](../specs/006-nuget-selected-evidence/producer-evidence-006-0014.md),
[0016 validation](../specs/006-nuget-selected-evidence/validation-006-0016.md),
[retrospective](../specs/006-nuget-selected-evidence/retrospective.md),
[0021 discovery](nuget-repository-sources.md),
[0022 validation](../maintenance/nuget-repository-sources/validation.md).
These are retained observations, not new reproductions of old experiments.

The conclusion is a combination: genuine ecosystem constraints, deliberately
approved stronger guarantees, and historical over-specification **relative to
the newly stated product north star**. It was not accidental runtime drift or
dishonest implementation. Cross-artifact conformance review could correctly
approve H3 without settling whether its stronger claim was product-essential.

## Claim-by-claim necessity test

Classifications below concern the proposed snapshot/public-version-age claim.
Every current H3 obligation remains mandatory until replaced by human authority.

| Current requirement | Exact claim lost if removed without replacement | Necessity / proposed treatment |
|---|---|---|
| Contemporaneous producer attestation; replay prohibition | Original-event chronology and linkage to that historical producing baseline | **REQUIRED ONLY FOR STRONGER SUPPLY-CHAIN/REPRODUCIBILITY CLAIM.** Later accepted snapshot testimony can support A; never relabel it original-event proof. |
| Native NuGet provenance | Actual supplying source/content derived from the producing operation, rather than accepted namespace association | **REQUIRED ONLY FOR STRONGER SUPPLY-CHAIN/REPRODUCIBILITY CLAIM** as a mandatory evidence mechanism. It is useful source evidence, but not the only way to accept applicable public namespace. Removing it alone under current B leaves origin unsupported. |
| Public selected SHA512 equality | Selected content corresponds to catalog content identity | **REQUIRED ONLY FOR STRONGER SUPPLY-CHAIN/REPRODUCIBILITY CLAIM**; also defense in depth against substituted P/V. Not necessary for public P/V date once applicable namespace is independently established. Hash disagreement does not itself identify a private fork or explain cause. |
| Lock/witness local SHA512 equality | Witness content assertion refers to locked content | **DEFENSE-IN-DEPTH BUT NOT MEASUREMENT-ESSENTIAL** for A with bound selected P/V; essential to the existing content chain. Never call unequal hashes verified. |
| Exact project/lock byte binding | External testimony demonstrably applies to these supplied bytes, rather than another pair | Association is **REQUIRED FOR SELECTED-VERSION CLAIM**; exact-byte digests are **DEFENSE-IN-DEPTH BUT NOT MEASUREMENT-ESSENTIAL** as the universal mechanism. Retain them for supplied NuGet testimony: inexpensive, already implemented, prevent accidental stale/mixed binding. They do not prove history. |
| Framework/context binding | Selection corresponds to the source context being measured | **REQUIRED FOR SELECTED-VERSION CLAIM.** Keep sole matching framework and project association; never combine contexts or infer consumer resolution. Event timing is separate. |
| Package-specific actual public-origin assertion | Actual historical supplying endpoint | Actual acquisition is **REQUIRED ONLY FOR STRONGER SUPPLY-CHAIN/REPRODUCIBILITY CLAIM**. Applicable public namespace is **REQUIRED FOR PUBLIC-REGISTRY IDENTITY** and hence publication attribution. Replace actual-origin testimony only with explicit package/context-bound namespace authority, never name coincidence. |
| Complete explicit population / no unsupported membership/version/framework/RID influences | Claimed denominator and association are supported within the bounded static source | **REQUIRED FOR SELECTED-VERSION CLAIM / OTHER: denominator truthfulness.** Keep conservative parsing and qualified accepted completeness/context assertions; no evaluated-completeness promise. They need not be contemporaneous to describe accepted snapshot scope. |
| SDK identity/version and producer name/version | Exact producer/baseline identified for historical reconstruction | **OTHER:** SDK identity/context may matter to supported scope; exact tool-version inventory is principally stronger reproducibility/audit evidence. Not independently a release-date requirement. Do not remove current baseline fields in this discovery. |
| No unsupported source influences; explicit acceptance; no implicit witness | Namespace attribution has an accepted accountable basis and no known contradictory source evidence | **REQUIRED FOR PUBLIC-REGISTRY IDENTITY** under a testimony route. Keep fail-closed unknown/private/conflicting namespace and deliberate acceptance. No generic “assume public” switch. |
| Catalog ID/version, usable created, complete eligible latest | Public metadata is about the correct version and actual comparator | **REQUIRED FOR PUBLICATION-DATE CLAIM.** Keep H4 unchanged, including missing-latest-date failure, no older fallback. |

None of the whole content/event chain is simply redundant: its parts protect
distinct stronger claims. The product question is whether those claims should
gate every age, not whether their checks are pointless. Bounds, verified TLS,
safe reads, no execution, privacy and supervision remain protection boundaries;
their necessity is not negated by measurement parity.

## Minimum common contract and concrete recommended H3

The minimum is sufficient **only for an accepted artifact snapshot claim**:

1. Establish a source-qualified direct occurrence and its supported population.
   State the directness convention; do not imply evaluated/runtime completeness.
2. Obtain one exact used/selected P/V from an accepted declaration or selection
   artifact appropriate to the ecosystem. Associate it with source/context and
   fail on unsupported ambiguity or known contradiction; never resolve today.
3. Establish the applicable public package namespace/history **before lookup**.
   Use attributable artifact source evidence or explicitly accepted, package-
   and snapshot-bound supplier namespace testimony. Unknown/private/conflicting
   namespaces fail closed; public existence/hash coincidence alone is insufficient.
4. Retrieve authoritative identity-bound selected and eligible-latest dates under
   the ecosystem's declared publication/comparator policy. Missing required
   dates or incomplete required population remains unmeasurable.
5. Apply existing UTC/365.25-day arithmetic, exact same-version zero and flagged
   negative-date clamping. Aggregate measured occurrences only; preserve known,
   unknown and unavailable populations and successful sibling rows.
6. Explain the evidence/namespace basis and uncertainty. No acquisition, installed,
   deployment, compatible-upgrade or reproducible-build claim follows.

This is a target common truthfulness standard, not a claim today's Python/npm
positive source checks already satisfy step3. Their source-authority limitation
needs separate prospective product consideration, not a silent change in this run.
Latest policies also differ today: timestamp-max for siblings versus NuGet numeric
precedence. Parity does not authorize changing those established comparators.

**Recommended replacement H3, for human selection:** accept a supplied supported
project/schema1 lock pair as an attributable bounded snapshot, retain current
byte/project/framework/request/direct-population checks, and accept explicit
package-specific testimony that its selected P/V belongs to the canonical
nuget.org namespace whose public history should be measured. That testimony must
bind exact supplied project/lock bytes and context and disclose its scope; it may
be made later from retained evidence. Do not require actual-download origin,
native package records, contemporaneity, local content-hash agreement or public
catalog content-hash agreement as gates to **that namespace/version-age claim**.
Retain qualified completeness/no unsupported context/source influences and reject
known contradictory namespace/selection evidence. Public namesakes alone confer
no authority. An unexplained content mismatch never becomes verified content;
if evidence instead establishes a private/repackaged distinct identity, reject
public attribution. No automatic witness acceptance or blanket public default.

This is concrete product meaning, not a proposed new serialized format. A later
approved spec must define the testimony's nonsecret fields, admissibility,
failure precedence and public reporting before architecture or code changes.
Existing strict witness fields must not silently acquire the new meaning.

Genuinely ecosystem-specific requirements remain: Python name/constraint and
freeze intersection rules; npm scope/path/selector and lock arbitration; Ruby
source-block/platform/observable-date interpretation and optional complete static
group selection; NuGet bounded MSBuild/context/normalization, direct/project
distinction, explicit occurrence identity and first-receipt/listed-greatest rules.
Optional stronger assurances include native acquisition evidence, content
correspondence, producer chronology, signatures, complete evaluated scope and
reproducible restore; none is established merely by a libyears number.

## Options and migration

| Option | Number/trust risk | Reproducibility and ordinary use | Parity, existing artifacts and migration |
|---|---|---|---|
| A KEEP CURRENT H3 | Supports stronger accepted event/content claim; testimony still can be false. Strongest content-substitution barrier here; unknown/private origins blocked. | Highest evidence-production burden; historical snapshots may never qualify; 0016 public mismatch withholds age. Not itself reproducible restore. | Approved baseline; no migration. Materially stricter than siblings. Historical valid results remain valid; missing results stay missing. |
| B MINIMUM MEASUREMENT H3 (recommended) | Truthful accepted snapshot/public-P/V age with bound namespace authority. Loses mandatory content-substitution detection and event assurance; false namespace testimony can misattribute a private fork. | Uses retained selection and later accountable testimony; metadata availability still limits yield; no build/restore promise. | Comparable snapshot truthfulness; stronger positive namespace basis than current Python/npm, analogous Ruby lock remote. Reuse strict evidence as input evidence when meanings suffice, never manufacture new testimony. Output trust/hash/public_content_verified meanings require explicit migration design/review; cannot silently label weaker rows with old states. |
| C TIERED ASSURANCE | Minimum age plus separately stated verified facts; must keep namespace unknown distinct from “low assurance.” Labels cannot repair missing selection/source/date. | Better optional audit detail, more concepts and maintenance; tier does not make missing dates measurable. | Preserves strict path and distinguishes old/new results but needs separately approved schema/output/aggregation semantics. Do not mix populations without visible basis. Not selected/implemented here. |
| D STAGED REDUCTION | Remove mandatory event chronology/native evidence, retain package namespace testimony and public/local content agreement. Preserves content checks but still rejects hash-domain mismatches. | Easier historical evidence than A, yet public-hash barrier remains even when P/V namespace is known. | Smaller conceptual move; still substantially stronger than siblings and does not solve 0016 mismatch. Requires output/authority migration, not a docs clarification. |

Recommend **B as the measurement contract**, preserving truthful stronger facts
when available without commissioning a new tier. C can follow only if humans
want that additional product. No requirement for identical file mechanics.

Concrete recommendation risk: an accepted, byte-bound assertion can still name
public P/V for privately modified or unrelated bytes. Dropping mandatory hashes
removes one contradiction detector. A user could read “used” as deployed code
despite snapshot qualification. Mitigations are explicit package namespace
acceptance, reject known source/selection conflicts, preserve precise claim text,
and avoid verified-content/event labels. These reduce risk, not authenticate truth.
If the human requires byte-level attribution rather than namespace-version age,
A is the coherent choice; convenience cannot override that decision.

Previously valid measurements remain valid for their original stronger claim
and also meet the weaker conceptual claim where namespace/date policies agree.
Old unmeasurable reports remain truthful historical outcomes under their contract;
do not rewrite them as errors or retroactively measured rows. Recompute only
under an explicitly identified future contract and available evidence. Same
fixed inputs/metadata should retain arithmetic, but newly admitted rows can change
totals/coverage; migration must account for population comparability, trust_basis,
origin_state/content_hash_state, omission/reasons and explicit-interface behavior.
Do not promise schema3 compatibility before independently reviewing a proposal.

## OASim practical consequence and limits

No new OASim access is necessary: [0021](nuget-repository-sources.md) and
[published correction validation](../maintenance/nuget-repository-sources/validation.md)
already distinguish parser, selection, witness acceptance and hash blockers.
This run does not access, execute, modify, regenerate or baseline OASim; prior
before/after equality remains historical evidence, not a new equality claim.

| Contract | Consequence using the retained observations |
|---|---|
| A current H3 | Ordinary no-mapping result remains 10 attempted sources, 8 unknown populations, 2 known populations totaling3 occurrences with missing accepted provenance. Retained Updater witness is present but not implicitly accepted. Prior explicit prospective event was 0/1 hash mismatch. No newly established measurable occurrence. |
| B minimum | The two supported populations/3 occurrences become candidates for acceptance without contemporaneous event/native/hash gates. Existing locks supply retained selection evidence; they do not alone establish applicable public namespace or all required dates. Prior controlled Updater event records support public association for that event, but current byte/context acceptance and current authoritative metadata are not revalidated here. Therefore **0 additional measurements established**, up to3 parser-admissible candidates pending required authority/date checks, not a promised3. |
| C tiered | Same minimum candidates as B; optional stronger facts may be retained separately. No extra populations merely from tier labels. |
| D staged reduction | Could remove missing-event barrier with later accepted testimony; retains Updater's observed public-hash blocker. No additional measured count established. |

Eight parser-rejected populations stay unknown under every H3-only option.
51 raw literal occurrences/24 package IDs/15 edges are a research inventory,
not denominator or measurable count. Historical Phase2 selection corroboration
across51 is useful future scope evidence, not parser authorization or current
namespace/date completeness. Assets/export remain unsupported product inputs.
H3 blocks the accepted subset; parser/context support blocks most project
populations. Neither alone explains all missing technical-debt results.

## Verification, observation and next gate

Parent ran the focused offline suite across requirements, snapshot, scan, npm,
Yarn, Ruby local/registry, NuGet provenance/source/registry/repository: **219 PASS**.
Tests demonstrate current behavior; no live registry ages, new producer event,
positive yield, hash-domain cause or hosted CI result is claimed. No full-suite
rerun is needed for documentation-only discovery. Exact source/test obligations
are independently checked by reviewers against the frozen candidate.

Run identity **006-0023**, cross-ecosystem product-semantics discovery in the
006 follow-up lineage, not Feature007 or approved implementation. 006-0022's
machine handoff exists; human post-run telemetry/continuity was not supplied in
this commission. Preserve that enrichment gap and leave the ledger unchanged;
neither prior nor current run is appended here. Current handoff goes to
`/tmp/libyears-observations/006-0023.json`, with unavailable telemetry blank.
User-supplied published synchronization of1ba915f is accepted commissioning
evidence; no remote/hosted CI observation or push is inferred.

**Exact next human decision:** retain byte/event-provenance as a mandatory
measurement claim (A), or select the proposed bound snapshot/public-namespace
version-age contract (B), explicitly accepting loss of mandatory acquisition/
content assurance and rejecting namesake-only authority. If B is selected,
authorize a separate specification/migration lifecycle before any runtime work.
Tiered output (C), parser expansion, source-policy changes for siblings and
alternate metadata providers remain separate unselected work.
