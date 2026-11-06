# NuGet root recognition technical plan

Governing [specification](spec.md) SHA256
`662700c4975449117e9a04ac7fc7144e48c983dbbc3587220b77eb51454cc753`;
approval and subsequent plan disposition live in [reviews.md](reviews.md).

Add one focused `libyears/nuget_discovery.py`, independent of project parsers,
sources and adapters. A frozen NuGetRecognition holds `candidates: tuple[str,...]`
and `status` (`complete`, `incomplete`, `unavailable`). Incomplete/unavailable
records always have an empty tuple. No SourceResult/model/schema changes.

Discovery uses a descriptor-anchored depth-first traversal. Require O_DIRECTORY,
O_NOFOLLOW, O_NONBLOCK, descriptor-relative os.open/os.stat, and descriptor-based
os.scandir; otherwise return unavailable before opening anything. The user-selected
root opens as a non-following directory; symlink roots are incomplete. Descendants
open relative to their parent descriptor with the same flags. A metadata/type
inspection with follow_symlinks=False excludes symlinks, reparse points and special
files. Skip excluded directory names before descending. Compare inspected and
opened device/inode identity, and verify parent-relative identity after recursion.
Compare directory identity/mtime/ctime before and after enumeration/recursion to
detect ordinary mutation. Never open candidate project files or follow entry paths.
No installed-worker or registry path is involved.

Bound total entries while consuming scandir (cap+1 detects overflow), before
sorting. Sort only bounded directory entries. Count each visited directory and
candidate globally; inclusive constants are 256/10,000/100, depth four. Encountering
a nonexcluded deeper directory makes the entire result incomplete. A small private
exception unwinds limit/error paths to one result; try/finally closes every directory
and context-managed scandir closes iterators. At most five directory levels stay
open. OSError, ValueError and NotImplementedError become incomplete, with no raw
exception retained. Capability absence is unavailable. Fixed inputs produce sorted
POSIX-style relative paths; overflow/error results have no traversal-order-dependent
partial list. This is a bounded observation, not an atomic snapshot or latency SLA.

In cli.main, after a successful scan, only human/unselected directory invocations
call discovery. JSON bypasses it entirely; direct-file and explicit selection bypass
it. A root metadata error in this optional step produces incomplete recognition
rather than discarding successful sibling measurement. Pass optional recognition
to format_human only when there are candidates or status is incomplete/unavailable;
default calls keep established signatures/results when there is nothing to disclose.
Existing injected scan functions and existing format_json are unchanged.

The human formatter accepts optional recognition and passes it to the mixed
formatter. When present, label source ecosystems `Ecosystems scanned for measurement`
(singular branch likewise). Insert a separate recognition block before measurement
facts; never append `nuget` to the measurement ecosystem list. It names the bounded
candidate count or incomplete/unavailable status, JSON-quotes relative paths using
ensure_ascii=True, states no NuGet measurement, and explains the generic existing
command `python3 -m libyears PATH --nuget-project NAME.csproj`, where PATH is the
chosen candidate's parent. Do not generate executable commands from filenames.
Say eligibility/lock/explicit provenance requirements still apply. No diagnostics,
raw exception paths or new JSON facts are introduced. Legacy ScanReport injected
tests can receive the same human block without changing their metric facts.

Tests are split deliberately: semantic CLI/output tests inject NuGetRecognition
and real/injected ordinary source results; actual traversal tests exercise the
production filesystem only on capable hosts. Unskipped refusal tests disable each
required primitive and assert no opening. Race/error/limit tests use existing
standard-library mock seams plus synthetic directories; semantic composition never
requires successful descriptor traversal. All no-network/process guards are checked
after calls to catch swallowed guard exceptions. Cover cap/cap+1 at real production
values, exact depth/exclusions, link/FIFO/reparse refusal, all handles closed,
no content reads, control-character escaping, sibling metrics and JSON equality.

Update README basic usage, SPEC current behavior, AGENTS recognition clarification,
CHANGELOG Unreleased Fixed and ROADMAP's existing listing opportunity. Preserve
all Feature006 artifact bytes and historical operational records. Record R1–R6
evidence and a concise correction retrospective in this maintenance directory.

For OASim, from the trusted scanner checkout run exactly the authorized root
command; capture stdout/stderr/exit outside target/Git. No explicit selection or
public lookup is necessary. Before and after, hash all 223 currently tracked
files for integrity only, retain revision and complete porcelain status including
untracked names, and compare; never interpret unrelated target contents. These
checks prove tracked bytes/modes and status unchanged, not untracked-byte or
OS-wide side-effect invariance. No target code or package manager runs.

Run focused tests, full deterministic suite, dedicated real-worker witnesses,
full capability-disabled simulation and canonical GitLeaks history gate on the
committed candidate; diff checks before each commit. Freeze changed bytes and
operational evidence for fresh independent implementation/convergence review.
Bounded findings follow canonical correction/freeze/fresh-review mechanics.
Actual Windows and hosted checks remain post-publication witnesses, not local
acceptance predecessors; no push is authorized.
