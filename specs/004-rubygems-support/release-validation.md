# Feature 004: T018 release-validation evidence

## Disposition

**COMPLETE — authorized human-supplied live validation succeeded.** The human
performed the required human-readable and JSON scans in the normal user execution
environment after Codex DNS prevented live validation. The existing CLI used
`--ca-bundle <authorized-ca-bundle>` for the already authorized dpc-admin
root. This completion accepts the human-supplied evidence below; Codex did not
rerun live requests or independently inspect the preserved successful raw JSON.
T019 remains pending and requires independent convergence in a fresh context.

## Successful manual release evidence

The human reports these existing CLI invocations, using the authorized temporary
bundle without changing code or trust configuration:

```text
python -m libyears <authorized-checkout>/dpc-app/dpc-admin --verbose --ca-bundle <authorized-ca-bundle>
python -m libyears <authorized-checkout>/dpc-app/dpc-admin --json --ca-bundle <authorized-ca-bundle>
```

| Scope | Discovered | Measured | JSON coverage | Human coverage |
|---|---:|---:|---:|---:|
| Repository | 79 | 77 | 0.9746835443037974 | 97.5% |
| npm | 10 | 10 | 1.0 | 100.0% |
| RubyGems | 69 | 67 | 0.9710144927536232 | 97.1% |

Repository JSON total_libyears is 257.15223751425964. Human values are total
257.15, mean 3.34, median 4.20 and maximum 7.34. Ruby human values are total
236.15, mean 3.52, median 4.20 and maximum 7.34. Reported human/JSON agreement is
at documented display precision, including individual results and provenance.
Counts, coverage fractions, repository total rounding and repository mean
rounding are also checked directly from the supplied numeric summary. No exact
Ruby aggregate or individual publication timestamp is invented from rounded data.

The preserved JSON reports schema_version 3, ecosystems npm and rubygems,
source_errors [], and only two unmeasurable rows: bundler and tzinfo-data, both
lock_version_missing (human: exact selected spec unavailable). There are no Ruby
registry/transport failures. Ruby evidence reports declaration_source and
snapshot_source Gemfile.lock, format gemfile_lock, scope all_direct_locked and
publication_basis earliest_admissible_supported_observable. The human confirms
selected-artifact and used/latest publication-artifact provenance in the JSON,
including real multi-platform publication evidence. This is live validation
evidence supplied by the human, not an independent convergence verdict or a new
claim that Codex audited every timestamp against a registry response.

TLS trust reported by the successful CLI is
`explicit CA bundle: <authorized-ca-bundle>`. Certificate and hostname
verification remained enabled. The human reports no changes to repository code,
target files, system/Python trust configuration or certificate material during
validation. Existing target-integrity evidence below remains intact: before/after
manifests matched during earlier runs and both Codex retries; the human attests
the successful manual validation left target files unchanged. No new manual
manifest digest or transport trace was supplied, and none is implied.

Current separate smoke disposition: **REDUNDANT**. Successful authorized real-root
human/JSON dogfood exercised the approved verified RubyGems metadata and
publication path; a separate libyears live smoke would add no necessary evidence.
Earlier UNAVAILABLE dispositions are historical. OpenSSL and Python HTTP 200
checks establish human-reported trust-boundary context, not substitute dogfood.

T018 completion conditions are satisfied using the explicitly accepted human
evidence, existing integrity records and no-change attestation. No runtime or
test code changed. T017's 289 offline tests and 52/52 AC audit remain the
deterministic gate; no new suite or live request was run for this reconciliation.
Only release-validation.md and tasks.md are changed. Repository checks found no
tracked or copied CA bundle/certificate material. Final diff reviewed and
git diff --check passed before the authorized T018 commit. Stop before T019.

## Historical environmental attempts

All blocked statuses, smoke dispositions and unsuccessful CLI captures below
describe earlier attempts, superseded by the successful manual evidence above.
Codex DNS failures are execution-environment failures, not libyears or RubyGems
failures. Neither failed Ruby 0/69 nor initial 10/79 output is meaningful
dependency coverage or a repository freshness result.

## Authorized trust-boundary resolution and resumed attempt

Historical environmental sequence, distinguished from deterministic correctness:

1. The original certifi-only request failed with URLError wrapping
   SSLCertVerificationError, CERTIFICATE_VERIFY_FAILED: unable to get local issuer
   certificate, OpenSSL verification code 20, before HTTP. The prior read-only
   investigation found identical failure through restricted and shared default
   verified paths, no redirect involvement and no demonstrated Feature 004 defect.
2. Later, Codex requests encountered an agent execution-environment DNS limitation, including escalated attempts. The user reported successful host and normal Python DNS.
3. The user manually reproduced the TLS failure in their normal environment and identified managed TLS inspection of rubygems.org and the organizational CA required for verified connectivity.
 4. Human-established provenance: a read-only export of the explicitly authorized organizational CA was combined with the existing public CA bundle in  `<authorized-ca-bundle>`. The user reported successful verified OpenSSL connectivity using the exported root, successful Python context loading using the combined bundle and verified urllib HTTP 200 from https://rubygems.org/. These are user-supplied results, not Codex observations.
5. The user explicitly authorized this temporary bundle through the existing
   `--ca-bundle` interface for T018. No certificate material was copied into this
   repository or committed. No system/Python trust configuration was changed.

Resumed production entry point arguments:

```text
python -B -m libyears <authorized-checkout>/dpc-app/dpc-admin --verbose --ca-bundle <authorized-ca-bundle>
```

The entry point ran via runpy with those arguments. Passive profile observers
captured original transport returns and the scan report; an exception trace
captured restricted-path errors without replacing requests, trust or scan logic.
Temporary output and integrity records were stored outside both repositories.
Human starts: 2026-10-28 19:33:20.567449 UTC (sandbox) and
19:33:42.942581 UTC (escalated retry). Both exited 0, but all 77 registry requests
failed DNS: ten npm requests and 67 Ruby identity requests. All 67 Ruby errors in
the escalated retry were URLError wrapping gaierror:
`[Errno 8] nodename nor servname provided, or not known`. No verification code,
HTTP status, Ruby population, publication date or metric was obtained.
Two Ruby declarations, bundler and tzinfo-data, retained lock_version_missing.

The authorized bundle loaded successfully. Observed transport settings were
CERT_REQUIRED, hostname checking enabled, explicit trust path
`<authorized-ca-bundle>`, timeout 10 seconds and User-Agent libyears/0.1;
Ruby retained rubygems.org authority and the 16,777,216-byte cap.
Python 3.11.0, macOS 26.7.2 arm64 and OpenSSL 1.1.1q were unchanged.
This attempt cannot test whether TLS code 20 is resolved inside Codex: DNS failed
before TLS. It does not contradict the user's successful verified connectivity.

Observed output: Ruby 0/69 and repository 0/79 measured, serialized totals 0.0
and null mean/median/maximum. These are environment-blocked results, not meaningful
dependency coverage or freshness measurements. No new JSON CLI scan or human/JSON
comparison was performed. The captured internal report is not JSON CLI evidence.
Selected lock provenance remains available; publication provenance is unverified.

Before/after manifests were identical for each attempt and across both attempts:
281 entries including the root, 218 regular files, preserving relative paths,
types, permissions, mtime_ns, file sizes/hashes and symlink text without following
links. Canonical SHA-256 (json.dumps with sort_keys=True):
`c0e924be546286042e4d20b3ab76b5c6a5b3c3be72d745a15fc46d1b14cec68c`.
The three root evidence hashes match the historical table below. The historical
record reports 280 entries; this retry's count includes the root. No claim of
full-manifest identity across sessions is made; integrity passed within this retry.

At this earlier attempt, smoke disposition was **UNAVAILABLE** in Codex because
DNS prevented useful verified transport evidence. The user's connectivity check supplies trust-boundary
context but does not complete required real-root publication/metric validation.
Remaining blocker: Codex DNS. Stop before JSON and independent convergence.
T017's 289 offline tests and 52/52 AC audit remain the deterministic gate; no
runtime change or new deterministic suite is required for this evidence update.

## Historical initial validation disposition

**BLOCKED — T018 incomplete.** The authorized real-root human and JSON runs
completed and agree on available output, but verified RubyGems TLS failed for
every eligible Ruby candidate. No Ruby publication population, canonical date,
latest selection, publication provenance or libyears value was established live.
Required Ruby dogfood evidence remains incomplete; do not advance to T019.
No runtime, product, architecture or trust-policy remediation was attempted.

## Authorization and method

The user explicitly authorized read-only T018 validation of
`<authorized-checkout>/dpc-app/dpc-admin`, including before/after target integrity.
After root inspection found supported npm evidence, the user separately authorized
npm registry requests for these same human/JSON runs. This grants no access to
other historical discovery roots. Neither target tooling nor repository code ran;
no target file was written. Gemfile contents were not interpreted. Opaque content
hashes were used solely for the explicitly authorized integrity check.

Validated implementation: `6e27d1349b3e7f848dec30aaf6a44d8ada282a6e` (T017), with a clean initial working tree.
The production CLI entry point was invoked with these arguments:

```text
python -m libyears <authorized-checkout>/dpc-app/dpc-admin --verbose
python -m libyears <authorized-checkout>/dpc-app/dpc-admin --json
```

For passive transport evidence, a temporary standard-library runner set the same
CLI argv and called `runpy.run_module("libyears", run_name="__main__")`.
A `sys.setprofile` observer recorded calls/returns of the original
`VerifiedJSONTransport.get`: URL, start/elapsed time, configured TLS/transport
settings, returned-byte size/hash or typed failure. It neither replaced transport
methods nor injected HTTP, clocks, lookup results or CLI scan behavior. Output
and observation files were written to temporary storage outside the target.
The complete public outputs are retained below; temporary files are not required
to read this record. This is execution evidence, not independent convergence.

## Environment and attempts

- Python 3.11.0, macOS 26.7.2 arm64, OpenSSL 1.1.1q (5 Jul 2022).
- No explicit `--ca-bundle`; normal trust selection reported
  `pip-bundled CA fallback` in both runs.
- Preliminary sandbox human attempt: 77 DNS failures, exit 0, no measurements.
  This environmental attempt was kept separate from the following live results.
  Network escalation was approved before rerunning outside the sandbox.
- Live human: 2026-10-28 18:57:01.164479 UTC; 11.128 seconds; exit 0.
- Live JSON: 2026-10-28 18:58:04.341804 UTC; 10.349 seconds; exit 0.
- Both live runs: 10 npm responses returned bytes; 67 Ruby identity requests
  failed with the safe diagnostic `TLS certificate verification failure`.
  All ten npm response SHA-256 values matched between runs. No Ruby response
  body or HTTP status was obtained. The certificate-chain cause was not diagnosed.

## Human/JSON comparison and provenance

The following historical values are preserved as raw output evidence. The 10/79
result is not meaningful dependency coverage: Ruby registry measurement was
blocked by the environment. It cannot establish repository freshness.

| Scope | Discovered | Measured | Coverage | Total | Mean | Median | Maximum |
|---|---:|---:|---:|---:|---:|---:|---:|
| Repository | 79 | 10 | 10/79 (12.7% displayed) | 21.004480118988766 | 2.100448011898877 | 0.7076195982425787 | 5.251032024330113 |
| npm | 10 | 10 | 1.0 (100.0%) | 21.004480118988766 | 2.100448011898877 | 0.7076195982425787 | 5.251032024330113 |
| RubyGems | 69 | 0 | 0.0 (0.0%) | 0.0 | null | null | null |

Schema 3 detects only npm and RubyGems; no source error or invented Python source
appears. Known Ruby scope is retained despite registry failure. Human totals
round to 21.00 / 2.10 / 0.71 / 5.25, matching JSON. Every measured row's exact
name, used/latest version, source and value agrees at human display precision.
Independently recalculated all ten npm row values from their JSON UTC timestamps
using elapsed seconds / (86400 * 365.25), exact same-version zero and anomaly
rules, then checked sum/mean/median/max and measured/discovered coverage.
These npm successes do not substitute for missing Ruby success evidence.

All 69 recorded Ruby direct declarations appear as dependency-level failures
with original declared text. `bundler (>= 1.15.0)` and `tzinfo-data` have
`lock_version_missing`, no selected artifact, and no requests. The other 67
have `registry_error`; each retains its exact selected version, `ruby` platform
and `https://rubygems.org` source, with **no** used/latest publication arrays.
Their identities and selected versions are retained in the JSON capture below.
No publication time, yanking assertion or partial metric was fabricated.

Ruby evidence is `Gemfile.lock` for both declaration and snapshot,
`format=gemfile_lock`, `scope=all_direct_locked`, and
`publication_basis=earliest_admissible_supported_observable`. npm retains its
existing package.json/package-lock.json evidence. Human output includes all-direct
scope, uninterpreted groups, observable-history limits, absence not proving yanking
or never-existence, record-disappearance effects, and unavailable nulls.
All failure names, original declarations and contextual human reasons were checked
against JSON; all 67 safe verbose diagnostics identify TLS verification failure.
No human/JSON discrepancy was found in the available evidence.

## Transport evidence and limits

Both live runs observed `CERT_REQUIRED`, hostname checking enabled, a 10-second
request timeout and User-Agent `libyears/0.1`. Every Ruby request had fixed
`rubygems.org` authority and a 16,777,216-byte response cap. The adapter's approved
maximum is two requests / 32 MiB per candidate; redirects are rejected, no retry
is performed, and requests are paced at least 0.11 seconds apart.

Observed per live run: 67 Ruby requests, exactly one per locally accepted
candidate, in ascending exact-name order, all at
`https://rubygems.org/api/v1/gems/{name}.json`, from `actionmailbox` through
`webpacker`. No versions-population request followed a failed identity request.
No bundler/tzinfo-data, transitive, private, archive or alternate-host request
occurred. Minimum observed Ruby start spacing was 0.110368292 seconds (human)
and 0.110326958 seconds (JSON), consistent with the configured pacing.

No 429, Retry-After, redirect, oversize or incomplete-body event was observed;
those behaviors remain supported by deterministic evidence rather than this run.
The successful npm requests used the existing unbounded default transport;
Ruby's opt-in limits did not change npm policy. Verification was never disabled,
no alternate CA path was searched for, and no unapproved registry was contacted.

## Target integrity

Before/after opaque recursive manifests were identical: 280 entries, including
218 regular files. Manifests record relative paths, lstat type/mode and mtime_ns,
regular-file size/SHA-256, and symlink text without following symlinks. Root
membership was also unchanged (16 entries). No parent Git metadata was inspected
or modified. Reads can update filesystem access times; access times were excluded.

The canonical manifest digest (SHA-256 of `json.dumps(rows, sort_keys=True)`,
rows sorted by relative path) was identical before and after:
`6e4bdefd40b16d8864815576f432950624a058a752d60d91050e7992c9f58a4e`.

| Root evidence | Before and after SHA-256 |
|---|---|
| Gemfile.lock | `e8852e0719202c9e5b210d7da434cae0a094865c82ebf404f15fe27da39146a1` |
| package.json | `8f3b262a46a2969eb8bc4a7ce857d51e5fea2d11fd669424dd2c2208e93988c4` |
| package-lock.json | `4bacb1e061e32d0d0f5615e74e53050003f3bb412d3fae8aa74a355cc9f96553` |

## Smoke disposition

**UNAVAILABLE.** A separate RubyGems metadata smoke could add publication-path
evidence because dogfood never passed certificate verification. Useful successful
smoke evidence could not be obtained through the approved verified transport in
this environment; another identical request would repeat the observed failure.
No separate smoke was run, no success is claimed, and no TLS bypass or additional
endpoint is authorized. This optional smoke is not a convergence prerequisite.
The blocker is incomplete required Ruby real-root dogfood, not optional smoke.

## Verification and stopping boundary

T017 remains the deterministic correctness gate: 289 tests passed, 52/52
acceptance criteria audited, all offline (see tasks.md). T018 requires no new
correctness suite; none was rerun for this evidence-only change. Live TLS and
sandbox DNS failures are environmental evidence, not deterministic test failures.

Release checks passed for the available evidence: human/JSON counts, all rows and
reasons, rounded arithmetic/aggregates, scope/history disclosures, selected Ruby
provenance and absent publication arrays, verified transport settings and observed
scheduling, identical successful npm metadata, and complete target manifest
agreement. Required successful Ruby publication provenance and arithmetic checks
are **blocked**, so T018 is not complete. Diff inspected and `git diff --check`
passed before committing this partial record.

Next dependency-ready work remains resuming T018 with working verified RubyGems
trust, using an explicitly authorized trust configuration if one is needed.
No cause or CA remedy is inferred here. T019 independent read-only convergence,
T020 completion/radar reconciliation and T021 retrospective remain unstarted.
No approved spec/plan, runtime, tests, user documentation or external target changed.

## Retained public output

The human capture below is a sanitized transcription: its local checkout path has been replaced. The JSON capture retains every original field/value, with whitespace compacted to one dependency/failure object per line. Command examples and quoted trust-path diagnostics use sanitized local-path placeholders where present.
Original unsanitized stdout SHA-256 values follow. These identify the original captures and do not authenticate the sanitized human transcription:

- Human: `150f7ed7ad155f1481d282fbddc0836024953f594482e00834975c7590e8ea37`
- JSON before compaction: `9cb21804bf2c180dcc8bb22736ca37d330265aa644148178413948b7a99fc334`

<details>
<summary>Human output (--verbose)</summary>

```text
Libyears: <authorized-checkout>/dpc-app/dpc-admin
Ecosystems: npm, rubygems

RubyGems version evidence: Gemfile.lock.
All direct dependencies recorded in Gemfile.lock; groups are not interpreted.
Publication dates are earliest admissible supported observable evidence, not complete historical knowledge.
Missing public records prove neither yanking nor never-existence; record disappearance may change future measurements.
Null counts and coverage mean unavailable.
Repository: 12.7% coverage; 10 / 79 measured; total 21.00, mean 2.10, median 0.71, max 5.25 libyears
npm: 100.0% coverage; 10 / 10 measured; total 21.00, mean 2.10, median 0.71, max 5.25 libyears
rubygems: 0.0% coverage; 0 / 69 measured; total 0.00, mean null, median null, max null libyears

DEPENDENCY       ECOSYSTEM  USED       LATEST       LIBYEARS  SOURCE
@rails/activestorage npm        6.1.4      7.2.400      5.25  package_lock
ssri             npm        6.0.2      14.0.0       5.08  package_lock
tar              npm        6.1.11     7.5.22       4.91  package_lock
@rails/ujs       npm        6.1.4      7.1.600      4.35  package_lock
@rails/webpacker npm        5.4.3      5.4.4        1.42  package_lock
@cmsgov/design-system-core npm        3.7.2      3.7.2        0.00  package_lock
@cmsgov/design-system-layout npm        3.7.2      3.7.2        0.00  package_lock
normalize.css    npm        8.0.1      8.0.1        0.00  package_lock
svg4everybody    npm        2.1.9      2.1.9        0.00  package_lock
turbolinks       npm        5.2.0      5.2.0        0.00  package_lock

Unmeasurable:
  rubygems: bundler (bundler (>= 1.15.0))    exact selected spec unavailable in Gemfile.lock
  rubygems: tzinfo-data (tzinfo-data)    exact selected spec unavailable in Gemfile.lock
  rubygems: actionmailbox (actionmailbox (~> 6.1.6))    registry or transport error
  rubygems: actionmailer (actionmailer (~> 6.1.6))    registry or transport error
  rubygems: actionpack (actionpack (~> 6.1.6))    registry or transport error
  rubygems: actiontext (actiontext (~> 6.1.6))    registry or transport error
  rubygems: actionview (actionview (~> 6.1.6))    registry or transport error
  rubygems: active_model_serializers (active_model_serializers)    registry or transport error
  rubygems: activejob (activejob (~> 6.1.6))    registry or transport error
  rubygems: activemodel (activemodel (~> 6.1.6))    registry or transport error
  rubygems: activerecord (activerecord (~> 6.1.6))    registry or transport error
  rubygems: activestorage (activestorage (~> 6.1.6))    registry or transport error
  rubygems: activesupport (activesupport (~> 6.1.6))    registry or transport error
  rubygems: bootsnap (bootsnap (>= 1.4.2))    registry or transport error
  rubygems: bundler-audit (bundler-audit)    registry or transport error
  rubygems: byebug (byebug)    registry or transport error
  rubygems: capybara (capybara (>= 2.15))    registry or transport error
  rubygems: climate_control (climate_control)    registry or transport error
  rubygems: database_cleaner (database_cleaner)    registry or transport error
  rubygems: devise (devise)    registry or transport error
  rubygems: devise-async (devise-async)    registry or transport error
  rubygems: devise-security (devise-security)    registry or transport error
  rubygems: dotenv-rails (dotenv-rails)    registry or transport error
  rubygems: factory_bot_rails (factory_bot_rails)    registry or transport error
  rubygems: fakefs (fakefs)    registry or transport error
  rubygems: fakeredis (fakeredis)    registry or transport error
  rubygems: fhir_client (fhir_client)    registry or transport error
  rubygems: health_check (health_check)    registry or transport error
  rubygems: jbuilder (jbuilder (~> 2.7))    registry or transport error
  rubygems: kaminari (kaminari)    registry or transport error
  rubygems: letter_opener (letter_opener)    registry or transport error
  rubygems: listen (listen (~> 3.2))    registry or transport error
  rubygems: lograge (lograge)    registry or transport error
  rubygems: luhnacy (luhnacy (~> 0.2.1))    registry or transport error
  rubygems: macaroons (macaroons)    registry or transport error
  rubygems: newrelic_rpm (newrelic_rpm (~> 6.10))    registry or transport error
  rubygems: nokogiri (nokogiri (>= 1.13.4))    registry or transport error
  rubygems: octokit (octokit)    registry or transport error
  rubygems: omniauth-github (omniauth-github)    registry or transport error
  rubygems: omniauth-oktaoauth (omniauth-oktaoauth)    registry or transport error
  rubygems: omniauth-rails_csrf_protection (omniauth-rails_csrf_protection (~> 0.1))    registry or transport error
  rubygems: pg (pg (>= 0.18, < 2.0))    registry or transport error
  rubygems: pry (pry)    registry or transport error
  rubygems: pry-nav (pry-nav)    registry or transport error
  rubygems: puma (puma (~> 4.3.12))    registry or transport error
  rubygems: rails-controller-testing (rails-controller-testing)    registry or transport error
  rubygems: railties (railties (~> 6.1.6))    registry or transport error
  rubygems: rbnacl (rbnacl)    registry or transport error
  rubygems: rbnacl-libsodium (rbnacl-libsodium)    registry or transport error
  rubygems: redis (redis (~> 4.0))    registry or transport error
  rubygems: redis-namespace (redis-namespace)    registry or transport error
  rubygems: rexml (rexml (>= 3.2.5))    registry or transport error
  rubygems: rspec-rails (rspec-rails)    registry or transport error
  rubygems: rubocop (rubocop)    registry or transport error
  rubygems: rubocop-performance (rubocop-performance)    registry or transport error
  rubygems: sassc-rails (sassc-rails (>= 2.1.2))    registry or transport error
  rubygems: selenium-webdriver (selenium-webdriver)    registry or transport error
  rubygems: sidekiq (sidekiq (~> 6.4))    registry or transport error
  rubygems: sidekiq_alive (sidekiq_alive)    registry or transport error
  rubygems: simplecov (simplecov (<= 0.17))    registry or transport error
  rubygems: spring (spring)    registry or transport error
  rubygems: spring-watcher-listen (spring-watcher-listen (~> 2.0.0))    registry or transport error
  rubygems: truemail (truemail)    registry or transport error
  rubygems: turbolinks (turbolinks (~> 5))    registry or transport error
  rubygems: uglifier (uglifier (>= 1.3.0))    registry or transport error
  rubygems: web-console (web-console (>= 3.3.0))    registry or transport error
  rubygems: webdrivers (webdrivers)    registry or transport error
  rubygems: webmock (webmock)    registry or transport error
  rubygems: webpacker (webpacker (~> 4.0))    registry or transport error

TLS trust: pip-bundled CA fallback
Registry diagnostics:
  bundler: No ordinary selected lock spec.
  tzinfo-data: No ordinary selected lock spec.
  actionmailbox: TLS certificate verification failure
  actionmailer: TLS certificate verification failure
  actionpack: TLS certificate verification failure
  actiontext: TLS certificate verification failure
  actionview: TLS certificate verification failure
  active_model_serializers: TLS certificate verification failure
  activejob: TLS certificate verification failure
  activemodel: TLS certificate verification failure
  activerecord: TLS certificate verification failure
  activestorage: TLS certificate verification failure
  activesupport: TLS certificate verification failure
  bootsnap: TLS certificate verification failure
  bundler-audit: TLS certificate verification failure
  byebug: TLS certificate verification failure
  capybara: TLS certificate verification failure
  climate_control: TLS certificate verification failure
  database_cleaner: TLS certificate verification failure
  devise: TLS certificate verification failure
  devise-async: TLS certificate verification failure
  devise-security: TLS certificate verification failure
  dotenv-rails: TLS certificate verification failure
  factory_bot_rails: TLS certificate verification failure
  fakefs: TLS certificate verification failure
  fakeredis: TLS certificate verification failure
  fhir_client: TLS certificate verification failure
  health_check: TLS certificate verification failure
  jbuilder: TLS certificate verification failure
  kaminari: TLS certificate verification failure
  letter_opener: TLS certificate verification failure
  listen: TLS certificate verification failure
  lograge: TLS certificate verification failure
  luhnacy: TLS certificate verification failure
  macaroons: TLS certificate verification failure
  newrelic_rpm: TLS certificate verification failure
  nokogiri: TLS certificate verification failure
  octokit: TLS certificate verification failure
  omniauth-github: TLS certificate verification failure
  omniauth-oktaoauth: TLS certificate verification failure
  omniauth-rails_csrf_protection: TLS certificate verification failure
  pg: TLS certificate verification failure
  pry: TLS certificate verification failure
  pry-nav: TLS certificate verification failure
  puma: TLS certificate verification failure
  rails-controller-testing: TLS certificate verification failure
  railties: TLS certificate verification failure
  rbnacl: TLS certificate verification failure
  rbnacl-libsodium: TLS certificate verification failure
  redis: TLS certificate verification failure
  redis-namespace: TLS certificate verification failure
  rexml: TLS certificate verification failure
  rspec-rails: TLS certificate verification failure
  rubocop: TLS certificate verification failure
  rubocop-performance: TLS certificate verification failure
  sassc-rails: TLS certificate verification failure
  selenium-webdriver: TLS certificate verification failure
  sidekiq: TLS certificate verification failure
  sidekiq_alive: TLS certificate verification failure
  simplecov: TLS certificate verification failure
  spring: TLS certificate verification failure
  spring-watcher-listen: TLS certificate verification failure
  truemail: TLS certificate verification failure
  turbolinks: TLS certificate verification failure
  uglifier: TLS certificate verification failure
  web-console: TLS certificate verification failure
  webdrivers: TLS certificate verification failure
  webmock: TLS certificate verification failure
  webpacker: TLS certificate verification failure
```

</details>

<details>
<summary>JSON output (all fields retained)</summary>

```json
{
  "schema_version": 3,
  "metric": "libyears",
  "dependency_scope": "direct",
  "ecosystems": ["npm", "rubygems"],
  "version_evidence": {"npm": {"declaration_source": "package.json", "snapshot_source": "package-lock.json"}, "rubygems": {"declaration_source": "Gemfile.lock", "snapshot_source": "Gemfile.lock", "format": "gemfile_lock", "scope": "all_direct_locked", "publication_basis": "earliest_admissible_supported_observable"}},
  "summary": {"dependencies_discovered": 79, "dependencies_measured": 10, "coverage": 0.12658227848101267, "total_libyears": 21.004480118988766, "mean_libyears": 2.100448011898877, "median_libyears": 0.7076195982425787, "max_libyears": 5.251032024330113, "by_ecosystem": {"npm": {"dependencies_discovered": 10, "dependencies_measured": 10, "coverage": 1.0, "total_libyears": 21.004480118988766, "mean_libyears": 2.100448011898877, "median_libyears": 0.7076195982425787, "max_libyears": 5.251032024330113}, "rubygems": {"dependencies_discovered": 69, "dependencies_measured": 0, "coverage": 0.0, "total_libyears": 0.0, "mean_libyears": null, "median_libyears": null, "max_libyears": null}}},
  "dependencies": [
    {"ecosystem": "npm", "name": "@cmsgov/design-system-core", "used_version": "3.7.2", "used_release_time": "2020-07-08T15:25:59.599000Z", "latest_stable_version": "3.7.2", "latest_stable_release_time": "2020-07-08T15:25:59.599000Z", "libyears": 0.0, "timestamp_anomaly": false, "version_source": "package_lock"},
    {"ecosystem": "npm", "name": "@cmsgov/design-system-layout", "used_version": "3.7.2", "used_release_time": "2020-07-08T15:26:27.709000Z", "latest_stable_version": "3.7.2", "latest_stable_release_time": "2020-07-08T15:26:27.709000Z", "libyears": 0.0, "timestamp_anomaly": false, "version_source": "package_lock"},
    {"ecosystem": "npm", "name": "@rails/activestorage", "used_version": "6.1.4", "used_release_time": "2021-06-24T20:41:07.533000Z", "latest_stable_version": "7.2.400", "latest_stable_release_time": "2026-09-24T19:13:55.744000Z", "libyears": 5.251032024330113, "timestamp_anomaly": false, "version_source": "package_lock"},
    {"ecosystem": "npm", "name": "@rails/ujs", "used_version": "6.1.4", "used_release_time": "2021-06-24T20:40:25.705000Z", "latest_stable_version": "7.1.600", "latest_stable_release_time": "2025-10-28T23:20:18.866000Z", "libyears": 4.345273188106828, "timestamp_anomaly": false, "version_source": "package_lock"},
    {"ecosystem": "npm", "name": "@rails/webpacker", "used_version": "5.4.3", "used_release_time": "2021-09-14T19:36:39.684000Z", "latest_stable_version": "5.4.4", "latest_stable_release_time": "2023-02-13T17:35:52.151000Z", "libyears": 1.4152391964851574, "timestamp_anomaly": false, "version_source": "package_lock"},
    {"ecosystem": "npm", "name": "normalize.css", "used_version": "8.0.1", "used_release_time": "2018-11-09T22:48:56.639000Z", "latest_stable_version": "8.0.1", "latest_stable_release_time": "2018-11-09T22:48:56.639000Z", "libyears": 0.0, "timestamp_anomaly": false, "version_source": "package_lock"},
    {"ecosystem": "npm", "name": "ssri", "used_version": "6.0.2", "used_release_time": "2021-04-07T20:01:20.235000Z", "latest_stable_version": "14.0.0", "latest_stable_release_time": "2026-05-08T18:33:10.421000Z", "libyears": 5.084021287613759, "timestamp_anomaly": false, "version_source": "package_lock"},
    {"ecosystem": "npm", "name": "svg4everybody", "used_version": "2.1.9", "used_release_time": "2017-07-20T23:09:46.119000Z", "latest_stable_version": "2.1.9", "latest_stable_release_time": "2017-07-20T23:09:46.119000Z", "libyears": 0.0, "timestamp_anomaly": false, "version_source": "package_lock"},
    {"ecosystem": "npm", "name": "tar", "used_version": "6.1.11", "used_release_time": "2021-08-26T16:16:13.333000Z", "latest_stable_version": "7.5.22", "latest_stable_release_time": "2026-07-24T15:48:51.111000Z", "libyears": 4.908914422452911, "timestamp_anomaly": false, "version_source": "package_lock"},
    {"ecosystem": "npm", "name": "turbolinks", "used_version": "5.2.0", "used_release_time": "2018-08-20T15:43:21.931000Z", "latest_stable_version": "5.2.0", "latest_stable_release_time": "2018-08-20T15:43:21.931000Z", "libyears": 0.0, "timestamp_anomaly": false, "version_source": "package_lock"}
  ],
  "unmeasurable": [
    {"ecosystem": "rubygems", "name": "bundler", "declared": "bundler (>= 1.15.0)", "reason": "lock_version_missing"},
    {"ecosystem": "rubygems", "name": "tzinfo-data", "declared": "tzinfo-data", "reason": "lock_version_missing"},
    {"ecosystem": "rubygems", "name": "actionmailbox", "declared": "actionmailbox (~> 6.1.6)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.1.6.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "actionmailer", "declared": "actionmailer (~> 6.1.6)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.1.6.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "actionpack", "declared": "actionpack (~> 6.1.6)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.1.6.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "actiontext", "declared": "actiontext (~> 6.1.6)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.1.6.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "actionview", "declared": "actionview (~> 6.1.6)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.1.6.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "active_model_serializers", "declared": "active_model_serializers", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "0.10.13", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "activejob", "declared": "activejob (~> 6.1.6)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.1.6.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "activemodel", "declared": "activemodel (~> 6.1.6)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.1.6.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "activerecord", "declared": "activerecord (~> 6.1.6)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.1.6.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "activestorage", "declared": "activestorage (~> 6.1.6)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.1.6.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "activesupport", "declared": "activesupport (~> 6.1.6)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.1.6.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "bootsnap", "declared": "bootsnap (>= 1.4.2)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.12.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "bundler-audit", "declared": "bundler-audit", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "0.9.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "byebug", "declared": "byebug", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "11.1.3", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "capybara", "declared": "capybara (>= 2.15)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "3.37.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "climate_control", "declared": "climate_control", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.1.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "database_cleaner", "declared": "database_cleaner", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "2.0.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "devise", "declared": "devise", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "4.8.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "devise-async", "declared": "devise-async", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.0.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "devise-security", "declared": "devise-security", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "0.17.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "dotenv-rails", "declared": "dotenv-rails", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "2.7.6", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "factory_bot_rails", "declared": "factory_bot_rails", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.2.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "fakefs", "declared": "fakefs", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.7.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "fakeredis", "declared": "fakeredis", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "0.8.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "fhir_client", "declared": "fhir_client", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "5.0.3", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "health_check", "declared": "health_check", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "3.1.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "jbuilder", "declared": "jbuilder (~> 2.7)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "2.11.5", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "kaminari", "declared": "kaminari", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.2.2", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "letter_opener", "declared": "letter_opener", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.8.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "listen", "declared": "listen (~> 3.2)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "3.7.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "lograge", "declared": "lograge", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "0.12.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "luhnacy", "declared": "luhnacy (~> 0.2.1)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "0.2.2", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "macaroons", "declared": "macaroons", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.0.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "newrelic_rpm", "declared": "newrelic_rpm (~> 6.10)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.15.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "nokogiri", "declared": "nokogiri (>= 1.13.4)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.13.6", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "octokit", "declared": "octokit", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "4.25.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "omniauth-github", "declared": "omniauth-github", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.4.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "omniauth-oktaoauth", "declared": "omniauth-oktaoauth", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "0.1.6", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "omniauth-rails_csrf_protection", "declared": "omniauth-rails_csrf_protection (~> 0.1)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "0.1.2", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "pg", "declared": "pg (>= 0.18, < 2.0)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.4.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "pry", "declared": "pry", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "0.14.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "pry-nav", "declared": "pry-nav", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.0.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "puma", "declared": "puma (~> 4.3.12)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "4.3.12", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "rails-controller-testing", "declared": "rails-controller-testing", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.0.5", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "railties", "declared": "railties (~> 6.1.6)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.1.6.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "rbnacl", "declared": "rbnacl", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "5.0.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "rbnacl-libsodium", "declared": "rbnacl-libsodium", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.0.16", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "redis", "declared": "redis (~> 4.0)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "4.6.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "redis-namespace", "declared": "redis-namespace", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.8.2", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "rexml", "declared": "rexml (>= 3.2.5)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "3.2.5", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "rspec-rails", "declared": "rspec-rails", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "5.1.2", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "rubocop", "declared": "rubocop", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.30.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "rubocop-performance", "declared": "rubocop-performance", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "1.14.2", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "sassc-rails", "declared": "sassc-rails (>= 2.1.2)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "2.1.2", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "selenium-webdriver", "declared": "selenium-webdriver", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "4.2.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "sidekiq", "declared": "sidekiq (~> 6.4)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "6.5.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "sidekiq_alive", "declared": "sidekiq_alive", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "2.1.5", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "simplecov", "declared": "simplecov (<= 0.17)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "0.17.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "spring", "declared": "spring", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "2.1.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "spring-watcher-listen", "declared": "spring-watcher-listen (~> 2.0.0)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "2.0.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "truemail", "declared": "truemail", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "2.7.3", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "turbolinks", "declared": "turbolinks (~> 5)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "5.2.1", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "uglifier", "declared": "uglifier (>= 1.3.0)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "4.2.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "web-console", "declared": "web-console (>= 3.3.0)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "4.2.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "webdrivers", "declared": "webdrivers", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "5.0.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "webmock", "declared": "webmock", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "3.14.0", "platform": "ruby", "source": "https://rubygems.org"}]}},
    {"ecosystem": "rubygems", "name": "webpacker", "declared": "webpacker (~> 4.0)", "reason": "registry_error", "rubygems_evidence": {"selected_artifacts": [{"version": "4.3.0", "platform": "ruby", "source": "https://rubygems.org"}]}}
  ],
  "source_errors": []
}
```

</details>
