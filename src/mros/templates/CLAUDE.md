# MROS project instructions

## Natural-language research front door

- For substantive requests to research, gather research notes, review literature, trace a concept or history, compare evidence, verify exact wording, build a dossier, or ground design decisions, invoke the project `research` skill automatically.
- The user supplies a rough inquiry. The machine owns route selection, source planning, searches, durable records, resumption, and audit.
- Do not require slash commands, numbered phases, YAML templates, or repeated continuation prompts.
- Never invoke a generic or external `deep-research` skill in this repository.
- Ask at most one clarification only when ambiguity materially changes the evidence base or deliverable.
- Store substantive work in a unique `research/runs/<run-id>/`. Never overwrite framework root records or edit package/templates during a research run.

## Research behavior

1. Create the run and begin useful discovery or reading in the same turn; do not spend a turn reading schemas or general documentation.
2. Search broadly with distinct strategies, select by source role, and read only high-value materials deeply.
3. Record exact queries, source roles, exact terms, evidence, claims, and audit in the run.
4. Search snippets, metadata, abstracts, generated summaries, and model memory are leads, not source evidence.
5. For exact wording, reopen a bounded source location and verify the quotation before using it.
6. Keep each reference's terminology distinct before building cross-source synthesis.
7. Challenge central claims with alternate chronology, definitions, criticism, source dependence, and access limits.
8. Use one bounded scout and one fresh verifier sequentially when useful; never create a swarm.
9. Respect source exclusions, privacy, Zotero read-only policy, and the prohibition on whole-document Zotero retrieval.
10. Persist after meaningful batches and keep `user_visible_status` current. If usage ends, a fresh session should resume the newest active run from its state.
11. Complete only after a passed or pass-with-limits audit and `mros run-validate`.

## Operating defaults

- Current Sonnet alias, medium effort for main reasoning.
- Lower effort for bounded discovery and metadata triage.
- No full repository tests, template synchronization, package maintenance, or schema reading during ordinary research.
- Give the user simple progress messages, not internal command names.
