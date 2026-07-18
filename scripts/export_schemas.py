#!/usr/bin/env python3
"""Export or verify stable JSON Schemas for every public MROS record type."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mros.models import (  # noqa: E402
    AuditReport,
    CandidateLink,
    ClaimRecord,
    DesignDecision,
    EventRecord,
    EvidenceCard,
    EvidenceSpan,
    HandoffReceipt,
    QueryRecord,
    ResearchContract,
    ResearchQuestion,
    RunState,
    SourceRecord,
)

MODELS = {
    "research-contract": ResearchContract,
    "research-question": ResearchQuestion,
    "source-record": SourceRecord,
    "query-record": QueryRecord,
    "evidence-span": EvidenceSpan,
    "evidence-card": EvidenceCard,
    "candidate-link": CandidateLink,
    "claim-record": ClaimRecord,
    "design-decision": DesignDecision,
    "event-record": EventRecord,
    "handoff-receipt": HandoffReceipt,
    "run-state": RunState,
    "audit-report": AuditReport,
}


def render_schema(name: str, model: type) -> str:
    schema = model.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = f"https://mros.local/schemas/{name}.schema.json"
    return json.dumps(schema, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when committed schemas are stale")
    args = parser.parse_args()
    target = ROOT / "config" / "schemas"
    target.mkdir(parents=True, exist_ok=True)
    stale: list[str] = []
    expected_names = {f"{name}.schema.json" for name in MODELS}
    actual_names = {path.name for path in target.glob("*.schema.json")}
    for extra in sorted(actual_names - expected_names):
        stale.append(f"unexpected schema: {extra}")
    for name, model in MODELS.items():
        path = target / f"{name}.schema.json"
        expected = render_schema(name, model)
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                stale.append(f"stale schema: {path.name}")
        else:
            path.write_text(expected, encoding="utf-8")
    if stale:
        print(json.dumps({"ok": False, "issues": stale}, indent=2))
        return 1
    print(json.dumps({"ok": True, "schemas": len(MODELS), "target": str(target), "check": args.check}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
