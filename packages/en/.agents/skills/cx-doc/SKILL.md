---
name: cx-doc
description: Use for caller-facing common-package tutorials and stable topic documents under docs/cx/docs, research notes under docs/cx/notes, and tutorial navigation in the project-root AGENTS.md. Trigger for common packages, stable interfaces, protocols, data processes, feature systems, technical direction, research conclusions, or project-rule initialization, and require domain tutorials before implementation.
version: 0.1.0
---

# cx Tutorials, Topic Documents, and Project Rules

## Purpose

Let callers use every common package correctly through a tutorial, and let agents find required domain reading through the project-root `AGENTS.md`. Durable documents describe only current valid facts and do not preserve solution history.

## Directories and entries

```text
AGENTS.md
docs/cx/docs/
docs/cx/docs/00.index.md
docs/cx/docs/01.configuration_tutorial.md
docs/cx/notes/
docs/cx/notes/01.choose_time_series_model.md
```

- The project-root `AGENTS.md` supplements the global `AGENTS.md`.
- `docs/cx/docs/` stores common-package tutorials and stable technical processes.
- `docs/cx/notes/` stores conclusions for explicit research questions.
- This skill's `assets/AGENTS.md` is the default project-rule template. Copy it to the project root and tailor it to the actual project.

## Common-package tutorials

Every common package, reusable component, and stable public interface has one independent numbered tutorial under `docs/cx/docs/`. A common package without a tutorial is incomplete and cannot be used directly in a new domain task.

Write from the caller's perspective and explain how to complete real work rather than cataloging internal classes, fields, or implementation steps. Every tutorial contains:

```text
Tutorial goal:
Audience and scenarios:
Prerequisites:
Public entry and source location:
Inputs and outputs:
Minimal runnable example:
Steps and the expected result of each step:
Common failures and handling:
Key constraints:
Verification:
```

- Examples use the current public entry, run in order, and state observable expected results.
- Failure guidance covers actual caller failures and correct handling without adding product-code fallbacks.
- The tutorial is the sole detailed usage source for a common package. Other documents link to it without copying the body.
- `docs/cx/docs/00.index.md` lists only topic, tutorial file, domain, and public entry.
- Add the tutorial and index entry with a new common package. Update the existing tutorial when its public entry changes.

## Project AGENTS.md

Every project has a root `AGENTS.md`. It supplements global rules without copying or weakening them.

To create or update project rules:

1. Read project goals, primary languages, package managers, build entries, directory structure, and existing common packages.
2. Use this skill's `assets/AGENTS.md` as the structure for the project-root `AGENTS.md`.
3. Record project goals, language and toolchain, project commands, project-specific boundaries, and verification.
4. Register each common package's domain, tutorial link, public entry, and conditions that require reading it first.
5. Use repository-relative links that both people and agents can open directly.
6. Before planning, designing, or coding in a domain, read every tutorial linked for that domain.
7. When a common package has no tutorial, use `$cx-doc` to add the tutorial and navigation before implementation continues.

The project `AGENTS.md` contains project-specific facts only. Global disciplines remain in the global `AGENTS.md`.

## Stable topics and research notes

- Protocols, data formats, data loading, field semantics, feature systems, metric definitions, and technical direction may use the same numbered topic structure.
- Each research question has one current conclusion under `docs/cx/notes/`.
- State the answer first, then evidence, applicability, limitations, and work impact.
- Durable documents contain no old solutions, comparisons, scratchpads, excerpt piles, or completed-change history.

## Workflow

1. Read the project-root `AGENTS.md`. If it is absent, create it from this skill's asset and tailor it to the project.
2. Read the current domain's registered common-package tutorials and `docs/cx/docs/00.index.md`.
3. Search each tutorial's public entry, source location, and real callers to confirm the documentation is current.
4. Reuse existing capabilities whenever they satisfy the need. Never bypass a common package to create similar logic.
5. When adding or changing a common package, update its tutorial, index, and project `AGENTS.md` navigation.
6. Use `$cx-review` to verify tutorial executability, links, project-rule completeness, and implementation consistency.

## Review requirements

- Every common package has a caller tutorial with a real public entry and valid example.
- The project `AGENTS.md` matches the project's languages, goals, toolchain, and actual common packages.
- The project `AGENTS.md` links every common-package tutorial and states domain reading requirements.
- `docs/cx/docs/`, `docs/cx/notes/`, and project rules contain no draft, backup, old version, duplicate tutorial, or broken link.
