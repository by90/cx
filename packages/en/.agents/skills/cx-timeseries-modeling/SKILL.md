---
name: cx-timeseries-modeling
description: Use for heterogeneous multivariate time-series modeling, forecasting-target design, field-role classification, covariate design, leakage checks, backtesting, metric selection, and PyTorch time-series framework choice. PyTorch Forecasting is the default primary reference, especially TimeSeriesDataSet and Temporal Fusion Transformer variable roles, gating, and variable selection.
version: 0.1.1
---

# cx Heterogeneous Time-Series Modeling

## Language Rules

- Use the package language for conversations, explanations, plans, summaries, review decisions, verification evidence, and cx documents. Do not mix languages inside prose fragments or term lists.
- In Chinese-package work, if an English identifier, command, path, API name, library, protocol, standard, proper name, or ambiguity-sensitive term must remain in English, explain its meaning, role, and local context in Chinese in the same sentence or an adjacent sentence. In English-package work, explain unavoidable non-English terms in English.

## Purpose

Handle multivariate time series where each field has a different meaning. Do not treat fields as image pixels, homogeneous channels, or ordinary tokens by default. Model field semantics before choosing convolution, attention, RNNs, N-HiTS, TFT, or other models.

## Required Workflow

1. Define the target, forecast horizon, time granularity, entity grouping, train/validation/test time ranges, and business metric first.
2. When the project has formal models, read formal source, effective configurations, checkpoint descriptions, and business reports directly from project-authorized Git tags and frozen artifacts, then establish a formal baseline with the same data scope, label, split, and aggregation contract. Unless the user explicitly requests it, do not check out a tag, restore the working tree, create a worktree, or retrain a historical release merely to compare baselines. Simple statistical baselines supplement rather than replace the formal-model baseline.
3. Before training a new model, loss, feature, capacity, optimization, or scheduling direction, use `$cx-research` to research one explicit question online and synthesize formal-release facts with primary sources, peer-reviewed papers, and reliable reproductions into the current note under `docs/cx/notes/`. Do not train until the research freezes a falsifiable hypothesis, one changed variable, and contract-comparable acceptance criteria.
4. Independently count strict validation-loss improvements for every run. A run becomes valid model evidence only after at least twenty-one strict improvements. Mark a run with fewer than twenty-one as invalid evidence: it cannot support accepting or rejecting a model, loss, feature, capacity, optimizer, or schedule; serve as a baseline; promote or scale a candidate; or determine the next change. A local business-metric peak cannot bypass this gate.
5. Build a field semantics table: target, group id, static categorical, static real, time-varying known categorical/real, time-varying observed/unknown categorical/real, future-unavailable fields, missing-value policy, scaling policy, and leakage risk.
6. Use PyTorch Forecasting as the default primary reference. Use `TimeSeriesDataSet` for field roles and Temporal Fusion Transformer for variable selection, static context, gating, and multi-horizon forecasting patterns.
7. Do not default to plain CNNs, plain Transformers, or variables-as-tokens layouts. Allow them only after role-aware encoding, leakage checks, and baseline comparisons.
8. Establish naive, seasonal naive, linear, or tree baselines before comparing deep models. Do not compare only complex models.
9. Choose deep candidates by data size and objective: baseline/N-BEATS/N-HiTS first for smaller data, TFT for richer covariates and medium-or-larger data, and DeepAR or quantile losses for probabilistic forecasts.
10. Attention weights over time or variables are not direct feature importance. Combine variable-selection outputs with ablation, permutation, and business review.
11. Splits must be temporal or rolling-origin backtests. Random row splits are forbidden when they can leak future information.
12. Metrics must match the business objective: point forecasts can use MAE/RMSE/SMAPE/MASE; quantile or probabilistic forecasts must record quantile loss, coverage, or calibration.
13. Add `$cx-pytorch-hpo` for tuning: reuse the project's shared tuner, explicitly use a mature HPO sampler/pruner to jointly suggest parameters and allocate training resources on a fixed data boundary, and continuously analyze completed, pruned, and failed trials with the validation business metric first. Stock tasks use every eligible registration-regime entity; they neither sample one tenth of entities nor switch between lightweight and full-data stages.
14. Do not create unit tests by default; when unit tests are explicitly requested, verify only windows, field roles, leakage checks, metrics, and model input/output shapes. Do not run long training in unit tests.

## Framework Selection

- **PyTorch Forecasting is the primary reference**: `TimeSeriesDataSet` explicitly separates static variables, known-future variables, and observed-history variables; TFT provides variable selection, gating, and interpretability hooks for heterogeneous fields.
- **NeuralForecast is a secondary comparator**: use it for a broad modern model zoo, fast baselines, or Auto models, while keeping the field semantics table and leakage checks.
- **Darts is an orchestration aid**: useful for comparing classical and Torch models quickly, but do not let one API hide variable roles.
- **Plain Transformer/CNN is not the default**: time-series variables are usually not homogeneous tokens or pixels unless the architecture explicitly handles variable semantics.

## Modeling Evidence

- Field semantics table and leakage check.
- Horizon, granularity, group id, target, and label definition.
- Directly read formal-release tags, frozen configurations and reports, and the contract-comparable formal baseline; explicitly record when the project has no formal release.
- The pre-training research question, sources, synthesis, falsifiable hypothesis, one changed variable, and acceptance criteria.
- Baseline and deep-model metrics, together with each run's cumulative strict validation-loss improvement count and evidence eligibility.
- Rolling-origin or temporal split description.
- Proof that covariates are available at prediction time.
- Reason for choosing PyTorch Forecasting, NeuralForecast, Darts, or another framework.
- The fixed data boundary, complete conditional search space, frozen baseline, persistent study, training/validation trails, trial states, progress analysis, and final validation incumbent's strict test and backtest shared with `$cx-pytorch-hpo`.

## Research Reminders

- Transformers are not naturally superior for time series; every attention model needs baseline comparison.
- Patch, inverted-transformer, and channel-independent structures may be candidates, but they do not replace the field semantics table.
- TFT interpretation is an engineering signal, not causal proof.
