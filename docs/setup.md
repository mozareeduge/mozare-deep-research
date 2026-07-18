# Setup

## 1. Install the repository

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m pytest
python -m mros verify .
```

## 2. Update and inspect Claude Code

```bash
claude update
claude --version
claude doctor
```

The repository expects current support for skill `model` and `effort`, custom subagent `maxTurns`, project hooks, and Sonnet 5.

## 3. Configure MCP servers locally

Review `.mcp.json.example`, then copy it:

```bash
cp .mcp.json.example .mcp.json
claude mcp list
```

Package commands can differ by upstream release. Confirm the installation command in each upstream README. Keep tokens and keys in environment variables or local settings.

## 4. Prepare Zotero

- Start Zotero.
- Enable local access required by the selected Zotero MCP mode.
- Test search, metadata and one bounded page read.
- Do not enable write tools during initial setup.

## 5. Start the first run

```bash
claude
```

Then invoke `/00-frame`. Complete and approve the contract before discovery.
