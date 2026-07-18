#!/usr/bin/env python3
"""Mirror or verify the Claude harness included as wheel package data."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src" / "mros" / "templates"
NAMES = ("CLAUDE.md", ".claude", "config", ".mcp.json.example", ".env.example")


def files_under(path: Path) -> dict[Path, bytes]:
    if path.is_file():
        return {Path(path.name): path.read_bytes()}
    return {
        item.relative_to(path): item.read_bytes()
        for item in path.rglob("*")
        if item.is_file() and "__pycache__" not in item.parts and item.suffix not in {".pyc", ".pyo"}
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when the packaged mirror is stale")
    args = parser.parse_args()
    if args.check:
        issues: list[str] = []
        for name in NAMES:
            source = ROOT / name
            destination = TARGET / name
            if not destination.exists() or files_under(source) != files_under(destination):
                issues.append(f"stale packaged harness: {name}")
        if issues:
            print("\n".join(issues))
            return 1
        print("Packaged Claude harness is current")
        return 0

    if TARGET.exists():
        shutil.rmtree(TARGET)
    TARGET.mkdir(parents=True)
    for name in NAMES:
        source = ROOT / name
        destination = TARGET / name
        if source.is_dir():
            shutil.copytree(
                source,
                destination,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
            )
        else:
            shutil.copy2(source, destination)
    print(TARGET)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
