---
name: cx-bdd-tdd
description: 用于 feature、bugfix、requirements、architecture、implementation planning、BDD scenarios、TDD tests、changelog updates 和 AI-assisted coding workflow。
version: 1.0.0
---

# cx BDD/TDD 单一研发文档工作流

## 目的

使用本 skill 将研发固定在 `docs/ENGINEERING_SPEC.md` 和 `docs/CHANGELOG.md` 上。研发主文档是行为、设计、任务、测试、通用模块和验证证据的唯一来源。变更记录只是简洁的历史索引，不是第二份需求文档。

## 必须执行的流程

1. 规划前先阅读 `docs/ENGINEERING_SPEC.md` 和 `docs/CHANGELOG.md`。
2. 创建或更新一个相关的 `CHANGE-YYYY-NNN` 条目。
3. 更新研发主文档已有章节，不要创建新的规划文件。
4. 先新增或修订 BDD 场景，再写实现细节。
5. 代码变更前先补测试矩阵。
6. 先写最窄的失败测试，并运行命令证明它按预期失败。
7. 实现能通过失败测试的最小改动。
8. 测试通过后再重构。
9. 将验证命令和结果记录到研发主文档。

## BDD 场景格式

```gherkin
Scenario: BDD-AREA-001 - 简短行为标题
  Given <初始上下文>
  When <事件>
  Then <可观察结果>
```

场景中要包含业务规则、边界场景、关联 change ID 和关联测试。BDD ID 应该能跨重构长期保留。

## TDD 矩阵格式

```text
BDD-AREA-001 -> tests/test_file.py::TestClass::test_behavior
Expected red: <实现前为什么会失败>
Command: python -m unittest tests.test_file.TestClass.test_behavior
```

## 文档规则

不要创建孤立的 `spec.md`、`plan.md`、`tasks.md` 或随意设计文档。需要计划时，把计划写入 `docs/ENGINEERING_SPEC.md` 的 Task Queue 章节。
