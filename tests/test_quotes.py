from pathlib import Path

from mros.quotes import normalize_text, quote_hash, verify_quote, verify_quote_file


def test_exact_quote_match_reports_source_offsets():
    match = verify_quote("alpha beta gamma", "beta")
    assert match.matched and match.mode == "exact"
    assert (match.start, match.end) == (6, 10)


def test_normalized_quote_handles_unicode_and_whitespace():
    source = "The ﬁeld\ncontains   a relation."
    match = verify_quote(source, "The field contains a relation.")
    assert match.matched and match.mode == "normalized"


def test_exact_only_fails_on_whitespace_change():
    match = verify_quote("a  b", "a b", allow_normalized=False)
    assert not match.matched


def test_empty_quote_is_rejected():
    assert verify_quote("abc", "  ").reason == "empty quote"


def test_quote_hash_is_normalization_stable():
    assert quote_hash("A\nB") == quote_hash("A   B")


def test_verify_quote_file(tmp_path: Path):
    source = tmp_path / "source.txt"
    source.write_text("bounded evidence", encoding="utf-8")
    assert verify_quote_file(source, "bounded").matched


def test_soft_hyphen_removed():
    assert normalize_text("evi\u00addence") == "evidence"
