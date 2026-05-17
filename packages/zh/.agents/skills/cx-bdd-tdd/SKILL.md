---
name: cx-bdd-tdd
description: 用于 feature、bugfix、requirements、architecture、implementation planning、BDD scenarios、TDD tests、changelog updates 和 AI-assisted coding workflow。
version: 1.0.0
---

# cx BDD/TDD 文档集工作流

## 目的

使用本 skill 将研发固定在 `docs/` 下的一个或多个研发文档集上。小项目可以使用 `docs/ENGINEERING_SPEC.md` 和 `docs/CHANGELOG.md`；多组功能必须使用 `docs/<feature-group>/ENGINEERING_SPEC.md` 和 `docs/<feature-group>/CHANGELOG.md`，并在 `docs/INDEX.md` 或 `docs/README.md` 维护索引和说明。

## 必须执行的流程

1. 规划前先阅读 `docs/INDEX.md` 或 `docs/README.md`，再阅读目标文档集的 `ENGINEERING_SPEC.md` 和 `CHANGELOG.md`。
2. 如果功能属于新功能组，先创建 `docs/<feature-group>/` 文档集，并把它登记到根索引。
3. 在目标文档集内创建或更新一个相关的 `CHANGE-YYYY-NNN` 条目。
4. 更新目标研发主文档已有章节，不要创建新的零散规划文件。
5. 先新增或修订业务场景：主成功场景、分支场景和异常场景，再写实现细节。
6. 代码变更前先补测试矩阵，并让每个主成功、分支或异常场景都能映射到测试或明确说明不测原因。
7. 先写最窄的失败测试，并运行命令证明它按预期失败。
8. 实现能通过失败测试的最小改动。
9. 测试通过后再重构。
10. 将验证命令和结果记录到目标研发主文档。
11. 新增或修改代码时，代码文件、类、函数和关键语句都必须写面向初学者的相近说明注释；默认逐行解释代码意图，除非该行是纯格式或重复结构。

## BDD 场景格式

```gherkin
Scenario: BDD-AREA-001 - 简短行为标题
  Given <初始上下文>
  When <事件>
  Then <可观察结果>
```

场景中要包含业务规则、边界场景、关联 change ID 和关联测试。BDD ID 应该能跨重构长期保留。

## 业务场景结构

每个复杂行为都必须拆成：

```text
Main success scenario: 正常路径和最终可观察结果。
Alternate scenarios: 合法分支、可选路径、不同角色或不同输入形态。
Exception scenarios: 错误输入、缺失数据、权限失败、外部依赖失败和必须抛出的异常。
```

异常场景不能只写“处理失败”；必须说明失败原因、系统响应、用户可见结果和是否写入日志或验证证据。

## TDD 矩阵格式

```text
BDD-AREA-001 -> tests/test_file.py::TestClass::test_behavior
Expected red: <实现前为什么会失败>
Command: python -m unittest tests.test_file.TestClass.test_behavior
```

## 文档规则

不要创建孤立的 `spec.md`、`plan.md`、`tasks.md` 或随意设计文档。需要计划时，把计划写入目标文档集 `ENGINEERING_SPEC.md` 的 Task Queue 章节。

中文版本或中文交付物中的所有文档必须使用简体中文，并且长期保留的文档必须放在项目的 `docs/` 文件夹下。

BDD 场景、测试矩阵、实现计划和验证证据必须写入项目 `docs/` 文件夹中的目标研发文档集。多功能组项目中，`docs/` 根目录只放索引和说明；具体功能文档放在 `docs/<feature-group>/`。

## 文档集布局

单功能项目可以使用：

```text
docs/ENGINEERING_SPEC.md
docs/CHANGELOG.md
```

多功能组项目使用：

```text
docs/INDEX.md
docs/<feature-group>/ENGINEERING_SPEC.md
docs/<feature-group>/CHANGELOG.md
```
