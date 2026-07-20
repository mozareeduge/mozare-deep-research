# MROS v1 phase skills (archived)

These skills are preserved for maintenance and historical comparison. They are no longer active user-facing commands in v1.1.

## 00-frame

```markdown
---
name: 00-frame
description: Use at the start of a project or consequential phase to establish purpose, decisions, scope, exclusions, uncertainty, budgets, and approval gates.
disable-model-invocation: true
model: sonnet
effort: medium
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash(python -m mros *)
  - Bash(python -m mros verify *)
---

# Frame a research run

Read the user request and current project state. Do not search yet. Update `research/contract.yaml`, then create or revise `research/questions.yaml` as a dependency-aware set of bounded questions. Each question must state why it matters, what decision it informs, acceptable evidence, counter-search requirement, and a stop rule. Mark assumptions explicitly. Ask for human approval only where the scope or target decision remains materially ambiguous. Run `python -m mros validate .` before returning.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 10-intake

```markdown
---
name: 10-intake
description: Use when files, notes, links, transcripts, generated text, or source records enter the project.
disable-model-invocation: true
model: sonnet
effort: low
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash(python -m mros *)
  - Bash(python -m mros verify *)
---

# Intake research material

Receive the supplied material without turning it into a final argument. Record provenance, access status, version, direct versus interpretive or generated components, current allowed uses, what it cannot support, required verification, and destination. Preserve originals unchanged. Add or update records in `sources/manifests/sources.yaml`; write consequential changes to the event log. Run validation.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 100-draft

```markdown
---
name: 100-draft
description: Use to compose a section or release only after an approved outline and evidence assignment exist.
disable-model-invocation: true
model: sonnet
effort: medium
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash(python -m mros *)
  - Bash(python -m mros verify *)
---

# Draft from approved claims

Use only the section brief, approved claims, assigned evidence, relevant definitions, and a compact continuity memo. Move from concrete material to concept, mechanism, consequence, and stake as the genre requires. Preserve degrees of certainty. Keep internal claim IDs during drafting. Do not introduce new factual claims or citations; route them back to discovery and evidence.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 110-audit

```markdown
---
name: 110-audit
description: Use before treating a section, decision, or release as complete.
disable-model-invocation: true
model: sonnet
effort: medium
allowed-tools:
- Read
- Grep
- Glob
- Write
- Edit
- Bash(python -m mros *)
- Bash(python -m mros verify *)
- mcp__zotero__zotero_get_item_metadata
- mcp__zotero__zotero_read_pdf_pages
- mcp__zotero__zotero_export_bibliography
---

# Audit claims, citations, and release

Run `python -m mros audit . --release` for a release, or `python -m mros validate .` during research. Then use the citation-auditor in a fresh context. Check exact support, location, source identity, directness, independence, challenges, scope, current facts, placeholders, omissions, and genre. Block only research-integrity or stated-requirement failures.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 120-design-translation

```markdown
---
name: 120-design-translation
description: Use when accepted research must produce an interface, workflow, data structure, architecture, prototype, or evaluation.
disable-model-invocation: true
model: sonnet
effort: medium
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash(python -m mros *)
  - Bash(python -m mros verify *)
---

# Translate research into design

For each consequential decision, record: source condition, accepted claim, operation or mechanism, user need or behavior, design consequence, technical consequence, alternatives, selected option, test, risks, and reversibility. An analogy is useful only when it produces a concrete mechanism or evaluative condition and preserves relevant differences. Add a `DesignDecision` record and link it to claims and evidence.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 130-handoff

```markdown
---
name: 130-handoff
description: Use before clearing context or ending a coherent phase.
disable-model-invocation: true
model: sonnet
effort: low
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash(python -m mros *)
  - Bash(python -m mros verify *)
---

# Close a phase cleanly

Update state files, run validation, and write `research/handoff.yaml`. Record objective completed, files changed, sources/evidence/claims affected, decisions, unresolved items, failed routes, next actions, routes not to repeat, and verification evidence. The receipt must be sufficient for a fresh session without replaying the conversation.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 20-question-map

```markdown
---
name: 20-question-map
description: Use to decompose an approved purpose into questions whose dependencies, evidence requirements, and decisions are explicit.
disable-model-invocation: true
model: sonnet
effort: medium
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash(python -m mros *)
  - Bash(python -m mros verify *)
---

# Build the question map

Work from the approved contract. Build a directed question set, not a list of broad topics. Prioritize leaf questions that unlock later decisions. Include factual, bibliographic, conceptual, mechanism, comparison, method, design, technical, evaluation, and challenge questions only where needed. Avoid numeric confidence scores. Record criticality, minimum direct evidence, minimum independent groups, languages, source preferences, and stopping conditions.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 30-discover

```markdown
---
name: 30-discover
description: Use after questions and source policies are approved to search scholarly
  providers, the local library, official sites, archives, or repositories.
disable-model-invocation: true
model: sonnet
effort: low
allowed-tools:
- Read
- Grep
- Glob
- Write
- Edit
- Bash(python -m mros *)
- Bash(python -m mros verify *)
- mcp__academic_tools__*
- mcp__zotero__zotero_search_items
- mcp__zotero__zotero_semantic_search
- mcp__zotero__zotero_get_item_metadata
- mcp__zotero__zotero_get_collection_items
- mcp__zotero__zotero_find_related_papers
---

# Run bounded discovery

Search one question leaf at a time. Generate bounded query families: broad discovery, exact identifier, terminology variants, backward and forward citations, challenges, non-English variants, and local-corpus search. Use the source object to choose the retrieval lane. Record every executed query in `queries/ledger.jsonl`, including provider, filters, batch, candidates, selections, rejections, and reasons. Do not draft findings from search snippets.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 40-screen

```markdown
---
name: 40-screen
description: Use to apply explicit inclusion and exclusion criteria to a compact candidate batch.
disable-model-invocation: true
model: haiku
effort: low
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash(python -m mros *)
  - Bash(python -m mros verify *)
---

# Screen candidate sources

Use the source-screener for straightforward batches. Screen from title, abstract, provenance, access, and declared criteria only. Return include, exclude, or uncertain. Do not infer the full argument from metadata. Route conceptually dense, multilingual, unusual, central, or ambiguous sources to Sonnet or human review. Preserve rejection reasons.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 50-acquire

```markdown
---
name: 50-acquire
description: Use after screening to preserve accepted source versions and prepare
  bounded local access.
disable-model-invocation: true
model: sonnet
effort: low
allowed-tools:
- Read
- Grep
- Glob
- Write
- Edit
- Bash(python -m mros *)
- Bash(python -m mros verify *)
- mcp__academic_tools__download_pdf
- mcp__academic_tools__convert_paper
- mcp__academic_tools__import_paper
- mcp__zotero__zotero_get_item_metadata
- mcp__zotero__zotero_get_item_children
- mcp__zotero__zotero_read_pdf_pages
---

# Acquire and snapshot the corpus

Acquire only accepted or high-potential sources. Preserve originals, hashes, versions, rights and access status, conversion tool/version, and extraction limitations. Prefer metadata, abstract, section index, selected pages, then full conversion only when justified. Create a corpus snapshot identifier before evidence work. Do not place credentials in the repository.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 60-evidence

```markdown
---
name: 60-evidence
description: Use to retrieve passages, verify exact text and locations, and create
  evidence records for one question.
disable-model-invocation: true
model: sonnet
effort: medium
allowed-tools:
- Read
- Grep
- Glob
- Write
- Edit
- Bash(python -m mros *)
- Bash(python -m mros verify *)
- mcp__academic_tools__get_paper_section
- mcp__academic_tools__get_paper_sections
- mcp__academic_tools__find_in_paper
- mcp__zotero__zotero_semantic_search
- mcp__zotero__zotero_get_item_metadata
- mcp__zotero__zotero_get_annotations
- mcp__zotero__zotero_read_pdf_pages
---

# Build verified evidence

Retrieve candidate passages with deterministic or local ranking before model interpretation. Keep passages separate and retain source IDs, locations, context, and scores. Verify quotations with `python -m mros quote-verify`. Then use the evidence-reviewer to qualify accepted spans. A passage may be rejected or deferred. Generated descriptions, summaries, and search snippets cannot upgrade themselves into source evidence. Validate the project after updates.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 70-challenge

```markdown
---
name: 70-challenge
description: Use after initial evidence exists to search for counterexamples, limits,
  alternatives, and simpler explanations.
disable-model-invocation: true
model: sonnet
effort: medium
allowed-tools:
- Read
- Grep
- Glob
- Write
- Edit
- Bash(python -m mros *)
- Bash(python -m mros verify *)
- mcp__academic_tools__*
- mcp__zotero__zotero_search_items
- mcp__zotero__zotero_semantic_search
- mcp__zotero__zotero_get_item_metadata
- mcp__zotero__zotero_read_pdf_pages
- mcp__zotero__zotero_find_related_papers
---

# Challenge central claims

For each central question or proposed claim, define what would weaken, narrow, redirect, or falsify it. Run at least one explicit challenge query where required, record it in the query ledger, and create refuting or qualifying evidence records when found. Test whether familiar vocabulary or conventional associations are creating false force. Absence of counterevidence is not proof of the claim.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 80-claims

```markdown
---
name: 80-claims
description: Use to convert accepted evidence and tested candidate links into atomic, qualified claim records.
disable-model-invocation: true
model: sonnet
effort: medium
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash(python -m mros *)
  - Bash(python -m mros verify *)
---

# Construct scoped claims

Create one scoped proposition per claim. Link supporting, refuting, and qualifying evidence; distinguish direct from indirect support; state assumptions, inference type, uncertainty, and dependencies. A candidate link can be promoted only when evidence supports the stated use. Supported and contested claims must satisfy their schemas. Do not promote a claim merely because it is fluent or theoretically attractive.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```

## 90-synthesis-plan

```markdown
---
name: 90-synthesis-plan
description: Use after critical questions meet their evidence gate to design the target document or artifact.
disable-model-invocation: true
model: sonnet
effort: medium
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash(python -m mros *)
  - Bash(python -m mros verify *)
---

# Plan an evidence-led output

Restate audience, genre, purpose, and the minimum complete path. Build the outline from approved claims and unresolved questions, then assign evidence. Every section needs a function, claim IDs, evidence IDs, and an output budget. Unsupported sections become explicit gaps rather than model-memory prose. Record excluded material and its destination.

## Completion contract

- Update typed project records rather than leaving decisions only in chat.
- Preserve explicit unknown and rejected states.
- Return a compact decision summary and the next bounded action.

```
