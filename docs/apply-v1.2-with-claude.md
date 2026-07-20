# Apply MROS v1.2 with Claude Code

Place `mozare-research-os-v1.2.0.zip` and its checksum in the repository root, then open a fresh Claude Code session on `mozareeduge/mozare-deep-research` and provide:

```text
Upgrade this repository from MROS v1.1 to the v1.2 release archive in the repository root.

INPUTS
- mozare-research-os-v1.2.0.zip
- mozare-research-os-v1.2.0.sha256

CONSTRAINTS
- Work on a new branch `upgrade/mros-v1.2`.
- Do not merge.
- Preserve my untracked/local `.mcp.json`, `.env*`, `.venv`, Zotero data, private corpora, and local settings.
- Do not install paid services or add credentials.
- Do not redesign the release unless a real compatibility or correctness issue is found.
- Use low effort for inspection and medium only for a real repair.

PROCESS
1. Verify the SHA-256 and inspect the archive before extraction.
2. Read README.md, docs/revision-analysis-v1.2.md, docs/simulation-uncreative-writing.md, docs/migration-v1.1-to-v1.2.md, TEST_REPORT.md, and releases/mros-v1.2.0.md from the archive.
3. Replace tracked MROS source with the v1.2 release while preserving local ignored files.
4. Confirm there is one active project research skill and that it is model-invocable from rough natural-language requests.
5. Confirm WebSearch/WebFetch and Academic Tools are available; Zotero remains read-only and whole-document retrieval remains denied.
6. Run the documented compilation, schema, test, verification, release-audit, wheel, clean-install, and ZIP checks.
7. Run the synthetic Uncreative Writing concept-dossier flow test.
8. Use one bounded fresh reviewer to check only correctness, research-integrity, installation, permission, and packaging gaps.
9. Fix valid findings, rerun affected checks, commit, push, and open a draft PR titled `Upgrade MROS to v1.2 concept-dossier controller`.
10. Do not run the real web research yet and do not merge.

FINAL REPORT
Return branch, PR, head SHA, checksum, test totals, package results, changes from the release, reviewer result, and remaining live-certification steps.
```
