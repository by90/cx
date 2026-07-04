---
name: cx-pytorch-quick-hpo
description: Use for quick tuning in PyTorch, Lightning, and time-series projects; use about one tenth complete-entity data to study field contribution, feature sets, window length, labels, training hyperparameters, optimizer/scheduler choices, and model capacity before full-data tuning.
version: 0.1.0
---

# cx PyTorch Quick HPO

## Language Rules

- Use the package language for conversations, explanations, plans, summaries, review decisions, verification evidence, and cx documents. Do not mix languages inside prose fragments or term lists.
- In Chinese-package work, if an English identifier, command, path, API name, library, protocol, standard, proper name, or ambiguity-sensitive term must remain in English, explain its meaning, role, and local context in Chinese in the same sentence or an adjacent sentence. In English-package work, explain unavoidable non-English terms in English.

## Purpose

Find candidate configurations worth sending to full-data tuning with a smaller but complete sample. Quick tuning prioritizes data field combinations, window length, and label definitions before training hyperparameters, optimizer, scheduler, and model structure.

## Iron Rules

1. The training, inference, and backtest entrypoints must run by themselves with default configuration; menus and tuning orchestrators may only call those scripts or stable entrypoints.
2. A tuning run must initialize from the target model's default config, then let the shared tuning facility clone and mutate typed config objects in memory before passing them to training, inference, or backtest entrypoints. Every trial behavior change must affect only the in-memory config object, including fields, labels, window length, batch size, learning rate, optimizer, scheduler, model structure, output directory, and saved snapshots. Do not create temporary YAML files or temporary config directories as a trial fact source, do not rewrite current config files for trial behavior, and do not implement separate config-rewrite flows inside individual model directories.
3. When saving checkpoints or weights, persist the complete config snapshot associated with the in-memory recipe alongside that artifact. The tuning script may persist trial configs, best recipes, metrics, and backtest configs into the output directory, but must never rewrite the current project config, default config, or user-maintained config files.
4. Quick tuning uses about one tenth of the data, but the sampling unit must be a complete entity. For daily data from 2,000 stocks, randomly select about 200 stocks and keep each selected stock's full daily history.
5. Before quick tuning, study every field in the field combination for every candidate model against the label: positive contribution, negative contribution, and noise suspicion. Identify important fields, secondary fields, duplicated fields, and likely redundant fields.
6. Field research must be documented in the target `docs/cx` scenario, task, change, or experiment summary area.
7. Field research must separate the semantic roles of daily base fields, market-strength indicators, position indicators, and ranking indicators: daily fields are the base; market-strength indicators measure cross-sectional overall strength; position indicators measure location in a time window; ranking indicators measure cross-sectional comparison.
8. Ranking fields need a dedicated check. They usually correspond to base fields, so determine whether using base and ranking fields together is harmful, whether ranking fields alone are sufficient, and whether ranking plus position fields works.
9. Before tuning, give explicit recommendations for enabled fields/features. Use one fixed model to validate different field combinations and document the recommendation in the field-research document.
10. Search in this order: field combinations, window length, and label definitions; training hyperparameters, optimizer, and scheduler; model structure, capacity, and complexity.
11. Window length and batch size must be searched together. Longer windows increase memory and compute cost, and attention-like or pairwise representations can grow close to quadratically with window length.
12. On high-memory hardware such as two NVIDIA RTX 5090 GPUs with 32 GB VRAM per card, treat VRAM use, GPU utilization, and training throughput as first-class constraints. For each window/field recipe, prefer the largest stable batch: start at `8192` when plausible, then fall back to `4096`, `2048`, `1024`, and `512` only when OOM, long windows, wide fields, or model structure require it. Do not keep tiny batches just because they are conservative.
13. Quick training has a planned cap of 60 epochs, monitors `val_loss`, and normally uses early-stopping patience 8. Stop when early stopping triggers, but naturally completing 60 epochs with stable improvement is the better candidate signal.
14. Record the ratio of `val_loss` improvement count to epoch count. A low ratio indicates questionable convergence quality, even when the final `val_loss` is acceptable.
15. For classification tasks, use `val_loss`/cross-entropy as the default training objective, tuning monitor, and early-stopping monitor. Record accuracy, precision, recall, F1, and AUC only as business evaluation metrics.
16. In multi-model projects, each model may have its own unique best field set, window length, label, and capacity configuration. Quick tuning must keep each model's per-model best candidate instead of prematurely keeping only one cross-model global ranking.
17. Quick tuning must establish a five-minute tracking cadence: take a baseline sample immediately after startup, then report every 5 minutes with the current trial, current epoch, latest `val_loss`, current best `val_loss`, `val_loss` improvement count, elapsed trial time, average epoch time, estimated remaining trials/epochs, GPU utilization, VRAM usage, peak VRAM, system memory, and current process memory. If no epoch or artifact changes within a 5-minute window, report the stalled position, process id, and resource-log path being written.
18. Every epoch and every trial must be written to a shared resource-monitoring artifact. Epoch records must include epoch index, start/end time, epoch duration, cumulative trial duration, training or validation `val_loss`, current best `val_loss`, GPU utilization, allocated/reserved/peak/free VRAM, total/available system memory, process memory, sample throughput, OOM status, and error reason. Trial-end records must include total trial duration, average epoch duration, completed epoch count, early-stop epoch, `val_loss` improvement count, best/final `val_loss`, `test_loss`, backtest metrics, and resource-log path.
19. Quick candidate reports must include Top10 business metrics: Top10 hit rate, mean gain for hit candidates, mean gain for missed candidates, Top10 downside share, and mean loss among downside candidates. The top-10 candidate table must also include trial name, stage, key recipe, `val_loss`, `test_loss`, trained epochs, `val_loss` improvement count, trial duration, average epoch duration, and those Top10 metrics.

## Required Workflow

1. Confirm the target `docs/cx` use case, design document, task, or change defines the business objective, data boundary, label target, and validation path. If not, return to `$cx-workflow` to recommend `$cx-story`, `$cx-research`, or `$cx-timeseries-modeling`.
2. Before startup or resume, confirm resource-monitor paths, the five-minute sampling method, and the top-10 candidate report fields. If the project lacks a shared resource monitor, add the public monitor and narrow tests first; do not replace structured artifacts with terminal spam.
3. Use `$cx-common-module` to check whether training entrypoints, backtest entrypoints, config hooks, recipes, resource monitoring, metric aggregation, and output persistence already have public entrypoints. If not, define the calling model first.
4. Use `$cx-pytorch-tdd` to verify standalone training, standalone backtesting, config clone/override hooks, trial-to-config mapping, resource monitoring, metric parsing, and output persistence paths.
5. Run field contribution research and small experiments before field candidates are tuned. Do not search model capacity while field semantics are still unclear.
6. Use one fixed model to validate field combinations, window length, and label definitions, then produce data recipe candidates.
7. Once data recipes are stable, search window length and batch size together. On dual 32 GB RTX 5090 hardware, try `8192`, `4096`, `2048`, `1024`, and `512` in descending order for each candidate window, and keep the fastest non-OOM setting with strong VRAM and GPU utilization.
8. Search learning rate, weight decay, optimizer, and scheduler after the window/batch budget is fixed; when batch size changes, retune learning rate with it.
9. Search model-structure parameters last, such as hidden size, layers, dropout, encoder length, capacity, and complexity.
10. Rerun the best recipe and record best trial, top candidates, each model's per-model best recipe, failed trials, pruned trials, five-minute tracking summaries, random seed, data version, field recommendations, and convergence evidence in the target `docs/cx` task, change, or experiment summary.
11. When the user requests business-first ranking, show the top-10 candidates by Top10 hit rate, missed-candidate mean gain, downside share, downside mean loss, and `val_loss`, while still preserving the `val_loss` diagnostic view.

## Verification Evidence

- Training and backtest scripts run independently with default config.
- Per-trial field enablement, field order, feature mode, per-field level counts, expanded per-field bins, label contract, and the complete config snapshot associated one-to-one with each checkpoint or weight artifact.
- Complete-entity one-tenth sample unit, entity count, coverage, and random seed.
- Field contribution, negative contribution, noise suspicion, duplicated fields, and redundant-field conclusions.
- Field-combination recommendation and fixed-model validation results.
- Window length, batch size, peak VRAM, remaining VRAM, GPU utilization, OOM status, sample throughput, epoch seconds, label definition, training hyperparameter, optimizer, scheduler, and model-structure search spaces.
- 60 epochs / patience 8 execution, early-stop epoch, best `val_loss`, `val_loss` improvement count, and improvement ratio.
- Five-minute tracking summaries with sample time, current trial, current epoch, latest `val_loss`, best `val_loss`, `val_loss` improvement count, elapsed trial time, average epoch seconds, estimated remaining work, GPU utilization, VRAM usage, peak VRAM, system memory, and process memory.
- Per-trial total duration, average epoch duration, completed epochs, early-stop epoch, best/final `val_loss`, `test_loss`, resource-log path, and OOM or failure reason.
- Top-10 candidate table with Top10 hit rate, hit-candidate mean gain, missed-candidate mean gain, Top10 downside share, downside mean loss, `val_loss`, `test_loss`, trained epochs, `val_loss` improvement count, trial duration, and average epoch duration.
- Each model's per-model best candidate, candidate configurations recommended for full-data tuning, and reasons rejected candidates are excluded.
