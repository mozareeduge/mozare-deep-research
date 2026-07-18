import json
from pathlib import Path

from mros.events import append_event, verify_event_chain
from mros.models import EventRecord


def test_event_chain_round_trip(tmp_path: Path):
    path = tmp_path / "events.jsonl"
    first = append_event(path, EventRecord(event_id="event.01", actor="human", action="frame"))
    second = append_event(path, EventRecord(event_id="event.02", actor="tool", action="validate"))
    assert first.previous_hash is None
    assert second.previous_hash == first.event_hash
    assert verify_event_chain(path) == []


def test_event_chain_detects_tampering(tmp_path: Path):
    path = tmp_path / "events.jsonl"
    append_event(path, EventRecord(event_id="event.01", actor="human", action="frame"))
    row = json.loads(path.read_text(encoding="utf-8"))
    row["action"] = "tampered"
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")
    assert any("event_hash mismatch" in issue for issue in verify_event_chain(path))


def test_empty_event_log_is_valid(tmp_path: Path):
    assert verify_event_chain(tmp_path / "missing.jsonl") == []
