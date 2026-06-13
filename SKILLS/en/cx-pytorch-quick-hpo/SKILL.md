---
name: cx-pytorch-quick-hpo
description: Use for quick tuning in PyTorch, Lightning, and time-series projects; use about one tenth complete-entity data to study field contribution, feature sets, window length, labels, training hyperparameters, optimizer/scheduler choices, and model capacity before full-data tuning.
version: 0.1.0
---

# cx PyTorch Quick HPO

## Purpose

Find candidate configurations worth sending to full-data tuning with a smaller but complete sample. Quick tuning prioritizes data field combinations, window length, and label definitions before training hyperparameters, optimizer, scheduler, and model structure.

## Iron Rules

1. The training script must run by itself with default configuration. The tuning script may only clone and modify typed config in memory through a config hook, then pass that config object into the training entrypoint.
2. The backtest script must run by itself with default configuration. The tuning script may only call the backtest entrypoint with an in-memory config object and must not edit the current backtest config file.
3. When saving results, the tuning script may only persist trial configs, best recipes, metrics, and backtest configs into the output directory. Never rewrite the current project config, default config, or user-maintained config files.
4. Quick tuning uses about one tenth of the data, but the sampling unit must be a complete entity. For daily data from 2,000 stocks, randomly select about 200 stocks and keep each selected stock's full daily history.
5. Before quick tuning, study every field in the field combination for every candidate model against the label: positive contribution, negative contribution, and noise suspicion. Identify important fields, secondary fields, duplicated fields, and likely redundant fields.
6. Field research must be documented in the target documentation set's data-processing area. If the project already has a `series` data-processing directory, prefer `docs/<feature_group>/series/`.
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

## Required Workflow

1. Confirm the target documentation set defines the business objective, data boundary, label target, and validation path. If not, return to `$cx-workflow` to recommend `$cx-bdd`, `$cx-research`, or `$cx-timeseries-modeling`.
2. Use `$cx-common-module` to check whether training entrypoints, backtest entrypoints, config hooks, recipes, and output persistence already have public entrypoints. If not, define the calling model first.
3. Use `$cx-pytorch-tdd` to verify standalone training, standalone backtesting, config clone/override hooks, trial-to-config mapping, and output persistence paths.
4. Run field contribution research and small experiments before field candidates are tuned. Do not search model capacity while field semantics are still unclear.
5. Use one fixed model to validate field combinations, window length, and label definitions, then produce data recipe candidates.
6. Once data recipes are stable, search window length and batch size together. On dual 32 GB RTX 5090 hardware, try `8192`, `4096`, `2048`, `1024`, and `512` in descending order for each candidate window, and keep the fastest non-OOM setting with strong VRAM and GPU utilization.
7. Search learning rate, weight decay, optimizer, and scheduler after the window/batch budget is fixed; when batch size changes, retune learning rate with it.
8. Search model-structure parameters last, such as hidden size, layers, dropout, encoder length, capacity, and complexity.
9. Rerun the best recipe and record best trial, top candidates, each model's per-model best recipe, failed trials, pruned trials, random seed, data version, field recommendations, and convergence evidence in the target documentation set.

## Verification Evidence

- Training and backtest scripts run independently with default config.
- The tuning script only changes config in memory; the output directory contains saved trial config and best recipe; current config files are unchanged.
- Complete-entity one-tenth sample unit, entity count, coverage, and random seed.
- Field contribution, negative contribution, noise suspicion, duplicated fields, and redundant-field conclusions.
- Field-combination recommendation and fixed-model validation results.
- Window length, batch size, peak VRAM, remaining VRAM, GPU utilization, OOM status, sample throughput, epoch seconds, label definition, training hyperparameter, optimizer, scheduler, and model-structure search spaces.
- 60 epochs / patience 8 execution, early-stop epoch, best `val_loss`, `val_loss` improvement count, and improvement ratio.
- Each model's per-model best candidate, candidate configurations recommended for full-data tuning, and reasons rejected candidates are excluded.
