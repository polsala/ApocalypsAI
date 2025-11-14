import os
import time
import argparse

def collect_dust(directory, age_threshold_days, dry_run=True):
    """Scans a directory for files older than age_threshold_days and optionally deletes them.

    Args:
        directory (str): The path to the directory to scan.
        age_threshold_days (int): Files older than this many days will be targeted.
        dry_run (bool): If True, only list files; if False, delete them.

    Returns:
        list: A list of paths to files that were identified/deleted.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found or is not a directory.")
        return []

    print(f"\n--- Initiating Cosmic Dust Collection in '{directory}' ---")
    print(f"Targeting files older than {age_threshold_days} days. {'(Dry Run)' if dry_run else '(DELETION MODE)'}")

    collected_files = []
    current_time = time.time()
    threshold_timestamp = current_time - (age_threshold_days * 24 * 60 * 60)

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                # Use os.path.getmtime for modification time
                file_mtime = os.path.getmtime(filepath)
                if file_mtime < threshold_timestamp:
                    collected_files.append(filepath)
            except OSError as e:
                print(f"Warning: Could not access file '{filepath}': {e}")

    if not collected_files:
        print("No cosmic dust found. Your systems are remarkably clean... for now.")
        return []

    print(f"\nIdentified {len(collected_files)} pieces of cosmic dust:")
    for f in collected_files:
        print(f"  - {f}")

    if not dry_run:
        print("\n--- Purging Cosmic Dust ---")
        deleted_count = 0
        for f in collected_files:
            try:
                os.remove(f)
                print(f"  [PURGED] {f}")
                deleted_count += 1
            except OSError as e:
                print(f"  [FAILED] Could not purge '{f}': {e}")
        print(f"\nSuccessfully purged {deleted_count} pieces of cosmic dust.")
    else:
        print("\n(To actually purge these files, run with the '--delete' flag.)")

    print("--- Cosmic Dust Collection Complete ---")
    return collected_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Collector: Identify and optionally remove old files."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to scan for cosmic dust."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Minimum age in days for a file to be considered cosmic dust (default: 30)."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If set, identified files will be permanently deleted. Use with caution!"
    )

    args = parser.parse_args()

    collect_dust(args.directory, args.age, dry_run=not args.delete)
