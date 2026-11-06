# NuGet root recognition validation — 006-0020

Classification: **bounded product correction after Feature 006 operational
closure**, using maintenance artifacts and the normal SDD workflow. It is not
Feature 007 and does not reopen the original feature's converged/closed history.
Code candidate: `45c455e`; baseline: clean `13c6a66`. Independent convergence
disposition belongs in [reviews.md](reviews.md); this evidence is frozen first.

## Final behavior and discovery boundary

Ordinary human directory invocations recognize regular lowercase `.csproj`
filename candidates and list escaped relative paths. Counts cover root depth
zero through depth four only. Deeper subtrees, all dot-prefixed directories and
exact `bin`, `obj`, `node_modules`, `packages`, `vendor`, `venv`, `__pycache__`
directories are excluded. No symlinks/reparse points or special files qualify.
Bounds: 256 visited directories, 10,000 enumerated entries (including skipped
entries), 100 candidates; inclusive cap/cap+1 enforcement. Count overflow and
access/replacement/filesystem failures suppress lists/totals and report incomplete.
Absent required descriptor/non-following capabilities report unavailable before
opening anything. These are observations, not atomic snapshots or latency SLAs.

Recognition never opens project contents or establishes NuGet dependency/source
authority. One or many candidates require explicit immediate-filename selection
at the chosen parent directory, then all existing eligibility/lock/provenance
checks. No selection, aggregation, deduplication, repository NuGet metric,
solution/reference semantics, package-manager/target execution, archives,
configuration/cache/credential inspection, generic analyzer or additional
ecosystem/provider work is introduced. JSON performs no recognition; scan/model,
schema-v3, source authority, publication rules and metric arithmetic are unchanged.
Other root ecosystems retain their available measured rows and numeric facts.

## Required OASim user-journey witness

From the trusted scanner checkout, the exact authorized absolute-root command
`python3 -m libyears OASIM_ROOT` (actual argv retained privately) exits **0** with
empty stderr. Its output includes the following excerpt; no paths are abbreviated
in the retained raw report:

```text
Ecosystems scanned for measurement: none

NuGet / C# project candidates: 10 (bounded search).
Search covers root through depth 4; hidden/generated/dependency directories are excluded.
```

Ten quoted project paths follow, in sorted order: MRCalc, MatchRunBenchmarks,
MatchRunCLI, MatchRunEngine, MatchRunProfileUpdater, MatchRunProfiling,
MatchRunTests, OASim, OASimCLI and SimulationEngine, each under its existing
`SRTRMatchRunApplication/NAME/NAME.csproj` location. The report then states:

```text
No NuGet measurement was performed. Explicit project selection is required.
Use the chosen project's parent directory as PATH and its filename as NAME.csproj:
  python3 -m libyears PATH --nuget-project NAME.csproj
Measurement still requires an eligible project, packages.lock.json and an explicitly
accepted --nuget-provenance NAME.json witness. Candidate names alone establish none of these.
```

Repository metrics remain null coverage, **0/0 measured**, total **0.00**, null
mean/median/max. No project was implicitly selected or claimed measured.
The misleading exact `Ecosystems: none` line is absent.

Before the initial smoke and after each attempt, integrity-only hashing compares
all **223 tracked files**, including byte lengths, SHA256 and modes. Revision and
full porcelain status (including untracked names) also match exactly. The trusted
helper runs outside the target with Git optional locks disabled; unrelated
application contents are hashed only, never interpreted/executed. No target write
or package-manager/target execution occurs. This proves tracked bytes/modes and
status unchanged; it is not a byte audit of untracked/ignored contents or OS-wide
side effects. The recognition code reads only directory metadata.

The first smoke at `dae94b2` failed R6: a deeper assets subtree caused the original
policy to suppress the entire list. Initial stdout/stderr, metadata-only diagnosis
and integrity evidence remain retained. The implementation conformed to that
original rule. The explicit [specification correction](depth-spec-correction.md)
and [architecture/task correction](depth-plan-correction.md) were separately
frozen and freshly approved before D1 code changes. The corrected command above
then ran once and passed. No failure is backdated or hidden; traversal was not
expanded to obtain the result.

## Acceptance and verification

| Criterion | Actual evidence |
|---|---|
| R1 | Discovery zero/one/many sorted names, malformed/unsupported/unreadable content with no opens, exact suffix/type; human one/many tests assert no NuGet source/process/network calls and no NuGet request |
| R2 | Real production-sized directory/entry/candidate cap and cap+1, global budgets, exact five opens for depth-four inclusion/depth-five pruning, exclusions, symlink/FIFO/reparse refusal, success cleanup |
| R3 | Unskipped primitive-disabled no-open/no-scan tests; separate filesystem replacement/mutation/error cleanup; injected human incomplete/unavailable/metadata failure with safe text and no false absence |
| R4 | Escaped control/non-ASCII candidate display and generic noninterpolated command; one measured sibling and three actual measurable PyPI/npm/Ruby sources with dir_fd disabled retain explicit rows/counts/total and per-ecosystem numeric assertions |
| R5 | JSON/verbose JSON exact equality and zero recognition calls, empty human exact equality, direct-file/explicit selection bypass; existing shared output/CLI/mixed/NuGet regressions; scan/model/JSON serializers unchanged |
| R6 | Exact real-root smoke and raw comparison, 223 tracked byte/mode/revision/status equality, full offline/capability/worker/history/diff checks below; independent convergence follows freeze |

| Check | Observed local result on corrected code |
|---|---|
| Discovery + recognition + NuGet CLI + CLI + output + mixed focused tests | **129 PASS** |
| `python3 -m unittest discover -s tests` | **663 PASS**, zero skips |
| Full suite, os.supports_dir_fd empty before discovery | **663 PASS, 44 genuine filesystem skips** |
| `python3 -m unittest tests.test_nuget_worker.RealWorkerTests` | **3 PASS** |
| `python3 tools/check_gitleaks.py` at committed `45c455e` | **exit 0**, GitLeaks **8.30.1**, **264 commits**, no unsuppressed findings; actual config/full available history |
| Working/range/staged `git diff --check` | **PASS** at task boundaries; final disposition check follows |

Capability simulation is local evidence only. Production refusal tests and
portable composition execute; only genuine filesystem witnesses skip. **Actual
Windows CI and hosted checks for this candidate are UNOBSERVED**, requiring
separately authorized publication. Historical Windows/GitLeaks success recorded
in the closed Feature006 operational loop applies to that historical commit.
Scanner policy/config/exact historical exceptions and workflow remain unchanged.

Private evidence: `/tmp/libyears-observations/006-0020`, including raw initial/
corrected stdout/stderr, tracked manifests, metadata-only diagnosis, smoke
comparison, test/history logs, freeze manifest and independent review reports.
Fingerprints, absolute checkout paths and raw target status are not published.

## Reconciliation and handoff

ROADMAP's existing project-root discovery/listing opportunity records human
selection of this bounded NuGet correction and points to these artifacts.
Broader cross-ecosystem listing/indexing remains unselected. Feature006 artifacts,
historical convergence and operational closure retain their original bytes.

The required obvious invocation found a product-rule defect that deterministic
fixtures faithfully reproduced as designed; unit success alone did not establish
the real journey. Returning to specification, retaining the failure, narrowing
the completeness claim and fresh reviewing each correction gate resolved it
within the existing product authority. No attention/resource savings, positive
NuGet measurement yield or broad repository coverage is inferred.

After independent convergence, the next human gate is **publication authorization**
for this committed candidate. Only then observe actual Windows and hosted checks.
No push, release/tag, Feature007/Java, provider adoption or target execution occurs.
Run `006-0020` is handed off separately, not appended to the ledger; child reviews
have no separate observations. No unavailable telemetry is reconstructed.
