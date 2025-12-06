import os
import argparse
from datetime import datetime, timedelta

def get_file_info(filepath):
    """
    Retrieves modification time and size for a given file.
    Returns (mtime_timestamp, size_bytes) or (None, None) if file not found.
    """
    try:
        stat_info = os.stat(filepath)
        return stat_info.st_mtime, stat_info.st_size
    except FileNotFoundError:
        return None, None

def scan_directory(path, min_age_days, min_size_mb, current_time):
    """
    Scans a directory for files matching age and size criteria.
    Returns a list of (filepath, age_days, size_mb) tuples.
    """
    candidates = []
    min_size_bytes = min_size_mb * 1024 * 1024

    for root, _, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            mtime_timestamp, size_bytes = get_file_info(filepath)

            if mtime_timestamp is None or size_bytes is None:
                continue # Skip if file info can't be retrieved

            file_mtime = datetime.fromtimestamp(mtime_timestamp)
            age_timedelta = current_time - file_mtime
            age_days = age_timedelta.days

            size_mb = size_bytes / (1024 * 1024)

            if age_days >= min_age_days and size_mb >= min_size_bytes:
                candidates.append((filepath, age_days, size_mb))
    return candidates

def main():
    parser = argparse.ArgumentParser(
        description="Cataclysmic Cache Cleaner: Identifies old or large files for potential deletion."
    )
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="Directory to scan. Can be specified multiple times."
    )
    parser.add_argument(
        "--min-age",
        type=int,
        default=30,
        help="Minimum age in days for a file to be considered a candidate (default: 30)."
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=50,
        help="Minimum size in megabytes for a file to be considered a candidate (default: 50)."
    )

    args = parser.parse_args()

    print(f"Cataclysmic Cache Cleaner Report (Thresholds: Age >= {args.min_age} days, Size >= {args.min_size} MB)")
    print("-" * 80)

    all_candidates = []
    current_time = datetime.now() # Mocked in tests

    for path in args.path:
        if not os.path.isdir(path):
            print(f"Warning: Path '{path}' is not a valid directory. Skipping.")
            continue

        print(f"\nScanning: {path}")
        candidates = scan_directory(path, args.min_age, args.min_size, current_time)
        if not candidates:
            print("  No candidates found in this path.")
        for filepath, age_days, size_mb in candidates:
            print(f"  - {filepath} (Age: {age_days} days, Size: {size_mb:.1f} MB) - Candidate!")
            all_candidates.append((filepath, age_days, size_mb))

    print("-" * 80)
    print(f"Total Cataclysmic Candidates Found: {len(all_candidates)}")

if __name__ == "__main__":
    main()
