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
            "validation_loss_best": trial.get("validation_loss_best"),
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
        "schema_version": 2,
        "data_scope_id": scope["id"],
        "data_scope_start_date": scope["start_date"],
        "business_metric": metric,
        "direction": direction,
        "optimizer": {
            field: optimizer[field]
            for field in ("tool", "sampler", "pruner", "storage")
        },
        "resource_policy": resource,
        "counts": {"total": len(rows), **counts},
        "best_trial": best,
        "parameter_importance": importance,
        "failures": [row for row in rows if row["failure"]],
        "trials": rows,
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
        f"- Trials: complete={result['counts']['complete']}, pruned={result['counts']['pruned']}, failed={result['counts']['failed']}, running={result['counts']['running']}.",
        f"- Incumbent: {best_text}.",
        "- Strict test used for selection: false.",
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
            "| Trial | State | Value | Epochs | Failure |",
            "| ---: | --- | ---: | ---: | --- |",
        ]
    )
    for row in result["trials"]:
        value = "" if row["value"] is None else f"{row['value']:.8f}"
        lines.append(
            f"| {row['number']} | {row['state']} | {value} | {row['completed_epochs']} | {row['failure'] or ''} |"
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
