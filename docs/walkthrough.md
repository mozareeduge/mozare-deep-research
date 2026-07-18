# Minimal end-to-end walkthrough

This example shows the mechanics without prescribing a topic.

## 1. Frame

Run `/00-frame` and complete `research/contract.yaml` with one bounded purpose, one target decision, scope, exclusions, audience, output, uncertainty policy, and budget.

## 2. Map questions

Run `/20-question-map`. Create one central question and any prerequisite leaf questions in `research/questions.yaml`. Each question declares acceptable evidence, counter-search requirements, and a stop rule.

## 3. Discover

Run `/30-discover` for one leaf question. Execute a bounded query family and append every exact query to `queries/ledger.jsonl`. Normalize candidate metadata into `sources/manifests/sources.yaml`.

## 4. Screen and acquire

Run `/40-screen`, then `/50-acquire`. Include, exclude, or mark uncertain from compact records. Copy or link accepted local files into the corpus, hash them, record access and transformation status, and preserve rejected candidates with reasons.

## 5. Retrieve and verify evidence

Run `/60-evidence`.

1. Search the accepted corpus through Zotero, Academic Tools, PaperQA retrieval-only mode, or a local index.
2. Select bounded candidate passages.
3. Read the source pages/section around each candidate.
4. Store exact text and location in `evidence/spans/spans.yaml`.
5. Run quotation verification.
6. Independently qualify accepted passages into `evidence/cards/cards.yaml`.

## 6. Challenge

Run `/70-challenge`. Search for counterexamples, alternate explanations, conflicting versions, access limits, or familiar associations that could make the proposed result look more specific than it is.

## 7. Build claims

Run `/80-claims`. Create atomic wording in `claims/claims.yaml`. Supporting, refuting, and qualifying evidence remain explicit. Unsupported or contested states are legal; silently overstated prose is not.

## 8. Plan and draft

Run `/90-synthesis-plan`, obtain human approval, then `/100-draft`. A section receives only its brief, approved claims, assigned evidence, necessary definitions, uncertainty language, and a compact continuity note.

## 9. Audit

Run `/110-audit`, followed by:

```bash
python -m mros audit . --release
python -m mros verify .
```

Repair claims or reopen search rather than patching prose around a failed citation.

## 10. Translate and hand off

Use `/120-design-translation` when research must produce an interface, data structure, technical architecture, prototype, or evaluation. Use `/130-handoff` before clearing context or ending the phase, then verify:

```bash
python -m mros verify . --phase-stop
```
