# Remaining Tier 2 Outbound Actions

This list reflects the interactive completion session recorded in
[checklist.md](checklist.md). Approval and review outcomes there are attributed
as reported by the project owner; this repository does not contain their source
artifacts.

## Human review

- Run static code vulnerability analysis and triage any findings. The project
  owner deferred the recurring scan schedule and responsible role.
- `SECURITY.md` retains its existing unresolved policy and static-analysis
  TODOs at the project owner's direction.
- Branch/merge policy and release ownership/versioning/cadence/lifecycle remain
  deferred.

## External verification and repository administration

- Verify the CMS code.json schema accepts `contractNumber: [0]`; this exact
  value was specified by the project owner.
- After publication, record public fork and clone counts in `code.json`.
- After the public switch, verify the GitHub Pages site and dependency graph
  SBOM URL, and configure the repository About details and topics.
- Repository administrators will enable and verify Dependabot alerts, secret
  scanning, and branch protection after the public switch.
- Enable GitHub Actions after the switch, approve workflow/action dependencies
  and permissions, and verify hosted CI, Gitleaks, and repolinter runs.

## Publication and rollout

- Complete outbound review, then perform the authorized public switch.
- Prepare and distribute the required CMS announcements and add the completed
  metadata to the relevant inventory.
- Releases, packages, and deployments are not configured or available to verify.

## Optional automation

- `contributors.yml`, auto-changelog, and updateCodeJSON automation remain
  omitted. DCO is not required.
