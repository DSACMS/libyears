# Maven scope-evidence diagnosis — 007-0031

## Disposition

**No correction is justified by the retained evidence.** All 39 version-known
refusals retain no scope origin. The producing implementation therefore selected
no scope field; its compile-default guard was closed by management/import
uncertainty. Applying compile across that guard would violate the approved
contract, not restore a missing unconditional Maven default.

This is an implementation-derived branch diagnosis, **not recovery of the
original model graph**. The original POM snapshots, context flags, blocked keys
and profile/BOM graph were not retained with these rows. Their exact upstream
trigger remains unresolved for all 39. No evidence establishes a supported fact
lost in transformation, and no runtime/parser/admission change is made.

| Retained-occurrence outcome | Count and qualification |
| --- | --- |
| Must remain refused on the available facts | 39; scope is unknown and cannot mint a capability |
| Independently certified original-input root cause | 0; row evidence does not identify which upstream uncertainty set the guard |
| Affected by a verified implementation defect | 0 established |
| Newly supportable after a correction | 0; no correction justified or applied |
| Still unresolved at original parent/management/profile/BOM level | 39; overlaps the safe-refusal count, not another population |
| Established case needing a new product policy decision | 0; the next gap is factual evidence, not permission to default |

The historical 40 measured occurrences / 10 comparisons and total
9.29860822749512 conventional Maven libyears remain unchanged. This diagnosis adds
no live ages, complete population, coverage, or Observed evidence.

## Evidence and pinned semantics

Entry point: [yield audit](maven-yield-audit.md). Start: clean
`007c33e53a2635091574363dfb75746bcd3ba271`. `D` denotes the actual directory returned
by `python3 tools/observation_handoff.py directory`. Original
`D/007-0028/json.stdout` supplies all 39 rows and source contexts. The matching
ordinary output and closed worker evidence establish their unchanged refusal
history; `before.json`/`after.json` contain hashes/metadata, not original XML.
No target, trust input, workstation configuration, private repository or package
endpoint was accessed. Retained records are not reconstructed into original POMs.

The governing contract is [S3 steps 1–6](../specs/007-maven-dependency-age/spec.md#s3--maven-population-and-bounded-local-model),
with [plan](../specs/007-maven-dependency-age/plan.md) and existing review disposition.
It explicitly requires delayed scope defaults, exact-key field precedence,
consumer-written management exceptions per field, and no compile default across
unknown management that could supply scope. Optional remains independently false
by default. An external or missing parent may leave precisely that uncertainty.

Necessary source order/default facts were not retained in the local factual
extracts, so only five exact Apache Maven **maven-3.9.11** source files were read
on 2026-11-17. No adjacent source exploration or target-derived queries occurred.

| Pinned authoritative source | Inspected fact |
| --- | --- |
| [DefaultModelBuilder](https://raw.githubusercontent.com/apache/maven/maven-3.9.11/maven-model-builder/src/main/java/org/apache/maven/model/building/DefaultModelBuilder.java) | Inheritance assembly and interpolation precede phase-two dependency-management import, management injection, then default-value injection. |
| [DefaultModelNormalizer](https://raw.githubusercontent.com/apache/maven/maven-3.9.11/maven-model-builder/src/main/java/org/apache/maven/model/normalization/DefaultModelNormalizer.java) | `injectDependencyDefaults` supplies compile when final scope is empty; this normalization follows management, not raw child-field parsing. |
| [DefaultDependencyManagementInjector](https://raw.githubusercontent.com/apache/maven/maven-3.9.11/maven-model-builder/src/main/java/org/apache/maven/model/management/DefaultDependencyManagementInjector.java) | Matching dependency keys merge management non-dominantly; optional is not managed. |
| [ModelMerger](https://raw.githubusercontent.com/apache/maven/maven-3.9.11/maven-model/src/main/java/org/apache/maven/model/merge/ModelMerger.java) | Scope merge copies a nonnull source when dominant or when target scope is null. |
| [MavenModelMerger](https://raw.githubusercontent.com/apache/maven/maven-3.9.11/maven-model-builder/src/main/java/org/apache/maven/model/merge/MavenModelMerger.java) | Extends the base merger without a scope-specific override. |

These are paraphrased technical facts, not copied Java implementation. Upstream
ASF attribution and author Benjamin Bentmann are acknowledged; existing
[Apache License](../third_party/maven-3.9.11/LICENSE) and
[NOTICE](../third_party/maven-3.9.11/NOTICE) remain intact. Full Maven evaluation is
broader than libyears' approved conservative subset. Upstream normalization does
not authorize libyears to assume away unresolved management. Explicit empty
scope at final Maven normalization is also not evidence that any of these 39 had
an explicitly empty original field.

## Exact branch trace and limits

The relevant [implementation](../libyears/maven_project.py) is unchanged from the
captured run:

1. `_records` distinguishes absence from selected fields, retains raw scope text
   and its origin, and blocks ambiguous/unsupported ordinary keys. `_merge`
   performs field-level inheritance before final fact selection.
2. `_selected_field` first returns a surviving explicit/inherited ordinary scope;
   otherwise it considers admissible exact-key management. Compile is returned
   only when both `imports_unknown` and `management_unknown` are false.
3. `_declared_occurrence` appends a selected field's origin **before** expansion,
   profile/variant checks and scope-value validation. The serializer preserves
   these origins. A selected empty, invalid literal, computed, profile-conflicting
   or later rejected scope would therefore still have a scope origin.
4. Every one of the 39 has no scope origin. Thus the scope field was absent at the
   selector result, not lost during expansion or serialization. Under this code,
   the default gate must have been closed. `_fact_context` propagates
   `management_unknown` into `imports_unknown`, so import/management uncertainty
   was necessarily present; the exact flag source is inferred, not retained.
5. Exact version, artifact identity and optional=false survive. A null scope then
   produces `UNSUPPORTED_MODEL`; [admission](../libyears/maven.py) requires the
   otherwise-ready fact state and creates no work for this row. Successful same-GA
   siblings cannot transfer capability or metadata results to it.

All 39 are in `base_model` with absent classifier and no selected scope origin;
38 have model type `jar`, and `common/pom.xml`'s spring-cloud-aws-dependencies
record has type `pom`. Their seven source contexts retain
`parent_sources=[pom.xml]`. This says
a local root parent was associated, not that its own ancestry/management was
complete. Earlier [validation](../specs/007-maven-dependency-age/positive-validation.md)
records external-parent and bounded-discovery limitations, consistent with this
trace but insufficient to identify every original flag or exclude secondary
profile/BOM/blocked-management influences.
The type=pom record R18 is an ordinary project dependency here; it is not evidence
of a dependency-management BOM import and cannot itself explain the import guard.

| Possible scope/influence | What can be concluded for all 39 |
| --- | --- |
| Omitted ordinary field | No surviving raw ordinary scope was selected. Whether original omission or an earlier unsupported/lost input explains that absence cannot be certified without snapshots. |
| Explicit empty, literal, computed or inherited ordinary scope | None was selected at the fact boundary; a selected field would retain an origin. Original XML history cannot be reconstructed. |
| Managed scope | No admissible managed scope was selected; distinguish absent, inherited-with-import uncertainty, unresolved or blocked management only with the missing context. |
| Profile conflict / blocked management key | May coexist; exact sets are not serialized. They cannot justify falling back to compile or to an inherited field. |
| Blocked ordinary key | Ordinary ambiguous keys are removed rather than revived from a parent. These 39 emitted rows do not supply the discarded-key history. |
| Scope lost after selection | Excluded by origin retention for these rows; loss before selection is not established or excluded by original input evidence. |

Scope is the immediate admission blocker on these 39, but a symptom of upstream
uncertainty rather than proof of a scope-default bug. It is not safe to claim
that a simple default would recover 39 comparisons. Other model/version gaps,
source admission, catalogue/date success and unknown population remain independent.

## All retained occurrences

`U` applies the complete branch/uncertainty analysis above to **each** row. Source
plus GA and model type, with common context/classifier, identify each occurrence here;
R-numbers are audit-local labels in original JSON order, not schema identifiers.

| Audit ID | Source | Public GA | Model type | Retained version | Scope trace |
| --- | --- | --- | --- | --- | --- |
| R01 | api/pom.xml | ch.qos.logback.access:logback-access-tomcat | jar | 2.0.7 | U |
| R02 | api/pom.xml | com.datadoghq:java-dogstatsd-client | jar | 4.4.5 | U |
| R03 | api/pom.xml | com.okta.jwt:okta-jwt-verifier | jar | 0.5.14 | U |
| R04 | api/pom.xml | dev.akkinoc.spring.boot:logback-access-spring-boot-starter | jar | 5.0.0 | U |
| R05 | api/pom.xml | gov.cms.ab2d:ab2d-events-client | jar | 3.3.19 | U |
| R06 | api/pom.xml | net.logstash.logback:logstash-logback-encoder | jar | 9.0 | U |
| R07 | api/pom.xml | org.apache.httpcomponents.client5:httpclient5 | jar | 5.6.4 | U |
| R08 | api/pom.xml | org.apache.httpcomponents.core5:httpcore5 | jar | 5.4.4 | U |
| R09 | api/pom.xml | org.springdoc:springdoc-openapi-starter-webmvc-ui | jar | 2.8.9 | U |
| R10 | common/pom.xml | ca.uhn.hapi.fhir:hapi-fhir-structures-dstu3 | jar | 8.12.1 | U |
| R11 | common/pom.xml | ca.uhn.hapi.fhir:hapi-fhir-structures-r4 | jar | 8.12.1 | U |
| R12 | common/pom.xml | com.datadoghq:dd-trace-api | jar | 1.63.0 | U |
| R13 | common/pom.xml | commons-fileupload:commons-fileupload | jar | 1.6.0 | U |
| R14 | common/pom.xml | commons-io:commons-io | jar | 2.19.0 | U |
| R15 | common/pom.xml | gov.cms.ab2d:ab2d-contracts-client | jar | 2.3.2 | U |
| R16 | common/pom.xml | gov.cms.ab2d:ab2d-events-client | jar | 3.3.19 | U |
| R17 | common/pom.xml | gov.cms.ab2d:ab2d-fhir | jar | 2.5.11 | U |
| R18 | common/pom.xml | io.awspring.cloud:spring-cloud-aws-dependencies | pom | 4.1.1 | U |
| R19 | common/pom.xml | io.awspring.cloud:spring-cloud-aws-starter-sqs | jar | 4.1.1 | U |
| R20 | common/pom.xml | org.apache.commons:commons-compress | jar | 1.28.0 | U |
| R21 | common/pom.xml | org.modelmapper:modelmapper | jar | 3.2.4 | U |
| R22 | common/pom.xml | org.postgresql:postgresql | jar | 42.7.14 | U |
| R23 | common/pom.xml | org.springframework.cloud:spring-cloud-starter-openfeign | jar | 5.0.1 | U |
| R24 | coverage/pom.xml | com.datadoghq:java-dogstatsd-client | jar | 4.4.5 | U |
| R25 | e2e-bfd-test/pom.xml | ca.uhn.hapi.fhir:hapi-fhir-client | jar | 8.12.1 | U |
| R26 | e2e-bfd-test/pom.xml | gov.cms.ab2d:ab2d-bfd | jar | 4.8.5 | U |
| R27 | e2e-bfd-test/pom.xml | io.awspring.cloud:spring-cloud-aws-starter-sqs | jar | 4.1.1 | U |
| R28 | e2e-test/pom.xml | gov.cms.ab2d:ab2d-events-client | jar | 3.3.19 | U |
| R29 | e2e-test/pom.xml | io.jsonwebtoken:jjwt-api | jar | 0.12.6 | U |
| R30 | e2e-test/pom.xml | org.yaml:snakeyaml | jar | 2.0 | U |
| R31 | job/pom.xml | org.postgresql:postgresql | jar | 42.7.14 | U |
| R32 | worker/pom.xml | ca.uhn.hapi.fhir:hapi-fhir-client | jar | 8.12.1 | U |
| R33 | worker/pom.xml | com.datadoghq:java-dogstatsd-client | jar | 4.4.5 | U |
| R34 | worker/pom.xml | gov.cms.ab2d:ab2d-aggregator | jar | 2.1.9 | U |
| R35 | worker/pom.xml | gov.cms.ab2d:ab2d-bfd | jar | 4.8.5 | U |
| R36 | worker/pom.xml | gov.cms.ab2d:ab2d-events-client | jar | 3.3.19 | U |
| R37 | worker/pom.xml | gov.cms.ab2d:ab2d-filters | jar | 3.2.6 | U |
| R38 | worker/pom.xml | gov.cms.ab2d:ab2d-sns-client | jar | 1.1.14 | U |
| R39 | worker/pom.xml | net.logstash.logback:logstash-logback-encoder | jar | 9.0 | U |

## Offline verification and next step

Existing focused regressions: `PYTHONPATH=tests python3 -m unittest
 test_maven_facts test_maven_project test_maven_acceptance test_maven_scan`:
**95 PASS**. They cover established omitted-scope compile defaults, explicit and
inherited scope, managed precedence, unresolved imports, malformed management,
blocked keys/fallback, profile effects and independent safe siblings.

An additional in-memory staged fixture uses a missing external parent, a refused
scope-less root requirement, an explicit same-GA child requirement and independent
safe siblings. Admission excludes only the refused occurrence; same-GA shared
metadata refusal does not relabel it. Synthetic catalogue refusals are injected;
no date lookup or new age is produced. Counterfactually forcing compile when the
selector returns no scope mints a prohibited capability and makes **two existing
boundary regressions fail**, as expected. Removing the patch restores the original
code; no production or tracked test bytes are changed. This negative witness
rejects the proposed unsafe shortcut; it does not reconstruct AB2D inputs.

The next useful step is separately authorized, bounded **source-evidence capture**
for these seven POMs and their contained parent/management/profile context, using
safe reader boundaries. To make claims about these historical 39, captured bytes
must match retained input hashes; changed bytes support only a new offline case.
Keep any raw snapshots private and retain only safe field/uncertainty provenance.
No external parent/BOM fetching, parser expansion, resolver, live measurement or
new population policy follows. There is no consequential product choice to invent
before first obtaining the missing factual evidence.

Original `007-0030` handoff/artifact validate at the expected completion revision;
it is appended once with supplied run-level 443-second telemetry and confirmed
164/164 account readings. Original notes/runtime qualifications and earlier ledger
bytes remain unchanged. Ledger: 80 unique rows, 44 columns; `007-0031` is not
appended. Review/final documentation checks are recorded below at closure.

## Review and closure

Two fresh non-author scopes completed: scope/defaulting/contract **APPROVE after
focused correction**; admission/security/uncertainty/siblings **APPROVE**. The
initial draft's all-jar assertion was caught by exact-key verification and the
semantics review; corrected table/prose retain 38 jar rows and R18's ordinary pom
row, explicitly distinct from a BOM import. Original finding and correction are
preserved here; no product defect was established. Both reviewers inspected the
corrected frozen bytes and independently ran the 95 focused tests and offline
negative witness. Parent validated their findings and collateral coverage. New
child contexts, no overrides requested; actual child configuration/resources are
unobserved. The semantic reviewer directly inspected the pinned upstream evidence.

Exact 39-row/key/type/origin checks, 16 local links/anchors across the new record
and audit, ledger prefix/shape/uniqueness, whitespace and sensitivity checks pass.
Configured GitLeaks current-content and committed-history gates pass; final commit
identity/history counts and clean-tree verification are in the current durable
handoff. No runtime or tracked test files changed, so full-suite,
capability-disabled and worker reruns for code corrections are not applicable.
No target/trust/private input access, package endpoint, build, live measurement,
push, tag or release. Any source capture requires separate access authorization.

Follow-up: [007-0032 captured scope context](maven-scope-context.md) establishes
historical eight-POM correspondence and resolves the 39 original local refusal
paths: 38 lack matching management, one matches only an import entry; all retain
external-parent/BOM uncertainty. No runtime defect or scope-default repair is
established. The earlier missing-snapshot limitation above remains historical.
