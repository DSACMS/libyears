# Qualified repository snapshot validation — 006-0028

Runtime R2 candidate a2aa3c6; spec/plan/graph freezes and dispositions in reviews.md.
Historical artifacts remain frozen, including006-0027 preserved in e736736.

## Boundary matrix and traceability

| User case / obligation | Actual witness |
| --- | --- |
| 1 A first | SourceTests.test_a_precedence_preserves_missing_testimony_and_v3_refusal; old A/v1/v2 source/cascade/precision tests unchanged |
| 2 unrelated unsupported syntax | PrimitiveTests.test_unrelated_syntax_does_not_require_complete_a_semantics; ordinary no-mapping B1 source test |
| 3–7 add/remove/request/extra/missing | PrimitiveTests.test_both_directions_and_changed_requests_are_terminal; SourceTests.test_bidirectional_stale_and_mismatched_locks_cannot_be_repaired_by_v3, both no-witness and rebound synthetic public-v3 boundaries |
| 8 framework mismatch | Same terminal source test and PrimitiveTests framework test |
| 9 ambiguous/multiple context | PrimitiveTests.test_framework_conflicts_ambiguity_and_unextractable_facts; whole-lock multiple-context negatives; repeated equal literals leave B1 unavailable and preserve B2 |
| 10 unsupported/malformed whole lock | PrimitiveTests unsafe/over-budget test; SourceTests.test_unsafe_and_unsupported_whole_evidence_never_reaches_witness |
| 11 duplicate/ambiguous IDs | Case aliases in both project and lock, whole-source refusal before witness/capability |
| 12 copied mismatching lock | Primitive copied test plus terminal ID/request/framework source boundaries |
| 13 coherent copied pair | PrimitiveTests.test_copied_matching_pair_and_normalized_minimum_are_eligible; policy source limitations explicitly no historical producing association |
| 14 dirty input | Real filesystem test creates staged project, dirties current bytes, leaves lock untracked; real safe reader accepts current coherent pair, Git status unchanged |
| 15 non-Git input | Real filesystem test accepts pair without .git; guards prove runtime uses no process/Git/network |
| 16 no namespace | SourceTests automatic_b1_namespace_absent: known N/selected version, unsupported_dependency_source, no witness read/process/socket/URL/capability; real OASim48 such rows |
| 17 explicit valid namespace | SourceTests B1+v3 test uses real registry/capability codecs with offline metadata transport, latest-used exactly0.0, no acquired/content/event claim |
| 18 B1+v3 retention | Same test retains qualified_repository_snapshot basis, supplied_snapshot_population_assertion trust and accepted_retained_external_direct_snapshot limitation |
| 19 contradiction+v3 | Terminal source mutations rebound synthetic testimony; reverse conflict checked even with unextractable framework; no witness read or lookup |
| 20 independent occurrences | SourceTests unavailable_a_and_independent_b1_occurrences; old repository/mixed repeated-source tests |
| Q2 partial knowledge | Strict metadata/conditional/nested/computed/root/group/mutation negatives; all-known conflict checks before other ineligibility; no A grammar change |
| Q3 B2 retained | Computed references, imports, repeated identical framework literals and ambiguous shared immediate lock can use explicit v3; explicit precision historical tests remain |
| Q4 invalid explicit evidence | Wrong bytes/project/framework, false assertions, malformed/extra/old-version testimony refused with B1 N retained; namespace private/unknown/conflicting tests zero calls |
| Q4 schema/privacy | Source basis/limitations/trust and row selection serialized schema3; concise current-snapshot qualifier and truthful namespace reason; no canary/raw digests/origin/target root; real verboseJSON equals JSON |
| Q5 safety/compatibility | Existing reader/discovery/worker refusal and cross-ecosystem suites, semantic tests active without native capabilities; historical fixture bytes unchanged |

PrimitiveTests/SourceTests above are in tests/test_nuget_repository_snapshot.py;
existing test_nuget_population_source covers explicit B2 and ordinary A/B composition.

## Executed checks

- Initial unchanged baseline:730 tests PASS/no skips.
- R1:72 primitive/project/lock/provenance tests PASS.
- R2:276 focused project/lock/provenance/population/source/repository/cascade/scan/
  CLI/output/mixed tests PASS. Full deterministic `python3 -m unittest discover -s tests`:
  **751 PASS/no skips**. Capability-disabled full discovery, setting
  os.supports_dir_fd=set() before imports/discovery: **751 successful,51 genuine
  native filesystem skips**, including2 new dirty/non-Git witnesses. Semantic and
  capability-refusal tests remain active; no fabricated platform support.
- Dedicated tests.test_nuget_worker.RealWorkerTests: **3 PASS**.
- git diff --check PASS. Canonical history GitLeaks follows committed R3 and closure.
- Initial expected ordinary fixture basis assertion and an author test argument
  mistake were corrected before passing runs, not misrepresented as passes.

Private logs:006-0028/full.log and capability.log. Capability simulation does not
establish actual Windows behavior. Actual hosted Windows/macOS/security/CI remain
post-publication witnesses for this candidate.

## Actual ordinary OASim journey

Exact authorized target invocation from trusted scanner checkout:
`python3 -m libyears OASIM_ROOT` (exact absolute authorized path retained privately).
Also executed --json and --verbose companions. Each exits0, stderr0bytes. Raw outputs
and exits retained privately under006-0028/oasim-{human,json,verbose}.*. In-process
ordinary/JSON/verbose/verboseJSON companions with socket/process/URL guards return
exact same output; **zero network/process calls**, verboseJSON equals JSON.
No mappings, witnesses, locks or retained evidence are generated or accepted.

| Source under SRTRMatchRunApplication | A occurrences | B1 occurrences | B2 occurrences |
| --- | ---: | ---: | ---: |
| MRCalc | — | 9 | 0 |
| MatchRunBenchmarks | — | 2 | 0 |
| MatchRunCLI | — | 8 | 0 |
| MatchRunEngine | — | 4 | 0 |
| MatchRunProfileUpdater | 1 | — | 0 |
| MatchRunProfiling | 2 | — | 0 |
| MatchRunTests | — | 5 | 0 |
| OASim | — | 9 | 0 |
| OASimCLI | — | 9 | 0 |
| SimulationEngine | — | 2 | 0 |
| Total | 2 populations / 3 | 8 populations / 48 | 0 / 0 |

**Accepted repository denominator N=51** independent occurrences. Repository/NuGet
M=0; coverage=null. No measured rows,48 individual unmeasurable rows and2 source
errors. Total0.0, mean/median/max null are not evidence of freshness. Each B1 source
has known N, M0/coverage0; the two A source measurements/numerics/coverage remain
null because existing whole witness authority is unavailable. The distinction is
unchanged aggregation, not a new coverage policy.

Exact blockers: all48 B1 rows unsupported_dependency_source, with selected versions
retained and human text “accepted public namespace authority unavailable; no public
namesake is substituted”. No B1 source reports unsupported_nuget_project or missing
supplier population authority. A Updater/Profiling retain nuget_provenance_missing:
existing baseline/context/namespace testimony is not selected. Existing Updater
witness presence is not acceptance. No real public date/latest/age is newly checked;
metadata suitability remains untested after namespace. Missing stronger event/content/
reproduction assurance is not substituted as the blocker. No namespace is automated.

## Target integrity

Trusted capture helper established baseline before content inspection: HEAD,
full NUL porcelain-v2 status including ignored state, exact index digest/entries,
223 tracked and12 nonignored untracked file bytes/modes/size/mtime,50 ignored file
names/types/modes/size/mtime and relevant ignored evidence (none). No config/cache/
credential/asset interpretation; ignored unrelated bytes are not hashed. Captures
are not atomic or OS-wide invariance. Initial directory-only inventory capture was
expanded to the full50-file inventory before any project/lock interpretation.

After current production parsers, ordinary commands and guarded companions:
**byte-identical oasim-before.json and oasim-after.json**. Existing dirty state is
preserved, not claimed clean. No target writes/cleanup/normalization/execution,
dotnet/NuGet/MSBuild/restore/build/tests, new evidence or target-behalf network.
Final equality is repeated at closure. Private capture helper/manifests and guarded-
operation.json retain the exact witnesses.

## Outcome and remaining gates

Implementation supports the deliberately narrower current-snapshot policy:
full observable parity can replace repeated population-selection intent after
reusable human policy approval; it does not recover producer history or namespace.
This one case informs the future retrospective framework, not a universal rule.
No framework is created. Namespace automation, bounded static grammar, stronger
producer assurance, CI action warning maintenance and evaluated MSBuild use cases
remain separate future work. No push; next human gate after independent convergence
is publication authorization followed by actual hosted platform/security/CI.
