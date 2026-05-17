# ENGINEERING_SPEC.md

这是某个功能组的长期研发主文档。单功能项目可以把它放在 `docs/ENGINEERING_SPEC.md`；多功能组项目应放在 `docs/<feature-group>/ENGINEERING_SPEC.md`，并从 `docs/INDEX.md` 链接到这里。

## 0. Document Rules

- 本功能组的业务目标、BDD 场景、架构、测试矩阵、复用组件决策和验证证据都放在这里。
- 同目录 `CHANGELOG.md` 是唯一按顺序记录变更和变更任务的文档；不要把具体变更编号复制到这里。
- 本文件不能包含具体变更编号；如果需要安排变更任务，请更新同目录 `CHANGELOG.md`。
- 每个新增或变化的业务行为都应该有主成功场景、必要分支场景和异常场景。
- 编程任务在实现前映射测试；非编程任务不使用 TDD，而是记录检查清单、审阅证据或交付确认。

## 1. Product Intent

TODO：描述产品、用户、当前目标和非目标。

## 2. Feature Scope

| Scope | Included | Excluded | Notes |
| --- | --- | --- | --- |
| Workflow | 使用目标文档集表达业务行为和验证证据 | 在主规格文档中排序变更任务 | 变更顺序只在 `CHANGELOG.md` 中维护 |

## 3. Behavior Map

| Area | Behavior | BDD IDs | Notes |
| --- | --- | --- | --- |
| Workflow | 研发从目标文档集和变更记录开始 | BDD-CX-001 | 初始策略 |

## 4. BDD Scenarios

### Scenario: BDD-CX-001 - 开发使用文档集 BDD 工作流

Main success scenario:

Given 开发者提出功能或缺陷需求
When 助手规划并实现该工作
Then 它在目标研发主文档描述业务行为和验收标准
And 它在同目录变更记录中按顺序记录变更任务
And 它为编程行为先写失败测试再写生产代码
And 测试或检查通过后记录验证证据

Alternate scenarios:

- 单功能项目可以直接使用 `docs/ENGINEERING_SPEC.md` 和 `docs/CHANGELOG.md`。
- 多功能组项目应使用 `docs/<feature-group>/ENGINEERING_SPEC.md`、同目录 `CHANGELOG.md` 和可选 `GUIDE.md`。
- 文档、研究、安装、配置或审查等非编程任务不启动 TDD，只记录目标、检查结果和证据。
- 可复用组件抽取前，先搜索现有项目、相关 skills、历史项目和本功能组 Reusable Component Registry。

Exception scenarios:

- 如果缺少目标文档集，先创建功能组目录并登记到 `docs/INDEX.md`。
- 如果具体变更编号出现在本文件，交付前验证必须失败，并移动到同目录 `CHANGELOG.md`。
- 如果测试不可运行，必须记录原因、替代验证和剩余风险。

- Business rule: 工作必须在目标文档集中保持可搜索、可审计，同时让变更顺序只在 changelog 中维护。
- Edge cases: 紧急 bugfix、重构、Python ML、Rust UI、复用组件抽取、纯文档任务。
- Related tests: `tools/validate_single_source.py`, `tools/validate_skill_pack.py`, `tools/validate_cx_pack.py`

## 5. Technical Architecture

TODO：描述重要模块、接口、数据流、错误处理和集成边界。

## 6. Test Matrix

| BDD ID | Test command | Expected red | Status |
| --- | --- | --- | --- |
| BDD-CX-001 | `python tools/validate_single_source.py .` | 如果 docs 缺失、出现孤立文档或具体变更编号写入主规格文档，则失败 | Active |

## 7. Implementation Notes

| Topic | Notes | Status |
| --- | --- | --- |
| Adoption | 将 TODO 章节替换为项目内容；变更任务顺序写入 `CHANGELOG.md` | planned |

## 8. Reusable Component Registry

| Component | Purpose | Public API | Owners/Callers | Tests | Migration notes |
| --- | --- | --- | --- | --- | --- |
| indexed_series | 按实体、分类或窗口索引的长序列封装 | TODO | TODO | TODO | TODO |
| progress_ui | 多任务进度状态和适配器 | TODO | TODO | TODO | TODO |
| ragged_tensors | 变长 tensor 工具 | TODO | TODO | TODO | TODO |
| lightning_test_harness | 小型确定性 Lightning 测试夹具 | TODO | TODO | TODO | TODO |
| gpui_state_model | Rust UI 纯状态和 reducer | TODO | TODO | TODO | TODO |

## 9. Verification Evidence

| Date | Source | Command | Result | Notes |
| --- | --- | --- | --- | --- |
| 2026-05-13 | BDD-CX-001 | `python tools/validate_single_source.py examples/python_ml_project` | pass | 示例验证 |

## 10. Decision Log

| Date | Decision | Reason | Consequences |
| --- | --- | --- | --- |
| 2026-05-13 | 使用目标研发文档集、独立变更记录和版本索引 | 避免文档膨胀，让 AI 任务可搜索 | 需要流程纪律和验证脚本 |
