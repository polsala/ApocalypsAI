import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        return None # File might be inaccessible or not exist

def find_duplicate_files(directories, verbose=False):
    """
    Finds duplicate files in the given directories based on their MD5 hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    """
    hashes = defaultdict(list)
    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Warning: Directory not found or not accessible: {directory}")
            continue

        if verbose:
            print(f"Scanning directory: {directory}")

        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.isfile(filepath): # Ensure it's a file, not a broken symlink or dir
                    file_hash = calculate_file_hash(filepath)
                    if file_hash:
                        hashes[file_hash].append(filepath)
                        if verbose:
                            print(f"  Hashed: {filepath} -> {file_hash}")
    return hashes

def report_and_remove_duplicates(duplicate_groups, remove=False, verbose=False):
    """
    Reports duplicate files and optionally removes them.
    Returns a tuple: (files_found, files_removed).
    """
    total_files_found = 0
    total_files_removed = 0

    for file_hash, filepaths in duplicate_groups.items():
        if len(filepaths) > 1:
            total_files_found += len(filepaths)
            print(f"\n--- Duplicate Group (Hash: {file_hash}) ---")
            print(f"  Original: {filepaths[0]}")
            for i, duplicate_path in enumerate(filepaths[1:]):
                print(f"  Duplicate {i+1}: {duplicate_path}")
                if remove:
                    try:
                        os.remove(duplicate_path)
                        total_files_removed += 1
                        print(f"    [REMOVED] {duplicate_path}")
                    except OSError as e:
                        print(f"    [ERROR] Could not remove {duplicate_path}: {e}")
                else:
                    print(f"    [DRY RUN] Would remove {duplicate_path}")
    return total_files_found, total_files_removed

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Purifier: Detects and optionally removes duplicate files."
    )
    parser.add_argument(
        "directories",
        nargs=":",
        help="One or more directories to scan for duplicate files."
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="If specified, duplicate files will be deleted. By default, it performs a dry run."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="If specified, prints more detailed information during the scan."
    )

    args = parser.parse_args()

    if not args.directories:
        print("Error: At least one directory path must be provided.")
        parser.print_help()
        return

    print("Starting Nightly Echo Chamber Purifier...")
    print(f"Scanning directories: {', '.join(args.directories)}")
    print(f"Mode: {'REMOVE duplicates' if args.remove else 'DRY RUN (no files will be deleted)'}")

    duplicate_groups = find_duplicate_files(args.directories, args.verbose)
    
    # Filter out groups with only one file (not duplicates)
    actual_duplicates = {h: paths for h, paths in duplicate_groups.items() if len(paths) > 1}

    if not actual_duplicates:
        print("\nNo duplicate files found. Your echo chamber is pure!")
        return

    files_found, files_removed = report_and_remove_duplicates(actual_duplicates, args.remove, args.verbose)

    print("\n--- Summary ---")
    print(f"Total duplicate files identified (including originals): {files_found}")
    print(f"Total files that {'were removed' if args.remove else 'would be removed'}: {files_removed}")
    print("Purification complete!")

if __name__ == "__main__":
    main()
