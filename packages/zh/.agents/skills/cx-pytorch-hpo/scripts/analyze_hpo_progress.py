#!/usr/bin/env python3
"""在不读取严格测试的前提下验证并汇总持久化自动调参台账。"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

# 二十一次验证损失严格改进是训练取得模型证据资格的固定下界。
MIN_EVIDENCE_IMPROVEMENTS = 21


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


def _epoch_reports(
    trial: dict,
    number: int,
    completed_epochs: int,
    patience: int,
) -> list[dict]:
    """验证并规范化一个参数试验的逐轮训练与业务报告。

    Args:
        trial: 当前参数试验台账对象。
        number: 参数试验序号。
        completed_epochs: 已完成的完整训练轮数。
        patience: study 冻结的早停忍耐轮数。

    Returns:
        按一基轮次连续排列的规范化逐轮报告。
    """
    # 逐轮报告是完成训练诊断所需的唯一轨迹来源。
    reports = trial.get("epoch_reports")
    # 台账必须显式保存每个完整训练轮，不能只保留最终状态。
    if not isinstance(reports, list):
        raise ValueError(f"trial {number} epoch_reports must be an array")
    # 已完成轮数与报告数量必须一致，避免缺轮仍生成完成结论。
    if len(reports) != completed_epochs:
        raise ValueError(f"trial {number} epoch_reports must match completed_epochs")
    # 规范化结果只保留统一报告合同中的当前字段。
    normalized = []
    # 验证损失累计改进次数必须随训练单调不减。
    previous_improvements = 0
    # 一基轮次连续性使平台开始轮次可以直接解释。
    for expected_epoch, report in enumerate(reports, start=1):
        # 每个轮次报告必须是具名字段对象。
        if not isinstance(report, dict):
            raise ValueError(f"trial {number} epoch report must be an object")
        # 实际轮次必须与完整报告顺序一致。
        epoch = int(report.get("epoch", 0))
        if epoch != expected_epoch:
            raise ValueError(f"trial {number} epoch reports must be contiguous")
        # 累计严格改进次数独立于早停选择目标计数。
        improvements = int(report.get("validation_loss_improvement_count", -1))
        if improvements < previous_improvements:
            raise ValueError(
                f"trial {number} validation loss improvement count must not decrease"
            )
        # 当前值成为下一轮累计次数的下界。
        previous_improvements = improvements
        # 早停计数必须处于零到冻结忍耐之间。
        early_stopping_count = int(report.get("early_stopping_count", -1))
        if early_stopping_count < 0 or early_stopping_count > patience:
            raise ValueError(f"trial {number} early stopping count is out of range")
        # 股票业务报告必须同时提供动态与固定前排口径。
        business = _mapping(report, "business_report")
        # 当前轮次的训练、验证和业务事实形成一个不可变分析行。
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
    # 返回值供损失完善度、平台和 Markdown 报告共同复用。
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
    """计算理论损失完善度、平台轮次和人工拟合结论字段。

    Args:
        trial: 当前参数试验台账对象。
        number: 参数试验序号。
        state: 规范化参数试验状态。
        reports: 已验证的逐轮训练与业务报告。
        reference: 无信息理论基准损失。
        floor: 可用时的理论损失下界。
        precision: 判断有意义损失变化的冻结精度。
        plateau_window: 判定平台所需的连续完整轮数。

    Returns:
        没有完整训练轮时返回空值，否则返回统一完成报告。
    """
    # 没有完整训练轮时不存在损失完善度或平台证据。
    if not reports:
        return None
    # 最小验证损失轮是完成报告的固定比较点。
    best = min(reports, key=lambda row: row["validation_loss"])
    # 最终完整训练轮保留停止时真实状态。
    final = reports[-1]
    # 证据资格只由末轮累计验证损失严格改进次数确定。
    evidence_eligible = (
        final["validation_loss_improvement_count"] >= MIN_EVIDENCE_IMPROVEMENTS
    )
    # 资格原因进入机器报告，使无效训练不能被局部业务峰值覆盖。
    eligibility_reason = (
        "validation_loss_improvements_reached_21"
        if evidence_eligible
        else "validation_loss_improvements_below_21"
    )
    # 冻结精度相对的运行最佳用于识别有意义改善。
    meaningful_best = reports[0]["validation_loss"]
    # 第一轮建立初始可比损失基线。
    last_meaningful_epoch = reports[0]["epoch"]
    # 后续轮次只在超过冻结精度时刷新平台起点。
    for report in reports[1:]:
        # 累积超过精度的小变化最终仍可形成一次有意义改善。
        if report["validation_loss"] < meaningful_best - precision:
            # 新的有意义最佳成为后续平台比较基线。
            meaningful_best = report["validation_loss"]
            # 当前轮次是最近一次有意义验证改善轮。
            last_meaningful_epoch = report["epoch"]
    # 只有终止前完整覆盖观察窗口时才声明平台开始轮次。
    plateau_start = (
        last_meaningful_epoch + 1
        if final["epoch"] - last_meaningful_epoch >= plateau_window
        else None
    )
    # 参数试验必须明确训练与验证损失是否允许相减。
    comparable = trial.get("losses_comparable")
    if not isinstance(comparable, bool):
        raise ValueError(f"trial {number} losses_comparable must be boolean")
    # 不可比时保留项目给出的具体口径原因。
    incomparable_reason = None
    if not comparable:
        # 明确原因阻止分析器生成误导性泛化差距。
        incomparable_reason = _text(trial, "loss_incomparability_reason")
    # 只有取得证据资格的已结束参数试验才允许人工拟合判断。
    fit_assessment = trial.get("fit_assessment")
    # 完成或剪枝且证据有效时必须冻结人工结论。
    if state in ("complete", "pruned") and evidence_eligible:
        # 固定值域保持机器可读，同时不让工具自动替代人工判断。
        if fit_assessment not in (
            "overfitting",
            "underfitting",
            "healthy_fit",
            "insufficient_evidence",
        ):
            raise ValueError(f"trial {number} fit_assessment is invalid")
    # 未取得资格的终态只允许明确的无效证据状态，禁止方向结论。
    elif state in ("complete", "pruned"):
        if fit_assessment not in (None, "invalid_evidence"):
            raise ValueError(f"trial {number} invalid evidence cannot assess fit")
        # 分析结果统一使用一个机器值表达无效训练。
        fit_assessment = "invalid_evidence"
    # 运行中和失败参数试验可以尚未形成人工判断。
    elif fit_assessment is not None:
        # 已提供的非终态人工判断仍必须使用相同值域。
        fit_assessment = _text(trial, "fit_assessment")
    # 人工判断必须列出所依据的具体轮次。
    evidence_epochs = trial.get("fit_evidence_epochs", [])
    if not isinstance(evidence_epochs, list):
        raise ValueError(f"trial {number} fit_evidence_epochs must be an array")
    # 证据轮次转换为稳定的一基整数列表。
    evidence_epochs = [int(epoch) for epoch in evidence_epochs]
    # 无效训练不得保留貌似支持方向判断的人工证据轮次。
    if not evidence_eligible and evidence_epochs:
        raise ValueError(f"trial {number} invalid evidence cannot have fit epochs")
    # 任何证据都必须落在当前参数试验的真实训练范围内。
    if any(epoch < 1 or epoch > final["epoch"] for epoch in evidence_epochs):
        raise ValueError(f"trial {number} fit evidence epoch is out of range")
    # 相对理论基准的绝对改善直接使用最小验证损失。
    absolute_improvement = reference - best["validation_loss"]
    # 理论基准为零时相对改善百分比没有定义。
    relative_improvement = (
        None if reference == 0 else absolute_improvement / abs(reference) * 100
    )
    # 只有有效理论下界才能计算可改善损失完成率。
    completion = (
        None
        if floor is None or reference <= floor
        else absolute_improvement / (reference - floor) * 100
    )
    # 同口径损失才生成训练与验证差值。
    best_gap = best["validation_loss"] - best["train_loss"] if comparable else None
    # 最终差值只用于人工拟合诊断，不参与选择。
    final_gap = final["validation_loss"] - final["train_loss"] if comparable else None
    # 完成报告同时保存理论、训练、验证、业务和人工证据。
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
        "evidence_eligible": evidence_eligible,
        "eligibility_reason": eligibility_reason,
        "fit_assessment": fit_assessment,
        "fit_evidence_epochs": evidence_epochs,
        "business_at_validation_best": best["business_report"],
        "business_at_final": final["business_report"],
        "validation_loss_improvement_count": final["validation_loss_improvement_count"],
        "early_stopping_count": final["early_stopping_count"],
    }


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

    # 正式标签基线是新方向训练前的唯一项目级业务起点。
    formal_baseline = _mapping(payload, "formal_baseline")
    # 标签和冻结产物引用共同证明基线来自只读正式事实。
    formal_baseline = {
        "tag": _text(formal_baseline, "tag"),
        "artifact_reference": _text(formal_baseline, "artifact_reference"),
    }
    # 研究笔记路径证明新的方向在训练前已经完成问题导向研究。
    research_note = _text(payload, "research_note")

    # 调参工具必须明确记录采样器、剪枝器和可恢复存储。
    optimizer = _mapping(payload, "optimizer")
    for field in ("tool", "sampler", "pruner", "storage"):
        _text(optimizer, field)
    # 采样器不得从无效训练学习下一配置方向。
    if optimizer.get("sampler_uses_only_evidence_eligible_trials") is not True:
        raise ValueError("sampler must use only evidence-eligible trials")
    # 模型效果剪枝只能使用已经取得证据资格的参数试验。
    if optimizer.get("pruner_uses_only_evidence_eligible_trials") is not True:
        raise ValueError("pruner must use only evidence-eligible trials")
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
    # 资源合同显式冻结模型效果剪枝可以开始的证据资格下界。
    if (
        int(resource.get("minimum_evidence_validation_loss_improvements", 0))
        != MIN_EVIDENCE_IMPROVEMENTS
    ):
        raise ValueError("minimum evidence improvements must equal 21")

    # 唯一验证业务目标决定参数试验方向和当前最优。
    objective = _mapping(payload, "objective")
    metric = _text(objective, "business_metric")
    direction = _text(objective, "direction")
    if direction not in ("maximize", "minimize"):
        raise ValueError("objective.direction must be maximize or minimize")

    # 无信息理论基准是训练完善度的固定起点，不能来自任一参数试验。
    loss_reference = _number(payload.get("loss_reference"), "loss_reference")
    # 理论下界允许显式为空，表示当前损失没有可证明的完善度分母。
    loss_floor_value = payload.get("loss_floor")
    # 有限理论下界保留为统一浮点数供全部参数试验复用。
    loss_floor = (
        None if loss_floor_value is None else _number(loss_floor_value, "loss_floor")
    )
    # 损失报告精度决定哪些变化可以解释为有意义改善。
    loss_report_precision = _number(
        payload.get("loss_report_precision"), "loss_report_precision"
    )
    if loss_report_precision <= 0:
        raise ValueError("loss_report_precision must be positive")
    # 平台观察窗口必须包含至少一个完整训练轮。
    plateau_window = int(payload.get("plateau_window", 0))
    if plateau_window <= 0:
        raise ValueError("plateau_window must be positive")

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
        # 完整逐轮训练与业务报告支撑理论完善度和平台诊断。
        epoch_reports = _epoch_reports(
            trial,
            number,
            epochs,
            int(resource["early_stopping_patience"]),
        )
        # 股票排名刻度和动态 N 口径必须与数值一同冻结。
        business_context = _mapping(trial, "business_context")
        # 四个文本字段使跨刻度 TopN 比较可以复核。
        business_context = {
            field: _text(business_context, field)
            for field in (
                "scale",
                "opportunity_definition",
                "daily_n_source",
                "aggregation",
            )
        }
        # 统一完成报告由逐轮轨迹和 study 理论损失合同计算。
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
        # 没有完整训练轮时证据资格固定为假并说明缺少轨迹。
        evidence_eligible = (
            False if loss_report is None else loss_report["evidence_eligible"]
        )
        # 模型效果剪枝只能发生在当前参数试验越过证据门禁以后。
        if state == "pruned" and not evidence_eligible:
            raise ValueError(
                f"trial {number} pruning requires 21 validation loss improvements"
            )
        # 每个分析行都携带资格原因，避免调用者只看目标值。
        eligibility_reason = (
            "no_complete_epoch"
            if loss_report is None
            else loss_report["eligibility_reason"]
        )
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
            "evidence_eligible": evidence_eligible,
            "eligibility_reason": eligibility_reason,
            "training_report": loss_report,
            "duration_seconds": trial.get("duration_seconds"),
            "gpu_peak_reserved_bytes": trial.get("gpu_peak_reserved_bytes"),
            "failure": trial.get("failure"),
            "artifacts": trial.get("artifacts", {}),
        }
        rows.append(row)
        # 当前最优候选集合只接收已经取得证据资格的完整参数试验。
        if state == "complete" and evidence_eligible:
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
    # 参数重要性调用方必须声明只使用有效证据参数试验。
    if (
        payload.get("parameter_importance_uses_only_evidence_eligible_trials")
        is not True
    ):
        raise ValueError("parameter importance must use only evidence-eligible trials")
    # 没有任何有效完整试验时不得伪造参数重要性。
    if not completed and importance:
        raise ValueError("parameter importance requires evidence-eligible trials")
    # 资格计数把有效、终态无效和仍在运行等待的状态分开。
    eligibility_counts = {
        "eligible": sum(row["evidence_eligible"] for row in rows),
        "invalid": sum(
            row["state"] in ("complete", "pruned", "failed")
            and not row["evidence_eligible"]
            for row in rows
        ),
        "pending": sum(
            row["state"] in ("running", "waiting") and not row["evidence_eligible"]
            for row in rows
        ),
    }
    # 返回值同时保留资源策略、失败原因、参数重要性和严格测试隔离事实。
    return {
        "schema_version": 4,
        "data_scope_id": scope["id"],
        "data_scope_start_date": scope["start_date"],
        "formal_baseline": formal_baseline,
        "research_note": research_note,
        "business_metric": metric,
        "direction": direction,
        "optimizer": {
            field: optimizer[field]
            for field in (
                "tool",
                "sampler",
                "pruner",
                "storage",
                "sampler_uses_only_evidence_eligible_trials",
                "pruner_uses_only_evidence_eligible_trials",
            )
        },
        "resource_policy": resource,
        "loss_reference": loss_reference,
        "loss_floor": loss_floor,
        "loss_report_precision": loss_report_precision,
        "plateau_window": plateau_window,
        "counts": {"total": len(rows), **counts},
        "eligibility_counts": eligibility_counts,
        "best_trial": best,
        "parameter_importance": importance,
        "failures": [row for row in rows if row["failure"]],
        "trials": rows,
        # 选择合同明确只有冻结目标对应的参数试验值参与选参。
        "used_for_selection": {
            "trial_value": True,
            "evidence_eligibility_gate": True,
            "objective_metric": metric,
            "epoch_reports": False,
            "training_report": False,
            "strict_test": False,
        },
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
        "# 自动调参进度分析",
        "",
        f"- 数据范围：{result['data_scope_id']}，起始日 {result['data_scope_start_date']}，覆盖全部合格实体。",
        f"- 正式基线：{result['formal_baseline']['tag']}；冻结产物={result['formal_baseline']['artifact_reference']}。",
        f"- 训练前研究：{result['research_note']}。",
        f"- 选择目标：{result['business_metric']}（{result['direction']}）。",
        f"- 工具：{result['optimizer']['tool']}；采样器={result['optimizer']['sampler']}；剪枝器={result['optimizer']['pruner']}。",
        f"- 损失基准：{result['loss_reference']:.8f}；理论下界={result['loss_floor']}；报告精度={result['loss_report_precision']}；平台窗口={result['plateau_window']}。",
        f"- 参数试验：完成={result['counts']['complete']}，剪枝={result['counts']['pruned']}，失败={result['counts']['failed']}，运行中={result['counts']['running']}。",
        f"- 证据资格：有效={result['eligibility_counts']['eligible']}，无效={result['eligibility_counts']['invalid']}，等待={result['eligibility_counts']['pending']}；门禁为至少二十一次验证损失严格改进。",
        f"- 当前选择结果：{best_text}。",
        f"- 选择合同：只使用取得证据资格参数试验的 trial.value 对应的 {result['used_for_selection']['objective_metric']}；无效训练、逐轮报告、训练诊断和严格测试不参与选参。",
        "",
        "## 参数重要性",
        "",
    ]
    lines.extend(
        [
            f"- {name}: {value:.6f}"
            for name, value in result["parameter_importance"].items()
        ]
        or ["- 完成参数试验不足，暂不可用。"]
    )
    lines.extend(
        [
            "",
            "## 参数试验摘要",
            "",
            "| 参数试验 | 状态 | 证据资格 | 资格原因 | 目标值 | 完成轮数 | 最优轮次 | 该轮训练损失 | 最小验证损失 | 理论基准绝对改善 | 理论基准相对改善 | 可改善损失完成率 | 平台开始轮次 | 拟合判断 | 验证损失改进次数 | 早停计数 | 失败原因 |",
            "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |",
        ]
    )
    for row in result["trials"]:
        # 未完成首轮的参数试验没有可展示的训练完成报告。
        report = row["training_report"]
        # 统一空值避免 Markdown 把不可用百分比误写成零。
        best_validation = (
            "" if report is None else f"{report['validation_loss_best']:.8f}"
        )
        # 最优轮次把训练损失、验证损失和业务报告绑定到同一检查点。
        best_epoch = "" if report is None else str(report["validation_best_epoch"])
        # 同轮训练损失用于人工核对训练与验证是否开始背离。
        train_at_best = (
            "" if report is None else f"{report['train_loss_at_validation_best']:.8f}"
        )
        # 绝对改善直接回答实际损失比无信息理论基准降低多少。
        absolute = "" if report is None else f"{report['absolute_improvement']:.8f}"
        # 理论基准为零时相对改善不可用，必须保持为空。
        relative = (
            ""
            if report is None or report["relative_improvement_percent"] is None
            else f"{report['relative_improvement_percent']:.4f}%"
        )
        # 可改善损失完成率保留百分号以区别原始损失。
        completion = (
            ""
            if report is None or report["reducible_loss_completion_percent"] is None
            else f"{report['reducible_loss_completion_percent']:.4f}%"
        )
        # 平台不足一个完整窗口时不写虚构轮次。
        plateau = (
            ""
            if report is None or report["plateau_start_epoch"] is None
            else str(report["plateau_start_epoch"])
        )
        # 人工拟合结论只读取台账冻结值，不由渲染器推断。
        fit = (
            ""
            if report is None or report["fit_assessment"] is None
            else report["fit_assessment"]
        )
        # 末轮验证损失改进次数用于回顾训练畅通性。
        improvements = (
            "" if report is None else str(report["validation_loss_improvement_count"])
        )
        # 末轮早停计数与改进次数保持独立列。
        early_stop = "" if report is None else str(report["early_stopping_count"])
        value = "" if row["value"] is None else f"{row['value']:.8f}"
        lines.append(
            f"| {row['number']} | {row['state']} | {row['evidence_eligible']} | {row['eligibility_reason']} | {value} | {row['completed_epochs']} | {best_epoch} | {train_at_best} | {best_validation} | {absolute} | {relative} | {completion} | {plateau} | {fit} | {improvements} | {early_stop} | {row['failure'] or ''} |"
        )
    # 逐轮表格完整呈现用户要求的训练状态和股票业务报告。
    lines.extend(
        [
            "",
            "## 逐轮训练与业务报告",
            "",
            "| 参数试验 | 轮次 | 训练损失 | 验证损失 | 验证损失改进次数 | 早停计数 | 动态 TopN | 固定 Top1 | 固定 Top3 | 固定 Top10 |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    # 每个参数试验按真实完整轮次依次展开，运行中参数试验也可以持续查看。
    for row in result["trials"]:
        # 最大轮数与早停忍耐来自冻结资源合同，禁止由单个参数试验改写。
        max_epochs = result["resource_policy"]["max_resource"]
        # 早停分母固定为 study 忍耐轮数。
        patience = result["resource_policy"]["early_stopping_patience"]
        # 每个完整训练轮同时展示损失、计数与四个业务口径。
        for report in row["epoch_reports"]:
            # 当前轮股票业务事实与同一轮损失绑定。
            business = report["business_report"]
            # 百分比保留四位，避免显示精度掩盖真实变化。
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
    # 股票排名业务值单列，避免与损失完成百分比混淆。
    lines.extend(
        [
            "",
            "## 最小验证损失轮的业务排名",
            "",
            "| 参数试验 | 刻度 | 动态 TopN | 固定 Top1 | 固定 Top3 | 固定 Top10 |",
            "| ---: | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    # 每个已有完整训练轮的参数试验报告同一验证损失最佳轮业务值。
    for row in result["trials"]:
        # 没有训练报告时跳过业务空行。
        if row["training_report"] is None:
            continue
        # 业务值来自与最小验证损失相同的训练轮。
        business = row["training_report"]["business_at_validation_best"]
        # 百分比统一保留四位，避免两位显示掩盖真实变化。
        lines.append(
            f"| {row['number']} | {row['business_context']['scale']} | "
            f"{business['dynamic_topn'] * 100:.4f}% | "
            f"{business['fixed_top1'] * 100:.4f}% | "
            f"{business['fixed_top3'] * 100:.4f}% | "
            f"{business['fixed_top10'] * 100:.4f}% |"
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
