import os
import shutil
import argparse
import sys

# Whimsical patterns for digital dust bunnies
DUST_BUNNY_PATTERNS = [
    '.tmp', '.temp', '.log', '.bak', '.old',
    'cache/', '__pycache__/', '.pytest_cache/', '.mypy_cache/',
    'node_modules/', 'target/', 'build/', 'dist/',
    'temp/', 'tmp/',
    '*.swp', '*.swo', # Vim swap files
    '*.DS_Store', # macOS specific
    'Thumbs.db' # Windows specific
]

# Whimsical messages
WHIMSICAL_MESSAGES = [
    "🔍 Scanning for digital dust bunnies...",
    "✨ Found a particularly fluffy one!",
    "🧹 Sweeping away digital detritus...",
    "🚀 Your system feels lighter already!",
    "🌟 Making space for new adventures!",
    "🗑️ Disposing of forgotten bits and bytes."
]

def is_dust_bunny(path, patterns):
    """Checks if a given path matches any of the dust bunny patterns."""
    filename = os.path.basename(path)
    for pattern in patterns:
        if pattern.endswith('/') and os.path.isdir(path) and filename == pattern[:-1]:
            return True
        if pattern.startswith('*.'):
            if filename.endswith(pattern[1:]):
                return True
        elif pattern in filename:
            return True
    return False

def find_dust_bunnies(root_paths, patterns, verbose=False):
    """Walks through root_paths to find files/directories matching patterns."""
    found_bunnies = []
    for root_path in root_paths:
        if not os.path.exists(root_path):
            print(f"Warning: Path '{root_path}' does not exist. Skipping.", file=sys.stderr)
            continue

        if verbose:
            print(f"\n{WHIMSICAL_MESSAGES[0]} in '{root_path}'...")

        for dirpath, dirnames, filenames in os.walk(root_path):
            # Check directories
            for dname in list(dirnames): # Use list to allow modification of dirnames in place
                full_path = os.path.join(dirpath, dname)
                if is_dust_bunny(full_path, patterns):
                    found_bunnies.append(full_path)
                    dirnames.remove(dname) # Don't recurse into identified dust bunny directories

            # Check files
            for fname in filenames:
                full_path = os.path.join(dirpath, fname)
                if is_dust_bunny(full_path, patterns):
                    found_bunnies.append(full_path)
    return found_bunnies

def remove_dust_bunny(path):
    """Removes a file or directory."""
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Sweeper: Whimsical cleanup for your digital lair."
    )
    parser.add_argument(
        'paths', metavar='PATH', type=str, nargs='*', default=['.'],
        help='One or more paths to scan for dust bunnies. Defaults to current directory.'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Perform a dry run: show what would be deleted without actually deleting anything.'
    )
    parser.add_argument(
        '--force', '-f', action='store_true',
        help='Skip interactive confirmation and delete immediately (use with caution!).'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Show more detailed output during scanning.'
    )

    args = parser.parse_args()

    print(f"\n{WHIMSICAL_MESSAGES[0]}")
    if args.dry_run:
        print("\n--- DRY RUN MODE --- No files will be deleted. --- ")

    dust_bunnies = find_dust_bunnies(args.paths, DUST_BUNNY_PATTERNS, args.verbose)

    if not dust_bunnies:
        print("\n🎉 Hooray! No digital dust bunnies found. Your system is sparkling clean!")
        return

    print(f"\n{WHIMSICAL_MESSAGES[1]} ({len(dust_bunnies)} found):")
    for bunny in dust_bunnies:
        print(f"  - {bunny}")

    if args.dry_run:
        print("\n--- DRY RUN COMPLETE --- No changes were made. --- ")
        return

    if not args.force:
        try:
            confirmation = input("\nReady to sweep these dust bunnies away? (y/N): ").strip().lower()
            if confirmation != 'y':
                print("\n🧹 Cleanup cancelled. Your dust bunnies live to see another day.")
                return
        except KeyboardInterrupt:
            print("\n🧹 Cleanup interrupted. Your dust bunnies live to see another day.")
            return

    print(f"\n{WHIMSICAL_MESSAGES[2]}")
    deleted_count = 0
    for bunny in dust_bunnies:
        try:
            remove_dust_bunny(bunny)
            print(f"  [DELETED] {bunny}")
            deleted_count += 1
        except OSError as e:
            print(f"  [ERROR] Could not delete {bunny}: {e}", file=sys.stderr)

    print(f"\n{WHIMSICAL_MESSAGES[3]} ({deleted_count} items swept away)!\n")

if __name__ == '__main__':
    main()
