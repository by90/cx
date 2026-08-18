---
name: cx-pytorch-hpo
description: Use for automatic HPO in PyTorch, Lightning, and stock time-series projects; reuse the project's shared tuner, optimize the validation business metric on every eligible registration-regime entity, jointly search data, model, optimization, schedule, and loss parameters with a mature sampler/pruner, and admit trials safely through CPU, physical-memory, commit-memory, and per-GPU VRAM capacity gates.
metadata:
  version: 0.4.0
---

# cx Automatic PyTorch HPO

## Purpose

Delegate candidate direction, parameter interaction, and training-resource allocation to a recoverable, auditable HPO tool instead of letting the agent repeatedly tune in a wrong manual direction. Do not split tuning into lightweight and full-data stages, sample one tenth of entities, or use strict test for parameter selection.

## Invariants

1. Read the project `AGENTS.md`, effective config, shared training/HPO entrypoints, callers, tests, frozen baseline, and real artifacts first. Evolve an existing model-independent tuner instead of copying its lifecycle into model directories.
2. Stock HPO uses every eligible entity and daily row from the applicable registration-regime start; the ChiNext default is `2020-08-24`. Resource pressure must not reduce entity coverage.
3. Labels, levels, ranking scores, TopN/Top10, and splits come from the authoritative project entrypoint. Freeze validation/test target-date boundaries when window length changes. A label or business-contract change requires a separate study and cannot be directly ranked.
4. The validation business metric is the sampler, pruner, and incumbent objective. Validation loss supports gradients, diagnosis, and required checkpoints only; lower loss alone cannot promote a trial.
5. Strict test never enters the study, intermediate values, pruning, parameter importance, or next configuration. Audit only the validation-selected incumbent. If test participates in selection, declare contamination and stop.
6. Explicitly use a mature HPO tool. Prefer Optuna for a local PyTorch/Lightning workload by default. Before selecting Ray Tune, Syne Tune, SMAC, or another tool, use official documentation to compare OS support, process/memory overhead, recoverable storage, conditional spaces, parallel sampling, and multi-fidelity pruning, then record the choice.
7. Automated HPO does not fix every trial's epoch count or patience. Disable framework-native manual early stopping and let the pruner stop trials from per-epoch validation business metrics. A global resource-axis ceiling may enforce hardware, wall-clock, and safety bounds, but trials need not exhaust it.
8. The search space cannot collapse to latent width. Cover task-relevant data/windows, field representation, temporal model, longitudinal/cross-sectional summaries, optimizer, learning rate, weight decay, batch, scheduler and warmup/period/min-lr/restart parameters, dropout, and loss. User-frozen values stay outside the search.
9. Use define-by-run conditional spaces: sample only parameters relevant to the selected optimizer, scheduler, architecture, or loss. Architecture combinations must satisfy divisibility, shape, and memory constraints. Do not resample class weighting after project evidence has rejected it.
10. Default to serial high-resource work and never run more than two such jobs concurrently. Run at most one independent trial worker per GPU. Dual-GPU concurrency must pass host and per-GPU capacity admission and consumes both concurrency slots.
11. Record train/validation loss, cumulative business best, learning rate, time, steps, CPU, physical memory, commit memory, and per-GPU VRAM every epoch. Freeze the effective config, epoch trail, business-best, validation-loss-best, and prune/completion-final state per trial. OOM, exhausted commit memory, and exceptions are explicit trial states with reasons.
12. A one-percentage-point or similar meaningful-delta rule applies only between two completed, contract-comparable trials. Within one run, report only business best with epoch and validation-loss best with epoch.

## Shared Module Contract

The shared tuner alone:

- Creates or restores a persistent study and freezes tool version, sampler, pruner, seed, objective direction, resource policy, and data digest.
- Converts suggestions into typed in-memory configs without editing product defaults or exposing experiment parameters through CLI flags.
- Reports cumulative per-epoch validation business best to the pruner while disabling framework-native manual early stopping.
- Owns each trial's artifact directory, GPU identity, state, checkpoints, resource facts, and recovery.
- Continuously writes `analysis.json` and `analysis.md` with completed/pruned/failed/running trials, incumbent, parameters, actual epochs, resources, failures, and parameter importance.
- Prevents the agent from overriding the next configuration, epoch count, or stop decision while sampler/pruner execution is active.

Thin model adapters declare only networks, losses, and search space. Physically remove old QuickTune, manual one-candidate approval, immutable `1000/20`, and dual protocols. Historical manual runs remain results facts only.

## Resource Capacity Admission

1. Treat trial workers, full test suites, backtests, analyzers, and diagnostics that load substantial data as high-resource work. Run them serially by default and never run more than two concurrently.
2. Before starting a formal study, before a worker claims each new trial, and before starting any high-resource auxiliary process, read total CPU load and heavy processes, total and available physical memory, system committed bytes and commit limit, total and free VRAM plus processes per GPU, and the current high-resource-job count. On Windows, read `\Memory\Available MBytes`, `\Memory\Committed Bytes`, and `\Memory\Commit Limit` separately; available physical memory cannot substitute for commit headroom.
3. Derive the proposed job's incremental peak from the latest comparable measurement or a real-tensor smoke run, then freeze it and an explicit reserve in `resource_policy`. Admit the job only when concurrency, CPU, physical memory, commit memory, and target-GPU VRAM all retain their budgeted headroom. Do not claim safety from an arbitrary fixed threshold that lacks measurement.
4. Start one trial worker by default. Allow one worker on each of two GPUs only after both GPUs and host capacity pass fresh admission. Those workers consume both concurrency slots, so do not concurrently start a full test, backtest, analyzer, or other high-resource job.
5. During execution, write resource snapshots and actual peaks to a file-backed trail at a fixed sampling interval. Re-run admission before adding any process. If load is still rising or commit/VRAM headroom is insufficient, dispatch no new work; wait for release or return to serial execution.
6. On a resource failure, record the trial state, original error, and failure-time snapshot, release resources from ended processes, and diagnose the root cause before resuming the same study. Never retry blindly, swallow the exception, or reduce registration-regime stock or daily-row coverage to evade capacity limits.

## Workflow

1. Freeze data scope, validation/test date boundaries, label, business objective, hardware/wall-clock limits, excluded parameters, and a `resource_policy` containing incremental peaks and reserves.
2. Research current tools online. A local dual-GPU PyTorch workload normally uses Optuna multivariate TPE for conditional/joint sampling and Hyperband or Successive Halving for multi-fidelity stopping; document why a heavier orchestration layer is unnecessary.
3. Use TDD to connect a per-epoch trainer observer, pruning exceptions, three checkpoints, persistent shared storage, recovery, and analysis. Validate multiprocess locking with an infrastructure-only smoke test, not a reduced-stock formal trial.
4. Define the full space. Use suitable linear/log distributions for continuous values and categoricals for windows/architectures. Do not binary-search a business dimension without evidence of monotonicity.
5. Fix seed and study name, start one worker, and permit one worker per GPU only after capacity admission passes again. Let the sampler suggest configurations and the pruner determine actual epochs; do not manually redirect a running study.
6. Monitor objective, CPU, physical memory, commit memory, per-GPU VRAM, OOM, zombie trials, storage, and artifacts without touching strict test. Diagnose the failure and pass capacity admission again before resuming the same study; never delete unfavorable trials.
7. Freeze the incumbent only after the study reaches its wall-clock or convergence stop. Reproduce with independent seeds where needed, then run strict test/backtest once with the project-authorized validation-loss checkpoint.

## Extreme-Imbalance Objective

- For nine levels, retain per-class support, confusion, highest-two precision/recall, coverage, selected returns, tail risk, and daily stability. Overall accuracy cannot replace the business objective.
- Multiclass, ordinal, pairwise/listwise ranking, and differentiable Top-K can be conditional loss choices. Different labels or business definitions require separate studies. Loss values are not directly comparable across definitions, though the unchanged business metric is.
- Reporting cumulative business best reduces misleading multi-fidelity decisions from one noisy epoch; retain every raw epoch value too.

## Progress Analyzer

Run:

    python scripts/analyze_hpo_progress.py path/to/ledger.json path/to/analysis

The ledger contains `data_scope`, `optimizer`, `objective`, `resource_policy`, `trials`, and `strict_test_used_for_selection`. `optimizer` records tool, sampler, pruner, and persistent storage. Each trial records `number/state/value/params/intermediate_values/completed_epochs` plus validation, resource, failure, and artifact facts.

The analyzer validates and summarizes the study; it never replaces the sampler's next suggestion. Output includes state counts, incumbent, actual epochs, failure reasons, available parameter importance, and proof that strict test did not select trials.

## Completion Evidence

- Official evidence for tool choice, shared-module/caller audit, and physical removal of the old protocol.
- Registration start, all eligible entity count, date boundaries, data version, and content digest.
- Sampler/pruner/storage/resource policy, complete conditional search space, and user-frozen values; the resource policy includes the latest comparable peaks, reserves, serial default, and two-job concurrency ceiling.
- Admission evidence for one worker and fresh dual-GPU admission, concurrent-storage smoke, per-epoch resource trails, trial states, effective configs, checkpoints, and continuous analysis.
- Validation result and independent reproduction for the incumbent; final strict test with proof that it never entered search.
