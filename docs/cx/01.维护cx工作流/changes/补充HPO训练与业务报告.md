# 变更：补充 HPO 训练与业务报告

## 当前事实

- `$cx-pytorch-hpo` 要求保存逐轮轨迹，但没有固定面向用户的逐轮训练报告字段。
- 参数试验完成报告没有计算模型相对无信息理论基准损失消除了多少可改善损失。
- 股票排名业务报告和人工过拟合、欠拟合、损失平台诊断没有形成统一完成口径。

## 目标状态

- 逐轮报告训练轮次、验证损失改进次数、早停计数、训练损失和验证损失。
- study 启动前冻结与当前损失定义、权重、归约和标签分布一致的无信息理论基准损失及理论下界。
- 参数试验结束后报告最小验证损失相对理论基准的绝对改善、相对改善百分比和可改善损失完成率。
- 股票排名任务报告动态 TopN、固定 Top1、Top3 和 Top10；动态 TopN 作为不同标签刻度之间的统一业务比较标准，同时保留刻度和 N 的定义。
- 人工结合逐轮训练与验证损失评估过拟合、欠拟合或无法判断，并记录验证损失平台开始轮次和证据。
- 所有新增字段默认只用于报告和诊断，不改变项目冻结的搜索目标、晋级、剪枝、早停、检查点或严格测试隔离规则。

## 顺序工作清单

1. 修改 `00.设计.md` 和原任务 `tasks/04.同步双语安装包.md` 的当前规则与验证方式。
2. 修改中文 `$cx-pytorch-hpo` 技能源及中文安装包镜像。
3. 修改中文轨迹分析工具，使机器可读分析真实生成理论损失完善度、业务排名和平台轮次字段。
4. 同步英文 `$cx-pytorch-hpo` 技能源、轨迹分析工具及英文安装包镜像。
5. 执行双语技能、安装包、镜像、编码和静态规则验证。
6. 使用 `$cx-review` 完成交付物质量审查和完成证据门禁。

## 文件范围

- `docs/cx/01.维护cx工作流/00.设计.md`
- `docs/cx/01.维护cx工作流/tasks/04.同步双语安装包.md`
- `SKILLS/zh/cx-pytorch-hpo/SKILL.md`
- `SKILLS/zh/cx-pytorch-hpo/scripts/analyze_hpo_progress.py`
- `packages/zh/.agents/skills/cx-pytorch-hpo/SKILL.md`
- `packages/zh/.agents/skills/cx-pytorch-hpo/scripts/analyze_hpo_progress.py`
- `SKILLS/en/cx-pytorch-hpo/SKILL.md`
- `SKILLS/en/cx-pytorch-hpo/scripts/analyze_hpo_progress.py`
- `packages/en/.agents/skills/cx-pytorch-hpo/SKILL.md`
- `packages/en/.agents/skills/cx-pytorch-hpo/scripts/analyze_hpo_progress.py`

## 验证方式

- 核对中英文规则对逐轮训练报告、理论损失完善度、股票排名报告和人工拟合诊断的语义等价。
- 核对技能源与对应安装包镜像逐字一致。
- 运行仓库现有双语发行静态验证和 `skill-creator` 快速校验。
- 运行 `git diff --check`。
