# Maven latest comparator — run007-0007 reviewed decision candidate

## Selected policy — run007-0008

The human selects **conservative known-stable with potentially maximal unknown
refusal**, including the exact numeric/release-alias/service-pack whitelist below.
Machine identifier: `maven_conservative_stable_v1`. The two alternatives and their
then-pending gate below remain historical decision evidence; broad admission is
not selected.

Apply the retained shared snapshot/prerelease exclusions first. Let E be the
known-eligible exact strings under the whitelist. If E is empty, latest is
unavailable. Otherwise compute its Maven-ordered maximum. Compare every remaining
unknown safe exact string under the same pinned ordering: unknown strictly below
that maximum cannot change it and does not poison the catalogue; unknown at or
above it gives `unknown_latest_eligibility`. An inability to order a relevant value
safely within budgets makes latest unavailable, never guessed. Finally require
one exact eligible maximum string; distinct equal maxima give
`ambiguous_latest_version`. Identical strings are duplicates, not ties. No date
can resolve eligibility or a tie.

The rationale is claim-specific uncertainty: inability to prove an unfamiliar
qualifier prerelease does not establish authority to call it stable. Lower yield
is preferred to silently accepting unfamiliar preview/development conventions.
Unfamiliar versions are not declared invalid or undesirable. The rule withholds
only an unsupported default comparison target.

The selected target remains global across the accepted GA catalogue, independent
of requested family/type/classifier, with no compatibility/variant history claim.
ComparableVersion3.9.11 and complete current GA metadata remain the technical
basis. Service packs and ga/final/release aliases are eligible; alpha/beta/
milestone/rc (including pinned aliases) and snapshots (including timestamped
forms) are excluded. Measured-version admission remains independently governed
by S4. Historical recommendations below are superseded by this selection.


The human selected conventional time evidence, not a latest/stable predicate.
Read with [S7](spec.md#s7--maven-comparator-evidence-cascade-and-conventional-time-basis)
and the retained [ordering investigation](publication-history.md#question2-catalogue-ordering-and-product-eligibility).
No new timestamp/provider or portfolio survey was performed. This document presents
policy alternatives; neither is selected. Review disposition lives in [reviews](reviews.md).

## Technically determined catalogue and precedence

Use the entire accepted Central GA metadata available-version list, not latest,
release, Search, a provider, directory listing or modification-date order. Reject
incomplete/unsafe/incoherent/over-budget responses. Current catalogue may change;
no all-ever history, atomic state or variant availability is claimed. See the
[Maven metadata model](https://maven.apache.org/ref/3.9.11/maven-repository-metadata/repository-metadata.html).

Freeze Apache Maven maven-artifact **ComparableVersion3.9.11** as the conventional
artifact precedence. This is not “whatever Maven currently resolves.” Its pinned
[source](https://maven.apache.org/ref/3.9.11/maven-artifact/xref/org/apache/maven/artifact/versioning/ComparableVersion.html)
and [tests](https://raw.githubusercontent.com/apache/maven/maven-3.9.11/maven-artifact/src/test/java/org/apache/maven/artifact/versioning/ComparableVersionTest.java)
govern numeric segments, separators, digit/letter transitions and qualifier aliases.
Known precedence is alpha < beta < milestone < rc < snapshot < empty < sp, followed
by unknown qualifiers in lexical qualifier order. cr aliases rc; ga/final/release
alias empty; a/b/m expand only when followed by a digit in that implementation.
Case-insensitive ordering is not case-insensitive coordinate/path identity.

Maven3.9.11's [range resolver](https://maven.apache.org/ref/3.9.11/maven-resolver-provider/xref/org/apache/maven/repository/internal/DefaultVersionRangeResolver.html)
uses GenericVersionScheme; it is a distinct range mechanism, not required for this
maximum claim. Its [documented rules](https://maven.apache.org/resolver/maven-resolver-util/apidocs/org/eclipse/aether/util/version/GenericVersionScheme.html)
must not be substituted. Current unversioned POM prose treats underscore as a
separator; pinned ComparableVersion3.9.11 does not. Later offline conformance must
cover that discrepancy, aliases, nested segments, digit transitions and equality.
No Java/Maven execution or generic cross-ecosystem version framework follows.

Ordering does not decide stability. Central imposes [no universal version convention](https://central.sonatype.org/publish/requirements/coordinates/).
Tools differ: retained [practice evidence](ecosystem-practice.md#latest-practice-utility-and-human-gate)
shows Renovate accepts unknown forms such as1-foo as stable, Dependabot adds request
and prerelease filters, and OpenRewrite uses its own selector grammar. None is a
universal Maven default, and none is adopted wholesale.

## Shared safeguards for both serious alternatives

- Exclude case-insensitive SNAPSHOT qualifier tokens, Maven suffix snapshots and
  timestamped snapshots recognized by pinned [ArtifactUtils3.9.11](https://maven.apache.org/ref/3.9.11/maven-artifact/xref/org/apache/maven/artifact/ArtifactUtils.html).
  Do not expand/fetch snapshot metadata. Measured requests retain S4's snapshot refusal.
- Exclude candidates with alpha, beta, milestone or rc tokens, including cr alias
  and context-dependent a/b/m plus digit aliases under the pinned tokenizer.
  A numeric-only used version does not permit a prerelease comparator. Used
  prerelease versions can still be exact declared facts; latest eligibility and
  measured-version admission are independent.
- Candidate entries are safe exact version strings, never ranges, LATEST/RELEASE
  selectors or property expressions. A range/selector in the catalogue invalidates
  candidate admission; request ranges remain unsupported except the existing hard
  singleton request unwrapping. A spelling “release” inside an exact numeric version
  is a qualifier alias, distinct from the dynamic selector RELEASE.
- Collapse only identical catalogue strings. Multiple distinct eligible maximum
  strings (e.g.1,1.0,1.0.0, or1.0-final when present together at the maximum) make
  latest unavailable, even if their dates agree. No lexical, response-order or
  date tie-break. Exact aliases still name distinct POM paths.
- Select greatest eligible version before dates; missing target POM/date ends the
  measurement, never selects an older candidate. Same exact version still requires
  admitted time evidence before producing exact0.0.
- Recommend a **global current GA maximum**, independent of requested major/family,
  range, scope, type and classifier. This measures freshness, not a compatible
  upgrade. Preserve module/model/artifact identities and disclose that GA/POM
  evidence certifies no classifier availability/history or compatibility.

## Two consequential alternatives

For precision, define the conservative known-stable syntax as a numeric core
`[0-9]+(?:[.-][0-9]+)*`, optionally followed by one ga/final/release alias or sp
service-pack qualifier with optional decimal number, with an optional dot/hyphen
before that qualifier. Match the entire string, ASCII case-insensitively. Thus
1,1.0,1-0,1.0.Final,1.0RELEASE,1.0-sp and1.0-sp2 qualify. Any recognized prerelease
or snapshot above remains excluded first. This is a deliberate libyears whitelist,
not a Maven grammar or proof of publisher intent.

| Alternative | Exact additional rule | Maven establishes / libyears adds |
| --- | --- | --- |
| **Conservative known-stable (recommended)** | Admit only the known-stable syntax above. Other safe non-prerelease strings are **unknown**, not silently unstable. If any unknown compares at or above the greatest admitted candidate, latest is unavailable (`unknown_latest_eligibility`). Unknown below that maximum cannot affect it. With no admitted candidate, latest is unavailable. | Maven supplies precedence/token aliases; libyears supplies whitelist, service-pack eligibility and uncertainty refusal |
| **Broad conventional non-prerelease** | Admit every safe exact candidate not excluded by the shared snapshot/known-prerelease rules, including unknown qualifiers and nonnumeric forms. Then require a unique greatest exact string. | Maven supplies precedence; libyears deliberately treats absence of recognized prerelease tokens as sufficient stability convention |

Both admit service packs and recognized release aliases. This is explicit policy,
not a claim that Maven calls every service pack stable. Maven precedence can place
unknown qualifiers above sp; no bare ordering result becomes stability evidence.

| Catalogue boundary (illustrative strings) | Conservative | Broad |
| --- | --- | --- |
| 1.0,2.0-RC1,2.0-beta2,2.0-M1 | 1.0 | 1.0 |
| 1.0,1.0-sp1 | 1.0-sp1 | 1.0-sp1 |
| 1.0,2.0-preview1 | unavailable: unknown potentially maximal | 2.0-preview1; possible prerelease false positive |
| 1.0,2.0-redhat-1 | unavailable: unknown potentially maximal | 2.0-redhat-1; variant/fork-like label is not source authority |
| 1.0-foo,2.0 | 2.0 if foo orders below2.0 | 2.0 |
| 1.0,1.0.Final at greatest order | ambiguous maximum | ambiguous maximum |
| 1.0,2.0-SNAPSHOT,2.0-20261112.120000-1 | 1.0 | 1.0 |

These are proposed acceptance examples, not executed Maven/product tests. A label
such as redhat is not itself positive private/fork assignment; actual attributable
contrary evidence still refuses before any public request under S7.

Conservative policy avoids calling an unknown preview stable; its cost is missing
legitimate vendor/calendar/custom releases or unconventional stable syntax. It
may surprise Maven users whose projects rely on those releases; explicit unknown
reasons make that cost explainable. It best preserves libyears' exclusion of
prereleases without claiming impossible universal stability knowledge.

Broad policy improves yield and resembles retained Renovate unknown-qualifier
practice, but is **not** full Renovate compatibility. It may call preview/dev/custom
prereleases stable and select a surprising unknown suffix over a familiar stable
release. That weakens ordinary latest-stable expectations and needs conscious
human acceptance. Source refusal remains independent; this policy grants no
private namesake permission.

Both are deterministic for identical accepted inputs/pinned rules, not immutable
across repository changes. Whitelist/token-rule changes require reviewed policy
versioning; adding a newly unknown candidate can change conservative availability.
The chosen machine policy identifier and documentation must expose the rule.

## Shapes not recommended as additional default choices

“Greatest non-SNAPSHOT” would select2.0-RC1 over1.0, directly conflicting with the
existing prerelease exclusion. Ordering alone does not make that a latest-stable
policy. It would need an explicit changed product claim, so is not a third
recommended alternative.

Request-relative compatibility (for example greatest eligible1.x for a1.x request
when2.x exists) answers a different maintenance question and depends on request /
resolver context this feature does not establish. A prerelease request permitting
newer prereleases would also change the ordinary stable target. No ranges are
resolved. Recommend keeping the global target; no requested-version family filter,
compatibility promise or third upgrade-advice mode is introduced.

## Exact human gate

Choose **conservative known-stable with potentially maximal unknown refusal**, or
**broad conventional non-prerelease including unknown qualifiers**. Each includes
service packs, release aliases, unique-max refusal and the global GA target described
above. The recommendation is conservative. Neither choice is made by the author
or reviewers. If the human wants different service-pack/request-family treatment,
that is a product revision to specify, not a technical ordering question.

After selection: finish the already identified technical source-policy grammar /
budgets, independently review the whole specification, then advance only through
its authorized lifecycle. No plan/tasks or implementation at this decision stop.
