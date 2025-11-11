import os
import time
import argparse
from datetime import datetime, timedelta

def find_dust_bunnies(
    path: str,
    min_age_days: int = 90,
    exclude_extensions: list[str] = None,
    exclude_dirs: list[str] = None
) -> list[tuple[str, datetime]]:
    """
    Scans a directory for files (digital dust bunnies) that haven't been
    modified in at least `min_age_days`.

    Args:
        path (str): The root directory to scan.
        min_age_days (int): Minimum age in days for a file to be considered old.
        exclude_extensions (list[str]): List of file extensions to ignore (e.g., ['.log', '.tmp']).
        exclude_dirs (list[str]): List of directory names to ignore (e.g., ['node_modules', '.git']).

    Returns:
        list[tuple[str, datetime]]: A list of (file_path, last_modified_datetime) for
                                    identified dust bunnies.
    """
    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a valid directory.")
        return []

    dust_bunnies = []
    now = datetime.now()
    age_threshold = now - timedelta(days=min_age_days)

    exclude_extensions = [ext.lower() for ext in exclude_extensions] if exclude_extensions else []
    exclude_dirs = [d.lower() for d in exclude_dirs] if exclude_dirs else []

    for root, dirs, files in os.walk(path):
        # Modify dirs in-place to prune traversal
        dirs[:] = [d for d in dirs if d.lower() not in exclude_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            
            # Check if file extension is excluded
            _, ext = os.path.splitext(file)
            if ext.lower() in exclude_extensions:
                continue

            try:
                # Get last modification time
                mtime_timestamp = os.path.getmtime(file_path)
                mtime_datetime = datetime.fromtimestamp(mtime_timestamp)

                if mtime_datetime < age_threshold:
                    dust_bunnies.append((file_path, mtime_datetime))
            except OSError as e:
                # Handle cases where file might be inaccessible or deleted during scan
                print(f"Warning: Could not access '{file_path}': {e}")
                continue
    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Identify old, forgotten files (digital dust bunnies) in specified directories."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--min-age-days",
        type=int,
        default=90,
        help="Minimum age in days for a file to be considered a 'dust bunny' (default: 90)."
    )
    parser.add_argument(
        "--exclude-ext",
        nargs="*",
        default=[],
        help="Space-separated list of file extensions to ignore (e.g., .log .bak)."
    )
    parser.add_argument(
        "--exclude-dir",
        nargs="*",
        default=[],
        help="Space-separated list of directory names to ignore (e.g., node_modules .git)."
    )

    args = parser.parse_args()

    print(f"Scanning '{args.path}' for digital dust bunnies older than {args.min_age_days} days...")
    print(f"Excluding extensions: {', '.join(args.exclude_ext) if args.exclude_ext else 'None'}")
    print(f"Excluding directories: {', '.join(args.exclude_dir) if args.exclude_dir else 'None'}")

    dust_bunnies = find_dust_bunnies(
        args.path,
        args.min_age_days,
        args.exclude_ext,
        args.exclude_dir
    )

    if dust_bunnies:
        print(f"\nFound {len(dust_bunnies)} digital dust bunnies older than {args.min_age_days} days in '{args.path}':")
        for file_path, mtime in sorted(dust_bunnies):
            print(f"- {file_path} (Last modified: {mtime.strftime('%Y-%m-%d')})")
    else:
        print(f"\nNo digital dust bunnies found older than {args.min_age_days} days in '{args.path}'. Your digital space is sparkling clean!")

if __name__ == "__main__":
    main()
