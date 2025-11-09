import os
import time
import argparse
from datetime import datetime, timedelta

def find_old_files(directory, age_days):
    """
    Recursively finds files in a directory older than a specified age.
    Returns a list of (filepath, age_in_days).
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory not found: {directory}")
        return []

    old_files = []
    now = datetime.now()
    cutoff_time = now - timedelta(days=age_days)

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                # getmtime returns a float representing seconds since the epoch
                mod_timestamp = os.path.getmtime(filepath)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)

                if mod_datetime < cutoff_time:
                    age = (now - mod_datetime).days
                    old_files.append((filepath, age))
            except OSError as e:
                print(f"Warning: Could not access file {filepath}: {e}")
                continue
    return old_files

def delete_files(file_list, dry_run=True, confirm_delete=False, force_delete=False):
    """
    Deletes files from the given list, respecting dry_run, confirm_delete, and force_delete flags.
    """
    if not file_list:
        print("No digital dust bunnies found. Your digital space is pristine!")
        return

    print(f"Found {len(file_list)} digital dust bunnies older than the specified age.")

    if dry_run and not force_delete:
        print("\n--- Dry Run Mode --- (No files will be deleted) ---")
        for filepath, age in file_list:
            print(f"[DRY RUN] Would delete: {filepath} (Age: {age} days)")
        print("--------------------------------------------------")
        return

    if force_delete:
        print("\n--- Force Delete Mode --- (Deleting without confirmation) ---")
        for filepath, age in file_list:
            try:
                os.remove(filepath)
                print(f"Deleted: {filepath} (Age: {age} days)")
            except OSError as e:
                print(f"Error deleting {filepath}: {e}")
        print("--------------------------------------------------")
        return

    # Interactive deletion
    print("\n--- Interactive Deletion Mode ---")
    for filepath, age in file_list:
        response = input(f"Delete '{filepath}' (Age: {age} days)? [y/N]: ").lower()
        if response == 'y':
            try:
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            except OSError as e:
                print(f"Error deleting {filepath}: {e}")
        else:
            print(f"Skipped: {filepath}")
    print("--------------------------------------------------")

def main():
    parser = argparse.ArgumentParser(
        description="Identify and optionally remove old, unused files (digital 'dust bunnies')."
    )
    parser.add_argument(
        "--directory",
        required=True,
        help="The root directory to scan for old files."
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="The minimum age in days for a file to be considered a 'dust bunny'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only list files that would be deleted, without actually deleting them. Default if no other delete flag is used."
    )
    parser.add_argument(
        "--confirm-delete",
        action="store_true",
        help="Prompt for confirmation before deleting each file. Ignored if --force-delete is used."
    )
    parser.add_argument(
        "--force-delete",
        action="store_true",
        help="Delete all identified files without prompting. Use with extreme caution! Overrides --dry-run and --confirm-delete."
    )

    args = parser.parse_args()

    # Determine deletion mode precedence
    dry_run_mode = True # Default to dry run
    confirm_delete_mode = False
    force_delete_mode = False

    if args.force_delete:
        force_delete_mode = True
        dry_run_mode = False
        confirm_delete_mode = False # Ensure confirm is off if force is on
    elif args.confirm_delete:
        confirm_delete_mode = True
        dry_run_mode = False
    elif args.dry_run:
        dry_run_mode = True
    # Else: if no flags are set, dry_run_mode remains True by default

    old_files = find_old_files(args.directory, args.age)
    delete_files(old_files, dry_run=dry_run_mode, confirm_delete=confirm_delete_mode, force_delete=force_delete_mode)

if __name__ == "__main__":
    main()
