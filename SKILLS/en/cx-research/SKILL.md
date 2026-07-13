---
name: cx-research
description: Use for model selection, AI paper reviews, model principles, recent literature, source screening, and technical-option research. Every effort must answer one explicit question, save the synthesized current conclusion under docs/cx/notes, and explain the conclusion, evidence, limits, and work impact in fluent plain language.
version: 0.1.0
---

# cx Question-Driven Research

## Purpose

Research answers a concrete question that affects current work. The repository keeps only the synthesized current conclusion, never search scratchpads, excerpt piles, candidate lists, or replaced conclusions.

## Source strategy

1. Primary sources: official documentation, model cards, technical reports, papers, conference pages, benchmark repositories, and source code.
2. Discovery sources: arXiv, OpenReview, Semantic Scholar, OpenAlex, Papers with Code, and citation graphs.
3. Interpretation: laboratory blogs, engineering blogs, expert articles, technical talks, and replication reports.
4. Community signals: issues, forums, and social posts are weak signals and cannot support a conclusion alone.

## Required workflow

1. Define the research question, decision deadline, audience, and conclusion needed by current work.
2. State inclusion and exclusion criteria before searching.
3. Search primary, discovery, and reliable interpretation sources.
4. Use an explicit date window for “latest” or “recent.” “Last six months” means the six calendar months before today.
5. Deduplicate with stable identifiers.
6. Distinguish peer-reviewed papers, preprints, interpretation, benchmarks, and vendor claims.
7. Extract source, date, claim, method, evidence quality, limits, and relevance.
8. Synthesize by consensus, conflict, maturity, applicability, and implementation consequence.
9. Cite every non-obvious claim and state unknown, disputed, or volatile points.
10. Use `$cx-doc` to create or update the numbered question file under `docs/cx/notes/`.
11. Use `$cx-review` for research quality, note quality, and completion evidence.

## Research note

```markdown
# Research: specific question

## Research question

## Conclusion

Answer the question first.

## Plain-language explanation

Explain why in language the project reader can understand.

## Evidence and sources

## Applicability

## Limits and unknowns

## Impact on current work
```

- Save it as `docs/cx/notes/NN.concise_question.md`.
- Keep one current conclusion per question and update it in place.
- Put old/new differences only in an unfinished change file.
- Use fluent, concrete language rather than invented terms or jargon piles.

## Required output

- Research question and time window.
- Inclusion and exclusion criteria.
- Direct conclusion and plain-language explanation.
- Key evidence, source links, and evidence quality.
- Applicability, limits, unknowns, and impact on current work.
- Current research note under `docs/cx/notes/`.
- Unified `$cx-review` decision.
