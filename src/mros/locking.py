"""Small cross-platform lock-file primitive for single-writer project records."""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


class LockTimeout(TimeoutError):
    pass


@contextmanager
def file_lock(target: Path, *, timeout: float = 10.0, stale_after: float = 300.0) -> Iterator[None]:
    lock = target.with_name(target.name + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(f"pid={os.getpid()}\ncreated={time.time()}\n")
                handle.flush()
                os.fsync(handle.fileno())
            break
        except FileExistsError:
            try:
                age = time.time() - lock.stat().st_mtime
                if age > stale_after:
                    lock.unlink(missing_ok=True)
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() >= deadline:
                raise LockTimeout(f"timed out waiting for lock {lock}")
            time.sleep(0.05)
    try:
        yield
    finally:
        lock.unlink(missing_ok=True)
