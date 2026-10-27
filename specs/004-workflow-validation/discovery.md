# Feature 004 Discovery: Evidence and Candidate Direction

## Status

**READY FOR FOCUSED RUBY FEASIBILITY REVIEW**

No Feature 004 implementation direction approved yet. Discovery remains before
specification. Ruby support is a candidate, not an approved Feature 004.

## Initial Recommendation — Historical

The initial draft was committed as
`df7aee60446795f67da321331f778c3d1457fea7`
(`docs(discovery): draft Feature 004 direction`) before independent review.
It recommended **no-code workflow validation**, with Python exact-evidence
usability as the runner-up. The rationale was that manifest prevalence alone
did not establish the next useful capability; it proposed asking users about
measurement attempts before choosing a parser or ecosystem.

That recommendation is preserved as history, not the current direction.
The exact initial inventory, comparisons, proposed research, and rationale
remain available in the corresponding reconstructed commit, with publication-hygiene sanitization only. The review and bounded technical
investigation below supersede its candidate ranking and broad human questions.
See [reviews.md](reviews.md) for the review disposition.

## Independent Discovery Review

**Initial recommendation:** no-code workflow validation.
**Review verdict:** CONTINUE DISCOVERY.

The independent review findings, supplied for this revision, required these
changes in interpretation:

- The sandboxed `0/77` registry result is **agent-environment evidence**, not
  evidence of a product need for offline operation. Codex sandbox failures are
  excluded from product evidence. Feature 003's recorded `77/77` successful
  dogfood remains separate historical validation.
- Workflow validation is **continued discovery**, not Feature 004 itself. The
  initial proposal was too vague to define a product capability.
- Python exact-evidence compatibility was selected as the next **bounded
  experiment**, before any new Python parser recommendation.
- Broad human research was premature while repository evidence could answer
  the technical questions cheaply.
- Root identification/listing must remain separate from portfolio aggregation.

The completed experiment tested whether at least two distinct project roots
have supported non-exact direct declarations and already-produced local exact
selected-version evidence that current `--resolved` cannot consume unchanged.

## Current Capability

Libyears measures direct dependencies when it can connect a declaration to an
exact used version and a public registry release timestamp. It currently
supports Python packages from PyPI and npm packages from the npm registry.

- Python declarations come from `requirements.txt`. Exact `==` pins are
  evidence themselves. Non-exact declarations can use the optional
  `--resolved` snapshot, a narrow `NAME==VERSION` file; declarations determine
  scope and snapshot-only transitive entries are ignored. A snapshot may be
  generated outside libyears, for example with `pip freeze`, but that describes
  the environment used to create it and is not necessarily repository history.
- npm scope is root `package.json` production `dependencies`, excluding names
  also declared in `optionalDependencies`. Root `package-lock.json` v2/v3
  provides selected versions. Feature 003 added root Yarn Classic v1 lockfile
  evidence. If both lockfiles exist, neither is selected. Dev, peer,
  optional-only, workspace, and transitive dependencies remain out of scope.
- A scan can combine Python and npm. Public JSON is schema v3, with
  ecosystem-keyed version evidence and repository plus per-ecosystem summaries.
- A dependency whose version, registry record, or timestamp cannot be safely
  established is listed as `unmeasurable` with a stable reason. A failed,
  malformed, conflicting, or unsupported whole source is represented in
  `source_errors`; where the dependency denominator is known but evidence is
  rejected wholesale, measured count and coverage can be null. This differs
  from an ordinary dependency-level `0/N` result.
- Scanning is static. Libyears does not install packages, execute repository
  code, run package managers, resolve ranges, or calculate a dependency graph.
  Python and npm registry access is isolated in adapters and uses verified
  HTTPS. Without usable registry access, dependencies with exact evidence still
  cannot be assigned release timestamps. The deterministic test suite uses
  local fixtures/mocks; this discovery did not run it.

Deliberate limits include direct-only scope, bounded parsers, no guesses when
evidence is absent or ambiguous, no support for other ecosystems, no generic
resolver or semantic-version engine, and registry dependence for timestamp
authority. README's link to GitHub's dependency page for this repository is not
a repository-local SBOM and does not change those capabilities.

## Deep Evidence Investigation

### Method and evidence boundaries

The completed read-only investigation examined dependency metadata and relevant
setup/build/CI evidence under `<local-collection-a>` and
`<local-collection-b>`, plus current Libyears parsing, matching, reporting,
tests, and relevant Git history. No external repository code or package manager
was executed, dependencies were not installed or resolved, and no live package
lookup was performed. Ruby feasibility also used authoritative public
RubyGems/Bundler documentation.

**Observation:** the two authorized directories are collections of project
trees, not two Git checkouts as the initial draft described them. Counts below
are bounded observations, not population estimates, independent deployments,
or evidence of adoption. Installed package trees were excluded from project
counts and inspected separately only for relevant existing metadata.

### Python

**Observation:** there are **10 metadata-bearing roots / 8 project families**
after conservative copy grouping. Paths below are relative to the authorized
collection named in the first column. Every row contains `requirements.txt`.

| Collection / project root | Requirements entries | Declaration and exact-evidence observations |
|---|---:|---|
| <local-collection-a> / `metrics` | 7 | Six bare names and one numeric minimum; urllib3 explicitly described as indirectly required |
| <local-collection-a> / `code-book` | 4 | Four supported numeric minimums; no retained selected-version artifact found |
| <local-collection-a> / `year-in-review` | 1 | PyGithub minimum; no selected-version artifact found |
| <local-collection-a> / `<local-copy-group>/year-in-review` | 1 | Requirements and README byte-identical to the preceding project |
| <local-collection-a> / `repo-scaffolder` | 5 | cookiecutter exact pin, bare pytest-cookies, three explicitly indirect security bounds |
| <local-collection-a> / `<local-copy-group>/repo-scaffolder` | 5 | Requirements and README byte-identical to the preceding scaffolder |
| <local-collection-a> / `share-it-savings` | 2 | matplotlib/numpy minimums; local installed metadata, but no demonstrated project-resolution artifact |
| <local-collection-a> / `code-gov/scripts` | 2 | Bare names; CI installs this nested requirements file |
| <local-collection-a> / `<local-copy-group>/super-changelog` | 0 | Empty requirements file; four project dependencies in `pyproject.toml`, unsupported by current discovery |
| <local-collection-b> / `dpc-app` | 1 | Bare bzt for smoke-test tooling; no retained Python selection artifact found |

There are **28 non-comment requirements entries: 2 exact pins and 26 non-exact
declarations**. Both exact pins are the same copied `cookiecutter==2.6.0`
declaration, not independent resolution evidence. Seven entries across metrics
and the two scaffolders explicitly describe indirect security bounds; current
file discovery does not establish that these are direct application dependencies.

No requirements includes, hashes, indexes, editable installs, direct URLs, or
environment markers were observed in these ten files. No retained Python lock,
compiled/frozen requirements, or dependency export was found. Super-changelog
ignores `poetry.lock`, but no such file was found; ignoring a filename does not
prove generation. Its pyproject supplies declarations, not selected versions.

**Compatibility observation:** current `--resolved` accepts exact
`NAME==VERSION` text records, comments, and identical normalized duplicates;
conflicting versions fail closed. Repository declarations determine scope and
snapshot-only packages are ignored. Snapshot matching supports bare names,
textually matching exact pins, and numeric-dotted minimums. This conclusion is
supported by `libyears/snapshot.py`, `libyears/constraints.py`,
`libyears/scan.py`, and their corresponding tests.

One root, share-it-savings, has local installed distribution metadata for
matplotlib `3.11.1` and numpy `2.4.6`. Separate `Name:`/`Version:` headers could
be extracted into compatible snapshot records. The metadata establishes that
local environment's versions; no build association or retention workflow
establishes historical project selection. It is not Git-tracked and the
environment contains unrelated packages. Even accepting this as qualifying
environment evidence would yield only one root, below the required two.

**Strict hypothesis result: THRESHOLD NOT MET.** There is no demonstrated
retained project-resolution artifact blocked by `--resolved`, and no repeated
retained Python evidence incompatibility. The dominant observed problem is
**absence of retained exact evidence**, not incompatibility with the current
snapshot format. Normal installation instructions and CI download caches do
not demonstrate manual evidence-preparation burden.

**Inference:** no new Python exact-evidence parser is justified by this sample.
Pyproject declaration discovery is a separate, weaker opportunity: it would
expose four declarations in one root without establishing their used versions.

### Project roots

**Observation:** structural/project-root multiplicity is real. DPC has separate
application build targets, Dockerfiles, and portal test invocations;
`design-system/lerna.json` lists `packages/*` and workspace use; Maven parent
POMs enumerate modules; code-gov CI explicitly installs
`scripts/requirements.txt`. These build/workspace systems encode multiple roots.
The inspected design-system copy has no root `package.json`, despite nested
manifests and its workspace configuration.

**Missing evidence:** no demonstrated Libyears root-selection failure,
repeated measurement invocation, or recurring user pain was found. Existing
root lists may already be sufficient for an external wrapper.

**Inference:** candidate-root discovery/listing may help navigation, but this
is distinct from portfolio aggregation. No cross-project metric aggregation
or denominator semantics are evaluated or proposed here.

### Ruby

**Observation:** four application roots under `<local-collection-b>/dpc-app` each contain a
Gemfile and Gemfile.lock. Their Dockerfiles explicitly copy and consume those
locks through Bundler installation, and run dependency audits. This is retained
evidence consumed by build instructions, not merely four unexplored file pairs;
builds were not executed during discovery.

| Application | Literal Gemfile declarations, all groups | Names with ordinary exact lock specs |
|---|---:|---:|
| `dpc-admin` | 69 | 67 |
| `dpc-adminv2` | 57 | 55 |
| `dpc-impl` | 55 | 53 |
| `dpc-web` | 66 | 64 |

In each root, literal direct declaration names match the lock's `DEPENDENCIES`
name set. Most declarations have ordinary exact locked versions, and all four
locks identify the public RubyGems source. No active Git/PATH lock sources were
observed; a Git source helper and commented examples do not establish active
Git dependencies. These are four application roots in one project family,
not four independent users or validated deployments.

Groups, platforms, and special entries remain material semantic questions.
Development/test groups are present. `bundler` and platform-conditioned
`tzinfo-data` lack ordinary gem-spec entries in each lock; `BUNDLED WITH` must
not automatically be substituted for application dependency evidence.
Adminv2 has generic and Darwin nokogiri variants. Build instructions set
`force_ruby_platform true`, but this does not establish a general platform rule.
The table is not an approved production scope or measured coverage result.

**Inference:** many ordinary declarations appear conservatively mappable to
exact lock evidence without running Bundler. General Gemfiles are executable
Ruby, so this does not establish that arbitrary declaration evaluation can be
supported statically. See the [Gemfile reference](https://guides.rubygems.org/gemfile/)
and [lockfile documentation](https://guides.rubygems.org/gemfile-lock/).

Public RubyGems timestamp metadata appears available: the
[RubyGems API documentation](https://guides.rubygems.org/rubygems-org-api/)
describes version records with creation timestamps, prerelease indicators,
and platforms. Canonical publication-time, platform, and yanked-release
semantics still need technical review; no live package lookups validated them.

**Evidence fitness: MEDIUM-HIGH. Demand confidence: LOW-MEDIUM.** These are
qualitative judgments based on the evidence above. User demand and useful
conservative scope remain unproven. This is not implementation readiness.

### Go/JVM

**NO MATERIAL EVIDENCE DELTA.** Six Go module/sum pairs remain, without a retained
selected build list, generated module inventory, or `vendor/modules.txt`.
No JVM dependency lock, resolved tree/report, or build-associated inventory was
found. The deeper walk found 22 POMs, correcting the initial draft's 21-file
count without improving selected-version evidence. Feature 003's evidence
limitations remain; sums and declarations must not be treated as resolution.

### Provenance

**NO DEMONSTRATED PROBLEM.** Schema v3 already distinguishes declaration and
version sources and source-level versus dependency-level failures. The metrics
project has historical Libyears graphs, but collection delegates to another
package; no consumer of this CLI schema demonstrated a missing provenance
field. Possible missing root identity, content hashes, or lookup timestamps
are not by themselves product requirements.

### Offline/cache

**PLAUSIBLE BUT UNDEMONSTRATED.** CI installation caches and historical metric
outputs exist, but no air-gapped measurement, public-registry restriction,
release-metadata cache, or requirement to replay historical registry state was
demonstrated. npm `--prefer-offline` is installation evidence; EASI's offline
feature-flag mode is unrelated. Codex sandbox/network failures are explicitly
excluded from product evidence.

## Candidate Ranking

This ranks **investigation priority**, not implementation approval. Counts
express observed evidence reach, not demand or expected adoption.

| Rank | Serious product candidate | Evidence and limitations | Scope and boundary judgment |
|---|---|---|---|
| 1 | Bounded Ruby evidence support | Four build-consumed manifest/lock pairs; MEDIUM-HIGH evidence fitness, LOW-MEDIUM demand confidence | Potential static subset; new registry and ecosystem maintenance; group/platform semantics unresolved |
| 2 | Project-root discovery/listing | Multiple roots encoded in build/workspace systems; user pain unproven | Potentially bounded navigation aid; external wrapper remains credible; no portfolio aggregation |
| 3 | Python pyproject declaration discovery | Four invisible project declarations in one root; no retained exact selections | Could improve discovery completeness, not demonstrated measurement coverage; overlapping declaration tables need care |

The following are lowered or removed from the serious shortlist unless new
evidence changes their case:

- **New Python exact-evidence parser:** the explicit two-root threshold failed.
- **Offline/cache:** no demonstrated measurement requirement; sandbox failures
  provide no product evidence.
- **Go and JVM:** no new selected-version artifacts address prior limitations.
- **Provenance expansion:** no observed downstream consumer gap.
- **pnpm/SBOM:** no relevant project evidence establishes demand for ingestion;
  generator index records and an installed library's own SBOM are not project
  resolution inventories.

Workflow validation is ongoing discovery, not a ranked product feature.

## Recommended Direction

**No Feature 004 implementation direction approved yet.**

Bounded Ruby exact-evidence support is the strongest current candidate and
should receive **one focused feasibility/product-scope review before a human
Feature 004 decision**. Do not call Ruby Feature 004 yet.

The review should use the four observed application pairs to assess a useful
static scope, groups/platforms and special entries, timestamp authority,
conservative coverage limits, and the cost of a third registry. It should
identify what can be established without runtime Gemfile evaluation or
resolution, and present remaining product choices rather than silently making
them. This is investigation, not specification, architecture, or implementation.

Preserve the small static metric boundary: no package-manager execution,
repository-code evaluation, dependency resolution, generic plugin framework,
portfolio aggregation, or metric-semantic changes are authorized.

## Falsification: Reasons Not to Build Ruby

Do not build the candidate if evidence establishes that:

- Intended users do not measure these applications.
- The applications are irrelevant or historical copies for the intended use.
- Useful scope requires runtime Gemfile evaluation.
- Platform/group semantics cannot be conservatively bounded.
- Conservative measurable coverage is too small to be useful.
- Third-registry maintenance cost is not justified by the user benefit.

Four matching file pairs alone do not overcome any of these conditions.

## Remaining Human Questions

After the focused technical review, the smallest useful human question is:

- Does the demonstrated conservative Ruby scope serve an intended measurement
  workflow well enough to justify adding and maintaining a third registry?

This requires user/product judgment. Most remaining Ruby semantics can be
investigated technically before human attention is required: declaration/lock
mapping, special entries, platform variants, group information retained in
artifacts, timestamp authority, and resulting coverage limits. Only unresolved
scope/value tradeoffs should be escalated. Broad workflow research is not the
next step, and no product direction is approved by this question.

## Process Record

Feature 002's retrospective exposed missing review rationale; Feature 003's
discovery/reviews improved that record and recommended committing drafts before
review. Feature 004 applies that experiment: `df7aee60446795f67da321331f778c3d1457fea7` preserves the exact initial
discovery, while this separate revision preserves the supplied independent
review disposition and completed deep-investigation findings. Git retains the
before/after artifacts without preserving chat transcripts or rewriting history.
The evidence summary distinguishes observations, inferences, and missing demand;
it does not claim a new independent review of this revision.
