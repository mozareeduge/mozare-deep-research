"""Normalization helpers for Academic Tools MCP results."""

from __future__ import annotations

from typing import Any

from .base import CandidateSource
from ..identifiers import normalize_arxiv, normalize_doi


def normalize_result(result: dict[str, Any], provider: str) -> CandidateSource:
    title = str(result.get("title") or result.get("display_name") or "Untitled")
    creators = result.get("authors") or result.get("creators") or []
    if creators and isinstance(creators[0], dict):
        creators = [str(x.get("name") or x.get("display_name") or "") for x in creators]
    doi = normalize_doi(str(result.get("doi") or ""))
    arxiv = normalize_arxiv(str(result.get("arxiv_id") or result.get("id") or ""))
    identifiers = {k: v for k, v in {"doi": doi, "arxiv": arxiv}.items() if v}
    external_id = doi or arxiv or str(result.get("id") or result.get("url") or title)
    return CandidateSource(
        external_id=external_id,
        title=title,
        creators=[x for x in creators if x],
        date=str(result.get("year") or result.get("date") or "") or None,
        identifiers=identifiers,
        provider=provider,
        abstract=result.get("abstract"),
        url=result.get("url") or result.get("landing_page_url"),
        raw=result,
    )
