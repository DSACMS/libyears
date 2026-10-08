# AGENTS.md

## Project

This repository implements the CHAOSS Libyears metric as a small local CLI.

The tool measures dependency freshness using release dates:

`libyears = (latest_stable_release_date - used_version_release_date) / 365.25 days`

The project intentionally favors simplicity, transparency, reproducibility, and long-term maintainability over broad ecosystem support.

## Runtime

- Python 3.11+
- Python standard library only
- No third-party runtime dependencies
- No database
- No server
- No containers
- No GitHub API dependency
- Do not invoke package managers or dependency resolvers unless an approved specification explicitly changes this boundary.

## Commands

Run the full deterministic test suite:

`python -m unittest discover -s tests`

Use verbose test output only when diagnosing failures or when test names are materially useful:

`python -m unittest discover -s tests -v`

Run the CLI:

`python -m libyears PATH`

Example:

`python -m libyears .`

JSON output:

`python -m libyears . --json`

## Engineering Rules

- Do not add third-party runtime dependencies.
- Do not change metric semantics without explicit instruction.
- Do not guess missing dependency versions or release dates.
- Prefer returning "unmeasurable" with a reason over fabricating data.
- Network access must be isolated behind registry adapter interfaces.
- Unit tests must not require network access.
- Use `unittest` and `unittest.mock`.
- Add tests with behavioral changes rather than deferring tests to the end.
- Keep modules small and focused.
- Do not refactor unrelated code.
- Do not add package ecosystems unless explicitly authorized by an approved specification or direct instruction.
- Do not implement generic package-manager, plugin, resolver, or semantic-version frameworks speculatively.
- Do not parse semantic versions generically when authoritative registry metadata can answer the question.
- Keep human-readable output separate from JSON serialization.
- JSON output is a versioned, stable machine-readable interface once released.
- Preserve existing ecosystem behavior when adding another ecosystem unless an approved specification explicitly changes it.
- Fail closed when evidence is missing, malformed, ambiguous, unsupported, or unsafe to interpret.

## Human Readability

Optimize implementation for human comprehension and long-term maintenance.

Assume the next maintainer may be an early-career Python developer who did
not participate in the original implementation.

Prefer:

- straightforward, idiomatic Python over clever or compressed code;
- explicit control flow over dense expressions;
- descriptive names over abbreviations;
- small functions with one clear responsibility;
- standard-library patterns familiar to ordinary Python developers;
- data structures that make domain concepts visible;
- comments that explain non-obvious reasons or constraints rather than
  restating the code;
- tests that demonstrate behavior clearly enough to serve as examples.

Avoid:

- unnecessary abstraction;
- metaprogramming when ordinary Python is sufficient;
- clever one-liners;
- deeply nested control flow;
- premature generic frameworks;
- indirection that does not remove meaningful duplication or isolate a real
  boundary;
- abstractions introduced only because a future feature might need them.

When two implementations are similarly correct, prefer the one that requires
less context to understand.

A small amount of duplication is preferable to a premature abstraction when
the duplicated concepts may evolve independently.

Do not reduce correctness, security, or explicit error handling merely to make
code shorter.

During review, treat unnecessary cognitive complexity as a maintainability
defect, not merely a style preference.

## Spec-Driven Development

Substantial features should follow the repository's spec-driven development workflow.

Feature artifacts live under:

`specs/NNN-feature-name/`

The normal progression is:

1. `spec.md` — user-visible behavior, scope, requirements, and acceptance criteria.
2. Clarification/review — resolve product ambiguity before technical planning.
3. `plan.md` — technical architecture for the approved specification.
4. Architecture review — resolve design issues before task decomposition.
5. `tasks.md` — dependency-ordered, bounded implementation tasks.
6. Task-graph review — verify ordering, scope, traceability, and safe task boundaries.
7. Implementation — execute approved tasks.
8. Verification and dogfooding.
9. Read-only convergence review against spec, plan, implementation, tests, and documentation.

When approved feature `spec.md`, `plan.md`, and `tasks.md` exist:

- Treat them as the source of truth for implementation.
- Do not rediscover or redesign approved requirements during implementation.
- Execute only dependency-ready approved tasks.
- Do not modify an approved spec or plan to justify an implementation choice.
- Stop and report a gap rather than inventing a missing product or architecture decision.
- Do not silently expand feature scope.
- Keep acceptance-criteria traceability intact when tasks change.

If implementation reveals a genuine product requirement that the approved specification does not address, return to the specification phase rather than deciding it in code.

## Git / Scope Discipline

For implementation tasks:

1. Inspect only files relevant to the task.
2. Make the smallest change that satisfies the approved behavior.
3. Run the narrowest relevant tests first.
4. Run broader regression tests at meaningful integration or phase boundaries.
5. Inspect the diff and run `git diff --check` before committing.
6. Keep each completed SDD task independently reviewable.
7. Summarize only:
   - task or phase status
   - files changed
   - behavior implemented
   - tests/results
   - local commit, when applicable
   - unresolved blockers or deviations

Do not make opportunistic cleanup changes.

### Git safety

- One completed SDD task should normally correspond to one local commit.
- Local task commits are allowed when explicitly requested by the execution prompt.
- Do not push unless explicitly instructed.
- Do not tag releases unless explicitly instructed.
- Do not rebase, reset, squash, amend published history, change remotes, force-push, or otherwise rewrite history unless explicitly instructed.
- Never combine unrelated tasks merely to reduce commit count.
- Do not mark a task complete unless its acceptance criteria and required verification pass.

## Filesystem Boundaries

Treat the repository workspace as the default filesystem boundary.

- Do not search, enumerate, inspect, or read files outside the current
  repository unless the user explicitly authorizes a specific external path
  or directory for the current task.
- The existence of readable sibling repositories or home-directory files does
  not imply permission to inspect them.
- When external input is required, ask the user to identify or authorize the
  path rather than searching the filesystem broadly.
- An explicitly authorized external repository may be read only for the
  stated task.
- Do not modify an external repository unless the user separately and
  explicitly authorizes modification.
- Do not inspect unrelated files in the user's home directory, credentials,
  configuration directories, keychains, SSH directories, browser data, or
  other sensitive locations.
- Prefer the narrowest filesystem access sufficient to complete the task.

## Testing and Context Efficiency

Optimize for correctness with low-context execution.

### Focused testing

During implementation:

- Prefer the narrowest relevant test target.
- Prefer compact successful output.
- Do not use `-v` by default.
- Use verbose output when diagnosing a failure, when individual test names are needed, or when a task explicitly requires it.
- Do not repeatedly run the complete suite after trivial changes unless required by the task.
- Run the complete deterministic suite at meaningful integration and phase boundaries.
- If shared behavior is changed, run the relevant regression tests even if the current feature tests pass.

Successful full-suite command:

`python -m unittest discover -s tests`

### Offline determinism

- Deterministic automated tests must not require network access.
- Registry responses should be represented with local fixtures or mocks.
- Live registry smoke tests, when specified, must be separate from deterministic unit correctness.
- A transient network failure in an optional live smoke test must not be misrepresented as a deterministic unit-test failure.

### Context discipline

- Read the smallest relevant source and test ranges needed for the current task.
- Do not repeatedly reread large unrelated files.
- Reuse conclusions already established by approved specs, plans, tasks, and the current thread.
- Do not generate broad repository summaries unless requested.
- Avoid dumping large successful test logs into the conversation when a compact result is sufficient.
- When a command succeeds, report the result concisely rather than reproducing routine output.

## Communication and Autonomy

Do not narrate routine work.

Routine work includes:

- file inspection
- straightforward edits
- normal test execution
- Git status/diff checks
- local commits already authorized by the execution prompt

During autonomous execution, interrupt only when necessary for:

- an unresolved product decision
- an architecture decision absent from the approved plan
- contradictory requirements
- a security or policy question
- a public contract/schema change not already approved
- an out-of-scope requirement
- a blocker that cannot safely be resolved within the current task

Do not ask for confirmation merely to continue behavior already approved by the spec, plan, tasks, and execution prompt.

Completion reports should be concise and contain only the information requested by the execution prompt.

## Phase-Level Autonomous Execution

When explicitly instructed to execute an approved SDD phase autonomously:

- Execute only tasks in that phase.
- Respect task dependencies.
- Complete tasks sequentially unless parallel execution is explicitly authorized.
- Run each task's focused verification.
- Mark a task complete only after its acceptance criteria pass.
- Create one local commit per completed task when authorized.
- Continue to the next dependency-ready task in the same phase.
- Run the full deterministic suite at the phase boundary.
- Run `git diff --check`.
- Confirm the working tree is clean after the final authorized commit.
- Stop before beginning the next phase.
- Do not push.

Stop autonomous execution rather than inventing a decision if:

- the approved spec and plan disagree
- required behavior is unspecified
- a new architecture decision is necessary
- existing released behavior would need to change unexpectedly
- a security boundary would need to change
- an acceptance criterion is contradictory or impossible
- completing the task would require explicitly out-of-scope work

## Metric Policy

Default scope:

- Direct dependencies only.
- Exact resolved versions are preferred.
- Prerelease versions are not considered "latest stable."
- No grace period.
- One libyear equals 365.25 days.
- Negative libyear values are clamped to zero only when timestamp ordering anomalies occur and must be flagged.
- A dependency whose used version is the latest stable version must produce exactly `0.0` libyears.
- Dependencies that cannot be measured are excluded from numerical aggregates but included in coverage statistics when their dependency scope was successfully discovered.
- When dependency discovery itself fails and the denominator is unknowable, do not fabricate coverage.

Output aggregates may include repository-wide and ecosystem-specific values as defined by the active schema/specification:

- dependency count discovered
- dependency count measured
- coverage
- cumulative libyears
- mean libyears
- median libyears
- maximum libyears

Individual measurable dependencies should include:

- ecosystem
- package name
- used version
- used version release timestamp
- latest stable version
- latest stable release timestamp
- libyears
- version evidence/source where defined by the active schema

Unmeasurable dependencies should include:

- ecosystem
- package name
- declared version/specifier where available
- stable machine-readable reason

Source-level failures should remain distinct from dependency-level unmeasurable results when the active specification defines that distinction.

## Ecosystem Scope

The current implementation supports direct Python packages from PyPI and
direct npm production dependencies under Feature 002. Public JSON output uses
schema version 3, with ecosystem-keyed evidence and repository plus
per-ecosystem summaries. Keep source-discovery failures in `source_errors` and
dependency-level failures in `unmeasurable`.

Additional ecosystems may be added only through explicit instruction or an approved feature specification.

Feature 002 authorizes npm ecosystem support according to:

- `specs/002-npm-support/spec.md`
- `specs/002-npm-support/plan.md`
- `specs/002-npm-support/tasks.md`

npm scope is limited to root `package.json` `dependencies`, excluding names
also present in `optionalDependencies`; `package-lock.json` versions 2 and 3
provide exact version evidence. Do not expand npm scope to development,
peer, workspace, or transitive dependencies without a separately approved
specification.

Do not infer authorization for Maven, Go, Cargo, RubyGems, NuGet, additional npm dependency scopes, or other registries from the existence of npm support.

For ecosystem behavior, the approved feature specification takes precedence over generic assumptions in this file.
