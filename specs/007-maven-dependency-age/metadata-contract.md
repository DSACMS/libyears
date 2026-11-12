# Feature 007 bounded public metadata contract

This is a normative companion to [S7](spec.md#s7--maven-comparator-evidence-cascade-and-conventional-time-basis),
not authority to contact targets now. It completes transport/date details for the
already selected conventional claim. Local refusal always precedes public I/O.

## Destinations and input authority

Only `https://repo.maven.apache.org:443` at `/maven2/` is a network destination.
Construct GA metadata and exact GAV POM paths locally from admitted case-sensitive
coordinate/version components under [local input bounds](source-policy.md).
Group dots become path separators; quote each artifact/version path component
without interpreting percent escapes, queries, slashes or user-supplied URLs.
Only these two representations may be fetched: GA `maven-metadata.xml` and
`GROUP/ARTIFACT/VERSION/ARTIFACT-VERSION.pom`. No archive, dependency/parent/BOM
POM, directory listing, Search/index/provider or private/alternate endpoint.
The POM being dated is a metadata representation, not a fetched transitive model.

A capability contains only an already admitted group, artifact and independently
admitted measured exact version; no target root, path, XML, source URL, settings,
credentials or executable name. Parent keeps occurrence-to-capability associations.
Worker revalidates every capability against the closed lexical grammar. It cannot
upgrade source authority after a namesake response. Cache only after admission;
a denied sibling occurrence cannot borrow another occurrence's accepted capability.

Require verified TLS and the existing explicit `--ca-bundle` trust override when
supplied; otherwise standard system trust. No insecure mode. The parent validates
and stages only the explicitly supplied CA material in private worker storage;
no host/user Maven trust/configuration lookup. Disable proxy discovery, ambient
HTTP auth/netrc, cookies, environment redirects and target-directed URLs. Do not
forward credentials or consult environment CA/proxy variables. Reject **all HTTP
redirects** rather than following them, including same-host redirects. DNS/TLS/
transport/status errors are sanitized unavailable evidence, not alternate routes.
Use GET with `Accept-Encoding: identity`; reject compressed/unsupported content
encodings. No retry loop, conditional/304/date fallback or HEAD-to-GET cascade.

## Whole responses, identity and dates

A successful HTTP200 whole-body GET is required. Enforce header/body/time budgets
while streaming; Content-Length does not replace actual-byte counting. A short
body, mismatching advertised length, unsafe XML, unsupported encoding or response
shape rejects that representation. Never use Last-Modified on a non200 response.
Metadata/POM XML obey the common safe XML rules and response-specific limits below.

GA metadata must be a metadata root (no namespace or exactly `http://maven.apache.org/METADATA/1.1.0`
under the [versioned schema](https://maven.apache.org/xsd/repository-metadata-1.1.0.xsd)), with one exact groupId/artifactId pair, one versioning and one versions
list. Every version entry is safe exact text under the local/version bounds;
duplicate singleton fields, selectors/ranges, truncated lists and overages make
the entire catalogue unavailable. Byte-identical version entries collapse only for
selection, not into normalized repository spellings. Ignore lastUpdated/latest/
release for selection and date; they cannot rescue an absent versions list.
Retain retrieval UTC time as freshness, not version time. No persistent historical
catalogue or all-ever completeness claim is introduced.

The versioned POM must be a well-framed project in the supported POM namespace.
Use only its top-level identity and distributionManagement/relocation to validate
the representation being dated; do not evaluate its dependencies/properties/parents.
ArtifactId must be one literal exact expected value. Group/version must be exact
literal expected values either directly, or from a literal immediate parent field
when the project omits that field. Do not fetch the parent. Unresolved identity,
known mismatch, duplicate relevant fields or any relocation leaves that date
unavailable. This is conservative representation association, not acquired-content
proof. Unknown unrelated build/dependency syntax is not evaluated or recursively
followed, and does not itself change a valid identity.

Require exactly one Last-Modified value in IMF-fixdate form (HTTP weekday, Gregorian
date, seconds, GMT); reject malformed/impossible dates, timezone-free values,
conflicting/duplicate headers or dates later than retrieval UTC time. Normalize to
aware UTC without adding precision. A narrower accepted HTTP-date grammar is
intentional; missing legacy syntax yields unavailable evidence. Response Date,
server filesystem time and local retrieval time never supply a replacement.

Select the unique eligible maximum **before** requesting its POM date. If that date
or the measured date fails, affected ages are unavailable. No older candidate or
other field replaces it. Same exact version needs one admitted shared date and then
produces exactly0.0. Distinct comparison-equivalent strings never share dates by
normalization. A successful current catalogue need not contain the measured version
if its exact supported POM/date is independently available; absence does not prove
never-publication/private origin. Ordinary arithmetic/anomaly flags remain in S1/S7.

## Fixed budgets and isolation

| Boundary | Limit / exhaustion |
| --- | --- |
| One GA catalogue | 2MiB body; 10,000 version entries before duplicate collapse |
| One public POM | 1MiB body; common safe XML structural limits |
| One version | 256 ASCII characters; 128 digits per numeric segment; 128 parsed items/nesting levels; inability to reproduce pinned ordering within limits refuses catalogue maximum |
| One response | 64KiB total headers; 100 header fields; 10 seconds including DNS/connect/TLS/headers/body; body cap remains active without Content-Length |
| One GA across repeated commands | 60 seconds wall time, including its catalogue and all POM dates |
| One scan Maven batch | 300 seconds wall time; 300 GET attempts; 64MiB total response bodies; zero retries/redirects |
| Worker command/result | 16KiB per atomic message, one measured GA/version command; bounded sanitized result, no raw catalogue/XML/header/error body |
| Startup / cleanup | 10 seconds readiness; 0.5-second bounded termination/reap attempt; unreaped worker stops further Maven network work |

Use one trusted installed **isolated Python metadata worker** for the scan, with a
parent supervisor enforcing wall deadlines even during blocked DNS/reads. No Java,
Maven/Gradle/target code, target working directory or import/PYTHONPATH injection.
Revalidate result shape, exact requested identity, dates, finite numbers, closed
basis/reason values and command sequence in the parent. Invalid protocol stops the
worker and refuses dependent results; no synchronous fallback. Missing required
safe process/filesystem primitives refuses Maven I/O with a capability reason.

Only bounded per-scan memory caching is selected: one accepted catalogue/target
result per exact GA and one date result per exact GAV. Bound cached bytes by the
scan input budget; preserve individual occurrence identity/weighting. Failed results
may be reused as failures, never as admission. Account elapsed GA/scan time across
cache hits and commands; budgets never reset per module. Sort commands by GA,
measured version and occurrence identity for deterministic budget attribution;
this scheduling order is **not version precedence**. Exhaustion refuses remaining
affected rows while preserving completed siblings and independently known population.

## Stable failure and acceptance surface

Source/view failures use fixed reason codes, no raw parser/network text. At minimum:
`maven_discovery_unavailable`, `maven_population_unknown`, `maven_unsupported_model`,
`maven_unsupported_version`, `maven_comparator_refused`, `maven_policy_unknown`,
`maven_observed_reader_unavailable`, `maven_catalogue_unavailable`,
`unknown_latest_eligibility`, `ambiguous_latest_version`, `no_stable_release`,
`maven_time_basis_unavailable`, `maven_metadata_worker_unavailable`,
`maven_metadata_budget_exceeded`, and legacy `maven_plural_projection_unavailable`.
Different diagnostic categories may explain a fixed reason only through a closed,
sanitized vocabulary. No source URLs, absolute roots, credentials or raw evidence.
No-eligible known catalogue gives no_stable_release; no eligible candidate with
unknown candidates gives unknown_latest_eligibility.

Preserve S6 collection admission: safe countable occurrence records or certified
empty population accept a Declared collection independently of row version, policy
or date success. All missing/unsupported versions, all pre-HTTP policy refusals and
metadata/date failures are row failures (known N, M=0/coverage0 when complete N>0),
not whole-view unavailability. No accepted collection means null M/numerics; unknown
population means null denominator/coverage. Initial Observed has no accepted collection. Per-GA catalogue failure affects its dependent
rows, never erases successful other GAs/modules/ecosystems. Existing CLI exit meanings
remain: data unavailability/partial coverage is a completed scan, not a usage error;
invalid CLI/path and systemic top-level failures retain existing meanings.

Offline acceptance includes fixed-host/path/proxy/auth/redirect refusal, malformed
identity/XML/date/status/header cases, over-budget/blocked worker/protocol behavior,
unknown-below/equal/above maximum and ties, exact same-version missing-date refusal,
all S6 partial/null cases and mixed-sibling preservation. Real public-target validation
is a separately authorized later witness, not a prerequisite for deterministic tests.
