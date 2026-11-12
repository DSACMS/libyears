# Feature 007 deterministic verification

T012 candidate, based on converged T011 `c433f05`. The approved [specification](spec.md),
[plan](plan.md), [tasks](tasks.md) and [review record](reviews.md) govern this report.
This is deterministic conformance evidence, **not completed Feature007 operational
validation or release/publication**. Actual DPC usefulness/integrity remains pending
[GPUBLIC and T013](validation-preparation.md); T014 final convergence follows it.

## Implemented scope and evidence chain

Ordinary directory scans build bounded safe POM snapshots, supported local base-model
Declared occurrences, local comparator decisions, closed accepted capabilities,
whole current GA selection, exact POM modification dates and independent Maven views.
No Observed reader, join, target execution, resolver, parent/BOM fetching, archive,
Gradle or new supplier format exists. Maven does not enter legacy scalar rows/totals.

The converged implementation boundaries in this run are:

| Task | Local commit / checkpoint |
| --- | --- |
| T006 | `2fad613` local comparator admission; independent authority/privacy checkpoint |
| T007 | `d417426` pure catalogue/POM/date parsers |
| T008 | `caf6635` supervised fixed-public HTTPS; independent security/lifecycle checkpoint |
| T009 | `b1111b5` source orchestration and admitted age results |
| T009 bounded correction | `6e8a616` accepted catalogue freshness retained independently for S7 output |
| T010 | `4330270` directory dispatch, additive schema3 and paired human output |
| T011 | `c433f05` decomposed integrated adversarial checkpoint and unknown-dependency refusal correction |

T001–T005 remain the immutable predecessors ending at `9cdca81`. One local commit
per converged task was preserved; the later freshness correction has its own fix
commit, with no history rewrite or task-boundary collapse. T012 final approval/hash
is recorded in reviews and Git after the frozen documentation candidate is reviewed.

## Deterministic verification

Commands run from the repository root:

```text
python -m unittest discover -s tests
python -m unittest discover -s tests -p 'test_maven*.py'
git diff --check
python tools/check_gitleaks.py
```

The T011 implementation checkpoint passed **1080 tests run,1 skipped**, including
**297 Maven tests** and10 integrated acceptance tests. The T012 candidate independently reran the full suite: **1080 run,1 skip,PASS**
on CPython3.11.0/darwin. Local link/anchor verification checked239 references across
18 current/Feature007/provenance documents with zero failures. Configured GitLeaks
8.30.1 history346 and current documentation scans pass before the T012 commit;
post-commit history and exact frozen digests accompany its convergence record.

A separate run patches `os.supports_dir_fd` to an empty set **before test discovery**:
1080 run,99 skipped,PASS. This checks portable semantic and explicit refusal paths,
not positive native Windows behavior. Sixteen sibling-semantics modules supply
certified Maven absence as fixture input; native Maven discovery/refusal has separate
witnesses. No runtime safety primitive was weakened to preserve old fixture results.

Native filesystem/process tests on this host include contained no-follow snapshots,
links/changes/bounds, actual trusted isolated worker readiness/import exclusion,
blocked-worker kill/reap, death/malformed-protocol refusal and retained deferred
handles. Independent reviews also used anonymous local socketpairs to reproduce
partial timeouts and validate byte/framing corrections. They contacted no endpoint.
Injected raw HTTP/clock/lookup fixtures do not prove live TLS/registry fitness.

[Configured CI](../../.github/workflows/ci.yml) declares Linux/macOS/Windows × Python
3.11–3.13, but this unpublished candidate has no executed hosted matrix. Required
missing filesystem/process capabilities fail closed. No positive Windows-support,
complete evaluated model or real-target-yield claim follows from skipped/injected tests.

## Acceptance accounting

All deterministic obligations are closed by actual code/tests and independent
reviews. Operational components are explicitly pending rather than marked passed.
Test files contain the exact behavioral cases; [T011 reconciliation](reviews.md#run007-0014--t011-integrated-adversarial-checkpoint)
records the independent audit slices, defect and focused closure.

| AC | Actual offline witnesses / remaining operational evidence |
| --- | --- |
| AC01 | [Model](../../tests/test_maven_model.py), [results](../../tests/test_maven_results.py), [paired output](../../tests/test_maven_output.py); initial Observed unavailable |
| AC02 | [Project](../../tests/test_maven_project.py), [facts](../../tests/test_maven_facts.py), model source/context/exact-key association/refusal |
| AC03 | Full S6 result matrix, [scan compositions](../../tests/test_maven_scan.py), [integrated occurrence weighting](../../tests/test_maven_acceptance.py) |
| AC04 | Project/fact partial inheritance, delayed defaults, unmanaged optional and consuming-source origins |
| AC05 | Fact/acceptance management/import field precedence, no BOM population/fetch, blocked unsafe same-key fallback |
| AC06 | Project handlers/model keys; acceptance plain/test-jar/classifier/POM/tooling/system scope; no systemPath read |
| AC07 | [Property](../../libyears/maven_properties.py)/fact/version tests; consumer context, reserved builtins/cycles/budgets/snapshot refusal |
| AC08 | Fact/project/scan and conditional-internal acceptance cases; safe rows with null N/coverage |
| AC09 | Model/scan/output reader-unavailable and Maven/Gradle divergence; no fabricated selection/intake |
| AC10 | [Policy](../../tests/test_maven_policy.py), credential/extension/denied-GA acceptance; zero forbidden requests |
| AC11 | [Pinned version](../../tests/test_maven_version.py), [registry](../../tests/test_maven_registry.py), scan/output; terminal dates/global maximum/exact zero/conventional disclosure |
| AC12 | Output plus integrated privacy/known/unknown/unavailable/zero cases; independent seven-field paired summaries |
| AC13 | Output Maven-only, four successful/empty sibling, all-unavailable mixed and incomplete-discovery witnesses; old source suites retain their contracts |
| AC14 | Synthetic ordinary module/CLI preparation; **actual authorized DPC witness pending GPUBLIC/T013**, no target N/yield promise |
| AC15 | Acceptance reuses retained AB2D external-parent/type/POM/Gradle shapes; native POM-only reads, no target/Gradle intake |
| AC16 | Input integrity, offline guards/privacy/[HTTP](../../tests/test_maven_http.py)/[worker](../../tests/test_maven_worker.py); **actual target integrity/disclosure pending T013** |
| AC17 | Exact repository/profile/settings/mirror/launch/filter/extension policy and all-local-before-batch staging |
| AC18 | [Discovery](../../tests/test_maven_discovery.py)/[input](../../tests/test_maven_input.py)/model/property/policy/version/registry/header/body/scan budget refusals |
| AC19 | Worker/protocol/HTTP isolation, blocked deadline, death/no restart/fallback/deferred handle and unskipped capability refusal; hosted matrix unexecuted |
| AC20 | Pinned aliases/service packs/prereleases/snapshots/unknown-below versus equal-above/ties and bounded catalogue selection |

Synthetic DPC-shaped N6/M3 or N6/M0 and AB2D-shaped typed rows are small counterexamples,
not measurements of those repositories. Retained discovery's198 written DPC elements
are not a metric denominator. A useful eventual witness may have no positive age yield
if attributable requests and understandable limitations remain; it cannot claim
complete evaluated scope, observed selection or successful execution.

## Review findings and correction provenance

The run recovered durable authority across a fresh parent boundary without a new
T006 task grant. Independent reviews and bounded corrections closed ten material
implementation/evidence gaps: four T006 admission/relevance/grammar defects, one
T007 identity-normalization defect, three T008 streaming/framing defects, separate
S7 catalogue-freshness retention and one T011 unsupported-dependency admission defect.
Original REVISE dispositions remain in [reviews](reviews.md); fresh focused closure
was obtained rather than overruling findings with positive sibling slices.

One qualifying public evidence read was needed: the pinned Maven3.9.11 model reference.
[Policy facts](../../third_party/maven-3.9.11/policy-facts.json) retain the exact URL,
retrieval UTC, SHA256,14 build-field names, ASF attribution/transformation/limits.
Raw HTML stays temporary; Apache LICENSE/NOTICE are unchanged. There was no package
metadata request, private/target access, new production trust relationship or external
code execution. Existing source/version pin provenance remains in that directory.

The initiating fresh-parent prompt restated persistence; the repository independently
contained the execution envelope and task/security state. No new decision or additional
human reauthorization relay occurred. This does not isolate behavior with a prompt
containing no authority reminder. The boundary demonstrated recoverable state, not causal
fresh-context safety, resource savings or generalized harness effectiveness. No
important conversation-only normative dependency was found. No harness or SKILL was
created. Native child configuration/resources and current account/runtime telemetry
remain unobserved; no credit delta or runtime subdivision was fabricated.

## Remaining gates

T012 approval establishes deterministic readiness only. GPUBLIC must separately
identify/authorize the exact public DPC target/path/revision/status, public coordinate
HTTP disclosure, safe artifact/diagnostic/reviewer capture and read-only integrity.
T013/T014 are not complete. Private validation and push/release/publication remain
separately gated. No target access or publication follows merely from this report.
