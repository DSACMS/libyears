# Feature 006 real-root validation preparation — T015

**Preparation complete; live execution pending separate T016 authority.**
No target has been selected, accessed or produced. Discovery's OASim evidence
confers no access. This procedure grants no target, network, producer, trust,
push or release permission. K5 remains a mandatory predecessor for convergence.

## Established offline evidence

[Acceptance evidence](acceptance.md) reconciles all 36 criteria, 23 S6 reason
pairs, finite limits and retained correction witnesses. [Reviews](reviews.md)
records independent K1–K4 approval, including K2-M1 and K3-C1 closure. The latest
full deterministic suite passed **631 tests**; the NuGet suite passed **225**.
These are offline results, not live yield, hash-domain fitness or real-root proof.

Exact published `77d66b9` passed nine Windows/POSIX CI matrix jobs with explicit
worker lifecycle, offline-suite and whitespace steps. Relevant worker dependency
bytes remain unchanged. This does not claim Windows execution of later CLI tests
or safe local reading where required filesystem primitives are unavailable.
The separate hosted secret check remains failed, with a synthetic local finding
reproduced and the hosted full cause unavailable; no exception was applied.

## Authority required before T016

The commissioning human must identify and authorize:

- One exact existing directory, immediate selected `.csproj` filename and
  immediate supplied witness `.json` filename; root `packages.lock.json` is fixed.
  Explicit witness selection accepts its qualified producer/supplier assertions.
- Read-only scanner access and the byte-comparison boundary. Include the three
  selected inputs and any co-located supported sibling inputs that will be read.
  No ancestor, reference, cache, source-configuration or credential inspection.
- Required public metadata network access. NuGet uses only approved api.nuget.org
  metadata. Co-located Python/npm/Yarn/Ruby inputs retain their ordinary discovery
  and registry behavior; authorize those accesses too or identify a suitable
  already-existing root. Do not silently invent a new root or copy/modify inputs.
- An exact private evidence directory outside both the target and Git, plus the
  executing channel: authorized agent execution or an explicitly accepted human
  evidence handoff. Record which raw outputs the agent actually inspected.
- The trusted scanner checkout/commit and a host with required safe-reader
  primitives. Existing verified trust must work; this procedure permits no new
  credentials, CA/trust changes or TLS bypass. NuGet does not forward the explicit
  `--ca-bundle` flag to its worker.

No restore, install, resolution, dotnet/NuGet/MSBuild, SDK or target-code execution,
package archive/private-content fetch, witness production, source/hash-policy
workaround, other project or portfolio traversal is part of this authorization.
If required retained inputs are absent, stop and report that gap; do not create
them using a producer or fabricate assertions.

## Bounded execution after authorization

Run from the trusted scanner checkout, never from the target. Resolve the four
parameters below only from the human's authorization. The evidence directory must
already be separately authorized and prepared; never redirect outputs into the
target. Commands are POSIX-shell examples and have **not** been executed here.

```sh
: "${VALIDATION_ROOT:?exact authorized target directory required}"
: "${PROJECT_FILE:?authorized immediate project filename required}"
: "${WITNESS_FILE:?authorized immediate accepted witness filename required}"
: "${EVIDENCE_DIR:?authorized private evidence directory required}"
```

1. Record scanner commit, execution channel, authorized input boundary and safe
   logical context. Verify the selected snapshot can be read under existing safety
   policy. Keep paths, raw witnesses and input fingerprints private and outside Git.
2. Capture an exact before-manifest for the authorized inputs. The following block
   covers only the three NuGet inputs using the production scoped reader; it
   neither traverses references nor weakens safety for a hashing tool. Repeat it
   after the scans with `inputs-after.json` as the output argument.

```sh
python - "$VALIDATION_ROOT" "$PROJECT_FILE" "$WITNESS_FILE" \
  "$EVIDENCE_DIR/inputs-before.json" <<'PY'
import hashlib
import json
from pathlib import Path
import sys
from libyears.nuget_input import ScopedNuGetReader

root, project, witness, destination = sys.argv[1:]
manifest = {}
with ScopedNuGetReader(Path(root), project, witness) as reader:
    for name in (project, 'packages.lock.json', witness):
        data = reader.read(name).data
        manifest[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
Path(destination).write_text(json.dumps(manifest, sort_keys=True, indent=2) + '\n', encoding='utf-8')
PY
```

   Extend the manifest only for explicitly authorized sibling inputs with an
   approved safe read method, or accept a specifically identified human manifest.
   State exactly which bytes were compared. This three-file manifest alone is not
   a whole-tree invariance claim. Missing safe access keeps that comparison
   incomplete; do not replace it with timestamps, Git status or unsafe reads.
3. Perform at most these two read-only scans, retaining each exit status and
   separate stdout/stderr. No automatic rerun, alternate target or repair loop.

```sh
if python -m libyears "$VALIDATION_ROOT" --nuget-project "$PROJECT_FILE" \
  --nuget-provenance "$WITNESS_FILE" --json \
  > "$EVIDENCE_DIR/report.json" 2> "$EVIDENCE_DIR/json.stderr"; then
  printf '0\n' > "$EVIDENCE_DIR/json.exit"
else
  printf '%s\n' "$?" > "$EVIDENCE_DIR/json.exit"
fi

if python -m libyears "$VALIDATION_ROOT" --nuget-project "$PROJECT_FILE" \
  --nuget-provenance "$WITNESS_FILE" \
  > "$EVIDENCE_DIR/report.txt" 2> "$EVIDENCE_DIR/human.stderr"; then
  printf '0\n' > "$EVIDENCE_DIR/human.exit"
else
  printf '%s\n' "$?" > "$EVIDENCE_DIR/human.exit"
fi
```

   A completed source-error, empty or partial report exits0; usage/path exits1;
   unexpected worker/report failure exits2. Record rather than suppress failures.
   Package/metadata-scan budgets are 60/300 seconds per invocation, including index
   work and cancellation reserve; other sources/startup/OS scheduling are not a
   hard real-time whole-CLI promise. Do not fetch archives or change trust on failure.
4. Capture the after-manifest with the same method/boundary and compare byte counts
   and SHA256 values exactly. Investigate any difference without writing the target;
   external concurrent changes do not establish scanner mutation by themselves.
5. Inspect the actual raw safe reports and make the comparisons below. Record
   capture times: the two scans see current public metadata independently. A
   listing/publication-population change can explain differences; do not silently
   normalize responses or repeatedly scan until a desired result appears.

## Required comparison record

| Concern | Evidence to retain and compare |
|---|---|
| Context and scope | Selected safe project/witness names, literal framework, all supported explicit direct population including test/tool/analyzer/PrivateAssets; excluded references do not count. Match declarations, report rows and known/unknown N without inventing scope. |
| Selection | Safe declaration minimum and lock-requested text, unique Direct association, original/normalized selected identity and packages_lock source. A request mismatch claims no selection. No requirement-satisfaction or resolver claim. |
| Origin/content | Supplied-assertion trust basis and safe origin/hash states; local rejection causes no public namesake request. Public verified states require identity/SHA512 agreement. Keep raw hashes/origins/baseline out of public summaries. |
| Publication/latest | Identity-bound used/actual-greatest-listed-stable created dates, normalized UTC, listing flags and first-receipt basis. No published/commit/local-date or older-candidate fallback; selected unlisted/prerelease may measure. |
| Arithmetic | Independently recompute each measurable age as max(0, (latest-created minus used-created).total_seconds()) / (86400 * 365.25); check negative anomaly flags and exact zero for identical normalized identities. Verify measured-only totals/mean/median/max and S6 counts/coverage/nulls, including available sibling rows. |
| Human/JSON | Context, scope, requests/selections, authority/hash states, dates, reasons, identities and numeric facts agree. Distinguish unavailable, zero coverage and validated empty. Explain any observed metadata change between captures. |
| Privacy and invariance | Safe reports contain no raw XML/witness/hash/origin/baseline/private paths or exception bodies. Exact authorized before/after bytes match; qualify any uninspected boundary. |
| Yield and environment | Record discovered/measured counts and reason distribution, actual hash correspondence observed, unavailable claims and environmental failures. Do not infer universal signing/hash-domain fitness or complete publication history from one root. |

The independent arithmetic check uses captured safe timestamps, not new lookups.
No live result is prefilled. If a date/hash/scope claim cannot be inspected,
retain the missing obligation rather than claiming it passed. A useful-yield or
hash-domain failure cannot authorize weaker H3/H4, another feed, archive repair,
restoration or a newly selected target.

## Expected private evidence and K5 disposition

Retain authorized context/execution metadata; input-boundary before/after manifests;
raw safe JSON and human reports with stderr and exit statuses; the comparison
record with per-obligation PASS/FAIL/UNAVAILABLE; observed environment/live failures;
and exact artifact locations supplied to the reviewer. Mark execution and agent
inspection separately, including any accepted human attestation. Do not copy raw
witnesses, private root paths, fingerprints or sensitive metadata into public Git.

T016 records actual evidence completeness, findings and limitations. Missing target,
permission, safe inputs or required evidence keeps T016 pending/incomplete. A smoke
check or passing deterministic suite does not replace required real-root evidence.
K5 must explicitly disposition that evidence before T017/K6 convergence. Any newly
needed product/security/trust/target/producer decision returns to human authority.
T018 retrospective/roadmap work still requires its separate authorization.

**Current next gate: explicit T016 target/read/network/evidence-channel authority.**
No T016 execution, K5 disposition, T017/K6 convergence or T018 work has begun.
