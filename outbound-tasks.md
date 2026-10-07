### Factual metadata needed

- **code.json:** Confirm project status, license and usage classification, CMS organization, repository visibility and authorized public URL, reuse counts, supported platforms and category, maintenance model, contract number, SBOM, contact, feedback channel, AI Use Case ID, FISMA level, group, related projects and systems, healthcare subset, and user types. The current TODO values make the file fail CMS schema validation; the public repository URL is specifically unresolved.
- **README.md:** Supply approved project vision and mission, agency mission, team mission and charter, and applicable federal policy/compliance references.
- **COMMUNITY.md and .github/CODEOWNERS:** Identify accountable project contacts, roles, affiliations, maintainers, approvers, reviewers, and authorized GitHub handles. Confirm community principles.
- **CONTRIBUTING.md:** Decide whether outside contributions are accepted; provide issue/support channels; establish branching, review, release, and AI contribution policies; identify applicable policy evidence.
- **checklist.md:** Determine Tier 2 suitability; document project-specific open-source benefits, financial/security/privacy risks, and answers about PII/PHI, CMS systems, credentials, and job codes.

### Security/privacy review

- **checklist.md:** Complete independent full-history review for sensitive remarks, internal URLs/IPs, credentials, privacy, and provenance. The Gitleaks scan is limited evidence and does not complete this review.
- **SECURITY.md:** Confirm policy coverage, security contact and escalation path, response expectations, and supported versions. Select and run static security analysis; triage findings; define scan frequency and responsible reviewers.
- **CODE\_OF\_CONDUCT.md:** Approve the conduct policy and assign a private reporting contact, enforcement owner, and escalation path.

### Licensing/provenance

- **LICENSE, CONTRIBUTING.md, and checklist.md:** Establish rights ownership and provenance; have the authorized reviewer select and approve the license and contribution terms; replace the placeholder with approved license text. Complete the separate commit-history/provenance review.

### Repository settings

- **checklist.md:** Verify Dependabot and secret-scanning alerts, branch protections, branching policy, repository About details and homepage features. Confirm Actions/runners are supported and validate hosted workflows.
- **checklist.md:** Decide the disposition of tracked Python bytecode. Complete the remaining repository hygiene and code.json metadata before treating the draft as inventory-ready.

### Required approvals/sign-offs

- **checklist.md:** Obtain recommendations from at least two qualified independent code reviewers; ISSO and ISG technical approvals; and business-owner risk acceptance.
- **checklist.md:** Authorized stakeholders must complete security/privacy, national-security/intelligence, FOIA, export, TSA, and classified-information attestations; document review outcomes and dates.
- **checklist.md:** After approval, complete the required release settings, communications, and inventory tracking.
