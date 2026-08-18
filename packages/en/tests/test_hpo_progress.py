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
            "max_resource": 1000,
            "framework_early_stopping": False,
        },
        "strict_test_used_for_selection": strict_test_used,
        "parameter_importance": {"learning_rate": 0.7, "window_size": 0.3},
        "trials": list(trials),
    }


class TestHpoProgress(unittest.TestCase):
    def test_tracks_variable_epochs_states_and_incumbent(self) -> None:
        result = MODULE.analyze(
            payload(
                trial(0, "complete", 0.14, 83),
                trial(1, "pruned", epochs=20),
                trial(2, "complete", 0.16, 247),
                trial(3, "failed", failure="CUDA OOM"),
            )
        )

        self.assertEqual(2, result["counts"]["complete"])
        self.assertEqual(1, result["counts"]["pruned"])
        self.assertEqual(1, result["counts"]["failed"])
        self.assertEqual(2, result["best_trial"]["number"])
        self.assertEqual(247, result["best_trial"]["completed_epochs"])
        self.assertEqual("CUDA OOM", result["failures"][0]["failure"])

    def test_rejects_strict_test_participation(self) -> None:
        with self.assertRaisesRegex(ValueError, "strict test"):
            MODULE.analyze(
                payload(trial(0, "complete", 0.14, 80), strict_test_used=True)
            )

    def test_requires_registration_regime_all_entity_scope(self) -> None:
        value = payload(trial(0, "complete", 0.14, 80))
        value["data_scope"]["all_eligible_entities"] = False
        with self.assertRaisesRegex(ValueError, "all eligible entities"):
            MODULE.analyze(value)

    def test_requires_sampler_pruner_storage_and_disables_framework_stop(self) -> None:
        value = payload(trial(0, "complete", 0.14, 80))
        value["optimizer"]["pruner"] = ""
        with self.assertRaisesRegex(ValueError, "pruner"):
            MODULE.analyze(value)
        value = payload(trial(0, "complete", 0.14, 80))
        value["resource_policy"]["framework_early_stopping"] = True
        with self.assertRaisesRegex(ValueError, "disable framework early stopping"):
            MODULE.analyze(value)


if __name__ == "__main__":
    unittest.main()
