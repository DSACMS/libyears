# Changelog

Notable changes to Libyears are documented here.

## [Unreleased]

### Fixed

- Recognize bounded C# project candidates in ordinary human repository-root
  reports and explain explicit NuGet selection, so unselected projects are not
  mistaken for absent ecosystems. No automatic selection, NuGet aggregation or
  JSON/measurement contract change.

- Align human-readable dependency tables using the displayed headers and values,
  including long package names and versions, with right-aligned libyears values.

### Security

- Prevent pathological backtracking when classifying npm registry versions,
  preserving the accepted SemVer forms and release-selection behavior.

### Added

- Measure explicitly selected NuGet project snapshots with `--nuget-project`
  and an explicitly accepted producer/supplier witness via `--nuget-provenance`.
  Require coherent lock evidence and local/public content agreement; use nuget.org
  first-receipt dates and greatest listed stable versions. Add safe schema-v3
  evidence and availability reporting without executing dotnet, NuGet or MSBuild.
  NuGet measurement remains opt-in; unsupported filesystem safety primitives fail closed.

- Measure explicitly selected declared Ruby groups with repeatable
  `--ruby-group GROUP` on directory scans, using a conservative static Gemfile
  subset and independently authorized exact Gemfile.lock evidence. Unsupported
  or ambiguous syntax fails closed; safe declaration provenance stays separate
  from version evidence. Results describe supplied files only, without executing
  Ruby/Bundler or claiming installed, deployed or runtime scope. Ordinary
  all-direct Ruby scans remain unchanged when the option is absent.

- Measure direct RubyGems dependencies from a bounded root `Gemfile.lock` snapshot,
  alongside Python and npm, without executing Ruby or Bundler. Preserve selected
  artifact and observable publication provenance in additive schema-v3 evidence;
  report unsupported or missing evidence with honest coverage.

- Use root Yarn Classic v1 `yarn.lock` evidence to measure direct npm production
  dependencies with exact resolved versions.
- Scan direct npm production dependencies from the root `package.json`, using
  exact versions from root `package-lock.json` v2 or v3 without running npm or
  resolving dependency ranges.
- Scan npm and PyPI dependencies together, with repository-wide and
  per-ecosystem measurement summaries.
- Report source discovery failures separately from dependency-level
  unmeasurable results, including failures in one ecosystem while retaining
  successful measurements from another.
- Use shared verified HTTPS registry transport for PyPI and npm metadata
  requests.

### Changed

- Upgrade JSON output from schema v2 to schema v3. This is an intentional
  compatibility change for machine consumers: reports now identify ecosystems,
  include per-ecosystem summaries and ecosystem-keyed version evidence, and
  expose source errors separately.

## [0.1.1] - 2026-10-07

### Added

- Support resolved version snapshots as exact version evidence for declared
  Python dependencies, without measuring snapshot-only transitive packages.
- Add portable continuous integration for the test suite.

### Changed

- Improve human-readable measurement diagnostics while keeping the JSON
  contract unchanged.

## [0.1.0] - 2026-10-02

### Added

- Introduce a local Python CLI that measures direct Python dependency age from
  exact `requirements.txt` pins and PyPI release timestamps.
- Report individual measurements, aggregate libyears, coverage, and
  dependency-level reasons when measurements cannot be made.
- Provide machine-readable JSON output and human-readable scan diagnostics.
