# Existing SBOM corpus feasibility — 007-0047

**Useful exact versions are available without target execution. Start by specifying
bounded local CycloneDX JSON inventory evidence, with automatic discovery and an
explicit file override. Qualify paired Maven Observed facts separately; do not
reinterpret a generic SBOM as resolved direct dependencies.** This is reviewed
discovery, not authorization for a reader, flag, schema or product change.

## Boundary and corpus

The clean starting Git boundary is `d0065444b39adfda6795dbed2023d103b748f2c5`.
The [previous search](maven-observed-artifacts.md#actual-availability-and-limits)
remains historical evidence of absence within its inspected filenames/depths,
not absence elsewhere. This investigation does not re-search DPC, AB2D or BFD.
The new artifacts prove feasibility elsewhere; none establishes improved results
for those targets. The [existing S5 contract](../specs/007-maven-dependency-age/spec.md#s5--observed-evidence-and-availability)
and settled Maven conventional POM-modification date basis remain unchanged.
No age metadata lookup, measurement, target tool/script, generator or workflow ran.

Retrieved on 2026-11-20, within a 40-minute author cap; acquisition stopped once
the contrasts below supported a recommendation. Authentic artifacts, not schema
examples or synthetic yield, supply the counts. Raw bytes, retrieval timestamps,
SHA256 digests, procedures and count output are retained privately in helper-resolved
`D/007-0047/`; D is printed by `python tools/observation_handoff.py directory`.
The provenance table names stable public retrieval locations; GitHub graph exports
are time-specific snapshots and cannot be reproduced byte-for-byte by re-exporting.

| Artifact and public source | Producer / subject binding | Recorded shape and licensing |
| --- | --- | --- |
| [Apache commons-lang GitHub export](https://api.github.com/repos/apache/commons-lang/dependency-graph/sbom/generate-report) | GitHub Dependency Graph, protobom build `72f62ebd2215+dirty`; created 16:57:15Z; repository subject `master`, no commit | SPDX2.3; 28 packages, 27 repository DEPENDS_ON edges; CC0-1.0 |
| [psf/requests GitHub export](https://api.github.com/repos/psf/requests/dependency-graph/sbom/generate-report) | Same GitHub/protobom producer plus dependabot; created 16:58:12Z; subject `main`, no commit | SPDX2.3; 30 packages, 29 repository DEPENDS_ON edges; CC0-1.0 |
| [Dependency-Track4.13.4 release bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.13.4/bom.json) | CycloneDX Maven plugin2.9.1 asserted; root `org.dependencytrack:dependency-track:war:4.13.4`; release tag resolves to `996203dc6d88a6dfa2f129603b2ef778360ccce3`; no BOM creation timestamp | CycloneDX1.5; 201 component entries including the root, 201 graph-node entries; no BOM-level license; subject Apache-2.0 and repository LICENSE inspected |
| [CPython3.13.0 source-release SBOM](https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz.spdx.json) | Python Release Managers, ReleaseTools revision `1ec898a8998efdc3230fdd229ad976b49faf7cc6`; created 2024-10-07T07:30:24Z; describes CPython3.13.0 source distribution | SPDX2.3; 25 packages, 24 DEPENDS_ON, one DESCRIBES and 4722 CONTAINS relationships; CC0-1.0 |
| [CPython checked-in source fragment](https://github.com/python/cpython/blob/60403a5409ff2c3f3b07dd2ca91a7a3e096839c7/Misc/sbom.spdx.json) | Tag v3.13.0 independently dereferenced to this commit; curated vendored-source metadata | SPDX2.3-shaped fragment: 5 packages, 111 CONTAINS edges; lacks creationInfo/dataLicense and standalone document framing; retain as a discovery false-positive witness, not a supported full document |

Digest identity (SHA256, complete raw bytes):

| Artifact | Digest |
| --- | --- |
| commons-lang graph | `afd5dbe6b7bf559ed80331b3744446dfffff73654a73b9b3e11e129651d4a868` |
| requests graph | `f56c65db64f0a1520aa84619b6ac2e9e8d4addd03d1ce7541543862e9e1e26a2` |
| Dependency-Track CycloneDX | `c201f3a64e7b2c510b83fe99dd6e945244030c6484009100b04a257721dba790` |
| CPython release SPDX | `feba258898139ca77b6421e80cba8fa7edd4cf29809bb545c32aadd404142e36` |
| CPython source fragment | `1ef5cc95d8b527b42030636359dd737ed8fcb255f42ea04478b2cd2b1129bb76` |

Raw files are not redistributed here. An application's license and licenses of
listed components do not automatically license the SBOM as a dataset. Private
durable retention avoids assuming redistribution rights where unstated.

## Counts and truthful claims

Counts are observed records and **potential reader candidates**, not libyears
measurements or accepted joins. “Exact candidate” requires a version-bearing purl
matching the version field in a supported ecosystem; it is not resolution proof.
Subject roots, producer metadata and unsupported ecosystems are excluded from
those candidate counts. Maven plugin identities remain identity candidates,
without implying they belong in the existing direct dependency population.

| Artifact | Supported identities / exact candidates | Directness and source/context | Potential existing-occurrence join / inventory-only now |
| --- | --- | --- | --- |
| commons-lang graph | 17 Maven identities; 3 exact, 14 missing versions; 10 Actions plus repository root outside Maven scope | All 27 dependencies point from repository root; plugins and project dependencies mixed; no manifest/module/context mapping | 0 established joins; all 17 Maven records inventory-only, only3 have exact candidate versions |
| requests graph | 19 PyPI records; 3 exact records representing2 unique identities/versions; 12 missing versions, 4 ranges; 10 Actions plus root outside Python scope | Repository edges only; sphinx7.2.6 appears twice with distinct SPDX IDs and identical purl; no source occurrence mapping | 0 established joins; all19 PyPI records inventory-only; no fabricated occurrence from duplicate package records |
| Dependency-Track CycloneDX | 200 external Maven components, all exact; root is repeated in components and metadata and must not count as an external dependency | 43 represented root edges, all43 uniquely match literal G/A declarations in release POM; other157 external components lack root-direct edges | 43 candidates for later qualification, **0 accepted current-checkout joins**; all200 external records remain inventory-only today |
| CPython release SPDX | 20 versioned PyPI purls, all matching package versions; 4 other external components plus CPython root | PyPI components include pip and its bundled dependencies, plus vendored macholib; component containment/dependency graph describes the distribution | 0 joins to ordinary project direct Python population; all20 PyPI records inventory-only |
| CPython source fragment | 5 version fields, 1 exact PyPI purl (macholib1.0) | File containment, not a direct dependency graph; source fragment rather than full SPDX document | 0 candidates for accepted intake as a full document; useful negative framing witness |

No version-bearing purl/version-field disagreement was found in these artifacts.
The requests range-valued versionInfo fields have unversioned purls: they are not
exact versions. Missing identities/versions remain missing, not malformed by fiat.
No parser conformance or adversarial validation claim follows from these counts.
The repeated sphinx record is not two known module occurrences or an exact-version
conflict. Cross-artifact packages refer to different subjects; differing versions
there would not be a same-occurrence conflict.

The Maven artifact is materially richer than a bare inventory. For example,
`jakarta.servlet:jakarta.servlet-api` is a unique provided-scope direct declaration
with no version in the root POM, while the root edge names6.1.0. This is additional
exact information, not proof of new measurable yield or that its Declared version
could not be obtained from other approved evidence. The pinned
[POM](https://github.com/DependencyTrack/dependency-track/blob/996203dc6d88a6dfa2f129603b2ef778360ccce3/pom.xml)
contains57 direct declarations:42 compile,1 provided,14 test. Its CycloneDX
configuration excludes tests. Thus43 matches cannot certify the existing complete
direct-occurrence population. A safe positive fact need not await full coverage,
but neither missing tests nor transitive components may silently change N.

Purls preserve `type=jar` on199 entries, `classifier=native&type=jar` on one
`com.github.jnr:jffi` entry, and `type=war` on the root. Group/artifact/version
fields agree with those purls. Keep qualifiers and original Maven model keys;
artifact type/classifier defaults and handler aliases require qualification,
not dropping qualifiers or equating same G/A. CycloneDX scope `required` on200
entries is not Maven compile/runtime scope or evidence that each is direct.

The pinned [build workflow](https://github.com/DependencyTrack/dependency-track/blob/996203dc6d88a6dfa2f129603b2ef778360ccce3/.github/workflows/_meta-build.yaml)
describes Maven builds, profile changes, a later makeBom and a service-BOM merge.
It supports a build-associated producer interpretation; it is not an independently
verified execution trace for this asset or exact local model-context binding.
The BOM has no input-byte manifest establishing current POM/parent/profile
correspondence. Release/tag association and component hashes do not prove that
correspondence, resolution completeness, runtime use or deployment. Hashes of
downloaded SBOM bytes bind our assessment to those bytes; component/archive hashes
bind their claimed content, not local dependency-system selection or public namespace.

GitHub [documents a graph assembled from manifests, locks and submissions](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-graph).
Neither export identifies per-record derivation or a commit-bound local context.
A current hosted graph can mix sources and stale submissions. Repository DEPENDS_ON
edges cannot be promoted into Maven module or Python production-direct edges.
The [CPython documentation](https://www.python.org/downloads/metadata/sbom/)
identifies release SBOMs for source distributions: its PyPI inventory shows useful
versions without establishing an installed environment or ordinary requirements
population. No package URL grants public comparator admission. SBOM generation
time is not package publication time. No date-policy change is proposed.

## Decision matrix and coherent defaults

All entries below are recommendations for later specification, not selected flags
or an approved trust route. Local default discovery is the human's selected usability
direction; default remote acquisition is a separate disclosure decision.

| Family or intake | Benefit | Minimum claim / recommendation |
| --- | --- | --- |
| GitHub dependency-graph SPDX | Convenient public current inventory; easy acquisition in this corpus, but few exact supported records and no per-module binding | Later hosted inventory source; never generic resolver/Observed authority |
| Non-GitHub SPDX | Real release inventory can supply exact PyPI versions; partial checked-in fragments also exist | Later explicit/full-document adapter; require document/subject framing and typed relationships, never infer directness from presence |
| CycloneDX JSON | Strongest Maven witness here: explicit root edges and variant-qualified exact versions | First bounded family, initially1.5; independently labeled inventory facts and provenance, then separately qualify a pinned producer for paired Observed facts |
| Local automatic discovery | No need to know an SBOM exists; no inherent network disclosure | Default on, bounded conventional names and shallow directories; no links, no arbitrary content crawl; discovery finds candidates, not trust or automatic joins |
| Explicit file intake, provisional --sbom | Handles unusual names and disambiguates subjects | Same parser/safety limits; selects exact bytes, does not attest current binding, directness or public namespace; explicit selection overrides automatic candidate selection |
| Hosted acquisition | Existing release assets and public graph exports need no local target tool | Default off; explicit public repository/release selection and opt-in acquisition; fixed documented providers, no URLs followed from SBOM fields |

Recommend a single disable control, provisionally `--no-sbom`, suppressing automatic
discovery and acquisition. A contradictory explicit file plus disable request should
be a clear option error, not hidden precedence. Offline mode should block hosted
acquisition and still permit local snapshots. An unavailable/403/404/timeout hosted
source is unavailable evidence, not an empty dependency set. Normal local results
survive; show a concise source status rather than fail the whole scan. No implicit
credentials, private-resource probing or package downloads to improve yield.

Keep existing Declared/Observed metric views. Put origin such as “release SBOM,
CycloneDX Maven plugin2.9.1” in an evidence/source column for genuinely joined facts.
Until association is accepted, show a separately labeled **SBOM inventory** listing
asserted versions, subject and relationship status, with no merged age totals or
repository coverage. SBOM is a source, not a third metric/version-state column.
Avoid overwhelming ordinary output with transitive rows; use a concise inventory
availability/count and an independently requested inventory detail view.

When exact local and SBOM selections for the same accepted context disagree, expose
a conflict and withhold the additional-source join; keep independent local results.
A Declared request differing from an independently selected Observed version is
not inherently a conflict. Multiple subjects/contexts must not be merged or selected
by mtime/first match; report ambiguity and allow explicit selection. Stale unbound
artifacts remain historical inventories. Missing directness/context prevents joining,
not retaining a valid inventory claim. Malformed/oversized/unsupported documents
get bounded source-level refusal without erasing safe siblings or fabricating N.

## Acquisition safety and reproducibility

The [current official API documentation](https://docs.github.com/en/rest/dependency-graph/sboms)
was inspected before export. API version2026-03-10: GET generate-report then GET
fetch-report; both successful exports returned302 to verified HTTPS download hosts,
with no202 polling needed. The obsolete synchronous endpoint was not used. No
Actions, build or dependency submission was triggered. Acquisition unavailability
would not prove a repository lacks dependencies or an existing SBOM.

The retrieval helper enforced8MiB per response,10-second connect,30-second request,
three redirects maximum, fixed exact HTTPS host validation and no automatic curl
redirect following. A chain is bounded by120 seconds; this pass performs no202
retry. The initial commons-lang generation used a separate30-second/1MiB request.
Two early download redirects were refused until the GitHub-supplied destination
host was explicitly validated; no insecure fallback. The durable log proves18
acquisitions plus3 followed redirects (21 HTTP requests); author invocation
observations add3 initial/unlogged requests, for24 total. This includes one duplicate
generation due to a recorder201 handling error. Three valid text captures initially raised post-save JSON decoding
errors; saved bytes remain valid evidence. Official documentation browsing is
separate from these retrieval counts. Headers and signed download locations were
discarded; no package artifact or arbitrary SBOM URL was fetched.

No explicit authentication or trust override was supplied. Initial curl calls did
not suppress startup configuration; no configuration was inspected and absence of
ambient configuration was not established. The retained helper now uses `curl -q`;
a future implementation must avoid ambient credentials/configuration and forbid
credential forwarding. No secrets or signed URLs are retained in the corpus record.
Future parser/acquisition limits, duplicate-member/refusal semantics and diagnostics
need specification; follow the [existing safety findings](maven-observed-artifacts.md#privacy-safety-and-next-step)
without turning discovery code into a production reader.

## Smallest next slice and specification handoff

1. **Credible route:** yes, already-published release SBOMs can provide substantially
   richer exact version information without executing the target. Local copies are
   the simplest consumption path. This corpus does not estimate general prevalence.
2. **First family:** bounded local CycloneDX JSON1.5, automatic candidate discovery
   plus explicit selection/disable; prioritize the real Dependency-Track witness.
   Defer hosted acquisition and broad producer/format support. Keep the inventory
   label until independent scope/context association qualifies positive paired facts.
3. **Observed:** no artifact is accepted by the current release. A future qualified
   Maven producer plus exact current input/context/model-key/directness association
   could support S5 retained-selection facts; generic format validity cannot.
4. **Join/coverage barriers:** repository-deduplicated graphs, omitted test scope,
   variant aliases, repeated occurrences, absent local byte/context binding and
   unspecified derivation. Root GAV/tag equality and a hash alone do not repair them.
5. **Default behavior:** bounded local discovery on, network acquisition off,
   explicit override and disable; offline/local failure preserves independent results;
   conflicts visible, no silent replacement or denominator change.
6. **Human decisions before specification:** accept a separately labeled inventory
   first slice versus requiring paired Observed qualification before shipping;
   approve the bounded1.5/producer scope and what accountable binding testimony may
   suffice for future joins; choose ordinary output/detail exposure. Hosted opt-in
   scope/disclosure is a later distinct decision, not implied by default local discovery.
7. **Concrete acceptance witness, not executed product tests:** use the retained
   Dependency-Track bytes and pinned POM as a public offline fixture. Automatic local
   discovery should reveal200 external exact inventory records,43 represented root
   edges, preserve57 local direct declarations and disclose14 tests omitted by the
   SBOM. A supplier/context-qualified follow-up must demonstrate at least one safe
   new paired version fact (servlet6.1.0 is a candidate), with unchanged independent
   Declared rows and unknown complete Observed coverage. Without that qualification,
   success is truthful useful inventory display, not improved measured ages. Mutate
   versions/context, add an ambiguous second subject, remove edges and test
   offline/unavailable/oversized inputs to prove safe degradation. No target tools
   or registry calls are needed for this witness.

The [review companion](sbom-corpus-feasibility-review.md) records the frozen scopes,
corrections and final checks. The prior007-0046 original handoff/artifact/final freeze
were verified and reconciled once without supplied telemetry enrichment; unknowns
and qualifications remain. Current007-0047 is not appended to the ledger.
No runtime, CLI, schema, metric or current product behavior changed.
