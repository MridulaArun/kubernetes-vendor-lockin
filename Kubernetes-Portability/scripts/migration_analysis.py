
import yaml
import csv
from pathlib import Path

# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Folder locations
CONFIG_DIR = BASE_DIR / "configurations"
RESULT_DIR = BASE_DIR / "results"

# Create results folder if missing
RESULT_DIR.mkdir(exist_ok=True)

# Available Kubernetes environments
ENVIRONMENTS = {
    "1": "eks_config.yaml",
    "2": "gke_config.yaml",
    "3": "aks_config.yaml",
    "4": "kubeadm_config.yaml"
}


# Load a YAML configuration file
def load_yaml(filename):

    file_path = CONFIG_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data


# Convert configuration list into a dictionary
def create_config_map(data):

    config_map = {}

    for item in data["configurations"]:

        key = (item["component"], item["setting"])

        config_map[key] = item

    return config_map


# Compare two Kubernetes environments
def compare_environments(source, destination):

    source_map = create_config_map(source)
    destination_map = create_config_map(destination)

    # Collect all configuration keys
    all_keys = sorted(set(source_map) | set(destination_map))

    results = []

    for key in all_keys:

        source_item = source_map.get(key)
        destination_item = destination_map.get(key)

        if source_item is None:

            status = "NEW IN DESTINATION"
            action = "Add destination configuration"
            reason = destination_item["reason"]

            source_value = "Not available"
            destination_value = destination_item["value"]

        elif destination_item is None:

            status = "NOT IN DESTINATION"
            action = "Review or replace configuration"
            reason = source_item["reason"]

            source_value = source_item["value"]
            destination_value = "Not available"

        elif source_item["value"] == destination_item["value"]:

            status = "UNCHANGED"
            action = "Reuse configuration"
            reason = "Configuration value is the same"

            source_value = source_item["value"]
            destination_value = destination_item["value"]

        else:

            status = "MODIFICATION REQUIRED"
            action = "Replace source-specific configuration"

            reason = (
                source_item["reason"]
                + " -> "
                + destination_item["reason"]
            )

            source_value = source_item["value"]
            destination_value = destination_item["value"]

        results.append({
            "component": key[0],
            "setting": key[1],
            "source_value": source_value,
            "destination_value": destination_value,
            "status": status,
            "action": action,
            "reason": reason
        })

    return results


# Display migration results
def display_results(results, source_name, destination_name):

    print("\n" + "=" * 65)
    print("          KUBERNETES MIGRATION ANALYSIS")
    print("=" * 65)

    print("Source platform      :", source_name)
    print("Destination platform :", destination_name)

    print("\nCONFIGURATION COMPARISON")
    print("-" * 65)

    for result in results:

        print("\nComponent :", result["component"])
        print("Setting   :", result["setting"])
        print("Source    :", result["source_value"])
        print("Target    :", result["destination_value"])
        print("Status    :", result["status"])
        print("Action    :", result["action"])
        print("Reason    :", result["reason"])

    print("\n" + "=" * 65)


# Save migration results into a CSV file

# Save migration results into a CSV file
def save_report(results, source_name, destination_name):

    output_file = RESULT_DIR / "migration_results.csv"

    fieldnames = [
        "source_platform",
        "destination_platform",
        "component",
        "setting",
        "source_value",
        "destination_value",
        "status",
        "action",
        "reason"
    ]

    # Check whether the CSV already exists and contains data
    file_exists = output_file.exists() and output_file.stat().st_size > 0

    # Append new results instead of overwriting old results
    with open(output_file, "a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write column headings only for a new or empty file
        if not file_exists:
            writer.writeheader()

        for result in results:

            row = result.copy()

            row["source_platform"] = source_name
            row["destination_platform"] = destination_name

            writer.writerow(row)

    print("\nMigration report saved successfully!")
    print("File location:", output_file)
    print("New migration results added to the report.")


# Main program
def main():

    print("\nKUBERNETES PORTABILITY PROJECT")
    print("MIGRATION ANALYSIS MODULE")

    # Load common application configuration
    common_app = load_yaml("common_app.yaml")

    app = common_app["application"]

    print("\nApplication being migrated:")
    print(app["name"])

    print("\nCOMMON KUBERNETES RESOURCES")

    for component in ["deployment", "service", "storage", "identity"]:

        resource = app[component]

        print(
            component,
            "->",
            resource["kind"],
            "-> Common Kubernetes resource"
        )

    # Display environment options
    print("\nSelect SOURCE environment:")
    print("1. AWS EKS")
    print("2. Google GKE")
    print("3. Azure AKS")
    print("4. Kubeadm")

    source_choice = input("\nEnter source option: ").strip()

    print("\nSelect DESTINATION environment:")
    print("1. AWS EKS")
    print("2. Google GKE")
    print("3. Azure AKS")
    print("4. Kubeadm")

    destination_choice = input("\nEnter destination option: ").strip()

    # Validate selections
    if source_choice not in ENVIRONMENTS:
        print("Invalid source selection!")
        return

    if destination_choice not in ENVIRONMENTS:
        print("Invalid destination selection!")
        return

    if source_choice == destination_choice:
        print("Source and destination cannot be the same!")
        return

    # Load source and destination profiles
    source = load_yaml(ENVIRONMENTS[source_choice])
    destination = load_yaml(ENVIRONMENTS[destination_choice])

    # Compare configurations
    results = compare_environments(source, destination)

    # Display comparison
    display_results(
        results,
        source["platform"],
        destination["platform"]
    )

    # Generate CSV report
    save_report(
        results,
        source["platform"],
        destination["platform"]
    )


# Program execution starts here
if __name__ == "__main__":
    main()
