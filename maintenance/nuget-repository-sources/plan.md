# Repository-source technical plan

Governing specification SHA256
54f16902a737016ca51bf797b89c10ff0969567c12e11f8d6096a8cd6bb64189;
independently approved in reviews.md. Candidate plan, disposition in reviews.md.

## Activation and local sources (R1/R2/R6)

CLI ordinary directory calls request `nuget_repository=True` from the mixed scan;
human and JSON follow the same path. Internal scan default remains legacy inactive
unless explicit NuGetRequest or repository mode is requested. This keeps existing
non-NuGet semantic consumers independent of host discovery capability. Direct-file
and explicit modes bypass automatic traversal. Remove CLI's separate post-scan
production recognition; preserve optional formatter recognition for legacy callers.

Validate repeatable exact --nuget-witness PROJECT=NAME.json before snapshot/CA/
source reads. Exactly one equals; safe nonempty relative POSIX project components,
.csproj suffix; immediate .json witness, not packages.lock.json; no controls,
absolute/dot/dotdot/backslash/glob/list syntax or duplicate mappings. Reject mixing
with existing explicit options or direct files. Reuse safe NuGet argparse error
handling and exact-option policy. Internally validate the same mapping pairs and
activation conflicts before any source work. Unmatched valid mappings become
unknown-population sources; discovery failure suppresses unmatched errors.

Reuse discover_nuget_candidates unchanged (approved depth correction included).
Add focused nuget_sources.py: repository orchestration invokes read_nuget_source
for every candidate, or yields a sentinel unavailable SourceResult for discovery
failure. Source identities are sorted root-relative paths; failure sentinel uses
None and source `repository`. Each project retains its own parent lock/witness.
No auto witness reading, source association from graphs, or parser expansion.

Add a RepositoryNuGetReader subclass of ScopedNuGetReader in this focused module.
It opens the caller-selected repository anchor with non-following directory flags,
then each parent component relative to the preceding descriptor, never resolving
an ancestor through Path.resolve. Check reparse/type and inspected/opened identity;
retain at most five parent descriptors and verify parent-relative identity after
source reads. Close all on success/error. Existing required scoped-reader safety
capabilities (including readlink) and discovery primitives must be present.
Reuse bounded permitted-file reads, contained file-link handling and byte checks.
Expose a small `_root_unchanged` method on the original reader for its current
root checks; override it to validate held descriptor chain bindings with no-follow
metadata. No changes to the original selected root/link semantics. The source
reader accepts an optional already constructed reader; ordinary mode injects the
anchored reader, explicit mode constructs its original reader unchanged.

## Identity and one batch (R3/R6)

Append optional `source_id` to NuGetEvidence, SourceResult and SourceError only.
Ordinary mode attaches source_id to every staged row/candidate/error; explicit
mode leaves it absent. Keep NuGetEvidence.project as immediate filename so witness
binding and existing semantics remain unchanged. No package deduplication.

Flatten all authorized occurrences into one adapter.lookup_all call. Construct
adapter only if at least one capability exists. Retain duplicate capabilities in
the batch; associate returned results through per-capability queues in stable
occurrence order, then join separately to each source's own staged evidence.
Do not use a package-name/version dictionary across projects. Existing adapter
sorting is stable and the single supervisor owns deadlines, counters and cooldown.
A failed occurrence never overwrites a successful one even with equal capability.
No worker/protocol/network-policy change is required.

Build NuGet source summaries from each source's rows (filter by source_id), then
fold all NuGet sources into one ecosystem summary. Reuse _available_summary and
metric arithmetic. Null N if any unknown; availability any for M, all for coverage;
NuGet numeric aggregates null only when all relevant NuGet sources unavailable.
Keep repository numeric semantics and all other ecosystem behavior. Add optional
MixedScanReport repository-mode flag and source-summary mapping, with inert defaults.

## Output and documentation (R4/R5)

Serialize SourceError manually so source_id is omitted in existing explicit and
other-ecosystem errors. Ordinary mode always includes it for NuGet, including null
on discovery errors. Ordinary dependency source_id comes from staged evidence.
Factor only the existing source-evidence dictionary assembly into a small helper;
legacy output uses it unchanged. Ordinary version_evidence omits the selected-only
NuGet singleton; append top-level nuget_sources entries with source identity,
existing evidence fields, summary, measurement_available. Ecosystem set derives
from actual sources/errors rather than only singleton keys. Explicit output has
no new collection or source_id keys. Sort sources lexically; null sentinel first.

Human formatter uses the same per-source summaries: one shared existing NuGet
trust/date/scope disclosure plus bounded occurrence explanation and a line per
quoted root-relative identity with known/unknown population/availability and all
summary facts. Stage details add quoted source identity to each row; errors prefix
quoted source identity. All automatic filenames (including immediate project,
snapshot and witness evidence) use JSON string framing. Preserve explicit shape
and existing formatter-only recognition when passed by legacy callers. Suppress
raw root/diagnostics whenever NuGet sources are present, including discovery failure.
CLI unexpected automatic NuGet errors get fixed safe text, including rendering.
Update README/SPEC/AGENTS/CHANGELOG/ROADMAP at documentation checkpoint, preserving
historical Feature006/006-0020 artifacts. No new generic analyzer boundary.

## Verification and release boundary (R1–R6)

Add portable semantic fixtures using existing LocalInput/scoped-reader seams and
injected candidate inventories. Cover equal names and identical/different versions,
equal project basenames, repeated equal capabilities with differing results,
accepted empty/all-failed/partial/full sources, known unavailable versus unknown,
successful sibling sources/ecosystems, mapping validation/acceptance/missing mapping,
no implicit witness read/lookup, explicit baseline JSON equality, discovery failure,
control escaping and safe error text. Use no-network/no-process guards checked
after calls. Existing real discovery tests retain exact bounds/capability refusal.
Add separate capable-host ancestor/link/reparse/race/descriptor-cleanup witnesses
for the new anchored reader plus unskipped primitive-refusal tests. Semantic tests
inject readers and inventories instead of relying on filesystem support.

Run focused tests per task and full suite at integration boundary, plus full suite
with os.supports_dir_fd empty before discovery, real-worker lifecycle tests, diff
checks and python3 tools/check_gitleaks.py on committed candidate. No runtime third-
party dependency or target/package-manager execution. Local Windows simulation is
not actual Windows evidence; hosted CI is a post-publication human gate.

OASim pre-state already captured before target inspection: revision, tracked and
nonignored untracked file bytes/modes/mtime, exact NUL status, ignored inventory
and relevant ignored project/evidence bytes. Run exact ordinary command from the
trusted scanner checkout with stdout/stderr/exit outside target, then recapture
and require exact manifest equality. Do not clean pre-existing state or claim
ignored unrelated byte/atomic OS-wide invariance. No target execution/evidence
production, no particular coverage target. Freeze tests/code/docs/validation for
fresh independent implementation/convergence review; correct bounded findings
and freshly reverify. No push. Next human gate is publication authorization then
actual hosted Windows/other CI observation, unless a new authority gap arises.
