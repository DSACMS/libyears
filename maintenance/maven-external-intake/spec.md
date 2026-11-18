# Restricted Maven external-management intake — 007-0038

## Authority and claim

The human selects explicitly accepted, byte-bound external parent/BOM documents
as conditional static evidence for Declared fields under pinned Maven 3.9.11
composition. This prospective correction supersedes S3's no-external-intake rule
only through the explicit interface below. All ordinary local behavior stays under
existing Feature 007 authority. The reviewed [seven-field proof](../../discovery/maven-composition-semantics.md)
is the first witness; this is not an effective model, successful build, historical
resolution, Observed selection, deployment or complete population claim.

## Contract

C1. `--maven-management FILE` explicitly accepts one bounded JSON envelope, never
an automatically discovered file. Only directory scans support it. The envelope
has exactly `schema_version: 1`, `basis: restricted_static_maven_3_9_11_v1`,
`documents`, and `consumers`. No acquisition or origin assertion grants applicability
or public comparison. Invalid envelope input produces a fixed, sanitized request
error before scanning or network. No raw paths, hashes, XML or supplied labels enter
ordinary diagnostics. FILE nominates one regular file at an explicit relative or
absolute path. Acquire one immutable snapshot using no-follow directory/file opens,
nonblocking regular-file checks, stable identity before/after bounded reads and
overage detection before parsing. Links, special files, replacement, unavailable
safety capabilities and read errors refuse before any scan/network. JSON nesting
is limited to 16, object/list nodes to 20000, strings to 3 MiB and consumers/keys
to 100/10000 total. Reject duplicate JSON members at every depth, nonexact types
(including boolean schema versions), invalid UTF-8, nonfinite numbers and malformed
hash/base64 encodings. No partial envelope acceptance.

C2. Documents have exactly `gav` (three literal strings), `roles` (nonempty unique
subset of parent/bom), `sha256`, and `content_base64`. Decode exact bytes; verify
hash, literal model identity (including literal inherited group/version), supported
POM XML and unique GAV. Maximum 64 documents, 2 MiB decoded aggregate, existing
per-POM XML limits, envelope 4 MiB. Documents are embedded; no file/URL references,
acquisition, host cache/settings/environment or build execution exists.

C3. Each consumer has exactly `source_id`, `context_id: base_model`, `bindings`
(mapping every participating local lineage source ID to its byte SHA256), and
`keys` (nonempty unique exact group_id/artifact_id/type/classifier objects).
Only listed source-qualified keys may receive a field. Duplicate consumers/keys,
unsafe identities and extra keys refuse the envelope. Each granted occurrence
independently verifies current consumer and every local ancestor byte binding,
exact parent GAV and role, before using external facts. Missing/mismatched binding,
document, role or identity refuses that occurrence; a cached same-GA result cannot
bypass verification. Extra documents grant nothing to other occurrences.

C4. Preserve the existing local rows/population/version/optional facts. Initial
intake fills only absent scope on an existing exact-version Declared occurrence
currently refused as unsupported model, with supported artifact and optional.
The ordinary declaration must occur at exactly one site across the selected raw
lineage; same-key ordinary inheritance collisions are outside this intake. Existing
local field-level inheritance remains unchanged. External parent and management
composition uses child-first whole-entry key selection, then ordered independent
BOM imports (first winner), non-dominant field injection and final ordinary compile
default. Never fill an omitted management scope from a losing entry. Exact model
keys include type and classifier without handler aliases. Raw parent properties
interpolate in the consumer context; imported BOMs use their own parent/property
context. Optional is never managed. Preserve exact ordinary versions, including
consumer property origins; refuse any conflict with established local facts.

C5. This finite proof requires complete accepted literal parent lineages for every
model actually visited. Only existing supported scalar substitutions are allowed.
Reject relevant unsupported syntax, ambiguous keys, duplicate/conflicting fields,
profile properties/management/identity writes, or a profile ordinary write of the
requested key. Known unrelated profile ordinary keys and opaque known build/report
containers cannot change this field; no profile activation is evaluated. Unsupported
identities or malformed management prevent negative-key claims. An existing target
management key shields against all imports. Otherwise visit imports in order until
a proven winner; an unknown earlier import blocks, even if a later or cached document
contains the key. Unknown later imports cannot change a winner. No winner across
incomplete imports cannot default scope. Whole-model validity remains unknown.
Parent/import cycles, depth >16, >128 visited model builds per occurrence, or total
>10000 proof builds refuse without erasing safe sibling rows. No general evaluator,
resolver, transitive population or default across relevant uncertainty.

C6. Successful rows add scope basis `accepted_external_management_static_v1` and
fixed limitations disclosing accepted applicability, static incomplete model and
unestablished build/history/Observed. Existing source/view unknown populations,
Observed, metric, comparator/time basis and sibling behavior remain unchanged.
Public lookup still requires existing per-source policy and per-occurrence
admission. External document repositories/origin never grant comparator permission. External
parent repository policy is not reconstructed: if any visited external parent
contains repositories or profile repository declarations, scope proof may survive
but public comparison for that occurrence is refused as policy unknown. Imported
BOM repositories do not govern consumer comparison. External parent launch/settings
context is excluded by the explicitly accepted static basis, not discovered from
ambient files. This conservative parent-policy rule grants no new HTTP authority.
Invalid per-occurrence proof retains original row and adds fixed intake refusal
status; it cannot erase independent safe results. No inherited or same-GA fallback.

## Acceptance

A1. Reproduce retained offline baseline first: 127 rows, 39 exact-version scope
refusals and 42 prior scope-ready facts. Verify corpus, consumer and proof identities.
A2. Actual supported intake admits exactly seven conditional scopes (five Boot,
two AWS); all 39 exact versions, 32 unresolved controls and 42 prior triples survive.
Scope-ready baseline/candidate are 42/49; this is not a complete denominator.
A3. Tests discriminate whole-entry dominance, import order, parent/raw versus BOM
interpolation, exact keys, delayed default, bindings/missing/conflicting/syntax,
cycles/limits, safe siblings, no fallback/cache bypass and no Observed conversion.
Also cover linked/special/replaced envelope files, unavailable read primitives,
duplicate JSON members, deep nesting, wrong types/encoding and parent-policy veto.
A4. Integration exercises CLI option plus real scan/admission/measurement seams;
existing policy can refuse a newly scoped row before HTTP. Required full suite,
capability-disabled suite, real-worker and configured security checks pass.
A5. Independent contract/admission review precedes plan/tasks review and execution;
material corrections receive fresh focused verification. Final independent admission/
security and result-usefulness reviews inspect frozen implementation/results.
A6. Retained response replay and live measurements are separately labeled. Capture
before/after integrity for authorized target reads. Live uses only the exact recovered
approved private trust input and fixed public existing transport. Otherwise report
live blocked. No new POM acquisition. Publish an exact usable invocation, keeping
sensitive local values private. Report remaining blockers by stage and no complete N.
