import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def find_dust_files(
    root_dir: str,
    min_age_days: int = 30,
    patterns: list[str] = None,
    dry_run: bool = True
) -> list[str]:
    """
    Scans a directory for files considered 'cosmic dust' based on age and patterns.

    Args:
        root_dir: The root directory to start scanning.
        min_age_days: Files older than this many days are considered dust.
        patterns: List of glob patterns to match filenames or directory names (e.g., ['*.log', '__pycache__']).
                  If None, all files older than min_age_days are considered.
        dry_run: If True, only report files; if False, actually delete them.

    Returns:
        A list of paths to identified dust files.
    """
    dust_files = []
    now = datetime.now()
    cutoff_time = now - timedelta(days=min_age_days)

    print(f"Scanning '{root_dir}' for cosmic dust...")
    print(f"Considering files older than {min_age_days} days (before {cutoff_time.strftime('%Y-%m-%d %H:%M:%S')}).")
    if patterns:
        print(f"Matching patterns: {', '.join(patterns)}")
    else:
        print("No specific patterns provided; considering all files older than the age cutoff.")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude common VCS directories and the utility's own directory
        dirnames[:] = [d for d in dirnames if d not in ['.git', '.svn', '.hg', 'node_modules', 'venv', 'env']]

        # Check if the current directory itself matches a pattern (e.g., '__pycache__')
        current_dir_name = os.path.basename(dirpath)
        is_dir_pattern_match = False
        if patterns:
            for pattern in patterns:
                if fnmatch.fnmatch(current_dir_name, pattern):
                    is_dir_pattern_match = True
                    break

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # Get modification time
                mtime_timestamp = os.path.getmtime(file_path)
                mtime_datetime = datetime.fromtimestamp(mtime_timestamp)

                is_old_enough = mtime_datetime < cutoff_time
                is_file_pattern_match = False

                if patterns:
                    for pattern in patterns:
                        if fnmatch.fnmatch(filename, pattern):
                            is_file_pattern_match = True
                            break
                else:
                    # If no patterns, all files older than min_age_days are candidates
                    is_file_pattern_match = True

                # A file is dust if it's old AND (its filename matches a pattern OR its parent directory matches a pattern)
                if is_old_enough and (is_file_pattern_match or is_dir_pattern_match):
                    dust_files.append(file_path)

            except OSError as e:
                print(f"Warning: Could not access '{file_path}': {e}")
                continue

    if dust_files:
        print(f"\nIdentified {len(dust_files)} pieces of cosmic dust:")
        for f in dust_files:
            print(f"  - {f}")
        if not dry_run:
            print("\nInitiating cosmic dust removal...")
            for f in dust_files:
                try:
                    os.remove(f)
                    print(f"  Removed: {f}")
                except OSError as e:
                    print(f"  Error removing '{f}': {e}")
            print("Cosmic dust removal complete.")
        else:
            print("\nThis was a dry run. To actually delete files, run with the '--delete' flag.")
    else:
        print("No cosmic dust found. Your repository is sparkling clean!")

    return dust_files


def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Collector: Scans and cleans up old/temporary files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning for dust."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Only consider files older than this many days. Default is 30."
    )
    parser.add_argument(
        "--patterns",
        nargs='*', # 0 or more arguments
        default=None,
        help="One or more glob patterns (e.g., '*.log', 'temp_*', '__pycache__') to match against filenames or directory names."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If present, actually delete the identified dust files. Use with caution!"
    )

    args = parser.parse_args()

    find_dust_files(
        root_dir=args.path,
        min_age_days=args.age,
        patterns=args.patterns,
        dry_run=not args.delete
    )


if __name__ == "__main__":
    main()
