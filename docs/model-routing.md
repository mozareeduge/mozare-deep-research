# Claude model and effort routing

**As-of date:** 2026-07-17.

The project uses the `sonnet` alias and medium effort at session start. On the direct Anthropic route, the alias currently resolves to Sonnet 5. Skills and subagents set their own effort for the active turn or worker.

## Routing matrix

| Work | Model | Effort | Reason |
|---|---|---|---|
| Intake and query variants | Sonnet | low | bounded extraction and formatting |
| Straightforward metadata screen | Haiku | low | low-risk batch classification |
| Ambiguous screen | Sonnet | low | escalation for nuance |
| Evidence qualification | Sonnet | medium | local interpretation matters |
| Challenge reading and claims | Sonnet | medium | requires scoped reasoning |
| Outline and section drafting | Sonnet | medium | preserves quality without default high effort |
| Final central audit | Sonnet | high | one bounded independent gate |
| Exceptional architecture conflict | Opus | high | only with human approval and a compact packet |

## Rules

- Do not use high effort for search, file conversion, deduplication, quotation matching, or ledger updates.
- Do not use `max` or `ultracode` as a project default.
- Do not hand an expensive model the complete corpus.
- Benchmark Haiku, Sonnet low/medium/high, and optional older models on real project tasks before changing routing.
- A model improvement does not remove the need for bounded context and deterministic verification.
