---
name: 30-discover
description: Use after questions and source policies are approved to search scholarly
  providers, the local library, official sites, archives, or repositories.
disable-model-invocation: true
model: sonnet
effort: low
allowed-tools:
- Read
- Grep
- Glob
- Write
- Edit
- Bash(python -m mros *)
- Bash(python -m mros verify *)
- mcp__academic_tools__*
- mcp__zotero__zotero_search_items
- mcp__zotero__zotero_semantic_search
- mcp__zotero__zotero_get_item_metadata
- mcp__zotero__zotero_get_collection_items
- mcp__zotero__zotero_find_related_papers
---

# Run bounded discovery

Search one question leaf at a time. Generate bounded query families: broad discovery, exact identifier, terminology variants, backward and forward citations, challenges, non-English variants, and local-corpus search. Use the source object to choose the retrieval lane. Record every executed query in `queries/ledger.jsonl`, including provider, filters, batch, candidates, selections, rejections, and reasons. Do not draft findings from search snippets.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
