from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def test_claude_settings_are_valid_and_bounded():
    settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
    assert settings["model"] == "sonnet"
    assert settings["effortLevel"] == "medium"
    assert "Stop" in settings["hooks"]
    assert all("rm -rf" not in allowed for allowed in settings["permissions"]["allow"])
    stop_command = settings["hooks"]["Stop"][0]["hooks"][0]["command"]
    assert stop_command == "mros-stop-gate"
    hook_text = (ROOT / "scripts/hooks/stop_gate.py").read_text(encoding="utf-8")
    assert '"--phase-stop"' not in hook_text


def test_all_skills_have_supported_core_frontmatter():
    allowed = {
        "name",
        "description",
        "model",
        "effort",
        "allowed-tools",
        "disable-model-invocation",
        "context",
        "agent",
        "user-invocable",
    }
    skills = sorted((ROOT / ".claude/skills").glob("*/SKILL.md"))
    assert len(skills) >= 10
    for skill in skills:
        text = skill.read_text(encoding="utf-8")
        assert text.startswith("---\n"), skill
        front = text.split("---", 2)[1]
        data = yaml.safe_load(front)
        expected_name = skill.parent.name
        assert data.get("name") == expected_name
        assert SKILL_NAME_RE.fullmatch(expected_name)
        assert len(expected_name) <= 64
        assert data.get("description")
        assert set(data).issubset(allowed), (skill, set(data) - allowed)
        assert data.get("effort") in {"low", "medium", "high"}
        assert isinstance(data.get("allowed-tools"), list)


def test_all_agents_are_bounded_and_supported():
    allowed = {
        "name",
        "description",
        "tools",
        "disallowedTools",
        "model",
        "permissionMode",
        "maxTurns",
        "skills",
        "mcpServers",
        "hooks",
        "memory",
        "background",
        "effort",
        "isolation",
        "color",
    }
    agents = sorted((ROOT / ".claude/agents").glob("*.md"))
    assert agents
    for agent in agents:
        text = agent.read_text(encoding="utf-8")
        data = yaml.safe_load(text.split("---", 2)[1])
        assert set(data).issubset(allowed), (agent, set(data) - allowed)
        assert data.get("name") == agent.stem
        assert data.get("model") in {"haiku", "sonnet", "opus"}
        assert data.get("effort") in {"low", "medium", "high"}
        assert 0 < int(data.get("maxTurns", 0)) <= 12
        assert isinstance(data.get("tools"), str)
        assert "Write" not in data.get("tools", "") or data["name"] == "source-screener"


def test_exported_schemas_are_complete_and_valid_json():
    expected = {
        "audit-report",
        "candidate-link",
        "claim-record",
        "design-decision",
        "event-record",
        "evidence-card",
        "evidence-span",
        "handoff-receipt",
        "query-record",
        "research-contract",
        "research-question",
        "run-state",
        "source-record",
    }
    schema_dir = ROOT / "config/schemas"
    found = {p.name.removesuffix(".schema.json") for p in schema_dir.glob("*.schema.json")}
    assert found == expected
    for path in schema_dir.glob("*.schema.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert data["$id"].endswith(path.name)
        assert data["type"] == "object"


def test_mcp_example_contains_no_literal_secrets():
    text = (ROOT / ".mcp.json.example").read_text(encoding="utf-8")
    assert "sk-" not in text
    assert "${" in text


def test_no_empty_claim_of_live_integration_certification():
    limitations = (ROOT / "docs/limitations.md").read_text(encoding="utf-8").lower()
    assert "live" in limitations
    assert "not executed" in limitations
    assert (ROOT / "docs/live-certification.md").exists()


def test_release_contains_no_placeholder_markers():
    release_files = [p for p in (ROOT / "releases").glob("*") if p.is_file() and p.name != ".gitkeep"]
    assert release_files
    forbidden = re.compile(r"\b(?:TODO|TBD|FIXME|CITATION NEEDED)\b|\?\?\?", re.I)
    for path in release_files:
        assert not forbidden.search(path.read_text(encoding="utf-8")), path


def test_packaged_harness_mirror_matches_source():
    mirror = ROOT / "src/mros/templates"
    for name in ["CLAUDE.md", ".claude", "config", ".mcp.json.example", ".env.example"]:
        source = ROOT / name
        target = mirror / name
        assert target.exists()
        if source.is_file():
            assert source.read_bytes() == target.read_bytes()
        else:
            source_files = {
                p.relative_to(source): p.read_bytes()
                for p in source.rglob("*")
                if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
            }
            target_files = {
                p.relative_to(target): p.read_bytes()
                for p in target.rglob("*")
                if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
            }
            assert target_files == source_files


def test_zotero_permissions_are_explicitly_read_only():
    settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
    allowed = set(settings["permissions"]["allow"])
    assert "mcp__zotero__*" not in allowed
    forbidden_fragments = {
        "create",
        "update",
        "delete",
        "trash",
        "merge",
        "add_",
        "remove_",
        "write",
    }
    zotero_allowed = {item for item in allowed if item.startswith("mcp__zotero__")}
    assert zotero_allowed
    for item in zotero_allowed:
        assert not any(fragment in item for fragment in forbidden_fragments), item


def test_mcp_example_pins_audited_distributions():
    data = json.loads((ROOT / ".mcp.json.example").read_text(encoding="utf-8"))
    academic = data["mcpServers"]["academic_tools"]
    zotero = data["mcpServers"]["zotero"]
    assert academic["args"] == ["academic-tools-mcp==2026.6.4"]
    assert zotero["args"] == ["--from", "zotero-mcp-server==0.6.2", "zotero-mcp"]
