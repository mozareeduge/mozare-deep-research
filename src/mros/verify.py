"""Repository verification shared by CLI, hooks, and development scripts."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from .audit import audit_project
from .method import check_operational_language, compile_method


def verify_project(
    root: Path, *, phase_stop: bool = False, development_checks: bool = True
) -> dict[str, Any]:
    root = root.resolve()
    issues: list[str] = []

    try:
        compile_method(root)
    except Exception as exc:
        issues.append(f"method compilation failed: {exc}")
    try:
        issues.extend(check_operational_language(root))
    except Exception as exc:
        issues.append(f"operational language check failed: {exc}")

    # Development-repository invariants are checked only by explicit CLI/build verification.
    development_commands = [
        (root / "scripts/export_schemas.py", [sys.executable, "scripts/export_schemas.py", "--check"], "exported schemas are stale"),
        (root / "scripts/sync_templates.py", [sys.executable, "scripts/sync_templates.py", "--check"], "packaged Claude harness is stale"),
    ]
    if development_checks:
        for marker, command, failure in development_commands:
            if not marker.is_file():
                continue
            proc = subprocess.run(command, cwd=root, text=True, capture_output=True)
            if proc.returncode:
                detail = (proc.stdout + "\n" + proc.stderr).strip()
                issues.append(f"{failure}: {detail}")

    if development_checks and (root / "src/mros").is_dir() and (root / "tests").is_dir():
        proc = subprocess.run(
            [sys.executable, "-m", "compileall", "-q", "src", "tests", "scripts"],
            cwd=root,
            text=True,
            capture_output=True,
        )
        if proc.returncode:
            issues.append("python compileall failed: " + (proc.stdout + proc.stderr).strip())

    report = audit_project(root, release_mode=False)
    issues.extend(f"{item.code}: {item.message}" for item in report.blockers)

    if phase_stop:
        handoff = root / "research/handoff.yaml"
        try:
            data = yaml.safe_load(handoff.read_text(encoding="utf-8")) or {}
            if not data.get("objective_completed"):
                issues.append("research/handoff.yaml has no objective_completed")
            if not data.get("verification"):
                issues.append("research/handoff.yaml has no verification evidence")
        except Exception as exc:
            issues.append(f"handoff receipt invalid: {exc}")

    return {
        "ok": not issues,
        "phase_stop": phase_stop,
        "audit_warnings": len(report.warnings),
        "development_checks": development_checks,
        "issues": issues,
    }
