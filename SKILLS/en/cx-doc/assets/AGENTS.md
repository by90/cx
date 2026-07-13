# AGENTS.md

This file supplements the global `AGENTS.md` with current project facts, boundaries, and required tutorials. Global rules remain in force. Do not copy, weaken, or override them here.

## Project goals

1. TODO: state the concrete project result and why it is needed.
2. TODO
3. TODO

## Languages and toolchain

| Item | Current choice | Commands or entries |
| --- | --- | --- |
| Primary languages | TODO | TODO |
| Package manager or build tool | TODO | TODO |
| Run entry | TODO | TODO |
| Formatting and static checks | TODO | TODO |
| Test entry when explicitly authorized | TODO | TODO |

## Project structure and boundaries

- Source directory: TODO
- Documentation directory: `docs/cx/`
- Temporary artifact directory: TODO
- Project-specific boundaries: TODO

## Common-package tutorial navigation

| Domain | Common package or stable capability | Tutorial link | Public entry | Read-first condition |
| --- | --- | --- | --- | --- |
| TODO | TODO | [TODO](docs/cx/docs/NN.topic.md) | TODO | TODO |

## Domain reading gate

1. Identify the current work's domain before planning, designing, or coding.
2. Read every matching tutorial above and confirm public entries, inputs, outputs, constraints, and verification.
3. Search the documented source locations and real callers to confirm each tutorial is current.
4. If a common package has no tutorial or a link is broken, use `$cx-doc` to fix the tutorial and navigation before continuing.
5. Reuse an existing common package whenever it satisfies the need. Do not create similar implementation.

## Project-specific rules

- TODO: include only rules caused by project goals, languages, toolchain, environment, or domain constraints.

## Verification and delivery

- Narrowest effective verification: TODO
- Package- or project-level verification: TODO
- Use `$cx-review` before delivery to verify implementation, tutorials, links, and completion evidence.
