# MROS v1.2.0 — Concept-dossier controller and exact-term research state

## Release purpose

V1.2 strengthens the natural-language research machine for inquiries whose value depends on exact terminology, reference-specific wording, conceptual history, and a durable research note dossier.

The user still submits one rough inquiry. The machine now infers both research depth and output profile, logs searches, assigns source roles, reads selected materials, records verified exact terms, challenges claims, creates a dossier and visualization, and audits completion.

## Major additions

- `concept-dossier` output profile;
- exact query ledger and term ledger;
- source roles and reading status;
- explicit route, stage, budget, progress, and user-visible status;
- source-note and visualization artifacts;
- gap-directed low-gain stopping;
- profile-sensitive completion gates;
- compact run summary and cleaner session resumption;
- synthetic end-to-end Uncreative Writing flow test;
- full 0-100 simulation for nontechnical users.

## Preserved decisions

- one automatic project-owned `research` skill;
- no user-operated phases or slash commands;
- built-in web plus Academic Tools and optional read-only Zotero;
- no paid model API dependency;
- no uncontrolled agent swarm;
- no whole-document or mutating Zotero operations;
- PaperQA remains optional retrieval-only infrastructure;
- deterministic validation does not claim intellectual correctness.

## Certification boundary

Offline tests certify package, record, permission, and synthetic flow contracts. Live research quality, source access, automatic routing, elapsed time, and superiority over generic deep research remain benchmark-gated in the user's installed Claude environment.
