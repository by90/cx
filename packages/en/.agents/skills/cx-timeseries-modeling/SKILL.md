---
name: cx-timeseries-modeling
description: Use for heterogeneous multivariate time-series modeling, forecasting-target design, field-role classification, covariate design, leakage checks, backtesting, metric selection, and PyTorch time-series framework choice. PyTorch Forecasting is the default primary reference, especially TimeSeriesDataSet and Temporal Fusion Transformer variable roles, gating, and variable selection.
version: 0.1.0
---

# cx Heterogeneous Time-Series Modeling

## Language Rules

- Use the package language for conversations, explanations, plans, summaries, review decisions, verification evidence, and cx documents. Do not mix languages inside prose fragments or term lists.
- In Chinese-package work, if an English identifier, command, path, API name, library, protocol, standard, proper name, or ambiguity-sensitive term must remain in English, explain its meaning, role, and local context in Chinese in the same sentence or an adjacent sentence. In English-package work, explain unavoidable non-English terms in English.

## Purpose

Handle multivariate time series where each field has a different meaning. Do not treat fields as image pixels, homogeneous channels, or ordinary tokens by default. Model field semantics before choosing convolution, attention, RNNs, N-HiTS, TFT, or other models.

## Required Workflow

1. Define the target, forecast horizon, time granularity, entity grouping, train/validation/test time ranges, and business metric first.
2. Build a field semantics table: target, group id, static categorical, static real, time-varying known categorical/real, time-varying observed/unknown categorical/real, future-unavailable fields, missing-value policy, scaling policy, and leakage risk.
3. Use PyTorch Forecasting as the default primary reference. Use `TimeSeriesDataSet` for field roles and Temporal Fusion Transformer for variable selection, static context, gating, and multi-horizon forecasting patterns.
4. Do not default to plain CNNs, plain Transformers, or variables-as-tokens layouts. Allow them only after role-aware encoding, leakage checks, and baseline comparisons.
5. Establish naive, seasonal naive, linear, or tree baselines before comparing deep models. Do not compare only complex models.
6. Choose deep candidates by data size and objective: baseline/N-BEATS/N-HiTS first for smaller data, TFT for richer covariates and medium-or-larger data, and DeepAR or quantile losses for probabilistic forecasts.
7. Attention weights over time or variables are not direct feature importance. Combine variable-selection outputs with ablation, permutation, and business review.
8. Splits must be temporal or rolling-origin backtests. Random row splits are forbidden when they can leak future information.
9. Metrics must match the business objective: point forecasts can use MAE/RMSE/SMAPE/MASE; quantile or probabilistic forecasts must record quantile loss, coverage, or calibration.
10. When quickly tuning fields, labels, windows, model structure, or model choice, add `$cx-pytorch-quick-hpo`; when complete-data training, testing, backtesting, and release-candidate selection are required, add `$cx-pytorch-full-hpo`, and express the search space as config recipes.
11. Do not create unit tests by default; when unit tests are explicitly requested, verify only windows, field roles, leakage checks, metrics, and model input/output shapes. Do not run long training in unit tests.

## Framework Selection

- **PyTorch Forecasting is the primary reference**: `TimeSeriesDataSet` explicitly separates static variables, known-future variables, and observed-history variables; TFT provides variable selection, gating, and interpretability hooks for heterogeneous fields.
- **NeuralForecast is a secondary comparator**: use it for a broad modern model zoo, fast baselines, or Auto models, while keeping the field semantics table and leakage checks.
- **Darts is an orchestration aid**: useful for comparing classical and Torch models quickly, but do not let one API hide variable roles.
- **Plain Transformer/CNN is not the default**: time-series variables are usually not homogeneous tokens or pixels unless the architecture explicitly handles variable semantics.

## Modeling Evidence

- Field semantics table and leakage check.
- Horizon, granularity, group id, target, and label definition.
- Baseline metrics and deep-model metrics.
- Rolling-origin or temporal split description.
- Proof that covariates are available at prediction time.
- Reason for choosing PyTorch Forecasting, NeuralForecast, Darts, or another framework.
- Shared search space, best recipe, full-data training, test, backtest, and rerun result when `$cx-pytorch-quick-hpo` / `$cx-pytorch-full-hpo` are used.

## Research Reminders

- Transformers are not naturally superior for time series; every attention model needs baseline comparison.
- Patch, inverted-transformer, and channel-independent structures may be candidates, but they do not replace the field semantics table.
- TFT interpretation is an engineering signal, not causal proof.
