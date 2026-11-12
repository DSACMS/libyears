# Apache Maven 3.9.11 ordering evidence

The exact upstream tag is `maven-3.9.11` in Apache's Maven repository.
[provenance.json](provenance.json) records every retrieved URL and SHA-256.
Only those six public source/license evidence files were retrieved; no Maven
Central metadata, dependencies, target files or executables were accessed.
Artifact.java is necessary because ArtifactUtils delegates its snapshot suffix
and timestamp regular expression to constants there. No other adjacent source
was needed. Raw Java files remain temporary analysis inputs outside Git.

## Derivation and licensing

Apache Maven is licensed under Apache License 2.0. The exact upstream
[LICENSE](LICENSE) and [NOTICE](NOTICE) are retained without alteration, including
ASF attribution. ComparableVersion source credits Kenney Westerhof and Hervé
Boutemy; its test source credits Hervé Boutemy. These pertinent upstream author
attributions are retained here and in the adapted module/vector notices. The root
repository license does not replace these obligations.

libyears/maven_version.py is a bounded Python adaptation of ComparableVersion's
item/list algorithm, with snapshot recognition derived from ArtifactUtils and
Artifact. Its module notice identifies the derivation and modifications. Python
integers replace the numeric implementations, retaining their precedence ranks
(including all-zero segment width); immutable records replace mutable Java lists.
ASCII/path safety and resource refusal are libyears restrictions. Equality means
comparison equality; no Java hash, mutable reuse, canonical text API, CLI or Java
runtime is reproduced. Eligibility is separately libyears-owned product policy.

The small offline fixture tests/fixtures/maven/comparable-version-3.9.11.json
retains the two ordered arrays and literal equality/less-than argument pairs
from ComparableVersionTest. It omits Java code/comments/harness. The test module
adds explicit MNG-5568/6572/6964/7644, leading-zero, qualifier-context, underscore,
budget and policy boundaries. Expected values come from the pinned tests/source,
not the Python implementation. These adapted vectors and the derived Python
algorithm retain Apache attribution under this LICENSE/NOTICE; they are not
claimed as wholly original upstream-independent expression. No full upstream
Java file is vendored or executed. Future tests are entirely offline.

## Contract limits

Ordering is pinned ComparableVersion precedence, not Resolver range semantics.
Only safe ASCII exact strings up to256 characters are supported, with128 digits
per numeric segment and128 scalar/child-list items before normalization; root
list depth is separately capped at128. Catalogue count is capped at10000 entries
before identical duplicates collapse. Refused inputs never disappear from a
catalogue to manufacture a maximum. Snapshot suffix matching and timestamp
recognition follow ArtifactUtils; qualifier tokens follow ComparableVersion,
where underscore and plus are ordinary string content rather than separators.
The conservative whitelist and unknown/tie refusal are defined by the approved
Feature007 latest policy, independently of this upstream ordering evidence.

## Pinned irregularity

Source inspection and an explicit regression retain the nested-list comparisons
`1-0.alpha < 1 < 1-sp2` and `1-0.alpha > 1-sp2`. Consequently this pin is not
claimed universally transitive. The alpha token excludes that candidate before
latest selection. Fixed-corpus antisymmetry/transitivity checks cover ordinary
eligible and unknown forms; catalogue permutation tests separately establish
policy determinism. No upstream repair or eligibility-policy change is made.

## T004 artifact-handler facts

[artifact-handlers.json](artifact-handlers.json) records the exact versioned
Apache Maven3.9.11 handler-reference URL, retrieval time, SHA256 of the temporary
HTML and the eleven type/extension/default-classifier mappings used by T004.
The page identifies version3.9.11 and directly supplies all required facts; no
adjacent source, linked assets, scripts or secondary page was retrieved/executed.
Its author is Hervé Boutemy and its footer credits The Apache Software Foundation
(2001–2025); those credits and the existing Apache LICENSE/NOTICE are retained.
The JSON explicitly identifies its transformation from the table. Only factual
mapping columns are retained; the complete HTML remains a temporary evidence input.

libyears/maven_project.py applies these facts after raw model-key construction.
It does not turn handler aliases into management-key equality or evaluated build
behavior. Explicit supported classifiers override handler defaults. Packaging,
classpath, dependency inclusion and language columns do not change project-direct
population; custom handlers, runtime execution and variant availability remain
unsupported. The approved T004 graph/raw-inheritance contract supplies the other
implementation rules; no additional source access was necessary.
