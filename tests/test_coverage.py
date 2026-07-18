from mros.coverage import compute_question_coverage, marginal_unique_source_gain
from mros.models import (
    ClaimRecord,
    ClaimStatus,
    Directness,
    EvidenceCard,
    EvidenceRequirement,
    EvidenceRole,
    QueryRecord,
    QuestionType,
    ResearchQuestion,
    ReviewStatus,
)


def question():
    return ResearchQuestion(
        question_id="q.01",
        text="What follows?",
        question_type=QuestionType.CONCEPTUAL,
        critical=True,
        evidence_requirement=EvidenceRequirement(
            min_direct_evidence=1,
            min_independent_groups=1,
            counter_search_required=True,
        ),
    )


def test_coverage_passes_with_claim_evidence_and_counter_search():
    card = EvidenceCard(
        evidence_id="ev.01",
        question_ids=["q.01"],
        span_ids=["sp.01"],
        proposition="P",
        role=EvidenceRole.SUPPORT,
        directness=Directness.DIRECT,
        review_status=ReviewStatus.ACCEPTED,
        reviewer="reviewer",
        independence_group="group-a",
    )
    claim = ClaimRecord(
        claim_id="cl.01",
        wording="C",
        question_ids=["q.01"],
        status=ClaimStatus.SUPPORTED,
        supporting_evidence_ids=["ev.01"],
    )
    query = QueryRecord(
        query_id="query.01",
        question_id="q.01",
        provider="test",
        exact_query="counter",
        query_type="counter",
    )
    result = compute_question_coverage([question()], [claim], [card], [query])[0]
    assert result.requirement_met


def test_coverage_reports_missing_requirements():
    result = compute_question_coverage([question()], [], [], [])[0]
    assert not result.requirement_met
    assert "counter-search not recorded" in result.blockers
    assert "no scoped central claim decision" in result.blockers


def test_marginal_unique_source_gain_tracks_novelty():
    queries = [
        QueryRecord(query_id="query.01", question_id="q.01", provider="x", exact_query="a", batch_number=1, selected_ids=["s1", "s2"]),
        QueryRecord(query_id="query.02", question_id="q.01", provider="x", exact_query="b", batch_number=2, selected_ids=["s2", "s3"]),
        QueryRecord(query_id="query.03", question_id="q.01", provider="x", exact_query="c", batch_number=3, selected_ids=["s3"]),
    ]
    assert marginal_unique_source_gain(queries, "q.01") == [1, 0]
