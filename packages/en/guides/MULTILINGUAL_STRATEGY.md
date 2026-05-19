# Multilingual Strategy

## Recommendation

Maintain one GitHub repository with two installable language packages:

```text
packages/en
packages/zh
```

The skill names and agent names must be identical in both packages and must start with `cx-`. The language changes only human-facing content: descriptions, instructions, templates, guides, and examples.

## Why not install both languages into one target project

Codex discovers skills by scanning `.agents/skills` from the current working directory up to the repository root. If two skills share the same `name`, they are not merged; both may appear. That creates ambiguity and wastes context. Install only one language pack into the target repository.

## GitHub README approach

Put a short `README.md` in the repository root and link to `README.zh-CN.md`. GitHub renders the root README as the primary visitor page and relative links keep the repository usable after cloning.

## Naming stability

Keep names stable across language packages. During pre-1.0 development, interface and workflow changes use minor versions while the major version stays `0`; after `1.0.0`, incompatible renames require a major release:

- `$cx-bdd`
- `$cx-tdd`
- `$cx-changelog`
- `$cx-version`
- `$cx-research`
- `$cx-pytorch-tdd`
- `$cx-rust-tdd`
- `$cx-common-module`
- `$cx-evidence`

Consistent names let users write prompts, tutorials, and automation once, then choose the language package separately.
