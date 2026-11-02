
import json
import sys
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
        "migration_time": 0.20,
        "failed_deployments": 0.15,
        "provider_dependencies": 0.10,
    }

    limits = {
        "yaml_change_percent": 100,
        "manual_rewrites": 20,
        "failed_deployments": 10,
        "provider_dependencies": 10,
    }

    time_keys = {
        "migration_time_minutes": 120,
        "migration_time_hours": 48,
    }
    present_time_keys = [key for key in time_keys if key in metrics]
    if len(present_time_keys) != 1:
        raise ValueError(
            "metrics must contain exactly one of migration_time_minutes "
            "or migration_time_hours"
        )

    time_key = present_time_keys[0]
    limits["migration_time"] = time_keys[time_key]
    metric_keys = {
        "yaml_change_percent": "yaml_change_percent",
        "manual_rewrites": "manual_rewrites",
        "migration_time": time_key,
        "failed_deployments": "failed_deployments",
        "provider_dependencies": "provider_dependencies",
    }

    score = 0

    for metric, weight in weights.items():
        input_metric = metric_keys[metric]
        try:
            value = float(metrics[input_metric])
        except KeyError as error:
            raise ValueError(f"Missing required metric: {input_metric}") from error
        except (TypeError, ValueError) as error:
            raise ValueError(f"{input_metric} must be a number") from error

        if value < 0 or value > limits[metric]:
            raise ValueError(
                f"{input_metric} must be between 0 and {limits[metric]} "
                f"(got {value:g})"
            )

        portability = 100 * (1 - value / limits[metric])
        score += portability * weight

    return round(score, 2)


def main():
    input_file = Path("migration_metrics.json")

    if not input_file.exists():
        print(f"Error: {input_file.resolve()} was not found.", file=sys.stderr)
        sys.exit(1)

    with input_file.open("r", encoding="utf-8") as file:
        experiments = json.load(file)

    if not isinstance(experiments, list):
        print("Error: migration_metrics.json must contain a JSON list.", file=sys.stderr)
        sys.exit(1)

    invalid_records = 0
    for index, experiment in enumerate(experiments, start=1):
        if not isinstance(experiment, dict):
            print(f"\nRecord {index}: expected a JSON object; skipping.")
            invalid_records += 1
            continue

        migration = experiment.get("migration", f"Record {index}")
        metrics = experiment.get("metrics")
        if not isinstance(metrics, dict):
            print(f"\n{migration}: missing or invalid metrics object; skipping.")
            invalid_records += 1
            continue

        try:
            score = calculate_portability_score(metrics)
        except ValueError as error:
            print(f"\n{migration}: cannot calculate score: {error}")
            invalid_records += 1
            continue

        print(f"\nMigration: {migration}")
        stored_score = metrics.get("portability_score_percent")
        if stored_score is not None:
            print(f"Stored portability score: {stored_score}/100")
        print(f"Formula-calculated portability score: {score}/100")

    if invalid_records:
        print(
            f"\n{invalid_records} record(s) could not be scored. "
            "Correct the reported values or limits and run the scorer again.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
