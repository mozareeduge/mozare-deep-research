# MROS v1.0.0 → v1.2.0 Migration Receipt

## Versions

| Field | Value |
|---|---|
| Source version (repository before migration) | mozare-research-os 1.0.0 (commit `f05b55c`) |
| Target version | mozare-research-os 1.2.0 |
| Release archive | `mozare-research-os-v1.2.0.zip` |
| Migration branch | `migration/mros-v1.2` |

## Archive checksum

| Field | Value |
|---|---|
| Expected SHA-256 (`mozare-research-os-v1.2.0.sha256`) | `baf0d67e998a59ebbdc46a0dc8a03f5129561dac52c4edc975480ef4ebe1281d` |
| Computed SHA-256 (`sha256sum mozare-research-os-v1.2.0.zip`) | `baf0d67e998a59ebbdc46a0dc8a03f5129561dac52c4edc975480ef4ebe1281d` |
| Result | **MATCH** |

Before extraction, the ZIP member list (172 entries) was inspected: no absolute paths, no `../` traversal segments, no embedded `.git` directory, no symlink entries, and a single top-level root (`mozare-research-os/`). The archive was extracted only after this check and the checksum match.

## Starting repository state

An in-place migration, not an empty-repo install. The repository already carried an installed and certified MROS v1.0.0 (see `audits/initial-installation.md`), plus in-progress **uncommitted** local edits to `research/contract.yaml` and `research/questions.yaml` repurposing the framework's own root research contract into a real research definition for a literature-review dossier on "Uncreative Writing," and two untracked local files: `audits/local-bootstrap-pending.md` (local MCP bootstrap notes) and a stray `src/mros/templates/.claude/settings.local.json` (a local permissions file mistakenly synced into the packaged-template tree).

## Migration strategy

1. Verified checksum and inspected the archive (above), then extracted to an isolated temp directory outside the repository.
2. Read the release's high-value docs (README, CLAUDE.md, TEST_REPORT.md, architecture/setup/testing/live-certification, revision-analysis-v1.2, simulation-uncreative-writing, migration-v1.1-to-v1.2, apply-v1.2-with-claude, pyproject.toml, `.claude/settings.json`, `.claude/skills/research/SKILL.md`, both new agents, `.mcp.json.example`, CI workflow) before changing any tracked file.
3. Created branch `migration/mros-v1.2` from the v1.0.0 commit.
4. Archived the user's in-progress "Uncreative Writing" contract/questions (see below) **before** they could be overwritten by the release's own generic framework-identity defaults for those same root paths.
5. Removed (via `git rm`) the 18 obsolete v1.0 active files — 12 numbered phase skills and their 12 packaged-template mirrors, plus 5 old agents and their 5 packaged-template mirrors, plus 6 obsolete `.mros/compiled/run-profiles/*.md` files — confirming their content is preserved verbatim in the release's own `docs/archive/v1-agents.md` and `docs/archive/v1-phase-skills.md`.
6. Copied all 172 release files into the repository root (root-level, not nested under `mozare-research-os/`), overwriting every existing tracked framework file.
7. Removed one non-release stray file: `src/mros/templates/.claude/settings.local.json` (confirmed cruft, already flagged in the user's own `audits/local-bootstrap-pending.md` as needing removal before the next commit).
8. Verified the reconciled tree, ran the full offline verification suite, ran one bounded read-only reviewer, and wrote this receipt.

## User material preserved

| Item | Disposition |
|---|---|
| In-progress "Uncreative Writing" research contract (`research/contract.yaml`) | Archived verbatim at `docs/archive/pre-v1.2-uncreative-writing-contract.yaml` before the root file was reset to the v1.2 release's own framework-identity defaults. Not lost. |
| In-progress "Uncreative Writing" research questions (`research/questions.yaml`) | Archived verbatim at `docs/archive/pre-v1.2-uncreative-writing-questions.yaml`, same reasoning. |
| `audits/local-bootstrap-pending.md` | Left untouched and untracked; excluded from this migration's staged/committed tree by design (confirmed with `git status --short` before staging — see Step 6). |
| `.claude/settings.local.json` (real local file) | Left untouched; remains gitignored and unstaged. |
| `audits/initial-installation.md` (v1.0 install receipt) | Kept as-is; not part of the v1.2 release, no conflict, valuable install history. |

**Why the contract/questions files were archived rather than kept live:** v1.2's architecture moves user research topics out of the root `research/contract.yaml`/`questions.yaml` (which are now, as in the shipped release, the framework's *own* self-referential meta-contract describing MROS itself) and into isolated `research/runs/<run-id>/` directories created automatically per inquiry. The user's manually-authored v1.0-era contract does not fit that structure directly; archiving preserves its content for reference. Re-submitting the same natural-language request under v1.2 will now produce a proper `research/runs/` entry with the full v1.2 query/term/evidence/claim/audit apparatus — which is exactly what the Phase 7 synthetic simulation below demonstrates.

## Obsolete files removed or archived

- 12 numbered phase skills (`00-frame` … `90-synthesis-plan`) and their packaged-template mirrors — removed; content preserved in `docs/archive/v1-phase-skills.md` (shipped by the release itself, verified to match our repository's actual files verbatim).
- 5 old agents (`citation-auditor`, `contradiction-reviewer`, `evidence-reviewer`, `final-adversary`, `source-screener`) and their packaged-template mirrors — removed; content preserved in `docs/archive/v1-agents.md` (same verbatim match).
- 6 obsolete `.mros/compiled/run-profiles/*.md` files (`compare`, `critical`, `evidence`, `prototype-test`, `scan`, `synthesis`) — removed, replaced by the v1.2 route profiles (`lookup`, `brief`, `deep`, `design`).
- 1 stray non-release file (`src/mros/templates/.claude/settings.local.json`) — deleted (untracked, never committed, previously self-flagged as cruft).

## Expected vs. unexpected differences

A full three-way reconciliation (release file list vs. pre-migration tracked file list vs. post-copy tree) found:
- **115 files** as expected v1.2 content replacements (all root framework files: `src/mros/`, `config/`, `docs/`, `scripts/`, `tests/`, schemas, `pyproject.toml`, CI, README/CLAUDE.md, etc.).
- **44 files** as expected removals of obsolete v1.0 active files (staged as `D`).
- **~38 new files** as intentional v1.2 additions (new `research` skill + 2 agents, 7 new run-record schemas, `src/mros/runs.py`, `tests/test_runs.py`, new/renamed docs, `research/runs/.gitkeep`).
- **0 unexpected differences.** Every release file was confirmed present at the repository root (no nested `mozare-research-os/` directory); no release file was missing from the working tree.

## Changes made beyond the unmodified release content

1. Archived the pre-migration Uncreative Writing contract/questions (2 new files under `docs/archive/`, not part of the release).
2. Removed the stray non-release `src/mros/templates/.claude/settings.local.json`.
3. No source, schema, test, or validator content from the release was edited, weakened, or otherwise altered. The bounded reviewer (Step 4) found zero blocking/material issues, so no repair commit was required.

## Commands executed (verification)

```
.venv/Scripts/python.exe -m pip install -e '.[dev]'
.venv/Scripts/python.exe -m compileall -q src tests scripts
.venv/Scripts/python.exe scripts/export_schemas.py --check
.venv/Scripts/python.exe scripts/sync_templates.py --check
.venv/Scripts/python.exe -m pytest --cov=mros --cov-report=term-missing
.venv/Scripts/python.exe -m mros validate .
.venv/Scripts/python.exe -m mros verify .
.venv/Scripts/python.exe -m mros verify . --phase-stop
.venv/Scripts/python.exe -m mros audit . --release
.venv/Scripts/python.exe -m mros event-verify .
.venv/Scripts/python.exe -m pip wheel . --no-deps -w dist
python -m venv <isolated wheel venv>
<wheel venv>/Scripts/python.exe -m pip install dist/mozare_research_os-1.2.0-py3-none-any.whl
<wheel venv>/Scripts/python.exe -m mros init <tmp>/wheel-project --project-id wheel-project --title "Wheel Project" --with-claude
<wheel venv>/Scripts/python.exe -m mros doctor <tmp>/wheel-project
<wheel venv>/Scripts/python.exe -m mros validate <tmp>/wheel-project
<wheel venv>/Scripts/python.exe -m mros run-init <tmp>/wheel-project/research/runs/uncreative-writing-test --mode deep --output-profile concept-dossier ...
<wheel venv>/Scripts/python.exe -m mros run-summary <tmp>/wheel-project/research/runs/uncreative-writing-test
<wheel venv>/Scripts/python.exe -m mros run-validate <tmp>/wheel-project/research/runs/uncreative-writing-test
```

## Test totals and coverage

| Check | Result |
|---|---|
| Automated tests | **94 passed, 0 failed** (matches shipped `TEST_REPORT.md`) |
| Statement/branch coverage | **75%** overall, branch measurement enabled |
| Python compilation | PASS |
| Exported JSON Schemas | **20 current and valid** |
| Packaged Claude harness mirror (`sync_templates.py --check`) | PASS |
| `mros validate .` | PASS — 0 issues |
| `mros verify .` | PASS — 0 issues |
| `mros verify . --phase-stop` | PASS |
| `mros audit . --release` | PASS — 0 blockers, 0 warnings |
| `mros event-verify .` | PASS — event chain valid |

## Wheel and clean-install results

- Wheel built: `mozare_research_os-1.2.0-py3-none-any.whl`.
- Installed cleanly into an isolated venv outside the repository.
- From the installed wheel: `mros init --with-claude`, `mros doctor`, `mros validate` all PASS on a freshly initialized project.
- From the installed wheel: `mros run-init --mode deep --output-profile concept-dossier` correctly created a run with the inferred budget, source lanes (`web`, `academic`), an excluded lane (`zotero`), and stated requirements; `mros run-summary` and `mros run-validate` both PASS (0 issues, `ok: true`).

## Synthetic "Uncreative Writing" concept-dossier simulation

The repository's own offline test suite (`tests/test_runs.py::test_full_concept_dossier_flow_is_valid`) encodes exactly the target inquiry — *"Gather a research note dossier around the concept 'uncreative writing' with exact terms and wording"* — end-to-end, and it passed as part of the 94-test run. It exercises: `mode=deep` + `output_profile=concept-dossier` inference, query records across two distinct lanes/strategies, five role-tagged sources (`primary-core`, `primary-adjacent`, `scholarly-interpretation`, `critique`, `reception`), verified exact-quotation evidence, a verified term record, a *qualified* claim carrying both supporting and counter-evidence, a non-empty dossier and a Mermaid visualization, a passing audit, and a `validate_run` result with `ok: true` and zero blocker issues. Its fixture content is explicitly labeled `"This synthetic end-to-end fixture demonstrates the dossier architecture rather than making a historical claim"` — it is not presented as real scholarship.

Separately, the CLI-level wheel smoke test above independently exercised the live *routing/creation* path (not the content-authoring path) for the same inquiry: `run-init --mode deep --output-profile concept-dossier` on a fresh project, confirming the machine infers route and profile, creates an isolated run directory, and stores the correct lanes/requirements — without any slash command, YAML authoring, or phase name from the user, and without invoking generic `deep-research` (`Skill(deep-research)` is explicitly denied in `.claude/settings.json`).

Negative completion-gate coverage, confirmed via passing tests plus direct code inspection of `src/mros/runs.py`:

| Gate | Test | Result |
|---|---|---|
| Missing primary-core source / query history | `test_run_validation_blocks_missing_source` | PASS (blocks) |
| Supported claim referencing missing evidence | `test_complete_run_blocks_supported_claim_without_evidence` | PASS (blocks) |
| Unverified evidence | `test_complete_run_blocks_unverified_claim_evidence` | PASS (blocks) |
| Exact term without verified quotation | `test_concept_dossier_blocks_unverified_term` | PASS (blocks) |
| Empty dossier | `empty_deliverable` blocker code confirmed in `runs.py` (dossier content is length-checked) | Confirmed in code |
| Missing/failed audit | `audit_status` gate confirmed in `runs.py`; `test_release_audit_requires_release_artifact` / `test_release_audit_rejects_placeholders` / `test_release_audit_accepts_clean_artifact` | PASS (blocks) |

## Independent reviewer result

One fresh, bounded, read-only reviewer subagent (Explore-type, Read/Grep/Glob/read-only Bash only) was given the migration objective, changed-file list, the semantic research skill, settings/permission files, relevant schemas/validators, the synthetic-inquiry result, test/coverage summary, and security/packaging results. It was scoped to report only demonstrated blocking or material problems across 13 categories (routing, user effort, deep-research leakage, source breadth, quotation integrity, Zotero restrictions, evidence/completion gates, resumability, migration preservation, packaging, secrets, CI accuracy, documentation claims).

**Result: 0 blocking/material findings.** No repair was required; full verification, release audit, and secret scan were therefore not rerun (nothing changed after the review).

## Security result

- Secret-pattern scan (API keys, passwords, tokens, private-key headers) across tracked and untracked files (excluding `.git`, `.venv`, `dist`, `build`, caches): **no literal secrets found** — only commented-out placeholder variable names in `.env.example` files (`# ZOTERO_API_KEY=`, `# SEMANTIC_SCHOLAR_API_KEY=`).
- Zotero: read-only in the normal workflow; `zotero_get_item_fulltext` (whole-document retrieval) and all `zotero_create_*` / `zotero_update_*` / `zotero_delete_*` / `zotero_add_*` / `zotero_remove_*` / `zotero_merge_duplicates` mutation families are explicitly denied in both `.claude/settings.json` and the packaged template.
- PaperQA remains an optional, retrieval-only extra (`pyproject.toml` `[project.optional-dependencies] paperqa`), not installed or exercised.
- No paid API calls, credentials, or live network research were performed during this migration.
- Build artifacts (`build/`, `dist/`, `__pycache__/`, `*.egg-info/`), the local venv, the release ZIP/checksum, `.mcp.json`, and `.claude/settings.local.json` are all correctly excluded via `.gitignore` and were not staged.

## Known limitations

- Live integration certification (real Claude Code auto-routing, real Academic Tools/Zotero network calls, real web search/fetch, elapsed-time and subscription-usage behavior) has **not** been performed — this requires the user's own running services, credentials, and Claude subscription, per `docs/live-certification.md` and `docs/benchmark-protocol.md`.
- Comparative benchmark evidence against Claude's generic Deep Research (source fitness, primary-source coverage, citation support, user effort, elapsed time) is not yet established.
- Python 3.14.3 (the local interpreter used for `.venv` in this environment) is newer than any version pinned in CI's tested matrix (3.11–3.14); CI itself already includes 3.14, so this is a consistency note rather than a gap.

## Remaining local-only live-certification work

Per `docs/live-certification.md`, to be performed by the user locally after this PR merges:
1. `claude mcp list` and authenticate the Academic Tools and Zotero MCP servers.
2. Resolve one known scholarly identifier via Academic Tools; confirm built-in web search/fetch inspect one official source page.
3. Confirm Zotero finds one known source and reads a bounded page range; confirm whole-document and write operations remain unreachable.
4. Submit the real one-sentence "Uncreative Writing" inquiry in a fresh session (no slash command) and confirm automatic routing, durable run creation, exact-wording verification, challenge search, dossier + visualization delivery, and a passing `mros run-validate`.
5. Interrupt an active run and confirm resumption via ordinary language ("continue the research") in a fresh session.
6. Run the full benchmark protocol (`docs/benchmark-protocol.md`) across three consecutive real inquiries before routine adoption.
