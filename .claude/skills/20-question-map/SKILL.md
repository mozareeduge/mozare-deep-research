---
name: 20-question-map
description: Use to decompose an approved purpose into questions whose dependencies, evidence requirements, and decisions are explicit.
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

# Build the question map

Work from the approved contract. Build a directed question set, not a list of broad topics. Prioritize leaf questions that unlock later decisions. Include factual, bibliographic, conceptual, mechanism, comparison, method, design, technical, evaluation, and challenge questions only where needed. Avoid numeric confidence scores. Record criticality, minimum direct evidence, minimum independent groups, languages, source preferences, and stopping conditions.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
