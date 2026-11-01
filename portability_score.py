import csv
from pathlib import Path

import matplotlib.pyplot as plt

from dynamic_portability import analyze_configurations

ROOT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ROOT_DIR / "results"
GRAPHS_DIR = ROOT_DIR / "graphs"


def calculate_scores():
    return analyze_configurations()


def save_results(data):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RESULTS_DIR / "portability_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"[+] Portability results successfully saved to {csv_path}")


def generate_graphs(data):
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
    environments = [row["Environment"] for row in data]
    scores = [row["Portability Score (%)"] for row in data]
    efforts = [row["Migration Effort (Hrs)"] for row in data]

    plt.figure(figsize=(8, 5))
    plt.bar(
        environments,
        scores,
        color=["#2ca02c", "#1f77b4", "#ff7f0e", "#d62728"],
    )
    plt.ylim(0, 100)
    plt.ylabel("Portability Score (%)")
    plt.title("Kubernetes Environment Portability Index")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.savefig(GRAPHS_DIR / "portability_score_chart.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    if all(effort is not None for effort in efforts):
        plt.bar(environments, efforts, color="#9467bd")
        plt.ylabel("Estimated Migration Effort (Hours)")
        plt.title("Migration Effort Across Kubernetes Environments")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    else:
        plt.axis("off")
        plt.text(
            0.5,
            0.5,
            "Migration effort cannot be inferred from the current configuration data.",
            ha="center",
            va="center",
            wrap=True,
        )
        plt.title("Migration Effort: Not Available")
    plt.savefig(GRAPHS_DIR / "migration_effort_chart.png")
    plt.close()
    print(f"[+] Comparison graphs successfully generated in {GRAPHS_DIR}/")


if __name__ == "__main__":
    print("Initializing Portability Measurement Module...")
    results = calculate_scores()
    save_results(results)
    generate_graphs(results)
    print("Portability Measurement Module execution completed!")
