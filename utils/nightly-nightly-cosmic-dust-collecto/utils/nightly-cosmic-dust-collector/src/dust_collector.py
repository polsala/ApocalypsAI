import os
import argparse
import datetime
import time
from typing import List, Tuple

def find_cosmic_dust(
    target_path: str,
    min_age_days: int = 30,
) -> List[Tuple[str, str]]:
    """
    Scans the target_path for files considered 'cosmic dust'.
    Cosmic dust includes:
    - Empty files (0 bytes).
    - Files not modified for at least min_age_days.

    Args:
        target_path (str): The directory to scan.
        min_age_days (int): Minimum age in days for a file to be considered old.

    Returns:
        List[Tuple[str, str]]: A list of (file_path, reason) tuples for identified dust.
    """
    dust_files: List[Tuple[str, str]] = []
    now = time.time()
    age_threshold_timestamp = now - (min_age_days * 24 * 60 * 60)

    if not os.path.isdir(target_path):
        print(f"Error: Path '{target_path}' is not a valid directory.")
        return []

    for root, _, files in os.walk(target_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                if not os.path.isfile(file_path):
                    continue

                file_size = os.path.getsize(file_path)
                file_mtime = os.path.getmtime(file_path)

                if file_size == 0:
                    dust_files.append((file_path, "Empty file"))
                elif file_mtime < age_threshold_timestamp:
                    # Only add if not already marked as empty
                    if (file_path, "Empty file") not in dust_files:
                        modified_date = datetime.datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d')
                        dust_files.append((file_path, f"Older than {min_age_days} days (last modified: {modified_date})"))

            except OSError as e:
                print(f"Warning: Could not access '{file_path}': {e}")
            except Exception as e:
                print(f"An unexpected error occurred with file '{file_path}': {e}")

    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Find and manage old/empty files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning for cosmic dust."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Files not modified for this many days or more will be considered old dust. Default is 30 days."
    )
    parser.add_argument(
        "--action",
        type=str,
        choices=["list", "delete"],
        default="list",
        help="Action to perform: 'list' (default) to show files, 'delete' to remove them."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="When used with --action delete, shows what would be deleted without actual deletion."
    )

    args = parser.parse_args()

    print(f"🌌 Scanning '{args.path}' for cosmic dust (min age: {args.age} days)...")
    dust_files = find_cosmic_dust(args.path, args.age)

    if not dust_files:
        print("✨ No cosmic dust found. Your repository is sparkling clean!")
        return

    print(f"\n--- Identified Cosmic Dust ({len(dust_files)} files) ---")
    for file_path, reason in dust_files:
        print(f"- {file_path} ({reason})")

    if args.action == "delete":
        if args.dry_run:
            print("\n--- DRY RUN: Files listed above WOULD BE DELETED ---")
            print("To actually delete, run without --dry-run.")
        else:
            print("\n--- Deleting Cosmic Dust ---")
            for file_path, _ in dust_files:
                try:
                    os.remove(file_path)
                    print(f"🗑️ Deleted: {file_path}")
                except OSError as e:
                    print(f"❌ Error deleting '{file_path}': {e}")
            print("\nDeletion process complete.")
    else: # args.action == "list"
        print("\n--- Listing Complete ---")
        print("To delete these files, run with '--action delete' (consider '--dry-run' first!).")

if __name__ == "__main__":
    main()
