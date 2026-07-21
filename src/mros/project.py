from __future__ import annotations

import shutil
from pathlib import Path

from .io import dump_data


PROJECT_DIRS = [
    "research", "research/runs", "sources/manifests", "sources/inbox", "corpus/originals", "corpus/index",
    "queries", "evidence/spans", "evidence/cards", "relations", "claims", "decisions",
    "events", "audits", "releases", "residue", ".mros",
]


def package_root() -> Path:
    return Path(__file__).resolve().parents[2]


def init_project(root: Path, project_id: str, title: str, force: bool = False) -> None:
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    marker = root / ".mros" / "project.yaml"
    if marker.exists() and not force:
        raise FileExistsError(f"MROS project already exists at {root}")
    for relative in PROJECT_DIRS:
        (root / relative).mkdir(parents=True, exist_ok=True)
    for directory in ["research/runs", "sources/inbox", "corpus/originals", "corpus/index", "audits", "releases", "residue"]:
        (root / directory / ".gitkeep").touch()
    dump_data(marker, {"project_id": project_id, "title": title, "schema_version": "1.2"})
    dump_data(root / "research" / "contract.yaml", {
        "project_id": project_id,
        "title": title,
        "research_purpose": "Define the research purpose before discovery.",
        "target_decisions": [], "audiences": [], "genres": [], "scope": [], "exclusions": [],
        "uncertainty_policy": "Record unknown, not accessed, and not verified states explicitly.",
        "languages": ["en"], "source_policies": [], "output_obligations": [],
        "approval_gates": ["scope", "central_claim_promotion", "destructive_library_change", "final_release"],
        "budget": {
            "model": "sonnet", "effort": "medium", "max_query_batches": 2,
            "max_tool_calls": 30, "max_candidates": 20, "max_full_sources": 5,
            "max_evidence_spans": 12, "max_subagents": 1, "max_output_words": 1500,
            "stop_rule": "Stop when critical claims are supported, contested, or explicitly unresolved and marginal evidence gain is low."
        }
    })
    dump_data(root / "research" / "questions.yaml", {"questions": []})
    dump_data(root / "research" / "state.yaml", {
        "phase": "frame", "active_question_ids": [], "blockers": [], "next_actions": ["Complete research/contract.yaml"],
        "budget": {
            "model": "sonnet", "effort": "medium", "max_query_batches": 2,
            "max_tool_calls": 30, "max_candidates": 20, "max_full_sources": 5,
            "max_evidence_spans": 12, "max_subagents": 1, "max_output_words": 1500,
            "stop_rule": "Stop when critical claims are supported, contested, or explicitly unresolved and marginal evidence gain is low."
        }
    })
    dump_data(root / "sources" / "manifests" / "sources.yaml", {"sources": []})
    dump_data(root / "evidence" / "spans" / "spans.yaml", {"spans": []})
    dump_data(root / "evidence" / "cards" / "cards.yaml", {"cards": []})
    dump_data(root / "relations" / "candidates.yaml", {"links": []})
    dump_data(root / "claims" / "claims.yaml", {"claims": []})
    dump_data(root / "decisions" / "records.yaml", {"decisions": []})
    (root / "queries" / "ledger.jsonl").touch()
    (root / "events" / "events.jsonl").touch()
    (root / "research" / "handoff.yaml").write_text("{}\n", encoding="utf-8")


def copy_claude_harness(destination: Path) -> None:
    source_root = package_root()
    if not (source_root / "CLAUDE.md").is_file():
        source_root = Path(__file__).resolve().parent / "templates"
    required = ["CLAUDE.md", ".claude", "config", ".mcp.json.example", ".env.example"]
    missing = [item for item in required if not (source_root / item).exists()]
    if missing:
        raise FileNotFoundError(
            f"packaged Claude harness is incomplete; missing: {', '.join(missing)}"
        )
    for item in required:
        src = source_root / item
        dst = destination / item
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
