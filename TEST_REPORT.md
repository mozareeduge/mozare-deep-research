# MROS v1.0.0 Test Report

**Certification date:** 2026-07-17  
**Environment:** Linux, Python 3.13.5  
**Scope:** offline core, repository contracts, build/package installation, and extracted release archive

## Result

**PASS for the offline-verifiable release.**

The test suite completed with **83 passed, 0 failed**. Statement coverage was **76%** with branch coverage enabled. All repository, phase-stop, and release audits completed with zero blockers and zero warnings.

## Commands and results

| Check | Command | Result |
|---|---|---|
| Unit and contract tests | `python -m pytest -q` | PASS — 83 tests |
| Coverage | `python -m pytest --cov=mros --cov-report=term-missing` | PASS — 76% total statement coverage |
| JSON Schema freshness | `python scripts/export_schemas.py --check` | PASS — 13 schemas current |
| Packaged harness freshness | `python scripts/sync_templates.py --check` | PASS |
| Python compilation | `python -m compileall -q src tests scripts` | PASS |
| Full verification | `python -m mros verify .` | PASS — 0 audit warnings |
| Phase-boundary verification | `python -m mros verify . --phase-stop` | PASS |
| Installation diagnostics | `python -m mros doctor .` | PASS; optional PaperQA not installed |
| Structural validation | `python -m mros validate .` | PASS — no issues |
| Release audit | `python -m mros audit . --release` | PASS — 0 blockers, 0 warnings |
| Wheel build | `python -m pip wheel . --no-deps` | PASS |
| Clean wheel install | install in a new virtual environment | PASS |
| Wheel-installed workspace initialization | `mros init ... --with-claude` | PASS |
| Wheel-installed workspace validation | `mros doctor`, `mros validate`, `mros verify` | PASS |
| Installed Claude hooks | `mros-session-context`, `mros-stop-gate` | PASS |
| Final ZIP CRC | Python `ZipFile.testzip()` | PASS |
| Extracted ZIP test suite | `python -m pytest -q` | PASS |
| Extracted ZIP verification | `python -m mros verify .` and release audit | PASS |

## Areas tested

- strict Pydantic model invariants and generated-material evidence firewall;
- DOI, arXiv, ISBN, and URL normalization;
- exact and normalized Unicode quotation matching;
- evidence/source/claim/question/decision referential integrity;
- direct, indirect, metadata-only, and generated evidence restrictions;
- central-question coverage and counter-search rules;
- candidate-link and claim promotion requirements;
- event hash calculation, tamper detection, duplicate detection, concurrent append safety, and state/event-head consistency;
- atomic JSON/YAML replacement and concurrent JSONL writers;
- lock timeout and stale-lock recovery;
- method compilation and operational-vocabulary checks;
- Academic Tools and Zotero read-only adapter policies;
- PaperQA retrieval-only contract, explicit metadata, disabled summarization/enrichment policy, and current `Settings` shape through a contract double;
- CLI initialization, validation, events, quotation verification, handoff, and diagnostics;
- Claude skill and subagent frontmatter contracts;
- read-only Zotero permission allowlist;
- pinned MCP example distributions;
- package-data mirror used by wheel-installed `--with-claude` initialization;
- stop-hook recursion protection, valid-state passage, and invalid-state blocking;
- release placeholder detection and final release audit.

## Explicitly not certified here

The following require the user's own environment and are not claimed as live-tested:

- real Claude Code model invocation or subscription-limit behavior;
- live Academic Tools MCP network calls;
- live Zotero library search, semantic index, PDF-page reading, or permission enforcement;
- a real PaperQA installation indexing a substantive corpus;
- embedding and reranking quality for Persian, book-heavy, archival, artistic, or project-specific corpora;
- end-to-end scholarly accuracy on the user's gold set.

The exact local procedure is in `docs/live-certification.md`. These boundaries are release limitations, not hidden test gaps.
