import os
import argparse
import sys
from typing import List, Tuple

def find_empty_directories(root_path: str, verbose: bool = False) -> List[str]:
    """
    Finds all empty directories within the given root_path.
    """
    empty_dirs = []
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.", file=sys.stderr)
        return []

    if verbose:
        print(f"Scanning '{root_path}' for empty directories...")

    for dirpath, dirnames, filenames in os.walk(root_path):
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
            if verbose:
                print(f"  Found empty directory: {dirpath}")
    return empty_dirs

def find_broken_symlinks(root_path: str, verbose: bool = False) -> List[str]:
    """
    Finds all broken symbolic links within the given root_path.
    """
    broken_links = []
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.", file=sys.stderr)
        return []

    if verbose:
        print(f"Scanning '{root_path}' for broken symbolic links...")

    for dirpath, dirnames, filenames in os.walk(root_path):
        for name in dirnames + filenames:
            full_path = os.path.join(dirpath, name)
            if os.path.islink(full_path) and not os.path.exists(full_path):
                broken_links.append(full_path)
                if verbose:
                    print(f"  Found broken symlink: {full_path}")
    return broken_links

def clean_up(empty_dirs: List[str], broken_links: List[str], verbose: bool = False) -> Tuple[int, int]:
    """
    Removes the specified empty directories and broken symbolic links.
    Returns the count of removed items.
    """
    removed_dirs = 0
    removed_links = 0

    # Remove empty directories (from deepest to shallowest to avoid issues)
    for d in sorted(empty_dirs, key=len, reverse=True):
        try:
            os.rmdir(d)
            removed_dirs += 1
            if verbose:
                print(f"Removed empty directory: {d}")
        except OSError as e:
            print(f"Warning: Could not remove empty directory '{d}': {e}", file=sys.stderr)

    # Remove broken symlinks
    for l in broken_links:
        try:
            os.remove(l)
            removed_links += 1
            if verbose:
                print(f"Removed broken symlink: {l}")
        except OSError as e:
            print(f"Warning: Could not remove broken symlink '{l}': {e}", file=sys.stderr)

    return removed_dirs, removed_links

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital dust bunnies: empty directories and broken symbolic links."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="If provided, the utility will proceed to remove detected items. Use with caution!"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="If provided, prints more detailed information during the scan."
    )

    args = parser.parse_args()

    root_path = os.path.abspath(args.path)

    if not os.path.isdir(root_path):
        print(f"Error: The specified path '{root_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print(f"--- Nightly Digital Dust Sweeper ---")
    print(f"Scanning path: {root_path}")
    print(f"Clean mode: {'ENABLED' if args.clean else 'DISABLED (Dry Run)'}")
    print("-" * 35)

    empty_dirs = find_empty_directories(root_path, args.verbose)
    broken_links = find_broken_symlinks(root_path, args.verbose)

    print("\n--- Scan Results ---")
    if empty_dirs:
        print(f"Found {len(empty_dirs)} empty directories:")
        for d in empty_dirs:
            print(f"  - {d}")
    else:
        print("No empty directories found.")

    if broken_links:
        print(f"Found {len(broken_links)} broken symbolic links:")
        for l in broken_links:
            print(f"  - {l}")
    else:
        print("No broken symbolic links found.")

    print("-" * 35)

    if args.clean:
        if empty_dirs or broken_links:
            print("\nInitiating cleanup...")
            removed_dirs, removed_links = clean_up(empty_dirs, broken_links, args.verbose)
            print(f"\nCleanup complete: Removed {removed_dirs} empty directories and {removed_links} broken symlinks.")
        else:
            print("Nothing to clean up.")
    else:
        print("\nDry run complete. No changes were made. Use --clean to remove detected items.")

    print("\n--- Dust Sweeper Finished ---")

if __name__ == "__main__":
    main()
