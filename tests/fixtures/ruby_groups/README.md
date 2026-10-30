# Synthetic Ruby group fixtures

These small fixtures demonstrate only supplied-file declaration membership.
They do not describe an application, installation, runtime, deployment, or
publication history. The checked-in Gemfiles exercise recognition; composed
tests create their small root Gemfile/lock pairs in temporary directories.

| Fixture | Expected recognition / selected population |
|---|---|
| `memberships.Gemfile` | Accepted. `default` selects rack; `test` or `development` selects rake and debug; `Test` selects debug; `bench` selects none. `default` plus `test` selects rack, rake and debug once each. All five names are established, preserving case. Optionality does not change membership. |
| `duplicate.Gemfile` | Reject all scope with `duplicate_gemfile_declaration`, line 5. No partial rack population. |
| `unsupported.Gemfile` | Reject all scope with `unsupported_gemfile_syntax`, line 5, including when `unselected` was not requested. No partial rack population. |

## Deterministic acceptance index (T010)

Paths below are relative to `tests/`. Every named witness asserts behavior;
this index does not substitute for running it. Parser negative tables and
cross-stage precedence witnesses remain separate. This is synthetic offline
acceptance evidence, not the later required authorized real-root example.

Aliases for test locations:

- **P**: `test_gemfile.GemfileParserTests`
- **R**: `test_ruby_groups.ScopedRubyReadTests`
- **S**: `test_ruby_groups.ScopedSourceAvailabilityTests`
- **A**: `test_ruby_groups.ScopedLockAssociationTests`
- **M**: `test_scoped_scan.ScopedScanTests`
- **C**: `test_cli.ScopedRubyCLITests`
- **O**: `test_output.ScopedRubyJsonTests`
- **X**: `test_ruby_group_acceptance.RubyGroupAcceptanceTests`
- **G**: `test_rubygems_registry` (class specified below)

| Criterion | Concrete witnesses / assertions |
|---|---|
| AC-01 | M.`test_ordinary_path_never_opens_gemfile_and_retains_source_call`; `test_rubygems.RootSourceTests.test_lock_only_and_gemfile_presence_have_identical_unchanged_results`. Absent, accepted and arbitrary Gemfiles have identical ordinary results with no read. |
| AC-02 | C.`test_explicit_exact_groups_union_duplicates_and_expected_age`; X.`test_real_adapter_population_reaches_scoped_cli_with_platform_dates`. Exact direct identity, Test/test distinction, expected age and public artifact provenance reach CLI JSON. |
| AC-03 | P.`test_explicit_default_group_is_an_ordinary_membership`; X.`test_root_read_allowlist_integrity_and_no_implicit_production_or_default`. Explicit test/default/production each selects exactly its own dependency. |
| AC-04 | S.`test_union_deduplicates_and_retains_full_memberships_without_default`; C.`test_explicit_exact_groups_union_duplicates_and_expected_age`. Overlapping block/option memberships yield one count/row/lookup. |
| AC-05 | C.`test_explicit_exact_groups_union_duplicates_and_expected_age`; M.`test_scoped_request_is_canonical_and_chooses_only_scoped_source`. Repeated/multiple requests select the union and serialize sorted unique names. |
| AC-06 | S.`test_known_empty_absent_and_accepted_lock_and_rejected_lock`; O.`test_empty_scopes_keep_requested_inputs_and_recognition_state`. Empty named/default scope, N=0, null coverage; rejected lock retains unavailable measurement. |
| AC-07 | S.`test_complete_recognition_then_unknown_group_prevents_lock_read`; X.`test_cli_precedence_stages_safe_output_and_successful_siblings` (unknown). One error, unknown N, no partial union/lock recognition/lookup. |
| AC-08 | P.`test_all_literal_and_require_options_preserve_requirements`, `test_all_group_option_forms_and_orderings`, `test_whitespace_comments_lf_crlf_and_no_final_newline`; P negative tables `test_unsupported_statement_families_never_return_partial_scope`, `test_unsupported_calls_options_expressions_and_trailing_tokens`, `test_malformed_recognized_forms`, `test_literals_reject_escapes_interpolation_and_newlines`, `test_first_physical_line_defect_precedes_completion_defects`, `test_physical_line_byte_limit_exact_one_over_and_crlf`; R.`test_byte_limits_are_exact_and_reads_stop_at_limit_plus_one`. Positive closed subset, unselected code, completion precedence and limits are independently exercised. |
| AC-09 | P.`test_block_membership_unions_and_optional_flags`, `test_nested_blocks_and_unselected_code_reject`; X root read allowlist test. Optional true/false retain declared membership without config reads; nesting rejects. |
| AC-10 | P.`test_duplicates_anywhere_reject_without_merging`; S.`test_rejected_entire_lock_preserves_known_scope_even_for_excluded_rows`. Identical/conflicting/cross-group declarations and whole-lock duplicate-direct rejection. |
| AC-11 | S.`test_safe_read_reasons_map_to_source_without_salvage`; R.`test_escaping_links_never_open_or_read_target`, `test_nonregular_dangling_and_unreadable_are_safe_failures`; S.`test_gemfile_fifo_replacement_composes_unknown_scope_and_no_lock_read`. Correct source reasons, unknown N and no lookup including P1. |
| AC-12 | S.`test_missing_lock_keeps_pins_as_unmeasurable_safe_declarations`, `test_known_empty_absent_and_accepted_lock_and_rejected_lock`; X precedence (absent lock). Known names retained, no pin fallback; absent lock with N=0 is empty. |
| AC-13 | A.`test_missing_direct_identity_cannot_use_transitive_spec_or_pin`; X precedence (missing direct). Exact missing direct identity cannot use matching transitive spec or declaration pin. |
| AC-14 | A.`test_excluded_and_lock_only_identities_never_become_candidates`, `test_textual_mismatch_table_preserves_both_safe_values_without_artifacts`; O.`test_mismatch_preserves_both_literal_values_without_version_artifacts`; X precedence (mismatch). Null/text, term order, whitespace, operators, equal multiple literals and safe mismatch wording. |
| AC-15 | M.`test_availability_matrix_with_and_without_successful_siblings`; S.`test_rejected_entire_lock_preserves_known_scope_even_for_excluded_rows`; A.`test_existing_isolated_selection_failures_keep_scope_and_artifact_rules`. Known N including zero, null unavailable measurements versus isolated failures. |
| AC-16 | A.`test_lock_authority_prefix_precedes_mismatch_and_selected_evidence`, `test_f1_nonpublic_gemfile_precedes_missing_direct_after_lock_acceptance`; X precedence (F1/local authority). Private/mixed/pinned/GIT/PATH/multiple-remote sources never authorize public namesakes. |
| AC-17 | M.`test_availability_matrix_with_and_without_successful_siblings`; O.`test_human_empty_unavailable_and_wholly_unmeasurable_remain_distinct`. Empty/null, unknown/unavailable and known N/0% remain distinct. |
| AC-18 | M.`test_availability_matrix_with_and_without_successful_siblings`; X precedence (all stages with/without siblings). Python/npm rows and numeric totals survive while unknown denominator and unavailable coverage rules remain. |
| AC-19 | M.`test_three_ecosystems_keep_same_name_and_snapshot_python_only`; C.`test_resolved_remains_python_only_and_verbose_json_is_identical`; full suite including `test_pypi`, `test_npm`, `test_npm_registry`, `test_yarn`, `test_mixed_scan`. Existing ecosystems, Yarn conflict and same-name isolation remain covered. |
| AC-20 | O.`test_human_measured_scope_and_evidence_match_json_in_both_branches`, `test_human_empty_unavailable_and_wholly_unmeasurable_remain_distinct`, `test_human_failures_retain_safe_metadata_and_omit_unsupported_text`, `test_human_source_reasons_are_contextual_and_safe`; X precedence. Paired single/mixed normal/verbose output, source labels, safe requirements and counts. |
| AC-21 | O.`test_source_evidence_presence_and_null_format_across_unavailable_states`, `test_empty_scopes_keep_requested_inputs_and_recognition_state`, `test_missing_lock_and_missing_direct_omit_unknown_requirement`, `test_measured_evidence_keeps_full_memberships_requirement_order_and_artifacts`, `test_known_absent_requirement_is_null_on_success_local_and_registry_failure`, `test_f1_and_f2_preserve_safe_evidence_and_never_echo_unsafe_text`, `test_scoped_failures_retain_only_established_artifact_populations`, `test_mismatch_preserves_both_literal_values_without_version_artifacts`, `test_ordinary_ruby_shape_is_unchanged_and_scoped_serializer_is_explicit`. Exact schema-v3 dictionaries, omission/null distinctions, publication artifacts and ordinary omission; X precedence asserts verbose JSON equality. |
| AC-22 | O.`test_human_measured_scope_and_evidence_match_json_in_both_branches`, `test_human_failures_retain_safe_metadata_and_omit_unsupported_text`; X root read allowlist test treats production as an ordinary group. Supplied-file and observable-publication limitations, no runtime/deployment/coherence claim. |
| AC-23 | X.`test_root_read_allowlist_integrity_and_no_implicit_production_or_default` guards root descriptor/content reads, execution/archive entry points, config/credential/include/gemspec decoys, and before/after all target file bytes/names; P.`test_parser_does_not_access_files_network_or_execute_code`. No live HTTP, target execution or mutation. |
| AC-24 | R.`test_missing_inputs_ignore_parent_nested_and_alternate_decoys`, `test_internal_links_read_only_resolved_contained_file`, `test_escaping_links_never_open_or_read_target`, `test_final_and_directory_symlink_replacements_reject_and_close`; BOTH R regular-to-FIFO and S composed FIFO tests; C.`test_scoped_direct_file_and_invalid_paths_are_usage_errors`; X read allowlist. Exact root names, containment and direct-file refusal. |
| AC-25 | X real-adapter test; M.`test_scoped_default_adapter_retains_ca_bundle_and_trust`; G.`RegistryPopulationTests.test_explicit_ca_and_timeout_use_shared_policy`, `test_exact_limit_excess_and_truncation_through_restricted_transport`, `test_redirect_handler_rejects_every_supported_redirect_status`; G.`RateLimitTests`; `test_pypi.PyPITests.test_python_default_trust_is_kept_when_available`, `test_pip_fallback_only_when_default_has_no_trust_and_uses_verified_cafile`, `test_custom_ca_bundle_uses_verified_default_context`; `test_registry.BoundedTransportTests.test_restricted_opener_reuses_selected_context_timeout_and_user_agent`. Fixed authority, verified TLS/trust, redirect rejection, limits, pacing/cooldown. |
| AC-26 | X real-adapter test; M.`test_same_version_zero_and_flagged_timestamp_clamping`; G.`PublicationTests` and `test_metric`. Earliest admissible platform dates, excluded invalid dates/prereleases, latest stable, exact arithmetic/zero and anomaly flag. |
| AC-27 | C.`test_evidence_failures_and_empty_scopes_are_completed_reports`, `test_malformed_missing_empty_and_comma_values_are_usage_errors_before_scan`, `test_scoped_direct_file_and_invalid_paths_are_usage_errors`, `test_request_errors_and_unrelated_systemic_errors_keep_distinct_exits`; X precedence completed partial/source errors. Exits 0/1/2 retain meanings. |
| AC-28 | X precedence table independently spans recognition → unknown group → absent/rejected lock → F1 → absent direct → local authority/F2 → mismatch → selection → registry, in CLI JSON/human/verbose with sibling survival. F1: accepted lock missing private declaration's direct identity, known N, no lookup. F2: unsupported requirement, omitted lock requirement/artifacts, safe declaration/N/no lookup/no unsafe echo. A.`test_nonpublic_gemfile_does_not_override_unavailable_lock_precedence`, O ordinary omission test, and BOTH S FIFO witnesses retain earlier-stage and ordinary behavior. |

P1 has four existing bounded subprocess witnesses in `test_ruby_groups.py`:
R.`test_gemfile_regular_to_fifo_replacement_does_not_block`,
R.`test_lock_regular_to_fifo_replacement_does_not_block`,
S.`test_gemfile_fifo_replacement_composes_unknown_scope_and_no_lock_read`, and
S.`test_lock_fifo_replacement_composes_known_scope_and_no_rows`.
They replace regular inputs at final open, assert nonblocking/no-follow flags,
reject before content consumption, close descriptors and make zero lookups.
Capability-refusal mocks remain separate; these witnesses are reused, not copied.
