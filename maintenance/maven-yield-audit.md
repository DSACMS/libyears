# Maven yield and maintenance usefulness — 007-0030

## Assessment

The retained configured AB2D result is a credible **partial Declared-age demo**:
40 measured module/model occurrences reduce to 10 distinct package comparisons,
six with positive age and four with zero age. The occurrence-weighted total is
9.29860822749512 conventional Maven libyears. This identifies where measured age
is concentrated and which models repeat a comparison; it is not a complete
inventory, runtime observation, or upgrade plan.

The strongest next investigation is the missing scope evidence on **39
exact-version occurrences**. Version availability alone did not admit them.
Only two currently admitted occurrences remain catalogue-unavailable; their
transport recoverability is unknown. The principal limits are missing local/model facts
and conservative admission, alongside unknown population; presentation repetition
is an inspection cost addressed by the grouping below, not the cause of low yield.

## Evidence index and boundaries

Audit starts at clean `030a1b4650d4a0c0f46dc5a76cd1c5435b3f74cb`.
No target, certificate, private trust reference or network is accessed in this
run. Public package/model facts below come directly from retained rows, not a
summary substituted for missing rows. No new scan or freshness assertion.

`D` below means the directory resolved by
`python3 tools/observation_handoff.py directory`, not an assumed Git layout.
These local captures are noncanonical and are not copied into Git.

| Evidence | Location / role |
| --- | --- |
| Current original 127-row report | `D/007-0028/json.stdout`: `maven.occurrences`, `sources`, `views`; primary numerical evidence |
| Actual ordinary output and process results | `D/007-0028/ordinary.stdout`, both forms' `.stderr` and `*-evidence.json`: ordinary rounding, exit 0/empty stderr, closed worker command/result messages |
| Prior integrity witness | `D/007-0028/before.json`, `after.json`: compare retained snapshots only; no target reinspection |
| Reviewed configured validation | [007-0028 completion](presentation-polish.md#configured-ab2d-comparison-resumed--007-0028), completion `c81f781683b101d7e136b7404526cfc087aa9a12`; runtime bytes match published `a134005…` |
| Earlier positive evidence | [007-0019 witness](../specs/007-maven-dependency-age/positive-witness.md) and its tracked occurrence CSV: historical, not substituted for current rows/dates |
| Unconfigured comparison and DPC | [007-0027 smoke](presentation-polish.md#published-ordinary-user-smoke--007-0027), retained `D/007-0027/dpc-json.stdout`; distinct contexts |
| Meaning of refusal fields | [Declared facts](../libyears/maven_project.py), [admission](../libyears/maven.py), [summaries](../libyears/maven_results.py), [HTTP error collapse](../libyears/maven_http.py); code inspection only |

Configured 007-0028 intentionally ran ordinary and JSON, **not verbose**. There
is no configured verbose capture to audit. Earlier unconfigured verbose output
is not a source of positive measurements. Current raw rows and closed results are
available, so this gap does not prevent row/date reconciliation. Original target
revision was `9c785d41da3f7dd72f5be62cfc42ee7b1bf74459`; retained bounded integrity
comparison passes, without implying current target state or all ignored bytes.

## What was measured

View: `supported_local_base_model_request` (Declared), including inherited static
requests attributed to each consuming source/model. Each `(source_id, base_model,
model dependency key)` occurrence counts independently. Comparator basis is
`conventional_central`, pinned Maven 3.9.11 ordering and conservative stable
eligibility; comparator versions are global GA targets, not compatible upgrades.
Dates are **versioned public POM Last-Modified**, a conventional release-age
surrogate, not first publication, acquisition, content or producer history.

| Statistic | Exact retained value |
| --- | ---: |
| Measured occurrences | 40 |
| Distinct measured GA identities | 10 |
| Distinct measured artifact identities (extension/classifier included) | 10 |
| Distinct `(GA, declared version, comparator version)` combinations | 10 |
| Positive-age occurrences / comparison groups | 15 / 6 |
| Zero-age occurrences / comparison groups | 25 / 4 |
| Total libyears | 9.29860822749512 |
| Mean libyears per measured occurrence | 0.232465205687378 |
| Median | 0.0 |
| Maximum | 1.524357270514868 |
| Complete population / coverage | unknown / null |

All measured artifact keys here are `jar` with absent classifier. These counts
are neither unique repository dependencies nor actionable upgrade-task counts.
Zero means the exact Declared version equals the admitted comparator and both
required dates passed admission; it does not establish health or runtime currency.
Observed has no accepted retained-selection reader and remains independently
unavailable with all numeric fields null. Legacy scalar values are null too.

## Contributor inspection

Sorted by occurrence-weighted contribution. `All8` means `api/pom.xml`,
`common/pom.xml`, `coverage/pom.xml`, `e2e-bfd-test/pom.xml`, `e2e-test/pom.xml`,
`job/pom.xml`, root `pom.xml`, `worker/pom.xml`. Other module labels also mean that
module's `pom.xml`. These are attribution sites, not eight independent code edits.
Age and subtotal columns are rounded to nine decimal places for inspection;
full retained dates/values drive the exact statistics above.

| Public GA | Declared | Comparator | Occurrences | Age each | Contribution | Affected models |
| --- | --- | --- | ---: | ---: | ---: | --- |
| org.mockito:mockito-core | 5.16.1 | 5.24.0 | 2 | 1.524357271 | 3.048714541 | job, worker |
| org.testcontainers:testcontainers | 1.21.4 | 2.0.5 | 8 | 0.344232293 | 2.753858342 | All8 |
| io.jsonwebtoken:jjwt-impl | 0.12.6 | 0.13.0 | 1 | 1.164002586 | 1.164002586 | e2e-test |
| io.jsonwebtoken:jjwt-jackson | 0.12.6 | 0.13.0 | 1 | 1.164002174 | 1.164002174 | e2e-test |
| com.datadoghq:dd-java-agent | 1.63.0 | 1.69.0 | 2 | 0.459338511 | 0.918677022 | api, worker |
| org.apache.httpcomponents.core5:httpcore5 | 5.4.3 | 5.4.4 | 1 | 0.249353563 | 0.249353563 | common |
| com.okta.jwt:okta-jwt-verifier-impl | 0.5.14 | 0.5.14 | 1 | 0 | 0 | api |
| org.testcontainers:junit-jupiter | 1.21.4 | 1.21.4 | 8 | 0 | 0 | All8 |
| org.testcontainers:localstack | 1.21.4 | 1.21.4 | 8 | 0 | 0 | All8 |
| org.testcontainers:postgresql | 1.21.4 | 1.21.4 | 8 | 0 | 0 | All8 |

Grouping merges only identical artifact/version/comparator/date comparisons for
inspection. The sum of `occurrences × full-precision age` remains the approved
9.29860822749512; no deduplicated metric is introduced. Mockito and Testcontainers
account for about 62.4% of that measured total. Mockito has the largest per-row
age; Testcontainers' eight repetitions explain its large weighted contribution.
A maintainer can inspect these source-qualified comparisons first, then consult
release notes, compatibility and their actual deployment evidence separately.
Age alone establishes no vulnerability, upgrade safety, effort or task count.

## Why the rest is unavailable

The retained row primary outcomes partition **only the 127 safe records**:
40 measured + 46 unsupported-version + 39 unsupported-model + 2 catalogue-unavailable.
They do not partition the unknown repository population or all underlying causes.
Distinct GA sets overlap across outcomes; success cannot transfer row authority.

| Layer | Supported count / finding | Limitation |
| --- | --- | --- |
| Population/discovery | 8 source views all unknown population; repository discovery unavailable | Earlier local validation records missing external parent evidence and bounded incomplete discovery. Current JSON does not retain the precise discovery I/O subcause or model graph; no full N or coverage can be recovered. |
| Version facts | 46 rows / 25 GA have null versions | 43 retained requests are null; 3 retain property expressions (2 logback, 1 commons-lang3). Null serialized request does not prove an absent original declaration; it can be unavailable or suppressed. No version guessing. |
| Local model admission | 39 rows / 29 GA across 7 sources have versions but all have null scope | All 39 retain artifact keys and optional=false. Code refuses missing scope/model facts. Raw local model graph/POM snapshots are not present in this capture; the exact scope cause per row cannot be reconstructed. Unknown imports/management can prevent a compile default under existing rules. |
| Comparator/source policy | No primary comparator/policy refusal among current AB2D rows | This does not certify that every unversioned/unadmitted row would pass later. Retained DPC separately has 36 policy-unknown + 143 unsupported-version rows, 0 measured; no trust option fixes pre-lookup policy refusal. |
| Catalogue/latest eligibility | 2 rows, one GA: gov.cms.ab2d:ab2d-filters 3.2.6 in coverage and e2e-test | Catalogue unavailable; no explicit ambiguous-latest, unknown-eligibility or no-stable result. No classification of HTTP absence/private origin, parse rejection or eligibility failure can be inferred. |
| Date evidence | 0 primary date-unavailable rows in current report; 16 successful POM-date results | All 40 measured rows bind to these dates; no dates were attempted for refused rows or the failed GA. This does not establish date availability for the rest. |
| Transport/trust | Configured verified transport succeeded; each form has 27 reservations, 26 body-producing results and 80,849 bytes | One zero-body catalogue result leaves its trust/DNS/connect/deadline/HTTP/content cause unestablished. Existing HTTP exceptions collapse to a fixed reason. No-option smoke's 42 catalogue failures are a separate observation, not diagnosed TLS. |
| Observed | 8 source views independently unavailable; no accepted reader | No observed population/count/version/ages; Declared is not substituted. |
| Legacy source errors | 9 plural-projection warnings: 8 sources + discovery | Compatibility projection notices, not nine extra rejected sources or rows. |

There are **60 null-scope rows**: the 39 model refusals plus 21 of the 46
version refusals. Thus the visible primary reason can hide another blocker.
For example, httpcore5 is measured in one model/version and model-refused in
another; mockito-core is measured in two models but version-unavailable elsewhere.
These overlaps prevent treating any candidate count as promised new measurements.
The independently unknown population sits outside this retained-row arithmetic.

## Bounded next work, ranked

Existing supported operation is already demonstrated: explicit approved
`--ca-bundle` configuration enables the configured positive result. It adds no
version, scope, population or Observed evidence. The newly preserved private copy
has only offline copy/load validation; no live test is assumed or requested here.

| Rank | Bounded next investigation | Demonstrated reach / usefulness and uncertainty | Authority class |
| --- | --- | --- | --- |
| 1 | Trace the 39 version-known, scope-missing rows to exact missing scope/management facts; start with retained origins and existing fixtures, and request narrowly scoped source-snapshot capture only if necessary | 39 occurrences / 29 GA / 7 models. Most direct pre-lookup bottleneck with versions already present; high confidence in count, uncertain safe recoverability and metadata/date yield. Could establish a bounded correctness issue or confirm required absent evidence; do not default scope to compile. | Evidence investigation, not a current option. Any parser/admission correction requires separate approved work; new external parent/BOM acquisition or evaluation needs new human scope/policy authority. |
| 2 | Classify the 46 null-version rows by unavailable local management/property fact before considering expanded intake | 46 occurrences / 25 GA; 21 also lack scope. Larger count but less immediately usable evidence. High confidence in retained counts, low confidence in positive yield without additional inputs; no complete denominator promised. | Bounded evidence study; supplying resolver/build output or adding an Observed reader is new product authority, not an implied repair or authorized invocation. |
| 3 | Design a sanitized catalogue-failure diagnostic distinction for the one failing admitted GA | Only 2 occurrences; useful to distinguish transport/HTTP/framing/parsing from catalogue policy, but smaller demonstrated yield reach. Cause and recoverability remain unknown. No automatic live rerun. | Prospective diagnostic product work, separately reviewed for disclosure/schema impact; no runtime or trust change in this audit. |

Rank 1 precedes the larger version gap because its exact versions are already
available and the missing field is localized. None of these ranks authorizes
relaxing source policy, fetching external parents, resolving dependencies, or
changing the settled comparator, time basis, metric or Observed contract.

## Maintainer explanation and audit disposition

“This report shows how far a supported static slice of our declared Maven
requirements trails the admitted public comparator, using public POM modification
times. Mockito and Testcontainers concentrate the measured age across identifiable
models. Some comparisons are exactly current under this policy. We still lack
complete population, many model/version facts and any Observed runtime selection,
so this is an inspection aid, not a full dependency inventory or safe-upgrade list.”

That supports a credible demo with the positive and unavailable portions visible.
It is an assessed usefulness conclusion from the rows, not a consequence of CI.
Showing 40 as a unique-dependency or upgrade-task count would mislead; showing the
grouped table alongside unknown coverage makes the limits understandable.

`007-0029` is reconciled once from its original 44-field durable handoff and matching
completion artifact. Supplied **run-level** 377 seconds remains distinct from
`007-0028`'s resumed 366-second segment and missing first segment. Original
qualifications/notes and earlier ledger bytes are preserved; confirmed account
continuity retains 163 before and 164 after, without a derived delta. Ledger:
79 unique 44-column rows; current `007-0030` is not appended. No executable changes,
target access, certificate/trust access, network, live measurement or push.

Fresh non-author review: **COMPLETE / APPROVE, no material findings**. The reviewer
independently reconciled rows, grouping/arithmetic, source attribution, blockers,
provenance, usefulness and privacy. Parent validated the result and adopted its
optional wording refinement making transport recoverability explicitly unknown.
New child context, no overrides requested; actual child configuration/resources
unobserved. Offline arithmetic/table checks, 7 local links/anchors, ledger
prefix/shape/uniqueness, whitespace and manual sensitivity checks pass, as do
configured GitLeaks current content and full-history gates (final commit details
in the durable handoff). No product suite rerun for documentation-only changes.
Local tracking refs remain `a134005…`; actual remote state is not queried under
this run's no-network boundary. No publication is performed.

Follow-up: [007-0031 scope-evidence diagnosis](maven-scope-evidence.md) traces all
39 refusals to an unselected scope with a closed management-uncertainty default
gate. No implementation defect or new measurable occurrence is established;
original per-row context remains a bounded evidence-capture prerequisite.

## Current next-yield handoff — 007-0040

Presentation has converged at `225c40d`: [individual unmeasurable rows](maven-unmeasurable.md)
now expose all80 retained failures beside47 measured records (28 zeros), without a
complete denominator. The historical007-0030 assessment above is preserved, not a
current40-measurement result. Latest primary input is the authenticated007-0038
candidate report, also frozen by007-0039; raw total13.40209657895404, unknown
population/coverage and unavailable Observed. No new measurement occurred.

| Remaining stage | Retained evidence | Next-step implication |
| --- | --- | --- |
| 32 model-fact failures | Existing exact versions survive; the reviewed0036/0037 audit leaves these32 exact keys without a proven retained winning-management path | Do not default scope or repeat the completed seven-key proof. Their missing applicable-content/composition questions remain; no particular additional document or recoverable count is established |
| 46 version failures | 25 already have scope (13 test,8 provided,3 runtime,1 compile);21 also lack scope.43 have no retained request;3 retain property expressions | Prefer a finite, scope-ready version witness over promising the entire bucket. A missing serialized request alone does not prove an absent declaration |
| 2 catalogue failures | gov.cms.ab2d:ab2d-filters3.2.6 in coverage and e2e-test | Fixed failure does not retain transport/HTTP/content subcause; recoverability is unknown. A diagnostic-only correction or separately authorized exact live classification could inform it, but cannot promise age yield |
| Unknown discovery/population | Retained127 rows are a safe partial slice | No coverage denominator or complete inventory follows from repairing row fields |
| Observed unavailable | No accepted retained-selection reader | Separate evidence/reader product work; not a shortcut to Declared yield |

**Recommend a bounded version-intake correction, first witnessed by seven existing
org.springframework.boot:spring-boot-starter-test / jar / absent-classifier rows**:
api, common, coverage, e2e-bfd-test, e2e-test, job and worker (`/pom.xml` in each).
These are different occurrences from the seven scope recoveries in007-0038.

A narrow raw-site inventory after presentation convergence verifies retained
consumer/root bytes, literal parent associations through Boot starter parent4.1.1
to Boot dependencies4.1.1, one ordinary declaration per consumer with absent
version and scope=test, no nearer same-key management entry, and no same-key
profile dependency/management record in that inspected chain. The already retained
Boot dependencies document has one exact-key management entry with **literal
version4.1.1**. Thus this witness needs neither new document acquisition nor scalar
property evaluation, and it avoids adding a scope-default proof. This is a finite
inventory motivating the proposal, not production admission, complete model
validity, historical resolution, current-target correspondence or age evidence.

[Current intake C4](maven-external-intake/spec.md#contract) intentionally accepts
only missing scope on already exact-version, unsupported-model rows. The seven
version-refused rows are ineligible today. Existing authority does **not** permit
removing that guard or implementing this next capability. The smallest next human
gate is authorization of a bounded C4/version-evidence correction: explicitly
accepted, byte/context/key-bound management may supply an absent ordinary Declared
version under the pinned static rules, using these seven as the first witness.
Then specify/review the field eligibility, explicit-version precedence, ordinary
collision limits, consumer bindings, provenance/limitations, refusal controls and
integration with existing comparator/date policy before implementation. Keep all
other row/population/Observed authority unchanged. Coverage and worker budgets must
not be relaxed. Future live age validation needs its own explicit grant.

The retained literal candidate and already-known scope make this a better-supported
starting slice than an unranked32-key content closure or all46 version gaps. It does
not rank every alternative, promise seven admitted versions/ages, or authorize
anything beyond this recommendation. Production versions admitted/new ages in this
run: **0/0**. `D/007-0040/next-yield-check.py` and `next-yield-evidence.json` retain
exact raw sites/bindings and the finite inventory; the original artifact prefix,
report, model bytes and existing intake are unchanged. No completed composition
investigation is rerun and no broader evaluator is proposed.
