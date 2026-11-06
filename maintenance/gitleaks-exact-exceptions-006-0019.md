# Exact historical GitLeaks exceptions — 006-0019

Baseline: clean `b2e30bd92d32c7a4c746f0d886c6f2ae17a9ef1a`.
Observation 006-0018 is recorded separately in `c6bacb2` with human-supplied
/status enrichment; original runtime provenance/confounding is preserved.
This is post-convergence security maintenance, not Feature 007.

## Human decision and implementation

The commissioning human explicitly approved exactly two historical fingerprints:

```text
943d5de022a13103a2657a3be6b10f711565047a:specs/006-nuget-selected-evidence/reviews.md:generic-api-key:1557
8377163f6e8396c3f089a5cb54dc476d5bbff7fe:tests/test_nuget_registry.py:generic-api-key:491
```

The root `.gitleaksignore` uses GitLeaks' canonical four-component exact
fingerprint mechanism. Both findings are verified historical synthetic test/canary
material; neither is known to contain a real credential. Current representation
was already corrected. Rewriting history is disproportionate and prohibited.
Exact suppression retains detection of unrelated/new findings, as the 006-0018
controls and this run demonstrate. No additional fingerprints, path/directory,
rule, content-pattern or repository exclusions are authorized or installed.
The config, defaults, workflow, scanner version and canonical gate are unchanged.
Historical Feature 006 evidence is unchanged.

Fingerprints identify commit/file/rule/start-line rather than a secret digest;
these specific historical lines were inspected. Scanner upgrades or changed
fingerprint attribution require reassessment and new controls, never automatic
broadening. See the original [analysis](operational-smoke-006-0018.md) and
[review](operational-smoke-006-0018-review.md); their pending-policy statements
remain historical evidence, superseded only by this explicit decision.

## Verification

Local GitLeaks 8.30.1; canonical `python3 tools/check_gitleaks.py`: exit 0,
258 commits scanned, zero unsuppressed findings before the maintenance commit.
Full local history over available refs is used, not a restricted passing range.
Gate tests: **4 PASS**. Full deterministic suite: **640 PASS**, zero skips.
No application behavior, dependencies, filesystem handling or CI trust changes.

An isolated disposable clone commits the verified historical synthetic expression
in both formerly affected files and `synthetic-control.txt`, plus a constructed
fake token for `github-pat`. No real credential is used. Scan with the root ignore
absent: exit 1 / six findings. Scan with the exact candidate ignore: exit 1 / four
findings. Set comparison proves the removed findings equal exactly the two
approved historical fingerprints; all three new generic-api-key findings and
the separate github-pat finding remain detectable. Both files are checked
individually. The clone is never pushed.

An initial experimental comparison retained the automatic root ignore while
passing an empty external ignore file; both scans returned four findings, so its
six-to-four assertion correctly failed. It establishes no before-policy baseline.
The corrected experiment removes the clone's root ignore for the before scan
and restores the exact candidate for the after scan. Raw redacted reports, script,
set comparison and the initial attempt are retained outside Git in the run's
normal temporary evidence directory (`006-0019`). No repository control fixture
or scanner-policy weakening was needed.

## Review and publication boundary

The candidate is frozen by SHA256 before fresh non-author security review.
Review verdict and parent validation are recorded separately in
[gitleaks-exact-exceptions-006-0019-review.md](gitleaks-exact-exceptions-006-0019-review.md).
The freeze covers `.gitleaksignore` and this evidence; the already committed
observation is independently auditable. Review disposition adds no exception.

No history rewrite, push, force push, release/tag, Feature 007/Java work or OASim
access/execution/modification occurs. Local passing history does not establish
hosted success. Hosted GitLeaks: **UNVERIFIED after correction**. Windows:
**EXPECTED PASS / actual execution unobserved**. Next gate:
**HUMAN PRE-PUSH / PUBLICATION AUTHORIZATION**, followed by actual hosted evidence.
