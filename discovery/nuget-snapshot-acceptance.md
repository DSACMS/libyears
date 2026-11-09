# What explicit snapshot acceptance supplies — 006-0027

Discovery only, exact published starting candidate
`72dc9a28d46f117e6786a29afe8b42f9a4596001`, initially clean. Disposition lives in
[the independent review record](nuget-snapshot-acceptance-review.md). No new
population authority, specification, plan, task graph or implementation is approved.

## Decision presented

Explicit v3 acceptance supplies **accountable snapshot association and scope
assertions plus permission to use that interpretation**. It does not supply
missing selected versions. Computing current digests supplies byte binding, not
those assertions. Currentness of evaluated MSBuild state is explicitly outside B;
removing that imaginary requirement would not remove the actual acceptance gate.

The gate is partly objective, partly supplier knowledge and partly product policy.
It is neither wholly inherent human judgment nor wholly redundant scaffolding.
Repository bytes can establish the narrower facts described below. They cannot
prove that this lock was actually produced for these project bytes or that an
uninterpreted evaluated graph had exactly the asserted explicit population.
V3 does not demand a producer event, but accepting a supplier's assertion of
coherence remains different from proving it or choosing an artifact by policy.

**Recommendation for human consideration:** retain P0 today. Consider a new,
strict repository-represented snapshot route P7 inside P6, using positive literal
population equality rather than P2's one-way known-conflict checks. Such a route
would choose the current attributable colocated pair as the measurement snapshot
by product policy; it would not discover a historical producing association.
Whether that is sufficient for B is the new human trust/product decision. Do not
claim P7 already establishes every fact currently delegated to a v3 supplier.
If actual accountable producing association remains necessary, retain explicit
acceptance or separately accepted retained producer evidence. No evidence here
establishes an automatic substitute for that stronger interpretation.

## Governing evidence and preserved history

Read together: Feature006 [S2–S4](../specs/006-nuget-selected-evidence/spec.md),
[project/association plan](../specs/006-nuget-selected-evidence/plan.md), its review
history and original producer/validation records; repository-source
[occurrence contract](../maintenance/nuget-repository-sources/spec.md);
[parity discovery](measurement-evidence-parity.md) and review;
[approved cascade C1–C4](../maintenance/measurement-evidence-cascade/spec.md);
[population discovery](nuget-population-basis.md) and
[review](nuget-population-basis-review.md); snapshot
[specification](../maintenance/nuget-snapshot-population/spec.md),
[plan](../maintenance/nuget-snapshot-population/plan.md),
[tasks](../maintenance/nuget-snapshot-population/tasks.md),
[implementation validation](../maintenance/nuget-snapshot-population/validation.md)
and [reviews](../maintenance/nuget-snapshot-population/reviews.md).

Current code audited: nuget_project, nuget_lock, nuget_population,
nuget_provenance, nuget/read_nuget_source, nuget_sources and repository composition;
Python snapshot intersection, npm manifest/lock association and Ruby source/direct
selection. V1 retains producer/native-origin/event and baseline meanings. V2
removes event/content requirements but retains A baseline and explicit namespace.
V3 is B-only: no A baseline prerequisite, no historical event requirement, new
snapshot external-Direct-completeness assertion. All versions require explicit
selection; none authorizes automatic acceptance. The completed cascade and B
selection are not reopened; original refusals/evidence remain historical.

## V3 decomposition

Classes: A objective local; B derived coherence; C historical/producer knowledge;
D intent/policy; E namespace; F stronger assurance; G other. Multiple classes in a
row identify distinct clauses, not an indivisible witness. “Necessary” describes
the logical claim, not a requirement to keep this exact JSON representation.

| V3 field / assertion | Claim protected | Class | Locally establishable / evidence | Stale or conflict risk | Population necessary? | Stronger assurance necessary? | Namespace necessary? | Human judgment actually required? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| version = integer 3, exact keys/types/bounds/duplicate refusal | Interpret the intended B contract unambiguously | A/G: contract discriminator | Yes, strict JSON parser | Wrong contract/ambiguous JSON refuses | Yes, some unambiguous route | No | No | No factual judgment; policy chooses route |
| project immediate filename; explicit root-relative mapping | Attribute occurrence to a source | A + D | Reader/discovery establishes current path; mapping selects it | Shared parent/copied lock does not identify its producer | Yes | Not event proof | No | Automatic deterministic attribution possible only under new policy |
| framework | Name the one accepted snapshot context | A/B + D | Sole literal lock key; known project literals compared | Conditional/computed/changed contexts may escape partial extraction | Yes | No reproducibility proof | No | Context choice can be policy; evaluated context is not proven |
| project_sha256 | Exact project bytes accepted | A/B | Compute exact bytes and compare supplied digest | Freshly hashing stale pair binds the stale pair; old witness catches byte changes | Yes, exact association; hash representation optional | Useful, insufficient | No | No |
| lock_sha256 | Exact whole lock bytes accepted | A/B | Same as above, whole accepted lock | No timestamp/producer identity in digest | Yes, exact association | Useful, insufficient | No | No |
| coherent_snapshot = true: these bytes belong together | Accountable association for named retained snapshot | D plus supplier knowledge; C only if justified by actual producing history | Local agreement corroborates; bytes alone cannot recover actual producing relationship | Identical-domain copied lock; hidden input changes | Yes under current P2 | Historical producing proof is stronger and optional | No | Supplier needs an accountable basis now; replacing it with artifact-selection policy needs human authority |
| explicit_external_direct_complete = true: all Direct are explicit external | Exclude SDK implicit packages, project nodes, closure and unintended populations | B for literal membership; supplier knowledge for unobserved scope; D acceptance | Lock distinguishes Direct/Transitive/Project, but Direct alone does not certify written explicit origin; full literal equality positively anchors every included ID | Extra stale/implicit Direct can pass current one-way probe | Yes | No acquisition/content consequence | No | Not inherently for visible exact equality; unknown scope still needs sufficient evidence/acceptance |
| same completeness assertion: complete for accepted framework snapshot | Whole snapshot population, not partial salvage | A/B for all records in whole lock; supplier knowledge/D for semantic completeness | Enumerate all Direct; cannot prove evaluated graph omitted nothing | Hidden MSBuild/SDK/import influences; old coherent snapshots | Yes; never substitute partial known list | No current evaluated completeness requirement | No | Cannot assert unknown remainder from partial parsing; a new narrower policy must state what it chooses |
| packages array (may be empty), per-record id and version | Bind optional namespace assertions to exact selected P/V; refuse aliases | A/B | Validate records and selected identity association | Wrong/missing P/V never grants capability | Not needed; empty valid | No | Binding needed when claiming namespace | No identity judgment |
| packages[].namespace | Applicable public publication namespace for that P/V | E + D; sometimes supplier history | NOT from project/lock/hash/name/public existence; current accepted testimony independent | Private namesakes, unknown/conflicting source | No | Does not imply acquisition/content | Yes before lookup | Existing explicit namespace authority unchanged; not investigated for automation |
| explicit CLI acceptance itself | User accepts supplier assertions and selects interpretation | D | Invocation is observable intent; repository file presence is not that intent | Auto-discovery would silently change authority | Required by current contract | No | Separate explicit records still needed | Product can replace selection only through new human decision |
| absent producer/event/content/deployment/reproducibility fields | No such claims in v3 | F (excluded) | Cannot infer them from digests, Git, colocation | Mistaking snapshot for deployment/history | No | Needed only if independently claiming those facts | No | Not a reason to require new attestation for age |
| no current evaluated completeness assertion | B retained snapshot limitation | F/G (excluded stronger claim) | No evaluation performed | Same-byte imports/environment can differ | No | Needed for stronger current/evaluated claim only | No | Not supplied even by present v3 |

Thus the missing categories are **information about semantic association/scope
where local facts do not suffice, intent, and trust/policy authority**. Binding
is already mechanically available. Historical information may ground a supplier's
assertion but is not mandatory v3 event testimony. Evaluated currentness is neither
available nor supplied by this gate. No category substitutes for namespace.

## Repository evidence: what it buys

1. **Colocation:** conventional candidate location, not project identity inside the
   lock, freshness, explicit origin or accountable association. Several projects
   can share a parent. P1 is insufficient.
2. **Exact bytes:** a reproducible measurement basis for this read, resistance to
   substitution against a preexisting accepted digest. Fresh digests provide no
   independent acceptance, chronology or assurance that these bytes ever met a
   producer. P3 adds inspectability/revalidation to P2, not semantic information.
3. **Project/lock coherence:** equal literal IDs and normalized requests are positive
   facts about visible declarations and recorded Direct records. A matched sole
   framework is a positive context check. Neither proves current MSBuild evaluation.
   Current snapshot_population checks known project IDs against Direct in one
   direction; lock-only IDs may be accepted by testimony. Selected versions must
   be supported lock identities; matching requests is not solving request
   satisfaction. No general resolver/range checker is proposed.
4. **Partial knowledge:** yes, safe literal facts remain useful cross-checks after
   A fails on unrelated syntax. They must not become a partial denominator or A
   completeness. Positive equality can show every recorded Direct ID is explicitly
   written; it cannot reveal an import adding an unrecorded dependency or prove a
   written item survived evaluation. P7 must qualify the accepted snapshot claim.
5. **Git:** a commit associates stored blobs in a tree; a history can identify
   recorded byte changes. Co-commit, “lock newer,” HEAD membership and clean status
   are not restore/build chronology. Author/commit dates are not authenticated
   production clocks. Current worktree bytes, not HEAD alone, must be bound. An
   unchanged tracked project plus untracked lock has no commit-based pair witness.
   Dirty unrelated files need not invalidate a byte-bound snapshot. No Git is a
   legitimate deployment context. Git may enrich optional chronology; it cannot
   discharge the missing assertion and should not be mandatory.
6. **Retained producer evidence:** durable Phase2 account records exact project
   inputs, ten restores/oracles/locks, 51 explicit/Direct agreement and 92 closure
   native source/hash records. Those are useful historical corroboration, not
   independent resolver implementations. Raw experiment bundles were temporary,
   outside the target and are not reread or assumed available in this run. Current
   target retains ten locks, ten ignored assets filenames, and one Updater v1
   witness. Assets are not approved population/namespace product inputs. No asset,
   cache or configuration contents were opened. Updater v1 binds current project/
   lock/framework; it is still unselected and cannot become v3 or sibling authority.
   A signed or accountable retained association could be a future P5 route only
   under explicit acceptance policy; a discoverable file is not self-authenticating.
7. **Lock self-description:** whole schema1/sole literal framework, typed records,
   canonical requested minimums and supported resolved identities can be checked.
   Direct is a restore graph classification, not proof of explicit csproj authorship.
   No project-name/digest, effective source, restore date or provenance appears.
8. **Other present evidence:** filenames, mtimes, source-control state and retained
   summaries support inspection, not authority. Do not inspect imports/ancestors
   or invent generated state. No additional ordinary artifact closes this gap here.

Microsoft documents dependency-change lock regeneration and locked-mode refusal,
SDK implicit PackageReferences, and per-framework graphs. This supports treating
staleness and implicit scope as concrete risks; it does not authenticate a supplied
lock. [Official PackageReference documentation](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files#locking-dependencies).
The current documentation also discusses newer schema features; existing schema1
bounds remain unchanged. No locked-mode command was executed.

## Policy comparison and adversarial cases

P4 below is deliberately concrete: require both exact current blobs tracked in
HEAD, a co-commit association and no subsequent relevant byte change. Even this
cannot establish production; a weaker Git predicate cannot do better. P5 means
sufficient accountable retained binding/scope evidence, not an old prose mention.
P6 inherits its constituent policy's limits; no “strongest” route overrides a
known contradiction. Preserve accepted stronger evidence separately, without a
universal assurance ladder.

| Policy | Truthfulness and failure risks | Usability / burden / complexity / parity |
| --- | --- | --- |
| P0 explicit v3 | Current approved supplier association/scope, not authenticated truth; stale false testimony remains possible | Human burden; no Git requirement; existing cross-platform reader safety; strictest acceptance mechanics |
| P1 colocation | Valid format alone accepts stale additions/removals/requests/context, copied and unrelated locks; no explicit-only assurance | Easiest, simple and non-Git; insufficient NuGet evidence |
| P2 local coherence | Current B structural checker catches visible additions/request/framework conflicts, not extra Direct/removed refs or hidden influence; no producing association | Useful cross-check, no Git; insufficient replacement for all v3 assertions |
| P3 P2 + current byte binding | Same semantic false acceptances as P2; hashes retain exact basis and detect later substitutions against it | Small cost, inspectable/platform neutral; no new information about truth |
| P4 P3 + Git predicate | Records tree chronology, still accepts a co-committed stale/copied coherent pair; refuses untracked pairs and non-Git inputs | Poor OASim yield, complexity/history availability cost; unjustified mandatory Git dependence |
| P5 retained producer evidence | Can establish specific accountable historical pair/scope if exact evidence actually available and accepted; still not evaluated currentness | Potential strongest association, high producer/trust/format burden, not general ordinary-file policy; current old summary not sufficient |
| P6 hybrid A -> repository B -> attested B -> unavailable | Useful only if repository B independently justified; A failure other than supported-grammar refusal must never trigger fallback; conflicts never bypassed | Good ordinary usability, moderate new route complexity; A later namespace failure still cannot become B |
| P7 positive literal parity + byte-bound repository interpretation | Require all written package refs extractable as unconditional literal identities/minima, unique IDs, exact bidirectional equality to all Direct, sole matching literal framework, safe whole evidence; refuse known package/context mutation constructs and ambiguous project attribution. Stops visible stale/implicit extras; indistinguishable copied pair still possible | Best narrow candidate for policy-selected represented snapshot; no Git, human file or evaluation required; no A completeness claim. Ancillary unsupported syntax can remain uninterpreted. New extraction/refusal rules need prospective spec/review, not a general parser expansion |

P7's proposed claim is precise: **“For this current repository project/lock byte
pair and sole framework, policy selects the lock-recorded Direct versions as the
measurement snapshot; every included package is also an unconditional literal
explicit reference with matching request. Current evaluated completeness and
historical producing association are unestablished.”** This is narrower evidence
than supplier-asserted coherence, not a redefinition of existing v3. Human approval
must determine whether it is sufficient to instantiate B, or whether a distinct
prospective association qualification is necessary. Output/schema design is deferred.

A proof of production cannot be recovered by relabeling policy selection as
“coherent_snapshot=true.” Do not manufacture witnesses. For unknown/computed
references P7 refuses, leaving explicitly accepted B available if sufficient.
Unknown external SDK/import state remains outside the represented snapshot claim;
no automatic route may advertise it as evaluated completeness. An unrelated
unknown property is not itself proof of a hidden dependency or a contradiction.

The following are deterministic counterexamples, not real OASim modifications.
Private probes execute current pure parsers and a discovery-only P7 predicate.
P1 means supported whole lock and safely framed project; P2 is current B conflict
probe; P3 computes current identities, so has identical admission. P7 predicates
are exploratory, not a production-ready specification. Independent review found
two child-element omissions in the first exploratory probe: conflicting nested
Version and a nonsimple framework node. Corrected private probes refuse both;
strict existing reference/metadata checks and simple framework checks independently
pass every actual target pair. Prospective rules must still cover unknown/duplicate
metadata, mutation attributes, root/group conditions and all unsafe framing.

| Case | P1 | P2/P3 | P7 | P0 / P4 / P5 / P6 implications |
| --- | --- | --- | --- | --- |
| 1 all visible facts agree | accepts | accepts | accepts | P0 still needs testimony; Git/producer can enrich, not prove evaluated state |
| 2 literal added, missing Direct | false accept | refuses | refuses | Known contradiction defeats all legitimate routes |
| 3 literal removed, old Direct retained | false accept | accepts under testimony | refuses | P0 may still be truthful for independently accepted explicit historical scope; automatic current pairing needs reverse check; Git co-commit alone can be stale |
| 4 request changed | false accept | refuses | refuses | Same selected version does not repair request conflict |
| 5 target/computed syntax changes refs invisibly | false accept for current claim | may accept under testimony | refuses known local mutation/unextractable refs | Invisible imported/SDK mutation can pass all local tests; none may claim evaluated currentness; accepted historical snapshot may remain meaningful |
| 6 copied lock with different IDs/requests/context | false accept | refuses detectable differences, accepts extras | refuses differences | No route may bypass visible conflict |
| 6b copied lock identical on relevant facts | accepts | accepts | accepts | No bytes-only predicate can distinguish original and copied same-domain artifact; P4 also cannot authenticate origin; P5 or accountable testimony needed if origin matters |
| 7 changed framework | false accept | refuses known literal mismatch | refuses mismatch/unknown context | Conditional hidden context may escape P2; no whole multi/RID context salvage |
| 8 valid pair, no trustworthy producing association | accepts | accepts | accepts only as policy-selected representation | This is the central new decision, not evidence of production; P0/P5 need an actual accountable basis |
| 9 no Git | accepts | accepts | accepts | P4 refuses; other routes do not acquire or lose production truth because Git is absent |
| 10 dirty repository | accepts | current bytes checked | current bytes checked | Relevant visible conflict refuses; unrelated dirt irrelevant; P4 refuses relevant HEAD mismatch; no cleanup permitted |
| 11 conflicting Version child / 12 nonsimple framework child | accepts | may defer to testimony | corrected exploratory probe refuses | Future strict extraction must reject these; initial private predicate omission was discovery scaffolding, not a production defect |

P7 does not eliminate same-domain copied/stale selected-version risk. A lock with
matching request but arbitrarily old supported resolved version can pass; current
contract checks neither resolution nor request satisfaction, and even a satisfied
minimum cannot prove recency. This is acceptable only for an explicitly qualified
recorded snapshot policy, not evidence of successful restore or actual current use.
P6 inherits this, with P0 as fallback only for eligible unsupported syntax, never
to override known conflicts. Stale outside-project inputs can change evaluated
state with identical project and lock bytes; v3 itself never guaranteed otherwise.

## Ten-project application

Baseline captured before target reads: HEAD
`1e937015e1d242fee5597ea0fbdc4cd5c983f101`; 223 tracked, 12 nonignored untracked,
50 ignored inventory entries. All ten projects equal HEAD blobs. All ten locks
are **untracked with no path history**, so “committed together” and “lock after
project commit” cannot be established. Mtime is not used as producer chronology.
All twenty current project/lock byte digests equal the retained 006-0026 baseline.
Existing dirty state is preserved; it is not a clean-repository witness.

Every row has schema1, sole net10.0, supported Direct requested/resolved identities,
exact case-insensitive literal/Direct ID equality, normalized request equality,
no conditional/computed written PackageReference, no known contradiction, and
no current explicit witness selection. Available evidence for every row is the
attributable project, colocated untracked lock, byte identities, literal equality,
HEAD project blob and prior retained experiment account. This common evidence
and common remaining uncertainty apply individually to all ten rows: no actual
producing association/current evaluation/namespace follows. Updater additionally
has current-byte-compatible retained v1 testimony, still not selected. No v3
acceptance is found or created.

All paths below are under SRTRMatchRunApplication, with project name as directory
and basename. “Eligible” is structural, not accepted population. P1/P2/P3/P7 show
counterfactual structural policy results; A always wins on its two supported rows.
P4 refuses each untracked lock; P5 supplies no automatically admissible v3 route.
P6 uses proposed P7 only after eligible A failure. A status comes from the current parser; inspected unsupported constructs are
corroborated against current bytes and the frozen0025 audit. The parser returns
only an unsupported category, not a first-form diagnostic; no new grammar authority
follows. Strict existing reference parsing, framework framing and local mutation
inspection independently confirm these ten counterfactual P7 results.

| Project | A status / inspected unsupported forms (not parser diagnostics) | Lock Direct / B structural | Explicit B now | P1/P2/P3 | P4 | P5 automatic | P7 / P6 proposed result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MRCalc | unsupported: ApplicationIcon and other assembly/application properties; conditional output and resource/item forms | 9 / eligible | absent | would accept B | refuse | refuse | would accept B9: full literal parity |
| MatchRunBenchmarks | unsupported: StartupObject, CopyLocalLockFileAssemblies | 2 / eligible | absent | would accept B | refuse | refuse | would accept B2: full literal parity |
| MatchRunCLI | unsupported: ApplicationIcon, assembly/version/startup properties; conditional output and None Update | 8 / eligible | absent | would accept B | refuse | refuse | would accept B8: full literal parity |
| MatchRunEngine | unsupported: AssemblyVersion, FileVersion, Version | 4 / eligible | absent | would accept B | refuse | refuse | would accept B4: full literal parity |
| MatchRunProfileUpdater | supported A1 | 1 / structurally valid, B precedence-ineligible | absent; v1 retained unselected | A precedence | B not attempted | no new authority | retain A1, existing whole evidence still unavailable |
| MatchRunProfiling | supported A2 | 2 / structurally valid, B precedence-ineligible | absent | A precedence | B not attempted | refuse | retain A2, existing whole evidence still unavailable |
| MatchRunTests | unsupported: IsPackable | 5 / eligible | absent | would accept B | refuse | refuse | would accept B5: full literal parity |
| OASim | unsupported: ApplicationIcon and other assembly/application properties; conditional output and resource/item forms | 9 / eligible | absent | would accept B | refuse | refuse | would accept B9: full literal parity |
| OASimCLI | unsupported: Version; None Update | 9 / eligible | absent | would accept B | refuse | refuse | would accept B9: full literal parity |
| SimulationEngine | unsupported: Version | 2 / eligible | absent | would accept B | refuse | refuse | would accept B2: full literal parity |

P0/current result: A2 populations/3 known occurrences, eight unknown populations,
B0; no accepted repository denominator. P1–P3's same OASim yield is not proof of
safety; counterexamples distinguish them. P7/P6 could add B8/48 if newly approved,
yielding a population inventory of A3+B48=51. That does **not** automatically
admit A's unavailable whole context evidence or establish M/N for the repository.
Do not promise repository measured=0 or 0% until whole-source evidence semantics
are specified. No selected P/V namespace is accepted by ordinary invocation.
Zero real ages are established now and no metadata lookup is attempted. Even
if population and whole-source admission were later approved, zero ages without
namespace would be successful blocker isolation, not a reason to automate namespace.

## Parity and human-gate lifecycle

Python uses declared requirement population intersected with supplied exact/freeze
selection; raw freeze extras cannot enlarge it. npm uses root production manifest
scope with bounded manifest/lock association; Yarn uses declared selector matching.
Neither requires an equivalent human event/association attestation. Ruby ordinary
mode takes complete supported lock DEPENDENCIES as the direct snapshot without
reading Gemfile; its supported public GEM remote separately supplies namespace.
None proves current installed/deployed use or complete historical production.
NuGet's implicit Direct entries and evaluated/multiple/RID context are concrete
extra risks. They justify positive explicit-ID/context checks and refusal, not
an unavoidable human gate for every byte-bound, policy-chosen snapshot.

Parity therefore supports considering P7; it does not already authorize it.
Python/npm lack the positive namespace gate required here; that sibling concern
remains ROADMAP15, unchanged. A stale Ruby lock relative to Gemfile may still be
a truthful lock snapshot; presenting any sibling snapshot as current deployment
would be a separate truthfulness concern, not a defect established by this run.
No sibling implementation is weakened or strengthened.

Methodology hypothesis for the planned reusable retrospective: explicit human
acceptance may scaffold an unknown trust boundary; accumulated evidence may
permit deterministic policy to replace selection where the same necessary facts
are observable or a clearly narrower claim is consciously approved. This case
supports decomposing the gate, not a universal rule that human gates disappear.
The unresolved association interpretation here prevents treating that hypothesis
as a demonstrated automatic substitution. No retrospective framework is created.

## Status and exact human gate

Discovery freezes before independent decomposed review; review disposition and
actual focused checks/target final equality are recorded separately. No runtime,
output, schema, metric, namespace, parser or CI maintenance changes. Hosted results
for published72dc9a2 are appended to the snapshot review history on the human's
supplied basis, not claimed as agent-observed logs. Historical contracts unchanged.

**HUMAN PRODUCT / SNAPSHOT-ACCEPTANCE DECISION:** may policy choose the safely
attributable current project/lock pair as the represented B snapshot when every
included Direct has positive literal identity/request parity, sole context and
exact byte binding, with known conflict refusal and explicit no-producing-history/
no-current-evaluation limitations? Or must accountable supplier association/scope
remain necessary? Recommend considering the former only with those limitations,
explicit B fallback preserved for unextractable scope, A precedence and all
namespace authority unchanged. Selecting this is consequential new authority.
Stop here before specification/plan/tasks/code; approval must authorize the next
prospective specification and independent review, not merely “automate v3.”
