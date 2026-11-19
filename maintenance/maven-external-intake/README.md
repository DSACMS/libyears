# Explicit external Maven management

Use `python3 -m libyears ROOT --maven-management accepted-management.json --json`.
The option explicitly accepts the embedded parent/BOM representations for the
listed byte-bound consumer contexts and exact field keys. It can supply missing
Declared scope facts and genuinely absent ordinary Declared versions; it does not establish an effective POM, successful build,
historical resolution, runtime selection, complete population or acquisition.
No evidence is discovered or downloaded automatically.

The UTF-8 JSON envelope contains exactly:

```json
{
  "schema_version": 1,
  "basis": "restricted_static_maven_3_9_11_v1",
  "documents": [{
    "gav": ["example.parent", "parent", "1.0"],
    "roles": ["parent"],
    "sha256": "<64 lowercase hexadecimal characters over exact POM bytes>",
    "content_base64": "<strict base64 of those same bytes>"
  }],
  "consumers": [{
    "source_id": "module/pom.xml",
    "context_id": "base_model",
    "bindings": {
      "module/pom.xml": "<SHA256 of exact consumer bytes>",
      "pom.xml": "<SHA256 of exact participating local parent bytes>"
    },
    "keys": [{"group_id": "example", "artifact_id": "library", "type": "jar", "classifier": null}]
  }]
}
```

The placeholders above must be replaced with actual hashes/base64. Roles may be
`parent`, `bom` or both. Each GAV and source occurs once. Bind every local ancestor
visited by the proof; accept every required external parent explicitly. Referenced
BOMs require the `bom` role. Coordinates, file presence or public origin alone do
not establish applicability. Supply only documents/context assumptions you accept.
Keep real envelopes private when they contain private model details.

Composition uses Maven 3.9.11 whole-entry management dominance, ordered imports,
raw-parent consumer interpolation and independent BOM interpolation. Missing scope
normalizes to compile only after applicable uncertainty is discharged for that
exact key. Unknown earlier imports block; unknown later imports cannot replace a
proven winning key. Same-key ordinary inheritance collisions, relevant profile
writes, unsupported syntax, missing/changed bindings, cycles and budgets refuse.
Other rows and existing local behavior survive. Limits: 4 MiB envelope, 64 documents,
2 MiB decoded aggregate, existing per-POM XML limits, 100 consumers, 10000 total keys,
16-deep lineages/import recursion and bounded per-row/scan proof work.

The file must be a safe regular file with no symlink ancestors. Unsupported safe
filesystem primitives refuse. Invalid envelopes produce a fixed request error.
A refused field proof retains the existing row and reports `management_status`.
Accepted rows disclose `scope_basis=accepted_external_management_static_v1` and
fixed limitations. Scope admission and public age comparison are separate: existing
repository policy still applies; external-parent repository policy conservatively
withholds comparison. Imported BOM repositories never grant consumer authority.
Observed remains unavailable and coverage can remain unknown.

Managed versions require a single ordinary declaration with no version field.
Explicit versions remain unchanged; empty, malformed, unresolved or unsupported
ordinary versions cannot be repaired. A whole winning exact management key must
supply a supported exact version; missing/invalid winning fields never fall back.
The supplied version is a static Declared request fact, not a resolved/installed
or Observed selection. Management-only entries create no dependencies.

JSON adds `version_management_status` separately from the existing scope-only
`management_status`. A successful Declared fact has `managed_version`: the original
managed request, winning local source or external document GAV, verified local
lineage sources, visited accepted GAVs, applicability basis and fixed limitations.
Existing ordinary request/origins/version_basis retain their meanings. Verbose
shows the managed origin even if later metadata or policy refuses an age. Scope,
version and age availability remain separate. The concise ordinary tables still
show every retained unmeasurable occurrence and its reason. See the
[007-0043 validation](validation.md#managed-declared-version-yield--007-0043).
