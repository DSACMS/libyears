# Feature 005 Discovery: Bounded Static Gemfile Group Scope

**Current status: SELECTED FOR SPECIFICATION. Specification readiness: YES.**

The subsequent [human product decision](#human-product-decision) resolves H1–H3.
The original discovery record below preserves run `005-0001`'s Product Direction
Pending finding and HUMAN DECISION REQUIRED conclusion as historical evidence.

## Historical discovery status — 005-0001

**Status: HUMAN DECISION REQUIRED. Specification readiness: NO.**

Bounded discovery is complete. Current durable authority does not select a
product capability as Feature 005. Interpreted Gemfile group/production scope
is an authorized investigation opportunity, not an approved feature.
`005-discovery` is a neutral holding directory, not a selected product slug;
rename it normally when a human selects the direction. No specification,
implementation plan, or task graph is begun by this record.

Evidence baseline: repository commit
`d7262534fadf5834490f6d66e48f8053df7a68ef`; discovery date 2026-10-29.

## Feature / problem statement and roadmap authority

**F1 — Feature 005 identity remains unselected.**
[ROADMAP.md](../../ROADMAP.md), “States,” “Current Radar,” and “How Opportunities
Move,” distinguish investigation from product approval. States express evidence
and confidence, not delivery priority. EXPLORE becomes SELECTED only through
human product approval. The only SELECTED reference is completed Feature 004.

| Opportunity | State | Evidence and remaining question |
|---|---|---|
| Interpreted Gemfile group/production scope | EXPLORE | Development/test declarations occur in the historical Ruby sample; useful static scope and the intended user outcome remain unestablished. |
| Project-root discovery/listing | WATCH | Build/workspace metadata identifies multiple roots; recurring missed-root or costly-selection workflows have not been demonstrated. Existing metadata or wrappers may suffice. |
| Go selected-version support | WATCH | Prior discovery found module/sum files without the retained selected-version evidence it sought; no new qualifying workflow was established here. |
| Python pyproject declaration discovery | WATCH | One historical root had four declarations hidden behind an empty requirements file, without retained exact versions. More discovered declarations need not yield more measurements. |
| Portfolio orchestration | DEFER | Multiple roots do not settle cross-project aggregation semantics or whether orchestration belongs in this CLI. |

The Gemfile opportunity is the clearest next **bounded investigation** under
current radar authority. It cannot automatically become Feature 005. Its problem
hypothesis is that users need Ruby dependency-age information for selected
declaration groups, which the all-direct lock report cannot provide. Group
annotations, filtered measurements, and deployed production scope are distinct
possible outcomes; no intended workflow has selected among them.

Git corroborates the boundary: `a16145f` selected Feature 004 while separately
retaining interpreted scope as EXPLORE; `577c81e` reconciled completion;
`1fcbd89` closed the retrospective. The [Feature 004 human
selection](../004-rubygems-support/discovery.md#human-product-decision) accepted
all-direct scope deliberately. Its [completion
record](../004-rubygems-support/tasks.md#status-and-authority) supersedes older
pending paragraphs. Neither the [routing guidance](../../AGENT_ROUTING.md) nor
[observation infrastructure](../../observations/README.md) selects a product.

## Current behavior / baseline

| Evidence path | Current scope and behavior |
|---|---|
| Python/PyPI | `requirements.txt` declarations; exact pins or a supplied `--resolved` snapshot establish versions. Snapshot-only packages do not enlarge scope. |
| npm/package-lock and Yarn Classic | Root `package.json` production `dependencies`, excluding optional overlap; package-lock v2/v3 or Yarn Classic v1 supplies exact evidence. Simultaneous root locks reject npm resolution evidence. |
| RubyGems | Root `Gemfile.lock` supplies all recorded direct names and supported exact selections. Gemfile is never read; groups are uninterpreted. Direct-file arguments do not activate Ruby. |

The [README](../../README.md), [SPEC](../../SPEC.md), and approved Feature
[003](../003-yarn-lock-evidence/spec.md) and
[004](../004-rubygems-support/spec.md) contracts govern this baseline.
[scan.py](../../libyears/scan.py), `scan_mixed_repository`, explicitly combines
three sources for one supplied location; it does not enumerate projects.
[rubygems.py](../../libyears/rubygems.py), `ruby_source_result` and
`_source_evidence`, read the root lock and label scope `all_direct_locked`.
`authorize_public_selection` independently gates public registry lookup.

Concrete witnesses in [test_rubygems.py](../../tests/test_rubygems.py) include
`test_only_root_lock_is_read`,
`test_lock_only_and_gemfile_presence_have_identical_unchanged_results`, and
`test_all_associations_and_pin_block_public_namesake_without_http`.
[test_mixed_scan.py](../../tests/test_mixed_scan.py),
`test_availability_matrix_preserves_known_scope_and_sibling_success`, protects
known versus unavailable scope and successful sibling ecosystems. Group support
would require a new scope/source contract, not merely a display change.

## Bounded discovery method

Read repository rules, routing guidance, roadmap, SPEC, README, CONTRIBUTING,
and observation protocol; reconciled completed Feature 003/004 discovery,
specification, plan, review, task, release-validation and retrospective evidence
with relevant Git history. Inspected source and test assertions for the scope,
source-authority and reporting boundaries above.

Consulted official RubyGems/Bundler documentation and version-tagged upstream
source for the EXPLORE opportunity. Public sources below were retrieved on
2026-10-29. No application corpus was newly collected, external local checkout
accessed, package manager executed, or live registry measurement performed.
Existing test assertions were inspected; historical suites and dogfood were not
rerun. This is discovery, not another convergence audit.

## Observed evidence and its implications

### F2 — Locks omit groups; production scope needs a separate definition

The upstream v3.6.9 [lock generator](https://raw.githubusercontent.com/rubygems/rubygems/v3.6.9/bundler/lib/bundler/lockfile_generator.rb)
emits dependency lock representations. [Dependency](https://raw.githubusercontent.com/rubygems/rubygems/v3.6.9/bundler/lib/bundler/dependency.rb)
stores group membership separately; its lock method extends the
[base serialization](https://raw.githubusercontent.com/rubygems/rubygems/v3.6.9/bundler/lib/bundler/rubygems_ext.rb),
which emits names and requirements, with a source marker. These entries do not
serialize groups. The current [parsed-lock model](../../libyears/gemfile_lock.py)
likewise has no group evidence. Better lock parsing cannot recover that absence.

The official [group guide](https://guides.rubygems.org/groups/) distinguishes
default, overlapping and optional groups, installation selection, and runtime
loading. A gem can remain included through another group even when one membership
is excluded. The version-tagged [selection implementation](https://raw.githubusercontent.com/rubygems/rubygems/v3.6.9/bundler/lib/bundler/definition.rb),
`requested_groups` and `dependencies_for`, also uses configuration and relevant
dependencies rather than a universal production-name rule.

**Inference:** selecting only `production`, selecting `default` plus
`production`, and excluding development/test can produce different populations.
A smaller age total after filtering would not establish improved freshness.
Declared groups cannot alone certify what a deployment installs or loads.

### F3 — Complete static scope and file association need explicit claims

The [Gemfile reference](https://guides.rubygems.org/gemfile/) describes Ruby
evaluation, conditional installation, gemspec declarations and additional
Gemfile evaluation. The v3.6.9 [DSL implementation](https://raw.githubusercontent.com/rubygems/rubygems/v3.6.9/bundler/lib/bundler/dsl.rb)
provides concrete witnesses in `eval_gemfile`, `gemspec`, `group` and `install_if`.
A static literal subset may be possible; its useful coverage is not demonstrated.

**Analytical counterexamples, not executed fixtures:** an enclosing conditional
can affect a familiar literal declaration; a gem in two groups defeats an
“any excluded group excludes the gem” shortcut. Unknown Ruby can affect scope or
source authority, so recognizing selected lines cannot certify a complete
population while silently ignoring the rest.

Moving a declaration between groups can leave lock names and versions unchanged.
Thus equal name sets do not prove that a supplied Gemfile and lock describe the
same group snapshot. A future product must distinguish measurement of supplied
files from historical coherence or deployment claims. Group evidence must also
preserve independent lock-source authorization; it cannot authorize a private
name's public namesake.

These are implications for a possible new contract, not defects in Feature 004.
Upstream examples of newer lock sections also do not expand its intentionally
bounded format; CHECKSUMS remains unsupported under its approved specification.

### F4 — Historical evidence does not establish demand or useful subset coverage

[Feature 004 discovery](../004-rubygems-support/discovery.md#deep-evidence-investigation)
records four build-consumed Ruby application pairs in one project family, with
development/test groups. Its [feasibility
review](../004-rubygems-support/reviews.md#ruby-feasibility-review) retained
approximately 238/247 direct occurrences before registry lookup. This supports
the earlier all-direct evidence model, not group-parser coverage or adoption.

The retained record does not provide a complete Gemfile construct census,
per-group measurement benefit, repeated user demand, or an accepted static
subset. [Successful Feature 004 validation](../004-rubygems-support/release-validation.md#successful-manual-release-evidence)
reports Ruby 67/69 and repository 77/79 measurement for all-direct scope. That
accepted human-supplied evidence was not independently audited in full from raw
JSON by the recording agent; it does not validate a future group filter.

The alternative radar entries retain their documented limitations. Feature 004's
Python compatibility investigation did not find repeated retained exact evidence
blocked by `--resolved`; root multiplicity did not demonstrate recurring selection
pain; Go/JVM investigation found no material selected-evidence improvement over
[Feature 003 discovery](../003-yarn-lock-evidence/discovery.md).
No new census or demand inference is made here.

## Decisions already established

[AGENTS.md](../../AGENTS.md), [SPEC](../../SPEC.md), and approved feature contracts
retain static analysis, Python standard-library-only runtime, direct dependency
scope, exact evidence, authoritative public timestamps, and unchanged metric
arithmetic. Missing information must not be guessed. Schema v3 separates
`source_errors` from dependency-level `unmeasurable`; unknown scope is not zero
coverage. Successful sibling ecosystems survive source failures.

Feature 004's source-authority, platform-evidence and observable-publication
choices remain settled. No group inference may bypass them. Existing behavior
remains governing unless a new approved contract explicitly changes it. Verified
TLS, repository filesystem boundaries and separate external-target permission
remain mandatory. Contribution/release procedures in
[CONTRIBUTING.md](../../CONTRIBUTING.md) do not supply product, trust or publication
authority for this discovery.

## Product questions

### MUST RESOLVE BEFORE SPECIFICATION

1. **H1 — Select the direction.** Should Feature 005 pursue Gemfile scope, another
   evidenced opportunity, or remain unselected while discovery continues? Radar
   order and the feature number supply no answer.
2. **H2 — If Gemfile scope is chosen, identify the intended user outcome.** Is the
   need group annotation, measurement for explicitly selected declared groups,
   or deployed production scope? Identify the representative workflow and the
   claim that would make the result useful. Deployment reconstruction has not
   been shown compatible with the present boundary.
3. **H3 — Accept or reject the bounded tradeoff.** Would static Gemfile inspection
   that rejects unsupported files and describes a qualified supplied-file pair
   justify additional maintenance? Establish the compatibility intention for
   existing all-direct scans. The human may accept the present evidence for a
   bounded direction or request stronger feasibility evidence first; no rejection
   rate or historical/runtime guarantee is invented here.

H2–H3 are conditional on choosing Gemfile scope, not demands to resolve every
radar item. A human choosing another direction needs its own bounded outcome.
External-local target access requires fresh authorization before inspection; it
is not inherently a prerequisite to specification if sufficient public/supplied
evidence and product approval exist. Trust and publication authority remain
separate gates for actions that actually need them.

### CAN DEFER TO SPECIFICATION

For the Gemfile candidate, after direction and intended outcome are approved:

1. **S1 — Inputs and completeness:** supported static forms, recognition, unknown
   constructs, missing inputs and when scope cannot be established.
2. **S2 — Group semantics:** default, overlapping, nested and optional membership
   and selection rules within the approved outcome.
3. **S3 — Evidence association and failures:** declaration/lock disagreement,
   source authority, duplicate identity, and source versus dependency failure.
4. **S4 — Public behavior:** activation/defaults, compatibility, empty versus
   unavailable coverage, diagnostics, provenance and schema treatment.
5. **S5 — Acceptance evidence:** concrete successful and rejected examples,
   expected user benefit and required real-root validation.

These are observable contract questions, not implementation discretion. New
consequential product choices discovered there still require human clarification.

### CAN DEFER TO PLANNING

1. **P1:** parser strategy, internal representation and resource bounds.
2. **P2:** module ownership and integration with existing source/adapter results.
3. **P3:** fixtures, focused regressions and acceptance-traceability organization.
4. **P4:** dependency ordering, coherent public activation and validation execution.

No architecture is selected here. Required validation and optional live smoke
must remain distinct; redundant smoke must not become a mandatory dependency.

### OUT OF SCOPE

Ruby/Gemfile/gemspec execution; package-manager invocation, installation or
resolution; private sources, credentials or public-namesake substitution;
installed/runtime-environment reconstruction; generic parser/resolver frameworks;
additional ecosystems or expanded npm scopes; recursive project aggregation;
metric changes, broader Bundler-format support, caching or new provenance
requirements without separate approval. This run also excludes specification,
planning, tasks, implementation, ledger edits, external repository modification,
release, tagging and pushing.

## Evidence limitations and readiness

Public documentation retrieval succeeded. Native CLI registry connectivity and
agent/host parity were not tested. Historical TLS and later DNS limitations are
separate environmental evidence, not current product failures or a caching need.
Official documentation and version-tagged source establish specific semantic
witnesses, not universal Bundler compatibility, application acceptance or demand.
Historical external collections were not re-inspected; their old permissions do
not transfer to this work.

If stronger feasibility evidence is wanted, use named public revisions or newly
authorized Gemfile/lock pairs relevant to the intended workflow. Record revision,
all material constructs, group membership, complete-scope confidence, file
association and unsupported cases. Distinguish scope recognition, exact-version
availability and registry measurement. Compare complete-file interpretation with
expected selected scope, not just recognized lines; a second project family can
challenge sample-specific conclusions. This is an optional bounded discovery
method, not a task graph or numerical readiness threshold. Stop if useful scope
requires general Ruby evaluation or package-manager execution, as ROADMAP directs.

**HUMAN DECISION REQUIRED.** The four findings above complete this bounded
handoff. H1–H3 remain unanswered; specification readiness is NO. The next author
can conduct product clarification from this artifact without temporary research
files. No product slug, specification, architecture or implementation approval
is implied by preserving discovery durably.

## Human Product Decision

**Decision date:** 2026-10-29. Human product authority supplied H1–H3 before
selection-recording run `005-0002`, following discovery run `005-0001`.

**Decision:** SELECTED FOR SPECIFICATION

**Feature 005:** Bounded static Gemfile group scope

- **H1 — SELECT bounded static Gemfile group scope as Feature 005.** This is
  deliberate human product approval, independent of roadmap order, EXPLORE
  status, or agent preference.
- **H2 — Dependency-age measurement for an explicitly selected set of statically
  declared Gemfile groups.** Supported static Gemfile evidence may establish
  dependencies belonging to selected declared groups, associated with existing
  supported exact Gemfile.lock evidence for measurement. The claim is bounded
  to the supplied declaration/lock evidence. Group names are project-supplied
  declarations; users explicitly select the groups to measure. There is no
  implicit production scope and no claim about deployed, installed, or
  runtime-loaded dependencies or a reconstructed Bundler environment.
- **H3 — ACCEPT the maintenance/rejection tradeoff of a conservative static
  Gemfile subset.** A deliberately bounded set of statically interpretable forms
  may be supported. Transparent incompleteness is preferable to opaque inference.

Existing ordinary Ruby scanning preserves the approved all-direct Gemfile.lock
behavior as the default unless scoped group behavior is explicitly requested.
Gemfile Ruby must never be executed, and Bundler must never be invoked for
interpretation, installation, or resolution. Partially understood Gemfiles must
never silently establish complete scope; unsupported or ambiguous constructs
that prevent establishment of requested scope fail closed.

Independent lock-source/public-source authorization remains mandatory; private
or unauthorized evidence must never be replaced by a public namesake. Associating
Gemfile names with Gemfile.lock selections establishes no historical-coherence
claim and no deployment-state claim. The discovery exclusions remain unchanged.

**Specification readiness: YES — READY to begin.** This subsequent human decision
resolves the historical H1–H3 gate; it does not change what was known or selected
when `005-0001` stopped at HUMAN DECISION REQUIRED. The normal directory rename
from `specs/005-discovery/` to `specs/005-gemfile-group-scope/` records the selected
direction without rewriting discovery history.

S1–S5 remain specification work: inputs/completeness, group semantics, evidence
association/failures, public behavior, and acceptance evidence. CLI spelling and
exact public syntax remain for specification. New consequential product questions
still require human clarification. Parser architecture, internal representation,
module ownership, resource bounds beyond existing policy, fixture organization,
implementation order, and detailed validation execution remain planning concerns.
No specification, plan, task graph, or product implementation is begun by this
selection record.
