from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
ARXIV_RE = re.compile(r"(?:arxiv:)?((?:\d{4}\.\d{4,5})(?:v\d+)?|[a-z-]+/\d{7})(?:\.pdf)?$", re.I)
ISBN_RE = re.compile(r"(?:97[89])?\d{9}[\dXx]")


def normalize_doi(value: str) -> str | None:
    match = DOI_RE.search(value.strip())
    return match.group(0).rstrip(".,;)").lower() if match else None


def normalize_arxiv(value: str) -> str | None:
    cleaned = value.strip().split("?")[0].rstrip("/")
    cleaned = cleaned.rsplit("/", 1)[-1] if "arxiv.org" in cleaned else cleaned
    match = ARXIV_RE.search(cleaned)
    return match.group(1).lower() if match else None


def normalize_isbn(value: str) -> str | None:
    cleaned = re.sub(r"[^0-9Xx]", "", value)
    return cleaned.upper() if ISBN_RE.fullmatch(cleaned) else None


def canonicalize_url(value: str) -> str:
    raw = value.strip()
    if "://" not in raw:
        raw = "https://" + raw.lstrip("/")
    parts = urlsplit(raw)
    scheme = parts.scheme.lower() or "https"
    host = (parts.hostname or "").lower()
    port = parts.port
    netloc = host
    if port and not ((scheme == "https" and port == 443) or (scheme == "http" and port == 80)):
        netloc = f"{host}:{port}"
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    if path != "/":
        path = path.rstrip("/")
    tracking = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid", "gclid"}
    query = urlencode(sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() not in tracking))
    return urlunsplit((scheme, netloc, path, query, ""))
