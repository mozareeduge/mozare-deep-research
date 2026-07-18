"""Claude Code hook entry points installed with the MROS package."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

from .verify import verify_project


def session_context_main() -> None:
    root = Path.cwd()
    state_path = root / "research/state.yaml"
    handoff_path = root / "research/handoff.yaml"
    parts = ["MROS session context:"]
    if state_path.exists():
        state = yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}
        parts.append(f"- phase: {state.get('phase', 'unknown')}")
        parts.append(
            f"- active questions: {', '.join(state.get('active_question_ids', [])) or 'none'}"
        )
        parts.append(f"- blockers: {len(state.get('blockers', []))}")
        next_actions = state.get("next_actions", [])[:3]
        if next_actions:
            parts.append("- next actions: " + " | ".join(next_actions))
    if handoff_path.exists():
        handoff = yaml.safe_load(handoff_path.read_text(encoding="utf-8")) or {}
        if handoff.get("objective_completed"):
            parts.append(f"- last objective: {handoff['objective_completed']}")
    print("\n".join(parts))


def stop_gate_main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    if payload.get("stop_hook_active"):
        print("{}")
        return
    result = verify_project(Path.cwd(), phase_stop=False, development_checks=False)
    if result["ok"]:
        print("{}")
        return
    reason = "\n".join(str(item) for item in result["issues"])[-8000:]
    print(
        json.dumps(
            {
                "decision": "block",
                "reason": "MROS repository verification failed. Fix the following before stopping:\n"
                + reason,
            }
        )
    )
