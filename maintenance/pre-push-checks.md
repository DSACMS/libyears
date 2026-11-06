# Local checks before authorized publication

Run relevant locally reproducible hosted checks on the committed candidate before
pushing. Record exact commit, tool versions, results and gaps. This checklist does
not authorize a push or security exception, and local success never establishes
actual hosted CI success.

From the repository root:

```sh
python3 -m unittest tests.test_nuget_worker.RealWorkerTests
python3 -m unittest discover -s tests
git diff --check
python3 tools/check_gitleaks.py
```

The first three correspond to the Python CI job on the local OS/interpreter.
For filesystem-related test changes also discover and run the full suite with
`os.supports_dir_fd` patched to an empty set BEFORE test discovery. This preserves
real-reader skips and exercises portable semantic and refusal witnesses. Do not
report this as Windows execution. The actual OS/Python matrix and worker lifecycle
steps remain required hosted evidence. The separate live PyPI check can be run
with the workflow's exact temporary single-pin procedure when network access is
authorized; distinguish registry/environment failures from offline correctness.

`tools/check_gitleaks.py` is the canonical local history gate. It requires the
observed hosted GitLeaks **8.30.1**, rejects shallow history, uses the actual
`.github/.gitleaks.toml`, runs hosted `detect` mode with fully redacted logs and a
temporary SARIF report, and propagates scanner failure nonzero. It installs
nothing and adds no suppression. Commit intended changes first: history detection
does not scan uncommitted new content. A checkout scan may supplement it.

GitLeaks 8.30.1's default history source runs `git log -p -U0 --full-history --all
--diff-filter=tuxdb`. Available refs affect scope; compare local and hosted refs
and scan counts when investigating differences. Full local history can include
more refs than a hosted checkout; do not restrict it to a convenient passing range.
Check required refs are present, without assuming a non-shallow clone contains
all future hosted refs. Hosted pull-request merge commits can add evidence not yet
present locally. The action currently defaults to `latest`; before claiming
version parity, inspect its resolved version and reconcile the local gate's
expected version if it changes. Do not silently use an older scanner or downgrade
the hosted version to obtain a pass.

Offline gate tests verify history invocation, actual config, nonzero propagation,
version mismatch, missing tooling and shallow refusal. To check the real scanner
or a proposed exception, use an isolated temporary clone and synthetic content:

1. Run the gate-equivalent scan before any experimental exception.
2. In the clone only, append the known historical synthetic fixture expression to
   each affected file and another path; create a new local synthetic commit.
3. Include a constructed fake token matching a separate configured rule.
4. Rescan before/after the proposed exact-fingerprint file supplied explicitly
   from outside the repository. Require only the two old fingerprints to disappear;
   all new same-file, other-path and other-rule controls must still fail nonzero.

Never push the control clone or add real credentials. These experiments do not
approve repository policy changes. Run 006-0018 retained this experiment and its
redacted reports outside Git; [results and proposed policy gate](operational-smoke-006-0018.md).

Primary references: GitLeaks [history command implementation](https://github.com/gitleaks/gitleaks/blob/v8.30.1/sources/git.go),
[detect compatibility command](https://github.com/gitleaks/gitleaks/blob/v8.30.1/cmd/detect.go)
and [action version input](https://github.com/gacts/gitleaks/blob/v1/action.yml).
