# 调研笔记

本包基于当前 Codex customization 模型：

- `AGENTS.md` 是 coding agents 的持久仓库指导。
- Skills 是可复用工作流，以包含 `SKILL.md` 的目录保存。每个 skill 需要 `name` 和 `description`。
- 仓库级 skills 放在 `.agents/skills` 下被发现。
- Skills 可以通过 `$skill-name` 显式调用，也可以根据 description 被隐式选择。
- 自定义 subagents 放在 `.codex/agents/*.toml`。每个 custom agent 需要 `name`、`description` 和 `developer_instructions`。
- Codex 只有在用户明确要求时才会启动 subagents。

参考资料：

- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/codex/concepts/customization
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- https://agents.md/

核心设计决策是保留 Spec/Plan/Tasks 的阶段纪律，但把长期产物压缩进 `docs/` 下的文档集。小项目可以使用 `docs/ENGINEERING_SPEC.md` 和 `docs/CHANGELOG.md`；多功能组项目使用 `docs/INDEX.md`、`docs/VERSIONS.md` 加多个 `docs/<feature-group>/` 文档集。具体变更编号和任务顺序只在各功能组 `CHANGELOG.md` 中维护，非编程任务不使用 TDD。这样既能保留可测试行为和审计历史，又能防止按需求生成文档垃圾。
