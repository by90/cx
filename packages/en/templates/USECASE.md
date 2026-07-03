# 00.use_case.md

## Use Case Name

TODO: Use an action phrase for one user goal, such as "save current location".

## Goal

TODO: Describe the result the actor gets when this use case succeeds. One use case describes one user goal.

## Actors

- Primary actor: TODO
- Supporting systems: TODO

## Preconditions

- TODO

## Trigger

- TODO: Describe who starts this use case and when.

## Main Success Scenario

1. TODO: Start from the trigger and describe the first actor-system interaction.
1.1 If the business condition for step 1 is not satisfied, TODO: describe the system response and say whether the flow returns to a step, ends this use case, or enters another use case.
2. TODO: Continue the most common successful path.
2.1 If step 2 has an alternate or exception condition, TODO: describe the response and next destination.
3. TODO: End with the completed user goal and observable successful result.

> Keep the main success scenario to about 3 to 9 main steps. Substeps such as `1.1` express conditions, alternate behavior, or exceptions attached to a concrete main step and do not count as main steps. Do not put multiple mutually exclusive choices or multiple user goals into one main success scenario. Split a complex conditional flow into a separate use case and write "enter use case: TODO" in the substep.

## Sub-Use-Case Index

| Sub-use case | Trigger step | Entry condition |
| --- | --- | --- |
| TODO | TODO | Split when a conditional flow needs its own actors, preconditions, main success scenario, and completion criteria. |

## Completion Conditions

- All tasks are complete.
- Explicitly declared verification passes; when unit tests are not declared, tests are not a default completion condition.
- `$cx-review` passes for code, documentation, design, change, or other deliverables.
- `$cx-evidence` evidence review passes before handoff.
- Changes are marked complete.
