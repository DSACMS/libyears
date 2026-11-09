# README architecture review and verification — 006-0034

## Scope and frozen candidates

Authority: bounded human documentation commission before Feature007;
[pre-edit migration map](readme-architecture.md). Starting clean/published
`0506861761b048e5e5a8d65a75d4c933d124df97` was confirmed against both remote
main refs read-only. This lifecycle starts after publication of the completed
Feature006 methodology retrospective. Neither its Feature Story nor its handoff
was rewritten. No Feature007, target-repository, registry or product work occurred.

Inventory commit: `eb3372c`. Initial migration candidate:
`31bce96198c02c6946ff86e83032823844e42dcc`. All original reviews inspected that
candidate directly against the starting README. Fresh non-author children used
`fork_turns=none`, without model/effort overrides; actual child resource telemetry
was unavailable. They received decomposed scopes and no sibling conclusions.
The parent validated findings and coverage; this is not approval by majority.

## Independent review dispositions

| Scope | Completed coverage / initial disposition | Findings and reconciliation |
| --- | --- | --- |
| A: first-time usability | COMPLETE / APPROVE | First command, setup, summary, options, limitations and navigation inspected; no material finding. |
| B: knowledge preservation | COMPLETE / APPROVE | All114 baseline non-heading blocks reconciled:98 whitespace-normalized verbatim,16 individually inspected. Original examples and link destinations retained; no material loss. Noted inherited contributor security contradiction. |
| C: ecosystem accuracy / one-guide coherence | COMPLETE / APPROVE | Inspected README/guide and relevant Features002–006 and NuGet corrections. Population, selection, comparator, assurance, dates and coverage distinctions supported. Suggested explicit testimony scope on the bound_snapshot_namespace paragraph. |
| D: normative boundary | COMPLETE / APPROVE | All six candidate files and relevant approved contracts reviewed. SPEC has exactly three navigation replacements; no requirements/history migrated into it and no product/schema/CLI change. |
| E: adopted OSPO / discoverability | COMPLETE / REVISE | Required README content substantive; governance properly links existing homes. CONTRIBUTING retained an inherited three-day response promise contradicted by SECURITY. Parent accepted finding and removed the duplicate promise in favor of canonical SECURITY guidance. |
| F: architecture / navigation / maintainability | COMPLETE / REVISE | Coherent front door + indexed single guide; no hierarchy needed, headings/backlinks valid. Five unheaded-block map locators were inaccurate; actual content retained. Parent accepted finding; explicit corrected locators now supersede frozen inventory rows. |

The parent independently found an additional example problem through an offline
CLI fixture: the illustrative summary inherited SPEC-style inline coverage, while
actual current output puts Coverage on its own line. README was corrected without
changing SPEC or runtime behavior. The parent also applied C's nonblocking scope
clarification; accepted-testimony rows now explicitly own bound_snapshot_namespace.

### Fresh correction review

Three-file correction freeze (over31bce96), independently verified before review:

| File | SHA-256 |
| --- | --- |
| README.md | 34e2dba552328bcf0a24c9c7af11a94184a90e9f388fdaaab89ac7a3022313cb |
| ECOSYSTEMS.md | 32bc247ce0789509bbc6c3e02a8c0cc8b75f349e5968592b75ea84066b1b1abb |
| CONTRIBUTING.md | 9858c0e1ac732742689402b4dffc84bcaccb712d20b05774e308a6355505bff0 |

Fresh non-author correction reviewer E: **COMPLETE / APPROVE**. Verified security
finding closure, confidentiality, continued Bugcrowd/HHS discovery through
SECURITY, substantive mandatory README content and no invented policy. Inspected
the output and NuGet corrections as collateral; no new contract/behavior change.

Fresh non-author correction reviewer A/C: **COMPLETE / APPROVE**. Reproduced exact
README summary with local format_human and the illustrative MetricSummary; ran
`python3 -m unittest tests.test_output`: **30 PASS**. Inspected implementation labels
to confirm testimony versus automatic measurement_basis. No first-use regression
or knowledge loss; security correction agrees with canonical unresolved policy.

Map locator correction is separately frozen at SHA-256
`816c395ef19d7d4325c2b0738c126e0838033dac71623586361f5db2218b9bdc`.
Fresh non-author F1 reviewer: **COMPLETE / APPROVE**. Independently verified all
five superseding locator rows against original README, preserved inventory history,
content/destination anchors, migration claims and every local map link including
this review record. No residual finding.

## Actual verification

- Initial and corrected local Markdown checks: **139 / 138 destinations and anchors,
  zero failures**, respectively, over README, guide, SPEC, CONTRIBUTING, Ruby
  retrospective and migration map at those checkpoints. Final expanded checks
  including this review record: **146 destinations/anchors, zero failures**.
- Repository Markdown backlinks to removed README anchors were searched. Two Ruby
  retrospective destinations were repaired (including a pre-existing mission
  anchor mismatch); no narrative changes. SPEC's three template/workflow pointers
  now reach the guide. No compatibility redirect hierarchy was needed for known
  repository consumers; unknown external old deep links cannot be verified.
- `python3 -m libyears --help`: **PASS**, no target scan/network.
- **21** documented libyears command forms parsed by the actual argument parser;
  placeholder targets/CA files and optional pip-freeze were not executed.
- Full guide Python-only JSON example exactly reproduced using temporary local
  requirements plus mocked PyPI metadata. README summary exactly reproduced from
  a synthetic2/3 CLI fixture. Socket creation was patched to fail, preventing
  network access. These are illustrative examples, not live release observations.
- The first temporary verification-script invocation needed the repository on
  PYTHONPATH; rerun succeeded. This was a check-harness path issue, not a product
  defect. The subsequent summary mismatch exposed the real documentation finding
  above, which was corrected and reverified.
- All **17** error-level README content rules from adopted repolinter.json match;
  file existence checked separately. Independent E checked substantive meanings,
  not merely strings. No package manager/repolinter installation or config change.
  This is a bounded documentation audit, not blanket maturity/outbound certification.
- `git diff --check`: **PASS** at inventory, candidate and corrected checkpoints.
- `python3 tools/check_gitleaks.py`: initial committed candidate **PASS**, GitLeaks
  8.30.1, complete configured history,328 commits, zero unsuppressed findings.
  Current proposed six documentation files additionally passed stdin scanning.
  No suppression/config/history changes. Final committed history is rechecked
  after the closure commit; actual final result is reported in the handoff.
- Changed repository paths are Markdown only; no runtime, tests, executable files,
  schema, CLI, CI or target files changed. No full product suite required or run.
  No live registry/target validation, package managers, OASim inspection/execution,
  Feature007, pushes, tags or history rewriting.

## Result and next gate

README is226 lines (previously921), with a short first command, interpretation,
ecosystem table, common options, limitations and substantive required project
sections. Size is descriptive; success is navigability plus preserved knowledge.
ECOSYSTEMS is940 lines including explanatory framing and navigation, not a new
normative source. Its length alone does not justify a docs/ hierarchy: common
questions and differences remain visible, with per-ecosystem/advanced NuGet anchors.
SPEC remains normative, with only destination changes. Governance remains in
COMMUNITY/CONTRIBUTING; no nonexistent GOVERNANCE policy was invented.

Meaningful deduplication: development instructions delegate to CONTRIBUTING;
security commitments delegate to SECURITY. Detailed ecosystem material moves to
its explanatory home; historical rationale stays in original artifacts. LICENSE
and policy files are unchanged. No material knowledge loss was found across the
assigned independent scopes and fresh correction checks.

Exact next human gate: accept or revise this documentation architecture and local
candidate, and separately authorize publication if desired. Feature007 remains
unstarted and still requires separate roadmap selection and bounded authorization.
This review grants neither publication nor next-feature authority.
