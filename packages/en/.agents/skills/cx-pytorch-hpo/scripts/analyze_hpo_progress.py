#!/usr/bin/env python3
"""Validate and summarize a persistent automatic-HPO ledger without strict test."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def _mapping(payload: dict, field: str) -> dict:
    """Read one required object field.

    Args:
        payload: Current parent mapping.
        field: Field that must contain an object.

    Returns:
        The object stored under the field.
    """
    value = payload.get(field)
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    return value


def _text(payload: dict, field: str) -> str:
    """Read one required non-empty text field.

    Args:
        payload: Current parent mapping.
        field: Field that must contain non-empty text.

    Returns:
        Text with surrounding whitespace removed.
    """
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be non-empty text")
    return value.strip()


def _number(value: Any, field: str) -> float:
    """Convert one required finite number to a float.

    Args:
        value: Numeric value from the ledger.
        field: Field description used in an error.

    Returns:
        A finite floating-point number.
    """
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")
    return result


def _epoch_reports(
    trial: dict,
    number: int,
    completed_epochs: int,
    patience: int,
) -> list[dict]:
    """Validate and normalize one trial's per-epoch training and business report.

    Args:
        trial: Current trial ledger object.
        number: Trial number.
        completed_epochs: Number of complete training epochs.
        patience: Study-frozen early-stopping patience.

    Returns:
        Normalized reports in contiguous one-based epoch order.
    """
    # The per-epoch report is the sole trail used by completion diagnostics.
    reports = trial.get("epoch_reports")
    # The ledger must preserve every complete epoch rather than only final state.
    if not isinstance(reports, list):
        raise ValueError(f"trial {number} epoch_reports must be an array")
    # Epoch count and report count must agree before a completion claim is made.
    if len(reports) != completed_epochs:
        raise ValueError(f"trial {number} epoch_reports must match completed_epochs")
    # The normalized result retains only fields from the unified report contract.
    normalized = []
    # Cumulative strict validation-loss improvements cannot decrease over time.
    previous_improvements = 0
    # Contiguous one-based epochs make plateau start directly interpretable.
    for expected_epoch, report in enumerate(reports, start=1):
        # Each epoch report must be an object with named fields.
        if not isinstance(report, dict):
            raise ValueError(f"trial {number} epoch report must be an object")
        # The recorded epoch must match its complete-trail position.
        epoch = int(report.get("epoch", 0))
        if epoch != expected_epoch:
            raise ValueError(f"trial {number} epoch reports must be contiguous")
        # The validation-loss count remains separate from selection patience.
        improvements = int(report.get("validation_loss_improvement_count", -1))
        if improvements < previous_improvements:
            raise ValueError(
                f"trial {number} validation loss improvement count must not decrease"
            )
        # The current count becomes the lower bound for the next epoch.
        previous_improvements = improvements
        # Early-stopping count stays between zero and frozen patience.
        early_stopping_count = int(report.get("early_stopping_count", -1))
        if early_stopping_count < 0 or early_stopping_count > patience:
            raise ValueError(f"trial {number} early stopping count is out of range")
        # Stock business reporting supplies both dynamic and fixed prefixes.
        business = _mapping(report, "business_report")
        # Training, validation, and business facts form one immutable analysis row.
        normalized.append(
            {
                "epoch": epoch,
                "train_loss": _number(
                    report.get("train_loss"), f"trial {number} train loss"
                ),
                "validation_loss": _number(
                    report.get("validation_loss"),
                    f"trial {number} validation loss",
                ),
                "validation_loss_improvement_count": improvements,
                "early_stopping_count": early_stopping_count,
                "business_report": {
                    "dynamic_topn": _number(
                        business.get("dynamic_topn"),
                        f"trial {number} dynamic TopN",
                    ),
                    "fixed_top1": _number(
                        business.get("fixed_top1"), f"trial {number} fixed Top1"
                    ),
                    "fixed_top3": _number(
                        business.get("fixed_top3"), f"trial {number} fixed Top3"
                    ),
                    "fixed_top10": _number(
                        business.get("fixed_top10"),
                        f"trial {number} fixed Top10",
                    ),
                },
            }
        )
    # The shared result feeds loss completion, plateau, and Markdown reporting.
    return normalized


def _loss_report(
    trial: dict,
    number: int,
    state: str,
    reports: list[dict],
    reference: float,
    floor: float | None,
    precision: float,
    plateau_window: int,
) -> dict | None:
    """Calculate theoretical-loss completion, plateau, and manual-fit fields.

    Args:
        trial: Current trial ledger object.
        number: Trial number.
        state: Normalized trial state.
        reports: Validated per-epoch training and business reports.
        reference: No-information theoretical reference loss.
        floor: Theoretical loss floor when available.
        precision: Frozen precision for meaningful loss movement.
        plateau_window: Complete trailing epochs required for a plateau.

    Returns:
        None without a complete epoch, otherwise the unified completion report.
    """
    # No complete epoch means no loss-completion or plateau evidence exists.
    if not reports:
        return None
    # The minimum validation-loss epoch is the fixed completion comparison point.
    best = min(reports, key=lambda row: row["validation_loss"])
    # The last complete epoch preserves the true stopping state.
    final = reports[-1]
    # Precision-relative running best identifies meaningful improvements.
    meaningful_best = reports[0]["validation_loss"]
    # Epoch one establishes the initial comparable loss level.
    last_meaningful_epoch = reports[0]["epoch"]
    # Later epochs reset plateau only when they exceed frozen precision.
    for report in reports[1:]:
        # Accumulated small changes can eventually become meaningful.
        if report["validation_loss"] < meaningful_best - precision:
            # The newly meaningful best becomes the next comparison baseline.
            meaningful_best = report["validation_loss"]
            # This epoch is the latest meaningful validation improvement.
            last_meaningful_epoch = report["epoch"]
    # Declare a plateau only after a complete terminal observation window.
    plateau_start = (
        last_meaningful_epoch + 1
        if final["epoch"] - last_meaningful_epoch >= plateau_window
        else None
    )
    # Each trial states whether train and validation losses may be subtracted.
    comparable = trial.get("losses_comparable")
    if not isinstance(comparable, bool):
        raise ValueError(f"trial {number} losses_comparable must be boolean")
    # Preserve the project's concrete semantics when the losses are incomparable.
    incomparable_reason = None
    if not comparable:
        # An explicit reason prevents a misleading generalization gap.
        incomparable_reason = _text(trial, "loss_incomparability_reason")
    # An ended effective trial must freeze a manual fit assessment.
    fit_assessment = trial.get("fit_assessment")
    # Complete and pruned states both require the human assessment contract.
    if state in ("complete", "pruned"):
        # A fixed value set stays machine-readable without automating judgment.
        if fit_assessment not in (
            "overfitting",
            "underfitting",
            "healthy_fit",
            "insufficient_evidence",
        ):
            raise ValueError(f"trial {number} fit_assessment is invalid")
    # Running and failed trials may not yet have a manual assessment.
    elif fit_assessment is not None:
        # A supplied non-terminal value still uses the same text contract.
        fit_assessment = _text(trial, "fit_assessment")
    # Manual judgment records the concrete epochs used as evidence.
    evidence_epochs = trial.get("fit_evidence_epochs", [])
    if not isinstance(evidence_epochs, list):
        raise ValueError(f"trial {number} fit_evidence_epochs must be an array")
    # Convert evidence to a stable list of one-based integer epochs.
    evidence_epochs = [int(epoch) for epoch in evidence_epochs]
    # Every evidence epoch must exist in this trial's real trail.
    if any(epoch < 1 or epoch > final["epoch"] for epoch in evidence_epochs):
        raise ValueError(f"trial {number} fit evidence epoch is out of range")
    # Absolute improvement compares best validation loss with the frozen reference.
    absolute_improvement = reference - best["validation_loss"]
    # Relative improvement is undefined when the theoretical reference is zero.
    relative_improvement = (
        None if reference == 0 else absolute_improvement / abs(reference) * 100
    )
    # Reducible-loss completion requires a valid theoretical floor.
    completion = (
        None
        if floor is None or reference <= floor
        else absolute_improvement / (reference - floor) * 100
    )
    # Produce a train-validation gap only under comparable loss semantics.
    best_gap = best["validation_loss"] - best["train_loss"] if comparable else None
    # The final gap supports manual fit diagnosis and never selects a trial.
    final_gap = final["validation_loss"] - final["train_loss"] if comparable else None
    # Preserve theoretical, training, validation, business, and human evidence.
    return {
        "validation_best_epoch": best["epoch"],
        "train_loss_at_validation_best": best["train_loss"],
        "validation_loss_best": best["validation_loss"],
        "gap_at_validation_best": best_gap,
        "final_epoch": final["epoch"],
        "final_train_loss": final["train_loss"],
        "final_validation_loss": final["validation_loss"],
        "final_gap": final_gap,
        "loss_reference": reference,
        "loss_floor": floor,
        "absolute_improvement": absolute_improvement,
        "relative_improvement_percent": relative_improvement,
        "reducible_loss_completion_percent": completion,
        "plateau_start_epoch": plateau_start,
        "plateau_window": plateau_window,
        "loss_report_precision": precision,
        "losses_comparable": comparable,
        "loss_incomparability_reason": incomparable_reason,
        "fit_assessment": fit_assessment,
        "fit_evidence_epochs": evidence_epochs,
        "business_at_validation_best": best["business_report"],
        "business_at_final": final["business_report"],
        "validation_loss_improvement_count": final["validation_loss_improvement_count"],
        "early_stopping_count": final["early_stopping_count"],
    }


def analyze(payload: dict) -> dict:
    """Validate HPO scope, tools, stopping policy, trial states, and incumbent.

    Args:
        payload: Root object of the persistent HPO ledger.

    Returns:
        A normalized result ready for analysis artifacts.
    """
    # The registration regime and all eligible entities are fixed stock-HPO premises.
    if not isinstance(payload, dict):
        raise ValueError("ledger must be an object")
    scope = _mapping(payload, "data_scope")
    if scope.get("kind") != "registration_regime":
        raise ValueError("data scope must be the registration regime")
    _text(scope, "id")
    _text(scope, "start_date")
    if scope.get("all_eligible_entities") is not True:
        raise ValueError("registration-regime HPO must use all eligible entities")
    if payload.get("strict_test_used_for_selection") is not False:
        raise ValueError("strict test must not participate in HPO")

    # The optimizer records its sampler, pruner, and recoverable storage explicitly.
    optimizer = _mapping(payload, "optimizer")
    for field in ("tool", "sampler", "pruner", "storage"):
        _text(optimizer, field)
    resource = _mapping(payload, "resource_policy")
    if _number(resource.get("max_wallclock_seconds"), "max_wallclock_seconds") <= 0:
        raise ValueError("max_wallclock_seconds must be positive")
    # Formal HPO and ordinary candidates share 120 epochs as the per-trial limit.
    max_epochs = int(resource.get("max_resource", 0))
    if max_epochs != 120:
        raise ValueError("max_resource must equal 120 epochs")
    # The trainer keeps early stopping while the pruner only terminates weaker trials sooner.
    if resource.get("framework_early_stopping") is not True:
        raise ValueError("automatic HPO must enable framework early stopping")
    # Stop a trial after nine epochs without any validation-objective improvement.
    if int(resource.get("early_stopping_patience", 0)) != 9:
        raise ValueError("early stopping patience must equal 9 epochs")
    # A zero threshold ensures that every strict improvement resets patience immediately.
    if (
        _number(resource.get("early_stopping_min_delta"), "early_stopping_min_delta")
        != 0
    ):
        raise ValueError("early stopping min_delta must equal zero")

    # The single validation business objective defines direction and the incumbent.
    objective = _mapping(payload, "objective")
    metric = _text(objective, "business_metric")
    direction = _text(objective, "direction")
    if direction not in ("maximize", "minimize"):
        raise ValueError("objective.direction must be maximize or minimize")

    # The no-information theoretical reference cannot come from any trial.
    loss_reference = _number(payload.get("loss_reference"), "loss_reference")
    # A null floor records that the current loss lacks a provable completion scale.
    loss_floor_value = payload.get("loss_floor")
    # Normalize an available finite floor once for every trial.
    loss_floor = (
        None if loss_floor_value is None else _number(loss_floor_value, "loss_floor")
    )
    # Reporting precision decides whether loss movement is meaningful.
    loss_report_precision = _number(
        payload.get("loss_report_precision"), "loss_report_precision"
    )
    if loss_report_precision <= 0:
        raise ValueError("loss_report_precision must be positive")
    # A plateau observation window contains at least one complete epoch.
    plateau_window = int(payload.get("plateau_window", 0))
    if plateau_window <= 0:
        raise ValueError("plateau_window must be positive")

    # The ledger retains complete, pruned, failed, running, and waiting trials.
    trials = payload.get("trials")
    if not isinstance(trials, list):
        raise ValueError("trials must be an array")
    allowed = {"complete", "pruned", "failed", "running", "waiting"}
    numbers: set[int] = set()
    rows = []
    completed = []
    # Normalize every trial against the current field contract.
    for trial in trials:
        if not isinstance(trial, dict):
            raise ValueError("every trial must be an object")
        number = int(trial.get("number", -1))
        if number < 0 or number in numbers:
            raise ValueError("trial numbers must be unique non-negative integers")
        numbers.add(number)
        state = _text(trial, "state").lower()
        if state not in allowed:
            raise ValueError(f"unsupported trial state: {state}")
        params = trial.get("params")
        if not isinstance(params, dict):
            raise ValueError("trial.params must be an object")
        intermediate = trial.get("intermediate_values", {})
        if not isinstance(intermediate, (dict, list)):
            raise ValueError("trial.intermediate_values must be an object or array")
        values = (
            intermediate.values() if isinstance(intermediate, dict) else intermediate
        )
        for value in values:
            _number(value, f"trial {number} intermediate value")
        epochs = int(trial.get("completed_epochs", 0))
        if epochs < 0:
            raise ValueError("completed_epochs must be non-negative")
        # Pruned, failed, and completed trials all remain within the unified epoch limit.
        if epochs > max_epochs:
            raise ValueError("completed_epochs must not exceed 120")
        # The full training and business trail supports completion and plateau facts.
        epoch_reports = _epoch_reports(
            trial,
            number,
            epochs,
            int(resource["early_stopping_patience"]),
        )
        # Freeze stock-ranking scale and dynamic-N semantics beside metric values.
        business_context = _mapping(trial, "business_context")
        # Four text fields make cross-scale TopN comparison auditable.
        business_context = {
            field: _text(business_context, field)
            for field in (
                "scale",
                "opportunity_definition",
                "daily_n_source",
                "aggregation",
            )
        }
        # Calculate the unified completion report from the study loss contract.
        loss_report = _loss_report(
            trial,
            number,
            state,
            epoch_reports,
            loss_reference,
            loss_floor,
            loss_report_precision,
            plateau_window,
        )
        value = trial.get("value")
        if state == "complete":
            value = _number(value, f"trial {number} value")
        elif value is not None:
            value = _number(value, f"trial {number} value")
        row = {
            "number": number,
            "state": state,
            "value": value,
            "params": params,
            "completed_epochs": epochs,
            "business_best_epoch": trial.get("business_best_epoch"),
            "validation_loss_best": (
                None if loss_report is None else loss_report["validation_loss_best"]
            ),
            "epoch_reports": epoch_reports,
            "business_context": business_context,
            "training_report": loss_report,
            "duration_seconds": trial.get("duration_seconds"),
            "gpu_peak_reserved_bytes": trial.get("gpu_peak_reserved_bytes"),
            "failure": trial.get("failure"),
            "artifacts": trial.get("artifacts", {}),
        }
        rows.append(row)
        if state == "complete":
            completed.append(row)

    # Only completed trials can become incumbent; other states remain audit evidence.
    best = None
    if completed:
        select = max if direction == "maximize" else min
        best = select(completed, key=lambda row: row["value"])
    counts = {state: sum(row["state"] == state for row in rows) for state in allowed}
    importance = payload.get("parameter_importance", {})
    if not isinstance(importance, dict):
        raise ValueError("parameter_importance must be an object")
    importance = {
        str(name): _number(value, f"parameter importance {name}")
        for name, value in importance.items()
    }
    # Preserve resources, failures, importance, and strict-test isolation in the result.
    return {
        "schema_version": 3,
        "data_scope_id": scope["id"],
        "data_scope_start_date": scope["start_date"],
        "business_metric": metric,
        "direction": direction,
        "optimizer": {
            field: optimizer[field]
            for field in ("tool", "sampler", "pruner", "storage")
        },
        "resource_policy": resource,
        "loss_reference": loss_reference,
        "loss_floor": loss_floor,
        "loss_report_precision": loss_report_precision,
        "plateau_window": plateau_window,
        "counts": {"total": len(rows), **counts},
        "best_trial": best,
        "parameter_importance": importance,
        "failures": [row for row in rows if row["failure"]],
        "trials": rows,
        # The selection contract makes the frozen trial value the sole selection input.
        "used_for_selection": {
            "trial_value": True,
            "objective_metric": metric,
            "epoch_reports": False,
            "training_report": False,
            "strict_test": False,
        },
        "strict_test_used_for_selection": False,
    }


def markdown(result: dict) -> str:
    """Render a compact automatic-HPO audit report.

    Args:
        result: Normalized result returned by `analyze`.

    Returns:
        Markdown report text ending with a newline.
    """
    best = result["best_trial"]
    best_text = (
        "none"
        if best is None
        else f"trial {best['number']} value={best['value']:.8f} epochs={best['completed_epochs']}"
    )
    lines = [
        "# Automatic HPO progress analysis",
        "",
        f"- Data scope: {result['data_scope_id']} from {result['data_scope_start_date']}; all eligible entities.",
        f"- Objective: {result['business_metric']} ({result['direction']}).",
        f"- Tool: {result['optimizer']['tool']}; sampler={result['optimizer']['sampler']}; pruner={result['optimizer']['pruner']}.",
        f"- Loss reference: {result['loss_reference']:.8f}; floor={result['loss_floor']}; precision={result['loss_report_precision']}; plateau window={result['plateau_window']}.",
        f"- Trials: complete={result['counts']['complete']}, pruned={result['counts']['pruned']}, failed={result['counts']['failed']}, running={result['counts']['running']}.",
        f"- Incumbent: {best_text}.",
        f"- Selection contract: only trial.value for {result['used_for_selection']['objective_metric']}; epoch reports, training diagnostics, and strict test are report-only.",
        "",
        "## Parameter importance",
        "",
    ]
    lines.extend(
        [
            f"- {name}: {value:.6f}"
            for name, value in result["parameter_importance"].items()
        ]
        or ["- Not enough completed trials."]
    )
    lines.extend(
        [
            "",
            "## Trial trail",
            "",
            "| Trial | State | Value | Epochs | Best epoch | Train loss at best | Best validation loss | Absolute reference improvement | Relative reference improvement | Reducible-loss completion | Plateau start | Fit | Validation improvements | Early stop | Failure |",
            "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |",
        ]
    )
    for row in result["trials"]:
        # A trial without a first complete epoch has no completion report.
        report = row["training_report"]
        # Keep unavailable values blank so Markdown never presents them as zero.
        best_validation = (
            "" if report is None else f"{report['validation_loss_best']:.8f}"
        )
        # The best epoch binds training, validation, and business facts to one checkpoint.
        best_epoch = "" if report is None else str(report["validation_best_epoch"])
        # Same-epoch training loss supports manual train-validation divergence review.
        train_at_best = (
            "" if report is None else f"{report['train_loss_at_validation_best']:.8f}"
        )
        # Absolute improvement answers how far actual loss beats the no-information reference.
        absolute = "" if report is None else f"{report['absolute_improvement']:.8f}"
        # Relative improvement stays blank when a zero theoretical reference makes it undefined.
        relative = (
            ""
            if report is None or report["relative_improvement_percent"] is None
            else f"{report['relative_improvement_percent']:.4f}%"
        )
        # A percent sign distinguishes completion from raw loss.
        completion = (
            ""
            if report is None or report["reducible_loss_completion_percent"] is None
            else f"{report['reducible_loss_completion_percent']:.4f}%"
        )
        # Do not fabricate a plateau before a complete observation window exists.
        plateau = (
            ""
            if report is None or report["plateau_start_epoch"] is None
            else str(report["plateau_start_epoch"])
        )
        # Render only the manual fit value already frozen in the ledger.
        fit = (
            ""
            if report is None or report["fit_assessment"] is None
            else report["fit_assessment"]
        )
        # Final validation-loss improvement count summarizes training continuity.
        improvements = (
            "" if report is None else str(report["validation_loss_improvement_count"])
        )
        # Final early-stopping count stays separate from validation improvements.
        early_stop = "" if report is None else str(report["early_stopping_count"])
        value = "" if row["value"] is None else f"{row['value']:.8f}"
        lines.append(
            f"| {row['number']} | {row['state']} | {value} | {row['completed_epochs']} | {best_epoch} | {train_at_best} | {best_validation} | {absolute} | {relative} | {completion} | {plateau} | {fit} | {improvements} | {early_stop} | {row['failure'] or ''} |"
        )
    # The epoch table exposes every requested training state and stock business measure.
    lines.extend(
        [
            "",
            "## Per-epoch training and business report",
            "",
            "| Trial | Epoch | Train loss | Validation loss | Validation loss improvements | Early stop | Dynamic TopN | Fixed Top1 | Fixed Top3 | Fixed Top10 |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    # Trials are expanded in completed-epoch order, including an active trial's current trail.
    for row in result["trials"]:
        # The maximum epoch count comes from the frozen study resource contract.
        max_epochs = result["resource_policy"]["max_resource"]
        # The early-stopping denominator is the frozen study patience.
        patience = result["resource_policy"]["early_stopping_patience"]
        # Each complete epoch keeps losses, counters, and all four business measures together.
        for report in row["epoch_reports"]:
            # Business observations remain bound to the same training epoch.
            business = report["business_report"]
            # Four decimal percentage precision prevents display rounding from hiding changes.
            lines.append(
                f"| {row['number']} | {report['epoch']}/{max_epochs} | "
                f"{report['train_loss']:.8f} | {report['validation_loss']:.8f} | "
                f"{report['validation_loss_improvement_count']} | "
                f"{report['early_stopping_count']}/{patience} | "
                f"{business['dynamic_topn'] * 100:.4f}% | "
                f"{business['fixed_top1'] * 100:.4f}% | "
                f"{business['fixed_top3'] * 100:.4f}% | "
                f"{business['fixed_top10'] * 100:.4f}% |"
            )
    # Stock-ranking business facts remain separate from loss completion.
    lines.extend(
        [
            "",
            "## Business ranking at validation-loss best",
            "",
            "| Trial | Scale | Dynamic TopN | Top1 | Top3 | Top10 |",
            "| ---: | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    # Report business values from the validation-loss-best epoch for each trial.
    for row in result["trials"]:
        # Skip an empty business row when no complete epoch exists.
        if row["training_report"] is None:
            continue
        # Business values share the exact epoch used by minimum validation loss.
        business = row["training_report"]["business_at_validation_best"]
        # Four decimal percentage places prevent display rounding from hiding movement.
        lines.append(
            f"| {row['number']} | {row['business_context']['scale']} | "
            f"{business['dynamic_topn'] * 100:.4f}% | "
            f"{business['fixed_top1'] * 100:.4f}% | "
            f"{business['fixed_top3'] * 100:.4f}% | "
            f"{business['fixed_top10'] * 100:.4f}% |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    """Read a ledger and write JSON and Markdown analysis artifacts.

    Returns:
        Zero after both analysis artifacts are written successfully.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args()
    result = analyze(json.loads(args.ledger.read_text(encoding="utf-8")))
    args.output_directory.mkdir(parents=True, exist_ok=False)
    (args.output_directory / "analysis.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (args.output_directory / "analysis.md").write_text(
        markdown(result), encoding="utf-8", newline="\n"
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    # Return the analyzer status unchanged to the invoking terminal.
    raise SystemExit(main())
