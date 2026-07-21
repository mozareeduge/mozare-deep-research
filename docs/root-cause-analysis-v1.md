# Root-cause analysis: why MROS v1 did not function as the intended research machine

## Observed failures

The first live tests showed four distinct behaviors:

1. A source-specific Zotero query produced useful passages, but Claude retrieved complete full text and later relied on conversation memory for quote-critical wording.
2. A broad research request activated another skill named `/deep-research`, not MROS.
3. Correct MROS use required the user to invoke `/00-frame` and provide a highly structured prompt.
4. The framing phase spent a long time reading schemas, created no research, and later invented a nonexistent `/01-search` command.

These are not isolated prompt mistakes. They follow from the v1 architecture.

## Primary root causes

### 1. The product was a validation framework, not an orchestrated researcher

The Python package validates records, identifiers, evidence links, event chains, and releases. It does not decide how to handle a natural-language inquiry, create a research run, search, screen, read, synthesize, or resume. All intellectual orchestration was delegated to fourteen small prompt skills.

### 2. The internal workflow became the user interface

V1 exposed numbered implementation phases as manual slash commands. The user had to know which command came next and supply extra routing instructions. This reversed the intended authority: the user operated the workflow rather than stating the research need.

### 3. Every phase skill disabled automatic invocation

All fourteen skills used `disable-model-invocation: true`. Claude therefore could not choose them from a rough inquiry. A different available skill with a matching “deep research” description was selected instead.

### 4. There was no semantic front door

V1 had no single project skill whose job was to infer whether a request required a lookup, close reading, brief, deep review, or research-to-design route. It also had no persistent instruction telling Claude to prefer MROS over generic research skills.

### 5. The source architecture and the active tool surface diverged

The discovery instructions mentioned official websites, archives, and repositories, but the skill did not pre-approve built-in `WebSearch` and `WebFetch`. Academic Tools and Zotero were treated as the main lanes even though book-heavy humanities research requires broader web, publisher, archival, and primary-source routes.

### 6. Permission allowlists were mistaken for restrictions

A skill's `allowed-tools` field pre-approves tools for that turn; it does not remove other tools. V1 allowed safe Zotero tools but did not globally deny `zotero_get_item_fulltext` or the write tool families. The live full-text retrieval was therefore possible.

### 7. One framework repository was also one mutable research project

Root files such as `research/contract.yaml` and `research/questions.yaml` held framework-development state and were then overwritten for a specific inquiry. There was no first-class run directory, so multiple inquiries, resumption, and comparison were awkward.

### 8. Schema formality appeared before research value

The model had to inspect large JSON Schemas and hand-write detailed YAML before it could search. This created latency, error opportunities, and pseudo-precision. Stage-inappropriate warnings made a correct empty framing state appear problematic.

### 9. Phase fragmentation weakened continuity

The model had to recommend or invoke a sequence of independently named skills. The workflow name `/01-search` was hallucinated because there was no orchestrator carrying the actual phase graph. Skill permissions also clear after the invoking turn, while skill text remains in context, producing subtle behavior differences across turns.

### 10. The test suite measured software integrity, not research performance

The 83 tests established that schemas and code behaved as written. They did not test automatic skill selection, source quality, citation entailment, coverage, user effort, time, or comparison with generic deep research.

## V1.1 correction

V1.1 keeps deterministic validation but changes the product boundary:

- one auto-invoked `research` skill is the natural-language front door;
- five internal routes replace fourteen user-visible phases;
- each substantial inquiry gets an isolated durable run;
- built-in web, Academic Tools, Zotero, and local files are routed by source type;
- generic `deep-research` is denied inside the project;
- Zotero whole-document and write tools are denied;
- one scout and one verifier may be used sequentially;
- exact quotations must be re-opened and checked;
- framework maintenance is separated from research execution;
- evaluation includes user effort, time, source quality, citation support, and counterevidence.

The archived v1 instructions remain available for audit and selective reuse, but they no longer define the normal interaction.
