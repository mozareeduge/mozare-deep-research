from __future__ import annotations

import io
import json
from pathlib import Path

from mros.hooks import session_context_main, stop_gate_main
from mros.project import copy_claude_harness
from mros.verify import verify_project


def test_verify_project_passes_initialized_workspace(project: Path):
    copy_claude_harness(project)
    result = verify_project(project, development_checks=False)
    assert result["ok"] is True
    assert result["development_checks"] is False


def test_phase_stop_requires_completed_handoff(project: Path):
    copy_claude_harness(project)
    result = verify_project(project, phase_stop=True, development_checks=False)
    assert result["ok"] is False
    assert any("objective_completed" in issue for issue in result["issues"])


def test_session_context_reports_compact_state(project: Path, monkeypatch, capsys):
    monkeypatch.chdir(project)
    session_context_main()
    text = capsys.readouterr().out
    assert "MROS session context" in text
    assert "phase: frame" in text
    assert "next actions" in text


def test_stop_gate_allows_valid_repository(project: Path, monkeypatch, capsys):
    copy_claude_harness(project)
    monkeypatch.chdir(project)
    monkeypatch.setattr("sys.stdin", io.StringIO("{}"))
    stop_gate_main()
    assert capsys.readouterr().out.strip() == "{}"


def test_stop_gate_blocks_invalid_repository(project: Path, monkeypatch, capsys):
    copy_claude_harness(project)
    (project / "research/contract.yaml").write_text("bad: schema\n", encoding="utf-8")
    monkeypatch.chdir(project)
    monkeypatch.setattr("sys.stdin", io.StringIO("{}"))
    stop_gate_main()
    payload = json.loads(capsys.readouterr().out)
    assert payload["decision"] == "block"
    assert "invalid_contract" in payload["reason"]


def test_stop_gate_avoids_recursive_block(project: Path, monkeypatch, capsys):
    copy_claude_harness(project)
    monkeypatch.chdir(project)
    monkeypatch.setattr("sys.stdin", io.StringIO('{"stop_hook_active": true}'))
    stop_gate_main()
    assert capsys.readouterr().out.strip() == "{}"
