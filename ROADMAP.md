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
| [NuGet namespace automation](#17-nuget-comparatorpublic-namespace-authority) | EXPLORE | Namespace authority | Separate evidence investigation |
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
| [Java ecosystem repodive](#11-java-ecosystem-repodive) | SELECTED (007 Maven plural views) | Java contract | Public Maven-first SDD |
| [Plural dependency-age views across ecosystems](#23-plural-dependency-age-views-across-ecosystems) | EXPLORE | Evidence/output semantics | Separate future selection |

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
no interface, migration or generic plugin framework is selected. Java discovery
adds observational evidence below, without an interface experiment.

**Success signal:** A concrete change-history/test-cost map and bounded comparison
show lower maintenance burden with equivalent domain, privacy and failure witnesses.

**Stop condition:** Indirection hides ecosystem rules or supplies no demonstrated
benefit over current explicit boundaries.

**007-0001 evidence:** Java discovery observes source/population/version/comparator
questions; public metadata lookup and Java reporting remain prospective. Maven inheritance and
Gradle configuration/variant scope make a universal source interface premature.
See [analyzer observations](discovery/java-ecosystem-repodive.md#methodology-and-architecture-observations).
No seam/refactor selected.

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
selected solution to the observed mismatch. At this entry's original post006
boundary, no provider research had occurred.

**007-0005 concrete Maven evidence:** One bounded [alternative-age investigation](specs/007-maven-dependency-age/age-evidence-alternatives.md)
examines ecosyste.ms, deps.dev, Libraries.io and Socket. Open adapters/documentation
show modification-time derivations rather than independent publication authority;
deps.dev asserts publication but its Maven derivation remains unestablished.
ecosyste.ms also exposes a separate current version-record creation time; this is
not first-ever observation or Central publication, and its maintenance utility /
historical stability require human judgment. Sonatype cataloging has a distinct
event definition and product API, without an established anonymous public date
route. This use case concretely strengthens provenance/semantics research, not
provider adoption. State remains EXPLORE; no provider is SELECTED. Source caching,
derivation and observation are different trust relationships; schema names alone
do not establish the event. Exact findings and limits are in the linked record.
Human007-0006 rejects provider-row creation for Feature007 product use, retaining
the investigation as evidence. The [final tooling-practice investigation](specs/007-maven-dependency-age/ecosystem-practice.md)
does not reopen provider adoption: independently repeated modification-date use
can support only an explicitly conventional claim, never publication authority.
Opportunity9 remains EXPLORE; no provider is selected.

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

**007-0001 evidence:** Repository lifecycle/baton/frozen review rules transferred
to Java discovery; the prompt still supplied new external/public-only authority,
no-execution boundaries and six review scopes. Missing prior baton remains a real
handoff limit. This is another feature in libyears, not cross-project validation;
no prompt-size or attention saving was measured. Continuation007-0002 recovers
portfolio context without reinventory; new plural product authority, conditional
stage authority and public-only disclosure still required a substantial prompt.
The human reports roughly22K for007-0001; exact comparable prompt measurements
remain absent. Twelve decomposed review contexts closed11 author issues and
rejected unnecessary schema/granularity human gates, leaving one actual source-
policy choice plus technical date evidence. This is not an efficiency or optimal-
reviewer-count claim. In007-0003 the human applies the durable006 evidence-floor
principle to Maven, while technical research separates Maven eligibility/mirrors/
filters and publication events. The principle transfers; the algorithm does not.
Run007-0004 begins in a fresh parent context created by the human/orchestrator
after reported approximately89% context utilization. Durable artifacts recovered
the plural contract, H1 decision, prior corrections and technical stop without
target reinventory. The substantial initiating prompt retransmitted task boundaries,
research questions, review scopes and new telemetry/continuity authority. No material
reasoning loss was identified, but absent methodology cannot be proven absent.
Decomposed date/interface/catalogue/order/variant/cascade reviews make coverage
inspectable; no reviewer-resource or net attention saving is measured. This is a
within-repository handoff observation, not a generalized harness validation.
Run007-0005 continues in the same parent context. Durable negative evidence narrows
research to four credible providers and current cataloging interfaces, rather than
repeating Central's rejected field hunt. New human authority permits alternative
public-provider research and analysis of different claims, but selects neither.
The prompt still retransmits extensive boundaries, questions and review scopes;
net prompt/attention savings remain unmeasured. Decomposed reviews must challenge
both unsupported publication labels and first-observation claims inferred from
database creation timestamps. Version basis versus time basis is retained as
prospective evidence, with no harness/skill or architecture implementation.
Run007-0006 uses those durable negatives to restrict the final authorized rung to
ecosystem practice. New human authority permits assessing a labeled convention,
not reclassifying old dates as publication; provider bookkeeping is now explicitly
rejected for product use. Unrelated implementations, primary versus fallback use,
date-free modernization and observation-based cooldowns must stay distinct in
synthesis. The prompt still carries substantial restrictions/questions; no measured
prompt/context/attention saving or generalized harness result follows. No skill
or tooling framework is implemented.
Run007-0007 starts in a fresh parent at a human product-decision boundary,
recovering the publication-negative/provider-negative/moderate-convention chain
from durable dirty-tree artifacts. New authority selects the conventional POM
Last-Modified claim; technical ordering is agent-resolvable while stable eligibility
remains normative. Extensive prompt retransmission persists, with no comparable
prompt-size/attention series or measured saving. The decision-boundary handoff is
usable here, not generalized harness validation; no harness/SKILL.md is implemented.
Run007-0008 continues that parent with only conservative latest eligibility newly
selected. Durable state avoids repeated portfolio/date/provider/practice research;
source-policy/parser/worker bounds are resolved technically. Fresh whole-specification
review finds collection-admission ambiguity; subsequent focused reviews catch a
residual numeric predicate and nullable-record collateral before final closure.
Plan and sequential tasks independently converge with no new product gate. The
immediate next human authority is implementation; live public/private validation
remain separate future gates. The extensive prompt and two internal concern-scope
clarifications show continuing retransmission burden; no measured attention savings
or fresh-parent causal benefit follows. No generalized harness or SKILL.md is built.
No shrinking burden or cross-project generality is established. See the
[discovery observations](discovery/java-ecosystem-repodive.md#methodology-and-architecture-observations).

**007-0016 recovery and authority observation:** Reviewed-graph authority/state
survived publication, reboot and fresh-parent recovery. The original007-0014 ephemeral
observation baton did not survive the human-confirmed reboot; no original fields or
row were reconstructed. Public candidate-root knowledge required human factual
recovery. GPUBLIC separately supplied real target/network/disclosure authority;
T013→T014 progression required no routine next-task approval. Hosted evidence retains
human provenance and native-capability skip limits. No real-target implementation
defect or new product decision arose; approved budget/extension refusals preserved
useful partial facts with zero requests. Operational location/temporary bytes were
missing despite durable normative authority. No new compaction, cross-project
generality, quantified savings or generalized harness/SKILL is claimed. See the
[retrospective](specs/007-maven-dependency-age/retrospective.md).

**Why this state:** Reusable practice merits evaluation, not a selected tool,
mandatory premium-model workflow or immediate skill implementation.

**Success signal:** Another authorized project preserves equivalent quality and
human authority with measured coordination/maintenance burden and accessible routing.

**Stop condition:** Packaging adds more administration than value, cannot preserve
repository-specific authority, or relies on unobserved resource claims.

**References:** [SDD_WORKFLOW.md](SDD_WORKFLOW.md), [Feature 005 retrospective](specs/005-gemfile-group-scope/retrospective.md), [Feature 006 retrospective](specs/006-nuget-selected-evidence/retrospective.md).

### 11. Java ecosystem repodive

**State:** SELECTED; Feature007 COMPLETE through independently converged T014 at
the reviewed pre-publication boundary. Earlier states below retain the selection
and decision history; no release, push or private validation is implied.

**Area:** Java discovery

**Contributor fit:** Human-requested bounded investigation

**Opportunity:** A future bounded Java ecosystem repository investigation to identify
actual direct declarations, retained selection and source/publication evidence.

**Evidence:** Authorized discovery007-0001 inspected seven public CMSgov clones:
four Maven-only, two Gradle-only, one mixed. Sixty-five project POMs contain864
written dependency elements (not an accepted denominator); AB2D retains20 Gradle
locks with configuration-specific selections but no directness/source attribution.
See the [repodive](discovery/java-ecosystem-repodive.md) and
[independent review](discovery/java-ecosystem-repodive-review.md).

**Why this state:** The human selects two independent views, declared and observed,
with external direct module-qualified occurrences, DPC primary and AB2D adversarial.
Initial Maven observed evidence may be unavailable; never substitute declarations,
add the two totals or retrofit siblings. Independent specification/correction reviews
close11 author issues and support additive schema3, not a new schema authority gate.
Human007-0003 resolves H1=NO: mere alternate/file eligibility is not a Central
comparator veto. The claim-specific cascade retains positive contrary refusals and
separate acquisition/content assurance. [T1 research](specs/007-maven-dependency-age/publication-history.md)
did not establish suitable public release-publication date authority. Four changed-
area independent reviews approve the bounded evidence stop/cascade, with no material
findings; whole specification remains unapproved. No plan/tasks or implementation
started. H1 is resolved; the current blocker is technical date authority, not a new
comparator vote. See the linked review record for the exact missing evidence bridge.
Dedicated007-0004 research also fails to establish an authoritative public historical
publication/availability timestamp binding. Catalogue and named ordering evidence
are retained; stable eligibility/latest admission remain unapproved. Stop for human
product direction: defer Java, authorize investigation of a different truthful date
claim, or another bounded direction. No proxy metric or implementation is selected.
The human007-0005 accepts that result and commissions the linked
[alternative-provider/date investigation](specs/007-maven-dependency-age/age-evidence-alternatives.md).
Public provider record creation is a narrower available fact for human evaluation;
no provider or time basis is selected, and publication T1 remains open.
Human007-0006 rejects row creation and authorizes the final
[ecosystem-convention rung](specs/007-maven-dependency-age/ecosystem-practice.md).
An explicitly conventional POM-date candidate now awaits human selection; it is
not authoritative first publication. Specification approval, plans/tasks and
implementation remain unstarted; no additional timestamp hunt is selected.
Human007-0007 now selects that narrower conventional basis, consciously leaving
publication authority unestablished. [Latest-policy alternatives](specs/007-maven-dependency-age/latest-policy.md)
isolate conservative unknown-refusing versus broad unknown-admitting eligibility;
pinned Maven precedence and current GA catalogue are technical contract decisions.
Specification remains blocked for that human policy choice, with technical source-
policy/budget completion still required before approval. No plan/tasks/implementation.
Human007-0008 selects conservative eligibility: unknown below maximum is harmless;
unknown at/above maximum refuses. Bounded source policy and metadata transport are
complete. Fresh whole-specification review plus focused correction closure approves
the specification; [plan](specs/007-maven-dependency-age/plan.md) and
[sequential graph](specs/007-maven-dependency-age/tasks.md) independently approve.
All implementation tasks remain NOT STARTED. No runtime/target/private authority
follows; exact next human gate is T001 implementation authorization.
See [human decision](specs/007-maven-dependency-age/discovery.md),
[specification draft](specs/007-maven-dependency-age/spec.md) and
[approval/gates](specs/007-maven-dependency-age/reviews.md).

**Success signal:** Human-selected truthful ordinary journey supported by the
observed evidence; no resolver execution inside libyears. Declaration versions
must never silently become selected-version claims.

**Stop condition:** Unapproved target/registry access or execution, false joins or
combined view arithmetic, unresolved consequential source/schema/date policy, or
implementation without separate authority.

**References:** [Feature 006 retrospective](specs/006-nuget-selected-evidence/retrospective.md#what-we-would-do-differently-and-human-handoff).

**007-0016 public reality:** [Actual ordinary DPC validation](specs/007-maven-dependency-age/validation.md)
retains nine safe sources/179 occurrence records/36 exact request facts after the
256-directory discovery bound, with unknown N/coverage, zero measured ages and
independent unavailable Observed. Nonempty extension evidence denies all comparison;
zero capabilities/requests/disclosures, unchanged clean exact discovery revision.
Fresh useful-journey/security reviews APPROVE. No target repair, relaxed policy,
private access or positive live date-fitness claim. Final
[convergence](specs/007-maven-dependency-age/convergence.md) and
[retrospective](specs/007-maven-dependency-age/retrospective.md) preserve the evidence
and remaining pre-publication boundary.

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

**State:** SELECTED in006-0030 under explicit conditional human direction.
Frozen006-0029 evidence830a19c remains historical; narrow
[investigation](discovery/nuget-conventional-comparator.md) and
[independent review](discovery/nuget-conventional-comparator-review.md) approve a
consciously conventional public reference with namespace correspondence assumed,
not independently established. Effective external configuration remains uninspected.

**006-0030 contract (superseded only by the correction below):** [C1–C6](maintenance/nuget-conventional-comparator/spec.md)
retains exact testimony and closed unique public mapping, then conventional
nuget.org comparison only absent contrary assignment/ambiguity. Enabled alternate/
local feeds without assignment remain ambiguous; no mirror/private inference.
Private/conflicting/unknown policy never reaches public lookup. Public namesakes
never grant authority. Stronger acquisition/content/producer facts stay separate21.

**A-floor:** Add ordinary no-witness qualified current-pair route retaining
A declaration population and strict whole-lock/ID/request/context qualification.
No fake hidden-baseline assertion; old precision/witness semantics preserved.
Parser18, evaluated19, CI20 and performance22 remain separate.

**Acceptance:** Independent spec/plan/graph and implementation/convergence before
first real OASim metadata attempt. Historical audit predicts33 no-config candidates
and18 alternate-source ambiguities, never a promised33/51 or51/51 measurement.
**006-0030 ordinary result:**33/51 measured,64.7059% coverage,26.5508747945
measured-subset libyears; all33 conventional comparator lookups succeed.18 remain
alternate-source ambiguity, not registry failures. A2/3+B1 8/48+B2zero retained,
OASim exact before/after unchanged. Full [validation](maintenance/nuget-conventional-comparator/validation.md)
and51-row result retained. Runtime locally converged after two reviewed corrections;
publication security gate historically remained one unsuppressed GitLeaks prose false positive.

**Methodology:** Use the lowest sufficient truthful evidence floor for the stated
age claim. Stronger evidence enriches assurance rather than automatically becoming
its minimum. Product policy selects a reference; it does not reconstruct history.
Human gates may scaffold unknown boundaries; ordinary-user smoke supplies product
acceptance evidence and hosted checks remain asynchronous. Partial coverage is
preferable to fabricated completeness. No retrospective framework created.

**006-0031 security and alternate-source investigation:** Exact security maintenance
is separately resolved in `e78b228` with the two explicitly approved historical
prose exceptions; canonical committed gate319commits PASS, no broad suppression
or history rewrite. See [security evidence](maintenance/gitleaks-exact-exceptions-006-0031.md).
The [final18 investigation](discovery/nuget-alternate-source-comparator.md) finds
byte-identical project-local AvaloniaCI/MyGet HTTPS additions, described as an
unstable-package CI feed, with no mapping/disable/clear or public-identity assignment.
Mirror/private/mixed namespace role remains UNKNOWN; all nine repeated identities
have no contrary package-specific repository evidence observed, never proved public.
006-0031 offline staging retained N51/33 capabilities/18 ambiguity refusals; no new
live measurement or comparator behavior. The latest real result remains006-0030.
Allowing unassigned alternate HTTPS eligibility under a positive-contrary-only rule
requires **HUMAN PRODUCT / ALTERNATE-SOURCE COMPARATOR DECISION**: accept or retain
refusal of observed competing-history ambiguity, separately from acquisition proof.
Existing exact testimony/mapping routes remain available; no target evidence is
fabricated. Stronger assurance21, parser18, CI20, performance22 and methodology10
remain separate; no retrospective framework or ancillary maintenance implemented.
Independent discovery review and exact target integrity are in the companion
[review](discovery/nuget-alternate-source-comparator-review.md).

**006-0032 human decision:** Explicitly SELECTED bounded positive-contrary-evidence
public comparator policy, accepting undisclosed private same-ID/version fork/history
risk and public identifier disclosure. Unassigned acquisition-source eligibility
alone is no comparator veto; positive assignment/exclusion/conflicting testimony/
unknown package-specific semantics remain terminal. No acquisition/content/history
claim. The [prospective correction](maintenance/nuget-positive-comparator/spec.md)
specification, plan and sequential task graph are independently approved; P1 runtime
and deterministic verification complete; independent pre-live convergence COMPLETE.
Actual ordinary human/JSON: **51/51 measured,100% coverage**, total51.77572640368723,
mean1.015210321640926,median1.3155551897482698,max3.630960922059979. All51
conventional_public_policy results usable,zero registry failures; all18 formerly
ambiguous rows authorized under the new human-selected policy. No alternate/private
endpoint contacted; exact target before/after equality. Full
[validation](maintenance/nuget-positive-comparator/validation.md) retains dates,
51-occurrence CSV and review limits. Security remains separately green with exact
exceptions. Independent operational closure is recorded in the correction reviews. Stronger assurance/parser/
CI/performance/retrospective work remains separate; no sibling semantic change.

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

**State:** WATCH for upstream managed Pages warnings; owned action maintenance
completed in006-0035; published1cd937f hosted evidence subsequently supplied
by the human (see the housekeeping follow-up). Ubuntu26 migration is upstream WATCH.
**Evidence:** Human-supplied72dc9a2 hosted checks ultimately GREEN. Recurring
checkout@v4/setup-node@v4 Node20-to-Node24 runtime warning likely belongs to
repository action maintenance. deploy-pages@v5 DEP0040 punycode ownership and
remediation require later investigation. Initial macOS runner exhaustion did not
execute candidate/tests; successful exact-candidate rerun supplies the witness.
**Success signal:** A separately scoped maintenance investigation identifies owned,
necessary action updates. **Stop condition:** Treating warnings as failed checks,
runner exhaustion as flaky tests, or bundling CI changes into population discovery.
**Reference:** [Supplied hosted evidence](maintenance/nuget-snapshot-population/reviews.md#published-candidate-supplied-hosted-evidence--006-0027).

**006-0035 bounded outcome:** Repository checkout uses now pin supported v7.0.1;
Tier2 setup-node pins v7.1.0, with Node22/uncached tooling preserved. **FIXED**
locally after fresh independent executable review. Managed Pages punycode and
upload-artifact runtime warnings are **UPSTREAM / MONITOR**, not candidate failures.
Reconsider on a relevant supported upstream fix or actual deployment failure;
no repository Pages redesign. Exact ownership, compatibility, hosted results and
limits are in [the housekeeping record](maintenance/post-006-housekeeping.md).

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

**006-0035 bounded outcome:** **UNDERSTOOD / DEFERRED**. Public metadata isolates
the dominant Windows delay inside the offline test step, rather than queue/setup.
Local profiling demonstrates a deliberate five-second worker negative witness and
771 native TLS context constructions across92 Ruby tests; Windows trust-store
cost remains a hypothesis, not an established root cause. No accidental wait was
demonstrated, so no optimization. Reconsider with exact-candidate Windows per-test,
TLS/subprocess/filesystem timing or recurring pressure on the20-minute budget.
Retain native capability/refusal witnesses. [Profile and limitations](maintenance/post-006-housekeeping.md#3-runtime-disparity--understood--deferred-optimization).

The same one-time sweep **FIXED** incidental CLI fixture output in three tests and
**RECONCILED** published product/methodology/documentation hosted evidence. No
further cleanup or Feature007 work is selected by that closure.

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

### 23. Plural dependency-age views across ecosystems

**State:** EXPLORE; no sibling contract or implementation selected.
**Opportunity:** Investigate independent declared and retained-evidence age views
outside Feature007. **Evidence:** Human007-0002 selects plural Maven views; the
[applicability table](specs/007-maven-dependency-age/discovery.md#methodology-and-prospective-applicability)
finds reusable fact/availability distinctions but ecosystem-specific scope/joins.
**Success signal:** Separately authorized real evidence supports a useful second
view without false joins, hidden defaults, duplicate totals or rewritten existing
fields. **Stop condition:** A conceptual analogy is treated as implementation or
public-namespace authority. No universal aggregate/analyzer is implied.

## How Opportunities Move

WATCH -> EXPLORE when evidence justifies bounded investigation.

EXPLORE -> SELECTED only after human product approval.

Any state -> DEFER when evidence shows the opportunity should not currently be
pursued.

SELECTED work moves into `specs/NNN-...` for SDD.

Movement should be preserved in Git history with a concise rationale. Items may
remain unchanged for long periods. The radar is deliberately selective.

## Post-Feature006 methodology boundary

The [post-feature retrospective](specs/006-nuget-selected-evidence/methodology-retrospective.md)
and [next-feature methodology handoff](specs/006-nuget-selected-evidence/methodology-handoff.md)
reconcile the journey through published `0eabe303…`. They select no new ecosystem.
At that retrospective boundary Feature007/Java was unstarted; human roadmap
selection and next-stage authority remained required. Cross-cutting actor guidance
lives in AGENT_ROUTING.md.

Java discovery007-0001 subsequently reconciled the published housekeeping boundary
1cd937f using explicitly supplied human hosted observations. Bounded public Java
discovery completed without selection in007-0001. Human007-0002 subsequently
selects Maven-first plural views for specification under the linked feature record.
The historical handoff remains evidence of its earlier state.
