# ENGINEERING_SPEC.md

这是某个功能组的长期研发主文档。单功能项目可以把它放在 `docs/ENGINEERING_SPEC.md`；多功能组项目应放在 `docs/<feature-group>/ENGINEERING_SPEC.md`，并从 `docs/INDEX.md` 链接到这里。

## 0. Document Rules

- 本功能组的需求、BDD 场景、架构、任务队列、测试矩阵、复用组件决策和验证证据都放在这里。
- 同一目录下的 `CHANGELOG.md` 只记录本功能组历史。
- 每个 `CHANGE-*` 条目都必须出现在同一文档集的 `CHANGELOG.md` 和这里。
- 每个新增或变化的行为都应该有主成功场景、必要分支场景和异常场景。
- 每个 BDD 场景都应该在实现前映射到测试；文档完成后必须等待用户确认，确认后才能写测试和实现。

## 1. Product Intent

TODO：描述产品、用户、当前目标和非目标。

## 2. Change Index

- CHANGE-2026-001：初始安装 cx 工作流。

## 3. Behavior Map

| Area | Behavior | BDD IDs | Notes |
| --- | --- | --- | --- |
| Workflow | 研发从目标文档集和变更记录开始 | BDD-CX-001 | 初始策略 |

## 4. BDD Scenarios

### Scenario: BDD-CX-001 - 开发使用文档集 BDD/TDD 工作流

Main success scenario:

Given 开发者提出功能或缺陷需求
When 助手规划并实现该工作
Then 它在实现前更新目标研发主文档和变更记录
And 它停止并等待用户确认文档和下一步实现计划
And 用户确认后，它先写失败测试再写生产代码
And 测试通过后记录验证证据

Alternate scenarios:

- 单功能项目可以直接使用 `docs/ENGINEERING_SPEC.md` 和 `docs/CHANGELOG.md`。
- 多功能组项目应使用 `docs/<feature-group>/ENGINEERING_SPEC.md` 和同目录 `CHANGELOG.md`。

Exception scenarios:

- 如果缺少目标文档集，先创建文档集并登记到 `docs/INDEX.md`。
- 如果 `CHANGE-*` 只出现在 changelog 而没有映射回研发主文档，交付前验证必须失败。

- Related change: CHANGE-2026-001
- Business rule: 工作必须在目标文档集中保持可搜索、可审计。
- Edge cases: 紧急 bugfix、重构、Python ML、Rust UI、复用组件抽取。
- Related tests: `tools/validate_single_source.py`, `tools/validate_skill_pack.py`, `tools/validate_cx_pack.py`

## 5. Technical Architecture

TODO：描述重要模块、接口、数据流、错误处理和集成边界。

## 6. Test Matrix

| BDD ID | Test command | Expected red | Status |
| --- | --- | --- | --- |
| BDD-CX-001 | `python tools/validate_single_source.py .` | 如果 docs 缺失、出现孤立文档或 change ID 未映射，则失败 | Active |

## 7. Task Queue

| Task | Source | Status | Notes |
| --- | --- | --- | --- |
| 安装 cx 包 | CHANGE-2026-001 | done | 将 TODO 章节替换为项目内容。 |

## 8. Reusable Component Registry

| Component | Purpose | Public API | Owners/Callers | Tests | Migration notes |
| --- | --- | --- | --- | --- | --- |
| indexed_series | 按实体、分类或窗口索引的长序列封装 | TODO | TODO | TODO | TODO |
| progress_ui | 多任务进度状态和适配器 | TODO | TODO | TODO | TODO |
| ragged_tensors | 变长 tensor 工具 | TODO | TODO | TODO | TODO |
| lightning_test_harness | 小型确定性 Lightning 测试夹具 | TODO | TODO | TODO | TODO |
| gpui_state_model | Rust UI 纯状态和 reducer | TODO | TODO | TODO | TODO |

## 9. Verification Evidence

| Date | Change | Command | Result | Notes |
| --- | --- | --- | --- | --- |
| 2026-05-13 | CHANGE-2026-001 | `python tools/validate_single_source.py examples/python_ml_project` | pass | 示例验证 |

## 10. Decision Log

| Date | Decision | Reason | Consequences |
| --- | --- | --- | --- |
| 2026-05-13 | 使用目标研发文档集和变更记录 | 避免文档膨胀，让 AI 任务可搜索 | 需要流程纪律和验证脚本 |
