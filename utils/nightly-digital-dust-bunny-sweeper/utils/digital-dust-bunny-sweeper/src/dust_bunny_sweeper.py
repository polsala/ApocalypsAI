import os
import argparse
import datetime
import time
import sys

DEFAULT_AGE_DAYS = 30
DEFAULT_EXTENSIONS = ['.log', '.tmp', '.bak']

def find_dust_bunnies(path, age_days, extensions):
    """
    Scans the given path for empty directories and old files.
    """
    empty_dirs = []
    old_files = []
    now = time.time()
    age_threshold_timestamp = now - (age_days * 24 * 60 * 60)

    print(f"\n🔍 Scanning '{path}' for digital dust bunnies...")

    for dirpath, dirnames, filenames in os.walk(path):
        # Check for empty directories
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)

        # Check for old files with specified extensions
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in extensions):
                file_path = os.path.join(dirpath, filename)
                try:
                    mtime = os.path.getmtime(file_path)
                    if mtime < age_threshold_timestamp:
                        old_files.append(file_path)
                except OSError as e:
                    print(f"⚠️ Could not access file '{file_path}': {e}")

    return empty_dirs, old_files

def sweep_dust_bunnies(empty_dirs, old_files, dry_run):
    """
    Deletes the identified empty directories and old files.
    """
    if dry_run:
        print("\n✨ Dry run complete! No actual sweeping was done. Here's what I *would* have swept:\n")
    else:
        print("\n🧹 Sweeping away the digital dust bunnies...\n")

    swept_count = 0

    # Delete old files first
    for f_path in old_files:
        try:
            if dry_run:
                print(f"  [DRY RUN] Would delete old file: {f_path}")
            else:
                os.remove(f_path)
                print(f"  Deleted old file: {f_path}")
                swept_count += 1
        except OSError as e:
            print(f"  ❌ Failed to delete file '{f_path}': {e}")

    # Delete empty directories (from deepest to shallowest to avoid issues)
    # Sorting in reverse order ensures we delete child directories before parents
    for d_path in sorted(empty_dirs, key=len, reverse=True):
        try:
            if dry_run:
                print(f"  [DRY RUN] Would delete empty directory: {d_path}")
            else:
                # Double-check if it's still empty after file deletions
                if not os.listdir(d_path):
                    os.rmdir(d_path)
                    print(f"  Deleted empty directory: {d_path}")
                    swept_count += 1
                else:
                    print(f"  Skipped non-empty directory: {d_path}")
        except OSError as e:
            print(f"  ❌ Failed to delete directory '{d_path}': {e}")

    if not dry_run:
        print(f"\n🎉 Sweeping complete! {swept_count} digital dust bunnies banished.")
    else:
        print("\n✨ Dry run finished. Ready for a real sweep when you are!")

def main():
    parser = argparse.ArgumentParser(
        description="A whimsical utility to sweep away digital 'dust bunnies' – old files and empty directories."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        required=True, 
        help='The root directory to start sweeping from.'
    )
    parser.add_argument(
        '--age', 
        type=int, 
        default=DEFAULT_AGE_DAYS, 
        help=f'Files older than this many days will be considered dust bunnies (default: {DEFAULT_AGE_DAYS}).'
    )
    parser.add_argument(
        '--extensions', 
        nargs='*', 
        default=DEFAULT_EXTENSIONS, 
        help=f'File extensions to target for deletion (default: {" ".join(DEFAULT_EXTENSIONS)}).'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help='Perform a scan and report, but do not delete any files or directories.'
    )
    parser.add_argument(
        '--force', 
        action='store_true', 
        help='Skip interactive confirmation and proceed with deletion immediately.'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.")
        sys.exit(1)

    empty_dirs, old_files = find_dust_bunnies(args.path, args.age, args.extensions)

    total_bunnies = len(empty_dirs) + len(old_files)

    if total_bunnies == 0:
        print("\n🥳 Hooray! No digital dust bunnies found. Your digital space is sparkling clean!")
        sys.exit(0)

    print(f"\nFound {total_bunnies} digital dust bunnies:")
    if empty_dirs:
        print(f"  - {len(empty_dirs)} empty directories.")
    if old_files:
        print(f"  - {len(old_files)} old files.")

    if args.dry_run:
        sweep_dust_bunnies(empty_dirs, old_files, True)
    elif args.force:
        print("\n⚠️ --force flag detected. Proceeding with deletion without confirmation.")
        sweep_dust_bunnies(empty_dirs, old_files, False)
    else:
        confirmation = input("\nReady to sweep these dust bunnies away? (y/N): ").lower()
        if confirmation == 'y':
            sweep_dust_bunnies(empty_dirs, old_files, False)
        else:
            print("\n😌 Phew! Dust bunnies spared for now. Come back anytime!")
            sys.exit(2) # No-op exit code

if __name__ == '__main__':
    main()
