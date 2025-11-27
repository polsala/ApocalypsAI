import os
import time
import argparse
from datetime import datetime, timedelta

def collect_dust(path: str, age_days: int, dry_run: bool = True) -> list[str]:
    """
    Scans the given path for files older than age_days and returns a list of their paths.
    If not dry_run, it also deletes the files.
    """
    if not os.path.isdir(path):
        print(f"ERROR: Path '{path}' is not a valid directory.")
        return []

    dust_files = []
    cutoff_time = time.time() - (age_days * 24 * 60 * 60) # seconds

    print(f"Scanning '{path}' for cosmic dust older than {age_days} days...")
    print(f"Cutoff date: {datetime.fromtimestamp(cutoff_time).strftime('%Y-%m-%d %H:%M:%S')}")

    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Get last modification time
                mod_time = os.path.getmtime(file_path)
                if mod_time < cutoff_time:
                    dust_files.append(file_path)
            except OSError as e:
                print(f"WARNING: Could not access '{file_path}': {e}")

    if not dust_files:
        print("No cosmic dust found. Your digital space is pristine!")
        return []

    print(f"\nIdentified {len(dust_files)} pieces of cosmic dust:")
    for f in dust_files:
        print(f"  - {f}")

    if not dry_run:
        print("\nInitiating cosmic dust collection (deletion)...")
        deleted_count = 0
        for f in dust_files:
            try:
                os.remove(f)
                print(f"  - Jettisoned: {f}")
                deleted_count += 1
            except OSError as e:
                print(f"  - FAILED to jettison '{f}': {e}")
        print(f"\nSuccessfully jettisoned {deleted_count} pieces of cosmic dust.")
    else:
        print("\nThis was a dry run. No files were deleted. Use --delete to jettison cosmic dust.")

    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Identify and optionally remove old files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The directory to scan for old files."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        required=True,
        help="Files older than this many days will be flagged as 'cosmic dust'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a scan and report files that *would* be deleted, but don't actually delete anything. (Default if --delete is not present)"
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete the identified 'cosmic dust' files. Use with caution!"
    )

    args = parser.parse_args()

    # If --delete is present, it overrides --dry-run. If neither, dry_run is True.
    is_dry_run = not args.delete

    collect_dust(args.path, args.age_days, is_dry_run)

if __name__ == "__main__":
    main()
