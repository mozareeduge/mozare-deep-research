# Live integration certification

Run this checklist in the actual research environment after installing the optional systems. Record the results in `audits/live-certification-YYYY-MM-DD.md` and append one event to `events/events.jsonl`.

## Preconditions

- Pin the exact versions or commit SHAs of Claude Code, Academic Tools MCP, Zotero MCP, and PaperQA.
- Review the current upstream release notes and permissions.
- Start from a temporary Zotero collection containing three known, non-sensitive sources.
- Keep Zotero write tools disabled.
- Do not place API keys in committed files.

## Academic Tools MCP

1. Run `claude mcp list` and confirm the server is connected.
2. Search one known DOI or arXiv identifier.
3. Record provider, exact query, result count, and normalized identifiers.
4. Traverse one reference and one citation page with a bounded result limit.
5. Confirm that snippets are stored as discovery records, not evidence cards.

## Zotero MCP

1. Search the same known source by title and item key.
2. Read its metadata and child attachment list.
3. Run semantic search for a phrase known to appear in the document.
4. Read a bounded two-page range around the hit.
5. Confirm that complete-paper and write tools are unavailable to the normal workflow.
6. Export one bibliography entry and compare it with the Zotero record.

## PaperQA retrieval-only adapter

1. Install with `python -m pip install -e '.[paperqa]'` in an isolated environment.
2. Build a manifest for three accepted local documents.
3. Build a `Docs` index using explicit citation metadata.
4. Retrieve five chunks for a known query through the MROS adapter.
5. Confirm that no answer-agent or per-passage summarization call occurred.
6. Compare top passages with Zotero/local lexical retrieval.
7. Validate at least one exact quotation and its page or section.

## Claude workflow

1. Run `/00-frame` on a bounded test question.
2. Complete discovery, screening, evidence, challenge, claims, outline, draft, and audit.
3. Confirm that a generated lead cannot become formal evidence without human review.
4. Confirm that the stop hook permits ordinary turns but blocks invalid repository state.
5. Run `/130-handoff`, then `python -m mros verify . --phase-stop`.

## Pass criteria

- No destructive Zotero action is possible from the normal profile.
- Every accepted evidence card resolves to an existing, validated span.
- Every formal claim resolves to accepted evidence allowed for formal use.
- No model-generated statement appears as source evidence.
- Query, source, evidence, claim, event, and handoff records validate.
- All deviations from the pinned contracts are documented.
