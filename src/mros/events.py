from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from .io import read_jsonl
from .locking import file_lock
from .models import EventRecord


def _canonical_event_payload(data: dict[str, Any]) -> bytes:
    payload = {k: v for k, v in data.items() if k != "event_hash"}
    payload.setdefault("previous_hash", None)
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def compute_event_hash(event: EventRecord | dict[str, Any]) -> str:
    data = (
        event.model_dump(mode="json", exclude_none=True)
        if isinstance(event, EventRecord)
        else dict(event)
    )
    return hashlib.sha256(_canonical_event_payload(data)).hexdigest()


def append_event(path: Path, event: EventRecord) -> EventRecord:
    """Append one event while holding a lock across predecessor lookup and write."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with file_lock(path):
        rows = read_jsonl(path)
        previous = rows[-1].get("event_hash") if rows else None
        data = event.model_dump(mode="json", exclude_none=True)
        data["previous_hash"] = previous
        data["event_hash"] = compute_event_hash(data)
        finalized = EventRecord.model_validate(data)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    finalized.model_dump(mode="json", exclude_none=True),
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )
            handle.flush()
            os.fsync(handle.fileno())
    return finalized


def verify_event_chain(path: Path) -> list[str]:
    issues: list[str] = []
    previous: str | None = None
    seen_ids: set[str] = set()
    for index, row in enumerate(read_jsonl(path), 1):
        try:
            record = EventRecord.model_validate(row)
        except Exception as exc:
            issues.append(f"event {index} is invalid: {exc}")
            continue
        if record.event_id in seen_ids:
            issues.append(f"event {index} duplicates event_id {record.event_id}")
        seen_ids.add(record.event_id)
        if row.get("previous_hash") != previous:
            issues.append(f"event {index} previous_hash mismatch")
        expected = compute_event_hash(row)
        if row.get("event_hash") != expected:
            issues.append(f"event {index} event_hash mismatch")
        previous = row.get("event_hash")
    return issues
