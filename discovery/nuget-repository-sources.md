# Repository-level NuGet project sources — 006-0021

## Disposition and authority

**Discovery complete; HUMAN PRODUCT DECISION REQUIRED before specification.**
Baseline: published `cce5e6a5863242fa9d0e8e1b9af486fd221f3138`, clean checkout.
The human commissions a fresh, read-only OASim investigation and conditionally
authorizes autonomous SDD only if independent project-source measurement already
fits existing population, evidence, metric and schema semantics. That condition
is not established. This is a distinct subsequent investigation, not a rewrite
of Feature 006 or the completed 006-0020 recognition correction, and not Feature007.
Independent audit and parent disposition are recorded in
[the review record](nuget-repository-sources-review.md).

The supplied complete hosted evidence for 006-0020 is reconciled separately in
[operational closure](../maintenance/nuget-root-recognition/operational-closure.md).
That successful contract remains intact. A satisfactory ordinary user journey
does not follow merely from contract convergence: repeated real use now exposes
a separate selection burden. No process expansion is needed to preserve this fact.

## Current semantics and candidate population

The candidate abstraction is useful: a project can be a dependency source rather
than a user selection decision. However, arithmetic accepting rows does not by
itself authorize what those rows count.

| Concept | Existing meaning / proposed distinction |
|---|---|
| Dependency identity | Ecosystem plus normalized package identity; Feature006 S6 explicitly uses ecosystem plus case-insensitive NuGet ID |
| Dependency source | One concrete declaration population with its own evidence acceptance and availability; a lock and witness supplement that population, not extra dependencies |
| Dependency occurrence | Proposed package membership within a particular project; distinguish by ecosystem, root-relative project identity and normalized ID |
| Measurement row | One successful eligible dependency with used/latest timestamps; proposed occurrences would each retain their own selected version |
| Repository denominator | Current sum of established source populations, null if any activated population is unknown; it is not a count of raw syntax nodes |

Current mixed scans have one PyPI population, one root npm population and one
Ruby population, plus at most one explicitly selected NuGet population.
[Feature002 §18](../specs/002-npm-support/spec.md) sums ecosystems; it does not
establish repeated same-ecosystem project membership. Same-name PyPI/npm/Ruby/NuGet
packages are independent ecosystem identities, not evidence for five occurrences
of one NuGet identity. Python identical exact declarations collapse to one;
conflicting pins become one unmeasurable identity (`requirements.py` and
`test_duplicate_same_exact_version_is_one_dependency`). npm package-lock and
Yarn evidence arbitrate for one root population, never add parallel populations.
Ruby platform artifacts and selected group unions similarly do not multiply
one dependency. NuGet duplicates within a project reject the source.

[SPEC §6](../SPEC.md) also prefers authoritative evidence for the same normalized
name and treats equally authoritative conflicting versions as unmeasurable.
Those are evidence arbitration rules, not a decisive oracle for separate project
contexts. They neither authorize repository deduplication nor establish occurrence
weighting. There is no released multi-project same-ecosystem precedent here.

**Recommendation:** explicitly approve source-qualified direct occurrences for
the new mode. Package X in five independently admitted projects would contribute
five occurrences, even at the same version. Different versions remain independent;
there is no invented repository-level used version. Such totals/means weight
repeated project membership; they answer a different population question from
unique-package inventory. This is defensible but requires human acceptance,
not an inference from the existing summation code. No deduplication is performed.

## Real target observations and integrity

Before target inspection, an external trusted helper captured revision, exact
NUL-delimited Git status with all untracked names and ignored state, tracked
bytes/modes, all nonignored untracked bytes/modes, ignored names and relevant
ignored project/lock/provenance evidence. Git optional locks were disabled.
Baseline: **223 tracked files, 12 nonignored untracked files, 50 ignored file
names**, revision `1e937015e1d242fee5597ea0fbdc4cd5c983f101`. No pristine-state
precondition was imposed. Untracked and ignored state predated this run.

Static inspection corroborates **10 projects, 51 literal PackageReference
occurrences, 24 case-folded package IDs, 15 ProjectReference edges, net10.0
throughout, and 10 retained locks**. The retained MatchRunProfileUpdater witness
is present; neither presence nor prior validation authorizes implicit acceptance.
No producer/native/cache/configuration/credential content is inspected.

The existing complete-project parser accepts only **2 projects / 3 references**:
MatchRunProfileUpdater (1) and MatchRunProfiling (2). The other **8 projects reject
as unsupported**, with unknown supported populations. Their project XML includes
constructs outside the approved conservative table, such as Version, IsPackable,
StartupObject, CopyLocalLockFileAssemblies, and additional resource items.
These examples do not prove all such constructs inert or identify every rejection
influence; no allowlist extension or partial salvage is attempted.

Calling the current reader separately for each already captured project name,
without a witness option, gives **8 unsupported_nuget_project source failures and
2 nuget_provenance_missing source failures**. This is a discovery probe, not a
repository metric or new CLI. The three accepted declarations retain known N but
null measurement/coverage. The other populations remain unknown; **51 is a raw
research inventory, not an admissible repository denominator**. Automatic discovery
alone would not make `N/51` truthful under current acceptance rules.

The exact ordinary command `python3 -m libyears OASIM_ROOT` was run from the trusted
scanner checkout. Exit **0**, stderr **empty**. It reports ten sorted bounded
filename candidates, depth/exclusions, **no NuGet measurement**, explicit project
selection guidance, and:

```text
Ecosystems scanned for measurement: none
Repository: null coverage; 0 / 0 measured; total 0.00, mean null, median null, max null libyears
```

This reproduces the current published behavior, not the proposed automatic mode.
Raw exact argv/stdout/stderr and manifests are retained privately under
`/tmp/libyears-observations/006-0021`. Initial inspection-helper use of the parser's
bytes interface failed before completing its probe; corrected use of LocalInput
then completed. This was harness misuse, not a product failure.

Final capture equals baseline exactly for revision, tracked bytes/modes/metadata,
all nonignored untracked bytes/modes/metadata, full status and ignored inventory.
There were no relevant ignored project/evidence files. Other ignored bytes were
not hashed; equality is established for the captured state, not an atomic or
OS-wide forensic snapshot. No target modifications, target application execution,
restore/build/test or generated evidence occurred. Target is **unchanged from
baseline**, not claimed clean.

## Project types, references and evidence

Feature006 S2 already includes every supported explicit PackageReference within
its selected project, including tests/tools/analyzers/PrivateAssets. It excludes
ProjectReference, FrameworkReference and implicit packages. Preserve this policy
for any approved independent source model: do not filter projects merely by
test/benchmark/CLI names. Discovery does not license unsupported project contents.
The 15 graph edges add **zero external dependency rows** and never merge or
recursively expand populations. Solutions establish no population authority.

H3 requires native actual-origin/hash provenance plus contemporaneous producer
attestation bound to exact project/lock bytes and context. Local/public hash
agreement still precedes dates. Ten locks do not supply provenance, and a public
namesake supplies no authority. Feature006 S1 explicitly treats
`--nuget-provenance NAME.json` as the user's acceptance of supplier assertions;
a conventionally found witness is never trusted. Therefore automatic project
enumeration can safely attempt sources with **no accepted witness**, but cannot
automatically use the retained witness just because it exists.

Two coherent choices remain: retain explicit witness acceptance through an
eventual project-to-witness mapping (separate from project selection), or accept
a new convention/authority for implicit testimony. Recommend the former; the
latter changes the trust boundary and is not authorized. No mapping format is
invented during discovery. Explicit single-project/provenance options remain
the current precise interface.

Partial coverage already works **after whole required sources are accepted**:
individual package failures yield M/N, including 0%. It does **not** turn missing
lock/witness sources into N invented unmeasurable rows. Feature006 S6/AC26–28
explicitly preserves known N, null measured/coverage/numerics and source_errors.
Unknown membership clears N. Keeping H3 intact does not itself settle whether a
new mode should change availability semantics. Recommend retaining the existing
null distinction; a numeric all-occurrence fraction including unavailable
sources needs a separate product decision and must not silently replace coverage.

## Output, arithmetic, composition and bounds

Internal NuGetEvidence already retains project/framework/requested per row, but
project is an immediate filename, insufficient for `a/App.csproj` versus
`b/App.csproj`. Minimum new identity is a safe root-relative project path, shared
by successful rows, dependency failures and source failures. Human output needs
that source identity plus per-project known/unknown population and availability;
all filenames must remain escaped and private diagnostics omitted.

Schema v3 has singleton `version_evidence.nuget` fields for one selected project,
framework and witness; source_errors has only ecosystem/source/reason.
`output._report_parts` overwrites evidence for repeated ecosystem keys;
`scan_mixed_repository` similarly overwrites per-ecosystem summaries and can pair
all NuGet rows with only one project's denominator. Neither is a valid
multi-project implementation. Per-row project alone cannot describe failed or
empty projects and cannot repair lost source evidence. Human/internal identity
alone leaves JSON ambiguous. An additive v3 source collection/row source ID
appears feasible in principle, preserving legacy explicit output, but requires
an explicit multi-source evidence contract; changing singleton values to arrays,
changing their existing meanings, or selecting a representative project is not
compatible by assumption. No schema bump is proven necessary, and none is made.

`metric.calculate_summary` already calculates measured count, total, mean,
median and maximum from all admitted rows, with coverage M/N for known nonzero N.
There is no arithmetic need to deduplicate. Under approved occurrence weighting,
the same arithmetic can operate unchanged; what admits and counts rows must first
be decided. Zero accepted measurements yield total 0.0 and null mean/median/max;
validated empty has 0/0 and null coverage; unavailable NuGet source numerics are
null. Partial projects with accepted evidence contribute successes; unknown
population makes repository N/coverage null. Unavailable sources keep coverage
null; measured is null only if all detected sources are unavailable. Available
sibling rows and numerical aggregates survive. Project-level summaries would be
new output, not existing released machinery.

Automatic NuGet must compose with existing root PyPI/npm/Ruby sources without
activating recursive sibling ecosystem discovery. Cross-ecosystem equal names
remain distinct. A rejected NuGet source must not erase sibling evidence/rows.
Per-source failures must also isolate successful NuGet projects. Multiple workers
must not silently multiply/reset existing scan-wide security budgets; that is a
later bounded architectural obligation, not reason for a generic analyzer refactor.

The corrected 006-0020 search is a useful candidate bound: depth0–4 inclusive,
named/hidden exclusions, no links/reparse traversal, caps256 directories/10,000
entries/100 candidates. Depth5 is intentional exclusion, **not** incompleteness.
The bounded count never claims exhaustive repository inventory. Overflow, errors
or incomplete traversal cannot yield a complete denominator; capability refusal
must remain explicit and fail closed. Missing/malformed/unsupported projects have
unknown populations; accepted declarations plus missing locks/witnesses retain N
but unavailable measurement. Mixed eligibility preserves safe sibling facts.
One or many projects should use the same approved source model; a sole candidate
does not acquire evidence authority by being alone.

## Alternatives and next human decision

| Model | Expectation and metric | Evidence/coverage/output | Complexity and isolation |
|---|---|---|---|
| A: explicit single project | Precise existing population; repeated selection remains burdensome | Established H3 acceptance, nullable source coverage, unambiguous v3 | Smallest existing implementation; sibling ecosystems preserved |
| B: independent project occurrences | Best fit for ordinary repository request; repeats weight membership | Needs explicit population/source contract; H3 unchanged; unavailable coverage remains null unless separately changed | Bounded per-source composition and attribution; isolate failures |
| C: unique package deduplication | Answers inventory question; different versions need a new choice | No authority for choosing one used version or discarding contexts | More policy and ambiguity; not recommended |
| D: solution population | May match a chosen build view, not all repository projects | New solution authority, absent/multiple solution policies and completeness | More parser/selection policy; not recommended |
| E: independent project reports only | Avoids cross-project weighting; removes manual enumeration | Each report keeps current acceptance/coverage; still needs safe identity and explicit witness mapping | Smaller compatibility bridge, but no single repository NuGet metric |

Recommend **B**, conditional on explicit human acceptance of source-qualified
occurrence weighting and a multi-source public evidence contract. Preserve all
project classes already covered by S2, no graph aggregation/deduplication,
unchanged H3, explicit witness acceptance, existing null availability, existing
metric arithmetic and explicit selection compatibility. E is the concrete
fallback if repository weighting is unwanted; A remains implemented meanwhile.

**Exact next gate:** human decision whether repeated same-ecosystem membership
becomes independent repository dependency occurrences in the new mode, with
the recommended existing unavailable-source semantics and explicit witness
acceptance. If selected, authorize specification of a compatible source-qualified
output contract (evaluate additive v3 before considering a version change).
Requiring numeric all-project coverage despite unavailable evidence, implicit
witness acceptance, or a schema-version change remains a separate human choice.
No specification, plan, tasks or implementation is approved by this recommendation.
