import json
import unittest
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
import tempfile
from unittest.mock import Mock

from libyears.model import (Dependency, DependencyMeasurement, GemfileEvidence, MetricSummary,
                            RegistryFailure, RegistryResult, RubyGemsEvidence,
                            RubyPublicationArtifact, SourceEvidence, SourceError, SourceResult)
from libyears.requirements import UnmeasurableRequirement
from libyears.output import format_human, format_json, report_to_dict
from libyears.scan import MixedScanReport, ScanReport, scan_mixed_repository


def report_with_data():
    utc = timezone.utc
    first = Dependency("pypi", "older", "1.0", datetime(2023, 1, 1, tzinfo=utc), "2.0", datetime(2024, 1, 1, tzinfo=utc))
    second = Dependency("pypi", "newer", "2.0", datetime(2023, 1, 1, tzinfo=utc), "2.1", datetime(2023, 1, 2, tzinfo=utc))
    return ScanReport(
        MetricSummary(3, 2, 2 / 3, 1.002, 0.501, 0.501, 1.0),
        (DependencyMeasurement(first, 1.0), DependencyMeasurement(second, 0.002)),
        (type("Unmeasurable", (), {"ecosystem": "pypi", "name": "missing", "declared": "missing>=1", "reason": "non_exact_version"})(),),
    )


def report_with_unmeasurable(*reasons):
    return ScanReport(
        MetricSummary(len(reasons), 0, 0.0, 0.0, None, None, None),
        (),
        tuple(
            UnmeasurableRequirement("package", f"package=={index}", reason)
            for index, reason in enumerate(reasons, start=1)
        ),
    )


class OutputTests(unittest.TestCase):
    def test_json_matches_schema_and_uses_utc_timestamps(self):
        report = report_with_data()
        rendered = format_json(report, ".")
        data = json.loads(rendered)
        self.assertEqual(data["schema_version"], 3)
        self.assertNotIn("repository", data)
        self.assertEqual(
            data["version_evidence"],
            {"pypi": {"declaration_source": "requirements.txt", "snapshot_source": None}},
        )
        self.assertEqual(data["summary"]["coverage"], 2 / 3)
        self.assertEqual(data["dependencies"][0]["used_release_time"], "2023-01-01T00:00:00Z")
        self.assertIsInstance(data["dependencies"][0]["libyears"], float)
        self.assertEqual(data["dependencies"][0]["version_source"], "requirements_exact")
        self.assertEqual(data["unmeasurable"][0]["reason"], "non_exact_version")
        self.assertEqual(data["summary"]["by_ecosystem"]["pypi"]["coverage"], 2 / 3)
        self.assertEqual(data["source_errors"], [])

    def test_json_with_snapshot_reports_v2_evidence_and_source(self):
        report = ScanReport(
            MetricSummary(1, 1, 1.0, 1.0, 1.0, 1.0, 1.0),
            (
                DependencyMeasurement(
                    Dependency(
                        "pypi", "requests", "2.31.0",
                        datetime(2023, 1, 1, tzinfo=timezone.utc),
                        "2.32.0", datetime(2024, 1, 1, tzinfo=timezone.utc),
                        "resolved_snapshot",
                    ),
                    1.0,
                ),
            ),
            (),
            "resolved.txt",
        )
        data = json.loads(format_json(report, "."))
        self.assertEqual(data["schema_version"], 3)
        self.assertEqual(
            data["version_evidence"]["pypi"]["snapshot_source"],
            {"format": "pip_freeze_exact", "path": "resolved.txt"},
        )
        self.assertEqual(data["dependencies"][0]["version_source"], "resolved_snapshot")

    def test_schema_v3_supports_npm_and_mixed_source_evidence(self):
        summary = MetricSummary(1, 0, 0.0, 0.0, None, None, None)
        npm = SourceResult(
            "npm", (), (), (), SourceEvidence("package.json", "package-lock.json"),
            dependencies_discovered=0, measurement_available=True,
        )
        pypi = SourceResult(
            "pypi", (), (), (), SourceEvidence("requirements.txt", None),
            dependencies_discovered=0, measurement_available=True,
        )
        for sources, expected in (((npm,), ["npm"]), ((pypi,), ["pypi"]), ((npm, pypi), ["npm", "pypi"])):
            report = MixedScanReport((), (), (), sources, summary,
                                     {source.ecosystem: summary for source in sources})
            data = json.loads(format_json(report, "."))
            self.assertEqual(data["schema_version"], 3)
            self.assertEqual(data["ecosystems"], expected)
            self.assertEqual(set(data["version_evidence"]), set(expected))
            self.assertEqual(set(data["summary"]["by_ecosystem"]), set(expected))

    def test_yarn_format_is_additive_and_existing_evidence_is_unchanged(self):
        summary = MetricSummary(1, 1, 1.0, 0.0, 0.0, 0.0, 0.0)
        original = report_with_data().measurements[0].dependency
        for ecosystem, snapshot, version_source, evidence_format, include_format in (
            ("npm", "yarn.lock", "yarn_lock", "yarn_lock_v1", True),
            ("npm", "package-lock.json", "package_lock", None, False),
            ("pypi", None, "requirements_exact", None, False),
        ):
            with self.subTest(ecosystem=ecosystem, snapshot=snapshot):
                declaration = "package.json" if ecosystem == "npm" else "requirements.txt"
                source = SourceResult(
                    ecosystem, (), (), (),
                    SourceEvidence(declaration, snapshot, evidence_format, include_format),
                    dependencies_discovered=1, measurement_available=True,
                )
                dependency = replace(original, ecosystem=ecosystem, version_source=version_source)
                report = MixedScanReport(
                    (DependencyMeasurement(dependency, 0.0),), (), (), (source,),
                    summary, {ecosystem: summary},
                )
                data = report_to_dict(report, ".")
                expected = {"declaration_source": declaration, "snapshot_source": snapshot}
                if include_format:
                    expected["format"] = evidence_format
                self.assertEqual(data["version_evidence"], {ecosystem: expected})
                self.assertNotIn("rubygems_evidence", data["dependencies"][0])
                self.assertNotIn("scope", data["version_evidence"][ecosystem])
                self.assertNotIn("publication_basis", data["version_evidence"][ecosystem])
                self.assertEqual(data["schema_version"], 3)
                self.assertEqual(data["dependencies"][0]["version_source"], version_source)
                if version_source == "yarn_lock":
                    self.assertIn("yarn.lock", format_human(report, "."))
                    python_source = replace(source, ecosystem="pypi", evidence=SourceEvidence("requirements.txt", None))
                    mixed = replace(report, source_results=(source, python_source))
                    self.assertIn("yarn.lock", format_human(mixed, "."))

    def test_schema_v3_keeps_source_failure_distinct_from_dependency_rows(self):
        summary = MetricSummary(None, 0, None, 0.0, None, None, None)
        source = SourceResult(
            "npm", (), (), (SourceError("npm", "package.json", "invalid_manifest"),),
            SourceEvidence("package.json", "package-lock.json"),
            dependencies_discovered=None, measurement_available=False,
        )
        report = MixedScanReport((), (), source.source_errors, (source,), summary, {"npm": summary})
        data = json.loads(format_json(report, "."))
        self.assertEqual(data["source_errors"], [{"ecosystem": "npm", "source": "package.json", "reason": "invalid_manifest"}])
        self.assertEqual(data["unmeasurable"], [])

    def test_json_preserves_fractional_seconds_without_adding_them(self):
        report = report_with_data()
        dependency = report.measurements[0].dependency
        dependency_with_fraction = Dependency(
            dependency.ecosystem,
            dependency.name,
            dependency.used_version,
            dependency.used_release_time.replace(microsecond=123400),
            dependency.latest_stable_version,
            dependency.latest_stable_release_time,
        )
        report = ScanReport(
            report.summary,
            (DependencyMeasurement(dependency_with_fraction, 1.0),),
            report.unmeasurable,
        )
        data = report_to_dict(report, ".")
        self.assertEqual(data["dependencies"][0]["used_release_time"], "2023-01-01T00:00:00.123400Z")
        self.assertEqual(data["dependencies"][0]["latest_stable_release_time"], "2024-01-01T00:00:00Z")

    def test_human_output_sorts_by_libyears_and_includes_summary(self):
        output = format_human(report_with_data(), ".")
        self.assertLess(output.index("older"), output.index("newer"))
        self.assertIn("Measured: 2 / 3 dependencies", output)
        self.assertIn("Coverage: 66.7%", output)
        self.assertIn("exact version not available", output)
        self.assertNotIn("non_exact_version", output)
        self.assertNotIn("SOURCE", output)

    def test_human_output_reports_evidence_and_mixed_sources(self):
        report = report_with_data()
        mixed_measurements = (
            report.measurements[0],
            DependencyMeasurement(
                Dependency(
                    "pypi", "newer", "2.0", datetime(2023, 1, 1, tzinfo=timezone.utc),
                    "2.1", datetime(2023, 1, 2, tzinfo=timezone.utc),
                    "resolved_snapshot",
                ),
                0.002,
            ),
        )
        mixed = ScanReport(report.summary, mixed_measurements, report.unmeasurable, "resolved.txt")
        output = format_human(mixed, ".")
        self.assertIn("Version evidence: requirements.txt; resolved snapshot: resolved.txt", output)
        self.assertIn("SOURCE", output)
        self.assertIn("requirements.txt", output)
        self.assertIn("snapshot", output)

    def test_human_output_uses_friendly_snapshot_failure_reasons(self):
        output = format_human(
            ScanReport(
                MetricSummary(4, 0, 0.0, 0.0, None, None, None),
                (),
                tuple(
                    UnmeasurableRequirement("pkg", "pkg", reason)
                    for reason in (
                        "snapshot_version_missing",
                        "snapshot_version_conflict",
                        "snapshot_version_incompatible",
                        "declared_snapshot_conflict",
                    )
                ),
                "resolved.txt",
            ),
            ".",
        )
        for text in (
            "exact version missing from supplied snapshot",
            "conflicting versions in supplied snapshot",
            "snapshot version does not satisfy declaration",
            "snapshot version conflicts with exact repository pin",
        ):
            self.assertIn(text, output)

    def test_human_output_distinguishes_no_supported_dependencies(self):
        report = ScanReport(MetricSummary(0, 0, None, 0.0, None, None, None), (), ())
        output = format_human(report, ".")
        self.assertIn("No supported dependency manifests or dependencies were found.", output)
        self.assertIn("Currently supported ecosystems: pypi", output)
        self.assertIn("No libyears measurement was calculated.", output)
        self.assertNotIn("DEPENDENCY", output)
        self.assertNotIn("Coverage:", output)
        self.assertNotIn("Total:", output)
        self.assertNotIn("failure", output.lower())

    def test_human_output_explains_zero_measurement_from_non_exact_versions(self):
        output = format_human(report_with_unmeasurable("non_exact_version"), ".")
        self.assertIn("No libyears measurement could be calculated", output)
        self.assertIn("All discovered dependencies lack exact versions.", output)
        self.assertIn("reproducible measurement", output)
        self.assertIn("exact version not available", output)
        self.assertNotIn("non_exact_version", output)
        self.assertIn("Measured: 0 / 1 dependencies", output)
        self.assertIn("Coverage: 0.0%", output)
        self.assertNotIn("DEPENDENCY", output)
        self.assertNotIn("Total:", output)

    def test_human_output_distinguishes_partial_measurement(self):
        output = format_human(report_with_data(), ".")
        self.assertIn("Partial measurement: 2 / 3 dependencies measured (66.7%).", output)
        self.assertIn("Total:", output)
        self.assertIn("exact version not available", output)
        self.assertNotIn("non_exact_version", output)

    def test_human_output_distinguishes_complete_measurement(self):
        report = report_with_data()
        complete = ScanReport(
            MetricSummary(2, 2, 1.0, 1.002, 0.501, 0.501, 1.0),
            report.measurements,
            (),
        )
        output = format_human(complete, ".")
        self.assertIn("Measurement complete: 2 / 2 dependencies measured.", output)
        self.assertNotIn("Partial measurement", output)

    def test_zero_report_uses_null_values_where_required(self):
        report = ScanReport(MetricSummary(0, 0, None, 0.0, None, None, None), (), ())
        data = report_to_dict(report, ".")
        self.assertIsNone(data["summary"]["coverage"])
        self.assertIsNone(data["summary"]["mean_libyears"])
        human = format_human(report, ".")
        self.assertNotIn("null", human)
        self.assertNotIn("Coverage:", human)
        self.assertNotIn("Total:", human)


class RubyPublicOutputTests(unittest.TestCase):
    def ruby_report(self, reason=None):
        from libyears.model import RubyGemsEvidence, RubyPublicationArtifact, SelectedRubyArtifact, UnmeasurableDependency
        date = datetime(2024, 1, 1, 2, 0, 0, 123456, tzinfo=timezone.utc)
        evidence = RubyGemsEvidence(
            (SelectedRubyArtifact('1.0', 'java', 'https://rubygems.org'),),
            (RubyPublicationArtifact('1.0', 'java', date),),
            (RubyPublicationArtifact('1.0', 'java', date, False),),
        )
        dependency = Dependency('rubygems', 'sample', '1.0', date, '1.0', date,
                                'gemfile_lock', evidence)
        source = SourceResult('rubygems', (), (), (), SourceEvidence(
            'Gemfile.lock', 'Gemfile.lock', 'gemfile_lock', True,
            'all_direct_locked', 'earliest_admissible_supported_observable'), 1, True)
        return MixedScanReport(
            () if reason else (DependencyMeasurement(dependency, 0.0),),
            (UnmeasurableDependency('rubygems', 'sample', 'sample (~> 1)', reason,
                                    RubyGemsEvidence(evidence.selected_artifacts)),) if reason else (),
            (), (source,), MetricSummary(1, 0 if reason else 1, 0.0 if reason else 1.0,
                                         0.0, None if reason else 0.0,
                                         None if reason else 0.0, None if reason else 0.0), {})

    def test_explicit_artifact_serialization_preserves_precision_and_unknown_yank(self):
        data = report_to_dict(self.ruby_report(), '.')
        self.assertEqual(data['schema_version'], 3)
        evidence = data['dependencies'][0]['rubygems_evidence']
        self.assertEqual(evidence['used_publication_artifacts'], [{
            'version': '1.0', 'platform': 'java',
            'publication_time': '2024-01-01T02:00:00.123456Z'}])
        self.assertIs(evidence['latest_publication_artifacts'][0]['yanked'], False)
        failure = report_to_dict(self.ruby_report('registry_error'), '.')['unmeasurable'][0]
        self.assertEqual(set(failure['rubygems_evidence']), {'selected_artifacts'})

    def test_scope_and_history_disclosures_are_present_in_normal_and_verbose_output(self):
        report = self.ruby_report()
        for verbose in (False, True):
            human = format_human(report, '.', verbose=verbose)
            for text in ('RubyGems', 'Gemfile.lock', 'All direct dependencies recorded',
                         'groups are not interpreted', 'not complete historical knowledge',
                         'record disappearance may change future measurements', '0.00', '100.0%'):
                self.assertIn(text, human)
        self.assertEqual(format_json(report, '.'), format_json(
            replace(report, diagnostics=(('sample', 'safe diagnostic'),)), '.'))

    def test_ruby_failure_words_are_contextual_and_preserve_direct_text(self):
        cases = {
            'lock_version_missing': 'exact selected spec unavailable in Gemfile.lock',
            'unsupported_dependency_name': 'unsupported RubyGems dependency name',
            'unsupported_requirement': 'unsupported requirement format',
            'unsupported_lock_evidence': 'unsupported selected version or artifact identity',
            'ambiguous_lock_evidence': 'differing versions or duplicate selected artifacts',
            'unsupported_dependency_source': 'no public namesake is substituted',
            'package_not_found': 'public RubyGems metadata reports package absence',
            'version_not_found': 'supported observable RubyGems records',
            'release_date_missing': 'release timestamp unavailable',
            'invalid_registry_response': 'invalid registry response',
            'registry_error': 'registry or transport error',
            'no_stable_release': 'no stable release available',
        }
        for reason, words in cases.items():
            with self.subTest(reason=reason):
                human = format_human(self.ruby_report(reason), '.')
                self.assertIn(words, human)
                self.assertIn('sample (~> 1)', human)
                self.assertIn('Coverage: 0.0%', human)
                for wrong in ('PyPI', 'package-lock.json', 'yarn.lock'):
                    self.assertNotIn(wrong, human)


class ScopedRubyJsonTests(unittest.TestCase):
    source = 'source "https://rubygems.org"\n'
    lock = ('GEM\n  remote: https://rubygems.org\n  specs:\n    rack (1)\n'
            'PLATFORMS\n  ruby\nDEPENDENCIES\n  rack\n')
    date = datetime(2024, 1, 1, 2, 0, 0, 123456, tzinfo=timezone.utc)

    def scan(self, gemfile, lock, *, groups=('default',), outcome=None, siblings=False):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        for name, text in (('Gemfile', gemfile), ('Gemfile.lock', lock)):
            if text is not None:
                (root / name).write_text(text, encoding='utf-8')
        if siblings:
            (root / 'requirements.txt').write_text('sibling==1\n')
        lookup = Mock(return_value=outcome or RegistryResult(
            'rack', '1', self.date, '1', self.date))
        report = scan_mixed_repository(root, ruby_groups=groups,
                                      rubygems_lookup=lookup,
                                      pypi_lookup=lambda name, version: RegistryResult(
                                          name, version, self.date, version, self.date))
        return report, lookup

    def evidence(self, groups, accepted):
        return {
            'declaration_source': 'Gemfile', 'snapshot_source': 'Gemfile.lock',
            'scope': 'selected_declared_groups', 'requested_groups': list(groups),
            'format': 'gemfile_lock' if accepted else None,
            'publication_basis': 'earliest_admissible_supported_observable',
        }

    def test_source_evidence_presence_and_null_format_across_unavailable_states(self):
        cases = (
            (None, self.lock, ('default',), 'gemfile_missing', None),
            ('end\n', self.lock, ('default',), 'invalid_gemfile', None),
            (self.source, self.lock, ('test',), 'unknown_ruby_group', None),
            (self.source + 'gem "rack"\n', 'BAD\n', ('default',),
             'unsupported_lockfile_format', 1),
            (self.source, 'BAD\n', ('default',), 'unsupported_lockfile_format', 0),
        )
        for gemfile, lock, groups, reason, count in cases:
            with self.subTest(reason=reason, count=count):
                report, lookup = self.scan(gemfile, lock, groups=groups)
                data = json.loads(format_json(report, '.'))
                self.assertEqual(data['schema_version'], 3)
                self.assertEqual(data['version_evidence'], {
                    'rubygems': self.evidence(groups, False)})
                self.assertEqual(data['ecosystems'], ['rubygems'])
                self.assertEqual(set(data['summary']['by_ecosystem']), {'rubygems'})
                self.assertEqual(data['source_errors'], [{
                    'ecosystem': 'rubygems',
                    'source': 'Gemfile.lock' if reason == 'unsupported_lockfile_format' else 'Gemfile',
                    'reason': reason,
                }])
                self.assertEqual(data['summary']['dependencies_discovered'], count)
                self.assertIsNone(data['summary']['coverage'])
                self.assertEqual(data['dependencies'], [])
                self.assertEqual(data['unmeasurable'], [])
                lookup.assert_not_called()

    def test_empty_scopes_keep_requested_inputs_and_recognition_state(self):
        for lock in (None, self.lock):
            with self.subTest(lock=lock):
                report, lookup = self.scan(self.source, lock)
                data = report_to_dict(report, '.')
                self.assertEqual(data['version_evidence'], {
                    'rubygems': self.evidence(('default',), lock is not None)})
                self.assertEqual(data['summary']['dependencies_discovered'], 0)
                self.assertEqual(data['summary']['dependencies_measured'], 0)
                self.assertIsNone(data['summary']['coverage'])
                self.assertEqual(data['unmeasurable'], [])
                self.assertEqual(data['source_errors'], [])
                lookup.assert_not_called()

    def test_missing_lock_and_missing_direct_omit_unknown_requirement(self):
        for lock, reason in ((None, 'lockfile_missing'),
                             (self.lock.replace('  rack\n', '  other\n'),
                              'lock_dependency_missing')):
            with self.subTest(reason=reason):
                report, lookup = self.scan(self.source + 'gem "rack", "= 1"\n', lock)
                data = report_to_dict(report, '.')
                self.assertEqual(data['unmeasurable'], [{
                    'ecosystem': 'rubygems', 'name': 'rack', 'declared': 'rack (= 1)',
                    'reason': reason, 'gemfile_evidence': {
                        'declared_groups': ['default'], 'declaration_requirements': ['= 1'],
                    },
                }])
                self.assertEqual(data['version_evidence']['rubygems'],
                                 self.evidence(('default',), lock is not None))
                self.assertEqual(data['summary']['coverage'], 0.0)
                lookup.assert_not_called()

    def test_measured_evidence_keeps_full_memberships_requirement_order_and_artifacts(self):
        publications = RubyGemsEvidence((),
            (RubyPublicationArtifact('1', 'ruby', self.date),),
            (RubyPublicationArtifact('1', 'ruby', self.date, False),))
        report, lookup = self.scan(
            self.source + 'gem "rack", ">= 1", "< 3", groups: [:test, :production, :Test]\n',
            self.lock.replace('  rack\n', '  rack (>= 1, < 3)\n'),
            groups=('production', 'Test', 'production'),
            outcome=RegistryResult('rack', '1', self.date, '1', self.date, publications))
        data = json.loads(format_json(report, '.'))
        self.assertEqual(data['version_evidence'], {
            'rubygems': self.evidence(('Test', 'production'), True)})
        self.assertEqual(data['dependencies'], [{
            'ecosystem': 'rubygems', 'name': 'rack', 'used_version': '1',
            'used_release_time': '2024-01-01T02:00:00.123456Z',
            'latest_stable_version': '1',
            'latest_stable_release_time': '2024-01-01T02:00:00.123456Z',
            'libyears': 0.0, 'timestamp_anomaly': False, 'version_source': 'gemfile_lock',
            'gemfile_evidence': {
                'declared_groups': ['Test', 'production', 'test'],
                'declaration_requirements': ['>= 1', '< 3'], 'lock_requirement': '>= 1, < 3',
            },
            'rubygems_evidence': {
                'selected_artifacts': [{'version': '1', 'platform': 'ruby',
                                        'source': 'https://rubygems.org'}],
                'used_publication_artifacts': [{'version': '1', 'platform': 'ruby',
                    'publication_time': '2024-01-01T02:00:00.123456Z'}],
                'latest_publication_artifacts': [{'version': '1', 'platform': 'ruby',
                    'publication_time': '2024-01-01T02:00:00.123456Z', 'yanked': False}],
            },
        }])
        lookup.assert_called_once_with('rack', '1')
        self.assertEqual(data['schema_version'], 3)

    def test_known_absent_requirement_is_null_on_success_local_and_registry_failure(self):
        cases = (
            (self.lock, None, None),
            (self.lock.replace('    rack (1)\n', ''), None, 'lock_version_missing'),
            (self.lock, RegistryFailure('rack', '1', 'registry_error', 'safe diagnostic'),
             'registry_error'),
        )
        for lock, outcome, reason in cases:
            with self.subTest(reason=reason):
                report, lookup = self.scan(self.source + 'gem "rack"\n', lock, outcome=outcome)
                data = report_to_dict(report, '.')
                row = data['unmeasurable'][0] if reason else data['dependencies'][0]
                self.assertEqual(row['gemfile_evidence'], {
                    'declared_groups': ['default'], 'declaration_requirements': [],
                    'lock_requirement': None,
                })
                if reason:
                    self.assertEqual(row['reason'], reason)
                    self.assertEqual(row['declared'], 'rack')
                if reason == 'registry_error':
                    self.assertEqual(row['rubygems_evidence'], {'selected_artifacts': [{
                        'version': '1', 'platform': 'ruby', 'source': 'https://rubygems.org'}]})
                if reason == 'lock_version_missing':
                    self.assertNotIn('rubygems_evidence', row)
                    lookup.assert_not_called()
                else:
                    lookup.assert_called_once_with('rack', '1')
                self.assertEqual(format_json(report, '.'), format_json(
                    replace(report, diagnostics=(('rack', 'HUMAN_ONLY_DIAGNOSTIC'),)), '.'))
                self.assertNotIn('HUMAN_ONLY_DIAGNOSTIC', format_json(report, '.'))

    def test_f1_and_f2_preserve_safe_evidence_and_never_echo_unsafe_text(self):
        cases = (
            ('source "https://PRIVATE_MARKER.invalid"\n', 'other',
             'unsupported_dependency_source', []),
            (self.source, 'rack (https://UNSAFE_MARKER.invalid)',
             'unsupported_requirement', ['>= 1']),
        )
        for source, direct, reason, requirements in cases:
            with self.subTest(reason=reason):
                declaration = 'gem "rack"' + (', ">= 1"' if requirements else '') + '\n'
                report, lookup = self.scan(source + declaration,
                                          self.lock.replace('  rack\n', '  ' + direct + '\n'))
                data = report_to_dict(report, '.')
                self.assertEqual(data['unmeasurable'], [{
                    'ecosystem': 'rubygems', 'name': 'rack',
                    'declared': 'rack (>= 1)' if requirements else 'rack', 'reason': reason,
                    'gemfile_evidence': {'declared_groups': ['default'],
                                         'declaration_requirements': requirements},
                }])
                self.assertEqual(data['summary']['dependencies_discovered'], 1)
                self.assertEqual(data['summary']['coverage'], 0.0)
                for marker in ('PRIVATE_MARKER', 'UNSAFE_MARKER'):
                    self.assertNotIn(marker, format_json(report, '.'))
                lookup.assert_not_called()

    def test_scoped_failures_retain_only_established_artifact_populations(self):
        publication = RubyGemsEvidence((),
            (RubyPublicationArtifact('1', 'ruby', self.date),), ())
        cases = (
            (self.lock.replace('    rack (1)\n', '    rack (1)\n    rack (unknown)\n'),
             None, 'unsupported_lock_evidence'),
            (self.lock, RegistryFailure('rack', '1', 'release_date_missing',
                                       'safe diagnostic', publication), 'release_date_missing'),
        )
        for lock, outcome, reason in cases:
            with self.subTest(reason=reason):
                report, lookup = self.scan(self.source + 'gem "rack"\n', lock, outcome=outcome)
                row = report_to_dict(report, '.')['unmeasurable'][0]
                expected = {'selected_artifacts': [{
                    'version': '1', 'platform': 'ruby', 'source': 'https://rubygems.org'}]}
                if outcome is not None:
                    expected['used_publication_artifacts'] = [{
                        'version': '1', 'platform': 'ruby',
                        'publication_time': '2024-01-01T02:00:00.123456Z'}]
                    expected['latest_publication_artifacts'] = []
                    lookup.assert_called_once_with('rack', '1')
                else:
                    lookup.assert_not_called()
                self.assertEqual(row['reason'], reason)
                self.assertEqual(row['rubygems_evidence'], expected)
                self.assertEqual(row['gemfile_evidence'], {
                    'declared_groups': ['default'], 'declaration_requirements': [],
                    'lock_requirement': None,
                })

    def test_mismatch_preserves_both_literal_values_without_version_artifacts(self):
        cases = (
            ('gem "rack"\n', '>= 0', []),
            ('gem "rack", ">= 0"\n', None, ['>= 0']),
            ('gem "rack", " >= 1 ", "< 3"\n', '< 3, >= 1', [' >= 1 ', '< 3']),
        )
        for declaration, requirement, expected in cases:
            with self.subTest(requirement=requirement):
                direct = 'rack' if requirement is None else 'rack (' + requirement + ')'
                report, lookup = self.scan(self.source + declaration,
                                          self.lock.replace('  rack\n', '  ' + direct + '\n'))
                self.assertEqual(report_to_dict(report, '.')['unmeasurable'], [{
                    'ecosystem': 'rubygems', 'name': 'rack',
                    'declared': 'rack' + (' (' + ', '.join(expected) + ')' if expected else ''),
                    'reason': 'declaration_lock_requirement_mismatch',
                    'gemfile_evidence': {'declared_groups': ['default'],
                        'declaration_requirements': expected, 'lock_requirement': requirement},
                }])
                lookup.assert_not_called()

    def test_human_measured_scope_and_evidence_match_json_in_both_branches(self):
        for siblings in (False, True):
            report, _ = self.scan(
                self.source + 'gem "rack", ">= 1", "< 3", groups: [:production, :test]\n',
                self.lock.replace('  rack\n', '  rack (>= 1, < 3)\n'),
                groups=('production',), siblings=siblings)
            before = format_json(report, '.')
            for verbose in (False, True):
                human = format_human(report, '.', verbose=verbose)
                for text in ('selected declared groups: production',
                             'supplied version snapshot: Gemfile.lock',
                             'Supplied declaration source: Gemfile',
                             'Gemfile.lock recognition: accepted',
                             'declared groups: production, test',
                             'declaration requirements: [">= 1", "< 3"]',
                             'Gemfile.lock requirement: ">= 1, < 3"',
                             'does not establish installed/deployed/runtime scope or historical coherence',
                             'not complete historical knowledge', 'record disappearance', '100.0%'):
                    self.assertIn(text, human)
                self.assertNotIn('groups are not interpreted', human)
                self.assertNotIn('All direct dependencies recorded', human)
            self.assertEqual(before, format_json(report, '.'))

    def test_human_empty_unavailable_and_wholly_unmeasurable_remain_distinct(self):
        cases = (
            (self.source, None, 'scope is empty', '0 / 0', None),
            (None, self.lock, 'scope unavailable', 'None / None', None),
            (self.source + 'gem "rack"\n', 'BAD\n', 'measurement unavailable', 'None / 1', None),
            (self.source + 'gem "rack"\n', None, 'wholly unmeasurable', '0 / 1', 0.0),
        )
        for gemfile, lock, text, counts, coverage in cases:
            for siblings in (False, True):
                with self.subTest(text=text, siblings=siblings):
                    report, _ = self.scan(gemfile, lock, siblings=siblings)
                    data = report_to_dict(report, '.')
                    self.assertEqual(data['summary']['by_ecosystem']['rubygems']['coverage'], coverage)
                    for verbose in (False, True):
                        human = format_human(report, '.', verbose=verbose)
                        self.assertIn(text, human)
                        self.assertIn(counts, human)
                        if lock is None:
                            self.assertIn('Gemfile.lock recognition: unavailable', human)

    def test_human_failures_retain_safe_metadata_and_omit_unsupported_text(self):
        cases = (
            ('source "https://PRIVATE_MARKER.invalid"\ngem "rack"\n',
             self.lock.replace('  rack\n', '  other\n'), None,
             'nonpublic Gemfile sources are unsupported', 'unavailable'),
            (self.source + 'gem "rack", ">= 1"\n',
             self.lock.replace('  rack\n', '  rack (https://UNSAFE_MARKER.invalid)\n'),
             None, 'unsupported requirement format', 'unavailable'),
            (self.source + 'gem "rack", ">= 1"\n', self.lock, None,
             'textual requirement evidence differs; equivalence not inferred', 'null'),
            (self.source + 'gem "rack"\n', self.lock.replace('  rack\n', '  other\n'),
             None, 'absent from direct Gemfile.lock dependencies', 'unavailable'),
            (self.source + 'gem "rack"\n', self.lock,
             RegistryFailure('rack', '1', 'registry_error', 'safe registry diagnostic'),
             'registry or transport error', 'null'),
        )
        for gemfile, lock, outcome, reason, lock_text in cases:
            for siblings in (False, True):
                with self.subTest(reason=reason, siblings=siblings):
                    report, _ = self.scan(gemfile, lock, outcome=outcome, siblings=siblings)
                    data = report_to_dict(report, '.')
                    self.assertEqual(data['summary']['by_ecosystem']['rubygems']['coverage'], 0.0)
                    for verbose in (False, True):
                        human = format_human(report, '.', verbose=verbose)
                        for text in (reason, 'declared groups: default',
                                     'Gemfile.lock requirement: ' + lock_text, '0.0%'):
                            self.assertIn(text, human)
                        for marker in ('UNSAFE_MARKER', 'PRIVATE_MARKER'):
                            self.assertNotIn(marker, human)
                            self.assertNotIn(marker, format_json(report, '.'))
                        if verbose and outcome:
                            self.assertIn('safe registry diagnostic', human)
                        elif outcome:
                            self.assertNotIn('safe registry diagnostic', human)
                    if reason.startswith('unsupported requirement'):
                        self.assertIn('declaration requirements: [">= 1"]', human)
                        self.assertNotIn('lock_requirement', data['unmeasurable'][0]['gemfile_evidence'])

    def test_human_source_reasons_are_contextual_and_safe(self):
        cases = (
            (None, 'Gemfile unavailable'),
            ('end\n', 'malformed declaration evidence'),
            (self.source + 'eval_gemfile "UNSAFE_MARKER"\n', 'unsupported static declaration syntax'),
            (self.source + 'gem "rack"\ngem "rack"\n', 'duplicate gem declarations'),
            (self.source, 'group is not established'),
        )
        for gemfile, reason in cases:
            report, lookup = self.scan(gemfile, self.lock, groups=('test',))
            lookup.assert_not_called()
            for verbose in (False, True):
                human = format_human(report, '.', verbose=verbose)
                self.assertIn(reason, human)
                self.assertNotIn('UNSAFE_MARKER', human)

    def test_ordinary_ruby_shape_is_unchanged_and_scoped_serializer_is_explicit(self):
        ordinary = RubyPublicOutputTests().ruby_report()
        data = report_to_dict(ordinary, '.')
        self.assertEqual(data['version_evidence'], {'rubygems': {
            'declaration_source': 'Gemfile.lock', 'snapshot_source': 'Gemfile.lock',
            'format': 'gemfile_lock', 'scope': 'all_direct_locked',
            'publication_basis': 'earliest_admissible_supported_observable',
        }})
        self.assertEqual(set(data['dependencies'][0]), {
            'ecosystem', 'name', 'used_version', 'used_release_time', 'latest_stable_version',
            'latest_stable_release_time', 'libyears', 'timestamp_anomaly', 'version_source',
            'rubygems_evidence',
        })
        self.assertNotIn('gemfile_evidence', report_to_dict(
            RubyPublicOutputTests().ruby_report('registry_error'), '.')['unmeasurable'][0])
        dependency = replace(ordinary.measurements[0].dependency,
            gemfile_evidence=GemfileEvidence(('test', 'Test', 'test'), ('< 3', '>= 1'),
                                            'UNAVAILABLE_MARKER', False))
        source = replace(ordinary.source_results[0], evidence=replace(
            ordinary.source_results[0].evidence, requested_groups=('test', 'Test', 'test')))
        scoped = replace(ordinary, measurements=(DependencyMeasurement(dependency, 0.0),),
                         source_results=(source,))
        serialized = report_to_dict(scoped, '.')
        self.assertEqual(serialized['dependencies'][0]['gemfile_evidence'], {
            'declared_groups': ['Test', 'test'], 'declaration_requirements': ['< 3', '>= 1'],
        })
        self.assertEqual(serialized['version_evidence']['rubygems']['requested_groups'],
                         ['Test', 'test'])
        self.assertNotIn('UNAVAILABLE_MARKER', format_json(scoped, '.'))
        self.assertNotIn('include_lock_requirement', format_json(scoped, '.'))


if __name__ == "__main__":
    unittest.main()
