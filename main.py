import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
SCRIPT_RUNS = {
    "1": (
        "Migration analysis",
        ROOT_DIR / "Kubernetes-Portability" / "scripts" / "migration_analysis.py",
        ROOT_DIR,
    ),
    "2": (
        "Dynamic portability analysis",
        ROOT_DIR / "dynamic_portability.py",
        ROOT_DIR,
    ),
    "3": (
        "Portability summary and graphs",
        ROOT_DIR / "portability_score.py",
        ROOT_DIR,
    ),
    "4": (
        "Sample migration metrics scoring",
        ROOT_DIR / "portability-scoring" / "scoring_engine.py",
        ROOT_DIR / "portability-scoring",
    ),
    "5": (
        "Migration viability and planning",
        ROOT_DIR / "portability-scoring" / "decision_engine.py",
        ROOT_DIR / "portability-scoring",
    ),
}


def run_scripts(choices):
    for choice in choices:
        name, script_path, working_directory = SCRIPT_RUNS[choice]
        print(f"\n--- Running {name} ---", flush=True)

        try:
            subprocess.run(
                [sys.executable, str(script_path)],
                cwd=working_directory,
                check=True,
            )
        except subprocess.CalledProcessError as error:
            print(
                f"{name} failed with exit code {error.returncode}. "
                "Remaining scripts were not run."
            )
            return

        print(f"--- Finished {name} ---")


def main():
    while True:
        print("\nKubernetes Portability Toolkit")
        print("1. Compare migration environments")
        print("2. Run dynamic portability analysis")
        print("3. Generate portability summary and graphs")
        print("4. Score sample migration metrics")
        print("5. Assess migration viability and generate a plan")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == "0":
            print("Exiting.")
            return
        if choice in SCRIPT_RUNS:
            run_scripts((choice,))
        else:
            print("Invalid option. Enter a number from 0 to 5.")


if __name__ == "__main__":
    main()
