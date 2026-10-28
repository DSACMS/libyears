# Feature 004 Technical Plan: Bounded RubyGems Support

## Status

Ready for narrow architecture verification

The independent architecture review of draft `223032e2b537d11a9dcbbf0eb49248d571373b1e` returned APPROVE WITH
CHANGES (PLAN CLARIFICATION REQUIRED). The three findings are clarified below;
architecture approval and implementation permission are not yet granted.
Task decomposition follows independent architecture approval.

## Approved Product Contract

The approved `spec.md` governs observable behavior, including all 52 acceptance
criteria. Its historical status paragraph predates the approval recorded in
`reviews.md` at `86be122e7570ed121572b25531f8b3994b2c6766`; that review approves technical planning only.
`c761b113ea19988e7e9ea5ca16b373c1e2c526fb` preserves the original specification, and `3b315696e4d03b5e7aac325b47a800abbade70e0` incorporates H1–H8.
Neither the historical paragraph nor this plan reopens those decisions.

Read root Gemfile.lock as an all-direct locked snapshot, without reading
Gemfile, resolving requirements, inspecting runtime platforms, or certifying Git
commit status. Preserve lock spelling, public-source authority, package-version
comparison across supported artifacts, earliest admissible observable dates,
and ASCII case-only registry identity. Preserve schema v3 and all existing
PyPI/npm/Yarn behavior. Missing public records establish neither yanking nor
historical nonexistence. No installation, Ruby/Bundler execution, credentials,
private-source access, archives, or additional runtime dependencies.

## Existing Architecture

The actual implementation already provides the necessary ecosystem-neutral
pipeline; Feature 003's plan describes an earlier state and is not the current
implementation contract.

- `scan.py` retains the legacy Python scan functions and exposes
  `scan_mixed_repository`, used by `cli.main`. `_python_source_result` combines
  requirements discovery with optional snapshot/constraint checks.
  `_npm_source_result` requires a root manifest and calls
  `npm.resolve_npm_evidence`. Direct file scanning stays Python-only.
- `npm.py` owns manifest scope, package-lock v2/v3 matching, Yarn selection,
  and `NpmAdapter`. `yarn.py` independently recognizes/parses Classic syntax;
  npm matching compares literal selectors. Both-lock conflict rejects npm
  evidence before reading either lock. Ruby must not alter those paths.
- `model.py` defines immutable `DependencyCandidate`, `SourceResult`,
  `SourceEvidence`, local failures and source errors. Candidates contain exact
  version, registry name, declaration and version source. `SourceResult`
  explicitly carries discovered count, measurement availability, presence,
  and human diagnostics; availability is not inferred from errors or rows.
- `RegistryResult` and `RegistryFailure` are shared adapter outcomes.
  `pypi.py` and the npm adapter own their registry/date/eligibility policies;
  both use `registry.VerifiedJSONTransport`. Transport owns verified TLS,
  explicit/default/environment/pip CA precedence, timeout, User-Agent, and safe
  failure categories. It currently reads unbounded bytes and follows urllib
  redirects; Ruby requires opt-in bounds and redirect restrictions.
- Mixed scanning pairs concrete sources with lookups, converts successful
  results to `Dependency`, calls `metric.measure_dependency`, and builds
  repository/per-ecosystem summaries through `_available_summary` and
  `metric.calculate_summary`. It already handles unknown denominators,
  rejected measurement, successful sibling rows and empty reports correctly.
- `metric.py` owns UTC elapsed-time arithmetic, anomaly clamping and numerical
  aggregates. It knows nothing about lockfiles or registry artifacts.
- `MixedScanReport` carries source results and safe diagnostic tuples.
  `output._report_parts` builds ecosystem-keyed provenance; `report_to_dict`
  explicitly serializes schema v3. Human formatting and `_reason_text` are
  separate; some reason wording still needs Ruby-specific context.
  CLI handles snapshot loading, CA validation, verbosity and exit categories.

Concrete reuse: SourceResult availability, candidates/failures, explicit source
pair iteration, summary calculation, verified transport and output serializers.
No registry dispatch framework, discovery framework, or generic lock model is
needed. Existing summaries and metric arithmetic suffice unchanged.

## Proposed Architecture

Three focused new modules are justified by separate responsibilities:

| Module | Inputs → outputs | Boundary and exclusions |
|---|---|---|
| `libyears/gemfile_lock.py` | decoded lock text → typed parsed lock or structural failure with safe context | Pure bounded syntax and duplicate preservation. No I/O, network, requirement semantics, source authorization, metric or serialization. |
| `libyears/rubygems.py` | root directory → SourceResult; parsed lock → authorized candidates/local failures | Root artifact reading, source authority and direct matching. No HTTP, publication selection, Gemfile interpretation or generic resolver. |
| `libyears/rubygems_registry.py` | authorized package name and exact version → RegistryResult/RegistryFailure with Ruby publication provenance | Public metadata validation, artifact classification and canonicalization. No repository parsing, source guessing, metric math or output formatting. |

Keep the adapter separate from `rubygems.py`: artifact population/date validation
and lock source attribution are substantial independent security boundaries.
Do not extract npm or Yarn code to make this arrangement symmetrical.

Flow: root lock → complete structural validation → exact direct matching and
public authority → candidates → fixed-authority registry adapter → established
dates/provenance → existing metric → existing availability summaries → output.

## Gemfile.lock Parser

Use a line-oriented state machine with named section handlers and explicit
indent levels. Small token validators may use anchored ASCII patterns; do not
use a single regex parser. Consume every nonblank line. Normalize line endings
only; preserve names, version text, declarations and distinct spec occurrences.

Minimum internal immutable records:

- `LockDependency(name, declared, requirement_text, source_pinned, line)`;
- `LockSpec(name, raw_selection, source_index, line)`; splitting into supported
  version/platform belongs to matching, so unsupported isolated tokens survive;
- `LockSource(kind, metadata, specs, line)`, preserving multiple GEM remotes;
- `ParsedGemfileLock(sources, dependencies, platforms)`;
- `LockParseFailure(reason, section, line, safe_category)`.

Metadata is a small ordered collection, not a dictionary that loses duplicate
keys. Tool/runtime sections need validation, not persisted domain records.
Nested requirements need framing validation and parent ownership, not storage
as a dependency graph. Lists preserve artifact duplicate rows for the matcher.

States distinguish heading, source metadata, specs, nested row, direct rows,
platforms and optional tool/runtime body. Enforce two/four/six-space framing;
reject tabs, orphan nested rows, malformed parentheses/trailing syntax,
conflict markers and misplaced fields. Allow LF/CRLF and blank separators.
Require at least one recognized source, one DEPENDENCIES and one nonempty
PLATFORMS. Empty DEPENDENCIES is valid. Reject repeated singleton sections,
direct names, platform entries and metadata keys except multiple GEM remotes.
PLATFORMS accepts the specified ASCII tokens and never selects a variant.
BUNDLED WITH accepts one indented tool token, and RUBY VERSION one description;
neither supplies versions or scope, and Bundler generation is not inferred.

GEM supports remote/specs framing. GIT/PATH support only the spec's metadata
allowlists and spec/nested envelopes, enabling safe ownership isolation without
following their values. Repeated GEM blocks remain distinct. Unknown fields,
unknown/recognized unsupported sections (including CHECKSUMS, CONTENT ADDRESSES,
PLUGIN SOURCE) record unsupported-format evidence. Continue structural checking
where safely possible so later malformed supported framing wins over that
classification. Never salvage a DEPENDENCIES substring from a rejected file.
An unclassifiable arbitrary/empty file is unsupported; recognizable supported
section structure missing required sections is invalid. Unsafe boundaries or
identity recovery reject the whole source, rather than guessing ownership.

Nested rows delimit a name and optional balanced requirement. Safely delimited
unsupported nested requirement text is inert. Broken framing is a source error.
Direct unsupported requirement text is preserved for dependency classification.
No nested requirement contributes scope or gets evaluated.

## Source Authority

`rubygems.authorize_public_selection` is the sole construction path for Ruby
candidates. It receives every spec occurrence for the exact direct name across
all source blocks, plus the direct pin marker; inspecting only a preferred
public block would violate the contract. Only GEM blocks with exactly one
literal `https://rubygems.org` remote, optionally ending in `/`, authorize public
identity. Repeated independently authorized blocks can combine evidence.

Any Git/PATH/nonpublic/missing/multiple-remote association or `!` blocks lookup,
including when a public namesake coexists. Safe ownership yields
unsupported_dependency_source; unsafe ownership rejects the source during
parsing. Never store remote values in output/diagnostics, and never pass them
to a transport. Candidates exist only after local validation and authority;
source rejection returns no candidates. Scan calls registry only for candidates.
This constructor gate plus no-call tests makes authority more than scattered
lookup conditionals. The adapter's public API accepts identity, never URLs;
it does not independently discover or override repository authority.

## Dependency Matching

Index specs by exact lock name to lists of occurrences. For each direct entry,
apply Failure Mapping precedence. Validate the bounded ASCII gem name (first
and last alphanumeric, at least one letter, internal letters/digits/`.`/`_`/`-`).
Validate requirement framing as comma-separated supported operator/version
terms with permitted whitespace and repeats. Bare exact, `=`, ranges and
compounds are retained without equality, satisfaction or equivalence checks.

After authority, no specs means lock_version_missing, even for exact
requirements, bundler or tzinfo-data. Parse ordinary selected version as digits
then nonempty ASCII alphanumeric dot segments; the first hyphen introduces
platform. No suffix means platform `ruby`. Preserve each supported artifact;
never choose host platform or filter through PLATFORMS. Extra identity or
unsupported isolated selection gives unsupported_lock_evidence. A malformed
row boundary was already rejected by the parser.

One supported spec establishes a version. Distinct supported artifacts with
identical version text establish one dependency, including across same-remote
blocks. Different versions or repeated identical artifact occurrences give
ambiguous_lock_evidence; do not deduplicate structural rows. Collect these
conditions before returning a reason so ambiguity precedes unsupported identity
where both can be established. Never infer meaning from unknown token fragments.
Retain safely established selected artifacts on failed dependencies where
material. Transitive-only names never create candidates or requests.

## RubyGems Registry Adapter

`RubyGemsAdapter.lookup(name, used_version)` follows the existing adapter API
and returns the common result/failure types with optional Ruby provenance.
Validate identity inputs defensively, safely quote a path component with no
permitted separators, and construct only fixed `https://rubygems.org` URLs.
No metadata links, repository URLs, credentials, retries or caching.

Parse JSON strictly, rejecting duplicate conflicting object keys and wrong
required types (including nonboolean classification). Validate all relevant
artifact records before selecting dates. Use `RubyArtifactRecord` for exact
version, platform, ABI classification, aware creation time or missing time,
prerelease, availability and optional authoritative yank status. This is adapter
internal and never serialized wholesale. Missing/invalid creation dates are
excluded individually; contradictory authoritative identity/date fields fail.
Byte-equivalent duplicate metadata can collapse; conflicting same-full-identity
records fail. Recognizable nonnull ruby_abi classes are excluded; malformed or
unclassifiable identity cannot be silently treated as generic.

Extend `VerifiedJSONTransport` with opt-in `max_response_bytes` and
`allowed_authority` controls. With neither enabled, preserve the existing
`request.urlopen` path, timeout/context/User-Agent arguments, no-argument
`response.read()`, redirect behavior and injected `transport.get(url)` contract.
Do not replace the default path globally or require existing injected transports
and response doubles to accept new arguments or expose headers/sized reads.
Existing PyPI/npm/Yarn transport semantics remain unchanged.

Ruby opts into a verified opener with a redirect handler rejecting all redirects
(simpler than maintaining an allowlist chain), reusing selected SSL context and
CA policy. Read at most limit+1 bytes and check declared length and incomplete
reads. Extend `TransportFailure` with defaulted optional typed bounded-failure
metadata: `response_too_large` for detected oversize; `incomplete_response` for
detected truncation, including `http.client.IncompleteRead` or EOF short of a
valid declared Content-Length. Classify these before generic exception handling;
never reuse partial bytes. Ruby maps both to `invalid_registry_response`, never
`registry_error`; these internal categories are not new public reasons. Ordinary
transport/TLS/timeout failures retain `registry_error`. Undetectable truncation
is not claimed detectable; malformed JSON still fails registry validation.
Default timeout remains 10 seconds. Set Ruby limit to 16 MiB per response, two
requests and 32 MiB total per candidate. Reject truncated/oversize populations
rather than measuring a prefix.

Before registry measurement, schedule all locally accepted Ruby candidates in
ascending lexical order of `(exact lock name, exact used version)`, using the
preserved ASCII text without case normalization. Direct names are unique; this
stable key does not depend on lockfile row/source order. Use that order for
sequential lookups and the existing fixed identity-then-population request order.

One adapter instance per scan paces sequential Ruby request starts at least
0.11 seconds apart using monotonic time, injected clock/sleep in tests. On 429
fail the affected lookup with registry_error immediately; never retry it.
Record a scan-local cooldown from a valid Retry-After (seconds or HTTP date);
subsequent candidates during cooldown fail without requests. An invalid/missing
header on 429 closes Ruby requests for that scan. TransportFailure gains optional
Retry-After metadata without changing existing consumers. No sleeps waiting for
long server cooldowns, alternate host, hidden retry or partial response reuse.
Cooldown state is scan-local and may suppress later scheduled requests under
this finite-request policy. Equivalent candidate sets in different lock orders
must yield the same observable results, requests and failure isolation with the
same deterministic per-request responses and injected time. This does not imply
identical results when upstream responses themselves change. No concurrency is
introduced.

## Registry Endpoint Strategy

Choose two metadata requests per locally accepted candidate:

1. `/api/v1/gems/{name}.json` establishes returned package name. Only its identity
   is used; its selected version/date/latest labels do not define population.
2. `/api/v1/versions/{validated_registry_name}.json` supplies the complete bounded
   observable public artifact array. Use returned spelling only after identity
   validation, retaining original lock spelling in reports.

The [official API reference](https://guides.rubygems.org/rubygems-org-api/)
documents name in package metadata and version-array fields `number`, `platform`,
`ruby_abi`, `prerelease`, `created_at`. A version-specific v2 response would not
supply the cross-version/platform population, so it is unnecessary here.

### Immutable implementation evidence

Pin RubyGems.org revision `9d5892f97d320b8d5ca8446f7119743afeb97183` for reproducible
fixture documentation. Inspected official source on 2026-10-28; no live package
lookups were performed. All links below use that same immutable revision:

- [Versions controller](https://raw.githubusercontent.com/rubygems/rubygems.org/9d5892f97d320b8d5ca8446f7119743afeb97183/app/controllers/api/v1/versions_controller.rb):
  `show` renders the full `public_versions.includes(:gem_download)` relation as
  JSON without pagination or a limit, and returns 404 for an empty relation.
- [Package model](https://raw.githubusercontent.com/rubygems/rubygems.org/9d5892f97d320b8d5ca8446f7119743afeb97183/app/models/rubygem.rb):
  `public_versions` applies `by_position.published`; `payload` includes `name`
  and `as_json` delegates to it, supporting the independent identity response.
- [Package controller](https://raw.githubusercontent.com/rubygems/rubygems.org/9d5892f97d320b8d5ca8446f7119743afeb97183/app/controllers/api/v1/rubygems_controller.rb):
  public `show` renders the package only when hosted with indexed public
  versions; otherwise it returns 404.
- [Version model](https://raw.githubusercontent.com/rubygems/rubygems.org/9d5892f97d320b8d5ca8446f7119743afeb97183/app/models/version.rb):
  `published` applies `indexed.by_created_at`, and `indexed` filters
  `indexed: true`. `payload` and delegated `as_json` expose `number`, `platform`,
  `ruby_abi`, `prerelease`, and `created_at` (separately from `built_at`).
  ABI validation allows null or a major.minor string; uniqueness checks include
  ABI alongside number/platform. Thus version/platform alone is insufficient
  identity for all upstream artifacts. Nonnull recognizable ABI classes remain
  excluded under the approved spec, without ABI resolution.

This source chain demonstrates a two-response strategy that supplies package
identity and the complete observable published artifact population at this
revision, including required classification and serialization. Published/indexed
membership establishes current availability; the population payload has no yank
history field and filters out unindexed records. Do not infer absence is yanking.
The package payload's selected-version fields do not define that population.

The approved spec, rather than this implementation snapshot, requires supported
full identity, authoritative creation times, stable/availability classification,
and no silent population truncation. The pin demonstrates endpoint feasibility
and anchors fixtures; it does not prove deployed behavior forever or guarantee
complete historical publication knowledge. Deployed metadata must still pass
strict validation; drift cannot justify weakening the approved wire requirements.

Require the documented fields/classification; null ruby_abi denotes ordinary
identity. Do not infer ABI absence from a missing required field. If future
responses authoritatively expose yanked records, normalized records retain them
and canonicalization supports them; conflicting endpoint availability and
explicit yank assertions fail validation rather than being guessed away.
No additional historical endpoint or historical reconstruction is planned.

404 before usable public package evidence means package_not_found. A subsequent
population 404 after identity success likewise means package no longer publicly
observable, with a safe disappearance diagnostic. A valid empty population or
population without supported exact used records gives version_not_found.
Supported used records with no admissible dates give release_date_missing;
otherwise no eligible stable version gives no_stable_release. Other HTTP/TLS
failures give registry_error; malformed/contradictory metadata gives
invalid_registry_response. No absence implies known yanked or never existed.

Use the pinned source chain above in fixture documentation. If endpoint drift
prevents establishing required identity or availability, fail closed and report
the gap; do not weaken the approved contract.

## Canonicalization

A directly testable Ruby-specific `canonical_publication(records)` returns the
earliest date plus contributing admissible artifacts. Establish supported
observable population first, retain observable yank evidence where available,
exclude missing/invalid/naive times, normalize to UTC with fractional precision,
exclude the entire UTC date 2009-07-25 and unsupported artifact classes, then
choose the minimum. Never use built_at, package update time or fallback dates.
No admissible records means no canonical date. Both roles call this helper on
the same version grouping, including used prereleases/yanked records if visible.

Latest eligibility separately requires an available supported stable artifact
and canonical date. Select greatest canonical timestamp, then ascending exact
version lexical tie-break; never numerical version order or server labels.
Canonical contributor arrays sort by version, platform and timestamp for stable
output. Same used/latest version reuses the identical canonical date and yields
exact zero. Negative anomalies remain existing metric behavior. `metric.py`
remains unchanged and learns no Ruby artifact concepts.

## Identity and Supply-Chain Boundary

Source authorization precedes any HTTP. Registry identity checking is a separate
boundary: compare ASCII strings after translating only A–Z to a–z. Require exact
punctuation and reject Unicode rather than casefolding it. All returned name
fields must agree. The identity endpoint is mandatory because the population
endpoint omits a name. Missing/mismatched identity is invalid_registry_response,
not a fallback search or alternate spelling lookup. Safe quoting does not
normalize identity. No aliases, fuzzy matching or typosquatting detection.

## Evidence and Schema v3

Extend existing model objects with defaulted optional, typed Ruby evidence;
existing positional constructors and serialization must remain compatible.
Keep output-facing domain records in `model.py`, avoiding imports of parser
internals into shared models:

- `SelectedRubyArtifact(version, platform, source)`;
- `RubyPublicationArtifact(version, platform, publication_time, yanked=None)`;
- `RubyGemsEvidence(selected_artifacts, used_publication_artifacts=None,
  latest_publication_artifacts=None)`.

Candidate, Dependency and UnmeasurableDependency carry optional rubygems_evidence.
RegistryResult/RegistryFailure carry optional Ruby publication evidence to retain
safely established material on failures; scan merges selected and publication
evidence explicitly. SourceEvidence adds optional scope/publication_basis fields.
Do not introduce an arbitrary metadata dictionary or serialize dataclasses blindly.

`version_evidence.rubygems` has declaration_source and snapshot_source
`Gemfile.lock`, accepted format `gemfile_lock` (null on source rejection), scope
`all_direct_locked`, publication_basis `earliest_admissible_supported_observable`.
Ruby measured rows have version_source `gemfile_lock` and rubygems_evidence with
selected_artifacts and used/latest_publication_artifacts as defined by spec.
Publication arrays include every supported admissible contributor, not just the
minimum; omit yanked unless known. Failure evidence omits unavailable arrays.
Source errors remain only ecosystem/source/reason. No parser structures or human
diagnostics enter JSON. Non-Ruby rows omit all new fields. Schema stays 3.

## Source Availability and Aggregation

Reuse SourceResult and `_available_summary` without changing their semantics:

| Ruby source state | Discovered / measured / coverage | Numeric summary |
|---|---|---|
| absent | omitted | omitted |
| valid empty | 0 / 0 / null | total 0.0, others null |
| rejected whole source | null / null / null | all Ruby numeric fields null |
| known N with local/registry failures | N / successful M / M/N | successful rows only |
| nonempty all registry failures | N / 0 / 0.0 | total 0.0, others null |

Rejected Ruby has no candidates or synthetic rows. Repository unknown discovery
and coverage follow existing source availability; successful sibling rows and
numeric aggregates survive. Measured is null only when every detected source is
unavailable, otherwise successful count including zero. With no sources use the
existing empty report. Repository total with no successful rows is 0.0 even
when counts are unknown. Metric and summary arithmetic remain unchanged.

## Failure Mapping

| Reason | Producer and level | Ruby lookup / sibling continuation |
|---|---|---|
| invalid_lockfile | root reader or structural parser; source | none / other ecosystems only |
| unsupported_lockfile_format | parser recognition/unsupported structure; source | none / other ecosystems only |
| unsupported_dependency_name | direct matcher; dependency | none / Ruby and other ecosystems |
| unsupported_requirement | direct framing validator; dependency | none / Ruby and other ecosystems |
| unsupported_dependency_source | authority gate; dependency | none / Ruby and other ecosystems |
| lock_version_missing | selection matcher; dependency | none / Ruby and other ecosystems |
| ambiguous_lock_evidence | duplicate/version matcher; dependency | none / Ruby and other ecosystems |
| unsupported_lock_evidence | artifact identity validator; dependency | none / Ruby and other ecosystems |
| package_not_found | adapter public absence; dependency | attempted / Ruby and other ecosystems |
| version_not_found | adapter supported used population; dependency | attempted / Ruby and other ecosystems |
| release_date_missing | canonical used date; dependency | attempted / Ruby and other ecosystems |
| no_stable_release | latest eligibility; dependency | attempted / Ruby and other ecosystems |
| registry_error | adapter transport/budget/rate limit; dependency | attempted or cooldown prevents request / Ruby and other ecosystems |
| invalid_registry_response | adapter decode/validation/size; dependency | attempted / Ruby and other ecosystems |

Deterministic precedence: malformed supported structure, unsupported whole
source, isolated name, direct requirement framing, authority, missing/ambiguous
selection, unsupported selected identity, registry. Validate registry metadata
before used absence, used date absence, then stable absence. Collect structural
findings before selecting their reason; never let parser iteration order change
failure category. No additional stable reasons are proposed.

## Diagnostics

Use existing `(name, safe message)` diagnostics and ecosystem/source-aware human
reason formatting. Preserve original declared text in dependency failures.
Give safe section/line/category for malformed locks; explain missing remote or
unsupported authority without remote values and explicitly state no public
namesake substitution. Distinguish differing variants, duplicate artifacts and
single unsupported identity rather than calling every platform failure ambiguous.
Registry identity mismatch, malformed metadata and import-day exclusions receive
safe category messages, never raw response bodies or exceptions. Normal Ruby
output always discloses all-direct scope, uninterpreted groups, observable-history
limits and possible changes after disappearance. Null coverage is unavailable,
not 0%. Whole-source errors name Gemfile.lock. Verbose JSON stays identical.

## Scan Integration

Add one root-only Ruby source operation to `scan_mixed_repository` alongside
`_npm_source_result`, with injectable rubygems adapter/lookup and ca_bundle.
Use artifact presence detection that distinguishes absence from a present
nonregular/unreadable artifact, including broken links; no Gemfile inspection.
Direct file arguments do not enter Ruby discovery. Add a third explicit source
pair. Replace repeated two-source tuples with one local sources tuple derived
from those pairs; this removes concrete duplicated enumeration in failures,
diagnostics, detection and returned report. It is not dynamic registration.

Preserve existing Python/npm functions and legacy scan APIs. The common loop
merges optional Ruby provenance on success/failure before invoking unchanged
measure_dependency. Include Ruby trust reporting when it is the active source.
Existing summaries consume the additional source unchanged. CLI needs no new
option; test exits, --resolved isolation, --verbose and --ca-bundle through the
existing CLI entry. No Ruby source activates until the public phase below.

## Public Activation Boundary

Internal parser, authority matcher, evidence model, transport controls and adapter
may land without scanning any Ruby project publicly. Defaulted model fields
serialize nothing for current ecosystems. Internal source tests may invoke Ruby
source discovery directly while scan remains unchanged.

Phase 5 is the single public activation boundary: orchestration, provenance,
source/summary behavior, human/JSON output and documentation become coherent in
one reviewable change. No earlier phase adds Ruby to scan's source pairs. A
stopped repository after each internal commit preserves the released contract.
If that coherent activation cannot fit a bounded commit, keep further internal
work unactivated rather than expose incomplete output.

## Testing Strategy

All correctness fixtures/mocks are offline unittest tests. Inject clock/sleep
and HTTP responses; prohibit live requests in new scan/CLI fixtures. Add tests
with each behavioral component, not at the end. Future task decomposition must
map all AC-01–52 to concrete cases; these are test families, not tasks.

- `test_gemfile_lock.py`: ordinary/empty locks, LF/CRLF, repeated GEM blocks,
  same/different/missing/multiple remotes, GIT/PATH envelopes, malformed indent,
  markers, unknown fields/sections, combined malformed/unsupported precedence,
  nested supported/inert unsupported/unsafe requirements, PLATFORMS missing,
  empty/repeated/duplicate/malformed, optional BUNDLED WITH and RUBY VERSION,
  duplicate rows, unsupported artifact framing and invalid text.
- `test_rubygems.py`: lock-only activation, Gemfile-only/no-source, directory vs
  direct-file/nested filenames, unreadable/nonregular artifacts, direct count,
  transitive exclusion, exact case matching, name syntax, requirement forms,
  ordinary/single platform/agreeing variants/differing versions/duplicates,
  unsupported identity, missing specs, special dependencies, and precedence.
  Assert no registry access for every rejected source/direct case, especially
  private/GIT/PATH + public namesake and uncertain remote ownership.
- `test_rubygems_registry.py`: mock identity case differences, punctuation and
  Unicode mismatches, absent package/version, prerelease used/latest roles,
  supported and unsupported ABI population, missing field/classification,
  missing/invalid/import-day dates, contradictory duplicate metadata and JSON,
  multiple artifacts, no stable release, response reorderings, TLS/HTTP errors,
  byte/request limits, truncation, redirects, pacing and Retry-After cooldown.
  Include normalized observable yanked records to test canonicalization without
  claiming current endpoints expose them; reject contradictory wire assertions.
  Assert separately that typed oversize and typed incomplete-response failures
  map to invalid_registry_response with no partial metric, while ordinary
  TLS/timeout/transport failures remain registry_error.
  Permute equivalent Gemfile.lock dependency orders with fixed per-request
  responses (including 429 and missing/valid Retry-After) and injected time;
  assert identical scheduled requests, cooldown suppression, rows, reasons,
  evidence and summaries.
- Canonical helper tests: earliest admissible, earlier yanked contributor, one
  inadmissible plus one valid, all inadmissible, UTC import-day offsets,
  fractional precision, deterministic ties, same-version exact zero. Exercise
  existing negative anomaly through metric calls rather than new Ruby math.
- Mixed/CLI/output: three ecosystems success, Ruby source rejection alongside
  success, partial Ruby local/registry failures, all Ruby registry failures,
  valid empty Ruby, all sources unavailable and no sources. Assert count/null
  matrices, per-ecosystem identities, human/JSON agreement, scope/history
  disclosures, contributor provenance, safe diagnostics, schema 3 and JSON
  verbosity invariance. Preserve exact existing Python/npm evidence objects.

Use small named lock/JSON fixtures under `tests/fixtures/rubygems/`; generated
variants in tests are appropriate for one changed boundary. No live-dependent
expected values or third-party parser comparison tests.

AC traceability families: recognition AC-01–05/52; direct matching AC-06–17;
authority/transport AC-18–20/43–45; dates/eligibility AC-21–29/51; summaries
AC-30–37; evidence/output/CLI AC-38–42; repeated sources/precedence AC-46–50.
Each belongs to offline verification, never exclusively future dogfood.

## Regression Boundaries

| Existing suite | Contract guarded |
|---|---|
| tests.test_pypi | PyPI adapter/date behavior; existing TLS/CA transport tests |
| tests.test_requirements, tests.test_snapshot, tests.test_constraints, tests.test_scan | Python declarations, snapshot matching, legacy scans |
| tests.test_npm | manifest scope, package-lock v2/v3, lock selection and Yarn matching |
| tests.test_yarn | Classic recognition/parser behavior |
| tests.test_npm_registry | npm registry identity, timestamp and transport semantics |
| tests.test_mixed_scan | availability, mixed aggregates and failure isolation |
| tests.test_metric | arithmetic, anomaly and numerical aggregates |
| tests.test_output | human output and stable schema-v3 serialization |
| tests.test_cli | CLI flags, CA validation, snapshots and exit categories |

Explicit default-path regression: existing urlopen patches and injected
`transport.get(url)` doubles must keep working unchanged, including no-argument
`read()` responses and original timeout/context/User-Agent and failure behavior.
Run existing PyPI/npm registry tests and Yarn/mixed regressions unchanged.
Add `tests.test_registry` for opt-in transport bounds/redirects and failure
metadata. Run focused module commands per phase, not the whole suite per small
edit. Run `python -m unittest discover -s tests` at transport/model integration,
public activation and final deterministic phase gates; `git diff --check` before
commits. This planning-only change requires whitespace/scope checks, not code
execution or a new full-suite claim.

## Release Validation

Future validation only, after implementation approval and deterministic gates:
select one explicitly authorized real Ruby root by inspecting only necessary
root lock evidence. Discovery's historical external paths grant no current read
permission. Use normal verified transport in human and JSON CLI runs, no tooling
execution, and compare scope/counts/reasons/arithmetic, selected and publication
provenance, history disclosures and environment/limits. Verify target unchanged.
Record discrepancies without silently fixing them inside validation. Optional
separate live smoke is useful only if dogfood did not establish the same path;
record a skip when redundant and separate environmental failure from offline
correctness. Finish with fresh-context independent read-only convergence against
spec, approved plan/tasks, implementation, tests, docs and release evidence.

## Documentation and Artifact Lifecycle

Commit this first draft before independent architecture review. Later record
review findings and revisions in reviews.md and Git; only after approval create
and review tasks.md. Do not change spec to accommodate implementation shortcuts.

At public activation update README, SPEC, CHANGELOG Unreleased Added, and AGENTS
ecosystem scope together with observable output. Explain bounded sections,
lock-only/all-direct meaning, requirements not evaluated, source authority,
platform provenance and history limitation. Preserve existing ecosystem details.
At release validation create release-validation.md; maintain reviews.md with
independent audit findings. After completion reconcile ROADMAP's SELECTED entry
using existing lifecycle conventions and completion references; no invented radar
state or new interpreted-Gemfile scope. Create retrospective.md after convergence,
including whether committed pre-review drafts improved durable reconstruction.
No release/tag/push is implied. None of these artifacts changes in this task.

## Human Readability

Use the small named Ruby records above, explicit loops/state transitions and
named authorization/canonicalization helpers. Keep raw lock/registry structures
inside their boundary. Explain why unsupported evidence blocks lookup, rather
than repeating code in comments. Avoid parser combinators, generalized registries,
normalization machinery, dense expressions and premature Yarn/Ruby deduplication.
Tests should read as examples of accepted evidence and each failure boundary.

## Expected File Changes

| Classification | Files | Concrete purpose |
|---|---|---|
| DEFINITELY NEEDED | libyears/gemfile_lock.py; tests/test_gemfile_lock.py | bounded parser and framing examples |
| DEFINITELY NEEDED | libyears/rubygems.py; tests/test_rubygems.py | source authority, direct matching and discovery |
| DEFINITELY NEEDED | libyears/rubygems_registry.py; tests/test_rubygems_registry.py | metadata, identity, canonicalization and bounds |
| DEFINITELY NEEDED | libyears/model.py | typed optional Ruby provenance and scope/basis metadata |
| DEFINITELY NEEDED | libyears/registry.py; tests/test_registry.py | opt-in bytes/redirect control and rate-limit failure metadata |
| DEFINITELY NEEDED | libyears/scan.py; tests/test_mixed_scan.py | third source, provenance transfer, availability regressions |
| DEFINITELY NEEDED | libyears/output.py; tests/test_output.py | additive Ruby evidence and contextual human output |
| DEFINITELY NEEDED | tests/test_cli.py; tests/fixtures/rubygems/ | public activation/security/exit and readable fixture cases |
| DEFINITELY NEEDED | README.md; SPEC.md; CHANGELOG.md; AGENTS.md | coherent activation documentation checkpoint |
| DEFINITELY NEEDED | specs/004-rubygems-support/release-validation.md; reviews.md; retrospective.md; tasks.md | later approved lifecycle, not this draft task |
| LIKELY NEEDED | ROADMAP.md | completion references under existing lifecycle convention |
| POSSIBLY NEEDED | tests/test_pypi.py; tests/test_npm_registry.py | default injection compatibility assertions; existing doubles must not require sized reads or opener support |
| SHOULD REMAIN UNCHANGED | libyears/metric.py; libyears/pypi.py; libyears/npm.py; libyears/yarn.py | existing arithmetic and ecosystem policies |
| SHOULD REMAIN UNCHANGED | libyears/requirements.py; snapshot.py; constraints.py; cli.py; __main__.py; __init__.py | no new flags, Python behavior or runtime setup |
| SHOULD REMAIN UNCHANGED | tests/test_metric.py; test_requirements.py; test_snapshot.py; test_constraints.py; test_scan.py; test_npm.py; test_yarn.py | existing regression assertions suffice |
| SHOULD REMAIN UNCHANGED | Feature 004 spec.md/discovery.md; Feature 003 artifacts | approved product/history records |

## Implementation Phases

Phases are prospective reviewable boundaries, not an approved task graph. Each
may decompose into small commits after architecture and task-graph approval.

| Phase | Objective / expected files | Activated behavior | Focused verification / safe stopping condition |
|---|---|---|---|
| 1 | bounded syntax: gemfile_lock.py, parser tests/fixtures | internal parser only | test_gemfile_lock; all structural failures preserve no partial scope; public scan unchanged |
| 2 | authority/matching and typed evidence: model.py, rubygems.py, test_rubygems | internally callable source results | parser/source tests plus output compatibility; no Ruby source pair; existing output unchanged |
| 3 | bounded shared transport: registry.py, test_registry | opt-in controls only | transport plus test_pypi/test_npm_registry; full deterministic gate; old callers unchanged |
| 4 | registry and canonicalization: rubygems_registry.py, adapter tests/fixtures | internally callable adapter only | adapter/source tests, no network; no public Ruby discovery or output |
| 5 | coherent public activation: scan.py/output.py, mixed/output/CLI tests, README/SPEC/CHANGELOG/AGENTS | full Ruby directory scanning with scope, summaries and provenance | mixed/output/CLI focused tests then full offline suite; public behavior/docs agree; all prior internal gates pass |
| 6 | deterministic convergence preparation: end-to-end fixtures/tests, later tasks traceability | no new product behavior | unique full-path cases, all 52 AC mapped, full deterministic gate, diff check; ready for release validation |
| 7 | authorized dogfood and independent convergence: release-validation.md/reviews.md; completion ROADMAP and post-convergence retrospective | no new runtime behavior | human/JSON comparison, unchanged target, independent fresh-context audit; record findings separately, no automatic remediation |

Phase 4 requires phases 2 and 3; phase 5 requires all internal phases. Sequential
execution is the default. Each completed task should remain independently
reviewable and leave a valid repository. Do not begin any phase from this draft.

## Architecture Risks

| Risk | Mitigation and test boundary | Stop/escalation condition |
|---|---|---|
| bounded parser misattributes structure | explicit state/indent rules, duplicate preservation, mixed malformed/unsupported fixtures | safe scope/ownership requires inference outside approved grammar |
| public namesake lookup | sole authorization constructor and all-occurrence ownership checks; no-call tests for every rejected authority | a candidate can reach HTTP without positive public authority |
| endpoint incompleteness/change | documented two-response observable population, bounded whole-body parsing, fixed-source fixture evidence | required identity/classification/population cannot be established; stop adapter approval rather than invent history |
| artifact identity collapse | require ABI classification, exclude recognized unsupported records, reject contradictions; platform/ABI fixtures | unsupported class cannot be distinguished from supported evidence |
| canonicalization drift | one named helper and shared per-version canonical result; used/latest permutation and date tests | observable implementation conflicts with normative timestamp policy |
| provenance bloat | three small output domain records, explicit serializer, no parser payload; schema fixtures | new field requires reinterpretation of existing schema rather than additive evidence |
| third-registry maintenance cost | focused modules, two requests, no caches/retries/framework; readable offline cases | scope demands generic resolver/parser machinery or extra runtime dependencies |
| existing ecosystem regression | opt-in transport changes, defaulted model fields, exact old-output assertions, full phase gates | fixing Ruby requires changing released PyPI/npm/Yarn semantics |
| rate/transport edge cases | sequential pacing, no retry, finite bytes/timeout, fail-closed cooldown; injected clock/HTTP tests | implementation needs unbounded waiting/fan-out or bypassing verified HTTPS |

No product-contract feasibility gap has been established by this draft. A later
gap must be reported separately and returned to specification, never planned
around by changing observable behavior.

## Technical Questions

### Clarified for narrow architecture verification

- Fixed upstream evidence: immutable controller/model chain recorded above.
- Bounded transport: opt-in only, distinct typed oversize/incomplete failures,
  Ruby invalid-response mapping and unchanged default injection specified.
- Cooldown order independence: stable pre-measurement candidate scheduling and
  deterministic permutation regression specified; cooldown remains scan-local.
- Independent review justified the three module boundaries and found no product
  escalation; seven phases and coherent phase-5 activation remain unchanged.

No unresolved material technical questions remain from the three findings;
these clarifications await independent narrow verification, not self-approval.

### SAFE TO DEFER TO TASK/IMPLEMENTATION

- Final helper/record names, fixture filenames and focused test grouping.
- Exact safe diagnostic wording and phase-to-task decomposition, preserving
  the precedence, offline gates and phase-5 public activation boundary above.

Resolved product questions remain NONE. Next gate: independent narrow
architecture verification of these clarifications.
