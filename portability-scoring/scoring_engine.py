
import json
from pathlib import Path


def calculate_portability_score(metrics):
    """
    Calculate a portability score out of 100.

    Lower migration effort produces a higher score.
    These initial weights are provisional and must be
    agreed upon by the project team.
    """

    weights = {
        "yaml_change_percent": 0.30,
        "manual_rewrites": 0.25,
        "migration_time_minutes": 0.20,
        "failed_deployments": 0.15,
        "provider_dependencies": 0.10,
    }

    limits = {
        "yaml_change_percent": 100,
        "manual_rewrites": 20,
        "migration_time_minutes": 120,
        "failed_deployments": 10,
        "provider_dependencies": 10,
    }

    score = 0

    for metric, weight in weights.items():
        value = float(metrics[metric])

        if value < 0 or value > limits[metric]:
            raise ValueError(
                f"{metric} must be between 0 and {limits[metric]}"
            )

        portability = 100 * (1 - value / limits[metric])
        score += portability * weight

    return round(score, 2)


def main():
    input_file = Path("migration_metrics.json")

    if not input_file.exists():
        print("Error: migration_metrics.json was not found.")
        return

    with input_file.open("r", encoding="utf-8") as file:
        experiments = json.load(file)

    for experiment in experiments:
        score = calculate_portability_score(experiment["metrics"])

        print(f"\nMigration: {experiment['migration']}")
        print(f"Portability score: {score}/100")


if __name__ == "__main__":
    main()
