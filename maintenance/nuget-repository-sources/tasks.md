# Repository-source tasks — 006-0022

Approved spec/plan digests and independent dispositions: reviews.md. Candidate
graph; approval in that record. Execute sequentially, one local commit per task;
no push. Existing Feature006 and recognition task IDs are unchanged.

- [x] **N1 — Anchored independent sources.** Predecessor: graph approval.
  R1/R2/R3/R6: add repository source module, anchored scoped-reader hook/subclass,
  optional source-reader injection and source identity fields. Complete/missing/
  unknown source inventories and unmatched mappings; unchanged parser/H3. Implement
  mapping validation helper for reuse by CLI/scan. Add portable fixture tests for
  all-source attempts/identities/unknown-vs-known/witness refusal and separate
  actual anchored directory/link/reparse/replacement/cleanup plus unskipped
  primitive-refusal tests. Reuse existing traversal bounds witnesses. Focused:
  repository-source/source/input/project/provenance/discovery tests. Check diff,
  commit. No CLI automatic activation until N2.

- [x] **N2 — Occurrence composition and public output.** Predecessor: N1.
  R1–R6: repository scan activation and early request validation; one batch with
  FIFO per-capability results; per-source/combined NuGet summaries; exact CLI
  witness option and automatic human/JSON directory mode; safe failures and
  root/diagnostic suppression. Implement additive source collection, row/error
  source IDs and escaped human source summaries/details. Keep explicit/direct-
  file/other-ecosystem output compatible. Add tests with implementation: equal
  names/versions/different versions, duplicate equal capabilities with differing
  outcomes, source and ecosystem siblings, unknown/unavailable/accepted empty/
  failed/partial/full, mappings/errors/no implicit authority, exact legacy JSON
  comparison and privacy. Adjust obsolete ordinary nonactivation witnesses to
  new authorized behavior; keep semantic tests injected and real refusal tests
  unskipped. Focused repository/scan/CLI/output/mixed/scoped/worker tests, full
  deterministic suite and full capability-disabled simulation at integration
  boundary; inspect diff/check and commit.

- [x] **N3 — Documentation and operational validation.** Predecessor: N2.
  R1–R6: update README/SPEC/AGENTS/CHANGELOG/ROADMAP at this checkpoint, with
  additive v3 contract, bounds, occurrence weighting, explicit acceptance and
  null semantics; preserve frozen original feature artifacts. Run focused/full
  deterministic/capability-disabled and dedicated real-worker lifecycle checks
  as necessary for final candidate; exact ordinary OASim command, raw output
  capture and required final manifest equality against captured pre-state.
  No target execution/evidence generation or cleaning existing state. Record
  requirement-to-test/evidence reconciliation, actual results and limits in
  validation.md. Diff/check, commit; run canonical GitLeaks history gate on
  committed candidate. Freeze candidate code/tests/docs/evidence for N4.

- [ ] **N4 — Independent implementation/convergence.** Predecessor: N3.
  Fresh read-only non-author review of R1–R6, authority/digests, implementation,
  tests/docs, schema compatibility, operational output/integrity and verification.
  Parent reconciles findings and all obligations. Bounded determined corrections
  get separate commits, focused regressions, freeze and fresh non-author review;
  new consequential authority stops. Do not claim a passed gate from incomplete
  audit. Record convergence and any limitations; ensure final diff/history checks,
  clean tree after final authorized commit, no push, current 44-key observation
  handoff outside Git (do not append current run). Next human gate: publication
  authorization and subsequent hosted Windows/other CI evidence.

Every R1–R6 obligation is jointly owned by N1/N2 behavior/tests and N3 evidence,
then reconciled at N4. Real OASim witness is required under explicit current access
authority; useful positive live yield, numeric coverage and hosted CI are not
local acceptance predecessors. No implementation can loosen H3 or infer population.

N1 verification: 97 focused tests PASS (sources/source/input/project/provenance/
discovery); no skips. Added portable semantics and real anchored ancestor/reparse/
replacement/cleanup plus unskipped capability refusal. Diff check PASS.

N2 verification: 195 focused tests PASS; full 683 PASS, no skips; full
capability-disabled 683 successful, 48 genuine filesystem skips. Semantic tests
use injected inventories/readers; unskipped refusal and real filesystem/worker
witnesses remain. Exact pre-implementation explicit JSON fixture matches.
Integration found/fixed measured-count loss with unknown sibling population;
obsolete nonactivation expectations and Ruby CLI inventory assumptions corrected
without weakening actual primitive-refusal witnesses. Diff check PASS.

N3 code/test verification reuses unchanged N2 final 683/683 capability results;
separate real-worker 3 PASS. Exact ordinary OASim exit0/empty stderr, ten automatic
attempts, eight unknown and two known-but-unavailable populations; repository
null coverage. Exact captured target before/after equality PASS. Documentation
checkpoint complete; GitLeaks executed on N3 commit and recorded in reviews.md.
