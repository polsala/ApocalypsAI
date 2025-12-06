import os
import time
import argparse
from datetime import datetime, timedelta

def get_old_files(directory: str, age_days: int) -> list[str]:
    """
    Scans a directory recursively and returns a list of files older than age_days.
    """
    old_files = []
    cutoff_timestamp = (datetime.now() - timedelta(days=age_days)).timestamp()

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Get last modification time
                mod_time = os.path.getmtime(file_path)
                if mod_time < cutoff_timestamp:
                    old_files.append(file_path)
            except OSError as e:
                print(f"Warning: Could not access file {file_path}: {e}")
                continue
    return old_files

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Digital Detritus Disposer - Clean up old files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for old files."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Files older than this many days will be considered detritus (default: 30)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only list files, do not delete (default if --delete is not specified)."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete the identified files. Use with caution!"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory '{args.path}' does not exist or is not a directory.")
        exit(1)

    if args.dry_run and args.delete:
        print("Error: Cannot use --dry-run and --delete together. Choose one.")
        exit(1)

    print(f"\nScanning '{args.path}' for files older than {args.age} days...")
    old_files = get_old_files(args.path, args.age)

    if not old_files:
        print("No digital detritus found! Your filesystem is sparkling clean. ✨")
        exit(0)

    print(f"\nFound {len(old_files)} pieces of digital detritus:")
    for file_path in old_files:
        print(f"  - {file_path}")

    if args.delete:
        print("\nInitiating detritus disposal... (This cannot be undone!)")
        for file_path in old_files:
            try:
                os.remove(file_path)
                print(f"  🗑️ Deleted: {file_path}")
            except OSError as e:
                print(f"  ❌ Error deleting {file_path}: {e}")
        print("\nDetritus disposal complete. Your filesystem thanks you! 💖")
    elif args.dry_run or (not args.dry_run and not args.delete): # Default to dry-run if neither is specified
        print("\nThis was a DRY RUN. No files were deleted.")
        print("To delete these files, run again with the --delete flag. Use with caution!")

if __name__ == "__main__":
    main()
