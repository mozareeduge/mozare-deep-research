---
name: 80-claims
description: Use to convert accepted evidence and tested candidate links into atomic, qualified claim records.
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

# Construct scoped claims

Create one scoped proposition per claim. Link supporting, refuting, and qualifying evidence; distinguish direct from indirect support; state assumptions, inference type, uncertainty, and dependencies. A candidate link can be promoted only when evidence supports the stated use. Supported and contested claims must satisfy their schemas. Do not promote a claim merely because it is fluent or theoretically attractive.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
