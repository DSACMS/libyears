# Feature 006 Implementation Task Graph

## Current H3 obligations and execution state — 006-0015

The corrected [specification](spec.md) at `2deb864` and the current H3 supplement
in [plan.md](plan.md) govern the refinement; original frozen hashes and pending
language below describe the original task-graph candidate. See [reviews.md](reviews.md)
for completed implementation history and the current gate. Preserve all T/AC/K
identifiers and historical task/checkpoint completions.

- T005/T006: existing version-1 assertion, byte/context, origin and hash mechanisms
  remain applicable. No native artifact reader or chronology authentication is
  required. Their executed synthetic witnesses do not prove a real producer event.
- T012/T013: supplemental bounded correction PENDING. Update `output.py` trust
  explanation, `cli.py` provenance help, corresponding output/help assertions,
  README.md, SPEC.md and synthetic fixture guidance to explain both evidence
  classes, contemporaneity and replay prohibition. Preserve JSON/schema/reasons,
  activation and all metric/security semantics. Freeze, focused non-author review,
  parent validation and relevant output/CLI/compatibility regression checks are
  required. Product code changes are not authorized in run 006-0015.
- T014/K4: historical offline approval is preserved. Reconcile supplemental
  reporting witnesses after the bounded correction; no newly claimed all-36
  acceptance from old test counts.
- T015: prospective preparation is extended in [release-validation.md](release-validation.md),
  including exact production-vs-consumption authority, retained bundle and checks.
- T016/K5: INCOMPLETE / NOT APPROVED. AC-13 adds independent audit of native
  evidence plus contemporaneous attestation and their package/event/byte/context
  binding. AC-16 adds retained 006-0014 as the historical replay negative; it may
  not supply original-event attestation. Existing deterministic AC-13/16 witnesses
  remain necessary but do not close these added event-evidence obligations.
- T017/K6 remain blocked by required K5 and current correction/evidence gaps.
  T018 and Feature 007 are not authorized.

All original predecessors remain mandatory. A new prospective producer event
requires separate exact target/tooling/source/input/write/capture authority;
resuming T016 separately requires a conforming retained bundle, explicit supplier
acceptance and consumer target/read/network/evidence-channel authority. No replay
can retrospectively qualify historical OASim. This graph update grants neither
execution permission nor a waiver of missing evidence.

## Status and governing authority

Candidate drafted and self-audited in fresh run `006-0007`, 2026-11-03.
Approval disposition, frozen digest and next gate live in [reviews.md](reviews.md).
This candidate remains byte-frozen after independent review commissioning;
neither this graph nor its approval authorizes implementation or external access.
All tasks and acceptance criteria below are pending.

The approved [specification](spec.md), SHA-256
`f02a947ae33dc83afa08a800e0bd965f56e697317e40dd1c6209d133f3c73cc8`,
and approved [technical plan](plan.md), SHA-256
`b340a41df7eee3e5e7e0b012c8976d7a79921a12960c3a156e212a004704c875`,
govern. Read their current approval record: 006-0004 closed F1/F2; 006-0006
closed P1. Historical draft and REVISE records remain evidence. This graph
assigns implementation and verification ownership without changing those decisions.

H1 means lock-only selection. H2 means one explicit SDK C# project, one literal
framework and all supported direct references, with qualified supplier testimony.
H3 means context-bound public origin plus local and public content agreement,
never public namesake inference. H4 means catalog created as first nuget.org
receipt and greatest currently listed stable from complete enumeration. Useful
live yield and hash-domain fitness remain unverified non-findings. A demonstrated
inability to honor these contracts returns to human authority.

## Dependency graph and execution rules

Every predecessor is mandatory, including independent review nodes. Table order
alone grants no readiness. Execute sequentially unless a future prompt explicitly
authorizes parallel work. Each T task is one bounded local commit when execution
and commits are authorized; K nodes freeze and independently review the phase,
with disposition/evidence retained in reviews.md. Review-record commits follow
the commissioning prompt. No task may bypass an unresolved K gate.

| Node | Reviewable work unit | Predecessors | Phase |
|---|---|---|---|
| T001 | Typed evidence and bounded version helpers | None | 1 foundations |
| T002 | Safe local reader and bounded JSON framing | T001 | 1 |
| T003 | Complete supported project parser | T001, T002 | 1 |
| T004 | Whole-lock schema and F2 validation | T001, T002, T003 | 1 |
| T005 | Witness schema, context and H3 local gate | T001, T002, T003, T004 | 1 |
| T006 | Internal source orchestration and F1 association | T003, T004, T005 | 1 |
| K1 | Fresh foundation/authority review | T006 | STOP |
| T007 | Restricted NuGet transport opt-ins and budgets | K1 | 2 adapter |
| T008 | P1 trusted worker, supervision and lifecycle | T007 | 2 |
| T009 | Complete public registration/catalog adapter | T001, T006, T007, T008 | 2 |
| K2 | Fresh security/metadata/P1 review | T009 | STOP |
| T010 | Internal mixed-scan and metric integration | K2 | 3 integration |
| T011 | Additive schema-v3 serialization | T010 | 3 |
| T012 | Human reporting from shared safe evidence | T010, T011 | 3 |
| T013 | Coherent CLI activation and user documentation | T010, T011, T012 | 3 |
| K3 | Fresh integration/output/compatibility review | T013 | STOP |
| T014 | Complete offline acceptance and reason audit | K3 | 4 acceptance |
| K4 | Fresh independent 36-AC acceptance audit | T014 | STOP |
| T015 | Real-root validation preparation | K4 | 5 preparation |
| T016 | Separately authorized real-root evidence | T015, explicit target/access authority | 5 validation |
| K5 | Real-root evidence disposition | T016 | STOP |
| T017 | Fresh read-only convergence | K1, K2, K3, K4, K5 | 6 convergence |
| K6 | Convergence disposition | T017 | STOP |
| T018 | Retrospective and human roadmap handoff | K6, separate authorization | closure |

Future phase authorization must name its tasks, checkpoints, commits and stop.
K1–K4 are independent review stops even if a phase execution prompt covers all
preceding tasks. An APPROVE is confined to completed review coverage; REVISE
requires validated findings and a separate bounded correction authorization;
INCOMPLETE identifies unaudited obligations. Never silently repair a frozen
candidate or treat positive slices as overriding another material finding.

No public activation before T013: T001–T012 add internal seams only, exercised
through tests. Existing scan/CLI defaults and ordinary reports must stay intact.
Tests accompany each behavioral task; T014 consolidates evidence, not deferred
component testing. At each phase boundary run the complete deterministic suite
`python -m unittest discover -s tests` and `git diff --check`. Run focused tests
first. Inspect each diff before a task commit; report clean/dirty state honestly.
No push, release or tag is authorized by this graph.

## Task completion contracts

Paths below are allowed surfaces for future authorized work, not edits performed
by task decomposition. Test module names are proposed concrete targets; use
`python -m unittest discover -s tests -p 'test_nuget_VERSION.py'` with the named
suffix (or equivalent explicit modules). Fixtures live under
`tests/fixtures/nuget/`; their README explains synthetic provenance and witness
assertions. All tests use unittest/mock, standard library and offline responses.

### T001 — Typed evidence and separate version concepts

Surfaces: `libyears/model.py`, new `nuget_version.py`, focused version/model tests.
Add optional NuGetEvidence/NuGetPublication records and private parser/authority
records in their owning modules as needed. None defaults must emit no new sibling
fields. Keep hashes/baseline separate from public evidence. Implement the plan's
three explicit helpers for requested minimum, selected identity and stable key;
no resolver, general range algebra or prerelease ordering.

Done when bounded two/three/four component requests normalize correctly; selected
identity accepts S5 leading zeros, suffix case and ignored build labels; stable
ordering compares four integers. Check length before conversion. Focused
`test_nuget_version.py` plus existing model/metric/output tests establish numeric
order, nonzero revision, unsupported forms, identity equivalence and unchanged
default records. This owns AC-24, with adapter use verified again in T009.

### T002 — Safe bounded local input

Surfaces: NuGet-local reader/framing helpers, focused `test_nuget_input.py` and
security fixtures. Reuse the descriptor-relative technique without altering Ruby
policy. Read only selected immediate project, fixed lock and explicit witness;
retain exact bytes. Implement all plan local byte/depth/value/string/digit/count
limits and strict duplicate-preserving JSON framing. Each consuming parser also
enforces its specific counts; T002 supplies the shared bounded mechanism.

Done when cap/cap+1, encoding, symlink-inside/escape, FIFO/device, replacement and
unsupported safety-primitive fixtures fail closed without blocking or partial
population. Reject nonfinite JSON and bool-as-schema-integer, distinguish malformed
from unsupported per S6. Demonstrate no ancestor/config/cache/reference traversal
and unchanged Ruby reader regressions. This owns AC-33; T003–T005 add their limit
boundary examples rather than assuming reader tests cover parser work.

### T003 — Complete project population

Surfaces: `nuget_project.py`, `test_nuget_project.py`, minimal XML fixtures.
Implement both bounded Expat passes and the plan's conservative literal tables.
Validate complete framing before semantic classification. Require literal SDK,
sole unconditional framework and immediate unconditional Include/Version refs;
ancillary metadata is allowed once per approved name. Reject DTD/entities,
namespaces, non-UTF-8 declarations, duplicate IDs, conditions, CPM/imports/targets,
computed/package-affecting/unknown constructs. SDK behavior is asserted, not read.

Done when AC-03–07 positive/negative matrices produce complete N or unknown N,
never partial scope. Cover both framework property forms; test/tool/analyzer and
PrivateAssets membership; ProjectReference/FrameworkReference/implicit exclusions
with referenced paths guarded against opening. All five S3 request forms pass
declaration parsing, while bracket-exact/ranges/floats/prerelease requests reject.
Use T001 normalization; never infer selection from a request.

### T004 — Whole-lock acceptance and F2

Surfaces: `nuget_lock.py`, `test_nuget_lock.py`, schema-1 fixtures.
Validate the complete root/framework/entry/dependency-map structure, strict fields,
kinds and case-insensitive ID uniqueness. Accept Direct/Transitive/Project closure
framing without adding population. Missing selected/hash strings may remain
isolated only as specified; present non-string fields follow the approved plan.

Done when AC-08/09 fixtures retain known N on lock rejection. F2 witnesses must
reject repeated resolved keys, case aliases, null/array/object resolved as whole
`invalid_lockfile`, additional frameworks/RIDs as unsupported, and absent resolved
as an attributable later failure. Whole malformed structure wins over unsupported
structure independent of key order. No NuGet ambiguity reason is introduced.

### T005 — Supplied witness and local authority

Surfaces: `nuget_provenance.py`, `test_nuget_provenance.py`, version-1 JSON witness
fixtures and fixture README. Implement the exact plan serialization, strict types,
duplicate/unknown field rejection, byte/context/SDK binding, coherent snapshot and
baseline assertions. Containment binds package records to the envelope. Test
normalized ID/version record uniqueness and unsupported-influence classification.

Done when AC-13–17 witnesses show explicit acceptance only, no conventional
discovery; missing/rejected witness retains independently known N while unsupported
population influence clears N. Matching singleton canonical public origin and
decoded 64-byte SHA512 agreement alone construct LocalAuthority. Missing/private/
alternate/conflicting origin and absent/invalid/mismatching hashes produce exact
reasons with zero adapter calls. Config/cache/mapping/blanket/hash-only markers
cannot authorize. Validate unselected records' framing without requiring public
origin. Raw origins/hashes/baseline never enter public records.

### T006 — Internal source orchestration and association

Surfaces: `nuget.py`, `test_nuget_source.py`, association/reason fixtures.
Compose complete project, lock and witness acceptance before per-package work;
return existing SourceResult availability semantics through an internal seam.
Extra Direct identities and wrong/stale context reject whole context. Implement
F1 exact canonical `[w, )` minimum comparison, then missing/unsupported selection
and local authority stages. Preserve only established safe evidence.

Done when AC-10–12 and local AC-31 cases pass: all five S3 pairs, differing request
and resolved, unequal minimum with shared resolved, every S3 noncanonical/negative
form, missing Direct with Transitive namesake, missing/non-string requested, and
missing/unsupported selection. Mismatch exposes safe lock_requested but no selected
provenance. Mtime/Git do not repair byte binding. Whole-source errors create no
fabricated package failures. Begin the mechanically enumerable S6 reason-trigger
table, with later owners extending it. No local rejection reaches lookup.

K1 freezes T001–T006 and reviews F1/F2, complete scope, whole-source precedence,
safe input limits, local authority/no-call proofs and evidence omission. It must
also inspect T001 default record compatibility. Stop before adapter work.

### T007 — Restricted transport and finite work

Surfaces: opt-in additions in `libyears/registry.py`, NuGet metadata client in
`nuget_registry.py`, `test_nuget_transport.py`, existing registry regressions.
Implement the plan's exact api.nuget.org authorities/path purposes, fixed service
index/hive, zero redirects/retries, verified TLS and bounded incremental gzip.
Apply every network table cap, request/counter scope and cooldown rule. Do not
change existing transport defaults or injected get(url) doubles.

Done when wrong host/port/userinfo/query/fragment/path/escaped separator/HTTP,
redirect, archive/private link, gzip bomb/truncation, byte/JSON/page/request limit
and 429/503/Retry-After matrices yield the specified response versus registry
errors. Sorted request scheduling and scan-local suppression must be explicit.
No sleeping retry, alternate host or partial enumeration. Run existing
registry/PyPI/npm/Ruby transport tests and full suite at this shared boundary.
Elapsed enforcement is not claimed until T008; admission-only checks are insufficient.

### T008 — P1 process boundary and absolute deadlines

Surfaces: NuGet-specific supervisor/worker modules, `test_nuget_worker.py` and
trusted offline blocking fixture; supported POSIX/Windows CI configuration only
as necessary for lifecycle coverage. Implement the approved private trusted
interpreter bootstrap, isolated imports/cwd, DEVNULL, readiness, sequential bounded
regular-file protocol, parent monotonic controller and complete cleanup lifecycle.
No target module, command, credential/config reader or generic worker framework.

Done when the entire blocking DNS/connect/TLS/header/body plus parsing/traversal
is killable; immutable 60/300-second package/scan deadlines include index discovery
and 0.5-second cancellation reserve. Preserve the 10-second readiness bound,
10-ms polling ceiling, 0.25-second terminate wait, bounded kill/reap and 16-KiB
atomic command/result cap. Reject exact/late cutoff results and do not restart
after cancellation; retain earlier successes and suppress remaining lookups.

Required deterministic witnesses are all AC-34 plan bullets: drip-feed below
socket timeout and byte caps; blocked connect/TLS/header/body; scan deadline
earlier than package; index stall, exhausted budget, early/exact/late completion;
ignored terminate/kill/reap faults, interruption, abrupt death, oversized/corrupt
protocol, closed handles/temp cleanup and unreaped systemic failure/deferred
cleanup. Include a mutation witness that fails admission-only/socket-only design.
Separate offline real-worker handshake/stall/cancel tests confirm OS exit and
cleanup on supported POSIX and Windows CI using an outer watchdog, not exact
wall-time assertions. Missing platform evidence is outstanding verification,
never a passed gate. Respect documented process-creation/OS limits; no hard
real-time whole-CLI claim or synchronous fallback.

### T009 — Public metadata and content/date authority

Surfaces: `nuget_registry.py`, `test_nuget_registry.py`, registration/catalog fixtures.
Adapter accepts LocalAuthority, invokes T008 supervision, and retains scan-local
counters/cooldown/index across sorted packages. Implement complete SemVer-2
registration traversal, identity/count/bounds/duplicate reconciliation, listing
defaults and selected/greatest-stable catalog leaves. Fetch only approved links,
never history/archive repair. Transfer only typed safe results across the worker.

Done when AC-18–23 pass, using T001 for identity/latest: public selected identity,
SHA512 algorithm/hash gating; used absence before hash/date; created-only UTC
parsing with zero-to-seven fractions; no naive/1900/conflicting date or older
dated fallback. Complete/no-stable/incomplete/unsupported-candidate and equivalent
alias conflict matrices must be covered. Used prerelease/unlisted may measure;
no request/framework/date compatibility filter may choose latest. Add registry
reason triggers and reordered-response request/evidence invariance tests. Complete
AC-34 composed transport/supervision tests and privacy canaries before K2.

K2 independently reviews security, metadata completeness, source/content gates,
public dates, all caps and P1 fake-controller plus real-worker evidence. Confirm
existing ecosystem transport regressions and full offline suite. Stop before integration.

### T010 — Internal scan/metric integration

Surfaces: `scan.py`, model/result propagation seams, `test_nuget_scan.py` and
`test_mixed_scan.py`. Add typed internal request and explicit fourth source/lookup
pair behind that request, still unreachable from public CLI. Transfer evidence
through candidate/success/failure/measurement paths. Keep Python --resolved,
npm/Yarn arbitration and both Ruby modes unchanged; reuse metric unchanged.

Done when AC-25–28 matrices verify every S6 per-source/repository null/zero/count
state: unknown project, known N/unavailable lock/witness (also N=0), unsupported
membership, validated empty, all-failed/partial/full accepted scope and all versus
some sources unavailable. Explicitly supply NuGet unavailable numeric handling;
do not rely on Ruby-specific serialization conditions. Available sibling rows and
same-name cross-ecosystem identities survive each failure. Check 365.25 days,
normalized identity exact zero, negative anomaly flag and measured-only totals.

### T011 — Additive JSON contract

Surfaces: `output.py`, `test_nuget_output.py`, existing output tests.
Serialize S7 source/row evidence exactly, with optional defaults omitting every
NuGet addition for siblings. Done when AC-29 full/partial/rejected-stage snapshots
prove schema 3, required source nulls, all stage-specific omissions, no mismatch
selection claim, packages_lock source and safe declared text. Ordinary/verbose
JSON must be identical. Test unavailable NuGet aggregates independently of Ruby.
Keep human text separate; no raw diagnostics in JSON.

### T012 — Human evidence and failure reporting

Surfaces: human formatter in `output.py`, focused output/correspondence tests.
Render from the same typed facts as JSON. Done when AC-30 comparisons check
identity/context, requests/selections, authority/hash states, dates, reasons and
numeric facts. Explain all-direct test/tool scope, accepted supplier assertions,
snapshot limitations, first receipt and listed-stable comparator. Distinguish
unavailable, zero coverage and empty. Preserve anomaly flags and ordinary sibling
reports. Privacy tests cover successful, failed and verbose human rendering.

### T013 — Coherent activation and documentation checkpoint

Surfaces: `cli.py`, `test_cli.py`/NuGet CLI tests; README.md, SPEC.md, AGENTS.md
ecosystem scope and CHANGELOG.md Unreleased Added. Expose only exact two options
with occurrence tracking and NuGet-specific safe argparse rendering. Validate
usage before any source read, pass the typed request, and activate completed
scan/output seams together. Documentation describes actual supported behavior,
numeric limits, supplied witness schema/acceptance, worker/time qualifications,
security, failures, source/date claims and retained limitations.

Done when AC-01/02 ordinary/co-located-artifact scans omit NuGet, explicit choice
selects only one immediate project and found witness never supplies authority.
Witness-only/repeated/abbreviated/malformed/missing values, paths/globs/lists and
direct-file activation exit 1 without raw option leaks. Missing explicit project
is source failure/exit 0; source/empty/partial reports and systemic exit 2 follow
existing contracts. Prove Python --resolved and Ruby options retain isolation.
Run full deterministic suite and check docs against implemented contract.

K3 freezes coherent activation and independently audits complete S6/S7 matrices,
CLI privacy/exits, human/JSON correspondence, ordinary and sibling compatibility,
and documentation accuracy. Stop before final acceptance consolidation.

### T014 — Final offline acceptance evidence

Surfaces: focused acceptance/security tests and a Feature 006 acceptance evidence
record. Reconcile every mapping below to actual test names/results, all plan
limits and every retained S6 reason. Add composed adversarial cases beyond unit
boundaries; do not mark an AC passed merely from its component's completion.
Own final cross-cutting AC-31/32/34/35/36 closure, incorporating earlier witnesses.

Done when reason-trigger enumeration has no missing/extra NuGet reason; combined
and permuted project/JSON/reference/page cases preserve earliest-stage outcomes,
safe evidence, sorted requests and summaries. Guard every public path against
forbidden process/network/cache/config/credential/reference access and compare
target bytes before/after. Permit only the exact installed trusted helper and
offline lifecycle fixture. Secret canaries in XML/witness/origins/arguments/paths/
responses/exceptions must be absent from stdout/stderr/JSON. Excluded evidence
can never repair failure. Include all P1 mutation/lifecycle witnesses, focused
regressions and full deterministic suite plus diff check. Report platform or
environment gaps explicitly; no external target or live network is needed.

K4 is a fresh independent all-36-AC acceptance audit of spec/plan/tasks/code/tests,
reason table, security and compatibility evidence. Distinguish audit completion,
findings and verdict. A test count alone does not establish acceptance.

### T015 — Validation preparation only

Surfaces: Feature 006 release/validation checklist, commands and expected evidence
shape. Prepare human/JSON comparisons for selected root/project/witness, scope,
selection, origin/hash states, created dates, metric arithmetic and unchanged
target bytes. Record offline results separately from live evidence. No target
is selected, accessed or produced here; discovery's OASim paths confer no access.
Done when T016 can execute a bounded, reviewable procedure after explicit target
and required network authority. Include yield/hash-domain and environmental limits.

### T016 — Required separately authorized real-root validation

Only authorized roots/access and read-only scanner use; never restore, target
execution, archives or source/hash-policy workaround. Capture the T015 comparisons
and raw safe evidence location, distinguishing agent inspection from accepted
human attestation. Separate live/environment failures from deterministic correctness.
Missing targets or unavailable evidence keeps this node pending/incomplete;
do not silently make required K5 optional or claim success from a smoke check.
K5 records evidence completeness, findings and disposition before convergence.

### T017 — Independent read-only convergence

Fresh non-author review reconciles all approved artifacts, implementation, tests,
documentation and K1–K5 evidence, with 36/36 AC accounting and cross-boundary
reconciliation. No repair in this task. K6 records CONVERGED only with complete
coverage and no unresolved material finding; otherwise record outstanding work
truthfully and stop for separately authorized correction/reverification.

### T018 — Retrospective and human handoff

After K6 and separate authorization, reconcile completed lifecycle evidence,
limitations and prospective observations into a retrospective and roadmap review
handoff. No invented telemetry/causal resource claim, release, next-feature work
or implied external authorization. Human roadmap selection remains a separate gate.

## Acceptance ownership and deterministic traceability — 36/36

Each AC has exactly one accountable completion owner. Contributors implement
sub-obligations earlier; the owner must reconcile their composed evidence before
claiming completion. Test families refer to the concrete modules above; witnesses
are obligations to implement, not executed tests. K4 re-audits every row.

| AC | Owner (contributors) | Required deterministic witness | Review |
|---|---|---|---|
| AC-01 | T013 (T010) | CLI exact selection vs ordinary co-located artifacts; NuGet absent unless activated | K3/K4 |
| AC-02 | T013 | CLI witness-only/repeat/abbreviation/path/value matrix exit 1; missing project source exit 0 | K3/K4 |
| AC-03 | T003 | Project TargetFramework and sole TargetFrameworks exact population/context positives | K1/K4 |
| AC-04 | T003 | Complete XML/context duplicate/computed/conditional/multi/RID/DTD/namespace negatives; no partial N | K1/K4 |
| AC-05 | T003 | Test/tool/analyzer/PrivateAssets counted; project/framework/implicit excluded; no path traversal | K1/K4 |
| AC-06 | T003 (T001) | Five supported S3 numeric forms; request meaning retained; range/exact/float/expansion/prerelease rejected | K1/K4 |
| AC-07 | T003 | Case duplicates and all package-affecting import/CPM/Target/Update/Remove/override/unknown negatives | K1/K4 |
| AC-08 | T004 | Sole-framework schema-1 Direct/Transitive/Project accepted; closure never adds scope | K1/K4 |
| AC-09 | T004 | Bool/schema/unknown fields/RID/extra context/duplicate keys/malformed framing reject lock with known N | K1/K4 |
| AC-10 | T006 (T001) | F1 five canonical pairs; selected differs from request; unequal minimum/shared resolved rejected | K1/K4 |
| AC-11 | T006 (T004) | All S3 negatives, missing Direct/version and unsupported string no-call; F2 duplicates/multivalue whole-lock rejection | K1/K4 |
| AC-12 | T006 (T005) | Extra Direct, wrong framework/project, changed byte digest; mtime/Git irrelevant | K1/K4 |
| AC-13 | T005 | Explicit version-1 envelope and exact byte/baseline binding; conventional witness never opened | K1/K4 |
| AC-14 | T005 (T006,T010) | Missing/corrupt witness known N unavailable; unsupported population assertion unknown N | K1/K3/K4 |
| AC-15 | T005 (T009) | Missing/private/alternate/unknown/conflicting origin with public namesake; zero requests | K1/K2/K4 |
| AC-16 | T005 | Blanket/config/mapping/cache/ID/version/hash-only input cannot construct LocalAuthority | K1/K4 |
| AC-17 | T005 | Strict decoded hashes equal/missing/invalid/mismatch; exact reason and zero calls on rejection | K1/K4 |
| AC-18 | T009 | Authorized local gate plus catalog ID/version/SHA512 missing/mismatch/equal matrix | K2/K4 |
| AC-19 | T009 | Distinct created/published/commit/listing/restore fields prove created-only used/latest | K2/K4 |
| AC-20 | T009 | Used/actual latest missing/invalid/naive/1900/conflicting created; no older fallback | K2/K4 |
| AC-21 | T009 (T001) | Complete paged SemVer-2 population, listed absent/false, greatest numeric stable independent of dates/constraints | K2/K4 |
| AC-22 | T009 | Missing page/count/bounds/unsupported candidate/conflicting alias/no stable matrix | K2/K4 |
| AC-23 | T009 | Used prerelease/unlisted measurable; package 404 vs version absence; no archives | K2/K4 |
| AC-24 | T001 (T009) | Leading zeros, missing patch/zero/nonzero revision, prerelease case/build equivalence and numeric ordering | K1/K2/K4 |
| AC-25 | T010 | 365.25-day delta, normalized equal-identity zero, flagged negative clamp, measured-only aggregates | K3/K4 |
| AC-26 | T010 (T006) | Missing/bad project unknown vs missing/bad lock known N/null measurement; no N fabricated rows | K3/K4 |
| AC-27 | T010 | Valid empty/rejected empty/all-failed/partial/full matrix; every S6 null/zero field | K3/K4 |
| AC-28 | T010 | Each NuGet failure with successful Python/npm/Yarn/Ruby; same-name identities and repository availability | K3/K4 |
| AC-29 | T011 | S7 full/partial/rejected stage presence/null/omission; schema 3, verbose equality, sibling output equality | K3/K4 |
| AC-30 | T012 | Human/JSON facts correspond including requests/states/dates/aggregates and supplier limitations | K3/K4 |
| AC-31 | T014 (T004,T006,T009,T011) | Every S6 reason has reachable trigger; combined/reordered stages; no ambiguity/unprocessed error/mismatch selection claim | K1/K2/K3/K4 |
| AC-32 | T014 (T002–T013) | Exact trusted-helper-only process guard; offline network/cache/config/credential/read guards and target byte invariance | K1/K3/K4 |
| AC-33 | T002 (T003–T005) | All local cap/cap+1 limits, unsafe/special/replaced/encoding/root-escape cases; bounded complete-source rejection | K1/K4 |
| AC-34 | T014 (T007–T009) | All approved URL/redirect/byte/gzip/page/request/rate/time bounds; full P1 controller/mutation and real-worker lifecycle matrix | K2/K4 |
| AC-35 | T014 (T005–T013) | Secret canaries across parser/CLI/worker/registry/output errors and success; no raw XML/witness/hash/origin/path leaks | K1/K2/K3/K4 |
| AC-36 | T014 (T003–T006,T013) | Assets/export/packages.config/CPM/import/conditional/private/multi-framework/RID/portfolio never repair evidence | K1/K3/K4 |

## Author self-audit and freeze contract

The graph has 18 pending tasks, six explicit review stops, acyclic dependencies
and one owner plus concrete deterministic witnesses for each of 36 unique ACs.
Component tests precede integration; final acceptance composes them. F1 is owned
by T006 with T001/T003 support; F2 by T004/T006 and T014 precedence closure;
P1 by T008 with T007/T009 composition and T014 final closure. K1–K6 retain all
approved checkpoints, and K5 is required but separately authorized.

Source authority, numeric bounds, safe destinations, privacy, schema-v3 addition,
availability, sibling behavior and metric remain the approved contracts. No
external validation target, producer execution, broader ecosystem/context/format,
private-feed access or speculative generic framework is introduced. Each unit
has bounded surfaces, done conditions and focused verification; coherent public
activation waits for scan, both serializers and docs. Missing consequential
decisions stop execution rather than modifying approved authority.

This is author traceability/self-audit, not independent approval or implemented
acceptance. Freeze exact candidate bytes/digest before fresh non-author task-graph
review; record findings, audit completeness and final disposition in reviews.md.
No post-freeze repair is included in this gate. If approved, the next gate is
explicit phase-1 execution authorization; if REVISE/INCOMPLETE, stop at the stated
correction or missing-review gate. No implementation occurs in run 006-0007.
