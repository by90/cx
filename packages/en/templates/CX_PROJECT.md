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
- Establish the task set once when a new story is created. After creation, task count, number, filename, and identity stay fixed.
- Complete one original task and its one production file at a time. An implementation change or code error updates the original task rather than creating a fix, removal, or modification task.
- Task files use `tasks/NN.task_name.md`; do not use `00.task.md`.
- Change files use `changes/change_name.md` only for unfinished work. Commit the file before implementation, delete it after review, and commit the deletion.
- Code stays minimal, reuse-first, low-duplication, and avoids bloated files or overly long identifiers.
- Common packages and stable technical processes have independent numbered topic documents under `docs/cx/docs/`; read existing topics before work.
- Every research effort saves its question-specific current conclusion and plain-language explanation under `docs/cx/notes/`.
- All cx scenarios, tasks, process documents, and changes live under `docs/cx`.
- Every durable document describes only current state, with no old solution, comparison, or completed change. Git preserves history.
- Code, documentation, tutorial, research, design, and process deliverables pass both `$cx-review` stages before completion.

## Scenario Index

| ID | Main Success Scenario | Path | Status |
| --- | --- | --- | --- |
| 01 | TODO | `docs/cx/01.TODO/` | planned |
