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
| [Bounded RubyGems lock-snapshot support](#1-bounded-rubygems-lock-snapshot-support) | SELECTED | RubyGems | Feature implementation after approved SDD |
| [Interpreted Gemfile group/production scope](#2-interpreted-gemfile-groupproduction-scope) | EXPLORE | RubyGems | Advanced rotation / research task |
| [Project-root discovery/listing](#3-project-root-discoverylisting) | WATCH | CLI / repository discovery | Rotation / product-discovery candidate |
| [Go selected-version support](#4-go-selected-version-support) | WATCH | Go | Advanced evidence investigation |
| [Python pyproject declaration discovery](#5-python-pyproject-declaration-discovery) | WATCH | PyPI | Rotation / bounded discovery task |
| [Portfolio orchestration](#6-portfolio-orchestration) | DEFER | Multi-project workflow | Separate tool / future product exploration |

### 1. Bounded RubyGems lock-snapshot support

**State:** SELECTED

**Area:** RubyGems

**Contributor fit:** Feature implementation after approved SDD

**Opportunity:** Measure direct RubyGems dependencies from committed Gemfile.lock
evidence without executing Ruby or Bundler.

**Evidence:** Feature 004 discovery and feasibility review.

**Why this state:** Human product decision selected it for specification.
Implementation is not approved.

**Success signal:** A conservative static contract can measure useful direct lock
evidence while failing closed on ambiguous/unsupported cases.

**Stop condition:** Specification demonstrates that useful behavior requires
Gemfile evaluation, dependency resolution, or unsafe platform/source inference.

**References:**

- [Feature 004 discovery](specs/004-rubygems-support/discovery.md)
- [Feature 004 reviews](specs/004-rubygems-support/reviews.md)

### 2. Interpreted Gemfile group/production scope

**State:** EXPLORE

**Area:** RubyGems

**Contributor fit:** Advanced rotation / research task

**Opportunity:** Investigate whether a safe bounded subset of Gemfile declarations
can recover group/production dependency scope.

**Evidence:** Feature 004 feasibility found that Gemfile.lock preserves direct
scope but not group membership; observed applications contain substantial
development/test dependencies.

**Why this state:** Potentially valuable, but Gemfiles are Ruby programs and
interpretation could violate libyears' static/no-execution philosophy. This is
future exploration; interpreted scope is explicitly deferred from Feature 004.

**Success signal:** A deliberately bounded static model recovers useful scope
without executing Ruby, running Bundler, resolving dependencies, or silently
accepting unsupported constructs.

**Stop condition:** Useful coverage requires general Ruby evaluation or
package-manager execution.

**References:**

- [Feature 004 discovery](specs/004-rubygems-support/discovery.md)
- [Feature 004 reviews](specs/004-rubygems-support/reviews.md)

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

## How Opportunities Move

WATCH -> EXPLORE when evidence justifies bounded investigation.

EXPLORE -> SELECTED only after human product approval.

Any state -> DEFER when evidence shows the opportunity should not currently be
pursued.

SELECTED work moves into `specs/NNN-...` for SDD.

Movement should be preserved in Git history with a concise rationale. Items may
remain unchanged for long periods. The radar is deliberately selective.
