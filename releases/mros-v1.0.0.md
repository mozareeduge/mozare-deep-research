# MROS v1.0.0

**Release date:** 2026-07-17  
**Status:** offline-verifiable final repository; live integrations require local certification

## Delivered system

MROS v1.0.0 provides a repo-native research operating system for Claude Code with:

- a compact research-integrity kernel instead of a long recurring methodology prompt;
- fourteen manually invoked phase skills;
- five bounded review and screening subagents;
- explicit Sonnet/Haiku effort routing;
- typed contracts for research, sources, queries, evidence, candidate links, claims, decisions, events, handoffs, state, and audits;
- JSON Schema exports for public records;
- identifier normalization, exact quotation validation, referential auditing, coverage diagnostics, and hash-chained events;
- atomic state writes and lock-protected ledgers;
- a deterministic stop gate and explicit phase-handoff gate;
- read-only default policies for Academic Tools MCP and Zotero MCP;
- an implemented retrieval-only PaperQA adapter that avoids answer-agent and passage-summary calls;
- CI across supported Python versions;
- implementation, threat, limitation, walkthrough, upstream-audit, and live-certification documentation.

## Architecture decisions

1. Git is the authoritative research-state store.
2. Zotero is the canonical bibliographic and human-reading library.
3. Deterministic and local tools perform retrieval mechanics and validation before model interpretation.
4. Claude Code performs bounded evidence qualification, challenge reading, claim construction, controlled synthesis, and audit.
5. The user retains authority over scope, central claim promotion, destructive library actions, and release.
6. Candidate connections remain distinct from accepted claims.
7. Generated output cannot promote itself to source evidence.
8. PaperQA is an optional local index and candidate-retrieval service, not the default research writer.
9. Ordinary stop-hook execution checks repository validity; a complete handoff is required only at an explicit phase boundary.

## Verification

The release passed 83 offline tests with 76% statement coverage, full and phase-stop verification, a clean wheel build/install/init cycle, and extracted-ZIP verification. Exact commands and untested live boundaries are recorded in the repository root `TEST_REPORT.md`.

## Known boundary

This release does not claim live certification of Claude Code, Zotero MCP, Academic Tools MCP, or PaperQA in the user's environment. The procedure for that certification is included in `docs/live-certification.md`.
