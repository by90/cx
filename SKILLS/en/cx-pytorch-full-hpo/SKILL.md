---
name: cx-pytorch-full-hpo
description: Use for full-data HPO in PyTorch, Lightning, and time-series projects; run exactly one candidate on all samples, then immediately diagnose convergence, speed, recall, business risk, and data correctness before evidence determines the next single change. Candidate count is unbounded, and prequeued continuous execution is forbidden.
version: 0.1.0
---

# cx PyTorch Full HPO

## Language Rules

- Use the package language for conversations, plans, conclusions, evidence, and cx documents.
- Keep code identifiers, commands, paths, API names, libraries, protocols, standards, and proper names unchanged when needed, and explain their local meaning in adjacent prose.

## Purpose

Evaluate one current candidate at a time on all samples. Pause immediately after its training, testing, and backtesting, diagnose the result completely, and use only that evidence to propose the next experiment. Full HPO is an open evidence loop, not a fixed candidate count, fixed candidate identity set, or continuously executing queue.

Quick-HPO results may provide initial evidence, but they are not a fixed-count admission gate. The user may directly specify the baseline, fixed dimensions, adjustable dimensions, epoch cap, early-stopping patience, and business objective. Current user requirements override skill defaults.

## Iron Rules

1. Allow only one full-data candidate to be planned, trained, tested, or backtested at a time. Never prebuild several candidates for continuous background execution, and never start the next candidate automatically.
2. Do not cap candidate count. Every new candidate must follow the completed diagnosis of the preceding candidate. Do not continue merely to increase experiment count when no new evidence exists.
3. Before each run, record a falsifiable hypothesis, one primary change, any necessarily coupled changes, fixed configuration, comparison baseline, expected metric improvement, and stop condition. Narrow independent changes that would prevent attribution.
4. Use every sample in the task-defined full-data boundary. Never silently reduce entities, securities, dates, or sample ratio under resource pressure. Adjust only task-authorized resource parameters or wait for resources.
5. When the user does not specify the epoch cap, early-stopping patience, and random seed, default to `120` epochs, patience `20`, and seed `3407` from the config subsystem. Persist any user or project override in the candidate recipe.
6. User goals and the current hypothesis determine adjustable dimensions. Do not limit full HPO by default to batch size, learning rate, optimizer, and scheduler. When fields, labels, windows, loss, sampling, model structure, or capacity changes, place the candidate in a new comparable group and do not directly rank losses with different meanings.
7. Keep training and backtest scripts independently runnable. Build the current candidate through typed in-memory config objects without rewriting user-maintained default config files.
8. Persist the complete configuration, data boundary, fields, labels, window, split, loss, sampling, model, optimizer, scheduler, batch settings, seed, epoch cap, actual patience, and artifact paths for every candidate.
9. For warm-up, hold, cool-down, or cyclic learning rates, persist scheduler name, stage lengths, cycle count, maximum and minimum learning rates, transition function, and actual patience. Diagnosis must read the actual per-epoch learning rate rather than only the planned recipe.
10. Start resource-intensive or long-running training in an external terminal outside Codex App. Continuously write standard output, standard error, progress, per-epoch metrics, resources, and failures to files that the agent reads for analysis.
11. Before launch, record available system memory, available VRAM, expected peak use, the safety margin reserved for the operating system and Codex App, and the start-or-adjust decision. A complete run must not be the first resource probe.
12. Take a baseline sample immediately after launch, then at least every five minutes read candidate state, epoch, training and validation losses, best validation loss, improvement count, actual learning rate, elapsed time, throughput, GPU utilization, VRAM, system memory, and process memory. If no epoch or artifact changes, report the stalled position, process id, and log paths.
13. Immediately after training, use the same config and best checkpoint for task-required testing and backtesting. When failure prevents a stage, record why it is missing and never substitute empty metrics or results from another run.
14. Stop the pipeline in diagnosis state after the complete training-testing-backtesting chain ends, or after any stage fails. Complete and persist every required diagnosis before constructing another candidate.
15. Ordinary accuracy is invalid as the primary measure for extreme imbalance. Classification must at least report positive support, confusion matrix, positive recall, precision, F1, balanced accuracy, area under the precision-recall curve, and lift over the positive-rate baseline. Ranking tasks must also report daily top-K recall, precision, and coverage.
16. Fixed-threshold classification and continuous-score ranking are different problems. Diagnose threshold, probability calibration, positive and negative score distributions, and ranking quality separately. Do not let an almost-all-negative threshold hide useful ranking information, or let ranking lift hide failed classification.
17. When backtesting or strict test results select the next candidate, explicitly record that the strict test has entered tuning and no longer provides an untouched unbiased estimate. When rolling validation or a separate selection segment exists, select threshold, K, and candidates only there.
18. Do not publish, tag, or change the default inference model without explicit user authorization. A best candidate is an evidence-backed recommendation; release still follows `$cx-version` and its user confirmation gate.

## Mandatory Post-Run Diagnosis

### 1. Why the Run Did Not Reach Its Epoch Cap

1. Distinguish normal completion, early stopping, out-of-memory failure, non-finite loss, data failure, process failure, manual stop, and external resource change.
2. Inspect monitored metric, minimum improvement, actual patience, last improvement epoch, best epoch, current learning-rate stage, epoch cap, completed epochs, and callback record.
3. Verify that last checkpoint, best checkpoint, resume state, and history are complete and share one provenance. Do not call an abnormal stop early stopping or call every early stop a failed model.

### 2. Why Loss Fell Slowly or Plateaued

1. Inspect per-epoch training loss, validation loss, their gap, smoothed trend, variance, improvement spacing, best epoch, and tail behavior together.
2. Inspect actual learning-rate history, optimizer state, weight decay, gradient norms, gradient clipping, physical batch, effective batch, gradient accumulation, and optimizer steps per epoch.
3. Distinguish excessive or insufficient learning rate, mismatched schedule stage, underfitting, overfitting, inadequate capacity, excessive regularization, label noise, conflicting objectives, and distribution drift.
4. Persist every component and weight of composite loss; check whether total-loss progress hides a stalled positive-class or ranking objective.

### 3. Why Training Was Slow

1. Separate data preparation, training batches, validation batches, checkpoint saving, testing, and backtesting time, including first-epoch versus steady-state behavior.
2. Record samples, physical batches, optimizer steps, mean batch time, samples per second, data wait, and model compute time.
3. Analyze CPU and GPU utilization, allocated/reserved/peak VRAM, system and process memory, disk input/output, data-loader workers, and device transfers together.
4. Explain throughput changes through window length, field count, input width, model capacity, batch settings, and precision. No single utilization number proves the bottleneck.

### 4. Why Recall or Ranking Coverage Was Low

1. Verify label definition, positive threshold, positive support in train/validation/test, the daily positive-count distribution, zero-positive days, time split, and sample membership.
2. Report confusion matrix, positive recall, precision, specificity, F1, balanced accuracy, area under the precision-recall curve, area under the receiver operating characteristic curve, positive baseline, and lift.
3. For daily top-K, report hits, total true positives, recall, precision, and the share of dates with at least one hit, both as daily distributions and full-period aggregates.
4. Compare score distributions, quantiles, and boundary cases for positives, false negatives, true negatives, and false positives to distinguish representation, loss, class weighting, sampling, capacity, threshold, calibration, and ranking overlap.
5. Check whether abundant flat or easy-negative samples dominate gradients. Class weighting, focal loss, stratified sampling, hard-example mining, or ranking loss are hypotheses only; change them one at a time and measure recall against false-positive cost.

### 5. Whether Business Risk Was Acceptable

1. For daily top-K, report return mean, median, quantiles, worst value, large-drop count and share, mean loss among downside samples, and mean loss in the worst tail.
2. Compare return distributions for hits, misses, false positives, and false negatives, and check whether higher recall was bought with more large drops.
3. Record transaction cost, suspension, price-limit, tradability, and repeated-security boundaries; mark unavailable facts as unverified.

### 6. Whether Data, Implementation, and Comparison Were Trustworthy

1. Verify field semantics, units, enable order, missing and abnormal distributions, normalization fit boundary, label source, window closure, time leakage, and cross-sectional ranking scope.
2. Verify seed, data version, training membership, resume identity, loss implementation, metric implementation, checkpoint selection, and prediction-label alignment.
3. Compare numeric metrics only inside groups with the same label, loss, split, evaluation frequency, and epoch cap. Report other candidates separately.
4. Inspect train-validation gap, temporal drift, daily metric variance, and domination by a few dates so that accidental one-day gains do not appear stable.

## Deciding the Next Candidate

After diagnosis, write:

1. One most likely and falsifiable primary cause.
2. Supporting evidence, contrary evidence, and missing evidence.
3. The next single primary change and necessary coupled changes.
4. Data, fields, labels, windows, model, and training parameters that remain fixed.
5. The primary expected metric, risk guardrail, and stop condition.
6. A decision to continue, gather more evidence, return to a smaller experiment, or stop full HPO.

When the primary cause remains ambiguous, run the smallest diagnostic or ablation before another complete candidate. A user-authorized continuing search may repeat this loop any number of times, but each repetition must be triggered separately by the preceding evidence.

## Required Workflow

1. Read the user objective, current config, existing training and backtest evidence, and dimensions the user fixed or authorized for change.
2. Use `$cx-common-module` to find existing config construction, training, testing, backtesting, metrics, and resource-monitoring entrypoints.
3. Use `$cx-tdd` and `$cx-pytorch-tdd` only when the user, task, or change explicitly requires unit tests or test-driven development. Otherwise create, modify, and run no unit tests.
4. Register the hypothesis, comparison boundary, complete recipe, resource budget, log paths, and stop condition for one current candidate.
5. Start only that candidate in an external terminal and read file logs at the five-minute cadence.
6. Immediately run same-provenance testing and backtesting after training, then stop in diagnosis state.
7. Complete the six mandatory diagnosis sections and next-candidate decision, preserving raw metrics, conclusions, and evidence paths.
8. Return to step 4 for one new candidate only when the decision is to continue and evidence supports a specific change. Never prequeue candidates.
9. End the loop when the user objective is reached, the user says stop, evidence makes further cost unreasonable, or an external condition blocks progress. Report completion state honestly.

## Verification Evidence

- Candidate hypothesis, one primary change, fixed configuration, complete recipe, full-sample boundary, data version, and seed.
- Prelaunch resource estimate, external process identity, standard-output and standard-error paths, per-epoch history, and five-minute resource summaries.
- Completed versus planned epochs, stop reason, final and best epochs, training and validation losses, actual learning rate, improvement count, gradients, and batch/step facts.
- Data preparation, training, validation, testing, backtesting, and saving times, plus throughput, GPU, VRAM, system memory, process memory, and input/output evidence.
- Class support, daily positive distribution, confusion matrix, positive recall, precision, F1, balanced accuracy, area under the precision-recall curve, baseline lift, and daily top-K recall, precision, and coverage.
- Top-K return distribution, large-drop count and share, worst return, mean downside loss, and worst-tail mean loss.
- Field, label, window, normalization, split, leakage, resume, checkpoint, and metric-alignment checks.
- Whether strict test entered selection, whether comparisons share one group, and the valid scope of conclusions.
- Mandatory diagnosis and next-candidate decision; when continuing, preserve how current evidence triggered the next candidate.
- Evidence that no candidate started before diagnosis finished and that no fixed-count continuous background queue exists.
