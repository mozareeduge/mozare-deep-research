# MROS comparative research benchmark

## Purpose

MROS should be retained only if one rough inquiry produces materially stronger, more inspectable research than the available generic research workflow without excessive time, prompting, or subscription usage.

## Comparison

Run the same inquiry in fresh sessions:

- **Baseline:** generic Claude research or `/deep-research` outside this project;
- **MROS:** one ordinary-language request in this repository.

Do not add hidden corrective prompts. Record model, effort, tools, elapsed time, visible user interventions, candidate and selected source counts, and interruptions.

## Primary concept-dossier case

> Gather up a research note dossier around the concept “uncreative writing” with exact terms and wording and concepts introduced and used by references.

Evaluate whether each route finds and reads the source roles needed for a historical and contested concept account, preserves reference-specific wording, and distinguishes primary formulation, interpretation, criticism, and later reception.

## Metrics, 0-4

| Dimension | 0 | 4 |
|---|---|---|
| User effort | repeated workflow prompting | one rough inquiry |
| Route/profile selection | wrong or generic | correct depth and deliverable profile |
| Search diversity | repeated narrow queries | distinct strategies and citation-chain coverage |
| Source fitness | weak or homogeneous | object-appropriate primary, scholarly, critical, and reception sources |
| Primary-source coverage | absent or indirect | central primary texts directly consulted |
| Exact-term integrity | paraphrase/memory/snippet | source-specific verified wording and locations |
| Citation support | missing or misaligned | consequential claims accurately supported |
| Conceptual specificity | merged generic vocabulary | reference-specific terms and differences preserved |
| Counterevidence | absent | credible criticism and alternative chronology integrated |
| Source independence | repeated citation chain treated as confirmation | dependence identified and managed |
| Analytical coverage | major terrain absent | formation, boundaries, disputes, and later reception covered |
| Uncertainty | false closure | access, chronology, and unresolved questions explicit |
| Deliverable quality | generic report | clear, genre-fit research-note dossier and useful visualization |
| Durability | chat only | resumable query/source/term/evidence/claim/audit trail |
| Efficiency | uncontrolled search or agents | bounded batches and low-gain stop logic |

## Blocking failures

- fabricated citation or quotation;
- term wording not rechecked from a bounded source;
- a central claim unsupported by its cited source;
- model-generated material presented as evidence;
- explicit source exclusion ignored;
- user required to operate internal phases;
- unexplained usage explosion or uncontrolled agent swarm;
- completed run missing query, term, evidence, claim, or audit records required by its profile.

## Acceptance threshold

Before routine replacement of the generic baseline:

- no blocking failure in three consecutive runs;
- mean score at least 3.2/4;
- exact-term integrity and citation support at least 3.5/4;
- user effort at least 3.5/4;
- no more than 1.5× baseline elapsed time unless source and audit quality are materially superior;
- completed run passes its deterministic profile gates.
