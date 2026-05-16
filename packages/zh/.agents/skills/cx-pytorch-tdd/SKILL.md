---
name: cx-pytorch-tdd
description: 用于 Python、PyTorch、Lightning、tensor utilities、model training、data modules、metrics 和 ML tests，强制 unittest-first、小测试和当前 API 验证。
version: 1.0.0
---

# cx Python / PyTorch / Lightning TDD

## 目的

用于 Python ML 代码、PyTorch tensor 工具、LightningModule、DataModule、训练循环、metrics 和模型测试。

## 必须执行的流程

1. 阅读 `docs/ENGINEERING_SPEC.md` 中相关 BDD ID 和 Common Module Registry 条目。
2. API 行为可能受版本影响时，查询 PyTorch 和 Lightning 官方最新文档。
3. 默认先写 Python `unittest` 测试，除非项目已有明确例外。
4. 测试必须确定性、小规模、CPU 优先，除非目标行为就是 GPU 行为。
5. tensor 变换优先写成纯函数，Lightning orchestration 尽量保持很薄。
6. 代码遵循 Black 默认规范，不修改无关用户代码。

## Tensor 测试清单

- 断言 shape、dtype 和 device。
- 测试空输入、单项、多项和变长输入。
- 涉及 padding、mask、length 时必须测试语义。
- 测试确定性和重要边界条件。
- 当可微性属于目标行为时，测试梯度。

## Lightning 清单

- 测试 LightningModule 构造。
- 用极小 batch 测试纯 loss 函数或 `training_step`。
- 如果自定义 optimizer，测试 optimizer 配置。
- orchestration 测试使用 `fast_dev_run`、有限 batch、小模型和小数据。
- 不要把长训练循环放进单元测试。
