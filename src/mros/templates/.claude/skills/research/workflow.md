# Adaptive research controller

## Route and profile

Choose the route by the work required, not by trigger words alone. Infer the output profile from the requested artifact.

| Route | Typical need | Default depth |
|---|---|---|
| lookup | source existence, identifier, narrow fact | 1-3 authoritative records |
| close-read | exact wording or interpretation from named sources | bounded pages/sections |
| brief | focused evidence-backed explanation | 4-8 strong sources |
| deep | literature review, conceptual history, dossier | map 20-40 candidates; select roughly 8-18 |
| design | research ending in decisions or prototypes | evidence plus decision records |

These are operating ranges, not quotas.

## Internal controller loop

1. **Route:** infer purpose, deliverable, scope, exclusions, source lanes, exact-wording needs, and budget.
2. **Map:** create a compact set of coverage slots and source roles.
3. **Discover:** run distinct bounded query strategies and record every query.
4. **Select:** remove duplicates and weak versions; choose sources for explicit roles.
5. **Read:** move from metadata to bounded section to close reading only when justified.
6. **Extract:** record exact terms, evidence, limits, and source-specific notes.
7. **Challenge:** search for criticism, alternative chronology, competing definitions, and source dependence.
8. **Synthesize:** build the output from verified evidence and term records.
9. **Verify:** use a fresh verifier on the most consequential claims and quotations.
10. **Deliver:** validate, save, and return the requested result.

## Progress and latency policy

- Create the run and start the first useful research action in the same turn.
- Do not spend a full turn reading schemas or general documentation.
- After each meaningful batch, update `state.yaml`, counts, `next_actions`, and `user_visible_status`.
- Give the user short progress statements such as “mapping core sources,” “reading primary texts,” “checking criticism,” and “auditing quotations.” Do not expose internal command syntax.
- If a tool or subprocess is stalled, terminate it and record the blocker rather than silently waiting.
- If usage or context is near its limit, checkpoint the active run and stop with a simple continuation instruction. A fresh session should resume automatically from the newest active run.

## Gap-directed iteration

After each discovery or reading batch, ask internally:

- Which required source role or coverage slot is still empty?
- Did the batch add a new primary source, exact term, contradiction, or materially different interpretation?
- Are results repeating the same source cluster or secondary citation chain?
- Is a central source only indirectly available?

Continue with a targeted gap search when the answer would materially alter the dossier. Stop after two bounded low-gain searches when remaining gaps are explicit.

## Interaction policy

- Never ask the user to invoke a next phase.
- Never invent command names.
- Do not ask approval for ordinary source selection or routing.
- Ask one compact question only for consequential ambiguity, inaccessible central material requiring a substitute, privacy/safety concerns, or a real tool/usage blocker.
