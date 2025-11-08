import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def get_file_age_in_days(filepath):
    """Returns the age of a file/directory in days based on its last modification time."""
    try:
        # Use st_mtime for modification time, st_atime for access time
        # st_mtime is generally more reliable for 'freshness'
        mod_time = os.path.getmtime(filepath)
        return (time.time() - mod_time) / (24 * 3600)
    except OSError:
        return float('inf') # File not found or inaccessible

def is_dust_bunny(filepath, min_age_days, patterns):
    """Determines if a file/directory is a 'dust bunny' based on age or patterns."""
    if not os.path.exists(filepath):
        return False

    # Check by age
    if min_age_days > 0:
        age = get_file_age_in_days(filepath)
        if age >= min_age_days:
            return True

    # Check by pattern
    filename = os.path.basename(filepath)
    for pattern in patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True

    return False

def find_dust_bunnies(root_dir, min_age_days, patterns):
    """Recursively finds 'dust bunnies' in the given root directory."""
    dust_bunnies = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check directories first
        for dname in list(dirnames): # Iterate over a copy to allow modification of dirnames
            full_path = os.path.join(dirpath, dname)
            if is_dust_bunny(full_path, min_age_days, patterns):
                dust_bunnies.append(full_path)
                dirnames.remove(dname) # Don't traverse into a directory that's a dust bunny itself

        # Check files
        for fname in filenames:
            full_path = os.path.join(dirpath, fname)
            if is_dust_bunny(full_path, min_age_days, patterns):
                dust_bunnies.append(full_path)
    return dust_bunnies

def sweep_dust_bunnies(dust_bunnies, dry_run):
    """Deletes or lists 'dust bunnies' based on dry_run flag."""
    if not dust_bunnies:
        print("\n✨ Your digital space is sparkling clean! No dust bunnies found. ✨")
        return

    print(f"\n🔍 Found {len(dust_bunnies)} digital dust bunnies:")
    for i, bunny in enumerate(dust_bunnies):
        print(f"  {i+1}. {bunny}")

    if dry_run:
        print("\n(This was a dry run. No files were actually swept away.)")
        return

    confirmation = input("\n🧹 Ready to sweep these dust bunnies away? (y/N): ").lower()
    if confirmation == 'y':
        print("\nSweeping...")
        for bunny in dust_bunnies:
            try:
                if os.path.isfile(bunny):
                    os.remove(bunny)
                    print(f"  ✅ Swept away file: {bunny}")
                elif os.path.isdir(bunny):
                    import shutil
                    shutil.rmtree(bunny)
                    print(f"  ✅ Swept away directory: {bunny}")
            except OSError as e:
                print(f"  ❌ Failed to sweep {bunny}: {e}")
        print("\n✨ Digital space tidied up! ✨")
    else:
        print("\nOperation cancelled. The dust bunnies live to see another day! 🐾")

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Sweeper: Tidy up your digital space!",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--path', required=True, help='The root directory to start scanning for dust bunnies.')
    parser.add_argument('--age', type=int, default=30, help='Files/directories not accessed or modified in this many days or more will be flagged. Default: 30.')
    parser.add_argument('--patterns', nargs='*', default=['*.log', '*.tmp', '*.bak'],
                        help='Space-separated list of glob patterns (e.g., "*.log" "temp_*"). Files/directories matching these patterns will be flagged. Default: *.log *.tmp *.bak')
    parser.add_argument('--dry-run', action='store_true', help='Only list what would be deleted, without performing any actual deletions. This is the default if --delete is not specified.')
    parser.add_argument('--delete', action='store_true', help='After listing, prompt for confirmation to delete the identified items. Use with caution!')

    args = parser.parse_args()

    if args.delete and args.dry_run:
        print("Error: Cannot use --delete and --dry-run together. Please choose one.")
        return

    # If --delete is not specified, it's a dry run by default
    is_dry_run = args.dry_run or not args.delete

    print(f"\n🧹 Initiating Digital Dust Bunny Sweep in '{args.path}'...")
    print(f"   Criteria: Older than {args.age} days OR matching patterns: {', '.join(args.patterns)}")

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.")
        return

    dust_bunnies = find_dust_bunnies(args.path, args.age, args.patterns)
    sweep_dust_bunnies(dust_bunnies, is_dry_run)

if __name__ == '__main__':
    main()
