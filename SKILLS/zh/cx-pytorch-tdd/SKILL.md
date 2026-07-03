---
name: cx-pytorch-tdd
description: 仅在用户当前请求、既有任务文档或变更文档明确声明需要 Python/PyTorch/Lightning 单元测试、TDD、tensor 测试或 ML 测试时使用；覆盖 uv 环境、Python/PyTorch/CUDA 稳定版本核对、小测试、少 mock 和当前 API 验证。
version: 0.1.0
---

# cx Python / PyTorch / Lightning 显式测试

## 目的

用于明确声明需要测试的 Python ML 代码、PyTorch tensor 工具、LightningModule、DataModule、训练循环、metrics 和模型测试。默认实现路径不主动创建或修改单元测试。

## 必须执行的流程

1. 先确认当前请求、任务文档或变更文档已经明确声明需要单元测试、TDD、tensor 测试或 ML 测试；没有明确声明时，返回 `$cx-workflow` 的默认单代码文件实现路径。
2. 阅读当前主成功场景文件夹中的 `00.用例.md`、`00. 设计.md`、当前 `changes/*.md` 和当前 `tasks/<编号.任务名>/00.任务.md`。
3. 使用项目级 `uv` 虚拟环境；Python 解释器优先使用 `uv` 安装和管理的版本，并通过 `uv sync`、`uv run`、`uv run --python <version>` 或项目已有 `uv` 工作流安装依赖和运行测试。
4. 创建或重建环境前，访问 Python 官网下载页和 PyTorch 官网 Start Locally 页，确认 Python、PyTorch、CUDA 选择的是当前官方稳定组合；不要默认使用 nightly、预发布或非官方轮子。
5. API 行为可能受版本影响时，查询 PyTorch 和 Lightning 官方最新文档。
6. 训练、数据准备、诊断和迁移脚本不得接收命令行参数；需要调整 batch、device、路径、seed、epoch、model variant 或诊断开关时，必须在 config 子系统定义带默认值的配置项，默认运行使用这些默认值。
7. 明确要求单元测试时使用 Python `unittest`；不要引入 `pytest`，除非项目已有明确例外。
8. 测试必须确定性、小规模、CPU 优先，除非目标行为就是 GPU 行为。
9. tensor 变换可以优先写成纯函数；只要涉及数据集状态、模型状态、训练状态、配置生命周期或领域不变量，就必须使用明确 OOP 建模。
10. 新增 dataset、tensor 容器、indexed series 或 test harness 前，先叠加 `$cx-common-module` 搜索已有可复用功能、类或组件。
11. 任务文档的基本量具是类或类型组；当前任务必须明确覆盖哪个 dataset、model、metric、config、tensor 容器或训练协作类型。
12. 遵循 `$cx-tdd` 的单代码文件边界、源码/测试布局和注释规则：源文件放在 `src/<subsystem>/`；明确要求测试时，测试镜像到 `tests/<subsystem>/`，源文件与 `*_test.py` 一一对应；源码和被声明的单元测试都必须有文件级作用说明、类说明、函数参数/返回说明和逐行意图注释。
13. 修改 Python 源码或测试后必须运行 Black 默认规范检查，例如 `python -m black --check src tests tools`；不修改无关用户代码。
14. 代码写完并完成必要验证后，必须使用 `$cx-review` 做代码交付物 review；重点核对实现是否与用例、设计、任务和变更文档一致，是否有重复 tensor/data/config 逻辑，是否完整 OOP，是否极简且无多余校验、变量传递、参数和命名。
15. review 不通过时，当前任务不得标记完成；先修复实现或文档，再重新验证和 review。

## 最小实现纪律

铁律：绝对禁止屎山代码。

- 默认选择能满足当前需求的最少代码实现，不提前框架化、泛化或抽象。
- 文件、类、方法和变量命名要短而清楚；避免把完整句子写进标识符，命名过长时优先提炼职责或复用领域术语。
- 不为单行转调、一次性逻辑或没有真实复用价值的流程创建函数、类、常量或校验器。
- 除非业务规则明确要求，不掩盖任何异常，不静默兜底，不把会导致产品问题的错误转成默认值、空结果、跳过、重试成功假象或 warning；开发期间应让这类错误中止运行。
- 判断标准很简单：如果同样错误发到产品会造成问题，就必须暴露为失败；只有业务明确要求降级、恢复或用户可见提示时，才允许写显式处理路径，并用测试覆盖。
- 不新增“看起来更安全”但需求没有要求的验证，例如文件名白名单、路径合法性检查、额外 AST 扫描、重复配置规则检查等。
- 严禁在大循环、训练循环、热路径或批处理内逐条检查数据合法性来兜底或拖慢性能；数据合法性应在入口、数据准备、测试夹具或单独诊断任务中处理，且不能替代真实失败。
- 默认不自行捕获或包装异常；底层库已经能给出清楚异常时，让原始异常直接抛出。
- 不创建自定义异常类型，除非调用方确实需要区分该异常并已有明确处理路径。
- 默认值优先通过函数或构造参数表达，不把简单路径、文件名或一次性默认值提升为模块级常量。
- 只保留当前行为需要的公开 API；不要增加调试入口、内存校验入口、扫描入口或预防未来需求的接口。
- 项目开发阶段绝不为旧代码保留兼容接口、旧入口、别名、适配层、桥接函数或新旧并存分支；不要考虑新旧代码兼容问题，改动后清除所有无用代码、旧路径、过时测试和废弃文档。
- YAML、JSON、数据库、文件系统等解析错误默认交给对应库或标准库处理；仅在业务规则明确要求时增加语义检查。
- 每个 helper 函数必须同时满足：有明确名字、减少重复或隔离真实复杂度、调用点不止一个或能显著提升可读性。否则内联。
- 重构目标是删除代码、降低分支、缩小公开面，而不是把逻辑搬到更多小函数里。

## Python 设计规则

- model state、dataset state、配置、生命周期和领域不变量必须使用完整面向对象设计。
- 优先使用显式类、dataclass、protocol、带类型的构造参数和有名字的方法，而不是动态属性访问。
- 默认禁止 `getattr`、`setattr`、`delattr`、monkey patch 或动态注入方法。
- 如果反射不可避免，必须先记录为什么显式方法、mapping、protocol 或 dispatch table 不适用；把反射隔离在极小 adapter 中，并直接测试它。
- 不要构造字符串驱动的训练流水线。使用带类型的配置对象和显式 factory。
- 不要为脚本新增 `argparse`、`click`、`typer`、`sys.argv` 或自定义命令行解析；任何可调整行为都通过 config 子系统配置项表达，且每项都有默认值。
- tensor 变换尽量小而纯，但不要把无关逻辑乱塞进 utility 文件；承载状态、生命周期或不变量的 tensor 相关逻辑必须进入明确类或类型组。
- Lightning orchestration 必须保持薄；领域逻辑放入经过测试的对象或纯函数。
- 避免过度 mock、全局可变状态、兜底式异常吞噬和隐藏文件系统副作用。

## 环境规则

- 使用项目根目录的 `uv` 环境，例如 `.venv`、`uv.lock` 和 `pyproject.toml` 所定义的环境。
- Python 解释器必须优先来自 `uv` 管理的安装；系统自带 `python` / `python3` 只能用于确认环境，不应代替项目 `uv` Python 运行测试、构建或工具命令。
- 如果必须新建环境，先核对 https://www.python.org/downloads/ 与 https://pytorch.org/get-started/locally/。
- 选择 PyTorch Stable 构建，并按官网矩阵选择 CPU 或 CUDA 轮子；CUDA 版本以 PyTorch 稳定版支持矩阵为准。
- 明确要求单元测试时，用 `uv run python -m unittest ...` 运行 Python 单元测试。

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
