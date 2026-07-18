from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class QuoteMatch:
    matched: bool
    mode: str
    start: int | None = None
    end: int | None = None
    normalized_sha256: str | None = None
    reason: str = ""


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u00ad", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def quote_hash(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def verify_quote(source_text: str, quote: str, allow_normalized: bool = True) -> QuoteMatch:
    if not quote.strip():
        return QuoteMatch(False, "none", reason="empty quote")
    start = source_text.find(quote)
    if start >= 0:
        return QuoteMatch(True, "exact", start, start + len(quote), quote_hash(quote))
    if not allow_normalized:
        return QuoteMatch(False, "exact", reason="exact text not found")
    source_norm = normalize_text(source_text)
    quote_norm = normalize_text(quote)
    start = source_norm.find(quote_norm)
    if start >= 0:
        return QuoteMatch(True, "normalized", start, start + len(quote_norm), quote_hash(quote_norm))
    return QuoteMatch(False, "normalized", reason="normalized text not found")


def verify_quote_file(source_path: Path, quote: str, allow_normalized: bool = True) -> QuoteMatch:
    return verify_quote(source_path.read_text(encoding="utf-8"), quote, allow_normalized=allow_normalized)
