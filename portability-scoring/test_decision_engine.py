import unittest
import json
from pathlib import Path

from decision_engine import ENVIRONMENTS, evaluate_migration, get_migration_metrics


def metrics(
    yaml_change_percent=50,
    manual_rewrites=10,
    migration_time_hours=24,
    failed_deployments=2,
    provider_dependencies=5,
):
    return {
        "yaml_change_percent": yaml_change_percent,
        "manual_rewrites": manual_rewrites,
        "migration_time_hours": migration_time_hours,
        "failed_deployments": failed_deployments,
        "provider_dependencies": provider_dependencies,
    }


class EvaluateMigrationTests(unittest.TestCase):
    def test_recommends_staying_when_score_is_below_20_percent(self):
        result = evaluate_migration(
            "low portability",
            metrics(
                yaml_change_percent=100,
                manual_rewrites=20,
                migration_time_hours=48,
                failed_deployments=10,
                provider_dependencies=0,
            ),
        )

        self.assertEqual(result["portability_score_percent"], 10)
        self.assertEqual(result["recommendation"], "Continue with the current service")
        self.assertIsNone(result["estimate"])

    def test_score_of_exactly_20_percent_does_not_trigger_score_cutoff(self):
        result = evaluate_migration(
            "score threshold",
            metrics(
                yaml_change_percent=100,
                manual_rewrites=20,
                migration_time_hours=24,
                failed_deployments=10,
                provider_dependencies=0,
            ),
        )

        self.assertEqual(result["portability_score_percent"], 20)
        self.assertEqual(result["recommendation"], "Migrate")

    def test_recommends_staying_when_provider_lock_in_is_above_threshold(self):
        result = evaluate_migration(
            "high lock-in", metrics(provider_dependencies=8)
        )

        self.assertEqual(result["recommendation"], "Continue with the current service")
        self.assertIn("Provider lock-in is too high", result["reasons"][0])
        self.assertIsNone(result["estimate"])

    def test_exact_lock_in_threshold_is_allowed_and_estimate_is_calculated(self):
        result = evaluate_migration(
            "threshold migration",
            metrics(migration_time_hours=30, provider_dependencies=7),
        )

        self.assertEqual(result["recommendation"], "Migrate")
        self.assertEqual(
            result["estimate"],
            {
                "effort_hours": 30,
                "person_days": 5,
                "engineers": 1,
                "calendar_workdays": 5,
            },
        )
        self.assertTrue(result["instructions"])

    def test_supports_migration_time_in_minutes(self):
        sample = metrics(provider_dependencies=5)
        del sample["migration_time_hours"]
        sample["migration_time_minutes"] = 90

        result = evaluate_migration("minutes migration", sample)

        self.assertEqual(result["estimate"]["effort_hours"], 1.5)
        self.assertEqual(result["estimate"]["calendar_workdays"], 1)

    def test_rejects_non_finite_metrics(self):
        with self.assertRaisesRegex(ValueError, "provider_dependencies"):
            evaluate_migration(
                "invalid metric", metrics(provider_dependencies=float("nan"))
            )

    def test_sample_metrics_cover_all_distinct_environment_pairs(self):
        metrics_file = Path(__file__).with_name("migration_metrics.json")
        with metrics_file.open("r", encoding="utf-8") as file:
            experiments = json.load(file)

        expected_pairs = {
            (source, destination)
            for source in ENVIRONMENTS.values()
            for destination in ENVIRONMENTS.values()
            if source != destination
        }
        actual_pairs = {
            (item["source_platform"], item["destination_platform"])
            for item in experiments
        }

        self.assertEqual(len(expected_pairs), 12)
        self.assertEqual(actual_pairs, expected_pairs)

    def test_adjusted_sample_dependencies_do_not_block_every_pair(self):
        metrics_file = Path(__file__).with_name("migration_metrics.json")
        with metrics_file.open("r", encoding="utf-8") as file:
            experiments = json.load(file)

        recommendations = [
            evaluate_migration(
                f"{item['source_platform']} to {item['destination_platform']}",
                item["metrics"],
            )["recommendation"]
            for item in experiments
        ]

        self.assertIn("Migrate", recommendations)
        self.assertNotIn("Continue with the current service", recommendations)

    def test_metrics_lookup_requires_an_available_direction(self):
        with self.assertRaisesRegex(ValueError, "No metrics found"):
            get_migration_metrics([], "AWS EKS", "Google GKE")


if __name__ == "__main__":
    unittest.main()
