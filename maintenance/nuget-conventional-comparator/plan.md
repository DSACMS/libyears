# Comparator implementation plan — 006-0030

Governing spec4c67d0339e4aae4b730f471d99a039c8f8733dd8c82eff389f84a17a971bad32;
approval in reviews.md. No generic configuration or resolver framework.

## Policy primitive and repository reader (C1–C3)

New focused nuget_comparator.py: bounded existing _xml_pass framing with no project
grammar expansion, exact config grammar and per-section sequential operations,
closed-state flags and safe fixed decision codes. Validate whole files before
exposing any policy; support exact-ID/prefix/wildcard ranking and winner count.
Separate eligibility-only ambiguity (testimony may resolve) from private assignment,
unknown policy, active mapping ambiguity and supported conventional public default.
Inspect project tree for named source influences without evaluation; Restore*/NuGet*
and Import/Target/Choose deny policy. Unknown external SDK state is a limitation.

RepositoryNuGetReader.comparator_policy reads only its held root-to-project chain.
Bound os.scandir descriptor iteration, case-insensitive relevant filename collision,
Directory.Build.props/targets/Directory.Packages.props presence refusal. Config
reads O_NOFOLLOW/nonblocking regular file with identity/reparse/size checks before
and after, exact named entry recheck and held directory identities. Snapshot each
directory identity before enumeration and after reads to detect new/disappearing
policy input. No symlink following, imported input read, URL fetching or raw errors.
Unknown-safe policy returned on any refusal; parser I/O failure never masquerades
as no config. Existing native capability gate remains; no runtime Git.
Pure parser fixtures exercise semantics even without descriptor support; real
reader witnesses separately test native containment/mutation/case/budget behavior.

## Source, capability and output integration (C3–C5)

Read policy under existing scoped reader with exact project bytes. Only ordinary
anchored reader supplies policy; explicit precision passes none and keeps historical
behavior/output. Existing injected legacy source fixtures can explicitly inject
no policy to preserve their historical-route tests; new policy integration fixtures
inject actual policy objects and test all new semantics without native capabilities.

Ordinary A without selected witness may enter narrow route only with existing
repository_snapshot_population qualification and unique attribution. Keep original
A context/iteration and declaration_derived; set source trust_basis
repository_current_pair_policy and fixed population limitations. Do not create
SupplierContext. Unavailable qualification keeps known A N/whole unavailable.
Existing supplied witness route validates first and retains its population meaning.
B1/B2 population processing unchanged. After selection and complete whole admission,
apply policy per exact package/version, with exact matching testimony distinguished
from missing record. Unknown/private/mapping ambiguity cannot use testimony or
convention; eligibility ambiguity can use valid exact public testimony. Exact
private/unknown testimony refuses. Missing record can use valid mapping/convention.

Mint LocalAuthority from exact project/lock SHA256, safe selected identity and policy
basis, no content hash, local state unavailable. Extend authority/result codecs
with repository_mapping/conventional_public_policy only; enforce unavailable
origin/content/no digest for both. Keep endpoint/service/catalog validation, worker
batch/deadline/request budgets and scan join untouched. Existing adapter handles
hash-free policy capabilities identically to v2 date lookup; no registry shortcut.
Add ordinary comparator_basis and conventional comparator_limitations to NuGetEvidence
and serialization, set only when authorized; preserve through metadata failures.
Default human policy lines explicitly state assumed correspondence and uninspected
external config when applicable; new safe refusal messages. Existing testimony
measurement/namespace/assurance retain meaning, policy rows use distinct basis and
policy-selected snapshot wording, no accepted supplier snapshot claim. Schema3
additive, precision byte-shape stable, verbose JSON identical.

## Verification and operation (C6)

Sequential tasks K1 primitive/reader inert; K2 integration/output/codecs; K3 docs
and independent convergence; K4 baselined actual measurement and closure. Each
completed implementation task gets focused tests/diff/local commit. K2 integration
runs full deterministic/capability-disabled discovery/real-worker3. K3 convergence
fresh decomposed authority/config/testimony/private, A/B1/output/schema and registry/
worker/portability/verification reviewers, parent validates material findings.
No public OASim request before convergence. New25-case matrix maps to named tests.
Negative transport spies assert zero authority/HTTP; positive fixture metadata
passes real codecs/adapter then arithmetic. Existing sibling regressions unchanged.

After local convergence, create trusted temporary capture helper006-0030: Git
optional locks disabled, exact revision/full NUL porcelain/index, all tracked and
nonignored untracked bytes/modes/size/mtime, ignored name inventory and relevant
ignored policy/project/lock files. No target helper installation. Capture before
first target interpretation and require identical after. Run exact ordinary
python3 -m libyears target and --json, retain outputs/errors/exit; existing public
worker only for locally authorized capabilities. Guarded local-only staging records
per-source authority before metadata, independently report zero private/unknown
capabilities. No alternate endpoint request, package manager or target execution.
Report actual registry failures without invented fallback dates; existing-authority
bounded defects get correction, relevant checks and fresh closure before retry.
Current docs/ROADMAP/CHANGELOG checkpoint reflects actual result and limitations.
Canonical history GitLeaks, diff, final integrity and clean tree after commits;
external44-key handoff, no current row append/push. Hosted validation asynchronous.
