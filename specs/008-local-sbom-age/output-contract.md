# SBOM JSON extension version 1

Normative companion to [spec.md S7](spec.md#s7--ordinary-verbose-and-json-output).
This defines the optional `sbom` member of schema3. It does not redefine the legacy
direct-scope fields. No implementation or generated product output exists yet.
All keys below are required unless explicitly optional; nullable means JSON null.
Reason strings are the closed vocabulary in spec S8. Arrays contain no null entries.
Unknown future extension keys are not asserted compatible with strict consumers.

## Envelope, selection and failure attribution

| Key | Type and values |
| --- | --- |
| format_version | integer1 |
| scope | `sbom_asserted_unique_component_versions` |
| legacy_fields_exclude_sbom | true |
| state | available / partial / unavailable under spec S7 |
| reason | first source failure reason when unavailable; otherwise null (row/graph reasons live in their records) |
| discovery | object defined below |
| selection | object defined below; survives refused document intake |
| document | accepted document object below, or null |
| population | accepted population object below, or null |
| summary | existing seven numeric/null statistic keys, defined below |
| components | array of component objects; empty on source refusal |
| graph | object below; retained even if graph unknown |
| reason_counts | `{source:array, components:array, graph:array}` of `{reason:string,count:integer>=1}`, sorted by reason; count unique member refusals after deduplication; each nonnull source/graph reason contributes1; absent reasons give empty arrays |
| limitations | ordered fixed code array below; never supplier strings |

`discovery` has exactly `mode` (automatic / explicit), `state` (complete /
incomplete / bypassed), `candidate_count` (observed matching entries integer>=0,
null when bypassed), `search_complete` (true / false, null when bypassed) and
`reason` (null or sbom_discovery_unavailable). Explicit mode is bypassed; ambiguity
is a complete discovery plus source reason sbom_selection_required. An incomplete
count is only an observed prefix, not a candidate denominator. Disabled/absent SBOM
has no extension at all; no disabled mode is needed.

`selection` has `mode` (automatic / explicit), `state` (selected / required /
unavailable), and nullable `source_id`. Selected means one safe lexical relative
path was chosen, not accepted content. It retains the path if later bytes are
missing, malformed or refused. Ambiguity gives required/null; incomplete or unsafe
automatic discovery gives unavailable/null. Explicit lexical option errors have no
report. Source_id must satisfy spec path safety and be escaped in JSON; no absolute
path/URI is emitted. `document.source_id`, when present, equals selection.source_id.

All summary keys are `dependencies_discovered`, `dependencies_measured`, `coverage`,
`total_libyears`, `mean_libyears`, `median_libyears`, `max_libyears`. First two are
nonnegative integers or null; others finite nonnegative numbers or null. Coverage
is in[0,1]. S6 defines N/M/empty/unavailable rules. Source refusal has all seven null,
document/population null, components empty; any safe selected-file identity remains
in selection. Reason counts distinguish whole-source failure from row failures.

## Document and safe assertions

`document` has `source_id`, `sha256` (64 lowercase hex of exact bytes),
`format:"CycloneDX"`, `spec_version:"1.5"`, `document_version` (integer>=1),
`serial_number`, `created`, `producer`, `subject`, `compositions`. Format validation
precedes this object; refused format does not populate it. Serial and created are
assertion objects `{value:string|null,status:available|absent|invalid|redacted}`.
Serial accepts exactly lowercase `urn:uuid:8-4-4-4-12` hexadecimal UUID syntax.
Created accepts an ASCII valid RFC3339 timestamp with seconds, at most6fractional
digits and Z or numeric timezone, normalized to UTC Z; otherwise invalid/null.
Neither supplies a package date. An absent assertion is absent/null; bounded valid
but unsafe display content is redacted/null, never silently copied.

`producer` has `state` (available / absent / redacted), `tools` (array) and
`tools_omitted` (nonnegative integer). Accept1.5 metadata.tools legacy array of tool
objects or object.components tool array; absent means absent/[]/0. Project only
name/version as `{name:string|null,version:string|null,status:available|redacted}`.
At most32 entries are displayed, in input order, with omitted count retained.
Malformed producer-only shapes give redacted/[]/0; never a lookup grant or lost
inventory. Unsafe strings become null and tool status redacted. Producer state is
redacted if any tool is redacted/omitted, available otherwise, absent if none.
Tool components never become inventory or graph vertices.

`subject` has `id:"subject"`, `name` (safe display string or null),
`name_status` (available / redacted), `identity` (nullable canonical identity below).
Its structurally required raw name need not be displayable. This explicitly resolves
the distinction between accepting bounded subject framing and withholding a hostile
label; a fixed subject placeholder still identifies the selected document's root.

Safe display strings are1–128 printable ASCII characters, without slash/backslash,
`@`, shell/terminal control characters or URI-prefix syntax; escape quotes before
rendering. Never output raw URLs, contact details, descriptions or diagnostics.
Canonical Maven fields use the narrower spec S4 grammar. Subject/unsupported labels
with unsafe content become null or fixed `component #INDEX` placeholders, with a
redacted status. Canonical identities are not reconstructed from redacted labels.

`compositions` has `state` (absent / asserted / unsupported), and `aggregates`
(array). Project only1.5 compositions[].aggregate enum values:
complete, incomplete, incomplete_first_party_only, incomplete_third_party_only,
unknown, not_specified. Sort/deduplicate enum strings; ignore no new completeness
inference. Empty/absent compositions gives absent/[]; unknown enum or malformed
composition-only shape gives unsupported/[]; otherwise asserted/values. Composition
references/assemblies do not create rows or graph edges. Unsupported composition
assertions remain a limitation, not whole-source or age failure.

## Members, counts and graph

Canonical `identity` is exactly `{group_id,artifact_id,version,type,classifier}`:
first four strings, classifier string or null, satisfying S4 (including supported
type). It is null when that supported tuple cannot be established. A nullable safe
component version may be retained separately even if identity is missing/conflicting;
it never grants lookup authority. supported_exact counts nonnull supported tuples
with a supported exact non-SNAPSHOT version, irrespective of later policy/date refusal.

`population` keys: `basis` (same string as scope), `inventory_records` (top-level
component objects before dedup, after subject alias removal), `subject_aliases_excluded`
(0 or1), `services_excluded` (nonnegative integer), `members` (N), `supported_exact`,
`completeness:"unknown"`, `relationships:{direct,transitive,unknown}` integer counts
which sum to N. Services and subject do not count as members. sum(component.record_count)
equals inventory_records; component array length equals N, including per-index
unidentifiable members. These are document counts, not repository coverage.

Each member has exactly `id`, `identity`, `label`, `label_status`, `version`,
`version_basis:"sbom_asserted_component_version"`, `record_count`, `reference_ids`,
`relationship`, `direct_path`, `transitive_path`, `age`, `reason`.

- IDs are `component-N` from the smallest zero-based source array index in the
  collapsed member. Unsupported index records use their own index. Order members
  by that index. Safe label is canonical `group:artifact` when available, otherwise
  safe raw name, otherwise `component #N`; label_status available/redacted.
- record_count>=1. Reference IDs are opaque `component-ref-N` for the underlying
  array indices with supplied refs, sorted numerically; absent refs add none.
  Subject alias adds none. Raw reference strings never leave the process.
- relationship is direct/transitive/unknown, under S3. For a valid graph the path
  booleans indicate represented subject paths of length1 or>=2 respectively;
  direct takes label precedence. If graph state is unknown/unavailable, both flags
  are null and relationship unknown. Unreachable valid-graph rows have false/false.
- age is null exactly when reason is nonnull. Each reason is a fixed S8 row reason;
  reason_counts.components counts one reason per member. For a successful age,
  component.version equals identity.version and reason=null. Unsupported/version-
  conflicting members retain no fabricated target/date/libyear value.

Age fields are exactly `comparison_version`, `measured_version_pom_last_modified`,
`comparison_version_pom_last_modified`, `libyears`, `timestamp_order_anomaly`,
`catalogue_retrieved_at`, `comparator_basis`, `time_basis`, `ordering_basis`,
`eligibility_policy`, `limitations`. All timestamps are identity-bound UTC Z;
catalogue retrieval timestamp is required for a successful age. Bases:
sbom_maven_central_convention, maven_conventional_pom_last_modified,
maven_comparable_version_3_9_11, maven_conservative_stable_v1. Numeric/flag semantics
reuse Feature007; age limitations include publication_history_not_established and
variant_availability_not_established. These do not imply actual public acquisition.

`graph` keys are `state` (available / unknown / unavailable), `reason`, `subject_id`,
`vertices`, `edges`, `cycles_present`. For an accepted document subject_id="subject";
source refusal uses null. Unknown state means absent graph with reason
sbom_graph_unknown, vertices/edges=[], cycles_present=null. Unavailable graph means
invalid graph evidence with reason sbom_graph_invalid and the same empty arrays/null;
no unsafe partial edges are emitted. Available graph has null reason, boolean
cycles_present, and every identified subject/component/service vertex (including
vertices omitted from dependency entries).

Exception for whole-source refusal/unselected input: graph is unknown with
reason=null, subject_id=null, empty vertices/edges and cycles_present=null. This
does not invent an additional graph failure for a document never accepted.

Vertices: `{id:string,kind:subject|component|service,member_id:string|null,
dependencies_known:boolean}`. IDs are subject, component-ref-N, service-ref-N
(service array index); absent service refs create no vertex. Member_id links each
component reference to its canonical row; null for subject/services. dependencies_known
is true only for an explicit graph node with a dependsOn array, including empty.
Edges are `{from:string,to:string}`, sorted by from then to in lexical opaque-ID
order, each once; all endpoints must be vertices. Vertices sort lexically by id.
No coordinates substitute for missing refs. Relationship computation precedes alias
collapse, preventing unioned package edges from manufacturing new paths.

Top-level limitations always include `sbom_supplier_assertions`,
`sbom_completeness_unknown`, `current_checkout_association_not_established`,
`resolved_direct_population_not_established`, `runtime_deployment_not_established`,
`central_correspondence_assumed`, `coordinate_disclosure_for_admitted_lookups`,
`acquisition_content_not_established`, `publication_history_not_established`,
`variant_availability_not_established`. Add `sbom_graph_unknown` or
`sbom_graph_invalid` for those graph states, `sbom_composition_unsupported` for an
unsupported composition assertion and `sbom_assertion_redacted` when any document
or member display assertion is withheld. Sort/deduplicate codes lexically.

## Representative contract witnesses

[accepted.json](examples/accepted.json), [partial.json](examples/partial.json) and
[refused.json](examples/refused.json) are complete `sbom` **section objects**, not
complete legacy schema3 envelopes. They are synthetic specification fixtures with
controlled metadata dates, fictitious G/A versions and digest placeholders; they
are not evidence of real corpus availability or measured ages. Examples use a
single-member synthetic document; they do not change the real200-member witness.

Accepted demonstrates N=M=1 and one365.25-day age; partial keeps the same exact
inventory/version with unavailable metadata, M=0/coverage0 and a visible reason;
refused preserves explicit safe source attribution while all population/statistics
are null. Future AC11/12 must embed these shapes alongside unchanged legacy fields.
