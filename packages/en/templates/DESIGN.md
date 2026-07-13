# 00.design.md

## Topic Documents and Reusable Code

| Topic document | Capability | Existing entry | Usage |
| --- | --- | --- | --- |
| `docs/cx/docs/NN.topic.md` | TODO | TODO | TODO |

## New Common Code Needed

| Capability | Proposed Entrypoint | Reuse Reason |
| --- | --- | --- |
| TODO | TODO | TODO |

## Functional Entrypoints

- Functional entrypoint: TODO
- Normal call style: TODO
- Special-case entrypoint: TODO
- Topic document: TODO; every common package has an independent numbered document under `docs/cx/docs/`.

## Default Parameters

- Configuration default: TODO; for example `path=Config.default_config_file()` or `batch_size=config.train.batch_size`.
- Field storage: TODO; use `self.xx = xx` inside the function body.

## Design Decisions

| Decision | Reason | Impact |
| --- | --- | --- |
| TODO | TODO | TODO |

## Implementation Boundary

- Establish the task set once for a new story. Never add, delete, or rename task files in an existing story.
- Each task handles one task document and one production file. Rewrite the original task when implementation changes.
- Unit tests are not default deliverables; add one matching unit-test file only when unit tests or TDD are explicitly requested.
- The task measure is a class or type group.
- Default implementation uses full object-oriented design, minimal code, reuse first, and avoids bloated files, overly long identifiers, and duplicated logic.
- Design, documentation, code, and other deliverables must pass artifact-quality and completion-evidence review in `$cx-review`.
- This document states only current design and contains no previous solution, comparison, or migration history.
