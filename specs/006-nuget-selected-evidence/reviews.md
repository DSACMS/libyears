# Feature 006 Reviews

## Decomposed independent specification review — 006-0003

**Date:** 2026-11-03. **Completion:** COMPLETE. **Verdict:** REVISE.
**Specification approval:** NOT APPROVED. **Validated material findings:** 2.
**Next gate:** SPECIFICATION CORRECTION; subsequent independent verification is
required before technical planning. No correction is performed in this run.

Reviewed baseline: `593fd1d0ee84b3895ac41b0337b8b2e860690539` (clean).
Frozen [specification](spec.md) SHA-256:
`ae3f79e266cc7ade9baa63fd7aee25dcc5a43e527d6e3676e75168a693ca4815`.
This matches the `006-0002` handoff. The specification remains byte-unchanged,
including its historical draft/self-audit/next-gate text. This record supplies
the current independent disposition without rewriting that history.

### Reviewer decomposition and independence

Three fresh non-author reviewers were commissioned with `fork_turns="none"`,
no model or effort overrides, separate scopes and the frozen digest. All three
read repository authority, the specification, reconciled discovery and retained
OASim experiment record directly. They received neither author conversation nor
current sibling conclusions; no sibling reports were shared before completion.
Historical reviews embedded in required discovery artifacts remain historical
evidence, not independent approval of this candidate. The parent waited for all
three completed reports before synthesis. Temporary reports remain outside Git.

| Reviewer | Assigned audit | Completed result |
|---|---|---|
| `/root/review_a` | NuGet declarations/lock/context/version/publication semantics, H1–H4 and empirical fidelity; primary Microsoft/NuGet references | MATERIAL FINDINGS; A1, raw request transformation |
| `/root/review_b` | Source authority, package/context/content binding, no namesakes, failures/denominators, privacy, input/network safety and no execution | PASS; no material finding in assigned slice |
| `/root/review_c` | Complete product contract, all 36 ACs, compatibility, metric, scope and exclusions | MATERIAL FINDING; C1, undefined selected-ambiguity trigger; 36/36 examined |

The parent independently read all required repository artifacts, the three
completed reports, relevant schema-v3 serialization in `libyears/output.py`,
availability aggregation in `libyears/scan.py`, arithmetic in
`libyears/metric.py`, and relevant existing metric/mixed-scan test assertions.
Those tests are compatibility references, not implemented NuGet acceptance
evidence. Product tests were not run for this documentation-only audit.
Actual child model/provider/effort/resource telemetry was unavailable. Fresh
assignments establish review separation, not independent resolver ground truth
or measured resource savings. Approval was not determined by majority vote.

### Validated material findings

#### F1 — Raw request transformation rejects supported normalized producer output

**Origin:** A1. **Owners:** S2 numeric requests; S3 request/Direct association;
S6 `declaration_lock_requirement_mismatch`. **ACs:** AC-06, AC-10, AC-11.

S2 supports two-, three- and four-component numeric minimum requests. S3 requires
the unnormalized declaration spelling inside exactly `[v, )` and explicitly
forbids version-spelling normalization. NuGet writes normalized range bounds.
Consequently a coherent declaration `Version="1.0"` and genuine lock request
`[1.0.0, )` fail the specified comparison; `Version="1.2.3.0"` and
`[1.2.3, )` fail likewise. The specification would label these ordinary producer
transformations requirement disagreements despite advertising the request forms
as supported. The three-component OASim examples do not substantiate this wider
raw-spelling transformation.

The parent independently inspected the primary source chain:
[lock serializer](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.ProjectModel/ProjectLockFile/PackagesLockFileFormat.cs)
uses `RequestedVersion.ToNormalizedString()`;
[range formatter](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Versioning/VersionRangeFormatter.cs)
normalizes its bound;
[version formatter](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Versioning/VersionFormatter.cs)
writes at least major/minor/patch and omits a zero revision.
[Microsoft's normalization reference](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning#normalized-version-numbers)
also documents zero-revision removal. This is source-based semantic validation,
not a restore experiment or a claim that arbitrary equivalent ranges are safe.

**Required later resolution:** reconcile the advertised numeric subset with an
explicit bounded producer transformation, or explicitly narrow that subset.
Acceptance evidence must cover real two-component and zero-fourth-component
normalization. Preserve requested-versus-selected separation, exact selection
from `resolved`, and the prohibition on a general range solver. Planning cannot
silently override S3. No such change is made here.

#### F2 — Selected ambiguity has no defined accepted input trigger

**Origin:** C1. **Owners:** S3 supported lock framing/unique association;
S6 `ambiguous_lock_evidence` and association precedence. **ACs:** AC-11, AC-31.

S3 allows one framework, one unique same-ID Direct entry and one selected
`resolved` value. Duplicate JSON keys, case-colliding identities and additional
frameworks reject the whole source. S6 nevertheless requires a dependency-level
ambiguity result for isolated multiple selected claims after safe association,
and AC-11/31 require its behavior and precedence to be independently testable.
No accepted representation for that condition is specified.

The parent independently checked the complete accepted framing and exclusions.
Repeated package IDs or `resolved` keys already have whole-source outcomes;
multiple frameworks are rejected. A list/object in `resolved` has no rule
selecting ambiguity over malformed structure or unsupported selected syntax.
A disagreeing witness version likewise has no defined mapping to this outcome.
Choosing one during planning would introduce an observable product decision.
This is a missing failure oracle, not a request to salvage duplicate identities.

**Required later resolution:** define the precise safely attributable trigger
and its precedence, or explicitly reserve the unreachable reason and reconcile
the mandatory acceptance obligation. Keep duplicate-identity whole-source
rejection. No representation or correction is invented in this run.

### Parent whole-contract reconciliation

| Gate | Independent parent assessment |
|---|---|
| H1 selection evidence | Faithful: only root `packages.lock.json` schema 1 supplies selection; explicit one-project activation; no assets/export fallback or generation. |
| H2 declaration/context | Population and accepted supplier limitations are faithful: one explicit SDK C# project/framework, bounded unconditional declarations, all-direct test/tool/analyzer inclusion and no evaluated-scope claim. F1 affects numeric request coherence; F2 affects the failure oracle. These prevent approval. |
| H3 source authority | Accepted testimony binds project/framework/bytes/package/selected identity/hash; explicit public origin precedes lookup; local disagreement prevents lookup; public agreement precedes measurement. Private/alternate/unknown/conflicting origins cannot query namesakes. Hashes do not prove origin or history. Hash-domain fitness limitation below remains explicit. |
| H4 publication | Faithful: identity-bound catalog `created` means first nuget.org receipt; greatest currently listed stable from complete SemVer-2-inclusive enumeration; no older dated fallback, date substitution, compatibility filter or archive reconstruction. |
| Failure/incompleteness | Whole-source unavailability preserves independently established N without fabricated package rows; unknown scope nulls denominator; individual failures retain M/N; validated empty differs from unavailable. Repository available rows survive. F2 is the bounded exception to deterministic failure testability. |
| Output compatibility | Schema v3/direct scope remains; only NuGet evidence is additive. Sibling identities, rows, evidence and summaries survive. NuGet unavailable numeric nulls do not retroactively change npm/Python/Ruby behavior. Partial evidence omits unestablished claims and protects private details. |
| Metric | Existing 365.25-day arithmetic, exact used=latest zero, flagged negative clamping and measured-only aggregates are preserved. |
| No execution | S8 expressly forbids dotnet/NuGet/MSBuild/package-manager/target execution, restore/install/resolution, import evaluation, archives, caches/config/credentials and input writes. External producer authority never transfers to the scanner. |
| Out of scope | Assets/package-list are research only. Transitive/project/implicit measurement, packages.config, general CPM/import/conditional evaluation, multiple TFMs/RIDs, private feeds, solution traversal and portfolio aggregation remain excluded. |

The parent rechecked first-receipt/hash fields against the
[catalog contract](https://learn.microsoft.com/en-us/nuget/api/catalog-resource)
and SemVer-2 enumeration/listing defaults against the
[registration contract](https://learn.microsoft.com/en-us/nuget/api/registration-base-url-resource).
The retained experiment supports 51 direct associations across ten contexts,
229 transitive occurrences, 15 project nodes and 92 closure origin/hash bindings.
Its shared producer, experimental locks, missing stale-pair experiment and lack
of public-age measurement are correctly qualified. No experiment is recast as
complete historical/evaluated scope or proven measurement yield.

### Acceptance accounting — 36/36 examined

This is coverage of the specification audit, not executed acceptance tests.
All 36 unique ACs were read and traced. Review C found 34 determinate and two
partially blocked by C1; parent validation of A1 also affects AC-06/10.
Thus 32 have no validated finding; four are affected by F1/F2. No requirement is
marked implemented or satisfied. The following preserves independent witness
directions and the final parent disposition without creating a technical plan.

| AC | Contract / independent acceptance evidence | Parent disposition |
|---|---|---|
| 01 | S1: exact project activation versus ordinary co-located-artifact scan | Auditable |
| 02 | S1/S6: invalid/repeated/abbreviated/path options exit 1; explicit missing project reports source failure/exit 0 | Auditable |
| 03 | S2: separate sole TargetFramework and single-valued TargetFrameworks populations | Auditable |
| 04 | S2/S6: multi/conditional/computed/duplicate framework, RID and invalid XML reject whole scope | Auditable |
| 05 | S2: all direct test/tool/analyzer/PrivateAssets count; project/framework/implicit packages do not | Auditable |
| 06 | S2/S3: numeric minimum forms retained; ranges/floats/brackets/expansion/prerelease requests rejected | F1: supported forms conflict with producer transformation |
| 07 | S2/S6: duplicates/case aliases and package-affecting unsupported constructs reject scope | Auditable |
| 08 | S3: schema 1 and sole context; closure kinds never enlarge measured membership | Auditable |
| 09 | S3/S6: bad schema/fields/context/duplicate JSON reject whole lock and preserve known N | Auditable |
| 10 | S3: Direct association uses resolved even when different from request; no solver | F1: numeric bound transformation needs reconciliation |
| 11 | S3/S6: isolated missing/mismatch/selected failures, zero lookup and no transitive fallback | F1/F2: false mismatch and undefined ambiguity trigger |
| 12 | S3/S4/S6: extra Direct/wrong context/stale digests reject; mtime/Git cannot repair | Auditable |
| 13 | S1/S4: explicit witness acceptance and required context/producer/baseline bindings; found witness untrusted | Auditable logical contract |
| 14 | S4/S6: absent/rejected witness unavailable; unsupported membership invalidates denominator | Auditable |
| 15 | S4/S6: absent/private/alternate/conflicting package origin produces zero public queries | Auditable |
| 16 | S4/S8: blanket switch/config/mapping/cache/identity/hash cannot authorize | Auditable |
| 17 | S4/S6: decoded local hash disagreement/unavailable evidence prevents lookup | Auditable |
| 18 | S4/S5: public lookup requires local authority; public identity/hash mismatch prevents measurement | Auditable requirement; empirical hash-domain limitation retained |
| 19 | S5/S7: only identity-bound created dates and first-receipt claim | Auditable |
| 20 | S5/S6: bad/missing/conflicting used or actual-latest dates; no substitutes/older fallback | Auditable |
| 21 | S5: complete SemVer-2 pages, listed defaults, numeric greatest stable | Auditable |
| 22 | S5/S6: incomplete/unsupported/conflicting identities cannot supply partial latest; no stable distinct | Auditable |
| 23 | S4/S5/S6: authorized unlisted/prerelease used versions; distinct package/version absence, no archives | Auditable |
| 24 | S5: numeric normalization/zero revision/suffix case/build identity and date-independent precedence | Auditable |
| 25 | S5: one-year arithmetic, equal-identity zero, anomaly clamping and measured-only totals | Auditable |
| 26 | S6: unknown project scope versus known N with unavailable lock; no fabricated failures | Auditable |
| 27 | S6: all-failed, partial, validated-empty and unavailable matrices | Auditable |
| 28 | S1/S6: successful siblings survive every NuGet failure; repository availability matrix | Auditable |
| 29 | S7: schema 3 presence/null/omission, partial safe evidence, ordinary/verbose compatibility | Auditable |
| 30 | S7: human/JSON identity/count/state/date/value agreement and supplier limitations | Auditable |
| 31 | S6/S7/S8: specified reasons/precedence/order invariance and no fabricated evidence | F2: ambiguity stage lacks independent trigger |
| 32 | S8: forbidden process/input/network accesses absent; target bytes unchanged; tests offline | Auditable |
| 33 | S1/S8: finite local limits and unsafe/nonregular/replaced input rejection without partial scope | Auditable; numeric bounds are later reviewed design |
| 34 | S5/S8: HTTPS destinations/redirects and finite response/request/time/rate-limit behavior | Auditable; destination/budget mechanics are later reviewed design |
| 35 | S4/S7/S8: adversarial secrets/paths/raw XML/witness/hash content never disclosed | Auditable |
| 36 | S1–S4/S8: excluded formats/context/source/portfolio cannot repair evidence | Auditable |

Specific parser/module structure, witness serialization, numerical resource
bounds, metadata destination enumeration and task organization remain design
work after specification approval. F1/F2 concern observable association/failure
behavior, so they cannot be resolved by silently choosing implementation details.

### Limitations, observations and verification

Review A identified a hash-domain question but did not establish a defect:
NuGet distinguishes signed-package content hashes from archive hashes; this
audit did not prove which signing-stage domain current catalog hashes describe
or demonstrate a mismatching selected package. The parent does not promote this
concern to a third finding or claim universal signed-package compatibility.
H3's accepted equality requirement is clear and fails closed on disagreement;
live useful yield and hash-domain fitness remain unvalidated. Any later semantic
correction must preserve human-approved H3 or return to human authority.

No live package metadata/age measurement, archives, raw historical temporary
experiment, external checkout, caches, credentials, config, producer execution
or target code was accessed. Primary-source URLs on upstream development branches
may change. No actual child model/effort/token/credit/runtime observations were
available. The audit is complete at specification level; its limitations are
not invented product findings or claims of implementation verification.

Run `006-0002` was appended exactly once from its 44-field handoff, enriched
only with authorized human session/model/provider/effort/agent-version/runtime
and account-continuity readings. Its `runtime_confounded=yes` and runtime note
remain verbatim; no credit delta is stored. All earlier ledger bytes remain
unchanged; `006-0001` and `006-0002` each occur once and every row has 44 fields.
Run `006-0003` and its children are not appended.

Verification confirms frozen specification bytes, unchanged discovery/history,
36 unique ACs, only the prior observation and this review artifact changed,
and `git diff --check` passes. One coherent local documentation commit contains
only those two files. No product code/tests, plan or tasks were changed or begun;
no push occurred. **Final verdict: REVISE. Next gate: SPECIFICATION CORRECTION.**


## F1/F2 correction and focused verification — 006-0004

**Date:** 2026-11-03. Candidate frozen before reviewer commissioning.
**Approval at freeze:** NOT APPROVED; focused independent verification pending.
Starting clean baseline: `56665a694ed7c65df3b1617fd0b4e57a34bec110`.
Corrected [specification](spec.md) SHA-256:
`f02a947ae33dc83afa08a800e0bd965f56e697317e40dd1c6209d133f3c73cc8`.
Word count: **4,997**, using whitespace-separated words (`str.split`).
The specification will remain byte-unchanged after commissioning; its status
section delegates approval and next-gate recording to the latest disposition
here, so review status cannot alter the reviewed candidate.

### Exact corrections and author self-audit

- **F1, S2/S3/S6; AC-06/10/11:** replace raw declaration-spelling insertion with
  bounded inclusive-minimum coherence. Supply missing patch zero, omit zero
  revision, retain nonzero revision; require canonical lock `[w, )` and equal
  numeric minimum bounds. `1.0` matches `[1.0.0, )`; `1.2.3.0` matches
  `[1.2.3, )`; `1.2.3.4` retains its fourth component. Five positive examples
  and explicit unequal-bound/unsupported-form negatives define the oracle.
  Equal selected outcomes cannot repair unequal requests. Unsupported project
  requests still reject scope; noncanonical/unsupported lock strings disagree,
  while missing/non-string requested evidence is malformed structure. No general
  range evaluator, satisfaction check or resolver is authorized. Declaration
  intent, original request evidence and lock-only selection remain separate.
- **F2, S3/S6; AC-11/31: choose B.** Remove the unreachable public failure reason
  `ambiguous_lock_evidence` and its precedence stage. One framework, one unique
  case-insensitive package key and one scalar selected value cannot produce
  multiple accepted Direct candidates. Repeated keys/case aliases and non-string
  selections (including arrays/objects) reject the whole lock as
  `invalid_lockfile`; extra frameworks remain `unsupported_lockfile_format`.
  Absent selected value remains `lock_version_missing`, unsupported selected
  string syntax remains `unsupported_lock_evidence`. No accepted ambiguous
  representation is invented.

Parent semantic verification used the primary NuGet
[lock serializer](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.ProjectModel/ProjectLockFile/PackagesLockFileFormat.cs),
[range formatter](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Versioning/VersionRangeFormatter.cs),
[version formatter](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Versioning/VersionFormatter.cs)
and [Microsoft version rules](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning#normalized-version-numbers).
The serializer normalizes RequestedVersion, the range formatter supplies the
inclusive/unbounded delimiters and the version formatter emits major/minor/patch
plus a nonzero legacy revision. This is source-based semantic verification,
not producer execution, live package measurement or empirical coverage evidence.
Development-branch source links may change. No OASim/raw experiment was needed.

The parent audited the complete corrected contract. All 36 AC identifiers remain
stable; only AC-06/10/11/31 wording changed. H1–H4's authority paragraph and S1,
S4, S5, S7, S8 remain byte-unchanged. All exclusions, known-denominator/source
availability distinctions, origin/hash/publication policy, metric and schema-v3
contracts remain intact. No new consequential product question or planning/
implementation authority was introduced. The historical 006-0003 hash-domain
fitness concern remains an **UNVERIFIED NON-FINDING**; no experiment or product
defect is inferred and useful measurement yield remains unvalidated.
`git diff --check` passed before freeze. This author audit does not approve the
specification or claim implementation acceptance; all AC checkboxes remain open.

Prior observation `006-0003` was appended exactly once from its 44-field handoff
with only the authorized human session/model/provider/effort/version/runtime and
account continuity readings added. Every other field, runtime_confounded=yes and
the existing runtime note remain verbatim; no credit delta is stored. All 24 data
rows have 44 fields; 006-0001 through 006-0003 each occur once and earlier ledger
bytes are unchanged. Current run 006-0004 and its reviewer are not appended.

### Fresh independent review and parent validation

**Reviewer:** `/root/f1_f2_verification`, one fresh non-author child commissioned
only after freeze, `fork_turns="none"`, no model/effort overrides. Actual child
model/provider/effort/runtime/credit telemetry is unavailable. No second reviewer
or repair cycle was used. The child independently read repository authority,
all three Feature 006 artifacts and the baseline diff, recovered relevant
truncated reads, verified the frozen digest/word count and consulted primary
NuGet sources. It made no file changes. Supporting evidence arrived separately
before its final verdict: **APPROVE (no material findings)**.

| Obligation | Independent evidence and parent disposition |
|---|---|
| F1 / AC-06 | Two-, three- and four-component declarations retain minimum meaning. All five S3 positive examples follow normalized serializer output, including omitted patch, zero revision and retained nonzero revision. Unsupported declarations still reject scope. PASS. |
| F1 / AC-10 | Same-ID Direct association compares only the supported normalized numeric bound; `1.0` versus `[1.0.1, )` fails even with shared `2.0.0` selection. Only resolved establishes selection; no satisfaction/resolution step. PASS. |
| F1/F2 / AC-11 | Negative request examples, malformed requested structure, missing Direct, absent selected string and unsupported selected string have distinct specified outcomes without lookup/fallback. Duplicates, case aliases and multi-value/non-string selections reject the whole lock; extra frameworks remain unsupported. PASS. |
| F2 / AC-31 | All retained S6 public reasons have reachable triggers. One accepted framework/key/scalar supplies at most one Direct candidate; removed ambiguity reason cannot be emitted. Whole-structure acceptance precedes association and malformed structure precedes unsupported structure. PASS. |
| Collateral | All 36 ACs read and reconciled with S1–S8. H1–H4, exclusions, supplier limitations, coverage, metric and schema-v3 compatibility preserved; no new consequential product question or embedded technical planning/implementation work. PASS. |

The reviewer audited the entire retained S6 reason set: project missing/invalid/
unsupported/duplicate; lock missing/invalid/unsupported and context mismatch;
witness missing/invalid and asserted unsupported influences; missing Direct,
request disagreement and missing/unsupported selected version; unsupported
origin; unavailable/mismatching hashes; authorized package/version absence;
missing usable creation date; complete enumeration without stable; invalid
registry response; and transport/service/budget failure. These are reachable
conditions, not claims that implementation fixtures already exist.

The parent validated the evidence against the frozen S2/S3/S6 and all 36 ACs,
rechecked the upstream serializer/formatter chain, and independently inspected
[NuGetVersion.IsLegacyVersion](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Versioning/NuGetVersion.cs)
(`Revision > 0`) and the
[version factory](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Versioning/NuGetVersionFactory.cs)
(missing numeric components become zero). This confirms the reviewer's
normalization claims rather than accepting its verdict alone. The accepted
framing and rejection rules leave no multiple-candidate representation to
exercise a dependency ambiguity code. Parent checks independently confirmed
unchanged H1–H4 and S1/S4/S5/S7/S8 bytes and changed AC wording limited to
06/10/11/31. No material collateral finding or new consequential question exists.
The unverified hash-domain fitness concern remains a non-finding; neither review
nor parent verification establishes live measurement yield or universal hash
domain fitness.

### Final disposition — current specification gate

**Completion:** COMPLETE. **Focused verdict:** APPROVE.
**Feature 006 specification status: APPROVED.** F1 and F2 are CLOSED.
**Acceptance accounting:** 36/36 specification obligations coherent; AC-06,
AC-10, AC-11 and AC-31 auditable. This is specification approval, not implemented
or executed acceptance; the 36 specification checkboxes remain open.
**Next gate: TECHNICAL PLANNING.** Planning has not begun and requires a separate
execution prompt. Implementation has not begun.

The approved specification is exactly the frozen candidate above, with no
post-commission edit, including no approval-only byte change. Approval is
recorded here through its status cross-reference. Historical 006-0003 REVISE
findings and hash-domain limitation remain intact. Only the prior observation,
F1/F2 specification correction and this review history enter one coherent local
Conventional Commit. Documentation/ledger integrity checks and
`git diff --check` pass; product tests were not run for documentation-only work.
No discovery/ROADMAP, product implementation/tests, plan or task changes, producer
execution, archives, external checkout, raw experiment or push occurred.

## Decomposed independent technical-plan review — 006-0005

**Date:** 2026-11-03. **Completion:** COMPLETE. **Final verdict:** REVISE.
**Plan status: NOT APPROVED. Validated material findings: 1.**
**Next gate: PLAN CORRECTION.** No correction, task decomposition or implementation
is performed in this run. Specification approval from 006-0004 remains in force.

### Candidate, authority and freeze

Starting clean HEAD: `62bfd38f6c96e821f2a4692a4e32b10e9ea8dae6`.
Approved specification SHA-256:
`f02a947ae33dc83afa08a800e0bd965f56e697317e40dd1c6209d133f3c73cc8`;
its bytes remain unchanged. The parent drafted and self-audited [plan.md](plan.md)
against S1–S8, H1–H4, F1/F2, all 36 ACs, existing model/source/scan/CLI/output/
transport seams and prior Ruby technical-plan conventions. `git diff --check`
passed before commissioning. Frozen candidate SHA-256:
`4a2e329a1eac2298c434aba436b1dfb99820836a413b794015055ca6c1ae40f3`.
Word count: **4,015** by whitespace-separated words (`str.split`). The plan was
not modified after commissioning, including no status-only edit. Its opening
status cross-reference points here for the current disposition.

### Independent review evidence

Three fresh non-author children received separate read-only assignments with
`fork_turns="none"`, no model/effort overrides and the exact approved specification
and frozen plan digests. No author conversation was inherited. Assignments were
concurrent; no sibling conclusions were shared before all three completed. Each
reviewer reconstructed relevant repository evidence directly. Existing historical
review records were available as historical authority, not current sibling input.
No reviewer wrote files, ran product tests, invoked producers or delegated further.
Actual child model/provider/effort/runtime/token/credit telemetry is unavailable;
requested no-overrides does not establish actual child configuration.

| Reviewer | Independent primary scope and completed result |
|---|---|
| `/root/plan_review_a` | PASS. Static complete-scope XML, schema-1 lock framing, direct/closure separation, framework association, F1 normalized minimums, F2 structural rejection, identity/stable ordering and local bounds. Relevant AC-03–12/21/24/25/31/33 witnesses credible. Independently recomputed both digests and checked primary NuGet normalization/serializer sources. |
| `/root/plan_review_b` | MATERIAL FINDINGS, B1 below. H3 origin/context/hash authority, namesake protection, H4 public resources/dates, local/network security, privacy and no execution audited completely. Other assigned obligations coherent; independently verified both frozen digests and primary Microsoft/Python sources. |
| `/root/plan_review_c` | PASS with planning AC coverage 36/36. Independently reconciled every AC mapping and current model/scan/CLI/output/metric seams, availability matrices, compatibility, deterministic strategy and K1–K6 gates. Digests supplied by parent, not independently recomputed by C. No missing planning evidence within its primary scope. |

C's cross-contract mapping review does not override B's transport-depth finding.
No majority vote determines approval. The parent waited for all final reports,
read their evidence and independently validated the material finding below.

### P1 — In-flight elapsed network deadlines are not designed

**Origin:** Review B / B1. **Affected obligations:** S8, AC-34; K2/K4.
**Disposition:** VALIDATED MATERIAL FINDING; unresolved in this frozen candidate.

The plan's network table promises a 10-second request timeout, 60-second package
elapsed budget and 300-second scan elapsed budget. Its enforcement text specifies
checking remaining elapsed budget before each request and reducing that request's
timeout. It reuses VerifiedJSONTransport with opt-in compression. No design
checks/cancels an in-flight operation at the absolute package/scan deadline, and
no concrete slow-response witness protects that distinction.

The parent inspected `libyears/registry.py`: `_get_restricted` passes timeout to
`opener.open`, then `_read_bounded_response` calls `response.read(limit + 1)`.
The documented [urllib timeout contract](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen)
is for blocking operations, not the total request lifecycle. A server can make
repeated progress inside the socket timeout while the body read continues beyond
the package or scan elapsed budget. Byte caps make total work finite but do not
establish the elapsed limits promised here. Pre-request checks cannot interrupt
that read. This is independent source/code validation, not a live slow-server
experiment or executed implementation failure.

**Required later correction:** specify an enforceable absolute-deadline mechanism
covering in-flight connection/response work and budget exhaustion, preserving
verified TLS, privacy, existing transport defaults and standard-library-only
runtime. Add a deterministic injected slow-response witness distinguishing
socket inactivity timeout from package/scan elapsed exhaustion. Do not silently
weaken S8, reinterpret elapsed budgets as admission-only checks, or rely on task
implementation to invent the missing transport architecture. Review the corrected
frozen candidate independently before approval. No mechanism is chosen here.

### Parent synthesis and acceptance accounting

**Traceability accounting: 36/36 ACs mapped and independently examined.** The
plan contains exactly one explicit component/witness/checkpoint row per AC.
35 have no validated planning defect; AC-34's intended witness is present but
insufficient for elapsed-deadline enforcement until P1 is corrected. Thus the
approval requirement of credible complete verification for all 36 is not met.
These counts concern planning evidence, not implemented or executed acceptance.

- F1 planning: PASS. AC-06/10/11 preserve omitted patch/zero revision, retained
  nonzero revision, five positive S3 pairs and different-minimum/shared-selection
  negatives; no selected-outcome shortcut, resolution or satisfaction check.
- F2 planning: PASS. AC-11/31 reject duplicate/case-aliased/multi-value selections
  as whole-lock malformed structure; additional frameworks remain unsupported;
  no NuGet dependency ambiguity reason or mismatch-row exact-selection claim.
- H1/H2: lock-only, explicit project/framework, all supported direct test/tool
  references, qualified baseline/coherence testimony, no evaluated completeness.
- H3: strict supplied witness, exact project/lock digests, context-bound per-package
  origin and local hash gate precede public metadata; catalog identity/SHA512
  agreement precedes authoritative dates. Supplier assertions remain distinct
  from independently observed public facts; no namesake fallback.
- H4: SemVer-2-inclusive complete registration, catalog leaves for selected and
  greatest listed stable, created-only first receipt, no older-date fallback.
  Parent checked the primary [registration](https://learn.microsoft.com/en-us/nuget/api/registration-base-url-resource)
  and [catalog](https://learn.microsoft.com/en-us/nuget/api/catalog-resource)
  resource contracts. Useful live yield/hash-domain fitness remain unverified
  non-findings; no public package-age measurement was performed.
- Integration: optional typed evidence, explicit fourth source pair, S6 matrix,
  schema-v3 additions, human/JSON correspondence and exact CLI validation are
  coherent. Parent checked existing SourceResult/summary/output/CLI code and
  relevant compatibility tests. C correctly notes current per-ecosystem
  unavailable-numeric handling is Ruby-scope-specific; NuGet must explicitly
  supply its condition at integration. The plan's S6 and AC-26–28 witnesses
  already require this; it is an implementation checkpoint, not a second defect.
- Determinism: synthetic directories, supplied lock/witness bytes, injected
  public responses/clocks and no-call guards; no network/dotnet/NuGet/restore/
  target execution required. P1 is the identified missing security witness.
- Checkpoints: K1 foundation; K2 transport/public adapter; K3 coherent integration/
  output/CLI; K4 offline acceptance; K5 separately authorized real-root evidence;
  K6 fresh convergence. No task graph is created by these phases.
- Scope: no assets/export product support, packages.config fallback, execution,
  CPM/general imports/conditions, multi-framework/RID, transitive measurement,
  private feeds, portfolio aggregation, metric or sibling policy change. No
  consequential product question was silently answered. P1 is within technical
  correction authority, not a reopened H1–H4 decision.

### Observation and repository integrity

Run 006-0004 was appended exactly once from the authorized 44-field handoff.
Only authorized human session/model/provider/effort/version/runtime/account
continuity fields enrich it; all other values remain exact, including
`runtime_confounded=yes` and its original runtime note. Credits 16/16 are
account-level continuity observations; no credit delta is derived or stored.
All 25 data rows have 44 fields; 006-0001 through 006-0004 each occur once.
Every earlier ledger byte is unchanged. Current run 006-0005 and children are
not appended. Its separate temporary 44-field handoff is outside Git.

Only the prior observation, frozen plan and this technical review record change.
Specification, discovery, ROADMAP and all product code/tests remain unchanged.
Documentation/ledger/digest/scope checks and `git diff --check` pass. Product
tests were not run for this documentation-only change. One coherent local
Conventional Commit is authorized; no push, implementation or tasks. The frozen
candidate is retained for the separately authorized PLAN CORRECTION gate.

## P1 correction and focused verification — 006-0006

**Date:** 2026-11-03. **Approval at freeze: NOT APPROVED.**
Starting clean HEAD: `17845b8f7bb5c07bf12616aa01171b926d0c9a8e`.
Only validated technical-plan finding P1 is corrected. Historical 006-0005
REVISE and its original frozen candidate remain above.

### Correction, self-audit and freeze

Corrected [plan.md](plan.md) frozen SHA-256:
`b340a41df7eee3e5e7e0b012c8976d7a79921a12960c3a156e212a004704c875`.
Word count: **5,168**, whitespace-separated (`str.split`). This file delegates
its approval status here and will remain byte-unchanged after commissioning.
Approved specification remains byte-identical at SHA-256
`f02a947ae33dc83afa08a800e0bd965f56e697317e40dd1c6209d133f3c73cc8`.

P1 correction distinguishes socket-operation timeout from absolute package and
NuGet metadata-scan deadlines. One isolated, trusted libyears Python worker
contains blocking DNS/connect/TLS/read, parsing and traversal. Parent monotonic
supervision cannot be reset by progress, reserves 0.5 seconds inside the 60/300
second budgets for terminate/kill/reap, rejects late results and suppresses later
requests after cancellation. Small bounded regular-file messages avoid blocking
IPC receives, shared locks and pipe/queue cancellation hazards. Normal, error,
interruption and unreaped-process paths have explicit cleanup/fail-closed rules.
Worker startup is offline, bounded readiness follows process creation, and the
plan explicitly records Python's noninterruptible process-creation and OS
scheduling limits rather than promising a hard real-time whole-CLI bound.

Parent checked authoritative Python 3.11
[urllib semantics](https://docs.python.org/3.11/library/urllib.request.html#urllib.request.urlopen)
and [subprocess lifecycle semantics](https://docs.python.org/3.11/library/subprocess.html#subprocess.Popen.wait).
The former exposes blocking-operation timeouts; the latter supplies bounded wait,
terminate/kill and the process-creation limitation. These support a process
supervisor, rather than a renamed socket timeout or uncancellable thread.
No live slow server, package-age experiment or implementation was executed.

AC-34 now requires fake-clock/process-controller witnesses for drip-feed progress,
blocked connect/TLS/header/body, package versus scan cutoff, late/exact-cutoff
results, termination escalation and cleanup faults; a mutation witness must reject
the former admission-only design. Separate offline real-worker lifecycle evidence
must prove cancellation reaches an actual blocking boundary on supported POSIX
and Windows CI. These are planning witnesses, not tests already passed.

Collateral self-audit: all **36/36** AC component/witness/checkpoint rows remain
unique and coherent with the approved S1–S8. AC-32 guards explicitly permit only
the installed trusted helper; package-manager/target execution stays forbidden.
Other mappings are unchanged except AC-34. H1–H4, F1/F2, source-authority gates,
content identity, created-only publication, complete listed-stable latest,
availability, privacy, metric, schema-v3 and sibling transport/output semantics
remain intact. No consequential product question or collateral finding was
established. `git diff --check` passed before freeze.

Prior observation 006-0005 is appended once from its exact schema-v1 handoff,
with only authorized session/model/provider/effort/version/reported-runtime and
account continuity readings enriched. runtime_confounded=yes and the original
runtime note are verbatim; no credit delta is stored. All 26 data rows have 44
fields; 006-0001 through 006-0005 each occur exactly once; earlier bytes are
unchanged. Run 006-0006 and its child are not appended.

### Fresh independent review and parent validation

**Reviewer:** `/root/p1_verification`, one fresh non-author child, commissioned
only after freeze with `fork_turns="none"`, no model/effort overrides. Actual
child model/provider/effort/runtime/token/credit telemetry is unavailable. No
second reviewer, delegation or repair cycle was used. The reviewer independently
read repository authority, all Feature 006 artifacts and the baseline diff,
recovered relevant truncated reads, recomputed both frozen digests and the plan
word count, and checked primary Python semantics. It changed no files.
**Completion: COMPLETE. Verdict: APPROVE; no material findings.**

| Obligation | Independent evidence and parent disposition |
|---|---|
| P1 / absolute deadlines | Blocking DNS/connect/TLS/header/body, parsing and traversal are confined to a killable worker. Fixed parent-owned monotonic deadlines and cancellation reserve remain independent of socket progress. No pre-request-only or thread-cancellation shortcut. PASS. |
| AC-34 regression witness | Drip-feed and separately blocked stages, earlier scan cutoff, exact/late results, socket-only mutation and real offline worker cancellation complement deterministic fake-clock arithmetic. Required future witnesses can catch P1's original defect. PASS at planning level. |
| Cleanup | Normal/interrupted/abrupt/ignored-termination/unreaped paths use finite wait, terminate/kill/reap, DEVNULL and bounded regular-file results; no blocking queue/pipe teardown or worker restart after cancellation. OS failure is systemic failure, not claimed deadline success. PASS. |
| Product fidelity | Installed trusted Python helper executes libyears, never scanned-target/package-manager code. Specification unchanged; H1–H4, F1/F2, source/content authority, dates, scope, privacy, availability, metric, schema-v3 and sibling behavior preserved. PASS. |
| Traceability/collateral | All 36 unique mappings read against the specification. No material collateral finding or new consequential product question. PASS. |

Parent independently validated the reviewer evidence against the frozen plan,
approved S8/AC-32/34 and the Python 3.11 contracts. `Popen.wait(timeout)` raises
on expiration rather than cancelling automatically; the plan explicitly sends
terminate and then kill, caps every wait, avoids context-manager/unbounded cleanup
and documents the different POSIX/Windows signals. Parent confirmed urllib's
blocking-operation timeout cannot supply this supervision and that subprocess
creation may itself be noninterruptible. Offline startup before the metadata
clock is explicit; no network is admitted until the command/deadlines exist.
These are ordinary process/OS enforcement guarantees, not a hard real-time claim.

The parent also checked the complete diff: nine unrelated architecture sections
are byte-identical, and only AC-32's exact trusted-helper guard and AC-34's witness
row changed among the 36 mappings. The added deadline design and verification
section, network-timeout clarification, trusted-helper fixture exception and
candidate provenance are confined to P1. No approved specification bytes changed;
no product-code/test or task graph changes occurred. The reviewer's APPROVE is
supported by mechanism and witness evidence, not accepted solely as a verdict.

### Final disposition — current technical-plan gate

**Completion: COMPLETE. Focused verdict: APPROVE. P1: CLOSED.**
**Feature 006 technical plan status: APPROVED.**
**Acceptance accounting: 36/36 coherent planning mappings; AC-34 architecture
and deterministic verification design PASS.** No implemented or executed NuGet
acceptance is claimed; all specification acceptance checkboxes remain open.
**Collateral material findings: NONE. New consequential product questions: NONE.**
**Next gate: IMPLEMENTATION TASK DECOMPOSITION.** A separate execution prompt is
required; no task graph or implementation is begun here.

Approved plan is exactly the 5,168-word frozen candidate above; no post-commission
or approval-only edit was made. Historical 006-0005 REVISE remains intact.
Hash-domain fitness/live useful yield remain unverified non-findings. Final
schema/digest/scope checks and `git diff --check` pass. Product tests were not run
for documentation-only work. Only the prior-run ledger row, P1 plan correction
and this review history enter one coherent local Conventional Commit. No
specification/discovery/ROADMAP/product code/tests, tasks, target or producer
execution, external checkout, archives, caches/config/credentials or push.
The complete current-run handoff is written outside Git; current run/child are
not appended to the canonical ledger.


## Independent task-graph gate — 006-0007

**Date:** 2026-11-03. **At freeze: NOT APPROVED; independent review pending.**
Starting clean HEAD: `1042e625a27c66bf4b011f08877dad157726ed14`.
Task decomposition is explicitly authorized; implementation, external validation,
Feature 007 and push are not. Run 006-0006 is already recorded; the ledger remains
unchanged. Run 006-0007 is handed off outside Git, never appended here.

### Author audit and frozen candidate

[Tasks](tasks.md) SHA-256:
`9e3fa72b5ff4aa903f842255e89118b672e645e5ab292ae9886f8d73cdb3dffe`.
Word count: **3,785**, whitespace-separated (`str.split`).
Approved specification and plan digests remain respectively
`f02a947ae33dc83afa08a800e0bd965f56e697317e40dd1c6209d133f3c73cc8` and
`b340a41df7eee3e5e7e0b012c8976d7a79921a12960c3a156e212a004704c875`.
All approval history was read alongside the current approved dispositions.

Author audit maps 36 unique ACs to one completion owner each and concrete
deterministic witnesses, checks 24 unique dependency-ordered nodes (18 tasks,
six review gates), and preserves F1/F2/P1, H1–H4, internal-only foundations and
coherent CLI activation. Mechanical AC ownership/dependency checks and
`git diff --check` pass. No implemented acceptance or independent approval is
claimed by self-audit. Product tests are not run for documentation-only work.

Candidate bytes are frozen before reviewer commissioning. No post-freeze repair
or approval-only task-file edit is authorized in this gate. Fresh non-author
reviewers receive separate scopes and inspect repository authority directly;
parent synthesis waits for all completed reports and validates material findings.

### Fresh independent review evidence

Three fresh non-author reviewers were commissioned after freeze, each with
`fork_turns="none"`, no model or effort override, an explicit read-only scope
and all three frozen digests. They directly read repository authority and the
complete current Feature 006 record, recovering truncated reads and independently
recomputing the matching digests. No author conversation was inherited, and no
current sibling conclusion was shared before all final reports completed.
No reviewer mutated files, ran tests, browsed, accessed targets, executed producers,
appended observations, committed or delegated. Actual child model/provider/effort/
resource telemetry was unavailable; requested settings do not establish it.

| Reviewer | Completed independent coverage | Result |
|---|---|---|
| `/root/task_review_a` | All 36 AC ownership/witness mappings; complete declarations, local task order, lock/F1/F2, version concepts, failure precedence and no invented decisions | COMPLETE / APPROVE; zero material findings |
| `/root/task_review_b` | H3/H4, local/public identity and hash authority, metadata completeness/dates/latest, security/privacy/caps, P1 supervision and controller/mutation/real-worker POSIX/Windows witnesses; inspected current reader/transport seams | COMPLETE / APPROVE; no material findings |
| `/root/task_review_c` | Whole dependency graph and review/commit boundaries, K1–K6, coherent activation, S6/S7/CLI, 36 AC ownership, documentation, required separately authorized validation/convergence; inspected current model/scan/output/CLI seams | COMPLETE / APPROVE; zero material findings |

### Parent reconciliation and final disposition

**Completion: COMPLETE. Task-graph verdict: APPROVE.**
**Feature 006 task graph status: APPROVED. Material findings: NONE.**
**Acceptance planning traceability: 36/36 unique owners and concrete deterministic
witness mappings; no implemented or executed NuGet acceptance is claimed.**
**Next gate: EXPLICIT PHASE-1 IMPLEMENTATION EXECUTION AUTHORIZATION
(T001–T006 and K1).** No task execution is begun by this disposition.

Parent reconciliation assesses the full gate rather than voting on slices:

- F1 remains the bounded normalized-minimum oracle, with all five positive pairs,
  unequal-minimum/shared-selected negatives and no resolver/satisfaction shortcut.
  T001/T003 supply concepts; T006 owns association and its exact evidence boundary.
- F2 remains whole-lock duplicate/case-alias/non-string selection rejection before
  association. T004/T006 and T014 cover reachable reasons and precedence, with
  no dependency ambiguity reason or selected provenance on request mismatch.
- P1 is a concrete T008 process/supervisor unit, with T007 transport and T009
  composition predecessors. The frozen plan's in-flight boundaries, fixed
  deadlines/reserve, bounded protocol/waits, no restart, cleanup/systemic faults,
  socket-only mutation and separate real-worker platform evidence are retained.
  Missing platform evidence cannot be presented as a passed gate.
- H3 local origin/hash authority precedes adapter use; public identity/hash
  agreement precedes dates. H4 complete listed-stable enumeration and created-only
  dates have concrete T009 witnesses. Privacy/no-execution safeguards accompany
  components and are composed by T014/K4, with only the trusted helper exception.
- Source availability remains distinct from individual failure and validated
  empty. Parent checked the current scan serializer's Ruby-specific unavailable
  numeric condition: T010/T011 explicitly require NuGet handling and regressions,
  rather than assuming the old condition suffices. Sibling evidence, metric and
  schema-v3 behavior retain dedicated integration/output/CLI verification.
- All dependencies point to earlier nodes; review gates are mandatory predecessors.
  T010–T012 stay internal until T013 activates scan, both reports, exact CLI and
  documentation coherently. K1–K4 separate implementation from independent review.
  K5 is required, cannot borrow discovery target authority and cannot become an
  optional smoke predecessor. K6 requires fresh read-only whole-feature convergence.

No omission, cross-slice contradiction or new consequential product/architecture
decision was established. Hash-domain fitness and useful live measurement yield
remain unverified non-findings. All 36 specification checkboxes remain open.
The exact 3,785-word candidate remains unchanged after commissioning, including
no approval-only edit. The approved spec/plan, discovery, ROADMAP and ledger remain
byte-unchanged. Historical findings and review dispositions remain intact.

Verification: matching approved/frozen digests, 36-owner accounting, 24-node
acyclic predecessor check, resolving local task links, unchanged authority/ledger
bytes, 44-column ledger shape with 006-0006 once and 006-0007 absent, and
`git diff --check`. Product tests were not run for documentation-only work.
Only tasks.md and this appended review record enter one coherent local
Conventional Commit. The complete 44-key run handoff is written outside Git at
`/tmp/libyears-observations/006-0007.json`. No implementation, Feature 007,
external validation/producer execution, forbidden filesystem access or push.


## Foundation implementation and K1 freeze — 006-0008

**Date:** 2026-11-03. **At freeze: independent K1 review PENDING.**
Starting clean HEAD: `d5e9472644a4d5478ca0dcd45b1480278f18bd5e`.
The commissioning human authorizes exactly T001–T006, local task commits and K1,
with native decomposition where dependency readiness permits. Implementation
remains internal; T007, external validation targets, Feature 007 and push are
hard stops. The approved spec/plan/tasks remain byte-unchanged at their recorded
digests. Historical task-file pending language is preserved with execution state
recorded here.

### Task execution and author verification

Each mandatory predecessor completed before its successor began. The graph has
no parallel-ready implementation nodes in this phase. Six fresh child authors
(`author_t001` through `author_t006`, `fork_turns="none"`, no overrides) each
owned one task's code/tests; the parent inspected their changes, ran verification
and created one coherent local commit per task. They are authors, not independent
K1 reviewers. Actual child model/effort/resource telemetry is unavailable.

| Task | Local commit | Implemented surfaces and verification |
|---|---|---|
| T001 | `4b1ed83` | Optional safe NuGet model records, separate bounded request/selected/stable version helpers; version/model/metric/output: 55 tests PASS. |
| T002 | `47233b0` | NuGet-local descriptor reader, exact bytes, bounded strict JSON/XML primitives; input plus scoped Ruby regressions: 75 tests PASS. |
| T003 | `3717fa0` | Two-pass complete XML project parser, conservative literal scope and immutable declarations; project/input/version: 47 tests PASS. |
| T004 | `ab54103` | Whole schema-1 lock framing and F2 structural rejection, closure separated from population; foundation suite: 69 tests PASS. |
| T005 | `efa6950` | Version-1 supplied witness, exact byte/context/SDK binding, private origin/hash authority; foundation suite: 85 tests PASS. |
| T006 | `677ded3` | Internal source composition, F1 canonical minimum association, staged evidence, availability and typed authority pairs; foundation suite: 98 tests PASS. |

Behavioral tests accompany every task. Real cap/cap+1 witnesses include local
bytes, JSON depth/values/strings/digits, XML depth/elements/attributes, 10,000
references and 50,000 lock/witness entries. The synthetic fixture README explains
supplier assertions and their limits. The local reason-trigger table enumerates
17 source/dependency reasons and checks their reachable triggers; public reasons
and composed final acceptance remain later-task obligations. Pre-freeze author
inspection corrected empty present selection to unsupported syntax, distinct from
absent selection, before the T006 commit.

Phase-boundary command `python -m unittest discover -s tests`: **499 tests PASS**.
Focused command `python -m unittest discover -s tests -p 'test_nuget*.py'`:
**98 tests PASS**. `git diff --check` passes; tree clean at the implementation
freeze. All tests are offline. No public activation, transport/worker, external
target, producer/package-manager execution, archives, configuration/cache/credential
inspection or push occurred. P1 remains preserved for its authorized later phase;
no deadline-enforcement implementation is claimed here.

### Frozen implementation checkpoint

**Candidate commit:** `677ded3545b513d9b121ca6d1c9a70866059e6f2`.
**Baseline:** `d5e9472644a4d5478ca0dcd45b1480278f18bd5e`.
This commit preserves all reviewed implementation/test bytes. No code/test repair
will occur after commissioning. This execution record is author evidence, not K1
approval. Fresh non-author review will inspect F1/F2, complete scope, whole-source
precedence, safe input limits, local authority/no-call proofs, evidence omission
and T001 default-record compatibility. Parent reconciliation must cover interactions
and validate findings rather than vote on slices. Under the approved task graph,
REVISE requires separate bounded correction authorization; INCOMPLETE remains
incomplete review evidence, not an inferred product defect.

Prior run 006-0007 is recorded exactly once in `06e16ce` from its machine handoff,
with authorized human status enrichment and account continuity readings 18/19.
Its original runtime note and confounding classification and earlier ledger bytes
are preserved; no credit delta is stored. Current run 006-0008 and children are
not appended. Its complete handoff will be written outside Git before reporting.


### Independent K1 review and parent reconciliation

Three fresh non-author reviewers were commissioned only after freeze, with
`fork_turns="none"`, no model/effort overrides, separate primary scopes and the
exact candidate/baseline. They directly inspected authority/code/tests, recovered
truncated reads and independently verified approved digests and frozen bytes.
No current sibling conclusions were shared before all reports completed. None
changed files, delegated, committed, used network, accessed external targets or
executed producers. Actual child settings/resource telemetry remain unavailable.

| Reviewer | Completed primary coverage | Completion / verdict |
|---|---|---|
| `/root/k1_scope_review` | Version concepts, complete project population, F1/F2, whole-lock structure, context/closure, precedence, evidence omission and local limits | COMPLETE / REVISE; one material finding |
| `/root/k1_authority_review` | Safe reader and all local bounds, whole witness/context/baseline, origin/hash authority, denominator/privacy/no-call/no-execution protections | COMPLETE / REVISE; same material finding independently reproduced |
| `/root/k1_contract_review` | Default model compatibility, source availability/empty states, local reason witnesses, staged evidence, candidate/authority pairing, internal activation boundary and maintainability | COMPLETE / APPROVE in assigned slice; no finding |

Independent scope/authority reviews each ran the 98-test foundation suite; scope
also ran 3 model, 13 metric and 30 output tests. Contract review independently ran
the 98-test foundation and full 499-test suites. All passed, as did diff checks.
Passing tests did not cover the boundary below and do not override its reproduction.
The parent inspected all completed reports and independently reproduced Direct
and Transitive variants. The two reports establish one overlapping finding, not
two separate defects. The positive compatibility slice does not overrule it.
No assigned review obligation remains unaudited; later-phase obligations remain
pending by design rather than making this K1 review incomplete.

#### K1-F1 — Lock version limits fail to reject the whole source

**Disposition: VALIDATED MATERIAL FINDING; OPEN.**
**Owners:** T004 whole-lock acceptance; T006 composed failure precedence.
**Affected obligations:** local version/component bounds, AC-33 and local AC-31;
whole-source availability/no-capability behavior.

`libyears/nuget_lock.py` `_entry` checks `resolved` only for string type. It does
not enforce the plan's 256-character version and 32-digit numeric-component
limits. T001's selected helper correctly rejects overflow, but T006 then converts
it into dependency-level `unsupported_lock_evidence`; Transitive entries do not
reach that helper and can leave unrelated Direct authority available.

Approved plan's local-bound table and whole-source classification, and spec S8,
require lock resource overflow to reject the entire source as
`unsupported_lockfile_format`. This differs from ordinary unsupported selected
syntax, which remains an isolated `unsupported_lock_evidence` result. No new
product decision is needed to identify that distinction.

**Exact offline witnesses**, using an otherwise accepted project, schema-1 lock
and correctly byte-bound supplied witness:

- Direct `resolved = "1.2+" + "a" * 253` (257 characters), or
  `resolved = "1." + "9" * 33`: actual source errors empty, one dependency
  `unsupported_lock_evidence`, N=1, measurement available. Parent reproduced both.
- Add a Transitive Helper with `resolved = "1.0-" + "a" * 253` or
  `resolved = "1." + "1" * 33` and a string hash to the otherwise valid direct
  fixture: actual source errors and dependency failures empty, one Direct
  LocalAuthority retained, N=1, measurement available. Parent reproduced both.

**Expected in all cases:** whole-source `unsupported_lockfile_format`, known N
retained, measurement unavailable, no dependency rows or authority capabilities.
Existing tests exercise general strings/counts/framework bounds but miss these
stricter lock-selected-version limits and their composed source outcome. The
candidate and tests remain unchanged so the failure evidence stays reproducible.

A later bounded correction must enforce consuming lock-version resource bounds
before association, add Direct and Transitive boundary/overflow witnesses and
whole-source/precedence/no-capability assertions, preserve F1/F2 and isolated
ordinary unsupported syntax, freeze the corrected candidate, and obtain fresh
focused non-author verification plus relevant regressions. This describes the
closure obligation; it does not authorize or perform the correction.

### Final K1 disposition — current implementation gate

**Review completion: COMPLETE. K1 verdict: REVISE.**
**Validated material findings: 1, K1-F1 OPEN. Foundation checkpoint: NOT APPROVED.**
T001–T006 have reviewable implementation commits and passing executed tests;
the pre-freeze author completion claims above do not establish final acceptance.
T004's consuming-version bound and T006's composed outcome require correction;
AC-33/local AC-31 are not marked complete. No specification checkbox or approved
spec/plan/task bytes are changed. Other assigned reviewed surfaces established
no additional material finding; final feature acceptance is not claimed.

**Next gate: SEPARATELY AUTHORIZED BOUNDED K1 CORRECTION AND FRESH VERIFICATION.**
The approved task graph explicitly requires separate bounded correction
authorization after REVISE. The commissioning prompt permits correction only
when the workflow/task authority clearly allows it; it does not override that
requirement. Therefore no correction cycle occurs in this run. Stop before T007;
no adapter, P1 worker, external validation target, Feature 007 or push is begun.
Historical F1/F2/P1 remain preserved; K1-F1 is a new implementation finding, not
reopening the approved product decisions. Useful live yield/hash-domain fitness
remain unverified non-findings. The full offline suite's 499 PASS and focused
98 PASS remain valid test results, with the uncovered boundary explicitly retained.


## K1-F1 bounded correction and focused verification — 006-0009

**Date:** 2026-11-03. **At freeze: NOT APPROVED; focused review pending.**
Starting clean HEAD: `b4372c5b9dcacfe69c391fe9708d30a4eef6b794`.
The commissioning human authorizes correction of only validated K1-F1,
local Conventional Commits, freeze, fresh non-author focused verification and
parent validation. T007, Feature 007, external targets, producer/target execution
and push remain hard stops. Historical 006-0008 REVISE evidence remains intact.
Approved spec/plan/tasks retain their recorded frozen digests and bytes.

### Bounded correction and author evidence

`nuget_lock.py` now checks version text during complete lock validation:
`requested` and `resolved` on every entry, plus every dependency-map request
on Direct, Transitive and Project nodes. The same 256-character and 32-decimal-
digit bounds apply before association, without parsing ranges, converting
numbers or requiring closure packages to become measurable/public-authorized.
Decimal runs are checked even inside request punctuation. Overflow is accumulated
as unsupported structure; whole-structure malformed findings still win regardless
of entry/context ordering. The existing source mapping yields
`unsupported_lockfile_format`, retains independently established N, marks
measurement unavailable and emits neither dependency rows nor LocalAuthority.
Within-bound unsupported selected syntax retains its isolated behavior.

Deterministic witnesses added to `test_nuget_lock.py` cover cap/cap+1 for all
accepted version-bearing fields and closure kinds, component limits inside
ranges and malformed-before-overflow precedence under entry/context permutations.
The general 16-KiB string witness now uses contentHash, whose general bound is
unchanged, rather than a request subject to the stricter version bound.
`test_nuget_source.py` reproduces all four exact 006-0008 Direct/Transitive
failure shapes with correctly byte-bound supplied witness, source filename,
known N, unavailable measurement, absent accepted-lock evidence and no rows or
capabilities. Further witnesses cover every closure request kind, overlong Direct
request before missing witness, malformed precedence, exact transitive bounds
and ordinary within-bound unsupported closure syntax with unrelated Direct
authority preserved. Existing F1/F2 and isolated unsupported-selection tests pass.
Input byte invariance, restricted reads and no-network/no-process guards remain
active in the composed source harness.

Verification before freeze: focused lock **25 PASS**, focused source **16 PASS**,
NuGet foundations **104 PASS**, complete deterministic suite **505 PASS**;
`git diff --check` PASS. Final composed precedence assertions were added after
the first full run; focused lock/source and the full 505-test suite passed again.
This is author verification, not independent approval or a new all-AC audit.

Candidate code/test SHA-256 values at freeze:

| File | SHA-256 |
|---|---|
| `libyears/nuget_lock.py` | `28f5d71b64cf22d3aebcc856270ddeec501212fa2ec9baff6416d8a487c7c9e0` |
| `tests/test_nuget_lock.py` | `42080ee03e86c505d474a81c9393775969d2528cd4fc22e1661e5164bd87f7f7` |
| `tests/test_nuget_source.py` | `47b1377d7a1a55ffac7122cc163038d413a49ac8af8343e92cc13918fc1d9c4f` |

The correction commit containing these bytes is the frozen candidate; review
commissioning identifies its exact hash. No code/test edits occur after freeze.
Review verdict and checkpoint disposition will be appended here separately.

Prior run 006-0008 was appended once in `ff08f60` from its 44-field handoff,
with authorized human /status fields and account continuity readings 19/22.
Its runtime_confounded=yes and original runtime note are preserved verbatim;
no credit delta is derived/stored and all earlier ledger bytes are unchanged.
Run 006-0009 and its reviewer are not appended. Git commit needed escalation
because sandbox index-lock creation failed; this is runtime confounding, not a
product failure. The current run's complete handoff remains outside Git.

### Fresh focused review and parent validation

**Frozen correction commit:** `a10459862b58c1b48605dfeb642c05d7c1e7b176`.
**Baseline:** `b4372c5b9dcacfe69c391fe9708d30a4eef6b794`.
One fresh non-author child `/root/k1_focused_verification` was commissioned only
following that commit, with `fork_turns="none"` and no model/effort overrides.
Actual child settings/resource telemetry is unavailable. The reviewer directly
read workflow and complete current Feature 006 authority/relevant discovery,
recovered truncated reads, independently verified authority/candidate hashes and
inspected underlying implementation, tests and diff. It made no file changes,
commits, delegation, network/target accesses or producer/target execution.
**Review completion: COMPLETE. Focused verdict: APPROVE. Material findings: NONE.**

| Focused obligation | Independent evidence and parent disposition |
|---|---|
| K1-F1 exact shapes | All four historical Direct/Transitive overflows reject the whole lock as unsupported_lockfile_format with known N, unavailable measurement, no rows/capabilities and no accepted-lock format claim. PASS. |
| Complete accepted structure | requested/resolved bounds apply to every entry and request values in Direct/Transitive/Project closure maps; closure cannot evade validation because it is unmeasured. PASS. |
| Boundaries and precedence | Exact caps accepted; ordinary within-bound unsupported selections remain isolated; malformed framing wins over overflow under entry/context permutations; lock overflow precedes witness/association. PASS. |
| Collateral | F1 canonical minimum comparison, F2 malformed whole-lock rejection, staged evidence omissions, origin/hash/no-call/privacy guards, T001 default compatibility and internal-only activation preserved. PASS. |

Reviewer independently ran **104 foundation tests** and **505 full deterministic
tests**, plus **29 additional composed cases** covering exact historical shapes,
closure kinds, N=0/N=2, byte invariance and explicit capability-construction
guards. All passed, as did `git diff --check`. This is focused closure and relevant
collateral verification, not a second complete feature/36-AC acceptance audit.

Parent validated the report against the approved local-bound table, S3/S6/S8,
T004/T006/K1 and frozen implementation. Separate parent execution reproduced all
four exact shapes with corrected source outcomes; temporarily bypassing the new
bound checker reproduced the prior isolated Direct failures and retained
Transitive authority, demonstrating the witnesses discriminate the defect.
No repository bytes were mutated by that check. Parent also independently checked
malformed-versus-closure-overflow precedence in both entry orders and **12**
additional N=0/N=2 cases across all closure kinds and both overflow classes, with
capability construction forbidden. All passed. Complete-parser placement and
accumulated findings support the review's whole-source and precedence claims;
no consequential missing decision or collateral material finding was established.

### Final disposition — corrected K1 checkpoint

**Completion: COMPLETE. Corrected K1 verdict: APPROVE. K1-F1: CLOSED.**
**T001–T006 foundation checkpoint: APPROVED.** This supersedes the historical
006-0008 checkpoint REVISE while retaining its original finding and reproduction.
T004 consuming bounds and T006 composed outcome now satisfy this checkpoint's
AC-33/local AC-31 closure obligations. Full feature acceptance, specification
checkboxes and later-task AC ownership remain pending; historical F1/F2/P1
approvals and frozen spec/plan/tasks remain unchanged.

**Next gate: EXPLICIT PHASE-2 EXECUTION AUTHORIZATION (T007–T009 and K2).**
Stop before T007. No adapter/worker implementation, public activation, external
validation target, Feature 007 or push occurred. Useful live yield/hash-domain
fitness remain unverified non-findings. Final checks verify unchanged frozen
code/tests and approved authority, prior-ledger bytes/44-field schema/unique IDs,
006-0008 present once, 006-0009 absent, and `git diff --check`. Only this appended
review disposition changes after freeze; its local Conventional Commit preserves
the exact reviewed correction. The complete current-run handoff is written to
`/tmp/libyears-observations/006-0009.json` before final reporting.


## Partial adapter phase and independent verification — 006-0010

**Date:** 2026-11-03. **Partial-phase verdict: REVISE.**
**Local assigned audits: COMPLETE. Phase completion: INCOMPLETE.**
**Validated material verification findings: 1, T008-V1 OPEN.**
**K2: NOT DEPENDENCY-READY / NOT APPROVED; no K2 approval is claimed.**
Starting clean HEAD: `dfe3b5abe0c640ff21f51512d12965b6bb10d0f2`.

### Authority, execution and candidate freeze

The commissioning human approved corrected T001–T006/K1 and authorized exactly
phase 2, T007–T009 through K2, local task commits and native decomposition.
The approved task graph remains the authority for mandatory predecessors and
required verification. T008 requires real-worker evidence on supported POSIX and
Windows; the existing CI matrix includes Windows, but no execution of the new
witnesses on Windows is available in this environment. Configured CI is not
passed evidence. Therefore T008 cannot be marked complete, T009 is not ready,
and the K2 node cannot be reached. No successor is begun by treating this gap
as an optional smoke check or waiving an approved obligation.

Two fresh child authors, `/root/transport` and `/root/worker`, used
`fork_turns="none"` without model/effort overrides. T008 began only after the
parent validated and committed T007. Each owned its task code/tests; the parent
inspected changes, ran verification and made the task commits. Actual child
settings/resource telemetry remain unavailable. Approved spec/plan/tasks retain
their frozen hashes and bytes; execution status is recorded here, not by editing
those authority artifacts. F1/F2/P1 and corrected K1/K1-F1 remain preserved.

| Task | Candidate commit | Implemented behavior / status |
|---|---|---|
| T007 | `4705a22` | COMPLETE within task scope. Opt-in bounded gzip and safe 503 Retry-After support; unchanged transport defaults/get(url) doubles; exact public metadata URL purposes, bounded JSON, package/scan counters, cooldown and admission checks. Absolute cancellation is not claimed from socket timeouts. |
| T008 | `ff65b02` | Implementation candidate; NOT COMPLETE. Trusted isolated worker, offline readiness, private cwd/DEVNULL, bounded atomic regular-file commands/results, fixed parent deadlines and cancellation reserve, finite terminate/kill/reap, typed safe publication/state results and deferred cleanup. Local verification below passes; Windows evidence and T008-V1 remain outstanding. |
| T009 | None | NOT STARTED: mandatory T008 predecessor is incomplete. Registration/catalog traversal, public hash/date gates and complete latest selection remain unimplemented. |

**Frozen partial-phase candidate:**
`ff65b026fae723d631f0170fb52ccb34ebea2f8e`.
**Baseline:** `dfe3b5abe0c640ff21f51512d12965b6bb10d0f2`.
Code/tests were committed before independent commissioning and remain unchanged
after freeze. The T008 commit explicitly retains incomplete Windows verification;
a reviewable implementation commit does not establish task acceptance.

The future T009 worker handler seam is
`lookup_authorized_package(authority, client) -> PackageResult`, lazily imported
only after a command. It is deliberately absent now. Startup/readiness is offline;
the retained client will own index/counters/cooldown across sequential commands.
No scan/CLI/output activation or synchronous network fallback is introduced.

Author/parent verification: T007 transport **12 PASS**, shared registry **18 PASS**,
PyPI **25 PASS**, npm registry **13 PASS**, RubyGems registry **29 PASS**;
T007 shared-boundary full suite **517 PASS**. Final T008 worker **21 PASS** and
full deterministic suite **538 PASS**, including closed foundation regressions.
The earlier parent NuGet-only run was **136 PASS** before the final socket-timeout
witness was added; the final 538-test full run includes that additional witness.
Parent also independently checked protocol exact 16-KiB cap, cap+1 rejection,
atomic nonpublication on overflow, symlink rejection and nonblocking FIFO
rejection. Diff checks pass. All execution was offline; real process tests launch
only the installed trusted Python helper or explicit trusted blocking fixture.

### Fresh independent partial-phase review

Two fresh non-author reviewers were commissioned after freeze with
`fork_turns="none"`, no model/effort overrides, the exact candidate/baseline and
separate scopes. They reconstructed complete current authority directly,
recovered truncated reads and verified the frozen candidate/approved digests.
No current sibling conclusions were shared before both completed reports.
Neither changed files, committed, delegated, used network/external targets or
executed producers/target code. Their assignments explicitly distinguish partial
verification from approval/execution of the non-ready K2 node.

| Reviewer | Completed assigned local coverage | Result |
|---|---|---|
| `/root/review_transport` | Shared transport/default compatibility; URL purposes, gzip/JSON and work caps, cooldown/admission, local authority interaction and static worker handoff | COMPLETE / APPROVE only in T007 slice; no material finding. Independently ran **121 PASS**: transport 12, shared registry 18, PyPI 25, npm 13, RubyGems 53. |
| `/root/review_worker` | Trusted bootstrap, protocol, parent deadlines/reserve, late results, lifecycle/cleanup/deferred faults, client retention and controller/mutation/local real-worker witnesses | Local assigned audit COMPLETE / REVISE; one verification finding below. Independently ran worker **21 PASS**, full **538 PASS**, and discriminating no-command mutation. T008 verification remains INCOMPLETE. |

Both confirmed clean frozen bytes and passing diff checks. Positive transport
coverage cannot overrule the worker finding or establish absent T009 composition.
Windows lifecycle evidence, T009 public resource/identity/hash/date/listing/latest
behavior, composed scheduling/budget allocation and remaining K2 reconciliation
are explicitly outstanding. Later integration/activation/acceptance is outside
this partial review. No full AC-18–23/34 or phase acceptance is claimed.

### T008-V1 — Real-worker witness does not prove blocking-handler entry

**Disposition: VALIDATED MATERIAL VERIFICATION FINDING; OPEN.**
**Owner:** T008; plan AC-34 real-worker witness (plan lines 404–410).
The required evidence must show cancellation reaches an actual blocking boundary.
`RealWorkerTests.test_offline_blocked_worker_cancelled_with_outer_watchdog`
asserts cancellation, OS process exit, temporary-directory removal and an unfired
outer watchdog, but never observes entry into the trusted fixture's `block`
handler. Worker readiness precedes command processing; an idle ready worker can
satisfy every current assertion without entering the injected blocking operation.

The reviewer suppressed publication only when the parent's `write_message` path
was `command.json`, leaving other protocol behavior and the separate worker
unchanged. One command was suppressed; the existing real-worker blocking test
still passed. The fixture remained in the no-command polling loop, so its
blocking handler could not have run. Parent independently reproduced this exact
mutation against the frozen candidate with unittest/mock and the same result:
**one suppressed command, one test PASS**. No repository bytes were modified.

Reproduction seam: patch `libyears.nuget_supervisor.write_message` with a wrapper
that returns without writing `command.json` and otherwise calls the original;
run the named real-worker test. This is a verification defect, not a demonstrated
failure of the supervisor's absolute-deadline implementation. Passing 538 tests
does not supply the missing positive blocking-boundary evidence.

Bounded closure obligation: establish and assert trusted fixture handler entry
before cancellation, retain offline isolation, outer watchdog, OS exit/cleanup
and absence of exact wall-time assertions; demonstrate the no-command mutation
then fails. Obtain required POSIX and Windows lifecycle evidence and fresh
non-author verification, including relevant collateral deadline/protocol/cleanup
regressions. This describes required closure, not an authorized correction or a
new architecture/product decision. P1's approved architectural resolution remains
closed; its implementation verification is incomplete here.

### Parent reconciliation and stop

The parent validated T008-V1 against the plan's explicit blocking-boundary
obligation, inspected fixture/test/worker control flow and independently reproduced
the no-command mutation. It also inspected the transport and worker seams and
passing regression evidence. No additional material implementation defect was
established in inspected surfaces. Missing Windows execution is a separate
verification gap, not a second product finding. Hash-domain fitness and useful
live yield remain unverified non-findings.

**Final partial-phase verdict: REVISE; phase completion INCOMPLETE.**
**T007 complete; T008 not complete; T009 not started; K2 pending/unapproved.**
The approved task graph requires separate bounded correction authorization after
REVISE. No frozen code/test correction occurs in this run. The next meaningful
gate is separately authorized T008 witness correction, required platform evidence
and fresh verification; T009 cannot begin until its mandatory predecessor passes.
No T010/integration, external validation target, Feature 007, producer/package-
manager execution, archive/config/cache/credential access, release/tag or push.

Prior run 006-0009 was appended once in `176c689` from its complete handoff, with
authorized human /status enrichment and account continuity readings 22/23.
Its runtime confounding and original runtime note are preserved; no credit delta
is derived/stored and earlier ledger bytes are unchanged. Git index creation was
sandbox-blocked, requiring escalation/approval waits for authorized local commits;
this is runtime confounding, not product failure. Current run 006-0010 and its
children are not appended. Its complete 44-field handoff is written outside Git
at `/tmp/libyears-observations/006-0010.json` before final reporting.
