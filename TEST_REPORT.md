# MROS v1.2.0 Test Report

**Date:** 2026-07-19  
**Status:** offline release candidate PASS; live automatic-routing and research-quality benchmark still required

## Summary

| Check | Result |
|---|---|
| Automated tests | **94 passed, 0 failed** |
| Statement/branch coverage | **75% overall**, branch measurement enabled |
| Python compilation | PASS |
| Exported JSON Schemas | **20 current and valid** |
| Packaged Claude harness mirror | PASS |
| `mros validate .` | PASS — 0 issues |
| `mros verify .` | PASS — 0 issues |
| `mros verify . --phase-stop` | PASS |
| `mros audit . --release` | PASS — 0 blockers, 0 warnings |
| Event hash chain | PASS |
| Wheel build | PASS — `mozare_research_os-1.2.0-py3-none-any.whl` |
| Clean-environment wheel installation | PASS |
| Wheel-installed `mros init --with-claude` | PASS |
| Installed semantic research harness | PASS |
| Installed concept-dossier run initialization | PASS |
| Installed run summary and validation | PASS |
| ZIP CRC/integrity | PASS |
| ZIP local-secret exclusion | PASS |
| Extracted-ZIP verification | PASS |

## What the automated tests establish

### Natural-language research interface

- one active project-owned `research` skill is installed;
- it is hidden from slash-command operation and available for automatic semantic selection;
- its description explicitly covers rough inquiries, research notes, dossiers, literature reviews, exact terms, wording, and reference-specific concepts;
- the active path includes web search/fetch, scholarly discovery, bounded Zotero access, durable records, challenge search, synthesis, and fresh verification;
- generic `deep-research` is denied within the project;
- the user is not required to operate numbered phase commands.

### Concept-dossier integrity

The synthetic end-to-end test models the target inquiry, “Gather up a research note dossier around the concept ‘uncreative writing’ with exact terms and wording and concepts introduced and used by references.” It verifies:

- route `deep` plus output profile `concept-dossier`;
- exact query records with search strategies and source selections;
- role-aware source records, including primary-core, interpretation, critique, and reception roles;
- verified exact-quotation evidence;
- reference-specific term records linked to exact evidence;
- a qualified claim with supporting and counterevidence;
- non-empty dossier and Mermaid visualization;
- passed audit and completion validation.

Negative tests block completion when:

- a claim references a missing source or evidence record;
- supporting evidence is unverified;
- an exact term is unverified or not linked to exact-quotation evidence;
- a completed concept dossier lacks a selected primary-core source or required query history.

### Durable resumption

- each substantive inquiry is isolated under `research/runs/<run-id>/`;
- request, state, plan, queries, sources, source notes, terms, evidence, claims, dossier, visualization, and audit files are created;
- run summaries expose route, profile, stage, status, counts, next actions, and unresolved questions;
- session context prioritizes the newest active semantic run rather than legacy framework state.

### Source and permission policy

- built-in web search and fetch are available to the research controller;
- Academic Tools remains available for scholarly metadata and citation traversal;
- Zotero normal access is an explicit read-only subset;
- Zotero whole-document retrieval and create/update/delete/add/remove/merge families are denied;
- exact wording requires bounded source recheck or exact-match verification;
- model memory, snippets, abstracts, and generated summaries cannot independently verify quotations.

### Packaging and installed-wheel smoke test

A wheel was built and installed in a fresh Python 3.13 virtual environment. From the installed wheel, the test:

1. created a new project with `mros init --with-claude`;
2. verified the installed repository and Claude harness;
3. confirmed the concept-dossier profile and **20 schemas** were packaged;
4. created an `uncreative-writing-test` run from an ordinary-language request;
5. inferred/stored `deep`, `concept-dossier`, web and academic lanes, Zotero exclusion, and exact-term requirements;
6. ran `mros run-summary` and `mros run-validate` successfully;
7. created a handoff and passed installed-project phase-stop verification.

A fresh initialized project is not expected to pass `mros audit --release` before it contains a release artifact; that command correctly reported the missing release as a blocker in the clean-install project.

### Release archive isolation

The release packager was run while fake local `.mcp.json`, `.env.local`, root `.claude/settings.local.json`, and packaged-template `settings.local.json` files contained a sentinel secret. The ZIP contained none of those paths or sentinel bytes, and its CRC check passed. The final ZIP was then extracted into a fresh directory, where compilation, the full 94-test suite, repository verification, phase-stop verification, release audit, schema freshness, and event-chain verification were rerun.

## Compatibility checked

- Package requires Python 3.11 or newer.
- CI configuration includes Python 3.11, 3.12, 3.13, and 3.14.
- The artifact was built and executed in this environment on Python 3.13.5.
- The user's local environment previously installed MROS on Python 3.14.3; v1.2 CI confirmation for Python 3.14 remains part of the migration PR.

## Explicit non-certification

Offline tests establish the orchestration and evidence-record contracts, not scholarly superiority. They cannot prove that:

- Claude Desktop will always auto-select the project skill for every phrasing;
- all web pages, scholarly providers, or local MCP services will be reachable;
- exact source pages will always be accessible;
- the resulting dossier is better than Claude's generic Deep Research;
- the user's Claude subscription will complete every deep run within one session.

Those claims remain gated by:

- `docs/live-certification.md` for semantic routing, web/scholarly tools, exact quotations, checkpoints, interruption, and resumption;
- `docs/benchmark-protocol.md` for source fitness, primary-source coverage, citation support, exact-term integrity, counterevidence, user effort, elapsed time, and usage.

V1.2 should be adopted for routine work only after three consecutive real inquiries complete without a blocking research-integrity failure and meet the documented benchmark threshold.
