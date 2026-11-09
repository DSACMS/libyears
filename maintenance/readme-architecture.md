# README information-architecture migration — 006-0034

## Boundary and inventory freeze

Inventory written **before README edits**, against clean starting HEAD
`0506861761b048e5e5a8d65a75d4c933d124df97` (921 lines).
Both remote main refs were read-only verified at that exact digest during this run.
The completed Feature006 methodology retrospective and handoff are therefore
published prior evidence, not a local candidate written by this lifecycle.
This bounded documentation assignment begins after that publication. Feature007
has not begun. No product, schema, CLI, target or registry work is authorized here.
Run006-0033 is the prior methodology lifecycle; next identity is **006-0034**.
No current-run ledger append or inferred runtime/credit delta is permitted.

High information value does not establish correct information location. Apply the
[actor framework](../AGENT_ROUTING.md#actors-capabilities-and-authority) to documents:
a document carries approved authority or explanation; neither detail nor repetition
creates new product authority. The author acts, fresh reviewers verify bounded
claims, the parent reconciles, and the human decides acceptance/publication.

## Document roles and authority

| Document / audience | Question and role | Authoritative there / links elsewhere | Failure if role expands |
| --- | --- | --- | --- |
| README / first-time users | What is this, how do I start, how do I interpret it? Entry + navigation | Current ordinary commands, key caveats, project identity; link guidance/contracts/policies | Important first command buried under exceptional evidence rules |
| ECOSYSTEMS / users and maintainers | Why do evidence and results differ? Explanatory + operational reference | Rich ecosystem examples and explanations; link approved contracts for exact obligations and history for rationale | Unindexed overflow or a competing normative specification |
| SPEC / implementers and integrators | What behavior is required? Normative baseline + extension index | Metric, output and core behavior; approved feature/correction contracts govern ecosystem details | Historical rationale looks like present requirements |
| specs and maintenance contracts / implementers and reviewers | What bounded change was approved? Normative / verification | Approved spec/plan/tasks and current review disposition; historical states stay attributed | Superseded gates accidentally regain authority |
| Retrospectives and discovery / maintainers and product owner | How did decisions arise, and what remains unknown? Historical / methodological | Evidence, chronology, rejected alternatives; link current contracts | Users must reconstruct current policy from history |
| CONTRIBUTING / contributors | How do I contribute and verify? Operational / participation | Setup, tests, reviews, AI disclosure, known deferred release rules | README becomes a second contributor handbook |
| COMMUNITY / participants | Who owns decisions and how do we participate? Governance | Roles, responsibilities, community principles; CODEOWNERS and CONTRIBUTING links | Invented governance or duplicate policy drifts |
| SECURITY, CODE_OF_CONDUCT, LICENSE / participants | Reporting, conduct, terms? Governance / legal artifacts | Their dedicated policy or license text; preserve explicit unresolved commitments | Navigation copy makes unsupported policy promises |
| checklist, code.json, outbound-tasks / stewards | What project-health requirements and external actions remain? Audit / metadata | Adopted Tier2 evidence, outstanding items and metadata | Documentation change mistaken for blanket maturity certification |
| ROADMAP / product owner | What opportunities exist? Decision/evidence radar | Selection state, deferred work and evidence; grants no automatic execution | Roadmap order mistaken for authorization |
| AGENTS, SDD_WORKFLOW, AGENT_ROUTING / humans and agents | What boundaries and workflow apply? Rules, lifecycle, provisional routing | Their distinct engineering/authority roles | Methodology crowds user documentation or routing becomes product policy |
| observations / recorder and analysts | What was observed and with what provenance? Operational schema + ledger | Schema and raw observations; no invented telemetry | Account boundaries become fictional task billing |

## Destination decisions

SPEC is normative in actual use (MUST/SHOULD, metric, schema, failure and extension
contracts), with intentionally retained original-MVP examples and superseding
extension references. It already contains the needed normative statements. Moving
rich README explanations/history into it would overload it and confuse authority.
Only navigation references will change; no normative text is migrated or weakened.

One **ECOSYSTEMS.md** is the smallest coherent missing home: no existing document
combines current cross-ecosystem guidance, examples, source distinctions and
operational reporting. Feature specs are normative and retrospectives historical;
neither answers that explanatory question. Use a shared model, shared reporting /
registry access, then Python, npm, RubyGems and NuGet with a short contents index.
No docs/ hierarchy or per-ecosystem files are justified. Preserve current technical
text substantially verbatim, adding scope labels where inherited historical claims
could mislead. Keep the historical event route as current v1 usage guidance,
linked to its historical rationale; do not copy the Feature Story.

## Frozen section migration map

Types: 1 entry; 2 normative contract; 3 ecosystem explanation; 4 historical rationale;
5 project/governance; 6 operational reference. Mixed rows distinguish explanation
from its controlling contract. Original line spans locate text at the frozen HEAD,
not future edited line numbers. Every heading is inventoried, followed below by
meaningful unheaded subsections with independent loss risks.

| Current heading / location | Purpose | Audience | Type | In README? | Existing canonical home | Proposed destination | Action | Knowledge-loss risk | References |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Libyears (L1–2) | Purpose, first command, interpretation or key caveats | New users | 1 entry | Summary only | README; SPEC for contract | README | Shorten + link richer detail to ECOSYSTEMS | High for Basic usage: preserve discovery and witness details | Update inbound README anchors; same-root destinations preserve relative links |
| About the Project (L3–11) | Purpose, first command, interpretation or key caveats | New users | 1 entry | Summary only | README; SPEC for contract | README | Shorten + link richer detail to ECOSYSTEMS | High for Basic usage: preserve discovery and witness details | Update inbound README anchors; same-root destinations preserve relative links |
| Agency Mission (L12–19) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| Team Mission (L20–27) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| Project Mission (L28–32) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| Project Vision (L33–37) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| Core Team (L38–41) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| What libyears measures (L42–54) | Purpose, first command, interpretation or key caveats | New users | 1 entry | Summary only | README; SPEC for contract | README | Shorten + link richer detail to ECOSYSTEMS | High for Basic usage: preserve discovery and witness details | Update inbound README anchors; same-root destinations preserve relative links |
| Important concept: version evidence (L55–70) | Evidence, scope, source authority, examples and limitations | Users / ecosystem maintainers | 3 explanation + 2 contract reference | Summary only | SPEC §26 and approved feature/maintenance specs govern; no complete explanatory home | ECOSYSTEMS matching ecosystem section | Move rich text; README summary + link | High: preserve examples, refusals, assurance distinctions, numeric bounds | Update inbound README anchors; same-root destinations preserve relative links |
| Basic usage (L71–116) | Purpose, first command, interpretation or key caveats | New users | 1 entry | Summary only | README; SPEC for contract | README | Shorten + link richer detail to ECOSYSTEMS | High for Basic usage: preserve discovery and witness details | Update inbound README anchors; same-root destinations preserve relative links |
| Exact-pinned requirements (L117–125) | Evidence, scope, source authority, examples and limitations | Users / ecosystem maintainers | 3 explanation + 2 contract reference | Summary only | SPEC §26 and approved feature/maintenance specs govern; no complete explanatory home | ECOSYSTEMS matching ecosystem section | Move rich text; README summary + link | High: preserve examples, refusals, assurance distinctions, numeric bounds | Update inbound README anchors; same-root destinations preserve relative links |
| Resolved snapshot workflow (L126–140) | Evidence, scope, source authority, examples and limitations | Users / ecosystem maintainers | 3 explanation + 2 contract reference | Summary only | SPEC §26 and approved feature/maintenance specs govern; no complete explanatory home | ECOSYSTEMS matching ecosystem section | Move rich text; README summary + link | High: preserve examples, refusals, assurance distinctions, numeric bounds | Update inbound README anchors; same-root destinations preserve relative links |
| TLS and enterprise environments (L141–165) | Trust configuration, diagnostics and schema example | Users / automation authors | 6 operational/reporting reference + 1 usage | Summary only | SPEC §§8,17; README examples | ECOSYSTEMS shared reporting / registry access | Move rich text; retain common options in README | High: retain CA precedence, full JSON example and worker exception | Update inbound README anchors; same-root destinations preserve relative links |
| Verbose diagnostics (L166–175) | Trust configuration, diagnostics and schema example | Users / automation authors | 6 operational/reporting reference + 1 usage | Summary only | SPEC §§8,17; README examples | ECOSYSTEMS shared reporting / registry access | Move rich text; retain common options in README | High: retain CA precedence, full JSON example and worker exception | Update inbound README anchors; same-root destinations preserve relative links |
| JSON output (L176–232) | Trust configuration, diagnostics and schema example | Users / automation authors | 6 operational/reporting reference + 1 usage | Summary only | SPEC §§8,17; README examples | ECOSYSTEMS shared reporting / registry access | Move rich text; retain common options in README | High: retain CA precedence, full JSON example and worker exception | Update inbound README anchors; same-root destinations preserve relative links |
| Measurement coverage (L233–239) | Purpose, first command, interpretation or key caveats | New users | 1 entry | Summary only | README; SPEC for contract | README | Shorten + link richer detail to ECOSYSTEMS | High for Basic usage: preserve discovery and witness details | Update inbound README anchors; same-root destinations preserve relative links |
| npm support (L240–271) | Evidence, scope, source authority, examples and limitations | Users / ecosystem maintainers | 3 explanation + 2 contract reference | Summary only | SPEC §26 and approved feature/maintenance specs govern; no complete explanatory home | ECOSYSTEMS matching ecosystem section | Move rich text; README summary + link | High: preserve examples, refusals, assurance distinctions, numeric bounds | Update inbound README anchors; same-root destinations preserve relative links |
| RubyGems support (L272–327) | Evidence, scope, source authority, examples and limitations | Users / ecosystem maintainers | 3 explanation + 2 contract reference | Summary only | SPEC §26 and approved feature/maintenance specs govern; no complete explanatory home | ECOSYSTEMS matching ecosystem section | Move rich text; README summary + link | High: preserve examples, refusals, assurance distinctions, numeric bounds | Update inbound README anchors; same-root destinations preserve relative links |
| Select declared Ruby groups (L328–437) | Evidence, scope, source authority, examples and limitations | Users / ecosystem maintainers | 3 explanation + 2 contract reference | Summary only | SPEC §26 and approved feature/maintenance specs govern; no complete explanatory home | ECOSYSTEMS matching ecosystem section | Move rich text; README summary + link | High: preserve examples, refusals, assurance distinctions, numeric bounds | Update inbound README anchors; same-root destinations preserve relative links |
| Ordinary NuGet version-age comparator (L438–475) | Evidence, scope, source authority, examples and limitations | Users / ecosystem maintainers | 3 explanation + 2 contract reference | Summary only | SPEC §26 and approved feature/maintenance specs govern; no complete explanatory home | ECOSYSTEMS matching ecosystem section | Move rich text; README summary + link | High: preserve examples, refusals, assurance distinctions, numeric bounds | Update inbound README anchors; same-root destinations preserve relative links |
| Explicit NuGet project snapshots (L476–633) | Evidence, scope, source authority, examples and limitations | Users / ecosystem maintainers | 3 explanation + 2 contract reference | Summary only | SPEC §26 and approved feature/maintenance specs govern; no complete explanatory home | ECOSYSTEMS matching ecosystem section | Move rich text; README summary + link | High: preserve examples, refusals, assurance distinctions, numeric bounds | Update inbound README anchors; same-root destinations preserve relative links |
| Qualified current repository snapshots (L634–675) | Evidence, scope, source authority, examples and limitations | Users / ecosystem maintainers | 3 explanation + 2 contract reference | Summary only | SPEC §26 and approved feature/maintenance specs govern; no complete explanatory home | ECOSYSTEMS matching ecosystem section | Move rich text; README summary + link | High: preserve examples, refusals, assurance distinctions, numeric bounds | Update inbound README anchors; same-root destinations preserve relative links |
| Explicitly accepted resolved-snapshot fallback (B2) (L676–851) | Evidence, scope, source authority, examples and limitations | Users / ecosystem maintainers | 3 explanation + 2 contract reference | Summary only | SPEC §26 and approved feature/maintenance specs govern; no complete explanatory home | ECOSYSTEMS matching ecosystem section | Move rich text; README summary + link | High: preserve examples, refusals, assurance distinctions, numeric bounds | Update inbound README anchors; same-root destinations preserve relative links |
| Current limitations (L852–866) | Purpose, first command, interpretation or key caveats | New users | 1 entry | Summary only | README; SPEC for contract | README | Shorten + link richer detail to ECOSYSTEMS | High for Basic usage: preserve discovery and witness details | Update inbound README anchors; same-root destinations preserve relative links |
| Development (L867–868) | Development setup and verification | Contributors | 5 project operations | Yes | CONTRIBUTING; AGENTS | README Development links → CONTRIBUTING | Deduplicate offline suite instruction to CONTRIBUTING | Low: canonical suite command retained; use compact output | Update inbound README anchors; same-root destinations preserve relative links |
| Local Development (L869–881) | Development setup and verification | Contributors | 5 project operations | Yes | CONTRIBUTING; AGENTS | README Development links → CONTRIBUTING | Deduplicate offline suite instruction to CONTRIBUTING | Low: canonical suite command retained; use compact output | Update inbound README anchors; same-root destinations preserve relative links |
| Coding Style and Linters (L882–886) | Development setup and verification | Contributors | 5 project operations | Yes | CONTRIBUTING; AGENTS | README Development links → CONTRIBUTING | Deduplicate offline suite instruction to CONTRIBUTING | Low: canonical suite command retained; use compact output | Update inbound README anchors; same-root destinations preserve relative links |
| Contributing (L887–890) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| Codeowners (L891–894) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| Community (L895–898) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| Community Guidelines (L899–903) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| Policies (L904–905) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| Open Source Policy (L906–909) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| Security and Responsible Disclosure Policy (L910–913) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| Software Bill of Materials (SBOM) (L914–918) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |
| Public Domain (L919–921) | Project identity, participation or policy discovery | Contributors / project stewards | 5 governance | Yes | COMMUNITY / CONTRIBUTING / SECURITY / LICENSE as applicable | README project resources | Retain heading and concise content/link | Low: canonical files retained | Update inbound README anchors; same-root destinations preserve relative links |

### Meaningful unheaded subsections

| Original location | Role / audience | Destination and action | Loss risk / reference obligations |
| --- | --- | --- | --- |
| Basic usage L80–115: occurrence scope, discovery bounds/exclusions, witness mappings, null coverage | 3 + contract reference / NuGet users | ECOSYSTEMS NuGet ordinary discovery; README keeps ordinary command and occurrence warning | High: keep exact bounds, mappings, no traversal, known/unknown and sibling semantics; link precision interface |
| JSON L183–231: full Python-only payload | 6 reporting / automation users | ECOSYSTEMS JSON output, verbatim payload with explicit synthetic label | High: preserve schema3 and all field/value examples; timestamps are illustrative, not registry observations |
| Ruby groups L364–436: Gemfile, output, JSON, association/refusal examples | 3 + contract reference / scoped Ruby users | ECOSYSTEMS Ruby group subsection, preserve all examples | High: no loss of null/omitted distinction, requirement equality, default selection or limits |
| NuGet L521–632: v1/v2 templates and event/snapshot distinctions | 3 + 4 linked rationale / precision users | ECOSYSTEMS explicit precision + witness subsections | High: retain every field, replay prohibition, assertion-not-authentication and minimum-floor distinctions |
| NuGet L706–727: v3 template and accountable scope | 3 + contract reference / snapshot users | ECOSYSTEMS B2 subsection | High: preserve complete envelope and absence of A completeness requirement |
| NuGet L745–758: created-date and latest/normalization semantics | 3 + contract reference / NuGet users | ECOSYSTEMS dates and versions | High: no date/ordering/compatibility weakening |
| NuGet L760–804: singleton vs ordinary schema, assurance, cross-ecosystem differences | 3 + 6 / automation users | ECOSYSTEMS output and assurance | High: preserve source IDs, safe staged facts, assurance versus measurement and namespace limitations |
| NuGet L806–820: denominator, sibling, exit and reader capability rules | 3 + contract reference / users | ECOSYSTEMS availability and safe input | High: unknown versus unavailable versus zero, worker support does not prove reader support |
| NuGet L822–850: numeric bounds, network, supervision and CA exception | 6 + contract reference / maintainers and operators | ECOSYSTEMS enforced bounds and metadata access | High: retain entire table, timeout exclusions and explicit CA not forwarded |
| README L906–917: CMS policy, disclosure commitment, SBOM explanation and links | 5 / participants | README concise links; SECURITY remains canonical for reporting caveats; SBOM resources remain linked | Existing README promises three-day response but SECURITY explicitly says unestablished. Deduplicate to SECURITY rather than repeat unsupported commitment; preserve Bugcrowd discovery there |
| README L919–921: public domain and contribution waiver | 5 / users and contributors | Retain README license statement; CONTRIBUTING retains submission waiver; LICENSE exact terms | High if legal meaning changed: no terms changed |

## Adopted maturity requirements

Sources: repository [checklist](../checklist.md#review-content) pinned to
[official Tier2 checklist](https://github.com/DSACMS/repo-scaffolder/blob/14e2a01482084da7bc1a5aac825e2f1ea23e8529/tier2/checklist.md)
and [resolved repolinter rules](../repolinter.json). The adopted local copies are
inspectable authority; availability of a current upstream page is not assumed.
README error-level checks require About the Project, Project Vision, Project
Mission, Agency Mission, Team Mission, Core Team, Local Development, Coding Style
and Linters, Contributing, Codeowners, Community, Community Guidelines, Policies,
Open Source Policy, Security and Responsible Disclosure Policy, Public Domain,
and Software Bill of Materials. Retain substantive short sections, not hidden
keyword stuffing. Contributor/community/policy references may link canonical files;
mission/vision context stays in README. Preserve public-domain terms and all
SBOM context links. Warning-level optional headings do not require whole documents
embedded in README; improve Documentation Index and Governance discovery.
GOVERNANCE.md does not exist and its configured checks are off (template: Tier3).
Use existing COMMUNITY roles and CONTRIBUTING decision/deferred-policy facts;
do not fabricate a governance policy or create a redundant file to satisfy a name.
This audit preserves documented requirements; it is not a fresh certification of
all external, security or maturity gates. No package managers or CI changes.

## Reconciliation and verification

At inventory freeze, candidate implementation and independent review were pending.
The completed migration and independent review are recorded in
[the review record](readme-architecture-reviews.md). The inventory above retains
its original proposed classifications and locators; corrections are explicit below.


### Locator correction and completed migration

Independent Reviewer F identified inaccurate ranges in five unheaded-subsection
rows of the frozen map. These are inventory locator errors, not missing migrated
content. The following ranges at original HEAD0506861 supersede those locators;
the frozen history and original rows remain inspectable.

| Original block | Correct frozen README location | Final destination |
| --- | --- | --- |
| v3 template and accountable scope | L685–699 template; L701–706 scope | [B2 / v3](../ECOSYSTEMS.md#explicitly-accepted-resolved-snapshot-fallback-b2) |
| Dates, latest and normalization | L734–747 | [Dates and versions](../ECOSYSTEMS.md#dates-and-versions) |
| Output, assurance and cross-ecosystem distinctions | L749–799 | [Output and assurance](../ECOSYSTEMS.md#output-and-assurance) |
| Availability, failure and safe input | L801–817 | [Availability and safe input](../ECOSYSTEMS.md#availability-and-safe-input) |
| Numeric bounds and metadata supervision | L819–850 | [Bounds](../ECOSYSTEMS.md#enforced-bounds) and [metadata access](../ECOSYSTEMS.md#metadata-access-and-supervision) |

All inventory dispositions are implemented. README retains the first-use path,
metric/coverage interpretation, ecosystem table, common options, key limitations,
required mission/identity statements and project-resource links. ECOSYSTEMS retains
the rich explanatory/operational reference and all ecosystem examples. SPEC has
only three destination substitutions. CONTRIBUTING now owns the compact offline
test instruction and links the user documentation roles. Two historical Ruby
retrospective links were repaired without changing its narrative. No Feature006
Feature Story or methodology handoff was rewritten.

Deduplication: README's verbose development test command delegates to CONTRIBUTING;
CONTRIBUTING's test command now uses repository-default compact output. README and
CONTRIBUTING delegate security reporting and unresolved response expectations to
SECURITY; neither repeats the inherited unestablished three-day promise. This
resolves an existing contradiction without establishing a new commitment. LICENSE,
COMMUNITY, conduct, security and maturity-rule files are unchanged.

Knowledge reconciliation: fresh Reviewer B accounted for all114 original
non-heading content blocks,98 verbatim after whitespace normalization and16
individually compared. The20 original fenced examples remain available, apart
from the intentionally compacted contributor test command; the guide retains18
transferred ecosystem/example blocks byte-for-byte at the initial candidate.
The README summary is an additional illustrative example, corrected against
actual mocked CLI output. No material knowledge loss was found. See the review
record for scope, correction freezes and verification limits.
