import os
import hashlib
import sys
from collections import defaultdict

def calculate_file_hash(filepath: str, block_size: int = 65536) -> str:
    """Calculates the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return ""

def find_duplicates(paths: list[str]) -> dict[str, list[str]]:
    """Finds duplicate files within the given list of directory paths.

    Returns a dictionary where keys are file hashes and values are lists of
    file paths that share that hash (i.e., are duplicates).
    """
    files_by_hash: dict[str, list[str]] = defaultdict(list)
    files_by_size: dict[int, list[str]] = defaultdict(list)

    # First pass: group files by size to quickly filter out non-duplicates
    for path_arg in paths:
        if not os.path.isdir(path_arg):
            print(f"Warning: Path '{path_arg}' is not a directory and will be skipped.", file=sys.stderr)
            continue
        for root, _, files in os.walk(path_arg):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    file_size = os.path.getsize(filepath)
                    files_by_size[file_size].append(filepath)
                except OSError as e:
                    print(f"Warning: Could not get size for {filepath}: {e}", file=sys.stderr)

    # Second pass: calculate hash only for files that share a size
    duplicate_hashes: dict[str, list[str]] = {}
    for size, filepaths in files_by_size.items():
        if len(filepaths) > 1: # Only check for duplicates if there's more than one file of this size
            for filepath in filepaths:
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    files_by_hash[file_hash].append(filepath)
    
    # Filter out hashes that only have one file (not duplicates)
    for file_hash, filepaths in files_by_hash.items():
        if len(filepaths) > 1:
            duplicate_hashes[file_hash] = filepaths

    return duplicate_hashes

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/duster.py <directory1> [directory2] ...", file=sys.stderr)
        sys.exit(1)

    target_paths = sys.argv[1:]
    duplicates = find_duplicates(target_paths)

    if not duplicates:
        print("No duplicate files found. Your digital wasteland is surprisingly clean!")
        sys.exit(0)

    print("\n--- Duplicate Files Report ---")
    for file_hash, filepaths in duplicates.items():
        print(f"\n--- Duplicate Group ---")
        print(f"Hash: {file_hash}")
        for filepath in filepaths:
            print(f"  - {filepath}")
    print("\n--- End of Report ---")
    sys.exit(0)

if __name__ == "__main__":
    main()
