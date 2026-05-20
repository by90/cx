---
name: cx-bdd
description: 用于 BDD 发现、功能文件夹命名、业务规则、Gherkin 风格示例、验收标准、主成功/分支/异常场景，以及把行为映射到后续测试。
version: 0.1.0
---

# cx BDD 发现与场景文档

## 目的

实现和 TDD 之前先使用本 skill。BDD 是通过具体示例发现行为的协作层，不只是测试格式，也不应该和 TDD 合并成一个含混的流程。

## 文档集命名

`docs/` 下的功能文件夹必须使用带顺序号的业务功能名：

```text
docs/1.配置系统/
docs/2.用户会话/
docs/3.模型评估/
```

英文项目使用同样结构：

```text
docs/1.Configuration System/
docs/2.User Sessions/
docs/3.Model Evaluation/
```

文件夹里的 BDD 文档必须使用同一个名字：

```text
docs/1.配置系统/BDD.md
# BDD: 1.配置系统

Feature: 1.配置系统
```

文件夹名、BDD 标题和 `Feature:` 名称必须完全一致。这样导航、提示词、场景和生成报告不会漂移。

## 必须执行的流程

1. 阅读 `docs/INDEX.md` 或 `docs/README.md`，再选择或创建目标编号功能文件夹。
2. 先创建或更新该文件夹中的 `BDD.md`，再写实现细节。
3. 用业务语言识别产品价值、用户角色和目标行为。
4. 使用 Three Amigos 思路：产品范围、测试边界、开发约束。
5. 先记录业务规则，再写具体示例。
6. 写主成功场景、分支场景和异常场景。
7. 每个 BDD 场景都要有稳定 BDD ID，并能映射到后续测试目标。
8. 除非业务行为本身就是技术能力，否则不要把实现细节写进 `Given` 和 `When`。
9. 通用功能、可复用功能或可复用类必须把调用模型写成可观察行为：公共入口、常规调用方式、特殊场景入口、实例或状态生命周期、状态来源、测试如何覆盖所有源码调用和非目标。
10. 通用/可复用功能的 BDD 场景优先描述调用方如何使用公共 API，而不是内部 helper 如何工作。
11. 在同一文件夹的 `ENGINEERING_SPEC.md` 中回链 BDD ID 和业务规则。
12. 同步同一文件夹的 `CHANGELOG.md`，让本次文档变更可审计。
13. 完成 BDD、研发主文档和变更记录后必须停止，向用户汇报文档结果和下一步实现计划。
14. 只有当用户明确确认继续，并且 BDD 场景足够清楚、能推导预期失败测试后，才交给 `$cx-tdd`。

## BDD 格式

长期项目文档使用 Markdown，场景块使用 Gherkin 风格：

```gherkin
Feature: 1.配置系统

  In order to keep local agents predictable
  As a project maintainer
  I want configuration changes to be validated before they are applied

  Rule: Invalid configuration is rejected before persistence

    Scenario: BDD-CONFIG-001 - Reject missing required model name
      Given a project configuration without a model name
      When the maintainer validates the configuration
      Then validation fails with a required-field message
      And the existing configuration is not overwritten
```

## 场景规则

- 一个场景只表达一个可观察行为。
- 每个场景优先保持 3 到 5 个步骤。
- `Given` 描述已知上下文，不写用户操作。
- `When` 描述事件或动作。
- `Then` 描述可观察结果。
- 使用 `Rule:` 按业务规则组织场景。
- 只有示例表能减少重复且不隐藏意图时，才使用 `Scenario Outline`。
- 每个异常场景都必须说明失败原因、系统响应、用户可见结果，以及证据或日志预期。
- 通用功能、可复用功能或可复用类至少应包含一个常规调用场景；如果存在测试目录、临时配置、替代数据源或不同运行环境，还应包含特殊入口场景和恢复场景。

## 输出

每次 BDD 更新都应该留下：

- `docs/` 下的编号功能文件夹。
- `BDD.md`，且标题和 `Feature:` 与文件夹名一致。
- 稳定 BDD ID。
- 主成功、分支和异常场景。
- 业务规则和未决问题。
- `ENGINEERING_SPEC.md` 到 BDD ID 的回链。
- 等待用户确认后才能进入 TDD 的下一步计划。
