# Libyears

Libyears is a local Python CLI that measures the age of direct Python, npm, and RubyGems
dependencies using release timestamps from their public registries.
It uses only the Python standard library at runtime.

Project website: https://dsacms.github.io/libyears

## CMS Open Source Program Office Mission

The function of the CMS Open Source Program Office is to:

> Establish and maintain guidance, policies, practices, and talent pipelines
> that advance access, build trust, and amplify impact across CMS, HHS, and
> Federal Open Source Ecosystems by working and sharing openly.

## What libyears measures

For each measurable dependency, libyears compares the release timestamp of its
exact used version with the timestamp of the latest stable release:

```text
libyears = max(latest stable release time - used release time, 0) / 365.25 days
```

The report includes total, mean, median, and maximum libyears, plus measurement
coverage. High libyears describes age; by itself, it does not mean a dependency
is vulnerable or unsafe.

## Important concept: version evidence

A dependency declaration says what a project requests, but it may not establish
the exact version used. For example, neither of these identifies an exact
version:

```text
requests
urllib3>=2.6.3
```

Libyears does not silently resolve those declarations against today's registry:
that would measure what might install now, not what the repository evidence
records. An exact repository pin or a resolved snapshot can provide version
evidence.

## Basic usage

Scan a directory (or a `requirements.txt` file directly):

```bash
python3 -m libyears PATH
python3 -m libyears PATH --json
```

## Exact-pinned requirements

Exact pins in `requirements.txt` can be measured directly:

```text
requests==2.34.2
pandas==2.3.3
```

## Resolved snapshot workflow

Create a snapshot and use it while scanning the repository:

```bash
python3 -m pip freeze > resolved.txt
python3 -m libyears PATH --resolved resolved.txt
```

The repository declarations still define direct dependency scope; the snapshot
supplies exact version evidence for those declared dependencies. Snapshot-only
transitive dependencies are ignored. Libyears does not invoke pip or install
dependencies itself. A freshly generated snapshot describes that environment
now, not historical repository state.

## TLS and enterprise environments

Registry requests use HTTPS with certificate verification enabled. Libyears follows
Python/OpenSSL defaults, including `SSL_CERT_FILE` and `SSL_CERT_DIR`. If the
active interpreter has no usable default CA source, it can fall back to an
existing pip-bundled CA file. An explicit bundle takes precedence:

```bash
python3 -m libyears PATH \
  --resolved resolved.txt \
  --ca-bundle /path/to/approved-ca-bundle.pem
```

Python's standard environment override is also supported:

```bash
SSL_CERT_FILE=/path/to/approved-ca-bundle.pem \
python3 -m libyears PATH --resolved resolved.txt
```

An explicit `--ca-bundle` is authoritative and validated before scanning. If no
trusted CA source is available, requests fail with verification enabled.

> Never use an unverified TLS context merely to make registry requests succeed.

## Verbose diagnostics

```bash
python3 -m libyears PATH --verbose
```

Verbose output can identify certificate verification failures, HTTP failures,
timeouts, DNS/network errors, malformed registry responses, and the selected TLS
trust source. Stable JSON reason identifiers remain unchanged.

## JSON output

JSON schema version 3 reports ecosystem-keyed version evidence, repository and
per-ecosystem summaries, and source discovery errors separately from
dependency-level failures. The schema v2 to v3 change is intentional. A
compact Python-only example:

```json
{
  "schema_version": 3,
  "metric": "libyears",
  "dependency_scope": "direct",
  "ecosystems": ["pypi"],
  "version_evidence": {
    "pypi": {
      "declaration_source": "requirements.txt",
      "snapshot_source": null
    }
  },
  "summary": {
    "dependencies_discovered": 1,
    "dependencies_measured": 1,
    "coverage": 1.0,
    "total_libyears": 0.999315537303217,
    "mean_libyears": 0.999315537303217,
    "median_libyears": 0.999315537303217,
    "max_libyears": 0.999315537303217,
    "by_ecosystem": {
      "pypi": {
        "dependencies_discovered": 1,
        "dependencies_measured": 1,
        "coverage": 1.0,
        "total_libyears": 0.999315537303217,
        "mean_libyears": 0.999315537303217,
        "median_libyears": 0.999315537303217,
        "max_libyears": 0.999315537303217
      }
    }
  },
  "dependencies": [
    {
      "ecosystem": "pypi",
      "name": "requests",
      "used_version": "2.34.2",
      "used_release_time": "2024-06-01T00:00:00Z",
      "latest_stable_version": "2.35.0",
      "latest_stable_release_time": "2025-06-01T00:00:00Z",
      "libyears": 0.999315537303217,
      "timestamp_anomaly": false,
      "version_source": "requirements_exact"
    }
  ],
  "unmeasurable": [],
  "source_errors": []
}
```

## Measurement coverage

Coverage is the number measured divided by the number discovered. `7 discovered
/ 0 measured` means no dependency age could be calculated; `7 discovered / 7
measured` means the aggregate covers every discovered dependency. Their numeric
totals cannot be interpreted as equivalent, even if both are low.

## npm support

For npm repositories, `package.json` root `dependencies` define direct
production scope, excluding names also declared in `optionalDependencies`.
Root `package-lock.json` versions 2 and 3 or root Yarn Classic v1 `yarn.lock`
provide exact used versions. Yarn evidence requires the canonical v1 header and
an exact textual match between the manifest declaration and a lock selector;
libyears does not evaluate ranges or execute Yarn/npm, install packages, or
resolve dependencies.
Development, peer, optional-only, workspace, and transitive dependencies are
outside this feature. Yarn Berry/v2+, PnP, and workspace aggregation are not
supported. `--resolved` remains Python-specific.

If both root lockfiles exist, neither is used, even if their versions agree:
`source_errors` reports `conflicting_resolution_sources`. Malformed supported
Yarn v1 uses `invalid_lockfile`; unsupported or safely unclassifiable Yarn uses
`unsupported_lockfile_format`. These whole-source failures retain the known
npm declaration count, but npm measured count and coverage are null. Mixed
repository coverage is also null; successful Python measurements and their
numeric aggregates survive. An invalid manifest makes npm counts and coverage
unknown.

Missing, unsupported-source, conflicting, or ambiguous dependency evidence
appears in `unmeasurable`, preserves the original declaration, and reduces
ordinary measured/discovered coverage without blocking other dependencies.
Human output identifies `yarn.lock` evidence and explains source failures.
JSON remains schema v3: Yarn measurements use `version_source: "yarn_lock"`,
and `version_evidence.npm` includes `format: "yarn_lock_v1"` and
`snapshot_source: "yarn.lock"`. Rejected unsupported/unclassifiable formats have
null format; simultaneous lockfiles have null format and snapshot source.
Existing package-lock and PyPI evidence representations are unchanged.

## RubyGems support

A directory scan recognizes exactly the root `Gemfile.lock`, even without a
Gemfile. All direct dependencies recorded in Gemfile.lock are counted; groups
are not interpreted. The report describes the supplied lock snapshot. It does
not certify committed bytes, current Gemfile contents, installed versions, or
runtime compatibility. Gemfile is never read or executed. `--resolved` remains
Python-specific; direct-file arguments do not activate Ruby discovery.

The supported bounded section format includes GEM, DEPENDENCIES, required
nonempty PLATFORMS, and optional BUNDLED WITH / RUBY VERSION. GIT and PATH
framing only isolates unsupported dependencies. Unknown fields/sections,
including CHECKSUMS, CONTENT ADDRESSES and PLUGIN SOURCE, reject the source.
This intentionally supports a subset of Bundler locks, not every generation.
No Ruby, Bundler, gemspec, installer, or resolver is executed.

Only a literal `https://rubygems.org` remote (optional trailing slash) supplies
public authority. Private, Git, PATH, multiple-remote and explicitly pinned
sources remain unmeasurable; a public namesake is never substituted. Exact
selected specs establish used versions; requirements are retained without
satisfaction or equivalence checks. Missing specs for direct `bundler` or
`tzinfo-data` remain counted. Agreeing distinct generic/platform artifacts
establish one package version and retain provenance; differing versions or
duplicate artifact rows are ambiguous. No host-platform selection occurs.

Ruby publication dates are the earliest admissible authoritative creation times
across supported observable artifacts, independently of locked platforms.
Missing/invalid dates and all 2009-07-25 UTC dates are excluded; build times are
never a fallback. Latest requires currently available stable artifact evidence
and chooses the greatest canonical date, with ascending exact version text for
ties. These dates are observable evidence, not complete historical knowledge.
Missing public records prove neither yanking nor never-existence. Disappearing
records may change future measurements.

JSON stays schema v3. `version_evidence.rubygems` identifies `Gemfile.lock`,
`format: "gemfile_lock"` (null on source rejection), `scope: "all_direct_locked"`,
and `publication_basis: "earliest_admissible_supported_observable"`.
Ruby rows use `version_source: "gemfile_lock"` and additive `rubygems_evidence`
with selected artifacts and admissible used/latest publication contributors.
Safely established evidence survives dependency failures; unavailable publication
arrays are omitted. Existing Python/npm evidence objects are unchanged.

Whole-lock rejection uses `source_errors`, with null Ruby counts, coverage and
numeric aggregates, and no invented rows. Known direct scope survives local or
registry failures, including total outages, in `unmeasurable`. Other ecosystems'
successes survive. Null coverage means unavailable; valid nonempty scope with no
measurements has 0% coverage. Completed partial/empty/source-error scans exit 0.

Ruby metadata requests use verified HTTPS with the existing CA precedence,
reject all redirects, and allow at most two requests per candidate, 16 MiB per
response (32 MiB total), with a default 10-second timeout. One scan-local adapter
paces request starts at least 0.11 seconds apart and respects 429 cooldowns
without retries. Authorized candidates run in exact name/version lexical order.
No archives or private source content are fetched. See the approved
[Feature 004 specification](specs/004-rubygems-support/spec.md) for the full boundary.

## Current limitations

- Python declarations are read from `requirements.txt`; npm declarations are
  read from the root `package.json`; RubyGems scope comes from root
  `Gemfile.lock` DEPENDENCIES.
- Direct dependencies only.
- The resolved snapshot format is a narrow list of exact `NAME==VERSION`
  entries; repository declarations determine which entries are in scope.
- Libyears does not install or resolve dependencies.
- Transitive dependencies are not measured by default.
- No other package ecosystems are supported.

## Development

Run the offline test suite with:

```bash
python3 -m unittest discover -s tests -v
```

See [SPEC.md](SPEC.md) for the full behavioral specification and [AGENTS.md](AGENTS.md)
for repository engineering rules.

## Policies

### Open Source Policy
We adhere to the [CMS Open Source Policy](https://github.com/CMSGov/cms-open-source-policy).
If you have any questions, just [shoot us an email](mailto:opensource@cms.hhs.gov).

### Security and Responsible Disclosure Policy
*Submit a vulnerability:* Vulnerability reports can be submitted through [Bugcrowd](https://bugcrowd.com/cms-vdp). Reports may be submitted anonymously. If you share contact information, we will acknowledge receipt of your report within 3 business days.
For more information about our Security, Vulnerability, and Responsible Disclosure Policies, see [SECURITY.md](SECURITY.md).

### Software Bill of Materials (SBOM)
A Software Bill of Materials (SBOM) is a formal record containing the details and supply chain relationships of various components used in building software.
In the spirit of [Executive Order 14028 - Improving the Nation's Cyber Security](https://www.gsa.gov/technology/it-contract-vehicles-and-purchasing-programs/information-technology-category/it-security/executive-order-14028), a SBOM for this repository is provided here: https://github.com/DSACMS/libyears/network/dependencies.
For more information and resources about SBOMs, visit: https://www.cisa.gov/sbom.

## Public Domain
This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/) as indicated in [LICENSE](LICENSE).
All contributions to this project will be released under the CC0 dedication. By submitting a pull request or issue, you are agreeing to comply with this waiver of copyright interest.
