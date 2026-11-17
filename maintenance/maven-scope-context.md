# Captured Maven scope context — 007-0032

## Result

**Historical correspondence established for the eight relevant POM inputs. No
implementation defect established; no localized correction is justified.**
The captured context reproduces all 127 historical local-fact rows. It explains
all 39 scope refusals: every consumer omits scope, and missing external management
prevents a compile default under the approved contract.

The prior [scope diagnosis](maven-scope-evidence.md) correctly preserved uncertainty
when snapshots were unavailable. This record supplies the missing context without
rewriting that history, the [yield audit](maven-yield-audit.md), or the original
40-occurrence / 10-comparison / 9.29860822749512-libyear measurement evidence.
No new age, complete denominator, coverage or Observed evidence is produced.

## Correspondence and capture

Starting libyears HEAD: `27beec5a1016440e54099985437ceb5ad2a89507`, clean.
The exact previously validated public CMSgov/ab2d location was recovered from the
original durable capture procedure, without searching other directories.
Target identity is public CMSgov/ab2d, revision
`9c785d41da3f7dd72f5be62cfc42ee7b1bf74459`, branch main, clean before/after.
Only seven affected child POMs plus their contained root `pom.xml` were read.
The root explicitly selects an external parent, so no additional local POM is
needed or followed. No remote parent/BOM, trust input or workstation configuration
was read; Git checks disabled ambient configuration/includes and execution routes.
Only target-local Git metadata was used for identity/routing safety and status.

All eight byte digests, revision, index entries, status and available historical
mode/size/mtime/inode fields match the original `007-0028/before.json`. Original
device/ctime values were not retained and are not invented. Current before/after
full input identities and bytes also match. This establishes correspondence for
these model inputs, not whole-filesystem immutability or a fresh source-policy,
transport or registry validation.

Capture uses the repository's no-follow, identity-checked `MavenInputReader`,
registered only for the eight authorized relative paths, with its XML/byte
limits. No whole-checkout discovery or target scripts/build tools ran. Offline
replay uses the original eight-source incomplete-discovery state and the unchanged
[model implementation](../libyears/maven_project.py); 127 exact keys, artifact
identities, scope/optional values, version requests/facts and field origins match
the original JSON. Historical ages are neither substituted nor recomputed here.

Let `D` be the directory resolved by `python3 tools/observation_handoff.py directory`.
Private durable evidence is under `D/007-0032/`:

| Record | Purpose |
| --- | --- |
| `target-reference.json`, `before.json`, `after.json` | Exact authorized location/public identity, revision/branch/status/index and inspected-file identities/digests |
| `snapshots/` | Eight original-byte POM snapshots; private, not tracked |
| `correspondence.json` | Per-input comparison with original retained digests and available identities |
| `scope-trace.json` | All 39 exact occurrence keys, raw/merged/selected facts, context flags, cause and admission-gate results |
| Capture/trace procedures | Reproducible bounded read procedure and offline instrumentation; no runtime modification |

Original `D/007-0028/` evidence remains unchanged. Raw snapshots, absolute local
paths and comparison details remain private. Reviewers inspect these captures
directly; public tables below retain only necessary package/model facts.

## Precise upstream uncertainty

Each child inherits the local root model. Its root parent is explicitly external:
`org.springframework.boot:spring-boot-starter-parent:4.1.1`, with empty
`relativePath`. `_resolve_model` records `pom.xml: external_parent`, leaves the
parent chain incomplete, and propagates that fact to every affected child.
`_fact_context` consequently initializes `imports_unknown=True`.

The root also declares these actual dependency-management imports:

| Source | Imported BOM | Supported local version fact |
| --- | --- | --- |
| pom.xml | io.awspring.cloud:spring-cloud-aws-dependencies | 4.1.1 |
| pom.xml | tools.jackson:jackson-bom | 3.2.3 |
| pom.xml | io.opentelemetry:opentelemetry-bom | 1.66.0 |

Each has literal scope `import` and type `pom`; its unread contents independently
retain `imports_unknown=True` in every affected consumer. Their version facts do
not reveal managed scope. These three imports and the external parent overlap
across the **same 39 occurrences**; they are not four additive populations.
Removing only one source of uncertainty would not establish absence of management.

For all 39, the captured graph shows `management_unknown=False`,
`unknown_profile=False`, no property uncertainty, no blocked properties, no direct
or managed field variants, and no ambiguous ordinary/management keys. None of the
eight POMs contains profiles. Thus malformed management, profile conflicts and
blocked-key fallback are not the observed causes. The uncertainty is **known
unread external context**, not an unrecognized local syntax or lost scope field.

## Disjoint selection paths and occurrence mapping

Every affected requirement is present directly in its consuming child POM; none
of these 39 is inherited as an ordinary dependency. All 39 omit scope in both raw
consumer and merged ordinary records: no explicit empty/literal/computed scope
was discarded. Versions comprise 10 literals and 29 supported property-expanded
facts. Artifact identity and optional=false survive independently.

| Path | Occurrences | Exact selection behavior |
| --- | ---: | --- |
| A | 38 | No matching exact model-key management entry. Scope is omitted; compile default is withheld because imports/parent management remain unknown. |
| B | 1 (R18) | Ordinary type=pom dependency matches the inherited AWS BOM-import management entry. `_selected_field` rejects that entry as non-ordinary management, then withholds compile for the same global uncertainty. |
| Total | 39 | Null selected scope → `maven_unsupported_model` → no capability/work for the occurrence. |

This is a disjoint partition by local selection path, not an additive count of
the overlapping upstream uncertainty sources. R18 is an **ordinary project
dependency**, not itself a BOM import. The separate management declaration is the
actual import. Model key type/classifier participate in the exact match.

The R labels refer to the complete key/version/type table in
[007-0031](maven-scope-evidence.md#all-retained-occurrences), preserved in original
JSON order. `scope-trace.json` separately retains each full key in this run.
All contexts are `base_model`, classifier absent; R18 is type pom, others jar.

| Consumer source | Path A audit IDs | Count A | Path B audit IDs | Count B |
| --- | --- | ---: | --- | ---: |
| api/pom.xml | R01–R09 | 9 | — | 0 |
| common/pom.xml | R10–R17, R19–R23 | 13 | R18 | 1 |
| coverage/pom.xml | R24 | 1 | — | 0 |
| e2e-bfd-test/pom.xml | R25–R27 | 3 | — | 0 |
| e2e-test/pom.xml | R28–R30 | 3 | — | 0 |
| job/pom.xml | R31 | 1 | — | 0 |
| worker/pom.xml | R32–R39 | 8 | — | 0 |
| Total | | 38 | | 1 |

The matched historical bytes and exact local-fact replay resolve the former
original-context gap for all 39. None now falls into historical noncorrespondence
or unresolved-local-cause categories. All are correctly refused under the
supported contract; external parent/BOM contents are intentionally outside the
initial intake. Those descriptions overlap and must not be summed. There are
zero established implementation inconsistencies and zero newly supported rows.
The actual external managed scopes remain unknown; this diagnosis does not claim
to know what Maven evaluation or those unread BOMs would supply.

## Contract, sibling safety and next action

[S3](../specs/007-maven-dependency-age/spec.md#s3--maven-population-and-bounded-local-model)
requires inheritance/management before defaults, refuses compile across unknown
management, and excludes parent/BOM content intake initially. The existing
[plan](../specs/007-maven-dependency-age/plan.md) and
[normative source policy](../specs/007-maven-dependency-age/source-policy.md) preserve
this boundary. Known versions and ordinary type=pom dependencies do not bypass it.
No new upstream research or product-policy reinterpretation is needed.

Offline admission instrumentation injects a permissive synthetic source-policy
result solely to test the **scope gate upper bound**, without reading any source
configuration. Even then all 39 lack work, while the original 42 scope-ready
occurrence keys survive unchanged, including independent safe siblings. This is
not a revalidation of source policy or authority for current registry requests.
No metadata worker, retained-date reuse or age calculation is invoked. A Python
audit guard rejects socket/subprocess activity during offline tracing.

**Do not implement a scope-default repair.** The diagnosis is expected refusal,
not a parser bug. If higher measurement yield is required, the next bounded step
is a separate product-scope decision about whether to investigate supported
external-management evidence intake. Current authority does not permit fetching
parents/BOMs, widening parsing/evaluation, editing the target or relaxing the guard.
Another trust/live run cannot provide the missing local model facts under the
current intake. Until separate product work is selected, retain these refusals
and the useful historical measured slice.

Original durable `007-0031` validates against its completion artifact and is
reconciled once with supplied run-level 720-second telemetry, confirmed before164
and after166 account readings. Original notes/runtime qualifications and earlier
ledger bytes remain unchanged; 81 unique 44-column rows, current `007-0032` absent.
Review/check/commit disposition follows after completion.

## Review and closure

Two fresh independent scopes completed **COMPLETE / APPROVE, no material
findings**: historical causality/contract and admission/sibling/sensitivity.
Both inspected the captured evidence directly and independently reproduced the
local-fact/trace checks. They used no network, fresh target reads, trust input or
workstation configuration. Parent synthesis validates both reports. New child
contexts, no overrides requested; actual child settings/resources are unobserved.

Checks pass: eight original byte/revision/available-identity bindings, current
inspected-input integrity, 127-row local-fact replay, exact 39-key mapping and
38/1 partition, 16 local links/anchors across the companion and scope record,
ledger prefix/shape/uniqueness, manual sensitivity inspection and whitespace.
Configured GitLeaks current-content and full-history gates pass; final commit,
history count and clean-tree state are retained in the durable handoff. No
executable files changed; no full product-suite rerun is needed or performed.
The bounded diagnosis stops here: no implementation, policy relaxation, live
measurement, push, tag or release.
