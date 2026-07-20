# Live integration and semantic research certification

Record results under `audits/live-certification-YYYY-MM-DD.md`.

## Test 1 — source tools

1. Confirm Academic Tools resolves one known scholarly identifier.
2. Confirm built-in web search and fetch inspect one official source page.
3. Confirm Zotero can find one known source and read a bounded page range.
4. Confirm Zotero whole-document and write operations are unavailable.

## Test 2 — automatic semantic routing

Start a fresh Local Code session and submit an ordinary-language source question. Do not type a slash command. Pass when the project `research` skill is selected and no generic deep-research skill runs.

## Test 3 — exact wording

Request two uninterrupted passages from a known source. Pass when Claude reopens bounded source locations, records accurate wording and location, separates quotation from interpretation, and does not rely on conversation memory.

## Test 4 — full concept dossier

In a fresh session submit only:

> Gather up a research note dossier around the concept “uncreative writing” with exact terms and wording and concepts introduced and used by references.

Pass when Claude:

- automatically infers `deep` + `concept-dossier`;
- creates an isolated run and begins discovery in the same turn;
- does not read framework schemas or require internal commands;
- records exact searches in `queries.jsonl`;
- uses web and academic lanes and respects any Zotero instruction;
- selects sources by role and reads bounded primary materials;
- creates source notes, verified term records, evidence, and claims;
- runs a challenge search and a low-gain stop check;
- produces a clear dossier and useful visualization;
- uses a fresh verifier;
- passes `mros run-validate`;
- completes without the user operating phases.

## Test 5 — resumption

Interrupt an active run after at least one meaningful batch. Start a fresh session and say only “continue the research.” Pass when the newest active run, stage, status, and next action are recovered without repeating the initial search.

## Blocking failures

- generic research skill selected;
- user required to invoke internal commands;
- exact wording taken from memory, snippets, or generated summaries;
- excluded source lane used;
- no query or term record in a completed web/academic concept dossier;
- unsupported or unverified central claim;
- destructive or whole-document Zotero operation;
- silent stall without a saved blocker or progress state;
- uncontrolled parallel agents.
