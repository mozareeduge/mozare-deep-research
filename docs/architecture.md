# Architecture

## Four planes

### Governance

Defines the research purpose, target decision, audience, genre, scope, exclusions, evidence requirements, budget, and human approval gates.

### Discovery and corpus

Routes searches to scholarly providers, Zotero, official web sources, archives, repositories, or local materials. It normalizes identifiers, preserves versions, records queries, screens candidates, and snapshots the accepted corpus.

### Evidence and argument

Retrieves bounded passages, reranks locally where useful, verifies exact text and location, qualifies evidence independently, seeks challenges, and builds atomic claims.

### Audit and translation

Checks citations and claim support, controls release wording, records omissions, and translates accepted research into user, design, technical, and evaluation decisions.

## Flow

```mermaid
flowchart TD
    A[Research contract] --> B[Question and decision graph]
    B --> C[Bounded search plan]
    C --> D[Academic Tools / Zotero / official web / local material]
    D --> E[Normalize, deduplicate, preserve lineage]
    E --> F[Screen and snapshot accepted corpus]
    F --> G[Zotero pages / local parsers / optional PaperQA retrieval]
    G --> H[Local ranking and passage packets]
    H --> I[Exact text and location validation]
    I --> J[Independent evidence qualification]
    J --> K[Challenge search and alternative explanations]
    K --> L[Atomic claim graph]
    L --> M{Critical coverage and marginal gain}
    M -->|gap| C
    M -->|sufficient or explicitly unresolved| N[Approved outline]
    N --> O[Evidence-bounded drafting]
    O --> P[Fresh citation and adversarial audit]
    P -->|repair| L
    P -->|new evidence| C
    P -->|pass| Q[Release and decision records]
```

## State boundaries

- Zotero owns bibliographic identity, attachments, human annotations, collections, and bibliography exports.
- Git owns questions, search history, evidence status, claims, generated text, decisions, audits, and event history.
- Claude sessions are disposable workers over bounded state.
- Scripts own exactness, referential integrity, hashing, and accounting.
