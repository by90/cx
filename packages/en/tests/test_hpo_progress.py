"""Test registration scope, stopping rules, and states in the HPO ledger analyzer."""

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
    """Build one minimal trial fact.

    Args:
        number: Stable trial number.
        state: Current trial state.
        value: Validation business metric for a completed trial.
        epochs: Actual completed training epochs.
        failure: Recorded trial failure reason.

    Returns:
        A trial dictionary accepted by the progress analyzer.
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
    """Build a ledger with unified 120-epoch and 9-epoch-patience stopping.

    Args:
        *trials: Trial facts included in the current study.
        strict_test_used: Whether strict test influenced parameter selection.

    Returns:
        A ledger containing data scope, tool, training policy, and trials.
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
    """Verify that the analyzer accepts only the current HPO contract."""

    def test_tracks_variable_epochs_states_and_incumbent(self) -> None:
        """Variable epochs stay within 120 while the business incumbent is selected."""
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
        """Reject a ledger when strict test participated in selection."""
        with self.assertRaisesRegex(ValueError, "strict test"):
            MODULE.analyze(
                payload(trial(0, "complete", 0.14, 80), strict_test_used=True)
            )

    def test_requires_registration_regime_all_entity_scope(self) -> None:
        """Require every eligible entity in the registration-regime scope."""
        value = payload(trial(0, "complete", 0.14, 80))
        value["data_scope"]["all_eligible_entities"] = False
        with self.assertRaisesRegex(ValueError, "all eligible entities"):
            MODULE.analyze(value)

    def test_requires_sampler_pruner_storage_and_unified_training_stop(self) -> None:
        """Require the tool and unified 120/9 zero-threshold stopping contract."""
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
        """Reject every unpruned trial that reaches epoch 121."""
        with self.assertRaisesRegex(ValueError, "completed_epochs must not exceed 120"):
            MODULE.analyze(payload(trial(0, "complete", 0.14, 121)))


if __name__ == "__main__":
    unittest.main()
