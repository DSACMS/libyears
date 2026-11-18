# Supplied Maven external-management evidence — 007-0034

## Recommendation and disposition

Investigate an **explicit offline manifest plus exact POM bytes**, bound to named
consumer snapshots and accepted parent/import edges. Start with a restricted,
nonconflicting static graph; refuse unsupported composition instead of emulating
Maven. This is a discovery recommendation, not an adopted contract or CLI feature.
The retained corpus establishes a real evidence gap, but contains **zero external
model documents**. Feasibility and useful recovery on AB2D remain untested.

Do not implement a compile-default repair. One supplied BOM cannot remove the
other unread imports or parent uncertainty. Preserve independent facts and the
existing 42 scope-ready keys. Neither 39 new measurable occurrences nor a complete
population, coverage, Observed selection or new age result follows.

## Evidence recovered

Starting HEAD is the expected `48b045417bfb15480e869b724844b9fe38e02b80`, clean.
Human reports publication to both remotes; subsequent hosted CI is **unknown**.
No remote reads are needed to answer this offline question. Governing sources are
[the current contract](../specs/007-maven-dependency-age/spec.md#s3--maven-population-and-bounded-local-model),
[scope diagnosis](../maintenance/maven-scope-evidence.md),
[captured context](../maintenance/maven-scope-context.md), and
[yield audit](../maintenance/maven-yield-audit.md).

`D` means the helper-resolved Git-associated observation directory. Only referenced
retained evidence was inspected: `D/007-0032/{before,after,correspondence}.json`,
eight `snapshots/` POMs, `scope-trace.json`, the offline `trace-context.py` procedure,
and `D/007-0028/{before.json,json.stdout}`. No new target checkout reads occurred.
All eight snapshot SHA256 values match both retained baselines; available identity,
revision/index/status correspondence and capture-before/after equality validate.
Re-executing the retained offline trace **with its final file-write removed**
reproduces 127 exact local-fact rows, the 39-key refusal mapping, and the 42 safe
scope-ready work keys under its explicitly synthetic permissive-policy probe.
The probe has a socket/subprocess audit guard; it does not revalidate source policy.

| External role in retained root | Exact established requested identity | What is missing |
| --- | --- | --- |
| Parent, explicit empty relativePath | org.springframework.boot:spring-boot-starter-parent:4.1.1 | Document bytes, accepted applicability, its parent/import closure and effects |
| Management import, type=pom/scope=import | io.awspring.cloud:spring-cloud-aws-dependencies:4.1.1 | Same; version expands from root spring-cloud-aws.version |
| Management import, type=pom/scope=import | tools.jackson:jackson-bom:3.2.3 | Same; version expands from root jackson-bom.version |
| Management import, type=pom/scope=import | io.opentelemetry:opentelemetry-bom:1.66.0 | Same; literal version |

These four first-hop identities are resolved in the captured supported context.
No recursive identity, depth, document count, availability or relevant managed
entry can be inferred from them. In particular, do not invent a Spring Boot
parent chain from familiarity with other releases. Their actual contents were
not read. There are no profiles in the eight retained POMs; this says nothing
about external ancestors/BOMs.

All 39 consumers directly omit scope: 38 have no matching local management;
R18 is an ordinary type=pom AWS dependency matching an import-only management
record, not itself a BOM import. Ten versions are literal, 29 property-expanded.
Parent incompleteness and the three imports overlap on the same 39. They are not
four additive groups. The historical 40 measured occurrences/10 comparisons and
9.29860822749512 libyears remain historical; no dates are reused or recomputed.

## Minimum evidence envelope

A proposed versioned manifest would carry the following, with strict schema,
ordered edge attribution and no implicit acceptance from file discovery:

| Binding | Required evidence / assertion |
| --- | --- |
| Consumer | Exact bytes/digests of all eight named local inputs, source and base-model context, local parent associations and parser/semantics version; Git revision only corroborates |
| Document | Safe relative manifest-local filename, byte length/SHA256, exact requested GAV, supported declared/effective GAV derivation, role-specific identity check; identical bytes may be shared |
| Edge | Referring document digest, declaration site/ordinal, parent versus import role, raw request plus supported expansion/context, target identity/digest, and explicit applicability acceptance for each consumer context |
| Applicability | Supplier asserts these exact documents are appropriate to this captured static slice and specified edges; namesake identity and checksum equality do not establish that assertion independently |
| Origin | Supplied assertion with unknown origin allowed only as disclosed supplied evidence; optional origin description is not authenticated acquisition history; no mandatory private URL, path, credentials or certificate |
| Closure | Explicit parent/import adjacency, terminal absence established by supported inspection, unresolved edges/constructs and limitations; supplier saying complete never overrides contradictory or uninterpretable XML |

Acceptance must be explicit in the invocation. A manifest is untrusted input,
not permission to follow file paths, repositories, URLs or additional declarations.
Identity inheritance/property expansion must be supported before accepting a
claimed effective GAV. Unresolved coordinates stop that edge, not trigger search.
Same GAV with different bytes is a conflict, not a first-file or newest-file choice.
A parent and BOM may share bytes only if both independent role/edge checks pass.

## Supported-fact and refusal matrix

The first useful candidate should restrict semantics further where necessary;
it must not claim full Maven model assembly. Current S3 still governs today.
The retained Maven-3.9.11 source findings in the scope diagnosis establish assembly
before interpolation/import/injection/default completion, non-dominant management
injection for absent ordinary fields, and the delayed final compile default.
They do not establish every external import-order corner case.

| Topic | Safe prospective result | Refusal / proof obligation |
| --- | --- | --- |
| Parent inheritance | Supported child explicit fields win; missing fields can inherit with field provenance | External parent ordinary dependencies can add direct occurrences. Never process only its management and then assert complete N; unknown relevant membership leaves N/coverage unknown |
| Management | Exact group/artifact/type/classifier keys; explicit ordinary version/scope wins; optional remains ordinary inheritance then false default | No GA-only matching, custom handler inference, import-as-ordinary scope, or management optional injection |
| Imports and precedence | Import only management, preserving source/model context, not a BOM's ordinary dependencies/properties/repositories wholesale | First boundary rejects overlapping competing imported keys and inherited-management/import collisions unless pinned source evidence and fixtures settle the composition. Do not invent first/last-wins; no convenient fallback |
| Properties | Retain supported finite scalar expressions and per-field origins; distinguish inherited expressions from already assembled imported entries | Consumer properties must not simply re-expand every imported BOM expression. Resolve each BOM in its own supported model context; unsupported builtins, profiles, duplicate/cyclic/unresolved properties withhold affected facts |
| Closure/defaults | Establish absence of applicable scope only after supported relevant ancestry/import closure | One exact matching entry does not certify graph closure. Missing documents, unresolved edge keys or potentially matching unknown entries withhold dependent management/defaults |
| Cycles/conflicts | Detect digest/identity/context edge cycles; collapse repeated identical documents only as storage | Cyclic ancestry/imports, conflicting same-GAV bytes and ambiguous same-level keys refuse affected graph facts, without arbitrary traversal-order selection |
| Partial evidence | Keep direct explicit facts, independent consumer-written management exceptions and unrelated safe siblings | Do not turn global uncertainty into blanket row deletion, or let one successful same-GA row/cache entry grant work to a refused occurrence |

A limited graph may make a managed version or scope attributable while population,
source-policy admission or date evidence stays unavailable. External parent policy
may also affect comparator admission. Imported repository policy must not simply
be treated as consumer policy; unsupported relevant policy semantics refuse before
HTTP. No manifest can grant public comparator permission through unknown/private
policy. Positive management knowledge and proven absence are distinct outcomes.

## Routes, resources and disclosure

| Route | Benefit | Additional authority / limitation |
| --- | --- | --- |
| Explicit supplied offline corpus (recommended first) | Repeatable private inspection; no coordinate disclosure to obtain models | User must assemble and accept exact context-bound documents, including recursive edges. Bytes/assertions do not prove actual acquisition, evaluated state or supplier history |
| Future fixed-public POM acquisition | Could reduce manual collection | Separate public-model applicability policy, coordinate-disclosure and acquisition grant. Fixed exact GAV versioned POM path on approved public endpoint, verified TLS, no redirects/retries/metadata search/alternate or document-supplied URL/private fallback. A GET proves neither applicability nor historical acquisition |

Keep four gates distinct: **model applicability**, **document acquisition
provenance**, **package comparator permission**, and **age-date evidence**.
Public coordinate identity alone satisfies none of the other gates. Existing
versioned-POM Last-Modified age convention remains separate from supplied model
file timestamps; offline model bytes must never become release dates.

Proposed first ceilings (not current authority): 16 distinct external documents,
1 MiB/document and 8 MiB external bytes within any stricter existing XML ceiling;
8 external parent/import edges on a path, scan-wide shared counters across all
consumers, bounded expression depth/size and existing XML node/depth limits.
Reserve budget before reading; conflicting/duplicate submissions count toward
input work limits rather than permitting unbounded rejected input. Cap manifest
at 64 KiB and 128 edge/consumer associations, with a single 60-second analysis
budget. Exceeding a cap leaves closure unavailable, never truncates it as complete.
These starting proposals may exclude AB2D's unknown real closure.

Use bounded regular-file/no-follow reads with before/after identity checks;
manifest-local containment, no absolute/parent paths, links, devices or ambient
search. Reject DTD/entities/XInclude and malformed XML without expansion or fetch;
no host/env/settings/cache reads, Maven/Gradle, plugins, scripts or target execution.
Raw POMs can disclose internal coordinates, URLs and comments: keep documents and
raw manifest private by default. Output fixed reasons and opaque supplied document
labels, not bodies, actual paths, arbitrary supplier strings or raw exceptions.
Document identity/digests are provenance checks, not signatures or trust proof.
Future network limits would need separate review (starting proposals: 16 attempts,
10 seconds/request, 60 seconds/batch, zero redirects, shared scan budgets).

Useful prospective failures include consumer-byte mismatch, document identity or
integrity mismatch, applicability not accepted, missing recursive edge,
unsupported relevant semantics, conflicting identity, cycle and resource limit.
Attach each safely to affected source/field, identify missing exact safe public
coordinates only when authorized for disclosure, retain independent rows, and
state why default/measurement remains unavailable. These are proposed diagnostic
categories, not additions to the released schema.

## User journey and verification gap

**Illustrative future syntax only; no such option exists today:**

```text
python -m libyears CAPTURE --maven-model-evidence models/manifest.json
Evidence: supplied static models; applicability explicitly accepted
Declared: additional supported management facts [actual counts only]
Unavailable: missing recursive parent; scope absence not established
Population/coverage: unknown; Observed: independently unavailable
Comparator/date work: separately admitted, otherwise unavailable
```

The user supplies the captured consumer bundle, the four exact first-hop POMs
above, and every supported recursively required parent/import POM with explicit
edge/context acceptance and binding. Partial submission can still provide an
inspectable missing-edge report and independent field facts; it cannot promise
any additional scope default. Whether this is useful enough to justify manual
assembly is a product question still open.

Offline acceptance outline, **proposed, not executed feature tests**:

1. Positive synthetic simple parent + BOM graph: own-context properties, explicit
   child overrides, inherited ordinary dependency membership, management injection
   and defaults only after closed absence; exact provenance per field.
2. Key/precedence adversaries: type/classifier differences and aliases, ordinary
   type=pom versus import, explicit scope-only management, overlapping imports in
   both orders and parent/import collisions (refuse unsupported composition).
3. Admission adversaries: stale consumer or document bytes, mismatched GAV/role,
   duplicate manifest keys/identity conflicts, fabricated closure, cycles/diamonds,
   missing grandparent, unresolved import GAV, profile-driven relevant facts,
   inherited versus BOM-local property overrides, reserved/env expressions.
4. Boundary adversaries: path escape/link/swap, DTD/entity/XInclude, oversized XML,
   deep graph/expansions, repeated rejected entries, aggregate/time exhaustion;
   sanitized diagnostics, zero socket/subprocess attempts, deterministic results.
5. Replay these exact eight POMs: preserve original 42 ready keys and 39 refusal
   keys with no supplied external evidence; partial corpus cannot open unrelated
   defaults. Maintain same-GA refusal isolation and unknown N/coverage. Compare
   supported additional facts only after accepted external documents exist.

Indispensable missing real evidence: all four first-hop documents, their unknown
recursive closure, and explicit consumer applicability assertions. They are not
present in this retained corpus. Also missing offline authoritative coverage:
Maven-3.9.11 importer/inheritance/interpolation implementations for external BOM
composition (including collision ordering, model-local interpolation and policy
inheritance). Existing local diagnosis/source summaries are insufficient for
those untested details. Proposed bounded retrieval, if separately authorized:
exact tagged DefaultDependencyManagementImporter, DefaultInheritanceAssembler,
MavenModelMerger, DefaultModelBuilder and relevant interpolator/merger source
methods from Apache Maven; retain exact bytes/tag and narrow references, no broad
crawl. No retrieval occurred. Synthetic witnesses cannot replace these real gaps.

**Next consequential selection:** commission a supplied-corpus feasibility study
with explicit applicability assertions, or defer because manual graph assembly is
too burdensome. A separate future acquisition grant could instead obtain the four
exact public documents and then request only newly identified supported recursive
edges; it must also settle applicability/disclosure, not silently accept namesakes.
Do not advance to specification until useful supported composition is demonstrated
or a deliberately narrower benefit is selected. This discovery stops before
specification, implementation, live validation and push.

Independent review and actual checks are recorded in the
[separate review](maven-external-management-review.md).

Follow-up: [007-0035 bounded acquisition and offline feasibility](maven-external-management-feasibility.md)
acquires 64 models but reaches incomplete closure; no new scope fact is established.
Its [review](maven-external-management-feasibility-review.md) governs that experiment's
disposition, without adopting production intake.
