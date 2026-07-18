# Known limitations

- Live Academic Tools MCP, Zotero MCP, Claude Code, and PaperQA operations were not executed in the packaged environment because they require the user's network, library, installation, permissions, or subscription. The adapters and policies are offline-tested against explicit contracts; live compatibility must still be certified locally.
- The PaperQA adapter targets the current PaperQA 5-style `Docs.aadd` and `Docs.retrieve_texts` interfaces. It fails closed on contract drift, but an upstream release can still require adaptation.
- MROS does not provide a complete PDF-layout engine. It validates normalized text produced by Zotero, PaperQA, or another parser; page, figure, table, note, and offset quality therefore depend on the upstream extraction.
- Exact quotation matching proves textual presence in the recorded normalized file. It does not by itself prove that the passage entails a claim, that the edition is authoritative, or that a translation is adequate.
- Local semantic ranking quality depends on the embedding and reranking models, corpus language, extraction quality, and chunking policy.
- Scholarly-provider coverage is uneven for books, chapters, archives, artistic works, minor literatures, new publications, and non-English sources.
- Citation counts, related-paper services, and support/contrast metadata are discovery signals, not universal quality scores.
- Hash-chained events are tamper-evident within the repository, not cryptographically signed or externally notarized.
- Claude aliases, effort semantics, subscription limits, MCP schemas, and upstream package behavior may change. Pin and retest before upgrades.
- Human evaluation remains necessary for conceptual specificity, cultural and historical context, ethical use, source fitness, design consequence, and final claim permission.
- MROS can enforce the distinctions and transformations it controls; it cannot make weak, inaccessible, or misinterpreted sources strong.
