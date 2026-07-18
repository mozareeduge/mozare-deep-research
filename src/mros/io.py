from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, TypeVar

import yaml
from pydantic import BaseModel

from .locking import file_lock

T = TypeVar("T", bound=BaseModel)


def load_data(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    raise ValueError(f"Unsupported data file: {path}")


def _serializable(data: Any) -> Any:
    if isinstance(data, BaseModel):
        return data.model_dump(mode="json", exclude_none=True)
    if isinstance(data, list):
        return [
            x.model_dump(mode="json", exclude_none=True) if isinstance(x, BaseModel) else x
            for x in data
        ]
    return data


def _render(path: Path, data: Any) -> str:
    data = _serializable(data)
    if path.suffix.lower() == ".json":
        return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    raise ValueError(f"Unsupported data file: {path}")


def dump_data(path: Path, data: Any) -> None:
    """Atomically replace a JSON/YAML record under a cross-platform lock file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    text = _render(path, data)
    with file_lock(path):
        fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        tmp = Path(tmp_name)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, path)
        finally:
            tmp.unlink(missing_ok=True)


def load_model(path: Path, model: type[T]) -> T:
    return model.model_validate(load_data(path))


def load_model_list(path: Path, key: str, model: type[T]) -> list[T]:
    raw = load_data(path) or {}
    values = raw.get(key, []) if isinstance(raw, dict) else raw
    return [model.model_validate(v) for v in values]


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
    with file_lock(path):
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line)
            handle.flush()
            os.fsync(handle.fileno())


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
    return rows
