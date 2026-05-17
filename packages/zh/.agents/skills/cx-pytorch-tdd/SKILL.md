---
name: cx-pytorch-tdd
description: 用于 Python、PyTorch、Lightning、tensor utilities、model training、data modules、metrics、ML tests、uv 项目环境、Python/PyTorch/CUDA 稳定版本核对和测试数据策略；强制 unittest-first、小测试、少 mock 和当前 API 验证。
version: 1.0.0
---

# cx Python / PyTorch / Lightning TDD

## 目的

用于 Python ML 代码、PyTorch tensor 工具、LightningModule、DataModule、训练循环、metrics 和模型测试。

## 必须执行的流程

1. 阅读目标文档集 `ENGINEERING_SPEC.md` 中相关 BDD ID 和 Common Module Registry 条目。
2. 使用项目级 `uv` 虚拟环境；优先通过 `uv sync`、`uv run` 或项目已有 `uv` 工作流安装依赖和运行测试。
3. 创建或重建环境前，访问 Python 官网下载页和 PyTorch 官网 Start Locally 页，确认 Python、PyTorch、CUDA 选择的是当前官方稳定组合；不要默认使用 nightly、预发布或非官方轮子。
4. API 行为可能受版本影响时，查询 PyTorch 和 Lightning 官方最新文档。
5. 默认先写 Python `unittest` 测试；不要引入 `pytest`，除非项目已有明确例外。
6. 测试必须确定性、小规模、CPU 优先，除非目标行为就是 GPU 行为。
7. tensor 变换优先写成纯函数，Lightning orchestration 尽量保持很薄。
8. 新增 dataset、tensor 容器、indexed series 或 test harness 前，先叠加 `$cx-common-module` 搜索已有复用组件。
9. 代码遵循 Black 默认规范，不修改无关用户代码。

## 环境规则

- 使用项目根目录的 `uv` 环境，例如 `.venv`、`uv.lock` 和 `pyproject.toml` 所定义的环境。
- 如果必须新建环境，先核对 https://www.python.org/downloads/ 与 https://pytorch.org/get-started/locally/。
- 选择 PyTorch Stable 构建，并按官网矩阵选择 CPU 或 CUDA 轮子；CUDA 版本以 PyTorch 稳定版支持矩阵为准。
- 用 `uv run python -m unittest ...` 运行 Python 单元测试。

## 测试数据规则

- 优先使用真实但缩小的单元测试数据。
- 涉及数据库时，优先使用小型 SQLite 数据库或 fixture，而不是 mock 数据访问层。
- 只有外部服务、时间、随机性、昂贵硬件或不可控副作用难以真实控制时，才少量使用 mock。

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
