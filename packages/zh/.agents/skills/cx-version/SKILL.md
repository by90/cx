---
name: cx-version
description: 用于 cx 包发布版本管理、SemVer 升级判断、Keep a Changelog 发布说明、带注释 Git tag、GitHub Release 和发布验证证据。
version: 1.0.0
---

# cx 发布版本管理

## 目的

准备、审查或说明 cx 包发布版本时使用本 skill。发布机制必须保持标准化：一个 SemVer 版本值、一份面向人的 changelog、一个带注释 Git tag，以及按需创建的 GitHub Release。

## 标准机制

1. 仓库根目录 `VERSION` 是唯一版本来源。它只保存 SemVer 值，例如 `2.0.0`，不带前缀 `v`。
2. `packages/en/manifest.json` 和 `packages/zh/manifest.json` 必须复制 `VERSION` 中完全相同的版本。
3. 根目录 `CHANGELOG.md` 遵循 Keep a Changelog。顶部保留 `## [Unreleased]`，每次发布新增 `## [X.Y.Z] - YYYY-MM-DD`。
4. Git 发布 tag 使用常见的 `vX.Y.Z` 名称。tag 名称带 `v`，SemVer 值本身不带 `v`。
5. 发布使用带注释 Git tag，例如 `git tag -a v2.0.0 -m "Release 2.0.0"`。
6. 如果创建 GitHub Release，它必须指向匹配 tag，并使用 changelog 对应版本章节作为发布说明。
7. 打 tag 前运行 `python tools/cx_version.py check .` 和 `python tools/validate_release.py .`。

## 版本升级规则

- `1.0.0`：第一版稳定公开工作流/API 契约。
- Major：不兼容的公开契约变化，例如删除或重命名公开 skill、agent、安装路径、CLI 命令、文档集规则、提示词契约或工作流 API。
- Minor：向后兼容的公开接口或工作流能力变化，例如新增 skill、agent、模板、可选字段、验证命令或兼容工作流路径。
- Patch：文案修复、验证脚本 bug、示例、翻译或实现修复，且不改变公开工作流/API 契约。
- Prerelease：只有版本确实不是最终发布时，才使用 `2.1.0-rc.1` 这类 SemVer 预发布标识。

如果接口发生变化，必须先判断兼容性：兼容性新增使用 `1.1.0` 这类 minor；破坏兼容性使用 `2.0.0` 这类 major。

## 发布检查清单

1. 根据公开工作流影响判断下一个版本。
2. 更新 `VERSION` 和两份 package manifest。
3. 将 `CHANGELOG.md` 中 `Unreleased` 下的用户可见变更移动到新版本章节。
4. 运行版本和发布验证。
5. 提交发布文件。
6. 创建名为 `vX.Y.Z` 的带注释 tag。
7. 需要公开发布页或下载归档时，创建 GitHub Release。
