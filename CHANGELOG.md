# Changelog

Notable changes to Libyears are documented here.

## [Unreleased]

### Fixed

- Align human-readable dependency tables using the displayed headers and values,
  including long package names and versions, with right-aligned libyears values.

### Security

- Prevent pathological backtracking when classifying npm registry versions,
  preserving the accepted SemVer forms and release-selection behavior.

### Changed

- Ordinary NuGet scans can date qualified selected versions against a disclosed
  conventional nuget.org reference when repository policy supplies no contrary
  assignment or ambiguity. Preserve stronger testimony and mapping separately;
  alternate/private/unknown policy never falls back to public namesakes. Supported
  declaration populations can use the same narrow current-pair measurement floor
  without inventing supplier baseline assertions. Schema v3 adds comparator basis
  and limitations; explicit precision behavior and metric arithmetic are unchanged.

- Measure accepted NuGet project/lock snapshots with explicit package-specific
  public namespace authority, without requiring historical acquisition or content
  agreement for version age. Retain stronger v1 assurance; accept later v2 bound
  snapshot testimony and expose evidence/limitations additively in schema v3.
  Unknown/private namespaces and unsupported populations still fail closed.
  Default human output is concise; verbose/JSON retains assurance detail.

- Ordinary directory scans automatically attempt bounded NuGet project sources.
  Direct package occurrences count independently per project; successful siblings
  survive failures and unknown populations keep repository coverage null. Add
  source-qualified schema-v3 evidence and human project summaries; retain explicit
  single-project selection; the prospective evidence cascade separates measurement
  prerequisites from optional event/content assurance.

### Added

- Automatically select qualified current NuGet repository project/lock snapshots
  when declaration-first population is unsupported. Require bidirectional literal
  dependency/request/context coherence, disclose the policy basis in schema v3,
  and report missing namespace authority truthfully. No Git or supplier snapshot
  witness is needed for B1 population; explicit v3 remains available. This does
  not establish producer history or authorize public lookup.

- Accept an explicitly bound resolved NuGet snapshot as a population fallback when
  static project parsing cannot establish population. New v3 supplier testimony
  binds exact project/lock bytes and explicit external Direct scope; schema-v3
  evidence discloses the snapshot basis and limitations. Namespace authority stays
  separate; lock presence alone supplies no population or namespace authority.

- Accept explicit per-project supplier witnesses with repeatable
  `--nuget-witness PROJECT=NAME.json` during ordinary repository scans.


- Measure explicitly selected NuGet project snapshots with `--nuget-project`
  and an explicitly accepted producer/supplier witness via `--nuget-provenance`.
  Require coherent lock and accepted public namespace evidence; report optional
  local/public content agreement separately and use nuget.org
  first-receipt dates and greatest listed stable versions. Add safe schema-v3
  evidence and availability reporting without executing dotnet, NuGet or MSBuild.
  Unsupported filesystem safety primitives fail closed.

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
