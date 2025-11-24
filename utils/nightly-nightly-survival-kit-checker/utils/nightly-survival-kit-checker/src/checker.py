import os
import argparse
from typing import List, Dict, Any

def check_survival_kit(directory: str, required_files: List[str]) -> Dict[str, Any]:
    """
    Checks for the presence of essential files in a given directory.

    Args:
        directory (str): The path to the directory to check.
        required_files (List[str]): A list of file names to look for.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - 'present': List of files found.
            - 'missing': List of files not found.
            - 'score': A string representing the survival score (e.g., "3/5").
            - 'status': "READY" if all files are present, "NEEDS ATTENTION" otherwise.
    """
    if not os.path.isdir(directory):
        return {
            'present': [],
            'missing': required_files,
            'score': f"0/{len(required_files)}",
            'status': "DIRECTORY NOT FOUND"
        }

    present_files = []
    missing_files = []

    for filename in required_files:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            present_files.append(filename)
        else:
            missing_files.append(filename)

    total_required = len(required_files)
    found_count = len(present_files)
    score = f"{found_count}/{total_required}"
    status = "READY" if found_count == total_required else "NEEDS ATTENTION"

    return {
        'present': present_files,
        'missing': missing_files,
        'score': score,
        'status': status
    }

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Survival Kit Checker: Ensures essential repository files are present."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the repository directory to check."
    )
    parser.add_argument(
        "--files",
        nargs=":",
        default=["README.md", "LICENSE", ".gitignore", "CONTRIBUTING.md", "SECURITY.md"],
        help="Space-separated list of essential files to check for. Defaults to common repo files."
    )

    args = parser.parse_args()

    print(f"Checking survival kit for directory: {args.directory}")
    print(f"Required files: {', '.join(args.files)}")

    result = check_survival_kit(args.directory, args.files)

    print("\n--- Survival Kit Report ---")
    print(f"Status: {result['status']}")
    print(f"Score: {result['score']}")
    if result['present']:
        print(f"Present files: {', '.join(result['present'])}")
    if result['missing']:
        print(f"Missing files: {', '.join(result['missing'])}")
        exit(1) # Indicate failure if essential files are missing

    print("--------------------------")
    if result['status'] == "READY":
        exit(0)
    else:
        exit(1) # Exit with error if not ready

if __name__ == "__main__":
    main()
