# How to Contribute

Read [README.md](README.md), [AGENTS.md](AGENTS.md), and the pending
[licensing decision](LICENSE) before preparing a contribution.
TODO(TIER2): Confirm whether external contributions are accepted, the submission
and support channels, and contribution licensing terms.

## Getting Started

Obtain an authorized checkout or source archive and open a terminal at its root.
Use Python 3.12+. See [Local Development](README.md#local-development) for CLI examples.

### Building dependencies

There are no third-party runtime or test dependencies to install. Tests use
`unittest` and `unittest.mock` from the standard library.

### Building the Project

No compilation, packaging, or build step is configured. Run from the repository root:

```sh
python -m libyears --help
python -m unittest discover -s tests -v
```

### Workflow and Branching

The inspected checkout uses `main`.
TODO(TIER2): Approve the branch/merge workflow, review rules, and contribution
eligibility. Git history alone does not establish those policies.

### Testing Conventions

Tests are in `tests/` and must run without network access. Add tests for behavioral
changes, run the narrowest relevant tests first, and run the full suite when
appropriate. Use mocked registry responses. Report commands and outcomes in the PR.

### Coding Style and Linters

Follow [AGENTS.md](AGENTS.md). Keep modules small; do not add third-party
application dependencies or unrelated refactors. Keep network operations behind
registry adapters and human output separate from JSON serialization. No Python
formatter or linter is currently configured. Repository checks use `repolinter lint .`.

### Writing Issues

Use the [issue template](.github/ISSUE_TEMPLATE.md) to describe expected behavior,
actual behavior, and reproducible steps with synthetic examples.
TODO(TIER2): Confirm the issue tracker and development support destination.
Security disclosures follow [SECURITY.md](SECURITY.md).

### Writing Pull Requests

Use the [pull request template](.github/PULL_REQUEST_TEMPLATE.md) to explain the
problem, solution, result, validation, and AI assistance where applicable.

### Reviewing Pull Requests

TODO(TIER2): Identify authorized reviewers and merge approvers and configure
branch protections. Routine PR review does not replace independent outbound review.

## Shipping Releases

TODO(TIER2): Define release ownership, versioning, cadence, support lifecycle, and
approval workflow. Complete the [outbound checklist](checklist.md) before release.

## Documentation

Preserve useful existing documentation and document behavior from repository
evidence. [SPEC.md](SPEC.md) describes the metric; [README.md](README.md) describes
current CLI use, including resolved snapshots added after the specification.

## AI Usage

The Tier 2 PR template includes disclosure of AI assistance and its scope.
TODO(TIER2): Confirm the project's AI contribution policy; contributors remain
responsible for understanding and verifying submitted changes.

## Policies

### Open Source Policy

Review the [CMS Open Source Policy](https://github.com/CMSGov/cms-open-source-policy).
TODO(TIER2): Confirm policy applicability and required compliance evidence; see
[README policies](README.md#policies).

### Security and Responsible Disclosure Policy

See [SECURITY.md](SECURITY.md). Do not post credentials or sensitive information
in issues or pull requests.

## Public domain

TODO(TIER2): Approve licensing and contribution terms and replace [LICENSE](LICENSE)
with the approved text. No CC0 dedication or contributor waiver is asserted.
