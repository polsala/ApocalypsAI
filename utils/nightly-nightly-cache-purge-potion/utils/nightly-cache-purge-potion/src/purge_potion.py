import os
import shutil
import sys
import argparse
from pathlib import Path

def get_cache_paths():
    """Returns a list of common user-level cache directories based on the OS."""
    paths = []
    home = Path.home()

    if sys.platform == 'win32':
        # Windows paths
        local_app_data = Path(os.getenv('LOCALAPPDATA', ''))
        temp_dir = Path(os.getenv('TEMP', ''))

        if local_app_data.exists():
            paths.append(local_app_data / 'Temp')
            paths.append(local_app_data / 'npm-cache')
        if temp_dir.exists():
            paths.append(temp_dir)
        if (home / '.pip' / 'cache').exists():
            paths.append(home / '.pip' / 'cache')
        if (home / '.cargo' / 'registry' / 'cache').exists():
            paths.append(home / '.cargo' / 'registry' / 'cache')

    elif sys.platform == 'darwin':
        # macOS paths
        paths.append(home / 'Library' / 'Caches')
        paths.append(home / '.npm')
        paths.append(home / '.pip' / 'cache')
        paths.append(home / '.cargo' / 'registry' / 'cache')
        paths.append(home / '.Trash') # User's Trash bin

    else: # Linux and other Unix-like systems
        paths.append(home / '.cache')
        paths.append(home / '.npm')
        paths.append(home / '.pip' / 'cache')
        paths.append(home / '.cargo' / 'registry' / 'cache')
        paths.append(home / '.local' / 'share' / 'Trash') # User's Trash bin

    # Filter out paths that don't exist to avoid unnecessary checks
    return [p for p in paths if p.exists()]

def purge_directory(path: Path, dry_run: bool = False, verbose: bool = False):
    """Recursively purges the contents of a directory, but not the directory itself."""
    if not path.is_dir():
        if verbose: print(f"  Skipping non-directory: {path}")
        return 0

    total_purged_items = 0
    if verbose: print(f"  Inspecting: {path}")

    for item in path.iterdir():
        if item.is_dir():
            if verbose: print(f"    {'Would remove' if dry_run else 'Removing'} directory: {item}")
            if not dry_run:
                try:
                    shutil.rmtree(item)
                    total_purged_items += 1
                except OSError as e:
                    print(f"    Error removing directory {item}: {e}", file=sys.stderr)
            else:
                total_purged_items += 1
        else:
            if verbose: print(f"    {'Would remove' if dry_run else 'Removing'} file: {item}")
            if not dry_run:
                try:
                    os.remove(item)
                    total_purged_items += 1
                except OSError as e:
                    print(f"    Error removing file {item}: {e}", file=sys.stderr)
            else:
                total_purged_items += 1
    return total_purged_items

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cache Purge Potion: Cleans common user-level cache and temporary files."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Perform a dry run without deleting any files, just show what would be removed."
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Show more detailed output during the purge process."
    )
    args = parser.parse_args()

    print("\n✨ Activating Nightly Cache Purge Potion... ✨")
    print(f"Mode: {'Dry Run (no changes will be made)' if args.dry_run else 'Actual Purge'}\n")

    cache_paths = get_cache_paths()
    if not cache_paths:
        print("No common cache directories found for this operating system. Potion remains sealed.")
        return

    total_items_purged = 0
    for path in cache_paths:
        print(f"  Attempting to cleanse: {path}")
        purged_count = purge_directory(path, args.dry_run, args.verbose)
        total_items_purged += purged_count
        if purged_count > 0:
            print(f"  {'Would have purged' if args.dry_run else 'Purged'} {purged_count} items from {path}.")
        else:
            print(f"  No items {'would be' if args.dry_run else 'were'} purged from {path}.")

    print(f"\n\n🔮 Potion complete! {'Would have purged' if args.dry_run else 'Purged'} a total of {total_items_purged} items.\n")
    if args.dry_run:
        print("Remember to run without --dry-run to apply changes.")

if __name__ == '__main__':
    main()
