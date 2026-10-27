# Feature 003 Technical Plan

## Status

Approved

## Existing Architecture

The current mixed scan is coordinated by `scan.scan_mixed_repository` in
`libyears/scan.py`:

1. `_python_source_result` discovers Python declarations and applies the
   optional `--resolved` snapshot through the existing snapshot and constraint
   code.
2. `_npm_source_result` calls `npm.discover_manifest`, then
   `npm.resolve_lockfile` for a root `package-lock.json`.
3. The coordinator pairs those two `SourceResult` values with their registry
   lookups, iterates candidates, turns successful registry results into
   `Dependency` objects, and retains registry failures as dependency-level
   unmeasurables.
4. `metric.measure_dependency` computes the existing arithmetic. The
   coordinator calls `metric.calculate_summary` for repository and
   per-ecosystem summaries.
5. `output.report_to_dict` in `libyears/output.py` serializes schema v3;
   `_format_mixed_human` formats mixed reports and `_reason_text` maps reason
   identifiers to readable text.

`npm.discover_manifest` reads only the root `package.json`, applies the
Feature 002 direct-production and optional-dependency rules, and records
unsupported dependency sources. `npm.resolve_lockfile` reads package-lock v2/v3
and calls the existing path-keyed v2/v3 resolution functions. Those functions
preserve an exact manifest/lock conflict check and produce `NpmDeclaration`
records with either `used_version` or a dependency reason. Existing package-lock
parse/entry failures currently become dependency-level `invalid_lockfile`
rows; Feature 003 must preserve that behavior for package-lock-only scans.

`DependencyCandidate`, `UnmeasurableDependency`, `SourceError`,
`SourceEvidence`, `SourceResult`, `Dependency`, and `MetricSummary` live in
`libyears/model.py`. A candidate already carries `version_source`; a measured
`Dependency` carries it into output. `SourceResult.dependencies_discovered`
currently derives a count from candidates and unmeasurables, but returns null
for every source error. `MetricSummary` already allows nullable discovered,
measured, coverage, and aggregate fields. `calculate_summary` derives measured
count from measurement rows; its `discovery_failed` option returns all summary
fields null.

The existing `NpmAdapter` in `libyears/npm.py` owns npm package metadata lookup
and delegates HTTPS, TLS/CA selection, timeout, User-Agent, and transport
diagnostics to `registry.VerifiedJSONTransport`. It selects release timestamps,
stable candidates, timestamp ties, and registry failure reasons. Feature 003
should pass its exact Yarn-backed version to this adapter without changing it.

For output, `_report_parts` constructs ecosystem-keyed evidence. It currently
emits only `declaration_source` and `snapshot_source`; `report_to_dict` fixes the
schema version at 3 and serializes source errors as `ecosystem`, `source`, and
`reason`. Human output prints candidate `version_source` in the mixed table,
but the one-ecosystem npm branch omits the source column. Source errors are
shown in mixed output using `_reason_text` and the source path.

Concrete code to reuse includes `discover_manifest`, `_unsupported_source`,
`_is_exact_version`, `resolve_lockfile`, `resolve_v2_lockfile`,
`resolve_v3_lockfile`, `NpmAdapter`, `DependencyCandidate`,
`UnmeasurableDependency`, `SourceError`, `SourceEvidence`, `SourceResult`,
`measure_dependency`, `calculate_summary`, `scan_mixed_repository`,
`report_to_dict`, `_format_mixed_human`, and `_reason_text`.

## Proposed Architecture

Keep one npm declaration discovery path and add a concrete Yarn v1 evidence
parser in a new `libyears/yarn.py`. Keep npm registry behavior in `npm.py`.
`npm.resolve_npm_evidence(root, discovery)` is the sole owner of npm evidence
selection; it checks root lockfile presence once and dispatches to the
appropriate existing or Yarn-specific resolver. The flow is:

```text
root package.json discovery
        ↓
explicit npm resolution-source selection
        ├── sole package-lock.json → existing resolver, unchanged
        ├── sole yarn.lock → focused Yarn v1 parser and textual matcher
        ├── both → source-level conflict
        └── neither → existing missing-evidence behavior
        ↓
DependencyCandidate / UnmeasurableDependency / SourceError
        ↓
existing NpmAdapter → existing metric and report pipeline
```

Do not add a registry, package-manager, parser-plugin, or generic lockfile
framework. Keep the `NpmAdapter` and verified transport unchanged. Use the
existing shared model types, adding only the source state and evidence metadata
needed to represent the approved counts and Yarn format.

## Evidence Source Selection

Keep `discover_manifest` separate from evidence selection. After successful
manifest discovery, `npm.resolve_npm_evidence(root, discovery)` checks the
presence of root `package-lock.json` and `yarn.lock` exactly once, before
reading either file:

- If both root files exist, produce one npm `SourceError` with
  `conflicting_resolution_sources`; do not parse either file, choose precedence,
  compare versions, make npm registry calls, or emit per-dependency rows.
- If only `package-lock.json` exists, call the existing `resolve_lockfile`
  path. Do not alter its v2/v3 selection or current unsupported-version and
  dependency failure behavior.
- If only `yarn.lock` exists, use the Yarn v1 recognition/parser/matcher.
- If neither exists, retain the package-lock resolver's current no-lock result:
  each supported declaration is discovered with `lock_version_missing`.
- If `package.json` discovery fails, stop before inspecting resolution sources
  and preserve `invalid_manifest` source handling.

This selection belongs in the npm source path, not in generic scan dispatch:
`package.json` always defines npm scope, and no other ecosystem chooses
between npm lock managers. `scan.py` must not repeat lock-presence checks.
`_python_source_result` and `--resolved` remain Python-specific and unchanged.

Use root paths only. In the both-present case, return the source conflict
without opening either lockfile. A lockfile without a root manifest does not
create npm scope, matching the existing root manifest behavior.

## Yarn Classic v1 Parser

Place the parser in `libyears/yarn.py`, separate from `npm.py`. `npm.py` is
already responsible for manifest interpretation, the package-lock resolver,
and the npm registry adapter; a focused module keeps the new lock syntax
isolated without introducing a generic framework.

Expose one narrow operation that accepts the root `yarn.lock` path and returns
ordered lock entries or a typed recognition/parse failure. Each valid entry
needs only:

- its decoded selector strings as an ordered tuple;
- its exact `version` field value;
- enough entry identity to retain separate entries and detect repeated
  selectors.

Recognition requires the canonical standalone `# yarn lockfile v1` line in
the initial comment/header area. Leading blank lines and comments are allowed;
the header must precede entries and must not be contradicted by generation or
format markers in that header area. A file without positive identification,
including contradictory generation markers or an explicitly different
Yarn-format marker, returns `unsupported_lockfile_format`. Do not infer a
version from the body. Once the canonical v1 header is established, failures
to parse required entry/key structure return `invalid_lockfile`.

Implement only the lock-key and entry structure needed by the approved
contract. A key is one or more selector strings separated by commas outside
quoted strings. Each selector is either an ordinary unquoted selector (a
nonempty sequence excluding commas, quotes, line breaks, and lock syntax
delimiters) or a double-quoted selector. Preserve decoded selector text
exactly; do not trim or otherwise normalize its content. Quoted selectors may
contain commas. The bounded quoted-string escape set is `\\` for a literal
backslash and `\"` for a literal double quote; reject every other escape
form rather than silently interpreting or normalizing it. This covers the
quote and backslash characters needed inside selector text while keeping the
parser from becoming a general string or YAML decoder. If implementation
fixtures establish that valid Yarn Classic v1 keys require another escape,
consult authoritative Yarn v1 syntax, document that reference in the parser
tests or code comment, and add the case explicitly before accepting it.

The key parser must consume the complete key line, enforce separators and
entry indentation, and reject empty members, dangling escapes, unterminated
quotes, trailing garbage, or ambiguous delimiters. Read one concrete `version`
field per entry and require its value to be a single usable exact version
before producing evidence. Preserve entries in a sequence rather than
collapsing them into a dictionary so distinct valid candidates remain visible.
Other v1 metadata fields are not evidence for this feature; recognize their
entry boundaries and safely ignore their values. Do not interpret tarball
URLs, integrity fields, dependency subtrees, or timestamps as version
evidence. Do not add a YAML dependency or parse the entire file as general
YAML. Malformed required structure in positively identified v1 is whole-file
`invalid_lockfile`; a repeated target selector in separate otherwise valid
entries remains visible to matching and becomes dependency-level ambiguity,
even when versions agree.

Validate a usable resolved version with npm's existing exact-version rule
(`_EXACT_VERSION` / `_is_exact_version`) at the npm evidence boundary. A
matching entry with no single usable exact version is
`ambiguous_lock_evidence`; no semver range matching is involved.

## Selector Representation and Matching

The matcher receives each manifest declaration's unchanged `name` and
`declared` text. Construct the target selector text as `name + "@" + declared`:

- `lodash` and `^4.17.0` becomes `lodash@^4.17.0`.
- `@apollo/client` and `^3.10.7` becomes `@apollo/client@^3.10.7`.

Compare that target with the parser's decoded selector strings using exact
text equality. Yarn quote and escape syntax is consumed by the parser and is
not comparison text. A multi-selector entry exposes each decoded selector
separately and all its selectors point to the same entry/version. No npm
semver evaluation, selector normalization, compatibility test, or registry
resolution occurs.

Keep a selector-to-entry-list index (or equivalent direct scan over the small
entry sequence) without discarding duplicate candidates:

- zero matching entries → `lock_version_missing`;
- one matching entry with one exact version → candidate with
  `version_source="yarn_lock"`;
- one exact manifest literal whose locked version differs →
  `declaration_lock_conflict`;
- multiple matching valid entries, including equal version strings →
  `ambiguous_lock_evidence`;
- one matching entry without one usable exact version →
  `ambiguous_lock_evidence`.

Multiple selector strings in one entry are valid; ambiguity counts entries
matching the specific target selector, not the total selectors in that entry.
The parser rejects malformed duplicate structure before matching. Thus the
matcher interprets committed evidence and never repairs, normalizes,
reconciles, or resolves it.

Unsupported manifest sources retain `unsupported_dependency_source` from
`discover_manifest` and do not reach registry lookup. Preserve the original
manifest declaration in every dependency-level unmeasurable record.

## Failure Model

| Reason | Level and detection point | Continue / registry lookup | Count and coverage consequence |
|---|---|---|---|
| `unsupported_dependency_source` | Dependency; existing root manifest source check | Continue other dependencies; no lookup for this declaration | Counts in N; ordinary M/N coverage |
| `lock_version_missing` | Dependency; no lock file or no textual selector match | Continue; no lookup for this declaration | Counts in N; ordinary M/N coverage |
| `declaration_lock_conflict` | Dependency; exact manifest literal differs from its one matching lock version | Continue; no lookup for this declaration | Counts in N; ordinary M/N coverage |
| `ambiguous_lock_evidence` | Dependency; multiple valid matching entries or one matching entry lacks one usable exact version | Continue; no lookup for this declaration | Counts in N; ordinary M/N coverage |
| `invalid_lockfile` | Source for positively identified Yarn v1; parser cannot safely parse required structure | Preserve other ecosystems; no npm candidate lookup and no synthetic dependency rows | Valid manifest gives npm discovered=N, measured=null, coverage=null; mixed repository retains known counts/successes and null coverage. Package-lock-only behavior remains its existing dependency-level behavior. |
| `unsupported_lockfile_format` | Source; generation is explicitly unsupported or file is unclassifiable/contradictory | Preserve other ecosystems; no npm candidate lookup or rows | Same rejected-whole-source count semantics as above |
| `conflicting_resolution_sources` | Source; both root lockfiles exist, before either is read | Preserve other ecosystems; no npm lookup or per-dependency rows | Same known N / null npm measured / null npm coverage semantics; mixed repository coverage null |
| `invalid_manifest` | Source; existing `discover_manifest` parse/shape check | Stop npm discovery; preserve other ecosystems; no npm lookup | npm discovered, measured, coverage null; repository discovery/coverage follows existing Feature 002 behavior |

A package-lock v2/v3 scan keeps its current reason classification and output.
The `invalid_lockfile` level is intentionally evidence-path-specific: a
positively identified malformed Yarn v1 file is source-level per Feature 003;
existing package-lock failures remain as currently tested.

## Count and Coverage Representation

`MetricSummary` already permits nullable counts and coverage. Represent source
availability explicitly in `SourceResult`, not by inferring it from
`source_errors`:

- discovery unavailable: `dependencies_discovered=None`,
  `measurement_available=False` (for example, `invalid_manifest`);
- discovery known but its whole resolution source was rejected:
  `dependencies_discovered=N`, `measurement_available=False`;
- dependency measurement available: `dependencies_discovered=N`,
  `measurement_available=True`, with candidate and dependency-level
  unmeasurable rows accounting for the discovered declarations.

`SourceResult` also retains its applicable candidates/result rows, source
errors, and existing diagnostic information. Keep these fields explicit and
small; do not introduce a generic state machine. A rejected source has no
synthetic per-dependency rows. A registry failure for one candidate remains a
dependency-level result and does not change source availability.

`scan_mixed_repository` owns derivation of repository and per-ecosystem
availability. It sums known discovered counts unless any detected source has
unknown discovery. A whole-source rejection makes that ecosystem's measured
count and coverage null. At repository level, successful rows from available
sources remain measured and contribute to total, mean, median, and maximum;
coverage is null if any detected source was rejected or discovery is unknown.
If the only detected ecosystem is rejected, its measured count is null. For
example, PyPI discovered 4/measured 3 and npm discovered 10/rejected yields
repository discovered 14, measured 3, coverage null, with numeric aggregates
computed from the three PyPI rows.

`calculate_summary` remains unaware of Yarn, parsing, source errors, and
lockfile semantics. It continues to calculate numeric values from measurable
rows. If clean construction from scan-derived availability requires a narrow
summary input, it may accept already-derived nullable `dependencies_measured`
and coverage availability; it must not infer either from source errors.
Prefer leaving `metric.py` unchanged if scan aggregation can construct the
summary without duplicating arithmetic. Do not calculate a normal summary and
patch fields in output code. No formulas change, and Yarn never appears in
metric arithmetic. Add focused regression coverage for all three states,
including mixed successful PyPI aggregates, before source integration relies
on this representation.

## Schema v3 and Evidence Metadata

Keep schema version 3. Yarn remains ecosystem `npm`; each Yarn-backed
`DependencyCandidate` uses `version_source="yarn_lock"`, which already flows
through `Dependency.version_source` to each measured JSON dependency.

Extend internal `SourceEvidence` with Yarn format metadata. `_report_parts`
should emit `format: "yarn_lock_v1"` for positively identified Yarn evidence,
`format: null` for an unsupported/unclassifiable Yarn source, and the approved
null format for a simultaneous-lock conflict. It should omit the new `format`
key for existing package-lock and PyPI evidence, preserving their serialized
representations. Keep `snapshot_source` as `yarn.lock` when Yarn is the selected
or rejected sole source; the simultaneous-source error identifies both paths
and leaves no source selected.

Serialize `SourceError` with its existing public `ecosystem`, `source`, and
`reason` fields only. If a small internal diagnostic is needed so human output
can say “unsupported generation” versus “could not classify” when known, keep
it out of the JSON object and do not change stable source-error shape. Do not
add a schema version, new ecosystem, or evidence record for lock-only
transitive dependencies.

## Registry Reuse

The Yarn matcher produces the same `DependencyCandidate` contract used by
package-lock: ecosystem `npm`, registry identity equal to the unchanged package
name, exact used version, original declaration, and version source. The scan
coordinator then calls the existing `NpmAdapter.lookup(name, used_version)`.
Do not alter `NpmAdapter`, `registry.VerifiedJSONTransport`, or their URL,
publication-time, stable-candidate, tie-break, prerelease, TLS, timeout,
User-Agent, CA, or failure behavior.

Existing `tests/test_npm_registry.py` already covers public registry URLs,
scoped-name URL encoding, publication timestamps, stable selection, tie rules,
prerelease behavior, TLS verification, CA bundles, timeout, User-Agent, and
transport/metadata failures. New mixed-scan tests should prove that a Yarn
candidate calls this existing lookup boundary with the exact name and locked
version. Preserve the metric test that latest-stable equality yields exactly
0.0.

## Human Output

Make only focused changes in `output.py`:

- Map `yarn_lock` to a readable `yarn.lock` evidence label and show it for
  successful Yarn measurements, including an npm-only report where the
  existing one-ecosystem branch currently omits a source column.
- Add readable reason text for missing Yarn evidence, ambiguous evidence, and
  conflicting resolution sources. For source-level errors, show the source
  path and explain malformed supported v1 versus unsupported/unclassifiable
  format; include parser context in the human diagnostic only when known.
- For simultaneous locks, name both paths and say neither supplied evidence;
  display null npm and repository coverage as required.

Do not redesign table layout, summaries, verbosity, or unrelated Python/npm
output.

## Testing Strategy

All deterministic coverage uses local fixtures and mocked registry calls; it
requires no network and runs no Yarn, npm, resolver, installer, or repository
code.

- **Parser:** canonical v1 header; leading comments; unsupported and missing or
  contradictory generation markers; malformed positively identified v1;
  quoted and unquoted selectors; escaped/quoted keys; scoped identities;
  comma-separated keys; one entry with several selectors; repeated target
  selector across valid entries; malformed duplicate key/field structure.
- **Evidence matching:** exact textual match; non-exact textual selector
  without range evaluation; zero match; exact declaration conflict; repeated
  entries with equal versions; missing/unusable entry version; unsupported
  declaration source; dependency-level failure isolation.
- **Source selection:** package-lock only for v2/v3, Yarn only, both regardless
  of contents, neither, malformed Yarn, unsupported/unclassifiable Yarn, and
  invalid manifest. Assert conflict short-circuits before either lockfile is
  parsed and makes no npm registry call.
- **Counts and coverage:** invalid manifest; valid manifest with rejected
  whole-source N/null/null; ordinary dependency-level M/N; mixed PyPI success
  with rejected npm evidence, preserving known discoveries and measurements
  while repository coverage is null.
- **Output:** Yarn `version_source`, conditional `format` metadata, stable
  source-error JSON shape, all new human diagnostics, and unchanged existing
  package-lock/PyPI JSON fields.
- **Regression:** retain package-lock v2/v3, PyPI, and Python `--resolved`
  tests. Reuse the existing npm registry suite for registry/TLS/CA behavior;
  add a boundary test proving Yarn invokes that adapter. Run the full
  deterministic unittest suite at the integration boundary. Live network tests
  are not correctness tests.

## Release Validation

Use one of the already observed Yarn Classic repositories from discovery after
confirming by static inspection that its root manifest and root lockfile form a
suitable isolated project. Do not select a target in this plan. The scan is
read-only and must not run Yarn/npm, install dependencies, resolve packages,
or execute project code. Compare human and JSON output and record target,
environment, discovered/measured counts, coverage, evidence metadata, reasons,
and any discrepancies. Optional live public npm registry validation is
separate from deterministic tests and remains subject to the existing network
policy.

## Expected File Changes

| File | Why |
|---|---|
| `libyears/yarn.py` | New focused static Yarn Classic v1 header, key, and entry parser. |
| `libyears/npm.py` | Select npm evidence source, adapt Yarn entries to existing npm declarations/candidates, and keep package-lock resolver behavior intact. |
| `libyears/model.py` | Carry explicit known discovery count/source rejection state and internal Yarn evidence/diagnostic metadata. |
| `libyears/metric.py` | Probably unchanged. Modify only if a narrowly justified summary-construction input is necessary to represent scan-derived nullable measured/coverage availability without duplicating arithmetic; formulas and source-agnostic behavior remain unchanged. |
| `libyears/scan.py` | Wire npm selection, source failures, registry candidates, and mixed source count/coverage aggregation. |
| `libyears/output.py` | Conditionally serialize Yarn format metadata and render the minimum Yarn evidence/failure diagnostics. |
| `tests/test_yarn.py` | Add offline tests for the focused parser contract. |
| `tests/test_npm.py` | Cover npm evidence selection and retain package-lock resolver compatibility assertions. |
| `tests/test_metric.py` | Cover explicit nullable-measured and coverage-unavailable summary states. |
| `tests/test_mixed_scan.py` | Cover source selection, candidate-to-registry reuse, mixed counts, isolation, and regression behavior. |
| `tests/test_output.py` | Cover conditional Yarn metadata, source errors, human messages, and unchanged package-lock/PyPI representations. |
| `README.md` | Document Yarn Classic v1 as npm version evidence and its static/no-install behavior at the feature documentation checkpoint. |

`registry.py`, `pypi.py`, `requirements.py`, `constraints.py`, `snapshot.py`,
`cli.py`, and `libyears/metric.py`'s arithmetic need no redesign. Existing
`tests/test_npm_registry.py` should remain unchanged because the registry
adapter is reused; its current tests provide the relevant registry/TLS/CA
regression evidence. Do not change `SPEC.md`, `AGENTS.md`, or `CHANGELOG.md` as
part of the implementation tasks unless a separately approved documentation or
release checkpoint calls for them.

## Implementation Phases

1. **Yarn v1 parser:** Add `yarn.py` and parser fixtures/tests for recognition,
   bounded keys/escapes, entry structure, and exact version fields. Keep the
   module independent of matching, scan orchestration, and registry access.
2. **Textual selector evidence:** Add matching from decoded selector strings
   to declarations and tests for exact identity, scoped names, multi-selector
   entries, repeated entries, missing evidence, declaration conflict, and
   ambiguity. No semver or package-spec parsing.
3. **Explicit source-result availability:** Add the three source states above
   and focused tests for invalid manifest, rejected whole source, and ordinary
   dependency-level partial measurement. Cover mixed PyPI success plus rejected
   npm evidence and preservation of successful numeric aggregates.
4. **Single npm evidence selector:** Implement
   `npm.resolve_npm_evidence(root, discovery)` as sole owner of one-time root
   lock-presence inspection. Test package-lock-only dispatch against existing
   v2/v3 behavior, including the existing npm/package-lock regression tests.
5. **Yarn integration through the selector:** Wire Yarn parser/matcher behind
   that selector; cover both-present short-circuit, Yarn-only, neither,
   malformed/unsupported sources, invalid manifest, registry lookup boundary,
   and source versus dependency failures.
6. **Summary/output/schema integration:** Derive repository and ecosystem
   availability in scan aggregation; add schema-v3 metadata and human output.
   Test mixed counts, null coverage, retained successful aggregates, stable
   source-error JSON shape, and unchanged PyPI/package-lock representations.
7. **Deterministic end-to-end regression:** Gate shared summary behavior with
   `test_metric.py` where applicable, `test_mixed_scan.py`, `test_scan.py`, and
   `test_npm.py`; also retain PyPI, snapshot, npm registry, TLS/CA, and output
   regressions. Run the full deterministic suite and `git diff --check`.
8. **Dogfood, optional live validation, and convergence:** After deterministic
   correctness, perform the read-only repository check. Keep optional live
   registry validation separate. Complete a read-only review against the
   approved spec, plan, implementation, tests, and documentation. Each phase
   must leave the repository coherent and valid.

Each implementation task should leave the repository in a coherent state;
parser behavior is independently testable before orchestration, and each
following phase adds one connected behavior plus focused regression coverage.

## Architecture Risks

| Risk | Containment |
|---|---|
| Selector matching drifts into semver or source resolution | Compare only `package + "@" + original declaration` with decoded selector text; no range library or registry lookup before an exact match. |
| Parser grows into a general Yarn/YAML implementation or misdecodes a selector | Keep one v1-only module with the bounded quoted/unquoted key grammar above; reject unsupported escapes, delimiters, and unsafe structure. |
| Malformed v1 and unsupported formats overlap | Require the canonical header first; without positive v1 identification return `unsupported_lockfile_format`, and only then classify structural failures as `invalid_lockfile`. |
| Null count state is collapsed into zero or inferred from an error | Store nullable discovery count and explicit measurement availability on `SourceResult`; derive aggregate availability in scan code and test npm N/null/null plus retained mixed rows. |
| Lock selection is duplicated or package-lock behavior regresses | Make `npm.resolve_npm_evidence` the sole selector; keep package-lock-only dispatch to the existing resolver and gate it with existing package-lock tests. |
| Metric formulas become coupled to evidence sources | Keep `calculate_summary` source-agnostic and preserve formulas; pass only already-derived nullable summary availability if a narrow interface change is necessary. |
| Human diagnostics change stable JSON | Carry optional format detail through the existing report diagnostics channel associated with source/path; do not add `SourceError` fields or serialize parser exceptions. |
| Workspace/monorepo evidence enters scope | Read only root `package.json` and root lockfiles; never recurse, inspect workspace child manifests, or use PnP metadata. |

## Technical Decisions

- **Human-only format diagnostics — resolved:** Use the existing report
  diagnostics channel, associated with the Yarn source path. When known, human
  output can distinguish an explicitly unsupported generation from a source
  that could not be safely classified. Keep `SourceError.reason` stable as
  `unsupported_lockfile_format`; do not serialize raw parser exceptions or
  change the JSON source-error shape.
- **Summary availability — resolved:** Select approach B. `SourceResult`
  carries explicit discovery and measurement availability; scan aggregation
  derives nullable repository and ecosystem counts/coverage. Do not infer
  rejection from source-error presence or mutate summaries in output code.
- **Bounded quote/escape handling — resolved:** Accept the specified ordinary
  unquoted selectors and double-quoted selectors with only `\\` and `\"`
  escapes; preserve decoded text exactly and reject malformed/unsupported
  forms as `invalid_lockfile` after positive v1 identification. If authoritative
  Yarn v1 syntax shows another escape is required for a valid key, record that
  source in an implementation comment/test and explicitly add its fixture
  before accepting it. This is implementation evidence, not a product decision.

No unresolved product question remains. The plan is ready for narrow
verification review.
