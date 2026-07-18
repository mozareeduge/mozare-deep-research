---
name: 70-challenge
description: Use after initial evidence exists to search for counterexamples, limits,
  alternatives, and simpler explanations.
disable-model-invocation: true
model: sonnet
effort: medium
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
- mcp__zotero__zotero_read_pdf_pages
- mcp__zotero__zotero_find_related_papers
---

# Challenge central claims

For each central question or proposed claim, define what would weaken, narrow, redirect, or falsify it. Run at least one explicit challenge query where required, record it in the query ledger, and create refuting or qualifying evidence records when found. Test whether familiar vocabulary or conventional associations are creating false force. Absence of counterevidence is not proof of the claim.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
