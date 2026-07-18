---
name: 130-handoff
description: Use before clearing context or ending a coherent phase.
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
---

# Close a phase cleanly

Update state files, run validation, and write `research/handoff.yaml`. Record objective completed, files changed, sources/evidence/claims affected, decisions, unresolved items, failed routes, next actions, routes not to repeat, and verification evidence. The receipt must be sufficient for a fresh session without replaying the conversation.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
