# Feature 004 Retrospective

Feature 004 is **COMPLETE / CONVERGED**, with all 21 lifecycle tasks closed.
This T021 synthesis follows the T020 baseline `577c81ef335a53c54084d15265690583c8aa49cf`; it adds no product
behavior or new convergence verdict. RubyGems support remains Unreleased.

## Feature Story

Feature 004 lets Libyears measure Ruby dependencies already recorded in a
project's root `Gemfile.lock`. Previously, the CLI measured Python and npm
dependencies, including Yarn Classic evidence, but could not use these Ruby
snapshots. Users can now scan a directory normally and receive Ruby measurements
alongside existing ecosystems, with coverage, explanations for missing
measurements, and machine-readable evidence.
Dependency age is the time between the used version's release and the latest
stable release, expressed in years.

The trust chain has three parts. The lock's `DEPENDENCIES` supplies recorded
direct scope. Supported lock specs establish selected versions and public source
authority. RubyGems.org metadata supplies observable publication dates. A package
name alone does not authorize a public lookup, and a platform-specific artifact
does not establish runtime compatibility.

The feature counts all recorded direct dependencies, including development/test
dependencies where present. It never reads or evaluates Gemfile, reconstructs
groups, executes Ruby or Bundler, installs gems, or resolves requirements. Private,
Git and PATH dependencies cannot borrow a public namesake's history. Missing
versions remain missing; unfamiliar lock sections are rejected.

This was harder than parsing a file and querying an API. Source ownership must
survive parsing. Several platform artifacts can represent one version, while
extra identity fields can make apparently similar records unsupported. Dates
describe supported observable history, which can change when records disappear.
Failures must preserve trustworthy counts and successful sibling ecosystems
without inventing evidence.

Confidence came from reviewed contracts, tests covering every acceptance
criterion, existing ecosystem regressions, authorized real-project validation,
and independent convergence. These support the bounded capability, not universal
Bundler compatibility. For deeper reading, start with the
[README guide](../../README.md#rubygems-support), then the [specification](spec.md)
for behavior, [plan](plan.md) for architecture, [reviews](reviews.md) for decisions,
[tasks](tasks.md) for deterministic witnesses, and
[release validation](release-validation.md) for live evidence and its limits.

## Evidence and Method

Repository artifacts and Git are authoritative here. Candidate A, Candidate B
and their blind reviews are synthesis inputs; their temporary files remain
outside Git. The current T021 instruction supplies unblinding metadata and
reconstructed process context, labeled below. A recorded human report establishes
what was accepted; it does not constitute independent replication.

This prose task checked chronology, claims and links against disk evidence.
Tests and live validation were not rerun. Historical pending paragraphs in
approved artifacts are superseded by the approval/completion records, not new
blockers. No external discovery target or certificate store was inspected.

## Decisions and Implementation

Ruby was not the initial recommendation. [Discovery](discovery.md) began with
no-code workflow validation (`df7aee60446795f67da321331f778c3d1457fea7`). Review rejected treating a sandboxed
0/77 result as an offline-product requirement and requested a bounded Python
evidence experiment. Ten metadata-bearing roots represented eight conservatively
grouped families; the investigation did not find two roots with retained exact
evidence that existing `--resolved` could not consume. Absent evidence, rather
than parser incompatibility, was the observed limitation.

Four application roots in one DPC family offered build-consumed Ruby locks.
Feasibility retained approximately 238/247 direct occurrences before registry
lookup: evidence fitness, not measured coverage or four independent customers.
The human selected bounded Ruby support (`a16145f5ed88be66e8591c91dd57df0ffc8b7fab`), accepting all-direct scope
and third-registry maintenance. Interpreted Gemfile/group scope remains separately
EXPLORE in [ROADMAP](../../ROADMAP.md). Root listing lacked demonstrated recurring
pain; Go/JVM lacked new selected-version evidence; cache and broader provenance
lacked demonstrated requirements.

Review made consequential changes before implementation:

| Gate | Correction | Draft → revision; approval |
|---|---|---|
| Specification | Separate publication history, availability and identity; resolve H1–H8; clarify failure precedence. Criteria grew from 45 to 52. | `c761b113ea19988e7e9ea5ca16b373c1e2c526fb` → `3b315696e4d03b5e7aac325b47a800abbade70e0`, review `5c5b69adb810827cd4c8e74d1bbbeef44bd34465`; `86be122e7570ed121572b25531f8b3994b2c6766` |
| Architecture | Pin upstream source evidence; make transport bounds opt-in; distinguish incomplete/oversize responses; schedule candidates deterministically under cooldown. | `223032e2b537d11a9dcbbf0eb49248d571373b1e` → `8b4bf8fb6535bad524fc02bdfdcc5e1beea79a92`; `1fdaf0d0356a1de8c0564dfad2b7a0b4190c9f64` |
| Task graph | Enforce transport restrictions at the first Ruby request; remove optional smoke as a mandatory dependency. Retain required dogfood; 22 tasks became 21. | `38df5a740b20121978ea4349c595b63e1f1288d5` → `c34600d1fdcdd4efeb9cae3eaf990d7c9c0fae8a`; `cf0490bda701e83183053a49e046f56adcb46cee` |

The implementation followed **parser → local/source evidence → shared transport
→ RubyGems registry → public activation → cross-boundary verification → live
validation → convergence**. T001–T003 preserved syntax, ownership and duplicates.
T004–T007 separated direct matching and public-source authorization from parsing.
T008–T010 protected existing transport contracts before adding optional bounds.
T011–T014 validated registry identity/populations, canonicalized dates, and paced
and ordered requests. The metric and existing ecosystem policy modules stayed
unchanged.

Two distinctions explain that separation. Rejecting Ruby's sole lock also loses
its scope denominator; Yarn can retain scope from a valid independent npm
manifest. Ruby's latest stable selection uses publication dates, not numeric
version order, and the same canonical date policy serves used and latest roles.
Neither rule belongs in a generic parser or new metric engine.

Public activation waited until **T015 (`0af7e1174aacf4de889c789748ddef7e9f12b472`)**. Scanning, nullable coverage,
failure isolation, provenance, human/JSON output and README/SPEC/CHANGELOG/AGENTS
updates became available together. Earlier internal commits remained safe
stopping points without exposing partial Ruby behavior. T016 added four composed
tests; T017 (`6e27d1349b3e7f848dec30aaf6a44d8ada282a6e`) recorded final deterministic traceability. T018 preserved
blocked (`bb6505fc0f9a63ffadeb8de218ab907aa4568b61`) and accepted (`ee79d35b79b82db6c8457cb14ba35bab39a43dc2`) validation. T019's completed review
was recorded with T020 (`577c81ef335a53c54084d15265690583c8aa49cf`), without product remediation.

## Material Human Interventions

**R** marks an initiating intervention reconstructed from supplied process context;
the cited repository records preserve its outcome, not the original conversation.
Unmarked decisions/results are durable in [discovery](discovery.md),
[reviews](reviews.md) or [release validation](release-validation.md).

| Intervention | Effect | Why human attention mattered |
|---|---|---|
| Reject arbitrary criterion-count limits (**R**) | Coverage followed consequential behavior; review found no inflation from absence of a cap. | A numerical target cannot settle completeness. |
| Select bounded Ruby; defer Gemfile interpretation | Accepted all-direct scope and maintenance cost. | Feasibility alone cannot decide usefulness. |
| Resolve H1–H8 product/trust choices | Fixed recognition, platform, history, timestamp, requirement and identity policies. | APIs cannot decide acceptable uncertainty. |
| Raise supply-chain/source-authority concern (**R**) | Public authority precedes lookup; no namesake substitution. | Matching names cannot confer trust; this is not malicious-package detection. |
| Authorize dpc-admin dogfood and npm requests | Bounded external access for mixed validation. | Historical paths were not standing permission. |
| Refuse weakened TLS (**R**) | Verification remained enabled; incomplete validation stopped. | Completion pressure did not authorize weaker trust. |
| Identify and explicitly authorize organizational root | Enabled temporary combined CA bundle through the existing interface. | The human supplied organizational trust authority. |
| Question human-only live validation (**R**) | Retained agent/host parity as a methodology concern. | A manual completion route should not silently become permanent labor. |
| Ask why npm/PyPI worked but RubyGems failed (**R**) | Compared destination-specific certificate chains. | Comparative evidence narrowed diagnosis; PyPI was not part of this dogfood. |
| Separate TLS interception from later DNS failure | Preserved distinct causes/limits in the T020 record. | Diagnosis determines whether trust, harness or product work is appropriate. |
| Question Low/Medium divergence and capability access | Preserved incomplete review separately from software findings. | Quality gates also affect participation; precise discussion is not retained. |

## Confidence Evidence

| Evidence | Recorded result and limit |
|---|---|
| Acceptance | T017 inspected passing witnesses for **52/52 criteria**; completed T019 found none unmet or ambiguous. |
| Deterministic correctness | **289 tests passed**, including Python/PyPI, npm/package-lock, Yarn, shared transport, metric and mixed-output regressions. |
| Architecture/readability | Architecture approval and completed convergence returned PASS; no newcomer comprehension study was conducted. |
| Compatibility | Ruby provenance is additive in **schema v3**; existing ecosystem evidence and field meanings are preserved. |
| dpc-admin dogfood | Repository **77/79 (97.5%)**, RubyGems **67/69 (97.1%)**, npm **10/10**. |
| Remaining failures | `bundler` and `tzinfo-data`: `lock_version_missing`; counted without fabricated versions or Gemfile-based exclusion. |
| Human/JSON agreement | Accepted human report confirms documented-precision agreement, schema 3 and empty `source_errors`; repository total `257.15223751425964`, displayed 257.15. |
| Provenance | Human confirmed selected and used/latest publication artifacts, including multiple platforms, `all_direct_locked` scope and `earliest_admissible_supported_observable` basis. |
| Target integrity | Earlier before/after manifests matched: 280 entries, 218 files; retries counted 281 including the root. Successful-run integrity rests on human no-change attestation, without a new manifest digest. |
| Convergence | Completed T019: CONVERGED, no material findings; release evidence SUFFICIENT. Separate smoke REDUNDANT. |

The [successful handoff](release-validation.md#successful-manual-release-evidence)
allowed checks of supplied counts, fractions and rounding. Codex did **not**
independently inspect the complete successful raw JSON. Do not promote that
handoff into a row-by-row registry audit.

Offline tests establish controlled accepted/rejected behavior, including malformed
inputs, cooldown and truncated responses. Synthetic yanked records exercise the
canonical contract without claiming current endpoints expose yank history. Live
validation establishes a real lock and then-observed metadata worked in one
authorized environment. Neither replaces the other or establishes broad demand,
complete history, or future endpoint stability.

## Release-Validation Chronology

### Destination-specific TLS interception

In the original escalated live runs, DNS worked: npm succeeded while RubyGems
failed certificate verification with OpenSSL code 20. A preliminary sandbox DNS
failure is a separate recorded attempt. Subsequent human host inspection found
ordinary public PKI for npm and PyPI, while RubyGems alone among those destinations was subject to managed TLS inspection.
Certifi lacked the organizational root.

The human identified and explicitly authorized that root. A temporary bundle
combined certifi roots with authorized organizational trust through existing
`--ca-bundle`. Certificate and hostname verification stayed enabled. Verified
connectivity and subsequent human live validation succeeded without product code
changes. No certificate material was committed. The earlier 10/79 output remains
environmental failure evidence, not meaningful Ruby coverage or completed dogfood.

### Later Codex native-resolution limitation

Later observations established an agent execution-environment DNS limitation: native resolution failed while normal host resolution and alternative DNS/TCP checks succeeded. The authorized bundle loaded, but these retries failed before TLS.

A fresh agent session reproduced native-resolution failure. This weakened stale shared-session state as the sole explanation; the exact cause remains unresolved. The later DNS issue did not cause the original TLS failure. No shared cause or causal effect of preceding session events is established. This is harness/platform friction, with no Feature 004 defect established.

Human execution supplied the accepted successful evidence. That resolved the
release-validation gate while leaving agent/host parity open. The
[T020 chronology](reviews.md#environmental-chronology-retained-for-t021) preserves
these human-supplied findings; this retrospective did not repeat the investigation.

## Repository Context and Feature 003 Comparison

Feature 003's [retrospective](../003-yarn-lock-evidence/retrospective.md) rated
storytelling MOSTLY and proposed committing drafts before review. Feature 004
preserved discovery `df7aee60446795f67da321331f778c3d1457fea7` → `67b7d89ca6f1c48bc92dcd128b19bb478a6ba969` and the specification/plan/task transitions
above. Its specification verifier explicitly found the before/after evidence
useful. This is a demonstrated improvement in reconstructability.

| Dimension | Feature 003 → Feature 004 |
|---|---|
| Intent and review corrections | Recoverable summaries, sometimes missing reviewed drafts → exact committed baselines and revisions alongside rationale. |
| Repository context | Fresh retrospective reconstructed the journey → multiple architecture/task/convergence gates explicitly reported context sufficient. Compact/focused instructions are documented most clearly for architecture reviews. |
| Human interventions | Product decisions preserved → H1–H8, access and organizational trust are explicit; some initiating questions still require reconstructed context. |
| Routing evidence | Approximate phase routing reconstructed retrospectively → T019 completion contrast recorded at T020; T021 authorship/review metadata supplied with this synthesis. Neither is a prospective cost ledger. |
| Complexity and validation | Yarn reused npm: 30 criteria, 187 tests, 77/77 dogfood; one diagnostic remediation → third registry, transport controls and publication evidence: 52 criteria, 289 tests, 77/79 dogfood; no completed-convergence material findings. |

The coverage figures concern different projects and scopes, not a trend. Test
and criterion counts describe obligations, not relative quality. Feature 004's
successful live evidence is less directly inspectable than its retained failure
captures, despite its stronger review history.

Durable artifacts supported bounded reviews without restating the whole contract.
A fresh context still needs role, baseline, authority, scope and stopping point.
T018's blocked/retry/completion records preserve resumable state, suggesting a
mechanism for interrupted-session recovery. No controlled recovery trial or
handoff-cost measurement is recorded. Prompt lengths, runtime and credits were
not prospectively tracked; shorter prompts are not established to cause faster
execution, lower cost or better reviews. Human attention savings also remain
unmeasured.

## Model Routing and Capability Access

Two naturally occurring observations deserve preservation:

| Observation | Result |
|---|---|
| T019 Astra Low broad audit | Incomplete; NOT CONVERGED; no product defect established. |
| T019 Astra Medium broad audit | Complete; CONVERGED; supplied the missing review evidence without remediation of a Low finding. |
| T021 Candidate A, GPT-6-Astra Low | Viable shorter, accessible narrative; later self-audit reported 2,460 words and MOSTLY storytelling. |
| T021 Candidate B, GPT-6-Astra XHigh | Deeper comparison and bounded experiments; original self-audit reported 5,240 words and MOSTLY storytelling. |
| Blind review 1, GPT-6-Astra Low | COMPLEMENTARY — CANONICAL SYNTHESIS SHOULD COMBINE THEM. |
| Blind review 2, GPT-6-Astra XHigh | B MATERIALLY STRONGER, while recognizing A's accessibility and concision. |

The T019 record is repository-native at T020. T021 identities and self-audit
metadata come from the human's unblinding instruction; the two candidates and
blind reviews were read from the four authorized temporary retrospective review
inputs. Neither review established a material factual defect in either candidate
or identified unsupported causal claims. Low review did flag B's specific
“human-requested” follow-up agenda as independently unsubstantiated. That
attribution limit is retained below. The self-audits identified evidence limits
around reconstructed interventions, successful output inspection, model effects
and unresolved DNS causation.

This synthesis retains A's accessible Feature Story and economical narrative,
and B's Feature 003 comparison, capability/access reasoning and bounded future
experiments. It selects and integrates those contributions rather than choosing
B or accumulating both texts. XHigh authorship/review confers no inherent
authority. The retrospective experiment is **n=1**, not causal evidence that
effort produced the differences; T019 likewise does not establish an optimal
routing rule.

An incomplete review leaves a gate open but is distinct from software failing a
completed review. Applying the [OSPO access mission](../../README.md#cms-open-source-program-office-mission)
and [community principles](../../COMMUNITY.md), open-source quality gates should
not silently require premium model access. Standards should remain unchanged.
The hypothesis is that smaller independently verifiable evidence tasks, followed
by synthesis checking all criteria and cross-boundary behavior, could make broad
gates accessible to more models. Feature 004 did not test it. Decomposition can
miss integration findings; collecting positive verdicts alone is insufficient.

## Human-Centered Open Source and Friction

Readable durable artifacts made decisions inspectable beyond the development
conversation. Human attention mattered at ambiguity and trust boundaries;
agents stopped at incomplete validation rather than inventing authority.
Focused source modules and assertion-level witnesses made implementation evidence
inspectable, with readability approved. These are concrete ways automation
preserved meaningful human control. Composable evidence offers a possible
alternative to requiring one model to perform an entire broad audit; broader
participation or reduced human effort has not been demonstrated.

Specification, architecture and task review corrected real ambiguities and unsafe
intermediate boundaries. That was useful correction, not demonstrated process
waste. However, optional smoke became a required dependency again after the
[same Feature 003 correction](../003-yarn-lock-evidence/reviews.md#task-graph-review):
recording a lesson did not prevent recurrence. Environmental retries, manual
handoff and an unfinished convergence attempt added work without changing the
product. Their time/cost is unmeasured. Historical pending paragraphs and richer
raw failure evidence than success evidence also impose navigation costs; current
authority pointers help readers distinguish them.

## Lessons for Feature 005

These are bounded experiments to consider, not approved Feature 005 work or
proven improvements:

1. **Record observations prospectively.** Candidate pipe-delimited fields:
   `stage | task_class | model | effort | context | prompt_chars | runtime_s | credits_before | credits_after | completion_status | finding_status | outcome`.
   Define units and measurement boundaries; retain unknowns and incomplete
   attempts rather than reconstructing runtime from Git timestamps.
2. **Separate completeness from verdict; test decomposed convergence.** Record
   audited coverage, unaudited obligations and findings separately. Compare bounded
   reviews plus cross-boundary synthesis with a broad audit where feasible,
   examining completion, missed findings and human work under the same standard.
3. **Test compact repository-context prompts.** Supply role, baseline, authority
   and stopping point; retain committed drafts. Record prompt/context measures
   before making efficiency claims. Explicitly check optional-versus-required
   dependencies to address the recurring smoke mistake.
4. **Check authorized agent/host network parity earlier when live work is needed.**
   Distinguish native DNS, TCP and verified destination-specific TLS before
   dogfood. Preserve trust authorization and final real-root validation. Where
   permitted, retain sanitized successful machine-readable evidence so manual
   fallback is more independently inspectable.

## Post-004 Follow-Up

The current human T021 instruction supplies this future cross-cutting agenda:
`AGENT_ROUTING.md`, a Feature 005 observation ledger, continued human-centered
development thesis, reusable methodology/starter harness exploration, and
notice-generator as a possible second-project/generalization test. Its earlier
attribution is reconstructed process context, not independently established by
pre-T021 repository history. Recording it here neither implements the agenda nor
approves another project's work. No routing file, ledger or Feature 005 work is
created by T021.

## Storytelling Verdict

**MOSTLY**, using Feature 003's framing. A fresh contributor can reconstruct
intent and alternatives, decisions, review corrections, implementation boundaries,
deterministic validation, accepted live validation and final convergence. Material
human decisions and remaining uncertainty are visible, with stronger before/after
evidence than Feature 003.

The qualification concerns the combined product/process story: some intervention
triggers are reconstructed; successful live evidence retains its handoff limits;
prompt/cost/recovery observations are missing; model effects and the exact native
resolver cause remain unresolved. These are evidence limits, not new blockers
or a reversal of convergence. Feature 004's artifact lifecycle is complete
through T021; no release, tag or push is implied.
