import os
import shutil
import argparse
from datetime import datetime, timedelta
import sys

def get_file_age_days(filepath):
    """Calculates the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (datetime.now() - datetime.fromtimestamp(mtime)).days
    except OSError:
        return -1 # Indicate error or unreadable file

def is_dust(filepath, max_size_bytes, min_age_days):
    """
    Determines if a file qualifies as 'cosmic dust'.
    A file is dust if it's empty, smaller than max_size_bytes, or older than min_age_days.
    """
    if not os.path.isfile(filepath):
        return False

    try:
        file_size = os.path.getsize(filepath)
        file_age = get_file_age_days(filepath)

        is_empty = file_size == 0
        is_small = file_size <= max_size_bytes
        is_old = file_age >= min_age_days if min_age_days > 0 else False

        # A file is dust if it meets any of the criteria
        return is_empty or is_small or is_old
    except OSError as e:
        print(f"Warning: Could not access file {filepath} - {e}", file=sys.stderr)
        return False

def collect_dust(
    paths,
    action,
    quarantine_path,
    max_size_bytes,
    min_age_days,
    exclude_dirs,
    verbose
):
    """
    Scans specified paths for 'cosmic dust' files and performs the chosen action.
    """
    dust_files = []
    for path in paths:
        if not os.path.isdir(path):
            print(f"Error: Path '{path}' is not a valid directory. Skipping.", file=sys.stderr)
            continue

        for root, dirs, files in os.walk(path):
            # Modify dirs in-place to prune traversal
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for filename in files:
                filepath = os.path.join(root, filename)
                if is_dust(filepath, max_size_bytes, min_age_days):
                    dust_files.append(filepath)
                    if verbose:
                        size = os.path.getsize(filepath)
                        age = get_file_age_days(filepath)
                        print(f"Found dust: {filepath} (Size: {size} bytes, Age: {age} days)")

    if not dust_files:
        print("No cosmic dust found. Your digital space is sparkling clean!")
        return

    print(f"\n--- Cosmic Dust Report ({len(dust_files)} files found) ---")
    for df in dust_files:
        print(f"- {df}")

    if action == "quarantine":
        os.makedirs(quarantine_path, exist_ok=True)
        print(f"\n--- Moving dust to quarantine: {quarantine_path} ---")
        for df in dust_files:
            try:
                dest_path = os.path.join(quarantine_path, os.path.basename(df))
                # Handle potential name collisions in quarantine by appending a timestamp
                if os.path.exists(dest_path):
                    name, ext = os.path.splitext(os.path.basename(df))
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    dest_path = os.path.join(quarantine_path, f"{name}_{timestamp}{ext}")

                shutil.move(df, dest_path)
                print(f"Moved: {df} -> {dest_path}")
            except Exception as e:
                print(f"Error moving {df}: {e}", file=sys.stderr)
    else: # action == "list"
        print("\n--- Action: List only. No files were moved. ---")


def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Scans directories for small, old, or empty files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "paths",
        nargs=":",
        default=["."],
        help="One or more directories to scan for cosmic dust."
    )
    parser.add_argument(
        "--action",
        choices=["list", "quarantine"],
        default="list",
        help="Action to perform: 'list' found files or 'quarantine' them."
    )
    parser.add_argument(
        "--quarantine-path",
        default="./dust_quarantine",
        help="Directory to move files to if action is 'quarantine'."
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1024, # 1KB
        help="Maximum file size in bytes to consider as dust. Set to 0 for empty files only."
    )
    parser.add_argument(
        "--min-age",
        type=int,
        default=30, # 30 days
        help="Minimum age in days for a file to be considered old dust. Set to 0 to ignore age."
    )
    parser.add_argument(
        "--exclude",
        type=str,
        default=".git,node_modules,venv,env",
        help="Comma-separated list of directory names to exclude from scanning."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed information about scanned files."
    )

    args = parser.parse_args()

    exclude_dirs_list = [d.strip() for d in args.exclude.split(',') if d.strip()]

    collect_dust(
        paths=args.paths,
        action=args.action,
        quarantine_path=args.quarantine_path,
        max_size_bytes=args.max_size,
        min_age_days=args.min_age,
        exclude_dirs=exclude_dirs_list,
        verbose=args.verbose
    )

if __name__ == "__main__":
    main()
