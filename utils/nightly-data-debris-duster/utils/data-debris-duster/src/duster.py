import os
import sys
import argparse

def find_empty_dirs(path):
    """
    Recursively finds all empty directories within the given path.
    Returns a list of paths to empty directories.
    """
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(path):
        # Check if the current directory is empty (no files and no subdirectories)
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def clean_empty_dirs(path, dry_run=True):
    """
    Finds and optionally removes empty directories.
    Returns a tuple: (list of found empty dirs, list of removed dirs).
    """
    found_empty = []
    removed_empty = []

    # Walk from the deepest directories up to ensure parent directories become empty
    # after their children are removed.
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        # Check if the current directory is empty
        # It's empty if it has no files and all its subdirectories (if any) have been removed
        # or were already empty.
        if not filenames and not os.listdir(dirpath): # os.listdir checks actual content
            found_empty.append(dirpath)
            if not dry_run:
                try:
                    os.rmdir(dirpath)
                    removed_empty.append(dirpath)
                except OSError as e:
                    print(f"Error removing {dirpath}: {e}", file=sys.stderr)
    return found_empty, removed_empty

def main():
    parser = argparse.ArgumentParser(
        description="Data Debris Duster: Identify and optionally remove empty directories."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The path to scan for empty directories."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove the identified empty directories. (Default: dry run)"
    )

    args = parser.parse_args()
    target_path = os.path.abspath(args.path)

    if not os.path.isdir(target_path):
        print(f"Error: Path '{target_path}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning '{target_path}' for digital debris...")

    found_empty, removed_empty = clean_empty_dirs(target_path, dry_run=not args.clean)

    if found_empty:
        print("\n--- Detected Digital Debris (Empty Directories) ---")
        for d in sorted(found_empty):
            print(f"- {d}")
        print(f"\nTotal debris piles found: {len(found_empty)}")

        if args.clean:
            if removed_empty:
                print("\n--- Debris Successfully Dusted ---")
                for d in sorted(removed_empty):
                    print(f"- Removed: {d}")
                print(f"\nTotal debris piles removed: {len(removed_empty)}")
            else:
                print("\nNo debris piles were removed (perhaps due to permissions or they became non-empty).")
        else:
            print("\nRun with '--clean' to remove these digital debris piles.")
    else:
        print("\nNo digital debris found. Your filesystem is pristine!")

if __name__ == "__main__":
    main()
