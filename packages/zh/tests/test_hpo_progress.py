"""自动调参轨迹分析器的注册制范围、停止规则和试验状态测试。"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).parents[1]
    / ".agents"
    / "skills"
    / "cx-pytorch-hpo"
    / "scripts"
    / "analyze_hpo_progress.py"
)
SPEC = importlib.util.spec_from_file_location("cx_hpo_progress", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {SCRIPT}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def trial(number: int, state: str, value=None, epochs: int = 0, failure=None) -> dict:
    """构造一个最小参数试验事实。

    Args:
        number: 参数试验序号。
        state: 参数试验当前状态。
        value: 已完成参数试验的验证业务指标。
        epochs: 实际完成训练轮数。
        failure: 参数试验失败原因。

    Returns:
        可交给轨迹分析器的参数试验字典。
    """
    return {
        "number": number,
        "state": state,
        "value": value,
        "params": {"window_size": 4 + number * 4, "learning_rate": 0.0001},
        "intermediate_values": {"1": 0.10 + number / 100},
        "completed_epochs": epochs,
        "business_best_epoch": epochs,
        "validation_loss_best": 1.2,
        "failure": failure,
    }


def payload(*trials: dict, strict_test_used: bool = False) -> dict:
    """构造启用统一一百二十轮九轮早停的调参台账。

    Args:
        *trials: 纳入当前调参研究的参数试验事实。
        strict_test_used: 严格测试是否参与了参数选择。

    Returns:
        包含数据范围、工具、训练规则和参数试验的台账字典。
    """
    return {
        "data_scope": {
            "id": "chinext_registration_20200824",
            "kind": "registration_regime",
            "start_date": "2020-08-24",
            "all_eligible_entities": True,
        },
        "optimizer": {
            "tool": "optuna",
            "sampler": "multivariate_tpe",
            "pruner": "hyperband",
            "storage": "journal",
        },
        "objective": {
            "business_metric": "validation_dynamic_topn_precision",
            "direction": "maximize",
        },
        "resource_policy": {
            "max_wallclock_seconds": 252000,
            "max_resource": 120,
            "framework_early_stopping": True,
            "early_stopping_patience": 9,
            "early_stopping_min_delta": 0.0,
        },
        "strict_test_used_for_selection": strict_test_used,
        "parameter_importance": {"learning_rate": 0.7, "window_size": 0.3},
        "trials": list(trials),
    }


class TestHpoProgress(unittest.TestCase):
    """验证分析器只接受当前自动调参合同。"""

    def test_tracks_variable_epochs_states_and_incumbent(self) -> None:
        """可变轮数不得突破一百二十轮且仍能选择验证业务最优参数试验。"""
        result = MODULE.analyze(
            payload(
                trial(0, "complete", 0.14, 83),
                trial(1, "pruned", epochs=20),
                trial(2, "complete", 0.16, 117),
                trial(3, "failed", failure="CUDA OOM"),
            )
        )

        self.assertEqual(2, result["counts"]["complete"])
        self.assertEqual(1, result["counts"]["pruned"])
        self.assertEqual(1, result["counts"]["failed"])
        self.assertEqual(2, result["best_trial"]["number"])
        self.assertEqual(117, result["best_trial"]["completed_epochs"])
        self.assertEqual("CUDA OOM", result["failures"][0]["failure"])

    def test_rejects_strict_test_participation(self) -> None:
        """严格测试参与参数选择时必须拒绝台账。"""
        with self.assertRaisesRegex(ValueError, "strict test"):
            MODULE.analyze(
                payload(trial(0, "complete", 0.14, 80), strict_test_used=True)
            )

    def test_requires_registration_regime_all_entity_scope(self) -> None:
        """股票调参必须覆盖注册制全部合格实体。"""
        value = payload(trial(0, "complete", 0.14, 80))
        value["data_scope"]["all_eligible_entities"] = False
        with self.assertRaisesRegex(ValueError, "all eligible entities"):
            MODULE.analyze(value)

    def test_requires_sampler_pruner_storage_and_unified_training_stop(self) -> None:
        """工具和统一的一百二十轮九轮零阈值早停必须同时存在。"""
        value = payload(trial(0, "complete", 0.14, 80))
        value["optimizer"]["pruner"] = ""
        with self.assertRaisesRegex(ValueError, "pruner"):
            MODULE.analyze(value)
        value = payload(trial(0, "complete", 0.14, 80))
        value["resource_policy"]["framework_early_stopping"] = False
        with self.assertRaisesRegex(ValueError, "enable framework early stopping"):
            MODULE.analyze(value)
        value = payload(trial(0, "complete", 0.14, 80))
        value["resource_policy"]["max_resource"] = 121
        with self.assertRaisesRegex(ValueError, "max_resource must equal 120"):
            MODULE.analyze(value)
        value = payload(trial(0, "complete", 0.14, 80))
        value["resource_policy"]["early_stopping_patience"] = 8
        with self.assertRaisesRegex(ValueError, "patience must equal 9"):
            MODULE.analyze(value)
        value = payload(trial(0, "complete", 0.14, 80))
        value["resource_policy"]["early_stopping_min_delta"] = 0.001
        with self.assertRaisesRegex(ValueError, "min_delta must equal zero"):
            MODULE.analyze(value)

    def test_rejects_trial_beyond_epoch_limit(self) -> None:
        """任何未剪枝参数试验都不能训练到第一百二十一轮。"""
        with self.assertRaisesRegex(ValueError, "completed_epochs must not exceed 120"):
            MODULE.analyze(payload(trial(0, "complete", 0.14, 121)))


if __name__ == "__main__":
    unittest.main()
