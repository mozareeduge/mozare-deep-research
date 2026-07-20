# MROS v1.1 revision analysis

## Product diagnosis

The live trial failed at the product boundary even though the v1 software tests passed. The intended product was “state a rough inquiry and receive strong, inspectable research.” The implemented product was “operate a repository of fourteen research commands and maintain typed records.” Those are not the same product.

The failure was compositional rather than caused by one bad prompt. Provenance, evidence states, counter-search, schema validation, phase separation, model routing, handoffs, Zotero, Academic Tools, and audit were individually defensible. Combined as user-visible obligations, they consumed attention before research began and left no component responsible for interpreting an ordinary request and carrying it to completion.

## Evidence from live tests

| Observation | What it demonstrates |
|---|---|
| A Baetens lookup found the source but used whole-document retrieval | safe Zotero tools were pre-approved, not actually exclusive |
| The exact-wording follow-up relied on already retrieved conversation text | the evidence policy existed but was not enforced by the active route |
| A broad inquiry ran another `/deep-research` skill | every MROS skill was manual and no project semantic front door competed for the request |
| The user had to type `/00-frame` and a long structured prompt | internal architecture had become the interface |
| Framing read schemas for a long time before writing anything | schema completion preceded research value |
| Claude recommended nonexistent `/01-search` | fragmented phase names were not owned by an orchestrator |
| Root contract/question files were repurposed for one topic | framework state and inquiry state were coupled |
| `/30-discover` described the web but lacked built-in web tools | conceptual architecture and executable tool surface diverged |

## Root-cause-to-fix matrix

| Root cause | Surgical correction | Preserved capability |
|---|---|---|
| No natural-language controller | one auto-selected project `research` skill | rich method remains in supporting policies |
| Fourteen manual phases | five internal adaptive routes | all old phase text archived verbatim |
| Generic skill collision | deny generic `deep-research`; project instructions prefer `research` | baseline can still be tested outside this project |
| Web route absent | pre-approve `WebSearch` and `WebFetch` | Academic Tools and Zotero remain complementary |
| Safe-tool allowlist mistaken for restriction | explicit deny rules for whole-document and write families | bounded Zotero metadata/page reading retained |
| Shared root inquiry state | unique `research/runs/<run-id>/` | v1 root records retained for compatibility |
| Schema ceremony before work | lightweight run state and JSONL records | strict Pydantic validation remains at boundaries |
| Per-turn validation overhead | validate at initialization/completion, not every turn | explicit run/release gates retained |
| Too many workers | one optional scout and one verifier, sequential | context isolation retained without a swarm |
| Hard-coded model release assumptions | current aliases plus empirical phase benchmark | effort routing retained |
| Software-only test suite | live semantic-routing and comparative research benchmark | all offline tests retained and extended |

## Why the new composition is smaller but stronger

The redesign does not remove research rigor. It moves rigor to the point where it is useful:

- source selection rules guide search, not the user's prompt;
- schemas validate durable records, not the initial conversation;
- exact quotation checks occur when a quote is promoted;
- challenge search occurs before central claims settle;
- audit occurs before completion;
- state is persisted after meaningful batches;
- the user sees a checkpoint only when a decision is genuinely consequential.

This distributes work according to comparative advantage: Claude interprets, routes, reads, compares, and synthesizes; deterministic code validates identifiers and record links; MCP and web tools retrieve; isolated workers compress broad search and audit; the user supplies purpose and resolves only material ambiguity.

## Deliberate non-goals

V1.1 does not attempt to create a fully autonomous academic authority, ingest every paper, run a large agent team, or promise superiority from architecture alone. The machine becomes a candidate replacement for generic deep research only after the live benchmark shows better source fitness, citation support, quotation integrity, counterevidence, and durability without disproportionate time or usage.

## Acceptance decision

Do not judge v1.1 by whether it can create files or pass schema tests. Judge it by whether a user can ask the original rough “Uncreative Writing” inquiry in one message and receive a stronger, more traceable result than the generic workflow, with no internal command management. The benchmark protocol makes that decision explicit.
