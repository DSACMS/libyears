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
