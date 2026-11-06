# NuGet root recognition: product contract

Bounded follow-up correction to Feature 006; approval lives in [reviews.md](reviews.md).
Original Feature 006 measurement contracts and closed history remain intact.

1. Ordinary human directory invocation without `--nuget-project` recognizes
   regular files with exact lowercase `.csproj` suffix as C# project candidates.
   Recognition examines names and filesystem metadata only. It does not assert
   SDK eligibility, PackageReferences, dependency population or measurement.
   Project contents may be malformed, unreadable or unsupported and still qualify
   as filename candidates. Symlinks and other special files do not qualify.
2. Search only the supplied root and descendants through four directory levels
   (root depth zero; candidate files in depth-four directories included). Skip
   all dot-prefixed directories and exact names `bin`, `obj`, `node_modules`,
   `packages`, `vendor`, `venv`, `__pycache__`. Do not follow directory links or
   reparse points. Never traverse solutions, project references, ancestors or
   external roots. At most 256 visited directories, 10,000 enumerated entries
   (including skipped entries) and 100 candidates. Limits are inclusive.
3. Completed recognition returns a sorted relative candidate list; its count
   means candidates in this bounded search only. A remaining nonexcluded directory
   beyond depth four, any limit overflow, inaccessible/replaced directory or
   filesystem error makes recognition incomplete. Required safety primitives
   unavailable makes recognition unavailable. Both states suppress candidate
   lists/exact totals and explain that presence/count are undetermined; they do
   not claim there are no projects. No raw exception or offending path is printed.
   Resource bounds constrain enumeration/work, not OS blocking latency or a
   concurrent filesystem's atomic snapshot. All handles are closed on every path.
4. Human output with candidates says NuGet/C# project candidates were found and
   **no NuGet measurement was performed**; lists quoted root-relative paths with
   control/non-ASCII characters escaped; explains explicit selection using the
   candidate's parent as PATH and filename as `--nuget-project NAME.csproj`.
   It states eligibility and existing lock/provenance requirements still apply.
   One candidate never activates measurement. Incomplete/unavailable recognition
   gives the same no-measurement/selection guidance without claiming presence.
   These reports must not print `Ecosystems: none`; source labels describe
   ecosystems scanned for measurement, independently of recognition.
5. A completed empty recognition keeps established human output unchanged.
   Recognition adds no source, dependency, summary, coverage denominator, evidence
   or error to the measurement report. Existing sibling ecosystems, all metric
   arithmetic and schema-v3 JSON remain unchanged. JSON performs no recognition
   traversal and receives no candidate text (including verbose JSON). Explicit
   NuGet selection and direct-file scans keep their existing behavior.
6. No target code/package manager execution, networking for recognition, project
   content reads, input writes, implicit selection, aggregation/deduplication,
   repository NuGet metric, solution/reference semantics, source/provenance change,
   runtime dependency, generic analyzer refactor or additional ecosystem work.

Acceptance criteria (all require implementation evidence):

- **R1:** Zero/one/many candidates obey exact filename/type rules, no content reads,
  deterministic sorting and no implicit selection, including malformed/unreadable
  content and unsupported declaration formats.
- **R2:** Exact depth, exclusions and directory/entry/candidate cap/cap+1 cases;
  links/reparse points/special files never escape; incomplete results reveal no
  exact population or partial candidate list; handles close on failures.
- **R3:** Unavailable primitives, unreadable directories and replacement races
  fail safely and visibly, without raw diagnostic disclosure or false absence.
- **R4:** Human candidate/status disclosure and useful explicit-selection guidance
  compose with measurable PyPI/npm/Ruby sources and preserve numeric facts.
  Names cannot inject terminal lines or shell commands into guidance.
- **R5:** JSON byte compatibility and no recognition traversal; no-source,
  direct-file and explicit-selection compatibility. Semantic composition uses
  injected evidence; real filesystem and capability-disabled witnesses separate.
- **R6:** Exact authorized OASim root command recognizes the known ten candidates,
  explains no NuGet measurement/next action, omits misleading `Ecosystems: none`,
  exits zero, and leaves tracked content and target status unchanged. Full offline
  suite, capability simulation, canonical GitLeaks history gate and diff checks
  pass. Freeze implementation and smoke evidence for independent convergence.
  Actual Windows/hosted evidence remains pending separate publication authority.
