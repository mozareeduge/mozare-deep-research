import pytest
from pydantic import ValidationError

from mros.models import (
    AccessStatus,
    AllowedUse,
    CandidateLink,
    ClaimRecord,
    ClaimStatus,
    DecisionStatus,
    DesignDecision,
    Directness,
    EvidenceCard,
    EvidenceLocation,
    EvidenceRole,
    LinkStatus,
    ReviewStatus,
    SourceKind,
    SourceRecord,
)


def test_metadata_only_source_cannot_support_formal_claim():
    with pytest.raises(ValidationError):
        SourceRecord(
            source_id="src.01",
            title="Metadata",
            kind=SourceKind.ARTICLE,
            access_status=AccessStatus.METADATA_ONLY,
            allowed_uses=[AllowedUse.FORMAL_CLAIM],
        )


def test_generated_source_cannot_support_formal_claim():
    with pytest.raises(ValidationError):
        SourceRecord(
            source_id="src.01",
            title="Generated",
            kind=SourceKind.GENERATED,
            access_status=AccessStatus.GENERATED,
            allowed_uses=[AllowedUse.FORMAL_CLAIM],
        )


def test_source_identifier_keys_are_normalized():
    source = SourceRecord(
        source_id="src.01",
        title="Source",
        kind=SourceKind.BOOK,
        identifiers={" DOI ": " 10.1/X "},
    )
    assert source.identifiers == {"doi": "10.1/X"}


def test_accepted_evidence_requires_reviewer():
    with pytest.raises(ValidationError):
        EvidenceCard(
            evidence_id="ev.01",
            span_ids=["span.01"],
            proposition="A proposition",
            role=EvidenceRole.SUPPORT,
            directness=Directness.DIRECT,
            review_status=ReviewStatus.ACCEPTED,
        )


def test_generated_candidate_cannot_be_formal_evidence():
    with pytest.raises(ValidationError):
        EvidenceCard(
            evidence_id="ev.01",
            span_ids=["span.01"],
            proposition="A proposition",
            role=EvidenceRole.SUPPORT,
            directness=Directness.GENERATED_CANDIDATE,
            allowed_uses=[AllowedUse.FORMAL_CLAIM],
        )


def test_supported_claim_requires_supporting_evidence():
    with pytest.raises(ValidationError):
        ClaimRecord(claim_id="cl.01", wording="Claim", status=ClaimStatus.SUPPORTED)


def test_contested_claim_requires_both_sides():
    with pytest.raises(ValidationError):
        ClaimRecord(
            claim_id="cl.01",
            wording="Claim",
            status=ClaimStatus.CONTESTED,
            supporting_evidence_ids=["ev.01"],
        )


def test_formal_export_requires_supported_or_contested_claim():
    with pytest.raises(ValidationError):
        ClaimRecord(
            claim_id="cl.01",
            wording="Claim",
            export_status=AllowedUse.FORMAL_CLAIM,
        )


def test_promoted_candidate_link_requires_support():
    with pytest.raises(ValidationError):
        CandidateLink(
            link_id="ln.01",
            participant_ids=["a1", "b1"],
            origin="human",
            description="Possible link",
            status=LinkStatus.PROMOTED,
        )


def test_accepted_design_decision_requires_grounding_and_option():
    with pytest.raises(ValidationError):
        DesignDecision(
            decision_id="dd.01",
            concept="c",
            operation="o",
            user_need="u",
            design_consequence="d",
            technical_consequence="t",
            test_or_evaluation="test",
            reversibility="reversible",
            status=DecisionStatus.ACCEPTED,
        )


def test_evidence_ranges_must_be_ordered():
    with pytest.raises(ValidationError):
        EvidenceLocation(page=3, page_end=2)
