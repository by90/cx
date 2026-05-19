---
name: cx-tdd
description: 用于 BDD 明确后的测试驱动开发：red-green-refactor、最窄失败测试、测试矩阵、代码质量门槛和验证证据。
version: 1.0.0
---

# cx TDD 实现纪律

## 目的

在 `$cx-bdd` 已经定义行为后使用本 skill。TDD 将 BDD 示例变成可执行测试，强制小步设计，并阻止助手直接写未经验证的生产代码。

## 必须执行的流程

1. 阅读目标功能文件夹中的 `BDD.md`、`ENGINEERING_SPEC.md` 和 `CHANGELOG.md`。
2. 选择一个 BDD ID 和一个可观察行为。
3. 确认提示词提供了验证命令，或从仓库中推断最窄的现有命令；两者都做不到时，先询问再实现。
4. 实现前先新增或更新 Test Matrix。
5. 先写最窄的失败测试。
6. 运行测试并记录预期 red failure。
7. 写能让测试通过的最小生产代码。
8. 运行最窄测试直到 green。
9. 只有 green 以后才重构，并且重构期间保持测试 green。
10. 变更影响共享行为时，运行更宽的验证。
11. 在目标功能文件夹中记录命令、结果和残留缺口。

## 代码质量规则

- 严禁堆砌式混乱代码。行为必须放在有名字的类型、小方法和明确接口后面。
- 当行为具有状态、生命周期、不变量或领域对象协作时，使用面向对象设计。
- 优先使用显式属性、方法、构造器、协议、trait 或接口，而不是动态反射。
- 默认禁止 Python `getattr`、`setattr`、`delattr`、monkey patch、动态注入方法或字符串分发。
- 如果确实需要动态反射，必须先证明没有更清晰的静态 API，记录理由，增加针对性测试，并把它隔离在小适配器里。
- 避免全局可变状态、隐藏 singleton、兜底式异常吞噬和过度 mock 的测试。
- 公共 API 必须小，并通过测试体现文档作用。
- 最终输出前，按提示词契约审查 diff：目标是否达成、约束是否遵守、验证是否运行、残留风险是否说明。

## Test Matrix 格式

```text
BDD-CONFIG-001 -> tests/test_config.py::ConfigValidationTest::test_missing_model_name_is_rejected
Expected red: validator currently accepts missing model names
Command: uv run python -m unittest tests.test_config.ConfigValidationTest.test_missing_model_name_is_rejected
```

## 输出

每个 TDD 循环都应该留下：

- BDD ID 到测试的映射。
- 已记录的 red failure。
- 最小实现。
- green 测试结果。
- 如发生重构，记录重构说明。
- 更新后的验证证据。
