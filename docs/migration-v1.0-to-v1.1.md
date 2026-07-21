# Migration from MROS v1.0 to v1.1

## What changes

V1.0 made the user operate fourteen numbered phase skills. V1.1 makes one project-owned `research` skill the semantic front door. A normal inquiry is sufficient; the skill selects a lookup, close-read, brief, deep, or design route and carries the internal workflow forward.

## What is preserved

- all v1 Python models, schemas, audit logic, quote verification, adapters, and tests;
- the methodology configuration and compiled integrity kernel;
- the exact contents of the fourteen phase skills and five earlier agents, preserved under `docs/archive/`;
- Zotero read-only policy, Academic Tools integration, and optional PaperQA adapter;
- release and installation history.

## What is replaced in the active Claude harness

- `.claude/skills/`: fourteen manual skills → one auto-selected `research` skill with supporting policy files;
- `.claude/agents/`: five phase workers → one bounded scout and one independent verifier;
- `.claude/settings.json`: adds built-in web tools, denies generic `deep-research`, denies Zotero whole-document/write operations, and removes per-turn Stop validation;
- root research state as the normal inquiry store → isolated `research/runs/<run-id>/` directories.

## Applying to an existing repository

1. Create a branch from the current `main`.
2. Back up local uncommitted research files.
3. Replace repository files with the v1.1 release contents while retaining uncommitted `.mcp.json`, `.env`, local Zotero data, and private corpus files.
4. Run `python scripts/sync_templates.py` only from a clean checkout. The script excludes `settings.local.json`, `.mcp.json`, secrets, and caches.
5. Install editable package, run tests, `mros compile-method .`, `mros verify .`, and `mros audit . --release`.
6. Start a fresh Claude session and issue one ordinary-language research request. Do not invoke a numbered command.

## Local files from v1.0

Do not commit or package:

- `.claude/settings.local.json`;
- `.mcp.json`;
- `.env*` except `.env.example`;
- `.venv/`, caches, model files, Zotero databases, or private corpus originals.

Existing root records such as `research/contract.yaml` remain for compatibility and forensic use. New inquiries should not overwrite them.
