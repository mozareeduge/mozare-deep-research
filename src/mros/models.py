"""Typed records for the Mozare Research Operating System.

The models intentionally use plain operational names. Rich theoretical vocabulary stays in
human-facing methodology documentation and is compiled into these distinctions rather than
repeated in model prompts.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


ID_PATTERN = r"^[a-z][a-z0-9_.:-]{1,127}$"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class AccessStatus(StrEnum):
    OPEN_PUBLIC = "open_public"
    METADATA_ONLY = "metadata_only"
    INSTITUTIONAL = "institutional_access"
    PERMISSION_BASED = "permission_based"
    PHYSICAL = "physical_consultation"
    PUBLISHED_MEDIATION = "published_mediation"
    RECONSTRUCTED = "reconstructed"
    GENERATED = "generated"
    UNKNOWN = "unknown"


class SourceKind(StrEnum):
    ARTICLE = "article"
    BOOK = "book"
    CHAPTER = "chapter"
    ARCHIVE_RECORD = "archive_record"
    DATASET = "dataset"
    WEBPAGE = "webpage"
    REPOSITORY = "repository"
    SOFTWARE_DOCS = "software_documentation"
    USER_NOTE = "user_note"
    GENERATED = "generated"
    OTHER = "other"


class AllowedUse(StrEnum):
    DISCOVERY = "discovery"
    INTERNAL_SYNTHESIS = "internal_synthesis"
    FORMAL_CLAIM = "formal_claim"
    DESIGN = "design"
    CREATIVE = "creative"
    APPENDIX = "appendix"
    RESIDUE = "residue"
    QUARANTINE = "quarantine"


class QuestionType(StrEnum):
    FACTUAL = "factual"
    BIBLIOGRAPHIC = "bibliographic"
    CONCEPTUAL = "conceptual"
    GENEALOGICAL = "genealogical"
    MECHANISM = "mechanism"
    COMPARATIVE = "comparative"
    METHODOLOGICAL = "methodological"
    DESIGN = "design_implication"
    TECHNICAL = "technical_feasibility"
    EVALUATION = "evaluation"
    COUNTERARGUMENT = "counterargument"
    OPEN_UNKNOWN = "open_unknown"


class QuestionStatus(StrEnum):
    OPEN = "open"
    SEARCHING = "searching"
    EVIDENCE_READY = "evidence_ready"
    CONTESTED = "contested"
    UNRESOLVED = "unresolved"
    CLOSED = "closed"


class EvidenceRole(StrEnum):
    SUPPORT = "support"
    REFUTE = "refute"
    QUALIFY = "qualify"
    DEFINE = "define"
    CONTEXTUALIZE = "contextualize"
    METHOD = "method"
    EXAMPLE = "example"


class Directness(StrEnum):
    DIRECT = "direct"
    INDIRECT = "indirect"
    SECONDARY_REFERENCE = "secondary_reference"
    GENERATED_CANDIDATE = "generated_candidate"


class ReviewStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"


class ClaimStatus(StrEnum):
    PROPOSED = "proposed"
    SUPPORTED = "supported"
    CONTESTED = "contested"
    INSUFFICIENT = "insufficient"
    WITHDRAWN = "withdrawn"


class ClaimCriticality(StrEnum):
    CENTRAL = "central"
    SUPPORTING = "supporting"
    CONTEXTUAL = "contextual"


class LinkStatus(StrEnum):
    CANDIDATE = "candidate"
    TESTED = "tested"
    PROMOTED = "promoted"
    REJECTED = "rejected"
    DEFERRED = "deferred"


class DecisionStatus(StrEnum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class ResearchBudget(StrictModel):
    model: str = "sonnet"
    effort: str = "medium"
    max_query_batches: int = Field(default=2, ge=1, le=50)
    max_tool_calls: int = Field(default=30, ge=1, le=500)
    max_candidates: int = Field(default=20, ge=1, le=500)
    max_full_sources: int = Field(default=5, ge=0, le=100)
    max_evidence_spans: int = Field(default=12, ge=1, le=200)
    max_subagents: int = Field(default=1, ge=0, le=10)
    max_output_words: int = Field(default=1500, ge=50, le=50000)
    stop_rule: str = "Stop when critical claims are supported, contested, or explicitly unresolved and marginal evidence gain is low."


class ResearchContract(StrictModel):
    project_id: str = Field(pattern=ID_PATTERN)
    title: str = Field(min_length=1, max_length=300)
    research_purpose: str = Field(min_length=1)
    target_decisions: list[str] = Field(default_factory=list)
    audiences: list[str] = Field(default_factory=list)
    genres: list[str] = Field(default_factory=list)
    scope: list[str] = Field(default_factory=list)
    exclusions: list[str] = Field(default_factory=list)
    uncertainty_policy: str = "Record unknown, not accessed, and not verified states explicitly."
    languages: list[str] = Field(default_factory=lambda: ["en"])
    source_policies: list[str] = Field(default_factory=list)
    output_obligations: list[str] = Field(default_factory=list)
    approval_gates: list[str] = Field(
        default_factory=lambda: [
            "scope",
            "central_claim_promotion",
            "destructive_library_change",
            "final_release",
        ]
    )
    budget: ResearchBudget = Field(default_factory=ResearchBudget)


class EvidenceRequirement(StrictModel):
    min_direct_evidence: int = Field(default=1, ge=0, le=20)
    min_independent_groups: int = Field(default=1, ge=0, le=20)
    counter_search_required: bool = True
    acceptable_source_kinds: list[SourceKind] = Field(default_factory=list)
    notes: str = ""


class ResearchQuestion(StrictModel):
    question_id: str = Field(pattern=ID_PATTERN)
    text: str = Field(min_length=1)
    question_type: QuestionType
    purpose_ids: list[str] = Field(default_factory=list)
    decision_ids: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    critical: bool = False
    status: QuestionStatus = QuestionStatus.OPEN
    evidence_requirement: EvidenceRequirement = Field(default_factory=EvidenceRequirement)
    preferred_source_types: list[SourceKind] = Field(default_factory=list)
    excluded_source_types: list[SourceKind] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    time_range: str | None = None
    stop_rule: str = ""
    notes: str = ""

    @model_validator(mode="after")
    def dependencies_do_not_self_reference(self) -> "ResearchQuestion":
        if self.question_id in self.dependencies:
            raise ValueError("question cannot depend on itself")
        return self


class SourceRecord(StrictModel):
    source_id: str = Field(pattern=ID_PATTERN)
    title: str = Field(min_length=1)
    creators: list[str] = Field(default_factory=list)
    date: str | None = None
    kind: SourceKind
    language: str | None = None
    identifiers: dict[str, str] = Field(default_factory=dict)
    canonical_location: str | None = None
    local_files: list[str] = Field(default_factory=list)
    acquired_at: datetime | None = None
    accessed_at: datetime | None = None
    version_status: str = "unknown"
    rights_status: str = "unknown"
    access_status: AccessStatus = AccessStatus.UNKNOWN
    provenance_status: str = "unknown"
    primary_secondary_status: str = "unknown"
    allowed_uses: list[AllowedUse] = Field(default_factory=lambda: [AllowedUse.DISCOVERY])
    independence_group: str | None = None
    generated_by: str | None = None
    notes: str = ""
    tags: list[str] = Field(default_factory=list)
    content_sha256: str | None = None

    @field_validator("identifiers")
    @classmethod
    def normalize_identifier_keys(cls, value: dict[str, str]) -> dict[str, str]:
        return {str(k).strip().lower(): str(v).strip() for k, v in value.items() if str(v).strip()}

    @model_validator(mode="after")
    def evidence_permissions_match_access(self) -> "SourceRecord":
        if self.access_status == AccessStatus.METADATA_ONLY and AllowedUse.FORMAL_CLAIM in self.allowed_uses:
            raise ValueError("metadata-only records cannot be allowed for formal content claims")
        if self.kind == SourceKind.GENERATED or self.access_status == AccessStatus.GENERATED:
            forbidden = {AllowedUse.FORMAL_CLAIM}
            if forbidden.intersection(self.allowed_uses):
                raise ValueError("generated material cannot be allowed as formal evidence")
        return self


class QueryRecord(StrictModel):
    query_id: str = Field(pattern=ID_PATTERN)
    question_id: str = Field(pattern=ID_PATTERN)
    provider: str
    exact_query: str
    query_type: str = "discovery"
    language: str | None = None
    filters: dict[str, Any] = Field(default_factory=dict)
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    result_count: int | None = Field(default=None, ge=0)
    candidate_ids: list[str] = Field(default_factory=list)
    selected_ids: list[str] = Field(default_factory=list)
    rejected_ids: list[str] = Field(default_factory=list)
    selection_reasons: dict[str, str] = Field(default_factory=dict)
    batch_number: int = Field(default=1, ge=1)
    cost_class: str = "deterministic"


class EvidenceLocation(StrictModel):
    page: int | None = Field(default=None, ge=1)
    page_end: int | None = Field(default=None, ge=1)
    section: str | None = None
    start_offset: int | None = Field(default=None, ge=0)
    end_offset: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def ranges_are_ordered(self) -> "EvidenceLocation":
        if self.page is not None and self.page_end is not None and self.page_end < self.page:
            raise ValueError("page_end must be >= page")
        if self.start_offset is not None and self.end_offset is not None and self.end_offset < self.start_offset:
            raise ValueError("end_offset must be >= start_offset")
        return self


class EvidenceSpan(StrictModel):
    span_id: str = Field(pattern=ID_PATTERN)
    source_id: str = Field(pattern=ID_PATTERN)
    file_path: str
    exact_text: str = Field(min_length=1)
    context_before: str = ""
    context_after: str = ""
    location: EvidenceLocation = Field(default_factory=EvidenceLocation)
    retrieval_query: str | None = None
    retrieval_score: float | None = None
    rerank_score: float | None = None
    parse_confidence: str = "unknown"
    quote_validation: ReviewStatus = ReviewStatus.PENDING
    normalized_sha256: str | None = None


class EvidenceCard(StrictModel):
    evidence_id: str = Field(pattern=ID_PATTERN)
    question_ids: list[str] = Field(default_factory=list)
    span_ids: list[str] = Field(min_length=1)
    proposition: str = Field(min_length=1)
    role: EvidenceRole
    directness: Directness
    scope: str = ""
    method_context: str = ""
    limitations: list[str] = Field(default_factory=list)
    independence_group: str | None = None
    review_status: ReviewStatus = ReviewStatus.PENDING
    reviewer: str | None = None
    allowed_uses: list[AllowedUse] = Field(default_factory=lambda: [AllowedUse.INTERNAL_SYNTHESIS])
    notes: str = ""

    @model_validator(mode="after")
    def accepted_cards_have_reviewer(self) -> "EvidenceCard":
        if self.review_status == ReviewStatus.ACCEPTED and not self.reviewer:
            raise ValueError("accepted evidence cards require a reviewer")
        if self.directness == Directness.GENERATED_CANDIDATE and AllowedUse.FORMAL_CLAIM in self.allowed_uses:
            raise ValueError("generated candidates cannot be allowed for formal claims")
        return self


class CandidateLink(StrictModel):
    link_id: str = Field(pattern=ID_PATTERN)
    participant_ids: list[str] = Field(min_length=2)
    origin: str
    description: str
    supporting_evidence_ids: list[str] = Field(default_factory=list)
    challenging_evidence_ids: list[str] = Field(default_factory=list)
    familiarity_risk: str = "not_checked"
    allowed_uses: list[AllowedUse] = Field(default_factory=lambda: [AllowedUse.INTERNAL_SYNTHESIS])
    status: LinkStatus = LinkStatus.CANDIDATE
    history: list[str] = Field(default_factory=list)
    reopening_condition: str = ""

    @model_validator(mode="after")
    def promoted_links_require_support(self) -> "CandidateLink":
        if self.status == LinkStatus.PROMOTED and not self.supporting_evidence_ids:
            raise ValueError("promoted candidate links require supporting evidence")
        return self


class ClaimRecord(StrictModel):
    claim_id: str = Field(pattern=ID_PATTERN)
    wording: str = Field(min_length=1)
    question_ids: list[str] = Field(default_factory=list)
    criticality: ClaimCriticality = ClaimCriticality.SUPPORTING
    status: ClaimStatus = ClaimStatus.PROPOSED
    supporting_evidence_ids: list[str] = Field(default_factory=list)
    refuting_evidence_ids: list[str] = Field(default_factory=list)
    qualifying_evidence_ids: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    inference_type: str = "interpretive"
    uncertainty: str = ""
    export_status: AllowedUse = AllowedUse.INTERNAL_SYNTHESIS
    citation_status: ReviewStatus = ReviewStatus.PENDING
    design_consequences: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def claim_status_has_required_evidence(self) -> "ClaimRecord":
        if self.status == ClaimStatus.SUPPORTED and not self.supporting_evidence_ids:
            raise ValueError("supported claims require supporting evidence")
        if self.status == ClaimStatus.CONTESTED:
            if not self.supporting_evidence_ids or not self.refuting_evidence_ids:
                raise ValueError("contested claims require both supporting and refuting evidence")
        if self.export_status == AllowedUse.FORMAL_CLAIM and self.status not in {
            ClaimStatus.SUPPORTED,
            ClaimStatus.CONTESTED,
        }:
            raise ValueError("formal-claim export requires a supported or contested claim")
        return self


class DesignDecision(StrictModel):
    decision_id: str = Field(pattern=ID_PATTERN)
    claim_ids: list[str] = Field(default_factory=list)
    concept: str
    operation: str
    user_need: str
    design_consequence: str
    technical_consequence: str
    alternatives: list[str] = Field(default_factory=list)
    selected_option: str | None = None
    evidence_ids: list[str] = Field(default_factory=list)
    test_or_evaluation: str
    risks: list[str] = Field(default_factory=list)
    reversibility: str
    status: DecisionStatus = DecisionStatus.PROPOSED

    @model_validator(mode="after")
    def accepted_decisions_are_grounded(self) -> "DesignDecision":
        if self.status == DecisionStatus.ACCEPTED:
            if not self.selected_option:
                raise ValueError("accepted decisions require a selected option")
            if not self.claim_ids and not self.evidence_ids:
                raise ValueError("accepted decisions require claim or evidence grounding")
        return self


class EventRecord(StrictModel):
    event_id: str = Field(pattern=ID_PATTERN)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor: str
    action: str
    input_ids: list[str] = Field(default_factory=list)
    output_ids: list[str] = Field(default_factory=list)
    tool: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)
    decision_note: str = ""
    status_changes: list[str] = Field(default_factory=list)
    branch: str = "main"
    previous_hash: str | None = None
    event_hash: str | None = None


class HandoffReceipt(StrictModel):
    objective_completed: str
    state_files_changed: list[str] = Field(default_factory=list)
    sources_added: list[str] = Field(default_factory=list)
    evidence_added: list[str] = Field(default_factory=list)
    claims_changed: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    unresolved: list[str] = Field(default_factory=list)
    failed_routes: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    do_not_repeat: list[str] = Field(default_factory=list)
    verification: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RunState(StrictModel):
    phase: str = "frame"
    active_question_ids: list[str] = Field(default_factory=list)
    corpus_snapshot_id: str | None = None
    last_event_hash: str | None = None
    blockers: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    budget: ResearchBudget = Field(default_factory=ResearchBudget)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditIssue(StrictModel):
    severity: str
    code: str
    message: str
    path: str | None = None
    object_id: str | None = None


class AuditReport(StrictModel):
    project_root: str
    release_mode: bool = False
    issues: list[AuditIssue] = Field(default_factory=list)
    checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def blockers(self) -> list[AuditIssue]:
        return [issue for issue in self.issues if issue.severity == "blocker"]

    @property
    def warnings(self) -> list[AuditIssue]:
        return [issue for issue in self.issues if issue.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.blockers
