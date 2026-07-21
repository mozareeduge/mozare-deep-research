# Claude model and effort routing

**Policy:** use capability aliases and observed quality, not a hard-coded marketing model number.

The project starts with the current `sonnet` alias at medium effort. The exact numbered model available in Claude Desktop, Claude Code web, a cloud provider, or a future release may differ. MROS must therefore remain functional on the current Sonnet offered by the client and benchmark phase-specific alternatives rather than assuming “Sonnet 5” or any other release is present.

## Routing matrix

| Work | Model | Effort | Reason |
|---|---|---|---|
| Narrow lookup | Sonnet | low | small, source-specific task |
| Broad source scouting | Haiku | low | bounded candidate mapping in an isolated context |
| Close reading and evidence qualification | Sonnet | medium | source context and interpretive precision matter |
| Claim construction and synthesis | Sonnet | medium | consequential reasoning without default overthinking |
| Fresh citation and scope verification | Sonnet | medium | independent integrity check |
| Exceptional unresolved judgment | current strongest available model | high | only after a compact evidence packet and only when materially useful |

## Rules

- Model effort is a routing decision, not a proxy for research quality.
- Do not use high effort for search, metadata handling, conversion, deduplication, quotation matching, or ledger updates.
- Do not use `max`, `ultracode`, long-running agent teams, or an uncontrolled worker swarm as defaults.
- Do not hand an expensive model the complete corpus when bounded source packets suffice.
- Escalate only after a defined quality failure, not pre-emptively.
- Benchmark the available Haiku and Sonnet configurations on real source screening, evidence qualification, quotation, synthesis, and audit tasks.
- Record client model, effort, elapsed time, corrections, and usage observations in benchmark reports.
