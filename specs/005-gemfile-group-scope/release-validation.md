# Feature 005: release-validation evidence and preparation

## Disposition

**T011 COMPLETE (005-0017). T012 COMPLETE (005-0018). T013 NOT STARTED.**
Three exact roots were explicitly authorized for read-only offline validation.
One successful real-root population comparison, one expected rejection and one
insufficient-evidence result are preserved below. No implementation defect was
found. This is T012 evidence, not convergence or release approval. No push,
tag or release occurred. The T011 preparation record below remains historical.

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

## T012 real-root validation procedure — prepared in 005-0017

The following procedure was prepared without execution in 005-0017. Its later
authorized execution is recorded below; the procedure itself supplies no permission. No prior Feature
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
- **Required authorized real-root evidence (T012):** COMPLETE in 005-0018 below. Required the
  named target/permitted supplied evidence, independent expected selected
  population, exact provenance, recognition/rejection comparison, denominator
  versus measurement accounting and before/after integrity. It remains required
  before T013 convergence; this procedure supplies no access permission.
- **Optional live registry smoke:** NOT PERFORMED or commissioned. Requires
  separate target/network authorization and verified existing transport. Record
  live outcomes/environmental failures separately. It cannot replace offline
  correctness or the required real-root comparison and has no mandatory task
  dependency. Never weaken trust controls or invoke a package manager for it.

## T012 authorized real-root evidence — 005-0018

**Disposition: COMPLETE.** Explicit human authority for this run names exactly
A `iv-cbv-payroll`, B `price-transparency-guide`, and C `dpc-admin`. C was newly
authorized for Feature 005; historical baseline familiarity supplied no expected
population or permission. Access was limited to root Gemfile/Gemfile.lock and Git
revision/status metadata. No alternate/nested target was sought. Local paths are
nonpublic authorization inputs and are deliberately omitted here.

### Method, chronology and offline provenance

All approved Feature 005 artifacts, including the complete T012 definition and
procedure and review history, were read before target access. Inputs were read
independently of libyears. A was absent; B's entire six-line Gemfile and entire
lock were manually interpreted against S1–S4. C's entire Gemfile and lock were
inspected independently; rejection at line 2 prevents any complete population
claim. No product parser, source function or output supplied the expectation.
The expected record was frozen **before any product invocation**, SHA-256
`1b74c2ef366309ebf37e7d2a227985d1e381752fa25c9235ddbef18642ff434a`.

The implemented entry point was `libyears.cli.main(argv, scan=scan)` with
canonical repeated `--ruby-group GROUP`, once human and once `--json` for each
case below, always against the authorized original root. A/C use `default` only
as rejection probes, without asserting an established group or population.
B uses `default`, `test`, `default+test`, and `test+default+test`; the last tests
canonical sorting/deduplication. Two registry scenarios per request make **12
cases / 24 CLI reports**, all exit 0 with empty stderr.

The scan callback delegates to the real `scan_mixed_repository` with injected
`rubygems_lookup`. To honor the Ruby-only input authorization, its Python/npm
source functions are mocked to absent `SourceResult`s (empty rows/errors,
N=0, measurement available, source_present=False); their lookup callbacks fail
if called. Thus no Python/npm application content is inspected and this run
makes no sibling-source discovery claim. Existing deterministic sibling evidence
remains in T010; repository summaries here cover only Ruby.

Registry evidence is **run-authored synthetic adapter output**, not registry
observations or a claim about these packages' actual ages:

```python
# Only the independently expected names/versions below may reach lookup.
# Scenario supplied:
RegistryResult(name, version, datetime(2020, 1, 1, tzinfo=timezone.utc),
               version, datetime(2020, 1, 1, tzinfo=timezone.utc))
# Scenario missing_date:
RegistryFailure(name, version, 'release_date_missing')
```

Both scenarios were fixed in the pre-product expectation. Same used/latest
version yields exactly 0.0 libyears. The adapter supplies no publication artifacts;
JSON correctly retains selected lock artifacts without inventing observable
publication records. Socket construction/connection, urllib opener access and
subprocess execution raise assertions throughout product execution. No adapter
HTTP, network, Ruby, Bundler, package manager or target code was invoked.

Before and after, only the two permitted input names were lstat'ed and, if
regular, opened read-only with O_NOFOLLOW|O_NONBLOCK, descriptor regular-file
validation and bounded binary reads. No symlink was followed. The integrity
manifest records each name's absence or regular type, mode, byte count, SHA-256
and symlink text (null for all present inputs), plus root symlink status and
Git metadata. All three roots are nonsymlinks. All before/after records match
exactly. No target writes were made; captures stayed outside targets.

Metadata commands, with `ROOT` standing for the authorized local root, were:

```text
git --no-optional-locks -c core.fsmonitor=false -C ROOT rev-parse HEAD
git --no-optional-locks -c core.fsmonitor=false -C ROOT status --porcelain=v1 --untracked-files=no
git --no-optional-locks -c core.fsmonitor=false -C ROOT status --porcelain=v1 --untracked-files=all -- Gemfile Gemfile.lock
git --no-optional-locks -c core.fsmonitor=false -C ROOT rev-parse --show-prefix
PYTHONPATH=. python CAPTURE/validate.py
```

`CAPTURE` denotes the nonpublic temporary run capture directory, outside Git.
It contains `expected-before-product.json`, `validate.py`, `results.json`,
`A/B/C-before.json`, equivalent after manifests, permitted binary input copies
and per-case human/JSON captures. Public reproduction requires the exact hashed
inputs and authorized root mapping; this record does not publish target content
or workstation topology. Reports in the capture replace their display path with
the safe target name. Complete expectations/results needed for review are below.

### Target A — iv-cbv-payroll

- Independently inspected revision: `9e80a7271f39271c878f4bd4cc38af09345e00c5`.
  Tracked status and permitted-input status clean; Git prefix empty. No remote
  identity/config was read; safe identity is the human-supplied target label.
- Both exactly named root inputs are **absent**, so no input hashes/bytes exist.
  No descendant search or alternate repository was used.
- Request: `default` rejection probe. Expected complete recognition unavailable;
  explicit groups, implicit/default membership, per-dependency memberships,
  union, association, source authority and population cannot be established.
  Lock is absent and must not be processed after the Gemfile failure.
- Observed in both registry scenarios/formats: `source_errors` contains exactly
  `Gemfile / gemfile_missing`; no dependency/unmeasurable rows or lookup.
  Requested groups `[default]`, format null. **N=null, M=null, N-M unavailable**,
  zero unmeasurable rows; Ruby coverage and every Ruby aggregate null.
- Human/JSON agree on unavailable scope/lock recognition and null accounting.
  Repository N/M/coverage are null; total remains 0.0, other numeric aggregates
  null, consistent with the existing repository aggregation contract.
- Integrity: both absences and provenance unchanged before/after.
  **Outcome: INSUFFICIENT EVIDENCE**, correctly explained by missing root inputs;
  no claim of successful population validation or implementation defect.

### Target B — price-transparency-guide

- Independently inspected revision: `66898bbd09f00612ffaaac76ea6a740e453904e4`.
  Tracked status and permitted-input status clean; Git prefix empty. Identity
  limitations are the same as A; no remote was consulted.
- Gemfile: regular, mode 0644, 85 bytes, SHA-256
  `d021c5de245ece8064c78fdcb69727454366afe1d9d9b23c8b76980a3d329308`.
- Gemfile.lock: regular, mode 0644, 779 bytes, SHA-256
  `f55183fcb3ca464d283267fa495f68149946065dd3fdf06af9826117aa6a9408`.
- Complete static recognition expected and observed. Exactly one top-level
  public source and a supported `group :test do` block establish groups
  `default` and `test`. Default is implicitly established **empty**; neither
  dependency acquires default membership. No other explicit group exists.

| Independently expected declaration | Complete memberships | Declaration requirements | Direct lock requirement | Selected exact generic version |
|---|---|---|---|---|
| json_schemer | test | [] | null | 2.5.0 |
| rspec | test | [] | null | 3.13.2 |

The entire lock has a single public GEM remote, unique generic specs/direct
identities, supported PLATFORMS and BUNDLED WITH sections. Both direct names
match exactly, neither is pinned, and absence equals absence for requirement
comparison. Both independently authorize selected artifacts with platform `ruby`
and source `https://rubygems.org`. All remaining specs are transitive and excluded
from scoped rows, counts and lookups.

| Requested options, in supplied order | Independent expected = observed names | Supplied N / M / unmeasurable | Missing-date N / M / unmeasurable |
|---|---|---|---|
| default | empty | 0 / 0 / 0 | 0 / 0 / 0 |
| test | json_schemer, rspec | 2 / 2 / 0 | 2 / 0 / 2 |
| default, test | json_schemer, rspec | 2 / 2 / 0 | 2 / 0 / 2 |
| test, default, test | json_schemer, rspec | 2 / 2 / 0 | 2 / 0 / 2 |

No default is added automatically; unions and repeated selections count each
name once. Serialized requests are sorted unique; row membership remains the
full `[test]`. Each selected name is looked up once per report, using precisely
the version above; empty scope makes zero calls. JSON has schema 3, accepted
`gemfile_lock` format, declaration requirements `[]`, present
`lock_requirement: null`, and exact selected-artifact provenance. Supplied
measurements retain `version_source: gemfile_lock` and exactly 0.0 ages.

Empty scope has null coverage, total 0.0 and null mean/median/max. Nonempty
supplied scope has coverage 1.0 and all age aggregates 0.0. Nonempty missing-date
scope has coverage 0.0, total 0.0, null mean/median/max and exactly two
`release_date_missing` rows. No source errors. Repository and Ruby summaries
agree. Human reports agree on identities, versions, full memberships, safe
requirements, 0/0 versus 2/2 versus 0/2 counts, percentages, source acceptance
and supplied-file/observable-publication limitations. **Outcome: PASS**;
one successful real-root target, including nonempty population comparisons.
Before/after manifests and Git metadata match exactly.

### Target C — dpc-admin (prior-validation baseline)

- Revision, tracked status, input status and Git prefix: **unavailable**; each
  permitted Git metadata command failed. No parent/sibling repository was
  searched to recover provenance. No revision association or clean-tree claim
  is inferred from the prior baseline or human authorization.
- Gemfile: regular, mode 0644, 2,848 bytes, SHA-256
  `8ec0c8d786c965f6deb228a0dc43038458c4b798b51f242ff54736bd1d61d167`.
- Gemfile.lock: regular, mode 0644, 12,463 bytes, SHA-256
  `e8852e0719202c9e5b210d7da434cae0a094865c82ebf404f15fe27da39146a1`.
- Independently expected complete-file rejection at physical **line 2**:
  `git_source` method/block is outside S1; interpolation also lies outside the
  literal subset. Later Ruby directive and `platforms:` options independently
  exceed the subset but cannot supersede the first defect. No raw line or URL
  is needed in diagnostics. Familiar declarations/groups later in the file
  cannot establish a complete scope. No expected membership map is manufactured.
- Request: `default` rejection probe only. Both formats/scenarios observe exactly
  `Gemfile / unsupported_gemfile_syntax`; no rows or lookup, format null,
  requested `[default]`. **N=null, M=null, N-M unavailable**, zero unmeasurable
  rows. Human/JSON agreement and repository/Ruby accounting match A's unavailable
  state; rejection remains visible.
- The independently inspected lock has supported section framing
  GEM/PLATFORMS/DEPENDENCIES/RUBY VERSION/BUNDLED WITH and a public remote;
  product lock recognition, direct association and selected-version authority
  remain **not reached**, not accepted. No hypothetical lock population counts
  compensate for rejected Gemfile scope.
- Input/type/mode/hash/link manifests match exactly before/after. Git metadata
  remains unavailable both times; integrity claim covers permitted input bytes
  and names, not the entire application checkout. **Outcome: EXPECTED REJECTION**.
  Conservative refusal is required by S1, not an implementation defect.

### Verification, limitations and task disposition

All 12 JSON cases asserted requested canonicalization, population identities,
full memberships, safe requirements, accepted/null format, selected artifacts,
lookup/exclusion sets, N/M/unmeasurable, stable reasons and summaries. All paired
human captures were reconciled against JSON, including limitations. All 24 CLI
reports exited 0; no network/subprocess guard fired. Before/after manifests
match for A, B and C. Only these three roots and permitted inputs/metadata were
accessed; no credentials, private configuration or unrelated application content
was inspected. No target modification occurred.

Two harness-only interruptions are retained: the initial capture printer assumed
A's absent Gemfile had a copy and stopped; it was corrected to preserve absence
and continue B/C. The initial report assertion incorrectly required repository
and Ruby totals to match in unavailable states. Existing scoped aggregation tests
explicitly preserve repository total 0.0 while Ruby total is null; the harness
assertion was corrected. Neither changed the frozen population expectations or
product code. No plausible implementation discrepancy remained.

**T012 is complete:** B supplies the required successful independent real-root
population comparison, A's insufficiency is explained by missing permitted inputs,
and C's rejection follows the approved whole-file contract. No failure is hidden
or offset by B's success. This run does not establish broad application coverage,
actual publication history, deployment/runtime state, historical pair coherence,
or whole-checkout integrity. No implementation fixes were made.
**T013 remains NOT STARTED and requires a separate execution instruction.**

Repository-local evidence checks: 005-0001–005-0017 exactly once with 44 fields;
all earlier ledger bytes preserved; 005-0017 matches its machine handoff plus
explicit human status additions, including blank credits_before and preserved
runtime-confounded note. Current 005-0018 is not appended. Only this file,
the narrow T012 task/status record and the prior observation row change.
`git diff --check` passes. No unrelated full suite was rerun; prior approved
390-test deterministic evidence remains distinct from this validation.
