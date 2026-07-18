from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest

from mros.adapters.academic_tools import normalize_result
from mros.adapters.paperqa import (
    PaperQAContractError,
    abuild_docs,
    aretrieve_from_docs,
    build_manifest_entries,
    recommended_settings,
)
from mros.adapters.zotero import DENIED_BY_DEFAULT, READ_ONLY_TOOLS, is_safe_default_tool


def test_academic_tools_normalizes_identifiers_and_authors():
    result = normalize_result(
        {
            "id": "https://arxiv.org/abs/2409.13740",
            "title": "PaperQA2",
            "authors": [{"name": "A"}, {"display_name": "B"}],
            "doi": "https://doi.org/10.1000/XYZ",
            "arxiv_id": "2409.13740",
        },
        "openalex",
    )
    assert result.identifiers == {"doi": "10.1000/xyz", "arxiv": "2409.13740"}
    assert result.creators == ["A", "B"]


def test_zotero_policy_is_read_only_by_default():
    assert is_safe_default_tool("zotero_read_pdf_pages")
    assert not is_safe_default_tool("zotero_delete_item")
    assert READ_ONLY_TOOLS.isdisjoint(DENIED_BY_DEFAULT)


def test_paperqa_policy_disables_summary_and_enrichment():
    settings = recommended_settings()
    assert settings["answer"]["evidence_skip_summary"] is True
    assert settings["answer"]["answer_filter_extra_background"] is False
    assert settings["parsing"]["multimodal"] == "on_without_enrichment"
    assert settings["policy"]["agent_answering"] is False


def test_build_manifest_entries_uses_explicit_metadata(tmp_path: Path):
    entries = build_manifest_entries(
        [{
            "source_id": "src.01",
            "title": "Title",
            "creators": ["Author"],
            "local_files": ["corpus/a.pdf"],
        }],
        tmp_path,
    )
    assert entries[0]["source_id"] == "src.01"
    assert entries[0]["citation"] == "Author. Title"
    assert entries[0]["file"] == str((tmp_path / "corpus/a.pdf").resolve())


class FakeDocs:
    def __init__(self):
        self.added = []

    async def aadd(self, path, citation, docname):
        self.added.append((path, citation, docname))

    async def retrieve_texts(self, query, k, settings, embedding_model=None):
        doc = SimpleNamespace(docname="src.01", dockey="key", citation="Citation")
        return [
            FakeText("passage one", "chunk 1", doc, page_num=4, section="Methods"),
            FakeText("passage two", "chunk 2", doc),
        ][:k]


class FakeText:
    def __init__(self, text, name, doc, **extra):
        self.text = text
        self.name = name
        self.doc = doc
        self.extra = extra
        for key, value in extra.items():
            setattr(self, key, value)

    def model_dump(self):
        return {"text": self.text, "name": self.name, **self.extra}


def test_abuild_docs_fails_closed_for_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        asyncio.run(abuild_docs([{"file": str(tmp_path / "missing.pdf"), "citation": "C", "source_id": "src.01"}], docs=FakeDocs()))


def test_abuild_docs_passes_explicit_citation_and_source_id(tmp_path: Path):
    file = tmp_path / "source.txt"
    file.write_text("text", encoding="utf-8")
    docs = FakeDocs()
    result = asyncio.run(abuild_docs([{"file": str(file), "citation": "C", "source_id": "src.01"}], docs=docs))
    assert result is docs
    assert docs.added == [(str(file), "C", "src.01")]


def test_retrieve_from_docs_converts_raw_chunks_without_llm_settings():
    docs = FakeDocs()
    settings = SimpleNamespace()
    passages = asyncio.run(aretrieve_from_docs(docs, "question", limit=2, settings=settings))
    assert [p.text for p in passages] == ["passage one", "passage two"]
    assert passages[0].page == 4
    assert passages[0].section == "Methods"
    assert passages[0].raw["requires_mros_validation"] is True


def test_retrieve_requires_supported_docs_contract():
    with pytest.raises(PaperQAContractError):
        asyncio.run(aretrieve_from_docs(object(), "question", settings=object()))


def test_retrieve_limit_must_be_positive():
    with pytest.raises(ValueError):
        asyncio.run(aretrieve_from_docs(FakeDocs(), "question", limit=0, settings=object()))


def test_make_settings_applies_current_paperqa_contract(monkeypatch):
    import sys
    import types

    class Answer:
        pass

    class Parsing:
        pass

    class FakeSettings:
        def __init__(self):
            self.answer = Answer()
            self.parsing = Parsing()

    class FakeDocsClass:
        pass

    class FakeMultimodal:
        ON_WITHOUT_ENRICHMENT = "no-enrichment"

    package = types.ModuleType("paperqa")
    package.Docs = FakeDocsClass
    package.Settings = FakeSettings
    settings_module = types.ModuleType("paperqa.settings")
    settings_module.MultimodalOptions = FakeMultimodal
    monkeypatch.setitem(sys.modules, "paperqa", package)
    monkeypatch.setitem(sys.modules, "paperqa.settings", settings_module)

    from mros.adapters.paperqa import make_settings

    settings = make_settings(evidence_k=7)
    assert settings.answer.evidence_k == 7
    assert settings.answer.evidence_skip_summary is True
    assert settings.answer.get_evidence_if_no_contexts is False
    assert settings.answer.max_concurrent_requests == 1
    assert settings.parsing.use_doc_details is False
    assert settings.parsing.multimodal == "no-enrichment"
