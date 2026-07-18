---
name: 60-evidence
description: Use to retrieve passages, verify exact text and locations, and create
  evidence records for one question.
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
- mcp__academic_tools__get_paper_section
- mcp__academic_tools__get_paper_sections
- mcp__academic_tools__find_in_paper
- mcp__zotero__zotero_semantic_search
- mcp__zotero__zotero_get_item_metadata
- mcp__zotero__zotero_get_annotations
- mcp__zotero__zotero_read_pdf_pages
---

# Build verified evidence

Retrieve candidate passages with deterministic or local ranking before model interpretation. Keep passages separate and retain source IDs, locations, context, and scores. Verify quotations with `python -m mros quote-verify`. Then use the evidence-reviewer to qualify accepted spans. A passage may be rejected or deferred. Generated descriptions, summaries, and search snippets cannot upgrade themselves into source evidence. Validate the project after updates.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
