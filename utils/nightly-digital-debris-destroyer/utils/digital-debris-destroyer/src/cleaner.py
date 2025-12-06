import os
import argparse
import fnmatch
import shutil
from datetime import datetime, timedelta

def find_and_delete_old_debris(
    root_path: str,
    patterns: list[str],
    age_days: int,
    dry_run: bool = True
) -> tuple[list[str], list[str]]:
    """
    Finds and optionally deletes files and directories matching patterns and age criteria.

    Args:
        root_path: The root directory to start scanning.
        patterns: A list of glob patterns to match files/directories.
        age_days: The minimum age in days for an item to be considered old.
        dry_run: If True, only report what would be deleted; otherwise, perform deletion.

    Returns:
        A tuple containing two lists: (deleted_items, skipped_items).
    """
    cutoff_time = datetime.now() - timedelta(days=age_days)
    found_items = []
    deleted_items = []
    skipped_items = []

    print(f"Scanning '{root_path}' for debris older than {age_days} days...")

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False): # topdown=False for safe dir deletion
        # Check files
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if not os.path.exists(full_path): # Skip if file was already deleted as part of a parent directory
                continue
            for pattern in patterns:
                if fnmatch.fnmatch(filename, pattern):
                    try:
                        mod_time = datetime.fromtimestamp(os.path.getmtime(full_path))
                        if mod_time < cutoff_time:
                            found_items.append(full_path)
                            if dry_run:
                                print(f"[DRY RUN] Would delete old file: {full_path} (Modified: {mod_time.strftime('%Y-%m-%d')})")
                            else:
                                try:
                                    os.remove(full_path)
                                    deleted_items.append(full_path)
                                    print(f"Deleted old file: {full_path} (Modified: {mod_time.strftime('%Y-%m-%d')})")
                                except OSError as e:
                                    skipped_items.append(full_path)
                                    print(f"Error deleting file {full_path}: {e}")
                            break # Matched a pattern, move to next file
                    except FileNotFoundError:
                        # File might have been deleted by another process or part of a parent dir deletion
                        pass

        # Check directories
        # We iterate dirnames in reverse to safely remove from the list if deleted
        for i in range(len(dirnames) - 1, -1, -1):
            dirname = dirnames[i]
            full_path = os.path.join(dirpath, dirname)
            if not os.path.exists(full_path): # Skip if dir was already deleted as part of a parent directory
                continue
            for pattern in patterns:
                # Check if the directory name itself matches, or if it's a directory pattern like 'dist/'
                if fnmatch.fnmatch(dirname, pattern) or fnmatch.fnmatch(dirname + '/', pattern):
                    try:
                        mod_time = datetime.fromtimestamp(os.path.getmtime(full_path))
                        if mod_time < cutoff_time:
                            found_items.append(full_path)
                            if dry_run:
                                print(f"[DRY RUN] Would delete old directory: {full_path} (Modified: {mod_time.strftime('%Y-%m-%d')})")
                            else:
                                try:
                                    shutil.rmtree(full_path)
                                    deleted_items.append(full_path)
                                    print(f"Deleted old directory: {full_path} (Modified: {mod_time.strftime('%Y-%m-%d')})")
                                    # Remove from dirnames so os.walk doesn't try to enter it
                                    del dirnames[i]
                                except OSError as e:
                                    skipped_items.append(full_path)
                                    print(f"Error deleting directory {full_path}: {e}")
                            break # Matched a pattern, move to next directory
                    except FileNotFoundError:
                        # Directory might have been deleted by another process
                        pass

    if dry_run:
        print("\n--- DRY RUN COMPLETE ---")
        if found_items:
            print(f"Found {len(found_items)} items that would be deleted:")
            for item in found_items:
                print(f"  - {item}")
        else:
            print("No old debris found matching criteria.")
    else:
        print("\n--- DELETION COMPLETE ---")
        if deleted_items:
            print(f"Successfully deleted {len(deleted_items)} items.")
        else:
            print("No old debris found or deleted matching criteria.")
        if skipped_items:
            print(f"Skipped {len(skipped_items)} items due to errors.")

    return deleted_items, skipped_items


def main():
    parser = argparse.ArgumentParser(
        description="Digital Debris Destroyer: Cleans up old files and directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning for debris."
    )
    parser.add_argument(
        "--patterns",
        nargs='+',
        required=True,
        help="One or more glob patterns to match files or directories (e.g., '*.log', '__pycache__')."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        required=True,
        help="The minimum age in days for a file or directory to be considered 'old'."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If provided, actually delete the matched files/directories. Use with caution!"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: The specified path '{args.path}' is not a valid directory.")
        exit(1)

    find_and_delete_old_debris(args.path, args.patterns, args.age_days, not args.delete)


if __name__ == "__main__":
    main()
