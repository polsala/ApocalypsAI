import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """
    Calculates the age of a file in days.
    Returns -1 if the file does not exist or its modification time cannot be retrieved.
    """
    try:
        mod_timestamp = os.path.getmtime(filepath)
        mod_datetime = datetime.fromtimestamp(mod_timestamp)
        current_datetime = datetime.now()
        age = current_datetime - mod_datetime
        return age.days
    except (FileNotFoundError, OSError):
        return -1

def find_old_files(directory, days_threshold, recursive=False, verbose=False):
    """
    Finds files in a directory (and optionally its subdirectories) older than days_threshold.
    Returns a list of file paths.
    """
    old_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath): # Ensure it's a file, not a broken symlink or directory
                age = get_file_age_days(filepath)
                if age >= days_threshold:
                    old_files.append(filepath)
                    if verbose:
                        print(f"Found old file: {filepath} (Age: {age} days)")
                elif verbose:
                    print(f"Skipping recent file: {filepath} (Age: {age} days)")
        if not recursive:
            break # Only process the top directory if not recursive
    return old_files

def delete_files(file_paths, dry_run=True, verbose=False):
    """
    Deletes a list of files. If dry_run is True, only prints what would be deleted.
    """
    if not file_paths:
        print("No old files found to process.")
        return

    action_word = "Would delete" if dry_run else "Deleting"
    print(f"\n--- {action_word} {len(file_paths)} file(s) ---")

    for filepath in file_paths:
        try:
            if dry_run:
                print(f"[DRY RUN] {action_word}: {filepath}")
            else:
                os.remove(filepath)
                print(f"{action_word}: {filepath}")
        except OSError as e:
            print(f"Error {action_word.lower()} {filepath}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Cleans up old files in a directory."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The directory to scan for old files."
    )
    parser.add_argument(
        "--days",
        type=int,
        required=True,
        help="Files older than this many days will be considered 'dust'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, only list files that would be deleted, without actually deleting them."
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="If present, scan subdirectories as well."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="If present, print more detailed output about files being processed."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory '{args.path}' not found.")
        exit(1)

    if args.days < 0:
        print("Error: --days must be a non-negative integer.")
        exit(1)

    print(f"Scanning '{args.path}' for files older than {args.days} days (recursive: {args.recursive})...")
    old_files = find_old_files(args.path, args.days, args.recursive, args.verbose)

    if old_files:
        print(f"Found {len(old_files)} file(s) considered 'cosmic dust'.")
        delete_files(old_files, args.dry_run, args.verbose)
    else:
        print("No cosmic dust found. Your digital space is pristine!")

if __name__ == "__main__":
    main()
