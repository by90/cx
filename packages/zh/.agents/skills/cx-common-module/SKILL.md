---
name: cx-common-module
description: 用于 code duplication、shared utilities，以及判断 progress UI、ragged tensor handling、test harnesses 或 GPUI state 是否应该成为 common modules。
version: 1.0.0
---

# cx 通用模块抽取

## 目的

将重复逻辑变成小而稳定、经过测试的通用模块。AI 辅助编程很容易在多个地方生成相似代码，本 skill 用 API 和测试约束来阻止这种漂移。

## 何时抽取

至少满足以下之一时抽取通用模块：

- 同一逻辑出现在两个或更多地方。
- 某个行为重要到需要自己的 BDD 场景。
- 逻辑跨越项目区域，例如训练和 UI。
- 逻辑容易出错：tensor padding、mask、进度同步、取消、metrics、checkpoint path 或 UI state reducer。

如果抽象只是猜测，且只有一个不清晰用例，就不要抽取。

## 必须输出

- 公共 API 提案。
- 测试先行。
- 兼容迁移计划。
- 更新 `docs/ENGINEERING_SPEC.md` 中的 Common Module Registry。
- 更新 Test Matrix。

## 初始模块优先级

1. `progress_ui`。
2. `ragged_tensors`。
3. `lightning_test_harness`。
4. `gpui_state_model`。
