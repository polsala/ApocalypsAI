import os
import hashlib
import argparse
import json
from collections import defaultdict

def calculate_sha256(filepath, chunk_size=4096):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError:
        return None

def find_duplicate_files(directories, min_size=0):
    """Finds duplicate files in the given directories.

    Args:
        directories (list): A list of directory paths to scan.
        min_size (int): Minimum file size in bytes to consider.

    Returns:
        dict: A dictionary where keys are SHA256 hashes and values are lists of file paths.
              Only includes hashes that have more than one file path (i.e., duplicates).
    """
    files_by_size = defaultdict(list)
    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Warning: Directory not found: {directory}")
            continue
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                try:
                    file_size = os.path.getsize(filepath)
                    if file_size >= min_size:
                        files_by_size[file_size].append(filepath)
                except OSError:
                    # Ignore files that cannot be accessed (e.g., broken symlinks, permission issues)
                    pass

    duplicates = defaultdict(list)
    for size, filepaths in files_by_size.items():
        if len(filepaths) < 2: # No need to hash if only one file of this size
            continue
        for filepath in filepaths:
            file_hash = calculate_sha256(filepath)
            if file_hash:
                duplicates[file_hash].append(filepath)
    
    # Filter out hashes that only have one file (i.e., not duplicates)
    return {h: paths for h, paths in duplicates.items() if len(paths) > 1}

def main():
    parser = argparse.ArgumentParser(
        description="Find duplicate files in specified directories."
    )
    parser.add_argument(
        "directories",
        metype=str,
        nargs='+',
        help="One or more directory paths to scan."
    )
    parser.add_argument(
        "--output-format",
        type=str,
        choices=['text', 'json'],
        default='text',
        help="Output format (text or json). Defaults to text."
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=0,
        help="Only consider files larger than or equal to this size (in bytes). Defaults to 0."
    )

    args = parser.parse_args()

    duplicate_sets = find_duplicate_files(args.directories, args.min_size)

    if not duplicate_sets:
        print("No duplicate files found.")
        return

    if args.output_format == 'json':
        output_data = []
        for file_hash, file_paths in duplicate_sets.items():
            # Assuming all files in a duplicate set have the same size
            # We can get the size from the first file path
            try:
                size = os.path.getsize(file_paths[0])
            except OSError:
                size = 0 # Fallback if file is suddenly inaccessible
            output_data.append({
                "hash": file_hash,
                "size": size,
                "files": sorted(file_paths)
            })
        print(json.dumps(output_data, indent=2))
    else: # text format
        print(f"Found {len(duplicate_sets)} sets of duplicate files:\n")
        for i, (file_hash, file_paths) in enumerate(duplicate_sets.items()):
            print(f"Set {i + 1} (SHA256: {file_hash}):")
            for filepath in sorted(file_paths):
                print(f"  - {filepath}")
            print()

if __name__ == "__main__":
    main()
