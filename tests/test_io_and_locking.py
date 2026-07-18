from __future__ import annotations

import json
import threading
import time
from pathlib import Path

import pytest

from mros.events import append_event, verify_event_chain
from mros.io import append_jsonl, dump_data, load_data, read_jsonl
from mros.locking import LockTimeout, file_lock
from mros.models import EventRecord


def test_dump_data_atomically_replaces_yaml(tmp_path: Path):
    path = tmp_path / "state.yaml"
    dump_data(path, {"version": 1, "items": ["a"]})
    dump_data(path, {"version": 2, "items": ["b"]})
    assert load_data(path) == {"version": 2, "items": ["b"]}
    assert not list(tmp_path.glob(".state.yaml.*"))
    assert not (tmp_path / "state.yaml.lock").exists()


def test_append_jsonl_serializes_concurrent_writers(tmp_path: Path):
    path = tmp_path / "ledger.jsonl"
    threads = [
        threading.Thread(target=append_jsonl, args=(path, {"id": i}))
        for i in range(12)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    rows = read_jsonl(path)
    assert sorted(row["id"] for row in rows) == list(range(12))


def test_event_append_is_chain_safe_for_concurrent_writers(tmp_path: Path):
    path = tmp_path / "events.jsonl"
    errors: list[Exception] = []

    def worker(index: int) -> None:
        try:
            append_event(
                path,
                EventRecord(event_id=f"event.{index:02d}", actor="test", action="append"),
            )
        except Exception as exc:  # pragma: no cover - failure diagnostics
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert errors == []
    assert len(read_jsonl(path)) == 10
    assert verify_event_chain(path) == []


def test_file_lock_times_out_when_live_lock_exists(tmp_path: Path):
    target = tmp_path / "record.yaml"
    with file_lock(target):
        with pytest.raises(LockTimeout):
            with file_lock(target, timeout=0.05, stale_after=60):
                pass


def test_file_lock_recovers_stale_lock(tmp_path: Path):
    target = tmp_path / "record.yaml"
    lock = tmp_path / "record.yaml.lock"
    lock.write_text("stale", encoding="utf-8")
    old = time.time() - 100
    import os

    os.utime(lock, (old, old))
    with file_lock(target, timeout=0.2, stale_after=1):
        assert lock.exists()
    assert not lock.exists()


def test_read_jsonl_reports_line_number(tmp_path: Path):
    path = tmp_path / "broken.jsonl"
    path.write_text(json.dumps({"ok": 1}) + "\nnot json\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r":2:"):
        read_jsonl(path)
