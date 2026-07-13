---
name: cx-pytorch-full-hpo
description: Use for full-data tuning in PyTorch, Lightning, and time-series projects; train, test, backtest, and compare the top 3 quick-HPO candidates using full data, with val_loss, test_loss, and backtest results used to select a release candidate model.
version: 0.1.0
---

# cx PyTorch Full HPO

## Language Rules

- Use the package language for conversations, explanations, plans, summaries, review decisions, verification evidence, and cx documents. Do not mix languages inside prose fragments or term lists.
- In Chinese-package work, if an English identifier, command, path, API name, library, protocol, standard, proper name, or ambiguity-sensitive term must remain in English, explain its meaning, role, and local context in Chinese in the same sentence or an adjacent sentence. In English-package work, explain unavoidable non-English terms in English.

## Resource-Safety Gate

The first step of every full-HPO experiment is to estimate expected system-memory and VRAM use, then decide whether the run may start. Record at least currently available system memory, currently available VRAM, expected peak use, the safety margin reserved for the operating system and Codex App, and the decision to start or reduce the experiment. The estimate may use model structure, tensor shapes, batch size, and a minimal trial run, but must not start full-data training merely to discover whether resources will be exhausted.

Full HPO is expected to consume substantial resources and run for a long time, so it must start in an external terminal outside Codex App. Codex App's built-in terminal must not host the training process or its high-volume output. Continuously write training progress, standard output, standard error, system memory, process memory, VRAM use, per-epoch metrics, and errors to file-based logs. The agent must analyze experiment status by reading those log files, without relying on scrolling terminal output, terminal control sequences, or other special terminal handling. This gate prevents resource exhaustion and system crashes, especially Codex App crashes caused by the training process or terminal-output load.

## Purpose

Validate quick-HPO candidates on complete data, select the best through third-best plans, and save the best model as a release candidate after training, test evaluation, backtesting, and user confirmation.

## Iron Rules

1. Full tuning must use `$cx-pytorch-quick-hpo` best recipe and candidate list as input. If quick tuning is skipped, document the reason, risk, and replacement validation path in the target `docs/cx` task, change, or experiment summary.
2. The training script must run by itself with default configuration. The full-tuning script may only clone and modify typed config in memory through a config hook, then pass that config object into the training entrypoint.
3. The backtest script must run by itself with default configuration. The full-tuning script may only call the backtest entrypoint with an in-memory config object and must not edit the current backtest config file.
4. When saving results, the tuning script may only persist trial configs, full-data recipes, test metrics, backtest configs, and model artifact paths into the output directory. Never rewrite the current project config, default config, or user-maintained config files.
5. Full tuning uses complete data, has a planned cap of 600 epochs, monitors `val_loss`, and normally uses early-stopping patience 20. Stop when early stopping triggers; do not force training to reach 600.
6. Full tuning first uses the quick-HPO best `val_loss` as the reference standard, then evaluates candidates with full-data `val_loss`, `test_loss`, and backtest results.
7. The full-tuning goal is to identify the best through third-best plans, but first fully train the rank-1 plan. Training must include test-set evaluation.
8. After rank-1 training and testing, immediately run backtesting. If the backtest result is good, ask the user whether to train the rank-2 and rank-3 candidates for comparison.
9. If the rank-1 backtest result is poor, record the failure reason and return to candidate ranking, field/label recipes, or quick-HPO evidence instead of automatically training other candidates.
10. When saving the best model as a release candidate, follow the existing `$cx-version` workflow, user-confirmation gate, version records, and release evidence requirements.
11. Multi-model projects must first select each model's per-model best release candidate, then compare those per-model winners to choose the global best. The global best is the default release for inference.
12. Inference must preserve the right to choose a different model release. The root `main` terminal menu and each model's `main` terminal menu must expose both the default global best release and selectable historical/candidate releases.
13. Full tuning must keep the same five-minute tracking cadence as quick tuning: take a baseline sample immediately after startup, then report every 5 minutes with the current candidate, current trial, current epoch, latest `val_loss`, current best `val_loss`, `val_loss` improvement count, elapsed candidate time, average epoch time, estimated remaining epochs, GPU utilization, VRAM usage, peak VRAM, system memory, and current process memory. If no epoch or artifact changes within a 5-minute window, report the stalled position, process id, and resource-log path.
14. Every full-tuning epoch, trial, and candidate must be written to a shared resource-monitoring artifact. Records must include start/end time, epoch duration, cumulative candidate duration, average epoch duration, GPU utilization, allocated/reserved/peak/free VRAM, total/available system memory, process memory, sample throughput, OOM status, best/final `val_loss`, `test_loss`, early-stop epoch, `val_loss` improvement count, and resource-log path.
15. Full candidate comparison and release recommendations must include Top10 business metrics: Top10 hit rate, mean gain for hit candidates, mean gain for missed candidates, Top10 downside share, and mean loss among downside candidates. Candidate tables must also include `val_loss`, `test_loss`, trained epochs, `val_loss` improvement count, trial duration, average epoch duration, and those business metrics.

## Required Workflow

1. Read the quick-HPO best recipe, top candidates, field recommendations, window length, label definition, training hyperparameters, and convergence evidence.
2. Use `$cx-common-module` to check whether full-data recipes, model saving, test evaluation, and backtest calls already have functional entrypoints. If not, define the calling model first.
3. Use `$cx-pytorch-tdd` to verify full-data config construction, in-memory config overrides, training entrypoint, test-stage entrypoint, backtest entrypoint, and output persistence.
4. Before starting the rank-1 candidate, confirm that resource monitoring, five-minute sampling, and candidate report fields can be written as structured artifacts. If missing, add the shared monitor and summary entrypoints first.
5. Train the rank-1 candidate with complete data and run test-set evaluation inside the training workflow. Every 5 minutes, report current epoch, `val_loss`, improvement count, candidate duration, and resource usage. After training, record `val_loss`, `test_loss`, resource metrics, and business metrics.
6. After training, derive the backtest config from the same in-memory config, run backtesting, and save the backtest config, Top10 hit rate, hit-candidate mean gain, missed-candidate mean gain, downside share, downside mean loss, and results into the output directory.
7. If the rank-1 candidate meets the backtest target, stop and ask the user whether to train the rank-2 and rank-3 candidates. Do not spend that compute before confirmation.
8. If the user confirms comparison, train and backtest rank-2 and rank-3 candidates in order, then rank all candidates by `val_loss`, `test_loss`, Top10 hit rate, missed-candidate mean gain, downside share, downside mean loss, and business risk.
9. For multi-model projects, select each model's per-model best candidate first, then compare the per-model winners to choose the global best. Set the global best as the default inference release.
10. Update, or require updating, the root `main` terminal menu and each model's `main` terminal menu so the global best release is selected by default while users can choose other model releases for inference.
11. After selecting the best model, write model artifact, recipe, test results, backtest results, five-minute tracking summaries, resource monitoring, data version, random seed, global-best basis, default inference release, and release recommendation into the target `docs/cx` task, change, or experiment summary.

## Verification Evidence

- Quick-HPO best recipe and top-3 candidate source.
- Training and backtest scripts run independently with default config.
- The full-tuning script only changes config in memory; the output directory contains full-data recipe, test config, backtest config, and candidate results; current config files are unchanged.
- Complete data boundary, train/validation/test split, data version, and random seed.
- 600 epochs / patience 20 execution, early-stop epoch, best `val_loss`, final `val_loss`, `test_loss`, and `val_loss` improvement count.
- Five-minute tracking summaries with sample time, current candidate, current epoch, latest `val_loss`, best `val_loss`, elapsed candidate time, average epoch seconds, estimated remaining epochs, GPU utilization, VRAM usage, peak VRAM, system memory, and process memory.
- Per-candidate trial duration, average epoch duration, peak VRAM, remaining VRAM, GPU utilization, system memory, process memory, sample throughput, and OOM or failure reason.
- Per-candidate Top10 hit rate, hit-candidate mean gain, missed-candidate mean gain, Top10 downside share, and downside mean loss.
- Rank-1 training, test, and backtest result, including whether the user was asked to continue with rank-2 and rank-3.
- Rank-2 and rank-3 comparison results; if skipped, record the user decision or stop reason.
- Candidate comparison table showing `val_loss`, `test_loss`, trained epochs, `val_loss` improvement count, trial duration, average epoch duration, and Top10 business metrics.
- Each model's per-model best release candidate, global-best selection basis, and default inference release.
- Verification that the root `main` terminal menu and each model's `main` terminal menu can choose the default global best or another release.
- Best model release-candidate path, recipe, metrics, backtest result, and `$cx-version` follow-up action.
