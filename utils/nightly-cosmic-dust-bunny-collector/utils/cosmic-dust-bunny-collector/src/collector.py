import os
import argparse
import fnmatch
from datetime import datetime, timedelta

def find_dust_bunnies(directory, age_days, patterns=None):
    """
    Finds files in the given directory that are older than age_days
    and optionally match any of the provided patterns.
    """
    dust_bunnies = []
    now = datetime.now()
    cutoff_time = now - timedelta(days=age_days)

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist or is not a directory.")
        return []

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                # Get modification time in seconds since the epoch
                mod_timestamp = os.path.getmtime(filepath)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)

                # Check age
                if mod_datetime < cutoff_time:
                    # Check patterns if provided
                    if patterns:
                        if any(fnmatch.fnmatch(filename, p) for p in patterns):
                            dust_bunnies.append(filepath)
                    else:
                        # No patterns, just age check
                        dust_bunnies.append(filepath)
            except OSError as e:
                print(f"Warning: Could not access file '{filepath}': {e}")
                continue
    return dust_bunnies

def clean_dust_bunnies(files_to_clean, dry_run=True):
    """
    Prints or deletes the list of files.
    """
    if not files_to_clean:
        print("No cosmic dust bunnies found to clean.")
        return

    mode = "[DRY RUN] Would delete:" if dry_run else "Deleting:"
    print(f"\n{mode}")
    for filepath in files_to_clean:
        print(f"  - {filepath}")
        if not dry_run:
            try:
                os.remove(filepath)
                print(f"    Successfully deleted: {filepath}")
            except OSError as e:
                print(f"    Error deleting '{filepath}': {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Collector: Clean up old files."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory to clean."
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="Files older than this many days will be considered 'dust bunnies'."
    )
    parser.add_argument(
        "--patterns",
        nargs='*', # 0 or more arguments
        default=None,
        help="One or more glob-style patterns (e.g., *.log, temp_*) to filter files."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If present, files will actually be deleted. Use with caution!"
    )

    args = parser.parse_args()

    print(f"Searching for cosmic dust bunnies in '{args.directory}' older than {args.age} days...")
    if args.patterns:
        print(f"  Filtered by patterns: {', '.join(args.patterns)}")

    dust_bunnies = find_dust_bunnies(args.directory, args.age, args.patterns)

    if dust_bunnies:
        print(f"Found {len(dust_bunnies)} cosmic dust bunnies.")
        clean_dust_bunnies(dust_bunnies, dry_run=not args.delete)
    else:
        print("No cosmic dust bunnies found matching criteria.")

if __name__ == "__main__":
    main()
