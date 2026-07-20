# Changelog

## 1.2.0 — Concept-dossier controller and exact-term ledger

### Changed

- Upgraded the semantic research skill from a high-level route description to an explicit internal controller: route, map, discover, select, read, extract, challenge, synthesize, verify, and deliver.
- Required useful discovery or reading to begin in the same turn as run initialization; ordinary research no longer reads schemas or performs framework maintenance.
- Added gap-directed iteration and simple user-visible progress instead of user-operated phases.
- Reworked source selection around evidential roles and an access ladder rather than source tiers or citation counts.
- Made concept dossiers plan their outline only after primary sources, exact terms, and evidence are visible.

### Added

- `concept-dossier` output profile for rough requests focused on exact terms, wording, definitions, and reference-specific concepts.
- Durable query and term ledgers: `queries.jsonl` and `terms.jsonl`.
- Source roles, reading status, query strategies, verification methods, claim types, explicit run stages, run budgets, progress fields, and user-visible status.
- `source-notes/` and `visualization.md` inside every substantive run.
- `mros run-summary` for compact resumption and black-box status checks.
- Completion gates requiring a selected primary-core source, verified term records, verified exact-quote evidence, and a query log for web/academic concept dossiers.
- A synthetic end-to-end Uncreative Writing concept-dossier test covering route, search, selection, exact terms, evidence, claims, visualization, audit, and completion.
- A full process simulation document for nontechnical users and evaluators.

### Fixed

- V1.1 could create a durable dossier without recording the exact terminology requested by the user.
- Search activity was not first-class in the lightweight run, weakening reproducibility.
- Session context mixed legacy project state with active semantic runs.
- The semantic skill could remain too abstract about latency, progress, evidence-first outlining, and low-gain stop conditions.

## 1.1.0 — Semantic research front door

### Changed

- Replaced fourteen user-operated phase skills with one auto-selected project `research` skill.
- Added adaptive lookup, close-read, brief, deep, and design routes inferred from ordinary-language inquiries.
- Added isolated durable research runs under `research/runs/<run-id>/`.
- Added built-in web discovery and fetch to the active research tool surface.
- Denied generic `deep-research`, Zotero whole-document retrieval, and Zotero write/destructive tool families in the project profile.
- Replaced five narrow phase agents with one bounded low-effort source scout and one independent verifier.
- Removed per-turn Stop-hook validation; retained compact SessionStart resumption context and explicit completion validation.
- Corrected Academic Tools MCP setup to use a pinned local clone and the upstream `uv run --directory ...` command.
- Changed model policy to the current capability alias rather than a specific numbered Sonnet release.
- Archived the full v1 phase skills and agents under `docs/archive/` rather than discarding them.

### Added

- `mros run-init`, `run-append`, `run-state`, and `run-validate` commands.
- Strict lightweight run records for sources, evidence, claims, state, and audit.
- Fail-closed completion checks for missing and unverified claim evidence.
- Natural-language live-certification and comparative benchmark protocols.
- Root-cause analysis and v1.0 → v1.1 migration guide.
- Tests for semantic skill configuration, isolated run lifecycle, inline record append, referential integrity, and completion evidence gates.

### Fixed

- Full-text Zotero access could remain available despite a safe-tool allowlist.
- Broad web research was described but not wired into the discovery tool surface.
- Research inquiries overwrote shared framework state.
- Claude could hallucinate or require internal command names.
- `scripts/sync_templates.py` could copy machine-local Claude settings into package templates.

## 1.0.0 — Initial evidence operating system

- Typed research records, schemas, deterministic validators, quote checking, event chain, adapters, Claude skills/agents/hooks, CI, packaging, and installation certification.
