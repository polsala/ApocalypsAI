import os
import shutil
import argparse
import datetime
import sys

def find_empty_dirs(root_path):
    """Finds all empty directories within a given root path."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check if the current directory is empty (no files and no subdirectories)
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def find_old_temp_files(root_path, age_days, extensions):
    """Finds files with specified extensions older than age_days."""
    old_files = []
    cutoff_time = datetime.datetime.now() - datetime.timedelta(days=age_days)

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                filepath = os.path.join(dirpath, filename)
                try:
                    # Get modification time and convert to datetime object
                    mod_timestamp = os.path.getmtime(filepath)
                    mod_datetime = datetime.datetime.fromtimestamp(mod_timestamp)

                    if mod_datetime < cutoff_time:
                        old_files.append(filepath)
                except OSError as e:
                    print(f"Warning: Could not access file {filepath}: {e}", file=sys.stderr)
    return old_files

def delete_items(items, dry_run):
    """Deletes a list of files or directories, with a dry-run option."""
    if not items:
        print("No items to delete.")
        return

    print(f"{'[DRY RUN] ' if dry_run else ''}Attempting to {'identify' if dry_run else 'delete'} {len(items)} items...")

    for item in items:
        if dry_run:
            print(f"  Would delete: {item}")
        else:
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item) # Use rmtree for directories
                    print(f"  Deleted directory: {item}")
                else:
                    os.remove(item)
                    print(f"  Deleted file: {item}")
            except OSError as e:
                print(f"Error deleting {item}: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Sweeper: Cleans up empty directories and old temporary files."
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
        default=30,
        help="Minimum age in days for a temporary file to be considered old. Default: 30."
    )
    parser.add_argument(
        "--extensions",
        nargs='+',
        default=['.tmp', '.log', '.bak', '.old', '.swp'],
        help="Space-separated list of file extensions to consider temporary. Default: .tmp .log .bak .old .swp"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, only report what would be deleted without making changes."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning '{args.path}' for digital dust bunnies...")

    # Find empty directories
    empty_dirs = find_empty_dirs(args.path)
    if empty_dirs:
        print(f"Found {len(empty_dirs)} empty directories:")
        delete_items(empty_dirs, args.dry_run)
    else:
        print("No empty directories found.")

    # Find old temporary files
    old_temp_files = find_old_temp_files(args.path, args.age, args.extensions)
    if old_temp_files:
        print(f"\nFound {len(old_temp_files)} old temporary files (older than {args.age} days, extensions: {', '.join(args.extensions)}):")
        delete_items(old_temp_files, args.dry_run)
    else:
        print(f"No old temporary files found (older than {args.age} days, extensions: {', '.join(args.extensions)}).")

    print("\nDigital Dust Bunny Sweeper finished.")

if __name__ == "__main__":
    main()
