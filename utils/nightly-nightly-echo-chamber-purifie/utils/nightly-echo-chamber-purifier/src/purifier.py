import os
import hashlib
from collections import defaultdict
import argparse
import sys

def calculate_file_hash(filepath, hash_algo='md5', chunk_size=4096):
    """Calculates the hash of a file."""
    if not os.path.isfile(filepath):
        return None
    
    hasher = hashlib.new(hash_algo)
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError:
        return None

def find_duplicate_files(start_path, hash_algo='md5', exclude_dirs=None):
    """
    Finds duplicate files in a given directory and its subdirectories.
    Returns a dictionary where keys are file hashes and values are lists of file paths.
    """
    if exclude_dirs is None:
        exclude_dirs = []
    
    hashes = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(start_path):
        # Modify dirnames in-place to prune directories from os.walk
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Skip symbolic links to avoid infinite loops or processing linked files multiple times
            if os.path.islink(filepath):
                continue
            
            file_hash = calculate_file_hash(filepath, hash_algo)
            if file_hash:
                hashes[file_hash].append(filepath)
    
    # Filter out unique files (those with only one path)
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Purifier: Finds duplicate files in a directory."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The starting directory to scan for duplicate files."
    )
    parser.add_argument(
        "--hash-algo",
        type=str,
        default="md5",
        choices=["md5", "sha1", "sha256"],
        help="Hashing algorithm to use (default: md5)."
    )
    parser.add_argument(
        "--exclude",
        type=str,
        nargs='*',
        default=[],
        help="Directories to exclude from the scan (e.g., --exclude .git node_modules)."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory '{args.path}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning '{args.path}' for duplicate files using {args.hash_algo.upper()}...")
    if args.exclude:
        print(f"Excluding directories: {', '.join(args.exclude)}")

    duplicates = find_duplicate_files(args.path, args.hash_algo, args.exclude)

    if not duplicates:
        print("\nNo duplicate files found. Your echo chamber is pure!")
        sys.exit(0)
    else:
        print(f"\nFound {len(duplicates)} sets of duplicate files:")
        for file_hash, paths in duplicates.items():
            print(f"\nHash: {file_hash}")
            for path in paths:
                print(f"  - {path}")
        print("\nConsider removing redundant files to purify your storage.")
        sys.exit(0) # Exit with 0 even if duplicates are found, as it's a report, not an error.

if __name__ == "__main__":
    main()
