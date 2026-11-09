# Alternate-source public comparator investigation — 006-0031

Status: frozen investigation for independent review, not a selected correction.
**HUMAN PRODUCT / ALTERNATE-SOURCE COMPARATOR DECISION REQUIRED.**
Current P0 remains implemented; no new comparator, parser, registry, schema or
metric behavior is authorized by this document. Reviewed baseline after security:
`e78b22829636181da19d0d6c09a8e486f6d014ff`.

## Claim and consequential choice

A public version-age comparator asks whether nuget.org is the chosen applicable
public release history for a selected dependency identity. It does not establish
acquisition endpoint, content equality, producer history, restore success, deployment
or runtime use. A genuine mirror of the same public identity should normally leave
that public age unchanged. Requiring acquisition proof solely because a mirror
served it would exceed this claim.

But an internal fork or private namesake can share ID and version with a public
package while having an independent history. Public dates can then describe the
wrong dependency history, including a misleading zero when selected equals public
latest. No acquisition proof is intrinsically needed; sufficient comparator
assignment, or deliberate product acceptance of a correspondence assumption, is.
The two propositions are distinct:

- Another source could have supplied the same public identity: acquisition ambiguity.
- Another source could define a different identity/history under the same ID/version:
  comparator ambiguity.

The already approved convention consciously assumes public correspondence for
repository silence/qualified public-only policy. It explicitly refuses observed
unassigned alternate eligibility. Changing that boundary is a new consequential
choice even though both routes use a conditional public reference. The uncertainty
need not make a chosen benchmark inherently dishonest; admitting it requires
intentional product authority and clear claim limitations. Namesake existence
cannot provide that authority and is not investigated here.

## Actual two configurations and scope

Only repository-contained, manifest-bound target evidence was interpreted.

| Fact | MRCalc | OASim |
| --- | --- | --- |
| Relative config | SRTRMatchRunApplication/MRCalc/nuget.config | SRTRMatchRunApplication/OASim/nuget.config |
| packageSources | one add, key AvaloniaCI | identical |
| Endpoint | https://www.myget.org/F/avalonia-ci/api/v2 | identical |
| Form | HTTPS URL, v2-shaped API path; no userinfo/query | identical |
| Explicit nuget.org entry | absent | absent |
| clear / remove | absent / absent | absent / absent |
| Disabled source section | absent | absent |
| Package source mapping | absent | absent |
| Credential/API-key section | absent | absent |
| Visible source-affecting properties/imports/targets/choose | none observed | none observed |

Both config SHA256 values:
`00b6335d5d0642f28d3a62dba52d530c14cc612a53dd8adcdc73ccbeb9c2d516`.
They are byte-identical and therefore semantically equivalent in isolation, but
located in separate project directories. Under the existing project-anchored
root-to-project policy, each governs its own project and any descendants, not the
sibling. No root/intermediate repository config or Directory.Build.props,
Directory.Build.targets, Directory.Packages.props was present in the inventory.
No user/machine/outside-root policy was read. Absence of disabling in this bounded
policy does not prove effective host enablement or default nuget.org presence.

The config comment describes an Avalonia CI feed for unstable packages and suggests
moving the file to the solution root to use it. The retained local position is the
current policy input; an instruction to move it does not disable it. No file moved.
Actual historical solution versus project invocation is not reconstructed.
Microsoft documents invocation-dependent configuration scope; current comparator
policy is expressly project-anchored, not a claim about that restore history.

Classification: **D, UNKNOWN publication-namespace role**, with positive descriptive
context that it is an Avalonia CI/unstable-package feed. Repository evidence does
not identify it as a public mirror/cache/proxy, a distinct private namespace, or a
known mixed feed. HTTPS, MyGet host, alias and Avalonia name prove none of these.
CI/unstable wording does not assert public-timeline equivalence, feed exclusivity,
or package-specific routing. Stable selected versions do not disable this source.
No retained inspected documentation calls it private/internal/public/mirror/cache/
proxy or assigns any of the nine selected identities to its publication history.
The comment is an intended package-family/use hint, not an ID mapping.

## Nine repeated identities

Both projects have nine unconditional literal PackageReferences and sole net10.0
schema1 locks with matching Direct IDs, normalized minimum requests and selections.
They remain separate project occurrences, never deduplicated.

| Identity | Selected version | Project/config/lock/documentation contrary-identity audit |
| --- | --- | --- |
| Avalonia | 0.10.19 | no contrary repository evidence observed |
| Avalonia.Desktop | 0.10.19 | no contrary repository evidence observed |
| Microsoft.Extensions.Configuration.Json | 10.0.14 | no contrary repository evidence observed |
| Serilog | 4.2.0 | no contrary repository evidence observed |
| Serilog.Expressions | 5.0.0 | no contrary repository evidence observed |
| Serilog.Settings.Configuration | 9.0.0 | no contrary repository evidence observed |
| Serilog.Sinks.Console | 6.0.0 | no contrary repository evidence observed |
| Serilog.Sinks.File | 6.0.0 | no contrary repository evidence observed |
| System.Configuration.ConfigurationManager | 10.0.14 | no contrary repository evidence observed |

This means no observed private/fork/republished/aliased/local/independently versioned
or source-mapped package indication in the inspected evidence. It does not mean
proved public. Credits attribute Avalonia and Serilog upstream homepages but do
not establish feed identity or selection authority. Documentation's general Git
fork/internal repository discussions do not describe NuGet packages. Locks retain
requested/resolved/version/hash evidence, not package-source assignment. Known
alternate eligibility remains the same policy ambiguity for all18; an alias hint
cannot restrict it to the two Avalonia IDs or exempt the other seven.

## Authoritative upstream semantics and inference limits

Microsoft's [source mapping documentation](https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping)
says all configured sources are searched by default; packages available from
multiple sources can have nondeterministic acquisition. Mapping filters eligible
sources by ID; exact patterns outrank prefixes, then longest prefix, then wildcard.
A cached package can bypass download mapping. These describe acquisition and
current policy, not proof of a historical supplying endpoint or publication history.
The same documentation distinguishes metadata-query behavior from download mapping;
Libyears retains its own stricter capability-before-metadata boundary.

The [config reference](https://learn.microsoft.com/en-us/nuget/reference/nuget-config-file)
uses aliases and URLs/paths, section-local collection operations and separate
disabling. Source order is ignored for PackageReference restore; the one alternate
entry does not assign priority or uniquely bind IDs. The
[hierarchy reference](https://learn.microsoft.com/en-us/nuget/consume-packages/configuring-nuget-behavior)
describes accumulation and invocation scope. No effective external settings are
inferred. Existing approved limitations about injected defaults remain unchanged.

[Package versioning](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning)
refers to a package using ID and exact version; this does not encode the acquisition
source or authenticate cross-feed correspondence. The
[PackageReference lock contract](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files#locking-dependencies)
and actual retained locks do not establish per-package feed origin. The
[restore property reference](https://learn.microsoft.com/en-us/nuget/reference/msbuild-targets#restore-properties)
shows source/config overrides; unknown explicit relevant influences continue to
refuse without evaluation. No resolver or target code was executed.

Inference: NuGet mechanics permit both genuine mirrored public packages and
independent same-ID/version packages. They cannot choose Libyears' comparator-risk
policy. A documented pure mirror role can support a future accepted identity
assertion, but service type alone cannot rule out private overlays/forks. No
upstream source supplies authorization to ignore the current ambiguity veto.

## Candidate policy comparison

| Candidate | Truthfulness / risk | Usability, inspectability, burden and parity |
| --- | --- | --- |
| P0 current strict eligibility | Disclosed public assumption on silence/public-only; alternate eligibility refuses. Protects against observable competing-history possibilities, without proving effective host closure. | Small current rule; genuine unassigned mirrors also blocked. Existing OASim33/51 retained; package evidence burden for18. |
| P1 positive contrary evidence only | A conditional public benchmark can remain meaningful through mirrors. Unknown private namesakes/forks can receive another history's dates and IDs can be sent publicly. No observed contrary assignment does not establish correspondence. | Lower ordinary burden; inspectable supported-policy guard possible. Requires new acceptance of ignoring observed competing eligibility. More like Python/npm attribution floor, not mandated by them. Potential51/51 depends on new authority and metadata, never promised. |
| P2 mirror-only exception | Require positively accepted repository evidence that relevant identity is ordinary public with public history, not just a mirror-service label. Mixed overlays cannot silently qualify. | Can admit genuine mirrors but OASim CI comment does not meet this floor. New evidence format/acceptance semantics needed unless existing exact testimony used. |
| P3 package-specific evidence | Existing valid exact public testimony or closed unique canonical-public mapping resolves eligibility, subject to conflicts/whole validation. No acquisition proof required. | Strong inspectability; higher maintainer burden. Already authorized mechanisms, no target policy/testimony is fabricated or written here. Does not promise current18. |
| P4 explicit comparator opt-in | Deliberately select public benchmark separately from feed mechanics, with exact scope and conflict precedence. | Existing accepted testimony already offers an exact route. A broader automatic comparator declaration would need separately approved trust/schema and precedence; not implemented or necessary now. |

P1 must define open-private-only additions, local sources, pure-HTTPS alternatives,
explicit public exclusion and mixed mappings; the slogan alone does not define a
safe implementation. A narrow future option could change only supported unassigned
HTTPS eligibility, retaining local/unknown/exclusion refusals, all mapping/testimony
precedence and current A/B1 admission. That is a proposed human choice, not a
silently selected P1 variant. Comparing public history instead of acquisition
endpoint is already approved; ignoring the observable possibility of another
history is not automatically entailed.

## Adversarial cases

Y = authority may permit query after qualified selection and whole supported
policy; R = no query. P1 below means a hypothetical decision to ignore alternate
eligibility, never to ignore positive assignment, unknown syntax or exclusions.
P2 extends current convention only for accepted pure-public-mirror evidence;
P3 column concerns existing exact mapping/testimony, not removal of P0 silence.

| Case | P0 today | P1 hypothetical / issue | P2 / P3 resolution |
| --- | --- | --- | --- |
| 1 nuget.org + genuine public mirror, no map | R | Y, same public history sensible if identity corresponds | P2 only accepted mirror identity; P3 exact public authority |
| 2 nuget.org + private feed, no map | R | Y absent identity assignment; competing private history risk | P2 R unless relevant identity supported; P3 exact public authority |
| 3 private-only feed | Open additions R ambiguous; closed exclusion R nonpublic | Open additions unresolved P1 design; closed exclusion R | No mirror inference; P3 cannot override exclusion |
| 4 private package with public same ID | R in mixed-source setting | Y if private fact unobserved; wrong-history risk | Positive private evidence R under every candidate |
| 5 public package through private cache | R absent resolving evidence | Y, acquisition endpoint alone should not change age | Accepted mirror identity or exact public testimony can resolve |
| 6 internal fork, same ID/version | R in mixed-source setting | Y if fork unobserved; dates/zero may mislead | Positive fork/conflict evidence R, exact responsible evidence needed |
| 7 unique private mapping | R | R | R; never public fallback |
| 8 unique public mapping | Y repository_mapping | Y | Y, current supported closed mapping requirements |
| 9 conflicting winning mappings | R | R | R; no weaker convention |
| 10 exact accepted public testimony | Y even eligibility-only ambiguity | Y | Y subject to conflicts/whole validation |
| 11 exact accepted private testimony | R | R | R |
| 12 no repository source config | Y convention, external uncertainty disclosed | Y | P0 silence retained; exact authority optional |
| 13 alternate disabled, public remains | Y with supported resolved disabling | Y | Y under current convention |
| 14 enabled local source | R ambiguous | New choice: exclude or accept competing local history | R absent exact authority; no filesystem feed access |
| 15 unsupported source-affecting project property | R unknown | R | R, no evaluation or fallback |
| 16 public namesake plus positive private evidence | R | R | R; existence never authority |
| 17 no contrary package evidence, alternate eligible | R ambiguous | Y by newly accepted assumption only | P2 needs mirror evidence; P3 exact authority |
| 18 same ID in public-policy/private-policy projects | Y / R separately | Y / R for positive assignments; mixed unknown branch changes only if selected | Never transfer sibling authority |

Cases4/6 with entirely absent repository policy already expose the current
convention's acknowledged residual assumption. This does not erase the explicit
boundary when a competing eligible source is observed. Failure-to-lookup outcomes
cannot validate an unauthorized namesake probe. No public request is permitted for
a case remaining private, conflicting or unknown under the chosen rule.
This is misattribution/disclosure risk; no actual install/execute dependency-confusion
attack occurred or is claimed. No target package code or archive was fetched.

## Narrow sibling check

Python requirements use exact pins plus optional snapshot, fixed PyPI metadata;
URL/VCS/local requirements refuse, but index directives do not establish positive
namespace for adjacent exact pins. npm production lock evidence uses fixed npm
metadata; resolved URL/integrity is not its source-authority gate. Yarn retains
version while resolved/integrity do not select namespace. These routes generally
do not change comparator merely because acquisition uses a proxy, but retain
private-attribution gaps. Ruby requires every relevant same-name lock source to
be a supported singleton public RubyGems remote; private/GIT/PATH/multiple remotes
or explicit pins refuse. An unrelated private Ruby source need not poison a
public package with independent supported source association.

Thus public publication history and acquisition endpoint are separable across
ecosystems, but released source-authority floors differ. Ruby retains positive
per-package source structure unavailable in NuGet locks. Existing Python/npm gaps
are already recorded as separate roadmap work, not evidence to weaken NuGet.
No sibling behavior changes. Code inspected: requirements.py, npm.py, yarn.py,
rubygems.py and their relevant tests, plus NuGet comparator/source/registry.

## Authority disposition and recommendation

Approved [C1–C3](../maintenance/nuget-conventional-comparator/spec.md) explicitly
requires absence of unresolved ambiguity and treats enabled noncanonical/local
sources without assignment as ambiguous. C3 lets accepted exact public testimony
resolve mere eligibility, never known exclusion/assignment/unsupported policy.
The [approval](nuget-conventional-comparator-review.md) calls refusal of alternate
eligibility an essential qualification. Current implementation and negative controls
conform; this is not an implementation bug or excess acquisition prerequisite.

Retain P0 and existing P3 routes now. A human may deliberately choose a bounded P1
public benchmark, accepting that an unobserved independent same-ID/version identity
can be dated against public history despite observed alternate eligibility. That
choice changes which identities may be publicly queried and counted as measured;
it is consequential comparator/trust authority, beyond prior acquisition separation.
No reviewer can grant it. P2 also lacks an automatic approved evidence rule and
these configs do not establish a pure mirror. No implementation proceeds.

Smallest human choice: **retain alternate-eligibility refusal, or explicitly accept
conventional public comparison for supported unassigned alternate HTTPS eligibility
when no positive contrary/unsupported policy exists**, with private/fork namesake
residual risk and public identifier disclosure consciously accepted. If selected,
prospective spec/review must resolve private-only, local and conflict boundaries
before plan/tasks/implementation; no metric/date loosening or namesake permission.
Existing package-specific testimony/mapping remains an alternative without this
policy change; no target edits or fabricated testimony are made here.

## Verification, frozen evidence and actual product result

Before first target interpretation: exact HEAD/full NUL status/index plus223 tracked
and12 nonignored untracked file bytes/modes/size/mtime,50 ignored names,zero relevant
ignored inputs. Before manifest SHA256:
`58569f6fc3a885b90ffd3a1d8937f71721f4d918affe44a412cf018529aac731`.
No cleanup/normalization; target is unchanged only when exact after equality passes,
not claimed clean or atomic OS-wide invariant. Unrelated ignored bytes unexamined.
Parent and D independently checked current project/config/lock evidence.

Current offline production source staging, with socket/process/HTTP entry points
denied: N51,33 conventional_public_policy capabilities,18 exact ambiguity refusals,
zero source errors; no network/process attempts. It creates no dates or new metrics.
Initial reporting probe used a wrong dataclass attribute; corrected projection
succeeded without any target or product modification.
Focused comparator/source/registry/repository/Python/npm/Yarn/Ruby tests:165 run,
OK with1 genuine case-alias filesystem skip. No runtime changes warrant a full
suite/capability-disabled/real-worker rerun; those implementation-only obligations
are not falsely claimed. Parent source audit confirms only already authorized
capabilities can reach the fixed public registry adapter; no feed was contacted.

Latest real ordinary result remains the frozen006-0030 measurement, not rerun here:
33/51,64.70588235294118% coverage; total26.550874794502747,
mean0.8045719634697803,median0.8462138558382133,max1.897372996584024 libyears.
All33 conventional_public_policy; explicit_testimony0/repository_mapping0.
All33 authorized public results succeeded, final registry failures0 in that run.
The measured-subset total is incomplete as a repository debt total. Each of the
nine identities above remains blocked once in each project (18 total), exclusively
nuget_comparator_ambiguous, not a registry failure. No51/51 claim or new live ages.

Security continuation e78b228 passes committed full319-commit GitLeaks with zero
unsuppressed; two approved prose occurrences plus the older two exact exceptions
remain exact, new controls detected. No broad config/rule/history changes. Final
investigation GitLeaks/whitespace/integrity/freeze review results belong in the
companion review. Phase2 review verdicts must complete before discovery closure.
006-0030 is recorded exactly once;006-0031 continues in the same context after
explicit security authorization, current run not appended. Runtime and current
after-credit observation remain unobserved; original counter continuity retained.
No push. Stronger assurance, parser expansion, CI maintenance, suite profiling and
retrospective framework remain separate roadmap opportunities; none implemented.
