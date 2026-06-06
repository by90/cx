---
name: cx-pytorch-hpo
description: 用于 PyTorch、Lightning 和时间序列项目的广义自动调参、实验设计和试验证据；覆盖超参数、样本组成、特征启用/禁用、特征范围、分级数组、标签定义、模型结构和模型选择。默认主工具是 Optuna，Ray Tune 只作为分布式执行外壳，BoTorch/Ax 只用于昂贵连续空间的贝叶斯优化。
version: 0.1.0
---

# cx PyTorch 广义自动调参

## 目的

把“调参”视为可审计的实验设计，而不是只搜索学习率、batch size 或 optimizer。适用于 PyTorch/Lightning 训练、特征 recipe、标签 recipe、模型结构和模型选择。

## 铁律

1. 自动调参先使用约十分之一的数据，但抽样单位必须是完整实体，不允许只截取实体的一部分记录。比如 2000 只股票的日线数据，应随机选择约 200 只股票，并保留这 200 只股票的完整日线。
2. 这份十分之一完整数据用于快速确定超参数、模型容量参数、特征分级数组、停牌处理策略、optimizer 选择和 scheduler 选择；不能用破碎样本替代完整实体样本。
3. 调参训练一般固定 60 个 epochs；必须确保 60 个 epochs 内不会被早停截断。
4. Early stopping 的 patience 一般设为 8，但这只是记录观察信号，不允许在 60 个 epochs 内真正停止训练。
5. 如果业务或算力必须偏离十分之一完整数据、60 epochs 或 patience=8，必须先在目标文档集记录理由、风险和替代验证方式。

## 必须执行的流程

1. 先确认目标功能文档集已经定义业务目标、评估指标、数据边界和用户确认；缺少这些时先回到 `$cx-bdd` 或 `$cx-research`。
2. 先写固定 baseline recipe，再允许自动搜索；baseline 必须能用小真实数据和 `unittest` 跑通。
3. 把搜索对象建模为 typed config recipe：`data_recipe`、`feature_recipe`、`label_recipe`、`model_recipe`、`training_recipe`、`evaluation_recipe`。
4. 所有可调项必须来自 config 子系统，并且都有默认值；禁止脚本命令行参数、环境变量临时开关或字符串分发。
5. 默认使用 Optuna 作为主工具：用 define-by-run 条件搜索空间表达特征开关、特征范围、分级数组、标签版本、模型类型、模型结构和训练超参数。
6. 默认使用 Optuna pruning 和 SQLite/RDB storage 记录 trial；小项目优先 SQLite，团队或长时间运行再迁移到共享数据库。
7. 只有需要多机、多 GPU、资源调度或复杂早停调度时，才把 Ray Tune 作为执行外壳；搜索算法仍可使用 OptunaSearch。
8. 只有连续变量维度较低、单次试验昂贵、需要贝叶斯 surrogate 或多目标优化时，才考虑 BoTorch/Ax。
9. 每个 trial 必须重建完整 recipe，避免只改训练循环而遗漏数据、特征或标签变更。
10. 调参不能直接在单元测试中跑完整搜索；单元测试只验证 recipe 构造、objective 包装、trial 到 config 的映射、指标计算和持久化路径。
11. 搜索后必须复跑 best recipe，并把 best trial、搜索空间、失败 trial、pruned trial、指标、随机种子和数据版本写入目标文档集验证证据。

## 工具选择

- **Optuna 是默认主工具**：适合动态条件搜索空间、离散/连续/分类变量、特征子集、模型选择、pruning、trial importance 和 SQLite 记录。
- **Ray Tune 是规模化外壳**：当本地 Optuna 不够并行、需要 GPU 资源调度或 ASHA/PBT 这类调度器时使用。
- **BoTorch/Ax 是专项工具**：适合昂贵、连续、低到中维、多目标或带约束的贝叶斯优化，不作为默认入口。
- **Lightning Tuner 是局部辅助**：只用于学习率或 batch size 这类局部探测，不能替代完整实验搜索。

## 搜索空间规则

- 特征启用/禁用用显式布尔或分类配置表达，不允许用字符串列表在 objective 中临时解析。
- 特征范围、分桶边界、分级数组必须是命名候选配置；需要连续边界时，用 typed config 表达上下限和默认值。
- 标签定义、预测目标、损失函数、采样策略和样本时间窗口都属于可调 recipe，但必须有业务解释和泄漏检查。
- 模型结构和模型选择可以进入搜索空间，例如 `model_family`、hidden size、layers、dropout、encoder length；每个候选都必须有最小测试覆盖。
- Trial importance 只能说明搜索空间内的经验敏感度，不能当作因果特征重要性；关键特征结论必须用 ablation、permutation 或业务审查复核。

## 验证证据

- Baseline recipe 和指标。
- Search space 的 config schema、默认值和候选值。
- Optuna study 名称、storage、sampler、pruner、trial 数量和 best trial。
- Best recipe 复跑命令和结果。
- 特征、标签、模型结构变更的业务解释和泄漏检查。
- 跳过 Ray Tune、BoTorch/Ax 或 Lightning Tuner 的理由。

## 主要参考

- Optuna：默认主工具，适合 define-by-run 动态搜索空间、pruning、importance 和 RDB storage。
- Ray Tune：仅用于分布式资源调度和大规模 trial 执行。
- BoTorch/Ax：仅用于高成本贝叶斯优化。
- PyTorch 官方 HPO 教程：作为 PyTorch 训练循环与调参集成参考。
