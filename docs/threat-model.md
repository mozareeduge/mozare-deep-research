# Threat model

## Protected assets

- credentials and private library data;
- unpublished sources and user notes;
- source/version identity;
- exact quotations and locations;
- evidence and claim status;
- human approval boundaries;
- event and decision history.

## Main risks and controls

| Risk | Control |
|---|---|
| Prompt injection in retrieved content | treat sources as data; restrict tools; no source may change system policy |
| Destructive Zotero operation | read-only default; writes excluded from ordinary skills; human approval |
| Context flooding | bounded passages; full-text tool denied; compact session context |
| Citation laundering | direct/indirect classification; source-reference verification queue |
| Generated content upgraded to evidence | model validators and audit blockers |
| Metadata record used for content claim | access-status validator and audit blocker |
| Tampered history | hash-chained event log and verification |
| Silent schema drift | Pydantic validation and test suite |
| MCP/package supply-chain change | pin versions in deployment; review release notes; workspace trust |
| Credential leakage | deny `.env` and `secrets/**`; `.mcp.json` gitignored |
| Automated overreach | manual skills, max turns, phase budgets, repository-validity stop gate, and explicit phase handoff |

## Non-goals

MROS does not sandbox third-party MCP servers. Run them under least privilege and audit their current source or release before upgrades.


## Stop-hook boundary

The automatic Stop hook validates repository invariants only. It does not require a new handoff after every conversational turn. Phase completion is explicit through `/130-handoff` and `python -m mros verify . --phase-stop`.
