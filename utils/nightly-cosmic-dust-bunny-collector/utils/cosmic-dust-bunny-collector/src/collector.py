import os
import argparse
import sys

def find_empty_dirs(root_path):
    """
    Recursively finds all empty directories within a given root_path.
    An empty directory is one that contains no files and no subdirectories.
    """
    empty_dirs = []
    # topdown=False ensures that child directories are visited before their parents.
    # This is crucial for correctly identifying and removing empty directories,
    # as a parent might become empty only after its children are removed.
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def remove_empty_dirs(dirs_to_remove):
    """
    Removes a list of directories. Prints success or failure messages.
    It sorts directories by length in reverse order to ensure deeper directories
    are removed first, preventing issues if a parent is removed before its child.
    """
    removed_count = 0
    for d in sorted(dirs_to_remove, key=len, reverse=True):
        try:
            os.rmdir(d)
            print(f"Successfully removed: {d}")
            removed_count += 1
        except OSError as e:
            print(f"Error removing {d}: {e}", file=sys.stderr)
    return removed_count

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Collector: Sweeps away empty directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The root path to scan for empty directories (default: current directory)."
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List empty directories found, but do not remove them."
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove empty directories found. USE WITH CAUTION!"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning '{os.path.abspath(args.path)}' for cosmic dust bunnies...")
    empty_dirs = find_empty_dirs(args.path)

    if not empty_dirs:
        print("No cosmic dust bunnies (empty directories) found. Your space is pristine! ✨")
        sys.exit(0)

    print(f"Found {len(empty_dirs)} cosmic dust bunnies:")
    for d in empty_dirs:
        print(f"  - {d}")

    if args.remove:
        confirm = input("Are you sure you want to remove these directories? (yes/no): ").lower()
        if confirm == 'yes':
            print("Initiating cleanup...")
            removed_count = remove_empty_dirs(empty_dirs)
            print(f"Cleanup complete. Removed {removed_count} directories.")
            sys.exit(0)
        else:
            print("Cleanup aborted.")
            sys.exit(2) # No-op exit code
    elif args.list:
        print("Listing complete. Use --remove to sweep them away.")
        sys.exit(0)
    else:
        print("No action specified. Use --list to see them or --remove to sweep them away.")
        sys.exit(2) # No-op exit code

if __name__ == "__main__":
    main()
