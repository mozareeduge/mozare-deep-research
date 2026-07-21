# Threat model

| Risk | Control |
|---|---|
| Wrong research workflow selected | CLAUDE.md requires the project `research` skill; generic `deep-research` skills are denied |
| User forced to operate internal phases | one semantic front door; no numbered command sequence |
| Zotero data mutation | write tool families denied; local read-only mode |
| Context blowout from whole papers | Zotero full-text denied; bounded pages/sections preferred |
| Search snippets treated as evidence | explicit evidence policy and final audit |
| Exact quotation from memory | bounded re-open and verification requirement |
| Agent swarm and usage exhaustion | one scout and one verifier sequentially; no agent teams |
| One inquiry overwrites another | isolated `research/runs/<run-id>/` directories |
| Framework modified during research | CLAUDE.md forbids framework/template maintenance in research runs |
| Hidden source dependence | source and evidence records retain lane, identity, and limitations |
| False completeness | audit may pass with explicit limits; unresolved central gaps remain visible |
| Malicious or irrelevant web content | source fitness, direct-source preference, and independent verification |
| Local configuration leakage | `.mcp.json`, `.env`, settings.local, corpora, indexes, and tool clones remain ignored |
