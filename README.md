# Libyears

Libyears is a local Python CLI that measures the freshness of direct PyPI dependencies using package release dates.

## About the Project

The tool reads dependency evidence from `requirements.txt` in a local directory
(or that file directly) and retrieves release metadata from PyPI. It uses Python
3.12+ and the standard library, with no third-party runtime dependencies,
database, server, containers, or GitHub API dependency.

For each measurable dependency:

```text
libyears = (latest_stable_release_date - used_version_release_date) / 365.25 days
```

Exact versions come from requirement pins or an explicitly supplied resolved
snapshot. Unknown versions or release dates remain unmeasurable. Latest stable
selection excludes prereleases and unavailable/yanked candidates; timestamp
ordering anomalies are clamped to zero and flagged. Reports include coverage,
cumulative, mean, median, and maximum libyears. Unmeasurable dependencies are
excluded from numerical aggregates and retained in coverage statistics.

This measures dependency freshness, not vulnerability or safety. It does not
install dependencies, execute the analyzed project, or resolve an environment.
Only PyPI is supported. See [SPEC.md](SPEC.md) for the metric design; its deferred
snapshot milestone predates the implemented `--resolved` option described below.

### Project Vision

TODO(TIER2): Obtain the project owner's approved vision. The engineering guidance
prioritizes simplicity, transparency, and long-term maintainability.

### Project Mission

TODO(TIER2): Obtain the approved project mission; the implemented technical
purpose is to measure dependency freshness from repository evidence.

### Agency Mission

TODO(TIER2): Confirm agency sponsorship and include the applicable mission from
an authoritative agency source.

### Team Mission

TODO(TIER2): Identify the responsible team and its approved charter or functional statement.

## Core Team

The [project members table](COMMUNITY.md#project-members) awaits confirmed owners
and contacts. Codeowners are pending identification; see
[CODEOWNERS](.github/CODEOWNERS).

## Documentation Index

- [SPEC.md](SPEC.md): metric specification and design constraints.
- [AGENTS.md](AGENTS.md): engineering rules and test commands.
- [CONTRIBUTING.md](CONTRIBUTING.md): development and contribution guidance.
- [COMMUNITY.md](COMMUNITY.md): ownership and community guidance.
- [SECURITY.md](SECURITY.md): disclosure guidance and pending security decisions.
- [Tier 2 checklist](checklist.md): outbound review record and remaining work.

## Repository Structure

`libyears/` contains the CLI, input parsing, registry adapter, metric, and output
modules. `tests/` contains offline unittest tests. `.github/` contains repository
hygiene and secret-scanning configuration.

## Local Development

1. Install Python 3.12 or later and obtain an authorized checkout or source archive.
2. Open a terminal in the repository root. No dependency installation or build is needed.
3. Run the CLI or tests:

```sh
python --version
python -m libyears --help
python -m libyears /path/to/project
python -m libyears /path/to/project --json
python -m unittest discover -s tests -v
```

`python -m libyears .` scans this repository. It currently has no
`requirements.txt`, so no supported dependencies are discovered.
Scanning exact dependencies requires HTTPS access to the public PyPI JSON API.

An existing resolved snapshot can supply exact `NAME==VERSION` entries:

```sh
python -m libyears /path/to/project --resolved /path/to/resolved.txt
```

The snapshot does not add transitive dependencies to scope. Entries are matched
to declared direct dependencies and checked against supported constraints;
conflicts or unsupported evidence remain unmeasurable. Libyears does not create
the snapshot or infer versions from your installed environment.

Exit codes: `0` means the scan completed (including partial or zero measurement),
`1` means a usage or filesystem error, and `2` means a systemic scan failure.

## Coding Style and Linters

Follow [AGENTS.md](AGENTS.md): standard library only, focused modules, no unrelated
refactoring, and offline `unittest`/`unittest.mock` tests for behavioral changes.
Preserve metric semantics and the machine-readable JSON interface. No application
formatter or code linter is configured. Repository hygiene uses
`repolinter lint .`; see [checklist.md](checklist.md) for the pinned configuration
and validation limitations.

## Development and Software Delivery Lifecycle

Development uses the local CLI and offline tests described above.
TODO(TIER2): Confirm contribution eligibility, review requirements, branching,
release responsibilities, and delivery cadence. No release approval is implied.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development instructions and pending
contribution-policy decisions.

## Community

See [COMMUNITY.md](COMMUNITY.md) for project contacts and participation guidance.
TODO(TIER2): Confirm support and feedback channels before inviting contributors.

### Community Guidelines

The [Code of Conduct](CODE_OF_CONDUCT.md) contains the Tier 2 template conduct
guidance pending approval of its reporting and enforcement arrangements.

## Policies

### Open Source Policy

The scaffolder references the [CMS Open Source Policy](https://github.com/CMSGov/cms-open-source-policy).
TODO(TIER2): Confirm applicable policies, including accessibility/Section 508,
interoperability and anti-deficiency requirements, and record the responsible
reviewers and evidence. No compliance or accessibility assessment is asserted.

### Security and Responsible Disclosure Policy

See [SECURITY.md](SECURITY.md) for the CMS template reporting resources and
unresolved project-specific scope and response arrangements.

### Software Bill of Materials (SBOM)

No SBOM is present in the repository. The application uses only the Python
standard library; GitHub Actions tooling is separate from application dependencies.
TODO(TIER2): Determine SBOM requirements and generate/review an appropriate
inventory, including automation dependencies as applicable. A dependency graph
URL alone is not evidence of a generated SBOM.

## Public domain

TODO(TIER2): Have the authorized owner/legal reviewer select and approve a
license and contribution terms. The scaffolder proposes CC0, but this repository
contains no evidence that CC0 has been authorized. [LICENSE](LICENSE) is a
review placeholder, not a license grant or public-domain dedication.
