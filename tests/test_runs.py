from __future__ import annotations

from pathlib import Path

import yaml

from mros.runs import (
    AuditStatus,
    OutputProfile,
    ResearchMode,
    RunStage,
    RunStatus,
    append_run_record,
    init_run,
    summarize_run,
    update_run_state,
    validate_run,
)


def _write_pass_audit(run: Path) -> None:
    (run / "audit.yaml").write_text(
        yaml.safe_dump(
            {
                "status": AuditStatus.PASS.value,
                "checks": ["citations checked", "exact terms checked"],
                "findings": [],
                "limitations": [],
                "reviewed_at": None,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def test_run_init_creates_lightweight_workspace(tmp_path: Path):
    run = tmp_path / "uncreative-writing-20260719"
    run.mkdir()
    (run / "request.md").write_text(
        "Gather a research note dossier around uncreative writing with exact terms.",
        encoding="utf-8",
    )
    state = init_run(
        run,
        mode=ResearchMode.DEEP,
        output_profile=OutputProfile.CONCEPT_DOSSIER,
        source_lanes=["web", "academic"],
        requirements=["exact-wording", "historical-map"],
    )
    assert state.mode == ResearchMode.DEEP
    assert state.output_profile == OutputProfile.CONCEPT_DOSSIER
    for name in [
        "queries.jsonl",
        "sources.jsonl",
        "terms.jsonl",
        "evidence.jsonl",
        "claims.jsonl",
        "visualization.md",
    ]:
        assert (run / name).exists()
    assert (run / "source-notes").is_dir()
    assert validate_run(run)["ok"] is True


def test_full_concept_dossier_flow_is_valid(tmp_path: Path):
    run = tmp_path / "uncreative-writing-demo"
    run.mkdir()
    (run / "request.md").write_text(
        'Gather a research note dossier around the concept "uncreative writing" with exact terms and wording.',
        encoding="utf-8",
    )
    init_run(
        run,
        mode=ResearchMode.DEEP,
        output_profile=OutputProfile.CONCEPT_DOSSIER,
        source_lanes=["web", "academic"],
        requirements=["exact-wording", "reference-by-reference", "visualization"],
        route_reason="The request asks for a historical, term-centered multi-source dossier.",
    )

    for query in [
        {
            "query_id": "query.exact",
            "exact_query": '"uncreative writing"',
            "strategy": "exact-term",
            "lane": "web",
            "purpose": "Locate explicit uses and canonical primary sources.",
            "batch": 1,
            "result_count": 12,
            "selected_source_ids": ["source.primary"],
        },
        {
            "query_id": "query.critique",
            "exact_query": '"uncreative writing" criticism',
            "strategy": "criticism",
            "lane": "academic",
            "purpose": "Locate scholarly challenges and later interpretation.",
            "batch": 2,
            "result_count": 8,
            "selected_source_ids": ["source.critique", "source.interpretation"],
        },
    ]:
        append_run_record(run, "query", query)

    for source in [
        {
            "source_id": "source.primary",
            "title": "Canonical primary source",
            "source_type": "book",
            "lane": "web",
            "role": "primary-core",
            "access_status": "accessible",
            "read_status": "close-read",
            "status": "selected",
            "citation": "Primary Author. Canonical Primary Source. 2011.",
            "selection_reason": "Explicitly names and defines the concept.",
        },
        {
            "source_id": "source.adjacent",
            "title": "Adjacent primary formulation",
            "source_type": "essay",
            "lane": "web",
            "role": "primary-adjacent",
            "access_status": "accessible",
            "read_status": "bounded-section",
            "status": "selected",
            "citation": "Adjacent Author. Adjacent Formulation. 2009.",
            "selection_reason": "Provides a neighboring term and practice.",
        },
        {
            "source_id": "source.interpretation",
            "title": "Scholarly interpretation",
            "source_type": "article",
            "lane": "academic",
            "role": "scholarly-interpretation",
            "access_status": "accessible",
            "read_status": "close-read",
            "status": "selected",
            "citation": "Scholar. Scholarly Interpretation. 2014.",
            "selection_reason": "Situates the concept historically.",
        },
        {
            "source_id": "source.critique",
            "title": "Critical response",
            "source_type": "article",
            "lane": "academic",
            "role": "critique",
            "access_status": "accessible",
            "read_status": "close-read",
            "status": "selected",
            "citation": "Critic. Critical Response. 2015.",
            "selection_reason": "Challenges exclusions and institutional effects.",
        },
        {
            "source_id": "source.reception",
            "title": "Later reception",
            "source_type": "chapter",
            "lane": "web",
            "role": "reception",
            "access_status": "preview_only",
            "read_status": "bounded-section",
            "status": "selected",
            "citation": "Later Scholar. Later Reception. 2020.",
            "selection_reason": "Tracks later use and teaching.",
        },
    ]:
        append_run_record(run, "source", source)

    append_run_record(
        run,
        "evidence",
        {
            "evidence_id": "evidence.definition",
            "source_id": "source.primary",
            "proposition": "The primary source defines the named practice through a specific formulation.",
            "role": "define",
            "exact_quote": "A short synthetic fixture quotation defining the named practice.",
            "context_before": "The author introduces the problem of authorship.",
            "context_after": "The author then describes practical consequences.",
            "location": "p. 12",
            "verified": True,
            "verification_method": "bounded-source-recheck",
        },
    )
    append_run_record(
        run,
        "evidence",
        {
            "evidence_id": "evidence.critique",
            "source_id": "source.critique",
            "proposition": "A critical source qualifies the concept's universal claims.",
            "role": "qualify",
            "paraphrase": "The critique argues that institutional position changes how appropriation is received.",
            "location": "pp. 4-6",
            "verified": True,
            "verification_method": "bounded-source-recheck",
        },
    )
    append_run_record(
        run,
        "term",
        {
            "term_id": "term.uncreative-writing",
            "label": "uncreative writing",
            "normalized_label": "uncreative writing",
            "kind": "definition",
            "source_id": "source.primary",
            "evidence_id": "evidence.definition",
            "exact_wording": "A short synthetic fixture quotation defining the named practice.",
            "location": "p. 12",
            "verified": True,
            "interpretation": "The wording makes the concept a procedure rather than a synonym for low quality.",
        },
    )
    append_run_record(
        run,
        "claim",
        {
            "claim_id": "claim.formation",
            "text": "The named concept is consolidated through a procedural account of writing rather than a simple rejection of creativity.",
            "claim_type": "definitional",
            "status": "qualified",
            "evidence_ids": ["evidence.definition"],
            "counterevidence_ids": ["evidence.critique"],
            "term_ids": ["term.uncreative-writing"],
            "scope": "The selected primary and critical sources.",
            "uncertainty": "This fixture does not establish first coinage.",
        },
    )

    (run / "dossier.md").write_text(
        "# Uncreative Writing: research note dossier\n\n"
        + "This synthetic end-to-end fixture demonstrates the dossier architecture rather than making a historical claim. "
        * 35,
        encoding="utf-8",
    )
    (run / "visualization.md").write_text(
        "# Concept map\n\n```mermaid\nflowchart LR\nA[Primary wording] --> B[Conceptual consolidation]\nB --> C[Critique]\n```\n",
        encoding="utf-8",
    )
    _write_pass_audit(run)
    update_run_state(
        run,
        status=RunStatus.COMPLETE,
        current_stage=RunStage.COMPLETE,
        user_visible_status="Research dossier complete and audited.",
        next_actions=[],
    )

    result = validate_run(run)
    assert result["ok"] is True
    assert result["counts"] == {
        "queries": 2,
        "sources": 5,
        "terms": 1,
        "evidence": 2,
        "claims": 1,
    }
    assert not [issue for issue in result["issues"] if issue["severity"] == "blocker"]
    summary = summarize_run(run)
    assert summary["output_profile"] == OutputProfile.CONCEPT_DOSSIER
    assert summary["stage"] == RunStage.COMPLETE


def test_run_validation_blocks_missing_source(tmp_path: Path):
    run = tmp_path / "broken-run"
    run.mkdir()
    (run / "request.md").write_text("Investigate.", encoding="utf-8")
    init_run(run, mode=ResearchMode.BRIEF)
    append_run_record(
        run,
        "evidence",
        {
            "evidence_id": "evidence.missing",
            "source_id": "source.missing",
            "proposition": "Something.",
            "paraphrase": "Something.",
            "verified": False,
        },
    )
    result = validate_run(run)
    assert result["ok"] is False
    assert any(issue["code"] == "missing_source" for issue in result["issues"])


def test_complete_run_blocks_supported_claim_without_evidence(tmp_path: Path):
    run = tmp_path / "unsupported-run"
    run.mkdir()
    (run / "request.md").write_text("Investigate.", encoding="utf-8")
    init_run(run, mode=ResearchMode.DEEP)
    append_run_record(
        run,
        "claim",
        {
            "claim_id": "claim.unsupported",
            "text": "A consequential claim.",
            "status": "supported",
        },
    )
    (run / "dossier.md").write_text("# Result\n\n" + "research output " * 120, encoding="utf-8")
    _write_pass_audit(run)
    update_run_state(run, status=RunStatus.COMPLETE, current_stage=RunStage.COMPLETE)
    result = validate_run(run)
    assert result["ok"] is False
    assert any(issue["code"] == "claim_without_evidence" for issue in result["issues"])


def test_complete_run_blocks_unverified_claim_evidence(tmp_path: Path):
    run = tmp_path / "unverified-run"
    run.mkdir()
    (run / "request.md").write_text("Investigate.", encoding="utf-8")
    init_run(run, mode=ResearchMode.BRIEF)
    append_run_record(
        run,
        "source",
        {
            "source_id": "source.one",
            "title": "Source",
            "source_type": "article",
            "lane": "web",
        },
    )
    append_run_record(
        run,
        "evidence",
        {
            "evidence_id": "evidence.one",
            "source_id": "source.one",
            "proposition": "A proposition.",
            "paraphrase": "A source passage.",
            "location": "p. 1",
            "verified": False,
        },
    )
    append_run_record(
        run,
        "claim",
        {
            "claim_id": "claim.one",
            "text": "A claim.",
            "status": "supported",
            "evidence_ids": ["evidence.one"],
        },
    )
    (run / "dossier.md").write_text("# Result\n\n" + "research output " * 120, encoding="utf-8")
    _write_pass_audit(run)
    update_run_state(run, status=RunStatus.COMPLETE, current_stage=RunStage.COMPLETE)
    result = validate_run(run)
    assert result["ok"] is False
    assert any(issue["code"] == "unverified_claim_evidence" for issue in result["issues"])


def test_concept_dossier_blocks_unverified_term(tmp_path: Path):
    run = tmp_path / "term-failure"
    run.mkdir()
    (run / "request.md").write_text("Build a concept dossier.", encoding="utf-8")
    init_run(
        run,
        mode=ResearchMode.DEEP,
        output_profile=OutputProfile.CONCEPT_DOSSIER,
        source_lanes=["web"],
    )
    append_run_record(
        run,
        "query",
        {
            "query_id": "query.one",
            "exact_query": '"concept"',
            "lane": "web",
            "purpose": "Find primary source.",
            "selected_source_ids": ["source.one"],
        },
    )
    append_run_record(
        run,
        "source",
        {
            "source_id": "source.one",
            "title": "Primary",
            "source_type": "book",
            "lane": "web",
            "role": "primary-core",
            "status": "selected",
        },
    )
    append_run_record(
        run,
        "evidence",
        {
            "evidence_id": "evidence.one",
            "source_id": "source.one",
            "proposition": "The term is used.",
            "exact_quote": "A candidate quotation.",
            "verified": False,
        },
    )
    append_run_record(
        run,
        "term",
        {
            "term_id": "term.one",
            "label": "concept",
            "source_id": "source.one",
            "evidence_id": "evidence.one",
            "exact_wording": "A candidate quotation.",
            "verified": False,
        },
    )
    append_run_record(
        run,
        "claim",
        {
            "claim_id": "claim.one",
            "text": "The concept is used.",
            "status": "supported",
            "evidence_ids": ["evidence.one"],
            "term_ids": ["term.one"],
        },
    )
    (run / "dossier.md").write_text("# Result\n\n" + "research output " * 120, encoding="utf-8")
    _write_pass_audit(run)
    update_run_state(run, status=RunStatus.COMPLETE, current_stage=RunStage.COMPLETE)
    result = validate_run(run)
    assert result["ok"] is False
    codes = {issue["code"] for issue in result["issues"]}
    assert "unverified_term" in codes
    assert "term_uses_unverified_evidence" in codes


def test_research_skill_is_semantic_front_door_and_concept_aware():
    root = Path(__file__).resolve().parents[1]
    text = (root / ".claude/skills/research/SKILL.md").read_text(encoding="utf-8")
    front = yaml.safe_load(text.split("---", 2)[1])
    assert front["name"] == "research"
    assert front.get("disable-model-invocation") is not True
    assert front.get("user-invocable") is False
    assert "rough natural-language" in front["description"]
    assert "exact terms" in front["description"]
    assert "WebSearch" in front["allowed-tools"]
    assert "WebFetch" in front["allowed-tools"]
    assert (root / ".claude/skills/research/profiles/concept-dossier.md").exists()
