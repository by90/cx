---
name: cx-common-module
description: 用于 code duplication、shared utilities、reusable components、component extraction、API design、indexed-series-like data structures，以及判断 progress UI、ragged tensor handling、test harnesses 或 GPUI state 是否应该成为 common modules。
version: 1.0.0
---

# cx 复用组件与通用模块抽取

## 目的

将重复逻辑、稳定数据结构、测试夹具和 UI 状态模型变成小而稳定、经过测试的复用组件。AI 辅助编程很容易在多个地方生成相似代码，本 skill 用搜索、API、迁移和测试约束来阻止这种漂移。

## 复用发现

新增抽象前必须先搜索：

1. 当前项目的 `src/`、`tests/`、`docs/` 和目标文档集 Common Module Registry。
2. 已启用和之前完成的相关 skills，例如 `$cx-pytorch-tdd`、`$cx-ragged-tensor`、`$cx-rust-ui`、`$cx-progress-ui` 和本 skill。
3. 用户明确提到的既有项目、历史项目或历史实现，例如 `rise202604` 中的 `IndexedSeries`。
4. 相邻领域是否已有同构结构，例如 indexed series、packed tensor batch、ragged tensor、time-window dataset、GPUI state reducer。

搜索后必须记录候选、采用/拒绝理由和迁移影响；没有搜索证据时，不要新增复用组件。

## 何时抽取

至少满足以下之一时抽取通用模块：

- 同一逻辑出现在两个或更多地方。
- 某个行为重要到需要自己的 BDD 场景。
- 逻辑跨越项目区域，例如训练和 UI。
- 逻辑容易出错：indexed series、tensor padding、mask、进度同步、取消、metrics、checkpoint path 或 UI state reducer。
- 数据结构已经表达了稳定领域概念，例如按实体分组的长序列、窗口索引、批次打包、状态 reducer 或测试数据夹具。

如果抽象只是猜测，且只有一个不清晰用例，就不要抽取。

## 必须输出

- 搜索证据和候选实现对比。
- 公共 API 提案，包含输入、输出、错误策略和最小示例。
- 测试先行，优先覆盖真实小数据和边界条件。
- 兼容迁移计划，说明哪些调用点迁移、哪些保持不动。
- 更新目标文档集 `ENGINEERING_SPEC.md` 中的 Common Module Registry。
- 更新目标文档集 Test Matrix。

## Registry 字段

```text
Component | Purpose | Public API | Owners/Callers | Tests | Migration notes
```

## 初始模块优先级

1. `indexed_series` 或 `indexed_tensor_series`：按分类、实体或时间窗口索引的长序列封装。
2. `progress_ui`。
3. `ragged_tensors`。
4. `lightning_test_harness`。
5. `gpui_state_model`。
