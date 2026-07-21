# Natural-language end-to-end walkthrough

## 1. Ask normally

Start a fresh session in this repository and write the real inquiry. No slash command is required.

> Research the concept of uncreative writing as a historical and contested formation. Produce a detailed academically valid dossier using scholarly literature, primary texts, archives, and trustworthy web sources. Do not use Zotero for this run.

Claude should automatically load the project `research` skill.

## 2. Automatic route and run creation

Claude infers that this is a `deep` route, creates `research/runs/<run-id>/request.md`, and initializes the run. It should ask no question unless a materially different scope or output remains possible.

## 3. Discovery

Claude selects source lanes from the request. For this example it uses built-in web search/fetch and Academic Tools, while respecting the Zotero exclusion. It may use one bounded discovery scout to keep candidate results out of the main context.

## 4. Evidence

Claude screens broadly, reads the strongest sources selectively, and records source and evidence entries. Search snippets do not become evidence. Exact quotations are re-opened from bounded source locations.

## 5. Challenge and synthesis

Claude looks for criticisms, competing periodizations, alternative accounts, and scope limits. It builds qualified claims and drafts the dossier from accepted evidence rather than from the search transcript.

## 6. Audit

For a deep run, Claude uses one fresh verifier and writes `audit.yaml`. Citation or evidence failures reopen research; prose is not patched around them.

## 7. Completion

Claude runs `mros run-validate`, returns the requested dossier and the run path, and states material limits. If the session ends first, the run stays active and a later request such as “continue the uncreative writing research” resumes it.
