"""Internal offline slice. Ordinary scan/CLI/production transport are separate."""

from .sbom_document import accept_document
from .sbom_graph import attach_graph
from .sbom_identity import canonical_members
from .sbom_input import SbomInputReader, intake_sbom
from .sbom_measure import measure_members, summarize_members
from .sbom_model import SbomFailure, SbomReport, SbomRequest
from .sbom_policy import admit_members


def scan_sbom(root, request=SbomRequest(), *, supervisor_factory,
              reader_factory=SbomInputReader, known_vetoes=()):
    intake = intake_sbom(root, request, reader_factory=reader_factory)
    if intake is None:
        return None
    if intake.reason is not None:
        return SbomReport(intake, summary=summarize_members(None))
    try:
        document = accept_document(intake.snapshot)
    except SbomFailure as failure:
        from dataclasses import replace
        return SbomReport(replace(intake, reason=failure.reason), summary=summarize_members(None))
    members = canonical_members(document)
    graph, members = attach_graph(document, members)
    members = admit_members(document, members, known_vetoes)
    members = measure_members(members, supervisor_factory=supervisor_factory)
    return SbomReport(intake, document, members, graph, summarize_members(members))
