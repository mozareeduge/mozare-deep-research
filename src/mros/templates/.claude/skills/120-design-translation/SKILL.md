---
name: 120-design-translation
description: Use when accepted research must produce an interface, workflow, data structure, architecture, prototype, or evaluation.
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

# Translate research into design

For each consequential decision, record: source condition, accepted claim, operation or mechanism, user need or behavior, design consequence, technical consequence, alternatives, selected option, test, risks, and reversibility. An analogy is useful only when it produces a concrete mechanism or evaluative condition and preserves relevant differences. Add a `DesignDecision` record and link it to claims and evidence.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
