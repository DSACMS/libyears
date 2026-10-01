# AGENTS.md

## Project

This repository implements the CHAOSS Libyears metric as a small local CLI.

The tool measures dependency freshness using release dates:

`libyears = (latest_stable_release_date - used_version_release_date) / 365.25 days`

The project intentionally favors simplicity, transparency, and long-term maintainability over broad ecosystem support.

## Runtime

- Python 3.12+
- Python standard library only
- No third-party runtime dependencies
- No database
- No server
- No containers
- No GitHub API dependency

## Commands

Run all tests:

`python -m unittest discover -s tests -v`

Run the CLI:

`python -m libyears PATH`

Example:

`python -m libyears .`

JSON output:

`python -m libyears . --json`

## Engineering Rules

- Do not add third-party dependencies.
- Do not change metric semantics without explicit instruction.
- Do not guess missing dependency versions or release dates.
- Prefer returning "unmeasurable" with a reason over fabricating data.
- Network access must be isolated behind registry adapter interfaces.
- Unit tests must not require network access.
- Use `unittest` and `unittest.mock`.
- Add tests for behavioral changes.
- Keep modules small and focused.
- Do not refactor unrelated code.
- Do not add additional package ecosystems unless explicitly requested.
- Do not parse semantic versions generically when authoritative registry metadata can answer the question.
- Keep human-readable output separate from JSON serialization.
- JSON output is considered a stable machine-readable interface once released.

## Git / Scope Discipline

For implementation tasks:

1. Inspect only files relevant to the task.
2. Make the smallest change that satisfies the requested behavior.
3. Run the narrowest relevant tests first.
4. Run the full test suite only when appropriate.
5. Summarize:
   - files changed
   - behavior implemented
   - tests run
   - unresolved issues

Do not make opportunistic cleanup changes.

## Metric Policy

Default scope:

- Direct dependencies only.
- Exact resolved versions are preferred.
- Prerelease versions are not considered "latest stable."
- No grace period.
- One libyear equals 365.25 days.
- Negative libyear values are clamped to zero only when timestamp ordering anomalies occur and must be flagged.
- Dependencies that cannot be measured are excluded from numerical aggregates but included in coverage statistics.

Output aggregates:

- dependency count discovered
- dependency count measured
- coverage percentage
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

Unmeasurable dependencies should include:

- ecosystem
- package name
- declared version/specifier where available
- reason

## Initial Ecosystem Scope

The first implementation supports Python packages from PyPI only.

Do not implement npm, Maven, Go, Cargo, RubyGems, NuGet, or other registries until explicitly requested.
