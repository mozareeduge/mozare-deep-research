---
name: 90-synthesis-plan
description: Use after critical questions meet their evidence gate to design the target document or artifact.
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

# Plan an evidence-led output

Restate audience, genre, purpose, and the minimum complete path. Build the outline from approved claims and unresolved questions, then assign evidence. Every section needs a function, claim IDs, evidence IDs, and an output budget. Unsupported sections become explicit gaps rather than model-memory prose. Record excluded material and its destination.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
