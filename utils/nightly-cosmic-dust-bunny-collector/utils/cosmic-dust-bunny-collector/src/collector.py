import os
import time
import argparse
from datetime import datetime, timedelta
import fnmatch

def find_dust_bunnies(
    directory: str,
    age_days: int,
    exclude_patterns: list[str] = None
) -> list[str]:
    """
    Scans a directory recursively for files older than a specified age.

    Args:
        directory: The root directory to scan.
        age_days: The age threshold in days. Files older than this are 'dust bunnies'.
        exclude_patterns: A list of glob patterns to exclude files/directories.

    Returns:
        A list of file paths identified as dust bunnies.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory not found: {directory}")
        return []

    dust_bunnies = []
    now = time.time()
    age_threshold_timestamp = now - (age_days * 24 * 60 * 60)

    for root, dirnames, filenames in os.walk(directory):
        # Filter out excluded directories before processing their contents
        # Create a copy of dirnames to modify it during iteration
        dirnames_copy = dirnames[:]
        for d in dirnames_copy:
            full_dir_path = os.path.join(root, d)
            if any(fnmatch.fnmatch(full_dir_path, p) for p in (exclude_patterns or [])):
                dirnames.remove(d) # Remove from the list os.walk uses for recursion

        for filename in filenames:
            file_path = os.path.join(root, filename)

            # Check if file_path matches any exclude pattern
            if any(fnmatch.fnmatch(file_path, p) for p in (exclude_patterns or [])):
                continue

            try:
                # Use getmtime (modification time) as a common indicator of 'staleness'
                # For more advanced use, could also consider getatime (access time) or getctime (creation time)
                mod_time = os.path.getmtime(file_path)
                if mod_time < age_threshold_timestamp:
                    dust_bunnies.append(file_path)
            except OSError as e:
                print(f"Warning: Could not access file {file_path}: {e}")

    return dust_bunnies

def collect_dust_bunnies(file_paths: list[str], dry_run: bool = True):
    """
    Prints or deletes the identified dust bunnies.

    Args:
        file_paths: A list of file paths to process.
        dry_run: If True, only print. If False, delete files.
    """
    if not file_paths:
        print("\n✨ No cosmic dust bunnies found! Your digital space is pristine. ✨")
        return

    action = "would be collected (deleted)" if dry_run else "are being collected (deleted)"
    print(f"\n🌌 Identified {len(file_paths)} cosmic dust bunnies that {action}:")

    for path in file_paths:
        print(f"  - {path}")
        if not dry_run:
            try:
                os.remove(path)
                print(f"    [COLLECTED] {path}")
            except OSError as e:
                print(f"    [ERROR] Failed to collect {path}: {e}")

    if not dry_run:
        print("\n🧹 Collection complete! Your digital realm is a bit cleaner. 🧹")
    else:
        print("\n💡 Run with `--collect` to permanently remove these files. 💡")


def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Collector: Find and optionally remove stale files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for dust bunnies."
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="Files older than this many days will be flagged as dust bunnies."
    )
    parser.add_argument(
        "--collect",
        action="store_true",
        help="Add this flag to actually delete the identified files. Use with caution!"
    )
    parser.add_argument(
        "--exclude",
        type=str,
        action="append",
        default=[],
        help="Glob patterns (e.g., '*.log', 'temp_dir/*') to exclude files or directories from scanning. Can be repeated."
    )

    args = parser.parse_args()

    print(f"\nScanning '{args.path}' for files older than {args.age} days...")
    dust_bunnies = find_dust_bunnies(args.path, args.age, args.exclude)
    collect_dust_bunnies(dust_bunnies, dry_run=not args.collect)


if __name__ == "__main__":
    main()
