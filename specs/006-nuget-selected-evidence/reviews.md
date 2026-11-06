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

## T008-V1 correction and focused verification — 006-0011

**Date:** 2026-11-03. **Focused audit: COMPLETE. Bounded correction: APPROVE.**
**New material findings: NONE. T008: INCOMPLETE; Windows evidence pending.**
**T009: NOT STARTED. K2: NOT DEPENDENCY-READY / NOT APPROVED.**
Starting clean HEAD: `e84d3d3951c0ca30e7492f6a916e76e59f0cbe3f`.

### Authority, correction and freeze

The commissioning human authorizes T008-V1 correction, fresh verification and
continuation through all already-authorized internal implementation/review gates,
including bounded correction cycles. New product/scope/trust/target authority,
producer execution, Feature 007 and push remain prohibited. `ac13716` makes the
requested concise workflow clarification: internal quality gates do not themselves
require new human authority. Required evidence and mandatory predecessors remain
binding. This supersedes historical routine correction/phase-message stops only
within the present execution authority; approved spec/plan/tasks stay byte-frozen.

One fresh child author, `/root/t008_correction`, owned only
`tests/test_nuget_worker.py` and the trusted `blocking_worker.py` fixture. The
fixture publishes bounded handler-entry evidence containing its PID, decoded
command authority and actual client deadlines, then waits on a never-set event
without consulting deadlines or naturally completing. A returned-handler marker
would expose unexpected completion. No product worker/supervisor bytes change.

The real-worker witness obtains offline readiness, observes entry explicitly,
then advances an injected metadata clock to the original working cutoff. The
60/300-second deadlines and 0.5-second reserve are unchanged and never reset.
Immediately before real termination it captures a live matching process, consumed
command, entry facts, and absence of result/handler return. It asserts bounded
real waits, cached exit status/reaping, process exit, removed temporary directory
and an unfired outer watchdog. The five-second missing-evidence guard bounds test
failure; elapsed startup time is not evidence of entry. A retained regression
suppresses only parent `command.json` publication and requires the same positive
witness to fail specifically at its missing-handler-entry assertion.

Parent verification before freeze: worker **22 PASS**, full deterministic suite
**539 PASS**, diff check PASS. A separate parent mutation executed the positive
witness with one suppressed command: **one expected failure**, specifically
`blocking handler was not entered`, no error. The former false-positive witness
is now discriminating. These runs used Darwin / Python 3.11.0, offline.

**Frozen correction:** `cb60f792fe1e041cf636926f5017b9ea5509908f`.
**Immediate baseline:** `ac13716`; product baseline remains `ff65b02`.
The correction commit explicitly retains incomplete Windows verification. It is
a reviewable correction candidate, not a completed T008 task. No code/test bytes
change after freeze.

### Independent verification and parent reconciliation

A fresh non-author reviewer, `/root/t008_focused_review`, was commissioned only
after freeze with `fork_turns="none"` and no model/effort overrides. It read the
complete current authority/history and underlying candidate/diff/control flow,
verified approved digests, and independently ran worker **22 PASS**, NuGet
**138 PASS** (including F1/F2/K1-F1 regressions), and full **539 PASS**. Its own
command-suppression mutation failed the same positive witness for missing entry,
with exactly one suppressed command and no deferred worker. Whitespace checks
passed and reviewed bytes remained clean. **Completion: COMPLETE. Bounded
correction verdict: APPROVE; material findings: NONE.** This is focused local
verification, not full platform or feature acceptance.

Parent validation reconciled the report with handler/command control flow, fixed
cutoff arithmetic, live pre-termination observations, bounded waits/exit/cleanup
and its independent mutation reproduction. The evidence supports the local
T008-V1 correction; F1/F2/P1/K1-F1 remain preserved. Full platform closure of
T008-V1 and T008 acceptance remain pending Windows execution. No new product or
architecture decision is required or invented.

### Windows evidence and first external authority gate

A separate fresh read-only child, `/root/windows_gate_review`, independently
completed the task/predecessor and repository CI authority audit. Its conclusion
agrees with parent inspection: tasks.md's mandatory-predecessor rule, T008 done
conditions and T009 dependency require observed Windows lifecycle evidence before
T008 completion/T009, rather than deferring it solely to K2/K4.

`.github/workflows/ci.yml` includes Windows Python 3.11–3.13 and the full offline
suite, triggered by push, pull request or manual dispatch after checkout. It has
no local patch input/transfer mechanism. Other workflows run Ubuntu hygiene and
security checks. Dispatch alone cannot supply unpublished corrected bytes. No
inspected repository mechanism can obtain the required candidate-specific Windows
evidence without publication or a newly authorized execution/transfer target.
No remote dispatch/access, credentials, push or Windows execution was attempted;
**Windows evidence: PENDING EXTERNAL CI, never PASS.**

**Stop: HUMAN/EXTERNAL AUTHORITY REQUIRED for Windows execution of the frozen
candidate.** The needed authority is a concrete authorized Windows environment
and candidate-transfer mechanism, or explicit authorization to publish the
candidate to a named remote/ref and run its Windows CI. Passing evidence must be
attributable to the frozen correction and reconciled before T008 can complete.
This is an execution-evidence boundary, not a reopened product choice or a waiver.
All currently possible correction/review work is complete. T009 and successors
remain blocked; K2–K6 were not reached. No real-root/OASim access, package-manager/
target execution, public activation, Feature 007 or push occurred.

All three children used fresh contexts with no overrides; actual child settings
and resource telemetry are unavailable. Reviewers made no changes or commits.
Prior run 006-0010 was appended once in `ac13716` with authorized human /status
and account continuity readings 23/26; original runtime note/confounding and
earlier ledger bytes remain preserved, with no derived credit delta. Current
run/children are not appended. Git writes required sandbox escalation and approval
waits, retained as runtime confounding. Final authority/ledger integrity and diff
checks pass. The complete 44-field current-run handoff is written outside Git at
`/tmp/libyears-observations/006-0011.json` before final reporting.


## Published Windows verification and bounded portability correction — 006-0012

**Date:** 2026-11-03. Starting clean HEAD:
`fa6a87334b72874cbe5e76266b48b16d866cb635`.
The human confirms that exact published candidate at local main, github/main
and cms/main. This run authorizes all remaining already-defined internal tasks
and checkpoints, bounded correction/fresh review cycles, and follow-up pushes
only to github/main and cms/main when needed for required CI evidence. Each push
requires clean committed bytes, deterministic verification, independent approval
and directly checked nondivergent remote refs; no force/history rewrite. Real-root
access, new credentials/trust, package-manager/target execution and Feature 007
remain outside authority. Approved spec/plan/tasks remain byte-frozen.

### Observed published failure and classification

[Python CI run 41726070279](https://github.com/DSACMS/libyears/actions/runs/41726070279)
identifies the exact published SHA above. Public jobs/check API evidence shows
Windows Python 3.11 (`126231048771`), 3.12 (`126231048816`) and 3.13
(`126231048884`) all FAIL the offline suite after successful checkout/setup.
Ubuntu Python 3.11–3.13 and the separate live PyPI smoke PASS. These results do
not establish Windows lifecycle success. Public 3.12 annotations show ten
`nuget_input.py:123` malformed rejections; the visible annotations are truncated
failure evidence, not a full failure enumeration. Raw logs require authentication
(HTTP 403); anonymous job HTML repeats the annotations and per-step log retrieval
returns 404. No credentials or trust changes are used to recover them.

A fresh read-only child `/root/windows_diagnosis`, fork_turns=none, independently
reads the complete authority and inspects annotations, HTML and underlying tests.
**Assigned diagnosis COMPLETE; original Windows lifecycle evidence INCOMPLETE.**
Parent validation confirms the approved reader intentionally rejects unavailable
O_DIRECTORY/O_NOFOLLOW/O_NONBLOCK and descriptor-relative safety primitives.
New input tests nevertheless assume those primitives, including mkfifo, and new
source semantic tests require actual successful reads on every host. The bounded
classification is **Feature 006 test portability defect**, not demonstrated
product/lifecycle defect, unrelated historical regression or infrastructure
failure. Annotation limits mean no claim that these were the only failures.
The child independently runs the three real-worker tests locally: 3 PASS on
Darwin, supplying no Windows PASS. Historical F1/F2/P1/K1-F1/T008-V1 evidence
and limitations remain retained.

### Bounded correction candidate

The correction preserves production bytes and fail-closed safety. Real descriptor
reader witnesses require the exact safety capabilities. Separate unskipped tests
prove absent-capability rejection without opening/reading content; portable source
semantics consume only bounded exact synthetic bytes through the test seam.
Production source refusal still establishes unknown denominator, unavailable
measurement, safe project error and no rows/authority/read/network/process/write.
F1/F2/K1-F1 semantic regressions remain runnable on unsupported hosts. LF/CRLF
input binding is tested without normalization; the two static byte-bound fixture
inputs receive narrow eol=lf attributes to preserve their committed witness hashes
across checkout. No production normalization is introduced.

The CI matrix now runs the explicit unskipped RealWorkerTests command before the
full suite, making candidate-specific readiness, observed blocking-entry/cancel/
reap/cleanup and discriminating no-command mutation observable as a separate step.
T008 explicitly permits CI changes necessary for platform lifecycle coverage.
The workflow bytes and public exact-SHA step status together can establish that
execution; the current failed full-suite status cannot. Parent local lifecycle
verification: 3 PASS. Candidate freeze, fresh focused verification and final
platform evidence/disposition follow below; T008 remains incomplete until then.

Prior observation 006-0011 is appended once in `006f4df`, retaining earlier ledger
bytes, the 44-field schema, original runtime note and runtime_confounded=yes.
Only authorized human /status fields and account continuity readings 26/27 enrich
the handoff, with provenance identified and no derived credit delta. Current run
006-0012 and children are not appended. Local Git writes require sandbox escalation;
network read also requires escalation, retained as runtime confounding.

Author child `/root/portability_correction` used a fresh context without overrides;
actual child settings/resource telemetry are unavailable. Focused input/source
45 PASS, NuGet 142 PASS. A missing-capability simulation deletes flags before
module import and clears descriptor/follow support: 45 run PASS with exactly
13 genuine filesystem-dependent skips; semantic F1/F2/K1-F1 and refusal tests
execute. A supported-host real reader/source integration witness retains actual
file whitelist, byte invariance and forbidden-access guards. Parent inspects the
complete correction diff and verifies exact static fixture hashes and LF Git
attributes. The corrected code/test/workflow candidate is frozen by its local
commit before non-author commissioning; no candidate edits follow commissioning.

Parent final full deterministic suite: **543 PASS**; diff check PASS.

### Fresh focused verification and publication readiness

**Frozen correction:** `78409d09d73479e54aae99af319318e1f9343913`;
baseline `006f4df`. Fresh non-author `/root/portability_review`, fork_turns=none,
no overrides, directly inspects complete authority/history, frozen bytes and diff.
**Completion COMPLETE / local correction APPROVE; material findings NONE.**
Independent NuGet142, real-worker3 and full543 PASS; missing-capability-before-
import simulation45 PASS with exactly13 real-filesystem skips. Static fixture
hashes, narrow LF attributes, production-unchanged diff and whitespace/tree PASS.
No reviewer writes/network/targets/commits/delegation; actual child settings and
resource telemetry unavailable. Parent independently repeats simulation45/13,
checks whole diff, immutable authority digests, real source composition guards
and explicit CI command. Local approval is supported; it does not claim Windows
execution, T008 completion, K2 or full feature acceptance.

Publication candidate adds only this approval record to the reviewed bytes.
Parent full543 PASS already verifies the exact code/test/workflow candidate;
subsequent changes are review prose only. Before delegated push the parent will
verify clean tree and both live main refs still equal the previously published
candidate, then push only main to github and cms without force, solely to obtain
mandatory Windows lifecycle/regression evidence. Evidence and final task
disposition will follow. The interrupted initial freeze tool did not execute;
subsequent state inspection and successful freeze preserve an explicit boundary.

### Observed follow-up Windows evidence and T008 disposition

Delegated pushes of `221f04819edfc3cc3a1f9de3f09408adee7b4088` succeeded only to
github/main and cms/main, without force. Immediately before each push the tree
was clean, local code/test/workflow verification and independent approval were
complete, and directly inspected remote refs matched the expected prior state.
After both pushes, live refs independently resolve to that exact candidate.

[Python CI run 41727847718](https://github.com/DSACMS/libyears/actions/runs/41727847718)
returns exact head SHA on every job. Fresh read-only observer
`/root/windows_diagnosis` and parent directly inspect public job metadata; the
explicit lifecycle command is unchanged from independently reviewed workflow.

| Windows Python | Job | Lifecycle step | Offline suite | Whitespace / job |
|---|---|---|---|---|
| 3.11 | [126237197713](https://github.com/DSACMS/libyears/actions/runs/41727847718/job/126237197713) | PASS | PASS | PASS |
| 3.12 | [126237197738](https://github.com/DSACMS/libyears/actions/runs/41727847718/job/126237197738) | PASS | PASS | PASS |
| 3.13 | [126237197462](https://github.com/DSACMS/libyears/actions/runs/41727847718/job/126237197462) | PASS | PASS | PASS |

All six Ubuntu/macOS Python3.11–3.13 matrix jobs also PASS lifecycle, full offline
suite and whitespace. The separate live PyPI smoke PASS is unrelated to NuGet
metadata fitness. Job metadata does not supply individual full-suite counts;
543 is the locally observed count. The explicit lifecycle step runs all three
unskipped reviewed witnesses; its success establishes actual Windows execution,
including positive handler-entry cancellation/reaping/cleanup and the retained
command-suppression mutation. This is observed CI evidence, not inference from
local tests, configured CI or an unrelated successful check.

**T008 COMPLETE. T008-V1 platform closure COMPLETE / CLOSED.** Local focused
correction review APPROVE plus required POSIX/Windows lifecycle evidence satisfy
this task gate. Historical F1/F2/P1/K1-F1 remain closed and witnessed. T007 remains
complete; T009 is now dependency-ready and execution continues automatically
under current authority. K2 is still pending until T009 and complete composed
review, not approved by T008 evidence. No new product or trust choice is made.

### T009 implementation and K2 freeze — 006-0012

After T008 completion, fresh child `/root/author_t009` implements only T009:
`nuget_registry.py`, focused registry tests, synthetic public metadata/reason
fixtures and their README. No supervisor/worker, scan/output/CLI or approved
contract bytes change. The parent directly inspects the complete diff and tests.

LocalAuthority-only parent batches sort candidates and invoke the existing
supervisor; the installed worker lazily calls the real metadata handler. Verified
SemVer-2 resource discovery is cached, including failure, at most once per scan.
Registration framing/count/bounds/listing/identity and complete inline/external
pages precede selection. Inline fragment page IDs are validated non-request
identifiers; all actual requests retain the approved fragment-free allowlist.
Equivalent aliases require material agreement, including duplicate catalog leaves;
missing duplicate evidence cannot silently prove agreement. No prerelease order
framework is introduced. Selected public identity/SHA512 correspondence precedes
created-only aware UTC dates; greatest listed stable is chosen before checking
its date, with no older fallback or published/commit substitute. Safe staged
PackageResult records alone cross the existing bounded protocol.

Pre-freeze parent inspection prompts bounded self-audit corrections for missing
alias evidence, split equal-core prerelease pages and once-only failed discovery.
A test-module import is corrected to work under both focused module invocation
and discovery. These are author preparation, not post-freeze review cycles.
True404 resource absence remains distinct from bounded404 invalid response and
allows other required catalog leaves to establish availability; timeout/service/
rate/structure failures retain existing fail-closed handling and budgets.

Author focused32, NuGet174 and full575 PASS. Parent independently runs focused32
and final full575 PASS; diff check PASS. Tests include every registry reason,
reordered page/alias/object request invariance, hostile/no-fetch links, secret
canaries, used/latest date/hash/identity matrices, failed-index caching, retained
cooldown/counters, sorted supervision, interruption cleanup, and actual handler/
byte-client/protocol/controller composition with index/page/catalog cutoff
discard/no restart. Existing P1/T008-V1 and foundation witnesses remain intact.
No live NuGet package, real root, producer or package manager is accessed.

The task commit freezes the complete phase candidate before K2 commissioning.
**T009 implementation/required local verification COMPLETE; K2 PENDING.** No
integration begins before independent phase disposition. Existing exact-SHA
Windows evidence above proves T008 lifecycle; K2 must reconcile whether any new
platform evidence is needed for the composed candidate. Actual child settings/
resource telemetry remain unavailable. Approved spec/plan/tasks stay byte-frozen.

### Independent K2 review — initial candidate

**Frozen candidate:** `8377163f6e8396c3f089a5cb54dc476d5bbff7fe`.
Two fresh non-author children, fork_turns=none without overrides, directly read
complete authority/history, verified digests and inspected frozen code/tests.
No sibling conclusions are shared until both reports complete. Neither edits,
commits, delegates, uses live network/targets or executes producers. Actual child
settings/resource telemetry are unavailable.

| Reviewer | Assigned completed coverage | Verdict / execution |
|---|---|---|
| `/root/k2_metadata_review` | H3/H4, complete registration/catalog identity/count/bounds/listing/alias reconciliation, selected content, created dates/latest, reasons/order/privacy | COMPLETE / REVISE, K2-M1; focused85 PASS plus adversarial reproductions |
| `/root/k2_security_review` | Shared transport/default compatibility, all limits/cooldown/scheduling, trusted worker/P1 lifecycle/protocol/deadlines/cleanup and T009 composition | Local audit COMPLETE / APPROVE, no implementation finding; focused151/full575 PASS; current-platform evidence pending |

#### K2-M1 — Unavailable alias material is mistaken for agreement

**VALIDATED MATERIAL IMPLEMENTATION FINDING / OPEN.** Owner T009; S5, plan
registration reconciliation, AC-22 and relevant AC-31. In `_reconcile_material`,
both absent/invalid hashes or creation dates reduce to identical None values.
Two equivalent middle aliases can therefore collapse despite missing evidence.
Using existing synthetic fixture versions 1.0.0, 2.0.0, 02.0+build and 3.0.0,
remove created from BOTH middle catalog documents: actual success/latest3.0.0;
expected invalid_registry_response. Removing both hashes, algorithms or all
material fields, and different invalid date strings, produces the same false
agreement. Reversed leaf order retains the false result and request schedule.
The parent independently reproduces missing-date, missing-hash and combined
cases against the exact frozen candidate without edits. The existing negative
witness covers only one unavailable side against a usable side.

Bounded closure is determined by approved authority: unavailable material cannot
prove duplicate-alias agreement. Preserve singleton missing-hash/date reasons;
add both-missing/both-invalid hash/algorithm/date cases across used/latest/middle
aliases, order invariance, no measurement claim, valid-equal/conflict and staged
absence/hash/date regressions. Freeze correction and commission fresh focused
non-author verification. No product or architecture choice is reopened.

**Initial K2 completion:** assigned local audits COMPLETE; phase verdict REVISE,
K2-M1 OPEN; unqualified platform verification INCOMPLETE. T010 not started.
Positive security review does not overrule the validated metadata defect.
Current authority permits the bounded correction cycle automatically.

The security reviewer separately notes that unchanged worker/supervisor/lifecycle
bytes retain their legitimate T008 closure at221f048, while worker bootstrap now
imports changed registry code. Parent agrees refreshed exact-candidate Windows
lifecycle/full-suite evidence is required before unqualified K2 approval. This is
outstanding verification, not a second defect or reopened T008-V1/P1. Delegated
push authority is available only after corrected candidate local review and
regressions pass. Full feature acceptance and live yield/hash-domain fitness
remain unclaimed.

### K2-M1 bounded correction and freeze

Fresh author `/root/k2_alias_correction`, fork_turns=none without overrides,
changes only registry reconciliation and focused registry tests. Duplicate groups
now require each catalog document to yield a usable SHA512 hash and created date
before equality can establish agreement. Singletons retain later hash/date-specific
failures; selected absence still precedes reconciliation. No public contract,
transport/supervisor policy or authority decision changes.

The new role × material matrix covers used/middle/latest alias pairs with both
missing or invalid hash/algorithm/created, differing invalid values, short hashes,
naive and sentinel dates. All39 subcases fail against pre-correction bytes, then
pass with correction; reversed leaf/object order retains exact failure and request
schedule. Additional witnesses preserve valid equal UTC spellings, all-position
conflicts, shared catalog links, singleton selected/latest semantics, selected
absence and safe staged evidence. Parent inspects the full two-file diff and
independently runs focused37 PASS. Author NuGet179/full580 PASS, whitespace PASS.

Correction code SHA-256:
`58f13fd5aaf967b5cb652af6bf828fa05084cd2f4359904e33828460d7c9dea0`;
registry test SHA-256:
`8ed0c7be874d11432a05a46e4b1c6cf4d2acf0368bcd8c30d18096283bd821c9`.
The local correction commit freezes these bytes before fresh focused review;
**K2-M1 remains OPEN pending independent closure. K2 not approved; T010 not begun.**
No live network, external root, package-manager/target execution or push occurs
in this correction. Earlier failed candidate and finding evidence remain intact.

### Fresh focused K2-M1 verification and parent reconciliation

Frozen correction `1ffa0f9bd40f5a9a151acfc9f1be7c799a09cfa9`, baseline
`c88d25933154b034eb8003204dd432d4bba0da0e`. Fresh non-author
`/root/k2_alias_verification`, fork_turns=none without overrides, reads complete
current authority and directly validates frozen bytes/diff. **Assigned focused
audit COMPLETE / APPROVE; no material findings.** Historical middle-alias missing
created/hash/algorithm/all-material cases now return exactly invalid response
without publications or verified-state claims. In-memory substitution of the
rejected Git function makes all39 matrix subcases fail with zero errors; no
repository bytes change. An additional135 independent cases pass across alias
roles, either/both sides, null/nonstring/invalid evidence, reordered inputs and
identical schedules. Valid equal/conflicting/shared-link aliases, singleton
reasons, latest with no local hash binding, absence precedence and safe stages
remain covered. Registry37/NuGet179/full580 PASS on Darwin/Python3.11.0; frozen
hashes, approved authority digests, clean tree and whitespace PASS.

Parent validates the exact eight-line guard against S5 and plan alias agreement,
checks full correction/tests and its own focused37 PASS plus historical defect
reproductions. **K2-M1 CLOSED.** Existing K2 slice coverage is complete and the
focused review closes its only material finding; this is not a second full audit
or full feature acceptance. Historical F1/F2/P1/K1-F1/T008-V1 remain closed.
Only refreshed exact-candidate platform evidence remains before K2 approval.

The next delegated push includes only Feature006 task/correction/review records
and reviewed implementation/tests. Local verification and independent reviews
are complete; candidate code/test bytes are unchanged after focused commissioning.
Before each push, clean tree and live remote main refs will be checked; both must
still match expected221f048, then each destination will be verified against the
intended candidate. No force, other refs/remotes, new credentials or trust changes.

### Refreshed K2 platform evidence and final disposition

Delegated push candidate `77d66b9a9a31be6b5cac0bf99c4ff8906a3da9a4` contains
only reviewed Feature006 task/correction/review work since221f048. Before each
push the tree is clean and live remote refs follow the expected transition:
both221f048 before github push, then github77d66b9/cms221f048 before cms push.
No unexpected divergence, force, other ref/remote or history rewrite occurs.
After both pushes each live main ref resolves exactly77d66b9.

[Python CI run41731562096](https://github.com/DSACMS/libyears/actions/runs/41731562096)
returns this exact SHA on all ten jobs. Read-only observer and parent inspect
actual public job metadata, including separately named lifecycle command.

| Windows Python | Job | Lifecycle / offline suite / whitespace / job |
|---|---|---|
| 3.11 | [126249961065](https://github.com/DSACMS/libyears/actions/runs/41731562096/job/126249961065) | PASS |
| 3.12 | [126249961144](https://github.com/DSACMS/libyears/actions/runs/41731562096/job/126249961144) | PASS |
| 3.13 | [126249961199](https://github.com/DSACMS/libyears/actions/runs/41731562096/job/126249961199) | PASS |

All six POSIX matrix jobs likewise PASS all three required steps. Live PyPI smoke
PASS separately; no NuGet yield/fitness claim follows. Local full580 and focused
review remain exact-code evidence; no individual hosted test count is inferred.
This closes the current-candidate platform verification gap.

### Separate hosted secret check and read-only triage

[Secret check41731561997](https://github.com/DSACMS/libyears/actions/runs/41731561997)
FAILS with a generic GitLeaks detection annotation, unlike the original published
baseline's passed check. Public logs/details are unavailable, check text empty and
artifacts absent. It is not dismissed as infrastructure or reported as passed.

Existing local Gitleaks8.30.1 with explicit repository configuration and fully
redacted output, scanning exact221f048..77d66b9, reproduces one generic-api-key
finding at published8377163, `tests/test_nuget_registry.py:491`. The entire source
line constructs a synthetic `TransportFailure(404, 'SECRET', bounded_failure='body_limit')`.
Parent directly inspects its provenance. Fresh read-only `/root/secret_canary_audit`
independently reproduces the same single fingerprint, inspects the synthetic
fixture/recording transport and verifies redaction. **Assigned triage COMPLETE:
reproduced finding is a synthetic false positive, no credential disclosure.**
No policy exception, scanner suppression, history rewrite or configuration change
is performed. Hosted resolved version/range/full failure cause remain unverified;
local reproduction does not establish that the hosted scan has only this finding.
This limitation remains explicit rather than manufacturing clearance.

The fresh authority audit and parent reconcile tasks: T010 requires K2; K2 requires
security/metadata/P1, regressions, full offline suite and platform evidence. No
current authority makes all unrelated CI checks green or a secret-scanner policy
exception a mandatory predecessor. Internal work can proceed without making any
new security-policy choice. Any later scanner exception needs separate authority;
this run leaves the failed check visible and unchanged.

**Corrected K2 completion COMPLETE / APPROVE. T007–T009 phase APPROVED.**
K2-M1 CLOSED; current POSIX/Windows evidence complete. F1/F2/P1/K1-F1/T008-V1
remain closed with retained witnesses. No new material implementation finding
remains. Full feature/36-AC acceptance is later T014/K4; live yield/hash-domain
fitness remains unverified. T010 is now dependency-ready and continues under
existing execution authority, without an unnecessary human routine gate.

### T010 — Internal scan/metric integration

After approved K2, fresh `/root/integration_author` implements only T010 before
stopping for parent verification/commit. `scan.py` adds typed NuGetRequest,
explicit fourth source/lookup pair, one LocalAuthority batch through the supervised
adapter, safe PackageResult-to-common-result propagation and explicit unavailable
NuGet numeric handling. Existing model records suffice; metric, worker import
graph, serializers and CLI bytes are unchanged. Public activation remains absent.
Normalized selected identity supplies metric equality while original safe selected
spelling remains evidence. Sibling policies and existing defaults are retained.

New NuGet scan and mixed-scan tests reconcile all S6 availability states, including
unknown versus known N, unavailableN0 versus validated empty, all/partial/full
individual failures, all versus some sources unavailable, and exact null/zero/
count summaries. Every local/public NuGet dependency failure and source failure
preserves same-name Python/npm/Ruby rows; Python resolved, Yarn arbitration and
both Ruby modes remain checked. Byte invariance, no-call source/local failures,
actual platform refusal and pre-source direct-file rejection are witnessed.
365.25-day arithmetic, normalized identity zero, negative anomaly flag and
measured-only totals use the unchanged metric. Author and parent independently
run focused/shared scan/snapshot/scoped/Yarn/Ruby/metric regressions: **136 PASS**;
diff check PASS. **T010 COMPLETE**, pending later K3 integration review. No
T011/output or CLI activation is included in this task commit. Full suite remains
required at the coherent phase boundary, avoiding redundant per-task full runs.

### T011 — Additive schema-v3 JSON

After committed T010, the same author context executes only T011 sequentially.
`output.py` serializes the exact NuGet source fields with required nulls and safe
row facts/publications only after their evidence stage. Existing schema3 fields,
sibling records and ordinary reports retain their shape; raw authority hashes,
origins/baseline and diagnostics never enter JSON. No human formatter or CLI
activation changes occur. New snapshots cover full/partial/rejected source N0/N1/
unknown, missing witness null, association mismatch with no selected provenance,
unsafe text omission, unsupported selection, origin/hash/publication stages,
normalized/original spelling, UTC/listed dates and empty/zero/full summaries.
Verbose-equivalent diagnostic enrichment cannot alter JSON. Author and parent
focused JSON/output/model/mixed/scoped regressions **84 PASS**; diff check PASS.
Parent directly inspects complete serializer/test diff. **T011 COMPLETE**, pending
K3 whole integration review. Approved contracts and worker import graph unchanged.

### T012 — Human evidence, correspondence and safe failures

The same author context executes T012 only after committed T011. Human output
uses the same typed source/row facts as JSON, showing context and safe input
names, all-direct test/tool/analyzer/PrivateAssets scope, accepted supplier trust
meaning and snapshot limits, first-receipt created dates and greatest listed
stable comparator. Established requests/original selections/normalized identities,
origin/hash states, UTC dates/listing, stable reasons, summaries and anomaly flags
are rendered without inventing omitted evidence. Unavailable measurement, zero
coverage and validated empty populations are explicitly distinguished.

Under S7/AC-35, NuGet-active reports abstract the passed root heading and omit
raw verbose diagnostics/TLS paths; ordinary sibling reports retain established
paths and verbose behavior. Parent pre-freeze inspection catches one composed
Yarn-source-error branch that could reinsert a diagnostics entry despite this
policy. The author limits the correction to fixed safe Yarn explanation in
NuGet-active mode and adds a mixed invalid-Yarn/successful-NuGet canary witness;
ordinary Yarn context is retained. This is author preparation before K3 freeze,
not a repair to an independently frozen review candidate.

Only `output.py` and NuGet output tests change. JSON snapshots remain unchanged;
human/JSON comparisons cover every source/dependency reason, partial safe states,
identity/context/request/date/numeric agreement, source availability and anomaly
flags. Success/failure and ordinary/verbose canaries cover private root/diagnostic/
origin/hash/producer values; ordinary output compatibility remains witnessed.
Author and parent output/model/mixed/scoped/CLI regressions **120 PASS**, whitespace
PASS. Parent directly inspects complete formatter changes and new correspondence
witnesses. **T012 COMPLETE**, pending K3. No CLI activation, table-alignment
cleanup, approved-contract change or external access occurs in this task.

### T013 — Coherent CLI activation and documentation checkpoint

Only after committed T010/T011/T012, the same author context activates exact
`--nuget-project NAME.csproj` and optional `--nuget-provenance NAME.json` through
typed request wiring. Occurrence tracking, exact spelling and directory/immediate
filename validation precede snapshot/CA/source content reads. Ordinary scans omit
NuGet despite co-located artifacts; Python resolved and Ruby group options retain
isolation. Usage/path failures exit1; completed missing-project/source/empty/partial
reports exit0; worker/systemic/render failures exit2 with fixed safe messages.
NuGet-specific argparse/input/exception/rendering privacy does not change ordinary
error/abbreviation behavior.

Parent pre-freeze inspection reproduces raw error risks for root-stat exceptions
and malformed single/triple-hyphen NuGet-looking options. Bounded preparation fixes
and retained regressions produce safe usage1 without content reads or raw tokens.
Rendering exceptions are also covered. Final prose explicitly limits packages_lock
version_source to measured rows, keeping standard failed-row fields plus evidence.
These are pre-freeze author corrections, not post-freeze checkpoint repairs.

README, public SPEC, AGENTS ecosystem scope and CHANGELOG Unreleased Added describe
actual supported inputs/scope/request normalization, strict version1 witness schema
and accepted assertions, identity/origin/local/public hash gates, created-only
first receipt and greatest listed stable, staged schema3 evidence, source/count/
coverage/metric semantics, all numeric limits, process/deadline qualifications,
privacy and exclusions. Reader safety refusal is distinguished from Windows worker
lifecycle support; worker default verified trust does not claim explicit CA override
forwarding. Live yield/hash-domain fitness and real-root evidence remain unverified.
No release/tag or policy exception is added.

Author focused/shared136 PASS, finalCLI38 PASS; author and parent full deterministic
suite **620 PASS** at coherent phase boundary. Parent inspects complete CLI/test/
documentation diff, recovers truncated reads and checks limits against current
source/approved plan; final doc-only clarification follows passing code tests.
Whitespace PASS. **T013 COMPLETE; K3 PENDING.** The task commit freezes the full
integration candidate before fresh non-author K3 commissioning. T014 not begun.
Approved spec/plan/tasks and trusted worker/registry import graph remain unchanged;
existing exact77d66b9 platform evidence retains its defined scope, without claiming
Windows execution of later CLI/output tests. Secret-check limitation stays separate
and unchanged; no targets, live NuGet, package managers or new trust are accessed.

### Independent K3 review — initial candidate

Frozen integration `aeb8964493cc442d3b0eaff7cf6430d9aeb00e81`, K2 baseline
`943d5de`. Two fresh non-author contexts, fork_turns=none without overrides,
read complete current authority, recover truncated reads and inspect frozen
implementation/tests/docs directly. Both complete before parent synthesis;
current sibling conclusions are not shared beforehand. No reviewer writes,
commits, delegates, uses external targets/live network or executes producers.
Actual child settings/resource telemetry are unavailable.

| Reviewer | Completed assigned coverage | Verdict / evidence |
|---|---|---|
| `/root/k3_output_review` | S6 scan/source/repository matrices; normalized metric and staged evidence; exact S7 JSON/human correspondence, privacy and ordinary/sibling compatibility | COMPLETE / APPROVE, no material finding; focused129/full620 PASS, 2401 composed availability cases and17 exact baseline comparisons PASS |
| `/root/k3_cli_docs_review` | Exact CLI activation/usage/read ordering/exits, argument/root/exception/render privacy; documentation contract/caps/platform qualification and option isolation | COMPLETE / REVISE, K3-C1; focused84/full620 PASS and77 additional invalid-argument cases PASS; two capitalized leaks reproduced |

The output matrix crosses seven NuGet states with seven states for each sibling,
using an independent summary oracle, serialized/human evidence and guarded
network/process boundaries. Its injected SourceResults exhaust aggregation;
concrete sibling parsing and ordinary byte-equivalence have separate inspected
tests and baseline comparisons. Reviewed worker/registry/transport/protocol and
workflow bytes retain exact77d66b9 platform scope; no new CLI Windows execution
is claimed or invented as a mandatory predecessor. Secret-check limitation stays
visible and unchanged, without policy exception. No material docs/scope divergence
or source/output finding is established in either assigned review.

#### K3-C1 — Capitalized malformed options bypass safe errors

**VALIDATED MATERIAL PRIVACY FINDING / OPEN.** Owner T013; plan safe NuGet argparse
rendering and AC-35. `_nuget_arguments_present` detects strings case-sensitively.
`main(['.', '--NuGet-project=SECRET-canary'])` and uppercase provenance equivalent
return1 while stderr echoes the entire raw token. Lowercase counterparts produce
fixed safe text. Source/snapshot/CA guards prove no content read occurs; the
privacy defect is error rendering. Parent independently reproduces both exact
frozen cases, including leaked canary. Positive output/compatibility review and
620 passing tests do not override it.

The existing authority determines bounded closure: recognize malformed NuGet-looking
case variants for sanitization while keeping actual option parsing exact and
case-sensitive. Add mixed/upper case canary regressions, preserve ordinary unrelated
argparse behavior, exact lowercase activation and pre-read exits. Freeze correction
and obtain fresh focused non-author verification plus relevant regressions.
**Initial K3 completion COMPLETE / REVISE, K3-C1 OPEN.** T014 not started; current
execution authority permits this correction cycle without a new human decision.

### K3-C1 bounded correction and freeze

The continued T013 author context changes only CLI privacy detection and its
focused tests. Case folding selects fixed error rendering; argparse registration
and accepted option spellings remain exact lowercase. The historical two
capitalized canary witnesses fail before correction and pass afterward. Sixty
mixed/upper case, abbreviation, single/double/triple-hyphen and equals/separate
variants now reject safely before snapshot/CA/scan reads, with no raw values or
traceback. A separate witness retains unrelated ordinary argparse context.

Author focused/shared139 and full623 PASS; parent inspects the complete minimal
code/test diff and independently runs CLI41 PASS. Whitespace PASS. No docs,
approved contract, source/metric/output, worker or registry bytes change. The
correction commit freezes these bytes before fresh focused non-author review;
**K3-C1 remains OPEN and K3 unapproved pending that closure. T014 not begun.**
This bounded cycle uses existing safe-error authority, with no new accepted flag,
product scope, trust policy or public schema decision. No external access/push.

### Fresh focused K3-C1 verification and final K3 disposition

Frozen correction `fb6daf70b5836a05f534c571351d88de86a109ef`, baseline
`212daa24254da5e888d362bca0c35c6e63552d82`. Fresh non-author
`/root/k3_case_verification`, fork_turns=none without overrides, directly reads
complete authority/history, verifies digests and inspects frozen bytes. **Focused
audit COMPLETE / APPROVE; no material findings.** Production change is solely
privacy-detector case folding/comment; registration, exact accepted options and
activation remain unchanged. Historical leaks close. Independent480 guarded
case/abbreviation/hyphen/equality/output-mode cases PASS; in-memory historical
detector substitution causes62 expected subtest failures with zero errors. Nineteen
ordinary/exact-lowercase parser comparisons remain identical. Focused131/full623
PASS on Darwin/Python3.11.0; clean/frozen bytes and whitespace PASS. No edits,
commits, network/target access or delegation; actual child settings/telemetry
remain unavailable.

Parent reconciles the minimal detector change, exact reproduced original leaks,
its independent CLI41 PASS and retained pre-read/error/activation witnesses with
both completed original K3 slices and focused closure. **K3-C1 CLOSED. Corrected
K3 COMPLETE / APPROVE. T010–T013 coherent integration checkpoint APPROVED.**
This is not full 36-AC K4 acceptance. All prior named closures remain preserved.
Worker/registry/transport/protocol/workflow bytes remain those reviewed with
exact77d66b9 platform evidence; no later CLI Windows execution is claimed and no
new mandatory platform gate is invented. Separate hosted secret-check failure,
synthetic local reproduction and hosted-evidence limitation remain unchanged;
no suppression/exception is authorized or applied.

T014 is dependency-ready and continues automatically under existing authority.
No target/network/producer/next-feature authority is conferred by this approval.

### T014 — Final offline acceptance consolidation and freeze

After approved K3, fresh `/root/acceptance_author` reads complete current authority
and adds eight composed acceptance/security tests, the fixture README explanation
and [acceptance.md](acceptance.md). No production or approved-contract bytes change.
The evidence reconciles 36 unique ACs to actual methods/results, all finite limits,
23 exact S6 level/reason pairs, P1 controller/mutation/real-worker evidence and
F1/F2/K1-F1/T008-V1/K2-M1/K3-C1 regression witnesses. It does not mark real-root,
convergence or frozen specification checkboxes complete.

Public CLI composition runs complete local parsers, authority, actual offline
metadata client/handler, typed result codec, unchanged metric and both renderers.
The injected batch lookup deliberately bypasses parent adapter/supervisor;
separate retained T009 controller/protocol composition and T008 real-process tests
supply that evidence. Portable synthetic-byte semantics and actual supported-host
descriptor reading remain distinct. Permutations preserve request schedule,
evidence and summaries; combined failures assert earliest stage, attempted input
names and no invented later errors. Private origins/metadata/exceptions/XML/
witnesses/root paths and excluded artifacts cannot leak or repair authority.
Synthetic target file bytes are unchanged during every scan.

Parent pre-freeze harness review requires post-main forbidden-call assertions,
since product exception handling could otherwise swallow a guard AssertionError
on an expected registry_error path. Retained socket/read mutation attempts are
caught even when swallowed inside the injected transport path. Descriptor calls
are also checked afterward. Setup materializes exact managed input presence before
snapshot, preserving excluded files; failed/missing cases cannot accidentally
reuse prior physical inputs. These are test-harness preparation, not product
corrections or post-freeze K4 repairs. No production defect is established.

Author acceptance8/NuGet225/full631 PASS; parent independently acceptance8/full631
PASS. Parent inspects the complete new tests/evidence, mechanically checks36 unique
AC rows and that referenced methods resolve, and checks tracked plus both new-file
whitespace PASS. **T014 author verification COMPLETE; K4 PENDING.** The local task
commit freezes tests/evidence before fresh independent all36 audit. Existing exact
77d66b9 Windows/POSIX worker-graph scope and hosted-secret-check limitations remain
explicit. No live NuGet, external target, producer, credentials/new trust, scanner
exception, Feature007 or push occurs; T015 not begun before K4.

### Independent K4 all36 acceptance audit — final offline disposition

Frozen candidate `f8e0477007c7310c1ccdc68d9fa7b7fcd5836251`, based on approved
K3 atcdfef4c. Three fresh non-author contexts, fork_turns=none without overrides,
directly read complete authority/history/acceptance evidence, recover truncations,
verify approved digests and inspect actual production/tests. Their reports complete
before synthesis without current sibling conclusion sharing. All are read-only;
no edits/commits/network/external targets/producers/delegation. Actual settings
and resource telemetry remain unavailable.

| Reviewer | Accountable complete AC coverage | Verdict / executed evidence |
|---|---|---|
| `/root/k4_local_audit` | AC03–17,24,33,36:18/18; local31/32/35 contributions | COMPLETE / APPROVE, no material finding; focused116 PASS and53 additional composed public cases PASS |
| `/root/k4_registry_audit` | AC18–23,34:7/7; public24/31/32/35 contributions | COMPLETE / APPROVE, no material finding; focused79/full631 PASS and122 adversarial assertions PASS |
| `/root/k4_contract_audit` | AC01/02,25–32,35:11/11;36 contribution | COMPLETE / APPROVE, no material finding; focused80/full631 PASS, reason reconciliation3 PASS and244 additional public cases PASS |

The accountable sets are disjoint and cover exactly36/36. Parent reconciliation
assesses cross-boundaries rather than counting positive votes: complete population
and known/unknown denominator join whole-lock/witness acceptance; F1/F2 association
precedes origin/hash capability; complete metadata identity/listing/alias evidence
precedes public content/date claims; normalized identity feeds unchanged arithmetic;
typed safe facts feed exact JSON and corresponding human output; every source/
repository null/zero/count state preserves sibling identities and aggregates.
All23 retained S6 pairs have reachable executable triggers, deterministic stage
precedence and safe omissions; no NuGet ambiguity or later-source invention.

The public acceptance injection bypasses adapter/supervisor and is explicitly
qualified. Separate inspected real adapter/client/protocol/controller composition
and offline real-worker witnesses supply cancellation/process evidence. Post-call
forbidden-operation histories catch deliberately swallowed socket/read attempts;
contract reviewer additionally discriminates swallowed subprocess.run. Actual
reader whitelist, unavailable-platform refusal, excluded evidence nonrepair and
before/after synthetic target bytes remain separate from portable fixtures.
CLI case-variant privacy, Yarn diagnostic protection, raw source/response/exception/
path canaries and all report modes retain their closed witnesses. Ordinary and
mixed Python/npm/Yarn/Ruby behavior and public documentation remain consistent.

Registry reviewer verifies13 dependency/lifecycle/workflow paths byte-identical
to exact77d66b9, whose nine platform jobs passed explicit lifecycle/full-suite/
whitespace. Other reviewers independently confirm relevant bytes unchanged.
This preserves required worker-graph platform evidence without claiming later
CLI/acceptance Windows execution. Live NuGet yield/hash-domain fitness, real-root
K5 evidence and K6 convergence remain unverified. The hosted secret-check FAIL,
local redacted synthetic reproduction and unavailable hosted full cause remain
separate and unchanged; no policy exception or new predecessor is invented.

**K4 audit completion COMPLETE / APPROVE. Offline accounting36/36 PASS.**
**T014 final offline acceptance checkpoint APPROVED.** No unresolved material
implementation finding remains; F1/F2/P1/K1-F1/T008-V1/K2-M1/K3-C1 stay closed.
Frozen spec/plan/tasks and acceptance candidate bytes remain unchanged after
commissioning, including no approval-only edit. Parent own acceptance8/full631
and traceability/whitespace checks remain valid. This approval is offline
acceptance, not full feature convergence, real-root validation, release or push.
T015 preparation is now dependency-ready and continues automatically. T016 still
requires explicit exact target/access/network authority; no target is selected
or accessed by this disposition and required K5 is not made optional.

### T015 — Validation preparation and first unresolved human authority gate

Following approved K4, parent authors [release-validation.md](release-validation.md)
without selecting, accessing or producing any target. It supplies exact future
parameter/access requirements, scoped before/after byte manifests, at most two
read-only CLI captures with individual exit statuses, human/JSON comparisons for
scope/selection/origin/hash/created dates/arithmetic/availability/privacy, evidence
shape and K5 disposition. Co-located sibling access is explicit, evidence stays
outside target/Git, three-input hashes are not a whole-tree claim, and agent raw
inspection is distinguished from accepted human attestation. Offline results stay
separate from unexecuted live yield/hash-domain and environmental evidence.
No producer, package manager, target code, archive, trust or source/hash-policy
workaround is included.

Frozen procedure SHA256:
`352e1c2daa5d5b5755810c8e4d30237a14f9662de197cd441a3a17409013f2ec`.
Fresh read-only `/root/validation_prep_review`, fork_turns=none without overrides,
completes an optional narrow preparation check against T015/T016/K5, security and
latest acceptance authority. **COMPLETE / APPROVE; no material findings.** All
three shell blocks pass static sh-n syntax checks; embedded Python passes AST
parsing. No procedure block or target/network/producer command executes. Digest
and frozen bytes remain unchanged. This optional review introduces no extra gate
and does not establish T016 evidence or K5 approval. Actual child settings/resource
telemetry are unavailable.

**T015 COMPLETE. Run006-0012 authorized internal continuation COMPLETE through
T015; STOP at separately authorized T016.** Required new authority is an exact
existing root/project/supplied witness, read/byte-comparison and public-network
scope (including any co-located siblings), private evidence location and executing
or accepted-handoff channel. No exact target/access grant currently exists;
discovery's OASim history is not authority. No target, dotnet/NuGet/MSBuild or
application code has been accessed/executed. K5 remains mandatory and pending;
T017/K6 convergence and T018 separately authorized closure remain dependency-blocked.
No Feature007, unrelated CLI table alignment, release/tag or further push occurs.

Latest full deterministic631 and NuGet225 PASS remain exact code/test evidence;
T015 changes documentation only. Approved spec/plan/tasks and frozen acceptance
candidate stay unchanged. The hosted secret-check failure/local synthetic finding
and hosted-cause limit stay visible, without scanner exception or history rewrite.
Only the two reviewed CI candidates221f048 and77d66b9 were pushed to github/main
and cms/main, with required clean/verification/review/ref checks and exact post-push
verification. Later authorized implementation/checkpoint commits remain local.
The current run is not appended; its complete44-field handoff is written outside
Git before final reporting. Final integrity/whitespace/tree checks follow the last
authorized local commit.

## Bounded T016 preflight and independent evidence disposition — 006-0013

**Date:** 2026-11-04. Starting clean HEAD:
`d7b0360a9205dcc4ee77d04ad98a9236397a4622`.
The commissioning human authorizes read-only OASim validation within ten named
candidate project directories, objective witness selection, public NuGet metadata
for a qualifying selection and bounded read-only revision/integrity metadata.
Already-authorized internal gates and bounded correction/review cycles may
continue; no target modification/execution, unrelated content, private feeds,
credentials, witness reconstruction, Feature 006 expansion or Feature 007.
Existing narrow CI push authority is retained but unused.

### Actual preflight, integrity and missing evidence

[Validation record](validation-006-0013.md) retains the complete bounded result.
The agent inspects immediate candidate input filenames and reads only the twenty
authorized project/lock inputs through the production scoped reader. Every lock
passes schema-1 framing; two projects establish supported declarations:
MatchRunProfileUpdater N=1 and MatchRunProfiling N=2, both net10.0. The other eight
are rejected by the approved conservative declaration rules. No denominator is
invented from recognizable fragments, and no parser expansion is proposed.

**No candidate has an immediate supplied provenance witness. Zero qualify.**
The only immediate JSON names are packages.lock.json and application settings;
settings contents are not read. No arbitrary filename, historical producer
observation, lock hash or public namesake is substituted for S4 assertions.
There is consequently no strongest qualifying witness to select and no human
project-selection question to relay. No scanner invocation or public lookup runs.

All twenty inspected project/lock byte counts and SHA-256 fingerprints match
before/after. Target HEAD and Git status restricted to those twenty paths also
match; Git is supplemental, not a replacement for byte comparison. Independent
standard-library XML inventory uses the same bounded bytes without evaluation.
Private evidence stays outside target/Git, including input fingerprints and raw
metadata. This proves only the inspected boundary, not whole-tree invariance.

No independent measurement expectations, paired CLI reports/stderr/exits,
scope/selection/origin/public-hash/created comparisons, arithmetic recomputation
or observed yield are fabricated. The record explicitly marks these required
obligations UNAVAILABLE/NOT EXECUTED. Qualification parser calls preceded the
freeze and are not recast as independently expected-versus-observed scanner
evidence. Previous offline acceptance36/36 and631 tests remain historical offline
results, not a substitute for required real-root evidence or new test execution.

### Freeze, independent review and parent reconciliation

Frozen validation-record SHA-256:
`2f1d242930aaa1595106ba4e7343f0a0fff4439039f1f5a90315a01d7b8edd1f`.
The private frozen manifest binds seven preflight records and this exact candidate.
Fresh non-author `/root/t016_gap_review`, fork_turns=none without overrides,
reads complete current authority and directly inspects all evidence. No current
sibling report or author conversation is inherited. Actual child settings/resource
telemetry are unavailable. Its report is retained privately as
`/tmp/libyears-observations/006-0013/independent-review.md`.

**Bounded evidence-gap audit COMPLETE / APPROVE; material findings NONE.**
The reviewer verifies all eight frozen bindings and four authority/procedure
digests, independently repeats ten-directory bounded filename enumeration,
matches all twenty safely read input fingerprints, reproduces all project/lock
classifications and XML inventories, and verifies retained manifest/metadata
equality. Its own read boundary excludes settings, references, ancestors,
configuration/cache/credentials and unrelated content. No network, CLI/worker,
producer/target execution, target writes or Git mutation occurs. Product tests
are not rerun for documentation-only qualification evidence. Whitespace passes.

Parent reconciliation checks the underlying inventories/manifests, production
qualification boundary and missing-obligation accounting. Independent repeated
qualification supports the absence of a suitable witness; it does not reconstruct
an execution trace or approve missing live evidence. Candidate and frozen
authority/procedure bytes stay unchanged after commissioning. No product defect
or bounded implementation correction is established.

### Current gate and observation baton

**T016 INCOMPLETE. K5 evidence INCOMPLETE / NOT APPROVED.** Approval applies to
the truthful gap record only. Required real-root comparisons remain outstanding;
T017/K6 cannot begin through an unsatisfied predecessor. T018 and Feature 007
are not begun. The next genuine human/evidence gate is an existing correctly
bound nonsecret supplied witness accepted for a supported authorized context,
or separately authorized new evidence/input boundary if none exists. No witness
is created, reconstructed or weakened and no producer/target execution is proposed
under this grant. H3/H4 and live yield/hash-domain limitations remain unchanged.

Prior006-0012 is appended exactly once in `21dd46d` from its existing44-field
handoff. Human-resupplied post-run /status enriches session/model/provider/effort,
agent version, local-background-server execution mode and account credits_after38.
Reported runtime and confirmed before-credit continuity were not supplied and
remain blank; original runtime note/confounding and earlier ledger bytes stay
exact. No credit delta is derived. Current006-0013 and its reviewer are not
appended. Git index writes require sandbox escalation, retained as runtime context.
The complete current-run handoff is written outside Git before final reporting.
No push, release/tag, unrelated CLI table work or synthetic-canary maintenance.

## Native producer experiment and authority correction — 006-0014

**Overall outcome D — EXPERIMENT BLOCKED. T016 INCOMPLETE; K5 NOT APPROVED.**
Starting clean HEAD `0ee799b3377ead78ace3aba07e0671b860f6d1ed`.
The human authorizes a bounded installed-.NET-10 producer experiment for the same
ten OASim candidates, public nuget.org, isolated temporary state and two fresh
non-author reviews. This exception never transfers to the libyears product.
No product/specification/plan/task or release-procedure change is authorized.

[Producer evidence](producer-evidence-006-0014.md) preserves documentation URLs,
frozen static expectations, selected leaf project/framework, exact commands and
environment, native artifact structures, every witness-field mapping, integrity,
limitations and the execution-scope deviation. Select MatchRunProfileUpdater,
supported net10.0/N1 without project references; the supported Profiling candidate
has two references. Other candidates remain as classified in 006-0013.

### Actual execution, evidence and unmet precondition

The source condition required determining source safety from bounded permitted
configuration **before restore**, stopping if public-only constraint could not
preserve target semantics/configuration. The agent instead restored exact-byte
temporary project/lock copies with directory-import discovery disabled and an
experiment-only public configuration. Original evaluated-context equivalence was
unestablished. That substitution is an execution-scope deviation: original-input
byte equality and unchanged target files do not prove original restore semantics.
The agent should have stopped at that mandatory precondition. Useful replay
output does not retroactively supply authority or complete the requested experiment.

SDK10.0.403 / reported NuGet7.9.0-rc.2412 restored the temporary replay. Initial
sandbox attempt failed DNS/NU1301; identical argv with network escalation exited0.
The successful log reports one public GET/OK/installation. Native metadata v2
retains canonical supplying source and a decoded64-byte SHA512 matching the
pre-existing lock for Microsoft.Win32.Registry5.0.0. Assets4/dgspec1/cache2 link
that extraction to the temporary sole-framework context. No complete native
baseline/coherence testimony or original-context equivalence is established.
No witness, product scan, public catalog/date/hash-domain validation or metric
comparison ran. A partial native-evidence result does not supersede overall D.

OASim revision stays `1e937015e1d242fee5597ea0fbdc4cd5c983f101`.
Selected original project/lock exact-byte manifests and selected-directory Git
status, including the pre-existing untracked lock, match before/after. The replay
copies also match. No whole-tree invariance is claimed. No OASim configuration
or source was written, application built/run/tested, private feed contacted or
credential operation invoked. No workload install/update was invoked. SDK/log
evidence is not an OS-wide trace of every side effect.

### Freeze, two independent audits and parent finding validation

Initial candidate SHA256
`3c5b1eb9c6e043e0f709ead95ac18e02991ba873f09b054e07f787b767ea34a6`;
private freeze.json SHA256
`a3b7221a7380a6ba2c8b66ffe4c0b221141e53079fd18efea9171d1c2a81ff13`.
Exact reviewed candidate bytes remain in the private frozen-candidate-1.md.
Evidence root: `/tmp/libyears-observations/006-0014`, outside OASim and Git.

| Fresh non-author reviewer | Independently completed coverage | Final initial-candidate verdict |
|---|---|---|
| /root/producer_semantics_review (A) | Microsoft/NuGet semantics, cache/extraction/hash/source meaning, isolation, commands/logs and witness inference; direct raw evidence and all frozen bindings | COMPLETE / REVISE, A1 authority precondition |
| /root/witness_contract_review (B) | Complete Feature006 authority, every strict witness field, H3/T016 fidelity, raw native/context evidence and consumer schema/placement | COMPLETE / REVISE, B-A1 same authority/outcome finding |

Both used fork_turns=none without model/effort overrides; actual child settings
and resource telemetry are unavailable. They received no current sibling report.
Their first assessments approved truthful partial-native accounting but did not
have the verbatim commissioning source condition. Parent supplied that exact
condition to each after A identified the missing-authority caveat. Both appended
superseding REVISE supplements. The original assessments and supplements remain
in reviewer-a.md/reviewer-b.md; they are not silently replaced with approvals.
No review executed producers/scans/target code or inspected package payloads.

Parent validates the overlapping finding as **one material experiment-authority
finding**, not two product defects. The frozen expectations explicitly excluded
original imported/ancestor defaults; neither that capture nor native output proves
original source/evaluation semantics. The commissioning STOP condition therefore
was unmet before execution. Both positive native-evidence slices remain valid
within replay scope but cannot overrule the authority finding. This is not a
majority-vote disposition or proof of actual private-feed access.

### Bounded documentary correction and second freeze

The corrected artifact identifies D as the overall outcome, records the actual
deviation and should-have-stopped condition, confines B to narrower empirical
yield, and stops all further producer work. No approved authority, raw evidence,
consumer semantics or witness assertions change. The initial frozen version is
preserved before correction; correction does not authorize prior execution.
Corrected candidate SHA256:
`827234703338388105a1559d50d25d1df6d0eea9c176714d05299feb29f2879e`.
Private freeze-2.json SHA256:
`3d4a18cb25cc534f47a2e93c27d88d6979fcf50a9f0b15670bd9ffa422447abc`.
Fresh focused non-author documentary verification is commissioned only after
this second freeze; its disposition follows separately below. No rerun follows.

### Observation and remaining gate

Prior006-0013 is appended exactly once from its44-field handoff, enriched with
human-supplied post-run session/model/provider/effort/version, reported runtime511
and account-level continuity readings38/41. Original runtime note/confounding and
all prior ledger bytes are preserved; no derived credit delta is stored. Current
006-0014 and children are not appended. Current handoff remains outside Git.

T016/K5 remain incomplete/unapproved; T017/K6/T018 cannot follow this record.
Stop at HUMAN PRODUCT/AUTHORITY DECISION for any further source/input/producer
boundary or added supplier testimony. No spec repair, policy weakening, target
modification, Feature007, side-issue maintenance, push, release or tag occurs.
Product tests are not rerun for this evidence/documentation change; previous631
offline tests and36/36 AC evidence remain historical, not live validation.

### Fresh correction verification, cleanup and final disposition

Fresh non-author /root/authority_correction_verification, fork_turns=none without
overrides, receives the exact commissioning source STOP condition and D definition.
It directly reads authority, both complete reports/supplements, original/corrected
candidates and raw evidence; all28 second-freeze bindings match independently.
**Focused documentary audit COMPLETE / APPROVE; no remaining material finding
in this correction scope.** Report: private correction-verification.md. Actual
child settings/resource telemetry are unavailable. No producer/target/product
execution, network or payload inspection occurs during verification.

Parent validates the narrow three-range correction against the verbatim user
condition and frozen command/expectations, plus raw native identity/source/hash
and original scoped integrity comparisons. **A1/B-A1 documentary representation
CLOSED. The historical execution deviation remains; approval cannot undo it.**
The native evidence audits remain complete within their original limited scope;
the focused correction review does not claim a second complete native audit.

After all reviews, the agent removes E/producer, including downloaded/extracted
package payload, caches, obj and temporary SDK state. It preserves exact selected
project/lock and experiment config bytes in E/captured-inputs, plus raw native JSON,
logs, freezes, command/environment records and all reviewer reports. cleanup.json
records removal and retained input hashes. No package payload/cache is retained
or committed; no target cleanup/write occurs. Both frozen candidate versions and
review history remain inspectable. The corrected durable candidate stays unchanged.

**Final D — EXPERIMENT BLOCKED. Required original-context source/semantics
precondition unmet. T016 INCOMPLETE; K5 INCOMPLETE / NOT APPROVED.** No subsequent
Feature006 gate begins. Further execution needs a source/input boundary meeting
the original condition or explicit new authority; the agent does not choose one.
Final checks cover unchanged frozen authority/evidence, prior ledger prefix and
44-field/unique-ID invariants, Markdown whitespace and git diff --check. No product
test result is invented. Documentation/ledger edits remain uncommitted; no local
commit or push is made under this experiment prompt.

## H3 authority refinement and specification review — 006-0015

**Date: 2026-11-04. Specification review COMPLETE / APPROVE.**
Starting clean HEAD: `052f8b501da9d6b81efc02c047225aea2af47a9c`.
The human expressly approves the two-class H3 model and replay prohibition,
independent specification review, necessary downstream reconciliation, prospective
procedure preparation and coherent local commits. No producer event, OASim access
or modification, product-code implementation, push or Feature 007 is authorized.
The human also identifies an intervening unnumbered recovery run; no account-credit
continuity is inferred. 006-0014 is already recorded once and is not appended again.
006-0015 itself is not appended.

### Frozen specification and self-audit

Corrected specification SHA256:
`57874690885a894f0ada14a263722e499add92c4cc7771d0862c2260d4d9cbe6`.
Frozen before non-author commissioning, then preserved unchanged in `2deb864`.
Only AC-13 and AC-16 wording changes among 36 stable identifiers. Mechanical
comparison to starting HEAD confirms S1/S2/S3/S5/S6/S7/S8 byte-identical; S4 and
authority/outcome/self-audit prose express the approved refinement. The author
re-audits all 36 obligations with coverage recorded in spec.md. This is not
self-approval or a new executed acceptance claim.

H3 now requires native evidence from the producing NuGet operation/context for
package identity, selected version, actual origin and content hash PLUS a
producer-side attestation created contemporaneously with that event, binding
native package evidence to exact project/lock bytes, framework and required
baseline/influence assertions. Native evidence and event testimony are distinct;
their linkage must be independently auditable. Retrospective replay alone cannot
supply original-event/context/absence-of-influence authority. The version-1
accepted-testimony envelope remains, without chronology authentication, new raw
native product input, signatures or new schema fields.

### Fresh independent specification review and parent validation

One fresh non-author `/root/h3_spec_review`, `fork_turns=none`, no model/effort
overrides, reconstructs authority/evidence directly and recovers truncated reads.
It verifies the frozen candidate and reads the relevant implementation for impact.
No author conversation is inherited. No file mutation, test/producer execution,
network, external target access or further delegation occurs. Actual child
model/effort/resource telemetry is unavailable; no child observation row is made.

**Review completion COMPLETE. Verdict APPROVE. Blocking specification findings: 0.**
The reviewer examines all 36 ACs: 01–12 activation/scope/F1/F2/lock unchanged;
13 supplies the two bound classes and retained-event audit; 14/15 source failure
and no namesakes unchanged; 16 adds the replay negative; 17/18 preserve local/
public hashes; 19–24 H4 dates/listing/versions unchanged; 25–28 metric/availability/
siblings unchanged; 29/30 schema/output obligations retained; 31–36 reasons,
no execution, P1/bounds/privacy/exclusions preserved. H1/H2/H4 and closed
F1/F2/P1/K1-F1/T008-V1/K2-M1/K3-C1 remain intact.

Parent validation checks S4's explicit event/package/byte/context linkage,
replay rule and trust limitation against the human decision and the complete
baseline diff. Existing `nuget_provenance.py` validates envelope/types/digests/
context/baseline and constructs LocalAuthority only after exact singleton public
origin and decoded local hash agreement. It does not authenticate chronology;
S4 expressly preserves accepted testimony rather than demanding that mechanism.
Public identity/hash verification still precedes dates. No new consequential
product question or material implementation redesign is established.

**Validated downstream finding:** output.py trust explanation at lines 451–454,
cli.py provenance help at 46–47, README witness guidance, SPEC's NuGet authority
paragraph and fixture guidance omit the newly explicit two classes/contemporaneity/
replay meaning. S4 requires the CLI to explain this trust meaning. This is a
bounded T012/T013 reporting/documentation correction, with corresponding tests
and focused independent verification; it is not a defect in the corrected spec
or authorization to implement product strings now. Parent directly reads those
surfaces and validates the omission. Existing acceptance rows 13/16 prove original
offline checks, not newly explicit real-event chronology; updated mappings must
retain that distinction. Current full implementation conformance is pending,
although existing parsing/local/public gates need no behavior change.

### Downstream reconciliation and prospective candidate freeze

Following specification APPROVE, discovery records the new human H3 decision;
plan/tasks/acceptance/release-validation receive controlling supplements, preserving
all original reviewed prose/digests as historical baselines and all T/AC/K IDs.
Original validation-006-0013.md and producer-evidence-006-0014.md remain byte-unchanged.
The prospective procedure requires event -> native evidence + contemporaneous
attestation -> close/freeze -> later read-only consumer -> independent K5.
It defines the minimum bundle, exact byte/native/event/context/hash linkage,
required influence assertions, source-safety precondition, public hash/date checks,
producer versus consumer authorities and truthful yield/absence accounting.
Prepared only: no operation, capture plan execution or new target is selected.

Historical OASim lacks contemporaneous attestation; 006-0013 correctly found T016
incomplete. 006-0014 retains useful isolated native package source/hash evidence,
not equivalence with historical producer semantics. Overall D/BLOCKED and its
execution deviation remain a negative empirical witness; no retrospective envelope
or attestation may make historical OASim conformant. Prospective OASim would need
new exact event/context/tool/source/input/write/capture and later consumer authority.

Downstream candidates frozen for independent consistency/procedure review:

| Artifact | SHA256 |
|---|---|
| discovery.md | `23b6be427f2ec99e7680ecc6bbc5d1b6cfbd5047d9e0dcbcc33d29497afbabb9` |
| plan.md | `63783bce6f0f661fc3fc73b0cb487a8bc796e070a8800491e62727494a748a30` |
| tasks.md | `06b18582a7aa3cd107b52d9f6ff43bc3246e7dae3ee726c72f3dbde45a784802` |
| acceptance.md | `546d6de4e0877b17a9ae895a2c52fbd49586e4c02ace0b588400db798f8d5f06` |
| release-validation.md | `69aefee27feb9f79bdec5e5d41de8f2fbaf08f60676a80e54f4d4a720145f54c` |

Parent focused regression: `python -m unittest tests.test_nuget_provenance`,
**16 PASS**. This confirms existing mechanisms only; no real event/attestation or
prospective validation is claimed. No product code/tests/public docs change in
this run. Whitespace and AC/unchanged-section checks pass. Full suite is not rerun
for authority/evidence documentation. Fresh downstream review disposition and
final checks follow separately; no implementation/validation approval is inferred
from this author reconciliation.

### Independent downstream review and final gate disposition

Fresh non-author `/root/h3_downstream_review`, `fork_turns=none` without overrides,
independently verifies the frozen spec and five downstream digests, reads authority,
supplements and prospective procedure, and returns **COMPLETE / APPROVE, no material
findings and no new consequential question**. This is consistency/procedure review,
not a second full specification/code audit. It changes no files, runs no tests or
producers, accesses no target/network and does not delegate. Actual child settings
and resource telemetry remain unavailable.

Parent validates that the unchanged historical bodies remain present in all five
supplemented artifacts; original review history remains an exact prefix. The
0013/0014 empirical records and ledger remain byte-identical to starting HEAD.
The prospective bundle links native records, contemporary testimony, exact inputs,
context and content before event closure; later consumer use remains read-only.
New exact production/source/input/write/capture and consumer authority are explicit,
not granted here. The pending reporting correction and required K5 are not waived.
All local Markdown file targets resolve; 36 AC identifiers remain unique, only
13/16 wording changed, and the 44-column ledger has unique IDs with 006-0014 once
and 006-0015 absent. Diff/whitespace checks pass. One initial integrity-check
assertion expected entire files to remain contiguous across inserted supplements;
the corrected check verifies unchanged title/body separately. No historical bytes
were changed to satisfy it.

**Corrected specification: APPROVED. Downstream reconciliation/procedure: APPROVED.**
**Existing implementation: core acceptance/authority mechanisms preserved; full
current conformance PENDING bounded T012/T013 trust-explanation correction and
verification. No implementation redesign or schema change is required.**
**T016/K5: historical and current evidence INCOMPLETE / NOT APPROVED.**
**T017/K6: cannot proceed before required prospective validation/K5 approval.**
No feature convergence, live yield, hash-domain fitness or retrospective OASim
attestation is claimed. Historical F1/F2/P1 and all later closed findings remain.

**Next genuine authority gate:** explicit bounded T012/T013 correction execution
for output/help/docs and corresponding regression assertions, freeze and fresh
focused verification. After that, separately authorize the precise new producer
event/capture plan and later consumer-validation target/read/network/channel;
retain both bound evidence classes contemporaneously, end/freeze the event, then
perform required T016/K5 retained-evidence validation. This run stops here.

The specification correction is committed as `2deb864`; a second coherent local
Conventional Commit records reviewed downstream reconciliation and this disposition.
The final commit is followed by clean-tree/digest/whitespace verification. No product
code/test or unrelated maintenance changes, producer/target execution, OASim write,
Feature 007, release/tag or push. The complete 44-field handoff is written outside
Git to `/tmp/libyears-observations/006-0015.json` before final reporting, with
unavailable run-start/model/credit/child telemetry blank. Git writes required
sandbox escalation; no credits_before continuity or active runtime is inferred.

## H3 reporting correction — 006-0016

Starting clean HEAD `b941c77658d394312aec2984f2dc79fb04d8465c`.
The human authorizes the bounded T012/T013 correction, fresh verification,
prospective producer/capture/consumer validation and continuation through existing
internal gates. No historical OASim provenance, target source/configuration
modification, application build/run/tests, private feed/credential use, scope
expansion or Feature 007 is authorized.

### Frozen correction and focused approval

Local correction `a383440` changes only human disclosure, provenance option help,
README/SPEC, synthetic fixture guidance and corresponding assertions. It explains
native NuGet package provenance PLUS contemporaneous producer attestation, binding
to event/exact project/lock/framework/influence assertions and the replay
prohibition. The version-1 envelope, schema3, CLI activation, parser/LocalAuthority,
public identity/hash/date gates, metric and ordinary/sibling behavior are unchanged.

Seven candidate file digests were frozen in private h3-freeze.json before fresh
non-author `/root/h3_reporting_review`, fork_turns=none without overrides. The
reviewer independently verifies all seven, reads controlling authority and the
complete diff, and runs focused output/CLI/compatibility **88 PASS**, whitespace
PASS. **Focused review COMPLETE / APPROVE; material findings NONE.** Private
report: `/tmp/libyears-observations/006-0016/h3-review.md`. Actual child model,
effort and resource telemetry are unavailable.

Parent validates the changed strings/doc meanings against S4, unchanged schema
and activation branches, fixture limitations and normal/verbose reporting
assertions. Parent focused88 and full deterministic **632 PASS**; whitespace
PASS. The first help test incorrectly expected SystemExit from main; it was
corrected before freeze to assert main's returned status and captured output.
No frozen candidate repair follows review.

**Bounded T012/T013 H3 reporting omission CLOSED / APPROVED.** This supplements
historical K3/K4 evidence, not a new synthetic proof of real-event AC-13/16.
All36 AC identities and H1/H2/H4 remain. Required T016/K5 event evidence remains
pending; no K5/convergence approval follows from reporting closure.

006-0015 is appended exactly once from its handoff with only authorized /status
enrichment and provenance notes. Its original runtime note/confounding remains;
credits_before stays blank because intervening unnumbered work broke continuity.
006-0016 and children are not appended. No unrelated work or push occurs.
