---
name: 110-audit
description: Use before treating a section, decision, or release as complete.
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
- mcp__zotero__zotero_get_item_metadata
- mcp__zotero__zotero_read_pdf_pages
- mcp__zotero__zotero_export_bibliography
---

# Audit claims, citations, and release

Run `python -m mros audit . --release` for a release, or `python -m mros validate .` during research. Then use the citation-auditor in a fresh context. Check exact support, location, source identity, directness, independence, challenges, scope, current facts, placeholders, omissions, and genre. Block only research-integrity or stated-requirement failures.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
