import os
import time
import argparse
from datetime import datetime, timedelta

def collect_dust(
    path: str,
    min_age_days: int = 30,
    min_size_mb: int = 10,
    file_extensions: list[str] = None,
    dry_run: bool = True
) -> list[str]:
    """
    Identifies and optionally cleans up 'digital dust' (old, large, or specific file types)
    in a given directory.

    Args:
        path (str): The root directory to start scanning from.
        min_age_days (int): Only consider files older than this many days.
        min_size_mb (int): Only consider files larger than this many megabytes.
        file_extensions (list[str]): List of file extensions to target (e.g., ['log', 'tmp']).
        dry_run (bool): If True, only report files; otherwise, delete them.

    Returns:
        list[str]: A list of paths to files that were identified/cleaned.
    """
    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a valid directory.")
        return []

    print(f"\n--- Cosmic Dust Collector {'(DRY RUN)' if dry_run else '(CLEANING)'} ---")
    print(f"Scanning: {path}")
    print(f"Criteria: Older than {min_age_days} days, Larger than {min_size_mb} MB")
    if file_extensions:
        print(f"Targeting extensions: {', '.join(file_extensions)}")
    print("--------------------------------------------------")

    cleaned_files = []
    current_time = time.time()
    age_threshold_timestamp = current_time - (min_age_days * 24 * 60 * 60)
    size_threshold_bytes = min_size_mb * 1024 * 1024

    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_stat = os.stat(file_path)
                file_mtime = file_stat.st_mtime
                file_size = file_stat.st_size
                file_ext = os.path.splitext(file)[1].lstrip('.').lower()

                is_old = file_mtime < age_threshold_timestamp
                is_large = file_size > size_threshold_bytes
                is_targeted_ext = not file_extensions or (file_ext in [ext.lower() for ext in file_extensions])

                if is_old and is_large and is_targeted_ext:
                    action = "[DRY RUN] Would delete" if dry_run else "[DELETING]"
                    print(f"{action}: {file_path} (Age: {datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d')}, Size: {file_size / (1024*1024):.2f} MB)")
                    cleaned_files.append(file_path)

                    if not dry_run:
                        os.remove(file_path)

            except OSError as e:
                print(f"Warning: Could not access {file_path} - {e}")
            except Exception as e:
                print(f"An unexpected error occurred with {file_path} - {e}")

    print("--------------------------------------------------")
    print(f"{'Identified' if dry_run else 'Cleaned'} {len(cleaned_files)} files.")
    print("--------------------------------------------------")
    return cleaned_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Collector: Identify and clean up old/large/specific files."
    )
    parser.add_argument("path", type=str, help="The root directory to start scanning from.")
    parser.add_argument(
        "--min-age-days",
        type=int,
        default=30,
        help="Only consider files older than this many days (default: 30)."
    )
    parser.add_argument(
        "--min-size-mb",
        type=int,
        default=10,
        help="Only consider files larger than this many megabytes (default: 10)."
    )
    parser.add_argument(
        "--extensions",
        type=str,
        help="Comma-separated list of file extensions to target (e.g., log,tmp,bak)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, only report files; do not delete them."
    )

    args = parser.parse_args()

    extensions_list = None
    if args.extensions:
        extensions_list = [ext.strip().lower() for ext in args.extensions.split(',')]

    collect_dust(
        path=args.path,
        min_age_days=args.min_age_days,
        min_size_mb=args.min_size_mb,
        file_extensions=extensions_list,
        dry_run=args.dry_run
    )
