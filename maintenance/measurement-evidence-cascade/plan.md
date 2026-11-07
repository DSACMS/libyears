# Evidence cascade technical plan — 006-0024

Governing approved spec SHA256:
dfce63d13a964c16b0ea72aa1178202a0e86a2dd955ffa9362f202db1445a15f.
Candidate approval disposition lives in reviews.md. No generic cascade framework.

## Local admission and facts (C1–C4)

Extend existing explicit witness parser with exact version dispatch. V1 framing,
required producer/sdk_version fields, native/event meaning, whole-input validation
precedence and no-implicit-acceptance stay intact. V2 omits producer and sdk_version,
requires per-package bounded nonempty namespace string instead of origins/hash,
and shares exact project/lock/framework/SDK/coherence/completeness binding. Reject
unknown fields and wrong types before semantic acceptance. Public namespace is
exact canonical nuget.org string; private/alternate/unknown strings are retained
privately only until safe refusal. No input discovery or generated testimony.
SupplierContext records contract version, privately; package records distinguish
namespace from actual origins. Missing matching package/version and noncanonical
namespace return unsupported_dependency_source before network. All byte/count/
JSON caps remain existing bounds.

Refactor LocalAuthority into the same internal capability with content_hash optional,
namespace_basis (accepted_producer_origin or accepted_snapshot_namespace) and
local_content_state (local_agreement, mismatch, unavailable). Default old constructor
values describe legacy producer/local agreement for existing internal fixtures;
production admission always derives these fields from accepted context. No digest
is carried unless decoded lock/witness agreement holds. V2 carries no content
hash, origin unavailable and local state unavailable. V1 still compares decoded
64-byte values and retains local mismatch/unavailability, but these no longer
reject independently accepted namespace. No parser/project/lock/population changes.

Add inert optional NuGetEvidence fields: measurement_basis, namespace_basis and
local_content_state. Set only after local authority succeeds; producer-event
assertion derives from accepted producer namespace basis. Source trust_basis stays
supplied_producer_assertion for v1/unaccepted legacy request and becomes
supplied_snapshot_assertion after recognized v2 framing. Source fields identify
requested contract, not acceptance. No acquisition claim from v2.

## Worker and metadata (C4–C6)

Extend private capability codec with exact namespace/local-state fields and nullable
content hash. Validate the two namespace values, digest spelling, selected identity,
consistent local-agreement/hash presence, and prohibit v2 hashes/local agreement.
Public capability cannot be manufactured from untrusted witness fields without
successful local admission. Existing worker bootstrap, private files, deadlines,
process cleanup, transport/URL/response/request/rate budgets remain unchanged.

PackageResult adds namespace_basis, default accepted_producer_origin for existing
trusted fixtures. Private result codec accepts unavailable origin only with snapshot
namespace, asserted_public or original fully-verified origin only with producer
namespace. Publication facts require this explicit namespace capability or original
verified chain; success always requires both publications. Preserve existing origin/
hash vocabulary and verified/public_agreement equivalence. Supervisor checks worker
namespace basis matches submitted capability and prevents verified content when
local agreement/hash was absent; failures preserve submitted safe local facts.
Registry worker exceptions/timeouts use an authority-derived failure factory,
so v2 never acquires producer/hash defaults accidentally.

Keep complete registration, identity/listing, catalog validation and date alias
reconciliation. Separate hash material from date/identity agreement: alias hash
absence/conflict alone cannot reject an otherwise unambiguous date/identity. Keep
unusable/conflicting alias dates invalid as before. Compare selected catalog hashes
(and any asserted registration hashes) with locally agreed digest only when that
operand exists. Missing/invalid public hash => unavailable; valid disagreement =>
mismatch; every required comparison agrees => public_agreement and original
public_content_verified. V1 local mismatch persists; no public_content_verified
without original local and public chain. V2 has no content comparison operand.
No public hash gate controls dates; selected/latest absence, bad identities,
incomplete listings, missing/conflicting dates and no stable still fail normally.
No older-latest fallback, no metric change. Retain established assurance on later
metadata failure; preserve local facts across worker-level registry failure.

## Joining and output (C1/C2/C5)

Existing source-qualified FIFO composition and one supervised batch remain.
Join worker facts to each staged row; retain local_content_state independently of
final hash state. Avoid transferring producer facts to namespace-only rows.
Serialize additive measurement_basis and namespace_basis once local authority
exists. Add assurance object with producer_event (asserted/unavailable),
local_content (local_agreement/mismatch/unavailable), public_content
(public_agreement/mismatch/unavailable/not_checked). public_content is derived
from final hash state: original public_agreement means agreement; a final mismatch
with prior local agreement means public mismatch; unavailable with prior local
agreement means public unavailable; otherwise not_checked. Local mismatches stay
separate and do not become public mismatch. Include limitations describing accepted
snapshot scope, unauthenticated acquisition testimony or unavailable acquisition,
content not verified when applicable, reproduction and deployment unestablished.
Never expose raw hashes, origins, baselines, producer identifiers or private paths.
No new values in old public origin/hash fields; v2 unavailable means no acquisition
origin, separate namespace_basis authorizes its dates. Existing row/source shapes
and literals retain meaning; new v2 source string identifies its requested contract.
No sibling fields/labels or schema bump. Verbose JSON remains identical.

Default human output uses concise snapshot/namespace qualification, source identity,
failures/counts and dependency/used/latest/libyears. Move expanded trust/event/hash
policy and per-row evidence details to verbose output, retaining source identity
for ordinary rows even in concise output. Structured output always has details.
Do not expose private root/diagnostics or silently hide source failures. Keep
existing non-NuGet formatter behavior. Update current README/SPEC/AGENTS and
CHANGELOG at documentation checkpoint; historical feature contracts untouched.

## Sequential verification and convergence (C1–C6)

Implement local parser/capability with tests, then worker/metadata/scan/output with
behavioral tests and migrate old hash-blocker assertions to new age-plus-assurance
expectations. Historical prose is evidence, not current runtime test oracle;
update runtime test reason extraction to current correction contract while keeping
historical S6 inventory explicitly historical. Preserve negative scope/context/
namespace tests and no-call/privacy/capability refusal witnesses. Add end-to-end
v2 no-event/no-hash success, v1 missing/local/public hash cases, metadata failure
with assurance, unsafe namespace zero requests, protocol forgery rejection, null/
partial/empty/sibling math, additive output and unchanged sibling fixtures.

Focused tests first; full deterministic and capability-disabled full discovery at
integration boundary, plus real-worker lifecycle. Capability simulation empties
os.supports_dir_fd before importing/discovering tests; do not add skips for semantic
fixtures or disable refusal tests. Simulation is not hosted Windows evidence.
Run diff check and canonical GitLeaks history gate on committed candidate.

Baseline OASim captured before access in private 006-0024/oasim-before.json:
revision, exact full status, tracked/nonignored untracked bytes/modes/mtime and
ignored inventory plus relevant ignored project/lock bytes. Baseline ordinary CLI
exit0/stderr empty: ten attempted sources, eight unsupported populations, two
known populations totaling3 with missing accepted witnesses, null coverage.
Run final exact python3 -m libyears OASIM_ROOT from trusted scanner checkout and
retain stdout/stderr/exit plus structured companion. Recompute manifest with same
method and require equality; no cleaning, target writes/execution or new producer
evidence. Report every source/known occurrence blocker separately from optional
assurance. No new testimony accepted implicitly merely because retained.

Freeze code/tests/docs/validation for fresh independent non-author reviews:
selection/context/population; namespace/claims/protocol/privacy; cross-ecosystem/
output/migration and operational consequences. Parent validates material findings;
determined bounded corrections get fresh re-review. Preserve failed/incomplete
reviews. Stop only for new consequential authority. No push. Hosted Windows/
security/CI remain post-publication, with human publication authorization next.
