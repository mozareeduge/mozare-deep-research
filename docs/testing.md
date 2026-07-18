# Testing and verification

## Offline tests

```bash
python -m pytest
python -m compileall -q src tests scripts
python -m mros verify .
```

The tests cover:

- model invariants;
- identifier normalization;
- Unicode-aware quote matching;
- event-chain integrity and tamper detection;
- claim/evidence referential integrity;
- generated and metadata-only evidence firewalls;
- critical-question coverage;
- method compilation and prohibited vocabulary checks;
- CLI project initialization and audit.

## Live integration certification

Not performed in the packaged environment because it requires the user's library, credentials, Claude account and network.

Run locally:

1. `claude mcp list` and authenticate servers.
2. Search one known paper through Academic Tools.
3. Search the same item in Zotero and read a two-page range.
4. Record both retrievals in a temporary query ledger.
5. Verify one exact quotation from a normalized local file.
6. Build an optional PaperQA index for three known documents and compare top passages against Zotero/local retrieval.
7. Confirm no Zotero write tool is available in the normal workflow.
8. Run a full evidence, claim, draft and audit cycle on a small gold set.
