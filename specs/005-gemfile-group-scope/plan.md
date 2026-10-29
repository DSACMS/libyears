# Feature 005 Technical Plan: Bounded Static Gemfile Group Scope

## Status and authority

**APPROVED** — focused independent verification completed in run `005-0011`,
2026-10-29. Next gate: TASK DECOMPOSITION. This plan grants no implementation
authority. No tasks or product implementation are created by this document.

The [approved specification](spec.md), including S1–S4 and AC-01–AC-28, governs
all observable behavior. [Review history](reviews.md), especially the final
005-0007 approval, resolves F1/F2; historical REVISE/INCOMPLETE text is not the
current gate. H1–H3 and Q1–Q3 are settled. No product-contract conflict was
identified. This design does not extend the supported Ruby language, evaluate
requirements, change metric policy, or authorize external targets/network work.

## Existing boundaries and component ownership

Repository inspection establishes these concrete extension points:

| Module/component | Planned responsibility |
|---|---|
| New `libyears/gemfile.py` | Pure line-oriented recognition of the closed S1 subset; immutable declaration/group records, complete-file validation and safe parse failures. No filesystem or registry calls. |
| `libyears/rubygems.py` | Preserve `ruby_source_result` all-direct path; add `scoped_ruby_source_result(root, requested_groups)`, safe scoped input reads, group selection, association and local failure precedence. Share existing name/requirement/authority checks and selected-artifact validation through small Ruby-specific helpers. |
| `libyears/gemfile_lock.py` | Reuse `parse_lockfile`, `LockDependency` and `ParsedGemfileLock` unchanged in semantics. Entire lock remains structurally validated before association. No group inference or new Bundler sections. |
| `libyears/model.py` | Add optional typed Gemfile row evidence and requested-group source evidence using trailing defaults; retain existing positional construction compatibility. |
| `libyears/scan.py` | Accept optional group request, choose one Ruby source path, propagate declaration evidence through registry success/failure, retain existing three-source orchestration. Correct scoped unavailable numeric summaries at the aggregation boundary. |
| `libyears/cli.py` | Repeatable validated `--ruby-group GROUP`, directory-only validation, canonical requested tuple, existing exit categories and Python-only `--resolved`. |
| `libyears/output.py` | Explicit additive schema-v3 serialization/omission and scoped human disclosures; existing ordinary output remains unchanged. |
| Existing registry adapters and `metric.py` | Reuse public-source transport, publication selection and arithmetic; no new runtime dependencies or registry semantics. |
| Tests, README.md, SPEC.md, CHANGELOG.md | Focused offline acceptance/regression coverage and later approved documentation checkpoint for activation, subset/rejection boundaries, provenance and limitations. |

Keep this a concrete Ruby evidence pipeline, with no generic parser, resolver,
plugin or source framework. Python 3.11+ standard library remains sufficient.

## Static recognition and declaration records

Use a small cursor over each physical line, with explicit functions for quoted
literal, symbol, comma/list, recognized keyword and end-of-line consumption.
Do not split comments or commas blindly: `#` within a permitted literal is
content; a comment begins only outside strings. Inspect strings before accepting
contents; escapes, interpolation and forbidden delimiter/newline forms reject.
No Ruby evaluator, subprocess, import of target code, or general Ruby AST is used.
LF/CRLF and spaces/tabs outside literals follow S1. Reject other control/framing
errors safely. Parentheses, semicolons, continuations and trailing tokens cannot
be consumed as an approved call. Keep recognizers anchored to complete lines.

Maintain one optional active group block, a seen-declaration-name set and the
established-group set initialized to `default`. The parser accepts only the
exact source/gem/group/end forms in S1. `source` is top-level, exactly once;
a nonpublic literal is recognized as inert evidence. Inside a group only gem,
blank and comment lines are accepted. A second group header while one is active
rejects nesting. Block optionality and `require:` are validated then discarded
because they do not change declared membership. Repeated keys, group/groups
coexistence and unknown options reject the file.

Proposed internal frozen records:

- `GemDeclaration`: exact name, ordered requirement-string tuple, sorted unique
  full declared-group tuple, physical line number. Safe display declaration is
  derived from name and requirements, never copied from an input line.
- `ParsedGemfile`: declarations in file order, sorted established groups, and
  a public-source-authorized boolean. The source literal is compared against
  the existing exact `https://rubygems.org` authority with optional trailing
  slash, then discarded; never use it as a request URL or diagnostic.
- `GemfileParseFailure`: stable reason, optional line number, fixed safe category.
  It contains no raw statement, URL or arbitrary exception text.

Move the small existing Feature 004 name and requirement framing validators
into `gemfile.py`, and import them in `rubygems.py` so both recognition and lock
authorization use identical rules without an import cycle. These checks remain
framing checks, with no semantic requirement parsing. Each requirement literal and its ordered joined
value must have supported framing. Name identities remain exact, case-sensitive
and unnormalized. Unsupported declaration framing rejects scope; isolated lock
requirement failure remains a dependency failure.

Top-level gems without explicit groups get only default. Explicit top-level
groups replace that implicit membership. Inside blocks take block/option union.
Supported empty blocks establish names. Duplicate declarations anywhere reject,
even if identical or unselected. Never emit a partial parse result. Process
physical-line defects in order; classify recognizable but incomplete/malformed
approved forms as `invalid_gemfile`, outside-subset constructs as
`unsupported_gemfile_syntax`, and duplicate gems with their dedicated reason.
Whole-file completion defects (missing source/unclosed block) follow line
defects. Unknown-group selection runs only after successful complete parsing.

## Filesystem safety and bounded work

Scoped reads use a private, Ruby-specific root reader in `rubygems.py`. Resolve
the supplied directory once as the containment boundary. Only exact root names
Gemfile and Gemfile.lock are considered; never enumerate children or inspect
parents, includes, gemspecs, config, credentials or alternate names. Internal
symlinks may resolve to regular files within that root; escaping, dangling and
nonregular targets cannot supply evidence. Inspect link metadata and resolve
containment before opening; never open an outside-root target to test validity.

To resist link replacement during access, open the validated resolved path by
walking its root-relative components with directory file descriptors and
no-follow flags. For BOTH Gemfile and Gemfile.lock, open the final component
with `os.open` using `O_RDONLY | O_NOFOLLOW | O_NONBLOCK`: a replacement FIFO
must not block waiting for a writer before type validation. Immediately use
`os.fstat` and `stat.S_ISREG` on that descriptor; reject any nonregular object
before wrapping the descriptor or consuming content. Read only from that same
validated descriptor. Keep directory-descriptor traversal and containment checks;
nonblocking access does not replace symlink/root protections. Do not fall back
to a blocking or unchecked pathname open. If the platform lacks the required
flags or directory-relative/no-follow operations, fail closed through the existing
safe source-failure mapping, without attempting an unsafe open. This uses only
standard-library capabilities and does not require platform-specific substitutes.
Close descriptors on all paths. This is a local helper for two Ruby files, not
a filesystem framework. Tests must simulate replacement between validation and
open and assert that outside-root content is never consumed.

Use binary bounded reads, strict UTF-8 decoding and explicit CRLF handling.
Planning limits for scoped input are 1 MiB Gemfile, 16 KiB per Gemfile physical
line, and 16 MiB lock; read at most limit+1 bytes. The Gemfile byte/line limits
bound declarations, symbols and literal storage without extra recursive/token
budgets. No recursive parser state exists. Gemfile excess returns
`unsupported_gemfile_syntax`, never partial scope. A scoped lock exceeding its
read bound returns source `invalid_lockfile`, retaining known scope and no rows.
These are scoped resource boundaries only; ordinary Feature 004 reads stay as
released. At-boundary/one-over tests establish deterministic behavior. File
limits also bound lock-parser allocation and repeated exact-name association
work; build direct-name indexing once, without changing artifact validation.

Map missing Gemfile to `gemfile_missing`, outside-root Gemfile to
`unsafe_gemfile`, and unreadable/nonregular/dangling/invalid UTF-8 Gemfile to
`invalid_gemfile`. Lock unsafe/unreadable/nonregular/invalid UTF-8 reads use
`invalid_lockfile`; absent lock has the separate known-scope policy below.
Diagnostics expose fixed categories and optional line numbers only. Do not copy
OS exception messages containing target paths or source values into reports.

## Scoped source flow and authority ordering

`scoped_ruby_source_result` always returns `source_present=True`, including when
both files are absent. Its evidence always names Gemfile/Gemfile.lock,
`selected_declared_groups`, sorted unique requested names and the existing
publication basis. Set include_format true, initially null.

Run this sequence explicitly; later inputs are not inspected after an earlier
terminal failure:

1. Read and completely recognize Gemfile. Failure produces one Gemfile source
   error, unknown denominator and no lock read/lookup.
2. Verify every requested exact group is established. Any unknown name produces
   one `unknown_ruby_group` source error, no partial union and no lock read.
3. Select the unique declaration union; this fixes N independently of the lock.
4. Read and parse the entire lock with existing whole-lock rules. Missing lock
   with N>0 gives one `lockfile_missing` row per selected declaration; pins
   never create candidates. Missing lock with N=0 is available empty. Rejected
   lock gives a source error, known N, unavailable measurement and no rows,
   including when N=0. Accepted lock sets format `gemfile_lock` even for empty
   scope. Excluded rows still participate in structural lock validation.
5. For an accepted lock, check nonpublic Gemfile source first for every selected
   name. Return `unsupported_dependency_source` without lookup or selected
   artifacts even when its direct lock identity is missing: this implements F1.
6. Under public Gemfile authority require an exact direct lock identity.
   Missing identity yields `lock_dependency_missing`, regardless of matching
   transitive specs. Index only DEPENDENCIES for this step.
7. For an existing direct row preserve Feature 004 local ordering: unsupported
   name, unsupported requirement, unsupported lock source. Factor that prefix
   from `authorize_public_selection` so scoped processing can then compare
   requirements before selected-spec/version checks. Ordinary processing calls
   the same prefix and unchanged remaining selection logic. All exact-name
   source occurrences and pins continue to participate in the authority gate.
8. Compare supported requirements exactly as S4: join declaration literals with
   `, ` in supplied order, zero literals as null; compare against the direct
   row's extracted text, without normalization. Different values yield
   `declaration_lock_requirement_mismatch`, no candidate or selected artifacts.
9. Only equal supported requirements and authorized identity proceed to existing
   selected-spec validation (`lock_version_missing`, ambiguity/unsupported
   evidence) and existing scheduled Ruby registry lookup. Retain existing
   artifact rules for these failures and subsequent registry outcomes.

No authority or local failure makes a request. Gemfile source cannot rehabilitate
lock authority and lock source cannot rehabilitate Gemfile authority. Missing or
rejected lock precedence remains ahead of nonpublic Gemfile authority. Reuse
current candidate scheduling and fixed public adapter; no URLs from declarations
or locks become destinations.

## Evidence propagation and safe output

Add `GemfileEvidence` in model.py with declared_groups and
declaration_requirements tuples, `lock_requirement: str | None`, and an explicit
`include_lock_requirement` boolean defaulting false. The boolean distinguishes
omitted unknown/unsafe evidence from present null (known absence). Add optional
`gemfile_evidence=None` trailing fields to DependencyCandidate, Dependency and
UnmeasurableDependency. Add `requested_groups: tuple[str, ...] | None = None`
to SourceEvidence. No registry result type needs declaration evidence: scan.py
copies it from the candidate on both success and RegistryFailure while keeping
current selected/publication artifact merging intact.

Construct safe declaration evidence before lock association. Add lock_requirement
only for matching direct rows in accepted locks whose requirement passes safe
framing, independently of whether measurement succeeds. Missing lock/direct row
omits it; rejected lock emits no rows. In F2, unsupported direct requirement
produces `unsupported_requirement`, omits that field and selected artifacts,
retains safe declaration evidence and N, and never echoes lock text. Replace
any inherited lock-derived `declared` with declaration-derived safe framing on
all scoped failures, including registry failures. Never serialize raw parsed
records with `asdict` as a shortcut.

output.py explicitly serializes the optional evidence object on both measured
and unmeasurable rows. It emits requested_groups only when present and preserves
schema_version=3 and all ordinary keys/values/omissions. Membership arrays are
sorted unique full memberships; requirement array order/content is unchanged.
Mismatch retains both supported values and no exact provenance. Verbose output
must not change JSON. Test each field's presence as well as value, especially
format=null, omitted lock_requirement and present lock_requirement=null.

Human output detects scoped source evidence in both single-ecosystem and mixed
branches. Replace only the scoped Ruby disclosure with selected declared groups,
supplied file labels, recognition availability and the supplied-file limitation:
no installed/deployed/runtime or historical-coherence claim. Keep observable
publication limitations. Add safe group/requirement details for measured and
unmeasurable rows in both branches. Explain mismatch with the approved wording
“textual requirement evidence differs; equivalence not inferred.” Explain
nonpublic Gemfile authority without printing its value. Use the specification's
stable reasons, with contextual Ruby text for new Gemfile, missing-lock,
missing-direct and mismatch failures. Distinguish known empty, wholly
unmeasurable and unavailable evidence explicitly, with JSON-consistent counts.

## CLI, mixed scanning and aggregation

Use argparse append for --ruby-group and a full-match ASCII symbol-name
validator without the colon. Empty strings, commas, whitespace, malformed names
and missing values are usage errors (1). Sort/deduplicate after validation;
absence remains None. Validate an existing directory target before discovery
when scoped; a direct file or invalid path is usage/path error 1. Keep ordinary
path handling unchanged. scan_mixed_repository also validates its optional
`ruby_groups` argument before source reads, with a dedicated scoped-request
ValueError subclass that CLI maps to 1; unrelated exceptions remain systemic 2.
CLI passes the new keyword only when requested, preserving injected scan-call
compatibility. --resolved is still passed exclusively to Python discovery.

Mixed scanning calls exactly one Ruby source function. Existing SourceResult
availability/count fields already express the new states:

| Scoped state | N | measurement_available | Rows | Ruby summary |
|---|---|---|---|---|
| Gemfile failure / unknown group | null | false | none | all null |
| Known scope / rejected lock | selected count | false | none | N retained; measured, coverage and all numeric aggregates null |
| Missing lock / N>0 | N | true | N unmeasurable | M=0, coverage 0%, total 0.0, other aggregates null |
| Empty scope / absent or accepted lock | 0 | true | none | 0/0, null coverage, total 0.0, other aggregates null |
| Accepted lock / local or registry failures | N | true | selected names only | M/N for N>0; measured values alone aggregate |

Inspection found `_available_summary` presently retains calculate_summary's
0.0 total when measurement_available=false and N is known. Adjust the
per-ecosystem aggregation boundary so unavailable scoped Ruby numeric aggregates
are null. Preserve ordinary outputs and repository successful-sibling numerical
aggregates; do not globally discard sibling measurements when one source fails.
Repository coverage is null if any detected source is unavailable, discovered
is null if any denominator is unknown, and measured is null only when every
detected source is unavailable. Test the known-N rejected-lock case with zero
and positive N; it cannot be represented as an ordinary empty result.

## Deterministic verification and acceptance traceability

Use unittest/unittest.mock only. Add tests/test_gemfile.py for pure recognition,
tests/test_ruby_groups.py for scoped source/association and filesystem boundaries;
extend existing test_cli.py, test_output.py and test_mixed_scan.py for composed
behavior. Small synthetic Gemfile/lock pairs live in
`tests/fixtures/ruby_groups/` with a README documenting expected memberships,
selected populations and rejection reasons. Generate boundary-sized inputs in
tests rather than checking in huge files. Fixtures make no real-application or
publication-history claims. Use injected registry results/local existing Ruby
population fixtures; spy on lookup arguments/counts and forbidden reads. No
network, package managers, target code or external checkouts are needed.

For P1, add separate Gemfile and Gemfile.lock replacement-to-FIFO regressions.
Start with valid regular root inputs, then interpose at the final `os.open`
after metadata/containment validation to replace the selected path with a FIFO
before invoking the real open with the production flags. For the lock case,
first allow Gemfile recognition and selected-scope establishment to complete.
Use no FIFO writer; assert the final flags include nonblocking/no-follow,
`fstat` rejects the opened FIFO before any content read, descriptors close,
and the source returns promptly with `invalid_gemfile` (unknown N, no lock read)
or `invalid_lockfile` (known N, no rows), respectively, and zero registry lookups.
Use a bounded subprocess guard so a regression fails instead of hanging the
suite; synchronize replacement at the open hook, without sleeps or timing races.
On platforms without FIFO/safe-open capabilities, skip only the real FIFO witness
and deterministically test capability failure with mocks: existing safe source
failure, no unsafe fallback or content read. Preserve ordinary all-direct no-read
regressions. A pre-existing FIFO fixture alone does not exercise P1.

| AC | Planned deterministic witness and owner |
|---|---|
| AC-01 | Existing RootSourceTests plus scoped regression: absent/valid/invalid Gemfile yields identical ordinary results and no Gemfile open. |
| AC-02 | CLI→mixed scan→mock Ruby result with expected age, direct exact association and separate Test/test identities. |
| AC-03 | Parser/source cases for implicit default membership, explicit default selection and no automatic default/production inclusion. |
| AC-04 | One declaration with block/option overlapping memberships; one row, count and lookup. |
| AC-05 | Multiple/repeated CLI groups compared to selected union; stable deduplicated evidence. |
| AC-06 | Empty named block and implicit empty default; accepted/absent lock empty states, rejected-lock exception. |
| AC-07 | Known+unknown requests yield one source error, no partial rows and lock-read spy untouched. |
| AC-08 | Parser table for every positive S1 form and negative syntax family, including comments/quotes, interpolation, trailing tokens and unselected code; line/completion precedence and resource limits. |
| AC-09 | Optional true/false same declared membership; no config reads; nested groups reject. |
| AC-10 | Identical/conflicting/cross-group duplicates reject Gemfile; existing duplicate-direct lock rejection exercised through scoped path. |
| AC-11 | Missing/unreadable/nonregular/dangling/invalid UTF-8/outside-root Gemfile yields correct source reason, null counts and zero lookups; P1 regular-to-FIFO replacement before final open. |
| AC-12 | Missing lock with safe declaration pins yields N failures and no candidates; N=0 absent-lock exception. |
| AC-13 | Public selected name absent direct row with matching transitive spec: one lock_dependency_missing, no lookup. |
| AC-14 | Lock-only/unselected names excluded; mismatch table covers absent vs >=0, order/whitespace/operator differences and identical multiple literals, with safe provenance and no selected artifacts/lookup for mismatch. |
| AC-15 | Malformed/duplicate/unsupported/rejected lock retains N including zero, no rows and null measurements; isolated unsupported/ambiguous selections retain denominator. |
| AC-16 | Existing authority matrix through scoped source: private, mixed public/private namesakes, pins, GIT/PATH, multiple remotes and nonpublic Gemfile with public lock; no HTTP. |
| AC-17 | Output/mixed availability matrix: empty vs unavailable vs N>0 wholly unmeasurable, explicit 0% and null distinctions. |
| AC-18 | Each scoped failure with successful Python/npm siblings and no siblings; assert full repository and ecosystem summaries. |
| AC-19 | Full existing PyPI/npm/Yarn/mixed regressions; same exact name in three ecosystems and --resolved remains Python-only. |
| AC-20 | Human/JSON paired fixtures in single/mixed and normal/verbose branches: sources, groups, memberships, safe requirements, counts, nonpublic/mismatch explanations and F2 redaction. |
| AC-21 | Exact schema-v3 dictionaries and key-presence assertions for all S4 states, measured/local/registry failures, full membership arrays, artifacts and ordinary omission. |
| AC-22 | Scoped human disclosures and JSON evidence labels assert supplied-file claim only; production treated as an ordinary exact group name. |
| AC-23 | Root file before/after snapshots, forbidden subprocess/project-execution spies, read allowlist and zero credential/config/archive access. |
| AC-24 | Root-only fixtures with parent/nested/alternate decoys, inside/outside/broken links and simulated link replacement plus P1 regular-to-FIFO replacement for BOTH inputs; no outside target reads; direct-file scoped CLI error. |
| AC-25 | Existing registry/TLS suite plus scoped adapter wiring checks for CA/trust, fixed authority, redirect rejection, pacing and transport limits. |
| AC-26 | Mock canonical publications through scoped scan: platform artifacts, earliest admissible dates, latest stable, exact same-version zero and flagged negative-date clamping; existing metric/registry tests. |
| AC-27 | CLI exit matrix: completed success/empty/partial/source errors 0; bad/missing/comma options, direct-file and path failures 1; unrelated systemic exception 2. |
| AC-28 | Composed precedence table from Gemfile rejection through unknown group, unavailable lock, F1, absent direct, local validation, mismatch, selected-spec and registry failures. F1: nonpublic rack absent accepted lock direct scope yields unsupported_dependency_source/N=1/M=0/no lookup. F2: unsupported direct requirement yields unsupported_requirement/N retained/omitted lock_requirement/no unsafe text/safe declaration metadata/no lookup. P1 safe-read failures for each input precede content consumption/lookup. Assert ordinary output unchanged. |

Shared composed tests may cover AC-04/05, AC-06/12/17, AC-14/20/21 and
AC-16/28 when each assertion names its obligation. Keep negative parser tables
and cross-stage precedence tables separate so sharing does not hide coverage.
Check unsafe text absence using distinctive synthetic markers across JSON,
human and verbose diagnostics; never use real secrets in fixtures.

During later implementation run focused discovery, e.g.
`python -m unittest discover -s tests -p 'test_gemfile.py'`, then the scoped-source
module and relevant existing Ruby/CLI/output/mixed tests at integration points.
Run `python -m unittest discover -s tests` at the completed integration boundary,
then `git diff --check`. Require offline witnesses for all 28 ACs before
convergence; planning traceability is not a claim of passed feature tests.

## Sequencing, compatibility and later validation gate

After independent plan approval, task decomposition should order pure parser
and typed evidence first, then safe source reads/association (including F1/F2),
then scan propagation/availability, public CLI/output integration, and finally
composed regression/documentation/acceptance evidence. Add behavioral tests with
each change. These are design dependencies, not authorized implementation tasks.

Compatibility hinges on the absent-request branch calling the unchanged
all-direct source, never reading Gemfile. Optional trailing model fields and
explicit serializer omission preserve ordinary schema-v3 dictionaries and
human wording. Shared Ruby validation extraction must preserve Feature 004
precedence/artifact results, verified by its existing tests. No third-party
runtime dependency, broader ecosystem, generic version parser or transport
change is required. No metric semantics change is planned.

Before convergence the specification also requires a real-root supplied-file
example with independently established expected selected population. A later
human must authorize the particular target or supply permitted evidence; this
plan authorizes no external repository access. Preserve rejected constructs,
input limitations and the supplied-file claim. Optional live registry smoke is
separate, requires its own authorization, and cannot replace deterministic
correctness or become a prerequisite for task completion. No live validation
is performed or authorized by this planning run.
