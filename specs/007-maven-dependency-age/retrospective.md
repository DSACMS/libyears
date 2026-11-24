# Maven and local-SBOM retrospective and handoff

## Published Maven/SBOM chapter — 007-0057

**Close the implemented chapter.** Maven T001–T014, external-management T1–T6,
Feature008 T001–T010/C1–C3/V001 and metadata-budget T1/V1/C1 have completed their
approved independent gates. No unresolved implementation acceptance criterion was
identified by the task/review reconciliation. Partial measurement and initially
unavailable Observed were explicit contracts, not promises to measure every row.
Historical pending paragraphs below retain their checkpoint meanings.

Both actual remote main refs verify human publication of
`27b6667cf71ab84e905648a16c465aa87b2ca350`. The earlier human screenshot showed six
Ubuntu/Windows jobs and Live PyPI passing, with three macOS jobs waiting. A single
later public hosted inspection in this closure finds all nine Python3.11–3.13
Ubuntu/macOS/Windows jobs and Live PyPI **completed/success**, including each matrix
job's worker-lifecycle, offline-test and whitespace steps. The exact-candidate
[Python run](https://github.com/DSACMS/libyears/actions/runs/45448605160) and four
other workflow summaries (secrets, hygiene, Push on main and pages) report success.
This closes the known hosted-matrix follow-up for that candidate without rewriting
the earlier partial observation. Job records, not raw test logs/counts or scanner
version logs, were inspected; no native Maven measurement capability is inferred
from a passing/skipped platform test. The new retrospective commit is local only.

### Useful results and their populations

The latest retained separate Dependency-Track4.13.4 SBOM result is **186/200 members
(93%)**, **337.47960139554345 conventional Maven libyears**. Its200 members represent
199 unique lookup identities, with43 direct and157 transitive graph relationships.
All104 previously measured ages stayed unchanged;82 additional members gained ages.
One configured batch made543 distinct requests in244.3073433330028seconds, with
**zero budget refusals**. Fourteen remain: five latest-eligibility refusals, five
unavailable catalogues and four unavailable dates. Underlying HTTP causes remain
unknown where the closed protocol supplies no cause. This is an asserted inventory,
with no established association to the representative checkouts or their current
builds. [Full before/after evidence](../../maintenance/sbom-metadata-budget/live-validation.md).

The following are the latest retained representative results from **007-0054 at
20b4bf0…**, not newly measured results at27b6667… and not the older positive-witness
checkpoint. No target was accessed or remeasured in this closure.

| Repository / invocation | Population | Measured / denominator | Total libyears | What it answers |
| --- | --- | --- | ---: | --- |
| Medicare dashboard, ordinary | npm direct production | 10/10 | 18.703444347637337 | Complete supported direct scope |
| metrics, ordinary | PyPI direct | 0/7 | 0, empty measured subset | Exact versions missing; repository N unknown |
| metrics, ordinary | npm direct production | 0/0 | 0, empty population | No production npm dependency age |
| dpc-app, ordinary | Maven Declared occurrences | 0/unknown | 0, empty measured subset |179 visible refusals, no age total |
| ab2d, ordinary | Maven Declared occurrences | 0/unknown | 0, empty measured subset |127 visible refusals; catalogue/model/version limits |
| ab2d, explicit CA only | Maven Declared occurrences | 40/unknown | 9.474748459958931 | Measured subset |
| ab2d, explicit CA + accepted management | Maven Declared occurrences | 54/unknown | 15.735360420310798 | Larger measured subset; population still incomplete |
| OASim, ordinary | NuGet direct project occurrences | 51/51 | 54.10496311259412 | Accepted bounded snapshot scope |

[Exact commands, human output, JSON reconciliation and integrity limits](../../maintenance/representative-smoke-007-0054.md)
remain inspectable. Repeated project/module occurrences retain their weights.
No totals in this table are added to the independent SBOM population. npm/PyPI
use publication dates; NuGet uses catalog-created receipt dates, independently
of the Maven conventional basis.

Maven **Declared** describes supported static requests, including explicitly
accepted bound management facts. **Observed** requires separately accepted retained
selection evidence; no Maven reader is implemented and its numerics stay unavailable.
**SBOM** measures a document's unique component-version/variant members, not either
Maven view. POM Last-Modified dates describe identity-checked versioned public POM
representations, not first publication, artifact content or runtime state. A missing
age remains unmeasurable; incomplete discovery keeps N/coverage unknown. Even100%
coverage of an asserted inventory would not establish complete repository scope.
Libyears is dependency-age lag under a stated population and time basis, not a
comprehensive measure of technical debt, upgrade effort, compatibility or security.

Users can scan supported local declarations and one existing supported CycloneDX1.5
SBOM without executing Maven/Java, builds, installs or resolvers. Ordinary directory
scans need no witness merely to discover that evidence. External management needs
explicit `--maven-management` acceptance; safe local bytes do not select themselves
as applicable models. Explicit `--ca-bundle` was necessary for AB2D's successful
configured transport in the retained environment; no ambient trust discovery or
TLS bypass substitutes. `--sbom-budget extended` explicitly opts only SBOM metadata
into600requests/600batch seconds; default remains300/300. It does not imply new source
permission. Existing README/ECOSYSTEMS own supported invocation syntax and limits.

### Feature story: from model facts to a useful inventory answer

The human wanted an actual, inspectable age-lag answer across representative
repositories, including what the number covered. Initial declarations yielded
little because local model evidence could not fill external parents/BOMs, unsupported
requests were not exact selected versions, discovery could be incomplete, and source
policy could refuse public correspondence. DPC's zero-yield witness satisfied the
approved attributable-facts contract but was not a satisfactory complete age answer.
Neither source refusal nor ordinary transport failure proved fresh dependencies.
The failed first-publication/provider investigations stayed negative evidence; the
human selected the narrower labeled POM-modification convention and conservative
latest eligibility rather than making undocumented timestamps into publication.

Accepted external-management evidence supplied restricted missing scopes, then
managed versions, with exact consumer/model/byte and winning-field associations.
Seven added scopes and seven managed-version occurrences were bounded corrections,
not an evaluator, resolver or automatic model acquisition route. The final retained
configured smoke measures54 versus40 with CA alone, still with unknown complete N.
The earlier0044 capture failed before coherent result recording; the corrected0045
capture and later0054 smoke are separate evidence, not a rewritten successful0044.
[Configured lineage and limitations](../../maintenance/maven-external-intake/configured-validation.md).

Observed discovery found no qualifying retained selection export in the bounded
candidate search. A release SBOM did provide real exact component inventory evidence,
so the human selected an independently useful age population instead of inventing
a current-checkout join. Feature008 added bounded local JSON framing, safe identity/
variant/alias handling, graph relationships, comparator restrictions and inspectable
measured/unmeasurable tables. It established neither current-build completeness nor
acquisition/content/deployment. Presentation work exposed refusals, unknown N,
Declared/Observed differences and rounded versus raw statistics rather than hiding
positively found dependencies behind empty summaries. Discovery-only suppression
can still obscure unknown repository scope;0054 records that remaining UX limit.

The first SBOM batches measured104/200. Retained0052 worker evidence shows300 distinct
operations and clean termination well below its byte/time ceilings; existing GA/date
caches already avoided duplicates.0054 has the same refusal frontier but no retained
worker counters, so its exact request count is not reconstructed. The separately
approved fixed opt-in600/600 profile addressed that operational count ceiling;
per-command/per-GA, scan/response-byte, verified TLS, endpoint and hard termination
limits stayed unchanged. The one0055 batch measured186/200 without budget refusals;
it did not force all192 or200 into measurement or start a retry loop.

```text
static declarations -> bounded external-management facts -> partial Declared ages
retained selection  -> no accepted reader                -> Observed unavailable
separate SBOM       -> 104/200 at standard budget          -> 186/200 opt-in
```

### Human decisions, actors and review

Apply the existing [actor/authority framework](../../AGENT_ROUTING.md#actors-capabilities-and-authority)
and [gate distinction](../006-nuget-selected-evidence/methodology-retrospective.md#human-gates-as-scaffolding-with-limits):

| Actor / evidence owner | Observed contribution and authority | Verification limit |
| --- | --- | --- |
| Human | Selected plural views, conventional date/eligibility policy, bounded management and separate SBOM scope; granted exact public-target/trust/disclosure/live and publication authority | Approval could not create missing historical date or acquisition facts |
| Author/orchestrator | Recovered contracts, implemented authorized tasks, captured real outputs, reconciled findings and prepared publication | Self-audit did not replace independent approval; target access was not target execution |
| Fresh independent reviewers | Challenged frozen spec/plan/runtime/result/closure claims; authors corrected findings and obtained focused verification | Scoped completion and verdict, not new product/trust authority or assumed model/resource telemetry |
| Repository contracts and tests | Carried established scope, bounded execution and executable acceptance witnesses across continuations | A plan/test fixture was not proof that a live command or hosted job ran |
| Local private evidence/helper | Preserved raw commands/results, digests, safe operational references and original observation batons | Noncanonical local state, not a backup, universal truth or permission to retain secrets |
| Hosted CI | Executed candidate/platform checks; records supplied exact current status | Queue state was not product failure; successful jobs did not establish complete inventory or positive native support for skipped primitives |

Convergence made practical corrections: identity/framing/freshness/admission issues
in Feature007; subject-wide and same-GA namespace veto propagation in Feature008;
and later repeated-option, DPC/dashboard heading attribution and scan-versus-response
byte-limit wording. The SBOM veto findings prevented a weaker alias/version from
borrowing public lookup permission. The last wording fix clarified64MiB cumulative
scan bytes versus2MiB catalogue/1MiB POM responses; it was not a runtime-budget change.
Original REVISE, incomplete captures and focused approvals remain in the
[007](reviews.md), [008](../008-local-sbom-age/reviews.md) and
[budget](../../maintenance/sbom-metadata-budget/reviews.md) review records.

Determined internal corrections/reviews should continue under an existing grant,
not use the human as an APPROVE-message bus. New scope, private access, coordinate
disclosure, organizational trust, metric convention and publication stayed consequential
human boundaries. Readiness followed by human execution and then actual hosted
observation worked as separate actor-owned actions; no agent push was inferred.

### Durable recovery and resource observations

The original007-0014 temporary handoff was human-confirmed lost after reboot and
remains missing; no original bytes/row or model runtime were reconstructed. Earlier
CA staging/location losses required specifically authorized factual recovery, not
workstation certificate search or permission to put trust details in public prose.
The later Git-directory helper made original0055/0056 batons available here, but
Git metadata/worktree deletion can still remove them. Local durability is not backup.

Repository contracts now let continuation prompts carry intent, deltas, exact new
authority and telemetry rather than repeat all normative history. This supports
smaller prompts as a design direction, not measured coordination savings or causal
evidence. No matched prompt-size, model-tier, active-compute or cross-project harness
experiment establishes efficiency. Human-reported1802seconds for0055 keeps its
runtime/confounding qualifications; account readings are not per-task billing.
0055 was already reconciled once;0056 is recorded from its original handoff without
invented status. Its ending credits are unknown, so0057's starting reading stays
blank rather than skipping that account boundary. Portable harness extraction stays
opportunity10 EXPLORE; no new SKILL/tool/general framework is implemented.

### Remaining-work disposition

[ROADMAP opportunity11](../../ROADMAP.md#11-java-ecosystem-repodive) owns Maven/SBOM
opportunities; [opportunity10](../../ROADMAP.md#10-human-centered-agentic-development-harness)
owns harness research. Existing opportunities9/23 retain provider/plural-view context.
This table disposes of work; it grants no implementation or investigation authority.

| Issue | Disposition | Closure consequence / existing owner |
| --- | --- | --- |
| Existing implementation acceptance | Complete through the named independent gates; no unmet AC identified | Close implemented chapter; preserve honest partial/unknown results |
| Exact27b6667 hosted evidence | Former operational follow-up now observed complete for nine matrix jobs +LivePyPI; all five workflow summaries successful | No known queued matrix prerequisite remains; no new retrospective-commit CI claim |
|14 remaining SBOM failures | Not an acceptance gap:5eligibility need admissible latest-selection evidence;9catalogue/date outcomes lack usable metadata/time evidence and unresolved HTTP causes | Future bounded operational/evidence follow-up only if selected; no policy relaxation or retry now; opportunity11/live validation owns details |
| Maven Observed ingestion | Deferred/unimplemented; no accepted reader | Separate retained export/context qualification and approved contract; opportunity11/23 |
| Broader external models/population completeness | Restricted management intake complete; general evaluation/acquisition/discovery expansion unimplemented | Separate product/architecture/disclosure scope; opportunity11; unknown N remains honest |
| Private-repository validation | Not performed and not required by the approved public proving-ground task | Separate exact-target/trust/disclosure grant; opportunity11; no private readiness claim |
| Further cross-ecosystem SBOM formats/identities | Not implemented; supported local CycloneDX1.5 Maven subset only | Separate selection/specification; opportunity11 corpus evidence/opportunity23; no implicit PyPI/SPDX or other ecosystem support |
| Portable harness extraction/generalization | Opportunity10 remains EXPLORE | Cross-project evidence, maintenance/accessibility/resource implications before packaging; no extraction now |

No new feature, metadata investigation, target access, package-tool execution,
publication, tag or release follows from this closure. The retained source is
published; any local retrospective/bookkeeping commit still needs its own human
publication decision. Detailed closure review and check provenance is appended to
[reviews](reviews.md); raw evidence and original current handoff stay helper-local.

---

## Earlier Feature007 retrospective (historical checkpoints)

The following account is retained verbatim from its earlier T014/positive-witness
checkpoints. Pending statements describe those dates, not the published status above.


T014 candidate. Final disposition is in [reviews](reviews.md). This retrospective
uses repository evidence, [deterministic verification](verification.md), the
[actual public witness](validation.md) and prospective observations. It is not a
release, cross-project benchmark or generalized development harness.

## Product outcome and evidence limits

The selected product question is answerable without executing Maven: what age facts
can supported local project requests establish, and what independently accepted
selection evidence exists? The implementation presents Declared and Observed side
by side. Initial Observed is unavailable because no reader was selected, not because
Declaring a version proves the selected version or because every artifact was searched.
Source/model identity, version facts, comparator authority, time basis, population
and collection availability remain distinct. This distinction preserves useful
facts when an age or complete denominator is unavailable.

The date investigation did not establish first-publication authority. The human
ultimately selected a narrower convention: public versioned POM modification time
as a release-age surrogate. That decision changed the supported claim, not the
historical evidence. The later conservative eligibility choice similarly added a
product predicate to pinned Maven precedence; ordering itself cannot prove stability.
Unknown potentially maximal qualifiers refuse rather than silently selecting an older
known/date-bearing version. Neither convention proves acquisition or runtime state.

Public reality exposed a substantial practical limit. At the selected clean DPC
revision, ordinary sorted discovery hits256 directories before reaching the root POM.
Nine safe child sources retain179 records and36 exact request facts, while external
population and coverage remain unknown. The nonempty root extension sentinel also
prevents comparison. The result has no measured age, yet independently reviewed
attributable requests and explicit limitations satisfy the approved usefulness
contract. There was no incentive to repair the target, lift bounds, ignore extensions
or weaken source policy just to produce a number. Long normal/verbose output remains
a convenience limitation. Positive live date yield and broad native filesystem
support are not established by this public witness.

## Independent convergence and corrections

The [task record](tasks.md) preserves bounded task commits and independent gates.
Earlier implementation reviews exposed claim-specific admission, identity, streaming/
framing, catalogue-freshness and unsupported-model defects; original REVISE evidence
and focused closures remain in reviews.md. Deterministic convergence was not treated
as an actual target witness. T013 independently reviewed the ordinary user journey
and security/privacy schedule, not just internal data structures.

Two T013 slices independently reproduced bounded discovery/input facts, exact output
projections, null/zero distinctions and target integrity. The security slice repeated
all three byte-identical CLI forms with socket/subprocess audit rejection, recording
no events. Fixed endpoint/redirect/ambient isolation stayed code and deterministic
evidence because this target admitted no network capability. Before/after proof is
bounded Git state/input equality, not a claim to have audited every ignored file.
No product defect or new consequential policy decision arose during GPUBLIC. Capture
preflight adjustments were resolved within existing authority before target content
capture. A correct refusal can pass validation without proving the refused operation.

## Authority, reboot and human intervention

Reviewed-graph delegation survived publication and a fresh parent. Repository state,
approved semantics and task authority were recoverable; T013→T014 required no new
next-task authorization. The GPUBLIC grant was consequential: it supplied real-target,
network/disclosure and integrity authority separately from implementation authority.
Public repository identity still did not waive occurrence-level source refusal.
Private validation and publication remain distinct future human gates.

The reboot demonstrated a different durability boundary. The human confirms the
original007-0014 `/tmp` observation handoff was destroyed and has no retained copy.
Its original bytes cannot be recovered. No missing fields or ledger row were
reconstructed; directly supplied final telemetry is preserved as human-observed
partial evidence only. Original context-compaction/autonomous-graph observations
already in the repository remain unchanged. The subsequent007-0015 handoff survived,
was verified and appended once with supplied final telemetry. Credits-before stays
blank absent direct observation or explicit qualifying continuity; no runtime
subdivision or canonical credit delta was invented.

The public candidate-root location had deliberately been omitted from published
prose and was also unavailable to the fresh parent. Human factual recovery identified
the already-selected public collection; it did not choose a new target or product
policy. A guessed unrelated collection path was not evidence of target absence.
The initial recovery stop preserved the private-target boundary but exposed the
operational cost of relying on temporary/local-only location knowledge. Retained
public identity/revision remained useful after the path was supplied.

The observation is therefore specific: repository authority/state survived reboot;
ephemeral observation bytes did not; local target-location knowledge required human
recovery. A durable nonpublic operational handoff location could be investigated in
future methodology work, but no storage policy, generalized harness or SKILL is
implemented here. Do not make personal topology public to compensate for temporary
storage loss.

## Prospective harness assessment and handoff

The task envelope avoided routine human message relay between converged tasks and
reviews. Independent review remained mandatory and distinct from new authority.
Hosted evidence was incorporated with its provenance and capability limits rather
than retransmitting or reopening the product contract. No material methodology was
found only in prior conversation; operational location and temporary observation
bytes were nevertheless missing. Current continuation observed no new compaction;
prior fresh-context/compaction evidence is historical, not a causal experiment.

Fewer approvals or a successful handoff do not establish net attention/resource
savings. Parent/child configuration and resource telemetry are not inferred; reported
runtime and account readings are not active compute or per-task billing. No comparable
prompt-size series or cross-project generality was measured. This phase supplies a
within-repository harness observation, including a real failure of ephemeral handoff
durability, rather than validation of a universal workflow.

Preserve the approved bounds, source policy, independent views, conventional-date
claim, test/provenance companions and real zero-yield witness. Any extension support,
discovery redesign, Observed reader, private proving ground or new evidence provider
requires its own appropriate authority. Stop at the reviewed pre-publication boundary
after independent T014 approval. Push/release/tag remain unauthorized.

## Post-convergence positive demonstration — 007-0017

The [bounded public investigation](positive-validation.md) autonomously ranked the
established candidates using unchanged admission code. QPP initially offered the
best known-coverage story, but its ordinary root journey would also disclose five
Python pins outside the Maven-only grant. That selection oversight was retained,
corrected before network disclosure and independently reviewed. AB2D became the
best qualifying ordinary journey, with42 admitted occurrences and unknown complete
population; the SDK remained an untested fallback. This extends the selection lesson:
whole-invocation disclosure matters alongside ecosystem-local admission.

AB2D exposed unavailable compiled default TLS trust before connection, rather than
positive age yield. No fallback could repair that environment and none was tried.
DPC's valid source-refusal witness remains intact. The single live grant supported
attempted validation, with network sandbox escalation and a remaining explicit trust
input/environment gate; no evidence or TLS rule was weakened to improve the demo.
Repository-resident contracts and discovery roles supplied routing; no generalized
harness or resource-saving conclusion follows. Positive live dates remain pending.

## Positive witness with explicit trust — 007-0019

The [AB2D follow-up](positive-witness.md) establishes40 measured Declared occurrences
with verified TLS, using the existing explicitly approved trust input and unchanged
product behavior. Complete population/coverage remain unknown; Observed unavailable.
The007-0017 preconnection baseline and DPC refusals remain valid. Private trust was
consumed without certificate identity discovery or durable disclosure. Evidence
distinguishes confirmed GETs from unresolved reserved attempts rather than inventing
precise transmission counts. This bounded success does not generalize Maven support
or turn environmental trust handling into a new product policy.
