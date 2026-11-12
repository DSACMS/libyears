# Maven bounded repository evidence — Feature 007

This is the normative local discovery, parser and source-policy subset for
[spec.md](spec.md). It completes the technical grammar under human H1=NO and the
selected conservative eligibility/time policies. It is not an evaluated settings,
effective-model or Resolver implementation. Approval lives in [reviews.md](reviews.md).
The policy result authorizes only a conventional Central comparison; it establishes
no acquired bytes, actual repository choice or producer/runtime history.

## B1 — Discovery and safe local inputs

Maven activates for ordinary **directory** input only, through regular files named
exactly `pom.xml`. A direct POM-file argument does not activate Maven. Walk the chosen
root in deterministic relative-name order, depth0 through4 inclusive, with at most
256 visited directories,10,000 directory entries inspected and100 candidate POMs.
Do not descend into names beginning with `.`, or exact basenames `bin`, `obj`,
`node_modules`, `packages`, `vendor`, `venv`, `__pycache__`, `target` or `build`.
The exact `.mvn` sentinels below are separate bounded policy reads, not source
traversal. A depth/exclusion boundary defines this supported discovery projection;
it is not a claim about sources elsewhere in a repository. A supported module or
parent edge crossing that boundary cannot silently establish association/completeness.

No directory or file symlink, junction/reparse point, device, FIFO, socket, ancestor
link or special file is followed. Bind the root and every accessed relative component
with safe no-follow, race-resistant identity checks; a mere realpath-prefix check
is insufficient. Required safety primitives/capabilities unavailable on a platform
mean the affected source is unavailable, never a permissive fallback. Do not open
outside the selected root, search ancestors beyond it, or interpret file repository
contents. Directory-limit exhaustion/read failure leaves discovered safe siblings
usable, but discovery completion and repository Maven N/coverage unknown. Never
present a capped prefix as the complete in-scope source set.
Complete discovery with no candidates omits Maven entirely. Incomplete discovery,
even before a candidate was seen, establishes neither absence nor an empty Maven
population: report a discovery failure and unknown presence/population, preserving
safe sources already observed. It is not a claim that Maven was positively found.

Only discovered POM candidates can supply local-parent/module model bytes. A parent
relativePath may normalize `..` only while safely contained and targeting a discovered
candidate; no extra source scan/read follows it. Empty relativePath/external parent
or an undiscovered/missing/mismatched parent leaves dependent inherited facts and
complete population unavailable under S3. Modules require unconditional literal
contained directory paths with a discovered immediate pom.xml; they add association,
never permission to traverse beyond discovery. Cycles, self edges, duplicate GAVs,
multiple incompatible aggregation roots and ambiguous targets refuse association.
No POM, source, module or occurrence is deduplicated through artifact aliases.

## B2 — Finite model and parsing grammar

| Boundary | Maximum / behavior |
| --- | --- |
| Any local XML document | 1MiB raw bytes; depth32;50,000 elements;32 attributes/element;16KiB scalar text/attribute; reject overage before accepting its framing |
| Total distinct local XML read in one scan | 32MiB; shared parent/settings bytes count once, stable identity checked |
| Parent chain | 16 distinct discovered POMs including consumer; cycle or overage leaves dependent model unavailable |
| Direct occurrence records | 10,000 per POM and10,000 across expanded source models; exceeding a source/scan bound makes affected population unknown, never a fabricated complete prefix |
| Properties | 4,096 entries/POM; property key128ASCII characters under S3's grammar; duplicate keys refuse affected attribution |
| Property expansion | 16 recursive substitution levels,1,024 substitutions/fact and64KiB final expansion; cycles/overage refuse dependent fact |
| Profiles / modules | 128 profiles and100 literal modules/POM; duplicate profile IDs or malformed relevant containers leave dependent facts/policy unknown |
| Relevant policy records | 1,024 repository/profile/filter records per source context including its local chain;64 mirrors and128 profiles/selected settings file |
| Configuration text | 64KiB/file;1,024 lines/arguments;2,048 characters/argument; at most one selected local settings file/context |
| Safe relative paths | 1,024 characters and32 components; no NUL/control character, URI, drive/UNC root, absolute path or host expansion |

Accept UTF-8 XML (optional UTF-8 BOM/declaration), root `project` in either no
namespace or `http://maven.apache.org/POM/4.0.0`, and literal modelVersion4.0.0.
Namespaced documents must use that same namespace for interpreted model elements;
foreign-namespace elements at relevant positions do not masquerade as Maven fields.
No DTD, entity declaration/reference beyond predefined XML escapes, XInclude,
external schema, network entity or transformation is processed. Reject DTD/entity
framing, malformed XML, duplicate scalar relevant elements, mixed scalar markup,
unsupported relevant namespace/attributes and over-budget framing. A schemaLocation
attribute is inert text, never a fetch instruction. Ordinary XML comments and
processing instructions carry no evidence. Duplicate dependency model keys retain
S2's ambiguity rule. Uninterpreted plugin/reporting/descriptive subtrees still count
toward framing budgets but never become dependency population or source authority.
Relevant unknown model constructs refuse at the smallest dependent scope; an unknown
name is not automatically ignored if it could change population/identity/policy.

Literal safe public identities are narrower than arbitrary Maven strings:

- groupId:1–128ASCII characters, dot-separated nonempty segments matching
  `[A-Za-z0-9_][A-Za-z0-9_-]*`;
- artifactId, type and classifier atoms:1–128ASCII characters matching
  `[A-Za-z0-9_][A-Za-z0-9_.-]*`, never a `.` or `..` path segment;
- exact version:1–256ASCII characters matching `[A-Za-z0-9][A-Za-z0-9._+-]*`;
  no slash/backslash, percent escape, colon, whitespace/control, property expression,
  range syntax or standalone dynamic LATEST/RELEASE selector. S4's hard singleton
  unwrapping precedes this exact-version check and preserves the original request.

Do not URL-decode or normalize these identities into another spelling. The network
boundary percent-encodes each safe path component, including `+`, after admission.
Request text may be retained only within scalar/output-safety bounds; unsupported
version syntax leaves independently safe known population intact. Explicit empty
classifier remains unsupported. The finite built-in type/handler mapping in S2 is
independent from safe lexical syntax; a safe custom type is still unsupported.

## B3 — Repository declarations and parent/profile effects

Inspect only ordinary `project/repositories/repository` entries and their equivalent
profile locations in the consumer plus accepted local-parent chain. A POM dependency
exclusion controls transitive selection, not Central eligibility; it creates no
package-source mapping. `pluginRepositories`, `distributionManagement` deployment
repositories, SCM, organization and project URLs do not assign project dependencies.
Never read an alternate/file repository or dependency POM to complete local policy.

A supported repository record has exactly one safe literal case-sensitive ID
(1–128ASCII `[A-Za-z0-9_.-]+`), scalar URL (max2,048), optional `layout=default`,
optional releases/snapshots policy and inert name. Policy enabled accepts literal
true/false only; omitted releases enabled defaults true. updatePolicy/checksumPolicy
are bounded inert acquisition policy, not namespace ownership or a time basis.
Dynamic layout, duplicate/missing/unsafe ID or relevant unknown fields are unknown
policy if they could override/exclude Central. A URL or activation uncertainty
confined to a known non-central unassigned alternate is merely eligibility; it
**does not veto** conventional comparison. No URL interpolation or endpoint request
is necessary to reach that result.

In the supported unconditional local chain, select the **nearest child whole record
by exact repository ID**; do not field-merge repository entries like dependencies.
Same-level duplicate IDs are ambiguous at their relevant scope. This follows pinned
[MavenModelMerger3.9.11](https://raw.githubusercontent.com/apache/maven/maven-3.9.11/maven-model-builder/src/main/java/org/apache/maven/model/merge/MavenModelMerger.java)
repository-list dominance. A missing external parent is missing stronger model
assurance, not automatic contrary source testimony; unknown complete population
remains separate, and safely attributed local rows can use the convention after
all available applicable local checks.

The conventional default has ID `central`, default layout, releases enabled and
public Central identity. Recognize public Central identity only for literal HTTPS
URLs with host `repo.maven.apache.org` or `repo1.maven.org`, no userinfo/query/fragment,
port absent or443, and exact `/maven2` or `/maven2/` path. Host matching is
case-insensitive; repository IDs remain case-sensitive. Recognition neither changes
the fixed lookup destination nor authorizes redirects/other hosts. HTTP URLs,
lookalike hosts, extra paths or credentials do not establish public Central identity.

An effective `central` record with releases disabled, nondefault layout, unsupported
or parameterized URL, or another location is explicit exclusion/redefinition or
unknown relevant Central policy: refuse affected comparison before HTTP. A different
known ID pointing to any public/private/file/parameterized alternate remains
eligibility only; even releases disabled there does not disable default Central.
Source order and alternate-only allowlists establish no package origin.

No profile activation is evaluated, including activeByDefault, JDK/OS/property/file
conditions or machine/CLI choices. Inspect every relevant local/ancestor profile as
potentially applicable: if it could replace/block Central or alter identity, its
comparison is unavailable unless all supported possibilities preserve the same
safe Central conclusion. Profile additions with known non-central IDs only remain
non-vetoing. Profiles affecting population/request facts independently follow S3;
a policy-only unknown must not erase an already known occurrence count. A known
unconditional child override may suppress an unconditional parent record, but
unknown profile order/interaction is never “repaired” by choosing a convenient one.

## B4 — Repository-contained launch/settings evidence

Do not inspect user/global/machine configuration, environment, caches, wrapper
scripts, CI scripts or arbitrary settings candidates. A co-located `settings.xml`
is not evidence of selection and is not opened. No home/installation path is read.
Only exact `.mvn` sentinel names in safely contained source ancestors up to the scan
root are checked; no `.mvn` directory enumeration or outside-root lookup occurs.

The one initially accepted settings-selection form is the scan-root
`.mvn/maven.config` for the disclosed ordinary root-launch context, parsed under the
Maven3.9.11 one-argument-per-line convention. Blank lines and lines beginning `#`
are ignored; no shell quoting, substitution, continuation, glob or response-file
syntax. Support exactly one `-s` or `--settings` followed by its own next-line path,
or `--settings=PATH`. The path is literal root-relative, contains no `..`, absolute /
drive / UNC / URI / property syntax, and safely resolves to one regular contained
XML file. This proves selection in that **retained local configuration**, not that
any real build used it. A second selector, nested competing `.mvn/maven.config`,
external/missing settings target or unsupported selector leaves relevant policy
unknown without following the path. Settings applicability never derives from a
basename, adjacent file, Git status or a successful namesake lookup. A nested
configuration containing only the same recognized inert arguments adds no source
conflict; a nested selector/unsupported context remains unavailable rather than
being guessed relative to the root.

Recognize and ignore only harmless formatting/diagnostic arguments `-B`,
`--batch-mode`, `-V`, `--show-version`, `-q`, `--quiet`, `-X`, `--debug`, `-e`,
`--errors`, `-ntp`, `--no-transfer-progress`, `-U` and `--update-snapshots`.
A literal `-DKEY[=VALUE]` is examined only for KEY matching
`[A-Za-z][A-Za-z0-9_.-]*`,1–128ASCII characters; do not
interpolate, expose or use VALUE. Known local-cache selection `maven.repo.local`
is acquisition eligibility only, never a Central veto, and its path is not followed.
The exact relevant key set is `maven.repo.central`, `maven.settings`,
`maven.user.settings`, `maven.global.settings`, `maven.ext.class.path`,
`maven.multiModuleProjectDirectory`, `user.home`, `maven.home`, and keys beginning
`aether.remoteRepositoryFilter.` or `maven.resolver.remoteRepositoryFilter.`.
These keys have unsupported potentially relevant policy and refuse dependent comparison, without pretending to know a newer
Resolver's filter semantics. Other explicit source-selection mechanisms appearing
at relevant model positions remain unsupported under B2. Other property keys supply
no accepted override in this static basis;
if referenced by a potentially Central-changing local field, that field is already
unknown under B3 rather than interpolated to a convenient value. Unreferenced
version, output or transport-tuning assignments do not themselves veto the narrower
Central convention. S3 already considers all possible relevant profile writes, and
no host value is read.
Support literal `-P`/`--activate-profiles` plus one next-line profile list
(comma-separated `[+!-]?[A-Za-z0-9_.-]+` tokens, at most128 tokens, no spaces)
only as a reason to retain those same possible profiles, not as activation evidence.
Plain goal tokens matching `[A-Za-z0-9_.:-]+` are inert text and never executed.
Other flags, global settings selectors, alternate POM selectors and ambiguous
tokenization are unsupported launch context: keep static population/facts but
withhold dependent comparator. This small parser is not a CLI implementation.
A supported `-o`/`--offline` is explicit repository-contained remote exclusion and
refuses HTTP.

A present `.mvn/jvm.config` is not executed. Empty/whitespace content and literal
memory-only `-Xms`/`-Xmx` decimal-size tokens with optional K/M/G suffix are harmless.
The same applies to `-XX:MaxMetaspaceSize=SIZE`, `-XX:MetaspaceSize=SIZE`,
`-XX:ReservedCodeCacheSize=SIZE` and `-XX:MaxDirectMemorySize=SIZE` with the same
SIZE grammar. Unknown switch names do not acquire harmless status by starting `-XX`.
Use the same bounded literal `-D` key classification above, with no value evaluation.
Unknown JVM switches, agents, classpath/extension loading, quoted/dynamic tokenization
or source-relevant properties withhold dependent comparison. Never interpret those
bytes as JVM/environment state. Presence of a nonempty
`.mvn/extensions.xml`, an entry under `build/extensions`, or plugin
`extensions=true` (including an unknown/dynamic extensions flag) indicates
unsupported possible repository/identity behavior: refuse dependent comparison
without loading code; standard static population may survive as S3's projection.
An explicitly empty `extensions` root in no namespace or
`http://maven.apache.org/EXTENSIONS/1.0.0` or
`http://maven.apache.org/EXTENSIONS/1.1.0`, under B2 structural framing, is harmless;
unknown root/namespace/content is unsupported. Do not apply the POM root rule to
this sentinel. A present root/nested
`.mvn/settings.xml` without the unique supported selector is a recognized alternative
configuration route, not silently trusted or opened: dependent policy is unknown.
These sentinels are checked only within the bounded root; unseen machine extensions
remain a disclosed limitation, not a reason to search or invent their effects.

Selected settings accepts root `settings`, no namespace or the exact Maven
namespaces `http://maven.apache.org/SETTINGS/1.0.0`,
`http://maven.apache.org/SETTINGS/1.1.0` or
`http://maven.apache.org/SETTINGS/1.2.0`, using B2's structural XML limits only,
not its POM root/modelVersion requirement. Remote metadata/POM readers likewise
reuse structural safety rules with their own network byte budgets, not the local
1MiB document limit. Interpret only
mirrors, profiles/repositories and activeProfiles as **possible relevant policy**;
no activation or interpolation is executed. Duplicate relevant scalars/IDs and
unknown relevant elements/attributes refuse dependent policy. Ignore bounded inert
pluginGroups/localRepository/interactiveMode/usePluginRegistry values without using
or following them. Literal offline=true refuses remote comparison; malformed or
dynamic offline is unknown. Never interpret credentials, proxy/server configuration,
private-key locations or external paths. Nonempty server/proxy credential-bearing
subtrees leave settings unsupported without extracting, copying or reporting their
contents. Diagnostics contain fixed reason codes only, never raw settings or URLs.
Settings profiles that only add unassigned alternates remain non-vetoing; profiles
that may exclude/redefine Central leave dependent policy unavailable.

## B5 — Mirrors, native filters and contrary evidence

For selected settings mirrors, retain declaration order, literal safe ID, bounded
URL, literal blocked boolean, default layout and mirrorOf/mirrorOfLayouts fields.
Mirror routing alone is acquisition eligibility, **not private/fork assignment**.
Never contact a mirror or treat its host as a new measurement destination. Maven's
[pinned settings model](https://maven.apache.org/ref/3.9.11/maven-settings/settings.html)
and [mirror guide](https://maven.apache.org/guides/mini/guide-mirror-settings.html)
establish exact-ID preference, then first matching pattern; multiple mirrors are
not combined. Use only this bounded syntax, evaluated against default Central's
`central` ID, HTTPS/nonlocal identity and `default` layout:

- exact literal IDs; comma-separated literals; `*`, `external:*`, `external:http:*`;
- `!ID` exclusion, with no surrounding/internal whitespace, empty tokens, arbitrary
  wildcard fragments, regular expressions or interpolation;
- mirrorOfLayouts absent means `default,legacy`; otherwise literal comma-separated
  layouts with `*` and `!layout` exclusions under the same bounded grammar.

Match exact whole mirrorOf=central first; otherwise use first matching declaration
under Maven3.9.11 rules, including explicit include/exclude precedence over wildcard.
`external:http:*` does not match HTTPS Central; `!central,*` excludes Central from
that mirror and does not exclude Central itself. A safely selected blocked=true
mirror matching Central is explicit Central block: refuse before HTTP. A supported
unblocked mirror match alone does not veto. Unknown relevant match/layout/blocking,
ambiguous IDs or unsupported grammar refuses; an exactly excluded/unrelated mirror
cannot poison Central merely by existing. Public identity recognition on a mirror
URL adds no acquisition/content assurance.

Initial Feature007 does **not** implement Resolver prefix/groupId filters. Any
recognized relevant repository-contained `aether.remoteRepositoryFilter.*`,
`maven.resolver.remoteRepositoryFilter.*`, Central-replacement or equivalent
unsupported repository-policy mechanism is unknown at its affected scope; refuse
before lookup rather than apply another Resolver revision's defaults. An alternate-
only filter is not by itself Central exclusion. No custom include/exclude XML,
NuGet-style packageSourceMapping or name-prefix/private-organization heuristic is
invented. No archive/cache/config fetch repairs unsupported policy.

No new private/fork assertion or supplier format is introduced. Initial positive
contrary authority consists of supported occurrence system assignment, supported
Central exclusion/redefinition/block, identity conflict/substitution/relocation
recognized in admitted evidence, and unsupported relevant policy. A suggestive
coordinate, alternate URL, vendored artifact/hash, same-ID namesake or file repository
is not such assignment. Stronger future accepted occurrence-specific evidence must
use its separately approved reader; none exists initially. Known contrary evidence
is terminal and cannot be discarded in favor of conventional comparison.

## B6 — Failure isolation and required witnesses

Policy rejection withholds age, never fabricates a selected version or deletes safe
Declared facts/population. A source policy failure normally affects all dependent
rows of that source; unrelated sources and successful sibling ecosystems survive.
System assignment affects only that occurrence. Unknown identity/population retains
S6 null denominator/coverage rules, independently for each version view. A fixed
sanitized reason distinguishes unsupported source policy, explicit source refusal,
unsafe input, budget exhaustion and unavailable inherited facts. No source URL,
XML, credential, absolute path or raw exception enters output.

Offline witnesses must cover: ordinary no-policy admission; alternate/file/dynamic
non-central additions without veto; child whole-ID override; central disabled /
redefined / dynamic identity; parent/profile Central exclusion; unknown profile
that only adds an alternate; missing external parent plus safe local rows; exact /
pattern / excluded / blocked mirrors; malformed mirror grammar; selected versus
co-located settings; escaping/multiple selectors; nested launch ambiguity; core
extension/JVM unknowns; no credential/alternate endpoint access; directory/XML /
expansion/occurrence/policy budgets; link/race/capability refusal; and mixed siblings.
These are future deterministic acceptance obligations, not executed tests.

Technical provenance: the bounded selection grammar follows the documented
[Maven configuration convention](https://maven.apache.org/configure.html) only for
its pinned3.9.11 subset. New Maven3.10 Central-replacement environment/property and
Maven4 automatic project-settings mechanisms shown in current docs are not silently
imported as supported3.9.11 semantics. Recognizable relevant unknown routes refuse.
No user/global settings, Maven/Gradle/Java/build tool, target or provider was accessed
or executed to define this contract.
