# Synthetic NuGet evidence fixtures

These fixtures are hand-authored offline examples, never outputs of a restore,
package manager, SDK, producer or external target. They do not establish real
package origin, archive hashes, SDK compatibility or public publication dates.
`lock-v1.json` exercises whole-lock closure framing independently of association.

`Witness.csproj`, `witness-lock-v1.json` and `witness-v1.json` form one synthetic
byte-bound snapshot. The differently named lock fixture is supplied directly to
the parser tests; a real selected scan reads only `packages.lock.json`. The hash
is base64 encoding of bytes 0 through 63, not a hash of an actual archive. The
witness's SHA-256 fields bind the exact fixture bytes, including final newlines.
No file found by convention confers witness acceptance: only an explicitly
selected witness may be supplied to the provenance parser.

The version-1 witness is a strict UTF-8 JSON object with required `version`,
`project`, `framework`, `project_sha256`, `lock_sha256`, `producer`,
`coherent_snapshot`, `baseline` and `packages` fields. Version is integer 1,
not a boolean. Digests are 64 lowercase hex characters. Producer has required
nonempty `name` and `version` strings. The coherence field is a boolean.

Baseline requires nonempty `sdk` and `sdk_version` strings and four booleans:
`explicit_population_complete`, `unsupported_membership_version_influences`,
`unsupported_framework_rid_influences`, and `unsupported_source_influences`.
These assertions cover relevant imported, generated, ancestor and central
inputs, including implicit SDK behavior. They claim that supported explicit
declarations are the complete population and that those inputs introduce no
unsupported membership/version, framework/RID or source influence. The SDK must
match the project's literal Sdk assertion. No SDK or imported file is loaded.
SDK version and producer identity are supplier assertions, not independently
verified observations. Complete population must be true and all three influence
flags false. Unsupported influences or incomplete population invalidate the
discovery denominator; malformed witness or failed context binding merely leave
an independently discovered declaration population unavailable for measurement.

Each package object has required `id` and supported selected `version` strings,
plus optional `content_hash` string and `origins` array of strings. Omitted hash
or origin is attributable to that identity and fails its local authority gate.
Present nonstring hashes or malformed origin containers reject the whole
witness. Duplicate fields and unknown fields at every level are rejected.
Case-insensitive ID plus normalized version must be unique; normalization ignores
build labels, folds prerelease case, and handles supported numeric normalization.
Unselected/transitive records require the same framing but need not claim public
origin or have a usable content hash. They never confer measurement authority.

Only a matching package record with exactly one origin string equal to
`https://api.nuget.org/v3/index.json`, together with lock/witness hashes decoding
as strict standard base64 to the same 64-byte SHA-512 value, constructs local
lookup authority. Missing/private/alternate/conflicting origins cannot authorize
a public namesake lookup. Blanket public flags, source lists/mappings, caches,
configuration, ID/version coincidence and hash coincidence alone cannot confer
origin authority. Local agreement accepts supplier testimony; public content
correspondence still requires the later public catalog identity/hash checks.

Raw origin strings, hashes, fingerprints and baseline/producer details stay in
internal records. Public evidence exposes only safe states and selected identity
facts. Tests perform no registry requests and use guards around the authority
boundary to ensure rejected packages never reach an adapter.

`registry-public.json` is a synthetic URL-to-document map containing a SemVer-2
service-index resource, an inline registration page, and two catalog
PackageDetails leaves. Its content hash encodes repeated `x` bytes, not package
archive content. The intentionally private packageContent canary must never be
fetched. The deliberately different created, published and commit timestamps
show that only catalog created supplies first-receipt dates. Test builders derive
small malformed, missing, alias, paged and reordered variants without network.

`registry-reason-triggers.json` extends the mechanically checked local S6 table
with every public-registry dependency reason, including bounded response errors
versus transport/budget failures. `test_nuget_registry.py` tests this table and
composes the real byte client and lookup handler with the supervisor's injected
process controller and bounded protocol. Absolute blocking/cancellation and real
OS lifecycle witnesses remain in `test_nuget_worker.py`; no package manager,
producer, live NuGet service or external project is used.

`test_nuget_acceptance.py` generates exact byte-bound variants and offline
multi-package registration/catalog maps from these same synthetic assertions.
It composes the public CLI, local parsers, actual metadata handler, typed result
protocol, metric and both renderers, with forbidden I/O/process/network guards
and before/after target-byte comparisons. A separate supported-host test uses
the real descriptor reader; portable semantic tests retain the bounded byte
seam and never imply unavailable filesystem primitives are safe. Existing
controller/mutation/real-worker tests remain the cancellation evidence.

The acceptance reason enumeration derives `(level, reason)` directly from S6
and checks exact equality with the union of both trigger tables; each table's
own executable test reaches every listed reason. The complete AC, limit,
privacy, ordering and platform evidence reconciliation lives in
`specs/006-nuget-selected-evidence/acceptance.md`.
