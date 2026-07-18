---
name: 100-draft
description: Use to compose a section or release only after an approved outline and evidence assignment exist.
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
---

# Draft from approved claims

Use only the section brief, approved claims, assigned evidence, relevant definitions, and a compact continuity memo. Move from concrete material to concept, mechanism, consequence, and stake as the genre requires. Preserve degrees of certainty. Keep internal claim IDs during drafting. Do not introduce new factual claims or citations; route them back to discovery and evidence.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
