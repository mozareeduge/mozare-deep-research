from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass

from .models import ClaimRecord, ClaimStatus, Directness, EvidenceCard, EvidenceRole, QueryRecord, ResearchQuestion, ReviewStatus


@dataclass
class QuestionCoverage:
    question_id: str
    critical: bool
    claim_statuses: dict[str, int]
    accepted_evidence: int
    direct_evidence: int
    independent_groups: int
    counter_search_done: bool
    requirement_met: bool
    blockers: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def compute_question_coverage(
    questions: list[ResearchQuestion],
    claims: list[ClaimRecord],
    cards: list[EvidenceCard],
    queries: list[QueryRecord],
) -> list[QuestionCoverage]:
    card_by_id = {card.evidence_id: card for card in cards}
    claims_by_q: dict[str, list[ClaimRecord]] = defaultdict(list)
    for claim in claims:
        for qid in claim.question_ids:
            claims_by_q[qid].append(claim)
    counter_qids = {q.question_id for q in queries if q.query_type.lower() in {"counter", "counterevidence", "challenge"}}
    result: list[QuestionCoverage] = []
    for question in questions:
        qclaims = claims_by_q.get(question.question_id, [])
        statuses: dict[str, int] = defaultdict(int)
        evidence_ids: set[str] = set()
        for claim in qclaims:
            statuses[claim.status.value] += 1
            evidence_ids.update(claim.supporting_evidence_ids)
            evidence_ids.update(claim.refuting_evidence_ids)
            evidence_ids.update(claim.qualifying_evidence_ids)
        accepted = [card_by_id[eid] for eid in evidence_ids if eid in card_by_id and card_by_id[eid].review_status == ReviewStatus.ACCEPTED]
        direct = [c for c in accepted if c.directness == Directness.DIRECT]
        groups = {c.independence_group for c in accepted if c.independence_group}
        counter_done = question.question_id in counter_qids
        blockers: list[str] = []
        req = question.evidence_requirement
        if len(direct) < req.min_direct_evidence:
            blockers.append(f"needs {req.min_direct_evidence - len(direct)} more direct evidence card(s)")
        if len(groups) < req.min_independent_groups:
            blockers.append(f"needs {req.min_independent_groups - len(groups)} more independent source group(s)")
        if req.counter_search_required and not counter_done:
            blockers.append("counter-search not recorded")
        if question.critical and not any(c.status in {ClaimStatus.SUPPORTED, ClaimStatus.CONTESTED, ClaimStatus.INSUFFICIENT} for c in qclaims):
            blockers.append("no scoped central claim decision")
        result.append(QuestionCoverage(
            question_id=question.question_id,
            critical=question.critical,
            claim_statuses=dict(statuses),
            accepted_evidence=len(accepted),
            direct_evidence=len(direct),
            independent_groups=len(groups),
            counter_search_done=counter_done,
            requirement_met=not blockers,
            blockers=blockers,
        ))
    return result


def marginal_unique_source_gain(queries: list[QueryRecord], question_id: str, recent_batches: int = 2) -> list[int]:
    batches: dict[int, set[str]] = defaultdict(set)
    for query in queries:
        if query.question_id == question_id:
            batches[query.batch_number].update(query.selected_ids)
    seen: set[str] = set()
    gains: list[int] = []
    for batch in sorted(batches):
        new = batches[batch] - seen
        gains.append(len(new))
        seen.update(batches[batch])
    return gains[-recent_batches:]
