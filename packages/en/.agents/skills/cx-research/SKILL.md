---
name: cx-research
description: Use for model selection research, AI paper surveys, model mechanism research, latest-six-month AI literature scans, source triage, blog interpretation, and citation-backed synthesis.
version: 0.0.1
---

# cx Research Workflow

## Purpose

Use this skill when the task is research rather than implementation: choosing a model, understanding a model family, comparing architectures, surveying recent AI papers, or collecting expert interpretations from papers and technical blogs.

## Source Strategy

Use multiple source classes and label them clearly:

1. Primary sources: official documentation, model cards, technical reports, arXiv papers, OpenReview submissions, conference proceedings, benchmark repositories, and source code.
2. Indexes and discovery tools: Semantic Scholar, arXiv search, OpenAlex, Papers with Code, Hugging Face Papers, conference pages, and citation graphs.
3. Interpretation sources: lab blogs, engineering blogs, independent expert writeups, talks, and reproducibility reports.
4. Community signals: GitHub issues, benchmark discussions, and forums only as weak signals, never as proof by themselves.

## Required Workflow

1. Define the research question, decision deadline, target user, and output format.
2. Define inclusion and exclusion criteria before collecting sources.
3. Search across academic sources, official sources, and interpretation sources.
4. For "latest" or "recent" AI research, use an explicit date window. "Last six months" means from today's date back six calendar months.
5. Deduplicate papers by title, DOI, arXiv ID, OpenReview ID, or Semantic Scholar Corpus ID.
6. Separate peer-reviewed papers, preprints, blog interpretations, benchmarks, and vendor claims.
7. Extract evidence into a table: source, date, venue/status, claim, method, evidence quality, limitations, and relevance.
8. Synthesize, do not merely list. Group by research direction, agreement, conflict, maturity, and implementation consequence.
9. Cite every non-obvious claim with a link.
10. State what is unknown, stale, disputed, or likely to change.

## Model Selection Research

For selecting a model, compare:

- Task fit and required modalities.
- Quality evidence on relevant benchmarks or internal evals.
- Context length, tool use, structured output, latency, throughput, reliability, and cost.
- Deployment constraints: API availability, local inference, privacy, licensing, region, and hardware.
- Failure modes: hallucination, weak reasoning, multilingual gaps, coding gaps, safety constraints, and eval contamination.
- Migration risk and fallback plan.

## Model Mechanism Research

For model principle research, prioritize original papers and technical reports. Explain architecture, training objective, data assumptions, inference behavior, scaling constraints, and known limitations. Do not treat marketing claims as mechanism evidence.

## Output Format

```text
Question:
Search window:
Sources searched:
Inclusion/exclusion criteria:

Findings:
1. Claim
   Evidence:
   Limits:
   Practical consequence:

Source table:
| Source | Date | Type | Claim | Evidence quality | Link |

Recommendation:
Open questions:
```
