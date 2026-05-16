---
name: cx-progress-ui
description: Use when implementing progress bars, multi-task status, training progress UI, ETA, cancellation, task phases, CLI progress, logging adapters, or GPUI progress components.
version: 1.0.0
---

# cx Multi-Task Progress UI

## Purpose

Create reusable progress state and rendering adapters for concurrent tasks such as multiple training jobs, evaluations, downloads, preprocessing runs, or desktop application workflows.

## Architecture

Separate three layers:

1. State model: pure data and reducer functions.
2. Event API: task started, advanced, phase changed, metric updated, cancelled, failed, completed.
3. Rendering adapters: CLI, logging, GPUI, and gpui-component.

## Minimal state fields

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

## Rules

- The state model must be testable without UI.
- Rendering adapters must not own business logic.
- Progress updates should be idempotent where practical.
- Concurrency must not corrupt task state.
- Cancellation and failure are first-class states.
- GPUI components should receive state snapshots and emit events; they should not compute training progress themselves.

## Tests

Cover independent updates for multiple tasks, completion of one task while another keeps running, cancellation, failure, deterministic ETA with a fake clock, and adapter snapshot correctness.
