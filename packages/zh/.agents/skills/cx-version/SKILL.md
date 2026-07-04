---
name: cx-version
description: 用于项目发布版本管理、项目内 SemVer 工具调用、版本升级判断、docs/VERSIONS.md、带注释 Git tag、GitHub Release 和发布验证证据。
version: 0.1.0
---

# cx 发布版本管理

## 语言规则

- 使用中文输出对话、说明、计划、总结、审查结论、验证证据和 cx 文档（本工作流维护的用例、任务、变更等文档）时，必须使用完整中文表达，不得写成中英文混杂的半句或词组堆叠。
- 只有代码标识符、命令、路径、接口名、库名、协议、标准名、外部专名，或翻译后会造成歧义的术语可以保留英文；保留英文时，必须在同句或相邻句用中文详细解释其含义、作用和当前上下文。

## 目的

准备、审查或说明项目发布版本时使用本 skill。发布机制必须标准化，并且优先使用目标项目内的无交互版本工具：

```bash
python tools/semver.py check --root .
python tools/semver.py next feature-group --root .
python tools/semver.py next patch --root .
python tools/semver.py prepare <version> "<title>" --root .
python tools/semver.py tag --root .
```

Codex App 需要结构化结果时，在 `check`、`next` 或 `prepare` 后追加 `--json`。

如果目标项目还没有该工具，把本 skill 目录下的 `scripts/semver.py` 复制为目标项目的 `tools/semver.py`，并在目标项目根目录提供 `VERSION` 与 `docs/VERSIONS.md`。

## 标准机制

1. 目标项目必须提供 `tools/semver.py`，或在发布前从本 skill 的 `scripts/semver.py` 复制同等实现；不要手写 `docs/VERSIONS.md` 条目代替工具。
2. 仓库根目录 `VERSION` 是唯一版本来源。它只保存 SemVer 值，例如 `0.1.0`，不带前缀 `v`。
3. 如果项目存在 `pyproject.toml`，其中 `[project].version` 必须与 `VERSION` 完全一致，并由 `tools/semver.py prepare` 同步。
4. `docs/VERSIONS.md` 是面向人的版本记录，标题使用 `## vX.Y.Z - 标题`。
5. Git 发布 tag 使用 `vX.Y.Z` 名称；tag 名称带 `v`，`VERSION` 值本身不带 `v`。
6. 发布使用带注释 Git tag，例如 `git tag -a v0.1.0 -m "Release 0.1.0"`；正常情况下由 `python tools/semver.py tag --root .` 创建。
7. 版本提交和发布 tag 只允许在 `main` 上创建。工作分支默认只保留在本地，除非用户在当前对话中明确覆盖 main-only 远端策略，否则不得 push；远端只应保留 `main` 和版本 tag。
8. cx 包自身发布仍可使用仓库根目录的 `tools/cx_version.py` 和 `tools/validate_release.py`；目标项目发布必须优先使用目标项目的 `tools/semver.py`。

## 版本升级规则

- 默认起点：新项目或未经验证的项目从 `0.0.1` 开始，除非用户明确说明项目已经达到 `1.0.0`。
- 默认升级：用户只要求更新、递增或准备版本号，但没有明确说明 minor、major、新功能组、稳定版或不兼容发布时，一律只更新最后一位 patch。
- Major `0`：项目尚未正式稳定；稳定接口和工作流契约变化是正常的。
- `0.x.x` 阶段新增功能组：只更新次版本，也就是 minor。例如 `0.1.3` 新增一个真实功能组时，下一版本应为 `0.2.0`。使用 `python tools/semver.py next feature-group --root .` 验证。
- `0.x.x` 阶段既有功能组内修改、bug 修复、文档调整、实现修复或小型重构：只更新最后一位，也就是 patch。例如 `0.1.3` 修复 `002_config` 内问题时，下一版本应为 `0.1.4`。使用 `python tools/semver.py next patch --root .` 验证。
- Pre-1.0 公开契约明显改变但不新增功能组时，默认按 patch 处理，除非用户明确把它归为新功能组或发布里程碑。
- `1.0.0`：第一版稳定公开工作流/API 契约，只有用户明确声明项目已经稳定后才使用。
- Post-1.0 minor：`1.0.0` 之后，`1.1.0` 表示向后兼容的公开新增。
- Post-1.0 major：`1.0.0` 之后，`2.0.0` 表示不兼容的公开契约变化。
- Prerelease：只有版本确实不是最终发布时，才使用 `0.2.0-rc.1` 这类 SemVer 预发布标识。

## 发布检查清单

1. 确认功能组或变更工作发生在独立本地分支上。
2. 判断发布类型：没有明确升级前置版本号时默认使用 `next patch`；只有新增功能组或用户明确要求 minor 时使用 `next feature-group`；既有功能组内修改、bugfix 或调整使用 `next patch`。
3. 请用户确认该版本已经完成并可以发布。
4. 用户确认后，把已完成的本地工作分支合并到 `main` 并删除本地分支。
5. 在 `main` 上运行 `python tools/semver.py check --root .`。
6. 在 `main` 上运行 `python tools/semver.py prepare <version> "<title>" --root . --feature-group <group> --summary "<summary>" --evidence "<evidence>"`。
7. 在 `main` 上重新运行项目测试和 `python tools/semver.py check --root .`。
8. 在 `main` 上提交 `VERSION`、`pyproject.toml` 和 `docs/VERSIONS.md` 等发布文件。
9. 在 `main` 上运行 `python tools/semver.py tag --root .` 创建带注释 tag。
10. push `main` 和发布 tag。
11. 需要公开发布页或下载归档时，创建 GitHub Release。

禁止在工作分支上创建版本提交或发布 tag。除非用户在当前对话中明确覆盖 main-only 远端策略，否则不要 push 工作分支。
