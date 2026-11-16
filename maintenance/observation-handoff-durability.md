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
