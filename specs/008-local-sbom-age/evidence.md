# Specification evidence — 007-0048

This is bounded verification for [spec.md](spec.md), not a technical implementation
plan, reader prototype or live measurement. The [reviewed discovery](../../discovery/sbom-corpus-feasibility.md)
owns corpus provenance/digests and historical target absences. Its inventory-only
shipping recommendation is superseded by the human's007-0048 selection of a separate
measurable SBOM population; current-checkout Observed semantics are unchanged.

## Corpus and format mechanics

Original007-0047 handoff, artifact words/digest and every final-freeze entry verified
against starting `aeeab3d1591fe71ae4639be70d0d8daea570febb`. Raw public examples remain
privately durable through the helper's `D/007-0047/`; this run preserves bindings,
verification outputs and frozen author/review bytes in `D/007-0048/`. No lost prior
helper bytes or telemetry were reconstructed.

Independent bounded JSON inspection of the retained Dependency-Track4.13.4 release
artifact confirms201 component entries, an exactly repeated metadata subject,
200 distinct external Maven component identities,21 service objects,424 graph edges
and200 subject-reachable external components. There are43 subject edges and157
other reachable components. The JSON nesting depth is7 and largest string948UTF-8
bytes, below selected limits. This establishes format fitness and prospective
inventory/relationship counts, not supported measurement yield. The source-POM
57 direct declarations/14 tests remain an independent population comparison.
No catalogue, age lookup, target execution or local artifact generation occurred.

Authoritative [CycloneDX1.5 schema](https://github.com/CycloneDX/specification/blob/master/schema/bom-1.5.schema.json)
and [Maven purl definition](https://github.com/package-url/purl-spec/blob/main/docs/types/definitions/maven-definition.md)
were retrieved as exact bounded public documentation: curl startup config disabled,
verified HTTPS, no redirects,1MiB/response,10-second connect/30-second request.
Retrieved2026-11-20; exact SHA256 and URLs are in the durable reference manifest.
The earlier proposed Maven-definition path returned404 through the browser; the
retained legacy PURL-SPECIFICATION file is a relocation notice, not substantive
grammar evidence. No target SBOM was newly acquired. The selected literal subset
does not require universal purl decoding or a generic schema engine.

The schema defines bom-ref identity, separate component containment and dependency
edges, and permits incomplete graphs; missing vertices do not establish no children.
Maven purls preserve case-sensitive group/artifact/version with jar as default type,
classifier as a variant and repository_url as an alternate repository pointer.
These mechanics justify narrow parsing and pre-lookup restriction handling; they
establish neither source acquisition nor trustworthy current-checkout selection.
Schema1.5 is justified by the actual non-GitHub Maven-plugin release corpus, rather
than by GitHub's separate SPDX export behavior. Full CPython SPDX and its partial
checked-in fragment supply genuine unsupported-format/framing witnesses.

## Actual output and policy compatibility

Inspected at starting HEAD:

- [output.py](../../libyears/output.py) report_to_dict builds schema3 legacy direct
  fields and separately appends Maven data; format_json serializes the dictionary.
- [maven_output.py](../../libyears/maven_output.py) projects sources/occurrences/views
  and renders aligned measured/refused tables; no independent inventory field exists.
- [maven_model.py](../../libyears/maven_model.py) constrains facts to Declared/Observed
  bases and occurrence keys; SBOM inventory cannot truthfully reuse those semantics.
- [CLI](../../libyears/cli.py) has no SBOM or offline switch. Safe exact option
  handling/argument errors already exist for scoped features. The proposed SBOM
  source adds no new global offline promise.
- [Maven policy](../../libyears/maven_policy.py), [version](../../libyears/maven_version.py),
  [registry](../../libyears/maven_registry.py) and [protocol](../../libyears/maven_protocol.py)
  establish source refusal, exact/snapshot/ordering behavior, fixed GAV POM identity
  and bounded metadata. Reuse semantic/time boundaries, not a fabricated source
  model requiring a local POM for an independent inventory claim.
- [Maven output witnesses](../../tests/test_maven_output.py) enforce schema3,
  null legacy Maven projection, sibling preservation and separated views. The
  [existing specification](../007-maven-dependency-age/spec.md#s8--additive-machine-output-schema3)
  explicitly qualifies closed-world consumer compatibility for additive keys.

Therefore an optional top-level `sbom` with its own population/scope can retain all
existing values without changing schema3 or adding SBOM to legacy arrays/ecosystems.
This is a compatibility argument supported by inspected contracts and code, **not
an implemented or tested extension**. Projection-equality and ordinary-output
witnesses remain required by AC12. Refusing to merge populations avoids inventing
a schema migration as a prerequisite; it does not claim every external consumer
accepts additional keys. Exact implementation-file digests and technical count
output are retained durably for reviewers.

The focused correction defines the extension completely in
[output-contract.md](output-contract.md), including safe selected-file attribution
when document acceptance fails, alias/reference graph projection, nullable assertion
statuses and reason counts. Its three committed examples are deliberately synthetic
section fixtures, with placeholder digest and controlled dates. A one-year arithmetic
witness and shape/count invariants can be checked offline without implementing an
SBOM parser or asserting a real package date.

## Adoption and next gate

No supported CMSgov/DSACMS artifact exists in this retained corpus. Prior known
public candidate metadata includes a hosted BFD lead; obtaining it is unnecessary
to settle this format/population contract and no acquisition was attempted.
No repository reinventory or private access occurred.

Human selection already authorizes useful SBOM ages independent of Observed joins.
Independent review must establish whether the specification is coherent and safe;
it cannot authorize a technical plan or implementation in this run. That is the
remaining stage boundary after convergence.
