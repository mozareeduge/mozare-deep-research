from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import yaml
from pydantic import ValidationError

from .coverage import compute_question_coverage
from .events import verify_event_chain
from .io import load_model, load_model_list, read_jsonl
from .models import (
    AccessStatus,
    AllowedUse,
    AuditIssue,
    AuditReport,
    CandidateLink,
    ClaimCriticality,
    ClaimRecord,
    DesignDecision,
    Directness,
    EvidenceCard,
    EvidenceSpan,
    HandoffReceipt,
    QueryRecord,
    ResearchContract,
    ResearchQuestion,
    ReviewStatus,
    RunState,
    SourceKind,
    SourceRecord,
)
from .quotes import quote_hash, verify_quote_file

PLACEHOLDER_RE = re.compile(
    r"\b(?:TODO|TBD|FIXME|CITATION NEEDED)\b|\?\?\?|\[\s*citation\s*\]",
    re.I,
)


def _issue(
    report: AuditReport,
    severity: str,
    code: str,
    message: str,
    path: str | None = None,
    object_id: str | None = None,
) -> None:
    report.issues.append(
        AuditIssue(
            severity=severity,
            code=code,
            message=message,
            path=path,
            object_id=object_id,
        )
    )


def _safe_load(report: AuditReport, root: Path, rel: str, key: str, model):
    path = root / rel
    try:
        return load_model_list(path, key, model)
    except FileNotFoundError:
        _issue(report, "blocker", "missing_file", f"required file is missing: {rel}", rel)
    except (ValidationError, ValueError, yaml.YAMLError) as exc:
        _issue(report, "blocker", "invalid_schema", str(exc), rel)
    return []


def _duplicates(values: list[str]) -> set[str]:
    return {value for value, count in Counter(values).items() if count > 1}


def _check_unique(report: AuditReport, code: str, values: list[str], path: str) -> None:
    duplicate = sorted(_duplicates(values))
    if duplicate:
        _issue(report, "blocker", code, f"duplicate IDs: {duplicate}", path)


def _question_cycles(questions: list[ResearchQuestion]) -> list[list[str]]:
    graph = {question.question_id: question.dependencies for question in questions}
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []
    cycles: list[list[str]] = []

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            start = stack.index(node)
            cycles.append(stack[start:] + [node])
            return
        visiting.add(node)
        stack.append(node)
        for neighbor in graph.get(node, []):
            if neighbor in graph:
                visit(neighbor)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
    return cycles


def _resolve_record_path(root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else root / path


def audit_project(root: Path, release_mode: bool = False) -> AuditReport:
    root = root.resolve()
    report = AuditReport(project_root=str(root), release_mode=release_mode)
    try:
        load_model(root / "research" / "contract.yaml", ResearchContract)
    except Exception as exc:
        _issue(
            report,
            "blocker",
            "invalid_contract",
            str(exc),
            "research/contract.yaml",
        )
    try:
        state = load_model(root / "research" / "state.yaml", RunState)
    except Exception as exc:
        _issue(
            report,
            "blocker",
            "invalid_state",
            str(exc),
            "research/state.yaml",
        )
        state = None

    questions = _safe_load(
        report, root, "research/questions.yaml", "questions", ResearchQuestion
    )
    sources = _safe_load(
        report, root, "sources/manifests/sources.yaml", "sources", SourceRecord
    )
    spans = _safe_load(
        report, root, "evidence/spans/spans.yaml", "spans", EvidenceSpan
    )
    cards = _safe_load(
        report, root, "evidence/cards/cards.yaml", "cards", EvidenceCard
    )
    links = _safe_load(
        report, root, "relations/candidates.yaml", "links", CandidateLink
    )
    claims = _safe_load(report, root, "claims/claims.yaml", "claims", ClaimRecord)
    decisions = _safe_load(
        report, root, "decisions/records.yaml", "decisions", DesignDecision
    )
    try:
        queries = [
            QueryRecord.model_validate(row)
            for row in read_jsonl(root / "queries/ledger.jsonl")
        ]
    except Exception as exc:
        _issue(
            report,
            "blocker",
            "invalid_query_ledger",
            str(exc),
            "queries/ledger.jsonl",
        )
        queries = []

    _check_unique(
        report,
        "duplicate_question_id",
        [x.question_id for x in questions],
        "research/questions.yaml",
    )
    _check_unique(
        report,
        "duplicate_source_id",
        [x.source_id for x in sources],
        "sources/manifests/sources.yaml",
    )
    _check_unique(
        report,
        "duplicate_span_id",
        [x.span_id for x in spans],
        "evidence/spans/spans.yaml",
    )
    _check_unique(
        report,
        "duplicate_evidence_id",
        [x.evidence_id for x in cards],
        "evidence/cards/cards.yaml",
    )
    _check_unique(
        report,
        "duplicate_link_id",
        [x.link_id for x in links],
        "relations/candidates.yaml",
    )
    _check_unique(
        report,
        "duplicate_claim_id",
        [x.claim_id for x in claims],
        "claims/claims.yaml",
    )
    _check_unique(
        report,
        "duplicate_decision_id",
        [x.decision_id for x in decisions],
        "decisions/records.yaml",
    )
    _check_unique(
        report,
        "duplicate_query_id",
        [x.query_id for x in queries],
        "queries/ledger.jsonl",
    )

    source_ids = {x.source_id for x in sources}
    span_ids = {x.span_id for x in spans}
    card_ids = {x.evidence_id for x in cards}
    claim_ids = {x.claim_id for x in claims}
    question_ids = {x.question_id for x in questions}
    source_by_id = {x.source_id: x for x in sources}
    span_by_id = {x.span_id: x for x in spans}
    card_by_id = {x.evidence_id: x for x in cards}

    for question in questions:
        missing = set(question.dependencies) - question_ids
        if missing:
            _issue(
                report,
                "blocker",
                "orphan_question_dependency",
                f"missing question dependencies: {sorted(missing)}",
                object_id=question.question_id,
            )
    for cycle in _question_cycles(questions):
        _issue(
            report,
            "blocker",
            "question_dependency_cycle",
            " -> ".join(cycle),
            "research/questions.yaml",
        )

    for source in sources:
        for local_file in source.local_files:
            path = _resolve_record_path(root, local_file)
            if not path.is_file():
                severity = (
                    "blocker"
                    if release_mode and AllowedUse.FORMAL_CLAIM in source.allowed_uses
                    else "warning"
                )
                _issue(
                    report,
                    severity,
                    "missing_source_file",
                    f"local source file not found: {local_file}",
                    object_id=source.source_id,
                )

    for query in queries:
        if query.question_id not in question_ids:
            _issue(
                report,
                "blocker",
                "orphan_query_question",
                f"query references missing question {query.question_id}",
                object_id=query.query_id,
            )

    for span in spans:
        if span.source_id not in source_ids:
            _issue(
                report,
                "blocker",
                "orphan_span",
                f"span references missing source {span.source_id}",
                object_id=span.span_id,
            )
        path = _resolve_record_path(root, span.file_path)
        if not path.is_file():
            severity = "blocker" if release_mode else "warning"
            _issue(
                report,
                severity,
                "missing_evidence_file",
                f"evidence source file not found: {span.file_path}",
                object_id=span.span_id,
            )
        elif span.quote_validation == ReviewStatus.ACCEPTED:
            match = verify_quote_file(path, span.exact_text)
            if not match.matched:
                _issue(
                    report,
                    "blocker",
                    "accepted_quote_mismatch",
                    "accepted quotation no longer matches its source file",
                    object_id=span.span_id,
                )
            if span.normalized_sha256 and span.normalized_sha256 != quote_hash(span.exact_text):
                _issue(
                    report,
                    "blocker",
                    "quote_hash_mismatch",
                    "stored normalized quotation hash does not match exact_text",
                    object_id=span.span_id,
                )
        if span.quote_validation != ReviewStatus.ACCEPTED:
            severity = "blocker" if release_mode else "warning"
            _issue(
                report,
                severity,
                "unverified_quote",
                "evidence span is not accepted as quote-verified",
                object_id=span.span_id,
            )

    for card in cards:
        missing = set(card.span_ids) - span_ids
        if missing:
            _issue(
                report,
                "blocker",
                "orphan_evidence_card",
                f"missing span ids: {sorted(missing)}",
                object_id=card.evidence_id,
            )
        missing_questions = set(card.question_ids) - question_ids
        if missing_questions:
            _issue(
                report,
                "blocker",
                "orphan_evidence_question",
                f"missing question ids: {sorted(missing_questions)}",
                object_id=card.evidence_id,
            )
        if card.review_status == ReviewStatus.ACCEPTED:
            for span_id in card.span_ids:
                span = span_by_id.get(span_id)
                source = source_by_id.get(span.source_id) if span else None
                if span and span.quote_validation != ReviewStatus.ACCEPTED:
                    _issue(
                        report,
                        "blocker",
                        "accepted_card_unverified_span",
                        "accepted evidence card includes an unverified span",
                        object_id=card.evidence_id,
                    )
                if source and (
                    source.kind == SourceKind.GENERATED
                    or source.access_status == AccessStatus.GENERATED
                ):
                    _issue(
                        report,
                        "blocker",
                        "generated_evidence_upgrade",
                        "generated material cannot be accepted as source evidence",
                        object_id=card.evidence_id,
                    )
                if source and source.access_status == AccessStatus.METADATA_ONLY:
                    _issue(
                        report,
                        "blocker",
                        "metadata_content_claim",
                        "metadata-only source cannot support passage evidence",
                        object_id=card.evidence_id,
                    )
        if (
            card.directness == Directness.GENERATED_CANDIDATE
            and AllowedUse.FORMAL_CLAIM in card.allowed_uses
        ):
            _issue(
                report,
                "blocker",
                "generated_formal_use",
                "generated candidate allowed for formal claim",
                object_id=card.evidence_id,
            )

    for claim in claims:
        referenced = set(
            claim.supporting_evidence_ids
            + claim.refuting_evidence_ids
            + claim.qualifying_evidence_ids
        )
        missing = referenced - card_ids
        if missing:
            _issue(
                report,
                "blocker",
                "orphan_claim_evidence",
                f"missing evidence ids: {sorted(missing)}",
                object_id=claim.claim_id,
            )
        missing_q = set(claim.question_ids) - question_ids
        if missing_q:
            _issue(
                report,
                "blocker",
                "orphan_claim_question",
                f"missing question ids: {sorted(missing_q)}",
                object_id=claim.claim_id,
            )
        missing_dependencies = set(claim.dependencies) - claim_ids
        if missing_dependencies:
            _issue(
                report,
                "blocker",
                "orphan_claim_dependency",
                f"missing claim dependencies: {sorted(missing_dependencies)}",
                object_id=claim.claim_id,
            )
        if claim.claim_id in claim.dependencies:
            _issue(
                report,
                "blocker",
                "claim_self_dependency",
                "claim cannot depend on itself",
                object_id=claim.claim_id,
            )
        if claim.export_status == AllowedUse.FORMAL_CLAIM:
            for evidence_id in claim.supporting_evidence_ids:
                card = card_by_id.get(evidence_id)
                if (
                    not card
                    or card.review_status != ReviewStatus.ACCEPTED
                    or AllowedUse.FORMAL_CLAIM not in card.allowed_uses
                ):
                    _issue(
                        report,
                        "blocker",
                        "formal_claim_unapproved_evidence",
                        "formal claim uses evidence not approved for formal use",
                        object_id=claim.claim_id,
                    )
        if (
            release_mode
            and claim.criticality == ClaimCriticality.CENTRAL
            and claim.citation_status != ReviewStatus.ACCEPTED
        ):
            _issue(
                report,
                "blocker",
                "central_claim_citation_unchecked",
                "central claim citation status is not accepted",
                object_id=claim.claim_id,
            )

    for link in links:
        missing = set(
            link.supporting_evidence_ids + link.challenging_evidence_ids
        ) - card_ids
        if missing:
            _issue(
                report,
                "blocker",
                "orphan_candidate_link",
                f"missing evidence ids: {sorted(missing)}",
                object_id=link.link_id,
            )

    for decision in decisions:
        missing_claims = set(decision.claim_ids) - claim_ids
        missing_evidence = set(decision.evidence_ids) - card_ids
        if missing_claims or missing_evidence:
            _issue(
                report,
                "blocker",
                "orphan_decision_grounding",
                f"missing claims={sorted(missing_claims)}, evidence={sorted(missing_evidence)}",
                object_id=decision.decision_id,
            )

    for coverage in compute_question_coverage(questions, claims, cards, queries):
        if coverage.critical and not coverage.requirement_met:
            severity = "blocker" if release_mode else "warning"
            _issue(
                report,
                severity,
                "critical_question_incomplete",
                "; ".join(coverage.blockers),
                object_id=coverage.question_id,
            )

    event_path = root / "events/events.jsonl"
    event_rows: list[dict] = []
    event_ledger_valid = True
    try:
        event_rows = read_jsonl(event_path)
        for issue in verify_event_chain(event_path):
            event_ledger_valid = False
            _issue(
                report,
                "blocker",
                "event_chain_invalid",
                issue,
                "events/events.jsonl",
            )
    except Exception as exc:
        event_ledger_valid = False
        _issue(
            report,
            "blocker",
            "invalid_event_ledger",
            str(exc),
            "events/events.jsonl",
        )
    if state is not None and event_ledger_valid:
        actual_last_hash = event_rows[-1].get("event_hash") if event_rows else None
        if state.last_event_hash != actual_last_hash:
            _issue(
                report,
                "blocker",
                "state_event_hash_mismatch",
                "research state last_event_hash does not match the event ledger",
                "research/state.yaml",
            )

    handoff_path = root / "research/handoff.yaml"
    if handoff_path.exists() and handoff_path.read_text(encoding="utf-8").strip() not in {"", "{}"}:
        try:
            load_model(handoff_path, HandoffReceipt)
        except Exception as exc:
            _issue(
                report,
                "warning" if not release_mode else "blocker",
                "invalid_handoff",
                str(exc),
                "research/handoff.yaml",
            )

    if release_mode:
        release_files = [
            p
            for p in (root / "releases").rglob("*")
            if p.is_file() and p.name != ".gitkeep"
        ]
        if not release_files:
            _issue(
                report,
                "blocker",
                "missing_release",
                "no release artifact exists",
                "releases",
            )
        for path in release_files:
            if path.suffix.lower() in {".md", ".txt", ".yaml", ".yml", ".json"}:
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                if PLACEHOLDER_RE.search(text):
                    _issue(
                        report,
                        "blocker",
                        "unresolved_placeholder",
                        "release contains an unresolved drafting or citation placeholder",
                        str(path.relative_to(root)),
                    )
    return report
