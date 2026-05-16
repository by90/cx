---
name: cx-progress-ui
description: 用于 progress bars、multi-task status、training progress UI、ETA、cancellation、task phases、CLI progress、logging adapters 和 GPUI progress components。
version: 1.0.0
---

# cx 多任务进度 UI

## 目的

为多个并发任务创建可复用的进度状态和渲染适配器，例如多个训练任务、评估、下载、预处理流程或桌面应用工作流。

## 架构

分离三层：

1. State model：纯数据和 reducer 函数。
2. Event API：task started、advanced、phase changed、metric updated、cancelled、failed、completed。
3. Rendering adapters：CLI、logging、GPUI、gpui-component。

## 最小状态字段

```text
task_id
title
phase
current
total
percent
eta_seconds
latest_metrics
status: pending | running | paused | cancelled | failed | completed
message
updated_at
```

## 规则

- state model 必须能脱离 UI 测试。
- rendering adapter 不持有业务逻辑。
- 进度更新在可行时保持幂等。
- 并发更新不能破坏任务状态。
- cancellation 和 failure 是一等状态，不只是 message。
- GPUI 组件接收状态快照并发出事件，不直接计算训练进度。

## 测试

覆盖多任务独立更新、一个任务完成而另一个继续运行、取消、失败、使用 fake clock 的确定性 ETA，以及 adapter 接收到的状态快照是否正确。
