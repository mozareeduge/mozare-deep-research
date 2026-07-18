---
name: 40-screen
description: Use to apply explicit inclusion and exclusion criteria to a compact candidate batch.
disable-model-invocation: true
model: haiku
effort: low
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash(python -m mros *)
  - Bash(python -m mros verify *)
---

# Screen candidate sources

Use the source-screener for straightforward batches. Screen from title, abstract, provenance, access, and declared criteria only. Return include, exclude, or uncertain. Do not infer the full argument from metadata. Route conceptually dense, multilingual, unusual, central, or ambiguous sources to Sonnet or human review. Preserve rejection reasons.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
