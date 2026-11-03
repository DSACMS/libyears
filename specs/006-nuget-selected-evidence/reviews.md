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
