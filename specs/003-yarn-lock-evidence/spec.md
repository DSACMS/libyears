# Feature 003: Yarn Classic Lock Evidence

## Status

Approved for technical planning

## Problem

Libyears measures npm dependencies when root `package.json` declarations can
be paired with exact versions from `package-lock.json` v2 or v3. Repositories
using Yarn Classic v1 record exact resolutions in `yarn.lock`, but that
repository-local evidence is not currently accepted. Users must otherwise
provide a different supported evidence source or leave those npm dependencies
unmeasured.

Feature 003 adds Yarn Classic v1 as another exact-version evidence source for
the existing **npm** ecosystem. It does not add an ecosystem.

## Goals

- Measure root npm production dependencies when an unambiguous Yarn Classic v1
  lock entry establishes the exact version.
- Keep `package.json` as the declaration and scope source and preserve original
  declaration text in unmeasurable output.
- Reuse existing npm release metadata, metric, stable-release rules, and
  registry security behavior.
- Fail closed at the narrowest level justified by the evidence.
- Keep scans static, offline-deterministic in tests, and independent of Yarn
  or npm execution.

## Non-Goals

- Yarn Berry/v2+, Yarn workspaces, or Plug'n'Play.
- Recursive child-manifest discovery or workspace aggregation.
- npm/Yarn range or selector resolution.
- Yarn CLI execution, npm CLI execution, package installation, or dependency
  resolution.
- Transitive dependency measurement, `devDependencies`, `peerDependencies`,
  or `optionalDependencies`.
- Private registries or registry authentication.
- A new package ecosystem or new dependency scopes.
- Portfolio scanning, Go, Maven, or SBOM ingestion.

## Scope

The feature applies only when scanning a directory containing a root
`package.json`. That file defines direct npm production dependencies using
the existing Feature 002 rules:

- Include names in `dependencies`.
- Exclude a name also present in `optionalDependencies`.
- Do not include dependencies declared only in development, peer, optional,
  bundled, transitive, or child workspace manifests.
- Preserve existing behavior and reason `unsupported_dependency_source` for
  declarations such as Git, local, workspace, remote-tarball, and npm-alias
  sources.

The only new evidence file is root `yarn.lock`, and the only supported format
is Yarn Classic lockfile v1. A root `package-lock.json` v2/v3 remains supported
with its existing behavior when it is the sole npm lockfile. No change is made
to package-lock v1 or unknown-version handling.

## Evidence Model

`package.json` is declaration and scope evidence. It does not establish a
resolved version by itself.

`yarn.lock` v1 is exact resolved-version evidence. A declared dependency is
measurable from Yarn evidence only if its package identity and declaration
selector correspond to exactly one safely parsed lock entry with one concrete
version. The package name appearing somewhere in the lockfile is insufficient.
Lockfile-only names never become direct dependencies.

Do not evaluate whether a locked version satisfies a range and do not query a
registry to resolve a selector. The lock entry is accepted as the repository's
resolution evidence only through the exact identity-and-selector match defined
below. Preserve the declaration string from `package.json` on every
dependency-level unmeasurable record.

Measured dependencies using Yarn evidence have:

- `ecosystem`: `npm`
- `version_source`: `yarn_lock`
- `version_evidence.npm.format`: `yarn_lock_v1`
- `version_evidence.npm.snapshot_source`: the root-relative source path
  `yarn.lock`

The declaration evidence remains `package.json`. In schema v3, the npm
evidence object adds `format` for Yarn evidence while retaining the existing
`declaration_source` and `snapshot_source` field names. For a missing or
unclassifiable lockfile, `format` is null; `snapshot_source` identifies the
expected root evidence path. When both lock managers conflict, the source error
identifies both paths and no format is selected.

## Yarn Classic v1 Recognition

Recognition is static and does not invoke Yarn. Positive v1 identification
requires the standalone canonical generated-file header line
`# yarn lockfile v1` in the initial comment/header area before lock entries.
Leading blank lines and other leading comments are permitted, but body syntax
alone never establishes v1. The canonical line must not be contradicted by
other generation/header evidence.

- If header/marker evidence explicitly identifies another Yarn generation or
  format, report source-level `unsupported_lockfile_format`.
- If the file cannot be positively identified as v1, including missing or
  contradictory generation/header evidence, report source-level
  `unsupported_lockfile_format`. Do not add a separate unclassifiable reason.
- If canonical evidence positively identifies Yarn Classic v1 but required
  structure cannot be parsed safely, report source-level `invalid_lockfile`.
- An absent `yarn.lock` is not a source-level format error. If no other
  supported lockfile exists, each supported direct declaration remains
  discovered and is unmeasurable with `lock_version_missing`.

A valid v1 file may contain constructs not supported for an individual
declaration. Such a construct does not make the whole file invalid. Apply the
dependency-level rules below; do not label a valid but unsupported construct
`invalid_lockfile`.

## Selector Matching

Matching is textual evidence matching, not semver evaluation. For each
in-scope root manifest dependency, preserve its package identity and original
declaration string, and identify the corresponding selector by combining the
identity and declaration. For example, `lodash` plus `^4.17.0` corresponds to
`lodash@^4.17.0`; `@apollo/client` plus `^3.10.7` corresponds to
`@apollo/client@^3.10.7`.

- Match the complete package identity as written in the manifest. Scoped
  names, including the `@scope/name` form, remain one identity and must not be
  split or reduced to the unscoped portion.
- Compare the package identity and selector with decoded selector strings
  represented by Yarn Classic v1 lock keys. Quoting and escaping are lockfile
  syntax; raw quote characters do not participate in matching.
- A comma-separated/multi-selector key represents multiple selector strings.
  Each decoded selector can independently match a manifest dependency. Multiple
  selectors sharing one lock entry are valid and do not create ambiguity.
- Exact manifest literals match only an identical selector string. The
  corresponding lock entry's version must also equal the manifest literal
  exactly. A different lock version is `declaration_lock_conflict`.
- Ordinary non-exact registry selectors may use the version from an exact
  matching lock selector. No range evaluation or selector normalization is
  performed.
- Do not match by package name alone, by a selector that merely appears
  compatible, or by a transitive entry with another selector.
- If no matching selector exists, use `lock_version_missing`.
- If the same target selector is represented by multiple valid lock entries,
  the evidence is ambiguous even if the entries report the same version. Use
  `ambiguous_lock_evidence`; do not reconcile the entries.
- If duplicate or malformed key structure makes the positively identified v1
  file structurally invalid, use source-level `invalid_lockfile` instead of
  dependency-level ambiguity.
- If one matching entry cannot unambiguously establish a single concrete
  version for that declaration, use `ambiguous_lock_evidence`.

## Evidence Precedence and Conflicts

The evidence-selection rules are:

1. If both root `package-lock.json` and root `yarn.lock` exist, report a
   source-level resolution-evidence conflict with reason
   `conflicting_resolution_sources`. This rule applies regardless of format
   validity, lock versions, or whether the entries happen to agree. Do not
   select, prioritize, parse for precedence, compare, or reconcile either
   lockfile. `package.json` declarations may still be discovered, but neither
   lockfile supplies usable exact-version evidence and no npm registry lookup
   is made from either source.
2. If only a supported package-lock v2/v3 exists, use existing Feature 002
   behavior unchanged.
3. If only `yarn.lock` exists, apply Yarn Classic v1 recognition and matching.
4. If neither lockfile exists, apply existing no-lock behavior: declarations
   are discovered and lack exact evidence with `lock_version_missing`.

The simultaneous-lock condition is a **source-level** error, not a set of
independent dependency failures. With a valid `package.json`, npm discovered
count remains known, while npm measured count and coverage are null. For a
mixed scan, repository discovered count includes all successfully discovered
ecosystems and repository measured count includes successful measurements from
unaffected ecosystems; repository coverage is null. Their successful
measurements and aggregates survive.

Null coverage is deliberate even though the declaration count may be known.
`0/N` would misleadingly report that each dependency independently failed
measurement; the product rejected the npm resolution-evidence source as
ambiguous. Output must identify the source conflict. The lockfiles must not be
accepted merely because observed versions agree.

For a declaration that has both an exact literal and a single matching lock
entry, the lock remains the evidence for the used version and must equal the
literal exactly. Otherwise, use the existing `declaration_lock_conflict`
reason; do not measure either version.

## Failure Model

Stable reason identifiers are:

| Reason | Level | Meaning |
|---|---|---|
| `unsupported_dependency_source` | Dependency | Declaration names an unsupported dependency source or protocol. Reuse Feature 002 semantics. |
| `lock_version_missing` | Dependency | No matching lock evidence exists for a supported declaration, including when no supported lockfile is present. Reuse Feature 002 semantics. |
| `declaration_lock_conflict` | Dependency | Exact manifest literal and its matching lock entry disagree. Reuse Feature 002 semantics. |
| `ambiguous_lock_evidence` | Dependency | Multiple or internally conflicting Yarn entries prevent one exact version from being established. New, ecosystem-independent identifier. |
| `invalid_lockfile` | Source | A recognized Yarn v1 lockfile is structurally malformed or cannot be parsed safely as a whole. Reuse the existing identifier with Yarn-specific source context. |
| `unsupported_lockfile_format` | Source | Yarn generation is clearly unsupported or the file cannot safely be classified as supported v1. New, format-neutral identifier; do not change existing package-lock `unsupported_lockfile_version` behavior. |
| `conflicting_resolution_sources` | Source | Root `package-lock.json` and `yarn.lock` coexist, so npm resolution evidence is rejected. New identifier. |
| `invalid_manifest` | Source | Root `package.json` is invalid. Reuse existing Feature 002 behavior. |

Dependency-level evidence failures do not invalidate other dependencies in
the same npm project. A valid but unsupported dependency protocol is not a
malformed lockfile. Whole-file parse/structure failure and simultaneous lock
sources are source-level failures and do not create synthetic dependency rows.

## Registry Behavior

Yarn changes only how the exact used npm version is established. Once that
version is established, reuse existing npm behavior without Yarn-specific
registry rules:

- Query only the public npm registry over verified HTTPS.
- Reuse existing package/version lookup, publication timestamps, stable
  release eligibility, and registry failure reasons.
- Preserve scoped package registry identity and URL encoding behavior.
- Reuse existing timeout, User-Agent, TLS/CA selection, and diagnostics.
- Do not use the Yarn tarball URL or any lockfile timestamp as a release date.
- A dependency whose used version equals latest stable remains exactly
  `0.0` libyears.
- No lookup occurs for a dependency without one exact version, for a
  dependency-level evidence failure, or when `conflicting_resolution_sources`
  applies.

## Coverage Semantics

Coverage remains measured dependencies divided by discovered dependencies,
except where this specification explicitly assigns null because manifest
discovery failed or a whole resolution source was rejected.

- **Complete Yarn evidence:** count all in-scope declarations; successful
  registry measurements contribute to numerator. Full success yields 100%.
- **Manifest discovery failure:** for an invalid root `package.json`, npm
  discovered and measured counts and npm coverage are null. Repository
  discovery/coverage follows existing Feature 002 behavior.
- **Dependency-level Yarn failures:** retain the declaration in the
  denominator, measure other dependencies normally, and report ordinary
  `measured/discovered` coverage. If all were discovered but none measured,
  coverage is 0.0 when the denominator is nonzero.
- **Missing lock entry/file:** `lock_version_missing` is a dependency-level
  failure; denominator remains known and ordinary coverage applies.
- **Rejected whole resolution source:** for a valid manifest, the declaration
  set is known: npm `dependencies_discovered` is N, while npm
  `dependencies_measured` and `coverage` are null. This applies to malformed
  v1, unsupported/unclassifiable Yarn format, and simultaneous lock sources.
  Do not fabricate per-dependency failure rows. In mixed scans, repository
  discovered count includes known declarations, measured count includes
  successful measurements from unaffected ecosystems, and repository coverage
  is null.
- **Conflicting resolution sources:** declarations remain counted if the
  manifest is valid; apply the rejected-whole-source counts above.
- **Mixed PyPI/Yarn:** repository counts combine known discovered dependencies
  and successful measurements across ecosystems when discovery succeeds.
  Per-ecosystem summaries use each ecosystem's own denominator. A source-level
  failure makes that ecosystem's measured count and coverage null, and
  repository coverage null, while known discovered counts and successful
  measurements from unaffected ecosystems remain available.
- If no dependency is discovered in a successfully discovered scope, coverage
  is null, as in the existing metric.

For a rejected whole source, `null` measured count means no meaningful
dependency measurement result was produced from that source. It is distinct
from `0/N`, which means N dependencies were independently eligible for
measurement and none succeeded. Numeric aggregates include successful
measurements that are available; when there are none, totals are 0.0 and
mean/median/maximum are null. Dependency-level unmeasurables remain excluded
from numeric aggregates, as today.

## Mixed-Ecosystem Behavior

- PyPI-only scans and Python measurement results remain unchanged.
- A package-lock-only npm scan retains Feature 002 behavior and output
  equivalence.
- A Yarn-only npm scan measures supported direct declarations through matched
  Yarn v1 evidence and the existing npm registry.
- A repository may report PyPI plus Yarn-backed npm measurements in one scan.
- A source-level Yarn error does not discard successful PyPI measurements.
  The error is in `source_errors`; failed npm discovery/coverage follows the
  source-level rules above.
- A dependency-level Yarn evidence failure does not discard other measurable
  npm dependencies or PyPI results.
- If both npm lock managers are present, no npm lookup occurs; successful
  PyPI measurements survive, and the evidence conflict remains visible.

## JSON Schema

Keep public JSON at **schema version 3**. No schema version change is required:
existing fields represent npm evidence, dependency-level unmeasurables,
source-level failures, ecosystem summaries, and null coverage. Yarn evidence
adds `format: "yarn_lock_v1"` to `version_evidence.npm`; `snapshot_source`
continues to carry the source path. Existing PyPI and package-lock JSON
representations remain equivalent. Consumers should ignore additive evidence
metadata fields they do not use.

The examples use illustrative package names and registry timestamps. Each shows
the complete relevant schema-v3 shape; unchanged fields are included where
needed to make the compatibility and count semantics clear.

### 1. npm-only Yarn evidence

```json
{
  "schema_version": 3,
  "metric": "libyears",
  "dependency_scope": "direct",
  "ecosystems": ["npm"],
  "version_evidence": {
    "npm": {
      "declaration_source": "package.json",
      "snapshot_source": "yarn.lock",
      "format": "yarn_lock_v1"
    }
  },
  "summary": {
    "dependencies_discovered": 1,
    "dependencies_measured": 1,
    "coverage": 1.0,
    "total_libyears": 0.0,
    "mean_libyears": 0.0,
    "median_libyears": 0.0,
    "max_libyears": 0.0,
    "by_ecosystem": {
      "npm": {
        "dependencies_discovered": 1,
        "dependencies_measured": 1,
        "coverage": 1.0,
        "total_libyears": 0.0,
        "mean_libyears": 0.0,
        "median_libyears": 0.0,
        "max_libyears": 0.0
      }
    }
  },
  "dependencies": [
    {
      "ecosystem": "npm",
      "name": "@example/widget",
      "used_version": "2.4.0",
      "used_release_time": "2025-01-01T00:00:00Z",
      "latest_stable_version": "2.4.0",
      "latest_stable_release_time": "2025-01-01T00:00:00Z",
      "libyears": 0.0,
      "timestamp_anomaly": false,
      "version_source": "yarn_lock"
    }
  ],
  "unmeasurable": [],
  "source_errors": []
}
```

### 2. Mixed PyPI and npm/Yarn evidence

```json
{
  "schema_version": 3,
  "metric": "libyears",
  "dependency_scope": "direct",
  "ecosystems": ["npm", "pypi"],
  "version_evidence": {
    "npm": {
      "declaration_source": "package.json",
      "snapshot_source": "yarn.lock",
      "format": "yarn_lock_v1"
    },
    "pypi": {
      "declaration_source": "requirements.txt",
      "snapshot_source": null
    }
  },
  "summary": {
    "dependencies_discovered": 2,
    "dependencies_measured": 2,
    "coverage": 1.0,
    "total_libyears": 1.0,
    "mean_libyears": 0.5,
    "median_libyears": 0.5,
    "max_libyears": 1.0,
    "by_ecosystem": {
      "npm": {
        "dependencies_discovered": 1,
        "dependencies_measured": 1,
        "coverage": 1.0,
        "total_libyears": 0.0,
        "mean_libyears": 0.0,
        "median_libyears": 0.0,
        "max_libyears": 0.0
      },
      "pypi": {
        "dependencies_discovered": 1,
        "dependencies_measured": 1,
        "coverage": 1.0,
        "total_libyears": 1.0,
        "mean_libyears": 1.0,
        "median_libyears": 1.0,
        "max_libyears": 1.0
      }
    }
  },
  "dependencies": [
    {
      "ecosystem": "npm",
      "name": "widget",
      "used_version": "2.4.0",
      "used_release_time": "2025-01-01T00:00:00Z",
      "latest_stable_version": "2.4.0",
      "latest_stable_release_time": "2025-01-01T00:00:00Z",
      "libyears": 0.0,
      "timestamp_anomaly": false,
      "version_source": "yarn_lock"
    },
    {
      "ecosystem": "pypi",
      "name": "sample",
      "used_version": "1.0.0",
      "used_release_time": "2024-01-01T00:00:00Z",
      "latest_stable_version": "1.1.0",
      "latest_stable_release_time": "2024-12-31T06:00:00Z",
      "libyears": 1.0,
      "timestamp_anomaly": false,
      "version_source": "requirements_exact"
    }
  ],
  "unmeasurable": [],
  "source_errors": []
}
```

### 3. Dependency-level ambiguous Yarn evidence

```json
{
  "schema_version": 3,
  "metric": "libyears",
  "dependency_scope": "direct",
  "ecosystems": ["npm"],
  "version_evidence": {
    "npm": {
      "declaration_source": "package.json",
      "snapshot_source": "yarn.lock",
      "format": "yarn_lock_v1"
    }
  },
  "summary": {
    "dependencies_discovered": 1,
    "dependencies_measured": 0,
    "coverage": 0.0,
    "total_libyears": 0.0,
    "mean_libyears": null,
    "median_libyears": null,
    "max_libyears": null,
    "by_ecosystem": {
      "npm": {
        "dependencies_discovered": 1,
        "dependencies_measured": 0,
        "coverage": 0.0,
        "total_libyears": 0.0,
        "mean_libyears": null,
        "median_libyears": null,
        "max_libyears": null
      }
    }
  },
  "dependencies": [],
  "unmeasurable": [
    {
      "ecosystem": "npm",
      "name": "widget",
      "declared": "^2.0.0",
      "reason": "ambiguous_lock_evidence"
    }
  ],
  "source_errors": []
}
```

The same shape applies to a missing match with reason `lock_version_missing`
or an exact declaration mismatch with reason `declaration_lock_conflict`.

### 4. Conflicting resolution sources in a mixed scan

```json
{
  "schema_version": 3,
  "metric": "libyears",
  "dependency_scope": "direct",
  "ecosystems": ["npm", "pypi"],
  "version_evidence": {
    "npm": {
      "declaration_source": "package.json",
      "snapshot_source": null,
      "format": null
    },
    "pypi": {
      "declaration_source": "requirements.txt",
      "snapshot_source": null
    }
  },
  "summary": {
    "dependencies_discovered": 2,
    "dependencies_measured": 1,
    "coverage": null,
    "total_libyears": 1.0,
    "mean_libyears": 1.0,
    "median_libyears": 1.0,
    "max_libyears": 1.0,
    "by_ecosystem": {
      "npm": {
        "dependencies_discovered": 1,
        "dependencies_measured": null,
        "coverage": null,
        "total_libyears": 0.0,
        "mean_libyears": null,
        "median_libyears": null,
        "max_libyears": null
      },
      "pypi": {
        "dependencies_discovered": 1,
        "dependencies_measured": 1,
        "coverage": 1.0,
        "total_libyears": 1.0,
        "mean_libyears": 1.0,
        "median_libyears": 1.0,
        "max_libyears": 1.0
      }
    }
  },
  "dependencies": [
    {
      "ecosystem": "pypi",
      "name": "sample",
      "used_version": "1.0.0",
      "used_release_time": "2024-01-01T00:00:00Z",
      "latest_stable_version": "1.1.0",
      "latest_stable_release_time": "2024-12-31T06:00:00Z",
      "libyears": 1.0,
      "timestamp_anomaly": false,
      "version_source": "requirements_exact"
    }
  ],
  "unmeasurable": [],
  "source_errors": [
    {
      "ecosystem": "npm",
      "source": "package-lock.json + yarn.lock",
      "reason": "conflicting_resolution_sources"
    }
  ]
}
```

### 5. Malformed Yarn Classic v1 lockfile

```json
{
  "schema_version": 3,
  "metric": "libyears",
  "dependency_scope": "direct",
  "ecosystems": ["npm"],
  "version_evidence": {
    "npm": {
      "declaration_source": "package.json",
      "snapshot_source": "yarn.lock",
      "format": "yarn_lock_v1"
    }
  },
  "summary": {
    "dependencies_discovered": 1,
    "dependencies_measured": null,
    "coverage": null,
    "total_libyears": 0.0,
    "mean_libyears": null,
    "median_libyears": null,
    "max_libyears": null,
    "by_ecosystem": {
      "npm": {
        "dependencies_discovered": 1,
        "dependencies_measured": null,
        "coverage": null,
        "total_libyears": 0.0,
        "mean_libyears": null,
        "median_libyears": null,
        "max_libyears": null
      }
    }
  },
  "dependencies": [],
  "unmeasurable": [],
  "source_errors": [
    {
      "ecosystem": "npm",
      "source": "yarn.lock",
      "reason": "invalid_lockfile"
    }
  ]
}
```

### 6. Unsupported or unclassifiable Yarn format

For a valid one-dependency manifest and a Yarn file without positive v1
identification, the counts match example 5. The metadata and source error are:

```json
{
  "schema_version": 3,
  "metric": "libyears",
  "dependency_scope": "direct",
  "ecosystems": ["npm"],
  "version_evidence": {
    "npm": {
      "declaration_source": "package.json",
      "snapshot_source": "yarn.lock",
      "format": null
    }
  },
  "summary": {
    "dependencies_discovered": 1,
    "dependencies_measured": null,
    "coverage": null,
    "total_libyears": 0.0,
    "mean_libyears": null,
    "median_libyears": null,
    "max_libyears": null,
    "by_ecosystem": {
      "npm": {
        "dependencies_discovered": 1,
        "dependencies_measured": null,
        "coverage": null,
        "total_libyears": 0.0,
        "mean_libyears": null,
        "median_libyears": null,
        "max_libyears": null
      }
    }
  },
  "dependencies": [],
  "unmeasurable": [],
  "source_errors": [
    {
      "ecosystem": "npm",
      "source": "yarn.lock",
      "reason": "unsupported_lockfile_format"
    }
  ]
}
```

## Human Output

Make only the changes needed to expose Yarn evidence and failures:

- For a measured npm dependency, identify `yarn.lock` as its version evidence
  in the existing source/evidence presentation.
- For a dependency-level failure, show the original declaration and a readable
  reason, including missing lock evidence, unsupported source, exact-declaration
  conflict, or ambiguous lock evidence.
- For source-level `invalid_lockfile` or `unsupported_lockfile_format`, name
  `yarn.lock` and explain that npm dependencies could not be measured from that
  evidence source.
- For `unsupported_lockfile_format`, explain whether the observed generation
  is explicitly unsupported or could not be classified safely, when that
  distinction is known.
- For `conflicting_resolution_sources`, name both lockfiles and state that
  neither was used. Show npm null coverage and, in a mixed scan, repository
  null coverage while retaining other ecosystem results.
- Do not imply a lockfile conflict is 0% coverage.

Do not redesign unrelated human output.

## Compatibility

- Existing package-lock v2/v3 scans remain equivalent in results, reasons,
  evidence metadata, and JSON representation.
- Existing PyPI scans and Python metric results remain equivalent.
- Keep schema version 3; add Yarn evidence metadata without changing existing
  package-lock or PyPI fields.
- Do not change libyears arithmetic, timestamp anomaly handling, or stable
  release selection.
- Do not change registry TLS/CA behavior or registry failure semantics.
- Add no runtime dependency.

## Security and Execution Boundaries

- Read only root `package.json`, root `yarn.lock`, and the existing supported
  evidence files needed for the scan.
- Never invoke Yarn, npm, another package manager, a resolver, or repository
  code. Never install packages.
- Do not access private registry configuration or credentials; query only the
  existing public npm registry adapter after exact evidence is established.
- Keep HTTPS certificate and hostname verification enabled under existing
  TLS/CA policy.
- Treat malformed, unsupported, ambiguous, or conflicting evidence as
  unmeasurable/source failure according to the failure level above. Do not
  guess versions or silently reconcile sources.

## Acceptance Criteria

- [ ] **AC-01:** A root `package.json` direct production dependency is measured from root `yarn.lock` only when the lockfile has canonical generated-file header evidence positively identifying Yarn Classic v1; body syntax alone does not identify v1.
- [ ] **AC-02:** An explicitly unsupported generation/format, or missing/contradictory generation evidence, produces source-level `unsupported_lockfile_format` and is never guessed to be v1.
- [ ] **AC-03:** A positively identified Yarn Classic v1 file with malformed required structure, including malformed duplicate-key structure, produces source-level `invalid_lockfile` and no dependency failure rows.
- [ ] **AC-04:** An ordinary unscoped declaration such as `lodash: "^4.17.0"` matches selector text `lodash@^4.17.0` and uses the lock entry's exact version without range evaluation.
- [ ] **AC-05:** A scoped declaration such as `@apollo/client: "^3.10.7"` matches `@apollo/client@^3.10.7` as one complete identity, preserved in JSON, human output, and registry lookup.
- [ ] **AC-06:** Quoted/escaped Yarn keys match on decoded selector strings; quote characters are not part of selector identity.
- [ ] **AC-07:** A comma-separated/multi-selector key can match each represented selector; multiple selectors in one entry are valid and do not create ambiguity.
- [ ] **AC-08:** An exact manifest literal is measurable only when the exact selector matches and the lock version equals the literal.
- [ ] **AC-09:** An exact manifest/lock version mismatch is unmeasurable with `declaration_lock_conflict`, with no registry lookup for that dependency.
- [ ] **AC-10:** A supported non-exact declaration with no matching selector is discovered and unmeasurable with `lock_version_missing`.
- [ ] **AC-11:** A declaration using an unsupported source or protocol is discovered and unmeasurable with `unsupported_dependency_source`; it does not make a valid Yarn file invalid.
- [ ] **AC-12:** The same target selector represented by multiple valid lock entries produces dependency-level `ambiguous_lock_evidence`, even when versions agree, with no registry lookup for that dependency.
- [ ] **AC-13:** An individual missing, unsupported, or ambiguous dependency does not prevent unrelated npm dependencies with usable evidence from being measured.
- [ ] **AC-14:** A missing root `yarn.lock`, when no package-lock exists, leaves supported declarations discovered and uses `lock_version_missing` without a source-level format error.
- [ ] **AC-15:** Root package-lock-only scans retain Feature 002 v2/v3 behavior; package-lock v1 and unknown-version behavior remains unchanged.
- [ ] **AC-16:** If both root lockfiles exist, one npm `source_errors` entry uses `conflicting_resolution_sources`, regardless of content or agreement; neither source is compared, selected, reconciled, or used.
- [ ] **AC-17:** With a valid manifest and any rejected whole resolution source, npm `dependencies_discovered` is N while npm `dependencies_measured` and coverage are null; no synthetic dependency failure rows or npm registry lookups are produced.
- [ ] **AC-18:** For rejected whole-source evidence, `null` measured count is distinct from `0/N`; available successful measurements contribute to numeric aggregates, while no-measurement totals are 0.0 and mean/median/maximum are null.
- [ ] **AC-19:** In a mixed scan with valid manifest, PyPI discovered=4/measured=3 and npm discovered=10/measured=null produce repository discovered=14, measured=3, coverage=null; unaffected ecosystem measurements and aggregates survive.
- [ ] **AC-20:** With dependency-level Yarn failures, npm discovered=N, measured=M, and coverage=M/N; mixed repository coverage uses known discovered declarations and successful measurements normally.
- [ ] **AC-21:** An invalid root manifest has npm discovered, measured, and coverage all null, with repository semantics unchanged from Feature 002.
- [ ] **AC-22:** Only root `package.json` `dependencies` define npm scope; names also in `optionalDependencies` remain excluded, and dev/peer/transitive/child-workspace dependencies are not counted.
- [ ] **AC-23:** Measured Yarn dependencies remain ecosystem `npm`, use `version_source: "yarn_lock"`, and expose `version_evidence.npm.format: "yarn_lock_v1"` and source path `yarn.lock`.
- [ ] **AC-24:** JSON for unsupported/unclassifiable Yarn format records source-level `unsupported_lockfile_format`, npm discovered=N, npm measured=null, coverage=null, and null Yarn format metadata.
- [ ] **AC-25:** JSON for malformed positively identified v1 evidence records source-level `invalid_lockfile` with npm discovered=N, measured=null, and coverage=null.
- [ ] **AC-26:** JSON for simultaneous lockfiles records `conflicting_resolution_sources`, null npm coverage and measured count, known declarations, and null repository coverage in a mixed scan while preserving other ecosystem results.
- [ ] **AC-27:** Dependency-level failures appear in `unmeasurable`; whole-source and manifest failures appear in `source_errors` with stable reason identifiers.
- [ ] **AC-28:** Public JSON remains schema version 3; existing package-lock and PyPI representations remain equivalent.
- [ ] **AC-29:** Human output distinguishes Yarn evidence used, missing, unsupported-source, and ambiguous dependency evidence, malformed supported v1, unsupported/unclassifiable format, and conflicting lock managers; it preserves original declarations and gives readable reasons.
- [ ] **AC-30:** Yarn-backed lookup reuses the existing public npm registry behavior, including timestamps, stable-release eligibility, TLS/CA, timeout, and registry failure semantics; latest-stable equality remains exactly 0.0 libyears.

## Deterministic Verification and Regression Requirements

- Deterministic tests cover selector matching, source failures, dependency-level isolation, mixed ecosystem counts, JSON, and human output using local fixtures and mocked registries only. Tests require no network and invoke no package manager, resolver, installation, or repository code.
- Existing package-lock regression tests and PyPI regression tests remain unchanged and pass; their scan results remain equivalent.

## Release Validation

Before release, scan at least one real local Yarn Classic v1 project with a
root manifest and lockfile. Record the target and environment, discovered and
measured npm counts, coverage, evidence metadata, unmeasurable reasons, and
human/JSON agreement. Do not run Yarn, npm, install dependencies, or execute
project code during the scan. Keep this release validation separate from the
offline deterministic test suite; live registry access is subject to the
existing approval and network policy.

## Open Product Questions

None. Discovery decisions are approved. The stable reason identifiers and
coverage behavior in this draft resolve the remaining discovery clarifications.
