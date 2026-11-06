# NuGet repository-root recognition correction

Run `006-0020`, starting clean at `13c6a66`. This is a bounded product
correction after Feature 006 operational closure, using the existing maintenance
artifact convention. It is neither Feature 007 nor a reopening of Feature 006.
The commissioning human authorizes the normal SDD gates, fresh independent
reviews, determined bounded corrections, implementation, local commits and
read-only OASim validation. Publication remains unauthorized.

The human repeatedly invokes libyears at OASim's repository root and receives
`Ecosystems: none`, despite ten known nested C# project files. The historical
[operational smoke](../operational-smoke-006-0018.md) classified this correctly
under the original explicit-selection contract. Its documentation repair and
[operational closure](../operational-smoke-closure.md) remain historical facts.
Repeated observed confusion now supplies product selection for this correction.

Current architecture already separates `cli.main`, `scan_mixed_repository`,
`format_human` and `format_json`. The scan creates a NuGet source only for an
explicit NuGetRequest. Adding a source for candidate filenames would falsely
change dependency counts, availability and schema-v3 meaning. Instead the CLI
can collect optional recognition evidence only for ordinary human directory
invocations and pass it to the human formatter. JSON and scan results need no
change. Existing root PyPI/npm/Ruby sources continue independently.

Filename/type evidence is sufficient for **C# project candidates**, not NuGet
dependencies, supported SDK declarations or measurable snapshots. Do not open
project contents, solutions, references, locks or witnesses for recognition.
Even malformed, unreadable or unsupported project content can be a candidate.
No implicit selection is justified for either a single candidate or many.
List relative paths and explain the existing parent-directory/immediate-filename
selection workflow; eligibility and provenance remain separate later checks.

A small depth/entry/directory/candidate bounded traversal is proportional to this
journey; broad indexing, solution interpretation and cross-project aggregation
are unnecessary. Exclude hidden/generated/dependency directories, do not follow
links, and anchor descendant access to open directories. Missing platform safety
capabilities must produce recognition unavailable, never an absence claim.
Partial/inaccessible/excessive traversal must be labeled incomplete and must not
publish an exact total or a misleading partial list. Stable completed lists can
be sorted independently of filesystem enumeration order.

The bounded candidate surface and human wording are specified in [spec.md](spec.md).
Lifecycle mechanics remain in [SDD_WORKFLOW.md](../../SDD_WORKFLOW.md).
