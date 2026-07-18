# Integration design

MROS keeps third-party systems behind narrow adapters. The external services discover or retrieve material; MROS owns provenance, evidence status, claims, decisions, and release gates.

## Academic Tools MCP

Use for structured scholarly discovery, identifiers, bibliographic metadata, citation traversal, open-PDF acquisition, section indexing, and bounded local search.

MROS responsibilities:

- persist every executed query before synthesis;
- normalize provider output into `SourceRecord` objects;
- request counts before large citation/reference pages;
- read sections or bounded passages instead of whole papers;
- preserve the provider, query, access route, and source version;
- treat provider snippets as discovery material until the underlying source is consulted;
- use its cache, batching, concurrency controls, and identifier routing rather than asking Claude to reproduce those operations.

The built-in adapter normalizes provider results but does not silently upgrade them to accepted evidence.

## Zotero MCP

Use Zotero as the canonical human library and page-consultation layer.

Default allowed operations:

- item and collection search;
- semantic passage discovery;
- metadata and child-attachment retrieval;
- reading existing annotations and notes as separately typed materials;
- bounded PDF-page reads;
- related-paper discovery;
- bibliography export;
- library-coverage reports during maintenance.

Denied by default:

- complete-paper output into Claude context;
- create, update, delete, trash, or merge operations;
- collection, tag, relation, note, or annotation mutation.

A separate library-maintenance workflow may enable selected writes only after a dry-run, preview, explicit human confirmation, and post-change verification.

Zotero owns bibliographic identity, attachments, collections, citation keys, and human annotations. Git owns the query ledger, evidence decisions, claim graph, generated drafts, audits, and design decisions.

## PaperQA

PaperQA is optional and retrieval-only in the baseline. The MROS adapter is implemented against the current PaperQA 5-style `Docs` contract while failing closed when the dependency or expected methods are unavailable.

Recommended path:

1. Build a manifest from accepted `SourceRecord` objects.
2. Supply explicit citation metadata and stable MROS source IDs.
3. Add local files to a PaperQA `Docs` index without LLM metadata inference.
4. Retrieve candidate chunks through `Docs.retrieve_texts`.
5. Use local embeddings and, where justified, a local reranker.
6. Disable per-passage LLM summaries and agent answer generation.
7. Parse figures and tables without automatic generated enrichment by default.
8. Export candidate passages to MROS.
9. Confirm exact text and location against the normalized source.
10. Qualify evidence and build claims inside MROS.

MROS deliberately does not call PaperQA's answer agent in the normal workflow. PaperQA output remains a retrieval candidate until MROS validation and review succeed.

## Live certification boundary

Offline tests use contract doubles and deterministic fixtures. Live certification requires the user's installed versions, library, credentials, network, and Claude plan. Follow `docs/live-certification.md` before treating an integration as production-ready.
