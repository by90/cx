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


def payload(*trials: dict, strict_test_used: bool = False) -> dict:
    return {
        "data_scope": {
            "id": "chinext_registration_20200824",
            "kind": "registration_regime",
            "start_date": "2020-08-24",
            "all_eligible_entities": True,
        },
        "objective": {
            "business_metric": "validation_dynamic_topn_precision",
            "higher_is_better": True,
            "minimum_business_delta": 0.01,
        },
        "training_contract": {
            "max_epochs": 1000,
            "early_stopping_patience": 20,
        },
        "strict_test_used_for_selection": strict_test_used,
        "baseline_trial": "baseline",
        "trials": list(trials),
        "proposed_next": {
            "hypothesis": "wider summaries may retain more context",
            "single_change": "summary_width: 64 -> 128",
        },
    }


def trial(
    name: str,
    business: float,
    loss: float,
    loss_group: str = "unweighted_ce",
) -> dict:
    return {
        "name": name,
        "business_comparison_group": "open_9level_same_split_and_metric",
        "loss_comparison_group": loss_group,
        "status": "completed",
        "business_metric": business,
        "best_validation_loss": loss,
        "final_validation_loss": loss + 0.01,
        "completed_epochs": 100,
        "planned_epochs": 1000,
        "max_epochs": 1000,
        "early_stopping_patience": 20,
        "best_epoch": 90,
        "resource_gate_passed": True,
        "changed_dimension": "summary_width",
    }


class TestHpoProgress(unittest.TestCase):
    def test_stops_after_two_business_regressions_despite_better_loss(self) -> None:
        result = MODULE.analyze(
            payload(
                trial("baseline", 0.20, 1.20),
                trial("candidate_1", 0.18, 1.10),
                trial("candidate_2", 0.17, 1.00),
            )
        )

        self.assertEqual(result["decision"], "stop")
        self.assertEqual(result["business_regression_streak"], 2)
        self.assertIn("objective_conflict", result["flags"])
        self.assertIn("business_regression_streak", result["flags"])

    def test_rejects_strict_test_participation(self) -> None:
        with self.assertRaisesRegex(ValueError, "strict test"):
            MODULE.analyze(
                payload(
                    trial("baseline", 0.20, 1.20),
                    strict_test_used=True,
                )
            )

    def test_requires_registration_regime_all_entity_scope(self) -> None:
        value = payload(trial("baseline", 0.20, 1.20))
        value["data_scope"]["all_eligible_entities"] = False

        with self.assertRaisesRegex(ValueError, "all eligible entities"):
            MODULE.analyze(value)

    def test_rejects_changes_to_fixed_training_contract(self) -> None:
        value = payload(trial("baseline", 0.20, 1.20))
        value["training_contract"]["early_stopping_patience"] = 21

        with self.assertRaisesRegex(ValueError, "1000.*20"):
            MODULE.analyze(value)

    def test_continues_only_one_evidence_backed_change(self) -> None:
        result = MODULE.analyze(
            payload(
                trial("baseline", 0.20, 1.20),
                trial("candidate_1", 0.22, 1.18),
            )
        )

        self.assertEqual(result["decision"], "continue")
        self.assertEqual(result["next_change"], "summary_width: 64 -> 128")
        self.assertEqual(result["flags"], [])

    def test_compares_business_but_not_loss_across_loss_contracts(self) -> None:
        result = MODULE.analyze(
            payload(
                trial("baseline", 0.20, 1.20),
                trial("ranking_loss", 0.22, 0.90, loss_group="ce_plus_bpr"),
            )
        )

        latest = result["trials"][-1]
        self.assertEqual(result["decision"], "continue")
        self.assertTrue(latest["business_comparable"])
        self.assertFalse(latest["validation_loss_comparable"])
        self.assertIsNone(latest["validation_loss_delta_from_baseline"])


if __name__ == "__main__":
    unittest.main()
