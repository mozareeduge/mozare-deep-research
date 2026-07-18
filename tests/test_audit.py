from pathlib import Path

import yaml

from mros.audit import audit_project
from mros.io import dump_data


def test_empty_initialized_project_passes_structural_audit(project: Path):
    report = audit_project(project)
    assert report.ok
    assert report.blockers == []


def test_release_audit_requires_release_artifact(project: Path):
    report = audit_project(project, release_mode=True)
    assert not report.ok
    assert any(issue.code == "missing_release" for issue in report.blockers)


def test_release_audit_rejects_placeholders(project: Path):
    release = project / "releases/report.md"
    release.write_text("A final sentence. TODO", encoding="utf-8")
    report = audit_project(project, release_mode=True)
    assert any(issue.code == "unresolved_placeholder" for issue in report.blockers)


def test_release_audit_accepts_clean_artifact(project: Path):
    (project / "releases/report.md").write_text("A verified release.", encoding="utf-8")
    assert audit_project(project, release_mode=True).ok


def test_audit_detects_orphan_span(project: Path):
    dump_data(project / "evidence/spans/spans.yaml", {"spans": [{
        "span_id": "sp.01",
        "source_id": "src.missing",
        "file_path": "x.txt",
        "exact_text": "evidence",
        "quote_validation": "accepted",
    }]})
    report = audit_project(project)
    assert any(issue.code == "orphan_span" for issue in report.blockers)


def test_audit_blocks_generated_source_upgrade(project: Path):
    dump_data(project / "sources/manifests/sources.yaml", {"sources": [{
        "source_id": "src.01", "title": "Generated", "kind": "generated",
        "access_status": "generated", "allowed_uses": ["discovery"]
    }]})
    dump_data(project / "evidence/spans/spans.yaml", {"spans": [{
        "span_id": "sp.01", "source_id": "src.01", "file_path": "x.txt",
        "exact_text": "evidence", "quote_validation": "accepted"
    }]})
    dump_data(project / "evidence/cards/cards.yaml", {"cards": [{
        "evidence_id": "ev.01", "span_ids": ["sp.01"], "proposition": "P",
        "role": "support", "directness": "direct", "review_status": "accepted",
        "reviewer": "human", "allowed_uses": ["internal_synthesis"]
    }]})
    report = audit_project(project)
    assert any(issue.code == "generated_evidence_upgrade" for issue in report.blockers)


def test_invalid_yaml_is_reported_as_blocker(project: Path):
    (project / "research/questions.yaml").write_text("questions: [", encoding="utf-8")
    report = audit_project(project)
    assert any(issue.code == "invalid_schema" for issue in report.blockers)


def test_audit_detects_state_event_hash_mismatch(project: Path):
    state_path = project / "research/state.yaml"
    state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
    state["last_event_hash"] = "0" * 64
    dump_data(state_path, state)
    report = audit_project(project)
    assert any(issue.code == "state_event_hash_mismatch" for issue in report.blockers)


def test_invalid_event_jsonl_is_reported_as_blocker(project: Path):
    (project / "events/events.jsonl").write_text("not-json\n", encoding="utf-8")
    report = audit_project(project)
    assert any(issue.code == "invalid_event_ledger" for issue in report.blockers)
