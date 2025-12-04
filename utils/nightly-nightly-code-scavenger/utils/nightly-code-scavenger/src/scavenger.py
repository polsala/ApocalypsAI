import os
import time
import argparse
from datetime import datetime, timedelta
import fnmatch

def get_file_age_days(filepath):
    """Returns the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except OSError:
        return -1 # Indicate error or file not found

def is_empty_dir(path):
    """Checks if a directory is empty."""
    return not os.listdir(path)

def is_temp_or_log_file(name, path):
    """Checks if a file or directory matches common temporary/log patterns."""
    temp_patterns = [
        '*.tmp', '*.log', '*.bak', '*.swp', '*.swo', '*.pyc', '*.pyo',
        '__pycache__', '.DS_Store', 'Thumbs.db', '.pytest_cache',
        '.coverage', '.mypy_cache', '.vscode', '.idea',
        'npm-debug.log', 'yarn-debug.log', 'build/', 'dist/',
        'target/', 'out/', 'node_modules/', '.env', '.venv',
        'venv/', 'env/'
    ]
    for pattern in temp_patterns:
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

def should_exclude(path, exclude_patterns):
    """Checks if a path should be excluded based on glob patterns."""
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

def scavenge(root_path, max_age_days=365, exclude_patterns=None):
    """
    Scans the given root_path for empty directories, old files, and temporary/log files.
    Returns a dictionary with categorized findings.
    """
    if exclude_patterns is None:
        exclude_patterns = []

    empty_dirs = []
    old_files = []
    temp_files = []

    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return {
            "empty_dirs": [],
            "old_files": [],
            "temp_files": []
        }

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
        # Filter out excluded directories from dirnames for current walk iteration
        dirnames[:] = [d for d in dirnames if not should_exclude(os.path.join(dirpath, d), exclude_patterns)]

        # Check for empty directories (after filtering)
        if not dirnames and not filenames and not should_exclude(dirpath, exclude_patterns):
            empty_dirs.append(dirpath)

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if should_exclude(filepath, exclude_patterns):
                continue

            # Check for old files
            age_days = get_file_age_days(filepath)
            if age_days > max_age_days:
                mtime_timestamp = os.path.getmtime(filepath)
                mtime_dt = datetime.fromtimestamp(mtime_timestamp)
                old_files.append(f"{filepath} (Last modified: {mtime_dt.strftime('%Y-%m-%d')})")

            # Check for temporary/log files
            if is_temp_or_log_file(filename, filepath):
                temp_files.append(filepath)
        
        # Also check if the current directory itself matches a temp pattern (e.g. __pycache__)
        if is_temp_or_log_file(os.path.basename(dirpath), dirpath) and dirpath != root_path and not should_exclude(dirpath, exclude_patterns):
            temp_files.append(dirpath + os.sep) # Add separator to indicate it's a directory

    return {
        "empty_dirs": sorted(list(set(empty_dirs))), # Use set to remove duplicates, then sort
        "old_files": sorted(list(set(old_files))),
        "temp_files": sorted(list(set(temp_files)))
    }

def main():
    parser = argparse.ArgumentParser(
        description="Scans a directory for empty directories, old files, and temporary/log files."
    )
    parser.add_argument(
        "path_to_scan",
        help="The root directory to begin scavenging."
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=365,
        help="Files older than this many days will be flagged as 'old'. Default is 365 days."
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="A glob pattern to exclude files or directories from scanning (e.g., '*/.git/*', 'node_modules'). Can be repeated."
    )

    args = parser.parse_args()

    print(f"Scavenging report for: {args.path_to_scan}\n")

    results = scavenge(args.path_to_scan, args.max_age_days, args.exclude)

    if not any(results.values()):
        print("No digital debris found. Your repository is pristine!")
        return

    if results["empty_dirs"]:
        print("--- Empty Directories ---")
        for d in results["empty_dirs"]:
            print(f"- {d}")
        print()

    if results["old_files"]:
        print(f"--- Old Files (modified > {args.max_age_days} days ago) ---")
        for f in results["old_files"]:
            print(f"- {f}")
        print()

    if results["temp_files"]:
        print("--- Temporary/Log Files ---")
        for f in results["temp_files"]:
            print(f"- {f}")
        print()

if __name__ == "__main__":
    main()
