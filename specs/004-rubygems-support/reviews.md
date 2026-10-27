# Feature 004 Reviews

**Discovery review status:** APPROVED FOR SPECIFICATION

Implementation is not approved. Earlier review statuses below are historical.

## Initial Discovery Review

**Initial draft commit:** df7aee60446795f67da321331f778c3d1457fea7
**Initial recommendation:** no-code workflow validation
**Review verdict:** CONTINUE DISCOVERY

### Material findings

- The sandbox/network result was environment-confounded. The `0/77` result is
  agent-environment evidence, not a demonstrated offline/cache product need.
- Workflow validation was too vague to be Feature 004; it is continued discovery.
- Python exact-evidence compatibility needed bounded testing against existing
  repository-local artifacts and current `--resolved` behavior.
- Broad human research was premature while technical evidence remained cheap
  to investigate.
- Root identification should remain separate from portfolio aggregation.

### Disposition

Continue discovery with the bounded Python evidence-compatibility experiment:
at least two distinct project roots must demonstrate supported non-exact direct
declarations plus already-produced local exact selected-version evidence that
cannot be consumed unchanged by current `--resolved`. No parser or product
capability was approved by this experiment selection.

This record preserves the independent review findings supplied for this
revision, not a reconstructed transcript or a new review of the revised draft.

## Deep Evidence Investigation

The completed read-only investigation is summarized with paths, counts,
limitations, and candidate comparisons in [discovery.md](discovery.md).

- **Python threshold: NOT MET.** Ten metadata-bearing roots represent eight
  conservatively grouped project families. The 28 requirements entries contain
  two copies of the same exact pin and 26 non-exact declarations.
- **No repeated retained Python evidence incompatibility.** The dominant gap
  is absence of retained exact evidence, not incompatibility with `--resolved`.
  One local environment has relevant installed metadata but lacks demonstrated
  project/build attribution; even counting it would not meet the two-root test.
- **Project-root multiplicity demonstrated; user pain not demonstrated.** Build
  and workspace systems encode roots, but no Libyears selection failure or
  recurring user burden was established. Listing is distinct from aggregation.
- **Ruby evidence materially strengthened.** Four DPC application pairs have
  build-consumed locks and strong ordinary declaration/lock alignment. Public
  timestamp metadata appears available; groups, platforms, special entries,
  useful scope, and demand remain unresolved. Evidence fitness is MEDIUM-HIGH;
  demand confidence is LOW-MEDIUM. Neither is implementation approval.
- **Go/JVM: NO MATERIAL EVIDENCE DELTA.**
- **Provenance: NO DEMONSTRATED PROBLEM.**
- **Offline/cache: PLAUSIBLE BUT UNDEMONSTRATED.** Codex sandbox failures are
  excluded from product evidence.

**Status at `67b7d89ca6f1c48bc92dcd128b19bb478a6ba969`:** READY FOR FOCUSED RUBY FEASIBILITY REVIEW

**Feature 004 product direction remains unapproved.** Bounded Ruby evidence
support ranks first for investigation, followed by project-root listing and
Python pyproject declaration discovery. One focused Ruby feasibility/product-
scope review should precede a human Feature 004 decision. No specification,
plan, task graph, Ruby implementation, or definitive feature selection is
approved by this status.

## Git-before-review experiment

The initial discovery was committed before review as `df7aee60446795f67da321331f778c3d1457fea7`
(`df7aee60446795f67da321331f778c3d1457fea7`,
`docs(discovery): draft Feature 004 direction`). That commit is unchanged.
`67b7d89ca6f1c48bc92dcd128b19bb478a6ba969` (`docs(discovery): refine Feature 004 evidence`) preserves the
post-review/deep-evidence state separately: Ruby was the strongest candidate,
but remained unapproved. Git retains exact before/after discovery artifacts
without preserving chat transcripts. The subsequent human decision below is
recorded in a separate change, alongside the normal directory rename to
`specs/004-rubygems-support/`. Neither earlier commit is rewritten.

## Ruby Feasibility Review

This concise record preserves the completed review findings supplied for this
human decision; it does not claim a new independent review or registry lookup.

**Verdict:** RUBY IS READY FOR HUMAN PRODUCT SELECTION

- **Bounded static model:** `Gemfile.lock DEPENDENCIES` -> direct scope;
  lock specs -> exact versions; RubyGems.org -> release metadata.
- Gemfile evaluation is unnecessary for the selected all-direct lock scope.
- Observed strict static evidence retains **238/247 direct occurrences** before
  registry lookup; this is not a registry-backed measurement result.
- The security/no-execution boundary is preservable.
- **Parser complexity:** MEDIUM when bounded.
- **Maintenance burden:** HIGH relative to the small CLI.
- Demand breadth remains limited to one observed project family.
- Production/group interpretation would materially change the proposition.

## Human Product Decision

**Decision:** SELECTED FOR SPECIFICATION

**Feature 004:** Bounded RubyGems lock-snapshot support

The human accepted all-direct lock-snapshot scope, including development/test
dependencies where present; the third-ecosystem maintenance cost; and deferred
interpreted-Gemfile/group/production scope. Gemfile.lock supplies recorded direct
scope and exact selected-version evidence; RubyGems.org is the intended public
release-metadata authority. No Gemfile evaluation, Ruby/Bundler execution, gem
installation, or dependency resolution is authorized. Unsupported or ambiguous
evidence fails closed.

The result describes the committed lock snapshot, not the currently evaluated
Gemfile, production-only scope, an installed environment, or a runtime environment.
The detailed behavioral questions listed in
[discovery.md](discovery.md#human-product-decision) remain for specification.

**Discovery review status:** APPROVED FOR SPECIFICATION

This approves specification work only, not implementation. The next gate is a
Feature 004 specification draft followed by clarification/review; no `spec.md`
is created by this decision record.
