---
name: cx-pytorch-hpo
description: Use for automatic HPO in PyTorch, Lightning, and stock time-series projects; reuse the project's shared tuner, optimize the validation business metric on every eligible registration-regime entity, jointly search data, model, optimization, schedule, and loss parameters with a mature sampler/pruner, and admit trials safely through CPU, physical-memory, commit-memory, and per-GPU VRAM capacity gates.
metadata:
  version: 0.4.5
---

# cx Automatic PyTorch HPO

## Purpose

Delegate candidate direction, parameter interaction, and training-resource allocation to a recoverable, auditable HPO tool instead of letting the agent repeatedly tune in a wrong manual direction. Do not split tuning into lightweight and full-data stages, sample one tenth of entities, or use strict test for parameter selection.

## Invariants

1. Read the project `AGENTS.md`, effective config, shared training/HPO entrypoints, callers, tests, frozen baseline, and real artifacts first. When a model-independent tuner already exists, change only the tuning script and reuse the current model and training entrypoints. A trial must not rewrite product defaults, shared model code, or shared training code, and the lifecycle must not be copied into model directories.
2. Stock HPO uses every eligible entity and daily row from the applicable registration-regime start; the ChiNext default is `2020-08-24`. Resource pressure must not reduce entity coverage.
3. Labels, levels, ranking scores, dynamic TopN, fixed Top1/Top3/Top10, and splits come from the authoritative project entrypoint. Freeze validation/test target-date boundaries when window length changes. A label or business-contract change requires a separate study and cannot be directly ranked.
4. The validation business metric is the sampler, pruner, and incumbent objective. Validation loss supports gradients, diagnosis, and required checkpoints only; lower loss alone cannot promote a trial.
5. Strict test never enters the study, intermediate values, pruning, parameter importance, or next configuration. Audit only the validation-selected incumbent. If test participates in selection, declare contamination and stop.
6. Explicitly use a mature HPO tool. Prefer Optuna for a local PyTorch/Lightning workload by default. Before selecting Ray Tune, Syne Tune, SMAC, or another tool, use official documentation to compare OS support, process/memory overhead, recoverable storage, conditional spaces, parallel sampling, and multi-fidelity pruning, then record the choice.
7. Both ordinary candidates and formal automated HPO trials train for at most `120` epochs and apply `9`-epoch patience to the project's explicit validation selection objective. The minimum improvement must be zero, so any strict improvement immediately resets patience. Only after the current trial reaches twenty-one strict validation-loss improvements may a pruner terminate it as relatively weak from per-epoch validation business metrics; pruning cannot cancel, replace, or extend the `120/9` rule. The study should seek a run-through trial that naturally completes 120 epochs while this rule remains active, but epoch count must not become an incumbent gate.
8. The search space cannot collapse to latent width. Cover task-relevant data/windows, field representation, temporal model, longitudinal/cross-sectional summaries, optimizer, learning rate, weight decay, batch, scheduler and warmup/period/min-lr/restart parameters, dropout, and loss. User-frozen values stay outside the search.
9. Use define-by-run conditional spaces: sample only parameters relevant to the selected optimizer, scheduler, architecture, or loss. Architecture combinations must satisfy divisibility, shape, and memory constraints. Do not resample class weighting after project evidence has rejected it.
10. Default to serial high-resource work and never run more than two such jobs concurrently. Run at most one independent trial worker per GPU. Dual-GPU concurrency must pass host and per-GPU capacity admission and consumes both concurrency slots.
11. Record and report epoch position, train/validation loss, cumulative strict validation-loss improvement count, early-stopping counter, cumulative business best, learning rate, time, steps, CPU, physical memory, commit memory, and per-GPU VRAM every epoch. After the sampler proposes concrete parameters and the in-memory overrides are materialized, freeze that trial's effective config, epoch trail, business-best, validation-loss-best, and prune/completion-final state. Every ended trial must produce theoretical-loss completion, business-ranking, and manual fit diagnostics. OOM, exhausted commit memory, and exceptions are explicit trial states with reasons.
12. A one-percentage-point or similar meaningful-delta rule applies only between two completed, contract-comparable trials. Within one run, report only business best with epoch and validation-loss best with epoch.
13. When the project has formal models, read project-authorized Git tags and frozen artifacts directly before starting the study, then freeze the strongest formal-model baseline with the same data scope, label, split, and aggregation contract. Unless the user explicitly requests it, do not check out a tag, restore the working tree, create a worktree, or retrain a historical release merely to compare baselines. A simple statistical baseline cannot replace the formal-model baseline.
14. Before training a new model, loss, feature, capacity, optimization, or scheduling direction, use `$cx-research` to research one explicit question online, synthesize formal-release facts with primary sources, peer-reviewed papers, and reliable reproductions into the current conclusion, and freeze a falsifiable hypothesis, one changed variable, and contract-comparable acceptance criteria. Do not substitute a sequence of manual candidates for unfinished research.
15. A trial gains model-evidence eligibility only after at least twenty-one cumulative strict validation-loss improvements. Mark a run below twenty-one as invalid evidence: it cannot support accepting or rejecting a model, loss, feature, capacity, optimizer, or schedule; become a baseline or incumbent; promote or scale a candidate; contribute parameter importance; or determine the next configuration. The sampler and pruner must not use it as directional evidence either.

## Unified Trial Stopping Rule

An ordinary single-candidate baseline, reproduction, falsifiable experiment, or formal automated HPO trial trains for at most `120` epochs and applies early stopping to the project's explicit validation selection objective. Stop when that objective has not improved for `9` complete epochs; do not require the run to complete `100` epochs first. After stopping, still freeze the business-best, validation-loss-best, and final states under the target project's rules. Run strict test with the project-authorized checkpoint only for the final frozen recipe.

Early-stopping comparison uses strict-improvement semantics with a minimum improvement of zero. Whenever the current validation selection objective is better than its previous best, however small the gain, reset patience immediately. Stop only after nine complete epochs with no improvement at all.

Formal automated HPO retains per-epoch validation business metrics but must not submit a model-effectiveness pruning decision before the current trial reaches twenty-one strict validation-loss improvements. After crossing the evidence gate, the pruner may terminate a relatively weak trial before its nine-epoch patience expires. A trial that is not pruned still obeys the `120/9` rule. Pruning supplements training early stopping; it cannot extend a stagnant trial beyond epoch 120 or bypass the rule that any improvement resets patience.

The `120/9` contract governs training lifecycle, not model-evidence eligibility. When early stopping, pruning, an exception, or resource termination leaves fewer than twenty-one cumulative strict validation-loss improvements, retain only the configuration, trail, and stop facts and mark the run as invalid evidence. Do not infer overfitting, underfitting, objective validity, or objective invalidity from it. Model-effectiveness pruning may begin only after the current trial has reached twenty-one strict improvements. A resource failure may terminate at any time but cannot influence the sampler, parameter importance, incumbent, or next direction. Never delay early stopping, increase patience, or manufacture tiny improvements merely to reach twenty-one.

## Unified Training and Business Report

### Per-Epoch Training Report

After every complete training epoch, report `current epoch/maximum epochs`, cumulative strict validation-loss improvement count, `current early-stopping counter/patience`, mean training loss for the epoch, and validation loss, for example `7/120` and `3/9`. Count validation-loss improvements independently. The early-stopping counter always follows the study-frozen validation selection objective, so the two counters must not be conflated. When validation loss is not the selection objective, its improvement count does not replace the business objective but still determines whether the run can become model evidence; below twenty-one, the sampler, pruner, and incumbent cannot use the result.

### Theoretical-Loss Completion

Before a study starts, the project's authoritative loss entrypoint freezes the no-information theoretical reference loss, theoretical floor, formula, label distribution, weights, masks, and reduction semantics. The no-information reference cannot read input features. Classification usually uses a constant prediction from the frozen label prior, regression usually uses the frozen training-target center, and a specialized loss must provide a project-defined, provably equivalent reference. The agent must not substitute an empirical guess, a single trial, or strict-test output for the theoretical reference. A change to loss, label representation, weighting, or reduction creates a new comparable group and reference.

For every ended trial with a complete loss trail, report the validation-loss-best epoch, training loss at that epoch, minimum validation loss, no-information theoretical reference loss, theoretical floor, absolute improvement `reference loss - minimum validation loss`, relative improvement percentage `(reference loss - minimum validation loss) / abs(reference loss) × 100%`, and reducible-loss completion rate `(reference loss - minimum validation loss) / (reference loss - theoretical floor) × 100%`. Report the affected percentage as unavailable rather than inventing a value when the reference is zero or the floor is invalid. Reducible-loss completion states how much theoretically reducible loss the model removed; it is not a business hit rate or a forecast of future return.

### Stock-Ranking Business Report

For a stock-ranking task, report dynamic TopN and fixed Top1, Top3, and Top10 hit rates after every epoch and at trial completion. Dynamic N is the true opportunity count for each trading day under each label scale. It is therefore the unified business comparison across grading scales only when population, target dates, opportunity semantics, and aggregation are aligned. The report must name the scale, opportunity definition, source of daily N, and cross-day aggregation. A label or opportunity-semantic change still requires a separate study; TopN cannot bypass comparability. Whether a business metric participates in selection is fixed by the study objective, not by its inclusion in the report.

### Manual Fit and Plateau Diagnosis

After every trial, the agent must first check the cumulative strict validation-loss improvement count. Below twenty-one, report only `invalid training evidence` and the raw trail; do not classify overfitting, underfitting, healthy fit, or objective direction. At twenty-one or more, inspect the complete training- and validation-loss trails and classify the evidence as `overfitting`, `underfitting`, `healthy fit`, or `insufficient evidence`, with concrete epoch evidence. Training loss continuing to fall while validation loss is flat or rising and the gap widens is evidence of overfitting. Both losses remaining near the no-information reference, staying close together, and still falling at termination is evidence of underfitting or unfinished optimization. Both improving without sustained validation divergence is evidence of healthy fit. One sign alone does not prove a root cause, so the conclusion must match the strength of the evidence.

The study freezes loss-reporting precision and a plateau observation window in advance. `plateau_start_epoch` is the first epoch of the terminal contiguous interval in which the running-best validation loss fails to improve beyond the frozen precision for one full observation window. Report the interval, window, precision, and corresponding training-loss direction. Treat changes below frozen precision as indistinguishable, not as improvement or degradation. When training and validation loss definitions, weights, or reductions are not comparable, report `comparable=false` and the reason, do not subtract them, and still report both raw trails.

Machine-readable analysis retains the per-epoch fields above, theoretical reference, theoretical floor, absolute improvement, relative improvement percentage, reducible-loss completion rate, business rankings, `evidence_eligible`, the eligibility reason, manual fit assessment, `plateau_start_epoch`, evidence epochs, comparability, and `used_for_selection`. A trial below twenty-one strict improvements or without a complete loss trail reports only the original facts, never fabricates a completion report, and cannot set `used_for_selection=true`.

## Configuration Lifecycle and Dual Objectives

1. A study freezes data boundaries, labels, the validation business objective, the `120/9` stopping contract, resource policy, search space, and excluded parameters. It does not prematurely freeze every parameter under search to one shared value set.
2. For each trial, the tuning script copies a typed config, overrides only the dimensions currently suggested by the sampler in memory, and passes the resulting config object explicitly to the existing model-construction and training entrypoints. Do not express a trial by rewriting product config files, module-level default objects, model source, or training source.
3. Freeze the trial's effective config snapshot immediately after applying its in-memory overrides. That snapshot reproduces only that trial and does not prevent the sampler from materializing a different config for the next trial.
4. Determine the incumbent by the unchanged validation business metric only among trials that have reached twenty-one strict validation-loss improvements. Epoch count alone neither grants nor removes eligibility. A trial stopping after twenty or thirty epochs may become incumbent only if it crossed the evidence gate; otherwise no local business peak permits selection.
5. Naturally completing 120 epochs is a separate training-lifecycle run-through objective. Keep nine-epoch early stopping, zero minimum improvement, and pruning genuinely active. Never fake run-through by delaying early stopping, increasing patience, imposing a minimum-epoch gate, or disabling pruning.

## Shared Module Contract

The shared tuner alone:

- Creates or restores a persistent study and separately freezes the study protocol, conditional search space, tool version, sampler, pruner, seed, objective direction, resource policy, and data digest.
- Copies a typed config for each trial, applies HPO suggestions only as in-memory overrides to that copy, and explicitly passes the effective config to the existing model and training entrypoints. It does not edit product defaults, shared model code, shared training code, or expose experiment parameters through CLI flags.
- Freezes the effective config snapshot at the trial-start boundary so each trial is reproducible without locking the next sample.
- Reports cumulative per-epoch validation business best to the pruner while every HPO trial keeps `120/9` training early stopping with zero minimum improvement.
- Owns each trial's artifact directory, GPU identity, state, checkpoints, resource facts, and recovery.
- Continuously writes `analysis.json` and `analysis.md` with completed/pruned/failed/running trials, the validation-business incumbent, parameters, actual epochs, resources, failures, parameter importance, and each ended trial's theoretical-loss completion, business rankings, manual fit assessment, and plateau start. Actual epochs in the full trail also expose whether any trial naturally completed 120 epochs.
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

1. Separately freeze data scope, validation/test date boundaries, label, business objective, the `120/9` contract, loss-reporting precision, plateau observation window, no-information theoretical reference loss, theoretical floor, conditional search space, hardware/wall-clock limits, excluded parameters, and a `resource_policy` containing incremental peaks and reserves. Do not misrepresent searched dimensions as one fixed config shared by every trial.
2. Research current tools online. A local dual-GPU PyTorch workload normally uses Optuna multivariate TPE for conditional/joint sampling and Hyperband or Successive Halving for multi-fidelity stopping; document why a heavier orchestration layer is unnecessary.
3. Use TDD to connect a per-epoch trainer observer, pruning exceptions, three checkpoints, persistent shared storage, recovery, and analysis. Validate multiprocess locking with an infrastructure-only smoke test, not a reduced-stock formal trial.
4. Define the full space. Use suitable linear/log distributions for continuous values and categoricals for windows/architectures. Do not binary-search a business dimension without evidence of monotonicity.
5. Fix seed and study name, start one worker, and permit one worker per GPU only after capacity admission passes again. Let the sampler suggest configurations and let the tuning script materialize and freeze the current trial's effective in-memory config. Only after the current trial reaches twenty-one strict validation-loss improvements may the pruner use validation business metrics to terminate a relatively weak trial; let `120/9` determine actual epochs for the remaining trials, and do not manually redirect a running study.
6. Monitor objective, CPU, physical memory, commit memory, per-GPU VRAM, OOM, zombie trials, storage, and artifacts without touching strict test. Diagnose the failure and pass capacity admission again before resuming the same study; never delete unfavorable trials.
7. Continuously report the validation-business incumbent selected from evidence-eligible trials, the count and reasons for invalid-evidence trials, whether a trial has naturally completed 120 epochs, and the unified training and business report; none replaces another. Freeze the incumbent only after the study reaches its wall-clock or convergence stop and contains at least one evidence-eligible trial. Reproduce with independent seeds where needed, then run strict test/backtest once with the project-authorized validation-loss checkpoint.

## Extreme-Imbalance Objective

- For nine levels, retain per-class support, confusion, highest-two precision/recall, coverage, selected returns, tail risk, and daily stability. Overall accuracy cannot replace the business objective.
- Multiclass, ordinal, pairwise/listwise ranking, and differentiable Top-K can be conditional loss choices. Different labels or business definitions require separate studies. Loss values are not directly comparable across definitions, though the unchanged business metric is.
- Reporting cumulative business best reduces misleading multi-fidelity decisions from one noisy epoch; retain every raw epoch value too.

## Progress Analyzer

Run:

    python scripts/analyze_hpo_progress.py path/to/ledger.json path/to/analysis

The ledger contains `data_scope`, `formal_baseline`, `research_note`, `optimizer`, `objective`, `loss_reference`, `loss_floor`, `loss_report_precision`, `plateau_window`, `resource_policy`, `trials`, and `strict_test_used_for_selection`. `optimizer` records tool, sampler, pruner, and persistent storage. Each trial records `number/state/value/params/actual_config/intermediate_values/completed_epochs`, `epoch_reports`, `business_context`, `evidence_eligible`, `eligibility_reason`, `losses_comparable`, `fit_assessment`, and `fit_evidence_epochs`. Every `epoch_reports` row contains epoch, train/validation loss, validation-loss improvement count, early-stopping counter, dynamic TopN, and fixed Top1/Top3/Top10. `business_context` records scale, opportunity definition, daily-N source, and cross-day aggregation.

`formal_baseline` records `tag` and `artifact_reference`, while `research_note` stores the current pre-training research-note path. `optimizer` must also set `sampler_uses_only_evidence_eligible_trials` and `pruner_uses_only_evidence_eligible_trials` to true, `resource_policy.minimum_evidence_validation_loss_improvements` must equal `21`, and the top-level `parameter_importance_uses_only_evidence_eligible_trials` must be true. The analyzer computes `evidence_eligible` and `eligibility_reason` from the epoch trail; callers cannot declare an invalid run eligible themselves.

The analyzer validates and summarizes the study; it never replaces the sampler's next suggestion. Output includes state counts, evidence-eligibility counts and reasons, the validation-business incumbent selected from evidence-eligible trials, actual epochs, failure reasons, parameter importance based only on eligible evidence, and each ended trial's theoretical-loss completion, business rankings, permitted manual fit assessment, and plateau start. It separately states whether those report fields participated in selection and proves that invalid evidence and strict test did not select trials. It must not change the existing incumbent rule.

## Completion Evidence

- Official evidence for tool choice, shared-module/caller audit, and physical removal of the old protocol.
- Directly read formal-release tags, frozen configurations and reports, the strongest contract-comparable formal baseline, and the pre-training online research note, falsifiable hypothesis, one changed variable, and acceptance criteria.
- Registration start, all eligible entity count, date boundaries, data version, and content digest.
- Sampler/pruner/storage/resource policy, complete conditional search space, and user-frozen values; evidence that trials did not rewrite product defaults or shared model/training code; the resource policy includes the latest comparable peaks, reserves, serial default, and two-job concurrency ceiling.
- Admission evidence for one worker and fresh dual-GPU admission, concurrent-storage smoke, per-epoch resource trails, every trial's effective config snapshot after in-memory overrides, checkpoints, stop reasons, nine-epoch patience counters, and continuous analysis.
- Every trial's cumulative strict validation-loss improvement count, evidence eligibility, and invalidity reason; the incumbent's validation-business result and proof of at least twenty-one strict improvements; whether any trial naturally completed 120 epochs with nine-epoch early stopping still active; every ended trial's per-epoch training report, theoretical-loss completion, business rankings, permitted manual fit and plateau diagnosis, and any needed independent reproduction; proof that invalid evidence never entered the sampler, pruner, parameter importance, incumbent, or next direction, and that final strict test never entered search.
