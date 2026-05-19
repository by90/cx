---
name: cx-bdd
description: Use for BDD discovery, feature-folder naming, business rules, Gherkin-style examples, acceptance criteria, main/alternate/exception scenarios, and mapping behavior to later tests.
version: 0.1.0
---

# cx BDD Discovery And Scenario Documentation

## Purpose

Use this skill before implementation and before TDD. BDD is the collaboration layer for discovering behavior through concrete examples. It is not just a test format, and it should not be merged into a TDD-only workflow.

## Documentation Set Naming

Feature folders under `docs/` must use an ordered business-feature name:

```text
docs/1.Configuration System/
docs/2.User Sessions/
docs/3.Model Evaluation/
```

Chinese projects should use the same pattern with Chinese feature names:

```text
docs/1.配置系统/
docs/2.用户会话/
docs/3.模型评估/
```

The BDD document inside the folder must use the same name as the folder:

```text
docs/1.配置系统/BDD.md
# BDD: 1.配置系统

Feature: 1.配置系统
```

The folder name, BDD heading, and `Feature:` name must match exactly. This keeps navigation, prompts, scenarios, and generated reports aligned.

## Required Flow

1. Read `docs/INDEX.md` or `docs/README.md`, then choose or create the target ordered feature folder.
2. Create or update `BDD.md` in that folder before editing implementation details.
3. Identify the product value, user role, and intended behavior in plain business language.
4. Use Three-Amigos thinking: product scope, tester edge cases, and developer constraints.
5. Capture business rules first, then concrete examples.
6. Write main success scenarios, alternate scenarios, and exception scenarios.
7. Map each BDD scenario to a stable BDD ID and later test target.
8. Keep implementation mechanics out of `Given` and `When` unless the business behavior is explicitly technical.
9. Update the same folder's `ENGINEERING_SPEC.md` with links back to BDD IDs and rules.
10. Hand off to `$cx-tdd` only after BDD scenarios are clear enough to produce expected failing tests.

## BDD Format

Use Markdown as the durable project document and Gherkin-style blocks for scenarios:

```gherkin
Feature: 1.配置系统

  In order to keep local agents predictable
  As a project maintainer
  I want configuration changes to be validated before they are applied

  Rule: Invalid configuration is rejected before persistence

    Scenario: BDD-CONFIG-001 - Reject missing required model name
      Given a project configuration without a model name
      When the maintainer validates the configuration
      Then validation fails with a required-field message
      And the existing configuration is not overwritten
```

## Scenario Rules

- Use one observable behavior per scenario.
- Prefer 3 to 5 steps per scenario.
- `Given` describes known context, not user interaction.
- `When` describes the event or action.
- `Then` describes an observable result.
- Use `Rule:` to group scenarios by business rule.
- Use `Scenario Outline` only when example tables reduce duplication without hiding intent.
- Every exception scenario must state cause, system response, user-visible outcome, and evidence or logging expectation.

## Output

Every BDD update should leave:

- An ordered feature folder under `docs/`.
- A `BDD.md` whose heading and `Feature:` match the folder name.
- Stable BDD IDs.
- Main, alternate, and exception scenarios.
- Business rules and open questions.
- Links from `ENGINEERING_SPEC.md` to the BDD IDs.
