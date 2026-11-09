# Qualified repository snapshot technical plan — 006-0028

Approved spec Q1–Q5 and dispositions in reviews.md govern. No A parser expansion.

## Qualification primitive (Q1–Q3)

Add repository_snapshot_population in nuget_population, independent of A parser
acceptance. Reuse snapshot_population for whole Direct validity, framing, budgets
and existing known contradictions; reuse _xml_pass, _reference and _simple_value
for strict local fact extraction. Return ProjectContext from lock only on complete
qualification; return None for insufficient observable facts; raise safe private
failure on known contradictions/unsafe evidence. Inspect every node via bounded
walk carrying parent/grandparent and whether any ancestor is conditioned. Collect
all package/framework facts regardless of ancillary unknown nodes. Strict reference
facts must be immediate root ItemGroup children without group attrs/text, and all
framework facts immediate unconditional root PropertyGroup simple nodes. Collect
known unconditional supported reference facts even when other facts are unsupported;
compare their IDs/requests to Direct and all known literal frameworks to lock.
When all reference occurrences are extractable, compare complete sets bidirectionally
BEFORE any other eligibility return (including ambiguous attribution). Keep duplicate
refusal and original B2 validator; no v3 override of ordinary known reverse mismatch.

Require root exact Project/Sdk literal framing. Record ineligibility for Import,
Target, Choose, PackageVersion, GlobalPackageReference, ManagePackageVersionsCentrally,
CentralPackageVersionOverrideEnabled, CentralPackageTransitivePinningEnabled,
RuntimeIdentifier(s). All written unextractable PackageReference/TargetFramework(s)
make B1 unavailable; no expansion/evaluation. Unknown unrelated syntax stays unknown,
not proven inert. No project-file inputs beyond held current bytes.

## Orchestration and output (Q1–Q4)

Add keyword-only repository_snapshot=False and unambiguous_snapshot=True to
read_nuget_source. Explicit singleton callers remain defaults and retain old flow.
Repository sources set repository_snapshot=True, with uniqueness computed from
already-complete discovery parent counts (no new directory walk). Always check
ordinary reverse contradictions before declining ambiguous B1 attribution.

On unsupported A ordinary mode, read/parse lock once through existing scoped reader;
call qualification. Terminal failures return unknown without witness read. Qualified
B1 stages N, framework, format, qualified_repository_snapshot, policy trust and fixed
limitations. No selected witness => context=None and rows fail namespace individually
without calling authorize_measurement or creating a capability. Explicit selected
witness => parse_population_provenance on the SAME project/lock bytes; preserve
supplier trust/accepted snapshot limitation and existing namespace semantics. Invalid
witness returns unavailable source retaining B1 N. Insufficient B1 => existing B2
with explicit v3 if present; no witness => original unsupported-project refusal.
No retry B1 after rejected B2. V1/v2 on B1 refuse; A remains unchanged.

Preserve per-occurrence candidate iteration; label both snapshot routes as snapshot
minimum, keep selected evidence even on namespace refusal. Row/source basis new
value is additive in schema3. Format B1 concise policy-selected current snapshot;
verbose existing basis/limitations. Change unsupported_dependency_source diagnostic
to accepted public namespace unavailable (also truthful for v1/v2). Do not claim
supplier witness unavailable on accepted B1. Worker/protocol/registry/scan arithmetic
remain untouched; no new namespace or hash contract. No Git calls in runtime.

## Verification and lifecycle (Q5)

Primitive tests use LocalInput; source/repository semantics use existing injected
reader/discovery seams so capability-disabled hosts still exercise them. Real
reader dirty/non-Git witnesses stay capability-gated, never replace safety refusal.
Test each durable20-case matrix item plus unknown context/reference syntax, partial
known conflicts despite ineligibility, DTD/limits, shared-lock attribution, B2 unknown
syntax fallback and explicit precision compatibility. Namespace negative controls
use socket/process/URL guards and zero-capability assertions; positive accepted
v3 uses existing offline real metadata path/capability codecs. Test schema3/verbose
JSON identity/privacy and A unavailable plus B1 known aggregation. Existing full
A/v1/v2/v3/source/mixed suites remain and any old ordinary-B2 fixture expectation
changes only for newly selected B1 basis, never historical fixture bytes.

Sequential tasks: inert primitive, integration/tests, docs/operation, convergence.
Each gets focused tests/diff/local commit; integration gets full deterministic,
capability-disabled discovery and3 real-worker tests. Documentation checkpoint
updates current README/SPEC/AGENTS/CHANGELOG/ROADMAP without historical rewrites.

Before first OASim access run trusted external capture helper at authorized temporary
006-0028 path; capture exact HEAD/status/index and file state under Q5. Execute
ordinary human/JSON/verbose commands from scanner checkout, retain exact output,
no mapping/evidence generation. Network is forbidden on target behalf: expected
zero authority; verify with guarded in-process companion as well as exact command.
Final capture must equal baseline. Report counts from implementation output, not
expectation, including A whole-evidence blockers and B1 namespace failures.

Freeze commits for fresh decomposed non-author implementation/convergence review:
coherence/precedence/partial knowledge; namespace/v3/claim/firewall; schema/output/
portability/OASim operational evidence. Parent validates all material findings.
Bounded corrections get focused/full verification as relevant and fresh closure.
Canonical history GitLeaks after committed candidate and closure; no push. Actual
hosted Windows/macOS/security/CI remain post-publication witnesses. No new authority
is invented at any review gate.
