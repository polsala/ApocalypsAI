import os
import argparse
import datetime
import sys

def find_empty_directories(path):
    """Finds all empty directories within the given path."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(path):
        # Check if the current directory itself is empty (no files and no subdirectories)
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def find_old_files(path, age_days):
    """Finds files older than 'age_days' within the given path."""
    old_files = []
    now = datetime.datetime.now()
    cutoff_time = now - datetime.timedelta(days=age_days)

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                # Get modification time (mtime) and convert to datetime object
                mtime_timestamp = os.path.getmtime(filepath)
                mtime_datetime = datetime.datetime.fromtimestamp(mtime_timestamp)

                if mtime_datetime < cutoff_time:
                    old_files.append(filepath)
            except OSError as e:
                print(f"Warning: Could not access file {filepath}: {e}", file=sys.stderr)
    return old_files

def confirm_action(prompt):
    """Asks the user for confirmation for an action."""
    while True:
        response = input(f"{prompt} (y/n): ").lower().strip()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Sweeper: Tidy up your digital realm."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory from which to begin the cosmic sweep."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only report what would be deleted, without making changes."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=30,
        help="Files older than this many days will be flagged for removal. (Default: 30)"
    )

    args = parser.parse_args()

    scan_path = os.path.abspath(args.path)

    if not os.path.isdir(scan_path):
        print(f"Error: Path '{scan_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print(f"\n--- Cosmic Dust Bunny Sweeper Initiated ---")
    print(f"Scanning: {scan_path}")
    print(f"Dry Run: {'Yes' if args.dry_run else 'No'}")
    print(f"Age Threshold: {args.age_days} days\n")

    # Find empty directories
    print("Searching for empty cosmic voids (directories)... ")
    empty_dirs = find_empty_directories(scan_path)
    if empty_dirs:
        print(f"Found {len(empty_dirs)} empty directories:")
        for d in empty_dirs:
            print(f"  - {d}")
    else:
        print("No empty cosmic voids found. Your space is tidy!")

    # Find old files
    print("\nSearching for ancient digital artifacts (old files)... ")
    old_files = find_old_files(scan_path, args.age_days)
    if old_files:
        print(f"Found {len(old_files)} files older than {args.age_days} days:")
        for f in old_files:
            print(f"  - {f}")
    else:
        print("No ancient digital artifacts found. All files are spry!")

    total_items_to_clean = len(empty_dirs) + len(old_files)

    if total_items_to_clean == 0:
        print("\nNo cosmic dust bunnies or empty voids found. Your system is pristine!")
        sys.exit(0)

    if args.dry_run:
        print(f"\nDry run complete. {total_items_to_clean} items would be cleaned.")
        sys.exit(0)

    print(f"\nTotal items to clean: {total_items_to_clean}")
    if not confirm_action("Proceed with actual deletion?"):
        print("Deletion cancelled. Your cosmic dust bunnies live to see another cycle.")
        sys.exit(0)

    print("\nInitiating cosmic cleansing...")
    deleted_count = 0

    # Delete old files first
    for f in old_files:
        try:
            os.remove(f)
            print(f"  [DELETED] File: {f}")
            deleted_count += 1
        except OSError as e:
            print(f"  [ERROR] Could not delete file {f}: {e}", file=sys.stderr)

    # Delete empty directories (re-check in case files were deleted from them)
    # To ensure proper deletion of nested empty dirs, we should sort them by path length (longest first).
    empty_dirs.sort(key=len, reverse=True) # Delete deepest first

    for d in empty_dirs:
        try:
            # Re-check if directory is still empty before attempting to remove
            if not os.listdir(d):
                os.rmdir(d)
                print(f"  [DELETED] Directory: {d}")
                deleted_count += 1
            else:
                print(f"  [SKIPPED] Directory not empty: {d}")
        except OSError as e:
            print(f"  [ERROR] Could not delete directory {d}: {e}", file=sys.stderr)

    print(f"\nCosmic cleansing complete! {deleted_count} items purged.")
    sys.exit(0)

if __name__ == "__main__":
    main()
