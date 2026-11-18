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
