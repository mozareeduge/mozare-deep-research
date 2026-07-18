"""Optional, retrieval-only PaperQA2 adapter.

MROS intentionally bypasses PaperQA's answer agent and per-passage LLM summaries.  It uses
PaperQA only to parse/index an accepted local corpus and return candidate chunks.  Every
returned chunk remains a candidate until MROS validates its location and qualifies it as
source evidence.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Iterable

from .base import CandidatePassage


class PaperQANotInstalled(RuntimeError):
    """Raised when the optional PaperQA integration is requested but unavailable."""


class PaperQAContractError(RuntimeError):
    """Raised when an installed PaperQA version lacks the APIs MROS relies on."""


def available() -> bool:
    try:
        import paperqa  # noqa: F401
    except ImportError:
        return False
    return True


def recommended_settings() -> dict[str, Any]:
    """Return the no-agent/no-enrichment policy used by MROS.

    This is a serializable policy record as well as documentation.  ``make_settings`` applies
    the supported fields to a live PaperQA Settings object.
    """

    return {
        "answer": {
            "evidence_k": 12,
            "evidence_skip_summary": True,
            "answer_max_sources": 5,
            "max_concurrent_requests": 1,
            "answer_filter_extra_background": False,
            "get_evidence_if_no_contexts": False,
        },
        "parsing": {
            "use_doc_details": False,
            "reader_config": {"chunk_chars": 3500, "overlap": 250},
            "multimodal": "on_without_enrichment",
        },
        "policy": {
            "agent_answering": False,
            "llm_metadata_inference": False,
            "llm_media_enrichment": False,
            "accepted_evidence_requires_mros_validation": True,
        },
    }


def _paperqa_imports() -> tuple[type[Any], type[Any], Any]:
    try:
        from paperqa import Docs, Settings
        from paperqa.settings import MultimodalOptions
    except ImportError as exc:
        raise PaperQANotInstalled(
            "Install the optional integration with `python -m pip install -e '.[paperqa]'`."
        ) from exc
    return Docs, Settings, MultimodalOptions


def make_settings(*, evidence_k: int = 12) -> Any:
    """Create PaperQA settings that avoid answer generation and evidence-summary calls."""

    _, Settings, MultimodalOptions = _paperqa_imports()
    settings = Settings()
    required = (
        (settings, "answer"),
        (settings, "parsing"),
    )
    if any(not hasattr(obj, attr) for obj, attr in required):
        raise PaperQAContractError("PaperQA Settings no longer exposes answer/parsing sections")

    settings.answer.evidence_k = evidence_k
    settings.answer.evidence_skip_summary = True
    settings.answer.answer_max_sources = min(5, evidence_k)
    settings.answer.max_concurrent_requests = 1
    settings.answer.answer_filter_extra_background = False
    settings.answer.get_evidence_if_no_contexts = False
    settings.parsing.use_doc_details = False
    settings.parsing.reader_config = {"chunk_chars": 3500, "overlap": 250}
    settings.parsing.multimodal = MultimodalOptions.ON_WITHOUT_ENRICHMENT
    return settings


def build_manifest_entries(
    source_records: list[dict[str, Any]], project_root: Path
) -> list[dict[str, str]]:
    """Convert accepted MROS source records into explicit PaperQA add instructions."""

    entries: list[dict[str, str]] = []
    for source in source_records:
        source_id = str(source["source_id"])
        title = str(source.get("title") or "Untitled")
        creators = [str(x) for x in source.get("creators") or []]
        citation = f"{', '.join(creators)}. {title}" if creators else title
        for local_file in source.get("local_files") or []:
            path = (project_root / str(local_file)).resolve()
            entries.append(
                {"file": str(path), "citation": citation, "source_id": source_id}
            )
    return entries


async def abuild_docs(
    entries: Iterable[dict[str, str]], *, docs: Any | None = None
) -> Any:
    """Create/populate a PaperQA Docs object without metadata inference.

    The manifest must provide both citation and source ID.  Missing files fail closed.
    """

    if docs is None:
        Docs, _, _ = _paperqa_imports()
        docs = Docs()
    if not hasattr(docs, "aadd"):
        raise PaperQAContractError("PaperQA Docs no longer exposes aadd")
    for entry in entries:
        path = Path(entry["file"])
        if not path.is_file():
            raise FileNotFoundError(path)
        await docs.aadd(
            str(path),
            citation=entry["citation"],
            docname=entry["source_id"],
        )
    return docs


def build_docs(entries: Iterable[dict[str, str]], *, docs: Any | None = None) -> Any:
    """Synchronous wrapper for scripts and CLI contexts."""

    return asyncio.run(abuild_docs(entries, docs=docs))


def _extra(text: Any, *keys: str) -> Any | None:
    data: dict[str, Any] = {}
    if hasattr(text, "model_dump"):
        try:
            data = text.model_dump()
        except Exception:
            data = {}
    for key in keys:
        value = data.get(key, getattr(text, key, None))
        if value is not None:
            return value
    return None


def _coerce_page(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        page = int(value)
    except (TypeError, ValueError):
        return None
    return page if page >= 1 else None


async def aretrieve_from_docs(
    docs: Any,
    query: str,
    *,
    limit: int = 12,
    settings: Any | None = None,
    embedding_model: Any | None = None,
) -> list[CandidatePassage]:
    """Return raw candidate chunks through PaperQA's retrieval API only.

    No answer model and no summary model are called.  Embeddings may still use the embedding
    backend configured in PaperQA; use a local sentence-transformer configuration to avoid API
    charges.
    """

    if limit < 1:
        raise ValueError("limit must be at least 1")
    if not hasattr(docs, "retrieve_texts"):
        raise PaperQAContractError("PaperQA Docs no longer exposes retrieve_texts")
    settings = make_settings(evidence_k=limit) if settings is None else settings
    matches = await docs.retrieve_texts(
        query,
        k=limit,
        settings=settings,
        embedding_model=embedding_model,
    )
    passages: list[CandidatePassage] = []
    for match in matches:
        doc = getattr(match, "doc", None)
        source_id = (
            getattr(doc, "docname", None)
            or getattr(doc, "dockey", None)
            or getattr(match, "name", None)
            or "unknown"
        )
        page = _coerce_page(_extra(match, "page", "page_num", "page_number"))
        section = _extra(match, "section", "section_name", "heading")
        passages.append(
            CandidatePassage(
                source_external_id=str(source_id),
                text=str(getattr(match, "text", "")),
                page=page,
                section=str(section) if section is not None else None,
                score=None,
                provider="paperqa-retrieval",
                raw={
                    "chunk_name": str(getattr(match, "name", "")),
                    "citation": str(getattr(doc, "citation", "")) if doc else "",
                    "requires_mros_validation": True,
                },
            )
        )
    return passages


def retrieve_from_docs(
    docs: Any,
    query: str,
    *,
    limit: int = 12,
    settings: Any | None = None,
    embedding_model: Any | None = None,
) -> list[CandidatePassage]:
    """Synchronous retrieval wrapper."""

    return asyncio.run(
        aretrieve_from_docs(
            docs,
            query,
            limit=limit,
            settings=settings,
            embedding_model=embedding_model,
        )
    )
