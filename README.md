# Libyears

Libyears measures how far direct dependency versions lag behind the latest stable
releases, using public registry timestamps. Use it to understand dependency
freshness alongside measurement coverage; age alone does not indicate security risk.

## Quick start

Use Python 3.11+ and obtain a [source checkout or archive](https://github.com/DSACMS/libyears).
Open a terminal in its root. There are no third-party runtime dependencies and no
build or installation step; run the module from that checkout:

```bash
python3 -m libyears .
python3 -m libyears /path/to/repository
```

Replace `/path/to/repository` with the directory you want to measure. Libyears reads
supported dependency files and requests public registry metadata over verified HTTPS.
It does not install dependencies or run the target project's tooling.

A report's summary looks like this illustrative example (not a live scan):

```text
Measured: 2 / 3 dependencies (66.7%)
Total:    4.12 libyears
Mean:     2.06
Median:   2.06
Maximum:  2.24
```

The report also lists measured dependencies and explains why others could not be
measured. A repository without supported evidence may return no measurement;
that is useful information, rather than a zero-age result.

## What libyears measures

For each measurable dependency, libyears compares the release time of its exact
used version with the latest stable release:

```text
libyears = max(latest stable release time - used release time, 0) / 365.25 days
```

Total is the sum of measured ages; mean is their average, median their middle
value, and maximum the largest. A dependency at the latest stable version has
exactly 0.0 libyears. Negative timestamp anomalies are clamped to zero and flagged.

Coverage is measured dependencies divided by discovered dependencies. Read it
alongside the total: 0 measured out of 7 and 7 out of 7 describe different results.
Unknown or unavailable coverage is reported as such, rather than as 0%. Unmeasurable
dependencies are excluded from numerical aggregates. [Evidence and coverage details](ECOSYSTEMS.md#common-measurement-model)
explain declarations, exact versions and source failures.

## Supported ecosystems

| Ecosystem | Direct scope and version evidence | Guide |
| --- | --- | --- |
| Python / PyPI | Root requirements.txt exact pins, or declarations plus a supplied resolved snapshot; direct-file scans supported | [Python](ECOSYSTEMS.md#python--pypi) |
| npm / Yarn Classic | Root package.json production dependencies excluding optional names; package-lock v2/v3 or Yarn Classic v1 | [npm and Yarn](ECOSYSTEMS.md#npm-and-yarn-classic) |
| RubyGems | Root Gemfile.lock direct dependencies; optional static Gemfile group selection | [RubyGems](ECOSYSTEMS.md#rubygems) |
| NuGet | Automatically attempted bounded .csproj sources with associated packages.lock.json evidence; precision interface also available | [NuGet](ECOSYSTEMS.md#nuget) |

Directory scans combine supported sources. NuGet counts each project's direct
external dependency occurrences independently, including test/tool/analyzer
references; repeated packages across projects count repeatedly. Discovery is
bounded to depth 0–4 and can leave population unknown. See the guide for exact
[discovery bounds and exclusions](ECOSYSTEMS.md#ordinary-discovery-and-witness-mappings).

## Common usage

Run these from the libyears source root; `PATH` is the target repository directory
(or a Python requirements file for direct-file scans):

```bash
python3 -m libyears PATH --json
python3 -m libyears PATH --verbose
python3 -m libyears PATH --resolved resolved.txt
python3 -m libyears PATH --ruby-group default --ruby-group test
python3 -m libyears --help
```

- `--json` emits stable schema version 3 for automation. [Example and field guidance](ECOSYSTEMS.md#json-output).
- `--verbose` adds human diagnostics without changing JSON.
- `--resolved` supplies exact Python versions while repository declarations still
  define direct scope. [Snapshot workflow](ECOSYSTEMS.md#resolved-snapshot-workflow).
- `--ruby-group` selects the union of explicitly named declared groups within a
  conservative static subset. [Group examples and restrictions](ECOSYSTEMS.md#select-declared-ruby-groups).
- For enterprise TLS, see [CA bundle configuration](ECOSYSTEMS.md#tls-and-enterprise-environments).
- For NuGet supplier testimony or precision/debugging, see [witness mappings](ECOSYSTEMS.md#ordinary-discovery-and-witness-mappings)
  and the [explicit single-project interface](ECOSYSTEMS.md#explicit-nuget-project-snapshots).

## Important limitations

- Direct dependencies only; no transitive measurement, installation or resolution.
  A declaration or range may not establish an exact version. Missing versions or
  dates remain unmeasurable; libyears does not guess them.
- Supported files and syntax are deliberately bounded. Unsupported source evidence
  can make counts/coverage unavailable while successful sibling results survive.
- Results describe supplied evidence and current observable registry history,
  not installed/deployed state, compatibility, reproducible builds or vulnerability.
  Registry record changes can change later measurements.
- Python/npm do not positively verify the applicable public namespace. Ruby requires
  supported public source authority. Ordinary NuGet may use nuget.org by disclosed
  convention after bounded repository inspection: an undisclosed private fork may
  receive the wrong public history, and queries disclose package identities.
  Known private/conflicting assignment or unknown relevant policy blocks NuGet lookup.
  [Source and comparator distinctions](ECOSYSTEMS.md#ordinary-nuget-version-age-comparator).
- Safe file-access primitives are required for bounded Ruby group/NuGet inputs.
  Unsupported hosts fail closed; Windows worker lifecycle support does not imply
  usable filesystem-reader support. [NuGet availability](ECOSYSTEMS.md#availability-and-safe-input).
- No ecosystems beyond those listed above are supported. See the [ecosystem guide](ECOSYSTEMS.md)
  for the detailed supported formats, refusal cases and evidence limits.

## Documentation Index

- [Ecosystem Guide](ECOSYSTEMS.md): evidence, detailed examples, output, TLS and limitations.
- [Specification](SPEC.md): normative metric/output contract and approved ecosystem extensions.
- [Changelog](CHANGELOG.md): notable changes; [Roadmap](ROADMAP.md): evidence-backed opportunities.
- [SDD workflow](SDD_WORKFLOW.md), [engineering rules](AGENTS.md), [agent routing](AGENT_ROUTING.md)
  and [observation protocol](observations/README.md): contributor/agent operations.
- [Methodology retrospective](specs/006-nuget-selected-evidence/methodology-retrospective.md)
  and [handoff](specs/006-nuget-selected-evidence/methodology-handoff.md): historical lessons and next-work boundaries.

## About the Project

Libyears is a small local CLI implemented with the Python standard library. It
measures direct Python, npm, RubyGems and bounded NuGet dependencies without
requiring a repository host, database or server.

Project website: https://dsacms.github.io/libyears

### Project Mission

Measure the age of direct dependencies using release timestamps from their
public registries through a small local CLI.

### Project Vision

Keep dependency freshness measurement simple, transparent, reproducible, and
maintainable, with human-readable evidence rather than guessed versions or dates.

### Agency Mission

CMS is working to modernize the nation's digital health ecosystem, including
through public infrastructure, improved data sharing and interoperability, and
collaboration that empowers people and improves care. See the
[CMS Health Technology Ecosystem overview](https://www.cms.gov/initiatives/health-technology-ecosystem/overview).

### Team Mission

The function of the CMS Open Source Program Office is to:

> Establish and maintain guidance, policies, practices, and talent pipelines
> that advance access, build trust, and amplify impact across CMS, HHS, and
> Federal Open Source Ecosystems by working and sharing openly.

### Core Team

See [Project Members](COMMUNITY.md#project-members) for contacts and roles.

## Development

### Local Development

[Getting Started](CONTRIBUTING.md#getting-started) covers setup and offline tests.
No compilation or third-party test dependencies are required.

### Coding Style and Linters

See [Coding Style and Linters](CONTRIBUTING.md#coding-style-and-linters) for
engineering guidance and configured checks.

## Contributing

External contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for
issues, pull requests, review, testing and AI assistance disclosure.

## Codeowners

Repository ownership is recorded in [.github/CODEOWNERS](.github/CODEOWNERS).

## Community

See [COMMUNITY.md](COMMUNITY.md) for community principles and roles.

### Community Guidelines

Read the [Community Guidelines](COMMUNITY.md#community-guidelines) and
[Code of Conduct](CODE_OF_CONDUCT.md) before participating.

### Governance

Current roles are in [COMMUNITY.md](COMMUNITY.md#roles--responsibilities);
review, workflow and deferred release policies are in [CONTRIBUTING.md](CONTRIBUTING.md).
There is no separate GOVERNANCE.md policy.

## Policies

### Open Source Policy

We adhere to the [CMS Open Source Policy](https://github.com/CMSGov/cms-open-source-policy).
For policy questions, contact [CMS OSPO](mailto:opensource@cms.hhs.gov).

### Security and Responsible Disclosure Policy

Read [SECURITY.md](SECURITY.md) before reporting vulnerabilities. It links the
reporting programs, scope instructions and unresolved project response expectations.
Do not disclose vulnerabilities or private data in public issues.

### Software Bill of Materials (SBOM)

An SBOM records software components and their supply chain relationships. See the
[repository dependency graph](https://github.com/DSACMS/libyears/network/dependencies),
the project's existing SBOM reference, and [CISA SBOM resources](https://www.cisa.gov/sbom).
The [Executive Order 14028 reference](https://www.gsa.gov/technology/it-contract-vehicles-and-purchasing-programs/information-technology-category/it-security/executive-order-14028)
provides context. The [outbound checklist](checklist.md) and [outstanding actions](outbound-tasks.md)
record project-health review and remaining external gates.

## Public Domain

This project is in the public domain within the United States, and copyright and
related rights worldwide are waived through the [CC0 1.0 Universal dedication](https://creativecommons.org/publicdomain/zero/1.0/)
in [LICENSE](LICENSE). Contributions are released under CC0; submitting an issue
or pull request agrees to that waiver, as described in [CONTRIBUTING.md](CONTRIBUTING.md#public-domain).
