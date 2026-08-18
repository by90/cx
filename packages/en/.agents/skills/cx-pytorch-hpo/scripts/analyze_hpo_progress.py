#!/usr/bin/env python3
"""Analyze an evidence-driven HPO ledger without reading strict-test metrics."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def _number(value: Any, field: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{field} must be finite")
    return number


def _mapping(payload: dict, field: str) -> dict:
    value = payload.get(field)
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    return value


def _text(payload: dict, field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be non-empty text")
    return value.strip()


def _business_delta(current: float, baseline: float, higher_is_better: bool) -> float:
    return current - baseline if higher_is_better else baseline - current


def analyze(payload: dict) -> dict:
    """Validate one registration-regime ledger and return its next-run decision."""

    if not isinstance(payload, dict):
        raise ValueError("ledger must be an object")

    scope = _mapping(payload, "data_scope")
    if scope.get("kind") != "registration_regime":
        raise ValueError("data scope must be the registration regime")
    _text(scope, "id")
    _text(scope, "start_date")
    if scope.get("all_eligible_entities") is not True:
        raise ValueError("registration-regime tuning must use all eligible entities")
    if payload.get("strict_test_used_for_selection") is not False:
        raise ValueError("strict test must not participate in candidate selection")

    training_contract = _mapping(payload, "training_contract")
    if (
        int(training_contract.get("max_epochs", 0)) != 1000
        or int(training_contract.get("early_stopping_patience", -1)) != 20
    ):
        raise ValueError(
            "training contract must keep max_epochs=1000 and "
            "early_stopping_patience=20"
        )

    objective = _mapping(payload, "objective")
    business_metric_name = _text(objective, "business_metric")
    higher_is_better = objective.get("higher_is_better")
    if not isinstance(higher_is_better, bool):
        raise ValueError("objective.higher_is_better must be boolean")
    minimum_delta = _number(
        objective.get("minimum_business_delta"), "minimum_business_delta"
    )
    if minimum_delta < 0:
        raise ValueError("minimum_business_delta must be non-negative")

    trials = payload.get("trials")
    if not isinstance(trials, list) or not trials:
        raise ValueError("trials must contain at least the frozen baseline")
    if any(not isinstance(trial, dict) for trial in trials):
        raise ValueError("every trial must be an object")

    names = [_text(trial, "name") for trial in trials]
    if len(set(names)) != len(names):
        raise ValueError("trial names must be unique")
    baseline_name = _text(payload, "baseline_trial")
    if baseline_name not in names:
        raise ValueError("baseline_trial must name a recorded trial")
    baseline_index = names.index(baseline_name)
    baseline = trials[baseline_index]
    if baseline.get("status") != "completed":
        raise ValueError("the frozen baseline must be completed")
    baseline_business_group = _text(baseline, "business_comparison_group")
    baseline_loss_group = _text(baseline, "loss_comparison_group")
    baseline_business = _number(
        baseline.get("business_metric"), "baseline.business_metric"
    )
    baseline_loss = _number(
        baseline.get("best_validation_loss"), "baseline.best_validation_loss"
    )

    flags: list[str] = []
    completed: list[dict] = []
    for index, trial in enumerate(trials):
        if (
            int(trial.get("planned_epochs", 0)) != 1000
            or int(trial.get("max_epochs", 0)) != 1000
            or int(trial.get("early_stopping_patience", -1)) != 20
        ):
            raise ValueError(
                "training contract must keep max_epochs=1000 and "
                "early_stopping_patience=20 for every trial"
            )
        if trial.get("strict_test_used_for_selection") is True:
            raise ValueError("strict test must not participate in candidate selection")
        if trial.get("status") != "completed":
            continue

        business = _number(
            trial.get("business_metric"), f"{names[index]}.business_metric"
        )
        loss = _number(
            trial.get("best_validation_loss"),
            f"{names[index]}.best_validation_loss",
        )
        business_group = _text(trial, "business_comparison_group")
        loss_group = _text(trial, "loss_comparison_group")
        business_comparable = business_group == baseline_business_group
        loss_comparable = loss_group == baseline_loss_group
        business_delta = (
            _business_delta(business, baseline_business, higher_is_better)
            if business_comparable
            else None
        )
        if index != baseline_index:
            changed_dimension = trial.get("changed_dimension")
            if not isinstance(changed_dimension, str) or not changed_dimension.strip():
                if "multiple_or_missing_changes" not in flags:
                    flags.append("multiple_or_missing_changes")
        if not business_comparable and "incomparable_business_group" not in flags:
            flags.append("incomparable_business_group")
        if trial.get("resource_gate_passed") is not True:
            if "resource_gate_failed" not in flags:
                flags.append("resource_gate_failed")

        completed.append(
            {
                "name": names[index],
                "business_comparison_group": business_group,
                "loss_comparison_group": loss_group,
                "business_comparable": business_comparable,
                "validation_loss_comparable": loss_comparable,
                "business_metric": business,
                "business_delta_from_baseline": business_delta,
                "best_validation_loss": loss,
                "validation_loss_delta_from_baseline": (
                    loss - baseline_loss if loss_comparable else None
                ),
                "completed_epochs": int(trial.get("completed_epochs", 0)),
                "planned_epochs": int(trial.get("planned_epochs", 0)),
                "best_epoch": int(trial.get("best_epoch", 0)),
                "resource_gate_passed": trial.get("resource_gate_passed") is True,
            }
        )

    comparable_after_baseline = [
        row
        for row in completed
        if row["name"] != baseline_name and row["business_comparable"]
    ]
    regression_streak = 0
    for row in reversed(comparable_after_baseline):
        if row["business_delta_from_baseline"] <= -minimum_delta:
            regression_streak += 1
        else:
            break

    conflicts = [
        row["name"]
        for row in comparable_after_baseline
        if row["business_delta_from_baseline"] <= -minimum_delta
        and row["validation_loss_comparable"]
        and row["validation_loss_delta_from_baseline"] < 0
    ]
    if conflicts:
        flags.append("objective_conflict")
    if regression_streak >= 2:
        flags.append("business_regression_streak")

    latest = completed[-1]
    if (
        latest["completed_epochs"] < latest["planned_epochs"]
        and latest["best_epoch"] <= 0
        and "no_effective_improvement" not in flags
    ):
        flags.append("no_effective_improvement")

    proposed_next = payload.get("proposed_next")
    next_change = None
    next_hypothesis = None
    if isinstance(proposed_next, dict):
        change = proposed_next.get("single_change")
        hypothesis = proposed_next.get("hypothesis")
        if isinstance(change, str) and change.strip():
            next_change = change.strip()
        if isinstance(hypothesis, str) and hypothesis.strip():
            next_hypothesis = hypothesis.strip()
    if next_change is None or next_hypothesis is None:
        flags.append("missing_next_hypothesis")

    blocking = {
        "business_regression_streak",
        "incomparable_business_group",
        "multiple_or_missing_changes",
        "no_effective_improvement",
        "objective_conflict",
        "resource_gate_failed",
        "missing_next_hypothesis",
    }
    decision = "stop" if any(flag in blocking for flag in flags) else "continue"
    reasons = {
        "business_regression_streak": "business metric regressed in two consecutive comparable candidates",
        "incomparable_business_group": "different label, split, or business-evaluation contracts cannot be ranked together",
        "multiple_or_missing_changes": "each candidate must declare exactly one changed dimension",
        "no_effective_improvement": "the latest run stopped without an effective validation improvement",
        "objective_conflict": "validation loss improved while the primary business metric regressed",
        "resource_gate_failed": "a completed trial exceeded its declared resource gate",
        "missing_next_hypothesis": "continuation needs one falsifiable hypothesis and one change",
    }
    return {
        "schema_version": 1,
        "data_scope_id": scope["id"],
        "data_scope_start_date": scope["start_date"],
        "training_contract": {
            "max_epochs": 1000,
            "early_stopping_patience": 20,
        },
        "business_metric": business_metric_name,
        "baseline_trial": baseline_name,
        "latest_trial": latest["name"],
        "business_regression_streak": regression_streak,
        "objective_conflict_trials": conflicts,
        "flags": flags,
        "decision": decision,
        "decision_reasons": [reasons[flag] for flag in flags if flag in reasons],
        "next_hypothesis": next_hypothesis if decision == "continue" else None,
        "next_change": next_change if decision == "continue" else None,
        "trials": completed,
        "strict_test_used_for_selection": False,
    }


def markdown(result: dict) -> str:
    """Render a compact audit report."""

    lines = [
        "# HPO progress analysis",
        "",
        f"- Data scope: {result['data_scope_id']} from {result['data_scope_start_date']}; all eligible entities.",
        f"- Primary business metric: {result['business_metric']}.",
        f"- Frozen baseline: {result['baseline_trial']}.",
        f"- Latest completed trial: {result['latest_trial']}.",
        f"- Decision: **{result['decision']}**.",
        f"- Consecutive business regressions: {result['business_regression_streak']}.",
        "- Strict test used for selection: false.",
        "",
        "## Signals",
        "",
    ]
    lines.extend([f"- {flag}" for flag in result["flags"]] or ["- No blocking signal."])
    if result["decision"] == "continue":
        lines.extend(
            [
                "",
                "## One permitted next change",
                "",
                f"- Hypothesis: {result['next_hypothesis']}",
                f"- Change: {result['next_change']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Comparable trial trail",
            "",
            "| Trial | Business | Delta vs baseline | Best validation loss | Loss delta | Epochs | Best epoch | Resource gate |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in result["trials"]:
        delta = row["business_delta_from_baseline"]
        delta_text = "not comparable" if delta is None else f"{delta:.6f}"
        loss_delta = row["validation_loss_delta_from_baseline"]
        loss_delta_text = (
            "not comparable" if loss_delta is None else f"{loss_delta:.6f}"
        )
        lines.append(
            f"| {row['name']} | {row['business_metric']:.6f} | {delta_text} | "
            f"{row['best_validation_loss']:.6f} | "
            f"{loss_delta_text} | "
            f"{row['completed_epochs']}/{row['planned_epochs']} | "
            f"{row['best_epoch']} | {row['resource_gate_passed']} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.ledger.read_text(encoding="utf-8"))
    result = analyze(payload)
    args.output_directory.mkdir(parents=True, exist_ok=False)
    (args.output_directory / "analysis.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (args.output_directory / "analysis.md").write_text(
        markdown(result),
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
