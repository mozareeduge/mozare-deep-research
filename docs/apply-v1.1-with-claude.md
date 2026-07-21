# Apply MROS v1.1 with Claude Code

This is a one-time repository migration prompt, not a research prompt. After migration, ordinary research inquiries should require no commands or templates.

Place `mozare-research-os-v1.1.0.zip` in the root of `mozareeduge/mozare-deep-research`, open a new Claude Code session on that repository, and provide:

```text
Migrate this repository from MROS v1.0 to the v1.1 release archive in the repository root.

Work on a new branch and open a draft pull request. Do not merge it.

Preserve all user-local/private files and do not commit `.mcp.json`, `.env*`, `.claude/settings.local.json`, Zotero data, private corpus files, virtual environments, caches, or model files.

Before changing files:
1. verify the archive integrity;
2. read README.md, docs/revision-analysis-v1.1.md, docs/migration-v1.0-to-v1.1.md, TEST_REPORT.md, and releases/mros-v1.1.0.md from the archive;
3. compare the release with current `main` and preserve any newer legitimate repository changes.

Apply the release so the repository has:
- one auto-selectable project skill named `research`;
- no active numbered research-phase skills;
- the old skills and agents preserved under `docs/archive/`;
- generic `deep-research` denied;
- built-in WebSearch/WebFetch enabled for MROS research;
- Zotero whole-document and write/destructive tools denied;
- isolated `research/runs/<run-id>/` state;
- the corrected Academic Tools MCP example;
- v1.1 package, schemas, tests, docs, and CI.

Do not change my local `.mcp.json`. Do not install PaperQA or paid APIs.

Run the documented full verification, including:
- schema and template checks;
- Python compilation;
- all tests with coverage;
- `mros validate .`;
- `mros verify .` and `--phase-stop`;
- release audit;
- event-chain verification;
- wheel build and clean wheel installation;
- wheel-installed `mros init --with-claude`;
- a lightweight run-init/run-validate smoke test;
- secret and tracked-file hygiene checks.

Use one fresh bounded reviewer after implementation. Fix only validated correctness, security, installation, or research-integrity gaps. Push the branch and open a draft PR with exact evidence. Do not begin a real research inquiry and do not merge.
```

After the PR is merged and the local checkout is updated, start a fresh Claude Desktop Local session and ask the real research question normally. Do not type `/00-frame`, `/deep-research`, or any numbered phase.
