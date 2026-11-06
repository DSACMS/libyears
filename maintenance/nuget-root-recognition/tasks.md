# NuGet root recognition task graph

Governing [spec](spec.md), approved SHA256
`662700c4975449117e9a04ac7fc7144e48c983dbbc3587220b77eb51454cc753`, and
[plan](plan.md), approved SHA256
`33f6be47a2902c1f45f90159bfd80ecb1f3bb2c6b4bc860cb92a119eb32698b4`.
Disposition and completion live in [reviews.md](reviews.md). Follow canonical
SDD_WORKFLOW rather than repeating its mechanics. Human prompt authorizes this
whole bounded correction, local commits, internal reviews/corrections and exact
read-only operational validation. No push or target execution is authorized.

| Task | Predecessors | Surfaces / done conditions | Acceptance |
|---|---|---|---|
| C1 | Approved task graph | Add nuget_discovery.py and focused test_nuget_discovery.py. Complete typed filename recognition, all finite traversal limits, safety/capability refusal, safe incomplete states, deterministic sorting and handle cleanup. Behavioral tests accompany implementation; production-sized cap/cap+1, content-read/process/network guards, real capability tests distinct from synthetic semantics. Focused tests pass; inspect diff and commit separately. | R1–R3 |
| C2 | C1 | Wire human/unselected directory recognition into cli.py and optional output.py disclosure; add test_nuget_recognition.py. Preserve direct-file/explicit selection/JSON bypass and scan/model results, sibling numeric facts and completed-empty output. Test escaped paths, one/many/incomplete/unavailable, sibling composition with injected recognition, no-call guards and JSON exact equality. Update README/SPEC/AGENTS/CHANGELOG and existing ROADMAP opportunity at this documentation checkpoint. Focused shared CLI/output/mixed/NuGet tests, full suite and capability-disabled full suite pass; inspect diff and commit separately. | R4–R5; R1 no implicit choice |
| C3 | C2 | Record exact authorized OASim root CLI stdout/stderr/exit, ten candidates, no misleading none, no NuGet measurement/selection. Compare before/after tracked bytes/modes/revision/full porcelain status. Record all R1–R6 evidence and concise retrospective in validation.md; run dedicated real-worker checks, canonical GitLeaks history gate on committed code candidate and diff checks. Freeze implementation/docs/tests and smoke/private evidence by hashes. | R6; reconcile R1–R5 |
| K1 | C3 | Fresh non-author read-only implementation/convergence review of spec/plan/tasks, all R1–R6, implementation/tests/docs, security/compatibility and actual smoke/integrity evidence. Parent validates findings/coverage and boundaries; determined bounded corrections require new freeze and fresh focused review. Record truthful convergence and remaining publication/Windows gates; commit evidence/disposition, rerun history gate on final committed candidate, confirm clean tree. | All six |

Execution is sequential. C1 and C2 each have one coherent local task commit;
C3/K1 evidence may share a final documentation commit because review changes
only disposition, not frozen substantive evidence. A preliminary authority-artifact
commit preserves the approved SDD gate candidates. Do not mark any task complete
from a passing count alone; the listed behavioral assertions must pass.
No new human gate is invented for bounded internal defects. Stop at the original
prompt's product/architecture/security/external authority hard stops.
