---
name: 10-intake
description: Use when files, notes, links, transcripts, generated text, or source records enter the project.
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

# Intake research material

Receive the supplied material without turning it into a final argument. Record provenance, access status, version, direct versus interpretive or generated components, current allowed uses, what it cannot support, required verification, and destination. Preserve originals unchanged. Add or update records in `sources/manifests/sources.yaml`; write consequential changes to the event log. Run validation.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.
