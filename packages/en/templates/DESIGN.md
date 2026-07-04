# 00.design.md

## Reusable Code

| Capability | Existing Entrypoint | Usage |
| --- | --- | --- |
| TODO | TODO | TODO |

## New Common Code Needed

| Capability | Proposed Entrypoint | Reuse Reason |
| --- | --- | --- |
| TODO | TODO | TODO |

## Public APIs

- Public entrypoint: TODO
- Normal call style: TODO
- Special-case entrypoint: TODO
- Package readme: TODO; common packages must list public APIs and usage.

## Default Parameters

- Configuration default: TODO; for example `path=Config.default_config_file()` or `batch_size=config.train.batch_size`.
- Field storage: TODO; use `self.xx = xx` inside the function body.

## Design Decisions

| Decision | Reason | Impact |
| --- | --- | --- |
| TODO | TODO | TODO |

## Implementation Boundary

- One task handles one task document and one production code file; split another task before editing a second code file.
- Unit tests are not default deliverables; add one matching unit-test file only when unit tests or TDD are explicitly requested.
- The task measure is a class or type group.
- Default implementation uses full OOP, minimal code, reuse first, and avoids bloated files, overly long identifiers, and duplicated logic.
- Design, documentation, code, or other deliverables must pass `$cx-review`; before handoff they must pass `$cx-evidence` evidence review.
