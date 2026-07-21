# MROS v1.2 revision analysis

## Why v1.1 still needed revision

V1.1 repaired the interface failure of v1.0 by adding one semantic front door. It could infer a deep route and create durable source, evidence, claim, and audit records. A full simulation of the user's target inquiry exposed a second product gap: the lightweight run still modeled generic research more strongly than the requested artifact.

The inquiry asks for a research-note dossier around a concept with **exact terms, wording, and concepts introduced and used by references**. A generic source/evidence/claim pipeline can produce a defensible essay while losing the source-specific vocabulary that makes the dossier valuable. Search activity was not a first-class record; exact formulations had no dedicated object; source selection had no explicit role map; and the active skill described stages without a sufficiently concrete controller for progress, low-gain iteration, evidence-first outlining, or concept-dossier composition.

## V1.2 product decision

V1.2 preserves one rough natural-language inquiry as the interface but adds an internal output-profile layer. The route answers “how deep?”; the profile answers “what kind of research object?”

For the target inquiry the machine infers:

- route: `deep`;
- output profile: `concept-dossier`;
- requirements: exact wording, reference-by-reference terminology, historical formation, criticism, later reception, references, and a useful visualization.

No user syntax is added.

## Benchmark mechanisms recomposed

| Source system or material | Retained mechanism | Modification for MROS |
|---|---|---|
| Recursive Research | checkpoints, gap-directed iteration, explicit stop decision, contradiction search | remove source tiers, weighted pseudo-measurement, fixed PhD quotas, and user-operated cycles; use source roles and two low-gain bounded batches |
| ScholarQA | retrieve/rerank, exact-quote extraction, evidence assignment before drafting, independent pipeline stages | preserve passage-level provenance; allow rejection/deferment; do not force every quote or evidence-free section; outline only after term/evidence records |
| PaperQA | reusable parsing/indexing, MMR/hybrid retrieval, manual no-agent access | optional local corpus retrieval only; no hidden LLM summaries or final-answer authority |
| Academic Tools | deterministic scholarly metadata, citation traversal, bounded text access, caching | log exact queries and normalize results into role-aware source records |
| Zotero MCP | semantic discovery, annotations, metadata, bounded page reading | read-only; whole-document and write operations denied; exact quotations require bounded page recheck |
| GPT Researcher | planner/executor/publisher separation and mixed web/local retrieval | do not install its separately billed orchestration; adapt the separation into one controller with durable work order and dossier publisher |
| STORM / Co-STORM | perspective mapping before report composition | adapt as source-role and coverage-slot mapping; do not accept generated encyclopedic prose as evidence |
| Local Deep Research | local-first privacy and reusable indexes | retain as a possible future deployment path, not an initial dependency |
| Research methodology dossier | wide/close loop, provenance, relation before claim, counterevidence, evidence firewall, genre-fit export | compile into source roles, term/evidence objects, challenge search, and completion gates; do not inject theoretical vocabulary into every turn |
| Token/context dossier and Claude guidance | progressive disclosure, clean context, handoff/checkpoint, bounded subagents, deterministic validation | supporting profile files, concise session hook, run summary, one scout, one verifier, no per-turn repository validation |

## Core changes

### Query history becomes first-class

`queries.jsonl` records exact search text, lane, strategy, purpose, batch, result count, and selected source IDs. This makes discovery reproducible and allows low-gain stop decisions.

### Exact concepts become first-class

`terms.jsonl` records a reference-specific label, function, exact wording, source, evidence, location, verification, variants, and interpretation. A term cannot be valid merely because the dossier contains quotation marks.

### Source roles replace universal tiers

Sources are selected for evidential functions: primary-core, primary-adjacent, scholarly interpretation, critique, reception, context, or discovery-only. Role coverage guides search without turning all fields into a rigid source quota.

### The controller becomes operational

The active skill now directs a continuous internal sequence:

`route → map → discover → select → read → extract → challenge → synthesize → verify → deliver`

It must create the run and start useful discovery in the same turn. It must not read schemas, synchronize templates, or run framework tests during ordinary research.

### Progress and resumption become visible but simple

The run stores `user_visible_status`, exact stage, counts, next actions, and open questions. Session start reports the newest active run instead of legacy framework state. The user can resume with ordinary language.

### Completion is profile-sensitive

A completed web/academic concept dossier requires:

- logged queries;
- a selected primary-core source;
- verified term records;
- exact-quotation evidence for each term;
- verified evidence for consequential claims;
- a non-empty dossier;
- a passed or pass-with-limits audit.

## What remains deliberately model-mediated

MROS does not attempt to convert a semantic inquiry into a fixed questionnaire or deterministic keyword classifier. Claude still interprets purpose, source relevance, historical specificity, and conceptual relations. Deterministic code checks the integrity of the record chain and completion conditions, not the intellectual truth of the interpretation.

## Acceptance criterion

V1.2 succeeds only when the user can submit the original one-sentence inquiry and the machine carries it to an academically useful dossier without slash commands, phase prompts, or schema work. The live benchmark must still establish source quality, citation support, exact-term integrity, counterevidence, elapsed time, and subscription efficiency against the generic baseline.
