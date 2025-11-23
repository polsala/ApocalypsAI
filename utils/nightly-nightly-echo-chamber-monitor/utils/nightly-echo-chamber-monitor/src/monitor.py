import os
import hashlib
import argparse
from collections import defaultdict
import fnmatch

def calculate_file_hash(filepath, hash_algorithm='sha256'):
    """
    Calculates the hash of a file's content.
    """
    hasher = hashlib.new(hash_algorithm)
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError:
        return None # Handle unreadable files gracefully

def find_duplicates(directory_path, exclude_patterns=None):
    """
    Scans the given directory for files with identical content.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    Only includes hashes that correspond to more than one file.
    """
    if not os.path.isdir(directory_path):
        raise ValueError(f"Directory not found: {directory_path}")

    file_hashes = defaultdict(list)
    exclude_patterns = exclude_patterns if exclude_patterns else []

    for root, dirnames, filenames in os.walk(directory_path):
        # Filter out excluded directories before processing files in them
        dirnames[:] = [d for d in dirnames if not any(
            fnmatch.fnmatch(os.path.join(os.path.relpath(root, directory_path), d), p)
            or fnmatch.fnmatch(d, p)
            for p in exclude_patterns
        )]

        for filename in filenames:
            filepath = os.path.join(root, filename)
            relative_filepath = os.path.relpath(filepath, directory_path)

            # Check if the current file should be excluded
            if any(fnmatch.fnmatch(relative_filepath, p) or fnmatch.fnmatch(filename, p) for p in exclude_patterns):
                continue

            file_hash = calculate_file_hash(filepath)
            if file_hash:
                file_hashes[file_hash].append(filepath)
    
    # Filter for actual duplicates (hashes with more than one file)
    duplicates = {hash_val: paths for hash_val, paths in file_hashes.items() if len(paths) > 1}
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Monitor: Detects duplicate files in a directory."
    )
    parser.add_argument(
        "--path", 
        type=str, 
        required=True, 
        help="The root directory to scan for duplicate files."
    )
    parser.add_argument(
        "--exclude", 
        type=str, 
        help="Comma-separated glob patterns to exclude files or directories. E.g., '*.log,temp_dir/*'"
    )

    args = parser.parse_args()

    exclude_patterns = [p.strip() for p in args.exclude.split(',')] if args.exclude else []

    print(f"Scanning directory: {args.path}")

    try:
        duplicate_groups = find_duplicates(args.path, exclude_patterns)

        if duplicate_groups:
            print(f"\nFound {len(duplicate_groups)} groups of duplicate files:\n")
            for i, (hash_val, paths) in enumerate(duplicate_groups.items()):
                print(f"--- Group {i + 1} ---")
                print(f"Hash: {hash_val}")
                for p in paths:
                    print(f"  - {p}")
                print()
            print("Scan complete. Consider cleaning up these echoes.")
        else:
            print("\nNo duplicate files (echoes) detected. Your directory is pristine!")

    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
