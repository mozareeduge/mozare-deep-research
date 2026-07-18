---
name: 50-acquire
description: Use after screening to preserve accepted source versions and prepare
  bounded local access.
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
- mcp__academic_tools__download_pdf
- mcp__academic_tools__convert_paper
- mcp__academic_tools__import_paper
- mcp__zotero__zotero_get_item_metadata
- mcp__zotero__zotero_get_item_children
- mcp__zotero__zotero_read_pdf_pages
---

# Acquire and snapshot the corpus

Acquire only accepted or high-potential sources. Preserve originals, hashes, versions, rights and access status, conversion tool/version, and extraction limitations. Prefer metadata, abstract, section index, selected pages, then full conversion only when justified. Create a corpus snapshot identifier before evidence work. Do not place credentials in the repository.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
