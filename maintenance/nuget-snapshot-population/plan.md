# Snapshot population technical plan — 006-0026

Candidate; governing spec and review digests/dispositions in reviews.md. No runtime
work before specification, plan and graph approval.

## Local snapshot evidence (P1–P3)

Add focused nuget_population.py. Reuse bounded whole XML framing from nuget_project
without changing parse_project acceptance. A safe probe inspects the Project/Sdk
root and collects only unconditional literal framework/package facts for conflict
checks; it never returns a declaration completeness claim. No file traversal,
condition evaluation or expansion. Duplicate known references refuse; known
framework/request/Direct conflicts refuse. Record uninterpreted remainder as
unknown, covered only by explicit accepted snapshot testimony.

Add exact v3 framing/binding in nuget_provenance beside preserved v1/v2 dispatch,
sharing existing strict objects/types/digests/package-record helpers and limits.
Return SupplierContext(contract_version=3) only after full framing and exact
project/lock/framework/coherence/external snapshot assertion checks. Packages
reuse v2 namespace records; authorize_measurement uses v2 namespace capability
for v3, without content/event claims. No worker/protocol/metadata changes.

Build B ProjectContext-like iteration data from whole accepted lock Direct entries,
with validated supported minimum requests and selected identities. This is internal
iteration reuse, not static completeness: retain explicit population_basis. All
Direct entries must pass before any B count or row escapes. Check MAX_DIRECT_REFERENCES.

## Source sequencing and output (P1–P4)

read_nuget_source still reads project first. Catch only A unsupported failures;
retain original refusal unless explicitly supplied v3 successfully establishes B.
Never catch malformed/missing/unsafe/limit/duplicate project failures for fallback.
Read lock/witness within existing reader; no new allowed filenames or CLI option.
Preserve old no-witness/v1/v2 A failures. On supported A, parse_provenance continues to reject v3 as malformed witness;
retain A count and unavailable measurement, with unchanged v1/v2 requirements.
Stage count/basis only after complete B acceptance; a B failure keeps unknown N
and no dependency rows. Reuse existing candidate iteration/namespace gate, one
supervised batch, source occurrence attribution and summary composition.

Add inert population_basis to NuGetEvidence and NuGetSourceEvidence; production
sources start unknown, become declaration_derived after A parse and resolved_snapshot
only after B acceptance. Source population_limitations contains fixed safe strings
only for B. Add source/row JSON keys without changing old fields. Default human
snapshot source qualifier and verbose limitations use existing formatter paths;
no raw XML/request/hash/testimony disclosure. Requests originate in lock for B:
report them as snapshot requests, never current project declarations.

## Verification and operational boundary (P5)

Synthetic fixtures construct explicit v3 assertions solely in offline tests.
Use existing injected reader seam with no socket/process/write guards during
source parsing. Cover A precedence despite v3, ineligible failures, missing
acceptance, old witnesses not reinterpreted, all binding/assertion failures,
malformed whole evidence, duplicate aliases, context/RID, literal contradiction,
unknown syntax accepted under snapshot testimony, Direct-only/empty/selected/
request rejection, namespace unknown/private/conflicting/absent zero capabilities,
positive public capability and metadata-composition, ordinary occurrence/source
identity, source unknown/unavailable and sibling aggregation, JSON/privacy and
human detail. Preserve historical fixture bytes; adjust legacy equality tests
only to remove newly additive population fields. Capability-disabled simulation
empties supports_dir_fd before discovery; semantic tests remain active.

Full deterministic, focused project/lock/source/repository/fixture tests, capability
suite and real-worker tests; git diff --check and history GitLeaks. OASim baseline
captured before target access in private 006-0026/oasim-before.json: revision,
full status/index, tracked/nonignored untracked bytes/modes/mtime, ignored inventory
and relevant ignored inputs. Run ordinary human/JSON commands from trusted checkout,
retain raw stdout/stderr/exits; inventory current exact project/lock pairs without
acceptance generation. No v3 retained evidence => actual B zero, even if potential
8/48. Do not manufacture a v3 document from old narrative. Final identical manifest
required. No target execution/writes/package managers/network namesake probes.

Freeze candidates and independently review population/binding/precedence and
namespace/output/operational cross-artifact obligations. Parent validates findings;
determined corrections get new freeze and fresh focused reviewers. Record no push
and next human publication/actual hosted CI gate; any new trust/schema/security
choice stops instead of being invented.
