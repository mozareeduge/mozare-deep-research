# Mozare Research Operating System (MROS)

MROS turns Claude Code into a natural-language, evidence-grounded research workspace. State a rough research need; the project `research` skill infers the route, searches the right source lanes, reads selected materials, records exact terms and evidence, challenges central claims, produces the requested artifact, and audits it. You do **not** operate numbered commands or prompt templates.

## Example

> Gather up a research note dossier around the concept “uncreative writing” with exact terms and wording and concepts introduced and used by references.

MROS should infer:

- route: `deep`;
- output profile: `concept-dossier`;
- emphasis: primary and scholarly references, exact wording, chronology, criticism, and later reception;
- source lanes: web and academic tools, plus Zotero or local files only when relevant and permitted.

It then conducts the run without asking the user to name phases.

## V1.2 flow

```text
rough inquiry
  → semantic route + output-profile inference
  → isolated durable run
  → broad source map with logged queries
  → role-based source selection
  → bounded reading and source notes
  → verified exact terms + evidence
  → challenge and low-gain stop check
  → evidence-led dossier and visualization
  → fresh audit
  → validated deliverable + resumable run
```

See [`docs/simulation-uncreative-writing.md`](docs/simulation-uncreative-writing.md) for a complete 0-100 walkthrough.

## Adaptive routes

- **lookup:** narrow source or factual questions;
- **close-read:** exact wording or interpretation from named sources;
- **brief:** bounded evidence-backed explanation;
- **deep:** literature review, conceptual history, research dossier, or contested synthesis;
- **design:** research ending in method, product, interface, prototype, or technical decisions.

The output profile adapts the internal composition. V1.2 adds `concept-dossier` for requests centered on exact terminology, wording, definitions, distinctions, and reference-specific concepts.

## Durable research runs

Substantive inquiries are stored separately from the framework:

```text
research/runs/<run-id>/
├── request.md
├── state.yaml
├── plan.md
├── queries.jsonl
├── sources.jsonl
├── source-notes/
├── terms.jsonl
├── evidence.jsonl
├── claims.jsonl
├── visualization.md
├── dossier.md
└── audit.yaml
```

This permits resumption after context or subscription limits and prevents one inquiry from overwriting another.

## Source tools

- **Built-in WebSearch/WebFetch:** publishers, primary web texts, archives, institutions, repositories, current sources.
- **Academic Tools MCP:** OpenAlex, Crossref, arXiv, citations/references, metadata, and bounded paper access.
- **Zotero MCP:** the user's library, annotations, metadata, and bounded page reading. Normal research is read-only; whole-document retrieval and writes are denied.
- **Direct local files:** user-provided books, articles, archives, datasets, code, and images.
- **PaperQA:** optional retrieval index for a large accepted local corpus; not required for the normal route.

## Research integrity

MROS distinguishes discovery, source access, exact wording, interpretation, evidence, claims, and generated synthesis. Search snippets are leads, not evidence. Exact terms must resolve to a bounded source recheck. Central claims must identify verified evidence, scope, uncertainty, and credible qualification or counterevidence.

## Installation

Requirements:

- Python 3.11+
- current Claude Code / Claude Desktop Code
- optional `uv`/`uvx` for MCP servers
- optional Zotero 7+ running locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
python -m pytest
python -m mros verify .
```

Copy `.mcp.json.example` to `.mcp.json`, replace the Academic Tools path with the absolute path of its pinned local clone, and keep `.mcp.json` uncommitted. See [`docs/setup.md`](docs/setup.md).

## Internal CLI

Claude normally uses these. They are not a user workflow:

```bash
mros run-init research/runs/my-run --mode deep --output-profile concept-dossier
mros run-append research/runs/my-run --kind query --json-file query.json
mros run-append research/runs/my-run --kind term --json-file term.json
mros run-state research/runs/my-run --stage evidence
mros run-summary research/runs/my-run
mros run-validate research/runs/my-run
```

## Evaluation

Offline tests validate the software contract, including a synthetic end-to-end concept-dossier flow. Live superiority over generic deep research still requires comparative evaluation of source fitness, primary coverage, citation support, exact wording, counterevidence, user effort, elapsed time, usage, and durability. See [`docs/benchmark-protocol.md`](docs/benchmark-protocol.md).

## License

MIT. Optional upstream tools retain their own licenses and terms.
