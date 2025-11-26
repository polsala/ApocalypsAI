import os
import argparse
from datetime import datetime, timedelta

def find_stale_files(root_path: str, stale_days: int) -> list[tuple[str, datetime]]:
    """
    Finds files in the given root_path that haven't been modified in `stale_days`.
    Returns a list of (file_path, last_modified_datetime) tuples.
    """
    stale_threshold = datetime.now() - timedelta(days=stale_days)
    stale_files = []

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # os.path.getmtime returns a float timestamp
                mod_timestamp = os.path.getmtime(file_path)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)
                if mod_datetime < stale_threshold:
                    stale_files.append((file_path, mod_datetime))
            except OSError:
                # Handle cases where file might be inaccessible or deleted during scan
                pass
    return stale_files

def find_empty_directories(root_path: str) -> list[str]:
    """
    Finds directories in the given root_path that are empty (contain no files or subdirectories).
    Returns a list of empty directory paths.
    """
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check if the directory itself is empty using os.listdir
        # Exclude the root_path itself from being reported as an empty directory.
        try:
            if not os.listdir(dirpath) and dirpath != root_path:
                empty_dirs.append(dirpath)
        except OSError:
            # Handle cases where directory might be inaccessible
            pass
    return empty_dirs

def main():
    parser = argparse.ArgumentParser(
        description="Scan a repository for digital debris (stale files and empty directories)."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for debris.",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=90,
        help="Number of days after which a file is considered stale. Defaults to 90.",
    )

    args = parser.parse_args()

    repo_path = os.path.abspath(args.path)
    stale_days = args.stale_days

    if not os.path.isdir(repo_path):
        print(f"Error: The provided path '{repo_path}' is not a valid directory.")
        exit(1)

    print(f"Scanning for digital debris in: {repo_path}\n")

    stale_files = find_stale_files(repo_path, stale_days)
    empty_dirs = find_empty_directories(repo_path)

    print(f"--- Stale Files (not modified in {stale_days} days) ---")
    if stale_files:
        for file_path, mod_datetime in stale_files:
            print(f"- {file_path} (Last modified: {mod_datetime.strftime('%Y-%m-%d')})")
    else:
        print("No stale files found. Your digital archives are fresh!")

    print("\n--- Empty Directories ---")
    if empty_dirs:
        for dir_path in empty_dirs:
            print(f"- {dir_path}/")
    else:
        print("No empty directories found. Your digital landscape is tidy!")

    print(f"\nScan complete. Total stale files: {len(stale_files)}, Total empty directories: {len(empty_dirs)}.")

    if stale_files or empty_dirs:
        exit(0) # Indicate findings
    else:
        exit(2) # Indicate no-op (nothing to change)

if __name__ == "__main__":
    main()
