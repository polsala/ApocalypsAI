import os
import shutil
import argparse
import datetime
import time

# Common temporary file patterns
TEMP_PATTERNS = [
    '.tmp', '.temp', '~', '.bak', '.swp', '.old', '.orig',
    '#',  # e.g., #file.txt#
    '._', # e.g., ._file.txt (macOS resource forks)
]

def _is_temp_file(filename):
    """Checks if a filename matches common temporary file patterns."""
    filename_lower = filename.lower()
    for pattern in TEMP_PATTERNS:
        if pattern.startswith('#') and filename_lower.startswith(pattern):
            return True
        if pattern.endswith('#') and filename_lower.endswith(pattern):
            return True
        if pattern in filename_lower:
            return True
    return False

def _is_dusty(filepath, age_threshold_days, size_threshold_kb, current_time):
    """Determines if a file is 'cosmic dust' based on defined criteria."""
    try:
        stat_info = os.stat(filepath)
        file_size = stat_info.st_size  # in bytes
        mod_time = stat_info.st_mtime  # in seconds since epoch

        # 1. Empty files
        if file_size == 0:
            return True, "empty file"

        # 2. Aged small files
        age_seconds = current_time - mod_time
        age_days = age_seconds / (60 * 60 * 24)

        if age_days > age_threshold_days and file_size < (size_threshold_kb * 1024):
            return True, f"old ({int(age_days)} days) and small ({file_size} bytes)"

        # 3. Temporary pattern files
        if _is_temp_file(os.path.basename(filepath)):
            return True, "temporary pattern file"

    except OSError:
        # File might have been deleted between os.walk and os.stat
        pass

    return False, ""

def collect_dust(
    target_dir: str,
    quarantine_dir: str,
    age_threshold_days: int = 90,
    size_threshold_kb: int = 1,
    dry_run: bool = False
):
    """Scans a directory for 'cosmic dust' and optionally quarantines them."""
    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist or is not a directory.")
        return

    if not os.path.exists(quarantine_dir):
        print(f"Creating quarantine directory: {quarantine_dir}")
        os.makedirs(quarantine_dir)
    elif not os.path.isdir(quarantine_dir):
        print(f"Error: Quarantine path '{quarantine_dir}' exists but is not a directory.")
        return

    print(f"Scanning '{target_dir}' for cosmic dust...")
    print(f"  - Age threshold: {age_threshold_days} days")
    print(f"  - Size threshold: {size_threshold_kb} KB")
    print(f"  - Dry run: {dry_run}")

    dust_found = []
    current_time = time.time()

    for root, _, files in os.walk(target_dir):
        # Exclude the quarantine directory itself from being scanned
        if os.path.abspath(root).startswith(os.path.abspath(quarantine_dir)):
            continue

        for filename in files:
            filepath = os.path.join(root, filename)
            is_dust, reason = _is_dusty(filepath, age_threshold_days, size_threshold_kb, current_time)

            if is_dust:
                dust_found.append((filepath, reason))
                print(f"  [DUST] {filepath} ({reason})")

                if not dry_run:
                    try:
                        relative_path = os.path.relpath(filepath, target_dir)
                        dest_path = os.path.join(quarantine_dir, relative_path)
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        shutil.move(filepath, dest_path)
                        print(f"    -> Quarantined to {dest_path}")
                    except Exception as e:
                        print(f"    -> Failed to quarantine {filepath}: {e}")

    if not dust_found:
        print("No cosmic dust found. Your directories are sparkling clean!")
    else:
        action = "reported" if dry_run else "quarantined"
        print(f"\nSummary: {len(dust_found)} cosmic dust files {action}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scan directories for 'cosmic dust' and optionally quarantine them."
    )
    parser.add_argument(
        "--target-dir",
        type=str,
        required=True,
        help="The directory to scan for cosmic dust."
    )
    parser.add_argument(
        "--quarantine-dir",
        type=str,
        required=True,
        help="The directory where identified dust files will be moved."
    )
    parser.add_argument(
        "--age-threshold-days",
        type=int,
        default=90,
        help="Files older than this many days (and smaller than size-threshold-kb) are considered dust. Default: 90."
    )
    parser.add_argument(
        "--size-threshold-kb",
        type=int,
        default=1,
        help="Files smaller than this many KB (and older than age-threshold-days) are considered dust. Default: 1."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, the utility will only report files and will not move them."
    )

    args = parser.parse_args()

    collect_dust(
        target_dir=args.target_dir,
        quarantine_dir=args.quarantine_dir,
        age_threshold_days=args.age_threshold_days,
        size_threshold_kb=args.size_threshold_kb,
        dry_run=args.dry_run
    )
