# Upstream systems: extraction and composition audit

MROS does not combine whole upstream applications. It selects mechanisms according to the research operation, removes duplicated orchestration, and keeps one authoritative project state.

## Recursive Research

**Retained**

- disk checkpoints that survive clean Claude sessions;
- explicit resume and handoff behavior;
- visible gaps and contradiction tasks;
- bounded research cycles and an explicit stop decision;
- separation of collection from final synthesis.

**Transformed**

- generic threads became a typed question-and-decision dependency graph;
- fixed source tiers became source/access records plus evidence directness, role, independence, and allowed use;
- finding counts became central-claim coverage, counter-search completion, and marginal unique-evidence gain;
- narrative checkpoints became validated state files and compact handoff receipts.

**Rejected from the default method**

- “PhD-level” labels;
- arbitrary minimum numbers of sources or cross-thread links;
- model-generated weighted matrices presented as measurement;
- compulsory speculative connections.

## Academic Tools MCP

**Retained as an external deterministic service**

- provider routing and identifier normalization;
- compact metadata and abstract triage;
- references and citation traversal;
- batched requests, caching, retry behavior, and concurrency control;
- bounded PDF acquisition, conversion locks, section indexes, in-paper search, and BM25;
- explicit output limits.

**MROS additions**

- immutable query records;
- canonical source records and cross-provider deduplication;
- source/access status and allowed-use controls;
- a rule that provider snippets remain discovery leads until source consultation.

## Ai2 ScholarQA

**Retained as pipeline ideas**

- lexical/full-text retrieval union;
- local reranking before generation;
- exact-evidence extraction;
- outline planning and assignment of evidence before drafting;
- typed intermediate objects and event traces;
- section-level revision actions.

**Transformed**

- expensive per-paper LLM extraction became bounded passage packets and one scoped evidence-qualification operation;
- forced quote placement became accept, reject, defer, or re-route decisions;
- serial full-report accumulation became section briefs plus compact continuity records;
- citation-count importance became optional contextual metadata;
- indirect references enter a verification queue instead of being laundered into evidence.

**Rejected**

- evidence-free sections written from model memory;
- mandatory use of every extracted quotation;
- a monolithic application runtime as the source of project truth.

## Zotero MCP

**Retained as the canonical human library**

- item, collection, tag, attachment, annotation, note, and citation-key navigation;
- semantic passage search and optional local reranking;
- bounded PDF-page consultation;
- bibliography export, coverage diagnostics, and related-paper discovery.

**Restricted**

- full-paper responses are denied during routine research;
- all write, merge, delete, relation, collection, tag, note, and annotation mutations are denied by default;
- semantic hits are candidates, not evidence;
- user notes remain distinct from source quotations.

## PaperQA

**Retained as an optional local corpus service**

- readers and page-aware parsing;
- reusable document indexes;
- sparse, semantic, and hybrid retrieval;
- metadata-aware chunks and local embeddings;
- a manual/no-agent `Docs` path.

**Transformed**

- the adapter supplies citation metadata from MROS/Zotero manifests;
- `Docs.retrieve_texts` is called directly;
- per-passage LLM summaries, answer generation, and media enrichment are disabled by default;
- retrieved chunks must pass MROS source-location and quotation validation.

**Rejected from the default path**

- `pqa ask` as the research controller;
- separately billed model calls hidden inside indexing or evidence summarization;
- accepting a generated answer as research evidence.

## Composition rule

Only one layer owns each kind of state:

- **Zotero:** bibliographic library, attachments, human annotations.
- **External retrieval tools:** discovery and bounded source access.
- **PaperQA/local indexes:** candidate passage retrieval.
- **MROS/Git:** questions, query history, evidence status, claims, decisions, audits, events, and releases.
- **Claude Code:** bounded interpretation and composition over validated state.
- **Human:** purpose, consequential promotion decisions, destructive actions, and release authority.
