from __future__ import annotations

from pathlib import Path

import yaml

KERNEL_HEADER = "# MROS operational kernel\n\n"


def load_method_config(root: Path) -> dict:
    path = root / "config" / "methodology.yaml"
    if not path.exists():
        raise FileNotFoundError(path)
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def render_kernel(config: dict) -> str:
    lines = [KERNEL_HEADER.rstrip(), ""]
    for index, invariant in enumerate(config.get("invariants", []), 1):
        lines.append(f"{index}. {invariant['operational_rule']}")
    lines.extend(["", "This kernel is intentionally compact. Load detailed procedures through phase skills.", ""])
    return "\n".join(lines)


def compile_method(root: Path) -> Path:
    config = load_method_config(root)
    out_dir = root / ".mros" / "compiled"
    out_dir.mkdir(parents=True, exist_ok=True)
    kernel_path = out_dir / "kernel.md"
    kernel = render_kernel(config)
    kernel_path.write_text(kernel, encoding="utf-8")
    profiles = config.get("run_profiles", {})
    profile_dir = out_dir / "run-profiles"
    profile_dir.mkdir(parents=True, exist_ok=True)
    for name, profile in profiles.items():
        text = f"# {name}\n\nPurpose: {profile['purpose']}\n\nRequired outputs:\n"
        text += "\n".join(f"- {item}" for item in profile.get("outputs", [])) + "\n"
        (profile_dir / f"{name}.md").write_text(text, encoding="utf-8")
    return kernel_path


def check_operational_language(root: Path) -> list[str]:
    config = load_method_config(root)
    prohibited = [term.lower() for term in config.get("prohibited_default_terms", [])]
    issues: list[str] = []
    paths = [root / "CLAUDE.md", *(root / ".claude" / "skills").glob("*/SKILL.md"), *(root / ".claude" / "agents").glob("*.md")]
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for term in prohibited:
            if term in text:
                issues.append(f"{path.relative_to(root)} contains prohibited default term: {term}")
    return issues
