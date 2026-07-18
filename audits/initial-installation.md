# MROS v1.0.0 Initial Installation Receipt

## Archive

| Field | Value |
|---|---|
| Archive | `mozare-research-os-v1.0.0.zip` |
| SHA-256 (computed) | `25cde48bbed261834f6cea64da0d4ccb62466783150ab0d296a7a369f4cce5f6` |
| Note | No `.sha256` companion file was included in the upload; hash was computed from the received archive |

## Installation

| Field | Value |
|---|---|
| Installation date | 2026-07-18 |
| Environment | Claude Code on the web (ephemeral Linux container) |
| OS | Linux 6.18.5 x86_64 |
| Python | 3.11.15 |
| Package version | mozare-research-os 1.0.0 |
| Branch | `claude/setup-mros-v1-5bdegu` |

## Commands executed

```bash
# Phase 1 – inspect
unzip -l <archive>
sha256sum <archive>

# Phase 2 – install source tree
cp -a <extracted>/mozare-research-os/. /home/user/mozare-deep-research/

# Phase 4 – environment
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'

# Compilation
.venv/bin/python -m compileall -q src tests scripts

# Tests
.venv/bin/python -m pytest                                 # 83 passed
.venv/bin/python -m pytest --cov=mros --cov-report=term-missing  # 76% coverage

# Schema and template checks
.venv/bin/python scripts/export_schemas.py --check         # 13 schemas current
.venv/bin/python scripts/sync_templates.py --check         # packaged harness current

# Repository verification
.venv/bin/python -m mros verify .                          # ok, 0 warnings
.venv/bin/python -m mros verify . --phase-stop             # ok
.venv/bin/python -m mros validate .                        # 0 issues
.venv/bin/python -m mros audit . --release                 # 0 blockers, 0 warnings
.venv/bin/python -m mros doctor .                          # all structural checks pass

# Build and wheel install
.venv/bin/python -m pip wheel . --no-deps -w dist          # mozare_research_os-1.0.0-py3-none-any.whl
python3 -m venv /tmp/mros-wheel-venv
/tmp/mros-wheel-venv/bin/python -m pip install dist/mozare_research_os-1.0.0-py3-none-any.whl
/tmp/mros-wheel-venv/bin/mros init /tmp/mros-wheel-project \
  --project-id wheel-project --title "Wheel Project" --with-claude
/tmp/mros-wheel-venv/bin/mros doctor /tmp/mros-wheel-project  # PASS
/tmp/mros-wheel-venv/bin/mros validate /tmp/mros-wheel-project  # PASS
```

## Test and verification results

| Check | Command | Result |
|---|---|---|
| Python compilation | `compileall -q src tests scripts` | PASS |
| Unit + contract tests | `pytest` | **83 passed, 0 failed** |
| Statement coverage | `pytest --cov=mros` | 76% (branch enabled) |
| JSON Schema freshness | `export_schemas.py --check` | PASS — 13 schemas |
| Packaged harness freshness | `sync_templates.py --check` | PASS |
| Full verification | `mros verify .` | PASS — 0 warnings |
| Phase-stop verification | `mros verify . --phase-stop` | PASS |
| Structural validation | `mros validate .` | PASS — 0 issues |
| Release audit | `mros audit . --release` | PASS — 0 blockers |
| Installation diagnostics | `mros doctor .` | PASS (PaperQA not installed — expected) |
| Wheel build | `pip wheel . --no-deps` | PASS |
| Clean wheel install | install in isolated venv | PASS |
| `mros init --with-claude` | from wheel | PASS |
| Hook entry points | `mros-session-context`, `mros-stop-gate` | present and executable |
| Secret scan | grep for credential patterns | No secrets in project files |
| Tracked-file hygiene | git status | .venv, dist, build correctly gitignored |

## Adversarial review findings and disposition

A bounded reviewer subagent inspected the installed repository against all stated invariants.

| Severity | File | Line | Finding | Disposition |
|---|---|---|---|---|
| HIGH | `.claude/agents/source-screener.md` | 4 | `Write` tool in a screening subagent. Agent instructions only say "Return one structured decision per source"; disk writes are a skill-level responsibility, not an agent responsibility. | **Fixed**: changed `tools: Read, Write` → `tools: Read` in agent file and matching template. |
| MEDIUM | `.claude/agents/source-screener.md`, `.claude/skills/40-screen/SKILL.md` | 6, 5 | `model: haiku` — reviewer claimed haiku is not an approved routing model. | **Dismissed**: `config/model-routing.yaml` line 7 explicitly designates `model: haiku, effort: low, escalate_to: "sonnet/low"` for `source-screening`. The README and release notes align with this design. Haiku is the intended cost tier for trivial screening batches. |

All other invariants reviewed as CLEAR: CLAUDE.md conciseness, Zotero read-only, PaperQA retrieval-only, evidence firewall, subagent bounds (after fix), skills manually invokable, no false live certification, tracked-file hygiene, no secrets, CI correctness, hook correctness.

## Changes made after extraction

1. **`.gitignore`** — appended `*.zip`, `*.sha256`, `*.whl` to prevent binary archives from being accidentally tracked.
2. **`.claude/agents/source-screener.md`** — removed `Write` tool from subagent (adversarial review finding: subagent returns decisions as text; writes are at skill/session level).
3. **`src/mros/templates/.claude/agents/source-screener.md`** — same change applied to the wheel-installable template.
4. **`audits/initial-installation.md`** — this file (installation receipt).

## Integrations that remain unverified

The following require the user's own credentials, running services, and local environment:

- **Claude Code** — real model invocation and subscription-limit behavior
- **Academic Tools MCP** — live network search, identifier resolution, PDF acquisition
- **Zotero MCP** — live library search, semantic index, PDF-page reading, permission enforcement
- **PaperQA** — corpus indexing, retrieval quality, embedding/reranking for the user's corpus
- End-to-end scholarly accuracy on the user's gold set

## Next steps for local live certification

Follow `docs/live-certification.md` exactly:

1. Install MROS in the research environment: `python -m pip install -e .`
2. Pin exact versions of Claude Code, Academic Tools MCP, Zotero MCP.
3. Run `claude update && claude --version && claude doctor`.
4. Copy `.mcp.json.example` → `.mcp.json`; add credentials to environment variables only.
5. Prepare a temporary Zotero collection with three known non-sensitive sources.
6. Verify Academic Tools MCP: search one known DOI, traverse one reference page.
7. Verify Zotero MCP: search, metadata, two-page range read; confirm no write tool is reachable.
8. Optionally install PaperQA (`pip install -e '.[paperqa]'`) and build a three-document index.
9. Run `/00-frame` → complete one full research cycle on the test question.
10. Record results in `audits/live-certification-YYYY-MM-DD.md`.

## Known limitations

- Python 3.13 not tested here (tested in CI across 3.11–3.13 in the original release environment).
- The `mros verify` command does not exercise the `cli.py` paths (0% coverage on `cli.py` noted); all CLI subcommands are tested indirectly via the installed entry point.
- PaperQA integration adapter is present and tested via a contract double; actual PaperQA library not installed.
