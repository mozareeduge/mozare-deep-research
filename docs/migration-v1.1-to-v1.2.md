# Migration from MROS v1.1 to v1.2

## Product change

V1.1 introduced one natural-language research skill and isolated runs. V1.2 makes that controller materially stronger for concept-centered dossiers and exact wording.

The user interface does not change: submit a rough inquiry in ordinary language.

## New run files

V1.2 adds:

- `queries.jsonl` — exact search history and selected source IDs;
- `terms.jsonl` — reference-specific exact terminology linked to evidence;
- `source-notes/` — compact close-reading notes for selected core sources;
- `visualization.md` — optional chronology or concept map.

Existing v1.1 runs remain readable. New runs use the expanded v1.2 state and record models.

## New completion gates

A completed concept dossier requires:

- a selected primary-core source;
- query records when web/academic lanes were used;
- at least one verified term record;
- exact-quotation evidence for every term;
- verified evidence for consequential claims;
- a passed or pass-with-limits audit.

## Migration procedure

1. Preserve local `.mcp.json`, `.env*`, Zotero data, private corpora, and `.venv` outside release replacement.
2. Apply the v1.2 release files on a new branch.
3. Run `python scripts/sync_templates.py` only after the source harness is final.
4. Run `python scripts/export_schemas.py --check`, `python -m pytest`, `python -m mros verify .`, and `python -m mros audit . --release`.
5. Confirm the packaged harness mirrors the root harness.
6. Run the synthetic concept-dossier test and then live certification with the one-sentence inquiry.
7. Open a draft PR; do not merge until CI and live semantic routing pass.

## Local configuration

Keep the current local `.mcp.json`. V1.2 does not require another MCP or paid API. Academic Tools, built-in web tools, and optional read-only Zotero remain the default lanes.
