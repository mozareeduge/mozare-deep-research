# Setup

## 1. Install the repository

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
python -m pytest
python -m mros verify .
```

## 2. Open the repository in Claude Code

Use a current Claude Code or Claude Desktop Code version that supports project skills, custom subagents, project hooks, and built-in `WebSearch`/`WebFetch`. The repository uses the current `sonnet` alias rather than requiring a specific numbered Sonnet release.

## 3. Configure MCP servers locally

Review `.mcp.json.example`, copy it to `.mcp.json`, and keep that file uncommitted.

For Academic Tools, clone the pinned upstream tag and run `uv sync`, then replace `ABSOLUTE_PATH_TO_ACADEMIC_TOOLS_MCP` with the real local path. The upstream-supported command is:

```text
uv run --directory <path> python -m academic_tools_mcp.server
```

For Zotero, keep `ZOTERO_LOCAL=true`, start Zotero 7+, and enable the local API. Do not add a Zotero API key for local use.

## 4. Verify the integrations

Confirm that Claude can:

- run one bounded academic identifier lookup;
- search one known Zotero item;
- inspect metadata and child attachments;
- read a bounded page range;
- use built-in web search and fetch;
- not call Zotero whole-document or write tools.

## 5. Start research

Ask the real question in ordinary language. Do not invoke a numbered phase or generic `/deep-research` skill. Claude should automatically use the project `research` skill and create a durable run when needed.
