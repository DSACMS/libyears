# Technical plan — restricted external management

Prospective correction to Feature007 P3 only at explicit intake; spec.md C1–C6
controls behavior. External models never enter discovery, aggregation, population,
internal-artifact or filesystem-policy graphs.

P1. Add a selected evidence snapshot method using MavenInputReader's descriptor
chain, regular-file/no-follow/identity checks and a separately bounded byte limit. Reject JSON depth/node/string overages, duplicate members and
nonexact types.
Load the envelope once at CLI/API request boundary; strict JSON duplicate rejection,
exact object schemas and list/count limits. Decode/hash/parse embedded POMs and
verify literal GAV. Convert to immutable accepted evidence. No supplied source
string becomes a secondary external path. Invalid envelope raises a fixed
MavenManagementRequestError; CLI renders a sanitized nonzero request error.

P2. New maven_management module owns evidence decoding and per-key proof. Reuse
bounded XML/raw project parsing and scalar expansion. Model a lineage from its
raw consumer, selecting existing local parents only via graph-established edges,
then exact accepted external parent documents by GAV and role. Bind every local
input in that lineage. Reject missing/conflicting identities and cycles/depth.
Build child-first ordered management maps as whole entries. Resolve each key
lazily: own non-import key wins; otherwise recursively query imports in order
in each imported model's own lineage/property environment. Any unknown earlier
import halts; no cached/global same-GA positive can bypass it. No import lookup
occurs when an own key shields the requested key. Parent properties remain raw
until consumer interpolation. Keep proof builds bounded per occurrence/scan.

P3. Apply only to explicitly granted existing eligible scope-missing rows between
declared_sources and source_policy/capability creation. Prove the ordinary field
site is unique, expand its version independently and require equality with the
existing exact version; require absent ordinary scope. Select managed scope or
normalize compile only after a proven winning key/complete negative traversal.
Never repair version, optional, population or Observed. On failure preserve row
with additive fixed refusal status. On success set scope and the existing
TIME_BASIS_UNAVAILABLE pre-comparator reason, plus additive basis/limitations.
Track whether any external consumer-parent document has repository policy; if so
retain the scope fact but veto comparison as policy unknown. Imported BOM repository
policy is not consumer policy. No alternate transport path. Existing policy continues to inspect only authorized
repository files and cannot acquire evidence automatically.

P4. Thread optional evidence through CLI, mixed scan, scan_maven and admit_sources
without changing no-option call signatures used by injected scanners. Add nullable
intake status/basis to the internal occurrence record, serialize only when intake
was requested for that row. Human/verbose output discloses static evidence once
when present. Provenance paths/hashes/labels stay out of output. Existing wire
worker messages/capabilities, arithmetic, time basis and Observed are untouched.

P5. Validate with deterministic injected snapshots and strict envelope/real-reader
tests, CLI/integration and independent policy-refusal controls. Reproduce retained
proof first, then create a private envelope from verified retained documents and
consumer snapshots. Exercise actual admit_sources/scan_maven and CLI on a private
snapshot directory; replay retained worker metadata only where exact responses
exist. Capture a separate before/after live run on the recorded public checkout
only if exact approved trust recovery validates. Run full suite, capability-disabled
suite, real Maven and NuGet worker tests, whitespace and current/history security
checks. Freeze code/results for fresh non-author admission/security and usefulness
reviews. Document all pending hosted/live evidence honestly.

## Managed version implementation extension — 007-0043

The approved spec C7–C10/A7–A9 prospectively supersedes P3's prohibition on version
repair only for genuinely absent ordinary versions. Existing P1/P2/P4/P5 machinery
and historical scope-only results remain. No new acquisition/transport/reader route.

P6. Keep per-occurrence engine eligibility inside the proof API. Add a distinct
version proof on granted base_model rows with unsupported-version reason, absent
established version, supported artifact and optional. Resolve/bind the full raw
consumer lineage, require one ordinary site and test RawDependency.field('version')
is None; never treat empty, failed expansion or suppressed serialized request as
absence. Extend the existing lazy winner traversal to select a requested field
from the same whole winning entry, carrying its original request and winning
source. Reuse existing scalar expansion and parse_version/is_snapshot, including
existing singleton-bracket normalization. Missing/invalid winning versions return
refusal, never parent/import/cache fallback. No generic evaluator/cache is added.
Keep scope traversal behavior stable. Record visited local sources and accepted
external GAVs per version proof; no supplied path/hash escapes. Existing depth,
per-proof and scan budgets cover all traversals including collateral scope checks.

P7. Represent successful evidence as a small immutable MavenManagedVersion record
attached to the Declared fact, with raw managed request, winning local source or
external GAV, verified local lineage source IDs and visited external GAVs. Fixed
basis/applicability/limitations are serialized additively as managed_version.
Validate shape/Declared association in the model. Preserve ordinary request,
version_basis and origins. A separate occurrence version_management_status reports
attempt success/refusal; management_status remains the existing scope status.
Do not infer scope acceptance from version success. No-option output has no new
fields. Metadata replacement of age/reason naturally retains attached provenance.

P8. In apply_management, attempt version independently only on missing-version rows.
Preserve any established ordinary versions. Verify any supported explicit ordinary
scope agrees with the retained scope; if a retained implicit scope exists, require
it to agree with the bounded winning-management/default result before relying on
that version in its context. Preserve unsupported explicit scopes as unsupported.
After version success choose unsupported-model if scope remains unavailable,
otherwise the existing pre-comparator reason; external-parent policy veto wins
for comparison only. Then the existing absent-scope proof may independently fill
scope. A refused scope proof retains any successful version and its reason.
No changes to source policy, capabilities, worker protocol, arithmetic or population.

P9. Extend _fact only conditionally with safe managed evidence, and occurrence
serialization with version_management_status. Verbose prints the managed evidence;
ordinary retains the aligned measured/unmeasurable tables and adds a concise shared
static-field disclosure. Preserve version/status visibility through catalogue/date/
policy/worker failures. Add deterministic composition/adversarial and actual CLI
integration tests using existing injected-reader/metadata seams; preserve real-reader
and capability-refusal tests. No platform attributes are assumed in new probes.

P10. Before runtime edits, hash and freeze current envelope, every snapshot, replay
procedure, baseline captures and retained worker responses in input-freeze.json;
validate response bytes against the prior0042 input digest. Use D/007-0043 frozen
management.json/snapshot and 007-0028 retained worker
responses for both CLI runs. Baseline is already captured before runtime changes:
127 rows,41 measured,46 version+32 model+8 catalogue refusals,raw9.29860822749512,
unknown N/coverage, unavailable Observed. Exactly seven new source/key grants augment
the previous scope grants in the same envelope used before and after. Reconfirm
raw-site bindings, preserve all previous exact versions/scopes/ages and compare raw
rows/summaries. Retained0038report47/80 stays historical, never the replay baseline.
If required metadata is absent, one separately labeled live batch may measure only
newly admitted exact candidate capabilities. Recover target/trust references privately
from established durable records; verify target/input correspondence and before/after
integrity using the retained bounded procedure. Live metadata uses real existing
supervisor/transport/limits and no additional coordinates. Do not rerun old live ages.
Retain closed metadata responses and raw candidate results separately; any combined
inspection must explicitly identify historical/replayed versus fresh rows.
Freeze runtime/tests and results for fresh semantic/admission/security and usefulness
convergence reviews. Run focused/full/disabled/native-worker/missing-attribute/security/
whitespace gates. Update usage, changelog, validation and roadmap at closure. No push;
hosted matrix remains unobserved. Store every continuation input/procedure durably.
