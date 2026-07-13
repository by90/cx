---
name: cx-doc
description: Use for numbered topic documents under docs/cx/docs and question-specific research notes under docs/cx/notes. Trigger for common packages, stable interfaces, protocols, data processes, feature systems, technical direction changes, or research conclusions, and require the agent to read existing topic documents before implementation.
version: 0.1.0
---

# cx Topic Documents and Research Notes

## Purpose

Store reusable technical knowledge in stable documents so the agent understands confirmed project capabilities and constraints before adding implementation. Durable documents describe only the current valid state and never preserve solution history.

## Directories

```text
docs/cx/docs/
docs/cx/docs/00.index.md
docs/cx/docs/01.market_data_server_protocol.md
docs/cx/docs/02.build_series_from_database.md
docs/cx/docs/03.daily_features.md
docs/cx/notes/
docs/cx/notes/01.choose_time_series_model.md
```

- `docs/cx/docs/` stores established topic knowledge that guides implementation.
- `docs/cx/notes/` stores conclusions for specific research questions.
- Use two-digit numbers and concise names. Keep one current document per topic.
- `00.index.md` lists the topic, file, scope, and source entry without repeating the body.

## Topic-document rules

Create an independent topic document for:

1. Every common package, reusable component, and stable public interface.
2. Protocols, data formats, data-loading processes, and field semantics used by multiple tasks.
3. Reused feature systems, metric definitions, model inputs, and training constraints.
4. The current principles and usage after a technical direction changes.

Each topic document states:

```text
Topic:
Problem solved:
Scope:
Current conclusion:
Public entry or source location:
Inputs and outputs:
Key constraints:
Shortest usage:
Verification:
```

- Describe only the current solution. Do not include prior solutions, comparisons, migration steps, or change history.
- A direction change rewrites the original topic document in place.
- Old/new differences belong only in the active unfinished file under `changes/`.
- The topic document is the only detailed interface and usage source for a common package. Other documents link to it without duplicating the body.

## Research-note rules

Every research activity answers one explicit question and saves one conclusion file under `docs/cx/notes/` with:

```text
Research question:
Conclusion:
Plain-language explanation:
Evidence and sources:
Applicability:
Limits and unknowns:
Impact on current work:
```

- Answer the question before explaining why.
- Use fluent, concrete, plain language without invented terminology or jargon piles.
- Keep only the synthesized current conclusion. Do not commit search scratchpads, excerpt collections, candidate lists, or replaced conclusions.

## Workflow

1. Read `docs/cx/docs/00.index.md`; if it is absent, inspect all relevant files under `docs/cx/docs/`.
2. Select topics relevant to the common package, protocol, data process, fields, features, or technical direction.
3. Search the documented source entries and real callers to confirm that documentation and implementation agree.
4. Reuse an existing capability whenever it satisfies the need. Never bypass a registered common package to create similar logic.
5. When adding a stable topic, create the next numbered topic document and update the index.
6. When research finishes, create or update the note for that question. Never create parallel versions.
7. Use `$cx-review` to check document quality, implementation consistency, and completion evidence.

## Review requirements

- Topic documents match current source entries and contain no duplicate detailed explanations.
- Durable documents contain no old solution, comparison, process narrative, or completed change record.
- Research notes answer a question directly, use adequate sources, explain the result plainly, and state actionable impact.
- `docs/cx/docs/` and `docs/cx/notes/` contain no drafts, backups, old versions, or duplicate topics.
