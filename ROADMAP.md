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

Human-selected product direction in discovery, approved for specification, or
active SDD work. Selection alone does not approve the next SDD gate.

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
| [Project-root discovery/listing](#3-project-root-discoverylisting) | SELECTED (bounded NuGet correction) | CLI / repository discovery | Bounded product correction |
| [NuGet repository project sources](#12-nuget-repository-project-sources) | SELECTED (source occurrences) | NuGet / repository population | Bounded product correction |
| [Cross-ecosystem measurement-evidence parity](#13-cross-ecosystem-measurement-evidence-parity) | SELECTED (006-0024 cascade) | Product semantics | Bounded measurement/assurance migration |
| [NuGet project/lock population](#14-nuget-project-population-and-retained-lock-population) | SELECTED (006-0026 bound snapshot fallback) | NuGet population/context | Bounded explicit acceptance |
| [Python/npm public namespace](#15-pythonnpm-positive-public-namespace-authority) | EXPLORE | Cross-ecosystem truthfulness | Separate source-authority investigation |
| [Snapshot acceptance/currentness](#16-repository-contained-snapshot-acceptance-and-currentness) | SELECTED (006-0028 B1) | NuGet acceptance | Separate product/trust contract |
| [NuGet namespace automation](#17-nuget-namespace-authority-automation) | EXPLORE | Namespace authority | Separate evidence investigation |
| [Bounded C# parser expansion](#18-bounded-static-c-project-parser-expansion) | EXPLORE | Static declarations | Bounded grammar review |
| [Evaluated MSBuild use cases](#19-evaluated-msbuild-population-use-cases) | DEFER | Evaluated context | Separate authority |
| [Hosted action-runtime maintenance](#20-hosted-action-runtime-maintenance-observations) | WATCH | CI maintenance | Separate warning investigation |
| [Stronger producer assurance](#21-stronger-nuget-producer-assurance) | EXPLORE | NuGet provenance | Separate retained evidence |
| [Go selected-version support](#4-go-selected-version-support) | WATCH | Go | Advanced evidence investigation |
| [Python pyproject declaration discovery](#5-python-pyproject-declaration-discovery) | WATCH | PyPI | Rotation / bounded discovery task |
| [Portfolio orchestration](#6-portfolio-orchestration) | DEFER | Multi-project workflow | Separate tool / future product exploration |
| [Ecosystem analyzer boundary](#8-ecosystem-analyzer-boundary) | EXPLORE | Architecture evidence | Bounded maintainability investigation |
| [Dependency-metadata providers](#9-dependency-metadata-providers) | EXPLORE | Evidence sources | Provider landscape investigation |
| [Human-centered agentic-development harness](#10-human-centered-agentic-development-harness) | EXPLORE | Methodology | Cross-project evidence and distribution study |
| [Java ecosystem repodive](#11-java-ecosystem-repodive) | EXPLORE | Java discovery | Human-requested bounded investigation |

### 3. Project-root discovery/listing

**State:** SELECTED for the bounded NuGet user-journey correction only.

**Area:** CLI / repository discovery

**Contributor fit:** Rotation / product-discovery candidate

**Opportunity:** Recognize/list bounded C# filename candidates in ordinary human
root reports without activating measurement or calculating cross-project aggregates.

**Evidence:** Feature 004 discovery observed multiple structurally meaningful
roots and build systems that enumerate them. Post-convergence run 006-0018
reproduced a human's ordinary OASim repository-root invocation reporting no
ecosystems despite ten known nested C# projects. Feature 006 intentionally
requires an explicit immediate project; this is a real root-selection UX gap.

**Why this state:** The human repeatedly reproduced the confusing ordinary-root
invocation after Feature 006 operational closure and explicitly selected the
smallest truthful recognition correction in run `006-0020`. The separate
[maintenance SDD artifacts](maintenance/nuget-root-recognition/discovery.md)
govern that bounded follow-up, not a new numbered feature or original Feature 006
acceptance. Implementation and review disposition live in its review record.
Broader cross-ecosystem project listing remains unselected; this correction
authorized no generic indexing, automatic choice, solution/reference interpretation
or aggregation. The distinct subsequent repository-measurement question is
tracked in opportunity 12 below.

**Success signal:** The obvious authorized OASim root command lists ten filename
candidates, states none were measured as NuGet, and explains explicit selection.
No measured attention-saving or broad adoption claim follows from one smoke.

**Bounded outcome:** Run `006-0020` implements the human-only correction and its
required root smoke recognizes ten candidates without NuGet measurement. See
[validation](maintenance/nuget-root-recognition/validation.md) and the linked review
record for completion/convergence disposition. The commissioning human subsequently
observed all nine OS/Python matrix jobs, Live PyPI smoke, secrets/hygiene/CodeQL
and pages workflows GREEN on published `cce5e6a`; the separate
[operational closure](maintenance/nuget-root-recognition/operational-closure.md)
records actual Windows 3.11/3.12/3.13 PASS and the complete hosted evidence.

**Stop condition:** Existing build/workspace metadata or simple external wrappers
already solve the workflow adequately.

**References:**

- [Feature 004 discovery](specs/004-rubygems-support/discovery.md)
- [Operational smoke maintenance](maintenance/operational-smoke-006-0018.md)
- [Bounded root correction and reviews](maintenance/nuget-root-recognition/reviews.md)

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

### 8. Ecosystem analyzer boundary

**State:** EXPLORE

**Area:** Architecture evidence

**Contributor fit:** Bounded maintainability investigation

**Opportunity:** Investigate an explicit ecosystem-analyzer seam inside the current
modular monolith, alongside keeping the existing explicit source pairs.

**Evidence:** Feature 006 adds staged authority, worker lifecycle and shared
scan/output branches; cumulative tests and cross-platform fixtures expose testing
and integration pressure. Maintenance hours or a scaling law were not measured.

**Why this state:** The approved retrospective recommends evidence gathering;
no interface, migration or generic plugin framework is selected. This run performs
no exploration.

**Success signal:** A concrete change-history/test-cost map and bounded comparison
show lower maintenance burden with equivalent domain, privacy and failure witnesses.

**Stop condition:** Indirection hides ecosystem rules or supplies no demonstrated
benefit over current explicit boundaries.

**References:** [Feature 006 retrospective](specs/006-nuget-selected-evidence/retrospective.md#architectural-complexity).

### 9. Dependency-metadata providers

**State:** EXPLORE

**Area:** Evidence sources

**Contributor fit:** Provider landscape investigation

**Opportunity:** Compare dependency-metadata providers, including ecosyste.ms,
against direct-registry evidence requirements.

**Evidence:** Feature 006's completed prospective validation yielded a native/public
hash mismatch and no measurable age. Registry identity, source authority, dates
and provider fidelity are separate questions; no alternative provider was tested.

**Why this state:** Human-requested future evidence gathering, not adoption or a
selected solution to the observed mismatch. No provider research occurs here.

**Success signal:** Concrete comparative evidence on coverage, source/content/date
fidelity, reproducibility and operational cost under the existing metric boundary.

**Stop condition:** A provider obscures authority, cannot substantiate required
claims, or requires an unapproved dependency/trust/semantic change.

**References:** [Feature 006 retrospective](specs/006-nuget-selected-evidence/retrospective.md#what-we-would-do-differently-and-human-handoff).

### 10. Human-centered agentic-development harness

**State:** EXPLORE

**Area:** Methodology

**Contributor fit:** Cross-project evidence and distribution study

**Opportunity:** Investigate a generalized development harness and possible
SKILL.md distribution of demonstrated lifecycle/review/baton practices.

**Evidence:** Features 004–006 retain frozen review/correction patterns;005/006
use internal orchestration and prospective observations. The qualitative17K prompt
signal motivated durable information architecture; measured attention savings and
cross-project generality remain absent.

**Why this state:** Reusable practice merits evaluation, not a selected tool,
mandatory premium-model workflow or immediate skill implementation.

**Success signal:** Another authorized project preserves equivalent quality and
human authority with measured coordination/maintenance burden and accessible routing.

**Stop condition:** Packaging adds more administration than value, cannot preserve
repository-specific authority, or relies on unobserved resource claims.

**References:** [SDD_WORKFLOW.md](SDD_WORKFLOW.md), [Feature 005 retrospective](specs/005-gemfile-group-scope/retrospective.md), [Feature 006 retrospective](specs/006-nuget-selected-evidence/retrospective.md).

### 11. Java ecosystem repodive

**State:** EXPLORE

**Area:** Java discovery

**Contributor fit:** Human-requested bounded investigation

**Opportunity:** A future bounded Java ecosystem repository investigation to identify
actual direct declarations, retained selection and source/publication evidence.

**Evidence:** The human explicitly requests preserving this opportunity in the
006-0017 closure commission. This closure supplies no new Java repository evidence.

**Why this state:** Human demand supports future evidence gathering; no Feature007,
Java support or external repository access is selected/authorized here.

**Success signal:** Separately authorized real repository evidence establishes a
useful bounded workflow without executing a resolver inside libyears.

**Stop condition:** Evidence requires unapproved target access, execution, unsupported
selection assumptions or ecosystem implementation before product selection.

**References:** [Feature 006 retrospective](specs/006-nuget-selected-evidence/retrospective.md#what-we-would-do-differently-and-human-handoff).

### 12. NuGet repository project sources

**State:** SELECTED in run `006-0022`. The human approves source-qualified
project occurrence weighting and autonomous SDD under the separate
[repository-source correction](maintenance/nuget-repository-sources/spec.md).

**Area:** NuGet / repository population and output

**Opportunity:** Let ordinary repository measurement discover independently
admissible bounded project sources while retaining explicit project selection.

**Evidence:** After completed 006-0020 recognition, repeated ordinary OASim use
still requires a project-selection decision. Run `006-0021` corroborates ten
projects/51 literal external-reference occurrences/24 package IDs/15 project
edges, but the current conservative parser accepts only two populations totaling
three references. Eight populations are unknown; the two accepted declarations
lack explicitly supplied witnesses in the no-acceptance probe. The historical
51-reference inventory cannot become current numeric coverage by assumption.

**Why this state:** The explicit human decision now authorizes repeated direct
membership across independently supported projects, without deduplication, solution
or reference-graph population authority. H3, explicit witness acceptance, unknown
population and unavailable-source null semantics remain binding. Additive schema3
representation requires independent review; incompatible output needs a human
schema decision. This is separate from completed recognition and from portfolio
orchestration across independent repositories.

**Implementation evidence:** The separate correction implements automatic bounded
source attempts with additive schema3 identity. Run006-0022 ordinary OASim smoke
attempts ten sources without a project-selection decision: eight unknown populations,
two known populations totaling three occurrences with missing accepted provenance,
and null repository coverage. Captured before/after state matches exactly. See
[validation](maintenance/nuget-repository-sources/validation.md) and current
[review disposition](maintenance/nuget-repository-sources/reviews.md); hosted
Windows/other CI remains a post-publication witness, not inferred here.

**Success signal:** A human-approved source/population contract makes ordinary
repository measurement truthful without choosing a project, preserves source
identity and failures, and keeps unknown or unavailable coverage honest.

**Stop condition:** Unresolved occurrence weighting, source/schema contract,
implicit testimony, deduplication, solution/graph authority, changed metric or
generated-evidence requirements. Implementation is authorized only through the approved correction lifecycle;
no broader ecosystem discovery is selected by this entry.

**References:** [Discovery and alternatives](discovery/nuget-repository-sources.md),
[independent review](discovery/nuget-repository-sources-review.md),
[006-0020 operational closure](maintenance/nuget-root-recognition/operational-closure.md).

### 13. Cross-ecosystem measurement-evidence parity

**State:** SELECTED in `006-0024`; the human approves a progressive measurement
cascade. Specification, plan and sequential graph independently approved;
implementation and operational evidence are locally CONVERGED after independent
review and bounded correction in [the correction](maintenance/measurement-evidence-cascade/reviews.md).

**Area:** Product semantics / public publication-history authority

**Opportunity:** Use the strongest accepted evidence while requiring only what
establishes the actual version-age claim. Measurement basis and stronger assurance
are related but distinct; missing acquisition/content/reproducibility evidence
must not automatically block a supported snapshot/public-namespace age.

**Evidence:** Discovery006-0023 reconciled current PyPI/npm/Ruby/NuGet contracts.
Historical H3 and published1ba915f truthfully implemented their stronger authority;
those outcomes remain unchanged. The prospective cascade keeps declaration-first
NuGet population, exact context/byte/request association and public namespace before
lookup; v1 facts survive and v2 accepts later bound snapshot/namespace testimony.
Additive schema3 evidence and verbose detail disclose narrower claims.

**Practical result:** Ordinary OASim still has ten attempts, eight unsupported
populations and two supported populations totaling3 occurrences with no accepted
witness mappings. Zero new ages are established; N/coverage remain unknown. Ten
retained locks alone cannot establish applicable public namespace. Target before/
after state equals. Parser limitations and namespace acceptance are distinct from
optional stronger assurance, and51 literal references are no denominator.

**Success signal:** Truthful snapshot ages plus inspectable strongest accepted
assurance, without namesake fallback, invented population or changed arithmetic.

**Stop condition:** New consequential trust/schema/security authority or incompatible
output; no implicit testimony, target execution, generic framework, Feature007 or
provider adoption. Publication/actual hosted witnesses remain separate authority.

**References:** [Historical discovery](discovery/measurement-evidence-parity.md),
[historical independent review](discovery/measurement-evidence-parity-review.md),
[current prospective specification](maintenance/measurement-evidence-cascade/spec.md),
[verification](maintenance/measurement-evidence-cascade/validation.md).

### 14. NuGet project population and retained lock population

**State:** SELECTED in `006-0026` by explicit human population authority.
The [bound snapshot correction](maintenance/nuget-snapshot-population/spec.md)
implements A-first, explicitly accepted B fallback; convergence disposition lives
in its [review record](maintenance/nuget-snapshot-population/reviews.md).
Run006-0025 discovery/review was frozen in be1fc47 before selection and remains
historical: no prior accepted51 denominator or mistaken prior refusal is implied.

**Area:** NuGet directness/context and ordinary usefulness

**Opportunity:** Select the smallest truthful population basis: bounded static
declaration support versus explicitly accepted bound snapshot fallback. Avoid
reimplementing MSBuild or claiming current/evaluated completeness from a lock.

**Evidence:** Fresh enumeration finds ten sole-net10.0 schema1 locks with 51 Direct
records, matching 51 literal references and normalized requests, with supported
selected versions throughout. This agreement is not an accepted denominator.
Current A accepts only Updater/Profiling (3 occurrences); eight reject for exact
ancillary-property, conditional-output or resource/item rules, not observed
conditional PackageReferences. Property-table corrections could admit 6/16;
narrow None Update support could reach 7/25. Broader inert-only grammar or an
independently bound snapshot basis could potentially reach 10/51, subject to
approval and acceptance. Neither automatically establishes currentness or absence
of implicit SDK references. The implemented cascade retained A deliberately.

**006-0025 recommendation (historical):** An explicit, bound snapshot-population fallback for human
consideration, preserving explicit external direct scope, context/byte association,
known-conflict refusal and visible population basis. No silent fallback or reuse
of old witness meanings. Namespace remains a separate prerequisite: existing
Updater testimony matches current bytes but requires explicit acceptance; no
automatic ordinary-file public authority was established. Registry dates remain
untested. Windows portability is separately closed on human-supplied repaired
70b4583 hosted evidence, without revising 006-0024's original local convergence.

**Success signal:** A separately selected directness/context contract admits useful
retained snapshots with truthful denominators and explicit stale/context limits.

**Stop condition:** Resolver/target execution, fabricated51 count, silent A/B mixing,
implicit/auto-reference scope or unapproved completeness testimony.

**References:** [Ten-project audit and alternatives](discovery/nuget-population-basis.md),
[independent review](discovery/nuget-population-basis-review.md),
[historical A/B determination](maintenance/measurement-evidence-cascade/spec.md#lock-and-population-determination-c3),
[exact prior operational blockers](maintenance/measurement-evidence-cascade/validation.md),
[post-publication Windows evidence](maintenance/measurement-evidence-cascade/reviews.md#repaired-published-candidate-supplied-hosted-evidence--006-0025).

**006-0026 implementation evidence:** strict v3 snapshot testimony binds exact
project/lock bytes, project identity and sole framework, with explicit external
Direct completeness. It does not require static A completeness or expand A grammar.
Namespace is independently explicit per P/V; no automatic acceptance. Synthetic
positive and refusal cases pass. Actual OASim no-mapping operation still establishes
A2/3, B0; eight sources/48 Direct occurrences are potential B only with sufficient
accepted testimony, absent here. Repository N/coverage remain unknown. Separate
follow-ons16–19 below retain currentness, namespace, parser and evaluated use cases.

### 15. Python/npm positive public namespace authority

**State:** EXPLORE; separate prospective product/trust opportunity, no sibling rewrite.

**Area:** Cross-ecosystem truthfulness

**Opportunity:** Establish and disclose applicable public namespace without treating
public P/V existence as authority for private or conflicting source evidence.

**Evidence:** Current Python exact/freeze and npm/Yarn lock routes use fixed public
adapters without positive namespace verification; npm does not use resolved URL/
integrity for this gate. Ruby has explicit supported public lock-source authority.
The cascade's common floor is a target standard, not a claim siblings already
satisfy its positive namespace requirement. No inspected repository is thereby
claimed private, and no historical measurement is rewritten.

**Success signal:** Separately approved source-authority/migration mechanics improve
truthfulness without guessing acquisition/deployment or breaking released contracts.

**Stop condition:** Copying weaker attribution into NuGet, namesake probing as
permission, scope/metric changes or silent compatibility degradation.

**References:** [Historical cross-ecosystem matrix](discovery/measurement-evidence-parity.md),
[current scope limits](maintenance/measurement-evidence-cascade/spec.md#smallest-cascade-and-ecosystem-scope-c2).

### 16. Repository-contained snapshot acceptance and currentness

**State:** SELECTED; human006-0028 approves qualified current snapshot policy.
Implementation and verification are in [the correction](maintenance/nuget-repository-snapshot/spec.md),
[reviews](maintenance/nuget-repository-snapshot/reviews.md) and
[validation](maintenance/nuget-repository-snapshot/validation.md).

**Outcome:** A remains first, B1 automatically qualifies current repository pairs
using strict literal identity/request/context equality in BOTH directions, then
explicit v3 B2 remains for insufficient automatic facts. Known conflicts cannot be
repaired by testimony. Policy selection claims no historical producing association
or complete evaluated state. Dirty/copied/non-Git coherent inputs are eligible.
Ordinary real-target result: A2/3, B1 8/48, B2 0; accepted N51, measured0, coverage
null because A whole testimony remains unavailable. B1's48 namespace failures
correctly authorize no lookup. Namespace automation remains separate17; parser18,
evaluated use19, CI20 and stronger producer assurance21 remain separate.

**Evidence:** Frozen006-0027 investigation/review preserved in e736736; approved
product decision consciously narrows claim to policy-selected CURRENT pair, not
an automatic equivalent of supplier history. Full observable parity prevents
stale removed/added/extra Direct mismatch, while coherent copied origin remains
unknowable. Current selected versions are recorded snapshot evidence, not restore
success, recency, deployment or namespace.

**Methodology result (one case):** A human gate can scaffold an unknown consequential
trust boundary. After explicit reusable product-policy selection and deterministic
qualification, ordinary runs need not repeatedly ask for the same population
selection. This does not remove independent namespace authority or generalize to
all human gates. Preserve for planned reusable retrospective framework; no framework
is created here.

### 17. NuGet comparator/public-namespace authority

**State:** EXPLORE; frozen006-0029 discovery, HUMAN PRODUCT /
NAMESPACE-AUTHORITY DECISION required. No automatic policy selected.

**Opportunity:** Establish the applicable publication comparator from positive
repository-contained policy, independently of acquisition/content/producer history.
**Evidence:** [Discovery](discovery/nuget-namespace-authority.md),
[all51 occurrence audit](discovery/nuget-namespace-authority-oasim.csv) and
[independent review](discovery/nuget-namespace-authority-review.md). Closed unique winning public mapping may support a deliberately CURRENT
comparator convention; a sole-public repository-only/no-mapping convention needs
separate acceptance because machine default sources can survive repository clear; open inheritance, multiple eligible sources, namesakes and
absence do not. OASim has two additive alternate configs/no mapping and eight
absent configs: zero51 newly authorized. No package queries/ages. Existing explicit
v1/v2/v3 namespace route remains; stronger assurance stays21.

**Separate A-floor opportunity:** A2/3 stops on whole baseline testimony while
B1 8/48 stages selection before namespace. Hidden baseline facts remain real, but
a future current-pair policy could remove unnecessary unrelated admission burden
without pretending to prove them. Requires separate human contract decision;
no A correction, parser18 expansion or evaluated19 execution selected.

**Success signal:** Human-selected precise comparator claim, closed positive source
assignment and private/conflicting negative controls; prospective spec/review before
implementation. **Stop condition:** Public existence/default convention/unknown or
private source substitutes nuget.org, or config is called acquisition history.

**Retrospective input:** Claim decomposition can reveal stronger assurance made an
unnecessary floor; human gates may scaffold unknown boundaries until reusable policy
is deliberately selected. Ordinary-user smoke tests product intent; hosted checks
are asynchronous evidence and do not replace synchronous trust authority. No reusable
retrospective framework created. [Existing cascade](maintenance/measurement-evidence-cascade/spec.md).

### 18. Bounded static C# project parser expansion

**State:** EXPLORE; no expansion selected in006-0026.

**Opportunity:** Review narrowly named ancillary properties/items separately from B.
**Evidence:** Frozen006-0025 reports property-only potential6/16 and narrow None
Update potential7/25. B leaves current A grammar unchanged.
**Success signal:** Separately approved bounded grammar with behavioral witnesses.
**Stop condition:** Arbitrary properties, conditions/import evaluation or count-driven
loosening. **Reference:** [Static alternatives](discovery/nuget-population-basis.md).

### 19. Evaluated MSBuild population use cases

**State:** DEFER; no evaluator or producer execution selected.

**Opportunity:** Investigate genuinely evaluated context needs under separate
human authority. **Evidence:** B claims only a retained accepted snapshot; imports,
conditions, SDK and environment can change current evaluated population.
**Success signal:** Concrete unmet evaluated-state use case and separate execution/
trust authority. **Stop condition:** Consumer CLI executes targets or becomes a
resolver. **Reference:** [Snapshot limitations](maintenance/nuget-snapshot-population/spec.md).

### 20. Hosted action-runtime maintenance observations

**State:** WATCH; no CI implementation selected.
**Evidence:** Human-supplied72dc9a2 hosted checks ultimately GREEN. Recurring
checkout@v4/setup-node@v4 Node20-to-Node24 runtime warning likely belongs to
repository action maintenance. deploy-pages@v5 DEP0040 punycode ownership and
remediation require later investigation. Initial macOS runner exhaustion did not
execute candidate/tests; successful exact-candidate rerun supplies the witness.
**Success signal:** A separately scoped maintenance investigation identifies owned,
necessary action updates. **Stop condition:** Treating warnings as failed checks,
runner exhaustion as flaky tests, or bundling CI changes into population discovery.
**Reference:** [Supplied hosted evidence](maintenance/nuget-snapshot-population/reviews.md#published-candidate-supplied-hosted-evidence--006-0027).

### 21. Stronger NuGet producer assurance

**State:** EXPLORE; no new producer execution selected.
**Opportunity:** Retain accountable historical association/event and content
correspondence evidence separately from qualified current-snapshot population.
**Evidence:** B1 proves no producing history; explicit v1/v2/v3 meanings remain,
and original controlled hash-domain/live-yield limitations are historical evidence.
**Success signal:** Separately authorized, inspectable stronger evidence enriches
assurance without becoming an unnecessary version-age prerequisite.
**Stop condition:** Generating testimony from current hashes, silently assuming
history/source or bundling target execution into the consumer.
**Reference:** [Cascade](maintenance/measurement-evidence-cascade/spec.md),
[qualified policy](maintenance/nuget-repository-snapshot/spec.md).

### 22. Test-suite performance profiling

**State:** WATCH; no optimization selected.
**Evidence:** Supplied exact b449c5d Windows full suite ran751 tests in159.702s,
with51 expected skips and worker3 PASS. This duration is not a diagnosis or evidence
of a candidate defect. **Success signal:** Separately scoped profiling identifies
measured causes before optimization. **Stop condition:** Bundling performance work
into namespace discovery or weakening deterministic/platform witnesses.

## Selected Work Moved into SDD

### 7. Bounded NuGet selected-version evidence

**Selection state:** SELECTED; completed Feature 006 through T018 in run
`006-0017`. This is a completion reference, not active discovery or a new release.

**Outcome:** T017/K6 CONVERGED with36/36 acceptance reconciliation; canonical
retrospective independently APPROVED. Explicit one-project lock/witness support
is implemented. Prospective real-root validation completed with **0/1 measured,
content_hash_mismatch**, correctly withholding publication/age. Useful positive
live yield and general hash-domain fitness remain unestablished. No producer
execution authority transfers to the CLI. Human roadmap selection remains separate.

**Area:** .NET / NuGet

**Contributor fit:** Bounded product discovery and independent review

**Opportunity:** Measure direct NuGet dependency age if supplied project/context
evidence can establish exact selected versions and authorize public metadata.

**Evidence:** A human reports a team outbounding OASim this month. Authorized
initial discovery found ten C# projects, 51 explicit PackageReference
declarations and 24 unique package IDs. The authorized Phase 2 resume produced
assets, oracle JSON and experimental locks agreeing on all 51 direct selections
and 229 transitive occurrences across ten net10.0 contexts. Separate hash-bound
NuGet metadata records public-source provenance for this producing run; retained
selection artifacts alone do not establish source authority. No age/publication
measurement was performed. H3–H4 now accept bound public-origin supplier
assertions plus public hash agreement and catalog-created first-receipt dates.

**Why this state:** The human selected BOUNDED NUGET SELECTED-VERSION EVIDENCE,
grounded in the completed ten-project Phase 2 comparison. Libyears consumes
supported declaration and retained/supplied selection evidence; it does not
perform restore or package resolution. This supersedes EXPLORE and the historical
unselected disposition without rewriting the pre-selection experiment. Human
H1–H4 accept lock-only selection, conservative one-project/framework declarations,
qualified supplier coherence, bound public-origin assertions with public hash
agreement, and first-receipt/listed-latest publication policy. Arbitrary generated
artifacts and public package-name coincidence do not supply authority.

**Success signal:** An authorized project/lock pair with
independently established direct population, producing context and safe
declaration association, plus public-source and publication-date witnesses.

**Stop condition:** Useful scope requires MSBuild/project execution, package
resolution, private-source/credential access, unapproved project aggregation,
or unsupported assumptions about selection, source authority or dates.

**References:**

- [NuGet / OASim pre-selection discovery](discovery/nuget-oasim.md)
- [Feature 006 discovery](specs/006-nuget-selected-evidence/discovery.md)
- [Feature 006 retrospective](specs/006-nuget-selected-evidence/retrospective.md)
- [Convergence and closure](specs/006-nuget-selected-evidence/reviews.md#t018-retrospective-and-closure--006-0017)
- [Prospective validation](specs/006-nuget-selected-evidence/validation-006-0016.md)

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
