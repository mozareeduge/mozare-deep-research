#!/usr/bin/env python3
from __future__ import annotations

import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / f"{ROOT.name}-v1.0.0.zip"
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "htmlcov", "build", "dist", ".tox", ".nox"}
SKIP_SUFFIXES = {".pyc", ".pyo"}
SKIP_FILES = {OUT.name, ".coverage"}


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return (
        any(part in SKIP_DIRS or part.endswith(".egg-info") for part in rel.parts)
        or path.suffix in SKIP_SUFFIXES
        or path.name in SKIP_FILES
    )


with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or should_skip(path):
            continue
        arcname = Path(ROOT.name) / path.relative_to(ROOT)
        info = zipfile.ZipInfo.from_file(path, arcname=str(arcname))
        # Reproducible permission bits; timestamps remain source timestamps for useful provenance.
        info.external_attr = (0o755 if os.access(path, os.X_OK) else 0o644) << 16
        archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
print(OUT)
