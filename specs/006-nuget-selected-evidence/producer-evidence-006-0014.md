# Native NuGet producer evidence experiment — 006-0014

**Overall outcome: D — EXPERIMENT BLOCKED. HUMAN PRODUCT/AUTHORITY DECISION.**
The required original-context source/semantics precondition was not established.
An isolated replay nevertheless ran; that was an execution-scope deviation, not
completion of the authorized original-context experiment. Its package evidence is
useful but partial (B describes that narrower evidence only). No witness was
manufactured, no consumer scan ran, and T016/K5 remain incomplete. Initial frozen
bytes and both reviews are retained privately; reviews.md preserves correction
and independent verification. This corrected candidate is frozen for verification.

## Authority and bounded selection

The human authorized this producer experiment against the exact OASim repository,
installed .NET 10, isolated temporary state, public nuget.org restore traffic,
two fresh non-author reviews, and a durable record. This exception is exclusively
producer-side: no product execution boundary, H1–H4, schema or specification is
changed. No OASim build, application execution, tests, workload installation,
private feed, credential use or configuration/source modification is authorized.

Starting libyears HEAD: `0ee799b3377ead78ace3aba07e0671b860f6d1ed`, clean.
OASim HEAD before/after: `1e937015e1d242fee5597ea0fbdc4cd5c983f101`.
The prior [006-0013 preflight](validation-006-0013.md) limits selection to its ten
candidates. Only MatchRunProfileUpdater and MatchRunProfiling have supported
declarations. Choose **MatchRunProfileUpdater.csproj / net10.0**: it has a complete
one-package lock and no project references. Profiling has two project references;
following those or suppressing their graph would make it a weaker isolated probe.
No additional candidate or unrelated application content was inspected.

Only those two project files were read for selection, followed by the selected
project/lock through ScopedNuGetReader. Immediate names were checked for
NuGet.Config, Directory.Build.props/targets, Directory.Packages.props and global.json
at repository root, SRTRMatchRunApplication, and both candidate directories;
none existed there. No configuration content, ancestor outside OASim, existing
cache, SDK source file, settings or referenced project content was inspected.

## Authoritative semantic check before restore

References checked on 2026-11-04, before producer execution:

1. Microsoft [global packages and caches](https://learn.microsoft.com/en-us/nuget/consume-packages/managing-the-global-packages-and-cache-folders):
   global-packages stores expanded packages outside project trees; exact installed
   versions are checked before other sources and HTTP cache. NUGET_PACKAGES,
   NUGET_HTTP_CACHE_PATH, NUGET_SCRATCH and NUGET_PLUGINS_CACHE_PATH redirect state.
   The metadata marker is written at successful extraction completion. Optional
   access-time updates and no-op restores make file timestamps unsuitable as a
   per-project acquisition history.
2. Microsoft [installed-package troubleshooting](https://learn.microsoft.com/en-us/nuget/concepts/troubleshooting-installed-packages):
   extraction writes .nupkg.metadata; NuGet 5.9+ records source, while older version-1
   records can lack it. Source identifies the configured supplying service, not
   any upstream behind that service. Normal-verbosity installation logs also
   report identity, version, source and content hash. This is producer testimony,
   not authenticated provenance or proof of original upstream authorship.
3. Microsoft [source mapping](https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping):
   an already cached package bypasses source lookup and mappings. Therefore a
   current source configuration cannot retroactively establish cached origin.
4. NuGet's [metadata design](https://github.com/NuGet/Home/wiki/Nupkg-Metadata-File)
   distinguishes signature-independent content hashes from archive hashes. Its
   historical version-1 example is not assumed to be today's complete schema.
   Current upstream [PackageExtractor](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Packaging/PackageExtractor.cs)
   writes ContentHash and supplying Source, separately from the archive SHA512;
   [PackageArchiveReader](https://raw.githubusercontent.com/NuGet/NuGet.Client/dev/src/NuGet.Core/NuGet.Packaging/PackageArchiveReader.cs)
   uses signed-content hash handling and an archive-hash fallback for unsigned
   packages. These development-branch sources corroborate semantics, not exact
   installed-binary identity. No public catalog hash-domain equivalence follows.
5. Microsoft [dotnet restore](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-restore):
   explicit configfile limits configuration to that file; locked mode prevents
   lock updates; packages redirects package state; no-http-cache avoids reuse.
   Restore can use MSBuild evaluation. Its success is not a complete input-baseline
   assertion. [MSBuild restore documentation](https://learn.microsoft.com/en-us/nuget/reference/msbuild-targets)
   describes generated dependency artifacts. No artifact is promoted to a product
   input through this experiment.

## Mandatory precondition and execution-scope deviation

The commissioning instruction required determining source safety from bounded
permitted configuration and stopping if authorized public restore could not be
constrained without changing target semantics or configuration. The pre-restore
record did not establish equivalence to the original evaluated context. The agent
substituted a copied project/lock with directory import discovery disabled and
an experiment-owned public configuration, then executed that narrower replay.
Exact project bytes and unchanged original files do not prove equivalent imported
source/dependency semantics. The required precondition remained unestablished;
the agent should have stopped before restore. This deviation is retained, not
retroactively approved by useful output or evidence-record review.

Both fresh reviewers initially approved the truthful partial record under their
assignments. After receiving the verbatim source/isolation condition, both
superseded that assessment with COMPLETE / REVISE on this authority issue. Parent
validation agrees. No private-feed contact, credential use or product defect is
established. No additional original-context execution or authority workaround is
attempted. The overall experiment is D, while the narrower replay yields partial
package evidence. No inference is used to bridge that distinction.

## Frozen expectations and isolation

Private evidence root E is `/tmp/libyears-observations/006-0014`.
P is E/producer. Before restore, expectations.json froze exact input bytes/digests,
the full lock, command, explicit environment, target revision/status, expected
population and comparison policy. Its SHA256 is
`3430691f5d0574994f464757fb3ca033c6e0a11fa92a746f1c9862416764ffd6`.
Raw target fingerprints stay outside Git, in inputs-before.json and expectations.json.

Frozen population: one explicit direct Microsoft.Win32.Registry, declaration 5.0.0,
lock requested `[5.0.0, )`, resolved 5.0.0, schema 1 / sole net10.0. No transitive
or project lock nodes exist. Expected native package population is exactly
Microsoft.Win32.Registry/5.0.0. Expected hashes came from the pre-existing lock;
origin had to be observed, never inferred from configured eligibility. The required
witness comparison is the plan's complete strict serialization, including all
baseline booleans and exact-byte context bindings.

To avoid target writes, target-generated imports and unbounded ancestor evaluation,
the producer restored exact-byte copies of the selected project and lock under
P/input. This is an **isolated replay**, not an in-place restore of OASim and not
proof of equivalence to its unexamined evaluated baseline. No target configuration
was edited. Directory import discovery was disabled explicitly; no target-derived
source property/import existed in the inspected project. An experiment-owned
NuGet.Config contains only:

```xml
<?xml version="1.0" encoding="utf-8"?><configuration><packageSources><clear/><add key="nuget.org" value="https://api.nuget.org/v3/index.json"/></packageSources><disabledPackageSources><clear/></disabledPackageSources><fallbackPackageFolders><clear/></fallbackPackageFolders></configuration>
```

This public-only configuration constrains the replay, without claiming knowledge
of outside-repository user/ancestor configuration. It preserves the supplied
literal dependencies/framework and locked selections; equivalence to the original
evaluated target semantics is UNESTABLISHED. The replay cannot authorize an
original-context witness by copying its project filename into an envelope.

The subprocess received a newly constructed environment, not inherited credentials,
proxy, source or plugin settings. Exact overrides (P expands as above):

```text
PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
DOTNET_ROOT=/usr/local/share/dotnet
DOTNET_CLI_HOME=P/cli
DOTNET_CLI_TELEMETRY_OPTOUT=1
DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
DOTNET_NOLOGO=1
DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE=true
DOTNET_CLI_USE_MSBUILD_SERVER=0
MSBUILDDISABLENODEREUSE=1
NUGET_PACKAGES=P/packages
NUGET_HTTP_CACHE_PATH=P/http
NUGET_SCRATCH=P/scratch
NUGET_PLUGINS_CACHE_PATH=P/plugins
TMPDIR=P/tmp
```

All these directories were newly created; no existing global package cache was
copied or used as evidence. HOME was not reassigned. The explicit configuration
contains no credentials. Only the public source is configured. No interactive
authentication or credential operation was invoked. Configuration and producer
artifacts confirm the single public source; this is not an OS packet-capture
claim about every SDK side effect.

## Exact producer commands and observed result

Commands used `/usr/local/share/dotnet/dotnet`, cwd=P, the environment above,
shell=False, captured stdout/stderr, and a 180-second restore subprocess timeout:

```sh
/usr/local/share/dotnet/dotnet --version
/usr/local/share/dotnet/dotnet restore P/input/MatchRunProfileUpdater.csproj --configfile P/NuGet.Config --packages P/packages --locked-mode --no-http-cache --disable-parallel --disable-build-servers --verbosity normal -p:NuGetAudit=false -p:ImportDirectoryBuildProps=false -p:ImportDirectoryBuildTargets=false -p:ImportDirectoryPackagesProps=false -p:RestoreFallbackFolders= -p:RestoreAdditionalProjectFallbackFolders=
/usr/local/share/dotnet/dotnet nuget --version
```

SDK: **10.0.403**. NuGet command version:
`7.9.0-rc.2412+5a2162bea6845eabc1fc721624a43568c65db3b1.5a2162bea6845eabc1fc721624a43568c65db3b1`.
SDK installation/tool source was not inspected. Workload update/install was never
invoked. The initial sandbox restore exited 1 with NU1301/DNS failure and a workload
verification diagnostic; these raw outputs are retained under sandbox-* names.
The identical command was retried with sandbox network escalation and exited **0**,
empty stderr. The failed attempt had not downloaded a package; the successful
attempt logs GET/OK and installation for the sole expected identity. Failed restore
output in temporary obj existed on retry; it is not treated as successful evidence.

Successful restore emitted NU1510: the explicit Registry reference is automatically
available and will not be pruned. The direct package remained in assets and was
installed. No reference was removed. The MSBuild summary says Build succeeded for
the Restore target; no Build target, compiler, application or test command ran.

## Observed native evidence and exact comparison

Only generated metadata/dependency artifacts and restore logs were inspected:

| Native artifact | Observed structure and linkage |
|---|---|
| P/packages/microsoft.win32.registry/5.0.0/.nupkg.metadata | Exactly version=2, contentHash, source. No package ID/version/project/framework fields. Source is the exact canonical public index URL. Decoded contentHash is 64 bytes and equals the frozen lock hash. |
| P/input/obj/project.assets.json | Format 4; sole net10.0 target; sole library Microsoft.Win32.Registry/5.0.0, type package, matching sha512 and package-relative path. Restore context names temporary project, package/output paths, sole config and public source; dependencies retain the direct minimum. |
| P/input/obj/MatchRunProfileUpdater.csproj.nuget.dgspec.json | Format 1; restore/project mapping for the temporary project, framework and dependency request. It describes evaluated restore inputs, not a signed or exhaustive imported-input inventory. |
| P/input/obj/project.nuget.cache | Version 2, success=true, temporary projectFilePath, dgSpecHash, expectedPackageFiles and NU1510. dgSpecHash is not project_sha256 or lock_sha256. |
| restore.stdout | GET/OK public flat-container index/archive and Installed identity/version/source/hash line corroborate fresh extraction. Source eligibility alone was not used as origin. |

Native JSON bytes are preserved verbatim in E/native, with source names, lengths
and SHA256 in native-manifest.json. No archive, DLL, nuspec or package payload
was opened by the capture/analysis code; only NuGet itself downloaded/extracted
the authorized package. Matching assets/lock/metadata share one producer and are
not independent resolver implementations. No catalog lookup or public hash/date
comparison occurred; signed-content versus public catalog fitness stays unverified.

## Witness-field mapping

Categories below are literal review classifications. Derived context means only
the observed isolated replay unless explicitly qualified; it does not certify
the original checkout's producing history.

| Required witness field | Classification | Native evidence → permitted transformation → meaning/gap |
|---|---|---|
| version | DERIVABLE WITHOUT AMBIGUITY FROM BOUND PRODUCER CONTEXT | Contract selects envelope version 1; native metadata version 2 is unrelated and must never be copied as witness version. A serializer could write 1 only after all meanings are satisfied. |
| project | DIRECTLY RETAINED BY NUGET | assets/dgspec temporary projectPath → filename → selected name; retaining the name does not establish original-path provenance. |
| framework | DIRECTLY RETAINED BY NUGET | sole assets target/originalTargetFrameworks → exact net10.0. |
| project_sha256 | DERIVABLE WITHOUT AMBIGUITY FROM BOUND PRODUCER CONTEXT | Before/after exact copied bytes → SHA256; capture adds a digest, not a NuGet assertion. Original selected project bytes match. |
| lock_sha256 | DERIVABLE WITHOUT AMBIGUITY FROM BOUND PRODUCER CONTEXT | Exact frozen/unchanged lock bytes → SHA256; native dgSpecHash is no substitute. |
| producer.name | DERIVABLE WITHOUT AMBIGUITY FROM BOUND PRODUCER CONTEXT | Executed dotnet/NuGet command identity → producer label; .nupkg.metadata has no producer-name field. |
| producer.version | DERIVABLE WITHOUT AMBIGUITY FROM BOUND PRODUCER CONTEXT | Captured dotnet nuget --version → exact reported version; retain SDK reading separately. |
| coherent_snapshot | NOT RETAINED / REQUIRES INFERENCE | Successful locked replay, retained bytes and artifacts support capture-context association; NuGet emits no assertion binding exact original project/lock digests and all relevant original inputs to one producing snapshot. |
| baseline.sdk | DERIVABLE WITHOUT AMBIGUITY FROM BOUND PRODUCER CONTEXT | Exact copied Project Sdk attribute plus controlled command → Microsoft.NET.Sdk for replay; not a native baseline attestation. |
| baseline.sdk_version | DERIVABLE WITHOUT AMBIGUITY FROM BOUND PRODUCER CONTEXT | dotnet --version → 10.0.403 under same cwd/environment; assets SdkAnalysisLevel is not the exact SDK version. |
| baseline.explicit_population_complete | NOT RETAINED / REQUIRES INFERENCE | Evaluated direct requests agree for replay, but no native assertion covers completeness under all original imported/generated/ancestor/central inputs. |
| baseline.unsupported_membership_version_influences | NOT RETAINED / REQUIRES INFERENCE | No native negative assertion about original relevant input baseline. Disabling import discovery for a replay does not attest the original baseline. |
| baseline.unsupported_framework_rid_influences | NOT RETAINED / REQUIRES INFERENCE | A sole output TFM and no RID graph do not assert absence of unsupported original influences. |
| baseline.unsupported_source_influences | NOT RETAINED / REQUIRES INFERENCE | Replay config/source observation proves this supplying service for this extraction; it does not attest original baseline source influences. |
| packages[].id | DIRECTLY RETAINED BY NUGET | assets target/library identity and Installed log → Microsoft.Win32.Registry; metadata directory association alone is insufficient. |
| packages[].version | DIRECTLY RETAINED BY NUGET | same native identity → exact 5.0.0, agrees with frozen lock resolved. |
| packages[].content_hash | DIRECTLY RETAINED BY NUGET | metadata contentHash → exact string unchanged; decoded SHA512 equals lock. Do not replace with archive hash. |
| packages[].origins | DIRECTLY RETAINED BY NUGET | metadata.source plus fresh Installed log → singleton exact canonical service URL. Preserves configured supplying source meaning; does not claim upstream authorship or historical origin for an earlier restore. |
| package containment binding to context/lock | DERIVABLE WITHOUT AMBIGUITY FROM BOUND PRODUCER CONTEXT | unique isolated package tree + assets path/hash + capture manifest → replay association. Native metadata alone has no context binding; original baseline remains unestablished. |

No CONFLICTING / AMBIGUOUS package identity, version, local content hash or supplying
source was observed in this one-package replay. Absence of complete baseline
testimony is insufficiency, not evidence that H3 is false. A qualified supplier
could add testimony under S4, but that would be an additional assertion, not a
faithful capture of native evidence alone. This run supplies no such assertion.

## Integrity, retained state and stop

Selected original project and lock byte counts/SHA256 match before/after, as do
the temporary copies after locked restore. Target HEAD and selected-directory
Git status, including untracked names, match before/after. These are scoped
checks, not whole-repository or outside-directory invariance claims. Selection
also read Profiling's project but no producer ran against it. No OASim file was
written by this procedure.

Private evidence includes expectations.json, inputs-before/after.json, git-after.json,
SDK/NuGet version captures, both restore attempts, comparison.json, run-producer.py,
and native-manifest.json/native artifacts. Temporary P contains the exact-byte
input replay, config, obj, downloaded/extracted package and isolated SDK/cache
state. It remains explicitly accounted for outside Git pending review; it must
not be committed. Cleanup disposition is recorded in reviews.md after review.

**No complete witness; no transformation script, CLI capture or T016 measurement.**
The existing consumer requires an immediate same-root explicitly accepted witness;
even a sufficient external capture would need a separately valid placement/input
boundary before an unchanged real-root procedure could use it without writing
OASim. This run never bypasses that constraint with a staged root called OASim.
No K5 approval, T017/K6 convergence or T018 work follows. No product tests were
rerun for an evidence-only change; prior 631/36-AC offline results remain historical.

The narrower replay establishes useful package-level observations only. The
authorized original-context experiment remains BLOCKED by the unestablished
source/semantics precondition; it was not completed faithfully. Separately, the
retained native evidence does not supply full baseline/coherence testimony.
Stop at HUMAN PRODUCT/AUTHORITY DECISION without modifying the contract, product
code, release procedure or approved spec/plan/tasks. Further producer work needs a
reviewable source/input boundary that honors the precondition, or new explicit
authority; this run selects neither. Feature 007 and the named maintenance side
issues remain untouched.
