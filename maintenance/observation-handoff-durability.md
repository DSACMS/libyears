# Local observation handoff durability — 007-0022

## Authority and bounded correction

Start: clean `7c1dd773ecb8bf1c85c2360cf906a739bace5867`. The human authorizes one
storage-class correction, exact migration of available `007-0021`, prior-run
observation reconciliation, independent review and one local commit. No product,
ecosystem, CLI-presentation, registry, TLS, schema-v3 or Feature 007 semantics change.
No network, private target, trust-material access or harness generalization.

Tracked authority and canonical observation history survived reboot; temporary
unreconciled batons did not reliably survive. Original `007-0014` remains lost and
must never be reconstructed. The later `007-0020` handoff was unavailable after
reboot too; that fact remains historical, not an invitation to reconstruct it.

## Contract

[The helper](../tools/observation_handoff.py) resolves the current checkout through
`git rev-parse --is-inside-work-tree --absolute-git-dir`, refuses bare repositories,
and locates `<resolved-git-dir>/libyears-harness/observations/`. This repository is
a normal working tree with a `.git` directory. Separate Git directories and linked
worktrees are tested; linked worktrees use their own Git directory, not the common
directory. A custom Git directory inside the worktree outside a reserved `.git`
component refuses before storage: Git otherwise exposes that metadata as untracked
content. State lasts only as long as that Git metadata; checkout removal/pruning,
disk loss and backup policy remain outside this correction.

The [observation protocol](../observations/README.md#local-handoff-and-authorized-append)
now distinguishes tracked canonical evidence, repository-associated noncanonical
working state and ephemeral `/tmp` scratch. No `.gitignore` or tracked marker is
needed. The `directory` command creates nothing; `write RUN_ID` accepts prepared
JSON from stdin or an optional file. Both ordinary writes and migration validate
the current 44 ordered keys and matching safe run identity. Duplicate keys refuse.
No values are invented. There is no ledger-write command or automatic reconciliation.

Writes use a human-readable JSON payload, an exclusive sibling temporary file,
flush/file-fsync/close and atomic `os.replace`. A failed replacement leaves an
existing final baton intact; cleanup removes the temporary sibling where possible.
Directory fsync, sudden-power-loss guarantees and concurrent-writer coordination
are explicitly out of scope. Use one writer per run ID. Ordinary reboot persistence
follows the selected filesystem storage class, not a simulated reboot experiment.

## Exact migration and separate reconciliation

The existing `007-0021` source parsed with all 44 expected keys and the correct run
identity. Only that available baton was migrated; no bulk migration occurred.
Source and destination SHA-256 are both:

`8d44d7d1704e252649f674f128b5ed42b5d05dfc336ca0e80eba999c04328447`

Destination: `<resolved-git-dir>/libyears-harness/observations/007-0021.json`.
The source remains at its actual historical `/tmp/libyears-observations/007-0021.json`
location, unchanged. Git status was identical before/after local-state creation;
`git ls-files` confirms no tracked destination. The initial sandbox denied Git-dir
writes; an explicit scoped helper escalation succeeded. This was an environment
permission boundary, not new storage/product policy authority.

As a separate authorized next-run recording action, `007-0021` was appended once
to the canonical ledger with supplied session/model/provider/effort/version,
reported runtime 769s and credits_after 155. The original fields/notes were retained
except authorized telemetry enrichment, with provenance appended in notes.
credits_before remains blank: no direct reading or explicit continuity supports it.
The original principal-artifact digest was verified before reconciliation.
All prior ledger bytes remain an exact prefix; 71 records, 44 columns, unique IDs.
Neither migration nor reconciliation altered either JSON copy. No `007-0014` or
`007-0020` row was fabricated. Historical temporary-path records remain unchanged.

The current run will write `007-0022.json` through the new helper before final
reporting, dogfooding the durable storage class. Its temporary prepared input is
recreatable scratch; its final baton is Git-directory local working state. Current
run telemetry unavailable to the agent remains blank. The current run is not
appended to the ledger by its own storage operation.

## Verification and review

Focused storage/tooling tests cover resolved Git paths, ordinary/separate/linked
layouts, bare-repository refusal, clean/untracked storage, atomic replacement and
failed replacement, JSON/identity/key validation, exact migration, missing-source
refusal, conflicting destination refusal, CLI dispatch, historical-reference and
canonical-ledger preservation. No workstation reboot is simulated.

Focused storage/security-tooling verification: **17 tests PASS**, including 13 new
storage tests and four existing GitLeaks gate tests. The final integrated suite
passes **1111 tests, one expected skip**. All 19 local links and
anchors in the three changed documents pass. Configured GitLeaks 8.30.1 scans 356
precommit history commits with zero findings; exact six-file current-content scan
also passes with zero findings. Whitespace checks pass.

One fresh non-author reviewer completed A durability/Git semantics, B observation
integrity and C scope/readability: **COMPLETE / APPROVE**, independently running
the initial 12 storage tests and verifying exact migration hashes, original artifact
digest, ledger-prefix preservation and permitted telemetry enrichment. A subsequent
author self-audit found the unprotected in-tree Git-dir case described above. The
bounded refusal/regression/docs correction received focused independent closure:
**COMPLETE / APPROVE**, all 13 storage tests independently passed, no further finding
or scope expansion. Final focused bookkeeping review also completed **COMPLETE /
APPROVE**, confirming corrected code/test digests, unchanged migration bytes and
ledger provenance. The current local handoff and final report record the single
commit, postcommit history gate and clean-tree boundary after current-run storage.

Canonical evidence remains the reviewed repository record and ledger; local batons
are working state and are not promoted wholesale into Git history.
The next consequential gate after convergence is human publication authority.
No push, tag, release, history rewrite or broader harness work is authorized.

## Hosted closure and publication actors — 007-0024

The earlier convergence and pending-publication statements above describe their
historical boundaries. Run `007-0023` subsequently published the converged work and
its one-file observation reconciliation as candidate
`899ca1f63cb57b984680dae245e8fbfe32aab75b`. Its original durable handoff validates
against the referenced repository ledger at that commit. The agent executed both
`git push github main:main` and `git push cms main:main`, then verified actual remote
refs against local HEAD. These execution/ref observations are retained separately
from later hosted results.

The initiating publication prompt remains accessible in the retained conversation.
It names `github` and `cms`, destination `main`, the converged `7c1dd77`/`4abe72f` set
plus only minimal observation bookkeeping, and required publication checks. Its
PUBLISH instruction states: “This prompt explicitly grants publication authority
for this bounded converged set.” This is retained initiating authority for that
specific publication, not retrospective authorization inferred from success.
The supplied transcript explicitly shows a one-time GitHub tool approval; that
technical permission is distinct from the initiating delegation. No broader or
standing authority follows from either. Original observation classifications and
runtime qualifications remain unchanged.

For this exact published candidate, the human now reports **all required hosted
CI/security checks GREEN**. This closes the hosted evidence boundary on
**human-observed evidence**, not agent verification. No attachment is accessible in
this session. The human also reports that the macOS log showed the exact candidate
checkout, three passing real-worker tests and 1,111 tests with one skip; those
individual log details remain attributed to that report, not an inspected log.
No workflow IDs, URLs, timings or Windows counts are supplied or inferred. Historical
local results and the original hosted-pending handoff are preserved.

The human's prospective policy is now canonical in
[Publication actors and delegation](../SDD_WORKFLOW.md#publication-actors-and-delegation),
linked by the pre-push guidance: agent preparation/verification/local commit,
human publication by default, with explicitly bounded agent delegation as an
exception. This policy does not silently normalize earlier agent pushes as the
default or reclassify the prior publication as unauthorized.

Run `007-0023` is reconciled once from its unchanged 44-key Git-directory baton,
with supplied telemetry and original notes/confounding retained. Its referenced
ledger digest was verified before append; all earlier ledger bytes remain an exact
prefix. The human's confirmed sequential continuity and the preceding recorded
credits_after 156 support credits_before 156 for that run; credits_after is 157.
No derived delta, invented reading, runtime subdivision or lost-baton reconstruction.
The ledger now has 73 unique records and 44 columns. Current `007-0024` is not appended.

This run changes documentation/observation bookkeeping only, with one fresh
non-author review and one coherent local commit after verification. No executable,
product contract, trust, target or CI configuration changes. No push is authorized
in this run. The next gate is **HUMAN PUBLICATION AUTHORITY** for this documentation
commit; the already-published candidate's human-observed hosted closure is separate.

Fresh non-author review completed **COMPLETE / APPROVE**, with no material finding.
The reviewer independently verified all four frozen file digests, original baton
and referenced baseline digest, exact ledger-prefix preservation, permitted
telemetry/continuity enrichment, historical actor/authority fidelity and scope.
Parent checks confirm 73 unique 44-column records, 18 local links/anchors and clean
whitespace. Configured GitLeaks 8.30.1 current-content and 358-commit precommit history
checks pass with zero findings. No product-suite rerun is required or claimed for
this documentation-only change. The final commit, postcommit history and durable
`007-0024` handoff verification are recorded in the local handoff and final report.
