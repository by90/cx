---
name: cx-pytorch-hpo
description: Use for unified HPO in PyTorch, Lightning, and stock time-series projects; reuse the project's shared tuning module, run one candidate at a time on every eligible registration-regime entity, analyze the full trail with the validation business metric first, and permit only one evidence-backed next change.
version: 0.2.1
---

# cx Unified PyTorch HPO

## Purpose

Build one model-independent, evidence-driven tuning loop. Do not split tuning into lightweight and full-data stages, sample one tenth of entities, or prequeue candidates. Model directories declare recipes only; the shared module owns data scope, training, validation, monitoring, comparison, analysis, and continuation gates.

## Invariants

1. Read the current project AGENTS.md, effective config, shared training and tuning entrypoints, callers, tests, frozen baseline, and historical artifacts first. Old Git versions are recovery evidence only.
2. Evolve an existing model-independent tuner instead of copying candidate loops, config mutation, monitoring, ranking, or reporting into model directories. If Git history contains a removed tuner, audit its deletion, old dependencies, and current interfaces before restoring necessary behavior with TDD.
3. Build a typed config from the model's formal config and make immutable in-memory replacements only. Never put trial values in product defaults. Freeze the complete effective config one-to-one with every weight.
4. Stock tuning uses every eligible entity and daily row from the applicable registration-regime start. The ChiNext default is 2020-08-24; use a more precise audited project fact when declared. Never sample one tenth of stocks, reduce coverage for resources, or call pre-registration history the tuning full-data stage.
5. Time splits, labels, levels, ranking scores, and hit definitions come from the authoritative project entrypoint. Never reinterpret a label as an opening gap, raw close regression, or another target. Label, split, or business-evaluation changes create a new business group; a loss change creates only a new loss group.
6. Train on training data and select weights, thresholds, candidates, and next changes on validation data. Strict test may audit a frozen candidate, but its metrics cannot enter progress analysis or next-candidate selection. If they do, stop and declare contamination.
7. Start one complete candidate at a time. Never prequeue, continuously autorun, or predetermine five candidates. Analyze the finished candidate first; continuation requires one falsifiable cause and one minimal change.
8. The validation business objective is primary for candidate selection. Validation loss supports gradients, checkpoints, and convergence diagnosis. Never advance solely on better loss while business performance keeps falling. Do not repeat a rejected class-weighting or similar scheme without a new hypothesis.
9. User hardware, memory, and elapsed-time limits are gates. Estimate VRAM, system memory, epoch time, and total time from real tensor shapes and a minimal run. Adjust only unfrozen capacity, batch, or precision; never change data coverage or user-fixed dimensions.
10. Freeze business-best, minimum-validation-loss, and true-final checkpoints whenever required. Strict test uses only the project-authorized checkpoint.
11. Every formal HPO candidate has immutable max_epochs=1000 and early_stopping_patience=20. Neither value is ever a candidate dimension. The shared tuner and progress analyzer must reject missing, overridden, or inconsistent values before launch. Older contracts may be retained only as historical preliminary runs and cannot enter the formal comparable trail.

## Shared Module Contract

The shared tuner is the only implementation of this lifecycle:

- Accept one candidate and in-memory config, never a candidate queue.
- Validate registration start, all eligible entities, temporal splits, data version, and content digests.
- Call independent training and validation entrypoints; thin model adapters build only networks, losses, and recipes.
- Record train/validation loss, primary business metric, learning rate, time, throughput, GPU utilization, VRAM, system memory, and process memory every epoch.
- Freeze effective config, required checkpoints, history, resources, validation predictions, business metrics, and analysis.
- Require one changed_dimension. Compare business metrics only inside a business_comparison_group with the same label, split, and business evaluation; compare validation loss only inside a loss_comparison_group with the same loss definition.
- Before launch, require both the global and per-trial training contract to be max_epochs=1000 and early_stopping_patience=20; reject either value as changed_dimension or an in-memory override.
- Refuse the next candidate until analysis returns continue.

Do not restore an old QuickTune API that sequentially runs all trials or puts business metrics behind loss. Its thin adapters, in-memory configs, validation isolation, resource audit, and frozen-artifact design remain useful evidence.

## Extreme-Imbalance Objective

1. Rerun and freeze the baseline with current source, config, and correct data boundary before changing algorithms.
2. Declare one primary validation business metric, such as daily dynamic-TopN highest-two-level precision or fixed-Top10 hit rate. Preserve recall, selected return, tail risk, and daily stability too.
3. For nine levels, save per-class support, confusion, highest-two-level precision and recall, prediction coverage, and calibration. Overall accuracy cannot replace the highest-two-level goal.
4. Multiclass, ordinal, differentiable-ranking, pairwise-ranking, and TopK compositions may be candidates, but change only loss in that experiment. Its loss enters a new loss group and is not directly compared; business remains comparable when label, split, and business evaluation stay fixed.
5. Never use strict test to select weights, thresholds, TopN, loss, architecture, or hyperparameters.

## One-Candidate Loop

1. Build a scope ledger. Mark fields, labels, windows, model capacity, longitudinal and cross-sectional summary capacity, loss, optimizer, learning rate, scheduler, batch, and precision as user-fixed, searched, or excluded with evidence.
2. Rerun and freeze baseline business, validation loss, resources, three checkpoints, and data summary.
3. Derive one falsifiable hypothesis from the previous analysis and change one dimension. Stop without a hypothesis.
4. Pass the resource gate, write structured artifacts each epoch, and report progress or the exact stall at least every five minutes.
5. After completion, read training and validation artifacts only and run scripts/analyze_hpo_progress.py. Do not train another candidate unless it returns continue.
6. Analyze business movement against baseline and the previous candidate, regression streaks, loss/business conflict, effective improvements, best epoch, resources, failures, and comparability.
7. Stop the complete-run chain after two significant comparable business regressions, or when loss improves while business materially regresses. Repair the objective, run a minimal diagnostic, or return to baseline.
8. Continue only after material business improvement without unacceptable risk or resource regression. Do not make strong claims below the project's minimum meaningful delta.
9. Run strict test and backtest after freezing the final recipe; report them separately from validation.

## Progress Analyzer

Run:

    python scripts/analyze_hpo_progress.py path/to/ledger.json path/to/analysis

The ledger contains data_scope, training_contract, objective, baseline_trial, trials, strict_test_used_for_selection, and at most one proposed_next. training_contract records immutable max_epochs=1000 and early_stopping_patience=20; every trial repeats planned_epochs=1000, max_epochs=1000, and early_stopping_patience=20. Each completed trial records its name, business_comparison_group, loss_comparison_group, primary business metric, best/final validation loss, completed/planned epochs, best epoch, resource gate, and unique changed_dimension.

The tool writes analysis.json and analysis.md. It enforces all-entity registration-regime scope and the 1000/20 training contract, rejects strict-test selection, and detects consecutive business regression, loss/business conflict, incomparable trials, multiple changes, ineffective learning, and resource failures. It analyzes evidence and never launches training.

## Completion Evidence

- Shared tuner and caller audit, including decisions about removed behavior.
- Registration start, eligible entity count, dates, three split boundaries, data version, and content digests.
- Frozen baseline, scope ledger, one change per candidate, and complete configs.
- Per-epoch business, loss, and resource trails; three checkpoints, validation predictions, and analysis per candidate.
- Baseline business deltas, regression streaks, objective conflicts, and stop/continue reasons.
- Strict test and backtest for the final frozen recipe, with proof that neither selected candidates.
