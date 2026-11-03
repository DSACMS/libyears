# npm SemVer ReDoS security maintenance

Classification: **SECURITY_DEFECT**. Rule: `py/redos`.
Baseline: `26fc59d`; repair commit: `a0553a7`; affected recognizer: `libyears/npm.py::_SEMVER_VERSION`.
This repository-level maintenance is independent of Features 005/006 and NuGet.

## Authority and root cause

Feature 002 [specification §14](../specs/002-npm-support/spec.md),
[plan: Stable Version Strategy](../specs/002-npm-support/plan.md), and
[T008](../specs/002-npm-support/tasks.md) authorize canonical concrete SemVer
classification. Commit `7b8450f` introduced the affected recognizer.
Registry version keys reach it through `_is_stable_version` before timestamp
filtering; a network timeout does not bound local regex work.

The nonnumeric prerelease branch was
`[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*`. Each `--` identifier has two ways
to place the required middle character. Choices multiply across dot-separated
identifiers when a later character forces rejection. The input
`"0.0.0-0." + "--." * n` ends in an invalid empty identifier. Parent probes,
each in a subprocess with a two-second guard, rejected at approximately
0.000055 / 0.000886 / 0.01398 / 0.21508 seconds for n=8/12/16/20.
These observations support the structural diagnosis, rather than defining a
performance contract. A single long hyphen identifier with a rejecting suffix
also admits quadratic work in the old branch. A completed prerelease, such as
`"0.0.0-0." + "--." * n + "end"`, is valid and must remain accepted.

## Repair and compatibility

Both nonnumeric branches now start `[0-9]*[A-Za-z-]`: the required letter or
hyphen is uniquely the first nondigit. Every previously accepted nonnumeric
identifier has exactly this decomposition. Pure numeric identifiers retain
their separate zero/positive-integer alternatives. Dots cannot be consumed by
identifier character classes; plus separates build metadata. Therefore a failing
suffix cannot multiply successful identifier decompositions. Failed digit-only
branches scan digits a bounded number of times. Matching work is linear in input
length, with no arbitrary length cap, atomic-engine dependency or suppression.

Core numbers still disallow leading zeros. Numeric prerelease identifiers still
disallow them, while `01a`, `00-`, standalone hyphens and dotted prereleases
remain valid. Build metadata permits leading zeros and hyphens. Empty components,
unsupported punctuation, Unicode characters, prefixes and whitespace still fail.
Capture group 1 is unchanged. Valid prereleases remain excluded from stable
selection; build-only versions remain eligible. Exact used-version lookup,
`_EXACT_VERSION`, snapshot/declaration behavior, publication ordering, metric and
schema are unchanged.

Parent differential validation compared original and repaired acceptance and
prerelease capture on 137,257 short suffixes over `01a-.+!` (length 0–6), with
no differences. This finite check supplements the decomposition argument.

## Durable regression and verification

`tests/test_npm_semver.py` covers explicit stable, prerelease, build and malformed
corpora; 3,110 generated prerelease/build cases against separate identifier rules;
and guarded subprocess probes at 8/16/32/128/1024 repeated attack segments.
Probes cover trailing dots, rejecting punctuation, long single identifiers,
valid repeated prereleases, 10,000-character valid numeric/build components and
long dotted build metadata. Acceptance/capture assertions are correctness oracles;
the ten-second subprocess timeout contains future regressions and is not a
matching-time target. Existing mocked npm registry and mixed scanning tests cover
ordinary behavior without network access.

Focused verification: `python -m unittest tests.test_npm_semver tests.test_npm
tests.test_npm_registry tests.test_yarn tests.test_mixed_scan` — **101 passed**.

Full deterministic suite: `python -m unittest discover -s tests` — **398 passed**.
`git diff --check` passed. Parent inspected the final product/test diff and
confirmed the two regex substitutions plus explanatory comment are the only
runtime changes. This documentation checkpoint also adds an Unreleased Security
entry to `CHANGELOG.md`.

Independent security review: **APPROVE**, complete, no material findings.
The reviewer verified both frozen hashes before/after review and ran 56 focused
npm tests. An in-memory restoration of both old fragments caused the actual
regression probe to hit its ten-second guard (`TimeoutExpired` after 10.004s);
`subprocess.run` killed and reaped the child. Additional guarded adversarial
families through 300,009 characters completed with the repaired recognizer.

Independent compatibility review: **APPROVE**, complete, no material findings.
The reviewer verified the frozen hashes, compared old/new acceptance and capture
on 274,514 bounded inputs without differences, and passed 144 tests across npm,
Yarn, mixed scanning, metrics and output. The parent reconciled both reviews
against source, contract, the frozen hashes and independently run verification.
No reviewer repair was required; no validated material findings remain.
Cross-platform CI and a fresh CodeQL run were not observed.

No existing safe documented local CodeQL execution mechanism was found in the
repository workflows or guidance. **CODEQL RECHECK PENDING**. The GitHub alert
has not been observed resolved. The next gate is a CodeQL run observing the
repair after a separately authorized push; this run does not push.

## Orchestration and observations

Two fresh read-only investigators completed independently:
`/root/investigator_a` (SemVer compatibility) and `/root/investigator_b`
(ReDoS mechanism). Both supported the same language-preserving structural repair.
The parent validated source/history, bounded reproduction and equivalence evidence
before editing. Investigator A also tested a different, single-identifier attack;
its polynomial behavior does not contradict the repeated-identifier exponential
reproduction.

The product/test candidate was frozen for two fresh non-author reviews:
`/root/reviewer_security` and `/root/reviewer_compatibility`.
Frozen SHA-256 values:

- `libyears/npm.py`: `5e8bde05b19285ba9a6fd2b218c9a0628b04c5730222e5718bba33c72c48a117`
- `tests/test_npm_semver.py`: `5e53e1d8b36328f9c7bf53213ef903f4ca887e9a9835033f5bcbc2cce7ac1706`

All four children were requested with `fork_turns="none"`, with no model or
reasoning-effort overrides. They received repository locations and their bounded
assignments, not sibling conclusions. Reviewers received frozen file hashes and
their review gates, not investigator verdicts. No sibling conclusions were shared
before completion. The security reviewer additionally received a request to
validate an in-memory reintroduction under a subprocess guard. Actual child
model/effort/version/resource telemetry was unavailable; requested settings do
not prove actual runtime configuration. The parent used the supplied task context
and fresh repository reads; no previous-session memory was used, and a context
reset cannot be independently attested through available telemetry.

`observations/README.md` defines Feature 005 IDs but no prospective maintenance
namespace. No ledger row or 005/006 ID was invented, and the 44-field schema and
ledger are unchanged. This artifact preserves the run. Recommendation for future
human approval: prospectively reserve `maint-0001`, `maint-0002`, etc., using
`feature=maintenance` and native children as parent orchestration details under
the existing schema. Do not retroactively encode this run as a prospective row.
