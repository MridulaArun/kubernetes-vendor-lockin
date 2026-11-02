import json
import math
import sys
from pathlib import Path

from scoring_engine import calculate_portability_score


ROOT_DIR = Path(__file__).resolve().parent
ENVIRONMENTS = {
    "1": "AWS EKS",
    "2": "Google GKE",
    "3": "Azure AKS",
    "4": "Kubeadm",
}
MIN_PORTABILITY_SCORE = 20
MAX_ACCEPTABLE_PROVIDER_DEPENDENCIES = 7
PRODUCTIVE_HOURS_PER_ENGINEER_PER_DAY = 6
PERSON_DAYS_PER_ENGINEER = 5
MAX_RECOMMENDED_ENGINEERS = 3


def evaluate_migration(migration, metrics):
    """Assess migration viability and estimate the effort for viable migrations."""
    score = calculate_portability_score(metrics)
    dependencies = float(metrics["provider_dependencies"])
    reasons = []

    if score < MIN_PORTABILITY_SCORE:
        reasons.append(
            f"Portability score is below {MIN_PORTABILITY_SCORE}%."
        )
    if dependencies > MAX_ACCEPTABLE_PROVIDER_DEPENDENCIES:
        reasons.append(
            "Provider lock-in is too high "
            f"({dependencies:g}/10; maximum allowed is "
            f"{MAX_ACCEPTABLE_PROVIDER_DEPENDENCIES}/10)."
        )

    result = {
        "migration": migration,
        "portability_score_percent": score,
        "provider_dependencies": dependencies,
        "recommendation": "Continue with the current service" if reasons else "Migrate",
        "reasons": reasons,
        "estimate": None,
        "instructions": [],
    }

    if reasons:
        return result

    if "migration_time_hours" in metrics:
        effort_hours = float(metrics["migration_time_hours"])
    else:
        effort_hours = float(metrics["migration_time_minutes"]) / 60

    person_days = effort_hours / PRODUCTIVE_HOURS_PER_ENGINEER_PER_DAY
    engineers = min(
        MAX_RECOMMENDED_ENGINEERS,
        max(1, math.ceil(person_days / PERSON_DAYS_PER_ENGINEER)),
    )
    workdays = math.ceil(person_days / engineers)

    result["estimate"] = {
        "effort_hours": round(effort_hours, 2),
        "person_days": round(person_days, 2),
        "engineers": engineers,
        "calendar_workdays": workdays,
    }
    result["instructions"] = [
        "Inventory provider-specific integrations and replace them with "
        "destination-provider equivalents or portable Kubernetes interfaces.",
        "Update the affected manifests (approximately "
        f"{float(metrics['yaml_change_percent']):g}% of YAML) and complete the "
        f"{float(metrics['manual_rewrites']):g} anticipated manual rewrites.",
        "Migrate storage and data; verify storage classes, access modes, "
        "backup, and restore behavior on the destination.",
        "Recreate workload identity, ingress, and load-balancing configuration "
        "using the destination provider's supported integrations.",
        "Deploy to a test cluster, validate application behavior and "
        "permissions, and address deployment failures before cutover.",
        "Cut over in stages, monitor the workload, and retain a tested "
        "rollback path to the source service.",
    ]
    return result


def display_result(result):
    print(f"\nMigration: {result['migration']}")
    print(f"Formula-calculated portability: {result['portability_score_percent']}/100")
    print(f"Provider dependencies: {result['provider_dependencies']:g}/10")
    print(f"Recommendation: {result['recommendation']}")

    if result["reasons"]:
        for reason in result["reasons"]:
            print(f"- {reason}")
        return

    estimate = result["estimate"]
    print(
        "Estimated effort: "
        f"{estimate['effort_hours']:g} person-hours "
        f"({estimate['person_days']:g} person-days)"
    )
    print(
        "Suggested team and schedule: "
        f"{estimate['engineers']} engineer(s), approximately "
        f"{estimate['calendar_workdays']} working day(s)"
    )
    print("Migration instructions:")
    for index, instruction in enumerate(result["instructions"], start=1):
        print(f"{index}. {instruction}")


def get_migration_metrics(experiments, source, destination):
    """Return metrics for one of the configured directed migration pairs."""
    for experiment in experiments:
        if (
            experiment.get("source_platform") == source
            and experiment.get("destination_platform") == destination
        ):
            metrics = experiment.get("metrics")
            if not isinstance(metrics, dict):
                raise ValueError(
                    f"Metrics for {source} to {destination} must be an object."
                )
            return metrics
    raise ValueError(f"No metrics found for {source} to {destination}.")


def choose_environment(prompt):
    print(f"\n{prompt}:")
    for choice, environment in ENVIRONMENTS.items():
        print(f"{choice}. {environment}")
    print("0. Cancel")

    choice = input("Select an environment: ").strip()
    if choice == "0":
        return None
    if choice not in ENVIRONMENTS:
        raise ValueError("Invalid environment selection.")
    return ENVIRONMENTS[choice]


def main():
    input_file = ROOT_DIR / "migration_metrics.json"
    if not input_file.exists():
        print(f"Error: {input_file} was not found.", file=sys.stderr)
        return 1

    try:
        with input_file.open("r", encoding="utf-8") as file:
            experiments = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Error: could not read {input_file}: {error}", file=sys.stderr)
        return 1

    if not isinstance(experiments, list):
        print("Error: migration_metrics.json must contain a JSON list.", file=sys.stderr)
        return 1

    try:
        source = choose_environment("Select SOURCE environment")
        if source is None:
            print("Migration assessment cancelled.")
            return 0

        destination = choose_environment("Select DESTINATION environment")
        if destination is None:
            print("Migration assessment cancelled.")
            return 0
        if source == destination:
            print("Source and destination must be different.", file=sys.stderr)
            return 1

        metrics = get_migration_metrics(experiments, source, destination)
        result = evaluate_migration(f"{source} to {destination}", metrics)
    except (AttributeError, TypeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    display_result(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
