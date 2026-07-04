# 00.project.md

## Project Goal

1. TODO: state the concrete result and why it is needed.
2. TODO
3. TODO

## Business Domain

TODO

## Technical Constraints

- Python, PyTorch, and Rust work do not use unit tests or TDD by default; create or edit unit tests only when the user request, task document, or change document explicitly asks for them.
- State, lifecycle, invariants, and domain collaboration use full object-oriented design or equivalent type modeling.
- Default execution completes one task document and edits one production code file; split another task before editing a second code file.
- Task files use `tasks/NN.task_name.md`; do not use `00.task.md`.
- Change files use `changes/change_name.md` without timestamps; changes record only later changes after implementation.
- Code stays minimal, reuse-first, low-duplication, and avoids bloated files or overly long identifiers.
- Common packages include package-local `readme.md` files that explain functional entrypoints and usage.
- All cx scenarios, tasks, process documents, and changes live under `docs/cx`.
- Code, documentation, tutorials, research, design, or process-change deliverables must pass `$cx-review`, then pass `$cx-evidence` evidence review before handoff.

## Scenario Index

| ID | Main Success Scenario | Path | Status |
| --- | --- | --- | --- |
| 01 | TODO | `docs/cx/01.TODO/` | planned |
