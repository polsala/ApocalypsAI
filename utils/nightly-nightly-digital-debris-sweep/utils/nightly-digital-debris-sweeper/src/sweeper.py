import os
import argparse
import sys

def find_broken_symlinks(root_dir: str, verbose: bool = False) -> list[str]:
    """
    Finds all broken symbolic links within a given root directory.
    A symlink is considered broken if its target does not exist.
    """
    broken_links = []
    if verbose:
        print(f"Scanning '{root_dir}' for broken symbolic links...")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for name in filenames + dirnames:
            full_path = os.path.join(dirpath, name)
            if os.path.islink(full_path):
                target_path = os.readlink(full_path)
                # Check if the target exists, resolving relative paths correctly
                if not os.path.exists(target_path) and not os.path.exists(os.path.join(os.path.dirname(full_path), target_path)):
                    broken_links.append(full_path)
                    if verbose:
                        print(f"  Found broken symlink: {full_path} -> {target_path}")
    return broken_links

def find_empty_directories(root_dir: str, verbose: bool = False) -> list[str]:
    """
    Finds all empty directories within a given root directory.
    A directory is considered empty if it contains no files or subdirectories.
    """
    empty_dirs = []
    if verbose:
        print(f"Scanning '{root_dir}' for empty directories...")

    # Walk from bottom-up to ensure subdirectories are processed first
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if not dirnames and not filenames:
            # Exclude the root_dir itself if it becomes empty due to removal of its contents
            if dirpath != root_dir:
                empty_dirs.append(dirpath)
                if verbose:
                    print(f"  Found empty directory: {dirpath}")
    return empty_dirs

def remove_paths(paths: list[str], action_desc: str, verbose: bool = False) -> int:
    """
    Removes a list of paths (files or directories).
    Returns the count of successfully removed paths.
    """
    removed_count = 0
    for path in paths:
        try:
            if os.path.islink(path) or os.path.isfile(path):
                os.remove(path)
                if verbose:
                    print(f"  Removed {action_desc}: {path}")
                removed_count += 1
            elif os.path.isdir(path):
                os.rmdir(path)
                if verbose:
                    print(f"  Removed {action_desc}: {path}")
                removed_count += 1
        except OSError as e:
            print(f"Error removing {action_desc} '{path}': {e}", file=sys.stderr)
    return removed_count

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Digital Debris Sweeper: Cleans up broken symlinks and empty directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--remove-symlinks",
        action="store_true",
        help="If specified, broken symbolic links will be removed. Otherwise, they will only be listed."
    )
    parser.add_argument(
        "--remove-empty-dirs",
        action="store_true",
        help="If specified, empty directories will be removed. Otherwise, they will only be listed."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed information about scanned items and actions."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: The specified path '{args.path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    total_removed = 0

    # Find and optionally remove broken symlinks
    broken_symlinks = find_broken_symlinks(args.path, args.verbose)
    if broken_symlinks:
        print(f"\n--- Found {len(broken_symlinks)} broken symbolic link(s) ---")
        for link in broken_symlinks:
            print(f"- {link}")
        if args.remove_symlinks:
            print("Attempting to remove broken symbolic links...")
            removed_count = remove_paths(broken_symlinks, "broken symlink", args.verbose)
            total_removed += removed_count
            print(f"Successfully removed {removed_count} broken symbolic link(s).")
        else:
            print("Use --remove-symlinks to remove them.")
    else:
        print("\nNo broken symbolic links found.")

    # Find and optionally remove empty directories
    empty_dirs = find_empty_directories(args.path, args.verbose)
    if empty_dirs:
        print(f"\n--- Found {len(empty_dirs)} empty directory(ies) ---")
        for d in empty_dirs:
            print(f"- {d}")
        if args.remove_empty_dirs:
            print("Attempting to remove empty directories...")
            removed_count = remove_paths(empty_dirs, "empty directory", args.verbose)
            total_removed += removed_count
            print(f"Successfully removed {removed_count} empty directory(ies).")
        else:
            print("Use --remove-empty-dirs to remove them.")
    else:
        print("\nNo empty directories found.")

    if total_removed > 0:
        print(f"\nCleanup complete. Total items removed: {total_removed}.")
    else:
        print("\nNo items were removed during this run.")

    sys.exit(0)

if __name__ == "__main__":
    main()
