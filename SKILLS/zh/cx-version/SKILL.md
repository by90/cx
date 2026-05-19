---
name: cx-version
description: 用于 cx 包发布版本管理、SemVer 升级判断、Keep a Changelog 发布说明、带注释 Git tag、GitHub Release 和发布验证证据。
version: 0.0.1
---

# cx 发布版本管理

## 目的

准备、审查或说明 cx 包发布版本时使用本 skill。发布机制必须保持标准化：一个 SemVer 版本值、一份面向人的 changelog、一个带注释 Git tag，以及按需创建的 GitHub Release。

## 标准机制

1. 仓库根目录 `VERSION` 是唯一版本来源。它只保存 SemVer 值，例如 `0.0.1`，不带前缀 `v`。
2. `packages/en/manifest.json` 和 `packages/zh/manifest.json` 必须复制 `VERSION` 中完全相同的版本。
3. 根目录 `CHANGELOG.md` 遵循 Keep a Changelog。顶部保留 `## [Unreleased]`，每次发布新增 `## [X.Y.Z] - YYYY-MM-DD`。
4. Git 发布 tag 使用常见的 `vX.Y.Z` 名称。tag 名称带 `v`，SemVer 值本身不带 `v`。
5. 发布使用带注释 Git tag，例如 `git tag -a v0.0.1 -m "Release 0.0.1"`。
6. 如果创建 GitHub Release，它必须指向匹配 tag，并使用 changelog 对应版本章节作为发布说明。
7. 打 tag 前运行 `python tools/cx_version.py check .` 和 `python tools/validate_release.py .`。

## 版本升级规则

- 默认起点：新项目或未经验证的项目从 `0.0.1` 开始，除非用户明确说明项目已经达到 `1.0.0`。
- Major `0`：项目尚未正式发布；这个阶段公开接口和工作流契约变化是正常的。
- Pre-1.0 minor：当主版本号为 `0` 时，`0.1.0` 这类 minor 表示接口变化、工作流契约变化、skill/agent 新增、工作流重命名或文档集规则变化。
- Pre-1.0 patch：当主版本号为 `0` 时，`0.0.2` 这类 patch 表示文案修复、验证脚本 bug、示例、翻译或实现修复，且不改变公开契约。
- `1.0.0`：第一版稳定公开工作流/API 契约，只有项目完成并被明确声明稳定后才使用。
- Post-1.0 minor：`1.0.0` 之后，`1.1.0` 这类 minor 表示向后兼容的公开新增。
- Post-1.0 major：`1.0.0` 之后，`2.0.0` 这类 major 表示不兼容的公开契约变化。
- Prerelease：只有版本确实不是最终发布时，才使用 `0.2.0-rc.1` 这类 SemVer 预发布标识。

如果 `1.0.0` 之前接口发生变化，主版本号仍保持 `0`，并提升 minor。不要跳到 `1.0.0`，除非用户明确声明项目已经稳定。

## 发布检查清单

1. 先判断项目是否仍处于 pre-1.0；没有明确稳定声明时，主版本号保持 `0`。
2. 根据公开工作流影响判断下一个版本。
3. 更新 `VERSION` 和两份 package manifest。
4. 将 `CHANGELOG.md` 中 `Unreleased` 下的用户可见变更移动到新版本章节。
5. 运行版本和发布验证。
6. 提交发布文件。
7. 创建名为 `vX.Y.Z` 的带注释 tag。
8. 需要公开发布页或下载归档时，创建 GitHub Release。
