---
name: cx-pytorch-hpo
description: Use for broad automatic tuning, experiment design, and evidence in PyTorch, Lightning, and time-series projects. Covers hyperparameters, sample composition, feature enablement, feature ranges, bucket arrays, label definitions, model structure, and model selection. Optuna is the default primary tool; Ray Tune is a distributed execution shell; BoTorch/Ax is reserved for expensive continuous Bayesian optimization.
version: 0.1.0
---

# cx PyTorch Broad HPO

## Purpose

Treat tuning as auditable experiment design, not only learning-rate, batch-size, or optimizer search. Use this for PyTorch/Lightning training, feature recipes, label recipes, model structure, and model selection.

## Iron Rules

1. Automatic tuning starts with about one tenth of the data, but the sampling unit must be a complete entity. Do not keep only partial records for an entity. For example, with daily data for 2,000 stocks, randomly select about 200 stocks and keep the full daily history for those 200 stocks.
2. This one-tenth complete-entity dataset is used to quickly determine hyperparameters, model-capacity parameters, feature bucket arrays, suspension-handling strategy, optimizer choice, and scheduler choice. Fragmented samples must not replace complete entity samples.
3. One-tenth-data tuning has a planned cap of 60 epochs and uses early stopping on `val_loss` with patience normally set to 8. If `val_loss` does not improve for 8 consecutive epochs, stop early; do not force training to continue just to "reach 60".
4. A successful one-tenth-data tuning candidate should naturally complete 60 epochs without triggering early stopping. If a trial stops before 60 epochs, record it as an early-stopped trial and as a signal of insufficient capacity, unstable scheduling, or an unsuitable feature/label recipe instead of continuing it to 60.
5. Full-data tuning uses the complete dataset, has a planned cap of 600 epochs, and uses early stopping on `val_loss` with patience normally set to 20. When early stopping triggers, stop training; do not force training to reach 600.
6. For classification tasks, use `val_loss`/cross-entropy as the default training objective, tuning monitor, and early-stopping monitor. Record accuracy, precision, recall, F1, AUC, and similar business evaluation metrics according to class balance and error costs. If accuracy or precision is used as the HPO primary objective, document the class distribution, threshold policy, and business reason in the target documentation set.
7. If business constraints or compute limits require deviating from one-tenth complete data, 60 epochs, patience 8, full-data 600 epochs, or patience 20, record the reason, risk, and alternative validation path in the target documentation set first.

## Required Workflow

1. Confirm the target documentation set already defines the business objective, metric, data boundary, and user approval. If not, return to `$cx-bdd` or `$cx-research`.
2. Write a fixed baseline recipe before automatic search. The baseline must run with small real data and `unittest`.
3. Model the search target as typed config recipes: `data_recipe`, `feature_recipe`, `label_recipe`, `model_recipe`, `training_recipe`, and `evaluation_recipe`.
4. Every tunable item must come from the config subsystem and have a default value. Do not use script command-line arguments, environment-variable toggles, or string dispatch.
5. Use Optuna as the default primary tool. Use define-by-run conditional search spaces for feature switches, feature ranges, bucket arrays, label versions, model type, model structure, and training hyperparameters.
6. Use Optuna pruning and SQLite/RDB storage by default. Prefer SQLite for small projects; move to a shared database only for team or long-running studies.
7. Use Ray Tune only when multi-machine execution, multi-GPU scheduling, resource placement, or advanced early-stopping schedulers are required. The search algorithm can still be OptunaSearch.
8. Use BoTorch/Ax only for low-dimensional expensive continuous spaces, Bayesian surrogates, constrained optimization, or multi-objective optimization.
9. Each trial must rebuild the full recipe, so data, feature, and label changes cannot be lost inside the training loop.
10. Unit tests must not run full searches. They only verify recipe construction, objective wrapping, trial-to-config mapping, metric calculation, and persistence paths.
11. After search, rerun the best recipe and record the best trial, search space, failed trials, pruned trials, metrics, random seeds, and data version in the target documentation set's verification evidence.

## Tool Selection

- **Optuna is the default primary tool**: use it for dynamic conditional spaces, discrete/continuous/categorical values, feature subsets, model choice, pruning, trial importance, and SQLite-backed studies.
- **Ray Tune is the scaling shell**: use it when local Optuna is not parallel enough, GPU scheduling matters, or ASHA/PBT-style schedulers are needed.
- **BoTorch/Ax is specialized**: use it for expensive, continuous, low-to-mid-dimensional, multi-objective, or constrained Bayesian optimization, not as the default entrypoint.
- **Lightning Tuner is local help**: use it only for learning-rate or batch-size probes, not as a full experiment-search replacement.

## Search-Space Rules

- Express feature enablement with explicit boolean or categorical config values. Do not parse ad hoc string lists inside the objective.
- Feature ranges, bucket boundaries, and graded arrays must be named candidate configs. When continuous bounds are needed, express lower bounds, upper bounds, and defaults in typed config.
- Label definitions, prediction targets, losses, sampling strategies, and time windows are tunable recipes, but they need business explanations and leakage checks.
- Model structure and model selection may enter the search space, such as `model_family`, hidden size, layers, dropout, and encoder length. Every candidate family needs minimal test coverage.
- Trial importance only shows empirical sensitivity inside the searched space. Do not treat it as causal feature importance; confirm important feature claims with ablation, permutation, or business review.

## Verification Evidence

- Baseline recipe and metrics.
- Search-space config schema, defaults, and candidate values.
- Optuna study name, storage, sampler, pruner, trial count, and best trial.
- Whether one-tenth-data tuning naturally completed 60 epochs; for early-stopped trials, record the epoch, best `val_loss`, and stopping reason.
- Whether full-data tuning followed 600 epochs / patience 20; when early stopping triggers, record the epoch, best `val_loss`, and follow-up handling.
- Best-recipe rerun command and result.
- Business explanation and leakage check for feature, label, and model-structure changes.
- Reason for skipping Ray Tune, BoTorch/Ax, or Lightning Tuner.

## Primary References

- Optuna: default primary tool for define-by-run dynamic spaces, pruning, importance, and RDB storage.
- Ray Tune: distributed scheduling and large-scale trial execution.
- BoTorch/Ax: expensive Bayesian optimization.
- PyTorch official HPO tutorial: reference for PyTorch training-loop integration.
