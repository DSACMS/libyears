# Libyears Opportunity Radar

This document preserves evidence-backed future opportunities in the repository.
It is:

- not a release schedule
- not a commitment
- not an issue tracker
- not a replacement for Feature specifications
- intended to make deferred opportunities portable across hosting platforms
  and discoverable by humans and agents

Items may later be projected into GitHub/GitLab issues or project boards for
collaboration, but this repository record remains durable.

## States

### SELECTED

Approved for specification or active SDD work.

### EXPLORE

Evidence justifies a bounded investigation, but the product direction is not
approved.

### WATCH

Plausible opportunity with insufficient evidence or demand to justify active
investigation.

### DEFER

Explicitly considered and deliberately not pursued now.

These states express evidence/confidence, not delivery priority.

## Entry Format

Each opportunity should preserve:

- Opportunity
- State
- Area
- Contributor fit
- Evidence
- Why this state
- Success signal
- Stop condition
- References

An item should not enter the radar merely because someone can imagine it.
An evidence-backed problem or learning opportunity is required.

## Current Radar

| Opportunity | State | Area | Contributor fit |
|---|---|---|---|
| [Project-root discovery/listing](#3-project-root-discoverylisting) | WATCH | CLI / repository discovery | Rotation / product-discovery candidate |
| [Go selected-version support](#4-go-selected-version-support) | WATCH | Go | Advanced evidence investigation |
| [Python pyproject declaration discovery](#5-python-pyproject-declaration-discovery) | WATCH | PyPI | Rotation / bounded discovery task |
| [Portfolio orchestration](#6-portfolio-orchestration) | DEFER | Multi-project workflow | Separate tool / future product exploration |

### 3. Project-root discovery/listing

**State:** WATCH

**Area:** CLI / repository discovery

**Contributor fit:** Rotation / product-discovery candidate

**Opportunity:** List plausible dependency project roots without calculating
cross-project aggregates.

**Evidence:** Feature 004 discovery observed multiple structurally meaningful
roots and build systems that enumerate them.

**Why this state:** Structural opportunity is real, but no recurring libyears
root-selection pain has been demonstrated.

**Success signal:** Evidence shows users repeatedly miss roots or spend meaningful
effort locating them, and a static listing materially reduces that burden.

**Stop condition:** Existing build/workspace metadata or simple external wrappers
already solve the workflow adequately.

**References:**

- [Feature 004 discovery](specs/004-rubygems-support/discovery.md)

### 4. Go selected-version support

**State:** WATCH

**Area:** Go

**Contributor fit:** Advanced evidence investigation

**Opportunity:** Measure direct Go dependencies if authoritative selected-version
evidence can be established statically.

**Evidence:** Go modules are present in the inspected portfolio.

**Why this state:** Repeated discovery has not found repository-local evidence
that safely establishes selected versions under libyears' evidence model.

**Success signal:** A concrete repository workflow exposes retained
selected-version evidence that can be mapped to direct dependencies without
executing Go tooling.

**Stop condition:** Useful evidence continues to require package-manager execution
or dependency selection.

**References:**

- [Feature 003 discovery](specs/003-yarn-lock-evidence/discovery.md)
- [Feature 004 discovery](specs/004-rubygems-support/discovery.md)

### 5. Python pyproject declaration discovery

**State:** WATCH

**Area:** PyPI

**Contributor fit:** Rotation / bounded discovery task

**Opportunity:** Discover direct Python declarations from pyproject.toml where
requirements.txt does not represent the project.

**Evidence:** Feature 004 discovery found one concrete root with modern project
declarations hidden behind an empty requirements file.

**Why this state:** The discovery gap is real, but no selected-version evidence was
found, so the observed case would not currently become measurable.

**Success signal:** Multiple real project roots demonstrate useful direct
declarations plus exact evidence that current declaration discovery prevents
libyears from measuring.

**Stop condition:** Improved declaration discovery does not produce additional
measurable dependencies.

**References:**

- [Feature 004 discovery](specs/004-rubygems-support/discovery.md)

### 6. Portfolio orchestration

**State:** DEFER

**Area:** Multi-project workflow

**Contributor fit:** Separate tool / future product exploration

**Opportunity:** Run dependency-age analysis across multiple project roots.

**Evidence:** Multiple-root repository structures exist.

**Why this state:** Prior discovery found unresolved cross-project aggregation
semantics and a credible case that orchestration belongs above/beside the core
metric.

**Success signal:** A concrete user workflow requires coordinated multi-root
invocation and defines what cross-project results should mean.

**Stop condition:** Simple wrappers/project tooling satisfy the need or
aggregation semantics remain unclear.

**References:**

- [Feature 003 discovery](specs/003-yarn-lock-evidence/discovery.md)
- [Feature 004 discovery](specs/004-rubygems-support/discovery.md)

## Selected Work Moved into SDD

### 1. Bounded RubyGems lock-snapshot support

**Selection state:** SELECTED; moved into Feature 004 under the existing SDD
lifecycle. This is a completion reference, not an active radar opportunity or a
new radar state.

**Area:** RubyGems

**Outcome:** Feature 004 is CONVERGED / COMPLETE through T021. Bounded direct
Gemfile.lock measurement is implemented without Ruby/Bundler execution.
T018 accepted authorized dpc-admin human/JSON evidence (RubyGems 67/69;
repository 77/79); T019 completed independent convergence with 52/52 acceptance
criteria covered and no material findings. T021's canonical retrospective is
complete; the artifact lifecycle is closed.

Gemfile group scope was excluded from Feature 004. The subsequent, separate
human decision below selects bounded static Gemfile group scope as Feature 005.
No release or tag is implied.

**References:**

- [Feature 004 discovery](specs/004-rubygems-support/discovery.md)
- [Feature 004 completion](specs/004-rubygems-support/tasks.md#t020-completion-reconciliation)
- [Independent convergence](specs/004-rubygems-support/reviews.md#t019-independent-convergence)
- [Release validation](specs/004-rubygems-support/release-validation.md)
- [Canonical retrospective](specs/004-rubygems-support/retrospective.md)

### 2. Bounded static Gemfile group scope

**Selection state:** SELECTED; moved into Feature 005 for specification under the
existing SDD lifecycle. Specification is READY to begin; implementation is not
approved by this selection.

**Area:** RubyGems

**Contributor fit:** Feature specification under approved product boundaries

**Opportunity:** Measure dependency age for an explicitly selected set of
statically declared Gemfile groups, using supported declaration evidence
associated with existing supported exact Gemfile.lock evidence.

**Evidence:** Feature 004 established all-direct lock measurement but no group
membership. Feature 005 bounded discovery preserved the scope and evidence
limitations and stopped at HUMAN DECISION REQUIRED in run `005-0001`.

**Why this state:** On 2026-10-29, human product authority deliberately selected
this direction and supplied H1–H3 before recording run `005-0002`. The human
accepts the maintenance/rejection tradeoff of a conservative static subset;
roadmap order and EXPLORE status did not select the feature.

**Success signal:** Useful measurement of explicitly selected declared groups
within supplied declaration/lock evidence, with transparent incompleteness and
failure when unsupported or ambiguous constructs prevent establishment of scope.
Ordinary Ruby scanning preserves all-direct Gemfile.lock behavior unless scoped
behavior is explicitly requested. Group names do not define implicit production
scope or establish deployed, installed, runtime-loaded, or reconstructed Bundler
environment claims. Declaration/lock association alone establishes no historical
coherence. Independent lock/public-source authorization remains mandatory;
private or unauthorized evidence must never use a public namesake.

**Stop condition:** Useful scope requires executing Ruby/Gemfile/gemspec code,
invoking Bundler, installing or resolving dependencies, or silently inferring
complete scope from a partially understood Gemfile.

**References:**

- [Feature 005 discovery and human decision](specs/005-gemfile-group-scope/discovery.md#human-product-decision)
- [Feature 004 discovery](specs/004-rubygems-support/discovery.md)
- [Feature 004 reviews](specs/004-rubygems-support/reviews.md)

## How Opportunities Move

WATCH -> EXPLORE when evidence justifies bounded investigation.

EXPLORE -> SELECTED only after human product approval.

Any state -> DEFER when evidence shows the opportunity should not currently be
pursued.

SELECTED work moves into `specs/NNN-...` for SDD.

Movement should be preserved in Git history with a concise rationale. Items may
remain unchanged for long periods. The radar is deliberately selective.
