from mros.identifiers import canonicalize_url, normalize_arxiv, normalize_doi, normalize_isbn


def test_normalize_doi_from_url_and_punctuation():
    assert normalize_doi("https://doi.org/10.1000/ABC.123).") == "10.1000/abc.123"


def test_normalize_doi_missing():
    assert normalize_doi("not a doi") is None


def test_normalize_arxiv_modern_url():
    assert normalize_arxiv("https://arxiv.org/pdf/2409.13740v2.pdf") == "2409.13740v2"


def test_normalize_arxiv_legacy():
    assert normalize_arxiv("arXiv:hep-th/9901001") == "hep-th/9901001"


def test_normalize_isbn_hyphenated():
    assert normalize_isbn("978-0-306-40615-7") == "9780306406157"


def test_normalize_isbn_rejects_short_value():
    assert normalize_isbn("1234") is None


def test_canonicalize_url_removes_tracking_and_default_port():
    assert canonicalize_url("HTTPS://Example.COM:443//a//b/?utm_source=x&z=2&a=1#frag") == "https://example.com/a/b?a=1&z=2"


def test_canonicalize_url_supplies_https():
    assert canonicalize_url("example.com/path") == "https://example.com/path"
