# Mozare Research Operating System (MROS)

MROS is a repo-native, evidence-first research operating system for Claude Code. It turns research methodology into typed records, bounded skills, deterministic validation, safe tool permissions, and replayable decisions rather than one enormous prompt.

The repository is designed for academically serious work across humanities, arts, design, AI-mediated research, technical investigation, and mixed corpora. It is especially suited to projects that combine scholarly sources, books, archives, websites, software, user materials, prototypes, and design decisions.

## What MROS changes

A conventional research agent searches, reads, and writes inside one conversation. MROS separates those operations:

```text
purpose and scope
  → question graph
  → query ledger
  → canonical source registry
  → accepted corpus snapshot
  → candidate passages
  → exact quotation validation
  → evidence qualification
  → challenge search
  → atomic claims
  → evidence-led outline
  → bounded drafting
  → independent audit
  → design and technical decisions
  → release, event history, and deferred routes
```

The repository, not the conversation, is the durable research memory.

## Included

- Pydantic models for contracts, questions, sources, query events, evidence spans, evidence cards, candidate links, claims, design decisions, handoffs, and audits.
- Deterministic DOI/arXiv/ISBN/URL normalization.
- Exact and normalized Unicode-aware quotation verification.
- Tamper-evident hash-chained event logs.
- Referential-integrity and release auditing.
- Critical-question coverage and marginal source-gain diagnostics.
- A method compiler that keeps rich human methodology out of routine prompts.
- Claude Code phase skills with model and effort routing.
- Read-only review subagents and a final adversarial reviewer.
- Session-start and repository-validity stop-gate hooks, plus explicit phase handoff.
- Read-only integration policies for Academic Tools MCP and Zotero MCP.
- An optional retrieval-only contract for PaperQA.
- Offline unit tests, exported JSON Schemas, CI, package verification, and live-certification procedures.

## Model policy

The project starts Claude Code on `sonnet` with `medium` effort. Individual skills override this:

- low: intake, query variants, compact screening, extraction;
- medium: evidence qualification, challenge reading, claims, outline, drafting, citation audit;
- high: one bounded final adversarial review;
- Opus: an exceptional human-approved decision packet only;
- `max`, `ultracode`, and Fable are not default research modes.

See [`docs/model-routing.md`](docs/model-routing.md).

## Quick start

Requirements:

- Python 3.11+
- Claude Code 2.1.197+ for Sonnet 5 and current skill/subagent fields
- optional: `uv` or `uvx` for MCP servers
- optional: Zotero running locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e .
python -m pytest
python -m mros verify .
```

Start Claude Code from the repository:

```bash
claude
```

The first substantive operation should be manual:

```text
/00-frame
```

## Create another research workspace

```bash
mros init ../my-research \
  --project-id my-research \
  --title "My Research Project" \
  --with-claude
```

## Core commands

```bash
mros doctor .
mros validate .
mros coverage .
mros quote-verify path/to/normalized-source.txt --text "Exact passage"
mros event-append . --event-id event.001 --actor human --action scope-approved
mros event-verify .
mros handoff . --objective "Completed source screening" \
  --verification "mros validate passed" \
  --next "Acquire accepted sources"
mros audit . --release
```

## MCP setup

Copy `.mcp.json.example` to `.mcp.json` only after checking commands and package names against the pinned versions installed on your machine. Project MCP configurations require workspace trust. Keep credentials in environment variables or local settings, never in the committed file.

```bash
cp .mcp.json.example .mcp.json
claude mcp list
```

MROS treats both MCP integrations as read-only during normal research. Zotero write operations require a separate human-approved maintenance workflow.

See [`docs/setup.md`](docs/setup.md), [`docs/integrations.md`](docs/integrations.md), and [`docs/live-certification.md`](docs/live-certification.md).

## Research files

| Path | Function |
|---|---|
| `research/contract.yaml` | Purpose, scope, target decisions, uncertainty, budget and gates |
| `research/questions.yaml` | Typed question and dependency map |
| `sources/manifests/sources.yaml` | Canonical source and access records |
| `queries/ledger.jsonl` | Immutable executed-query history |
| `evidence/spans/spans.yaml` | Exact source passages and locations |
| `evidence/cards/cards.yaml` | Reviewed propositions and evidence roles |
| `relations/candidates.yaml` | Candidate connections before claim promotion |
| `claims/claims.yaml` | Atomic supported, contested, insufficient, or withdrawn claims |
| `decisions/records.yaml` | Research-grounded design and technical decisions |
| `events/events.jsonl` | Hash-chained consequential event history |
| `research/handoff.yaml` | Clean-session receipt |
| `releases/` | Genre-specific output packages |
| `residue/` | Deferred, rejected, inaccessible, and omitted routes |

## External components

MROS does not copy or fork the studied repositories.

- **Academic Tools MCP:** scholarly metadata, identifiers, citations, PDF acquisition, sections, local lexical retrieval.
- **Zotero MCP:** canonical library, collection navigation, annotations, semantic discovery, bounded page reading, bibliography export.
- **PaperQA:** optional parsing and local retrieval index for accepted full-text corpora; agent answer generation is disabled in the default design.
- **ScholarQA and Recursive Research:** architectural ideas were selectively translated; neither runtime is required.

See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Design and audit documentation

- [`docs/upstream-audit.md`](docs/upstream-audit.md): what was retained, transformed, or rejected from each studied system.
- [`docs/system-decisions.md`](docs/system-decisions.md): final architectural decisions and reasons.
- [`docs/walkthrough.md`](docs/walkthrough.md): one complete research cycle.
- [`docs/live-certification.md`](docs/live-certification.md): local integration certification.
- [`TEST_REPORT.md`](TEST_REPORT.md): exact offline verification evidence.

## Safety and limits

MROS can validate the records and transformations it controls. It cannot guarantee that:

- external provider coverage is complete;
- a PDF conversion preserved every figure, note, or page boundary;
- an MCP server has not changed since audit;
- a citation is intellectually adequate merely because it resolves;
- a model interpretation is correct without human review;
- subscription limits will be identical across users or dates.

The supplied repository was tested offline. Live Zotero, MCP provider, Claude subscription, and PaperQA integration tests require the user's own environment and credentials.

## License

MIT. Optional upstream tools retain their own licenses and terms.
