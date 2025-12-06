import os
import subprocess
import sys
from typing import List, Dict

def get_git_untracked_files(repo_path: str) -> List[str]:
    """Gets a list of untracked files in the Git repository."""
    try:
        # --others: show untracked files
        # --exclude-standard: use standard excludes (e.g., .gitignore)
        result = subprocess.run(
            ['git', '-C', repo_path, 'ls-files', '--others', '--exclude-standard'],
            capture_output=True,
            text=True,
            check=True
        )
        return [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print("Git command not found. Please ensure Git is installed and in your PATH.", file=sys.stderr)
        return []

def get_empty_directories(repo_path: str) -> List[str]:
    """Gets a list of empty directories within the repository path."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(repo_path):
        # Exclude .git directory itself and its contents from being reported as empty
        if '.git' in dirpath.split(os.sep):
            continue

        # Check if the directory is truly empty (no files and no subdirectories)
        if not dirnames and not filenames:
            # Ensure it's not the root path itself if it's the only thing left
            # and it's not the repo_path itself if it's empty (which is usually not desired)
            if dirpath != repo_path:
                empty_dirs.append(os.path.relpath(dirpath, repo_path))
    return empty_dirs

def detect_digital_debris(repo_path: str) -> Dict[str, List[str]]:
    """Detects untracked files and empty directories in a given repository path."""
    if not os.path.isdir(repo_path):
        print(f"Error: Repository path '{repo_path}' does not exist or is not a directory.", file=sys.stderr)
        return {"untracked_files": [], "empty_directories": []}

    print(f"Scanning repository: {os.path.abspath(repo_path)}")

    untracked_files = get_git_untracked_files(repo_path)
    empty_dirs = get_empty_directories(repo_path)

    return {
        "untracked_files": untracked_files,
        "empty_directories": empty_dirs
    }

def print_report(debris_data: Dict[str, List[str]], repo_path: str):
    """Prints a formatted report of the detected digital debris."""
    print("\n--- Digital Debris Report ---")
    print(f"Scanning repository: {os.path.abspath(repo_path)}")

    untracked = debris_data.get("untracked_files", [])
    empty = debris_data.get("empty_directories", [])

    if untracked:
        print("\n🗑️ Untracked Files (Forgotten Relics):")
        for f in untracked:
            print(f"  - {f}")
    else:
        print("\n✅ No untracked files found. Your relics are accounted for!")

    if empty:
        print("\n🕳️ Empty Directories (Hollow Ruins):")
        for d in empty:
            print(f"  - {d}/")
    else:
        print("\n✅ No empty directories found. Your structures are sound!")

    print("\n--- End of Report ---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/detector.py <path_to_repository>", file=sys.stderr)
        sys.exit(1)

    repo_path = sys.argv[1]
    debris = detect_digital_debris(repo_path)
    print_report(debris, repo_path)

    # Exit with 0 as the report was successfully generated, regardless of findings.
    # An exit code of 1 is reserved for critical errors (e.g., invalid path, git not found).
    sys.exit(0)
