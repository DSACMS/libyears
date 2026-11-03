# Feature 006 Technical Plan: Bounded NuGet Selected-Version Evidence

## Status and authority

Candidate drafted in fresh run `006-0005`, 2026-11-03. Approval status and next
gate are recorded in [reviews.md](reviews.md); this file remains byte-frozen
through independent review, including after an approval. This plan grants no
implementation authority. Task decomposition requires the next separate gate.

Normative product contract: [spec.md](spec.md), approved SHA-256
`f02a947ae33dc83afa08a800e0bd965f56e697317e40dd1c6209d133f3c73cc8`.
S1–S8, H1–H4, F1/F2 and AC-01–36 govern all work below. Technical choices here
implement that contract; a consequential missing product decision must stop work
with HUMAN DECISION REQUIRED. No product decision is delegated to implementation.

## Architecture and boundaries

The pipeline is deliberately staged:

```text
explicit CLI selection -> safe project bytes -> complete declaration scope
 -> accepted whole lock -> accepted whole witness and context binding
 -> per-declaration association -> origin gate -> local hash gate
 -> authorized public metadata -> public content gate -> used/latest dates
 -> existing metric -> schema-v3 and human output
```

Whole-source acceptance precedes per-package processing. Never emit partially
parsed populations, manufacture dependency failures from an unavailable source,
or use later metadata to repair local rejection. Static supplied evidence is a
qualified snapshot, not evaluated MSBuild, restore success or runtime scope.

Use focused modules, not a registry/plugin framework:

| Component | Responsibility and principal records |
|---|---|
| `nuget_project.py` | bounded XML events, ProjectContext and DirectDeclaration |
| `nuget_lock.py` | duplicate-preserving schema-1 validation, LockSnapshot/LockEntry |
| `nuget_version.py` | separate request minimum, selected identity and stable precedence helpers |
| `nuget_provenance.py` | witness schema, byte binding, SupplierContext/PackageOrigin |
| `nuget.py` | source orchestration, reason precedence, association and LocalAuthority |
| `nuget_registry.py` | public resource traversal, normalized PublicVersion, typed adapter results |
| `model.py`, `scan.py`, `cli.py`, `output.py` | additive records, explicit source pair, options and serializers |

Records are frozen dataclasses with descriptive fields. Raw parser dictionaries
stay at input boundaries. Public evidence is separate from internal hash/baseline
records. Avoid sharing Ruby policy helpers merely because the shapes resemble
one another. Reuse the established transport and bounded descriptor-reading
technique; preserve old defaults and injected `get(url)` doubles.

## Safe local input and finite work

A NuGet-local reader follows `_ScopedRubyReader`'s descriptor-relative approach,
without changing Ruby behavior. Open the selected root as a directory descriptor;
resolve only the three permitted immediate filenames inside it. Permit only
symlinks whose resolved target is a regular file within that root. Reopen through
root-relative components with no-follow directory/file flags, nonblocking reads,
and fstat regular-file checks; compare device/inode and size/mtime before/after
reading and with the inspected path. Fail closed on replacement or unsupported
platform safety primitives. Never open a FIFO before nonblocking/type protection.
Do not search ancestors or follow ProjectReference paths. Retain exact bytes for
SHA-256 before UTF-8 decoding; do not normalize line endings for fingerprinting.

| Bound | Value / enforcement |
|---|---|
| Project / lock / witness bytes | 1 MiB / 16 MiB / 16 MiB; read at most cap+1 |
| XML depth / elements / attributes per element | 32 / 50,000 / 32, enforced during parser callbacks |
| JSON depth / total values per input | 32 / 200,000, lexical guard before json decoding |
| Direct references / lock entries / witness package records | 10,000 / 50,000 / 50,000 |
| General local string / version / numeric component | 16 KiB / 256 ASCII characters / 32 decimal digits |
| Framework / producer name/version / SDK assertion value | 128 / 256 each / 256 characters |

Numeric length is checked before integer conversion. Lexical JSON guards respect
quoted strings/escapes and count containers/scalars; `object_pairs_hook` rejects
duplicate keys at every level, `parse_constant` rejects nonfinite values, and
integer decoding checks digit length. Reject bool where integer schema 1 is
required. Apply whole-structure malformed-before-unsupported precedence, even
when an unsupported field appears earlier. Resource exhaustion terminates safely
without attempting unbounded diagnostic recovery. Project limits use
`unsupported_nuget_project`, lock limits `unsupported_lockfile_format`, witness
limits `invalid_nuget_provenance`. Encoding/I/O/malformed cases follow S6.

## Project declarations

Use standard-library Expat event parsing of strictly decoded UTF-8, with DTD,
entity-declaration and external-entity handlers rejecting input; no entity
substitution, external parser, XInclude, schema fetch or evaluation. A bounded
first pass validates complete XML framing; a second event pass validates the
supported context, collecting findings rather than returning a partial scope.
Reject namespaces and non-UTF-8 encoding declarations. Comments/formatting are
inert. Built-in XML character escapes yield literal attribute values, which must
still pass the declaration grammar.

Require root Project with a nonempty literal Sdk attribute. Accept one
unconditional PropertyGroup TargetFramework or single-valued TargetFrameworks,
using S2's literal ASCII framework grammar. Reject duplicates, both properties,
conditions, computed values, RID properties and semicolon lists. ItemGroup
PackageReference must be immediate, unconditional Include/Version attributes;
validate IDs and the dedicated numeric request grammar. Track lowercase ASCII
IDs before association; duplicate/case aliases reject the entire population.
Allow each of the four specified ancillary metadata names once across attributes
and children, with literal values; reject unknown metadata and Version children.

ProjectReference/FrameworkReference are inert membership exclusions and their
paths are never opened. Recognize them only as such, never as package evidence.
For other properties/items, use an explicit table of demonstrably unrelated
literal forms (initial examples OutputType, Nullable, ImplicitUsings, LangVersion,
AssemblyName, RootNamespace, Compile and None). Validate their structural/literal
context. Reject unknown forms unless reviewed as demonstrably inert, and always
reject imports, Choose/When, Target, package/version/restore/source-affecting
properties, PackageVersion, GlobalPackageReference, Update/Remove/VersionOverride
and computed/conditional membership. The table is a conservative recognition
mechanism, not an MSBuild evaluator. SDK imported behavior is only an accepted
baseline assertion; absence of Import never proves evaluated completeness.

## Lock and F1/F2 association

Validate the entire JSON envelope before association: only version and dependencies
at root, version integer 1, exactly the literal framework key, no RID/additional
context. Validate all entry kinds/fields from S3, including closure dependency
maps of ID/string pairs. Transitive and Project nodes frame closure only; they
never add population or satisfy a PackageReference. Reject unknown semantic
fields/kinds. Direct requires string requested; absent resolved/contentHash is
allowed for the specified isolated failures. Present non-string resolved is
malformed, including null/array/object. Hash absence/malformed string remains a
local hash failure; a non-string hash is malformed structure. Entry/dependency
ID maps reject case aliases, as well as exact duplicate JSON keys.

Extra Direct identities reject the whole context. Then associate each declaration
with its unique same-ID Direct. Missing Direct precedes request disagreement,
missing resolved and unsupported resolved. A Transitive namesake never repairs
missing Direct. Preserve safe original request text on mismatch but expose no
selected_version, normalized_version or selection_source until association
succeeds. Unsafe/overlong arbitrary strings are never echoed.

F1 has a small dedicated implementation: declaration parser accepts two to four
canonical decimal components; normalize to a four-integer minimum tuple and a
three-component spelling, adding patch zero and omitting revision zero. Lock
request is accepted only if exactly `[<normalized spelling>, )`. Compare minimum
tuples, not resolved versions. Tests explicitly cover all five S3 positive pairs,
`1.0` versus `[1.0.1, )` with both selecting `2.0.0`, retained nonzero revision,
and every S3 negative/noncanonical form. No range parser, satisfaction check or
resolver is introduced.

F2 has no dependency ambiguity state. Repeated keys, case aliases, repeated
resolved keys and non-string/multiple selections are `invalid_lockfile` before
association; additional contexts are `unsupported_lockfile_format`. No NuGet
path may emit `ambiguous_lock_evidence`. Missing requested is malformed structure;
a string outside the supported canonical serialized range is isolated mismatch.

## Supplied witness serialization and H3

Define a strict version-1 UTF-8 JSON object, rejecting duplicate/unknown fields:

```json
{
  "version": 1,
  "project": "Example.csproj",
  "framework": "net10.0",
  "project_sha256": "<64 lowercase hex>",
  "lock_sha256": "<64 lowercase hex>",
  "producer": {"name": "supplier", "version": "1"},
  "coherent_snapshot": true,
  "baseline": {
    "sdk": "Microsoft.NET.Sdk",
    "sdk_version": "10.0.100",
    "explicit_population_complete": true,
    "unsupported_membership_version_influences": false,
    "unsupported_framework_rid_influences": false,
    "unsupported_source_influences": false
  },
  "packages": [
    {"id": "Example", "version": "1.0.0", "content_hash": "<base64 SHA-512>",
     "origins": ["https://api.nuget.org/v3/index.json"]}
  ]
}
```

The baseline booleans explicitly cover imported, generated, ancestor and central
inputs; document this meaning in the schema/help and fixture README. Required
SDK assertion matches project Sdk literally; no SDK is loaded. Required fields
have strict types; unsupported version or structurally corrupt witness is
`invalid_nuget_provenance`. False coherence, digest/project/framework/SDK binding
disagreement or known stale pairing is `nuget_context_mismatch`; asserted
unsupported influences or incomplete explicit population is
`unsupported_nuget_project` with unknown denominator. Validate whole structure
before context checks. Baseline absence is invalid, never inferred.

Package records bind the envelope context/digests by containment, plus ID,
normalized selected identity and hash. Duplicate normalized ID/version records
are invalid witness framing. Unselected/transitive records confer no authority;
validate framing but do not demand their origin be public. Missing matching record,
empty origins, unknown/private/alternate/multiple conflicting origins yields
`unsupported_dependency_source`. Only a singleton exact canonical public URL
permits lookup; values are inspected as strings, never fetched or displayed.
An absent/invalid string hash yields `content_hash_unavailable`; decode strict
standard base64 to exactly 64 bytes. Compare lock and witness decoded hashes;
local mismatch prevents all requests for that package.

Only the positive local gate constructs LocalAuthority, containing context
fingerprints, canonical ID/version and agreed hash. Adapter lookup accepts this
record rather than bare ID/version. There is no blanket public switch, implicit
witness discovery, cache/config reader or origin inference from hash coincidence.
Supplier testimony enters solely through explicit `--nuget-provenance`; it stays
separate from PublicVersion observations. `asserted_public`/`local_agreement`
becomes `public_content_verified`/`public_agreement` only after identity and public
catalog SHA512 agreement. Hash domain fitness and useful live yield remain
unvalidated; disagreement fails closed, never archive repair or altered H3.

## Public API resources and transport

Verify resource contracts using primary Microsoft documentation:
[registration](https://learn.microsoft.com/en-us/nuget/api/registration-base-url-resource)
for the SemVer-2 hive and listing defaults,
[catalog](https://learn.microsoft.com/en-us/nuget/api/catalog-resource) for
PackageDetails identity/hash/first-receipt fields, and
[version normalization](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning#normalized-version-numbers).
The registration catalogEntry @id links directly to the source catalog document;
use those leaves, not a catalog history crawl. This resource composition is the
planned implementation inference from the two contracts.

Fetch fixed `https://api.nuget.org/v3/index.json` once per activated scan that
has authorized candidates. Select RegistrationsBaseUrl/3.6.0 only, requiring its
resource URL to be `https://api.nuget.org/v3/registration5-gz-semver2/`.
No older hive fallback. Conflicting/missing resource identity is invalid response.
Approved request destinations, all on exact authority `api.nuget.org` with no
port, userinfo, query or fragment:

- `/v3/index.json` for resource discovery;
- `/v3/registration5-gz-semver2/<lowercase-id>/index.json` and registration
  page/leaf JSON descendants for the same validated package ID;
- `/v3/catalog0/data/<timestamp>/<leaf>.json` only from validated registration
  catalogEntry links for the expected identity.

Validate paths component by component, excluding escaped separators, dot segments,
controls, backslashes and alternate authorities. Catalog leaf identity is checked
against the expected package/version after fetch. Other document links, including
packageContent, are ignored and never followed. Reject all redirects, even to
approved hosts, using existing restricted transport. Verified TLS/CA selection
remains shared; no TLS bypass, alternate-host retry or archive request.

Registration index/pages must enumerate a complete population: verify integer
counts against received arrays, page bounds against parsed versions, no missing
pages, repeated page URLs, overlap/conflicting duplicates or identity mismatch.
Inline pages are parsed; external pages are fetched from validated @id. Collect
all entries before choosing latest. Missing listed defaults true; explicit false
excludes latest; wrong type/conflicts invalidate. Unsupported potentially eligible
versions invalidate latest, never truncate silently. Equivalent identities collapse
only after material listing/hash/creation evidence agrees; inspect duplicate leaf
catalog documents when necessary. Check recognized isPrerelease flags against
parsed syntax when present. Unknown irrelevant API metadata may be ignored.

After complete structure/identity validation, locate selected identity (404 index
means package_not_found; complete index without selected means version_not_found).
Fetch catalog PackageDetails for selected and greatest listed stable identities,
and any equivalent duplicates needed for conflict checks. Require matching
ID/version/type and public selected SHA512 hash before dates authorize measurement.
No selected record means absence before hash/date validation. Missing selected
catalog record is version_not_found; missing actual-latest usable date evidence
is release_date_missing; malformed catalog identity/type is invalid response.
Catalog omission/malformed hash is content_hash_unavailable; unequal hash is
content_hash_mismatch. No latest package hash binding to a local artifact is
required; latest identity/date must still be authoritative.

Creation parsing accepts ISO timestamps with explicit Z/offset and zero to seven
fractional decimal digits; normalize UTC, truncating seventh-digit precision to
microseconds consistently before metric/output. Reject naive/invalid/year-1900
values as missing dates. Conflicting identity-bound creation assertions are
invalid_registry_response. Never use published, commit, listing or local times.
Choose greatest stable before checking its date; no older dated fallback. No
listed stable is no_stable_release. Authorized used prerelease/unlisted versions
remain eligible. Reuse measure_dependency unchanged with normalized identities,
so equivalent used/latest yields exactly zero and anomalies retain existing flags.

| Network/work bound | Value / behavior |
|---|---|
| Each wire body / decompressed body | 8 MiB / 32 MiB, bounded incremental gzip |
| Aggregate wire / expanded bytes per package | 64 MiB / 128 MiB |
| JSON depth / values / string | 32 / 500,000 / 1 MiB (identity/version limits remain stricter) |
| Pages / versions per package | 256 / 100,000; overflow invalid response |
| Requests | 512 per package; 4096 per scan including index |
| Timeout / total elapsed budget | 10 seconds per request; 60 seconds per package; 300 seconds per scan |
| Retries / redirects | zero / zero |

Wrap bounded VerifiedJSONTransport in a NuGet-only metadata client. Add opt-in
compressed-response handling with wire and expansion caps; do not change default
PyPI/npm/Ruby transport semantics. Accept identity/gzip only; malformed/truncated
encoding and byte/JSON/pagination bounds map invalid_registry_response. Timeout,
TLS, service, rate-limit and request/time budget failures map registry_error.
Inject monotonic clock and transport. No sleeping retries: on 429/503 with
Retry-After, record scan-local authority cooldown and fail the request; suppress
later requests until eligible, bounded by the scan budget. Invalid/missing header
uses fail-closed scan-local suppression. Sort candidates by canonical ID/version
and pages/duplicate links by validated URL before requests, so reorderings cannot
change cooldown or budget allocation. Check remaining elapsed budget before each
request and cap its timeout to remaining budget. No partial latest on exhaustion.

## Version helper boundaries

Three explicit functions prevent semantic leakage: parse_requested_minimum,
parse_selected_identity, stable_precedence_key. Selected/public syntax follows
S5's two-to-four numeric components, bounded ASCII suffix identifiers, leading
core zeros allowed, ignored build identity and lowercase prerelease identity.
Store original safe spelling separately. Stable key is the padded four-integer
tuple; prereleases never receive a latest key. One-component/legacy unsupported
forms fail closed. No ordering among prereleases, general semver/range framework
or resolver. Tests cover zero patch/revision, nonzero revision, leading zeros,
case-insensitive prerelease, build equivalence, 1.10 versus 1.9 and dates/ranges
that would select a different answer if wrongly consulted.

## Integration and output

Add optional NuGetEvidence/NuGetPublication records to candidate, dependency,
registry success/failure and unmeasurable flows, and NuGet source evidence with
S7 fields. Default None emits nothing for existing ecosystems. Keep authority
hashes/baseline private in internal records; transfer only safe states and dates.
An explicit NuGet lookup seam accepts LocalAuthority. Add a fourth explicit
source/lookup pair only at coherent public activation. Preserve legacy Python
scan APIs, --resolved isolation, npm/Yarn arbitration and both Ruby modes.

SourceResult already represents known N with measurement_available false and
unknown N separately. Use it unchanged in meaning: rejected project has N=null;
accepted declarations plus unavailable lock/witness has N known, no synthetic
package failures. Unsupported membership assertion clears N. Accepted empty
requires accepted lock and witness. Reuse _available_summary and existing mixed
aggregation; test all S6 availability cases, including siblings when NuGet is
unavailable. NuGet identity is ecosystem plus ASCII-folded ID, never merged with
same-name Python/npm/Ruby packages. Numeric rows alone enter existing metric.

Extend exact-option handling only for --nuget-project and --nuget-provenance,
preserving existing abbreviation behavior elsewhere. Parse these with occurrence
tracking to reject repeats; validate directory PATH, immediate filename suffix,
no separators/glob/list/absolute names, witness requires project. Missing explicit
project becomes source error, not usage error. Validate usage before reading any
source. Options pass a typed NuGet request to scan; no implicit .csproj search.
Exit 0/1/2 remains S1. Safe error formatting must not echo raw option values,
exception messages or parser input; sanitize NuGet argparse errors separately
so credential-bearing bad arguments cannot leak through standard error text.

Serialize exactly S7: top-level version_evidence.nuget only on activation;
all required evidence keys and specified nulls, format only after accepted lock;
per-row project/framework/requested plus states/basis, optional lock_requested,
selection and publication objects only after their stages establish them.
Measured version_source is packages_lock; declared is safe `ID (request)`.
Verbose JSON equals ordinary JSON. Human formatter consumes the same typed facts,
explaining all-direct test/tool scope, supplier acceptance, snapshot limitations,
first receipt, listed-stable comparator and unavailable/zero/empty distinction.
Source errors expose only ecosystem, safe source filename and reason. No raw
XML/witness/body, hashes, origins, producer baseline or unsafe path in either
output, diagnostic, usage error or unexpected NuGet exception rendering.

## Deterministic verification and traceability

Use unittest/mock and small synthetic directories under
`tests/fixtures/nuget/`. Name test families P (project), L (lock), V (versions),
W (witness/association), R (registry), I (mixed scan), C (CLI), O (output),
S (security/bounds). Each row below names a concrete witness to implement, not
an already executed acceptance test. Inject byte transport and clock; forbid
live urlopen and subprocess calls in acceptance fixtures. No dotnet/NuGet,
restore, target execution or OASim environment. Generate only size/depth boundary
variants; retain readable minimal positive and negative fixture examples.

Checkpoints: K1 foundation (parsing/association/authority); K2 public adapter and
transport; K3 integration/output/CLI; K4 final deterministic acceptance;
K5 separately authorized real-root validation; K6 fresh final convergence.

| AC | Owning work | Deterministic verification witness | Checkpoint |
|---|---|---|---|
| 01 | CLI/discovery | C ordinary co-located files omit NuGet; exact selection activates only chosen file | K3/K4 |
| 02 | CLI validation | C witness-only/repeat/abbreviation/file-path/bad-name exit 1; missing project source error exit 0 | K3/K4 |
| 03 | project | P TargetFramework and single TargetFrameworks positive fixtures yield exact N/context | K1/K4 |
| 04 | project | P each duplicate/computed/conditional/multi/RID/namespace/DTD case rejects without N | K1/K4 |
| 05 | project | P test/tool/analyzer/PrivateAssets count; project/framework/implicit exclusions and unopened referenced path | K1/K4 |
| 06 | request helper/project | V all five S3 pairs including 1.0 and 1.2.3.0; P ranges/floats/exact/prerelease reject | K1/K4 |
| 07 | project | P case duplicates and each CPM/import/Target/Update/Remove/override/unknown influence reject | K1/K4 |
| 08 | lock | L sole-framework Direct/Transitive/Project fixture; only declared Direct candidates | K1/K4 |
| 09 | lock | L version bool/unknown schema/fields/RID/extra context/duplicate keys reject whole, N retained | K1/K4 |
| 10 | association/F1 | W five normalized positives and request != selected; equal resolved with different minima rejects | K1/K4 |
| 11 | association/F1/F2 | W missing Direct, all S3 negatives, missing/unsupported resolved no-call; L arrays/aliases/repeated resolved reject whole | K1/K4 |
| 12 | context | W extra Direct, wrong project/framework, changed byte digest and irrelevant mtime/Git cases | K1/K4 |
| 13 | witness | W valid explicit version-1 envelope binds bytes; unselected conventional witness never opened | K1/K4 |
| 14 | source availability | W absent/corrupt witness N known unavailable; unsupported influence N unknown | K1/K3/K4 |
| 15 | origin | W missing/private/alternate/unknown/conflicting origins with public namesake; zero requests | K1/K2/K4 |
| 16 | origin | W config/cache/mapping/hash-only/blanket markers cannot construct LocalAuthority | K1/K4 |
| 17 | local hashes | W decoded equal hashes authorize; mismatch/invalid/missing hashes no-call with exact reasons | K1/K4 |
| 18 | public hashes | R selected catalog ID/version/algorithm/missing/mismatch/equal matrix; only equal measures | K2/K4 |
| 19 | created | R distinct created/published/commit/restore fixtures prove created alone supplies used/latest | K2/K4 |
| 20 | dates | R missing/naive/invalid/1900/contradictory dates for used/actual latest; older dated never used | K2/K4 |
| 21 | listing/latest | R paged SemVer-2 versions, absent/false listed, numeric greatest independent of dates/constraints | K2/K4 |
| 22 | completeness | R missing page/bad count/unsupported candidate/conflicting alias/no listed stable fixtures | K2/K4 |
| 23 | used availability | R authorized unlisted/prerelease success; 404 package/absent version; archive URL never fetched | K2/K4 |
| 24 | versions | V leading zeros/omitted patch/zero and nonzero revision/prerelease case/build aliases/numeric order | K1/K2/K4 |
| 25 | metric | I 365.25-day delta, normalized identity exact zero, negative anomaly flag, measured-only aggregates | K3/K4 |
| 26 | source summaries | I missing/bad project vs missing/bad lock matrix, known N and null measurement without N failures | K3/K4 |
| 27 | availability | I valid empty/rejected empty/0-of-N/partial/full fixtures assert every S6 null/zero field | K3/K4 |
| 28 | compatibility | I Python/npm/Yarn/Ruby success alongside each NuGet failure; same-name ecosystems stay distinct | K3/K4 |
| 29 | JSON | O full/partial/rejected-stage presence/omission/null snapshots, schema 3, verbose equality and old-output equality | K3/K4 |
| 30 | correspondence | O parse human/JSON fixture facts and compare counts/identities/requests/states/dates/values/disclosures | K3/K4 |
| 31 | precedence/F2 | W/R table with one trigger per every S6 reason plus combined/reordered triggers; no ambiguity or mismatch selection fields | K1/K2/K3/K4 |
| 32 | no execution | S patched process/network/cache/config access guards, before/after input byte digests, offline full path | K1/K3/K4 |
| 33 | local bounds | S cap and cap+1 bytes/depth/count/digits, symlink inside/escape, FIFO/device/replacement/encoding fixtures | K1/K4 |
| 34 | network bounds | R/S wrong host/path/redirect/userinfo/HTTP/gzip bomb/truncation/page/request/time/429 budgets | K2/K4 |
| 35 | privacy | C/O/S secret canaries in XML/witness/origin/paths/errors/responses absent from stdout/stderr/JSON | K1/K2/K3/K4 |
| 36 | scope | S co-located assets/export/packages.config/CPM/private/multi-context/portfolio fixtures never supply fallback | K1/K3/K4 |

Maintain a reason-trigger table mechanically enumerating every S6 stable reason
and its test, including source/dependency distinctions and invalid-response vs
budget failures. Permute object/reference/page order with fixed responses and
injected clock; assert identical reasons, evidence, request schedule and summaries.
Tests accompany each component, not deferred to K4. Existing suites for metric,
registry, PyPI/npm, Yarn, Ruby groups, mixed scans, output and CLI are regressions.

## Phases and review gates

These are architecture phases, not tasks or implementation authorization.

1. Internal foundations: safe reads, project/lock/version/witness parsers,
   association and local authority with typed evidence. No public activation.
   Focused P/L/V/W/S and existing model/output compatibility tests. K1 fresh
   independent review must validate F1/F2, complete scope and no-call authority.
2. Public adapter: bounded transport opt-ins and registration/catalog traversal.
   Focused R/S and existing registry/PyPI/npm/Ruby regression suites; full offline
   suite at shared transport boundary. K2 fresh security/metadata review before
   public integration; no partial resource or latest shortcut is acceptable.
3. Coherent activation: CLI, fourth source pair, evidence transfer, serializers,
   human output and documentation together. README, SPEC, AGENTS ecosystem scope
   and CHANGELOG Unreleased Added describe the actual approved capability.
   Focused I/C/O plus complete deterministic suite and diff check. K3 independent
   integration review preserves siblings and entire S6/S7 matrices.
4. Final offline acceptance: all 36 concrete witnesses and reason triggers,
   adversarial full paths, compatibility suite and privacy/no-execution guards.
   K4 independent acceptance audit; full `python -m unittest discover -s tests`,
   `git diff --check`, no network or producer dependency.
5. K5 later real-root validation requires separate explicit target authorization;
   discovery's OASim paths grant none. Compare human/JSON scope, selection,
   origin/hash states, dates and arithmetic, and confirm target bytes unchanged.
   Environmental/live metadata failures remain separate from offline correctness.
   No archive, restore or hash-policy workaround; record hash-domain/coverage
   limitations. Live validation cannot replace a deterministic witness.
6. K6 fresh read-only convergence against approved spec/plan/tasks, code, tests,
   docs and validation evidence; resolve findings through separately authorized
   correction work. Reconcile completion/retrospective only after passing gates.

Each phase stops at its review gate. Later task decomposition should preserve
internal-only commits until coherent activation and one reviewable task per
commit; it is not created here. Full-suite repetition is reserved for shared
integration/phase boundaries, with focused tests first.

## Planning self-audit and limitations

All 36 ACs have explicit component/witness/checkpoint mappings above. H1 remains
lock-only; H2 preserves bounded explicit direct scope and qualified testimony;
H3 requires origin plus local/public hash binding; H4 uses catalog created and
complete listed-stable ordering. F1 and F2 have dedicated positive, negative and
precedence witnesses. S6 availability matches existing SourceResult and mixed
summary seams without changing sibling semantics. S7 stays additive in schema 3.

No assets/export product reader, packages.config fallback, dotnet/NuGet/MSBuild
execution, CPM/import/condition evaluation, multi-framework/RID interpretation,
transitive measurement, private-feed access, portfolio aggregation or metric
change is planned. Input bytes remain read-only. No third-party dependency,
database, server, package resolver or speculative generic framework is needed.
No consequential product feasibility gap has been established. Live metadata
yield and signed-content hash-domain fitness are unvalidated, retained evidence
limitations rather than a new policy decision. A future demonstrated inability
to honor H3/H4 must return to human authority, never silently redefine them.

Final helper names and fixture subdivision can be chosen in task decomposition;
all semantic boundaries, numeric limits, safe destinations and approval gates
above remain binding. Review verdict belongs in reviews.md so this candidate can
remain unchanged after reviewers are commissioned.
