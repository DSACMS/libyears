# Feature 007 technical plan

## Authority and design

Run007-0008. The [whole specification](spec.md) and normative
[source policy](source-policy.md), [metadata contract](metadata-contract.md) and
[selected latest policy](latest-policy.md#selected-policy--run007-0008) are approved
in [reviews](reviews.md#run007-0008--whole-specification-convergence). This plan
awaits independent review; approval disposition lives there. No implementation,
public-target measurement/access renewal, private validation or push is authorized.

Implement a Maven-specific pipeline next to existing explicit ecosystem paths:

`bounded source inventory -> local model/occurrences -> Declared collection ->
local comparator refusals -> accepted metadata capabilities -> current catalogue /
conservative maximum -> exact POM modification dates -> independent views/output`.

No generic ecosystem/plugin/version framework, Maven execution or sibling plural/
time-basis retrofit. Small separate modules keep parsing, authority, network,
arithmetic and presentation inspectable. Limited duplication of existing safe
NuGet process/file patterns is preferable to a cross-ecosystem refactor here.

## P1 — Domain and summary boundaries

Add `maven_model.py` with immutable records for discovery, source/context, model key,
artifact key, raw field origins, occurrence, independently nullable request/version
facts, age, per-view collection state and metadata results. Store version_basis,
comparator_basis, time_basis and limitations separately. Do not shoehorn POM times
into public legacy Dependency/release-time records. Stable context ID is `base_model`
per source; safe parent-chain identities are separate context evidence, with internal
input bindings reserved for future joins. No current Observed reader or join route.

`maven_results.py` composes collections under S6 using explicit state branches.
Safe external identity records or certified complete emptiness admit Declared;
all missing versions/policy refusals remain row failures, even without HTTP. No
accepted collection means null M/numerics; unknown N means null coverage. Availability
labels do not substitute for arithmetic. Source and repository statistics operate
over the union of occurrence values, never average source means. A small Maven
summary implementation using existing MetricSummary and standard statistics avoids
changing sibling helper semantics. Numeric dates use existing `libyears_between`;
only admitted timestamps enter it. Same exact version reuses one admitted date for
exact0.0; reversed dates keep the existing anomaly flag/clamp.

Represent Observed as unavailable (`maven_observed_reader_unavailable`), all-null
summary, no invented N. Model-only tests may construct paired/observed-only cases
for expressiveness and non-substitution; no input feature creates them initially.

## P2 — Discovery and safe inputs

`maven_discovery.py` performs B1's deterministic bounded ordinary directory inventory.
Keep it separate from NuGet recognition so Maven's pom.xml names/exclusions/budgets
do not modify existing discovery. A direct file never activates Maven. Complete
empty inventory omits Maven; incomplete inventory retains safe observed sources and
an explicit unknown discovery result. Repository N/coverage cannot become known
from a capped prefix. Maven source errors are data, not a false missing-file usage error.

`maven_input.py` supplies descriptor-rooted no-follow/race-resistant reads, bounded
bytes and common safe XML framing. Stage a stable immutable in-memory input snapshot
for every used local POM/config, verify identities before admission and refuse
changes during reading. No later source-file reread may silently mix new bytes with
previous identities. Only discovered POMs supply parent/module bytes. Fixed .mvn
sentinels/settings use B4's separate exact safe paths. Do not enumerate/read user,
ancestor-outside-root or machine configuration. A missing capability fails closed.

Use standard-library incremental XML parsing with depth/element/attribute/scalar
counters, bounded total bytes and explicit DTD/entity/XInclude refusal before model
interpretation. Interpret namespaces exactly; schemaLocation is inert. Separate
structural framing acceptance from field-level model refusal. A malformed primary
model cannot be salvaged from a partial parser event stream. Tests inject safe reader
snapshots for semantic fixtures while native capability/race tests remain separate.

## P3 — Static model, association and declared facts

`maven_project.py` constructs the B2/S3 base-model snapshot without evaluating Maven:

1. Parse literal project/parent/module identities; bind contained discovered parents
   by relativePath plus exact GAV, with16-node chain/cycle limits.
2. Form unconditional module aggregation components independently from parent edges;
   ambiguity/unknown membership prevents unsupported internal exclusion.
3. Merge dependency fields by exact model key, child explicit values first, retaining
   origins. Keep scope default late and optional unmanaged.
4. Merge raw parent/child scalar properties, expand only S3's supported consumer-context
   names/builtins with budgets and reserved namespace precedence.
5. Apply management per field with unresolved-import conservatism. Do not fetch/read
   imported BOM contents, including local BOMs; direct supported facts survive.
6. Inspect possible source/ancestor profile effects conservatively. Withhold only
   dependent facts/population; unrelated execution plugins/profiles create no population.
7. Exclude internal requirements only by supported exact GAV in an unambiguous
   aggregation component. Retain external occurrences once per consuming source.

Use a small explicit built-in handler table pinned to Maven3.9.11. Keep model-key
management and artifact aliases distinct, including test-jar/tests cases. System
rows count when external identity is known, but never follow systemPath or compare.
Unknown handlers/types/classifiers and duplicate same-key records fail at the
smallest safe scope. Track global expanded-record/property/module budgets explicitly.
No resolver, host properties, effective POM, Gradle, transitive or plugin population.

## P4 — Local source/comparator admission

`maven_policy.py` consumes only the staged B3–B5 facts. Whole repository records
select by nearest child exact ID. Evaluate the conventional Central conclusion across
all possibly relevant profile writes. Extra non-central/file/parameterized eligibility
and unassigned mirrors do not veto. Central disable/redefinition/block, known identity
conflict/system assignment and unsafe relevant uncertainty refuse before capability
construction. Exact settings selection, known harmless launch properties, source-
relevant switches, extensions, mirror precedence/patterns/layouts and unsupported
filters follow B4/B5, not inferred Maven effective-state behavior.

Keep refusal reasons separate from population/fact evidence. Initially there is no
supplier assertion/private-assignment reader; do not synthesize one from suggestive
names, URLs or artifact hashes. A future stronger accepted reader requires separate
scope. Public remote POM relocation is terminal after its otherwise-authorized fetch.

`maven.py` is the source-level coordinator. It constructs closed accepted capabilities
only for safe exact Declared versions passing local policy; a test lookup seam must
receive none for denied rows. Group accepted work by exact GA/version only for
metadata scheduling/caching; map results back to every original occurrence without
deduplication or borrowing admission from another source.

## P5 — Ordering, eligibility and metadata parsing

`maven_version.py` reproduces pinned ComparableVersion3.9.11 item/list parsing and
comparison, with explicit numeric/string/list data structures and finite limits.
Use integer comparison for bounded numeric items, preserve exact original strings,
and implement upstream zero/list normalization and alias context faithfully. Do not
call Java or use SemVer/lexical order. Document derived code and retain required
Apache source/license/notice attribution in a small third-party provenance directory;
this adds no runtime dependency or package-manager operation.

Tests retain pinned upstream expected equality/ordering vectors plus adversarial
separator/underscore/nested-item/unknown/alias cases. Include antisymmetry/transitivity
checks over a fixed bounded corpus; no test regenerates expectations from the port.
Every supported safe version must match the pin; inability to compare refuses the
catalogue maximum instead of skipping that version. Eligible selection is a separate
function implementing maven_conservative_stable_v1, unknown-below/equal/above and
unique exact maximum. Snapshot suffix/token/timestamp recognition precedes eligibility.

`maven_registry.py` parses whole current GA metadata and exact POM representations
under the metadata contract. Reject bad catalogue identity/entries rather than take
a partial maximum. Literal POM/project-parent identity and any relocation are checked
without loading a parent. Require one valid supported Last-Modified and keep UTC
retrieval time separately. No date sorts versions or supplies a fallback. A measured
GAV may have its own POM even when absent from the current catalogue.

## P6 — Isolated HTTP worker and process protocol

Use Maven-specific `maven_supervisor.py`, a small closed `maven_protocol.py` codec,
and absolute installed `maven_worker.py` entry. Start trusted sys.executable with
`-I`, trusted installed imports only, a private temporary cwd and sanitized environment;
never target cwd/PYTHONPATH/imports. No Java, Maven, shell or target executable.
Use stdlib HTTPS with an explicit fixed host/path constructor, verified system trust
or staged explicitly supplied CA material, no proxies/netrc/auth/cookies/redirects,
and identity encoding. Do not change shared registry transport or NuGet worker behavior.

Keep each atomic command/result <=16KiB and perform **at most one GET per command**:
`select_target` fetches/parses the GA catalogue and returns only its selected exact
version/basis/retrieval time or fixed failure; `pom_date` fetches/parses one admitted
exact POM and returns only identity/date/retrieval time or fixed failure. Large raw
catalogues never enter the IPC protocol. Parent derives target-date requests only
from the accepted target result for the same admitted GA; measured-date requests
come only from accepted source capabilities. Worker validates closed operation/
sequence/coordinate schemas again. Internal selection evidence stays in the trusted
worker; parent validates result identity, allowed bases/reasons, timestamps and state.

One command's supervisor deadline is <=10seconds, including its single request and
bounded parsing, additionally limited by cumulative60-second GA and300-second scan
budgets. This also bounds blocked DNS before any socket timeout exists. Count every
attempt/body byte against scan300-GET/64MiB limits in both controller and client.
Read headers through a byte/count-capped reader before full header accumulation;
stream body with actual/advertised-length validation and response-specific cap.
The parent waits nonblockingly on bounded atomic messages and enforces deadlines.

On a returned per-representation failure, continue other admitted work within budgets.
On blocked deadline, protocol failure or worker death, terminate/reap with bounded
cleanup, refuse remaining Maven commands and preserve completed results. No worker
restart, synchronous fallback, retry or alternate endpoint. An unreaped worker
retains its handle for bounded deferred cleanup and forbids further Maven I/O.
Readiness cannot issue HTTP. No worker starts when all capabilities are denied.

Use bounded memory caches only for this scan, exact GA target/catalogue outcomes
and exact GAV dates including fixed failures. No persisted registry state. GA/scan
clocks and request/byte counters never reset per command/module. Schedule GAs and
measured strings deterministically; scheduling lexical order is not precedence.
Repeated occurrences reuse metadata while retaining independent source/row authority.

## P7 — Scan integration, schema and human output

Extend MixedScanReport with an optional Maven result, default absent; keep existing
single-view measurements/source results untouched. Ordinary directory scans invoke
Maven discovery automatically. Legacy source errors contain the unavailable plural
projection per detected source, or discovery failure with source_id null. Maven
presence/unknown discovery makes legacy repository N/coverage unknown per S8;
existing successful sibling rows/evidence/per-ecosystem summaries remain intact.
Do not insert any Maven age into legacy dependencies/unmeasurable/statistics.

Add Maven-specific serialization/human helpers (`maven_output.py`) called from the
existing output dispatch only when Maven is active/unknown. Fixed schema3 fields
follow S7/S8, including nullable request/version records, discovery and independent
views, exact POM timestamp names, conventional limitations and source-relative IDs.
Normal output prints paired headings/summaries, explicit unavailable Observed and
section-level conventional time basis; verbose expands provenance and limitations
without raw evidence/source URLs/absolute paths. Label the legacy sibling subset.
No new Java CLI flags or Observed-intake option. --resolved stays Python-only.
Existing exit-code meanings and ordinary non-Maven output stay unchanged when
complete Maven discovery finds no candidate; unknown discovery is an explicit failure.

At the later documentation checkpoint update README/SPEC/ECOSYSTEMS/CHANGELOG for
shipping scope and limitations, distinguishing conventional Maven dates, supported
base projection, module weighting and unknown/partial coverage. Do not claim released
support while only design artifacts exist. No sibling semantics/time vocabulary changes.

## P8 — Verification, portability and prospective validation

Deterministic tests use unittest/mock and local fixtures, no network. Establish pure
contracts/model/source authority/ordering/parser correctness before enabling HTTP.
Use injected reader/lookup/clock/HTTP seams; positive fixtures must not bypass denied
capability cases. Dedicated native filesystem/process tests retain capability refusal,
link/reparse/race, blocking-worker cleanup and trusted-import checks. In-memory semantic
fixtures do not prove native Windows safety. Platforms lacking required no-follow/
process primitives report unavailable; Windows CI tests that refusal explicitly.
Run Linux/macOS/Windows matrices before claiming supported positive native behavior.

Focused tests accompany each implementation task; full deterministic suite at source-
authority/HTTP integration and final boundaries. Include all AC01–AC20 cases, every
S6 composition, all-row failures with successful siblings, fixed-host/security/privacy
sentinels, blocked worker/protocol/byte/header/time limits, unknown eligibility and
missing-date/equal-zero cases. Four successful/empty sibling ecosystems, direct files,
no-Maven directories and incomplete discovery are mandatory regression witnesses.
Independent checkpoints review source admission before networking and then complete
integrated contracts; no test/live fetch weakens a refusal rule merely to get yield.

After deterministic convergence, prepare a separate public validation gate: exact
DPC target/revision/status, read-only access, safe public coordinate/HTTP authority,
artifact/diagnostic capture and integrity checks. Then test the ordinary root CLI /
JSON/verbose journey, preserve limitations and verify no target modification or
execution. No denominator/positive yield/Observed completeness promise. Live failure
is separate from offline correctness. Reuse retained AB2D adversarial shapes in
fixtures; no Gradle intake or target reinspection is needed without new authority.

Private validation requires its own future access/coordinate/source URL/path /
diagnostic/artifact/reviewer/observation/sanitization gate. No target is identified.
Final convergence reads approved spec/plan/tasks, implementation/tests/docs and
actual authorized validation evidence. Retrospective records gate/routing limits
without claiming attention savings or generic harness success.

## P9 — Traceability and next gate

| Plan surface | Specification acceptance |
| --- | --- |
| P1/P7 independent facts/collections/output | AC01–03,09,12–13 |
| P2/P3 bounded model/discovery/identity | AC04–08,18 |
| P4 pre-HTTP source authority | AC10,17–19 |
| P5/P6 catalogue/order/eligibility/date/transport | AC11,16,18–20 |
| P8 offline/security/mixed/platform/prospective journeys | AC01–20, especially14–16 |

Obtain fresh independent plan review and correct material findings with focused
non-author closure. Only an approved plan advances to sequential tasks/review.
Even approved tasks do not authorize implementation or target validation.
