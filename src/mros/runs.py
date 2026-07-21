"""Durable semantic research runs for MROS.

The run layer is intentionally lighter than the framework's legacy project records. It gives
Claude one inspectable unit for an ordinary-language inquiry while preserving the distinctions
needed for academic research: searches, sources, exact wording, evidence, claims, and audit.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import Field, model_validator

from .io import append_jsonl, dump_data, load_data, read_jsonl
from .models import ID_PATTERN, StrictModel


class ResearchMode(StrEnum):
    LOOKUP = "lookup"
    CLOSE_READ = "close-read"
    BRIEF = "brief"
    DEEP = "deep"
    DESIGN = "design"


class OutputProfile(StrEnum):
    SOURCE_ANSWER = "source-answer"
    RESEARCH_NOTE = "research-note"
    CONCEPT_DOSSIER = "concept-dossier"
    LITERATURE_REVIEW = "literature-review"
    COMPARATIVE_REPORT = "comparative-report"
    DESIGN_BRIEF = "design-brief"


class RunStage(StrEnum):
    ROUTING = "routing"
    PLANNING = "planning"
    DISCOVERY = "discovery"
    SELECTION = "selection"
    READING = "reading"
    EVIDENCE = "evidence"
    CHALLENGE = "challenge"
    SYNTHESIS = "synthesis"
    VERIFICATION = "verification"
    COMPLETE = "complete"


class RunStatus(StrEnum):
    ACTIVE = "active"
    NEEDS_INPUT = "needs_input"
    BLOCKED = "blocked"
    COMPLETE = "complete"


class AuditStatus(StrEnum):
    PENDING = "pending"
    PASS = "pass"
    PASS_WITH_LIMITS = "pass_with_limits"
    FAIL = "fail"


class AccessStatus(StrEnum):
    UNKNOWN = "unknown"
    ACCESSIBLE = "accessible"
    ABSTRACT_ONLY = "abstract_only"
    PREVIEW_ONLY = "preview_only"
    PAYWALLED = "paywalled"
    UNAVAILABLE = "unavailable"


class SourceStatus(StrEnum):
    CANDIDATE = "candidate"
    SELECTED = "selected"
    REJECTED = "rejected"
    UNAVAILABLE = "unavailable"


class SourceRole(StrEnum):
    PRIMARY_CORE = "primary-core"
    PRIMARY_ADJACENT = "primary-adjacent"
    SCHOLARLY_INTERPRETATION = "scholarly-interpretation"
    CRITIQUE = "critique"
    RECEPTION = "reception"
    CONTEXT = "context"
    DISCOVERY_ONLY = "discovery-only"


class ReadStatus(StrEnum):
    UNREAD = "unread"
    METADATA = "metadata"
    ABSTRACT = "abstract"
    BOUNDED_SECTION = "bounded-section"
    CLOSE_READ = "close-read"


class QueryStrategy(StrEnum):
    EXACT_TERM = "exact-term"
    CANONICAL_WORK = "canonical-work"
    TERMINOLOGY_VARIANT = "terminology-variant"
    CITATION_CHAIN = "citation-chain"
    PRECURSOR = "precursor"
    ADJACENT = "adjacent"
    CRITICISM = "criticism"
    RECEPTION = "reception"
    OFFICIAL_PRIMARY = "official-primary"
    NON_ENGLISH = "non-english"
    OTHER = "other"


class EvidenceRole(StrEnum):
    SUPPORT = "support"
    REFUTE = "refute"
    QUALIFY = "qualify"
    DEFINE = "define"
    CONTEXTUALIZE = "contextualize"
    EXAMPLE = "example"


class VerificationMethod(StrEnum):
    NOT_VERIFIED = "not-verified"
    BOUNDED_SOURCE_RECHECK = "bounded-source-recheck"
    EXACT_MATCH_SCRIPT = "exact-match-script"
    INDIRECT_REFERENCE = "indirect-reference"
    METADATA_ONLY = "metadata-only"


class TermKind(StrEnum):
    COINAGE = "coinage"
    DEFINITION = "definition"
    KEY_TERM = "key-term"
    METHOD = "method"
    DISTINCTION = "distinction"
    SLOGAN = "slogan"
    CRITIQUE = "critique"
    RECEPTION_LABEL = "reception-label"
    VARIANT = "variant"


class ClaimType(StrEnum):
    HISTORICAL = "historical"
    DEFINITIONAL = "definitional"
    INTERPRETIVE = "interpretive"
    COMPARATIVE = "comparative"
    RECEPTION = "reception"
    CRITICAL = "critical"
    METHODOLOGICAL = "methodological"
    DESIGN = "design"


class ClaimStatus(StrEnum):
    PROPOSED = "proposed"
    SUPPORTED = "supported"
    CONTESTED = "contested"
    QUALIFIED = "qualified"
    INSUFFICIENT = "insufficient"
    UNRESOLVED = "unresolved"
    WITHDRAWN = "withdrawn"


class ResearchBudget(StrictModel):
    max_query_batches: int = Field(default=4, ge=1, le=12)
    max_candidates: int = Field(default=40, ge=1, le=200)
    max_selected_sources: int = Field(default=18, ge=1, le=60)
    max_core_close_reads: int = Field(default=8, ge=1, le=30)
    max_evidence_items: int = Field(default=40, ge=1, le=200)
    max_terms: int = Field(default=50, ge=1, le=250)
    max_subagents: int = Field(default=2, ge=0, le=4)
    checkpoint_after_items: int = Field(default=5, ge=1, le=25)
    stop_rule: str = (
        "Stop when central coverage slots are supported, contested, or explicitly unresolved "
        "and two bounded searches add little consequential evidence."
    )


class ResearchRunState(StrictModel):
    run_id: str = Field(pattern=ID_PATTERN)
    title: str = Field(min_length=1, max_length=300)
    mode: ResearchMode
    output_profile: OutputProfile = OutputProfile.RESEARCH_NOTE
    route_reason: str = ""
    status: RunStatus = RunStatus.ACTIVE
    current_stage: RunStage = RunStage.PLANNING
    source_lanes: list[str] = Field(default_factory=list)
    excluded_lanes: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(default_factory=list)
    scope_notes: list[str] = Field(default_factory=list)
    budget: ResearchBudget = Field(default_factory=ResearchBudget)
    progress: dict[str, int] = Field(default_factory=dict)
    open_questions: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    user_visible_status: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RunQuery(StrictModel):
    query_id: str = Field(pattern=ID_PATTERN)
    exact_query: str = Field(min_length=1)
    strategy: QueryStrategy = QueryStrategy.OTHER
    lane: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    batch: int = Field(default=1, ge=1)
    result_count: int | None = Field(default=None, ge=0)
    selected_source_ids: list[str] = Field(default_factory=list)
    notes: str = ""
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RunSource(StrictModel):
    source_id: str = Field(pattern=ID_PATTERN)
    title: str = Field(min_length=1)
    url: str | None = None
    identifier: str | None = None
    source_type: str
    creators: list[str] = Field(default_factory=list)
    year: str | None = None
    lane: str
    role: SourceRole = SourceRole.CONTEXT
    access_status: AccessStatus = AccessStatus.UNKNOWN
    read_status: ReadStatus = ReadStatus.UNREAD
    status: SourceStatus = SourceStatus.CANDIDATE
    citation: str = ""
    selected_for: list[str] = Field(default_factory=list)
    selection_reason: str = ""
    limitations: list[str] = Field(default_factory=list)
    notes: str = ""


class RunEvidence(StrictModel):
    evidence_id: str = Field(pattern=ID_PATTERN)
    source_id: str = Field(pattern=ID_PATTERN)
    proposition: str = Field(min_length=1)
    role: EvidenceRole = EvidenceRole.SUPPORT
    exact_quote: str | None = None
    paraphrase: str | None = None
    context_before: str = ""
    context_after: str = ""
    location: str = ""
    verified: bool = False
    verification_method: VerificationMethod = VerificationMethod.NOT_VERIFIED
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def has_content(self) -> "RunEvidence":
        if not self.exact_quote and not self.paraphrase:
            raise ValueError("evidence requires exact_quote or paraphrase")
        if self.verified and self.verification_method == VerificationMethod.NOT_VERIFIED:
            raise ValueError("verified evidence requires a verification_method")
        return self


class RunTerm(StrictModel):
    term_id: str = Field(pattern=ID_PATTERN)
    label: str = Field(min_length=1)
    normalized_label: str = ""
    kind: TermKind = TermKind.KEY_TERM
    source_id: str = Field(pattern=ID_PATTERN)
    evidence_id: str = Field(pattern=ID_PATTERN)
    exact_wording: str = Field(min_length=1)
    location: str = ""
    verified: bool = False
    interpretation: str = ""
    variants: list[str] = Field(default_factory=list)
    notes: str = ""


class RunClaim(StrictModel):
    claim_id: str = Field(pattern=ID_PATTERN)
    text: str = Field(min_length=1)
    claim_type: ClaimType = ClaimType.INTERPRETIVE
    status: ClaimStatus = ClaimStatus.PROPOSED
    evidence_ids: list[str] = Field(default_factory=list)
    counterevidence_ids: list[str] = Field(default_factory=list)
    term_ids: list[str] = Field(default_factory=list)
    scope: str = ""
    uncertainty: str = ""
    notes: str = ""


class RunAudit(StrictModel):
    status: AuditStatus = AuditStatus.PENDING
    checks: list[str] = Field(default_factory=list)
    findings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    reviewed_at: datetime | None = None


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _request_text(run_dir: Path) -> str:
    request = run_dir / "request.md"
    if not request.is_file():
        raise FileNotFoundError(f"Create {request} with the user's request before run-init")
    text = request.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("request.md is empty")
    return text


def _default_title(request: str) -> str:
    first = next((line.strip("# ") for line in request.splitlines() if line.strip()), "Research run")
    return first[:120]


def init_run(
    run_dir: Path,
    *,
    mode: ResearchMode,
    title: str | None = None,
    source_lanes: list[str] | None = None,
    excluded_lanes: list[str] | None = None,
    output_profile: OutputProfile = OutputProfile.RESEARCH_NOTE,
    route_reason: str = "",
    requirements: list[str] | None = None,
    budget: ResearchBudget | None = None,
    force: bool = False,
) -> ResearchRunState:
    run_dir = run_dir.resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    request = _request_text(run_dir)
    state_path = run_dir / "state.yaml"
    if state_path.exists() and not force:
        raise FileExistsError(f"Research run already initialized at {run_dir}")
    run_id = run_dir.name.lower().replace("_", "-")
    if not re.fullmatch(ID_PATTERN, run_id):
        raise ValueError(
            "run directory name must start with a letter and use lowercase letters, digits, '.', ':', '_' or '-'"
        )
    state = ResearchRunState(
        run_id=run_id,
        title=title or _default_title(request),
        mode=mode,
        output_profile=output_profile,
        route_reason=route_reason,
        source_lanes=source_lanes or [],
        excluded_lanes=excluded_lanes or [],
        requirements=requirements or [],
        budget=budget or ResearchBudget(),
        next_actions=["Create a compact work order and begin the first bounded discovery batch."],
        user_visible_status="Preparing the research route.",
    )
    dump_data(state_path, state)
    (run_dir / "plan.md").write_text(
        "# Research work order\n\n"
        "- Purpose and deliverable:\n"
        "- Scope and exclusions:\n"
        "- Coverage slots:\n"
        "- Source roles and lanes:\n"
        "- Search strategies:\n"
        "- Reading priorities:\n"
        "- Stop condition:\n",
        encoding="utf-8",
    )
    for name in ["queries.jsonl", "sources.jsonl", "terms.jsonl", "evidence.jsonl", "claims.jsonl"]:
        (run_dir / name).touch()
    (run_dir / "source-notes").mkdir(exist_ok=True)
    (run_dir / "dossier.md").write_text("# Research output\n\n", encoding="utf-8")
    (run_dir / "visualization.md").write_text("# Research visualization\n\n", encoding="utf-8")
    dump_data(run_dir / "audit.yaml", RunAudit())
    return state


def append_run_record(run_dir: Path, kind: str, record: dict[str, Any]) -> StrictModel:
    mapping: dict[str, tuple[type[StrictModel], str]] = {
        "query": (RunQuery, "queries.jsonl"),
        "source": (RunSource, "sources.jsonl"),
        "term": (RunTerm, "terms.jsonl"),
        "evidence": (RunEvidence, "evidence.jsonl"),
        "claim": (RunClaim, "claims.jsonl"),
    }
    if kind not in mapping:
        raise ValueError(f"unknown record kind: {kind}")
    model, filename = mapping[kind]
    validated = model.model_validate(record)
    append_jsonl(run_dir / filename, validated.model_dump(mode="json", exclude_none=True))
    return validated


def update_run_state(run_dir: Path, **changes: Any) -> ResearchRunState:
    state = ResearchRunState.model_validate(load_data(run_dir / "state.yaml"))
    merged = state.model_dump(mode="python")
    merged.update(changes)
    merged["updated_at"] = _utcnow()
    updated = ResearchRunState.model_validate(merged)
    dump_data(run_dir / "state.yaml", updated)
    return updated


def summarize_run(run_dir: Path) -> dict[str, Any]:
    result = validate_run(run_dir)
    state = ResearchRunState.model_validate(load_data(run_dir / "state.yaml"))
    return {
        "run_id": state.run_id,
        "title": state.title,
        "mode": state.mode,
        "output_profile": state.output_profile,
        "status": state.status,
        "stage": state.current_stage,
        "user_visible_status": state.user_visible_status,
        "counts": result.get("counts", {}),
        "next_actions": state.next_actions[:3],
        "open_questions": state.open_questions[:3],
        "ok": result.get("ok", False),
        "issues": result.get("issues", []),
    }


def validate_run(run_dir: Path) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    issues: list[dict[str, str]] = []
    try:
        state = ResearchRunState.model_validate(load_data(run_dir / "state.yaml"))
    except Exception as exc:
        return {
            "ok": False,
            "run_dir": str(run_dir),
            "issues": [{"severity": "blocker", "code": "invalid_state", "message": str(exc)}],
        }

    def parse_rows(filename: str, model: type[StrictModel]) -> list[StrictModel]:
        rows: list[StrictModel] = []
        try:
            rows = [model.model_validate(row) for row in read_jsonl(run_dir / filename)]
        except Exception as exc:
            issues.append({"severity": "blocker", "code": f"invalid_{filename}", "message": str(exc)})
        return rows

    queries = parse_rows("queries.jsonl", RunQuery)
    sources = parse_rows("sources.jsonl", RunSource)
    terms = parse_rows("terms.jsonl", RunTerm)
    evidence = parse_rows("evidence.jsonl", RunEvidence)
    claims = parse_rows("claims.jsonl", RunClaim)

    def duplicate_ids(rows: list[StrictModel], field: str, code: str) -> None:
        values = [str(getattr(row, field)) for row in rows]
        for value in sorted({x for x in values if values.count(x) > 1}):
            issues.append({"severity": "blocker", "code": code, "message": value})

    duplicate_ids(queries, "query_id", "duplicate_query_id")
    duplicate_ids(sources, "source_id", "duplicate_source_id")
    duplicate_ids(terms, "term_id", "duplicate_term_id")
    duplicate_ids(evidence, "evidence_id", "duplicate_evidence_id")
    duplicate_ids(claims, "claim_id", "duplicate_claim_id")

    source_ids = {str(x.source_id) for x in sources}
    evidence_ids = {str(x.evidence_id) for x in evidence}
    term_ids = {str(x.term_id) for x in terms}
    evidence_by_id = {str(item.evidence_id): item for item in evidence}

    for query in queries:
        for source_id in query.selected_source_ids:
            if source_id not in source_ids:
                issues.append({
                    "severity": "blocker",
                    "code": "query_missing_source",
                    "message": f"{query.query_id} -> {source_id}",
                })
    for item in evidence:
        if item.source_id not in source_ids:
            issues.append({
                "severity": "blocker",
                "code": "missing_source",
                "message": f"{item.evidence_id} -> {item.source_id}",
            })
    for term in terms:
        if term.source_id not in source_ids:
            issues.append({
                "severity": "blocker",
                "code": "term_missing_source",
                "message": f"{term.term_id} -> {term.source_id}",
            })
        if term.evidence_id not in evidence_ids:
            issues.append({
                "severity": "blocker",
                "code": "term_missing_evidence",
                "message": f"{term.term_id} -> {term.evidence_id}",
            })
    for claim in claims:
        for evidence_id in claim.evidence_ids + claim.counterevidence_ids:
            if evidence_id not in evidence_ids:
                issues.append({
                    "severity": "blocker",
                    "code": "missing_evidence",
                    "message": f"{claim.claim_id} -> {evidence_id}",
                })
        for term_id in claim.term_ids:
            if term_id not in term_ids:
                issues.append({
                    "severity": "blocker",
                    "code": "missing_term",
                    "message": f"{claim.claim_id} -> {term_id}",
                })

    try:
        audit = RunAudit.model_validate(load_data(run_dir / "audit.yaml"))
    except Exception as exc:
        audit = RunAudit(status=AuditStatus.FAIL, limitations=[str(exc)])
        issues.append({"severity": "blocker", "code": "invalid_audit", "message": str(exc)})

    dossier = (run_dir / "dossier.md").read_text(encoding="utf-8").strip() if (run_dir / "dossier.md").exists() else ""
    if state.status == RunStatus.COMPLETE:
        if state.current_stage != RunStage.COMPLETE:
            issues.append({
                "severity": "blocker",
                "code": "stage_status_mismatch",
                "message": "complete status requires complete stage",
            })
        if len(dossier.split()) < 100:
            issues.append({
                "severity": "blocker",
                "code": "empty_deliverable",
                "message": "complete run has fewer than 100 dossier words",
            })
        if audit.status not in {AuditStatus.PASS, AuditStatus.PASS_WITH_LIMITS}:
            issues.append({
                "severity": "blocker",
                "code": "audit_not_passed",
                "message": str(audit.status),
            })
        consequential_statuses = {ClaimStatus.SUPPORTED, ClaimStatus.CONTESTED, ClaimStatus.QUALIFIED}
        consequential = [c for c in claims if c.status in consequential_statuses]
        if state.mode in {ResearchMode.DEEP, ResearchMode.DESIGN} and not consequential:
            issues.append({
                "severity": "blocker",
                "code": "no_supported_claims",
                "message": "deep/design run has no supported, contested, or qualified claims",
            })
        for claim in consequential:
            linked = list(dict.fromkeys(claim.evidence_ids + claim.counterevidence_ids))
            if not linked:
                issues.append({
                    "severity": "blocker",
                    "code": "claim_without_evidence",
                    "message": str(claim.claim_id),
                })
                continue
            for evidence_id in linked:
                item = evidence_by_id.get(evidence_id)
                if item is not None and not item.verified:
                    issues.append({
                        "severity": "blocker",
                        "code": "unverified_claim_evidence",
                        "message": f"{claim.claim_id} -> {evidence_id}",
                    })

        if state.output_profile == OutputProfile.CONCEPT_DOSSIER:
            if not terms:
                issues.append({
                    "severity": "blocker",
                    "code": "concept_dossier_without_terms",
                    "message": "concept dossier requires a verified term ledger",
                })
            if not any(s.status == SourceStatus.SELECTED and s.role == SourceRole.PRIMARY_CORE for s in sources):
                issues.append({
                    "severity": "blocker",
                    "code": "concept_dossier_without_primary_core",
                    "message": "concept dossier requires at least one selected primary-core source",
                })
            if any(lane in {"web", "academic"} for lane in state.source_lanes) and not queries:
                issues.append({
                    "severity": "blocker",
                    "code": "concept_dossier_without_query_log",
                    "message": "web/academic concept dossier requires a query log",
                })
            for term in terms:
                item = evidence_by_id.get(str(term.evidence_id))
                if not term.verified:
                    issues.append({
                        "severity": "blocker",
                        "code": "unverified_term",
                        "message": str(term.term_id),
                    })
                if item is not None:
                    if not item.verified:
                        issues.append({
                            "severity": "blocker",
                            "code": "term_uses_unverified_evidence",
                            "message": f"{term.term_id} -> {term.evidence_id}",
                        })
                    if not item.exact_quote:
                        issues.append({
                            "severity": "blocker",
                            "code": "term_without_exact_quote",
                            "message": f"{term.term_id} -> {term.evidence_id}",
                        })

        selected_sources = [s for s in sources if s.status == SourceStatus.SELECTED]
        if state.mode == ResearchMode.DEEP and len(selected_sources) < 5:
            issues.append({
                "severity": "warning",
                "code": "thin_deep_source_set",
                "message": f"deep run selected only {len(selected_sources)} sources",
            })
        if state.output_profile == OutputProfile.CONCEPT_DOSSIER:
            represented_roles = {s.role for s in selected_sources}
            if SourceRole.CRITIQUE not in represented_roles:
                issues.append({
                    "severity": "warning",
                    "code": "no_critique_source",
                    "message": "concept dossier has no selected critique source",
                })
            if SourceRole.SCHOLARLY_INTERPRETATION not in represented_roles:
                issues.append({
                    "severity": "warning",
                    "code": "no_scholarly_interpretation",
                    "message": "concept dossier has no selected scholarly interpretation",
                })

    return {
        "ok": not any(x["severity"] == "blocker" for x in issues),
        "run_dir": str(run_dir),
        "run_id": state.run_id,
        "mode": state.mode,
        "output_profile": state.output_profile,
        "status": state.status,
        "stage": state.current_stage,
        "counts": {
            "queries": len(queries),
            "sources": len(sources),
            "terms": len(terms),
            "evidence": len(evidence),
            "claims": len(claims),
        },
        "audit_status": audit.status,
        "issues": issues,
    }
