import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def find_dust_bunnies(
    path: str,
    age_days: int,
    patterns: list[str]
) -> list[str]:
    """
    Finds files in the given path that are older than age_days and match any of the patterns.
    """
    dust_bunnies = []
    cutoff_time = datetime.now() - timedelta(days=age_days)

    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Get modification time
                mod_timestamp = os.path.getmtime(file_path)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)

                if mod_datetime < cutoff_time:
                    # Check if file matches any pattern
                    for pattern in patterns:
                        if fnmatch.fnmatch(file_name, pattern):
                            dust_bunnies.append(file_path)
                            break # Found a match, no need to check other patterns for this file
            except OSError as e:
                print(f"Warning: Could not access {file_path}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred with {file_path}: {e}")
    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Data Dust-Bunny Sweeper: Cleans old, unused, or temporary files."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The root directory to start scanning from. Defaults to current working directory."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=30,
        help="Files older than this many days will be considered 'dust bunnies'. Defaults to 30 days."
    )
    parser.add_argument(
        "--patterns",
        type=str,
        default="*.tmp,*.log,*.bak,~*",
        help="A comma-separated list of glob patterns to match against filenames. Defaults to '*.tmp,*.log,*.bak,~*'."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="If present, identified files will be deleted. Use with caution!"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, the utility will only report files and will not delete anything, even if --clean is specified. This is the default behavior if --clean is not provided."
    )

    args = parser.parse_args()

    patterns_list = [p.strip() for p in args.patterns.split(',')]

    print(f"Scanning '{args.path}' for files older than {args.age_days} days matching patterns: {', '.join(patterns_list)}")

    dust_bunnies = find_dust_bunnies(args.path, args.age_days, patterns_list)

    if not dust_bunnies:
        print("No dust bunnies found! Your directory is sparkling clean.")
        return

    print(f"\nFound {len(dust_bunnies)} dust bunnies:")
    for bunny in dust_bunnies:
        print(f"  - {bunny}")

    if args.dry_run or not args.clean:
        print("\nThis was a DRY RUN. No files were deleted.")
        print("To delete these files, run again with the '--clean' flag (and without '--dry-run').")
    else:
        print("\nInitiating cleanup...")
        deleted_count = 0
        for bunny in dust_bunnies:
            try:
                os.remove(bunny)
                print(f"  Deleted: {bunny}")
                deleted_count += 1
            except OSError as e:
                print(f"  Error deleting {bunny}: {e}")
        print(f"\nCleanup complete. Successfully deleted {deleted_count} files.")

if __name__ == "__main__":
    main()
