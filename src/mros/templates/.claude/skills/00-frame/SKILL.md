---
name: 00-frame
description: Use at the start of a project or consequential phase to establish purpose, decisions, scope, exclusions, uncertainty, budgets, and approval gates.
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

# Frame a research run

Read the user request and current project state. Do not search yet. Update `research/contract.yaml`, then create or revise `research/questions.yaml` as a dependency-aware set of bounded questions. Each question must state why it matters, what decision it informs, acceptable evidence, counter-search requirement, and a stop rule. Mark assumptions explicitly. Ask for human approval only where the scope or target decision remains materially ambiguous. Run `python -m mros validate .` before returning.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
