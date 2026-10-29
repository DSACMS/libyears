# How to Contribute

External contributions are accepted. Open a pull request directly against
`github.com/DSACMS/libyears`. Read [README.md](README.md), [AGENTS.md](AGENTS.md),
and [LICENSE](LICENSE) before preparing a contribution. Contributions are
released under CC0 1.0 Universal as described in [Public Domain](#public-domain).

## Getting Started

Obtain an authorized checkout or source archive and open a terminal at its root.
Use Python 3.11+. See [Development](README.md#development) for CLI examples.

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
The branch and merge workflow, review rules, and contribution eligibility
policy are deferred for later decision. Git history alone does not establish
those policies.

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
File project issues at
https://github.com/DSACMS/libyears/issues. For CMS OSPO support, email
[opensource@cms.hhs.gov](mailto:opensource@cms.hhs.gov).
Security disclosures follow [SECURITY.md](SECURITY.md).

### Writing Pull Requests

Use the [pull request template](.github/PULL_REQUEST_TEMPLATE.md) to explain the
problem, solution, result, validation, and AI assistance where applicable.

### Reviewing Pull Requests

`@decause-gov` is the identified project reviewer and approver. Repository
administrators will configure branch protections after the repository becomes
public. Routine PR review does not replace independent outbound review.

## Shipping Releases

Release ownership, versioning, cadence, support lifecycle, and approval workflow
are deferred. Complete the [outbound checklist](checklist.md) before release.

## Documentation

Preserve useful existing documentation and document behavior from repository
evidence. [SPEC.md](SPEC.md) describes the metric; [README.md](README.md) describes
current CLI use, including resolved snapshots added after the specification.

## AI Usage

Disclose AI assistance and its scope in the pull request template. Add the
`AI-assisted` label when a pull request contains AI-generated code. Contributors
remain responsible for understanding and verifying submitted changes.

See [AGENT_ROUTING.md](AGENT_ROUTING.md) for a provisional working strategy on
agent capability, context, and review structure; existing quality gates remain
unchanged.

## Policies

### Open Source Policy
We adhere to the [CMS Open Source Policy](https://github.com/CMSGov/cms-open-source-policy).
If you have any questions, just [shoot us an email](mailto:opensource@cms.hhs.gov).

### Security and Responsible Disclosure Policy
*Submit a vulnerability:* Vulnerability reports can be submitted through [Bugcrowd](https://bugcrowd.com/cms-vdp). Reports may be submitted anonymously. If you share contact information, we will acknowledge receipt of your report within 3 business days.
 For more information about our Security, Vulnerability, and Responsible Disclosure Policies, see [SECURITY.md](SECURITY.md).

See [SECURITY.md](SECURITY.md). Do not post credentials or sensitive information
in issues or pull requests.

## Public Domain
This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/) as indicated in [LICENSE](LICENSE).
 All contributions to this project will be released under the CC0 dedication. By submitting a pull request or issue, you are agreeing to comply with this waiver of copyright interest.

DCO sign-off is not required for contributions.
