# Feature 003 Reviews

## Discovery Review

**Status:** Direction selected; discovery approval recorded below.

### Initial recommendation

Portfolio scanning of explicitly supplied local roots.

### Human review finding

The initial recommendation was challenged because:

- it does not improve underlying dependency evidence;
- portfolio aggregation introduces unresolved comparability semantics;
- orchestration may belong above the single-project metric.

Human product review did not accept portfolio scanning immediately.

### Requested follow-up

Focused feasibility comparison of Go, Maven, and Yarn using evidence fitness rather than raw repository prevalence.

### Follow-up result

Yarn Classic v1 had the strongest fit with libyears' evidence philosophy: the direct declaration and exact lock version can be read statically, while the existing npm registry adapter supplies release timestamps.

### Product direction

Proceed toward specification for Yarn Classic v1 exact-version evidence for the existing npm ecosystem. This is an additional npm evidence format, not a new ecosystem.

### Alternatives deferred

- **Portfolio scanning:** cross-project aggregation semantics and a concrete user workflow remain unestablished; consider a higher-level orchestration tool later.
- **Go:** observed `go.mod` requirements do not by themselves establish the selected version under Minimal Version Selection; `go.sum` is integrity evidence.
- **Maven:** useful coverage would require substantial effective-model interpretation, and canonical release timestamp semantics remain uncertain.
- **SBOM ingestion:** no actual SBOM artifacts were found in the bounded inventory.

### Remaining uncertainty

- The exact stable identifier for an individual dependency's ambiguous/conflicting Yarn lock evidence may be finalized during specification clarification. This does not block drafting `spec.md`.

## Discovery Approval

**Status:** APPROVED

- Yarn Classic v1 exact-version evidence for the existing npm ecosystem is selected for Feature 003. This is a new npm evidence format, not a new ecosystem.
- If root `package-lock.json` and `yarn.lock` coexist, treat them as a source-level resolution-evidence conflict with reason `conflicting_resolution_sources`. Neither source is used or compared; npm coverage is null, mixed-scan repository coverage is null, successful measurements from other ecosystems survive, and human and JSON output identify the conflict. Null coverage is deliberate because `0/N` would misrepresent source rejection as dependency-level measurement failure.
- Fail at the narrowest level justified by evidence. Individual unsupported or unmatched declarations remain dependency-level unmeasurable (`unsupported_dependency_source` or `lock_version_missing`); ambiguity/conflict for one dependency uses a stable conflict reason to be finalized during specification clarification. A malformed whole Yarn lockfile is source-level `invalid_lockfile`; a valid unsupported construct is not.
- Portfolio scanning, Go, Maven, and SBOM ingestion remain deferred as documented above.
- No remaining product question blocks drafting `spec.md`.

This log preserves the review outcome and decision path, not a transcript. It does not assign individual authorship beyond the documented human product review and commissioned follow-up.

## Specification Clarification Review

**Initial verdict:** REVISE
**Verification outcome:** APPROVE
**Status:** APPROVED

The independent specification review identified six material issues: Yarn
selector matching was underspecified; supported v1, unsupported, and malformed
format boundaries were underspecified; source-level count and coverage
semantics were inconsistent; JSON examples did not fully demonstrate the
schema compatibility boundary; some acceptance criteria described verification
process rather than product behavior; and human diagnostics needed a clearer
unsupported/unclassifiable distinction.

The approved clarifications are:

- Match textual package identity and decoded selector strings. Do not evaluate
  semver, resolve, normalize, repair, or reconcile evidence. Multiple selectors
  in one lock entry are valid; the same target selector in multiple valid
  entries is dependency-level `ambiguous_lock_evidence`. Structurally malformed
  duplicate keys in positively identified v1 evidence produce
  `invalid_lockfile`.
- Positively identify v1 only from the canonical standalone
  `# yarn lockfile v1` generated-file header. Explicitly unsupported, missing,
  or contradictory generation evidence produces
  `unsupported_lockfile_format`. A positively identified v1 file with invalid
  required structure produces `invalid_lockfile`.
- For a valid manifest and rejected whole resolution source, report
  `dependencies_discovered = N`, `dependencies_measured = null`, and
  `coverage = null` for npm. In mixed scans retain known discovered counts and
  successful measurements from unaffected ecosystems, with repository
  coverage null. This distinguishes source rejection from `0/N` dependency
  measurement failure.
- Retain schema v3. Corrected complete relevant examples demonstrate the
  approved counts, additive Yarn evidence metadata, and unchanged PyPI and
  package-lock representations.
- Keep test-process and release-process obligations outside the formal
  behavioral acceptance criteria. Require concise human diagnostics to
  distinguish unsupported from safely unclassifiable format when known.

The narrow verification review confirmed all six findings resolved, schema v3
compatibility, 30/30 clearly testable acceptance criteria, zero ambiguous
criteria, no missing material cases, and a sound contradiction check. Its final
verdict was APPROVE. No product question remains before technical planning.

## Architecture Review

**Initial verdict:** APPROVE WITH CHANGES
**Spec conformance:** PASS
**Architecture-review status:** APPROVED

### Material findings

The review found that source rejection was ambiguously inferred from error
presence; the Yarn parser grammar was insufficiently bounded; npm evidence
selection ownership was not singular; human-only diagnostics should reuse the
existing diagnostics channel; and `metric.py` was listed too eagerly despite
arithmetic remaining unchanged.

### Approved technical decisions

- Carry explicit source-result measurement availability, separate from source
  errors; select architecture approach B.
- Let scan aggregation derive repository and per-ecosystem count and coverage
  availability while preserving successful measurements from unaffected
  ecosystems.
- Use one npm evidence selector, `npm.resolve_npm_evidence(root, discovery)`,
  as the sole owner of root lock-presence inspection and dispatch.
- Keep Yarn parsing focused on bounded Yarn Classic v1 lock-key and entry
  syntax, preserve decoded selector text, and fail closed on malformed or
  unsupported quoting/escaping.
- Carry human-only unsupported/unclassifiable detail through the existing
  report diagnostics channel without changing source-error JSON.
- Isolate metric arithmetic: formulas do not change, summary calculation does
  not learn source semantics, and Yarn does not appear in metric arithmetic.
- Keep `metric.py` unchanged unless a narrowly justified summary-construction
  input is required to represent scan-derived nullable availability without
  duplicating arithmetic.

### Narrow verification outcome

- Findings 1–5 resolved.
- Mixed-summary architecture: SOUND.
- Implementation sequencing: SOUND.
- Readability: PASS.
- Spec conformance: PASS.
- Blocking technical questions: NONE.
- Final verdict: APPROVE.

The architecture is approved, and Feature 003 is ready for task decomposition.
