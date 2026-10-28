# Changelog

Notable changes to Libyears are documented here.

## [Unreleased]

### Added

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
