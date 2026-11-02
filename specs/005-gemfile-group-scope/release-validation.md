# Feature 005: release-validation evidence and preparation

## Disposition

**T011 COMPLETE — documentation and procedure preparation only (005-0017).**
**T012 NOT STARTED — pending explicit human authorization identifying a target
root or specifically permitted supplied evidence. T013 NOT STARTED.**
No real-root target was selected, searched for, inspected or analyzed; no external
checkout/remote repository or live registry was accessed in this run. Preparation
and synthetic examples do not satisfy T012 or establish convergence/release
readiness. No push, tag or release is authorized.

## Deterministic correctness evidence

The canonical [T010 acceptance index](../../tests/fixtures/ruby_groups/README.md#deterministic-acceptance-index-t010)
contains **AC-01 through AC-28, 28/28**, each mapped to concrete test methods and
observable assertions. It includes closed-language positive/negative tables,
source/dependency precedence, F1/F2, P1 for both inputs, exact CLI ages, safe
single/mixed human/JSON output, coverage, compatibility and integrity witnesses.
The [task record](tasks.md#t010--composed-acceptance-and-regression-verification)
preserves commands/results and implementation ownership; the [approved spec](spec.md#s5--acceptance-criteria)
defines the obligations. This index is offline correctness evidence, not proof of
application subset coverage or the required real-root population comparison.

Additional sole-option spelling evidence after T010 is in
`tests/test_cli.py`, `ScopedRubyCLITests.test_abbreviated_group_options_are_usage_errors_before_scan`
and `test_ordinary_option_spellings_and_abbreviations_remain_compatible` (see the corrected
[checkpoint record](reviews.md#focused-independent-post-t010-c-01-verification--005-0016)).

| Boundary | Status and durable evidence |
|---|---|
| Post-T005 foundation | COMPLETE / APPROVE, zero material findings; [005-0014 review](reviews.md#independent-post-t005-implementation-checkpoint--005-0014), frozen implementation `09be9fb`, 357 tests/no skips. P1 includes four bounded regular-to-FIFO witnesses plus capability refusal mocks. |
| Original post-T010 candidate | Historical COMPLETE / REVISE, C-01; [005-0015 review](reviews.md#independent-post-t010-implementation-checkpoint--005-0015). Its 388-test result did not establish rejection of abbreviated scoped options. |
| Corrected post-T010 checkpoint | COMPLETE / APPROVE, C-01 closed, T009 restored and T010 accepted; [005-0016 review](reviews.md#focused-independent-post-t010-c-01-verification--005-0016), frozen correction `ecc492407e1e6fd6a3947142b72f9e50ecca423b`. Foundation unchanged. |

Latest full deterministic suite: **390 passed, no skips**, retained from
005-0016; parent and independent reviewer each ran the commands below. This is
prior approved evidence, not a new full-suite run in T011. Documentation-only
changes do not change product/tests; focused report/CLI/example checks suffice
for this checkpoint.

| Exact command (005-0016) | Observed result, each verifier |
|---|---|
| `python -m unittest tests.test_cli tests.test_ruby_group_acceptance` | 32 passed |
| `python -m unittest tests.test_scoped_scan tests.test_mixed_scan tests.test_scan tests.test_output tests.test_ruby_groups tests.test_gemfile tests.test_gemfile_evidence tests.test_gemfile_lock tests.test_pypi tests.test_npm tests.test_npm_registry tests.test_yarn tests.test_rubygems tests.test_rubygems_registry tests.test_registry tests.test_metric` | 335 passed |
| `python -m unittest discover -s tests` | 390 passed, no skips |
| `git diff --check` | Passed |

T011 verification (005-0017):

| Exact command/check | Observed result |
|---|---|
| `python -m unittest tests.test_cli tests.test_output tests.test_ruby_group_acceptance` | 62 passed, no skips; synthetic fixtures/mocks only |
| `python -` with the example-check script below | 6 synthetic offline CLI invocations passed; README human/JSON fragments, selected counts, missing-lock reasons and integrity matched |
| Local Markdown link/AC-index/ledger/scope assertions | Passed; 28/28 AC entries; 005-0001–005-0016 once each, 44 fields per row; ledger identical to starting HEAD |
| `git diff --check` | Passed |

README, SPEC section 26 and curated CHANGELOG Unreleased/Added agree with
implemented `libyears/cli.py`, `scan.py`, `gemfile.py`, `rubygems.py` and scoped
`output.py` behavior. Both documented command forms use the actual repeatable
option. Human excerpts and JSON fragment below are verified without hypothetical
output or a live application. Limits/field detail remains canonical in spec/plan.
No deployment, installation, runtime or historical-coherence certification is made;
ordinary no-request all-direct Ruby behavior remains explicit.

### Reproducible README example check (synthetic only)

Run `python -` with this script as stdin from the repository root. It creates
only a temporary synthetic Gemfile, with no lock; no application is involved.
The two group selections and three report flag combinations match the README.

```python
import io, json, re, tempfile
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch
from libyears.cli import main

readme = Path('README.md').read_text()
fragment = json.loads(re.findall(r'```json\n(.*?)\n```', readme, re.S)[-1])
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    gemfile = root / 'Gemfile'
    gemfile.write_text('source "https://rubygems.org"\n'
                       'gem "rack", "~> 3.0"\ngroup :test do\n'
                       '  gem "rake"\nend\n')
    before = gemfile.read_bytes()
    with patch('urllib.request.OpenerDirector.open',
               side_effect=AssertionError('network forbidden')):
        for groups, names in ((['default'], ['rack']),
                              (['default', 'test'], ['rack', 'rake'])):
            options = [p for g in groups for p in ('--ruby-group', g)]
            for flags in ([], ['--json'], ['--json', '--verbose']):
                out, err = io.StringIO(), io.StringIO()
                with redirect_stdout(out), redirect_stderr(err):
                    code = main([str(root), *options, *flags])
                assert (code, err.getvalue()) == (0, '')
                if '--json' in flags:
                    data = json.loads(out.getvalue())
                    rows = data['unmeasurable']
                    assert sorted(r['name'] for r in rows) == names
                    assert all(r['reason'] == 'lockfile_missing' for r in rows)
                    assert data['summary']['dependencies_discovered'] == len(names)
                    assert data['summary']['dependencies_measured'] == 0
                    assert data['summary']['coverage'] == 0.0
                    if groups == ['default']:
                        assert rows == [fragment]
                else:
                    lines = [f"RubyGems selected declared groups: {', '.join(groups)}.",
                             'Supplied declaration source: Gemfile; supplied version snapshot: Gemfile.lock.']
                    assert all(line in out.getvalue() for line in lines)
                    if groups == ['default']:
                        assert all(line in readme for line in lines)
    assert gemfile.read_bytes() == before
    assert sorted(p.name for p in root.iterdir()) == ['Gemfile']
print('6 synthetic offline CLI examples passed; fragments/counts/integrity matched')
```

An initial T011 example harness incorrectly compared pretty-printed JSON text
with compact-array documentation formatting. It failed that formatting assertion;
inspection confirmed the row values matched. The script above compares parsed
JSON and passed; no product or example content correction was required.

## Future T012 real-root validation PROCEDURE — NOT EXECUTED

The following steps are instructions for a future authorized run, not completed
evidence. **T012 remains pending explicit human authorization.** No prior Feature
003/004 target permission transfers here. Do not search for or inspect candidates
before receiving authorization. Synthetic fixtures cannot substitute for this gate.

1. Obtain explicit human authorization naming the particular target root OR
   specifically permitted supplied evidence, exact allowed files/access and
   requested exact group names. The authorization must identify exact target/
   input/revision provenance, an independent expected selected population,
   expected recognition/rejection behavior, denominator versus measured/
   unmeasurable expectations and required before/after integrity evidence.
   Do not begin dependent validation while any required authorization input is
   missing. Record the authorization scope and evidence
   provenance without sensitive workstation paths or environment-specific trust
   details. Target selection/access is not authorized by this procedure.
2. Establish exact target/input/revision provenance: repository identity and
   revision where available, supplied-file origin, exact Gemfile/Gemfile.lock
   content hashes and any material working-copy differences. For supplied
   evidence record who supplied it, its revision association and limits; never
   infer that matching names/requirements prove historical coherence. Distinguish
   human attestation from independently inspected facts. Record unavailable
   metadata as unavailable.
3. Before running the product, independently establish the expected selected
   population from the permitted complete inputs. Preserve each selected name,
   declared full memberships, requested groups, union/deduplication and explicit
   default behavior. State expected complete recognition or precise rejection
   constructs/reasons (including syntax in unselected groups), lock recognition
   and authority/association expectations. Do not use product output itself as
   the expected-population oracle. If independent scope cannot be established,
   report insufficient evidence rather than inventing a denominator.
4. Record before-target integrity evidence under the authorized boundary: input
   hashes plus an agreed manifest of relevant names/types/bytes and symlink text
   without following escaping targets. Keep captures outside the target. For
   supplied evidence require equivalent before/after integrity records or an
   explicitly identified human attestation with its verification limits.
5. Use the implemented CLI entry point with repeated canonical `--ruby-group`
   options for the authorized names; capture both human and JSON reports and
   exact invocation/revision. Default to mocked/supplied registry results with
   their provenance, using a bounded harness as in deterministic CLI tests.
   No registry contact is permitted unless separately authorized. Do not run
   Ruby/Bundler/project tooling, install/resolve, fetch archives/private content,
   inspect config/credentials, modify the target or weaken TLS.
6. Compare independent expected versus observed recognition/rejection and selected
   identities, per-name evidence and exclusion/lookup populations. Separate N
   (discovered selected denominator) from M (measured) and N-M unmeasurable rows
   for available nonempty measurement. Record exact reasons and safe provenance;
   missing lock/direct/version and textual mismatch are not recognition success
   with measured versions. For unavailable Gemfile/unknown groups N is null;
   rejected lock retains N but M/coverage/aggregates are null with no rows.
   Known empty scope is 0/0 with null coverage, whereas known nonempty wholly
   unmeasurable scope is M=0 and 0%. Check repository/sibling summaries and human
   versus JSON agreement, retaining supported observable-publication limits.
7. Capture the same after-target integrity evidence and compare before/after.
   Record actual commands, exact results, expected versus observed populations,
   rejected constructs, input limitations and evidence locations. Restrict public
   records to safe provenance. If unsupported evidence prevents the required
   successful population comparison, or authority/evidence is unavailable, leave
   T012 pending; do not replace it with a synthetic fixture or optional smoke.
8. Only a later authorized run may assess T012 completion from sufficient real-root
   evidence. Stop before T013 unless separately commissioned; preparation and
   deterministic passing tests alone cannot establish convergence.

## Required versus optional validation

- **Deterministic correctness:** indexed above, offline fixtures/mocks; current
  approved full-suite evidence is 390 passed/no skips. This gate is satisfied.
- **Required authorized real-root evidence (T012):** NOT STARTED. Requires the
  named target/permitted supplied evidence, independent expected selected
  population, exact provenance, recognition/rejection comparison, denominator
  versus measurement accounting and before/after integrity. It remains required
  before T013 convergence; this procedure supplies no access permission.
- **Optional live registry smoke:** NOT PERFORMED or commissioned. Requires
  separate target/network authorization and verified existing transport. Record
  live outcomes/environmental failures separately. It cannot replace offline
  correctness or the required real-root comparison and has no mandatory task
  dependency. Never weaken trust controls or invoke a package manager for it.
