"""Claude Code hook entry points installed with the MROS package."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

from .verify import verify_project


def session_context_main() -> None:
    root = Path.cwd()
    parts = ["MROS session context:"]

    runs_root = root / "research" / "runs"
    active_runs: list[tuple[float, dict[str, object]]] = []
    if runs_root.exists():
        for candidate in runs_root.glob("*/state.yaml"):
            try:
                data = yaml.safe_load(candidate.read_text(encoding="utf-8")) or {}
                if data.get("status") in {"active", "needs_input", "blocked"}:
                    active_runs.append((candidate.stat().st_mtime, data))
            except Exception:
                continue

    if active_runs:
        _, active = max(active_runs, key=lambda item: item[0])
        parts.append(
            f"- active run: {active.get('run_id', 'unknown')} "
            f"[{active.get('output_profile', 'research-note')}] "
            f"({active.get('current_stage', 'unknown')})"
        )
        if active.get("user_visible_status"):
            parts.append(f"- status: {active['user_visible_status']}")
        next_actions = list(active.get("next_actions", []))[:2]
        if next_actions:
            parts.append("- next: " + " | ".join(str(x) for x in next_actions))
        open_questions = list(active.get("open_questions", []))[:2]
        if open_questions:
            parts.append("- unresolved: " + " | ".join(str(x) for x in open_questions))
    else:
        parts.append("- active run: none")
        parts.append("- next actions: start substantive research from the user's ordinary-language request")

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
