from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from mros.project import init_project


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str, cwd: Path = ROOT):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, "-m", "mros", *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_init_creates_complete_workspace(tmp_path: Path):
    target = tmp_path / "new"
    result = run_cli("init", str(target), "--project-id", "new-project", "--title", "New Project")
    assert result.returncode == 0, result.stderr
    assert (target / "research/contract.yaml").exists()
    assert (target / "events/events.jsonl").exists()


def test_init_refuses_to_overwrite_without_force(tmp_path: Path):
    target = tmp_path / "new"
    init_project(target, "new-project", "New Project")
    result = run_cli("init", str(target), "--project-id", "new-project", "--title", "New Project")
    assert result.returncode == 2
    assert "already exists" in result.stderr


def test_validate_command_passes_initialized_project(project: Path):
    result = run_cli("validate", str(project))
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["issues"] == []


def test_quote_verify_command_exit_status(tmp_path: Path):
    source = tmp_path / "source.txt"
    source.write_text("some evidence", encoding="utf-8")
    good = run_cli("quote-verify", str(source), "--text", "evidence")
    bad = run_cli("quote-verify", str(source), "--text", "absent")
    assert good.returncode == 0
    assert bad.returncode == 1


def test_event_cli_appends_and_verifies(project: Path):
    append = run_cli("event-append", str(project), "--event-id", "event.01", "--actor", "human", "--action", "approve")
    verify = run_cli("event-verify", str(project))
    assert append.returncode == 0, append.stderr
    assert verify.returncode == 0, verify.stderr


def test_handoff_cli_writes_required_receipt(project: Path):
    result = run_cli(
        "handoff", str(project),
        "--objective", "Completed a bounded phase",
        "--changed", "research/state.yaml",
        "--verification", "mros validate passed",
        "--next", "Start next phase",
    )
    assert result.returncode == 0, result.stderr
    text = (project / "research/handoff.yaml").read_text(encoding="utf-8")
    assert "Completed a bounded phase" in text


def test_doctor_reports_optional_paperqa_without_failing(project: Path):
    # copy minimum harness files that doctor treats as core
    (project / "CLAUDE.md").write_text("# Rules", encoding="utf-8")
    (project / ".claude").mkdir(exist_ok=True)
    (project / ".claude/settings.json").write_text("{}", encoding="utf-8")
    (project / "config").mkdir(exist_ok=True)
    (project / "config/methodology.yaml").write_text("invariants: []", encoding="utf-8")
    result = run_cli("doctor", str(project))
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["project_marker"] is True
    assert "paperqa_optional" in payload


def test_run_cli_lifecycle(tmp_path: Path):
    run = tmp_path / "semantic-run"
    run.mkdir()
    (run / "request.md").write_text("Research a concept deeply.", encoding="utf-8")
    init = run_cli("run-init", str(run), "--mode", "deep", "--source-lane", "web")
    assert init.returncode == 0, init.stderr
    status = run_cli("run-state", str(run), "--stage", "discovery", "--next", "Search first bounded batch")
    assert status.returncode == 0, status.stderr
    validate = run_cli("run-validate", str(run))
    assert validate.returncode == 0, validate.stderr
    payload = json.loads(validate.stdout)
    assert payload["mode"] == "deep"
    assert payload["status"] == "active"


def test_cli_run_append_accepts_inline_json(tmp_path: Path):
    project = tmp_path / "inline-run"
    project.mkdir()
    (project / "request.md").write_text("A bounded question.", encoding="utf-8")
    initialized = run_cli("run-init", str(project), "--mode", "brief")
    assert initialized.returncode == 0, initialized.stderr
    payload = '{"source_id":"source.inline","title":"Inline source","source_type":"article","lane":"web"}'
    appended = run_cli("run-append", str(project), "--kind", "source", "--json", payload)
    assert appended.returncode == 0, appended.stderr
    assert "source.inline" in appended.stdout


def test_event_cli_updates_state_hash(project: Path):
    result = run_cli(
        "event-append", str(project), "--event-id", "event.state-sync",
        "--actor", "test", "--action", "sync-state"
    )
    assert result.returncode == 0, result.stderr
    event = json.loads(result.stdout)
    import yaml
    state = yaml.safe_load((project / "research/state.yaml").read_text(encoding="utf-8"))
    assert state["last_event_hash"] == event["event_hash"]
