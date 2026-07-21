# MROS v1.1.0 — Natural-language research machine

## Release purpose

V1.1 repairs the main product failure found in live use: MROS v1.0 was a strong validation framework but made the user manually operate fourteen internal research phases. V1.1 turns an ordinary or rough research inquiry into the interface.

## User-visible behavior

The user asks naturally. Claude should automatically use the project `research` skill, select the lightest adequate route, search the appropriate web/scholarly/Zotero/local lanes, persist a separate run, challenge central claims, synthesize the requested deliverable, and audit it. No slash command, YAML brief, numbered phase, or repeated “continue” instruction is required for a normal run.

## Integrity retained

- source text, interpretation, and generated material remain distinct;
- search snippets remain leads, not evidence;
- exact quotations require bounded source rechecking;
- supported claims require existing verified evidence;
- counterevidence and material limitations remain explicit;
- Zotero remains read-only and whole-document retrieval is denied;
- deep/design completion requires a passed or limited-pass audit;
- each substantial inquiry is resumable under `research/runs/`.

## Resource policy

- main researcher: current Sonnet alias, medium effort;
- optional scout: Haiku, low effort, one bounded batch;
- optional verifier: fresh Sonnet, medium effort;
- workers are sequential;
- no agent team, uncontrolled swarm, `max`, or complete-corpus dumping.

## Certification boundary

The package, harness, permissions, run records, and deterministic completion gates are tested offline. Automatic skill selection, live web/MCP behavior, research quality, elapsed time, and usage must be certified in the actual Claude Desktop environment using `docs/live-certification.md` and compared with the generic baseline using `docs/benchmark-protocol.md`.
