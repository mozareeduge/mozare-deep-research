# System decision record

## D-001 — Natural language is the user interface

The user states the research need in ordinary language. Internal phases are not commands the user must operate.

## D-002 — One semantic research skill owns orchestration

A single auto-invoked `research` skill chooses lookup, close-read, brief, deep, or design routes and carries the run forward. Generic `deep-research` skills are denied inside the project.

## D-003 — Each substantive inquiry has an isolated run

Research state lives under `research/runs/<run-id>/`. Framework source and other inquiries are not overwritten.

## D-004 — Search breadth and reading depth are separated

Claude screens broadly but closely reads only high-value sources. Search snippets are discovery leads, never evidence.

## D-005 — Evidence promotion is fail-closed

Exact quotations require bounded source rechecking. Generated summaries and model memory cannot become source evidence.

## D-006 — Source lanes follow the source object

Built-in web, Academic Tools, Zotero, and local files are complementary routes. No one indexed corpus defines the field by convenience.

## D-007 — Zotero is bounded and read-only

The normal profile denies whole-document retrieval and all write families. Page-level consultation and metadata remain available.

## D-008 — Distributed agency stays small

At most one scout and one verifier are used sequentially. MROS does not use agent teams or uncontrolled parallelism.

## D-009 — Validation occurs at meaningful boundaries

The v1 Stop hook that validated the repository after every turn was removed. Durable runs are validated explicitly before completion; session start only prints compact resumable state.

## D-010 — Model aliases, not marketing versions

The project uses the current `sonnet` alias with medium effort and does not assume that a specific numbered Sonnet model is available in every client.

## D-011 — Methodology is compiled, not performed as vocabulary

Rich methodology remains in human documentation. Operational skills use plain actions, evidence rules, permissions, and tests.

## D-012 — Research quality requires comparative evaluation

Software tests are necessary but insufficient. MROS is benchmarked against generic research on user effort, source fitness, citation support, counterevidence, coverage, durability, time, and usage.

## D-013 — Route and output profile are separate

The route determines research depth; the output profile determines the research artifact. A concept dossier therefore receives term, chronology, and reference-specific composition without adding user syntax.

## D-014 — Exact terms are durable research objects

When wording or concepts introduced by references matter, they are stored in `terms.jsonl` and must link to verified exact-quotation evidence.

## D-015 — Search history is part of research state

Every executed query is recorded with strategy, lane, purpose, batch, result count, and selected source IDs. Search cannot remain an invisible chat action.

## D-016 — Source selection uses roles, not universal tiers

Primary formulation, adjacent primary material, interpretation, critique, reception, context, and discovery are distinct functions. The machine seeks role coverage without imposing fixed quotas across fields.

## D-017 — Useful work begins in the first turn

A research run must be created and begin discovery or source reading in the same turn. Framework schemas, tests, template synchronization, and package maintenance are excluded from ordinary research.

## D-018 — Profile-sensitive completion gates

A concept dossier cannot complete without a primary-core source, query history when external search was used, verified exact terms, verified claim evidence, and a passed audit.
