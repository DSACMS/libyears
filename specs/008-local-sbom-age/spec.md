# Feature 008 — Local SBOM dependency-age population

## Authority and outcome

Run007-0048 selects **local CycloneDX-first dependency-age measurement**, independent
of any current-checkout join. This specification supersedes the inventory-only
shipping recommendation in [007-0047 discovery](../../discovery/sbom-corpus-feasibility.md)
for this new capability; it does not rewrite that historical evidence. Approval
and frozen revisions are recorded in [reviews.md](reviews.md). Planning, task
decomposition and implementation require separate authority after specification
convergence. Governing workflow, observation and publication rules remain in their
existing repository homes.

An ordinary directory scan can discover one existing local SBOM, report which
subject it describes, retain its component inventory and calculate conventional
Maven dependency ages for supported exact versions. **SBOM age** describes the
selected document's asserted component population. It is neither Declared nor
Observed, nor a current repository/build/runtime/deployment inventory. Its totals
must never be added to, substituted for or joined with either Maven view or legacy
ecosystem populations. No new Observed reader or join is authorized.

Initial scope: one document and one subject, CycloneDX JSON **1.5**, flat component
inventory, supported Maven purls, explicit optional dependency graph. No SPDX,
other CycloneDX versions/XML, other package ecosystems, hosted acquisition,
generation, target execution, archive inspection, remote schema/reference following
or automatic interpretation of producer-specific extensions. Missing publication
history remains a limitation of the unchanged Maven time basis, not a new research
question. An independently useful age report does not require a matching checkout,
producer attestation, Git tracking, clean state or acquisition/content proof.

## S1 — Invocation, discovery and selection

`python -m libyears DIRECTORY` discovers local candidates by default. New exact,
non-abbreviated options: `--sbom RELATIVE_FILE` selects exactly one existing file
within DIRECTORY; `--no-sbom` disables all SBOM discovery/intake/metadata work.
Repeated selection, both options together, URI/absolute/escaping/unsafe paths or
`--sbom` with a nondirectory positional input are sanitized argument errors,
exit1 before scans. `--no-sbom` is harmless on existing direct-file scans; those
never automatically activate SBOM. Existing options and exit conventions otherwise
remain. Examples here are prospective interfaces, not commands supported today.

Discovery uses deterministic root-relative name order, directory depth0–3 inclusive,
128 directories including root,10,000 entries inspected and16 matching candidate
entries. Match case-sensitive basenames `bom.json`, `sbom.json`, or suffixes
`.cdx.json`, `.cyclonedx.json`. Skip dot-prefixed entries and directories named
`node_modules`, `vendor`, `packages`, `venv`, `__pycache__`, `bin`, `obj`.
`target` and `build` are intentionally eligible: existing outputs may contain the
useful artifact. No scripts, manifests or package archives are read to find an SBOM.
Depth/exclusions define a disclosed search boundary, not proof of absence elsewhere.

Finish bounded discovery before automatically opening content. Exactly one safely
identified candidate in a complete discovery permits automatic selection. S2's
document framing/subject acceptance and S5's independent comparator gate must then
pass; basename/colocation alone grant neither history nor current association.
Two or more candidates require explicit selection, even if contents/digests appear
equal or only one looks supported. No merging, newest-file preference or fallback
to a different candidate after refusal. Incomplete discovery, cap exhaustion or an
unsafe matching candidate prevents automatic selection. Explicit `--sbom` bypasses
candidate discovery, permits other names/depths within the same safety/byte limits,
and resolves document ambiguity, never semantic ambiguity inside a document.

Complete discovery with no candidates omits SBOM output. Ambiguous, incomplete,
unsafe or unsupported discovery has a concise SBOM status without fabricated rows
or counts; independent sources continue. A selected unavailable/malformed document
is a reportable SBOM source failure, exit0 with useful sibling output, not an
argument error or an empty successful population. Systemic failures retain existing
exit2 behavior. No hosted acquisition option, GitHub API, credential lookup or
remote inference is introduced. Local intake may lead to existing public registry
requests **only after S5**; it does not promise fully offline age calculation.

## S2 — Bounded acceptance and parsing

Read one stable regular-file byte snapshot, maximum8MiB, UTF-8 without BOM, exactly
one JSON object. Reject duplicate object member names anywhere, nonfinite numbers,
malformed/trailing JSON, invalid Unicode/unpaired surrogates and over-budget framing
before accepting population or enabling HTTP. Validate the entire framing, including
ignored fields. All parsed data remain inert. Do not use document schemas, URLs,
file paths, signatures or external references as instructions.

| Bound | Ceiling / refusal scope |
| --- | --- |
| JSON nesting / total value and member-name tokens | 32 containers / 250,000 tokens; reject whole source on overage |
| String / number / object / array | 16KiB UTF-8 per string or key,128 characters per numeric literal,256 members/object,20,000 items/array; whole-source refusal |
| Inventory | 10,000 component entries,1,000 service entries; limits count before root exclusion or deduplication |
| Graph | 11,001 dependency-node entries and50,000 edge entries, including duplicates before validation |
| Identity / references | Maven lexical limits from Feature007 B2; purl2,048ASCII characters; bom-ref1–1,024 UTF-8 bytes; document labels128ASCII characters |
| Paths | Existing safe relative-path lexical bound1,024 characters/32 components; explicit selection cannot escape root |

Root and every accessed path component must have race-resistant no-follow binding;
reject symlinks, ancestor links, reparse/junctions, devices, sockets and FIFOs.
Verify directory bindings and file identity before/open/after bounded read; mutation,
unsafe type, unavailable required primitives or read errors refuse affected intake.
Do not inspect ancestors outside DIRECTORY, machine config, caches or trust stores.
Explicit selection does not weaken file safety. These are behavioral safety
requirements; implementation mechanism belongs to the later plan.

Require `bomFormat="CycloneDX"`, `specVersion="1.5"`, `metadata.component` as one
subject object with bounded nonempty string `name` and `bom-ref`, and an explicit `components`
array (empty permitted). `version`, if present at document level, is an integer>=1,
not boolean; absent means1. Serial UUID and timestamp are optional assertions, not
acceptance/history requirements. The subject need not have a Maven identity/version.
Producer names may be absent. No repetitive human testimony is needed for these
encoded facts. No acceptance claim of full CycloneDX schema conformance is made.

Supported root fields are the1.5 schema fields `$schema`, `bomFormat`, `specVersion`,
`serialNumber`, `version`, `metadata`, `components`, `services`, `dependencies`,
`externalReferences`, `compositions`, `vulnerabilities`, `annotations`, `signature`,
`properties`, `formulation`. Known descriptive/security fields are inert bounded
data; unknown root fields refuse this subset. Only top-level components are the
inventory: a nonempty nested `components` array on subject or inventory component
refuses the source as `sbom_nested_population_unsupported`, rather than silently
discarding or flattening an assembly. Metadata tools, pedigree components, services
and vulnerability evidence never create dependency rows. A non-object component
entry or malformed relevant container refuses source framing. Malformed identity
scalars on an otherwise framed component produce a visible unmeasurable row.
Services are separately counted and excluded from numerical population; they may
be graph vertices. Compositions can retain supplied completeness assertions, never
certify completeness beyond this document or add omitted components.

## S3 — Population identity and relationships

Population basis: `sbom_asserted_unique_component_versions`. Accept all top-level
component objects except the subject alias; do not filter by Maven directness,
CycloneDX scope, graph reachability or successful measurement. Retain unsupported
ecosystems/types and missing identities as unmeasurable members. Thus the known
inventory denominator describes the accepted finite document projection, not all
dependencies that the producer might have omitted.

A supported component's package identity is case-sensitive `(group, artifact,
version, type, classifier)` after S4's specified defaulting only. Different exact
versions are distinct inventory members, not automatically a contradiction.
No Maven ComparableVersion equivalence, type-handler alias or local module
occurrence may deduplicate them. Identical supported identity tuples under distinct
references collapse to one package row with reference/record multiplicity retained;
union their encoded edges and restrictions, and never use one alias to bypass
another alias's refusal. A safely framed but unidentifiable record has its own
document-array-index member; do not deduplicate unknowns by name or invent a version.
Known identity/version field conflicts remain unmeasurable index members.

Every supplied bom-ref across subject/components/services must be unique and
nonempty. Exception required by the corpus: one top-level entry may repeat the
subject's bom-ref **only when that complete component object equals
metadata.component**; exclude it once as a subject alias. Any other repeated ref,
including conflicting versions under one ref, refuses the whole source:
`sbom_duplicate_reference`. Absent component refs are permitted for inventory,
using stable internal index identities; they cannot acquire graph relations by
coordinate/name matching. Subject never contributes an age or an inventory member.

Graph objects accept only `ref` and optional `dependsOn`. Each ref must identify
one accepted component, subject or service; repeated graph-node refs, duplicate
edges, dangling or external/BOM-Link refs make **graph evidence unavailable** with
a fixed reason. Keep accepted inventory and ages independent; do not repair graph
ambiguity or follow a reference. A missing graph, absent vertex entry or absent
dependsOn means that vertex's dependencies are unknown; explicit empty dependsOn
is a supplier assertion of no represented children, not completeness proof.

When graph evidence is valid, classify component refs relative to the selected
subject: `direct` if a subject edge names the ref; otherwise `transitive` if a path
of length>=2 reaches it; otherwise `unknown`. A direct edge takes presentation
precedence if another transitive path also exists; retain both path-presence flags.
Finite visited-set traversal supports cycles, which are flagged; cycles neither
add counts nor imply module occurrences. Services can connect paths but never
gain package rows. Component nesting, `scope`, licenses and component type are
not graph edges. Unreachable inventory stays included with relationship unknown,
not falsely “not a dependency.” For collapsed package rows, union ref relationships;
direct takes precedence, then transitive, then unknown. Graph failure makes all
relationships unknown except the excluded subject; it does not null known N.

## S4 — Supported Maven identity and version facts

Require a literal Maven purl `pkg:maven/GROUP/ARTIFACT@VERSION`, with exactly one
group/name path separator, no URI authority or subpath. Initial identity path atoms
are unescaped ASCII satisfying Feature007 B2 lexical safety; percent-encoded path
atoms are unsupported, not normalized into a new spelling. No case-folding,
property expansion, range resolution or name guessing. Component `group`, `name`
and `version` must be safe scalar strings and exactly agree with the purl; missing
version or purl remains a visible refusal. No purl-only repair of conflicting or
missing component fields. A bare component G/A/version without purl is inventory,
not initial lookup authority.

Initial qualifiers: `type` absent defaults to `jar`, or literal `jar`, `pom`, `war`;
`classifier` absent is null or one nonempty safe literal Feature007 atom. Explicit
empty/repeated qualifier, unsupported type/qualifier, malformed percent escape or
subpath refuses measurement. No handler execution/alias inference; custom types
and test-jar await separate scope. Preserve original purl and explicit/default type
state privately, expose only its safe parsed identity and variant in output.
`repository_url` is additionally recognized **as a restriction**, under S5, not
part of package identity or a lookup endpoint. Qualifier ordering does not create
duplicate identity. Parse qualifier keys literally once; percent-decode only
repository_url once as UTF-8 under2,048 characters, never form-decode `+` as space.
Other qualifier values use the literal safe atom grammar.

Version admission reuses Feature007 exact lexical, finite ordering and snapshot
rules. Missing versions, ranges, dynamic LATEST/RELEASE, property expressions,
SNAPSHOT and timestamped snapshots never become exact ages. A supported exact
non-SNAPSHOT used version need not itself pass the conservative latest-stable
eligibility filter: preserve the existing used-versus-latest distinction.
This is `sbom_asserted_component_version`, not a declaration, installed state or
guaranteed dependency-system resolver selection. Producer/build associations are
retained assertions, never automatically upgraded to producing-history assurance.

## S5 — Conventional comparator, dates and failure isolation

Use the existing fixed Central comparator convention, not an inference that a
purl proves namespace/public acquisition. A structurally accepted safe Maven
identity can use `sbom_maven_central_convention` when available relevant evidence
does not contradict it. Disclose assumed correspondence, possible undisclosed
private same-ID/version forks, coordinate disclosure to Central and absence of
acquisition/content/current-checkout proof. This adaptation accepts the document
population as the comparison subject: an unbound release SBOM needs no local POM
or namespace testimony before its own age report can be useful.

Before any coordinate leaves the process:

- A supplied repository_url must decode to exactly Feature007 B3's recognized
  public Central identity; other/ambiguous/unsafe values refuse comparison. It
  positively points this purl at another namespace; do not query a public namesake.
- Nonempty producer-specific properties, component evidence/pedigree, or
  `modified=true` are initially unsupported relevant correspondence semantics
  for affected components; retain inventory and refuse measurement. A restriction
  on the subject, document properties, metadata properties or nonempty formulation
  applies to every component. Unknown
  qualifier/source semantics never become implicit public lookup permission.
- Standard website/VCS/issue/build/distribution-intake references, supplier names,
  publisher, licenses and hashes alone establish neither private assignment nor
  public assurance. Standard `distribution` links are unassigned availability,
  not proof of acquisition; alternate eligibility alone does not veto convention.
  None of those URLs is requested. Any already-established positive private,
  conflicting or unknown namespace assignment for the same G/A in this invocation
  vetoes the SBOM comparison; a weaker alias cannot overrule it. Explicit local
  Central exclusions known for that identity likewise refuse before HTTP. No
  extra repository scan or current-checkout join is undertaken to invent either
  applicability or a negative proof; unknown evaluated/machine history is a
  disclosed limitation, not a fabricated source decision.

Use existing Maven ordering3.9.11, conservative latest policy, whole GA catalogue
selection, fixed-host trusted isolated metadata worker, verified TLS and POM identity
checks from [Feature007](../007-maven-dependency-age/spec.md#s7--maven-comparator-evidence-cascade-and-conventional-time-basis).
No new package-age lookup occurs during this specification run. Date basis remains
`maven_conventional_pom_last_modified`, at GAV POM-representation granularity, never
classifier-specific availability or first publication. SBOM timestamp, hashes,
VCS/release dates and file mtime never substitute. Exact same-version zero requires
the existing accepted latest and supported identity-bound time evidence; no offline
or missing-date shortcut. Clamp timestamp inversions only with the existing flag.

SBOM has its own finite metadata allowance no greater than Feature007's300 attempts,
64MiB and existing deadline/transport bounds, after ordinary sources have finished
their work. It cannot consume their budgets, revoke their results or read worker
state/config from them. No sharing of lookup authority: reuse of metadata bytes,
if later planned, must follow each row's independent admission. Order SBOM work by
safe canonical identity then index; exhausted/failed work retains all inventory
and completed ages, with stable per-row reasons. No target execution or resolver.

When offline or provider/worker/time evidence is unavailable, keep every inventory
row and its supported exact fact; age is null with a reason. No new global offline
flag or sibling transport-policy change is specified. Users can disable the SBOM
source entirely with --no-sbom. Measurement failure is never freshness or absence.

## S6 — Counts, coverage and arithmetic

For an accepted inventory let N be unique component-version members under S3,
including unsupported/unmeasurable index members; M counts rows with supported
age results, including exact0.0. Return inventory record count before deduplication,
subject aliases excluded, service count excluded, N, supported-exact count, M and
reason counts separately. Document completeness outside the accepted projection
is always `unknown`; even a producer's complete composition assertion does not
make repository/build coverage known. Relationship direct/transitive/unknown counts
partition N using S3; graph-unavailable makes unknown=N.

Coverage is M/N for N>0, labeled **SBOM population age coverage**, independent of
unknown real-world/document completeness. N=0 gives M=0, coverage=null (empty),
total0.0 and mean/median/max null. Accepted N>0 with no measured rows gives M=0,
coverage0.0,total0.0 and mean/median/max null, explicitly an empty measured subset.
Source-level refusal or no selection gives N/M/coverage/all numerics null, never
complete-empty output; no accepted prefix survives malformed whole-document framing.

Use unchanged365.25-day arithmetic and raw unrounded row ages for sum/mean/median/
max. Each deduplicated package-version-variant row contributes once, irrespective
of graph indegree, repeated paths, cycle count or local module usage. Distinct
classifiers/types remain distinct inventory members with the GAV time limitation.
Report measured-subset totals only; do not promise new measured counts or a
complete denominator from the corpus. Independent SBOM and repository results
may disagree without a same-context contradiction; do not overwrite either.

## S7 — Ordinary, verbose and JSON output

Ordinary output must answer subject/source, accepted population, measurable exact
versions, measured-subset ages and visible refusals. Use an independently headed
**SBOM dependency age** section with safe root-relative selected filename, format,
subject label, inventory basis, N/M/coverage/total/mean/median/max and the conventional
time/namespace/current-checkout limitations. For SBOM-only sources, lead with it
rather than an empty legacy0/0; otherwise preserve independent existing tables and
label their summaries as their existing direct-source populations.

Use the existing aligned-table style: `DEPENDENCY  VERSION  RELATION  LATEST
LIBYEARS  SOURCE`; SOURCE is concise `SBOM` with document attribution in the
heading. Identity includes supported nondefault type/classifier. Unknown versions
render `unavailable`, ages `unavailable`; a separate aligned **Unmeasurable** table
with `DEPENDENCY VERSION REASON` retains every refused inventory member, including
unsupported ecosystems and hostile/missing identities represented by a fixed
`component #INDEX` placeholder. No repeated unavailable Observed column per row.
All values are escaped before column measurement; no raw terminal controls, URLs,
absolute paths, free-form diagnostics, contact identities or arbitrary descriptions.

Verbose and JSON preserve document SHA256 (exact snapshot bytes), safe source ID,
selection mode, format/version, optional safe serial/timestamp, sanitized producer
name/version, subject, version basis, canonical member identities, multiplicities,
relationship/path flags and internal graph edges, graph status/reasons, composition
assertion status, eligibility/comparator/time bases, retrieval timestamps, measured
POM timestamps, anomaly flags, limitations and fixed refusal reasons. Raw bom-refs
can contain paths/URLs: replace them consistently with opaque document-local IDs,
retain reference equality/edges, never echo raw supplier paths/URLs. Unrepresentable
safe labels become null/placeholders with `redacted` status, not whole-source loss.
Timestamp/serial assertions that fail their bounded syntax are withheld with a
status; they cannot change measurement or repair identity conflicts.

Schema **3** remains: add an independent optional top-level `sbom` section with
`format_version:1`. Existing `dependency_scope:"direct"`, ecosystems, version_evidence,
legacy summaries/arrays/source_errors and the Maven section retain their exact
meaning and values. SBOM never adds a legacy source error or an ecosystem merely
by listing it. Its own `scope:"sbom_asserted_unique_component_versions"` and
`legacy_fields_exclude_sbom:true` make the boundary explicit. With SBOM absent or
disabled, existing output is unchanged. Dropping `sbom` from new JSON must reproduce
the same-input old projection, subject only to separately acquired live metadata
variation; deterministic compatibility witnesses freeze those responses.

The normative field names, complete nested structures, enum/null behavior,
source-failure attribution, reason counts and representative JSON witnesses are in
[output-contract.md](output-contract.md). That companion is part of this
specification, not a deferred planning decision. No declaration/Observed fields or
source/module occurrence key appear in SBOM rows. Accepted inventory with any row
refusal or unavailable graph is partial; unknown graph alone is not failure.

Evidence for this compatibility decision is in [evidence.md](evidence.md): actual
schema3 already accommodates independent Maven results. We do not insert inventory
into classes requiring Declared/Observed bases, reinterpret legacy direct scope or
claim all strict consumers tolerate new keys. Such consumers may reject this
additive section; an intentional schema4 migration is not needed to preserve the
existing field contracts. This is an output contract, not an implementation plan.

## S8 — Stable failures and acceptance witnesses

Source reasons: `sbom_discovery_unavailable`, `sbom_selection_required`,
`sbom_input_unavailable`, `sbom_input_unsafe`, `sbom_input_changed`,
`sbom_budget_exceeded`, `sbom_invalid_json`, `sbom_unsupported_format`,
`sbom_subject_unavailable`, `sbom_nested_population_unsupported`,
`sbom_duplicate_reference`. Graph reasons: `sbom_graph_invalid`,
`sbom_graph_unknown`. Row reasons: `sbom_identity_missing`,
`sbom_identity_conflict`, `sbom_identity_unsupported`, `sbom_version_missing`,
`sbom_version_unsupported`, `sbom_variant_unsupported`,
`sbom_comparator_refused`, `sbom_policy_unknown`, plus unchanged applicable Maven
catalogue/worker/budget/time-basis reasons. Precedence: whole framing/safety before
subject/population; row identity before version before variant before comparator
before metadata. Preserve reason counts and actionable fixed remedies: select one
file, supply a supported complete document, correct identity, obtain exact versions,
or retry registry availability; never suggest running a target build as consumption.

All following are **required future implementation witnesses**, not passed tests
or live age measurements in this specification run:

| AC | Required behavior / evidence |
| --- | --- |
| AC01 | Ordinary directory finds exactly one supported document; explicit unusual-name selection works; disable performs zero SBOM reads/lookups; ambiguity/caps refuse autoselection; nondirectory and malformed options stay scoped |
| AC02 | Exact retained Dependency-Track4.13.4 bytes admit201 component records, one subject alias excluded,200 unique external Maven members,21 excluded services; all200 root-reachable,43 direct and157 transitive; no promised age M |
| AC03 | Release POM's57 literal direct declarations/14 omitted tests remain a separate historical comparison; no57- or43-based SBOM denominator, local occurrence weighting, join or Observed reader appears |
| AC04 | Frozen positive metadata responses for a representative real corpus component yield a conventional age with correct identity, dates, latest policy and arithmetic; missing dates even for equal versions never produce unsupported zero; no target tool needed |
| AC05 | Entire source malformed/unsafe/oversized/nested/duplicate-ref fails with null N; safe siblings unchanged. Late malformed JSON in ignored data cannot permit earlier network requests |
| AC06 | Duplicate package tuples under distinct refs count once; restrictions union; distinct versions/variants count separately; missing/conflicting fields remain visible index rows; no cross-document merge |
| AC07 | Missing/partial graph, explicit empty children, cycles, service-mediated paths, unreachable nodes, both direct/transitive paths and dangling/duplicate edges produce S3 labels/status without losing independent inventory ages |
| AC08 | Purl field mismatch, percent path, empty/repeated/unknown qualifier, custom type, ranges and snapshots refuse only supported dependent scope; Central qualifier recognition never changes HTTP destination |
| AC09 | Positive private/conflicting/unknown namespace and known applicable Central exclusion refuse before lookup; unassigned alternate references alone do not veto; no local POM/attestation required for standalone inventory-age success |
| AC10 | Offline/worker/provider/budget failure retains N/exact facts and safe completed ages; SBOM cannot consume ordinary-source allowances or change sibling projection; M=0 differs visibly from source unavailable and empty inventory |
| AC11 | Ordinary output has aligned measured and refused tables, source/subject and summary; no repeated Observed fields; verbose/JSON recover detailed safe evidence, no controls/paths/URLs/credentials leaked |
| AC12 | Frozen response projection equality covers absent/disabled/positive/refused SBOM, SBOM-only, Maven Declared/Observed, and each Python/npm/Ruby/NuGet sibling, including unknown/empty populations; schema3 meanings stay intact |
| AC13 | Retained non-GitHub full CPython SPDX and checked-in partial fragment refuse unsupported format; GitHub SPDX does likewise. Non-GitHub CycloneDX release is the positive witness; no exporter-specific assumptions define intake |
| AC14 | Race/link/reparse/special-file/capability refusal and all byte/token/string/graph limits are exercised offline; external refs, schemas, service endpoints and embedded paths cause zero retrieval/execution |

No CMSgov/DSACMS SBOM is present in the retained007-0047 corpus; earlier bounded
candidate metadata supplies a hosted lead, not an accepted local artifact. That
optional adoption witness does not block convergence. Do not restart repository
inspection or require a new SBOM generation to satisfy this specification.
