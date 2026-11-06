# Post-convergence operational smoke — 006-0018

Baseline: clean `db24c03a03085d684b207d9f9a1b57de4d877f10`.
This is maintenance after Feature 006, not Feature 007. Historical T017/K6
CONVERGED and T018 closure remain intact. The commissioning human supplied the
published Windows and GitLeaks logs summarized below; these are authoritative
hosted evidence, not independently retrieved new hosted runs. No push is authorized.
Classifications below preceded repair. Independent frozen review and final parent
disposition are recorded in [the review record](operational-smoke-006-0018-review.md).

## A — OASim root invocation

**EXPECTED BOUNDED BEHAVIOR + UX GAP; project-root discovery/listing remains
unselected product work. No product activation or integration defect established.**

The authorized read-only ordinary repository-root command reproduces exit 0,
`Ecosystems: none`, N=0/M=0, null coverage, total 0.00 and null mean/median/max.
The root has none of requirements.txt, package.json, Gemfile.lock or
packages.lock.json. A narrow filename check confirms all ten already-known C#
projects at `SRTRMatchRunApplication/NAME/NAME.csproj`; no recursive inventory,
configuration/cache/credential read or target execution was needed.

S1, AC-01, T013 and the approved plan explicitly require an immediate selected
project and intentionally omit colocated .NET evidence from ordinary scans.
`scan_mixed_repository` creates its fourth source pair only for NuGetRequest;
ordinary mixed scans keep their existing root source rules. There is no solution
or ProjectReference traversal. CLI help offers the immediate-project option;
README's NuGet section already explains opt-in activation. The basic PATH example
and `none` output nevertheless leave an obvious human invocation easy to misread
as a repository-wide absence claim.

A second bounded invocation points PATH at the known MatchRunProfileUpdater
directory and explicitly selects MatchRunProfileUpdater.csproj, WITHOUT supplying
or accepting any witness. It exits 0, activates NuGet, establishes net10.0/N=1,
accepts the root lock and returns nuget_provenance_missing with null measurement
and coverage. No metadata lookup is authorized by this state. This traces the
activation distinction, not a new real-root measurement or permission to replay
production. Only selected project/lock content is involved in this explicit scan;
OASim is neither modified nor executed, and no dotnet/NuGet/MSBuild runs.

Bounded repair: README now explains root-only source inspection, the meaning of
`Ecosystems: none`, and selecting a nested project directory. Runtime output and
activation semantics are unchanged. The existing ROADMAP listing opportunity
moves WATCH -> EXPLORE: a real human pain point now warrants bounded investigation,
while recurring demand and listing utility remain unproven. This selects no
feature, recursive search, automatic choice or multi-project aggregate.
**HUMAN PRODUCT DECISION** remains necessary to select/define that future work.

## B — Windows composed-test failure

**TEST PORTABILITY DEFECT / COMPOSED-TEST ARCHITECTURE DEFECT. No product
portability or CI configuration defect established.**

Supplied hosted evidence: Windows Server 2025 / windows-2025-vs2026, exact
db24c03 checkout, real worker tests PASS, full suite 636 tests with 11 failing
subcases, all in NuGetMixedScanTests' source-failure preservation test. Expected
PyPI/npm/RubyGems becomes PyPI/npm only. Local pre-repair execution with
`os.supports_dir_fd=set()` reproduces exactly 11 assertion failures, no errors.
This is a capability simulation on macOS, not Windows execution.

For `ruby_groups=None`, the ordinary Ruby source succeeds. For `('default',)`,
the real _ScopedRubyReader correctly refuses unavailable safe primitives,
returning invalid_gemfile/unknown Ruby scope and no row. The test still demands
three measured siblings for each of eleven NuGet failure cases. Its purpose is
AC-28 semantic preservation WHEN a sibling is available, not requiring successful
safe filesystem reads on every platform. Baseline-versus-candidate equality alone
would not catch this: both could silently lose Ruby; explicit three-row/count
assertions must remain.

Repair supplies only Gemfile/Gemfile.lock fixture text through the existing
fixture_scoped_reads seam and deliberately disables dir_fd in this semantic test.
Actual parsers, source association, both Ruby modes, all NuGet failure reasons,
zero-lookup assertions, source ordering, same-name identities and every numeric
assertion remain. NuGet already uses its own synthetic byte-reader seam. No product
reader, fallback, platform skip or CI matrix changes.

The mechanism matches Feature 005's 005-0021 incident, which reproduced
89 failures/eight errors from composed tests assuming successful real scoped reads.
Feature 006's earlier 006-0012 correction separated NuGet semantics from descriptor
capability too. This specific repeated coupling is directly supported by execution
paths and capability simulations, not merely by counting incidents. It supports
narrow test-method guidance, not a broad suite refactor or analyzer redesign.

Real filesystem witnesses remain in test_ruby_groups/test_nuget_input, portable
production refusal/composition witnesses in test_scoped_portability and NuGet
source tests, semantic composition here, and full supported CI in the unchanged
workflow. Missing capability skips only genuine filesystem witnesses.

Verification: focused NuGet mixed/Ruby groups/acceptance **44 PASS**; gate tests
**4 PASS**; full deterministic **640 PASS**, no skips on the capable local host;
full suite with dir_fd unavailable before discovery **640 PASS, 32 genuine
filesystem skips**. Actual corrected Windows status: **UNOBSERVED / EXPECTED
PASS**, pending separately authorized publication and Python 3.11–3.13 CI.
Prior worker PASS does not establish this repaired test's Windows PASS.

## C — GitLeaks historical synthetic fixtures

**HISTORICAL SYNTHETIC-FIXTURE SCANNER INTERACTION + LOCAL/HOSTED SCAN-SCOPE
MISMATCH; unresolved policy acknowledgment gap, not a known current credential.**

The earlier maintenance truthfully established a clean current tree and a single
finding in a restricted historical range. Neither meant full-history clearance.
Hosted detect scans historical additions; deleting/changing current strings does
not remove old additions. The supplied hosted 8.30.1 run scanned 199 commits,
about 2.80 MB, and rejected two findings. Local 8.30.1 with unchanged actual config,
hosted detect mode and default history scope reproduces both exact fingerprints:

```text
943d5de022a13103a2657a3be6b10f711565047a:specs/006-nuget-selected-evidence/reviews.md:generic-api-key:1557
8377163f6e8396c3f089a5cb54dc476d5bbff7fe:tests/test_nuget_registry.py:generic-api-key:491
```

Local before result: **exit 1, two findings, 256 commits, about 3.58 MB**. GitLeaks'
default `--all` includes available local refs; differing graphs explain why count
parity is not asserted. Mode/version/config/history semantics match; this is not
a byte-identical hosted checkout or new hosted observation.

Direct historical source inspection shows the test constructs a TransportFailure
with HTTP404, arbitrary diagnostic SECRET and body_limit bounded failure, using
an in-memory recording transport and asserting invalid_registry_response. The
review line quotes that expression as scanner evidence. Neither is a credential
source or authentication value; both are demonstrably synthetic test evidence,
with no known real credential involved. Current representation was already repaired
in bbc0703; historical evidence and Git history remain unchanged in this run.

### HUMAN SECURITY-POLICY DECISION — proposed, NOT installed

The narrow supported mechanism is a root `.gitleaksignore` containing ONLY the
two full four-component fingerprints above, with rationale comments. No baseline,
commit-wide, content-wide, path-wide, rule-wide or directory-wide allowlist.
GitLeaks 8.30.1 [documents fingerprints](https://github.com/gitleaks/gitleaks/blob/v8.30.1/README.md#gitleaksignore)
and [matches commit/file/rule/line exactly](https://github.com/gitleaks/gitleaks/blob/v8.30.1/detect/detect.go).
Do not use the three-component global fingerprint form.

Only an external temporary proposed-ignore file was passed explicitly during
experiments. Repository configuration, workflow and active ignore policy are
unchanged. Before/after experiment on real local history: **exit 1/two -> exit
0/zero**. That zero is CONDITIONAL ON THE UNAPPROVED EXPERIMENT, never the current
gate result. The actual policy remains **FAIL/two**.

An isolated temporary clone adds the same synthetic expression in new commits
in BOTH affected files and another path, plus a constructed fake token for the
separate github-pat rule. Before: **exit 1/six findings**. Proposed exact ignore:
**exit 1/four findings**. Set comparison proves ONLY the two historical fingerprints
are removed; new generic-api-key findings in both files/elsewhere and the other
rule remain detected. No real credential is used. The clone is never pushed.

Residual risk: fingerprints identify a commit/file/rule/start-line, not a digest
of one matched secret. Another same-rule finding on that exact historical line
would also be ignored; inspection establishes these two lines' synthetic content.
History is immutable here, but future scanner rules/line attribution or fingerprint
format could change. This feature is documented experimental upstream. Version
changes require reassessment and re-running negative controls, not broadening the
exception automatically. Future commits have different identities and remain
scanned. Human approval is required before adding any ignore file.

### Authorized pre-push tooling

`python3 tools/check_gitleaks.py` requires 8.30.1 and non-shallow history, uses the
actual config and hosted detect mode, redacts output and propagates scanner exit.
The command itself changes no scanner policy. Its local result is **FAIL/exit 1,
two historical findings**. See [pre-push checks](pre-push-checks.md) for refs/version
limits, offline tests and real negative-control procedure. Hosted action defaults
to latest, so version parity must be checked again before publication.
Actual hosted status remains the supplied **FAIL/two**; no clearance claimed.

## Methodology and remaining gates

SDD_WORKFLOW already covered validation, convergence, authority, review and
honest platform claims, but lacked an explicit obvious-human-invocation and
full-history pre-push/observed-post-publication operational closure check.
The narrow addition distinguishes convergence from operational closure, preserves
optional smoke/task dependencies and no-push authority, and links one durable
local checklist. No new feature lifecycle or broad test migration is introduced.

Remaining gates: human security decision on the exact historical acknowledgment;
human publication authorization; then actual supported OS/Python CI, explicit
worker steps, live PyPI and hosted GitLeaks evidence on the published candidate.
Discovery/listing implementation requires separate human product selection.
Until then the reviewed local maintenance can be ready while operational closure
remains pending. No target execution/modification, history rewrite, policy exception,
new feature, release/tag or push occurs.
