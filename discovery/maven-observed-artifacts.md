# Retained Maven Observed evidence — 007-0046

**Discovery only. Recommend dependency-plugin JSON tree as the first format to
qualify; defer reader specification until an existing real export and its binding
context are supplied.** No reader, acceptance route, CLI or schema is approved here.
Consuming an export must require only libyears/Python, without Maven, Java, Gradle
or wrappers. Producing it is a separate workflow and authority; nothing was generated.

## Settled boundary

Starting HEAD `573e9b78a06f7e8951b212a841d58e678e0a1c2a` was clean.
The [approved contract S1/S2/S5](../specs/007-maven-dependency-age/spec.md#s5--observed-evidence-and-availability)
already defines Observed as an exact retained dependency-system selection,
independent of declarations and runtime. Its accepted-format, same-input/context,
directness and unambiguous occurrence association requirements remain binding.
This discovery recommends a future narrow claim; it does not reopen those decisions.

The [configured validation](../maintenance/maven-external-intake/configured-validation.md#007-0045-resumed-configured-validation--completed)
remains closed: 54 measured Declared occurrences, raw15.479713793190864,27 zero ages,
73 visible refusals (39 version,32 model,2 catalogue), unknown complete population/
coverage and independently unavailable Observed. All47 historical measurements
survived; seven managed occurrences added1.7480593264380053, while fresh catalogue
observations changed existing comparisons by0.3295578877988186. No validation was
rerun, no totals combined and no Declared refusal recovery is promised here.

## Actual availability and limits

The [prior repodive](java-ecosystem-repodive.md#portfolio-and-revision-inventory)
identified no committed Maven selection snapshot. Its AB2D Gradle locks and DPC
vendored metadata are different evidence; neither is a Maven direct-selection
export. BFD's hosted SBOM link is a lead, not a retained bound artifact.

This run confirms public origin identity before candidate inspection. All seven
candidates remain at the exact revisions in that prior inventory, clean before
and after. The search reads filenames, not application source: full bounded tracked
path lists (maximum10000 paths each), plus a no-link shallow filesystem inspection
(depth0–3,128 directories/10000 entries per candidate). Git revision/status/index,
tracked-inventory digest and bounded entry identities agree before/after. No matching
candidate content was read because the search found no plausible export filename.

| Public CMSgov candidate | Tracked paths | Shallow entries inspected | Shallow directory cap hit | Plausible exports |
| --- | ---: | ---: | --- | ---: |
| ab2d | 1410 | 537 | no | 0 |
| beneficiary-fhir-data | 4466 | 902 | yes | 0 |
| cms-bb2-java-sdk | 7 | 15 | no | 0 |
| dpc-app | 2309 | 694 | yes | 0 |
| nimbus-pub-code-scanning-1 | 17 | 22 | no | 0 |
| nimbus-pub-github-action-poc | 17 | 21 | no | 0 |
| qpp-conversion-tool | 677 | 218 | no | 0 |

Filename patterns cover dependency tree/list/report/graph/snapshot/resolved names,
SBOM/CycloneDX/SPDX, `bom.json/xml`, `dependencies.json/txt/xml/dot/graphml/tgf` and
dependency-tree/list variants. No links are followed; Git/machine caches and vendor
or environment directories are excluded. These are **8903 tracked paths and2409
shallow entries**, not an exhaustive content search. Arbitrarily named files,
deeper ignored outputs, skipped directories and remotely retained CI artifacts
remain unknown. No hosted artifact service was contacted. A checked-in CI recipe
or a hosted link would not prove that an export was retained or bind its contents.
There is **no real proving-ground export available within these bounds**.

## Focused format comparison

| Candidate | What it can represent | What it does not establish alone | Disposition |
| --- | --- | --- | --- |
| Dependency-plugin JSON tree | Hierarchical project/dependency nodes, G/A/V, type/classifier, scope and optional value | Consumer path/context, production options, current input binding, mediation state or collection completeness | Best first qualification target; one known producer version/mode, explicit acceptance |
| Retained text tree | Coordinate edges, depth and potentially omission/conflict annotations | Stable grammar across tool versions, logging/token sets, intact framing or accepted module association | Defer; more parsing ambiguity than JSON |
| `dependency:list` | Resolved artifact list; scope and classifier options | Directness by default, graph edges, unique source binding or completeness | Defer; transitive exclusion/options require independent production evidence |
| CycloneDX1.6 SBOM | Components and explicit dependency edges by references; composition metadata | Maven selection provenance, original model type/key, Maven scope/optionality or module directness merely from component presence | Defer generic SBOM reader; a pinned Maven producer would need separate qualification |
| SPDX2.3.1 SBOM | Packages plus typed relationships, including dependency relationships | Selected Maven graph, complete relationships or a unique Maven model-key mapping | Defer; generic package inventory is insufficient |
| Effective POM, dependencyManagement catalogue, vendored POM/JAR, Gradle lock, CI recipe | Expanded requests, management, content/inventory, another system's selection, or instructions respectively | Bound Maven direct-selection evidence | Not substitute Observed authority |

References: official [tree format examples](https://maven.apache.org/plugins/maven-dependency-plugin/examples/tree-mojo.html),
[tree parameters](https://maven.apache.org/plugins/maven-dependency-plugin/tree-mojo.html),
[list parameters](https://maven.apache.org/plugins/maven-dependency-plugin/list-mojo.html),
[CycloneDX1.6 dependencies/compositions](https://cyclonedx.org/docs/1.6/json/#dependencies),
and [SPDX2.3.1 relationships](https://spdx.github.io/spdx-spec/v2.3.1/relationships-between-SPDX-elements/).
Current plugin parameter pages describe3.11.0; they are comparison documentation,
not proof of identical3.8.1 behavior. CycloneDX dependency edges differ from component
nesting and `provides`; absent graph entries can mean unknown dependencies. Its
component scope terminology is not Maven scope. SPDX permits partial relationships;
absence of an edge does not certify absence of a dependency. Neither standard
alone proves that its producer used dependency-system selection rather than scanning
files or declarations. No SBOM producer implementation was qualified in this run.

## Pinned JSON semantics and remaining uncertainty

Implementation evidence is the Apache plugin's tagged3.8.1
[TreeMojo](https://github.com/apache/maven-dependency-plugin/blob/maven-dependency-plugin-3.8.1/src/main/java/org/apache/maven/plugins/dependency/tree/TreeMojo.java)
and [JsonDependencyNodeVisitor](https://github.com/apache/maven-dependency-plugin/blob/maven-dependency-plugin-3.8.1/src/main/java/org/apache/maven/plugins/dependency/tree/JsonDependencyNodeVisitor.java).
TreeMojo chooses different graph builders for verbose/nonverbose modes. It has
scope and serialization filters and append behavior. The JSON visitor recursively
writes artifact fields, renders optional as a string, substitutes empty text for
nulls and omits mediation/omission state. It also guards repeated node visits.
Its recursion reads node children directly; do not assume text-visitor filtering
behavior transfers unchanged to JSON. These findings support restricting the first
candidate to known nonverbose, unfiltered, single-project, non-appended output.
They do not certify every Maven/plugin combination or malformed producer output.

Inference: root children can describe represented direct edges under a qualified
producer graph, but depth alone cannot establish an accepted join. Verbose JSON
cannot safely distinguish omitted/conflicting candidates from selected nodes using
these fields. Duplicate same-key selections, missing identity or unsupported
handlers remain ambiguity; a supplier label cannot repair a contradiction.
No producer test execution or real export comparison established fidelity here;
a requested test-source path was unavailable. This is a qualification target,
not a claim that generic JSON trees are already supported.

## Proposed minimum acceptance, not a new contract

The smallest useful candidate is **positive paired facts for existing,
unambiguously identified direct occurrences**, initially with Observed population
and coverage unknown. Do not infer missing rows, zero dependencies or an
Observed-only population from a partial list. This keeps a safe individual fact
usable without requiring complete repository/evaluated-model assurance.

A future proposal should separate these layers:

1. **Encoded facts:** exact safe G/A/V and supported variant, root identity,
   represented edge, scope and optionality where faithfully encoded. Preserve the
   original model key separately from artifact identity. JSON's empty absent
   classifier encoding does not permit repairing an explicitly empty POM classifier
   or collapsing test-jar/jar aliases into a join. Reject unsupported exact versions
   under existing policy; never resolve a request, range or snapshot during intake.
2. **Explicit supplier acceptance:** accept the exact export bytes and their
   stated producer/plugin/Maven versions, selected nonverbose mode, filters/scope,
   append status, successful complete framing of the supplied document and whether
   it represents only part of the collection. Bind each accepted edge to a named
   safe source path/context/model key and exact current consumer/local-lineage bytes.
   Root GAV is a cross-check, not the association authority. Identify the represented
   production context (profiles, property overrides and relevant producer behavior)
   without reading ambient settings. Byte equality alone cannot establish equivalent
   contexts; any paired base-model association needs explicit applicability and no
   known contrary identity/directness/context evidence. Unknown relevant association
   withholds that join, without poisoning independent accepted siblings.
3. **Unknowns kept separate:** source hashes attest correspondence, not provenance
   or complete evaluation. No clean-Git prerequisite, successful application build,
   acquisition proof, archive/content hashes, reproducibility or runtime/deployment
   testimony is required for the narrower retained-selection claim. Production time
   can disclose staleness but does not prove current resolution. Changed bound input
   bytes prevent a current join; an old export is not silently refreshed. Existing
   request/selected-version differences are permitted, not inherently conflicts.
4. **Population versus positive facts:** collection/module omissions and incomplete
   transitive branches need not erase a structurally sound, positively accepted direct
   selection. Whole malformed/truncated/ambiguous framing or uncertain selection mode
   cannot be salvaged by guessing. Known conflicting selections for the same occurrence
   must remain visible as conflicts, not first/last wins. Fully collected direct scope,
   Observed-only rows and a denominator would need separate sufficient population
   evidence; the first candidate need not claim any of them.
5. **Comparator/disclosure authority:** offline selection acceptance grants no HTTP
   permission or public-namespace provenance. Future measurement must independently
   pass existing comparator/source policy and coordinate-disclosure authority for that
   occurrence. A Central-looking GAV or an SBOM download URL grants neither. Selection
   can remain established when comparison/date evidence is refused or absent.

These are discovery recommendations for a later approved boundary, not a wire format
or proposed schema. An initial paired reader could make independently evidenced
requested/selected versions visible, even when some Declared version facts are
missing. It cannot repair Declared refusals, supply an evaluated complete population,
combine view totals or promise additional measured ages. Contexts that cannot be
joined safely remain separate/unavailable; they must not be forced into base_model.

## Privacy, safety and next step

A future offline consumer should use explicit regular-file snapshots, no-follow
bounded reads and identity checks, strict UTF-8/JSON framing, duplicate-member and
nonfinite-number refusal, depth/node/string/byte limits and bounded traversal. Exact
limits belong in a later reviewed specification. No schema/URL/external-reference
fetch, archive extraction, path following, process execution or dependency resolution.
Validate even ignored nested data sufficiently to detect ambiguous framing; retain
safe facts only across separately attributable evidence failures. Do not emit raw
export contents, hashes, local paths, producer diagnostics, settings or arbitrary
supplier strings. Reports may include private coordinates/absolute paths: keep raw
engineering evidence private and review any eventual coordinate disclosure separately.

The decisive gap is a real retained export plus accountable binding/production
context. **Next step: human nominates an already-existing public JSON tree artifact
and its source/context/producer/options evidence, and authorizes a bounded offline
qualification.** A producer fixture or synthetic example can test a shape but cannot
establish target availability, fidelity or yield. No synthetic artifact was needed.
If none exists, defer; any future export production would be a separately authorized
human/CI workflow, never a libyears requirement to install or run Maven/Java.
No specification, reader work, schema change or fresh measurement follows this record.

## Evidence and review

D is resolved by `python tools/observation_handoff.py directory`.
`D/007-0046/` retains original0045 baton/artifact, ledger prefix/reconciliation,
`candidate-inspection.json` and inspection procedure, references and frozen review
inputs. Original0045 artifact/completion/final-freeze verify; it is appended once
with supplied667-second/model/session/account187 telemetry. Original runtime
qualifications survive; starting0045 account remains blank because0044 has no ending
reading. No derived credit delta or active runtime. Current run is not in the ledger.

Local official-document downloads failed with transport errors; no trust input was
read or changed and no insecure retry was made. The successful browser-tool official
source/document excerpts are retained separately from failed attempts, with exact
URLs and capture digests. They are not raw-source-byte retrieval or producer tests.
The initial investigation was bounded to the requested approximately20-minute scope;
no broad content repodive, hosted artifact hunt, registry call or target execution.
The [independent review record](maven-observed-artifacts-review.md) limits approval to
discovery and records final checks/disposition.
