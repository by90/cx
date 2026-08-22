#!/usr/bin/env python3
"""在不读取严格测试的前提下验证并汇总持久化自动调参台账。"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def _mapping(payload: dict, field: str) -> dict:
    """读取一个必需的对象字段。

    Args:
        payload: 当前父级字段字典。
        field: 必须存在且值为对象的字段名。

    Returns:
        字段对应的对象字典。
    """
    value = payload.get(field)
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    return value


def _text(payload: dict, field: str) -> str:
    """读取一个必需的非空文本字段。

    Args:
        payload: 当前父级字段字典。
        field: 必须存在且值为非空文本的字段名。

    Returns:
        去除首尾空白后的文本。
    """
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be non-empty text")
    return value.strip()


def _number(value: Any, field: str) -> float:
    """把一个必需的有限数值转换为浮点数。

    Args:
        value: 台账提供的数值。
        field: 发生错误时使用的字段说明。

    Returns:
        有限浮点数。
    """
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")
    return result


def analyze(payload: dict) -> dict:
    """验证自动调参范围、工具合同、停止规则、试验状态和当前最优。

    Args:
        payload: 持久化自动调参台账根对象。

    Returns:
        可直接写入分析文件的规范化结果。
    """
    # 根对象、注册制范围和全部合格实体是股票调参的固定前提。
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

    # 调参工具必须明确记录采样器、剪枝器和可恢复存储。
    optimizer = _mapping(payload, "optimizer")
    for field in ("tool", "sampler", "pruner", "storage"):
        _text(optimizer, field)
    resource = _mapping(payload, "resource_policy")
    if _number(resource.get("max_wallclock_seconds"), "max_wallclock_seconds") <= 0:
        raise ValueError("max_wallclock_seconds must be positive")
    # 正式调参与普通候选统一以一百二十轮作为单个参数试验的训练上限。
    max_epochs = int(resource.get("max_resource", 0))
    if max_epochs != 120:
        raise ValueError("max_resource must equal 120 epochs")
    # 框架训练器必须启用自身早停，剪枝器只负责更早淘汰相对劣势试验。
    if resource.get("framework_early_stopping") is not True:
        raise ValueError("automatic HPO must enable framework early stopping")
    # 连续九轮没有任何验证目标提高时停止当前参数试验。
    if int(resource.get("early_stopping_patience", 0)) != 9:
        raise ValueError("early stopping patience must equal 9 epochs")
    # 零提高阈值保证任意严格提高都会立即重置九轮忍耐计数。
    if (
        _number(resource.get("early_stopping_min_delta"), "early_stopping_min_delta")
        != 0
    ):
        raise ValueError("early stopping min_delta must equal zero")

    # 唯一验证业务目标决定参数试验方向和当前最优。
    objective = _mapping(payload, "objective")
    metric = _text(objective, "business_metric")
    direction = _text(objective, "direction")
    if direction not in ("maximize", "minimize"):
        raise ValueError("objective.direction must be maximize or minimize")

    # 参数试验列表保留完整、剪枝、失败、运行中和等待状态。
    trials = payload.get("trials")
    if not isinstance(trials, list):
        raise ValueError("trials must be an array")
    allowed = {"complete", "pruned", "failed", "running", "waiting"}
    numbers: set[int] = set()
    rows = []
    completed = []
    # 每个参数试验按统一字段合同转换为规范化分析行。
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
        # 剪枝、失败或正常完成都不能记录超过统一训练上限的实际轮数。
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

    # 只有完整参数试验参与当前最优选择，剪枝和失败试验仅供审计。
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
    # 返回值同时保留资源策略、失败原因、参数重要性和严格测试隔离事实。
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
    """渲染紧凑的自动调参审计报告。

    Args:
        result: `analyze` 返回的规范化分析结果。

    Returns:
        以换行结尾的 Markdown 报告正文。
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
    """读取台账并写出 JSON 与 Markdown 分析文件。

    Returns:
        分析文件成功写出时返回零。
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
    # 命令入口把分析结果状态原样交给调用终端。
    raise SystemExit(main())
