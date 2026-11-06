# GitLeaks synthetic-fixture maintenance

Queued maintenance authorized after Feature006 retrospective approval, executed
in run006-0017 after T018 at657e8a9 and separate table maintenance atf7d27e8.
No scanner policy/trust change, suppression, allowlist or history rewrite is permitted.

## Classification before changes

Existing local Gitleaks8.30.1, explicit unchanged `.github/.gitleaks.toml`, fully
redacted output and exact Git range221f048..77d66b9 reproduce one generic-api-key
finding at8377163, tests/test_nuget_registry.py:491. Direct source/provenance
inspection establishes synthetic TransportFailure arguments, not a credential.
The corresponding current file scan reproduces one finding at line619 before
editing. This matches the earlier recorded local interaction; it does not establish
the hosted scanner's resolved version/range or entire failure cause.

The bounded404 regression distinguishes malformed/limited response evidence from
ordinary package absence. Its diagnostic string is arbitrary; the assertion tests
invalid_registry_response, not that string's spelling. The independent privacy
canaries and their non-disclosure assertions remain untouched.

## Bounded representation correction

Change only that fixture's diagnostic to the obvious text `synthetic diagnostic`.
Status404, body-limit classification, transport/client path and expected invalid
response assertion remain unchanged. No production code or security test is removed
or weakened. The local current-file scan then exits0 with no finding.

A fully redacted whole-working-tree scan additionally identifies the historical
review paragraph's verbatim quotation of the same synthetic expression. That
quotation is rendered as prose listing the same arguments; original code remains
inspectable at8377163 with its exact recorded fingerprint. Review outcomes, findings,
chronology, counts and authority are unchanged. This is the same narrow fixture
representation in documentation, not an exception or erasure of the historical
scanner failure. A subsequent whole-working-tree scan exits0/no findings.

Commands use `gitleaks git . --config .github/.gitleaks.toml` with the explicit
historical range, or `gitleaks dir` on the current file/tree, always `--redact=100`,
`--no-banner`, `--no-color` and JSON reports outside Git. No baseline/ignore/allow
option is introduced. Exact commands, redacted reports/logs and freeze are retained
under `/tmp/libyears-observations/006-0017`. Scanner configuration and workflow
retain their baseline bytes.

## Verification and freeze

Focused registry/acceptance/CLI/output tests: **74 PASS**. A parent in-memory
transport mutation strips only the bounded-failure flag: the exact regression
then fails once, with package_not_found instead of invalid_registry_response,
zero errors. Thus its discriminating behavior survives the diagnostic edit.
The first mutation invocation named the wrong test class and a subsequent factory
patch disturbed type checks; corrected transport-return mutation provides the
actual evidence, without changing repository bytes or assertions.

Full deterministic suite: **636 PASS**. Independent disposition belongs in the
[review record](gitleaks-synthetic-canary-review.md).
The test file and review-paragraph bytes are frozen by the separately retained
SHA256 manifest before fresh non-author review. No new live-registry/platform
validation, hosted clearance, push, release or next feature is claimed. Historical
Git findings remain in unchanged history and may still be reported by scans that
include those commits; local working-tree cleanliness is a different claim.
