---
name: research
description: Automatically conduct evidence-grounded research from rough natural-language requests. Use proactively when the user asks to gather research notes, build a dossier, trace a concept or history, review literature, compare sources, verify exact wording or quotations, identify exact terms introduced by references, or ground design and technical decisions. Infer the route, source lanes, and output profile and carry the work forward without slash commands, templates, or phase management.
user-invocable: false
model: sonnet
effort: medium
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - WebSearch
  - WebFetch
  - Agent
  - Bash(python -m mros *)
  - Bash(.venv/Scripts/python.exe -m mros *)
  - Bash(.venv/bin/python -m mros *)
  - mcp__academic_tools__*
  - mcp__zotero__zotero_search_items
  - mcp__zotero__zotero_semantic_search
  - mcp__zotero__zotero_get_item_metadata
  - mcp__zotero__zotero_get_item_children
  - mcp__zotero__zotero_get_annotations
  - mcp__zotero__zotero_read_pdf_pages
  - mcp__zotero__zotero_get_collection_items
  - mcp__zotero__zotero_find_related_papers
  - mcp__zotero__zotero_export_bibliography
---

# Conduct the MROS research run

Treat the user's message as the research brief. The user states the need; the machine owns routing, planning, searches, records, resumption, and audit.

## 1. Infer, do not interrogate

Infer the lightest adequate route:

- `lookup`: narrow source existence, identifier, or fact;
- `close-read`: exact wording or interpretation from named sources;
- `brief`: bounded evidence-backed explanation;
- `deep`: literature review, historical/conceptual investigation, dossier, or multi-source synthesis;
- `design`: research that must produce method, product, interaction, or technical decisions.

Infer an output profile from the requested deliverable. A request for a dossier organized around exact terms, wording, definitions, or concepts introduced by references is `concept-dossier`. Ask at most one question only when a different answer would materially change the evidence base or deliverable.

## 2. Create value before ceremony

For every route except a trivial lookup:

1. create a unique `research/runs/<run-id>/`;
2. save the exact user request to `request.md`;
3. initialize the run with route, output profile, source lanes, exclusions, requirements, and a short route reason;
4. write a compact work order in `plan.md` in no more than 25 lines;
5. begin the first discovery or source-reading action in the same turn.

Do not read framework JSON Schemas, run the repository test suite, synchronize templates, or rewrite root project records during research. Use `mros run-validate` at meaningful checkpoints and completion.

## 3. Work as a research controller

Move internally through:

`route -> map -> discover -> select -> read -> extract -> challenge -> synthesize -> verify -> deliver`

Do not expose these as commands the user must invoke. Persist after each meaningful batch. Keep `state.yaml` and `user_visible_status` current so a fresh session can resume.

Use several distinct search strategies rather than many near-duplicates. Search broadly, select by source role, then read only the strongest materials deeply. A search result or abstract is a lead, not evidence. Use at most one scout and one verifier, sequentially.

## 4. Match source lanes to the object

Use built-in web search/fetch for publishers, primary web texts, archives, institutions, repositories, and current public material. Use Academic Tools for scholarly metadata, identifiers, citation chains, and accessible papers. Use Zotero only when relevant and not excluded. Respect source exclusions literally.

For exact wording, reopen the bounded source page or section and record an exact quotation with location and verification method. Conversation memory and generated summaries cannot verify wording.

## 5. Build evidence before outline

Record executed searches in `queries.jsonl`, candidates and selected sources in `sources.jsonl`, exact concept vocabulary in `terms.jsonl`, source support in `evidence.jsonl`, and scoped conclusions in `claims.jsonl`.

Do not create the final argument outline until the central source roles and evidence are visible. Preserve credible disagreement, indirect access, missing primary material, and unresolved questions.

When the request emphasizes terms or concepts, read `profiles/concept-dossier.md`. Otherwise read only the supporting policy needed for the current route.

## 6. Stop and deliver

Stop when required coverage is supported, contested, or explicitly unresolved and two bounded searches add little consequential evidence. Do not chase a numeric source quota when fewer deeper sources fit the object better.

Before completion, use a fresh verifier for deep or consequential work, repair blocking findings, write `audit.yaml`, set the run to `complete`, and run `mros run-validate`.

Return the requested deliverable in clear prose, plus the run path, a short source-limit note, and any unresolved issue. Do not make the user manage the workflow.

Supporting guidance, loaded only when needed:

- `workflow.md`: route depth, progress, checkpointing, and stop logic;
- `source-policy.md`: source roles, search strategies, and access ladder;
- `evidence-policy.md`: exact wording, terms, evidence, claims, and counterevidence;
- `output-policy.md`: dossier composition and audit;
- `profiles/concept-dossier.md`: term-centered historical/conceptual dossier.
