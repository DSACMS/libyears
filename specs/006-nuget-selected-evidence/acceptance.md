# Feature 006 offline acceptance evidence — T014

## Current-contract qualification — 006-0015

The original executed T014/K4 record below remains historical evidence against
its then-approved contract; no test result or review is erased or rerun by this
reconciliation. Corrected S4/AC-13/AC-16 are independently approved at `2deb864`.
All 36 AC identifiers remain; 34 AC wordings are unchanged.

| Refined obligation | Existing evidence retained | Additional evidence still required |
|---|---|---|
| AC-13 | Explicit version-1 envelope, exact-byte/context/baseline and package binding tests below | Independently audited native producer-time package provenance plus contemporaneous attestation, bound to the event/project/lock/framework/influences; prospective bundle under release-validation.md |
| AC-16 | Blanket/config/cache/mapping/identity/hash-only no-authority negatives below | Preserve 006-0014 D/BLOCKED as replay negative: useful native source/hash evidence cannot attest OASim's historical producing context; no fabricated replay-derived historical envelope |
| S4 trust explanation / AC-30 collateral | Original correspondence and supplier-limitation tests below | Bounded T012/T013 reporting/help/docs correction and focused independent verification, pending explicit execution authority |

The consumer's existing accepted-testimony checks remain applicable; they do not
independently prove chronology. No synthetic fixture is promoted to an actual
attestation. No new schema or product parser is required by this refinement.
Current full implementation conformance and refreshed acceptance are pending
the reporting correction and event evidence; historical offline 36/36 is not a
claim of current-contract or live validation completion. H1/H2/H4, closed
findings, metric and compatibility evidence remain intact.

Historical OASim has no required contemporaneous attestation. 006-0013 correctly
left T016 incomplete; 006-0014 established no original-context equivalence and
remains the blocked negative empirical witness. T016/K5 remain incomplete and
unapproved; T017/K6 cannot proceed. The prospective procedure is prepared only.

Author evidence in run `006-0012`, based on approved K3 at `cdfef4c`.
This record consolidates executed witnesses; it is not independent K4 approval,
real-root validation, convergence, release approval or a live measurement claim.
Approved spec/plan/tasks remain unchanged. The parent records the eventual frozen
candidate and independent disposition in reviews.md.

The new `tests/test_nuget_acceptance.py` composes public argument handling,
source discovery, complete local parsers, association/authority, the actual
metadata byte client and handler, typed worker-result encoding/decoding, metric,
summaries and human/JSON rendering. Its injected `nuget_lookup` bypasses the
parent NuGetRegistryAdapter and supervisor and directly runs the metadata client,
handler and typed result codec. The retained separate supervisor composition, controller/mutation
and real-process tests below establish that boundary; a synchronous injected
handler is not evidence of absolute cancellation by itself.

All generated inputs and URL-to-response maps are synthetic. They are neither
restored packages nor statements about actual package origin or first receipt.
No external root, OASim material, live NuGet, package manager, SDK, target code,
archive, cache, configuration or credentials were accessed.

## Executed verification

Commands and final results are recorded after final execution below. A result
applies to the named behavioral assertions, not merely to the number of tests.

| Command | Result |
|---|---|
| `python -m unittest tests.test_nuget_acceptance` | 8 PASS |
| `python -m unittest discover -s tests -p 'test_nuget*.py'` | 225 PASS |
| `python -m unittest discover -s tests` | 631 PASS |
| `git diff --check` and untracked-file whitespace checks | PASS |

The following 36-row reconciliation names actual tests. Module names are relative
to `tests/`; method names are exact. Each row's result is the executed offline
behavior, subject to the platform qualifications below. It does not mark the
frozen specification checkboxes or later human validation complete.

## Acceptance criteria reconciliation

| AC | Actual witnesses and observed assertions |
|---|---|
| 01 | `test_nuget_cli.NuGetCLITests.test_ordinary_scan_omits_colocated_nuget_and_preserves_other_abbreviations`, `test_one_selected_project_and_python_ruby_options_keep_their_scopes`; acceptance `test_public_path_permutations_preserve_requests_evidence_and_summaries`: explicit chosen project only, ordinary artifacts omit NuGet. |
| 02 | CLI `test_usage_failures_are_safe_and_precede_all_content_reads`, `test_direct_file_and_missing_root_are_safe_usage_errors`, `test_missing_project_and_source_failures_empty_partial_are_completed_reports`: invalid activation exit1 before reads; missing selected project/source reports exit0. |
| 03 | `test_nuget_project.NuGetProjectTests.test_complete_framework_forms_and_empty_population`; composed successful acceptance: both sole framework forms establish complete context and N. |
| 04 | Project `test_framework_context_rejections_never_return_partial_population`, `test_xml_context_and_external_entities_are_never_loaded`; acceptance `test_combined_earliest_stages_retain_only_safe_established_evidence`: rejected context gives unknown N and no later read/lookup. |
| 05 | Project `test_all_direct_roles_and_metadata_count_once`; acceptance `test_actual_reader_public_path_preserves_bytes_and_never_traverses_references`: all supported roles count, ProjectReference remains unopened and uncounted. |
| 06 | Project `test_request_minima_are_preserved_without_selection`, `test_unsupported_requests_and_id_grammar`; version `test_five_supported_request_minima`; source `test_five_canonical_pairs_and_different_selected_version`: five S3 numeric pairs accept; unsupported declarations reject scope. |
| 07 | Project `test_duplicate_ids_have_distinct_failure`, `test_package_affecting_and_unknown_constructs`, `test_complete_framing_precedes_unsupported_and_duplicate`: aliases, imports/CPM/conditions/generated/unknown constructs reject completely; malformed precedence retained. |
| 08 | Lock `test_schema_one_fixture_retains_closure_without_population`; source `test_association_missing_transitive_namesake_and_selection`: closure kinds frame evidence but never supply membership or missing Direct. |
| 09 | Lock `test_schema_requires_integer_and_root_required_fields`, `test_repeated_keys_at_every_level_reject_whole_lock`, `test_extra_empty_and_rid_contexts_are_unsupported`; scan `test_source_unavailability_matrix_known_and_unknown_including_zero`: rejected whole lock retains known N with null measurement. |
| 10 | Source `test_five_canonical_pairs_and_different_selected_version`, `test_all_s3_noncanonical_negative_requests_and_stage_omissions`: exact canonical minimum comparison accepts all five pairs; only resolved supplies selection. |
| 11 | Source `test_association_missing_transitive_namesake_and_selection`, `test_whole_lock_failures_precede_individual_failures`; lock `test_present_nonstring_selection_and_hash_reject_whole_lock`, `test_repeated_keys_at_every_level_reject_whole_lock`: isolated missing/unsupported/mismatch reasons make no lookup; F2 structural failures reject source. |
| 12 | Source `test_context_failures_extra_direct_framework_and_stale_bytes`, `test_exact_byte_binding_for_lf_and_crlf_without_normalization`; acceptance earliest-stage case: wrong context/digests and extra Direct reject; mtime/Git cannot repair binding. |
| 13 | Provenance `test_exact_fixture_binding_and_immutable_authority`, `test_context_binds_raw_bytes_not_equivalent_decoded_documents`; CLI `test_omitted_witness_never_accepts_found_file`: explicit bounded witness required. |
| 14 | Source `test_whole_witness_precedes_association_and_invalidates_population_only_when_asserted`; scan source-unavailability matrix: unavailable witness retains N, unsupported population assertion clears N. |
| 15 | Provenance `test_missing_private_alternate_and_conflicting_origins_never_admit_lookup`; acceptance `test_isolated_association_origin_hash_and_public_failures_compose`: unsupported beta origin never reaches metadata despite available namesake-style data. |
| 16 | Provenance `test_config_mapping_cache_blanket_and_hash_only_do_not_authorize`; acceptance `test_excluded_artifacts_cannot_repair_missing_or_rejected_authority`: local markers cannot supply LocalAuthority. |
| 17 | Provenance `test_hash_absent_invalid_and_mismatch_exact_reasons_and_precedence`; local reason trigger test: decoded 64-byte agreement required; absent/invalid/mismatch produces exact local failure and no call. |
| 18 | Registry `test_selected_identity_type_and_classification_matrix`, `test_public_hash_matrix_and_hash_before_date`; acceptance isolated case: public mismatch wins over unavailable date and never establishes publication. |
| 19 | Registry `test_created_only_success_and_default_listing`, `test_timestamp_fraction_offset_matrix`; acceptance success map deliberately gives unusable published/commit canaries yet measures created-only dates and one year. |
| 20 | Registry `test_missing_invalid_sentinel_naive_used_and_latest_no_fallback`, `test_creation_conflict_is_invalid_response`, `test_catalog_deleted_latest_never_uses_older_dated_release`: actual latest/used missing date never borrows older or alternate date. |
| 21 | Registry `test_latest_numeric_revision_and_listing_independent_of_dates`, `test_external_pages_sorted_complete_and_reordering_invariant`, `test_unlisted_prerelease_used_and_no_stable`: complete numeric greatest listed stable; listing default and exclusions retained. |
| 22 | Registry `test_registration_structure_count_bounds_flags_matrix`, `test_missing_external_page_and_overlap_reject_complete_latest`, `test_both_aliases_need_usable_hash_algorithm_and_creation_material`: incomplete/unsupported/conflicting/unavailable aliases fail; no partial latest. |
| 23 | Registry `test_unlisted_prerelease_used_and_no_stable`, `test_absent_package_used_and_catalog_before_hash_dates`, `test_hostile_links_never_fetched_including_inline_page_identifier`: authorized used need not be listed/stable; absence reasons distinct; archive links ignored. |
| 24 | Version `test_selected_normalization_preserves_safe_original`, `test_identity_equivalence_ignores_build_and_prerelease_case`, `test_numeric_stable_order_includes_revision`; registry `test_catalog_type_alias_and_normalized_identity`: bounded identity normalization and numeric order. |
| 25 | Scan `test_metric_arithmetic_identity_zero_anomaly_and_measured_only_totals`; acceptance success: 365.25-day delta gives exactly1 per dependency and total2, normalized used=latest zero, negative clamp flagged, failures excluded. |
| 26 | Scan `test_source_unavailability_matrix_known_and_unknown_including_zero`; acceptance earliest-stage cases: unknown project vs known lock/witness N, null measured/coverage, no fabricated package failures. |
| 27 | Scan `test_empty_all_failed_partial_and_full_accepted_population`; output `test_partial_empty_and_zero_coverage_numeric_snapshots`; acceptance isolated case: accepted all-failed N3/M0 coverage0 distinct from unavailable/validated empty. |
| 28 | Mixed scan `test_each_nuget_source_failure_preserves_siblings_in_both_ruby_modes`, `test_each_nuget_registry_failure_retains_three_same_name_rows`, `test_each_nuget_local_failure_preserves_same_name_siblings_without_lookup`, `test_four_same_names_success_and_yarn_arbitration_survive_nuget_failure`, `test_all_unavailable_and_some_available_with_zero_successes`: same-name identities, evidence and available aggregates survive every failure family. |
| 29 | Output `test_full_schema_v3_snapshot`, `test_source_rejection_snapshot_required_nulls_and_no_fabricated_rows`, `test_local_association_stage_snapshots_omit_unestablished_facts`, `test_ordinary_sibling_json_has_no_nuget_additions`; acceptance permutations: exact JSON equality with verbose and reordered facts. |
| 30 | Output `test_human_success_corresponds_to_json_and_explains_evidence_limits`, `test_human_source_failures_correspond_to_json_and_hide_root_and_diagnostics`, `test_human_distinguishes_unavailable_zero_empty_partial_and_full`, `test_human_anomaly_and_same_name_sibling_correspondence`; acceptance public success checks human identities/states/dates/trust against JSON. |
| 31 | Acceptance `test_retained_s6_reasons_exactly_match_reachable_trigger_tables`, `test_combined_earliest_stages_retain_only_safe_established_evidence`, `test_public_path_permutations_preserve_requests_evidence_and_summaries`, `test_isolated_association_origin_hash_and_public_failures_compose`; source and registry reachable reason tests below: earliest stages, sorted requests/equal summaries, omissions and no ambiguity claim. |
| 32 | Acceptance `exercise` guards all composed success/source/local/public-failure/ordinary report paths; actual-reader public-path test adds descriptor whitelist. CLI usage tests forbid pre-validation source/snapshot/CA reads. Worker bootstrap/lifecycle tests below permit only exact trusted helper/fixture. Before/after all synthetic target-file bytes equal. |
| 33 | Input, project, lock, provenance boundary witnesses in the complete limits table below; actual-reader source/input tests cover contained symlinks, escapes, special files and replacement. Portable refusal tests run independently of supported-reader skips. |
| 34 | All transport/metadata/supervisor bounds and P1 witnesses in tables below; registry `test_actual_handler_client_protocol_supervisor_success_and_late_discard` composes index/page/catalog cutoff with no restart. Actual process entry/cancel evidence is distinct from fake-clock arithmetic. |
| 35 | Acceptance `test_response_exception_and_local_secret_canaries_across_output_modes`, isolated origin case and private-root path in every composed case; CLI `test_capitalized_malformed_options_do_not_echo_secret_values`, `test_case_variant_abbreviated_and_malformed_options_are_safe_before_content_reads`, `test_safe_input_systemic_and_rendering_failures_and_success_path_privacy`; registry `test_no_secret_response_exception_or_hash_crosses_result_boundary`; output `test_human_staged_failures_preserve_omissions_and_private_canaries`. XML/witness/origin/argv/path/response/exception/hash canaries absent from human/verbose/JSON/stderr. |
| 36 | Acceptance `test_excluded_artifacts_cannot_repair_missing_or_rejected_authority`; project unsupported-construct/context tests; provenance origin tests; ordinary CLI co-location test: assets/export/packages.config/import/CPM/conditional/multiple framework/RID/private/portfolio inputs cannot repair missing lock/witness or activate implicit scope. |

## Retained S6 reason enumeration

`test_retained_s6_reasons_exactly_match_reachable_trigger_tables` extracts the
normative S6 table directly and requires exact equality of `(level, reason)`
with the union of the two committed JSON trigger tables. It also checks every
listed test method exists. The separate executable trigger tests produce each
reason and assert equality with their table; documentation/table existence alone
does not establish reachability. Hash reasons intentionally have both local and
public triggers. There are 23 distinct level/reason pairs, with no missing or
extra pair and no NuGet `ambiguous_lock_evidence`.

| Level | Reasons | Executed trigger |
|---|---|---|
| Source | `nuget_project_missing`, `invalid_nuget_project`, `unsupported_nuget_project`, `duplicate_nuget_declaration`, `lockfile_missing`, `invalid_lockfile`, `unsupported_lockfile_format`, `nuget_context_mismatch`, `nuget_provenance_missing`, `invalid_nuget_provenance` | `test_nuget_source.NuGetSourceTests.test_local_s6_reason_trigger_table` |
| Dependency/local | `lock_dependency_missing`, `declaration_lock_requirement_mismatch`, `lock_version_missing`, `unsupported_lock_evidence`, `unsupported_dependency_source`, `content_hash_unavailable`, `content_hash_mismatch` | Same local trigger test |
| Dependency/public | `package_not_found`, `version_not_found`, `content_hash_unavailable`, `content_hash_mismatch`, `release_date_missing`, `no_stable_release`, `invalid_registry_response`, `registry_error` | `test_nuget_registry.RegistryTests.test_registry_reason_trigger_table` |

Source `test_combined_failures_and_reordered_whole_source_precedence`, lock
`test_malformed_wins_over_unsupported_in_every_object_order`, project
`test_complete_framing_precedes_unsupported_and_duplicate`, registry
`test_reordered_alias_leaves_objects_and_dates_keep_schedule_and_result` and
acceptance permutations cover project/reference/JSON/page/leaf ordering. Malformed
whole structure wins over unsupported structure; whole sources precede association,
then origin/local hash/public structure/public hash/used/latest dates. Acceptance
asserts exact attempted input names, so unprocessed later inputs neither get read
nor invent source errors. Mismatch omits selected provenance; unsupported origin
does not query; public hash mismatch does not establish used publication.

Forbidden-operation mock histories and descriptor-open arguments are asserted
after `main` returns, outside product exception handlers. The acceptance test
`test_swallowed_forbidden_io_attempts_still_fail_acceptance_guards` injects socket
and file-read attempts into an expected registry-error path and catches their
exceptions in the mutation. Both must still fail the post-call guard, proving
that production exception sanitization cannot turn forbidden attempted I/O into
a false passing failure-path witness.

## All approved finite limits and safety witnesses

Methods below are in the named `test_nuget_*.py` module. Actual large local
population/byte and JSON limits have cap/cap+1 cases. Transport tests also use
smaller injected byte caps for encoding/decompression behavior, counter seeding
at the production aggregate/request boundary and injected lower traversal caps;
they do not claim to download large live bodies or enumerate 100,000 live releases.

| Plan limit / invariant | Actual witness |
|---|---|
| Project 1 MiB; lock 16 MiB; witness 16 MiB, cap+1 read maximum | Input `test_all_byte_caps_and_cap_plus_one_reads_at_most_cap_plus_one`; lock `test_byte_limit_uses_exact_bytes_and_does_not_trust_cached_text`; provenance `test_package_count_and_witness_bytes_caps` |
| XML depth 32/elements 50,000/attributes 32 | Input `test_xml_depth_elements_and_attributes_caps`; project `test_xml_callback_caps_and_cap_plus_one` |
| Local JSON depth 32/values 200,000/general string 16 KiB | Input `test_depth_cap_and_cap_plus_one_before_decoder`, `test_value_cap_and_cap_plus_one_containers_count_keys_do_not`, `test_string_cap_and_cap_plus_one_including_keys_and_escapes` |
| Direct 10,000; lock 50,000; witness 50,000 | Project `test_direct_reference_cap_and_cap_plus_one`; lock `test_actual_entry_count_cap_and_cap_plus_one`; provenance `test_real_package_record_count_cap_and_cap_plus_one` |
| Version 256 ASCII/numeric 32 digits; framework 128; producer name/version and SDK assertion 256 | Version `test_exact_length_boundaries`, `test_length_bounds_precede_integer_conversion`; project `test_framework_sdk_and_component_limits`; lock `test_version_bounds_cover_direct_transitive_and_all_closure_requests`, `test_component_bound_applies_inside_requested_ranges`; provenance `test_assertion_and_framework_exact_limits` |
| Duplicate/nonfinite/bool/encoding/framing safety | Input duplicate/nonfinite/boolean tests; project `test_xml_context_and_external_entities_are_never_loaded`; lock `test_invalid_json_utf8_and_safe_error`; provenance `test_unknown_and_duplicate_fields_at_every_level` |
| Contained symlinks, root escape, bounded loops, FIFO/device/directory, replacement/mutation | Input `test_permits_relative_absolute_and_nested_inside_symlinks`, `test_rejects_escape_without_inspecting_or_opening_outside`, `test_symlink_loop_is_bounded`, `test_fifo_and_directory_rejected_before_open_or_read`, `test_device_type_is_rejected_without_open`, `test_replacement_between_inspection_and_open_rejected_before_read`, `test_mutation_and_replacement_during_read_fail_closed` |
| Unavailable platform primitives refuse before read; exact-byte LF/CRLF binding | Input portable `test_missing_safety_primitives_fail_closed_without_open_or_read`; source `test_missing_safety_primitives_reject_source_before_reads_or_authority`, `test_exact_byte_binding_for_lf_and_crlf_without_normalization`; scan `test_production_reader_refusal_remains_unknown_without_open_or_lookup` |
| HTTPS exact approved resource purposes; no userinfo/port/query/fragment/escaping/downgrade/private/archive links; redirects 0 | Transport `test_rejected_urls_never_reach_transport`, `test_fixed_purposes_and_sorted_validated_page_schedule`; registry `test_hostile_links_never_fetched_including_inline_page_identifier`; shared `test_registry` verified TLS/restricted redirect regressions |
| Body 8 MiB wire/32 MiB expanded; aggregate 64 MiB/128 MiB; identity/gzip only | Transport `test_identity_and_incremental_gzip_exact_cap_and_wire_accounting`, `test_bad_encoding_expansion_truncation_crc_and_concatenation`, `test_wire_cap_and_declared_truncation`, `test_page_version_request_and_aggregate_caps` |
| Public JSON depth 32/values 500,000/string 1 MiB | Transport `test_json_depth_values_strings_and_invalid_framing` (actual production values/string caps and depth) |
| Pages 256/versions 100,000/requests 512 package and 4096 scan | Transport `test_page_version_request_and_aggregate_caps`; registry `test_page_version_request_limits_and_no_partial_latest`; no truncation into latest |
| Retries 0; rate-limit 429/503 Retry-After bounded header 128, cooldown scan-local | Transport `test_get_url_only_double_and_error_classes_and_no_retry`, `test_503_retry_after_is_an_opt_in_with_safe_header_filtering`, `test_rate_limit_cooldown_persists_across_packages_and_never_sleeps`; registry `test_service_index_cached_and_cooldown_scan_counters_retained` |
| Socket operation 10s/package 60s/scan 300s; cutoff reserve 0.5s; poll 10ms; terminate wait 0.25s; readiness 10s | Worker controller tests below and transport `test_deadline_admission_and_scan_not_reset`, `test_injected_absolute_cutoff_caps_socket_timeout_and_discards_late_bytes` |
| Atomic regular-file command/result 16 KiB, bounded schema and no raw diagnostics | Worker `test_bounded_regular_files_atomic_publication_and_closed_handles`, `test_protocol_bad_enum_types_and_ready_bool_are_rejected`, `test_authority_round_trip_and_no_raw_diagnostics`, `test_typed_success_and_staged_failure_round_trip` |

## P1, lifecycle and closed-finding regression evidence

All methods in this table execute as part of the NuGet and full offline suites.

| Obligation | Actual witness |
|---|---|
| Trusted isolated installed bootstrap, offline ready, fixed command deadlines | Worker `test_bootstrap_offline_readiness_and_fixed_command_deadlines`, `test_isolated_installed_worker_ready_without_handler_or_network`, `test_worker_retains_one_client_and_uses_parent_working_deadlines` |
| Blocked connect/TLS/header/body/index and progress below inactivity/byte limits cannot extend D | `test_blocked_stages_and_drip_progress_cannot_extend_deadline`, `test_socket_only_admission_mutation_fails_blocking_witness`; separate `test_socket_inactivity_failure_maps_to_registry_error` |
| Earlier scan cutoff, earlier success, exhausted admission, early/exact/late/post-validation result | `test_scan_cutoff_wins_preserving_earlier_result_and_exhaustion`, `test_success_exact_late_and_post_validation_cutoff`, `test_earlier_success_survives_later_cutoff_and_no_restart`, `test_already_exhausted_scan_does_not_publish_command` |
| Corrupt/oversized/abrupt death, interruption, startup/readiness failure | `test_corrupt_oversized_and_abrupt_death_fail_closed`, `test_interruption_cleans_up_and_propagates`, `test_startup_failure_is_safe_systemic_without_fallback`, `test_readiness_timeout_is_systemic_and_no_command` |
| Ignored terminate/kill/reap faults, bounded waits, handle/deferred cleanup | Blocked-stage test; `test_kill_and_reap_os_fault_is_systemic_and_deferred`, `test_unreaped_process_retains_path_then_nonblocking_reap` |
| Actual handler-entry before cancellation, live process, consumed command, no result/return, OS exit/reap/temp cleanup, outer watchdog | `RealWorkerTests.test_offline_blocked_worker_cancelled_with_outer_watchdog`; no-command mutation `test_suppressing_command_fails_real_blocking_handler_witness` |
| Real handler/client/protocol/controller composition and deadline discard | Registry `ComposedSupervisionTests.test_actual_handler_client_protocol_supervisor_success_and_late_discard`, `test_lazy_installed_worker_handler_uses_real_adapter_handler` |
| F1/F2 | Source five-pair, S3 negative and whole-lock tests; lock duplicate/non-string tests; acceptance reason enumeration/mismatch omission |
| K1-F1 | Source `test_k1_exact_direct_and_transitive_overflows_reject_whole_source`, `test_k1_closure_requests_and_direct_requests_cannot_bypass_bounds`, `test_k1_transitive_boundaries_preserve_unrelated_direct_authority`; lock complete bounds/precedence |
| K2-M1 | Registry `test_both_aliases_need_usable_hash_algorithm_and_creation_material`, `test_valid_equal_and_conflicting_alias_material_at_every_position`, `test_shared_catalog_document_still_requires_usable_duplicate_material`, `test_singleton_unavailable_material_preserves_reason_and_evidence_stages`, `test_used_absence_precedes_unavailable_duplicate_material` |
| K3-C1 | CLI capitalized and mixed-case malformed option witnesses, preserving ordinary argparse context and exact lowercase activation |

Required POSIX/Windows worker evidence is retained in reviews.md: exact published
`77d66b9a9a31be6b5cac0bf99c4ff8906a3da9a4`, CI41731562096, all three Windows
Python 3.11–3.13 and all six POSIX jobs passed explicit unskipped lifecycle, full
offline suite and whitespace steps. Worker/transport/registry/protocol/workflow
bytes remain unchanged since that evidence. These observations establish that
specific process graph's platform evidence; they do not claim Windows execution
of later CLI/output/acceptance tests. Actual descriptor-reader tests skip only
when required safety capabilities are absent; unskipped portable refusal and
synthetic-byte semantic witnesses remain separate. No hard real-time whole-CLI
bound is claimed for process creation, startup or OS scheduling failure.

## Remaining gates and limits

T014 author verification is followed by frozen-candidate fresh all-36 K4 audit.
T015 prepares a reviewable validation procedure only. Required T016/K5 real-root
evidence still needs separately identified/authorized target and access; it is
neither run nor made optional here. T017/K6 convergence and T018 human roadmap
handoff remain later gates. Useful live yield and hash-domain fitness remain
unverified; no hash-policy workaround is authorized.

The separate hosted secret check failure and its synthetic local reproduction
remain exactly as recorded in reviews.md. This task adds no scanner suppression,
exception, credentials, trust change or claim that the hosted check passed.
