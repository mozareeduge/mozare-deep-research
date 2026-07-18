# MROS project instructions

## Research integrity

1. Start each work unit from a stated question, target decision, scope, and exclusions.
2. Keep source text, prior scholarship, user interpretation, calculations, and generated material distinct.
3. Record source identity, version, access route, transformation history, and exact location where available.
4. Treat each new connection as a candidate until supporting and challenging evidence have been reviewed.
5. Never fill missing facts with plausible language. Record `unknown`, `not accessed`, or `not verified`.
6. A formal claim must resolve to accepted evidence. Its wording must not exceed that evidence.
7. For central claims, seek credible alternatives, counterexamples, and simpler explanations.
8. Use local scripts for normalization, deduplication, exact matching, validation, and accounting.
9. Write consequential state changes to disk before ending a phase.
10. Preserve rejected and deferred routes with a reason and a reopening condition.
11. Draft only from approved claims and assigned evidence.
12. Human approval is required for scope, central-claim promotion, destructive library changes, and final release.

## Operating rules

- Use Sonnet with medium effort by default. Phase skills override this where justified.
- Keep one coherent phase or question leaf per session.
- Use a subagent only when it isolates a bounded read-heavy review; default to one subagent at a time.
- Prefer page/section reads and passage packets over complete documents.
- Never use Zotero library-write operations unless a manually invoked maintenance workflow has explicit approval.
- PaperQA is retrieval-only in the default path; its generated answers are not accepted evidence.
- Before clearing context or ending a coherent phase, update `research/handoff.yaml` and run `python -m mros verify . --phase-stop`. Ordinary turns require only repository validity.
- Before release, run `python -m mros audit . --release`.

## Commands

- Install: `python -m pip install -e .`
- Tests: `python -m pytest`
- Validate research state: `python -m mros validate .`
- Coverage: `python -m mros coverage .`
- Compile/check method: `python -m mros compile-method .`
- Full repository verification: `python -m mros verify .`
