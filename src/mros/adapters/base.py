from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class CandidateSource:
    external_id: str
    title: str
    creators: list[str] = field(default_factory=list)
    date: str | None = None
    identifiers: dict[str, str] = field(default_factory=dict)
    provider: str = "unknown"
    abstract: str | None = None
    url: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class CandidatePassage:
    source_external_id: str
    text: str
    page: int | None = None
    section: str | None = None
    score: float | None = None
    provider: str = "unknown"
    raw: dict[str, Any] = field(default_factory=dict)


class DiscoveryAdapter(Protocol):
    name: str

    def search(self, query: str, limit: int = 20) -> list[CandidateSource]: ...


class PassageAdapter(Protocol):
    name: str

    def retrieve(self, query: str, source_ids: list[str] | None = None, limit: int = 20) -> list[CandidatePassage]: ...
