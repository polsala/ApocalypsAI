import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file's content."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        return None # Handle unreadable files

def find_duplicates(paths, min_size=0, exclude_dirs=None):
    """Finds duplicate files in the given paths based on content hash.

    Args:
        paths (list): List of directory paths to scan.
        min_size (int): Minimum file size in bytes to consider for duplication.
        exclude_dirs (list): List of directory names to exclude from scanning.

    Returns:
        dict: A dictionary where keys are file hashes and values are lists of file paths.
              Only includes hashes with more than one file (i.e., duplicates).
    """
    if exclude_dirs is None:
        exclude_dirs = []

    files_by_hash = defaultdict(list)
    for path in paths:
        if not os.path.isdir(path):
            print(f"Warning: Path '{path}' is not a valid directory. Skipping.")
            continue

        for root, dirs, files in os.walk(path):
            # Modify dirs in-place to prune directories for os.walk
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for filename in files:
                filepath = os.path.join(root, filename)
                # Skip symbolic links to avoid infinite loops or processing linked files as originals
                if not os.path.islink(filepath) and os.path.isfile(filepath):
                    try:
                        file_size = os.path.getsize(filepath)
                        if file_size < min_size:
                            continue

                        file_hash = calculate_file_hash(filepath)
                        if file_hash:
                            files_by_hash[file_hash].append(filepath)
                    except OSError as e:
                        print(f"Warning: Could not process '{filepath}': {e}")

    duplicates = {h: fpaths for h, fpaths in files_by_hash.items() if len(fpaths) > 1}
    return duplicates

def report_duplicates(duplicates):
    """Prints a report of found duplicate files."""
    if not duplicates:
        print("No duplicate files found. Your digital space is pristine!")
        return

    print(f"\nFound {len(duplicates)} groups of duplicate files:\n")
    for i, (file_hash, filepaths) in enumerate(duplicates.items()):
        print(f"Group {i+1} (Hash: {file_hash[:10]}...)")
        for filepath in filepaths:
            print(f"  - {filepath}")
        print()

def remove_duplicates(duplicates):
    """Interactively removes duplicate files, keeping one original."""
    if not duplicates:
        print("No duplicates to remove.")
        return

    print("\nInitiating interactive duplicate removal. For each group, the first file listed will be kept as the original.\n")
    removed_count = 0

    for file_hash, filepaths in duplicates.items():
        original_file = filepaths[0]
        print(f"Group (Hash: {file_hash[:10]}...): Keeping '{original_file}'")
        for i, duplicate_file in enumerate(filepaths[1:]):
            response = input(f"  Remove duplicate '{duplicate_file}'? (y/N): ").lower()
            if response == 'y':
                try:
                    os.remove(duplicate_file)
                    print(f"    Removed: {duplicate_file}")
                    removed_count += 1
                except OSError as e:
                    print(f"    Error removing '{duplicate_file}': {e}")
            else:
                print(f"    Skipped: {duplicate_file}")
    print(f"\nFinished removal. Total files removed: {removed_count}")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Purifier: Find and optionally remove duplicate files."
    )
    parser.add_argument(
        '--path', '-p', 
        nargs='+', 
        required=True, 
        help='One or more directory paths to scan for duplicates.'
    )
    parser.add_argument(
        '--remove', '-r', 
        action='store_true', 
        help='Enable interactive removal of duplicate files. The first file found in a group will be kept.'
    )
    parser.add_argument(
        '--exclude', '-e', 
        nargs='*', 
        default=[], 
        help='List of directory names to exclude from scanning (e.g., .git node_modules).' 
    )
    parser.add_argument(
        '--min-size', '-m', 
        type=int, 
        default=0, 
        help='Minimum file size in bytes to consider for duplication (default: 0).' 
    )

    args = parser.parse_args()

    print(f"Scanning for duplicate files in {args.path}...")
    duplicates = find_duplicates(args.path, args.min_size, args.exclude)

    report_duplicates(duplicates)

    if args.remove and duplicates:
        remove_duplicates(duplicates)
    elif args.remove and not duplicates:
        print("No duplicates found, so nothing to remove.")

if __name__ == '__main__':
    main()
