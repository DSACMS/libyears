# Feature 008 implementation task graph

## Readiness and authority

Derived only after independent approval of [plan.md](plan.md), committed at
`279e48e` in run007-0049; approval/evidence lives in [reviews.md](reviews.md).
[spec.md](spec.md), [output-contract.md](output-contract.md) and unchanged examples
govern behavior. This graph is reviewed planning, **not implementation authority**.
Every checkbox below is deliberately open. No runtime/prototype/product-test work
has begun. First execution requires a human grant identifying the authorized phase.

Once a phase is authorized, dependency-ready tasks and determined review corrections
progress without new human permission at every transition. Each task normally has
one explicit-file local commit when execution authority includes commits; inspect
and verify it under standing repository rules. Each task includes behavioral tests
with its change, a focused test result and self-audit against listed requirements.
Do not mark complete from code existence alone. Independent internal checkpoints
are below; they are not human authority gates unless a new decision/access is needed.

## Dependency spine and checkpoints

| Task | Dependencies | Bounded result |
| --- | --- | --- |
| T001 | implementation authority for phase A | Source-local records/request and safe bounded selection/snapshot |
| T002 | T001 | Whole JSON framing and flat1.5 document acceptance |
| T003 | T002 | Exact Maven identities, canonical members and alias attribution |
| T004 | T003 | Reference-first graph classification and failure isolation |
| T005 | T004 | Pure permission and already-known same-G/A veto propagation |
| T006 | T005 | Injected comparator/time adapter and independent SBOM summary |
| T007 | T006 | Safe JSON/tables and internal local-file→age-report slice; C1 |
| T008 | T007, C1, phase B authority | Exact CLI/scan wiring and production supervised adapter |
| T009 | T008 | Retained-corpus offline acceptance, sibling/platform regressions; C2 |
| T010 | T009, C2, phase C authority | User documentation/release-note checkpoint and read-only convergence; C3 |
| V001 | T010/C3 plus explicit later live validation/disclosure grant | Real retained-corpus live age validation, separately gated |

Phase A is T001–T007, the earliest useful **offline internal end-to-end** task set.
Its prerequisites include actual file safety, entire framing, population, graph,
admission and veto propagation; injected positive dates do not waive them. No CLI
or production network path is needed for this slice. Phase B adds ordinary-user
integration and full deterministic acceptance; phase C closes docs/conformance.
Later authority may authorize several phases together, but cannot skip their
technical checkpoints. Implementation grants and phase boundaries remain explicit.

**C1:** fresh non-author review of the complete thin slice's population/arithmetic/
safe output and admission/filesystem/framing/privacy isolation. Close material
findings through the standing correction/fresh-verification procedure before T008.
**C2:** independent integration review after retained-corpus offline witness and
deterministic regressions, including sibling projection equality and real worker
lifecycle/capability results. **C3:** read-only final convergence across spec,
approved plan, graph, implementation, tests and docs. No checkpoint infers live
yield, actual Windows/hosted success or publication from a local simulation.

## Phase A — First useful deterministic slice

### T001 — Safe source selection and snapshots

- [x] **T001** — requirements S1/S2; AC01/05/14; plan P1/P2.

Deliver `sbom_model.py`'s narrow request/discovery/selection/snapshot/failure records
and `sbom_input.py`. Implement automatic bounded filename discovery, explicit
root-relative selection and disable behavior at the library seam; CLI flags are
T008. Reuse exact public Maven safety predicates/identity helpers, not its reader
scope/XML behavior. Bind root/ancestor/child descriptors, charge all specified
budgets, preserve observed candidate counts and snapshot one stable regular file.
No content probing across ambiguous candidates; no parser, permission or transport.

Verify deterministic zero/one/multiple candidate selection, exact depth/candidate/
entry/directory limits, included target/build and specified exclusions, explicit
unusual names/depths, missing/unsafe/changed files and finite reads. Injected reader
tests exercise portable selection; native reader tests cover links, ancestor links,
reparse/special-file refusals and identity races. Capability-refusal tests are
unskipped and prove no fallback I/O. Disabled mode constructs no SBOM reader.

Completion: focused `test_sbom_input`/request witnesses pass, all descriptors close
on every refusal, source statuses retain safe selection and no false population;
review-ready diff/verification and coherent local commit. Native tests may skip
only genuinely unavailable primitives, with refusal still verified.

### T002 — Whole framing and document subset

- [x] **T002** — requirements S2/S8; AC05/13/14; plan P3.

Deliver `sbom_json.py` and `sbom_document.py`, extending local record types only
as necessary. Validate the entire snapshot with bounded preflight/strict decode,
duplicate-key/nonfinite/Unicode and numeric/string/container/token limits, then
flat1.5 root/subject/record/ref framing. Preserve one exact root alias and encoded
global/per-record restrictions. Extract optional assertions as statuses, not trust.
Reject unsupported root versions/nested populations without a partial denominator.
No supervisor or lookup authority can exist at this stage.

Verify every S2 framing ceiling at/over boundary, trailing/late malformed data in
ignored subtrees, BOM, numeric overflow/overlong tokens, duplicate keys everywhere,
non-object entries, missing subject, optional malformed assertions, duplicate refs
and exact/mutated subject aliases. Use small synthetic JSON bytes in deterministic
tests; genuine retained SPDX examples are unsupported-format local witnesses under
T009, never network-fetched test fixtures. Spy process/socket seams stay untouched.

Completion: focused `test_sbom_json`/`test_sbom_document` pass; all whole-source
refusals produce no accepted inventory or lookup; optional assertion refusal stays
at its specified scope. Preserve failing input handling without echoing payloads.

### T003 — Identities, canonical inventory and restrictions

- [x] **T003** — requirements S3/S4/S6/S8; AC02/03/06/08; plan P4.

Deliver `sbom_identity.py` and canonical member records. Enforce literal Maven
purl/field agreement, exact/snapshot policy, jar/pom/war/classifier subset and
restriction-only repository_url parsing. Default type only where authorized.
Retain unsupported/conflicting/unidentifiable rows by source index with fixed
reasons. Group exact supported tuples, preserve multiplicities/alias restrictions
and keep distinct versions/variants. Preserve **all original reference/index
attribution** for T004; grouping never destroys the pre-collapse graph evidence.
Do not introduce a generic purl or semantic-version framework.

Verify purl absence/mismatch/ranges/snapshots, case/exact spelling, default versus
explicit jar, custom/test-jar/empty/repeated/unknown qualifier refusal, percent path
and percent-encoded repository restriction behavior. Duplicate tuples under
different refs count once; unknown records stay distinct; differing versions or
classifiers remain separate. Malformed identity is visible and cannot grant lookup.
Unit fixtures explicitly show N/support-exact/record counts and no module weighting.

Completion: focused `test_sbom_identity` passes with S8 precedence; package groups
and raw-ref attribution remain separately inspectable, no producer/current model
claim and no transport construction.

### T004 — Graph evidence before member collapse

- [x] **T004** — requirements S3/S6/S7; AC02/03/06/07/14; plan P4.

Deliver `sbom_graph.py` and final inventory relationship attachment. Validate raw
local reference nodes/edges; opaque purl-shaped refs are not fetch targets. Handle
absent graph, missing versus empty children, invalid graph refusal, service vertices
and subject exclusion. Use finite depth-class traversal for both path flags and
iterative whole-graph cycle detection, then attach ref-unioned member labels.
Emit no partial edges for an invalid graph. Unreachable components remain members.

Verify cycles reachable/unreachable, self/back edges, service-mediated paths,
direct-plus-longer paths, omitted graph nodes, missing/empty dependsOn, dangling/
external refs, duplicate node/edge, aliases with different incoming/outgoing edges
and missing component refs. The alias case must detect a manufactured path if an
implementation mistakenly traverses the collapsed package graph. All graph-bound
failure tests retain valid inventory and prohibit URL following.

Completion: focused `test_sbom_graph` passes; relationship counts partition N,
opaque references/order match output contract, invalid graph does not null N and
no enumeration of all possible paths or recursion-dependent cycle behavior remains.

### T005 — Comparator permission and existing invocation vetoes

- [x] **T005** — requirements S5/S8; AC06/08/09/10/12/14; plan P5.

Deliver pure `sbom_policy.py` plus the defaulted private Maven admission/report
veto tuple described by P5. Collect safe same-G/A existing policy decisions before
version/measurement filtering, propagate them unchanged through the ordinary
Maven result, and never serialize them. Reduce document/metadata/subject/global,
alias and known-invocation restrictions before creating admitted SBOM work.
No extra POM/config reads, fabricated current-checkout join or legacy scalar change.
This task provides permission data, not a production lookup/default worker route.

Verify missing-version ordinary row still vetoes same-G/A SBOM lookup when its
source policy is refused/unknown; catalogue/time/version failure alone never becomes
a namespace veto. Test system/private/conflicting/unknown/known Central exclusions,
global versus alias restrictions, one weak alias versus another refusal, positive
Central qualifier and unassigned alternate distribution/intake non-veto. No POM or
attestation is required for a standalone otherwise-admissible document. Assert zero
file/process/HTTP calls from pure policy and unchanged frozen Maven public output.

Completion: focused `test_sbom_policy` plus affected Maven admission/output/policy
regressions pass; every admitted work item has independently checked permission,
no permission is inferred from cached metadata or a reason rendered as prose.

### T006 — Injected measurement and SBOM summaries

- [x] **T006** — requirements S5/S6/S8; AC04/09/10; plan P5/P6.

Deliver `sbom_measure.py` and separate age/final report types. Require an explicit
supervisor factory at this seam for the first slice; do not add a default production
transport yet. Translate independently admitted rows to exact `MavenCapability`
objects; use select_target/pom_date operations and existing identity/time/order/
arithmetic contracts. Use the within-batch cache only after row admission and
reattach outcomes to distinct members. Produce N/M/coverage/measured-subset summary
and fixed reasons, including empty/no-measurement/source-refused cases.

Verify with a fake supervisor returning controlled `MavenTarget`/`MavenPomDate`
responses: positive365.25-day age, same-version accepted date zero, missing dates
even for same version, inverted timestamps flagged/clamped, unknown latest,
catalogue/used-version/date failures, budget/worker refusal and completed siblings.
Distinct classifier rows retain weight even when sharing GAV time evidence.
Assert operation identity/order and no fake inference from SBOM creation time.
All tests patch process/socket defaults to fail if accidentally invoked.

Completion: focused `test_sbom_measure`/summary witnesses pass; rows have age iff
reason is null, all numeric values are finite, N survives row failures and a failed
source is never converted into a0/0 report. No new ordering/date policy code.

### T007 — Safe projection and useful offline local-file slice

- [x] **T007** — requirements S1–S8/output contract; AC01/04/05/10/11/12; plan P1/P6/P7.

Deliver `sbom_output.py` and `sbom.py`'s internal pipeline using the existing
reader plus **required injected** metadata factory. Emit exact whitelist JSON and
aligned measured/refused ordinary/verbose tables. Include safe file/subject/basis,
summary, all refused members, opaque graph/ref identities, assertion/redaction and
reason counts. No CLI/ordinary-scan/default-production wiring in this task.

End-to-end witness starts with a real temporary regular-file **synthetic input
document**, not a prebuilt final report: safe snapshot→whole parser→population/
graph→permission→controlled metadata→arithmetic→summary→both output forms. Include
at least one positive measured member and one visible refusal, N=2/M=1/coverage0.5,
raw measured total1.0 from controlled dates, plus all-refused/empty/source-refused
variants. Verify committed synthetic section-example shapes using matching input/
metadata fixtures, without pretending their placeholder digests are actual hashes.
Use a representative real corpus component identity in an additional controlled
metadata case for AC04; label controlled dates synthetic, never real age evidence.

Verify no raw controls/URLs/absolute paths/contacts/producer diagnostics reach
ordinary, verbose or JSON output; escaped widths align; identity variants remain
distinct; no repeated Observed fields, invented N or summed view totals. Future
unselected-source/status branches must match output-contract shapes too.

Completion: focused `test_sbom_output`/`test_sbom_pipeline` and prior phase-A
regressions pass, **C1 independently approves** the complete thin slice, bounded
corrections freshly verified and full deterministic phase-A boundary suite passes.
This is the earliest useful offline end-to-end answer, not a live demonstration or
implemented ordinary CLI flow. Stop before T008 unless phase B is authorized.

## Phase B — Ordinary integration and retained-corpus acceptance

### T008 — CLI, isolated production adapter and existing output composition

- [ ] **T008** — dependencies T007/C1 and phase B authority; requirements S1/S5/S7/S8;
  AC01/09/10/11/12; plan P2/P5/P6.

Wire exact CLI options, sanitized misuse/abbreviation handling, optional independent
`MixedScanReport.sbom`, ordinary-scan ordering and formatters. Add the default
existing `MavenSupervisor` only at production integration, after ordinary workers
close; honor its process-wide deferred-cleanup guard. Pass only already-established
same-G/A vetoes and explicit existing transport configuration. SBOM gets its own
bounded allowance; neither permission nor caches/requests transfer from siblings.
No new generic offline/hosted acquisition option. Keep direct-file scans unchanged.

Verify CLI through its injected `scan` seam using the **real mixed orchestrator**
and fake SBOM supervisor, not a hand-built report. Test default unique discovery,
explicit unusual filename, disable/no SBOM reader or supervisor, incompatible/
repeated/unsafe options before scanning, ambiguous/incomplete discovery and selected
file refusal with safe attribution. Exercise ordinary, verbose, JSON, NuGet precision
and Maven plural paths. Patch worker/process boundaries for real-adapter orchestration
tests: exact capability type/whitelist, zero startup on no admissions, no second
worker after deferred cleanup, no retries/redirects/unsafe fallback. Existing trusted
worker lifecycle regressions verify installed-worker behavior separately offline.

Completion: focused `test_sbom_cli`/mixed/output/admission/worker-related regressions
pass; dropping sbom leaves every frozen existing JSON value unchanged, and existing
tables/failures retain their populations and values. SBOM-only ordinary output
leads with its useful section rather than an empty legacy success banner. No actual
target-derived registry request is required or authorized by this task's tests.

### T009 — Offline corpus, failure matrix and platform integration checkpoint

- [ ] **T009** — requirements S1–S8; AC01–AC14; plan P7/P8.

Complete behavioral/regression gaps and a separate local retained-corpus acceptance
record. Do not make the deterministic unit suite depend on private Git-directory
artifacts or network. Small committed synthetic fixtures cover stable regressions;
an explicitly invoked local verification path reads original hash-bound corpus
with injected metadata. Unit correctness and private real-corpus availability are
separate reported results. Do not copy unrestricted raw SBOMs into tracked fixtures.

Offline real-corpus witness checks exact Dependency-Track digest,201 input entries,
one exact subject alias,200 external members,21 services,43 direct/157 transitive,
424 edges; then uses controlled responses to exercise ages without claiming real
date yield. Compare all57 POM literal declarations/14 omitted tests only as separate
provenance, never a new SBOM denominator. Non-GitHub full/fragment and GitHub SPDX
artifacts refuse unsupported format. Missing original raw bytes leave this corpus
checkpoint incomplete; never regenerate a target/export or substitute synthetic
availability. An implementation grant should include access to the retained originals.

Freeze same-input metadata for full sibling projection equality: Python/npm/Ruby/
NuGet, explicit and ordinary NuGet, Maven Declared/Observed, absent/disabled/
positive/refused SBOM, accepted empty and unknown ordinary sources. Cover every
resource ceiling and late framing, policy/global-alias restrictions, graph path
corner, worker cancellation/timeout/deferred cleanup, offline provider failures
and output redaction/status branch. Prove sibling budgets and completed results
survive SBOM exhaustion. Run full deterministic suite, relevant real worker checks,
capability-disabled-before-discovery suite and actual configured OS/Python matrix
when hosted evidence is available under its own execution/publication authority.
Local capability simulation is not Windows/hosted success; pending external evidence
is explicitly reported, not fabricated or silently waived.

Completion: local deterministic/native/refusal/retained-corpus witnesses pass,
**C2 independent integration review approves** after any focused corrections, and
the validation record distinguishes passed, skipped and pending hosted obligations.
Required unresolved corpus or safety evidence prevents checkpoint completion;
publication/hosted availability does not license a new access attempt by implication.

## Phase C — Documentation and conformance

### T010 — User guidance and final read-only convergence

- [ ] **T010** — dependencies T009/C2 and phase C authority; S1–S8/output contract;
  AC01–AC14 traceability; plan P6–P8.

Document the actual ordinary invocation and explicit/disable behavior, bounds,
SBOM subject/population/coverage, exact versions/refusals, conditional Central
metadata disclosure and unchanged conventional date limitations. Explain local
versus hosted acquisition, offline failures and preserved siblings. Add the notable
implemented feature to CHANGELOG at this documentation checkpoint, not a release.
Keep public examples clearly synthetic unless separately validated real dates exist.

Run documentation/link/anchor/sensitivity/security/whitespace and approved acceptance
traceability checks; rely on the just-completed deterministic suite unless changes
warrant another run. Obtain **C3 fresh non-author read-only convergence** across
specification/output contract, plan, tasks, actual runtime/tests and user docs,
reconciling all scopes and freshly verifying material corrections. Preserve task
commit boundaries, raw evidence and actual remaining validation/publication gaps.

Completion: C3 approves, every mandatory deterministic criterion has a result,
final local scope/tree is verified and actual implemented status is recorded with
limitations. No inferred live yield, repository coverage or hosted-platform PASS.
No push/tag/release unless separately and explicitly authorized.

## Separately gated operational witness

### V001 — Real retained-corpus live age validation

- [ ] **V001** — dependencies T010/C3 and a **new explicit human validation grant**.
  Traceability S5/S6, AC02/04/09/10/11 and plan P7's later gate.

The grant must identify exact retained artifact digest, permitted public Maven
coordinate disclosure/lookup set, finite worker budgets, TLS/trust inputs if any,
capture/privacy and stopping scope. Do not infer it from implementation, a passing
offline witness or this graph. No new SBOM acquisition, target checkout/build/tool,
private registry or machine trust discovery is part of this witness.

Under that later grant, run one coherent ordinary SBOM age report on the original
bytes through admitted production metadata, capture safe ordinary/verbose/JSON
views from the same result, reconcile all component statuses/summary arithmetic,
worker closure and artifact integrity. Retain unmeasurable outcomes and offline/
provider unavailability distinctly; promise neither M nor an age total or complete
repository inventory. Independent evidence/privacy/usefulness review must approve
the actual result before claiming real age-yield validation.

Completion means that specifically authorized validation and its independent
review are complete, or a qualified unavailable/blocked record identifies what
was not established. V001 is **not a predecessor** of deterministic implementation
or T010 completion. Pending V001 means live yield unverified; it does not authorize
an access workaround or silently turn optional live work into a product-test gate.

## Acceptance traceability and execution restart

| AC | Principal tasks / checkpoint |
| --- | --- |
| AC01 | T001/T007/T008/T009; C1/C2 |
| AC02 | T003/T004/T009; C2; V001 only for actual live ages |
| AC03 | T003/T004/T005/T008/T009; C1/C2 |
| AC04 | T006/T007/T009; C1/C2; V001 for real lookup yield |
| AC05 | T001/T002/T007/T009; C1/C2 |
| AC06 | T003/T004/T005/T009; C1/C2 |
| AC07 | T004/T009; C1/C2 |
| AC08 | T003/T005/T009; C1/C2 |
| AC09 | T005/T006/T008/T009; C1/C2 |
| AC10 | T005/T006/T007/T008/T009; C1/C2 |
| AC11 | T007/T008/T009; C1/C2 |
| AC12 | T005/T007/T008/T009; C1/C2 |
| AC13 | T002/T009; C2 |
| AC14 | T001/T002/T004/T005/T006/T009; C1/C2 |

All rows feed T010/C3 final conformance; no table entry is evidence a witness ran.
Earliest execution is **T001**, after implementation authority for phase A, with
approved spec/output contract/plan/graph and safe local test workspace. Retained
corpus access is needed at T009, not a package-manager/build prerequisite for the
thin slice. No genuine product decision is presently unresolved. Stop this planning
run at **IMPLEMENTATION AUTHORIZATION**; do not mark any implementation task done.
