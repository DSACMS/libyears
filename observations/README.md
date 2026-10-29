# Prospective agent observation ledger

**Prospective observation begins with Feature 005.** The canonical ledger is
[agent-runs.csv](agent-runs.csv). This is cross-cutting methodology infrastructure;
its creation does not begin Feature 005 discovery, specification, planning, or
implementation.

Features 001–004 informed this schema and the repository's routing strategy,
but are not retroactively encoded as observations. Their evidence remains in
their original repository artifacts and Git history. AGENT_ROUTING.md therefore
contains historical observations that legitimately do not have corresponding
ledger rows. This is intentional. Do not create reconstructed Feature 001–004
rows. Any future retrospective or reconstructed observations must use a separate,
explicitly provenance-labeled dataset rather than silently entering this ledger.
This setup run is pre-ledger infrastructure and must not receive a reconstructed
row either.

The ledger initially contains only its header. The first actual Feature 005 agent
run is reserved as `005-0001`, followed by `005-0002`, and so on. Use one row per
agent run, with append-oriented usage. A review of another run or artifact should
normally be another row.

## Collection principles

**Wide rows are cheap. Missing provenance is expensive.** Columns are intentionally
somewhat redundant where preserving raw observations may support later analysis.
However, a field may be blank when it was not observed. Never estimate, infer,
reconstruct, or fabricate metadata merely because a column exists. Unknown or
unobserved data should remain blank unless a controlled vocabulary explicitly
provides an `unknown` state for an observed classification.

The canonical ledger stores observations, not derived analytics. Derive elapsed
wall-clock duration, credit delta, cost per run, words per second, or findings per
credit separately if useful. Do not add canonical columns for those values or
quality, efficiency, or intelligence scores. Do not encode subjective scalar
quality judgments as observations. Credits, runtime, reasoning effort, prompt
size, and artifact size are not interchangeable measures of cost or quality.

Collecting metadata itself has a cost. Prefer automatic capture where reliable;
do not require humans to reconstruct obscure fields for completeness. Leave
fields blank when capture would create disproportionate burden or uncertain
data. Feature 005 should test whether this ledger is useful enough to justify
its collection cost. The methodology should eventually ask not only which
practices improve quality, but which practices can safely be removed.

## CSV format

This is a CSV dialect using `|` as the delimiter, deliberately stored with a
`.csv` extension, rather than a custom `.psv` format. Use UTF-8 text, one header
row, and repository-normalized LF newlines with a final newline. Configure
ordinary CSV/data tooling with delimiter `|` and quote character `"`.

Fields containing `|`, double quotes, or line breaks must be double-quoted.
Represent literal double quotes inside quoted fields with doubled quotes.
Prefer concise single-line field values where practical, especially `notes`.
For example, the illustrative field value `checks | "pass"` is serialized as
`"checks | ""pass"""`. This is a quoting example, not an observation row.
Quoted multiline fields remain part of one CSV record; use a CSV parser rather
than counting physical lines to count records.

Python's standard-library `csv.reader` and `csv.writer` support this dialect
with `delimiter="|"`, `quotechar='"'`, and `doublequote=True`; a writer can use
`quoting=csv.QUOTE_MINIMAL` and `lineterminator="\n"`. Open files with
`encoding="utf-8"` and `newline=""` for CSV handling.

## Data dictionary

Schema version: 1

These are exactly the 44 canonical columns, in header order. Keep names and
order unchanged in schema v1. Vocabulary values below are initial values;
blank always remains available for unobserved data.

| Column | Definition and recording rules |
|---|---|
| `run_id` | Stable repository-controlled primary observational identifier. Feature 005 uses `005-0001`, `005-0002`, and so on; the first actual run is reserved as `005-0001`. |
| `parent_run_id` | Optional direct workflow or evidence relationship to an earlier run. Chronological succession alone does not require it. |
| `session_id` | Directly observed agent/harness session identifier, when available. Provenance metadata, not the primary identity; leave blank when unavailable. Never reconstruct it from historical evidence or infer it from another run. |
| `experiment_id` | Groups deliberately comparative runs. Ordinary runs leave this blank. |
| `comparison_group` | The run's role within its experiment. Ordinary runs leave this blank. |
| `started_at` | Directly observed start time in unambiguous ISO-8601 form with timezone, for example `2026-10-29T14:00:00Z`. |
| `ended_at` | Directly observed end time in unambiguous ISO-8601 form with timezone. Do not use these timestamps to populate reported runtime. |
| `feature` | Feature/lifecycle context, for example `005`. |
| `stage` | Workflow stage, such as discovery, specification, planning, implementation, review, validation, retrospective, or methodology. |
| `task` | Concrete run/task identifier or concise task name. |
| `task_class` | Cognitive/work shape, aligned where practical with AGENT_ROUTING.md; see the extensible examples below. |
| `target` | What the run acts on or evaluates, for example Feature 005 discovery, `spec.md`, implementation convergence, or AGENT_ROUTING.md. |
| `commit` | Repository HEAD at the beginning of the run. |
| `dirty_tree` | Observed starting working-tree state: `no`, `yes`, or `unknown`. Do not hash or serialize the dirty diff into the ledger. |
| `model` | Reported model identity, when available. |
| `provider` | Reported model provider, when available. |
| `effort` | Reported reasoning-effort setting, when available. |
| `agent_version` | Directly observed agent/harness version. Harness behavior may change independently of model identity. |
| `context` | Small initial vocabulary: `fresh`, `continued`. |
| `context_note` | Context distinctions such as repository-grounded, repository plus bootstrap, blinded candidate review, or explicitly supplied temporary normative artifact. Do not claim context-window token counts unless directly observed. |
| `execution_mode` | Observed harness execution mode, such as daemon or no-daemon, when available. |
| `permissions` | Actual observed harness permissions, distinct from the authority inherent in the task. |
| `authority_scope` | Authority inherent in the task, such as `read_only`, `workspace_write`, `local_git`, `network_read`, `publication`, or `human_authenticated`. Use the clearest directly observed value and notes for material additional context. |
| `prompt_chars` | Exact character count when the exact prompt text is available; otherwise blank along with its hash. |
| `prompt_sha256` | SHA-256 of the exact prompt representation available to the recorder, without normalization. Experimental identity/provenance, not security. Leave blank if exact text is unavailable. |
| `network_required` | Whether successful completion of the assigned task requires external network access: `yes`, `no`, or `unknown`. |
| `environment_status` | Execution environment classification: `normal`, `degraded`, `blocked`, or `unknown`; not a product outcome. |
| `reported_runtime_s` | Raw agent/harness-reported runtime in seconds, when available. Never derive this from start/end timestamps or reinterpret reported elapsed time as active compute time. |
| `runtime_confounded` | Observed classification of reported runtime: `no`, `yes`, or `unknown`. |
| `runtime_note` | Material confounding such as workstation sleep/lock, interruption, backgrounding, or uncertainty about what the reported timer measures. |
| `credits_before` | Raw observed credits before the run, when available. Blank is preferable to reconstruction. |
| `credits_after` | Raw observed credits after the run, when available. Derive credit delta separately. |
| `completion_status` | Whether the assigned run completed its required work: `complete`, `incomplete`, or `blocked`. |
| `completion_reason` | Short factual explanation of completion status when useful. |
| `finding_status` | Whether material findings were established: `none`, `findings`, or `not_assessed`. |
| `finding_count` | Observed count of material findings when the run reports a meaningful count. Do not force a count when the review does not define one. |
| `outcome` | Reported gate/result, initially including `approve`, `revise`, `converged`, `not_converged`, `pass`, `fail`, `blocked`, or `n/a`. |
| `artifact_type` | Type of principal durable artifact produced or evaluated, when applicable. Not every run needs an artifact. |
| `artifact_path` | Repository-relative path of that principal artifact, when applicable. |
| `artifact_words` | Observed word count of that principal artifact, when available. |
| `artifact_sha256` | SHA-256 of that principal artifact when available; provenance or experimental identity, not a security claim. |
| `human_intervention` | Whether material human intervention occurred: `no` or `yes`. Ordinary prompt submission is not intervention. |
| `human_intervention_type` | Small extensible initial vocabulary: `clarification`, `authority`, `correction`, `redirect`, `environment`, or `experiment`. Use notes for concise context. |
| `notes` | Concise free text for material context that does not deserve a new schema field; never a transcript. Follow the CSV quoting rules for literal pipes, quotes, or line breaks. |

### Task and harness context

Initial `task_class` examples are `bounded_implementation`,
`deterministic_transformation`, `narrow_verification`, `broad_verification`,
`synthesis`, `security_privacy_review`, `authenticated_external_action`,
`discovery`, and `planning`. Extend this vocabulary when future work shapes
require it; do not make it artificially closed.

Harness permissions describe what the environment permits; task authority
describes what the assignment authorizes. Do not overengineer serialization of
multiple authority concepts in schema v1. Use the clearest observed value and
concise notes where material.

Do not store full prompts in the ledger. Count and hash only the exact prompt
representation available to the recorder. Do not normalize text before hashing
or reconstruct unavailable prompts merely to fill these fields.

### Completion, findings, and outcome

Keep completion, findings, and gate/result separate. An incomplete review that
establishes no defect is not equivalent to a completed review that passes.
A partial review can establish material findings while remaining incomplete.
An environment-blocked run is not evidence that the product failed.

Environment examples include unavailable DNS, authentication, or tooling.
Describe them generically without sensitive operational details. Record timer
uncertainty and interruptions as runtime context rather than inventing active
compute measurements.

### Artifacts and intervention

For multiple artifacts, record the principal target/output and use `notes` for
concise additional context rather than inventing nested serialization. If
repeated multi-artifact runs make this inadequate, revise the schema
prospectively later.

Record human intervention when a human materially changes, supplies authority
to, or unblocks the run. Ordinary prompt submission alone does not count.

## Experiments

Following AGENT_ROUTING.md, keep tasks and prompts constant where practical,
record material differences, and use prompt hashes when exact equality matters.
Blind reviewers where useful. Preserve raw observations and distinguish outcomes
from causal explanations. Small or n=1 comparisons are hypothesis-generating.
Use `experiment_id` and `comparison_group` only for deliberately comparative runs.

## Publication hygiene

Do not record personal absolute paths, local checkout topology, organizational
trust identifiers, sensitive environment-specific details, temporary remediation
paths, credentials, or session secrets. A Codex `session_id` is observational
provenance, not a credential; do not attach unrelated account/user identifiers.
Keep environment and intervention notes concise and suitable for publication.

## Schema evolution

Prefer additive prospective evolution. Do not rewrite historical rows to make
old observations look as though they were collected under a later schema.
If fields or vocabularies change, document when the change becomes effective.
Human readability and historical truth take priority over normalization.
