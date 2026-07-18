#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mros.verify import verify_project  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-stop", action="store_true")
    args = parser.parse_args()
    result = verify_project(ROOT, phase_stop=args.phase_stop)
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
