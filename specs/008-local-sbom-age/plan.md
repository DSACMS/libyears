# Feature 008 technical plan

## Authority and readiness

Implement only the converged [specification](spec.md), normative
[output contract](output-contract.md) and committed examples after implementation
authorization. Run007-0049 authorizes this plan, independent review and subsequent
task decomposition; no runtime, prototype or product tests are created in this run.
Disposition is recorded in [reviews.md](reviews.md). Product boundaries remain in
those owners; this plan chooses mechanisms, not different scope or acceptance.

The useful question is **how many conventional Maven libyears are represented by
this SBOM?** A safe local document plus injected metadata must answer it early,
with a measured-subset total, visible unmeasurable members and independent JSON.
Neither a live lookup nor current-checkout association precedes that witness.

## P1 — Data flow and module boundaries

Use a narrow source pipeline, with no extensible SBOM framework:

`request → bounded selection/snapshot → whole JSON framing → document inventory +
reference graph → canonical members + restrictions → admitted work → metadata +
ages → SBOM summary → safe output projection`.

Existing repository scans finish their ordinary discovery, policy and measurement
before SBOM metadata work. Selection/parsing can also remain after ordinary work
initially; no speculative acquisition or concurrency is needed. No SBOM stage
can mutate an ordinary report, consume its allowance or become its denominator.

| Planned file | Single responsibility and main seam |
| --- | --- |
| `libyears/sbom_model.py` | Small frozen records for request/selection, snapshot identity, canonical identity, members, graph, restrictions, age and final report; closed reasons/states; no I/O |
| `libyears/sbom_input.py` | SBOM-specific directory walk, explicit selection and stable8MiB snapshot; reader factory injectable for semantic tests |
| `libyears/sbom_json.py` | Bounded lexical preflight plus standard-library JSON decode and whole framing; no population or URLs interpreted |
| `libyears/sbom_document.py` | Flat1.5 subset, subject/duplicate-ref checks, assertion extraction, retained record indexes; no metadata authority |
| `libyears/sbom_identity.py` | Literal Maven purl subset, component-field agreement, exact/variant classification and alias grouping |
| `libyears/sbom_graph.py` | Reference-based validation, reachability/path flags and cycle detection before member collapse |
| `libyears/sbom_policy.py` | Global/alias/known-invocation restrictions → independent permission or fixed refusal; no filesystem/network access |
| `libyears/sbom_measure.py` | Adapter to existing Maven supervisor, age construction and pure accepted-population summaries; injected supervisor seam |
| `libyears/sbom_output.py` | Exact JSON projection and aligned ordinary/verbose lines from final safe facts |
| `libyears/sbom.py` | Small orchestration function returning absent/disabled None or a final SBOM report; reader/supervisor injection |

These names describe bounded responsibilities, not mandatory abstractions/classes
for every step. Straightforward functions and explicit control flow suffice. Split
because file safety, framing, identity, graph, permission and presentation have
different failure scopes. Avoid a producer registry, resolver, schema engine or
generic purl library. Keep the existing standard-library-only runtime.

Do not force SBOM rows through `DependencyCandidate`, `MavenOccurrence`,
`MavenCollection` or a fabricated Declared/Observed basis. Retain four facts
separately: member/version assertion; comparator admission; accepted time evidence;
and current-checkout association (always not established). Internal report records
carry both safe output facts and bounded private attribution; raw purls/refs/URLs
never enter generic diagnostics or dataclass-asdict serialization.

## P2 — Request, local selection and filesystem safety

Add exact scoped CLI options and an `SbomRequest` normalized before any scan.
Default is automatic directory mode; disabled means do not instantiate an SBOM
reader or supervisor. Explicit selection validates lexical containment before
scans; a subsequently missing/unreadable file is a report refusal, not an argument
error. Extend the existing CLI privacy guard for malformed SBOM option spellings
without changing acceptance/abbreviation behavior of existing options.

Use a separate reader, not a `MavenInputReader` subclass. Its registration rules,
excluded target/build directories, XML/config limits and XML-oriented errors do
not fit SBOM. Reuse the inspected public safety predicates/identity helpers in
`maven_input.py` where exact contracts fit (`filesystem_available`, reparse and
file/directory identity checks, relative path syntax). Do not change their behavior
or extract a generic filesystem framework just for this feature. A small explicit
duplication of descriptor-walking mechanics is preferable to inheriting wrong scope.

Anchor the positional directory through a no-follow descriptor chain, including
its supplied ancestors, as the current Maven reader does; no realpath-only trust.
Bind child names to descriptor identities, lstat before opening, revalidate opened
and current identities, reject reparse/special entries and always close descriptors.
Discovery enumerates names only within S1's exact depth/directory/entry/candidate
ceilings and exclusions; target/build are included. Sort names for deterministic
selection; charge each inspected entry, including refused matching entries. Record
partial candidate count as observation only. Before content access, require complete
discovery and a unique safe candidate; do not inspect multiple documents to choose.
Explicit mode bypasses discovery but uses the same root chain and snapshot checks.

Snapshot at most8MiB with bounded reads plus growth/EOF checks, compare complete
file identity before/open/after and all directory bindings, then hash exact accepted
bytes. Never follow schema/reference paths or read adjacent settings for SBOM.
All capabilities are checked before relevant I/O. Platforms lacking required
no-follow/dir-fd primitives refuse affected SBOM intake with fixed source reason;
do not emulate safety through permissive path APIs. Existing sibling capability
behavior remains untouched. Portable semantic tests use injected stable snapshots;
real-reader tests separately exercise primitives/refusals on supported platforms.

## P3 — Whole framing and document acceptance

Decode UTF-8 strictly, reject BOM and scan the complete bounded text before creating
an accepted document. A small lexical preflight counts containers, values/member
names, object members, array items and numeric-token lengths against S2. Skip
quoted strings with standard-library string decoding, check decoded UTF-8 length
and unpaired surrogates, and keep container counters in an explicit bounded stack.
This is a framing guard, not a second population parser or generic JSON library.
Use `json.loads` only after preflight, with duplicate-member refusal via pairs hook,
bounded numeric hooks and nonfinite rejection, including float overflow. Standard
JSON decoding supplies final grammar/trailing-token validation. Both stages must
succeed over the entire input, including inert security/descriptive subtrees.

Only then validate1.5 root fields, required subject/components framing, actual
integer document version, relevant containers and per-source inventory/graph
entry budgets. Counters charge records/edges before deduplication. Refuse nested
component populations, non-object inventory entries and repeated refs as specified;
recognize the one exactly identical metadata/top-level subject alias. Preserve
global, subject, metadata and per-record restrictions before discarding inert data.
Graph-invalid evidence is not whole-source failure; whole malformed JSON is.

Parse optional document assertions into the output-contract statuses. Extract
bounded tool names/version only, not contacts, free descriptions or producer
identity assurance. Malformed optional producer/composition assertions receive
their specified status; they do not create component rows or network permission.
Do not claim general CycloneDX validation or execute retained schema material.

No supervisor is constructed during discovery/framing/document acceptance. A late
duplicate key, unsafe identity binding or excessive ignored subtree therefore
cannot follow an earlier successful lookup. Expected failures map to the closed
source vocabulary; unexpected programming/system failures retain CLI systemic
handling and are never disguised as a valid empty population.

## P4 — Inventory identity, aliases and graph

Keep original top-level indexes. Apply S4's literal purl/component checks and
Feature007 exact lexical/snapshot rules; only jar/pom/war with supported classifier
are admitted variants. Do not apply latest eligibility to the used version.
Parse qualifiers once, preserve absent/explicit type distinction privately, decode
only repository_url as specified, and never use it as a destination. Unsupported
or conflicting fields yield a visible per-index member with the correct reason
precedence, not a guessed purl/version. Group fully supported tuples by exact
G/A/version/type/classifier; aggregate record/reference counts and restrictions.
Different exact versions and variants remain distinct; no ComparableVersion or
Maven handler alias may collapse membership.

Maintain an independent raw-ref→opaque-vertex table before grouping members.
Accept purl-shaped or other local opaque refs as equality keys; never interpret
them as URLs. External BOM-Link (`urn:cdx:`) references and dangling targets are
graph refusal, not fetch instructions. Validate unique graph nodes/edges and
specified vertex existence; an invalid graph emits no partial edge projection.
An absent graph is unknown; an explicit empty graph is available but gives no
represented subject paths. Missing dependsOn leaves dependencies_known false;
an explicit empty array records the supplier assertion only.

Compute reference paths first. A visited `(vertex, depth-class)` worklist uses
classes0(start),1 and2-or-more, preserving both direct and longer-path flags even
when a direct ref has another longer path or a cycle exists. Detect cycles using
an iterative color/stack traversal over all vertices, including unreachable ones.
This bounds work by a constant multiple of V+E, not number of possible paths.
Services can bridge paths but never become inventory members. Only after graph
classification union each member's reference flags; do not traverse an alias-
collapsed graph that could manufacture paths. Unknown/unreachable labels and
numeric opaque-ID ordering follow the output contract. Graph refusal preserves
known N and independent ages; whole-source refusal never exposes a prefix N.

## P5 — Comparator admission and existing Maven reuse

`sbom_policy` receives immutable document/global and alias restrictions plus a
small **already-known same-G/A veto set** from the completed ordinary invocation.
It performs no extra POM/config scan and does not establish a declaration join.
Absence of a veto is lack of available contrary evidence, not proof of public
origin. Reduce all supported alias restrictions before minting any capability;
a weaker alias never overrides another alias's private/unknown pointer or global
restriction. Preserve the spec's difference between repository_url assignment,
unsupported relevant semantics and unassigned distribution/intake eligibility.

An internal adaptation is needed: current `MavenScanReport` exposes rows/views,
but `admit_sources` can lose a policy decision when version evidence is missing.
Add a defaulted private comparator-restrictions tuple to Maven admission/report
records, populated from the existing per-source decision and safe occurrence GA
**before** version/measurement filtering. Record only safe G/A and closed refused/
unknown decision, not settings, URLs or paths. Include system assignment and
applicable Central refusal; unknown/input/budget source-policy decisions on known
GA remain unknown vetoes. Do not infer source policy from catalogue/time/version
failure or unknown complete population. Combine repeated GAs conservatively; any
known refusal/unknown applicable assignment vetoes that SBOM GA. No veto can grant
permission. Models without a safe GA cannot invent a package key or global veto.

Propagate that tuple without changing Maven rows, measurements, counts, source
errors, public projection or ordinary metadata requests. Existing injected Maven
reports default to no known vetoes. Add focused regressions proving version-missing
rows still convey source-policy refusal and metadata failure alone does not.
There is no cross-ecosystem name matching or reconstruction from rendered prose.

For each independently admitted SBOM member, create the existing exact
`MavenCapability` object (the supervisor deliberately type-checks it). Keep a
member→capability mapping; it carries no MavenOccurrence or authority from siblings.
The new adapter calls `MavenSupervisor.select_target` and `pom_date`; reuse existing
registry identity checks, ComparableVersion3.9.11, latest selection, trusted worker,
protocol validation, TLS and `metric.libyears_between`. Do not reuse `measure_admission`
by fabricating declared sources. An SBOM age record has the specified SBOM comparator
basis; `MavenAge`'s hard-coded conventional basis/occurrence projection is not changed.

Create a **new** supervisor only after ordinary workers have exited. Retain its
existing process-wide deferred-cleanup guard: an unreaped ordinary worker prohibits
new SBOM worker startup, yielding worker-unavailable rows instead of bypassing it.
SBOM receives its own unchanged upper bounds300 attempts/64MiB/300seconds,60seconds
per GA,10seconds per command,10seconds readiness and0.5seconds cleanup. No retries,
redirects, arbitrary hosts, cross-source cache or ambient config/trust discovery.
An explicitly supplied existing CA option follows the unchanged worker route.

Schedule admitted members by canonical identity then index, as S5 requires. Use
the existing supervisor's catalogue/date cache within this batch; attach outcomes
to each independently admitted member even if GAVs share time bytes. Do not let
cache availability skip row admission. Catalogue/target/date failures retain all
exact facts; dates must pass before arithmetic, including same-version zero. Exact
same-version target/date can reuse one accepted response. Preserve anomaly flags,
GAV date granularity and finite raw values. No package metadata is requested in
this planning run or by a deterministic injected witness.

## P6 — Final report, output and invocation integration

`sbom_measure` summarizes the final accepted members directly, with measured values
from successful age records only, not `calculate_summary`'s inferred denominator
or a legacy dependency wrapper. Reuse `MetricSummary` as a seven-field value type
where useful; explicitly pass N/M/null/empty behavior and fixed reason counts.
Unknown true completeness is independent from M/N. Source refusal creates a
final report retaining safe selection while document/population/statistics are
null; row/graph refusals create partial accepted reports. Unknown graph alone
does not force failure. Do not serialize intermediate pending-age records.

Add a defaulted optional `sbom` field to `MixedScanReport`, separate from
`source_results`, `by_ecosystem`, `maven` and all legacy aggregates. Add scoped
request/reader/supervisor injections to orchestration, retaining the ordinary
scan seams and direct-file behavior. Append SBOM work after ordinary sources;
pass only completed internal policy vetoes and explicit transport configuration.
Disabled/absent scans return None and preserve existing output bytes under frozen
responses. Expected SBOM failures remain in its own section, not legacy source_errors.

`sbom_output` owns an explicit whitelist projection matching output-contract.md,
never `asdict` on raw records. Redact at that boundary and render ordinary/verbose
from the same safe projection. Separate measured/refused aligned tables, keep
every unmeasurable member, escape before widths, and retain detailed safe identity,
graph, source, digest, assertion statuses and limitations. Stable public ordering
is member index/opaque-ID contract order, independent of measurement scheduling.

`report_to_dict` appends only the optional `sbom` field. Preserve all pre-existing
field values/sets and separate Maven projection, and never add SBOM ecosystems.
At the outer human formatter compose the section with the existing legacy/Maven
renderer using a report view with sbom=None to avoid recursion. Render SBOM first
when no ordinary source/failure is presentation-relevant; do not decide relevance
by M=0 or discard refused/unknown ordinary sources. Otherwise preserve existing
tables and qualify their population headings. Protect the selected root and raw
diagnostics when the SBOM privacy path is active, as Maven/NuGet already do;
disable/absence must not alter the old rendering route. Exercise ordinary, verbose,
explicit NuGet precision, mixed and direct-file dispatch separately.

## P7 — Sequence and verification strategy

The task graph is created only after this plan's independent approval. Sequence
implementation toward these bounded checkpoints rather than a generalized reader:

1. Source-local records, safe snapshot/discovery and whole framing, then complete
   flat inventory/identity/graph semantics. No transport authority yet.
2. Pure permission including already-known veto propagation; an injected metadata
   adapter, independent summary and both output forms. Together these form the
   earliest useful **internal deterministic end-to-end slice**: accepted local file
   → measured/refused table and exact SBOM JSON. Production network wiring is not
   its prerequisite; no capability safety is waived. Independent review checks
   this slice before user-facing live-enabled integration.
3. CLI/ordinary scan integration with the real supervised metadata adapter, full
   cross-ecosystem/platform/failure regressions and a retained-corpus **offline**
   acceptance checkpoint. This establishes implementation fitness, not live yield.
4. A separate later real retained-corpus **live age validation gate** requires a
   human grant naming exact artifact digest, public-coordinate disclosure and
   comparator/transport budget/trust scope. No target checkout, build or new SBOM
   acquisition follows by implication. Preserve every unmeasurable result and
   measured subset; do not promise M, total or repository coverage. Publication
   remains a separate gate; optional live work is not a deterministic predecessor.

Tests are written with behavioral tasks under unittest/mock. The first slice uses
small clearly synthetic byte fixtures and controlled metadata, including a measured
and an unmeasurable member,365.25-day positive arithmetic, supported equal-version
zero and missing-date refusal. Committed specification examples are output contract
witnesses, not parsable SBOMs or actual package dates. Derive small input fixtures
explicitly; do not relabel them authentic. Use exact key/null/enumeration assertions
and summary/graph invariants in addition to comparison with example shapes.

The retained real Dependency-Track bytes remain bound to the recorded digest:
201 entries, one exact subject alias,200 external members,21 services,43 direct/
157 transitive,424 edges. Real POM57/14 omitted tests stay a separate comparison.
Run parser/population/projection against that exact durable artifact through a
local verification fixture path; do not fetch it in unit tests or copy unrestricted
raw artifacts into tracked fixtures. If local raw storage is unavailable later,
record that corpus checkpoint incomplete, retaining deterministic fixture results;
recover the original permitted bytes rather than regenerate or infer them.
SPDX corpus/full/partial examples remain unsupported-format witnesses, not a GitHub
export dependency. No CMS adoption hunt is required.

Adversarial cases cover every S2 ceiling/whole late failure, raw hostile labels,
refs/purls/qualifiers, nested inventories, duplicate references versus package
aliases, global/alias veto union, graph invalidity/cycles/service bridges, unknown/
unreachable paths, malformed optional assertions, and source/row failure scopes.
Spy reader/supervisor/process/socket seams prove disabled/malformed/refused inputs
cause zero forbidden I/O. Injected semantic tests run even when native filesystem
primitives are unavailable; separately retain real-file/link/race/reparse/refusal
witnesses and existing isolated-worker lifecycle checks. Include capability-disabled
discovery-before-tests and actual hosted OS/Python matrix at the eventual verification
boundary; local simulation is not Windows/hosted success.

Freeze registry responses for compatibility witnesses: dropping sbom must reproduce
every old schema3 value for each Python/npm/Ruby/NuGet sibling, explicit/ordinary
NuGet modes, Maven views, empty/unknown inventories and absent/disabled/refused/
successful SBOM. Full deterministic suite is a meaningful phase/integration gate
during implementation, not a check run merely for this planning documentation.

## P8 — Requirements coverage and remaining gates

| Approved requirement | Planned surface / decisive witness |
| --- | --- |
| S1, AC01 | P2/P6 exact CLI/discovery/disable/selection; no-read/no-lookup spies |
| S2, AC05/14 | P2/P3 safety/framing before any permission; native and injected refusals |
| S3, AC02/03/06/07 | P3/P4 canonical inventory and reference-first graph; real corpus and adversarial counts |
| S4, AC08/13 | P3/P4 literal subset, identity reasons and unsupported authentic SPDX |
| S5, AC04/09/10 | P5 independent veto/admission, existing worker/time adapter, offline isolation |
| S6, AC02/04/10 | P6 accepted N/M arithmetic/null semantics, no occurrence weighting |
| S7/output contract, AC11/12 | P6 whitelist JSON and safe aligned tables, full frozen projection equality |
| S8 | P2–P7 source/graph/row reason precedence and actionable fixed diagnostics |

No unresolved product decision is introduced. The narrow internal veto channel,
separate reader and supervised adapter are technical consequences of inspected
contracts. If implementation encounters a genuine contradiction, use the existing
workflow's gap rule rather than editing approved requirements. The next authorized
work within run007-0049 is plan review, then approved-plan task decomposition and
review. Final stop: **IMPLEMENTATION AUTHORIZATION**. This plan grants no execution,
external access/disclosure, live validation or publication by its existence.
