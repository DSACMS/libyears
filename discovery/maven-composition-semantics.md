# Maven composition semantics — 007-0037

## Result and limits

**Seven conditional compile-scope conclusions; 32 unresolved controls.** Pinned
Maven 3.9.11 implementation establishes whole-entry management dominance, so
unread competing imports cannot supply a different scope to the seven identified
keys within the bounded static model below. No additional parent/BOM acquisition
is necessary for that field proof. This is stronger than 007-0036's unverified
composition triage, not proof that Maven can successfully build the incomplete
corpus or that these were historical build inputs.

| Claim level | Count / disposition |
| --- | --- |
| Unqualified historical/evaluated scopes established | 0 |
| Conditional bounded-static scope=compile | 7: five Boot, two AWS |
| Remaining unresolved scope occurrences | 32, unchanged control population |
| Production admissions / new ages / accepted denominator | None |

The conditional basis explicitly accepts the retained model representations,
uses their supported literal identities and scalar environments, excludes external
host/user/settings profile additions, plugins/evaluation and unknown target state,
and claims only noninterference for these exact direct keys. It does **not**
assume unknown models are empty. Full resolution/validation, acquisition history,
actual applicability, runtime selection and model completeness remain unproved.
All 39 existing versions and all 42 scope-ready keys/facts are preserved.

## Recovery and pinned evidence

Expected clean starting HEAD `f2783cc1465ff45879e7f2cb63cc92af213874a3` matches.
Governing history: [consumer audit](maven-consumer-context-audit.md),
[its review](maven-consumer-context-audit-review.md),
[feasibility](maven-external-management-feasibility.md),
[current S3](../specs/007-maven-dependency-age/spec.md#s3--maven-population-and-bounded-local-model)
and [source policy](../specs/007-maven-dependency-age/source-policy.md).
No target, trust input, machine configuration/cache or dependency POM was accessed
anew. Only explicitly authorized public Apache implementation/test/documentation
representations were retrieved, with verified TLS and no redirect following.

The versioned [model-builder documentation](https://maven.apache.org/ref/3.9.11/maven-model-builder/)
was the entry point. Apache's annotated release tag `maven-3.9.11`, tag object
`339fe48df7db320254962351797638d358958c93`, resolves to commit
`3e54c93a704957b63ee3494413a2b544fd3d825b`. Exact raw files below are pinned to that
commit, not a moving branch. Tag/reference bytes, URL/digest and release association
are retained; the initial ref capture lacks original request timestamp/status/size
fields. Successful artifact records retain URL/retrieval time/SHA256/size and curl
exit status in `D/007-0037/apache-evidence.json`, with bytes in `apache/`, where D
is resolved by the observation helper. Failed source/test representations are
recorded; publisher xref alternatives and an exact pinned interpolation-test
directory lookup were used within scope. No TLS exception or endpoint workaround.

Attribution: The Apache Software Foundation, Apache-2.0; original file headers
and author credits (including Benjamin Bentmann) remain in exact private files.
Existing [LICENSE](../third_party/maven-3.9.11/LICENSE) and
[NOTICE](../third_party/maven-3.9.11/NOTICE) remain intact. Tracked prose paraphrases
facts; no full Java source is copied or executed.

## Rule/source matrix

| Pinned rule | Decisive implementation and qualification |
| --- | --- |
| Parent inheritance precedes consumer interpolation | [Builder](https://github.com/apache/maven/blob/3e54c93a704957b63ee3494413a2b544fd3d825b/maven-model-builder/src/main/java/org/apache/maven/model/building/DefaultModelBuilder.java#L289-L421) clones raw lineage models, reads external parents as raw models (1012–1096), assembles inheritance, then interpolates the result. An independently built effective parent is not substituted on this path |
| Child properties win inherited model properties | [InheritanceAssembler](https://github.com/apache/maven/blob/3e54c93a704957b63ee3494413a2b544fd3d825b/maven-model-builder/src/main/java/org/apache/maven/model/inheritance/DefaultInheritanceAssembler.java#L60-L66) calls merger with sourceDominant=false; its properties override at 190–212 places child values last. The resulting consumer model supplies interpolation properties |
| Same-key list inheritance is whole-entry selection here | [ModelMerger](https://github.com/apache/maven/blob/3e54c93a704957b63ee3494413a2b544fd3d825b/maven-model/src/main/java/org/apache/maven/model/merge/ModelMerger.java#L2357-L2452) target entries precede parent entries; SourceDominant(false) retains the target object. Dependency-management lists use that keyed list merge at 1081–1089. Child list order is preserved; inherited missing keys append. This differs from field injection |
| Imports cannot fill fields of an existing management key | [Importer](https://github.com/apache/maven/blob/3e54c93a704957b63ee3494413a2b544fd3d825b/maven-model-builder/src/main/java/org/apache/maven/model/composition/DefaultDependencyManagementImporter.java#L45-L78) seeds target entries, then inserts absent keys from import sources in order. First source wins a repeated imported key as a whole entry, even when its scope is absent |
| BOM import is an independent model build | Builder 1104–1261 removes type=pom/scope=import declarations, builds each import with its own source and inherited properties, obtains only its effective management, then invokes the importer. Request user/system properties are forwarded; consumer model properties are not. Caching does not re-interpolate the imported management in the consumer |
| Interpolation traverses the chosen model, including management | [Visitor](https://github.com/apache/maven/blob/3e54c93a704957b63ee3494413a2b544fd3d825b/maven-model-builder/src/main/java/org/apache/maven/model/interpolation/StringVisitorModelInterpolator.java#L94-L103) and AbstractStringBasedModelInterpolator 99–174 use model properties (plus broader request sources outside this basis). Factory 127–133 selects StringVisitor; versioned docs mention deprecated StringSearch, so source/factory controls. Visitor 861–871,960–966,1029–1092 traverses management/dependencies and clears changed identity keys |
| Management injection is field-level and non-dominant | [Injector](https://github.com/apache/maven/blob/3e54c93a704957b63ee3494413a2b544fd3d825b/maven-model-builder/src/main/java/org/apache/maven/model/management/DefaultDependencyManagementInjector.java#L57-L83) matches ordinary dependencies and fills absent managed fields; ModelMerger scope routine 880–889 copies a nonnull managed scope only if target scope is null. Explicit ordinary versions/scopes survive. Optional is not managed |
| Default scope waits until after injection | [Normalizer](https://github.com/apache/maven/blob/3e54c93a704957b63ee3494413a2b544fd3d825b/maven-model-builder/src/main/java/org/apache/maven/model/normalization/DefaultModelNormalizer.java#L101-L118) sets empty ordinary dependency scope to compile. It does not default management-entry scopes. Builder 528–533 orders import → injection → defaults |
| Keys include exact type/classifier | [Dependency model](https://github.com/apache/maven/blob/3e54c93a704957b63ee3494413a2b544fd3d825b/maven-model/src/main/mdo/maven.mdo#L1224-L1236) uses groupId:artifactId:type plus classifier when present; MavenModelMerger 542–544 uses that key. No artifact-handler alias or GA-only substitution |

Tests inspected, **not executed**: DefaultModelBuilderTest.testCycleInImports
checks cycle handling, not dominance; AbstractModelInterpolatorTest's dependency-
version/project-version case and StringSearchModelInterpolatorTest corroborate
scalar context behavior in the legacy interpolator, not full Visitor conformance.
DefaultInheritanceAssemblerTest covers its assembly harness/URL cases;
ModelMergerTest tests serialization, not this seven-key dominance. A dedicated
importer test at the initially named path and its xref representation were not
retrievable; no nonexistent test is claimed to pass. Decisive precedence facts
come from the actual implementation call path, with bounded Python probes below.

**Compatibility qualification:** the pinned keyed-list collision path selects
whole entries, while current approved local S3 deliberately specifies field-level
inheritance. The seven paths do not depend on a same-key child/parent ordinary
field collision, and all preserved facts still agree. Future external intake must
state that boundary explicitly and preserve existing local authority; this source
finding does not authorize a local semantic repair or claim a runtime defect.

## Seven-occurrence derivation

The retained chain for H is consumer → local root → Boot starter parent 4.1.1 →
Boot dependencies 4.1.1. The Boot management entries exist before consumer imports,
have exact literal jar/absent-classifier keys and omit scope. No nearer management
entry replaces them. Every competing import therefore loses the entire key;
its scope cannot fill the omitted field. Ordinary scope is also omitted, management
injection supplies no scope, and final normalization gives compile.

For I, consumer root's first import is AWS dependencies 4.1.1; the same order and
version hold in both consuming child contexts. Its own explicit starter-sqs entry
wins over its inherited/imported management. The AWS parent is Spring Cloud
dependencies parent 5.0.3. The built AWS management is imported with its own
property environment; consumer root/children do not re-expand it. No target
ordinary-management entry precedes it for this key, and later imports cannot
replace it. Scope stays absent until ordinary compile normalization.

All direct parent-chain and AWS-parent-chain profiles are inspected: none writes
properties or management relevant to these entries; nativeTest's added literal
JUnit key differs. Repository/build profiles do not create a dependency scope.
Unseen imported profiles could affect their own management, but cannot override
the shielded key. Their errors can still prevent a successful full Maven build;
that unresolved validity is why the conclusion is conditional, not an effective
POM or successful-build claim.

Exact candidate document identities:

- **B**: org.springframework.boot:spring-boot-dependencies:4.1.1, SHA256
  `1c929eeccb48f8ee12225e9fec725177170b89575754bd903f184c185db77775`.
- **A**: io.awspring.cloud:spring-cloud-aws-dependencies:4.1.1, SHA256
  `e225a22c0f0269c4ea80fa78c23a0da6ef207cb7cb1bf6e95503ab070131ad0a`.

The corpus freeze binds their ancestor and consumer documents too; these are POM
byte digests, not certificate fingerprints. All seven are base_model, jar, absent
classifier and original refusal path A. Stable identity includes the full
source-qualified key; R numbers remain historical audit labels.

| ID | Consumer / exact GA | Retained request → exact version | Candidate / required rule | Supported field within basis |
| --- | --- | --- | --- | --- |
| R07 | api/pom.xml / org.apache.httpcomponents.client5:httpclient5 | `5.6.4` → 5.6.4 | B / existing target management key | conditional compile; final default |
| R08 | api/pom.xml / org.apache.httpcomponents.core5:httpcore5 | `5.4.4` → 5.4.4 | B / existing target management key | conditional compile; final default |
| R19 | common/pom.xml / io.awspring.cloud:spring-cloud-aws-starter-sqs | `${spring-cloud-aws.version}` → 4.1.1 | A / own-key and first-import dominance | conditional compile; final default |
| R22 | common/pom.xml / org.postgresql:postgresql | `${postgresql.version}` → 42.7.14 | B / existing target management key | conditional compile; final default |
| R27 | e2e-bfd-test/pom.xml / io.awspring.cloud:spring-cloud-aws-starter-sqs | `${spring-cloud-aws.version}` → 4.1.1 | A / own-key and first-import dominance | conditional compile; final default |
| R30 | e2e-test/pom.xml / org.yaml:snakeyaml | `2.0` → 2.0 | B / existing target management key | conditional compile; final default |
| R31 | job/pom.xml / org.postgresql:postgresql | `${postgresql.version}` → 42.7.14 | B / existing target management key | conditional compile; final default |

Each row has no ordinary scope and no winning managed scope; the newly derived
scope origin is final default normalization, not an imported explicit scope.
All exact used versions remain ordinary explicit fields, with retained property
origins where applicable; management cannot replace them. Full site/index,
ancestor/import paths and source-control witnesses are in `D/007-0037/proof.json`.
No production origin/provenance schema is changed.

## Controls, acquisition relevance and recommendation

The other **32** keys retain their prior unresolved classification. This run does
not prove absent applicable management for them, interpret all recursive models,
or turn a default into their scope. The original R18 ordinary-pom/import-only
path remains among these controls. Shared unknown flags are not extra occurrences.
All **127** historical local-fact rows, original **38/1** paths, **39** exact-version
facts and **42** scope-ready keys/scope/version/optional triples reproduce. The
42 triples also agree under the inspected whole-entry ordinary composition for
these actual snapshots. No safe sibling is erased; 46 version gaps/two catalogue
failures/historical 40 measurements are not re-investigated or replaced.

The four inherited import expressions now have source-backed consumer-context
substitution in this bounded basis: Jackson 2 BOM 2.22.3, Netty BOM 4.2.18.Final,
Kotlin BOM 2.1.0 and Testcontainers BOM 1.21.4 (full GAVs retained in 007-0035).
Those are not imported-BOM property leakage. A complete Maven model would need
applicable imports resolved; this fact does **not** make those four documents
necessary to decide the seven shielded fields. The six previously queued absent
models likewise cannot change these seven winning slots. No additional POM
acquisition is justified for this specific noninterference proof. Necessary
content for the 32, full model validity or population remains a separate question;
no claim is made that the ten-document list completes any closure.

`D/007-0037/proof.py --verify` validates Apache/body/candidate hashes and baseline,
then repeats the small keyed inheritance/import/injection/default demonstrations.
It tests 49 competing-scope sentinel cases across the seven paths, including
uninterpretable later scope, and discriminates first/last import order, whole-entry
selection versus field filling, explicit version preservation and BOM-own-context
project.version. Sentinels stand for possible management values, not arbitrary
model validity or executable effects. No Java, Maven or upstream tests execute;
these probes are not full-model equivalence certification. Raw sources, failures,
procedures and results remain private durable engineering evidence.

**Recommendation:** sufficient semantic evidence to propose a **restricted,
explicitly accepted static-model intake specification**, if the human selects a
claim permitting key-dominance field proofs without proving complete Maven model
validity. The supported result is seven conditional fields, not seven measurable
dependencies. That consequential claim/compatibility choice is the next gate;
no specification is started here. If complete successful evaluated models are
required instead, defer that intake or separately investigate supplied evaluated
model evidence. Do not solve that product choice by automatically acquiring more
POMs or building a generic resolver.

The [separate review](maven-composition-semantics-review.md) records independent
accuracy/safety review, bookkeeping and actual final checks. Current product
behavior, approved local contracts, source policy, dates, metrics and output stay
unchanged. Push performed: **NO**.
