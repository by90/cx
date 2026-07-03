# 调研笔记

本包基于当前 Codex customization 模型：

- `AGENTS.md` 是 coding agents 的持久仓库指导。
- Skills 是可复用工作流，以包含 `SKILL.md` 的目录保存。
- 仓库级 skills 放在 `.agents/skills` 下被发现。
- Skills 可以通过 `$skill-name` 显式调用，也可以根据 description 被隐式选择。
- 自定义 subagents 放在 `.codex/agents/*.toml`。
- Codex 只有在用户明确要求时才会启动 subagents。

参考资料：

- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/codex/concepts/customization
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- https://agents.md/

核心设计决策是保留“先文档明确边界，再按任务实现”的阶段纪律，但默认不进入单元测试或 TDD。AI 默认完成当前任务文档后只编辑一个生产代码文件；如果需要第二个代码文件，必须先拆成下一个任务。`docs/cx` 可以保存项目说明和业务领域说明；每个主成功场景一个文件夹；任务进入 `tasks/`；变更进入 `changes/`。代码、文档、教程、研究、设计和流程变更等交付物完成后都必须通过 `$cx-review`，交付前再通过 `$cx-evidence`。这样能让 AI 从未完成变更判断下一步，同时避免按需求生成散落文档、一次性实现多个文件、默认补测试或绕过审查。
