---
name: cx-pytorch-full-hpo
description: Use for full-data HPO in PyTorch, Lightning, and time-series projects; accept exactly 5 lightweight-HPO candidates, adjust only batch size, learning rate, optimizer parameters, and scheduler parameters on all samples, then train, test, and backtest every candidate.
version: 0.1.0
---

# cx PyTorch Full HPO

## Language Rules

- Use the package language for conversations, explanations, plans, summaries, review decisions, verification evidence, and cx documents. Do not mix languages inside prose fragments or term lists.
- In Chinese-package work, if an English identifier, command, path, API name, library, protocol, standard, proper name, or ambiguity-sensitive term must remain in English, explain its meaning, role, and local context in Chinese in the same sentence or an adjacent sentence. In English-package work, explain unavoidable non-English terms in English.

## Resource-Safety Gate

The first step of every full-HPO experiment is to estimate expected system-memory and VRAM use, then decide whether the run may start. Record at least currently available system memory, currently available VRAM, expected peak use, the safety margin reserved for the operating system and Codex App, and the decision to start or adjust allowed training parameters such as batch size. The estimate may use model structure, tensor shapes, batch size, and a minimal trial run, but must not start full-data training merely to discover whether resources will be exhausted. All samples are the full-HPO data boundary; resource pressure must not reduce the sample ratio or change parameters frozen by lightweight HPO. If allowed training-parameter changes still cannot run safely, wait for sufficient resources.

Full HPO is expected to consume substantial resources and run for a long time, so it must start in an external terminal outside Codex App. Codex App's built-in terminal must not host the training process or its high-volume output. Continuously write training progress, standard output, standard error, system memory, process memory, VRAM use, per-epoch metrics, and errors to file-based logs. The agent must analyze experiment status by reading those log files, without relying on scrolling terminal output, terminal control sequences, or other special terminal handling. This gate prevents resource exhaustion and system crashes, especially Codex App crashes caused by the training process or terminal-output load.

## Purpose

Validate the `5` candidates fixed by lightweight HPO on all samples. Full HPO keeps data parameters, labels, windows, and model structure fixed, adjusts only batch size, learning rate, optimizer parameters, and scheduler parameters, then selects a release candidate after every candidate completes training, test evaluation, and backtesting.

## Iron Rules

1. Full HPO must take exactly the `5` candidates, complete recipes, ablation results, and backtest results delivered by `$cx-pytorch-quick-hpo`. It must not skip lightweight HPO or add, remove, or replace candidate identities during the full-data stage.
2. The training script must run by itself with default configuration. The full-tuning script may only clone and modify typed config in memory through a config hook, then pass that config object into the training entrypoint.
3. The backtest script must run by itself with default configuration. The full-tuning script may only call the backtest entrypoint with an in-memory config object and must not edit the current backtest config file.
4. When saving results, the tuning script may only persist trial configs, full-data recipes, test metrics, backtest configs, and model artifact paths into the output directory. Never rewrite the current project config, default config, or user-maintained config files.
5. Full HPO uses all samples, has a fixed cap of `120` epochs, monitors `val_loss`, and uses fixed early-stopping patience `9`. Every random process in trials, model initialization, data shuffling, and backtesting reads the seed config whose value is `3407` from the config subsystem.
6. Full HPO freezes the data parameters, field set, bin boundaries, feature mode, label definition, window length, model structure, and model capacity selected by lightweight HPO. Each candidate may search only batch size, learning rate, optimizer parameters, and scheduler parameters.
7. Full-HPO ranking prioritizes training sustainability: `val_loss` improvement count and ratio, whether the trial completed all `120` epochs, the best epoch, and the absolute and proportional distance from the best epoch to the final epoch. When sustainability is comparable, use best/final `val_loss`, `test_loss`, and backtest results.
8. All `5` candidates must complete training on all samples and test-set evaluation. Full HPO must not train only higher-ranked candidates or pause after the first candidate for extra confirmation.
9. Run backtesting immediately after each candidate completes training and testing. A good or poor result affects final comparison but never justifies skipping the remaining candidates.
10. If a candidate trains, tests, or backtests poorly, record its result and cause, then continue with the remaining candidates. Decide whether to return to lightweight HPO only after all `5` candidates finish.
11. When saving the best model as a release candidate, follow the existing `$cx-version` workflow, user-confirmation gate, version records, and release evidence requirements.
12. Multi-model projects must first select each model's per-model best release candidate, then compare those per-model winners to choose the global best. The global best is the default release for inference.
13. Inference must preserve the right to choose a different model release. The root `main` terminal menu and each model's `main` terminal menu must expose both the default global best release and selectable historical/candidate releases.
14. Full HPO must keep the same five-minute tracking cadence as lightweight HPO: take a baseline sample immediately after startup, then report every 5 minutes with the current candidate, current trial, current epoch, latest `val_loss`, current best `val_loss`, `val_loss` improvement count, elapsed candidate time, average epoch time, estimated remaining epochs, GPU utilization, VRAM usage, peak VRAM, system memory, and current process memory. If no epoch or artifact changes within a 5-minute window, report the stalled position, process id, and resource-log path.
15. Every full-HPO epoch, trial, and candidate must be written to a shared resource-monitoring artifact. Records must include start/end time, epoch duration, cumulative candidate duration, average epoch duration, GPU utilization, allocated/reserved/peak/free VRAM, total/available system memory, process memory, sample throughput, OOM status, best/final `val_loss`, `test_loss`, early-stop epoch, `val_loss` improvement count, the absolute and proportional best-to-final-epoch distance, and resource-log path.
16. The five-candidate comparison and release recommendation must include Top10 business metrics: Top10 hit rate, mean gain for hit candidates, mean gain for missed candidates, Top10 downside share, and mean loss among downside candidates. The table must also include candidate identity, allowed training-parameter changes, `val_loss`, `test_loss`, trained epochs, `val_loss` improvement count, absolute and proportional best-to-final-epoch distance, trial duration, average epoch duration, and those business metrics.

## Required Workflow

1. Read the `5` candidates, complete recipes, per-candidate ablation results, per-candidate backtests, field recommendations, window lengths, label definitions, model structures, and convergence evidence from lightweight HPO, then lock every parameter that full HPO may not change.
2. Use `$cx-common-module` to check whether full-data recipes, model saving, test evaluation, and backtest calls already have functional entrypoints. If not, define the calling model first.
3. Use `$cx-pytorch-tdd` to verify full-data config construction, in-memory config overrides, training entrypoint, test-stage entrypoint, backtest entrypoint, and output persistence.
4. Before starting candidates, confirm that resource monitoring, five-minute sampling, and five-candidate report fields can be written as structured artifacts. If missing, add the shared monitor and summary entrypoints first.
5. For each candidate, search only batch size, learning rate, optimizer parameters, and scheduler parameters, then choose that candidate's full-data recipe by training sustainability. Every comparison fixes all samples, the `120`-epoch cap, early-stopping patience `9`, and seed config value `3407`.
6. Train all `5` candidates on all samples and run test-set evaluation inside each training workflow. Every 5 minutes, report the current epoch, `val_loss`, improvement count, candidate duration, and resource usage. After training, record `val_loss`, `test_loss`, resource metrics, and sustainability evidence.
7. After each candidate finishes training, derive the backtest config from the same in-memory config, immediately run backtesting, and save the backtest config, Top10 hit rate, hit-candidate mean gain, missed-candidate mean gain, downside share, downside mean loss, and results into the output directory.
8. After all `5` candidates complete training, testing, and backtesting, compare training sustainability first, then rank by `val_loss`, `test_loss`, Top10 hit rate, missed-candidate mean gain, downside share, downside mean loss, and business risk.
9. For multi-model projects, select each model's per-model best candidate first, then compare the per-model winners to choose the global best. Set the global best as the default inference release.
10. Update, or require updating, the root `main` terminal menu and each model's `main` terminal menu so the global best release is selected by default while users can choose other model releases for inference.
11. After selecting the best model, write model artifact, recipe, test results, backtest results, five-minute tracking summaries, resource monitoring, data version, random seed, global-best basis, default inference release, and release recommendation into the target `docs/cx` task, change, or experiment summary.

## Verification Evidence

- Source of the `5` lightweight-HPO candidates, complete recipes, per-candidate ablation results, and per-candidate backtests.
- Training and backtest scripts run independently with default config.
- The full-tuning script only changes config in memory; the output directory contains full-data recipe, test config, backtest config, and candidate results; current config files are unchanged.
- Complete data boundary, train/validation/test split, data version, and random seed.
- Execution evidence for all samples, the `120`-epoch cap, early-stopping patience `9`, and seed config value `3407`; for every candidate include early-stop epoch, best/final `val_loss`, `test_loss`, `val_loss` improvement count and ratio, best epoch, and best-to-final-epoch distance.
- Evidence that data parameters, labels, windows, and model structures did not change during full HPO, and that only batch size, learning rate, optimizer parameters, and scheduler parameters differed.
- Five-minute tracking summaries with sample time, current candidate, current epoch, latest `val_loss`, best `val_loss`, elapsed candidate time, average epoch seconds, estimated remaining epochs, GPU utilization, VRAM usage, peak VRAM, system memory, and process memory.
- Per-candidate trial duration, average epoch duration, peak VRAM, remaining VRAM, GPU utilization, system memory, process memory, sample throughput, and OOM or failure reason.
- Per-candidate Top10 hit rate, hit-candidate mean gain, missed-candidate mean gain, Top10 downside share, and downside mean loss.
- Training, test, and per-candidate backtest results for all `5` candidates. If any candidate fails, include the cause and evidence that the remaining candidates continued.
- Five-candidate comparison table showing allowed training-parameter changes, sustainability evidence, `val_loss`, `test_loss`, trained epochs, `val_loss` improvement count, absolute and proportional best-to-final-epoch distance, trial duration, average epoch duration, and Top10 business metrics.
- Each model's per-model best release candidate, global-best selection basis, and default inference release.
- Verification that the root `main` terminal menu and each model's `main` terminal menu can choose the default global best or another release.
- Best model release-candidate path, recipe, metrics, backtest result, and `$cx-version` follow-up action.
