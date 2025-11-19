import argparse
import os
import json

# Module-level definition of essential files
ESSENTIAL_FILES = [
    "README.md",
    "LICENSE",
    ".gitignore",
    "pyproject.toml", # Common for Python projects
    "requirements.txt" # Another common Python file
]

def check_survival_kit(directory: str) -> dict:
    """
    Checks a directory for essential repository files and returns a readiness report.
    """
    files_found = []
    files_missing = []

    for filename in ESSENTIAL_FILES:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            files_found.append(filename)
        else:
            files_missing.append(filename)
    
    total_essential = len(ESSENTIAL_FILES)
    found_count = len(files_found)
    
    if total_essential == 0:
        score = 100.0 # No essential files defined, so perfect score by default
    else:
        score = (found_count / total_essential) * 100.0

    status = "OK"
    message = "All essential files are present. Your survival kit is complete!"
    if files_missing:
        status = "WARNING"
        message = "Some essential files are missing. Improve your survival readiness!"
    if found_count == 0 and total_essential > 0:
        status = "CRITICAL"
        message = "No essential files found. Your survival kit is empty!"

    return {
        "directory": directory,
        "essential_files_checked": ESSENTIAL_FILES,
        "files_found": files_found,
        "files_missing": files_missing,
        "survival_readiness_score": round(score, 2),
        "status": status,
        "message": message
    }

def main():
    parser = argparse.ArgumentParser(
        description="Check a directory for essential repository files and report on survival readiness."
    )
    parser.add_argument(
        "--path", 
        type=str, 
        required=True, 
        help="The path to the directory to check."
    )
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(json.dumps({"error": f"Directory not found: {args.path}", "status": "ERROR"}))
        exit(1)

    report = check_survival_kit(args.path)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
