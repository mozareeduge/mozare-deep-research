#!/usr/bin/env python3
from __future__ import annotations

import os
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
RELEASE_NAME = "mozare-research-os"
OUT = ROOT.parent / f"{RELEASE_NAME}-v{VERSION}.zip"
SKIP_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", "htmlcov", "build", "dist", ".tox", ".nox", ".claude/worktrees",
}
SKIP_SUFFIXES = {".pyc", ".pyo"}
SKIP_FILES = {OUT.name, ".coverage", ".mcp.json", "settings.local.json"}
SKIP_PARTS = {"secrets"}


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return (
        any(part in SKIP_DIRS or part.endswith(".egg-info") for part in rel.parts)
        or any(part in SKIP_PARTS for part in rel.parts)
        or path.suffix in SKIP_SUFFIXES
        or path.name in SKIP_FILES
        or (path.name.startswith(".env") and path.name != ".env.example")
    )


with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or should_skip(path):
            continue
        arcname = Path(RELEASE_NAME) / path.relative_to(ROOT)
        info = zipfile.ZipInfo.from_file(path, arcname=str(arcname))
        info.external_attr = (0o755 if os.access(path, os.X_OK) else 0o644) << 16
        archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
print(OUT)
