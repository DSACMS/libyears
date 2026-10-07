# Security and Responsible Disclosure Policy

The Tier 2 scaffolder references the CMS vulnerability reporting program at
[Bugcrowd](https://bugcrowd.com/cms-vdp) and the
[HHS Vulnerability Disclosure Policy](https://www.hhs.gov/vulnerability-disclosure-policy/index.html).
Consult their scope and reporting instructions before using those channels.

TODO(TIER2): Confirm this repository's coverage by those policies, identify its
security contact and escalation path, and approve response expectations and
supported versions. The template's three-business-day acknowledgment commitment
has not been established for this project.

Do not disclose vulnerabilities, credentials, or private data in public issues.
This document does not authorize testing of systems outside an approved scope.

## Automated checks

The Gitleaks workflow scans full fetched Git history on pushes and pull requests.
Repository hygiene checks run on pushes, pull requests, and manual dispatch.
A workflow file is not evidence that a security review ran or that findings were
resolved. Gitleaks detects secrets; it is not a general code-vulnerability analysis.

TODO(TIER2): Select and run an appropriate static security-analysis tool, triage
findings, retain evidence, and establish recurring execution frequency and the
people responsible for interpreting and acting on results. Complete independent
code, credential-management, privacy, and history reviews in [checklist.md](checklist.md).
