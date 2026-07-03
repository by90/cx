# Multilingual Strategy

## Recommendation

Maintain two installable language packages in one GitHub repository:

```text
packages/en
packages/zh
```

English and Chinese skill and agent names must match exactly and start with `cx-`. Language affects only human-facing content: descriptions, instructions, templates, guides, and examples.

## Synchronization Order

When this repository changes workflow rules, skills, templates, or examples, complete the Chinese package first, then synchronize the English package. The Chinese package is the rule source; the English package must keep the same structure and constraints.

## Document Language

A target project installs one language package only. With the English package installed, cx-generated and cx-maintained documents should use English. With the Chinese package installed, those documents must use Simplified Chinese. Code identifiers, commands, API names, library names, and external proper names may remain in their source language.

## Why Not Install Both

Codex discovers `.agents/skills` from the working directory upward. If two language packages use the same `name`, they may both appear instead of merging. That creates ambiguity and wastes context.

## Stable Names

- `$cx-workflow`
- `$cx-story`
- `$cx-tdd`
- `$cx-changelog`
- `$cx-version`
- `$cx-research`
- `$cx-pytorch-tdd`
- `$cx-pytorch-quick-hpo`
- `$cx-pytorch-full-hpo`
- `$cx-timeseries-modeling`
- `$cx-rust-tdd`
- `$cx-common-module`
- `$cx-review`
- `$cx-evidence`
