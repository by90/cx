---
name: cx-timeseries-modeling
description: 用于异构多变量时间序列建模、预测目标设计、字段语义分层、协变量设计、泄漏检查、backtesting、指标选择和 PyTorch 时间序列框架选型。默认以 PyTorch Forecasting 为主要参考框架，尤其使用 TimeSeriesDataSet 和 Temporal Fusion Transformer 的变量角色、门控和变量选择思路。
version: 0.1.0
---

# cx 异构时间序列建模

## 目的

处理每个字段含义不同的多变量时间序列。默认不要把字段当成图像像素、同质 channel 或普通 token；先建模字段语义，再选择卷积、注意力、RNN、N-HiTS、TFT 或其他模型。

## 必须执行的流程

1. 先定义预测目标、预测 horizon、时间粒度、实体分组、训练/验证/测试时间范围和业务指标。
2. 建立字段语义表：target、group id、static categorical、static real、time-varying known categorical/real、time-varying observed/unknown categorical/real、不可用未来字段、缺失策略、缩放策略和泄漏风险。
3. 默认使用 PyTorch Forecasting 作为主要参考框架：用 `TimeSeriesDataSet` 表达字段角色，用 Temporal Fusion Transformer 参考变量选择、静态上下文、门控和多 horizon 预测。
4. 不要默认使用普通 CNN、普通 Transformer 或把变量维度直接当 token；只有字段已经过角色化编码、泄漏检查和 baseline 对比后才允许。
5. 先建立 naive、seasonal naive、linear 或 tree baseline，再比较深度模型；不能只拿复杂模型互相比。
6. 深度模型候选按数据规模和目标选择：小数据优先 baseline/N-BEATS/N-HiTS，中等以上且有丰富协变量时考虑 TFT，概率预测需要 DeepAR 或分位数损失。
7. 多变量字段的注意力权重不能直接当作特征重要性；变量重要性需要结合变量选择网络、ablation、permutation 和业务审查。
8. 切分必须按时间或 rolling origin backtesting；禁止随机行切分导致未来信息泄漏。
9. 指标必须匹配业务目标：point forecast 可用 MAE/RMSE/SMAPE/MASE，分位数或概率预测必须记录 quantile loss、coverage 或 calibration。
10. 需要调特征、标签、模型结构或模型选择时，叠加 `$cx-pytorch-hpo`，并把搜索空间写成 config recipe。
11. 单元测试只验证数据窗口、字段角色、泄漏检查、指标和模型输入输出形状；不要在单元测试里跑长训练。

## 框架选择

- **PyTorch Forecasting 是主参考**：它的 `TimeSeriesDataSet` 能显式区分静态变量、已知未来变量和观测历史变量，TFT 提供变量选择、门控和解释入口，适合异构字段建模。
- **NeuralForecast 是辅助对照**：当需要更大的现代模型集合、快速 baseline 或 Auto 模型时使用，但仍要保留字段语义表和泄漏检查。
- **Darts 是编排辅助**：适合快速比较传统模型和 Torch 模型，但不要让统一 API 掩盖字段角色。
- **普通 Transformer/CNN 不是默认选择**：时间序列变量通常不是同质 token 或像素，除非模型结构明确处理变量语义。

## 建模证据

- 字段语义表和泄漏检查。
- Horizon、granularity、group id、target 和 label 定义。
- Baseline 指标和深度模型指标。
- Rolling-origin 或时间切分说明。
- 协变量是否在预测时可用的证明。
- 选择 PyTorch Forecasting、NeuralForecast、Darts 或其他框架的理由。
- 与 `$cx-pytorch-hpo` 共享的搜索空间、best recipe 和复跑结果。

## 研究提醒

- Transformer 在时间序列上并不天然优于简单线性或专用结构；每次使用注意力模型都必须有 baseline 对照。
- Patch、inverted transformer 和 channel-independent 结构可以作为候选，但不能绕过字段语义表。
- TFT 的解释结果是工程线索，不是因果证明。
