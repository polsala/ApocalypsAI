import os
import argparse
from typing import List, Tuple

def find_empty_files(root_dir: str) -> List[str]:
    """Finds all empty files (0 bytes) within the given root directory."""
    empty_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                if os.path.isfile(filepath) and os.path.getsize(filepath) == 0:
                    empty_files.append(filepath)
            except OSError: # Handle cases like broken symlinks, permission errors
                pass
    return empty_files

def find_empty_dirs(root_dir: str) -> List[str]:
    """Finds all truly empty directories within the given root directory.
    A directory is considered truly empty if it contains no files and no non-empty subdirectories.
    """
    empty_dirs = []
    # Walk from bottom up to correctly identify empty directories
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if not filenames and not dirnames: # No files and no subdirectories (that haven't been removed yet)
            empty_dirs.append(dirpath)
    return empty_dirs

def generate_report(root_dir: str, empty_files: List[str], empty_dirs: List[str]) -> str:
    """Generates a formatted report of empty files and directories."""
    report = []
    report.append("--- Data Dust Bunny Duster Report ---")
    report.append(f"Scanned directory: {os.path.abspath(root_dir)}")
    report.append("\nEmpty Files Found:")
    if empty_files:
        for f in empty_files:
            report.append(f"  - {f}")
    else:
        report.append("  No empty files detected. Your digital floor is spotless!")

    report.append("\nEmpty Directories Found:")
    if empty_dirs:
        for d in empty_dirs:
            report.append(f"  - {d}")
    else:
        report.append("  No empty directories detected. Your digital shelves are sturdy!")

    report.append("\n-------------------------------------")
    return "\n".join(report)

def clean_up(empty_files: List[str], empty_dirs: List[str], dry_run: bool, verbose: bool) -> None:
    """Deletes the identified empty files and directories if not in dry-run mode."""
    if dry_run:
        print("\nDry run mode: No changes will be made.")
        return

    print("\nInitiating cleanup...")
    deleted_count = 0

    for f in empty_files:
        try:
            os.remove(f)
            if verbose: print(f"  Deleted empty file: {f}")
            deleted_count += 1
        except OSError as e:
            print(f"  Error deleting file {f}: {e}")

    # Sort directories by length in descending order to delete deepest first
    # This is crucial for os.rmdir to work correctly on nested empty directories
    for d in sorted(empty_dirs, key=len, reverse=True):
        try:
            os.rmdir(d)
            if verbose: print(f"  Deleted empty directory: {d}")
            deleted_count += 1
        except OSError as e:
            print(f"  Error deleting directory {d}: {e}")

    print(f"\nCleanup complete. Total items deleted: {deleted_count}")

def main():
    parser = argparse.ArgumentParser(
        description="Scans directories for empty files and empty subdirectories, providing a report and an option to delete them."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If provided, the utility will prompt for confirmation before deleting the identified empty files and directories. Use with caution!"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="If provided, print more detailed information during the scan."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: The specified path '{args.path}' is not a valid directory.")
        exit(1)

    print(f"Scanning '{args.path}' for digital dust bunnies...")

    empty_files = find_empty_files(args.path)
    empty_dirs = find_empty_dirs(args.path)

    report = generate_report(args.path, empty_files, empty_dirs)
    print(report)

    if args.delete:
        if empty_files or empty_dirs:
            confirmation = input("\nAre you sure you want to delete these items? (yes/no): ").lower()
            if confirmation == 'yes':
                clean_up(empty_files, empty_dirs, dry_run=False, verbose=args.verbose)
            else:
                print("Cleanup cancelled.")
        else:
            print("No empty files or directories to delete.")
    else:
        print("\nTo delete these items, run the utility again with the '--delete' flag.")

if __name__ == "__main__":
    main()
